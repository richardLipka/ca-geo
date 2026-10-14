# Plant pest and pathogen spread

| Field | Value |
|---|---|
| ID | `plant-pest-spread` |
| Longlist ref. | `ECO-09` (+ scenario `ECO-03` invasive species) |
| Category | ecology / plant health |
| Group | extension |
| Weighted score | 4.00 (revision 2) |
| Primary reference | `white2017modelling` (read in full; MIT code read) |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

A pest or pathogen spreads through a patchy host landscape (olive groves, ash stands,
orchards, riverbanks). Locally it builds up within a cell until most hosts are infected;
between cells it moves by short vector flights or diffusion and, rarely, by long jumps
(hitch-hiking on vehicles, trade, water). Control removes infected hosts in zones.
Scale: 1 km cells, yearly steps, regions of 10²–10⁵ km² (Xylella in Apulia); 5 m cells
for plant invaders along corridors (ECO-03). Demo questions: how wide must a buffer zone
be to stop a jumping pathogen, and how good must surveillance be? CZ: ash dieback
(`fritsch2026mechanistic`, France), giant hogweed (`nehrbass2007simulation`, W Bohemia).

## 2. Suitability for CA

Good: host cover and suitability are rasters, local spread is a neighbourhood kernel and
control zones are masks. Limits: long-distance jumps dominate the pattern and are poorly
known; vector biology, seasonality and latency are collapsed into one annual step; the
deterministic local spread depends on numerical details (§5, open questions).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `pest.N` | real in [0, K] | fraction of hosts infected (disease incidence) | dynamic |
| `host.U` | real in [0, 1] | proportional host (olive) cover | dynamic (reduced by control) |
| `host.K` | real in [0, 1] | infection carrying capacity, K = U + a(1 − U) | derived each step |
| `land` | boolean | land vs. sea (jump target mask) | static input |
| `control` | categorical {none, eradication zone, buffer zone} | control-zone mask | input / intervention |
| `pest.risk` | real in [0, 1] | mean incidence over the ensemble | output |
| `pest.arrival` | integer (year) | first year with N > 0 | output |

## 4. Neighbourhood and time step

- **Grid:** square 1 km × 1 km (`white2017modelling` Methods).
- **Neighbourhood:** dense kernel over the whole (padded) domain via FFT convolution
  (Eq. 3), plus random long jumps (Gaussian displacement).
- **Time step:** one year, matching the vector's summer feeding on olives (Methods).
- **Update scheme:** synchronous (growth, then dispersal of the whole field).
- **Boundary:** open with zero padding (no wrap-around; implementation
  Xylella-spread-model, file `Xylella_Spread_Model_With_Control.m`); sea cells hold zero
  and cannot receive jumps.

## 5. Transition rule

Restated from `white2017modelling` (Methods: Eqs. 1–3, Dispersal, Control strategies) with
the order and the open details taken from the MIT implementation
(`Xylella_Spread_Model_With_Control.m`, function `spread_model`). Per year:

1. **Local growth (Gompertz).** Continuous form `N(t) = K exp(−B exp(−A t))` (Eq. 1),
   discretised to one year: `N_{t+1} = K · (N_t / K)^{e^{−A}}`, i.e.
   `N' = K^{1−e^{−A}} · N^{e^{−A}}` (Eq. 2). Applied in every land cell.
2. **Short-range dispersal.** The grown field is convolved with an isotropic exponential
   kernel `k(x, y) = exp(−√(x² + y²) / b)` (Dispersal; mean distance b). The kernel is
   **not normalised** ("a normalizing constant is not required", Dispersal; the code uses
   centre weight 1). FFT on a zero-padded domain.
3. **Long-distance jumps (stratified dispersal).** Each cell may emit dispersers with a
   weight q·N (paper) — in the code a cell emits iff `U_i · u ≥ p` with u ~ U(0, 1), i.e.
   with probability max(0, 1 − p/U_i) where U_i is the post-dispersal value (q effectively
   1). An emitting cell sends M ~ uniform{1, …, M_max} dispersers; each displacement is
   drawn from a discrete 2D Gaussian with s.d. d; a landing in the sea is **redrawn**
   (code) / "not possible" (paper). A landing cell receives the initial Gompertz level
   e^{−B} (added to its value in the code).
4. **Masks and noise.** Sea and non-host cells are set to 0; values below a tolerance
   (1e-8) are set to 0 (code only).
5. **Control.** In the control zone(s), every infected cell is detected with a probability
   (paper: surveillance efficiency s compared with a random p_detect; code: u < eff).
   Detection removes all infected hosts: N = 0, host cover U reduced by the infected
   fraction (not replanted) and K recomputed. In the code the eradication zone is
   cleared of hosts at the start.

Spatial form (Eq. 3): `N_{t+1}(x) = Σ_y k(x − y) · f(N_t(y))`, with k the sum of the
deterministic short kernel and the stochastic jump kernel. Nothing is conserved.

**Open questions:** (a) no clamp N ≤ K after the convolution (the next Gompertz step pulls
values back towards K); (b) with b = 0.1 km on 1 km cells the neighbour weight is e^{−10}
≈ 4.5e-5, but Gompertz amplifies small values strongly (N^{0.05}), so the local front speed
is controlled by the noise tolerance — the tolerance is effectively a model parameter;
(c) the code zeroes non-olive cells, which contradicts a > 0 in K; (d) whether the jump
weight uses N before or after growth / dispersal (paper ambiguous, code: after
dispersal); (e) q is not given numerically.

### 5.1 Scenario ECO-03: corridor-driven invasion (`moenickes2013shapes`; not local, domain notes)

5 m cells with four stage densities (small / medium / large vegetative, flowering), a
density-dependent stage matrix, habitat suitability declining with succession. Offspring:
1 % to random distant cells, the rest on a discretised exponential kernel; offspring that
reach a corridor move along it (35 m on roads / rails, 100 m on rivers, rivers
downstream only) with probability p_shift; management with probability p_man.

### 5.2 Scenario ECO-03 (CZ): giant hogweed at Arnoltov (`nehrbass2007simulation`; not local)

Individual-based on 5 m cells (700 × 700 m), ceiling of 200 plants per suitable cell,
seedlings split into home cell, Moore neighbours and uniformly random distant cells;
habitat changes inserted in the observed years. Rate of increase of occupied cells:
simulated 1.16 vs. observed 1.15 per year (domain notes).

### 5.3 Variant: host–pathogen raster with kernels and weather (`jones2021iteratively`, PoPS; not local)

Per cell susceptible / infected host counts; reproduction rate modulated by weather;
dispersers follow a chosen kernel (Cauchy, exponential, …) and establish depending on host
availability and environment; ABC calibration. GPL code → reference / oracle only.

### 5.4 Variant: ash dieback reaction–diffusion (`fritsch2026mechanistic`)

Yearly cycle on 16 × 16 km quadrats: spores produced on colonised leaf litter (rachises),
diffused during ≈ 60 summer days (diffusion coefficient D) and infecting leaves, then the
new litter is colonised; modulated by summer heat (days > 28 °C), spring rain and ash
density. An explicit finite-difference step of the diffusion is a repeated `stencil`.

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| cell size | L | km | 1 | `white2017modelling` Methods | |
| Gompertz rate | A | yr⁻¹ | 3 | `white2017modelling` Local growth | CVC value 0.489 (Gottwald) |
| Gompertz initial-infection constant | B | – | 14.069 | `white2017modelling` Local growth | → 97 % after 2 years |
| non-host relative capacity | a | – | ∈ [0, 1]; 0 in code | `white2017modelling` Local growth; impl. Xylella-spread-model, `Xylella_Spread_Model_With_Control.m` | |
| short-range mean distance | b | km | 0.1 | `white2017modelling` Dispersal; impl. same file (`beta`) | |
| jump threshold | p | – | 0.2 | `white2017modelling` Dispersal; impl. (`strattol`) | |
| max dispersers per jump event | M_max | – | 5 | `white2017modelling` Dispersal; impl. (`randi(5)`) | |
| jump distance s.d. | d | km | 20 | `white2017modelling` Dispersal; impl. (`D`) | |
| jump weight | q | – | ∈ [0, 1], not given | `white2017modelling` Dispersal | open |
| control efficiency | s / eff | – | ∈ [0, 1]; 0.9 in code | `white2017modelling` Control; impl. (`eff`) | |
| zone widths (eradication / buffer) | – | km | 2 / 13 in code; control zone 25 km in Fig. 2b | impl. (`bufferwidth1/2`); `white2017modelling` Fig. 2 | |
| noise tolerance | tol | – | 1e-8 | impl. (`tol`) | behaves as a parameter (§5 b) |
| ensemble size / horizon | – | runs / yr | 10,000 / 5 | `white2017modelling` Results | risk map |
| ECO-03 long-distance fraction | p_LD | – | 0.01 | `moenickes2013shapes` (via `docs/research/domains/ecology.md`) | |
| ECO-03 corridor shift distance (roads, rails / rivers) | – | m | 35 / 100 | `moenickes2013shapes` (via domain notes) | rivers one-way |
| ECO-03 cell size | – | m | 5 | `moenickes2013shapes`; `nehrbass2007simulation` (via domain notes) | |
| hogweed ceiling per cell | – | plants | 200 | `nehrbass2007simulation` (via domain notes) | |
| ash-dieback quadrat / diffusion period | – | km / d | 16 / ≈ 60 | `fritsch2026mechanistic` §2–3.1 | D: posterior in figures |

## 6. Deterministic vs. stochastic

Growth and short-range dispersal are deterministic; jumps (emission, count, distance) and
detection are random. Risk is the **mean incidence** over an ensemble (10,000 runs in the
paper, `white2017modelling` Results), not only the probability of being reached. Fixed
seeds are needed for replay and paired scenario comparison (relative risk).

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| host cover | raster, continuous [0, 1] | U, K | required |
| land / sea (or "unreachable") mask | raster, boolean | jump target mask | required |
| initial outbreak | point / raster | initial N | required |
| control zones | vector → raster | control | optional (intervention) |
| corridors (ECO-03) | vector → raster / network | corridor movement | ECO-03 |
| climate modulators (5.4) | raster series | rates | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| tree species / ash share | ÚHÚL forest maps; Copernicus HRL Dominant Leaf Type | CZ / EU | to be verified |
| orchards / vineyards (hosts) | LPIS (culture types); CORINE Land Cover | CZ / EU | to be verified |
| occurrence records | AOPK ČR NDOP (invasive plants); EPPO / EU outbreak reports | CZ / EU | to be verified (licence) |
| corridors | DIBAVOD rivers; OSM roads / railways; ZABAGED | CZ | to be verified |
| climate | ČHMÚ gridded data; E-OBS; ERA5-Land | CZ / EU | to be verified |

## 9. Visualization

Yearly incidence map over the host-cover map, satellite outbreaks appearing after jumps,
an ensemble risk map, relative-risk profile beyond a drawn control zone. Interactions:
draw the buffer zone and set its width, surveillance-efficiency slider, seed an outbreak,
toggle long-distance jumps (show that narrow zones are jumped over).

## 10. Validation options

Continuous Boyce index of the risk map against positive tests (B = 0.951,
`white2017modelling` Results); ECO-03: modelling efficiency for occupied / new cells
(`moenickes2013shapes`), occupied-cell growth rate (`nehrbass2007simulation`); ash
dieback: yearly RMSE / likelihood (`fritsch2026mechanistic` Table 4). Quantitative CZ
validation depends on open occurrence data (to be verified).

## 11. Links to other models

Shares stratified dispersal with ECO-01 and EPI-04; ECO-03 shares corridors with MOV-03
(network rasters). Shared: SC-GRID, SC-LUT, SC-RECLASS, SC-GROWTH, SC-KERNEL, SC-LDD,
SC-SRC, SC-INTERV, SC-BOUNDARY, SC-ARRIVAL, SC-ENSEMBLE, SC-METRICS, SC-CALIB, SC-RNG,
SC-RASTERIZE, SC-EVENTS (ECO-03).

## 11a. Engine mapping

- **Stages per year:**
  1. `map` — Gompertz growth (SC-GROWTH), K from U and a.
  2. `convolve` — exponential kernel on a zero-padded domain (SC-KERNEL); for b ≪ cell
     size a 3 × 3 `stencil` is equivalent.
  3. `jump` — emission by threshold on N·u, M uniform, discrete Gaussian displacement,
     **redraw** on masked targets, add e^{−B} at the target (SC-LDD).
  4. `map` — masks and tolerance cut-off.
  5. `map` — control: Bernoulli detection per infected cell in the zone, reduce `host.U`
     (SC-INTERV zone mask).
  6. `reduce` — infected area, northernmost infected row.
- **Time policy:** fixed, 1 year. **Boundaries:** zero padding (open, nothing returns).
- **RNG:** per cell one uniform (emission) + one (detection); per disperser distance draws
  (keyed by event id, as in §8 of the architecture).
- **Observers:** arrival year, ensemble mean incidence (risk), relative risk vs. a paired
  no-control run.
- **Interventions:** draw / widen control zone, efficiency, seed outbreak.
- **Model-specific:** Gompertz parameters, threshold-emission rule.
- **Corrections to `model-mapping.md`:** (1) `host` is dynamic (control lowers it), not only
  an input; (2) the `jump` stage must support "redraw until allowed" besides "discard";
  (3) observers must support the ensemble **mean of a continuous field** and paired-scenario
  differences, not only hit probabilities; (4) ECO-03 corridors move offspring along a
  directed network by a fixed distance (rivers downstream only) — a `walk`-type stage
  (SC-EVENTS) or a directed network kernel, not just corridor-weighted stencil weights.

## 12. Complexity estimate

- **Implementation:** low–medium (FFT convolution and jump bookkeeping).
- **Computation in the browser:** low per run (≈ 10⁵ cells, ≤ 20 steps); the paper's
  10,000-run ensembles need workers / GPU or fewer runs.
- **Data preparation:** medium — host-cover rasters must be derived (no CZ outbreak map).

## 13. Risks

Jump parameters (p, M_max, d) were chosen to look plausible, not fitted
(`white2017modelling` Dispersal); results depend on the tolerance cut-off; Xylella in
Apulia is not a CZ problem, and a CZ pathogen case needs new parameters; users may read
risk maps as forecasts or as policy advice.

## 14. Open questions

- Clamp after convolution; role of the tolerance; non-host zeroing vs. a > 0; q (§5).
- Which CZ case: ash dieback (`fritsch2026mechanistic` parameters as figures only),
  hogweed (`moenickes2013shapes`, `nehrbass2007simulation` — both not local), or a
  fruit-tree pathogen (no reference yet)?
- Is FFT convolution needed at all for the demo grid sizes, or is a stencil enough?
- Open host and occurrence data for CZ (licences).

## 15. Literature and implementations

- **Primary reference:** `white2017modelling` — complete, small stratified-dispersal CA
  with control zones, quantitative fit and MIT code.
- **Supporting references:** `jones2021iteratively` (PoPS, not local);
  `moenickes2013shapes` (corridors, not local); `nehrbass2007simulation` (CZ hogweed, not
  local); `fritsch2026mechanistic` (ash dieback, read as preprint).
- **Benchmarks / reference data:** Xylella repo random host map (`olivegrowthprop.mat`) for
  a regression test against the MATLAB output; PoPS unit tests.
- **Implementations:** Xylella-spread-model (MATLAB, MIT) — reusable with notice; PoPS Core
  (GPL-2.0), rpops / r.pops.spread (GPL) — reference / oracle only.
- **Still missing:** `TODO(literature)` full texts of `moenickes2013shapes`,
  `nehrbass2007simulation`, `jones2021iteratively`; a CZ host–pathogen case.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| plant pest / pathogen spread | šíření škůdců a patogenů rostlin | phenomenon |
| disease incidence (infected fraction) | incidence choroby (podíl infikovaných hostitelů) | state variable |
| host cover | pokryvnost hostitelských rostlin | state variable |
| dispersal kernel | disperzní jádro | parameter |
| stratified dispersal | stratifikované šíření | parameter / process |
| Gompertz growth | Gompertzův růst | parameter |
| surveillance efficiency | účinnost dozoru | parameter |
| buffer zone / eradication zone | nárazníková zóna / zóna eradikace | UI action |
| risk map | mapa rizika | UI output |
| corridor | koridor (liniový prvek) | input |
