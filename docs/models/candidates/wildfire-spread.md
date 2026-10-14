# Wildfire spread

| Field | Value |
|---|---|
| ID | `wildfire-spread` |
| Longlist ref. | `HAZ-01` (+ scenario `URB-03` urban fire) |
| Category | natural hazards (fire) |
| Group | core ★ |
| Weighted score | 4.65 (revision 2) |
| Primary reference | `alexandridis2008cellular` (rule read from the full-text restatements `xia2025pytorchfire` and `freire2019using`; the original paper is not local, manifest status *manual*) |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

A vegetation fire spreads from burning fuel to neighbouring unburnt fuel. Spread is faster
and more likely in dry, dense, flammable vegetation, uphill and downwind; it slows on
downhill and upwind flanks and stops at non-burnable ground (water, rock, roads, built-up
land). In strong wind, embers lifted by the plume start spot fires ahead of the front.
Scales: cells of 5–100 m, steps of minutes to an hour, events of hours to days, areas up
to tens of km². Demo questions: where will the fire be in 6 h, which places are most
likely to burn, how much does a firebreak or a wind shift change that? CZ case: the
2022 Bohemian Switzerland fire (> 1000 ha, mostly bark-beetle-killed spruce,
`kudlackova2024using`).

## 2. Suitability for CA

Excellent: ignition is a local contagion between adjacent cells, and all drivers (fuel,
density, terrain, wind) are rasters. Limits: a Moore lattice distorts fire shapes
(octagons; anisotropy, `ghisu2015optimal`), the probability rule has no physical rate of
spread (time per step must be calibrated), spotting is non-local, and fire–atmosphere
coupling is absent. Fire behaviour (intensity, crown fire) is not modelled.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `fire.state` | categorical {non-burnable, unburnt, burning, burnt} | fire state (4 states in `freire2019using` §2.3; 3 in `xia2025pytorchfire`, where non-burnable = p_veg giving zero probability) | dynamic |
| `fuel` | categorical (vegetation type) | → p_veg via LUT | static input |
| `density` | categorical (vegetation density) | → p_den via LUT | static input |
| `dem` | real (m) | elevation | static input |
| `fire.dzSlot` | real per neighbour slot | slope angle towards each neighbour | static derived |
| wind | vector (speed m s⁻¹, direction) | global or per cell, may change in time | forcing |
| `fire.arrival` | real (step / h) | first ignition time | output |
| `fire.timer` | integer | steps since ignition (variants with burn duration, URB-03) | dynamic |

## 4. Neighbourhood and time step

- **Grid:** square; 20–100 m for landscapes (100 m `freire2019using`, 30 m
  `xia2025pytorchfire`, 20 m `trucchia2020propagator`), 3 m for URB-03 (`tan2019fire`).
- **Neighbourhood:** Moore (8 slots). Variants: firebrand jumps, wind-driven ray (N2 rule),
  wind-dependent radius for URB-03.
- **Time step:** abstract; real duration is calibrated (≈ 20 min in `freire2019using` §2.5;
  0.8 or 1.6 h in `xia2025pytorchfire` §3).
- **Update scheme:** synchronous (all burning neighbours read from the previous state).
- **Boundary:** closed — no fire enters or leaves; `xia2025pytorchfire` (App. A) pads the
  domain by 4980 m to avoid edge effects.

## 5. Transition rule

Restated from `freire2019using` §2.3 (Eqs. 1–4) and `xia2025pytorchfire` §2.2 (Eqs. 2–4, 9).
For each step t → t+1, every cell reads the previous state:

1. A non-burnable cell stays non-burnable; a burnt cell stays burnt (Rules 1, 3).
2. A burning cell becomes burnt (Rule 2: burning lasts exactly one step).
3. An unburnt cell *i* with at least one burning Moore neighbour *j* can ignite. For each
   burning neighbour the pair probability is
   `p_ij = p_h · (1 + p_veg,i) · (1 + p_den,i) · p_w,ij · p_s,ij`
   (`freire2019using` Eq. 1; `xia2025pytorchfire` Eq. 2). Vegetation factors are those of
   the cell being ignited (the target) — explicit in the PyTorchFire implementation
   (`external/PyTorchFire`, file `pytorchfire/model.py`), implicit in Freire.
4. Wind factor: `p_w,ij = exp(c1·V) · exp(c2·V·(cos θ_ij − 1))`, with V the wind speed and
   θ_ij the angle between the wind (blowing towards) and the direction from *j* to *i*
   (`freire2019using` Eq. 2; `xia2025pytorchfire` Eq. 3).
5. Slope factor: `p_s,ij = exp(a · θ_s,ij)`, `θ_s,ij = atan((E_i − E_j) / D_ij)`, with
   D = L for edge neighbours and √2·L for diagonals (`freire2019using` Eqs. 3–4; the
   extracted text prints the diagonal distance garbled, `xia2025pytorchfire` Eq. 1 uses
   √2·L). Uphill (E_i > E_j) increases the probability.
6. Combination over burning neighbours (independent attempts):
   `P_i = 1 − Π_j (1 − p_ij)` (`xia2025pytorchfire` Eq. 9). The original applies one
   Bernoulli trial per burning neighbour (`freire2019using` Rule 4); a single draw
   u < P_i per cell gives the same distribution and is preferred on the GPU.
7. Nothing is conserved. Fuel is consumed implicitly (burnt is absorbing).

**Open questions on the primary rule:** (a) how p_ij > 1 is handled in the original
(clamp to 1?) — PyTorchFire squashes it with `tanh(c·p)` (Eq. 5, c = 1.1486328125);
(b) whether slope uses degrees or radians (PyTorchFire: degrees, Eq. 4); (c) whether wind
direction is "from" or "towards" (PyTorchFire: towards, counter-clockwise from East);
(d) the PyTorchFire implementation indexes the slope of the *target cell towards its own
neighbour in the propagation direction* (one cell further), not from source to target
(`pytorchfire/model.py` + `pytorchfire/utils.py`, `calculate_slope`) — we will use the
source→target difference of Eq. 4.

### 5.1 Variant: burn duration (`xia2025pytorchfire`)

A burning cell stays burning with probability p_continue each step, else becomes burnt
(geometric burning duration; §2.2, after Li). Set p_continue = 0 to recover the original.

### 5.2 Variant: wind-driven ray, rule N2 (`freire2019using` §2.4)

After the N1 step, for each new ignition from burning cell *j*: if V_j > 8 m s⁻¹ and the
angle between wind and displacement < π/10, a number of further cells along the
displacement direction ignite as well; the number grows with V_j. **Open:** the count as a
function of V is only in Fig. 5 (not in the text); whether the extra cells need fuel /
pass a probability test is not stated.

### 5.3 Variant: cumulative-binomial direction weights (`hargrove2000simulating`, `trucchia2020propagator`)

Directional effects enter as an exponent: `p_ij = 1 − (1 − p_n)^{b_ij}`.
EMBYR: p_n = I from a fuel-to-fuel × moisture table (Table 1), b_ij from a wind-class bias
rose (Fig. 2), each neighbour tried independently, burning lasts one step (§2.4, step
list end of §2.5). PROPAGATOR: p_n from a 6 × 6 burning-fuel × target-fuel matrix
(Table 1), exponent α_wh = α_w · α_h (Eq. 2, curves in Figs. 7–8), times a moisture factor
e_m (Eq. 1). The exponent form keeps p ≤ 1 without clamping.

### 5.4 Variant: event-driven timing (`trucchia2020propagator` §2)

Each successful ignition is scheduled at t + d / (v_n · K_w · K_φ · f_m)
(Eqs. 3–6) in a priority queue; wind speed and direction are perturbed per step. Same
probability rule, real-time isochrones. EUPL code → reference only.

### 5.5 Variant: progress accumulator (`pais2021cell2fire` §2.2)

Each burning cell adds ROS_ij · Δt to a per-neighbour progress; the neighbour ignites when
progress reaches the centre-to-centre distance (head / flank / back ROS from an ellipse,
Canadian FBP). Deterministic apart from optional ROS noise (cvROS). GPL → reference only.

### 5.6 Variant: spotting (`hargrove2000simulating` §2.5, `lopezdecastro2024firespotting` §2.2)

Each burning cell emits firebrands (EMBYR: fixed count per fuel type, Table 2;
Alexandridis-type: Poisson count, §3). Landing distance: negative exponential (EMBYR),
`d = r_n · exp(c·V·(cos θ − 1))`-type with normal r_n and uniform θ (Alexandridis 2011
as restated, Eq. 3), or lognormal (Perryman, RandomFront). Direction: random at calm,
downwind with 3° normal spread otherwise (EMBYR). A brand landing on unburnt fuel ignites
with a fuel/moisture probability (EMBYR Table 2) or `p0·(1+p_veg)…` capped at 1
(Eq. 4). **Open:** the Poisson mean is not given in `lopezdecastro2024firespotting`.

### 5.7 Scenario URB-03: urban fire (`tan2019fire`, after `ohgai2007cellular`; neither local — domain notes)

3 m cells, states {no structure, burnable, ignited, burning, burnt out}; ignited → burning
after t1, burning → burnt after t2 (timers). Ignition probability `a · B · H(t) · W`:
material factor B, heat curve H of the burning duration, downwind-cone bias W; the reach
is a wind-dependent von Neumann radius D = 1.15(5 + 0.5v). **Open:** H(t) and W are not
legible in the extracted text; how several burning neighbours combine is not stated
(proposal: the same 1 − Π rule).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| base spread probability | p_h | – | 0.58 | `freire2019using` §2.5 (quoting Alexandridis 2008) | PyTorchFire default 0.3 (impl. PyTorchFire, `pytorchfire/model.py`) |
| slope coefficient | a | deg⁻¹ | 0.078 | `freire2019using` §2.5 | unit assumed degrees (open) |
| wind coefficient (speed) | c1 | s m⁻¹ | 0.045 | `freire2019using` §2.5, Fig. 6 | sensitivity in Fig. 6 |
| wind coefficient (direction) | c2 | s m⁻¹ | 0.131 | `freire2019using` §2.5, Fig. 6 | |
| p_veg: no vegetation / agriculture / forest / shrubland | p_veg | – | −1 / −0.4 / 0.4 / 0.4 | `freire2019using` Table 1 | forest and shrubland read as equal from extracted text — verify on PDF |
| p_den: none / sparse / normal / dense | p_den | – | −1 / −0.3 / 0 / 0.3 | `freire2019using` Table 1 | |
| roads (primary / secondary / tertiary), waterlines | p_veg = p_den | – | −0.8 / −0.7 / −0.4; −0.4 | `freire2019using` §2.2 | firebreak demo |
| N2 wind threshold / max angle | – | m s⁻¹ / rad | 8 / π/10 | `freire2019using` §2.4 | cell count: Fig. 5 only |
| cell size | L | m | 100; 30; 20 | `freire2019using` §2.5; `xia2025pytorchfire` §3; `trucchia2020propagator` §2 | |
| step duration | Δt | h | ≈ 0.33; 0.8 / 1.6 | `freire2019using` §2.5; `xia2025pytorchfire` §3 | calibrated, not physical |
| ensemble size | – | runs | 100 | `freire2019using` §2.5; `trucchia2020propagator` §2 | |
| squash constant | c | – | 1.1486328125 | `xia2025pytorchfire` Eqs. 5, 8 | variant only |
| continue-burning probability | p_continue | – | 0.4–0.6 (experiments); default 0.3 | `xia2025pytorchfire` §3; impl. PyTorchFire, `pytorchfire/model.py` | 0 = original rule |
| calibration bounds a, c1, c2 / p_h | – | – | [0, 1] / [0.2, 1] | `xia2025pytorchfire` Algorithm 1 | |
| p_veg / p_den from canopy cover / bulk density | – | – | rescaled to [−0.4, 0, 0.35] / [−0.2, 0, 0.4] (min, mean, max) | impl. PyTorchFire, `pytorchfire/firedataforge.py` | continuous alternative to LUT |
| EMBYR critical spread probability | i_c | – | ≈ 0.25 | `hargrove2000simulating` (results; 8-neighbour bond percolation) | unit test |
| EMBYR downwind bias (moderate / strong wind) | b | – | 2 / 3 | `hargrove2000simulating` §2.4 | other directions: Fig. 2 only |
| EMBYR brand mean distance (3 wind classes) | – | m | 150 / 250 / 300 | `hargrove2000simulating` §2.5 | 50 m cells |
| EMBYR brand direction spread | – | deg | 3 (normal) | `hargrove2000simulating` §2.5 | |
| EMBYR brands per cell / ignition prob. | – | –/– | per fuel class; 0.001–0.1 | `hargrove2000simulating` Table 2 | |
| PROPAGATOR nominal p_n / v_n | p_n / v_n | – / m min⁻¹ | 0.075–0.475 / 60–200 | `trucchia2020propagator` Table 1 | 6 classes |
| PROPAGATOR ROS factors | K_w, K_φ | – | exp(0.1783 V), exp(3.533 (tan φ)^1.2) | `trucchia2020propagator` Eqs. 5–6 | |
| PROPAGATOR moisture | M_x, c | –, – | 0.3; f_m = exp(−0.014 M) | `trucchia2020propagator` §2, Eq. 4 | |
| PROPAGATOR wind noise | – | – | speed × U[0.8, 1.2], dir + U[−11.25°, 11.25°] | `trucchia2020propagator` §2 | |
| spotting (Alexandridis-type) wind parameter / p0 / fuel factor | – | – | 0.191 / 0.6 / 0.4 | `lopezdecastro2024firespotting` Table 1 (from Alexandridis 2011) | |
| URB-03 cell, timers, material factor | – | m, min, – | 3; t1 = 4, t2 = 10; cement 0.01, metal 0.2, wood/plastic 1, mixed 0.7 | `tan2019fire` (via `docs/research/domains/fire.md`; not read locally) | to be verified on full text |

## 6. Deterministic vs. stochastic

Ignition is a Bernoulli event per cell and step; spotting, N2 ray and burn duration
(variant) are stochastic too. Randomness stands for unresolved fuel, gusts and fire
behaviour. One run is one possible fire, so the demo shows ensembles (≥ 100 runs) as a
burn-probability map; fixed seeds are needed for replay and for teaching ("same seed,
different wind").

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| fuel / vegetation type | raster, categorical | p_veg via LUT | required |
| vegetation density | raster, categorical or continuous | p_den | required (default 0) |
| DEM | raster, continuous | slope per slot | required |
| wind | scalar series or raster series | p_w | optional (calm default) |
| roads, waterways | vector → raster | negative loadings, firebreaks | optional |
| ignition points | vector / click | initial burning cells | required |
| fuel moisture | scalar / raster | PROPAGATOR variant | optional |
| buildings + material (URB-03) | vector → raster | fuel classes | URB-03 |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| vegetation type | CORINE Land Cover; Copernicus HRL Dominant Leaf Type / Forest Type | EU | to be verified |
| density | Copernicus HRL Tree Cover Density | EU | to be verified |
| forest stands (species, age) | ÚHÚL forest maps / management plans | CZ | to be verified (licence) |
| DEM | ČÚZK DMR 5G / 4G; Copernicus DEM | CZ / EU | to be verified |
| wind | ERA5 / ERA5-Land; ČHMÚ stations | global / CZ | to be verified |
| roads, rivers | OSM; ZABAGED; DIBAVOD | CZ | to be verified |
| burnt areas (validation) | EFFIS burnt areas; Bohemian Switzerland 2022 perimeter (NP authority) | EU / CZ | to be verified |
| buildings, material (URB-03) | RÚIAN / ZABAGED footprints; OSM building tags | CZ | material attribute to be verified |

## 9. Visualization

Animated state map over hillshade (unburnt / burning / burnt), arrival-time isochrones,
burn-probability map from the ensemble, burnt area vs. time chart. Interactions: click to
ignite, draw a firebreak, rotate / strengthen the wind, toggle spotting, compare two
scenarios side by side (e.g. dead vs. healthy spruce fuel, after `kudlackova2024using`).

## 10. Validation options

Burnt perimeter overlap (Jaccard, Sørensen) and arrival-time bias / RMSD against hot spots
(`freire2019using` §3: bias 8.3 h → −4.4 h, RMSD 12.9 h → 7.1 h with N2); calibrated
Jaccard 0.73–0.91 on simulated targets (`xia2025pytorchfire` §3, results tables). Unit tests:
EMBYR critical threshold ≈ 0.25 and its homogeneous-landscape tables
(`hargrove2000simulating` Tables 3–4). CZ: reproduce the 2022 Bohemian Switzerland
perimeter qualitatively (`kudlackova2024using`, 5 m FlamMap inputs, not CA).

## 11. Links to other models

Consumes ECO-01 dead-spruce maps as fuel (chain L2), LND land cover (L9). Feeds ATM-01 smoke
(L11), HYD-05 erosion on burnt slopes (L1), MOV-01 / MOV-03 evacuation (L12), ECO-02
succession (L4). Shared: SC-GRID, SC-LUT, SC-RECLASS, SC-SLOPE, SC-SLOT, SC-DIRWEIGHT,
SC-STOCH-SPREAD, SC-LDD, SC-QUEUE, SC-INTERV, SC-BOUNDARY, SC-ARRIVAL, SC-ENSEMBLE,
SC-METRICS, SC-CALIB, SC-RNG, SC-RASTERIZE.

## 11a. Engine mapping

- **Init:** SC-RECLASS fuel / density → p_veg, p_den (SC-LUT); derived slot layer
  `fire.dzSlot` = atan(ΔE/D) per slot (needs SC-DIRSLOPE, see below); rasterise roads /
  waterways (SC-RASTERIZE).
- **Stages per step:**
  1. `map` (optional) — per-step wind perturbation (PROPAGATOR variant), timers.
  2. `stencil` Moore — one kernel computes the next `fire.state` from the previous one:
     ignition of unburnt cells via p_ij and 1 − Π(1 − p_ij) with one uniform draw
     (SC-STOCH-SPREAD), slot weights from wind (SC-DIRWEIGHT) and `fire.dzSlot`; burning →
     burnt (always, or with 1 − p_continue). Doing both in one stage avoids a second pass
     that would see newly ignited cells.
  3. `jump` (optional) — spotting (SC-LDD), target mask = burnable cells.
  4. `reduce` — count burning (stop controller), burnt area.
- **Time policy:** fixed (calibrated Δt); `event` with `queue` for the PROPAGATOR variant.
- **Boundaries:** closed; optional padding.
- **RNG:** ≤ 2 uniforms per cell per step (ignite, burn-out); per burning cell Poisson
  count + per-brand distance / angle / ignition draws (keyed by brand id).
- **Observers:** SC-ARRIVAL, burnt area series, SC-ENSEMBLE burn probability.
- **Interventions:** ignite, firebreak (set non-burnable), change wind, water line
  (moisture, PROPAGATOR variant).
- **Model-specific:** the Alexandridis factor product, tanh squash, N2 ray, URB-03 timers
  and heat curve.
- **Corrections to `model-mapping.md`:** (1) a single `slope` derived layer is not enough:
  the rule needs a per-slot elevation difference (slot layer); (2) the planned separate
  `map` burning → burnt must read the *previous* state (or be merged into the stencil);
  (3) directional weights are used as multipliers (Alexandridis) **or exponents**
  (EMBYR / PROPAGATOR), so `Neighbourhood.directional` must hand per-slot weights to the
  kernel instead of applying them itself; (4) the N2 rule is a deterministic ray, not a
  random `jump`; (5) the Cell2Fire variant needs a stencil that reads the neighbour's
  slot value for the reverse slot (progress towards me), not a plain stencil; (6) URB-03
  needs a radius that changes with the wind forcing and per-cell timers.

## 12. Complexity estimate

- **Implementation:** low (base rule), medium with spotting / event variant.
- **Computation in the browser:** low per run (one stencil per step on 10⁶ cells);
  medium for 100-run ensembles (GPU or workers).
- **Data preparation:** medium — fuel loadings for CZ classes must be assigned and
  justified (no CZ calibration of the CA exists).

## 13. Risks

Loadings for CZ fuels are assumptions; step duration is calibrated, so users may read
times literally; lattice anisotropy produces octagonal fires; users may mistake the demo
for a fire-behaviour forecast. URB-03 material data probably not open.

## 14. Open questions

- Handling of p_ij > 1 in the original (clamp vs. tanh); units of θ_s.
- Forest vs. shrubland loading in `freire2019using` Table 1 (both 0.4 in extracted text).
- N2 rule: cell count vs. wind speed (Fig. 5) and whether extra cells need fuel.
- Spotting Poisson mean for the Alexandridis-type scheme.
- URB-03: H(t), W and multi-neighbour combination (`tan2019fire` full text not local).
- Anisotropy correction factors (`ghisu2015optimal`, `ghisu2015improved` — not local).
- Original Alexandridis paper unread (manual download needed).
- CZ fuel-class mapping and loadings (CLC / HRL / ÚHÚL → p_veg, p_den).

## 15. Literature and implementations

- **Primary reference:** `alexandridis2008cellular` — the simplest geographic fire CA,
  restated in two full texts with the full parameter set.
- **Supporting references:** `xia2025pytorchfire` (modern restatement, tanh, p_continue,
  calibration); `freire2019using` (parameters, CORINE-based loadings, N2 rule, ensembles);
  `trucchia2020propagator` (cumulative-binomial rule, event timing); `pais2021cell2fire`
  (progress accumulator); `hargrove2000simulating` (firebrands, test tables);
  `lopezdecastro2024firespotting` (spotting schemes); `ghisu2015optimal`,
  `ghisu2015improved` (anisotropy, not local); `tan2019fire`, `ohgai2007cellular`
  (URB-03, not local); `kudlackova2024using` (CZ case).
- **Benchmarks / reference data:** EMBYR homogeneous tables; PyTorchFire Bear 2020
  example; PROPAGATOR example DEM/fuel; Cell2Fire landscapes.
- **Implementations:** PyTorchFire (MIT) — reusable code with notice; PROPAGATOR
  `propagator_sim` (EUPL-1.2) — reference / oracle only; Cell2Fire (GPL-3.0) — reference /
  oracle only; manoe/wildfire_ca (BSD-2-Clause) — reusable; FireDynamicsAutomata (GPL-3.0)
  — reference only.
- **Still missing:** `TODO(literature)` original Alexandridis 2008 and 2011 full texts;
  Ghisu correction tables; Tan / Ohgai full texts; CZ fuel loadings.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| wildfire | požár v přírodě (lesní požár) | phenomenon |
| urban fire | požár v zástavbě | phenomenon |
| unburnt / burning / burnt / non-burnable | nezasažený / hořící / vyhořelý / nehořlavý | state variable |
| fuel (vegetation) type | typ paliva (vegetace) | parameter |
| vegetation density | hustota vegetace | parameter |
| base spread probability | základní pravděpodobnost šíření | parameter |
| wind speed / direction | rychlost / směr větru | parameter |
| slope | sklon svahu | parameter |
| fire spotting | přeskok požáru (vznik sekundárních ohnisek) | parameter / process |
| firebrand (ember) | letící žhavá částice | process |
| firebreak | protipožární průsek | UI action |
| ignite | zapálit | UI action |
| burn-probability map | mapa pravděpodobnosti vyhoření | UI output |
| isochrone | izochrona (čára stejného času příchodu) | UI output |
