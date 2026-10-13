# Reference implementations of the selected models

Status: inventory of 2026-10-13 (working selection = revision 2 of
`docs/review/evaluation-matrix.md`). Facts were checked through the GitHub API (`gh`), the
Zenodo and Mendeley Data APIs, and by reading source files of the shallow clones. Nothing
was built or executed.

## Purpose

1. Record which implementations of the selected models exist, who maintains them, under which
   licence, and what ca-geo can reuse (algorithm reference, test oracle, data).
2. Give short **architecture notes** for the engine design (`docs/architecture/`): grid,
   neighbourhood, update scheme, time step, conservation, randomness, boundaries,
   parallelism, I/O.
3. List local shallow clones (`external/`) and downloaded reference data (`data/reference/`).

Conventions: *Owner* A = authors of the cited paper / model, T = third party.
*Last commit* = GitHub `pushed_at` (or the commit date of the clone).
*Maturity*: 1 = prototype / script / student project, 2 = research code with docs or
examples, 3 = maintained package with tests and releases.
*Reuse*: **alg** = algorithm reference, **oracle** = expected outputs to compare against,
**data** = test inputs, **–** = nothing.
Licence column: SPDX from the GitHub API; "none" = no licence file (all rights reserved by
default); ⚠ = inconsistency, see the section notes.

## Summary table

### Core models

| Model | Implementation | Owner | Licence | Language | Last commit | Tests / data | Mat. | Reuse |
|---|---|---|---|---|---|---|---|---|
| HAZ-01 | PyTorchFire (`xia2025pytorchfire`) | A | MIT | Python (PyTorch) | 2026-09-24 | Bear 2020 inputs + target; paper dataset (Mendeley) | 3 | alg, oracle, data |
| HAZ-01 | PROPAGATOR `propagator_sim` (`trucchia2020propagator`) | A (CIMA) | EUPL-1.2 | Python + Numba | 2026-09-04 | pytest suite; example DEM + fuel GeoTIFF | 3 | alg, data |
| HAZ-01 | Cell2Fire (`pais2021cell2fire`) | A | GPL-3.0 ⚠ | C++ + Python | 2026-05-15 | 11 landscapes (Dogrib, Sub40x40, …) with weather + ignitions | 2 | alg, data |
| HAZ-01 | C2F-W (Cell2Fire derivative, S&B + Kitral fuels) | A (fire2a) | GPL-3.0 | C++ / Python | 2026-08-12 | example instances | 2 | alg |
| HAZ-01 | manoe/wildfire_ca (`alexandridis2008cellular`, `freire2019using`) | T | BSD-2-Clause | C++ | 2023-10-10 | none | 1 | alg |
| HAZ-01 | XC-Li/Parallel_CellularAutomaton_Wildfire | T | MIT | Python (mpi4py) | 2018-05-31 | none | 1 | – |
| HAZ-01 | GRASS `r.ros` + `r.spread` (Rothermel, heap-based spread) | T (GRASS) | GPL-2.0+ | C | 2026-10-12 | – | 3 | alg |
| HAZ-01 | ELMFIRE (level set, not CA) | T | AGPL-3.0 + Commons Clause ⚠ | Fortran | 2026-10-08 | `verification/` (elliptical shape, crown fire, spotting), `validation/` | 3 | oracle (concept only, see licence) |
| HAZ-01 | Pyretechnics / GridFire (raster fire spread) | T (SIG) | dual non-commercial/commercial ⚠ / EPL-2.0 | Python / Clojure | 2026-10-05 / 2024-05-22 | `test/` dir (Pyretechnics); GridFire not checked | 2–3 | alg |
| HAZ-01 | firelab/behave (Rothermel / BehavePlus core) | T (USFS) | public domain (US Gov.) | C++ | 2026-10-06 | – | 3 | alg (ROS sub-model) |
| HAZ-01 | emxsys/behave (Rothermel in JS) | T | MIT | JavaScript | 2018-06-12 | – | 1–2 | alg (JS ROS) |
| HAZ-01 | nramon/FireDynamicsAutomata (Almeida & Macau CA, canvas) | T | GPL-3.0 | JavaScript | 2021-01-10 | none | 1 | – (JS precedent only) |
| HAZ-01 | spotting scripts (`lopezdecastro2024firespotting`) | A | not checked | – | – | analysis scripts, gitlab.bcamath.org/malopez/fire-spotting | 1 | – |
| WAT | caflood (WCA2D, `guidolin2016weighted`) | A (Exeter) | MIT ⚠ (GPL-3 headers) | C++ + CADDIES `.ca` kernels | 2026-03-30 | none in repo | 2 | alg |
| WAT | WaterDesk/caflood (full CAFlood app) | A-related | MIT | C++ | 2025-02-19 | – | 2 | alg |
| WAT | LISFLOOD-FP 8.x (`shaw2021lisflood`, `bates2010simple`) | A (Bristol) | GPL-2.0 | C++/CUDA | Zenodo v8.3 (record dated 2026-10-13) | EA Tests 4/5 + Eden results (Zenodo 4661888) | 3 | alg, oracle, data |
| WAT | GRASS `r.sim.water` (SIMWE path sampling) | T (GRASS) | GPL-2.0+ | C (OpenMP) | 2026-10-12 | testsuite with reference depth/discharge rasters | 3 | alg, oracle |
| WAT | FlowFill (`callaghan2019computing`) | A | GPL-3.0 | Fortran | 2019-11-15 | – | 2 | alg |
| WAT | Fill–Spill–Merge (`barnes2021computing`) / RichDEM | A | MIT / GPL-3.0 | C++ | 2024-05-24 / 2024-06-24 | extensive unit tests | 3 | alg |
| WAT | HiPIMS-CUDA (finite volume, not CA) | T | GPL-3.0 | C++/CUDA | 2025-07-24 | – | 2 | – |
| WAT | aeplay/WebFlood (WebGL shallow water) | T (thesis) | MIT | JavaScript / GLSL | 2018-09-04 | dam-break (Fraccarollo–Toro), Iowa City, Lake Isabella scenarios | 2 | alg (browser GPU pattern), data |
| WAT | lisyarus/webgpu-shallow-water (virtual pipes) | T | MIT | C++ on WebGPU (WGSL) | 2025-02-04 | – | 2 | alg (WGSL pattern) |
| WAT | rkottomt/deluge-flood-sim | T | MIT | TypeScript (WebGPU) | 2026-10-13 | – | 1 (new, unvetted, 744 MB repo) | – |
| EPI-04 | SahulHumanSpread (`bradshaw2021stochastic`) | A | GPL-3.0 | R (scripts) | 2021-10-06 | CSV + TIF inputs (zipped), archaeological dates | 2 | alg, data |
| EPI-04 | SuperhighwaysSpreadModel (`bradshaw2023directionally`) | A | MIT | R | 2023-04-12 | inputs; Zenodo 7542562 | 2 | alg, data |
| EPI-04 | dispeRse (benchmark reimpl. of `gregoriodesouza2021reassessing`-type demic CA) | A (Gregorio de Souza) | MIT ⚠ (API: NOASSERTION) | C + R (CRAN) | 2023-07-19 | packaged data (Europe NPP/terrain, PPNB dates) | 3 | alg, data |
| EPI-04 | tupi-expansion (`gregoriodesouza2021reassessing`) | A | GPL-3.0 | Python + R | 2023-11-10 | inputs (repo 162 MB); Zenodo 4964642 | 2 | alg |
| EPI-05 | – (rabies front: no code found; `smith2002predicting` URL dead) | – | – | – | – | – | – | gap |
| ATM-02 | SAGA `sim_air_flow` "Cold Air Flow" (`conrad2020coldairflow`) | A (SAGA team) | GPL-2.0+ (file headers; repo API: none) | C++ (OpenMP) | 2025-06-12 (mirror) | – | 3 | alg |
| ATM-02 | REDCAPP (cold-air-pooling downscaling, not a flow model) | T | GPL-3.0 | Python | 2017-04-24 | – | 1 | – |
| ATM-02 | KLAM_21 (`sievers2016cold`) | A (DWD) | closed binaries | – | – | – | – | – |
| ECO-01 | MPB-Infestation (`liu2025multiscale`) | A | none | R (+ Python calibration) | 2025-04-02 | scenario folders with results | 2 | alg (licence!) |
| ECO-01 | IPS-UPS (`pietzsch2023nonparametric`) | A | none | R + NetLogo | 2022-08-26 | site data, IBM results, kappa results | 2 | alg, oracle (licence!) |
| ECO-01 | iLand incl. bark beetle module (`seidl2017climate`, `rammer2024individual`) | A | GPL-3.0 | C++ (Qt) | 2026-10-13 | not checked | 3 | alg |
| ECO-01 | LANDIS-II Biological Disturbance Agent extension | T | Apache-2.0 | C# | 2026-08-28 | not checked | 3 | alg |
| LND-01 | SLEUTH 3.0beta_p01 (`clarke1997selfmodifying`) | A (NCGIA / USGS) | none ⚠ | C | tarball (2000s) | demo50/100/200 inputs + scenario files + expected outputs (logs, GIFs) | 2 | alg, oracle, data |
| LND-01 | sleuth_automation (wrapper) | T | GPL-3.0 | Python | 2021-01-20 | – | 1 | – |
| LND-01 | FUTURES `r.futures` (`meentemeyer2013futures`, `petrasova2016open`) | A | GPL-2.0+ | C + Python (GRASS) | 2026-10-12 | testsuites with data for calib / demand / devpressure | 3 | alg, data |
| LND-01 | PLUS (`liang2021understanding`) | A | none | Windows binary only | 2025-12-14 | `PLUS_test_data.rar` (repo 723 MB) | 2 | – (no source) |
| LND-01 | mcPLUS | A (HPSCIL) | none | binaries / shell | 2025-03-11 | data | 1 | – |
| LND-01 | MOLUSCE QGIS plugin | T | GPL-2.0 | Python | 2026-04-14 | – | 3 | alg |
| LND-01 | lulcc R package | T | GPL-3.0 | R | 2020-05-10 | example data | 2 | alg |
| LND-01 | MUSE | T | MIT | Python | 2025-08-11 | sample data (repo 158 MB) | 2 | alg |
| LND-01 | gluc (LEAM) | T | GPL-2.0 | C | 2015-01-22 | – | 1 | – |
| LND-01 | johanlahti/urban-lu-model | T | MIT | Python | 2017-06-16 | – | 1 | – |

### Extension models

| Model | Implementation | Owner | Licence | Language | Last commit | Tests / data | Mat. | Reuse |
|---|---|---|---|---|---|---|---|---|
| MOV-03 | AccessMod 5 (WHO / UNIGE) | T | LGPL-3.0 | R + GRASS (`r.walk` fork) | 2026-09-04 | – | 3 | alg |
| MOV-03 | GRASS `r.cost` / `r.walk` (anisotropic cost surface) | T | GPL-2.0+ | C | 2026-10-12 | `r.cost/test_suite` | 3 | alg, oracle |
| MOV-03 | malariaAtlas R package (friction surfaces of `weiss2020global`) | T (MAP) | MIT | R | 2026-03-30 | data download functions | 3 | data (friction rasters) |
| MOV-03 | `nelson2019suite` R scripts (figshare 10.6084/m9.figshare.7638134.v3) | A | not checked | R | – | – | 1 | alg |
| HAZ-05 | MOLASSES (successor of `connor2012probabilistic`) | A | GPL-3.0 | C | 2022-12-02 | Fagradalsfjall DEM + vents + config | 2 | alg, data |
| HAZ-05 | USFvolcanology/molasses (older) | A | CC BY-NC 3.0 (README) | C | 2016-02-02 | raster samples | 1 | alg |
| HAZ-05 | SCIARA-fv2 CUDA (`spataro2010latest`) | T | GPL-2.0 | CUDA | 2015-05-09 | – | 1 | alg |
| HAZ-05 | MrLavaLoba (stochastic lobes, not CA) | T | custom MrLavaLoba licence ⚠ | Python | 2024-04-15 | examples | 2 | – |
| HAZ-05 | flowy (C++ port of MrLavaLoba) | T | GPL-3.0 | C++ | 2025-12-06 | – | 2 | – |
| ECO-09 | PoPS Core (`jones2021iteratively`) | A | GPL-2.0 | C++ (header-only) | 2026-06-30 | 27 unit-test files | 3 | alg, oracle |
| ECO-09 | rpops / r.pops.spread | A | GPL-3.0 / GPL-2.0 | R / GRASS | 2026-10-06 / 2026-09-21 | GRASS testsuite (r.pops.spread); rpops not checked | 3 | alg |
| ECO-09 | Xylella-spread-model (`white2017modelling`) | A | MIT | MATLAB | 2016-12-06 | olive-density `.mat` input | 2 | alg, data |
| ECO-03 | MDiG (`pitt2009predicting`) | A | GPL (COPYING; API NOASSERTION) | Python + GRASS | 2013-06-21 | test dir | 2 | alg |
| ECO-03 | MigClim (`engler2012migclim`) | A | GPL (DESCRIPTION) | C + R (CRAN archived 2020) | 2020-02-13 | package data | 2 | alg |
| ECO-03 | kissmig (`nobis2014kissmig`) | A | GPL-3+ (DESCRIPTION) | C++ + R (CRAN) | 2025-10-23 | package data | 3 | alg |
| ECO-03 | RangeShifter (`bocedi2021rangeshifter`) | A | GPL-3.0 | C++ / R | archived old repo; org active | – | 3 | – (IBM, not CA) |
| HAZ-02 | Flow-Py v1.0 (`damboise2022flowpy`) | A | GPL-3.0 | Python | 2022-06-20 (archived) | `examples/dam` | 2 | alg, data |
| HAZ-02 | AvaFrame incl. `com4FlowPy` (successor) | A (OpenNHM) | EUPL-1.2 | Python + Cython | 2026-10-12 | many test avalanches (`avaframe/data/ava*`), `ana1Tests` | 3 | alg, oracle, data |
| HAZ-02 | SAGA GPP (`wichmann2017gpp`) | A | GPL-2.0+ | C++ | 2025-06-12 | – | 3 | alg |
| HAZ-02 | Flow-R (`horton2013flowr`) | A | closed (compiled MATLAB) | – | – | – | – | – |
| HAZ-02 | OpenCAL `tests/sciddicaT` (`dambrosio2003simulating` lineage) | A-related | LGPL-3.0 | C (OpenCL/CUDA) | 2019-11-07 | test DEM + source | 2 | alg |
| HAZ-02 | r.avaflow (Mergili) — mirror kostyanp95/r.avaflow | A (official at avaflow.org) / T mirror | GPL-2.0+ (README badge) | C + R + Python | 2026-09-21 | – | 3 | – (shallow-flow PDE, not CA) |
| HAZ-02 | acannistra/runout (alpha-angle calculator) | T | none | JavaScript (Next.js) | 2023-01-25 | – | 1 | – |
| MOV-01 | chraibi/cellular_automata (Burstedde/Kirchner FFCA) | T (JuPedSim author) | GPL-2.0 | Python | 2021-03-02 | none | 1–2 | alg |
| MOV-01 | JuPedSim (not CA; RiMEA-style tests) | T | LGPL-3.0 | C++/Python | 2026-10-13 | verification tests | 3 | oracle (concept) |
| MOV-01 | various student FFCA repos (aleksejalex/floor_field_model MIT, Bio4Res GPL-3, …) | T | mixed | MATLAB/Java/Python | 2020–2025 | – | 1 | – |
| HYD-05 | SMODERP2D (`landa2019smoderp2d`) | A (ČVUT) | GPL-3.0 | Python (NumPy/SciPy) | 2026-09-24 | regression reference outputs (`tests/data/reference`) + Nučice, rain_sim, profile1d data | 3 | alg, oracle, data |
| HYD-05 | RillGrow (`favismortlock1998selforganizing`, `eltner2025using`) | A | none on GitHub; Zenodo 15576594 says CC BY 4.0 ⚠ | C++ | 2025-06-02 | `rg.ini`; data on OPARA (10.25532/OPARA-602) | 2 | alg |
| HYD-05 | CAESAR-Lisflood (`coulthard2013integrating`) | A | none on GitHub; Zenodo 321820 says CC BY 4.0 ⚠ | C# (Windows) | 2017-02-01 | DEMSIP dataset (Zenodo 7908491, 157 MB) | 2 | alg |
| HYD-05 | GRASS `r.sim.sediment` | T | GPL-2.0+ | C | 2026-10-12 | testsuite | 3 | alg, oracle |
| HYD-05 | Landlab erosion components (`hobley2017creative`) | T | MIT | Python | 2026-10-13 | extensive tests | 3 | alg |
| HYD-05 | WebGPU / WebGL hydraulic-erosion demos (GPU-Gang BSD-3, jobtalle MIT) | T | BSD-3 / MIT | TypeScript / JS | 2023 / 2020 | – | 1–2 | alg (GPU pattern only; not calibrated) |
| ATM-01 | CellAutDisp (`sonnenschein2025hybrid`) | A | GPL-3.0 | Python | 2024-04-22 | 4 test files; example workflows (data not included) | 2 | alg |
| HYD-09 | FEST (`ravazzani2011macroscopic`) | A | GPL per docs (unverified) | Fortran (Fossil repo on chiselapp) | – | – | 2 | alg (chiselapp returned HTTP 302 in this run) |
| HYD-09 | Landlab `GroundwaterDupuitPercolator` | T | MIT | Python | 2026-10-13 | tests | 3 | alg, oracle |
| HYD-09 | MODFLOW 6 / FloPy (not CA) | T (USGS) | public domain (USGS) | Fortran / Python | 2026-10-12 | large example + test suite | 3 | oracle |
| HYD-09 | HydroCAL (`furnari2024hydrocal`) on OpenCAL | A | – | – | – | code not found | – | gap |

## Per-implementation notes and architecture

The architecture notes cover the 13 most relevant implementations. Each note paraphrases
the source; nothing is copied.

### PyTorchFire — HAZ-01 (clone)

- Repo https://github.com/xiazeyu/PyTorchFire, MIT, PyPI `pytorchfire`; docs on ReadTheDocs.
- **Grid:** dense tensors `[H, W]` for vegetation and density factors, wind speed and
  direction; slope is `[H, W, 3, 3]` (one value per neighbour direction). State is a
  `[2, H, W]` boolean tensor (burning, burned).
- **Neighbourhood:** Moore. Implemented as eight shifted tensor slices, with no convolution
  layer. Out-of-grid neighbours are cut off by slicing (fixed "no fire outside" boundary).
- **Rule:** Alexandridis-type probability p_h(1+p_veg)(1+p_den)·p_slope·p_wind per
  direction, squashed with `tanh` so that it stays differentiable. A cell's ignition
  probability is 1 − Π(1 − p_neighbour). Burning cells keep burning with probability
  p_continue.
- **Update:** synchronous. The new state is computed from a copy of the old one.
- **Randomness:** global `torch.manual_seed`, with the seed stored on the model; uniform
  draws for every cell at each step.
- **Time step:** fixed (one CA step); time scale set in calibration.
- **Parallelism:** GPU through PyTorch. The paper compares this against an mpi4py CA
  (`examples/mpica.py`).
- **Calibration:** gradient descent through the accumulated ignition probabilities
  (`trainer.py`). This is the model's distinctive feature.
- **I/O:** `.npz` arrays in the examples; FireDataForge integration for real events.
- **For ca-geo:** the whole rule is a few vectorised tensor operations, so it maps directly
  onto a WebGPU compute shader. Its example data and paper dataset can serve as an oracle
  for a statistical comparison (stochastic outputs).

### PROPAGATOR (`propagator_sim`) — HAZ-01 (clone)

- Repo https://github.com/CIMAFoundation/propagator_sim, EUPL-1.2, CLI + web app + docs.
- **Grid:** 2D rasters (DEM, fuel class) plus a status array of shape
  `[rows, cols, realizations]`. Many stochastic realisations run together.
- **Neighbourhood:** Moore, using a fixed table of 8 offsets with precomputed distances and
  meteorological angles.
- **Update scheme:** **event-driven**. Each realisation has a min-heap of
  (time, row, col, ROS, fireline intensity) events. A Numba kernel
  `advance_front_until(t_end)` pops events in time order and pushes neighbour ignitions with
  transition time = distance / ROS (integer seconds, minimum 1 s).
- **Randomness:** a per-neighbour ignition draw against a transition probability (fuel
  table × wind/slope/moisture factors), plus stochastic spotting (lognormal landing
  distance, Poisson ember count). Uses NumPy's global RNG inside Numba, so there is no
  explicit per-realisation seed.
- **Time control:** continuous event time. Boundary conditions (wind, moisture, actions such
  as fire lines and water drops) are separate Python-side events that cut the run into
  windows.
- **Parallelism:** Numba `prange` over realisations. Output is a burn-probability map.
- **I/O:** GeoTIFF loaders and a tile loader. Outputs are GeoTIFF rasters, isochrone
  GeoJSON and JSON metadata. Configured with a JSON config plus a fuel YAML.
- **For ca-geo:** a clean reference for an **event-driven (priority-queue) fire engine**
  with an ensemble dimension. Its design notes (`docs/propagation_scheduler_refactor.md`)
  discuss windowed stepping against per-event overhead, which is directly relevant to our
  engine.

### Cell2Fire — HAZ-01 (clone)

- Repo https://github.com/cell2fire/Cell2Fire, GPL-3.0, but the GitHub description says
  "For Research Use Only" (⚠ ambiguity of intent; the licence file governs).
- **Grid:** cells are objects in a hash map (cell id → object), each holding adjacency,
  per-neighbour ROS, fire progress and distance to the neighbour's centre.
- **Update:** **message passing per fire period**. In each period of fixed length
  (`FirePeriodLen`, minutes) a burning cell adds ROS × period to its progress towards each
  neighbour. When the progress reaches the centre distance, it sends a message and the
  receiver ignites. ROS comes from the Canadian FBP system and is spread to 8 directions
  by an ellipse.
- **Weather:** a CSV table of weather periods, where one weather period spans several fire
  periods.
- **Randomness:** a `--seed` argument (default 123) for ignition sampling and
  replications.
- **Parallelism:** replications run in parallel (separate parallel-code tree).
- **I/O:** ESRI ASCII grids (`Forest.asc`, `elevation.asc`), a `Data.csv` fuel table, and
  CSV weather and ignitions.
- **Data:** 11 test landscapes (9 cells … Dogrib, about 137 MB in total).
- **For ca-geo:** an alternative to the event queue: a fixed-step "progress accumulator"
  that tolerates coarse time steps. Its landscapes are usable test inputs, but the FBP fuel
  model is Canadian.

### caflood (WCA2D) — WAT (clone)

- Repo https://github.com/AlbertChenExeter/caflood. The LICENSE says MIT, but the `.ca`
  kernel headers (`outflowWCA2Dv2.ca`, `waterdepth.ca`, `infiltration.ca`,
  `velocityDiffusive.ca`) say GPL-3 "cafloodpro" ⚠. The code needs the CADDIES CA API (not
  in the repo); it is a C++ host plus `.ca` rule kernels.
- **Grid / neighbourhood:** square grid, von Neumann, cell-centred water depth; edge buffers
  hold outflow and velocity.
- **Update:** synchronous, in two phases: outflow computed on edges, then depth updated
  from net fluxes. This makes it **mass-conservative by construction** (volume moves
  between cells). The weighting rule is summarised in `domains/hydrology.md`.
- **Time step:** **adaptive**. A velocity pass every "update DT" sets Δt from the maximum
  velocity (CFL-like factor α) between min and max Δt. Δt is snapped to fractions of the
  maximum so that output times are hit exactly (`computeDT`).
- **Boundaries:** an explicit boundary-elevation kernel (`setBoundaryEle.ca`). Rain and
  inflow are added by separate kernels.
- **Parallelism:** CADDIES back-ends (serial / OpenMP / OpenCL).
- **For ca-geo:** the best small reference for a **conservative, adaptive-Δt flood CA**.
  The two-phase (edge flux → cell update) pattern fits GPU ping-pong buffers.

### SMODERP2D — HYD-05 (also WAT) (clone)

- Repo https://github.com/storm-fsv-cvut/smoderp2d, GPL-3.0, active (ČVUT). Has GRASS,
  ArcGIS and QGIS providers and a CLI.
- **Grid:** NumPy masked arrays on the DEM grid. Flow directions come from D8 or MFD
  (`flow_algorithm/`). Sheet flow and rill flow are separate states; streams are 1D
  reaches.
- **Update:** **explicit** with CFL control: `courant.py` adapts Δt so that the maximum
  Courant number stays within limits (including rill Courant numbers). An **implicit**
  variant (`do_next_h_implicit`) solves the step with `scipy.optimize.root`.
- **Mass:** a water balance per cell (rain − infiltration (Philip) − outflow + inflow);
  cumulative fields track volumes.
- **Tests:** reference outputs for quick tests (sheet, rill, stream, MFD, diffusion,
  implicit) and for GIS tests (Nučice, rain simulator), plus a 1D profile case. These make a
  strong **regression oracle**.
- **Clone note:** on Windows the checkout warns about case-only filename collisions in
  `tests/data/nucice/streams.CPG`/`.cpg`.

### SAGA "Cold Air Flow" (`sim_air_flow`) — ATM-02 (sparse clone)

- Mirror https://github.com/saga-gis/saga-gis (official repo on SourceForge). The file
  header says GPL-2.0-or-later; the mirror has no top-level licence file in the API.
- **State:** cold-air layer height per cell. The flowing surface is DEM + air height.
- **Neighbourhood:** Moore (8). Outflow is shared among lower neighbours in proportion to
  drop / distance, a multiple-flow-direction scheme.
- **Velocity:** from a gravity-current formula (√(g'·h/friction·sin slope)). Production
  (cold-air generation per hour) and friction can be constant or a grid.
- **Time step:** **adaptive, CFL-like**: Δt = delay × cell size / v_max. If nothing moves,
  Δt doubles.
- **Boundaries:** an option for open edges (air leaves the grid) or closed edges.
- **Parallelism:** OpenMP over rows, with a critical section for v_max.
- **For ca-geo:** the only open, readable cold-air flow model found. It is CA-like enough
  to share the WAT outflow-distribution machinery.

### Flow-Py / AvaFrame `com4FlowPy` — HAZ-02 (clone of Flow-Py v1.0)

- Flow-Py https://github.com/avaframe/FlowPy (GPL-3.0, archived). Continued as `com4FlowPy`
  in AvaFrame https://github.com/OpenNHM/AvaFrame (EUPL-1.2 ⚠ different licence for the
  successor).
- **Algorithm:** for each release cell (sorted by altitude) a list of `Cell` objects grows
  downhill. Each cell spreads flux to lower neighbours by a Holmgren-type weight
  (tan β)^exp combined with a persistence term. A **travel-angle energy line**
  (z_delta, α angle, capped by `max_z_delta`) stops the run-out. Below `flux_threshold`
  the process stops.
- **Update:** path-wise (graph traversal per release area) rather than a global synchronous
  step. It is deterministic, with no randomness.
- **Outputs:** max z_delta, flux, cell counts, travel angles, path lengths;
  back-calculation to infrastructure cells.
- **Parallelism:** `multiprocessing` over raster tiles (`split_and_merge.py`).
- **I/O:** ASCII / GeoTIFF; ini or GUI parameters. Example: `examples/dam`.
- **AvaFrame** ships many test avalanches (`avaframe/data/avaAlr`, `avaBowl`,
  `avaFlatPlane`, `avaInclinedPlane`, `avaHelix`, …) and analysis tests (`ana1Tests`). It is
  not cloned (repo 330 MB); it is the better oracle source.

### MOLASSES — HAZ-05 (clone)

- Repo https://github.com/geoscience-community-codes/MOLASSES, GPL-3.0, C.
- **Grid:** a 2D array of cell structs (elevation, effective elevation, residual, parent
  code), plus an **active-cell list** that grows as lava spreads.
- **Rule:** each active cell shares all lava above its residual thickness with lower
  non-parent neighbours (8-neighbourhood, `neighbor_8.c`) in proportion to slope. A 4-bit
  parent code stops back-flow.
- **Update:** volume is erupted in **pulses** at the vent; after each pulse the active list
  is processed until it is stable. This is an asynchronous / sequential order, not a
  synchronous CA.
- **Mass:** an explicit check that erupted volume equals volume on the grid within 1e-8.
- **Randomness:** residual, pulse and total volume drawn from uniform or log-normal ranges
  (bundled `ranlib`; the seed comes from a phrase). Multiple flows and runs make
  probabilistic hazard maps.
- **I/O:** GMT/GDAL grid DEM (`.grd`), vents file, key-value `molasses.conf`, ASCII flow
  map.
- **Test data:** Fagradalsfjall DEM + vents. The flat / dipping-plane test DEMs mentioned in
  `domains/geomorphology.md` were **not found** in this default-branch commit (to be
  verified in other branches / USF repo).
- **Clone note:** contains precompiled static libraries (`lib/*.a`), which are not used.

### SahulHumanSpread — EPI-04 (clone)

- Repo https://github.com/cjabradshaw/SahulHumanSpread, GPL-3.0, R scripts.
- **Grid:** R matrices / arrays (0.5°, about 86×87 cells × time layers). Carrying capacity
  K comes from NPP rasters interpolated over time. Islands and unreachable land are blocked
  as `NA`.
- **Update:** synchronous per generation. Demographic growth uses a Leslie matrix with
  stochastic survival and fertility (beta samplers). The proportion of emigrants depends on
  N/K. Emigrants go to neighbours weighted by K; long-distance dispersal is added.
- **Randomness:** many stochastic draws (beta, Poisson) with **no `set.seed`** found, so
  runs are not reproducible as published.
- **Script quality:** hard-coded local paths (`source("~/Documents/…")`); research script,
  not a package.
- **Data:** `CSV files.zip`, `TIF files.zip`, archaeological dates.

### dispeRse — EPI-04 (clone)

- Repo https://github.com/jgregoriods/dispeRse. The R `DESCRIPTION` says "MIT + file
  LICENSE"; the GitHub API reports NOASSERTION ⚠ (format only).
- **Grid:** flat arrays (`row*ncol+col`) for population, environment (K) and terrain, plus
  an arrival-time raster.
- **Update:** an **active-cell list (frontier)**. Each tick applies logistic growth, then
  "fission": a cell whose N exceeds a threshold of K sends migrants to free neighbours. With
  `accel` 2–4 it reaches cells 2–4 away (leapfrogging). Population is changed **in place**
  while iterating, so the result depends on order.
- **Randomness:** none in the core (deterministic). Terrain codes act as barriers or
  corridors.
- **For ca-geo:** a compact template for EPI-04 / EPI-05 front models with an arrival-time
  output. The packaged Europe NPP/terrain data plus dates support validation.

### PoPS Core — ECO-09 (clone)

- Repo https://github.com/ncsu-landscape-dynamics/pops-core (the old `…/PoPS` name now
  redirects here), GPL-2.0, header-only C++.
- **Grid:** templated `Raster` class with host pools, infected / susceptible / exposed
  counts and mortality cohorts.
- **Dispersal:** pluggable **kernels** (Cauchy, exponential, power law, log-normal, Weibull,
  von Mises direction, network kernel along roads/rails, deterministic kernel variants).
  Natural and anthropogenic kernels can be combined.
- **Scheduling:** a date and step scheduler (weekly / monthly / daily), with seasonality,
  lethal temperature and treatments / quarantine as separate actions.
- **Randomness:** `generator_provider.hpp` supplies separate seeded generators per process
  (dispersal, establishment, weather, …), so runs are reproducible.
- **Tests:** 27 C++ test files.
- **For ca-geo:** reference for a **kernel abstraction** and **multi-stream seeding**,
  shared by ECO-01 / ECO-03 / ECO-09.

### SLEUTH 3.0beta_p01 — LND-01 (downloaded source tarball)

- Official tarball https://www.ncgia.ucsb.edu/projects/gig/Dnload/SLEUTH3.0beta_p01.tar.gz.
  **No licence statement** for the SLEUTH files; only the bundled GD and whirlgif libraries
  carry their own notices ⚠.
- **Grid:** GIF rasters (urban by year, roads by year, slope, excluded, hillshade, land
  use), held in a grid-object memory manager.
- **Rule:** four growth phases with five coefficients (diffusion, breed, spread, slope
  resistance, road gravity): spontaneous, new spreading centre, edge, road-influenced.
  **Self-modification** adjusts the coefficients when growth booms or busts. The Deltatron
  handles land-use change.
- **Update:** a yearly step with Monte Carlo iterations; brute-force calibration over
  coefficient ranges (start / step / stop in the scenario file).
- **Randomness:** its own RNG (`random.c`), seeded by `RANDOM_SEED` in the scenario file,
  so runs are reproducible.
- **Test data:** demo50 / 100 / 200 inputs, scenario files for calibrate / test / predict /
  derive, and **expected outputs** (`Output/…/control_stats.log`, `avg.log`, yearly GIFs).
  This is a ready oracle.
- **Download note:** the tarball contains prebuilt binaries (`GD/libgd.a`, `GD/webgif`,
  `grow`); none were run.

### WebFlood — WAT, browser precedent (clone)

- Repo https://github.com/aeplay/WebFlood, MIT; bachelor thesis PDF included.
- **Engine:** WebGL 1 GPGPU through the GLOW.js wrapper. Float textures (`GL.FLOAT`) in
  ping-pong framebuffers (`flipFlopFBO.js`). Separate fragment-shader passes for
  advection, height update, velocity update, precipitation and damage. A **reduction
  shader** (`sum-down-water`) checks the total water volume, and an
  `encode-float` shader is used for read-back.
- **Scheme:** semi-Lagrangian shallow-water solver (not a CA) with fixed `dt` (0.01 by
  default).
- **I/O:** GeoTIFF / PNG DEM loading in the browser (`tiff.js`, `png.js`) and 16-bit TIFF
  writer. Scenarios are in `scenarios.json`.
- **Data:** dam-break (Fraccarollo–Toro 1995) terrain and water TIFFs, Iowa City, Lake
  Isabella.
- **For ca-geo:** the closest found precedent for our stack: texture ping-pong, a mass
  check by GPU reduction, and in-browser GeoTIFF loading. It is old (2018, WebGL 1), so
  it is a pattern reference only.

### Other implementations (brief)

- **GRASS `r.sim.water` / `r.sim.sediment`** (sparse clone): SIMWE path-sampling (Monte
  Carlo walkers) with OpenMP. Each walker has its **own counter-based random stream**
  derived from the seed and the walker index, so results do not depend on the number of
  threads. Its testsuite holds packed reference depth/discharge rasters (an oracle for
  pluvial runoff).
- **GRASS `r.ros` + `r.spread`** (sparse clone): Rothermel ROS rasters (base, max,
  direction) followed by elliptical spread with a **min-heap of ignition times**
  (Dijkstra-like) and optional spotting. This is the classic GIS event-queue fire model.
- **GRASS `r.cost` / `r.walk`**: cost-distance with anisotropic walking cost (Tobler-like
  / Aitken–Langmuir), with a test suite. AccessMod builds on a modified `r.walk`.
- **FUTURES `r.futures`** (sparse clone): patch-growing urban model with development
  pressure, demand and calibration modules; GRASS testsuites with data.
- **CellAutDisp** (clone): iterates a 3×3 weighted-average filter (SciPy
  `generic_filter`) whose weights depend on wind. A calibrated number of repeats replaces a
  time step; on-road emissions are re-injected each iteration. The repo also contains
  committed `.pyc` files and a built wheel (not used).
- **MPB-Infestation** (clone): hex grid via even/odd column offsets, absorbing boundary,
  Bernoulli inclusion / survival draws (`rbinom`). Experiment folders hold results.
- **IPS-UPS** (clone): NetLogo IBM (IPS-SPREADS) with ODD, an R metamodel
  (`Upscaling.R`, Moore neighbour rule), kappa results for 2017/2018.
- **Xylella-spread-model** (clone): annual stratified dispersal. The local spread is an
  **FFT convolution with an exponential kernel on a zero-padded domain** (no wrap-around),
  and jumps come from a Gaussian kernel seeded by a threshold.
- **chraibi/cellular_automata** (clone): Burstedde/Kirchner FFCA. Static floor field by
  BFS from exits, dynamic floor field with decay / diffusion, random sequential update by
  default with an optional parallel update. A teaching-quality reference for MOV-01.
- **FireDynamicsAutomata** (clone): small canvas JS demo of a probabilistic fire CA; no
  geodata.
- **ELMFIRE**: very useful verification set (elliptical shape, crown fire, spotting) and
  validation fires. The licence is AGPL-3.0 with a "Commons Clause" (no selling) and a
  separate commercial licence, so it is **not OSI-open**. Use its test definitions as
  concepts only.

## Local clones (`external/`)

All clones are shallow (`--depth 1`); sparse ones use `--filter=blob:none --sparse`.
Sizes include `.git`. Total ≈ 468 MB.

| Path | URL | Commit | Commit date | Size |
|---|---|---|---|---|
| `external/PyTorchFire` | https://github.com/xiazeyu/PyTorchFire | `591e8c3cda44b7d6d68ab6bed71eb945cdc67832` | 2026-09-24 | 38 MB |
| `external/propagator_sim` | https://github.com/CIMAFoundation/propagator_sim | `48b45078093692aa8dcca98f51849a5fbcd981a5` | 2026-09-01 | 5 MB |
| `external/Cell2Fire` | https://github.com/cell2fire/Cell2Fire | `b860bcc57757172d20371dd4cca93f0ad8a6c598` | 2026-05-14 | 201 MB |
| `external/FireDynamicsAutomata` | https://github.com/nramon/FireDynamicsAutomata | `8af79ed97fc085bc0aea568937fb6000d9851158` | 2021-01-10 | 1 MB |
| `external/caflood` | https://github.com/AlbertChenExeter/caflood | `0ef53a6c405eda7fa709a36db78ac69bec8f92ec` | 2018-04-08 | 1 MB |
| `external/WebFlood` | https://github.com/aeplay/WebFlood | `31569ef5d7bdd188f2b395950973c748a645241e` | 2018-09-04 | 76 MB |
| `external/grass-raster-sim` (sparse: `raster/r.ros`, `r.spread`, `r.spreadpath`, `r.sim`, `r.walk`, `r.cost`, `COPYING`) | https://github.com/OSGeo/grass | `ba898e78d725dce81c6218dac1ceffee7f93e29f` | 2026-10-12 | 6 MB |
| `external/smoderp2d` | https://github.com/storm-fsv-cvut/smoderp2d | `6eb1bcb80b1f2a0978fd460298630ccc52b96daf` | 2026-09-24 | 48 MB |
| `external/SahulHumanSpread` | https://github.com/cjabradshaw/SahulHumanSpread | `1d5ea70db7274d4b31cfbcc5f0ac9effbf55cf99` | 2021-10-06 | 22 MB |
| `external/dispeRse` | https://github.com/jgregoriods/dispeRse | `b0e638dfe5905a161cad04ce9325ac9a1ce536bf` | 2023-07-03 | 2 MB |
| `external/saga-gis-sim` (sparse: `saga-gis/src/tools/simulation/sim_air_flow`, `sim_geomorphology`) | https://github.com/saga-gis/saga-gis | `24b7957d0edf0689ac531b5ce6752a7a2c6acb41` | 2025-06-12 | 1 MB |
| `external/MPB-Infestation` | https://github.com/liu-yanjun-dev/MPB-Infestation | `6a3e5d40ab6dd2d59f2d32f1787de5c4ca657907` | 2025-03-11 | 1 MB |
| `external/IPS-UPS` | https://github.com/bwpietzsch/IPS-UPS | `2bcc22bc12b8b83b347871bd555887c2447bb126` | 2022-08-26 | 16 MB |
| `external/SLEUTH3.0beta_p01` (extracted tarball, not git) | https://www.ncgia.ucsb.edu/projects/gig/Dnload/SLEUTH3.0beta_p01.tar.gz | tarball SHA-256 `e82d82d5634bdcfb45249641633ada5ee4953f9d21398a64eef40370d3f21c7c` | downloaded 2026-10-13 | 16 MB |
| `external/grass-addons-futures` (sparse: `src/raster/r.futures`, `COPYING`) | https://github.com/OSGeo/grass-addons | `3fefb01103c12697298f30c698c86dca2ac06c65` | 2026-10-12 | 12 MB |
| `external/MOLASSES` | https://github.com/geoscience-community-codes/MOLASSES | `2f480a7c9a8a01d99b5425e8c5c4abe8736de463` | 2021-05-13 | 21 MB |
| `external/Xylella-spread-model` | https://github.com/drsmwhite/Xylella-spread-model | `418d31847f3235bd182fb9a982bc2461dd06e075` | 2016-11-18 | 1 MB |
| `external/pops-core` | https://github.com/ncsu-landscape-dynamics/pops-core | `e208dcb24c73270d70a0c2ec460675351d468738` | 2026-06-30 | 2 MB |
| `external/FlowPy` | https://github.com/avaframe/FlowPy | `27ad81d3e804e4e9d85a9773fca10ee7dc428183` | 2022-06-20 | 4 MB |
| `external/cellular_automata_pedestrians` | https://github.com/chraibi/cellular_automata | `67a8326a892e73c5b7d138382dfcb53392c80a56` | 2021-03-02 | 2 MB |
| `external/CellAutDisp` | https://github.com/TabeaSonnenschein/CellAutDisp | `d502e598b17ab48723c15c65700259c8eb30b5b1` | 2024-04-22 | 2 MB |

Not cloned, for size or licence reasons (record only): AvaFrame (330 MB repo), ELMFIRE
(315 MB, non-OSI licence), iLand (130 MB), LISFLOOD-FP 8.3 (Zenodo zip 70 MB, GPL-2.0),
tupi-expansion (162 MB), PLUS (723 MB, binaries only), Landlab (278 MB), RillGrow (no
licence on GitHub).

## Reference datasets

Downloaded to `data/reference/` (each folder has its own README). Total ≈ 107 MB.

| Folder | Source | Licence | Size | Model | Content |
|---|---|---|---|---|---|
| `ea-benchmark-lisflood-fp8/` | Zenodo 10.5281/zenodo.4661888, `ea4.zip` | CC BY 4.0 | 16.8 MB (≈1 GB unpacked, kept zipped) | WAT | EA Test 4 inputs (DEMs 0.5–10 m, par, bci/bdy) + LISFLOOD-FP ACC/DG2 outputs (stage series, depth snapshots, mass) |
| `pytorchfire-dataset/` | Mendeley Data 10.17632/nx2wsksp9k.1 | CC BY 4.0 | 94.6 MB | HAZ-01 | HDF5 targets of the paper (layout not inspected) + prediction-time CSV |
| `caesar-lisflood-parameters/` | Zenodo 10.5281/zenodo.6594745 | CC BY 4.0 | 29 KB | HYD-05 | Parameter sets of published CAESAR-Lisflood applications |

Test data inside clones (no duplicate download): SLEUTH demo50/100/200 with expected
outputs; SMODERP2D `tests/data` with reference outputs; GRASS `r.sim.water` /
`r.sim.sediment` testsuites; `r.futures` testsuites; Cell2Fire `data/` (11 landscapes);
PROPAGATOR `example/` (DEM, fuel, ignition geometries); PyTorchFire `examples/Bear_2020`;
MOLASSES `inputs/`; Flow-Py `examples/dam`; WebFlood `scenarios/` (dam break, Iowa, Lake
Isabella); dispeRse `data/*.rda`; SahulHumanSpread zipped CSV/TIF; IPS-UPS site data and
results.

Recorded only (not downloaded):

| Dataset | URL | Size | Model | Reason |
|---|---|---|---|---|
| EA Test 5 results (LISFLOOD-FP 8.0) | https://zenodo.org/records/4661888 (`ea5.zip`) | 72 MB zip / ≈7.9 GB unpacked | WAT | Outputs only, no input DEM; downloaded, inspected, deleted |
| Eden / Storm Desmond results | same record, `eden.zip` | 3.4 GB | WAT | Too large |
| LISFLOOD-FP 8.3 code | Zenodo 10.5281/zenodo.13121119 | 70 MB | WAT | Code archive, GPL-2.0 |
| DEMSIP dataset (Skinner & Coulthard) | Zenodo 10.5281/zenodo.7908491 | 157 MB (`.7z`) | HYD-05 | CC BY 4.0; larger than useful now |
| RillGrow + Eltner 2025 data | Zenodo 10.5281/zenodo.15576594 (code, 158 KB); OPARA 10.25532/OPARA-602 (data, size not checked) | – | HYD-05 | Next round |
| AvaFrame test avalanches | https://github.com/OpenNHM/AvaFrame/tree/master/avaframe/data | part of a 330 MB repo | HAZ-02 | EUPL-1.2; a sparse clone is possible later |
| ELMFIRE verification cases | https://github.com/lautenberger/elmfire (`verification/`, `validation/`) | part of a 315 MB repo | HAZ-01 | AGPL + Commons Clause |
| PLUS test data | `PLUS_test_data.rar` in HPSCIL/Patch-generating_Land_Use_Simulation_Model | repo 723 MB | LND-01 | No licence |
| Global friction / accessibility surfaces (`weiss2020global`) | Malaria Atlas Project, via `malariaAtlas` R package | global rasters, size not checked (large) | MOV-03 | Too large; clip later |
| Lava benchmarks (`dietterich2017benchmarking`) | paper 10.1186/s13617-017-0061-x | – | HAZ-05 | No separate data release found; benchmark values must be taken from the paper |
| Xylella / Tupi / Superhighways code archives | Zenodo 192974 / 4964642 / 7542562 | 0.1–12 MB | ECO-09 / EPI-04 | Same content as the GitHub repos |

## Licence compatibility notes (facts, no decision)

ca-geo has no licence yet. The facts that matter for that choice:

- **Permissive (MIT, BSD, Apache-2.0, public domain):** PyTorchFire, manoe/wildfire_ca
  (BSD-2), Xylella (MIT), dispeRse (MIT per DESCRIPTION), Fill–Spill–Merge (MIT), Landlab
  (MIT), malariaAtlas (MIT), WebFlood (MIT), lisyarus WebGPU SWE (MIT), emxsys/behave (MIT),
  GPU-Gang erosion (BSD-3), LANDIS-II BDA (Apache-2.0), firelab/behave and MODFLOW 6
  (US-Government public domain). Code from these can be adapted under any ca-geo licence,
  keeping the copyright / notice texts.
- **Weak copyleft (LGPL-3.0, EUPL-1.2):** AccessMod, OpenCAL, JuPedSim (LGPL-3.0); PROPAGATOR
  and AvaFrame (EUPL-1.2). EUPL-1.2 is copyleft for the covered work and lists GPL-2/3,
  LGPL, AGPL, MPL and others as compatible licences. Porting code (not just linking) into
  ca-geo would make that part EUPL/LGPL-covered.
- **Strong copyleft (GPL-2.0, GPL-3.0, GPL-2.0+):** Cell2Fire, C2F-W, GRASS (GPL-2.0+),
  SAGA tools (GPL-2.0+), LISFLOOD-FP (GPL-2.0), SMODERP2D, MOLASSES, SahulHumanSpread,
  tupi-expansion, FlowPy, PoPS (GPL-2.0 core, GPL-3.0 rpops), MDiG, MigClim, kissmig,
  CellAutDisp, iLand, FlowFill, RichDEM, chraibi FFCA (GPL-2.0), SCIARA CUDA (GPL-2.0).
  Translating their code into JavaScript would make a derivative work. If ca-geo is not
  GPL-compatible, these can serve **only as algorithm references**: re-implement from the
  paper or our own description, and do not translate the code line by line. "GPL-2.0-only"
  code (LISFLOOD-FP, pops-core, chraibi FFCA, SCIARA CUDA) is not compatible with GPL-3.0
  code in one combined work.
- **Network copyleft / non-OSI:** ELMFIRE (AGPL-3.0 + Commons Clause, commercial licence
  separately), Pyretechnics (free for non-commercial research, commercial licence
  otherwise), MrLavaLoba (custom licence), USF molasses (CC BY-NC 3.0). Do not reuse their
  code; test definitions can be cited as concepts.
- **No licence (all rights reserved by default):** SLEUTH 3.0 source, MPB-Infestation,
  IPS-UPS, PLUS / mcPLUS (binaries), RillGrow (GitHub), CAESAR-Lisflood (GitHub),
  acannistra/runout, Thru-Echoes/gridfire-ui. Reading them for understanding is fine; do
  not copy code. Data can be used only with permission or a separate licence.
- **Inconsistencies to keep in mind:** caflood (MIT LICENSE vs GPL-3 headers in `.ca`
  kernels); Cell2Fire (GPL-3.0 vs "For Research Use Only" description); RillGrow and
  CAESAR-Lisflood (no licence on GitHub, CC BY 4.0 on the Zenodo deposit; CC BY is not a
  software licence); Flow-Py GPL-3.0 vs AvaFrame EUPL-1.2; dispeRse (GitHub
  NOASSERTION vs MIT in DESCRIPTION); MDiG (GitHub NOASSERTION, GPL in COPYING).
- **Data:** the three downloaded datasets are CC BY 4.0, so they need attribution when
  redistributed or used in demos.

## Gaps

- **EPI-05 rabies front:** no implementation found (the URL of `smith2002predicting` is
  dead). EPI-04 tools (dispeRse, Sahul) cover the front mechanics.
- **ATM-02 cold-air pooling:** only SAGA Cold Air Flow is open. KLAM_21 is closed and the
  GPU model of `nowatschin2006gpubased` has no public code. There is no validation dataset
  with expected outputs.
- **HYD-09 groundwater:** the CA-specific code (FEST, HydroCAL) is either not reachable
  (chiselapp redirected, HTTP 302) or not public. Landlab's Dupuit percolator and MODFLOW
  can serve as non-CA oracles.
- **MOV-01 evacuation over terrain:** only generic or teaching FFCA code exists. There is no
  open implementation of terrain-based anisotropic evacuation (`wood2012anisotropic` used
  closed ArcGIS tools). There is also no open RiMEA/NIST test-data package for CA models.
- **HAZ-05 lava:** no downloadable benchmark dataset; the benchmark values are in the paper
  only. The SCIARA authors' code is not public (a third-party CUDA port exists).
- **LND-01:** SLEUTH has no licence; PLUS / FLUS are binary-only. FUTURES (GPL) is the only
  maintained open-source urban CA with tests.
- **ECO-01:** the bark-beetle CA code (MPB-Infestation, IPS-UPS) has no licence.
- **JavaScript / WebGL / WebGPU:** no geographic CA implementation of any selected model
  exists in JS with validation. The precedents are generic: WebFlood (WebGL 1 shallow
  water, 2018), lisyarus WebGPU virtual-pipes SWE (C++ host), WebGPU hydraulic-erosion
  demos, a canvas fire CA, and a JS Rothermel library (emxsys/behave). This confirms the
  catalogue's finding that no peer-reviewed in-browser geographic CA exists.

## Problems in this run

- GitHub search returns few hits for multi-word queries, so the search was repeated with
  shorter queries and language filters. Third-party student repos were skipped unless they
  were the only option.
- The PyTorchFire HDF5 layout was not inspected (no HDF5 reader, and no new tool was
  installed).
- Downloading the EA Test 5 archive showed that it holds results only; it was deleted.
  The Test 5 inputs remain to be found.
- The FEST repository could not be re-verified: chiselapp returned a redirect (HTTP 302).
