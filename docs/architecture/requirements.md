# Engine requirements

Requirements for the ca-geo cellular-automata engine, derived from the **template models**
of the working selection (revision 2 of `docs/review/evaluation-matrix.md`: 6 core and 8
extension models). Every requirement is traced to the models and references that need it.
Model mechanics are taken from the entries in `docs/research/domains/*.md`; references are
BibTeX keys in `/references.bib`.

Priority: **M** = must (needed by a core model), **S** = should (needed by an extension
model), **C** = could (nice to have / future).

## Models covered

| ID | Model | Group | Primary templates |
|---|---|---|---|
| HAZ-01 | Wildfire spread (+URB-03 urban fire) | core ★ | `alexandridis2008cellular`, `xia2025pytorchfire`, `trucchia2020propagator`, `hargrove2000simulating` |
| WAT | Water flow / flooding (scenarios) | core ★ | `guidolin2016weighted`, `bates2010simple`, `callaghan2019computing`, `landa2019smoderp2d` |
| EPI-04 | Population dispersal (+EPI-05 rabies front, ECO-04) | core | `bradshaw2021stochastic`, `gregoriodesouza2021reassessing`, `smith2002predicting` |
| ATM-02 | Cold-air pooling | core | `nowatschin2006gpubased`, `sievers2016cold` |
| ECO-01 | Bark-beetle outbreak | core | `pietzsch2023nonparametric`, `liu2025multiscale` |
| LND-01 | Urban growth | core | `clarke1997selfmodifying`, `roodposhti2020towards`, `hewitt2019cellular` |
| MOV-03 | Accessibility front | extension | `wood2012anisotropic`, `nelson2019suite` |
| HAZ-05 | Lava flow | extension | `connor2012probabilistic`, `dietterich2017benchmarking` |
| ECO-09 | Plant pest / pathogen (+ECO-03 invasive) | extension | `white2017modelling`, `moenickes2013shapes` |
| HAZ-02 | Runout (+avalanche, rockfall) | extension | `damboise2022flowpy`, `dambrosio2003simulating` |
| MOV-01 | Pedestrian evacuation | extension | `kirchner2002simulation`, `kirchner2003friction` |
| HYD-05 | Soil erosion | extension | `landa2019smoderp2d`, `eltner2025using` |
| ATM-01 | Pollutant dispersion | extension | `sonnenschein2025hybrid` |
| HYD-09 | Groundwater flow | extension | `ravazzani2011macroscopic` |

## R1 — Space (grid, topology, layers)

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R1.1 | Regular **square raster** with georeference (CRS, origin, cell size, rows × cols) and a domain / NoData mask. | M | all |
| R1.2 | **Multiple layers per grid** with explicit dtype (u8, i32, f32), unit and role: static input, state, derived, output. | M | all |
| R1.3 | **Categorical layers with lookup tables** (class → parameters): fuel classes, land-use production / resistance, Manning n, stand types. | M | HAZ-01, ATM-02, ECO-01, LND-01, WAT |
| R1.4 | **Edge-centred (staggered) layers** — values on the faces between cells (fluxes, velocities). | M | WAT (`bates2010simple`), ATM-02 (`sievers2016cold`), HYD-09 |
| R1.5 | **Per-direction (neighbour-slot) layers** — K values per cell, one per neighbour (outflows, barrier weights between cells). | M | WAT (`guidolin2016weighted`), EPI-04/05 (river barriers), HAZ-02 |
| R1.6 | **Hexagonal topology** (centre + 6). | C | HAZ-02 (`dambrosio2003simulating`), ECO-01 (`liu2025multiscale`) — both can be resampled to square |
| R1.7 | **Graph topology** (irregular cells = polygons with adjacency). | C | EPI-05 (`smith2002predicting`); out-of-scope SOC-02 |
| R1.8 | **Agents / particles on the lattice** with cell exclusion. | S | MOV-01 |
| R1.9 | Grid sizes up to ~4 M cells (2000 × 2000) for interactive runs; larger only for offline / precomputed runs. | M | all (browser constraint) |

## R2 — Neighbourhoods and interaction range

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R2.1 | **von Neumann** (4) and **Moore** (8) neighbourhoods with per-neighbour distance and direction vector. | M | all |
| R2.2 | **Extended / weighted kernels** (radius r, distance-decay weights, direction-dependent weights). | M | LND-01 (up to 11 × 11, `roodposhti2020towards`), ATM-01 (wind-weighted n × n), ECO-09 |
| R2.3 | **Direction-dependent weights from a global or raster vector field** (wind, slope aspect). | M | HAZ-01, ATM-01, MOV-03 (anisotropic cost) |
| R2.4 | **Large-kernel convolution** (kernel of hundreds of metres to km on a fine grid; FFT or separable approximation). | S | ECO-09 (`white2017modelling`) |
| R2.5 | **Long-distance jumps**: rare stochastic transfers to distant cells drawn from a distribution (exponential / Gaussian distance, random direction, constraints such as "not into sea"). | M | EPI-04 (`bradshaw2021stochastic`), ECO-09, HAZ-01 (spotting, `hargrove2000simulating`) |
| R2.6 | **Path search along linear features** (walk along a road raster from a seed cell). | M | LND-01 road-influenced growth (`clarke1997selfmodifying`) |

## R3 — Update schemes

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R3.1 | **Synchronous gather update** (double buffering): a cell computes its new state from the old states of its neighbourhood. | M | HAZ-01, ECO-01, LND-01, MOV-01 (fields), ATM-01 |
| R3.2 | **Conservative flux update** in two passes: (a) each cell computes bounded outflows to its neighbours (or fluxes on faces), (b) each cell gathers inflows; total mass conserved by construction. | M | WAT, ATM-02, EPI-04 emigration, HYD-09, HYD-05, HAZ-02 (SCIDDICA) |
| R3.3 | **Several ordered sub-stages per time step** (e.g. four growth rules of SLEUTH; flux → depth → velocity of WCA2D). | M | LND-01, WAT, ECO-09 |
| R3.4 | **Event-driven / priority-queue propagation** (cells processed in order of a key: arrival time, water surface, cost). | M | MOV-03, HAZ-01 (`trucchia2020propagator` time-to-ignition), WAT (`callaghan2019computing` ordered variant) |
| R3.5 | **Active-front list with parent information** (propagation from source cells; state depends on the direction of arrival). | S | HAZ-05 (`connor2012probabilistic`), HAZ-02 (`damboise2022flowpy`) |
| R3.6 | **Propose–resolve update** for agents: every agent proposes a move; conflicts are resolved (randomly or with friction μ). | S | MOV-01 (`kirchner2002simulation`, `kirchner2003friction`) |
| R3.7 | **Global demand-constrained allocation**: rank cells by transition potential and convert the top N per class. | M | LND-01 (constrained CA, `hewitt2019cellular`) |
| R3.8 | **Gillespie-type continuous-time events** on a graph. | C | EPI-05 (`smith2002predicting`) — a discrete-time raster variant is acceptable |
| R3.9 | **Active-cell optimisation** (skip inactive regions: dry cells, unburnt far from the front). | S | HAZ-01, WAT, HAZ-05 (performance) |

## R4 — Time

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R4.1 | **Fixed time step** with physical meaning (seconds … years). | M | HAZ-01, ECO-01, LND-01, EPI-04, ATM-02 |
| R4.2 | **Adaptive time step** from a global reduction (CFL / velocity limit, min / max bounds). | M | WAT (`guidolin2016weighted`, `bates2010simple`), HYD-05 |
| R4.3 | **Iterate to convergence** (stop when max change < ε for k iterations). | S | WAT steady ponding (`callaghan2019computing`), MOV-03 iterative relaxation |
| R4.4 | **Pulse / budget-driven iteration** (iterations not tied to time; stop when a budget is used). | S | HAZ-05 |
| R4.5 | **Time-dependent forcing**: scalar time series (rain intensity, wind, hourly meteorology) and raster time series (radar rain). | M | WAT, ATM-01, ATM-02, ECO-01 (drought index) |
| R4.6 | **Separate model clock and display clock** (animation speed independent of Δt). | M | all demos |

## R5 — Randomness and ensembles

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R5.1 | **Reproducible per-cell random draws** (same seed → same result, independent of evaluation order and backend). | M | HAZ-01, ECO-01, LND-01, EPI-04, ECO-09, MOV-01 |
| R5.2 | Distributions: uniform, Bernoulli, exponential, normal / truncated normal, Poisson / binomial (exact or approximated), Weibull. | M | EPI-04 (demographic stochasticity), LND-01 (Weibull noise, `roodposhti2020towards`), HAZ-05 (truncated normal) |
| R5.3 | **Ensembles / Monte Carlo**: N runs with derived seeds, aggregated into frequency / probability maps, mean, quantiles, arrival-time statistics. | M | HAZ-01 (`trucchia2020propagator` ~100 runs), LND-01, HAZ-05 (thousands), MOV-01 (hundreds) |
| R5.4 | Ensembles run in parallel (workers) and must not block the UI. | M | as above |

## R6 — Sources, sinks, boundaries, interventions

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R6.1 | **Sources and sinks**: rain, point inflow hydrograph, lava vent, cold-air production per class, emission cells reset each iteration, pumping wells, infiltration. | M | WAT, ATM-02, ATM-01, HAZ-05, HYD-09 |
| R6.2 | **Boundary policies** per layer: open (mass leaves, accounted), closed / reflective, fixed value (Dirichlet), fixed flux (Neumann), NoData as wall or as sink, "forbidden target" masks (sea). | M | WAT, ATM-02, HYD-09, ECO-09 |
| R6.3 | **User interventions between steps**: ignite cells, draw barriers / dams / firebreaks, set control or vaccination zones, place exits, edit parameters. | M | all demos (didactic interaction) |
| R6.4 | **Controllers**: host-side logic between steps that reads global statistics and changes parameters (self-modification, stop conditions, scheduled events). | M | LND-01 (SLEUTH self-modification), HAZ-05 (pulses), WAT (hydrograph) |

## R7 — Derived layers and preprocessing

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R7.1 | Terrain derivatives: slope, aspect, hillshade, D8 flow direction, flow accumulation, depression filling (priority-flood). | M | WAT, HAZ-01, ATM-02, HAZ-02, MOV-03, LND-01 (slope) |
| R7.2 | Distance and cost surfaces (Euclidean distance, cost-distance, anisotropic Tobler slope cost). | M | MOV-03, MOV-01 (static floor field), LND-01 (accessibility) |
| R7.3 | Rasterisation of vector data (roads, rivers, polygons, barriers between cells). | M | LND-01, EPI-04/05, ECO-09, MOV-01 |
| R7.4 | Reclassification via lookup tables (land cover → fuel / production / K). | M | HAZ-01, ATM-02, EPI-04, ECO-01 |
| R7.5 | **Recomputable derived layers during a run** when their source becomes dynamic (eroded DEM → new slope; lava thickness → effective elevation). | S | HYD-05, HAZ-05 |
| R7.6 | Resampling / reprojection to a common grid; clipping to an area of interest. | M | all |

## R8 — Observation, output, validation

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R8.1 | **Global statistics per step** (sum, min, max, count, histogram) — also used for mass-balance checks. | M | all; WAT / ATM-02 / HYD-09 mass balance |
| R8.2 | **Accumulating outputs**: first-arrival time, maximum envelope (max depth, max energy height), visit counts. | M | HAZ-01, WAT, HAZ-02, MOV-03 |
| R8.3 | Snapshots at chosen times; export to GeoTIFF / PNG / CSV / JSON. | M | all |
| R8.4 | **Validation metrics** against reference maps: quantity / allocation disagreement, figure of merit, fuzzy kappa, Jaccard / Sørensen, RMSE against benchmark series. | M | LND-01, HAZ-01, WAT (`neelz2010benchmarking`), HAZ-05 (`dietterich2017benchmarking`) |
| R8.5 | **Benchmark runner** that executes published test cases headless and compares against expected outputs. | M | WAT, HAZ-02 (analytical tests), HYD-09 (Theis), MOV-01 (`ronchi2013process`) |

## R9 — Composition and coupling

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R9.1 | **Model chaining**: an output layer of one run becomes an input of another (fire → burnt area → runoff → erosion; chains L1–L14 in the longlist). | M | demo scenarios |
| R9.2 | **Co-located submodels sharing layers in one simulation** (erosion reading water fluxes every step). | S | HYD-05 (+WAT), ECO-01 (+drought) |
| R9.3 | Coupling of different time scales (minutes vs. years) via explicit synchronisation points. | C | chains with ECO / LND models |

## R10 — Calibration and parameters

| ID | Requirement | Prio | Needed by |
|---|---|---|---|
| R10.1 | **Parameter schema**: id, unit, default, range, i18n keys, and **provenance** (BibTeX key and table / section of the default value). | M | all (no invented values — project rule) |
| R10.2 | Parameter sweeps / random sampling / simple optimisation run headless in workers or Node. | S | LND-01 (`roodposhti2020towards`), HAZ-01, ECO-01 |
| R10.3 | Scenario presets (inputs + parameters + seed) that can be saved, shared and reloaded. | M | demos |

## R11 — Non-functional

| ID | Requirement | Prio |
|---|---|---|
| R11.1 | Runs in the **browser**, simulation off the UI thread (Web Workers). | M |
| R11.2 | Also runs **headless in Node** (tests, benchmarks, calibration, preprocessing). | M |
| R11.3 | **CPU reference implementation** of every model is the specification; accelerated backends must reproduce it within stated tolerance. | M |
| R11.4 | **GPU acceleration** for flux / stencil models with many steps (WAT, ATM-02, HYD-09, HAZ-01 ensembles). | S |
| R11.5 | Interactive frame rates (≥ 10 updates/s of the view) on a typical laptop for grids of ~1 M cells for the core models. | S |
| R11.6 | No hard-coded user-facing strings; all labels via `cs` / `en` catalogues (layer, parameter and state names have i18n keys). | M |
| R11.7 | Minimal runtime dependencies in the core; no server needed to run a demo (static hosting). | M |
| R11.8 | Deterministic, testable: same inputs + seed + backend → identical outputs. | M |
