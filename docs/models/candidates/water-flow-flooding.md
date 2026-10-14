# Water flow and flooding (one model with scenarios)

| Field | Value |
|---|---|
| ID | `water-flow-flooding` |
| Longlist ref. | `WAT` = HYD-01, HYD-02, HYD-03, HYD-04, URB-02, LND-03 |
| Category | hydrology, natural hazards |
| Group | core ★ |
| Weighted score | 4.30 (revision 2, `docs/review/evaluation-matrix.md`) |
| Primary reference | `guidolin2016weighted` (WCA2D) |
| Status | draft |
| Last updated | 2026-10-14 |

**Source note.** The paper `guidolin2016weighted` is **not local** (manifest status *manual*:
OA but publisher and repository block automated download). The rule in §5 is restated from
the domain notes (`docs/research/domains/hydrology.md`, WCA2D entry) and from reading the
co-author's caflood kernels (`external/caflood`, files `outflowWCA2Dv2.ca`,
`velocityWCA2Dv1.ca`, `velocityDiffusive.ca`, `waterdepth.ca`, `CADDIES2D.cpp`,
`Setup.cpp`). The kernels carry GPL-3 headers → **reference only, clean-room** (ADR 0006);
only facts are reported here, no code. Everything must be re-checked against the paper
once it is downloaded by hand.

## 1. Phenomenon

Water on the land surface moves downhill under gravity, slowed by friction, and
accumulates in depressions, valleys and streets. Sources are rain (spatially uniform or
radar raster), river inflow (hydrograph at the domain edge), a sewer surcharge, or the
sudden release of stored water (dam / pond breach). Losses are infiltration, drains and
outflow over the domain edge. Scales: metres (urban streets) to kilometres (floodplain),
seconds to days. User questions: *where does water go and pond? how deep, how fast, when
does it arrive? what changes with a dike, a breach, more impervious surface, a heavier storm?*

Scenarios (one engine model, several rule variants and inputs):

| Scenario | Longlist | Forcing | Preferred rule variant | Benchmark |
|---|---|---|---|---|
| Surface runoff and ponding | HYD-01 | rain + infiltration | WCA2D (dynamic) or FlowFill (equilibrium) | EA Test 1, 2; FSM end state |
| River flood inundation | HYD-02 | inflow hydrograph / fixed level at edge | local inertial (or WCA2D) | EA Test 4 (data local), Test 5 |
| Flash flood | HYD-03 | intense rain raster, infiltration | WCA2D | qualitative |
| Pluvial urban flood | URB-02 | rain on DSM with buildings, drain sinks | WCA2D or MoD (liu2015) | EA Test 8A |
| Pond cascade breach | HYD-04 | initial stored water + breach intervention | local inertial (dynamic wave front) | EA Test 6A / 5 (dam break) |
| Post-mining lake filling | LND-03 | slow inflow (river + groundwater) | volume bucket + level–volume curve | none (own design) |

## 2. Suitability for CA

Excellent. Exchange is purely between adjacent cells, inputs are rasters (DEM, roughness,
infiltration classes), and the conservative two-pass scheme (edge outflows → cell update)
is exactly mass-conserving and GPU-native. `caviedesvoullieme2018cellular` (abstract only)
shows that cell-based schemes coincide with zero-inertia finite-volume solvers, which
justifies presenting the CA as numerically sound.

Not captured well: full momentum (hydraulic jumps, supercritical flow over obstacles,
EA Test 3), sub-grid features (narrow dikes, culverts, sewer network), very fast dam-break
fronts with WCA2D (to be checked against Test 6A), and long-range hydraulic effects
(backwater) are reproduced only through many small steps.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `dem` z | real (m) | terrain / DSM elevation; dams and buildings raised | static (edited by interventions) |
| `roughness` n | real (s m⁻¹ᐟ³) or class + LUT | Manning coefficient | static |
| `infiltration` | class + LUT (rate, capacity) | loss parameters | static |
| `water.depth` h | real ≥ 0 (m) | water depth; η = z + h is the water surface | dynamic |
| `water.q` | face, real (m³ per step, signed) | outflow of the current step (WCA2D) | dynamic, persistent (read next step) |
| `water.qAcc` | face, real (m³) | outflow accumulated over the velocity update period | dynamic (reset every period) |
| `water.qx`, `water.qy` | face, real (m² s⁻¹) | unit discharge (local inertial variant) | dynamic, persistent |
| `water.speed` | real ≥ 0 (m s⁻¹) | cell velocity magnitude (and direction) | derived each period |
| `water.infCum`, `water.sinkCum` | real (m) | cumulative infiltration / drain loss | dynamic (mass balance) |
| `water.maxDepth`, `water.arrival`, `water.maxSpeed` | real | observers | output |

## 4. Neighbourhood and time step

- **Grid:** square; 1–10 m for urban / small catchments, 5–50 m for floodplains (EA tests
  use 2 m, 5 m, 50 m; `neelz2010benchmarking`, `shaw2021lisflood` §3).
- **Neighbourhood:** von Neumann (WCA2D, local inertial, liu2015 MoD). Moore appears in some
  WCA implementations (`yang2024convolutional`), in Cirbus (all lower neighbours,
  `cirbus2013cellular`) and in FlowFill (D8 steepest, `callaghan2019computing`).
- **Time step:** adaptive, seconds (urban) to tens of seconds (floodplain). caflood
  recomputes Δt only every *update period* (≤ 60 s) and snaps it to Δt_max / k.
  FlowFill has no physical time (iterations to convergence).
- **Update scheme:** synchronous two-pass (outflows on edges, then depth); FlowFill
  originally sequential in order of decreasing water surface.
- **Boundaries:** open (water leaves, recorded) by default; closed for basins; fixed level
  or inflow hydrograph on edge segments (HYD-02, EA Tests 1, 4).

## 5. Transition rule

Notation: cell 0 and its four neighbours k = 1..4; z ground, h depth, η = z + h; A cell
area, Δx edge length (= cell size), Δt current step, Δt′ previous step.

### 5.1 WCA2D (primary, `guidolin2016weighted`; restated from caflood v2 kernels)

Per step:

1. **Sources / sinks** (`map`). Add rain depth r(t)·Δt to every domain cell; add inflow
   volume / A at inflow cells. Infiltration in caflood is a single global rate (mm h⁻¹)
   removed once per update period as min(h, rate·T_u) (implementation caflood,
   `CADDIES2D.cpp`); spatially varying infiltration is our extension.
2. **Outflow pass** (`flux`, part a). Skip cells with h₀ < ε_ign. For each neighbour k:
   - available level drop ΔL_k = min(η₀ − η_k, h₀);
   - if ΔL_k > ε_tol, weight w_k = ΔL_k · A_k (storage volume the neighbour can take), else
     w_k = 0;
   - w_min = smallest positive w_k; w_max = largest, at edge k*;
   - W = Σ w_k + w_min (the extra w_min is the share that **stays** in the centre cell).
   If W = 0, no outflow. Otherwise:
   - I_prev = Σ_k (positive outflow of the previous step towards k) · Δt / Δt′;
   - v* = min(20 m s⁻¹, Manning velocity (1/n) h₀^(2/3) (ΔL_k*/Δx)^(1/2));
   - V_v = v* · h₀ · Δt · Δx (volume that can cross one edge in Δt);
   - total outflow I = min( w_min + I_prev , V_v · W / w_max , h₀ · A );
   - neighbour k receives I · w_k / W, written on the shared edge.
3. **Gather pass** (`flux`, part b). h₀ ← h₀ − (Σ outflows − Σ inflows) / A.
4. **Velocity and Δt** (every update period T_u, not every step). v1: per edge with
   outflow and mean depth h̄ ≥ tol, v = (outflow accumulated over T_u)/(h̄ Δx T_u), limited
   by Manning v with R = max(η₀,η_k) − max(z₀,z_k), S = min(h̄,|Δη|)/Δx, and by the
   critical velocity √(g h̄); edge vectors are summed to a cell velocity. Next Δt =
   min(Δt_max, α Δx / v_grid,max, α Δx / v_forcing) where v_forcing is a "potential
   velocity" estimated from the coming rain / inflow events. v2 (caflood default model)
   additionally takes per cell Δt_c = (A/4) · 2n / H_f^(5/3) · √S over edges with outflow
   and S ≥ slope tolerance (H_f flow depth at the edge), capped at 60 s, and uses the
   global minimum (implementation caflood, `velocityDiffusive.ca`; resembles a diffusive
   stability limit). Finally Δt is **snapped** to Δt_max / k for the smallest integer k
   giving Δt ≤ candidate, clamped to [Δt_min, Δt_max].

Conserved: water volume exactly (outflow pass never sends more than h₀·A; each edge has
one donor per step because only the higher-η cell sends). Not conserved: momentum (only the
I_prev term carries "memory").

**Open questions (paper unread):** (a) the domain notes call I_prev "inflow of the previous
step", the kernel reads the cell's own previous **outflows** — check the paper; (b)
whether the paper's Δt formula is v1 (velocity) or v2 (diffusive) for the test cases;
(c) how α, Δt_min/max and T_u were set per test; (d) whether A_k (neighbour area) matters
on regular grids (it is constant there).

### 5.2 Variant — local inertial (`bates2010simple` via `shaw2021lisflood` Eqs. 18–19)

Face unit discharge, Arakawa-C staggering:

- q^(n+1) at face (i−½) = [ q^n − g h_f Δt (η_i − η_(i−1))/Δx ] / [ 1 + g Δt n² |q^n| / h_f^(7/3) ],
  with h_f = max(η_i, η_(i−1)) − max(z_i, z_(i−1)) (`shaw2021lisflood` Eq. 19);
- h_i^(n+1) = h_i^n + Δt/Δx · (q_in − q_out summed over the four faces) (Eq. 18);
- Δt from a Courant condition with default Courant number 0.7 (§2.3); the formula itself is
  in `bates2010simple` (not local) → open question. θ-weighted stabilisation in
  `dealmeida2012improving` (not read).
- Required for HYD-02 (Tests 4, 5) and HYD-04 (dam-break fronts). Wet / dry handling
  (h_f ≤ 0 → q = 0) and the limiter against draining a cell below zero are not in the part
  read → open question.

### 5.3 Variant — minimisation of differences (`liu2015developing` §2.4; origin `digregorio1999empirical`)

Order per step: (i) add rain; (ii) subtract infiltration (rate × Δt until a cumulative
threshold, §2.2) or inlet drainage D = w·C·√(2gh)·k / A_r (Eqs. 3–5); (iii) Manning velocity
per cell, Δt = min over cells of Δx / v (§2.4, Eq. 7); (iv) MoD distribution: average η over
the centre and the neighbours still in the set, drop neighbours above the average, repeat
until stable, then send water so that the remaining neighbours reach the common level
(steps a–e). Diagonal exchange takes two iterations. Open: how "movable water" is
defined, simultaneous exchanges, and boundaries (not stated, see domain notes). MoD
properties: `avolio2012theorem` (not local). Same machinery as SCIDDICA / SCIARA (HAZ-02,
HAZ-05).

### 5.4 Variant — FlowFill equilibrium ponding (`callaghan2019computing` §2, Figs. 2–3)

Prescribed runoff depth on every cell. Each iteration visits cells from the highest
water surface down; each sends to its steepest D8 neighbour min(available water, ½ ·
water-surface difference); water crossing the edge is lost. Stop when the change of the
maximum per-iteration move |Δh_max| (Eq. 1) stays below a threshold for a plateau of
iterations. Optional correction: take the minimum with a fully filled DEM (Priority-Flood)
to remove overfilling (breaks exact conservation slightly). A synchronous Jacobi version
for the GPU is our adaptation → open question whether it still converges without
oscillation when several donors feed one cell. Reference end state: Fill–Spill–Merge
(`barnes2021computing`).

### 5.5 Variant — Cirbus multi-direction (`cirbus2013cellular`, CZ)

All lower Moore neighbours receive water; v = h^(2/3) s^(1/2)/n with terrain slope; transfer
time T = Δx/v; moved volume h·Δx·v·Δt; Δt starts at 1 s and is halved when T > Δt;
Green–Ampt infiltration; absorbing boundary. Split among receivers not specified → open.

### 5.6 Scenario-specific rules (our design, to be reviewed)

- **HYD-04 breach:** dams as raised `dem` cells; breach = intervention lowering a crest
  segment (instant or over a duration). Cascade: a controller watches η at the next dam
  crest and triggers its breach when overtopping lasts > t_b. No CA breach-development rule
  exists in the literature found (`hydrology.md`, gaps) → assumption.
- **LND-03 lake:** years-long filling; dynamic flow is unnecessary. Lake volume V(t) from
  inflow + groundwater exchange (HYD-09); level L from the DEM level–volume curve of the
  connected pit (reduce histogram); depth = max(0, L − z) in the connected basin.
  Assumption (`atmosphere-other.md`: no CA pit-lake model found).
- **URB-02:** buildings raised by 10 m (`liu2015developing` §3) or treated as closed cells;
  inlets as sink cells.

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Manning coefficient (default) | n | s m⁻¹ᐟ³ | 0.01 | implementation caflood, file `Setup.cpp` | global default only |
| Manning, EA Test 4 | n | s m⁻¹ᐟ³ | 0.05 | `shaw2021lisflood` §3.1 | flat floodplain |
| Manning, EA Test 5 | n | s m⁻¹ᐟ³ | 0.04 | `shaw2021lisflood` §3.2 | valley dam break |
| Manning, Eden case | n | s m⁻¹ᐟ³ | 0.035 channels, 0.075 elsewhere | `shaw2021lisflood` §3.3 | rain-on-grid |
| Manning per urban class | n | s m⁻¹ᐟ³ | 0.01–0.04 | `liu2015developing` §4.1, Table 2 | calibration grid |
| Manning, Ostravice | n | s m⁻¹ᐟ³ | 0.04 | `cirbus2013cellular` (domain notes) | whole area |
| Level-drop tolerance | ε_tol | m | 0.001 | implementation caflood, `Setup.cpp` | |
| Ignore-depth threshold | ε_ign | m | 0.001 | implementation caflood, `Setup.cpp` | dry cells skipped |
| Slope tolerance | – | % | 0.1 | implementation caflood, `Setup.cpp` | divided by 100 in code |
| Velocity cap | – | m s⁻¹ | 20 | implementation caflood, `outflowWCA2Dv2.ca` | |
| Velocity update period | T_u | s | ≤ 60 | implementation caflood, `Setup.cpp` | Δt_max ≤ T_u |
| Δt factor | α | – | not given | caflood requires it in config | open question |
| Δt min / max | Δt_min, Δt_max | s | not given | – | open question |
| Courant number (local inertial) | C | – | 0.7 | `shaw2021lisflood` §2.3 | |
| Infiltration rate (grassland) | R_a | mm h⁻¹ | 5.8 or 11.7 | `liu2015developing` §4.1 | |
| Inlet drainage rate | D | mm s⁻¹ | 4.6 | `liu2015developing` §3 | from orifice eq. |
| Orifice coefficient | C | – | 0.67 | `liu2015developing` §3 | |
| Building raise | – | m | 10 | `liu2015developing` §3 | URB-02 |
| FlowFill convergence threshold | |Δh_max| | mm | 0.01 (one site) | `callaghan2019computing` §4.1 | site-specific |
| FlowFill plateau length | – | iterations | 20 000 | `callaghan2019computing` §3–4 | |
| Ostravice source depth | – | m | 0.7 over 3 cells | `cirbus2013cellular` (domain notes) | + 0.2 / 0.3 m tributaries |
| EA Test 4 domain / grid | – | m | 1000 × 2000, Δx = 5 | `shaw2021lisflood` §3.1 | 5 h, 20 m breach inflow |
| EA Test 5 peak inflow | – | m³ s⁻¹ | 3000 | `shaw2021lisflood` §3.2 | 30 h |
| EA Test 8A rain peak | – | mm h⁻¹ | 400 over 3 min; point source 5 m³ s⁻¹ | `neelz2010benchmarking` §4.7.8 | 2 m grid |
| WCA2D test-case values | – | – | not given | paper unread | open question |

## 6. Deterministic vs. stochastic

Deterministic. Randomness only in optional ensembles over uncertain inputs (rain
intensity, breach time, roughness class values) → probability of inundation; no RNG
inside the rule.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| DTM / DSM | raster, continuous | terrain, buildings | required |
| Land cover / imperviousness | raster, categorical | roughness and infiltration via LUT | optional |
| Soil hydrologic class | raster / vector, categorical | infiltration parameters | optional |
| Rainfall | scalar series or raster series | source | scenario |
| Inflow hydrograph / water level | time series at edge segment | boundary source | HYD-02 |
| River network, dams, inlets | vector | rasterised barriers, breach segments, sinks | optional |
| Flood-zone polygons | vector | validation | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| DTM / DSM | ČÚZK DMR 5G, DMP 1G; Copernicus DEM / EU-DEM | CZ / EU | to be verified (licence, access) |
| Land cover | CORINE Land Cover, Urban Atlas, ZABAGED | EU / CZ | to be verified |
| Imperviousness | Copernicus HRL Imperviousness | EU | to be verified |
| Soils | VÚMOP BPEJ / soil maps; ESDAC | CZ / EU | to be verified |
| Rain | ČHMÚ radar and gauge data | CZ | to be verified (licence) |
| River network, water bodies, ponds | DIBAVOD (VÚV TGM), ZABAGED | CZ | to be verified |
| Flood zones | official CZ flood-zone maps (záplavová území), EU Floods Directive maps | CZ / EU | to be verified |
| Gauge hydrographs | ČHMÚ / state river authorities (Povodí) | CZ | to be verified |

## 9. Visualization

Animated depth over hillshade (blue ramp, transparent below 1–5 cm), velocity arrows or
streak lines, maximum-depth and arrival-time maps, hydrographs at clicked points, rain
and volume-balance chart. Interactions: rain intensity / duration slider, draw a dike
(raise cells), breach a dam, add pump / inlet, toggle buildings. Scenario comparison
(before / after an intervention) as difference map.

## 10. Validation options

EA benchmark (`neelz2010benchmarking`): Tests 1–2 (ponding), 4–5 (propagation), 6A (dam
break), 8A (urban rain + point source); Test 4 inputs and LISFLOOD-FP ACC outputs are
local (`data/reference/ea-benchmark-lisflood-fp8`). Steady ponding vs Fill–Spill–Merge /
Priority-Flood end state. CZ: Ostravice water levels (`cirbus2013cellular`, 11 surveyed
points). Official flood zones (qualitative extent comparison, SC-METRICS). Mass-balance
error as a built-in check.

## 11. Links to other models

Feeds HYD-05 erosion (submodel reading depth and outflows), MOV-01 / MOV-03 (flooded roads
as barriers, chain L12), LND-03 (lake), HYD-04 → HYD-02 (chain L5). Fed by HAZ-01
(burnt area → higher runoff, chain L1), LND-01 (imperviousness, L8), HYD-09 (groundwater
exchange), HYD-06 (snowmelt, L6). Shares `flux` machinery with ATM-02 cold air, EPI-04
emigration, HAZ-02 SCIDDICA, HAZ-05 SCIARA, HYD-09.

## 11a. Engine mapping

- **Stages (WCA2D), per step:**
  1. `map` sources / sinks — rain (Forcing, scalar or raster) × Δt, point inflow, drains,
     infiltration (capped by depth and remaining capacity); losses added to cumulative
     layers.
  2. `flux` (a) outflow pass → face layer `water.q` (signed; reads `water.depth`, `dem`,
     `roughness`, previous `water.q`, Δt, Δt′); (b) gather → `water.depth`.
  3. every T_u: `map` accumulate `water.qAcc` → `water.speed` and per-cell Δt candidate
     (scratch); `reduce` min Δt candidate, max speed.
  4. `reduce` total volume, boundary outflow (every step or every output time).
- **Stages (local inertial):** `flux` (a) face update of `water.qx/qy` (persistent state);
  (b) gather → depth; `reduce` max depth → Courant Δt.
- **Stages (FlowFill):** `flux` with D8 slot output and `converge` policy (GPU Jacobi) or
  `queue` ordered sweeps (CPU, original order).
- **Stages (LND-03):** `reduce` histogram of z in the pit mask + controller converting
  volume to level; `map` depth = max(0, L − z).
- **Time policy:** `adaptive` with (i) recomputation period T_u, (ii) snapping Δt =
  Δt_max / k, (iii) a forcing-aware limit (potential velocity of upcoming events),
  (iv) Δt′ kept for the I_prev scaling. `converge` for FlowFill; `fixed` (large Δt) for
  LND-03.
- **Boundaries:** `open` (outflow recorded; caflood keeps it in ghost cells instead),
  `closed`, `fixed(level)` and `flux(hydrograph)` on edge segments; NoData as wall or
  sink selectable.
- **RNG:** none (ensembles only).
- **Observers:** max depth, max speed, arrival time (h > threshold), hydrograph points,
  mass balance (SC-MASS), hazard rating h·(v + c) (`TODO(literature)` for the formula).
- **Interventions:** raise / lower cells (dike, dam, breach), rain change, add source /
  sink, toggle building mask.
- **Shared components:** SC-GRID, SC-LUT, SC-FACE, SC-SLOT (MoD / Moore / D8 variants),
  SC-SLOPE, SC-D8, SC-FILL, SC-RASTERIZE, SC-RECLASS, SC-OUTFLOW, SC-INERTIAL, SC-ADT,
  SC-SRC, SC-BOUNDARY, SC-ARRIVAL, SC-ENVELOPE, SC-MASS, SC-ENSEMBLE, SC-METRICS,
  SC-BENCH, SC-INTERV, SC-QUEUE (FlowFill CPU order, Priority-Flood).
- **Model-specific:** WCA2D weight formula with retained share and I_prev term, the
  velocity / Δt formulas, breach controller, lake level–volume bucket.
- **Corrections to `model-mapping.md`:** (1) WCA2D outflows fit a **face** layer (one donor
  per edge per step), not necessarily a slot layer; slot is needed only for Moore / D8 /
  MoD-with-diagonals variants. (2) The outflow layer is **persistent state** read in the
  next step (I_prev), not scratch. (3) Δt is recomputed every update period from an
  accumulated-flux velocity pass, not from a `reduce` at the start of every step.
  (4) Infiltration in caflood runs once per update period. (5) LND-03 needs a
  histogram `reduce` + connected-basin mask, not the flux stages.

## 12. Complexity estimate

- **Implementation:** medium — WCA2D kernel is short, but Δt logic, boundaries, mass
  accounting and three variants add up.
- **Computation:** medium–high — 10⁶ cells × 10⁴–10⁵ steps needs WebGPU; CPU fine for
  10⁵ cells; active-tile skipping of dry areas helps (`cirbus2013cellular` elevation mask).
- **Data preparation:** medium — DEM resampling, building burn-in, LUTs, hydrographs.

## 13. Risks

Scientific: WCA2D weak for dynamic waves (HYD-04) — check with Test 6A; results depend on
DEM resampling (`neelz2010benchmarking` §4.7.9 notes 0.05–0.2 m differences). Data:
dam heights and pond outlets not open (HYD-04). Technical: tiny Δt in steep / deep cells
throttles the whole grid. Communication: a demo is not a flood forecast; show disclaimer
and benchmark status.

## 14. Open questions

- WCA2D paper values (n, α, Δt bounds, T_u per test) and whether I_prev is outflow or inflow.
- Default rule for HYD-02: WCA2D (cheaper) or local inertial (better on Tests 4–5)?
- Local-inertial Δt formula and wet/dry handling (`bates2010simple` not local).
- FlowFill synchronous variant: convergence and oscillation with several donors.
- Open boundary: remove water or keep it in ghost cells (caflood) for accounting?
- Breach development rule (HYD-04) and pond data availability.
- Should infiltration be per step or per period; Green–Ampt / Philip vs constant rate?

## 15. Literature and implementations

- **Primary reference:** `guidolin2016weighted` — standard fast flood CA, open kernels, EA tests
  (paper not local).
- **Supporting:** `bates2010simple`, `shaw2021lisflood` (local inertial; Eqs. 18–19),
  `dealmeida2012improving` (stabilisation); `callaghan2019computing` (FlowFill);
  `barnes2021computing` (FSM end state), `barnes2014priority`, `planchon2002fast`
  (filling); `liu2015developing` (MoD + rain / infiltration / drains);
  `digregorio1999empirical`, `avolio2012theorem` (MoD origin / theory, not local);
  `cirbus2013cellular`, `landa2019smoderp2d` (CZ); `caviedesvoullieme2018cellular`
  (CA ≈ FV); `ghimire2012formulation` (CA2D predecessor); `wijaya2023rapid` (coarse +
  fine downscaling).
- **Benchmarks:** `neelz2010benchmarking`, `hunter2008benchmarking`;
  `data/reference/ea-benchmark-lisflood-fp8` (Test 4, CC BY 4.0).
- **Implementations:** caflood (AlbertChenExeter/caflood; LICENSE MIT but kernel headers
  GPL-3 ⚠ → reference only); WaterDesk/caflood (MIT, reusable after review);
  LISFLOOD-FP 8.x (GPL-2.0 → oracle); FlowFill (GPL-3.0 → reference); Fill–Spill–Merge
  (MIT → reusable) / RichDEM (GPL-3.0 → reference); GRASS r.sim.water (GPL → oracle);
  WebFlood (MIT, WebGL pattern), lisyarus webgpu-shallow-water (MIT, WGSL pattern).
- **Still missing:** WCA2D paper (manual download); Bates 2010 Δt formula;
  `TODO(literature)` flood hazard rating formula; breach-development literature.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| water flow and flooding | proudění vody a povodně | phenomenon |
| surface runoff and ponding | povrchový odtok a zadržení v bezodtokých depresích | scenario |
| water depth | hloubka vody | state variable |
| water surface elevation | výška hladiny | state variable |
| outflow | odtok (z buňky) | state variable |
| unit discharge | měrný průtok | state variable |
| Manning roughness coefficient | Manningův součinitel drsnosti | parameter |
| infiltration rate | intenzita infiltrace (vsaku) | parameter |
| inflow hydrograph | přítokový hydrogram | input |
| storm drain inlet | uliční vpusť | input |
| adaptive time step | adaptivní časový krok | engine |
| maximum depth map | mapa maximálních hloubek | output |
| draw a dike / breach a dam | nakreslit hráz / protrhnout hráz | UI action |
