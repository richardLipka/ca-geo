# Population dispersal and colonisation

| Field | Value |
|---|---|
| ID | `population-dispersal` |
| Longlist ref. | `EPI-04` (scenarios `EPI-05` rabies front, `ECO-04` habitat connectivity) |
| Category | ecology / epidemiology / archaeology (demic spread) |
| Group | core |
| Weighted score | 4.25 (revision 2) |
| Primary reference | `bradshaw2021stochastic` |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

A population lives in a landscape whose cells can support different numbers of individuals
(carrying capacity K). In each cell the population grows towards K; when a cell gets
crowded, groups leave for neighbouring cells, and occasionally a group travels far. The
result is a **colonisation front** that advances over suitable habitat, slows down or stops
at barriers (deserts, mountains, rivers, motorways, vaccination belts) and leaves behind a
saturated population. Examples: first peopling of a continent (`bradshaw2021stochastic`),
spread of farmers (`gregoriodesouza2021reassessing`, `fort2012modelling`), return of beaver
or wolf to Central Europe (`graham2022monitoring`, `john2010habitat`, `marucco2010predicting`),
a wildlife disease wave meeting a river (`smith2002predicting`).

Scales: cells of 0.5° (≈ 55 km) and one generation (27.9 years) for human peopling
(`bradshaw2021stochastic`, Methods); 50 km and 30 years in dispeRse (implementation
dispeRse, file `man/simulate_dispersal.Rd`); for returning mammals in CZ 1–5 km cells and
one year (assumption). Demo questions: *How fast does the front move? Where does it stall?
What does a barrier (river, motorway, vaccination zone) change? When will a species reach my
region?*

## 2. Suitability for CA

Very good. Growth is cell-local, emigration goes to the immediate neighbours, K is a raster
derived from land cover / productivity, and the main output (first-arrival time) is a
raster. Barriers are naturally per-cell (impassable habitat) or per-edge (a river between two
cells). Limits: long-distance dispersal is non-local (handled as a separate jump stage);
individual behaviour (pack formation, territory choice — `marucco2010predicting`,
`kramerschadt2004fragmented`) is not represented; one population per cell means no
age/sex structure; river-network species (beaver) are better on a network than on a
square grid (`hartman1995patterns`, `chaputbardy2017network`).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `pop.N` | real ≥ 0 (or integer for demographic noise) | number of individuals in the cell | dynamic |
| `K` | real ≥ 0 | carrying capacity (individuals per cell) | static input or time series (interpolated), Poisson-resampled each step in the primary |
| `pop.arrival` | time or NoData | first time N ≥ N_first | output |
| `pop.out` | real ≥ 0, slot (8) | emigrants sent to each neighbour this step | scratch |
| `barrier` | real [0,1], slot (8) | permeability of the edge to neighbour k (1 = free, 0 = closed) | static input |
| `terrain` | categorical {normal, barrier, corridor} | dispeRse-style cell mobility class | static input |
| `rugged` | real [0,1] | standardised ruggedness G_rel | static derived |
| `dWater` | real ≥ 0 (cells) | distance to water D_H2O | static derived |
| `catastrophe` | boolean | cell hit by a mortality event this step | scratch |
| EPI-05: `inf.state` | categorical {susceptible, infected} (+ vaccinated) | infection state per cell | dynamic |

## 4. Neighbourhood and time step

- **Grid:** square. 0.5° × 0.5° lattice of 86 × 87 cells in the primary
  (`bradshaw2021stochastic`, Methods "Cellular-automaton framework"); dispeRse reprojects
  to an equal-area grid whose cell size equals the migration distance per generation
  (implementation dispeRse, file `R/dispeRse.R`). Township polygons (graph) for EPI-05
  (`smith2002predicting`).
- **Neighbourhood:** Moore (8 neighbours) for emigration in both references; dispeRse
  extends to radius 2–4 for corridor cells; long-distance dispersal up to 10 cells
  (`bradshaw2021stochastic`, Methods "Global sensitivity analysis", item iii).
- **Time step:** one generation (27.9 years) in the primary, 30 years in dispeRse. The cell
  size and the step together bound the front speed (one cell per step without jumps,
  see §5.4).
- **Update scheme:** synchronous in the primary (per generation; also stated in
  `docs/research/implementations.md`). dispeRse updates the population **in place** while
  iterating the active list, so results depend on order; we use a synchronous version
  (open question: how much the arrival maps differ).
- **Boundary conditions:** closed. Outside the (possibly time-varying) land mask nothing
  lives and nothing is sent.

## 5. Transition rule

### 5.1 Primary: stochastic Ricker + emigration CA (`bradshaw2021stochastic`, Methods)

Per generation t, for every cell i (we write N_i, K_i for N_{i,t}, K_{i,t}):

1. **Carrying capacity.** K_i comes from hindcast net primary production P_p, rescaled to
   human densities between 0.018 and 1.152 km⁻² and multiplied by the cell area, then
   linearly interpolated between 1000-year layers ("Carrying capacity"). Three K–P_p forms
   are tested: linear; rotated parabola K = a·(P_p − h)² + K_max (Eq. 2); reciprocal
   quadratic yield density K = P_p / (a + b·P_p + c·P_p²) (Eq. 3). K is Poisson-resampled
   in every cell and step.
2. **Growth.** Ricker: N_i ← N_i · exp(r_m · (1 − N_i/K_i)) (Eq. 1, growth part). Cells
   with N_i < N_MVP receive extra mortality M_MVP (beta-resampled) (Methods, end of
   "Population-dynamics model").
3. **Emigration to the 8 neighbours.** For each neighbour j, visited in the fixed order
   NW, N, NE, W, E, SW, S, SE:
   - K_rel = K_i / K_j. Emigration is possible only if K_rel < 1 (the neighbour is better)
     **and** N_i / K_i exceeds a uniform random threshold in [0.3, 0.7].
   - It happens with probability Pr(E) = exp(−3.2 · K_rel) (Eq. 4).
   - The group size is N_mig ≈ N_i · P_mig with P_mig beta-resampled around 1/3 and
     SD = 0.05 · N_i · P_mig; emigrants already sent to earlier neighbours are removed
     before the next neighbour is evaluated.
   - The count is multiplied by the ruggedness reduction M_red = a + b · ∛G_rel (Eq. 6),
     which lowers movement by at most 1 %.
   - "Immigration" into i from a worse neighbour follows the same rules seen from the
     other side (open question Q2).
4. **Long-distance dispersal (LDD).** The probability that the dispersal distance exceeds d
   (d = 1…10 cell widths of 55.6 km) is Pr(d_max) = exp(−d / (a·M^b)) with the allometric
   maximum natal dispersal distance a·M^b for M = 50 kg; the maximum distance grows 12.7×
   per tenfold decrease of relative NPP ("Long-distance dispersal"). When an LDD event
   occurs, a Poisson draw around the maximum distance gives |Δx| and |Δy| in cells with
   random signs. The group size follows the emigration rule. The event is realised only
   with probability P_l = 1 − (D_l / D_H2O)^θ (Eq. 5, exponent placement uncertain in our
   text extraction — Q3), where D_l is the realised distance and D_H2O the distance to water.
5. **Catastrophes.** Each occupied cell suffers a catastrophe with probability 0.14 per
   generation; the cells are chosen by a Thomas cluster process (cluster centres Poisson,
   members displaced normally), so events are spatially aggregated; severity is
   beta-sampled around M_cat = 0.5 ("Catastrophic mortality events").
6. **Update:** N_i(t+1) = growth result − E_i + I_i (Eq. 1). What is conserved: emigrants
   leave i and arrive in j (conservative exchange); growth, catastrophes and MVP mortality
   change the total.
7. **Observer:** a cell is "peopled" when it first receives N_first = 100 individuals
   (Methods "Scenarios"); 100 runs per scenario give per-cell mean and 95 % interval of
   first-arrival time.

### 5.2 Variant: deterministic threshold model (dispeRse, MIT; `gregoriodesouza2021reassessing` family)

From implementation dispeRse (files `README.md`, `src/growth.c`, `src/fission.c`, facts only):

- K_i = environment value e_i ∈ [0,1] (relative density); local growth rate r_i = r · e_i^γ.
- Growth over one generation of length t years: closed-form logistic
  N ← K·N / ((K − N)·exp(−r_i·t) + N).
- Emigration ("fission", asymptotic threshold model): migrants m = N − φ·K if N/K > φ,
  else 0.
- Targets: Moore neighbours j with e_j > 0 and N_j < φ·K_j ("free" cells). Migrants are
  split in proportion to 1/d² (weight 1 orthogonal, 0.5 diagonal). If no target is free
  the cell becomes inactive.
- Terrain classes: cells marked **barrier** never emit; cells marked **corridor** may send
  migrants up to `accel` ∈ {2,3,4} cells away, but only to cells that are also corridor
  (weights 1/d²).
- First arrival = the step when a cell first receives migrants; origin cells start at
  N = K.
- No randomness in the core.

### 5.3 Variants from the scenarios

- **EPI-05 rabies front (`smith2002predicting`, PDF not local — from domain notes).** Cells
  are townships (graph, adjacency = shared border point). An uninfected township j gets
  infected with hazard μ (long-distance translocation) + Σ λ_ij over infected neighbours
  i; λ is lower across a major river (River model). Waiting times are exponential and the
  next infection is chosen proportionally (Gillespie). On a raster this becomes either
  (a) a `stencil` with per-step probability 1 − exp(−(μ + Σ_k b_k·λ)·Δt) where b_k is the
  barrier slot weight, or (b) exactly, an event-driven `queue`: every infected cell offers
  its neighbour a candidate time t_i + Exp(λ_ij), every cell also has an independent
  candidate time Exp(μ), and the smallest candidate wins (our reformulation; valid because
  infected cells stay infected — to be verified against the paper). Vaccination zones
  (assumption, no template): λ into vaccinated cells multiplied by (1 − coverage), or the
  cells marked non-susceptible. `TODO(literature)`: an oral-vaccination barrier template.
- **ECO-04 habitat connectivity.** Same rule; K from habitat suitability, `barrier` slot
  weights from motorways / fences / rivers (crossing structures restore permeability);
  compared with the cost-distance front of `accessibility-front` (§11). Lynx dispersal in
  `kramerschadt2004fragmented` is an individual-based model with road mortality (abstract
  only) — used as a qualitative check, not reimplemented.
- **Returning species in CZ.** Beaver: K > 0 only along streams, stream cells as dispeRse
  corridors, watershed divides slow the spread (`hartman1995patterns`); territory capacity
  plus logistic growth (`graham2022monitoring`); CZ habitat preferences
  (`john2010habitat`, content not read). Wolf: habitat-suitability K, packs approximated by
  cells (`marucco2010predicting`, abstract only).
- **Directed emigration (`bradshaw2023directionally`).** Emigration weighted by least-cost
  "superhighway" rasters — i.e. a static field from a `queue` used as slot weights (same
  mechanism as the pedestrian static floor field).

### 5.4 Front speed vs. dispersal (relation to the front model)

- Without jumps, the front advances at most one cell per step (Moore: also diagonally, so
  the front is square-ish and √2 faster along diagonals — a metrication artefact).
- The real speed is set by the **lag** n_lag: the number of steps a newly reached cell
  needs to grow from the arriving group to the emigration threshold (φ·K in dispeRse,
  0.3–0.7·K in the primary). Then v ≈ Δx / (n_lag · Δt), and n_lag depends on r, K and φ
  (our derivation, to be checked by simulation; not from the references).
- dispeRse ties the cell size to the migration distance per generation, so its maximum
  speed is `dist / t` (×`accel` in corridors).
- A deterministic dispeRse-like run should therefore resemble a `queue` (MOV-03) front
  whose per-cell traversal time is n_lag(i)·Δt. Differences: pooling of migrants from
  several neighbours shortens the lag; jumps create satellite foci. This gives a
  **consistency test** between the two models and a way to explain the population model
  as "a front whose speed comes from demography". `gregoriodesouza2021reassessing`
  compares its CA with an equation-based front model (Fisher with time delay, domain
  notes), which is the analytical reference.
- The primary's emergent rate was 0.71–0.92 km year⁻¹ (Results).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Time step (generation) | Δt | year | 27.9 | `bradshaw2021stochastic`, Methods (Eq. 1 text) | dispeRse default 30 (`t`) |
| Cell size | Δx | ° / km | 0.5° (55.6 km cell width) | `bradshaw2021stochastic`, Methods | CZ demo: assumption |
| Max. rate of increase per generation | r_m | — | not given in main text; GSA range 0.10–0.31 | `bradshaw2021stochastic`, Methods "Global sensitivity analysis" (i) | derived from a Leslie matrix; Q1 |
| Min / max human density for K | — | km⁻² | 0.018 / 1.152 | `bradshaw2021stochastic`, Methods "Carrying capacity" | |
| Cell area | A | km² | 3080.25 | ibid. | |
| Rotated parabola | a, h, K_max | — | a = −3, h = median P_p, K_max = 0.5 K_max(linear), rescaled | ibid., Eq. 2 | |
| Quadratic yield density | a, b, c | — | 200, 0.6, 0.2 | ibid., Eq. 3 | |
| Emigration N/K threshold | — | — | uniform in [0.3, 0.7]; GSA min 0.15–0.45, max 0.35–0.99 | ibid., "Emigration and immigration"; GSA (ix, x) | |
| Emigration probability coefficient | — | — | 3.2 in exp(−3.2 K_rel) | ibid., Eq. 4 | |
| Migrating proportion | P_mig | — | 1/3 (beta), SD 0.05·N·P_mig; GSA 0.17–0.50 | ibid., "Emigration and immigration"; GSA (viii) | most influential parameter |
| Allometric dispersal | a, b, M | km, —, kg | a = 3.31 ± 1.17, b = 0.65 ± 0.05, M = 50 | ibid., "Long-distance dispersal" | D_m 22.4–69.3 km |
| Max. LDD distance | D_cell | cells | 10 (GSA ×1–×5) | ibid., GSA (iii) | |
| LDD vs. NPP | — | — | ×12.7 per tenfold NPP decrease | ibid., "Long-distance dispersal" | |
| Hydrological resistance | θ | — | 3 (GSA 1.5–4.5) | ibid., Eq. 5; GSA (vi) | Q3 |
| Ruggedness reduction | a, b | — | 1.001116, −0.0104453 | ibid., Eq. 6 | ≤ 1 % effect |
| Minimum viable population | N_MVP | individuals | 100 (GSA 50–150) | ibid., Methods; GSA (iv) | |
| Extra mortality below MVP | M_MVP | — | 0.2 (beta; GSA 0.1–0.3) | ibid.; GSA (v) | |
| Catastrophe probability | — | gen⁻¹ | 0.14 | ibid., "Catastrophic mortality events" | |
| Catastrophe severity | M_cat | — | 0.5, SD 0.05; GSA 0.38–0.99 | ibid.; GSA (vii) | |
| Thomas process | κ, scale, μ | — | κ ∝ occupied cells with vector 0.3–1.2; scale 0.015; μ = 0.6 × mean occupied-grid dimension | ibid. | units of `scale` unclear, Q5 |
| First-arrival threshold | N_first | individuals | 100 (GSA 50–150) | ibid., "Scenarios"; GSA (xii) | |
| Founding population | N_0 | individuals | 1300–1500 | ibid., GSA paragraph | |
| Runs per scenario | — | — | 100 (GSA 1000) | ibid. | |
| dispeRse growth rate | r | year⁻¹ | 0.025 | implementation dispeRse, file `R/dispeRse.R` | same in `gregoriodesouza2021reassessing` (domain notes) |
| dispeRse emigration threshold | φ | — | 0.5 (example uses 0.33) | ibid., `R/dispeRse.R`, `man/simulate_dispersal.Rd` | |
| dispeRse migration distance | dist | km / generation | 50 | ibid. | = cell size |
| dispeRse corridor reach | accel | cells | 3, allowed {2,3,4} | ibid. | |
| dispeRse env. exponent | γ | — | 1 | ibid. | applied to r only (Q6) |
| Rabies (River model) | α, β, μ | rate | 0.66, 0.09, 2×10⁻⁴ | `smith2002predicting`, Table 1 (via `docs/research/domains/epidemics.md`) | PDF not local; units / time base not recorded (Q7) |
| Beaver territory capacity | — | territories | 120–183 (River Otter) | `graham2022monitoring` (abstract via domain notes) | catchment-specific |

## 6. Deterministic vs. stochastic

The primary is fully stochastic: Poisson K, uniform emigration threshold, Bernoulli
emigration, beta group sizes, LDD distances, catastrophes (clustered), beta MVP mortality.
Randomness stands for environmental and behavioural variability; the authors stress that
outputs are ensembles (100 runs, percentiles). The published R code sets no seed
(`docs/research/implementations.md`), so runs are not reproducible; our engine uses keyed
RNG and seeds. dispeRse is deterministic and serves as the simple, reproducible mode.
Demo: a "deterministic" toggle (dispeRse rule) and an "ensemble" mode with arrival-time
percentile maps.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| Habitat / productivity | raster (continuous) or land cover (categorical + LUT) | K and growth rate | required |
| Land / domain mask | raster (boolean), optionally time series | where the population can live | required |
| Barriers (rivers, motorways, fences) | vector lines → slot weights | edge permeability | optional |
| Corridors (streams, coastlines) | vector / raster → `terrain` class | extended reach | optional |
| DEM | raster | ruggedness | optional |
| Water bodies | raster / vector → distance | LDD limitation | optional |
| Origins | points + start times | initial population | required |
| Vaccination zones (EPI-05) | polygons → mask | reduced susceptibility | optional |
| Observed first arrivals | points with dates | validation | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| Land cover → K | CORINE Land Cover (Copernicus) | EU | to be verified |
| Forest / tree cover | Copernicus High Resolution Layers | EU | to be verified |
| Streams, water bodies | DIBAVOD (VÚV TGM); ZABAGED (ČÚZK) | CZ | to be verified |
| Roads, motorways, rail | ZABAGED; OpenStreetMap | CZ / global | to be verified |
| Wildlife crossings, migration corridors | AOPK ČR (migration-relevant areas) | CZ | to be verified |
| Species occurrences (beaver, wolf, lynx, jackal) | AOPK ČR species occurrence database (NDOP) | CZ | to be verified; licence |
| DEM | DMR 4G / 5G (ČÚZK), Copernicus DEM | CZ / EU | to be verified |
| Historical rabies cases | State Veterinary Administration (SVS ČR) | CZ | to be verified |
| Benchmark data | dispeRse packaged Europe NPP / terrain / dates; Sahul CSV/TIF | Europe / Sahul | local clones; licences per `docs/research/implementations.md` |

## 9. Visualization

Animated population density (log colour) over a basemap; the colonisation front as an
isochrone map of first-arrival time (generation / year); click to place origins; draw a
barrier (river, motorway, fence) or a vaccination belt and rerun; toggle deterministic /
ensemble; ensemble view with median and 95 % band of arrival time; a chart of occupied area
and front distance vs. time with the fitted front speed; side-by-side with the
`accessibility-front` cost front for the same landscape.

## 10. Validation options

- Primary: Spearman correlation between simulated and bias-corrected archaeological
  first-arrival maps (`bradshaw2021stochastic`, Results / Methods "Comparison layers").
- dispeRse / Tupi: RMSE of simulated arrival vs. radiocarbon dates against distance from
  origin (`gregoriodesouza2021reassessing`, domain notes); Europe benchmark data packaged in
  dispeRse (reproduce `fort2012modelling`-type isochrones).
- Rabies: χ² fit of township first-case dates (`smith2002predicting`).
- CZ: qualitative comparison with mapped beaver / wolf occurrences over time (data to be
  verified); only qualitative validation is realistic.
- Verification: dispeRse outputs as an oracle for the deterministic mode (MIT, may be run);
  queue-front consistency test (§5.4); mass balance of the exchange step.

## 11. Links to other models

- **`accessibility-front` (MOV-03):** cost-distance front over the same resistance raster;
  its static field can direct emigration (`bradshaw2023directionally`); consistency test of
  front speed (§5.4).
- **ECO-09 pest / pathogen:** same growth + dispersal structure with a kernel (`convolve`).
- **ECO-07 range shift, LND-02 abandonment:** change K over time.
- **HAZ-01 wildfire / WAT flood:** disturbance masks lowering K (chain, optional).
- Shared components: SC-GRID, SC-LUT, SC-RECLASS, SC-SLOT, SC-RASTERIZE, SC-GROWTH,
  SC-OUTFLOW, SC-LDD, SC-STOCH-SPREAD (EPI-05), SC-QUEUE (EPI-05 exact), SC-ARRIVAL,
  SC-ENSEMBLE, SC-MASS, SC-RNG, SC-INTERV, SC-BOUNDARY, SC-METRICS, SC-CALIB, SC-FLOORFIELD
  (directed variant).

## 11a. Engine mapping

- **Init:** `map` K from land cover via LUT (SC-RECLASS, SC-LUT); geodata: barrier slot
  weights (SC-RASTERIZE → SC-SLOT), ruggedness (SC-SLOPE family), distance to water
  (`queue` isotropic, SC-COST); intervention `introduce` sets origin N.
- **Stages per step (primary):**
  1. `map` K_t = interpolated forcing slice, Poisson resample (RNG key cell, step).
  2. `map` Ricker growth + MVP mortality (SC-GROWTH).
  3. `map` catastrophes from an event mask produced by a clustered point process
     (SC-CLUSTEREVENT) × beta severity.
  4. `flux` emigration (SC-OUTFLOW): outflow pass loops over the 8 slots **in fixed order**
     inside each cell, drawing threshold, Bernoulli and beta group size per slot (RNG key
     cell, step, slot), subtracting what was already sent, multiplied by M_red and the
     barrier slot weight; gather pass adds incoming groups.
  5. `jump` LDD (SC-LDD) in **conservative** mode: movers are removed from the source;
     targets accepted with a per-target probability P_l (not only a boolean mask).
  6. `reduce` occupied cells, total N, front distance (stop condition: saturation).
- **dispeRse mode:** `map` logistic growth; `flux` threshold emigration whose outflow pass
  reads neighbour N and K (target "free" test) and uses extended slots (radius 2–4) for
  corridor cells; no RNG.
- **EPI-05:** `stencil` SI with barrier slot weights (fixed Δt) or `queue` with exponential
  edge times (event policy); graph topology optional.
- **Time policy:** fixed (1 generation / 1 year); event for the EPI-05 queue variant.
- **Boundaries:** closed; domain mask may change over time (sea level) — Q8.
- **RNG:** keyed per (cell, step, stage, slot); sequential order of slots is deterministic.
- **Observers:** SC-ARRIVAL with a **threshold predicate** (N ≥ N_first); SC-MASS on the
  exchange; SC-ENSEMBLE with per-cell **percentiles** of arrival time; front-speed observer
  (arrival vs. distance from origin).
- **Interventions:** introduce population, draw barrier / crossing, vaccination zone, cull
  zone (set N = 0), change K.
- **Model-specific:** the Bradshaw emigration rule (K_rel, Eq. 4, beta groups), LDD
  water/NPP modifiers, ruggedness reduction, catastrophe clustering parameters.
- **Corrections to `model-mapping.md`:** (1) `jump` must be conservative (debit the
  source) and accept a probability layer for targets; (2) the outflow pass needs a per-cell
  sequential slot loop with RNG and may read neighbour state (dispeRse); (3) the arrival
  observer needs a threshold; (4) K is a raster time series with interpolation and per-step
  resampling; (5) catastrophes need a clustered event generator; (6) EPI-05 is better
  mapped to `queue` (exact Gillespie as first-passage) than to a `stencil` only.

## 12. Complexity estimate

- **Implementation:** medium — simple stages, but many stochastic modifiers; dispeRse mode
  is low.
- **Computation in the browser:** low — e.g. 300 × 300 cells × 300 steps × 100 runs.
- **Data preparation:** medium — K from land cover needs an expert LUT per species; barrier
  rasterisation onto edges.

## 13. Risks

- Scientific: K–habitat relationships are assumptions (the primary tests three forms and
  warns about population size); one cell = one population hides individual behaviour.
- Results depend strongly on P_mig and catastrophe severity (primary GSA) — show
  sensitivity.
- Communication: a returning-wolf demo can be read as a forecast or touch conflicts with
  farmers; label as illustrative. Archaeological scenarios must not be shown as settled
  history.
- Data: species occurrence data may have restricted licences.

## 14. Open questions

- Q1. Numeric r_m used in the primary (only the GSA range is in the text); read it from the
  implementation (SahulHumanSpread, GPL — facts only).
- Q2. Is "immigration" a separate step or just the receiving side of neighbours'
  emigration? Risk of double counting.
- Q3. Exact form of Eq. 5 (exponent θ on the ratio or elsewhere) — PDF extraction is
  garbled; check the typeset PDF.
- Q4. How is the occurrence of an LDD event drawn per cell and step (Pr(d_max) as event
  probability or as distance distribution)?
- Q5. Units of the Thomas process `scale` (0.015) and κ mapping.
- Q6. dispeRse documentation says γ shapes K and r, code applies γ to r only.
- Q7. Units and time base of smith2002 rates; exact River-model formula (PDF not local).
- Q8. Population in cells that become sea (time-varying mask): lost or moved?
- Q9. Order dependence: how different are synchronous and in-place dispeRse results?
- Q10. Vaccination barrier: source for coverage → transmission reduction
  (`TODO(literature)`).
- Q11. CZ species choice for the demo (beaver vs. wolf vs. golden jackal) — needs the
  author's decision.

## 15. Literature and implementations

- **Primary reference:** `bradshaw2021stochastic` — complete, quantitatively validated
  stochastic population CA with open code and data (read in full).
- **Supporting references:** `gregoriodesouza2021reassessing` (logistic + threshold
  emigration; PDF not local, domain notes), `fort2012modelling` (front benchmark),
  `bradshaw2023directionally` (cost-directed emigration), `smith2002predicting` (barrier
  model, EPI-05; not local), `marucco2010predicting` (wolf; not local),
  `graham2022monitoring` (beaver capacity + growth; not local), `john2010habitat` (CZ
  beaver habitat; not read), `hartman1995patterns` (beaver spread along drainages),
  `chaputbardy2017network` (river-network colonisation), `kramerschadt2004fragmented`
  (lynx connectivity; not local), `mcrae2008using` (circuit connectivity, context).
- **Implementations:**
  - dispeRse (https://github.com/jgregoriods/dispeRse) — MIT per DESCRIPTION (GitHub API
    NOASSERTION ⚠) — reusable code with notice; also oracle; packaged Europe data.
  - SahulHumanSpread (https://github.com/cjabradshaw/SahulHumanSpread) — GPL-3.0 —
    reference / oracle only.
  - SuperhighwaysSpreadModel (`bradshaw2023directionally`) — MIT — reusable (not cloned).
  - tupi-expansion (`gregoriodesouza2021reassessing`) — GPL-3.0 — reference only.
- **Still missing:** `TODO(literature)` vaccination-barrier rabies model on a grid;
  dispersal / growth parameters for beaver, wolf, golden jackal in CZ.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| population dispersal | šíření populace | phenomenon |
| colonisation front | čelo kolonizace | output |
| carrying capacity | nosná kapacita (prostředí) | state variable |
| emigration | emigrace (odchod) | process |
| emigration threshold | práh emigrace | parameter |
| growth rate | míra růstu | parameter |
| minimum viable population | minimální životaschopná populace | parameter |
| catastrophic mortality event | katastrofická úmrtnost | process |
| long-distance dispersal | šíření na velké vzdálenosti | process |
| barrier permeability | propustnost bariéry | parameter |
| corridor | koridor | input |
| first-arrival time | čas prvního příchodu | output |
| front speed | rychlost čela | output |
| vaccination zone | vakcinační pásmo | UI action |
| introduce population | vypustit populaci | UI action |
