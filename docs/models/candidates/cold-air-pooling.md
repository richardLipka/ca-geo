# Cold-air pooling and frost hollows

| Field | Value |
|---|---|
| ID | `cold-air-pooling` |
| Longlist ref. | `ATM-02` (scenario: urban ventilation corridors) |
| Category | atmosphere / local climate |
| Group | core |
| Weighted score | 4.05 (revision 2) |
| Primary reference | `nowatschin2006gpubased` |
| Status | draft |
| Last updated | 2026-10-14 |

> **Source note.** The primary reference is **not available locally** (`literature/manifest.md`:
> status `manual`, ACM, no OA copy). Its rule is restated from the round-2 notes in
> `docs/research/domains/atmosphere-other.md` (which say a free Univ. Siegen copy was read
> at that time). Every statement attributed to `nowatschin2006gpubased` below is
> therefore second-hand and must be checked against the full text (Q1). The open,
> readable reference implementation is the SAGA tool `conrad2020coldairflow` (GPL,
> reference / oracle only, ADR 0006); facts from it are cited as
> "implementation SAGA, file `saga-gis/src/tools/simulation/sim_air_flow/cold_air_flow.cpp`".

## 1. Phenomenon

On clear, calm nights the ground loses heat by long-wave radiation; the air in contact
with it cools, becomes denser than the air above and drains downslope as a shallow
gravity current (katabatic or drainage flow). It collects in valleys, basins and closed
depressions (frost hollows), where minimum temperatures can be many degrees lower than on
nearby slopes or ridges. Land cover controls both the production of cold air (open fields
and meadows produce much, forests and sealed surfaces little or none) and the resistance
to its flow (buildings, forest edges, embankments act as dams).

Scales: grid 5–100 m, domains of a few to a few tens of km, one night (4–10 h).
Questions a user wants answered: *Where does cold air collect? How deep is the pool
after n hours? Which slopes feed my town or orchard? Does a new building block, dam or
tree row cut off a ventilation corridor?* Czech relevance: frost hollows (Šumava bogs,
karst depressions — `dobos2025terrainbased` shows the method on a Hungarian karst
sinkhole), valley towns cooled by night drainage (`uiboupin2025how`: Plauen, ~20 km from
the CZ border).

## 2. Suitability for CA

Good. The models found are explicit local grid updates of a layer thickness moved
downslope by gravity — the same structure as the water models (WAT): a cell exchanges
air only with its 4 or 8 neighbours, depending on the difference of the *effective
surface* (terrain + cold-air height). Inputs are rasters (DEM, land cover). None of the
sources calls itself a CA (`docs/research/catalogue.md`: "CA-like grid models").

A CA cannot capture well: the vertical temperature structure (inversion profile), the
interaction with the ambient (synoptic) wind and turbulent mixing at the top of the
layer, radiation geometry (sky-view factor), momentum (overshooting, run-up on
counter-slopes) unless a momentum variant is used (KLAM-like, `sievers2016cold`), and the
heat budget (temperature itself is not a state in the simple model).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `dem` | real (m) | terrain or surface (DSM with buildings for the urban scenario) elevation | static input |
| `landuse` | categorical {field, meadow, vineyard, forest, settlement, …} | class → production, resistance | static input (editable by intervention) |
| `cold.k` | real ≥ 0 (m) | cold-air layer height | dynamic |
| `cold.v` | real (face, staggered) | face "velocity" / exchange coefficient between 4-neighbours (Nowatschin) | dynamic, scratch |
| `cold.out` | real ≥ 0 (slot, 8) | outflow to each neighbour (SAGA variant) | dynamic, scratch |
| `cold.speed` | real ≥ 0 (m h⁻¹) | gravity-current speed (SAGA variant) | dynamic, output |
| `cold.E`, `cold.u` | real | heat deficit, face momentum (KLAM-like variant only) | dynamic |
| `cold.maxK`, `cold.arrival` | real | maximum height, first arrival time | output |

## 4. Neighbourhood and time step

- **Grid:** square; 5–50 m for towns and frost hollows, up to 100 m for regional maps.
  KLAM_21 is run at 7 m (core) / 35 m (surroundings) in `uiboupin2025how` §2.2.
- **Neighbourhood:** von Neumann with staggered face values (Nowatschin, per notes);
  Moore 8 with drop / distance weights (SAGA implementation).
- **Time step:** Nowatschin — abstract step; how a step maps to model time is not given
  in the notes (Q2). SAGA — adaptive, Δt = delay · Δx / v_max (hours), doubled when nothing
  moves (implementation SAGA). Output in hourly maps (Nowatschin, notes) or every
  `TIME_UPDATE` = 10 min (SAGA default).
- **Update scheme:** synchronous. Nowatschin: two shader passes per step (faces, then
  cells) — a gather scheme. SAGA: outflows from the old state are *added* to neighbours
  inside a parallel loop (scatter); in ca-geo this must be rewritten as slot outflows +
  gather (same result, no write races).
- **Boundary conditions:** open (air leaves the domain) is the default in both;
  SAGA also offers closed edges. Open-edge outflow must be recorded (mass balance).

## 5. Transition rule

### 5.1 Primary rule (`nowatschin2006gpubased`, restated from domain notes)

State per cell i: terrain height h_i, cold-air height k_i, land-use class c_i.

1. **Production** (`map`): k_i ← k_i + p(c_i), where p is the production per land-use
   class per step (production table in the paper; units m³ m⁻² h⁻¹, i.e. metres of
   cold-air height per hour).
2. **Face velocity** (`flux` pass a, per face between von Neumann neighbours i, j):
   v_ij = (h_i + k_i − h_j − k_j) / w, with w the flow resistance of the land use.
   Sign gives the direction; the donor is the cell with the higher effective surface.
   No inertia: v depends only on the current surface gradient.
   *Open:* which cell's resistance (donor, receiver, mean) is used on a face (Q3); w is
   given "in %" — conversion to a divisor is unclear (Q4).
3. **Limiter** (per donor cell): the outgoing velocities of a cell are scaled so that
   their sum is ≤ 1; then the outflow over each outgoing face is v·k_donor, i.e. a cell
   never sends more than its content. This makes the scheme mass-conserving without a
   pressure / divergence projection.
4. **Gather** (`flux` pass b): k_i ← k_i + Σ inflows − Σ outflows.
5. **Boundaries:** faces to outside cells are open — air leaves the domain.

Conserved: total cold-air volume up to production (source) and boundary loss (sink).
Not conserved: momentum, heat (no temperature state). Ambiguities: Q2–Q5.

### 5.2 Variant: SAGA "Cold Air Flow" (`conrad2020coldairflow`, implementation SAGA)

Moore neighbourhood, effective surface S_i = h_i + k_i.

1. For each cell with k_i > 0 and friction f_i > 0: for each in-domain neighbour n with
   S_n < S_i, weight d_n = (S_i − S_n) / L_n (L_n = 1 or √2 cell lengths); with open
   edges an off-grid neighbour gets a weight from the mirrored inside neighbour and its
   share is discarded (leaves the domain). D = Σ d_n.
2. If D > 0, speed v_i = 3600 · √( g · (T − T_c)/T · (k_i / f_i) · sin s_i ) [m h⁻¹], where
   T, T_c are ambient and cold-air temperatures (K), g = 9.80665 m s⁻², and s_i is the
   slope of the *air surface* from central differences over the 4 neighbours
   (s = atan √(G² + H²)). This is a reduced-gravity gravity-current speed.
3. Global v_max = max v_i (`reduce`); Δt = delay · Δx / v_max (hours); if v_max = 0,
   Δt ← 2 Δt.
4. Moved height Δk_i = min(k_i, k_i · v_i · Δt / Δx); neighbour n receives Δk_i · d_n / D.
5. Production: k_i ← k_i + P_i · Δt (P in m h⁻¹), added after transport.
6. Initial state (reset): k_i = P_i · Δt₀ with Δt₀ = 1/360 h.

### 5.3 Variant: KLAM-like single-layer model (`sievers2016cold`, notes only)

Prognostic heat deficit E (loss rate P = a · Pmax, a per land-use class, Pmax = 30 W m⁻²)
and vertically averaged momentum on an Arakawa-C grid (gravity of the layer top,
friction from roughness, buildings and trees, optional ambient wind); layer depth H
diagnosed from E through a prescribed temperature-deficit profile; donor-cell advection;
dynamic time step. Several closures are only referenced to the German manual, so this is
an "advanced mode" for later (Q6). Output used in practice: density of cold-air volume
flow (DCAVF, m³ m⁻¹ s⁻¹) per cell (`uiboupin2025how` §2.5).

### 5.4 Static baseline (`chung2006minimum`, notes only)

No dynamics: D8 flow accumulation smoothed by a 5-cell focal mean as a cold-air
accumulation index, used in a regression for minimum temperature. Useful as a
comparison layer ("where would cold air go if it drained like water?").

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Production, field | p | m³ m⁻² h⁻¹ | 12 | `nowatschin2006gpubased`, production table (via domain notes) | to be verified (Q1) |
| Production, forest | p | m³ m⁻² h⁻¹ | 1 | same | |
| Production, settlement | p | m³ m⁻² h⁻¹ | 0 | same | |
| Production, meadow, vineyard | p | m³ m⁻² h⁻¹ | not given in notes | `nowatschin2006gpubased` | Q1 |
| Resistance per land use | w | % | not given in notes; table has a duplicated "settlement" row | `nowatschin2006gpubased` (via notes) | Q4 |
| Production (default) | P | m h⁻¹ | 1 (≥ 0; grid or constant) | implementation SAGA, `cold_air_flow.cpp` | not calibrated |
| Surface friction coefficient | f | – | 1 (≥ 0; grid or constant) | implementation SAGA | not calibrated |
| Simulation time | – | h | 6 | implementation SAGA; used in `dobos2025terrainbased` Fig. 7 | |
| Ambient air temperature | T | °C | 15 | implementation SAGA | `dobos2025terrainbased` §3.3.3 used ~15–16 °C |
| Cold-air temperature | T_c | °C | 5 | implementation SAGA | `dobos2025terrainbased` used 0 °C |
| Time-step adjustment | delay | – | 0.5 (0.01–1) | implementation SAGA | CFL-like safety factor |
| Initial time step | Δt₀ | h | 1/360 | implementation SAGA | source comment says "1 sec" but 1/360 h = 10 s (Q7) |
| Edge policy | – | – | open (default) / closed | implementation SAGA | |
| Max. local heat loss rate | Pmax | W m⁻² | 30 | `sievers2016cold` (as cited in `uiboupin2025how`, Table 1 caption) | KLAM variant |
| Heat-loss fraction a | a | – | forest 0.56; semi-open 0.25; park 1.0; open space 1.0; sealed −0.5; water 0.0; garden 0.8; cemetery 1.0; urban / potential trees 1.0 | `uiboupin2025how`, Table 1 | some values adjusted by the authors (bold in the table) |
| Roughness length z₀ | z₀ | m | forest 0.4; semi-open 0.02; park 0.3; open space 0.05; sealed 0.01; water 0.001; garden 0.1; cemetery 0.3; potential trees 0.1; urban trees 0.3 | `uiboupin2025how`, Table 1 | KLAM variant |
| DCAVF class limits | – | m³ m⁻¹ s⁻¹ | 7.5 / 15 / 25 / 50 | VDI classification as cited in `uiboupin2025how` §2.5 | for urban-ventilation legend |
| Grid size (KLAM case) | Δx | m | 7 (core), 35 (outer) | `uiboupin2025how` §2.2 | |
| Run length (KLAM case) | – | h | 4; outputs at 120 and 240 min | `uiboupin2025how` §2.5 | |

## 6. Deterministic vs. stochastic

Fully deterministic in all variants. No ensembles needed; scenario comparison
(land-use change A vs B) replaces them. RNG not used.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| DEM / DSM | raster, continuous | terrain h; DSM for buildings in towns | required |
| Land cover | raster, categorical | production and resistance via LUT | required (constant fallback) |
| Buildings | vector → raster | resistance / obstacles (urban scenario) | optional |
| Ambient and cold-air temperature | scalar | reduced gravity (SAGA variant) | optional (defaults) |
| Night length | scalar | run duration | required |
| Temperature observations | point time series | validation only | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| DEM | ČÚZK DMR 5G / DMR 4G | CZ | to be verified (licence, access) |
| DSM with buildings | ČÚZK DMP 1G | CZ | to be verified |
| DEM | Copernicus DEM GLO-30 / EU-DEM | EU | to be verified |
| Land cover | CORINE Land Cover; Urban Atlas (towns) | EU | to be verified; classes need reclassification (SC-RECLASS) |
| Land cover, buildings | ZABAGED; OpenStreetMap | CZ / global | to be verified |
| Tree cover | Copernicus HRL Tree Cover Density | EU | to be verified |
| Temperature | ČHMÚ station data; amateur frost-hollow stations | CZ | to be verified |

## 9. Visualization

Animated cold-air height over hillshade (blue transparency), arrows or streamlines for
flow direction, time slider "hours after sunset". Derived maps: maximum height, arrival
time of cold air, volume-flow density (urban corridor scenario, VDI-style classes).
Interactive: paint land use (build a housing estate, plant or cut forest, add a dam or
embankment), change night length; side-by-side "before / after" difference map. Learning
goal: cold air behaves like a slow, invisible liquid that fills basins and is blocked by
obstacles. Optional static baseline (D8 accumulation) for comparison.

## 10. Validation options

- Qualitative: pooling in known frost hollows and valley bottoms; blocking by
  embankments (`nowatschin2006gpubased` reported only qualitative hourly maps).
- Station data: minimum-temperature anomalies vs. simulated pool depth (as in
  `dobos2025terrainbased`: −16 °C daily-minimum contrast between sinkhole bottom and
  a control point during anticyclonic days, §3.3.3).
- Cross-model: SAGA tool as an oracle (same DEM, same parameters) — CLI run of the GPL
  tool is allowed as an external oracle; KLAM_21 published maps (e.g. `uiboupin2025how`)
  only qualitatively.
- Realistic: qualitative plus a station-anomaly check; no quantitative benchmark exists.

## 11. Links to other models

- **WAT** shares the whole outflow machinery (effective surface = terrain + fluid
  height, bounded outflow, gather); ATM-02 is the test that the `flux` stage is truly
  fluid-agnostic.
- **ATM-03 heavy gas** (TWODEE-like) and **ATM-05 snow redistribution**
  (`bernhardt2010snowslide`, "excess above holding capacity flows downhill") reuse it.
- **LND-01** urban growth → new land-use map → cold-air scenario (chain).
- **ATM-01** dispersion could use the cold-air flow field for night-time smoke.

## 11a. Engine mapping

- **Stages (Nowatschin variant), per step:**
  1. `map` production: `cold.k += lut(landuse, production) · Δt`.
  2. `flux` (face placement): pass a — raw face values v_ij from the effective-surface
     difference and LUT resistance; pass a′ — per-donor limiter (scale outgoing faces so
     Σ ≤ 1); pass b — gather.
  3. `reduce` (optional): total volume, boundary loss, max k.
- **Stages (SAGA variant), per step:** `stencil`/`map` speed v_i and drop weights into a
  slot layer; `reduce` v_max → Δt; `flux` (slot placement) outflow pass with
  min(k, k·v·Δt/Δx) split ∝ drop/length, gather; `map` production.
- **Time policy:** Nowatschin — `fixed` (step duration Q2); SAGA — `adaptive`
  (dt from `reduce`, factor `delay`, doubling when idle — needs a "grow when nothing
  moves" rule in TimePolicy, already noted in engine-architecture §7.1).
- **Boundaries:** `open` with boundary-flux record; `closed` optional.
- **RNG:** none. **Observers:** SC-ENVELOPE (max height), SC-ARRIVAL, SC-MASS, hourly
  snapshots. **Interventions:** paint land use, raise terrain (dam / embankment), add
  building footprint, set night length.
- **Shared components:** SC-GRID, SC-LUT, SC-RECLASS, SC-FACE (Nowatschin), SC-SLOT
  (SAGA), SC-OUTFLOW, SC-ADT (SAGA), SC-SRC, SC-BOUNDARY, SC-MASS, SC-ENVELOPE,
  SC-ARRIVAL, SC-INTERV, SC-SLOPE (air-surface slope), SC-D8 (static baseline),
  SC-EFFSURF (effective surface layer).
- **Model-specific:** reduced-gravity speed formula; production / resistance tables;
  KLAM heat-deficit closures.
- **Correction to `model-mapping.md`:** (1) the Nowatschin limiter "Σ outgoing ≤ 1" needs
  a per-donor normalisation sub-pass between the face pass and the gather — the face
  `flux` must support it explicitly; (2) the SAGA tool writes by scatter in a parallel
  loop — the mapping should state it is re-expressed as slot outflows + gather; (3) the
  primary reference is not local — the mapping's description is second-hand.

## 12. Complexity estimate

- **Implementation:** low (shares WAT `flux`); KLAM-like variant medium–high.
- **Computation in the browser:** low–medium; 10⁶ cells × a few thousand steps on GPU,
  fewer on CPU with active tiles.
- **Data preparation:** medium — land-use reclassification and building rasterisation.

## 13. Risks

- Scientific: the simple model has no temperature, no momentum, no ambient wind; units
  of production and resistance are uncertain (primary not verified); results are
  qualitative patterns, not temperatures.
- Data: land-cover class mapping to production / resistance is a judgement call.
- Technical: low.
- Communication: users may read pool depth as a frost forecast — label "relative
  cold-air accumulation, calm clear night assumed".

## 14. Open questions

- Q1: Obtain and read `nowatschin2006gpubased` (manifest `manual`); verify the rule, the
  production table (all classes) and the resistance table.
- Q2: What model time does one Nowatschin step represent? Is there a stability limit?
- Q3: Which land-use resistance is applied on a face (donor, receiver, mean)?
- Q4: How is resistance "in %" turned into the divisor w? Which settlement row in the
  duplicated table is correct?
- Q5: Is production added before or after transport within a step (SAGA: after)?
- Q6: Are KLAM_21 closures (temperature-deficit profile, friction terms) available
  openly enough to implement a KLAM-like variant? `TODO(literature)`.
- Q7: SAGA initial Δt: 1/360 h (10 s) vs comment "1 sec" — matters only for the first
  production increment.
- Q8: Does SAGA's parallel scatter (`Add_Value` from several threads) produce
  thread-order-dependent results? Relevant when it is used as an oracle (compare with
  single-threaded run).

## 15. Literature and implementations

- **Primary reference:** `nowatschin2006gpubased` — complete explicit CA-like rule with
  land-use tables, designed for GPU shaders (not local; see source note).
- **Supporting references:** `conrad2020coldairflow` — open variant with physical speed
  and adaptive Δt (grey literature); `sievers2016cold` — physically based KLAM_21
  (advanced variant, parameters); `uiboupin2025how` — urban-ventilation scenario,
  KLAM land-use table, DCAVF classes; `dobos2025terrainbased` — Central-European
  validation case using the SAGA tool; `chung2006minimum` — static baseline.
- **Benchmarks / reference data:** none standard; `dobos2025terrainbased` logger
  contrasts; SAGA oracle runs on our DEMs.
- **Implementations:** SAGA `sim_air_flow` (GPL-2.0+) — reference / oracle only;
  KLAM_21 (closed binaries, DWD) — reference results only; REDCAPP (GPL-3.0, not a flow
  model) — not used.
- **Still missing:** `TODO(literature)` — full text of the primary; Schwab (2000) and
  Bendix (2005) cited by the SAGA tool (not in references.bib); any CZ frost-hollow
  station dataset.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| cold-air pooling | stékání a hromadění studeného vzduchu | phenomenon |
| cold-air pool | jezero studeného vzduchu | phenomenon |
| frost hollow | mrazová kotlina | phenomenon |
| cold-air drainage (flow) | stékání studeného vzduchu | phenomenon |
| cold-air layer height | výška (mocnost) vrstvy studeného vzduchu | state variable |
| effective surface | efektivní povrch (terén + vrstva) | state variable |
| cold-air production | produkce studeného vzduchu | parameter |
| flow resistance | odpor proudění | parameter |
| surface friction coefficient | součinitel povrchového tření | parameter |
| heat-loss rate | míra tepelné ztráty | parameter |
| volume-flow density | hustota objemového toku studeného vzduchu | UI output |
| ventilation corridor | ventilační (provětrávací) koridor | UI output |
| night length | délka noci | UI action |
| paint land use | změnit využití území | UI action |
