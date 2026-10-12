# Fire — literature survey

Survey round: 1 (breadth-first), date 2026-10-12. Scoring per ../reimplementability-criteria.md.

## Search log

Date of all searches: 2026-10-12.

**Note on sources.** OpenAlex was the primary search engine for the first queries. After the first batch it returned HTTP 429, because the free daily budget shared by the network IP was used up (it resets at midnight UTC). We did not use an API key. From that point on, every search and every metadata check went through **Crossref** (`api.crossref.org`), which the brief allows. Abstracts missing from Crossref came from the Semantic Scholar Graph API, and some from web-search snippets of publisher or repository pages. All bibliographic fields in this file (title, authors, year, venue, volume, pages, DOI) come from Crossref metadata.

| Query | Source | Hits | Notes |
|---|---|---|---|
| `cellular automata wildfire spread` (relevance search) | OpenAlex | 1290 | Top results sorted by citations were off-topic (reviews, SOC). Switched to a title+abstract filter. |
| `cellular automata wildfire` (title_and_abstract filter, sorted by citations) | OpenAlex | 209 | Core list: Alexandridis 2008, Freire 2019, PROPAGATOR, Trunfio, Ghisu, Millington, BorealFireSim. |
| `cellular automata forest fire spread` (title_and_abstract) | OpenAlex | 159 | Karafyllidis 1997, Yassemi, Hernández Encinas, Alexandridis 2011, Rui, Jiang (WUI), Sun 2021. |
| `cellular automaton fire spread Rothermel` (title_and_abstract) | OpenAlex | 0 | Rothermel coupling appears in full texts, not in abstracts. |
| `cellular automata urban fire` (title_and_abstract) | OpenAlex | 45 | Zhao 2011, Wang 2024/25 (post-earthquake), Tan 2019, Mahmoud 2017, Jiang 2021. |
| `cellular automata urban fire spread buildings earthquake` | OpenAlex | 377 | Mostly noise. |
| (8 queries: Drossel–Schwabl, Bak–Chen–Tang, percolation, Clarke, Cell2Fire, physical CA, Hargrove, stochastic CA) | OpenAlex | – | HTTP 429, daily budget exhausted. Repeated in Crossref. |
| `Drossel Schwabl self-organized critical forest-fire model` | Crossref | 5.95 M (ranked) | Drossel & Schwabl 1992 and follow-ups. |
| `Bak Chen Tang forest-fire model chaos` | Crossref | 7.75 M (ranked) | Bak, Chen & Tang 1990. |
| `Clarke Brass Riggan cellular automaton model of wildfire propagation and extinction` | Crossref | ranked | **Not found.** Listed as an unverified lead. |
| `Cell2Fire cell-based forest fire growth model` | Crossref | ranked | Pais et al. 2021. |
| `physical-based cellular automaton model for forest-fire propagation` | Crossref | ranked | Collin et al. 2011; Zheng 2017 (ELM-CA). |
| `Hargrove simulating fire patterns in heterogeneous landscapes` | Crossref | ranked | Hargrove et al. 2000 (EMBYR). |
| `PyTorchFire GPU-accelerated wildfire simulator differentiable cellular automata` | Crossref | ranked | Xia & Cheng 2025; EGU abstract. |
| `Ohgai cellular automata fire spread built-up areas` | Crossref | ranked | Ohgai 2007, Zhao 2011, Achtemeier 2013. |
| `Sullivan wildland surface fire spread modelling simulation and mathematical analogue models` | Crossref | ranked | Sullivan 2009, parts 1–3. |
| `Johnston Kelso Milne efficient simulation of wildfire spread on an irregular grid` | Crossref | ranked | Johnston 2008; Kelso 2015 (evaluation against historical fires). |
| `Berjak Hearne improved cellular automaton ... savanna` | Crossref | ranked | Berjak & Hearne 2002. |
| `Almeida Macau stochastic cellular automata model for wildland fire spread dynamics` | Crossref | ranked | Almeida & Macau 2011. |
| `Rothermel mathematical model for predicting fire spread in wildland fuels` | Crossref | ranked | Rothermel 1972 report (DOI 10.2737/int-rp-115). |
| `cellular automata fire spread anisotropy distortion fire shape elliptical` | Crossref | ranked | Few direct hits. Anisotropy papers were found through the Trunfio, Ghisu and Johnston queries. |
| `wildfire spread simulation Czech Republic` | Crossref | ranked | No CZ CA study found. |
| `Bohemian Switzerland 2022 wildfire` / `Kudlackova FlamMap ...` | Crossref | ranked | Kudláčková et al. 2024 (FlamMap, not CA) and the preprint. |
| `cellular automata wildfire Sardinia Mediterranean calibration` | Crossref | ranked | Trunfio 2004, Avolio 2012, Dunn & Milne 2004. |
| `post-earthquake fire spread simulation cellular automata` | Crossref | ranked | Meng & Zhao 2011, Lee & Davidson 2010 (physics-based, not CA). |
| `Trucchia ... PROPAGATOR` / `Perello ... Liguria` | Crossref | ranked | PROPAGATOR follow-ups (2022, 2024, 2025). |
| `propagator wildfire`, `cellular automata wildfire`, `cell2fire`, `urban fire spread cellular automata` | GitHub search API | 11 / 48 / 19 / 1 | Official repos for PROPAGATOR, Cell2Fire and PyTorchFire; third-party implementation of Alexandridis 2008 / Freire 2019. |
| `ti:cellular AND ti:automata AND ti:wildfire`, `ti:PyTorchFire` | arXiv API | 6 / 1 | PyTorchFire arXiv HTML full text read. |
| DOI lookups (about 45 DOIs) | Crossref, Semantic Scholar | – | Metadata verification and abstracts. |

## Model families

1. **Abstract forest-fire / percolation models (foundations).**
   - Cells are tree / empty / burning, on a square lattice with a von Neumann neighbourhood. Trees grow with probability p and lightning strikes with probability f.
   - These models study self-organised criticality, not real fires. They are a minimal teaching baseline and give the percolation-threshold intuition: below a critical occupancy fire dies, above it fire crosses the landscape.
   - Keys: `drossel1992selforganized`, `bak1990forestfire` (verified, not assessed), `almeida2011stochastic`, `hargrove2000simulating` (critical spread probability of about 0.25 on an 8-neighbour landscape).
2. **Stochastic "probability of burning" CA (Alexandridis family).**
   - Moore neighbourhood with states unburnable / unburnt / burning / burnt.
   - Spread probability is p_burn = p_h·(1+p_veg)·(1+p_den)·p_w·p_s, where wind and slope enter as exponential factors.
   - Run as ensembles, the model gives burn-probability maps. This is the most re-implemented family, with published parameter values and several open implementations.
   - Keys: `alexandridis2008cellular`, `alexandridis2011wildland`, `freire2019using` (Portugal, wind-driven non-local spread), `xia2025pytorchfire` (differentiable GPU version with gradient calibration), `trucchia2020propagator` and `perello2024cellular` (operational Italian system; adds rate-of-spread timing, moisture and fuel-to-fuel probability tables).
3. **Deterministic CA driven by a rate-of-spread model (fractional-area / ROS CA).**
   - Each cell accumulates burned fraction or arrival time from a 1-D spread-rate model (Rothermel, Canadian FBP, Wang Zhengfei, etc.), applied along the 8 (or more) directions.
   - Keys: `karafyllidis1997model` (fractional burned area), `berjak2002improved` (adds Rothermel), `yassemi2008design` (GIS-CA with FBP, Canada), `rui2018forest` and `sun2021adaptive` (Chinese ROS model, time-step choice, adaptive step), `millington2009modelling` (fire CA inside a Mediterranean fire–succession model, Spain).
   - Context for the spread-rate sub-model: `rothermel1972mathematical`.
4. **Correcting grid anisotropy / fire-shape distortion.**
   - On a square grid with 8 neighbours, simulated fires become octagonal or diamond-shaped, and the shape depends on wind direction relative to the grid.
   - Remedies: spread directions not tied to lattice angles (`trunfio2011new`), velocity correction factors found by optimisation (`ghisu2015optimal`, `ghisu2015improved`), an irregular (randomised) grid with discrete-event simulation (`johnston2008efficient`), and per-cell elliptical spread with arrival-time messages (`pais2021cell2fire`).
5. **Cell-based operational simulators with open code.**
   - Keys: `pais2021cell2fire` (C++/Python, FBP, GPL-3.0), `trucchia2020propagator` (Python/Numba, EUPL-1.2), `xia2025pytorchfire` (PyTorch, MIT). These are the most directly reusable sources.
6. **Urban and wildland–urban interface (WUI) fire spread.**
   - Cells are buildings or building-scale grid cells. The rules combine within-building fire stages with building-to-building spread through distance, wind, material and firebrands.
   - Keys: `ohgai2007cellular` (Japan, community planning), `zhao2011simulation` (irregular coarse cells = buildings, Kobe 1995), `wang2025procedure` (post-earthquake damage feeding a CA, Kobe 1995), `tan2019fire` (probabilistic CA, Philippine informal settlements, accuracy and kappa reported), `jiang2021modelling` (heterogeneous CA coupling forest and house sub-models, California WUI), `mahmoud2017probabilistic` (WUI framework).
7. **Reviews and context.**
   - `sullivan2009wildland`: review of simulation and analogue spread models, including CA.
   - `kudlackova2024using`: FlamMap reconstruction of the 2022 Bohemian Switzerland fire. It is the main CZ calibration reference, but it does not use a CA.

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| `xia2025pytorchfire` | 2025 | PyTorchFire | wildfire, California | square 30 m / Moore / 3 states / stoch., differentiable | 2 2 2 2 2 | 10 | A | yes (MIT) | OA | full text (arXiv) |
| `trucchia2020propagator` | 2020 | PROPAGATOR | wildfire, Italy/Spain | square (20 m default) / Moore / stoch. + ROS timing | 2 2 2 2 1 | 9 | A | yes (EUPL-1.2) | OA | abstract + source code/docs |
| `alexandridis2008cellular` | 2008 | CA forest fire, Spetses 1990 | wildfire, Greece | square / Moore / 4 states / stoch. | 2 2 1 2 1 | 8 | B | third-party (BSD, MIT) | OA (publisher) | secondary full texts (Freire 2019, Xia 2025) + code |
| `freire2019using` | 2019 | CA wildfire, Tavira 2012 | wildfire, Portugal | square 100 m / Moore + wind-aligned non-local / 4 states / stoch. | 1 2 1 2 2 | 8 | B | third-party (BSD) | OA | full text |
| `pais2021cell2fire` | 2021 | Cell2Fire | wildfire, Canada | square 100 m / 8 neigh. / elliptical ROS, msg passing / det. | 2 2 2 1 2 | 9 | A | yes (GPL-3.0) | OA | full text |
| `perello2024cellular` | 2024 | PROPAGATOR prescribed fire, Liguria | wildfire + prescribed burns, Italy | as PROPAGATOR | 1 1 2 1 1 | 6 | C | yes (PROPAGATOR) | OA | abstract (provisional) |
| `rui2018forest` | 2018 | CA forest fire, time step | wildfire, NE China | square / 8 neigh. / ROS-driven / det. | 1 1 0 1 2 | 5 | C | not found | paywall | abstract (provisional) |
| `sun2021adaptive` | 2021 | Adaptive time-step CA | wildfire, Sichuan | square / 8 neigh. / ROS-driven, adaptive Δt / det. | 1 1 0 1 2 | 5 | C | not found | OA | abstract (provisional) |
| `tan2019fire` | 2019 | Probabilistic CA urban fire, Cebu | urban settlement fire, Philippines | square / neigh. n/s / prob. (wind, material, density) | 1 1 0 1 2 | 5 | C | not found | OA | abstract (provisional) |
| `ghisu2015optimal` | 2015 | Optimal CA (correction factors) | wildfire, anisotropy | square / extended neigh. / ROS / det. | 1 1 0 2 1 | 5 | C | not found | paywall | abstract (provisional) |
| `ghisu2015improved` | 2015 | Improved CA (Procedia) | wildfire, anisotropy | as above | 1 1 0 2 1 | 5 | C | not found | OA | abstract (provisional) |
| `almeida2011stochastic` | 2011 | Stochastic CA, critical line | abstract wildland fire | square / neigh. n/s / 3 states / stoch. | 1 1 0 2 1 | 5 | C | not found | OA | abstract (provisional) |
| `drossel1992selforganized` | 1992 | SOC forest-fire model | abstract (SOC) | square / von Neumann / 3 states / stoch. | 1 1 0 2 1 | 5 | C | not found (trivial) | paywall | abstract + encyclopedic description |
| `hargrove2000simulating` | 2000 | EMBYR | large fires, Yellowstone | square / Moore + firebrands / stoch. | 1 1 0 1 1 | 4 | C | not found | OA (Treesearch, not read) | abstract (provisional) |
| `yassemi2008design` | 2008 | GIS-CA fire behaviour | wildfire, Alberta | square / neigh. n/s / FBP ROS / det. | 1 1 0 1 1 | 4 | C | not found | preprint (SFU, not read) | abstract (provisional) |
| `alexandridis2011wildland` | 2011 | CA Parnitha 2007 + suppression | wildfire, Greece | square / Moore / stoch. + spotting, air tankers | 1 1 0 1 1 | 4 | C | not found | OA | abstract (provisional) |
| `johnston2008efficient` | 2008 | Irregular grid, DES | wildfire, anisotropy | irregular grid / Voronoi-like neigh. / discrete-event / det. | 1 1 0 1 1 | 4 | C | not found (Australis closed) | paywall | abstract (provisional) |
| `trunfio2011new` | 2011 | New CA algorithm (free directions) | wildfire, anisotropy | square / neigh. n/s / det. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| `millington2009modelling` | 2009 | Mediterranean fire–succession LFSM | fire regime + succession, Spain | square / neigh. n/s / fire CA + rule-based succession / stoch. | 1 1 0 1 1 | 4 | C | not found | preprint (Durham) | abstract (provisional) |
| `jiang2021modelling` | 2021 | Heterogeneous CA, WUI | WUI fire, California | heterogeneous cells (forest/house) / stoch.? | 1 1 0 1 1 | 4 | C | not found | OA | abstract (provisional) |
| `wang2025procedure` | 2025 | Post-earthquake urban fire CA | post-earthquake fire, Kobe | building-based CA / stoch.? | 1 1 0 1 1 | 4 | C | not found | preprint (Research Square) | abstract (provisional) |
| `zhao2011simulation` | 2011 | Irregular coarse CA, mass fire | urban mass fire, Kobe | irregular cells = buildings / 5 fire stages / 2 spread patterns / stoch. | 1 0 0 1 1 | 3 | D | not found | paywall | abstract (provisional) |
| `mahmoud2017probabilistic` | 2017 | Probabilistic CA WUI framework | WUI fire | grid / convection + embers / stoch. | 1 1 0 1 0 | 3 | D | not found | OA | abstract (provisional) |
| `karafyllidis1997model` | 1997 | CA forest fire (fractional area) | wildfire, hypothetical | square / Moore / continuous burned fraction / det. | 1 0 0 1 1 | 3 | D | not found | paywall | metadata + secondary descriptions (provisional) |
| `berjak2002improved` | 2002 | Improved CA, savanna (Rothermel) | savanna fire, S. Africa | square / Moore / fractional area + Rothermel / det. | 1 0 0 1 0 | 2 | D | not found | paywall | metadata + secondary descriptions (provisional) |
| `ohgai2007cellular` | 2007 | CA fire spread in built-up areas | urban fire, Japan | building-scale grid / n/s | 0 0 0 1 0 | 1 | D | not found | paywall | metadata + grant summary (provisional) |
| `sullivan2009wildland` | 2009 | Review: simulation & analogue models | review | – | n/a | – | n/a | – | paywall | abstract |
| `rothermel1972mathematical` | 1972 | Rothermel spread model | fire behaviour (1-D ROS) | – (sub-model for CA) | n/a | – | n/a | R package exists (not checked) | OA (USFS report) | metadata |
| `kudlackova2024using` | 2024 | FlamMap, Bohemian Switzerland 2022 | wildfire, CZ (not CA) | – | n/a | – | n/a | – | preprint OA | abstract |

"n/s" means not stated in the material we read.

## Entries

### xia2025pytorchfire — PyTorchFire: A GPU-accelerated wildfire simulator with Differentiable Cellular Automata
- **Citation:** Xia, Z., Cheng, S. (2025). PyTorchFire: A GPU-accelerated wildfire simulator with Differentiable Cellular Automata. *Environmental Modelling & Software* 188, 106401. DOI: 10.1016/j.envsoft.2025.106401 (verified: Crossref)
- **Access:** OA (CC BY); preprint at arXiv 2502.18738.
- **Phenomenon and study area:** Wildfire spread. Simulated and real California fires: Bear 2020, Brattain 2020, Pier 2017.
- **Model:**
  - Square cells of 30 m with a Moore neighbourhood. States are burnable, burning and burned, stored as two boolean channels.
  - Spread follows the Alexandridis probability p_h·(1+p_veg)·(1+p_den)·p_w·p_s. Wind and slope enter as exponential factors, and the product is squashed with a tanh to keep it below 1.
  - A cell's ignition probability combines all burning neighbours as 1 − ∏(1−p_i).
  - A burning cell keeps burning with probability p_continue.
  - Synchronous discrete steps; one step was 0.8–1.6 h in the experiments. Spotting is handled as new ignitions.
  - For gradient calibration, the random draws are kept but gradients flow through the ignition probabilities.
- **Inputs:** LANDFIRE canopy bulk density and cover (vegetation and density factors), LANDFIRE slope, ERA5-Land 10 m wind, and MODIS active-fire detections as targets.
- **Parameters:** Four calibrated parameters (p_h, a, c1, c2) plus a fixed p_continue. Default values are in the code. Calibration uses AdamW on a BCE plus pooled-MSE loss, and is fully described.
- **Code:** https://github.com/xiazeyu/PyTorchFire (MIT, verified 200); PyPI `pytorchfire` (verified); dataset https://data.mendeley.com/datasets/nx2wsksp9k/1 (verified). The Zenodo code DOI returned a 504 when checked.
- **Validation:** Jaccard index and Manhattan distance of burned-area time series. Tables give uncalibrated, calibrated and target Jaccard values per map and scale (for example, calibrated 0.73–0.91 on simulated targets).
- **Reimplementability:** S1 2 – rules, equations and update scheme stated, plus code; S2 2 – calibration procedure and defaults; S3 2 – open repository; S4 2 – open US data and a published dataset, and the model runs on generic vegetation/slope/wind rasters; S5 2 – quantitative tables → **10, A**. Assessed from: full text (arXiv HTML).
- **Browser fit:** Very good. The forward model is a few array operations per step, so a WebGL/WebGPU or plain-JS port is straightforward. Gradient calibration could be dropped or replaced by a simple search.
- **Relevance to ca-geo:** HAZ-01 core candidate: a modern, clean statement of the Alexandridis rule with test cases. Its calibration idea (fit p_h, c1, c2, a against a real perimeter) could be applied to the 2022 Bohemian Switzerland fire.

### trucchia2020propagator — PROPAGATOR: An Operational Cellular-Automata Based Wildfire Simulator
- **Citation:** Trucchia, A., D'Andrea, M., Baghino, F., Fiorucci, P., Ferraris, L., Negro, D., Gollini, A., Severino, M. (2020). PROPAGATOR: An Operational Cellular-Automata Based Wildfire Simulator. *Fire* 3(3), 26. DOI: 10.3390/fire3030026 (verified: Crossref)
- **Access:** OA (MDPI). The publisher page blocked automated fetching, so the full text was not read.
- **Phenomenon and study area:** Wildfire spread for civil protection, tested on past Mediterranean fires in Italy and Spain.
- **Model:**
  - Stochastic CA. Spread probability depends on the fuel class of the burning cell and the target cell, through a fuel-to-fuel probability matrix in the code. It is modulated by wind, slope and dead fine fuel moisture.
  - The propagation time per cell comes from a rate-of-spread model. The current code defaults to "wang" and also offers "rothermel".
  - Runs are many independent realisations, and the output is a per-cell burn-probability map at each time step.
  - Firebreaks and fire-fighting actions can be imposed.
  - The current code adds an ember-spotting model and a front-tracking scheduler.
- **Inputs:** DEM, a vegetation/fuel raster (7 legacy classes such as broadleaves, shrubs, non-vegetated…), wind speed/direction, moisture, and ignition points. The code repository includes a script that downloads Italian national data.
- **Parameters:** A full table in the code (`constants.py`): nominal ROS v0, dead/live fuel load, heating value, moisture, and a per-class spread-probability matrix. The wind/slope/moisture constants are in `functions.py`. Default cell size is 20 m with 100 realisations.
- **Code:** https://github.com/CIMAFoundation/propagator_sim (EUPL-1.2, Python/Numba, verified 200). There is also a third-party QGIS plugin (GiorgioMeschi/propagator-qgis-plugin, not checked).
- **Validation:** Agreement with real burned areas for several past fires, reported in the abstract. Metrics were not seen.
- **Reimplementability:** S1 2 – complete logic available in the documented open code (the paper itself was not read); S2 2 – full parameter tables in code; S3 2; S4 2 – generic DEM plus fuel classes that map from CORINE-type land cover; S5 1 – comparisons with real fires, but metrics not verified → **9, A**. Assessed from: abstract + source code/docs.
- **Browser fit:** Good. It was designed for speed. Ensembles of about 100 realisations on a regional grid are feasible in a Web Worker or on the GPU.
- **Relevance to ca-geo:** HAZ-01 strongest European operational reference. Its fuel classes match Mediterranean/European land cover, and its probability-map output fits a demo. It could be paired with ATM-01 (smoke) and MOV-01 (evacuation).

### alexandridis2008cellular — A cellular automata model for forest fire spread prediction: The case of the wildfire that swept through Spetses Island in 1990
- **Citation:** Alexandridis, A., Vakalis, D., Siettos, C.I., Bafas, G.V. (2008). A cellular automata model for forest fire spread prediction: The case of the wildfire that swept through Spetses Island in 1990. *Applied Mathematics and Computation* 204(1), 191–201. DOI: 10.1016/j.amc.2008.06.046 (verified: Crossref)
- **Access:** OA according to the earlier OpenAlex record. Publisher pages blocked automated fetching.
- **Phenomenon and study area:** Wildfire on Spetses island, Greece, 1990.
- **Model:** As restated in full texts by Freire & DaCamara (2019) and Xia & Cheng (2025):
  - Square grid with a Moore neighbourhood. States are no fuel, unburnt fuel, burning and burnt.
  - A burning cell burns out in one step and ignites each unburnt neighbour with p_burn = p_h·(1+p_veg)·(1+p_den)·p_w·p_s.
  - Wind factor p_w = exp(c1·V)·exp(c2·V·(cos θ − 1)). Slope factor p_s = exp(a·θ_s), with θ_s computed from the elevation difference and the cell distance.
  - Synchronous update.
- **Inputs:** Vegetation type and density maps, DEM, and wind speed/direction.
- **Parameters:** p_h = 0.58, a = 0.078, c1 = 0.045, c2 = 0.131, as quoted by Freire 2019, together with vegetation-type and density loadings.
- **Code:** No official code. Third-party open implementations: https://github.com/manoe/wildfire_ca (C++, BSD-2-Clause, verified 200; also implements Freire 2019), https://github.com/XC-Li/Parallel_CellularAutomaton_Wildfire (verified 200, not inspected), and PyTorchFire.
- **Validation:** Comparison with the observed Spetses fire. Details unread.
- **Reimplementability:** S1 2 – complete rule available via two independent full-text restatements and code; S2 2 – full parameter set published; S3 1 – third-party open code only, no author code (harmonised rule); S4 2 – runs on generic land-cover, DEM and wind layers; S5 1 – only qualitative fit known → **8, B**. Assessed from: secondary full texts (Freire 2019, Xia 2025) and code. The original paper was not read, so scores are provisional on the original.
- **Browser fit:** Excellent. It is the simplest geographic fire CA.
- **Relevance to ca-geo:** HAZ-01 baseline rule. URB-03 could reuse the same probability form with building material in place of vegetation.

### freire2019using — Using cellular automata to simulate wildfire propagation and to assist in fire management
- **Citation:** Freire, J.G., DaCamara, C.C. (2019). Using cellular automata to simulate wildfire propagation and to assist in fire management. *Natural Hazards and Earth System Sciences* 19(1), 169–179. DOI: 10.5194/nhess-19-169-2019 (verified: Crossref)
- **Access:** OA, https://nhess.copernicus.org/articles/19/169/2019/
- **Phenomenon and study area:** The 2012 Tavira fire, Algarve, Portugal, which burned about 24,800 ha.
- **Model:**
  - The Alexandridis CA on 100 m cells with 4 states.
  - New rule: when wind at the burning cell exceeds 8 m/s and the spread direction lies within π/10 of the wind, fire also jumps to further cells along that direction. The reach grows with wind speed, up to about 10 cells.
  - One time step is about 20 min, derived from the observed duration.
  - Ensembles of 100 runs, in constrained and unconstrained modes.
- **Inputs:** SRTM DEM; WRF winds downscaled with WindNinja; CORINE 2006, forest inventory and MODIS green vegetation fraction, aggregated to 4 vegetation types × 4 density classes. Roads and water lines get negative loadings.
- **Parameters:** All given (p0, a, c1, c2, a loadings table) plus a sensitivity test on c1 and c2.
- **Code:** No author code. Third-party https://github.com/manoe/wildfire_ca (verified).
- **Validation:** Burned fraction against the scar across probability thresholds, and bias and RMSD of simulated against MODIS-derived burn time. Bias improved from 8.3 h to −4.4 h and RMSD from 12.9 h to 7.1 h.
- **Reimplementability:** S1 1 – some ambiguities: the number of cells reached at a given wind speed is not exact, and the diagonal distance is stated oddly; S2 2; S3 1 (third-party only, harmonised rule); S4 2 – CORINE and SRTM are open; S5 2 → **8, B**. Assessed from: full text.
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** HAZ-01 EU case with CORINE-based fuel loadings, directly transferable to CZ CORINE/Urban Atlas. The road and water firebreak loadings are a nice demo feature.

### pais2021cell2fire — Cell2Fire: A Cell-Based Forest Fire Growth Model to Support Strategic Landscape Management Planning
- **Citation:** Pais, C., Carrasco, J., Martell, D.L., Weintraub, A., Woodruff, D.L. (2021). Cell2Fire: A Cell-Based Forest Fire Growth Model to Support Strategic Landscape Management Planning. *Frontiers in Forests and Global Change* 4, 692706. DOI: 10.3389/ffgc.2021.692706 (verified: Crossref)
- **Access:** OA.
- **Phenomenon and study area:** Wildfire growth in Canadian landscapes, including the Dogrib fire, and harvest planning.
- **Model:**
  - Square cells, 100 m in the experiments. A cell ignites when fire reaches its centre.
  - Each burning cell defines an ellipse from head, flank and back ROS, computed with the Canadian FBP system. It sends "burn" messages to up to 8 neighbours.
  - Fixed time step (1 min in the experiments). Optional intensity threshold. Burning stops when no neighbours are available or fuel runs out.
- **Inputs:** Fuel type raster (FBP codes), elevation, slope/aspect, grass curing, an hourly weather stream with FWI indices, and ignition points.
- **Parameters:** Fire behaviour comes from the published FBP equations and fuel types. User inputs are landscape and weather.
- **Code:** https://github.com/cell2fire/Cell2Fire (GPL-3.0, verified 200). Derivatives: https://github.com/fire2a/C2F-W (Scott & Burgan and Kitral fuel systems, verified 200).
- **Validation:** Against the Prometheus simulator, using 1−MSE, SSIM and Frobenius norm. For example, Dogrib: SSIM about 0.88, accuracy about 0.92.
- **Reimplementability:** S1 2; S2 2 – FBP published; S3 2; S4 1 – FBP fuel types are Canadian, so CZ use needs a fuel mapping (the C2F-W variant with Scott & Burgan fuels eases this); S5 2 → **9, A**. Assessed from: full text.
- **Browser fit:** Good for single fires. FBP equations are lengthy but closed-form.
- **Relevance to ca-geo:** HAZ-01 reference for "ROS + elliptical spread on a grid", which is the main anisotropy-reducing design. Its Scott & Burgan variant links to the fuel models used by Kudláčková 2024 (FlamMap).

### perello2024cellular — Cellular automata-based simulators for the design of prescribed fire plans: the case study of Liguria, Italy
- **Citation:** Perello, N., Trucchia, A., Baghino, F., Asif, B.S., Palmieri, L., Rebora, N., Fiorucci, P. (2024). Cellular automata-based simulators for the design of prescribed fire plans: the case study of Liguria, Italy. *Fire Ecology* 20(1), 7. DOI: 10.1186/s42408-023-00239-7 (verified: Crossref)
- **Access:** OA (SpringerOpen). The fetch was blocked by a cookie wall, so the full text was not read.
- **Phenomenon and study area:** Liguria, Italy. Reconstruction of the largest 2022 regional fire, then a Monte Carlo evaluation of candidate prescribed-burn areas.
- **Model:** PROPAGATOR (see `trucchia2020propagator`).
- **Inputs:** Regional fuel maps, DEM and weather scenarios (details not read).
- **Parameters:** Probably PROPAGATOR defaults plus regional fuel loads (not verified).
- **Code:** PROPAGATOR repository (verified).
- **Validation:** Historical-fire reconstruction and scenario statistics.
- **Reimplementability:** S1 1, S2 1, S3 2, S4 1, S5 1 → **6, C**. Assessed from: abstract (provisional).
- **Browser fit:** Same as PROPAGATOR.
- **Relevance to ca-geo:** HAZ-01 "what-if" demo idea: fuel treatment or clearing scenarios, parallel to Kudláčková's dead-spruce removal scenario in CZ. Also linked to L2 (bark beetle → fire).

### rui2018forest — Forest fire spread simulation algorithm based on cellular automata
- **Citation:** Rui, X., Hui, S., Yu, X., Zhang, G., Wu, B. (2018). Forest fire spread simulation algorithm based on cellular automata. *Natural Hazards* 91(1), 309–319. DOI: 10.1007/s11069-017-3127-5 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** 2006 fire in the Daxing'anling mountains, NE China.
- **Model:** CA combined with an existing ROS model. The key finding concerns the time step: the optimal Δt is about one-eighth of the cell burn-out time.
- **Inputs:** Fuel, terrain, weather; Landsat TM burned area as reference.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** Mean kappa 0.635 and accuracy 87.9% against Landsat TM.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 practical rule of thumb for choosing Δt in ROS-driven CA.

### sun2021adaptive — Adaptive Forest Fire Spread Simulation Algorithm Based on Cellular Automata
- **Citation:** Sun, L., Xu, C., He, Y., Zhao, Y., Xu, Y., Rui, X., Xu, H. (2021). Adaptive Forest Fire Spread Simulation Algorithm Based on Cellular Automata. *Forests* 12(11), 1431. DOI: 10.3390/f12111431 (verified: Crossref)
- **Access:** OA (MDPI blocked automated fetching).
- **Phenomenon and study area:** 2020 fire in Mianning County, Sichuan, China.
- **Model:** ROS-driven CA with an adaptive time step. A "speed change rate" index, computed from weather and local conditions, sets Δt.
- **Inputs:** Weather, terrain, fuel.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** Accuracy 96.9%, kappa 0.62.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 adaptive-step idea for animations, so that playback does not stall in slow phases.

### tan2019fire — Fire spread prediction using probabilistic cellular automata: the case of urban settlements in the Philippines
- **Citation:** Tan, E.E., Vicente, A.J. (2019). Fire Spread Prediction Using Probabilistic Cellular Automata: The Case of Urban Settlements in the Philippines. *The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences* XLII-4/W19, 415–420. DOI: 10.5194/isprs-archives-xlii-4-w19-415-2019 (verified: Crossref)
- **Access:** OA (PDF; automated text extraction failed).
- **Phenomenon and study area:** Fires in dense urban settlements, Cebu, Philippines.
- **Model:** Probabilistic CA over a GIS grid. Ignition probability depends on wind, building material and building density.
- **Inputs:** Building footprints and materials, wind.
- **Parameters:** Probably given (not read).
- **Code:** not found. A web tool is mentioned.
- **Validation:** Accuracy 83.5%, Cohen's kappa 0.67 against past fires.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Very good. Small grids.
- **Relevance to ca-geo:** URB-03 closest template: material-dependent, wind-driven building-to-building fire. Worth a full-text read in round 2.

### ghisu2015optimal — An optimal Cellular Automata algorithm for simulating wildfire spread
- **Citation:** Ghisu, T., Arca, B., Pellizzaro, G., Duce, P. (2015). An optimal Cellular Automata algorithm for simulating wildfire spread. *Environmental Modelling & Software* 71, 1–14. DOI: 10.1016/j.envsoft.2015.05.001 (verified: Crossref)
- **Access:** paywall. Repository records exist at CNR and UniCA IRIS, but were not accessible.
- **Phenomenon and study area:** Wildfire shape distortion. Homogeneous tests, then a FARSITE comparison with slope and wind (Sardinia group).
- **Model:** Raster CA in which the vector-model spread velocities (elliptical, Rothermel-type) are multiplied by direction-dependent correction factors. The factors are found by tabu-search optimisation, so that CA fire shapes match ideal ellipses.
- **Inputs:** Fuel, DEM, wind.
- **Parameters:** Correction factors, probably tabulated (not verified).
- **Code:** not found.
- **Validation:** Shape accuracy against two CA simulators and FARSITE.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2 (homogeneous tests need no data), S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01. If the correction-factor table is in the paper, it is a cheap fix for octagonal fire shapes. Priority full-text target.

### ghisu2015improved — An Improved Cellular Automata for Wildfire Spread
- **Citation:** Ghisu, T., Arca, B., Pellizzaro, G., Duce, P. (2015). An Improved Cellular Automata for Wildfire Spread. *Procedia Computer Science* 51, 2287–2296. DOI: 10.1016/j.procs.2015.05.388 (verified: Crossref)
- **Access:** OA (ScienceDirect blocked automated fetching).
- **Phenomenon and study area:** Same approach as `ghisu2015optimal`: velocity redefinition with correction factors and numerical optimisation, compared with two CA simulators.
- **Model / Inputs / Parameters:** As above.
- **Code:** not found.
- **Validation:** Shape comparison.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** The OA short version, the easiest route to the correction-factor method.

### almeida2011stochastic — Stochastic cellular automata model for wildland fire spread dynamics
- **Citation:** Almeida, R.M., Macau, E.E.N. (2011). Stochastic cellular automata model for wildland fire spread dynamics. *Journal of Physics: Conference Series* 285, 012038. DOI: 10.1088/1742-6596/285/1/012038 (verified: Crossref)
- **Access:** OA (PDF text not extractable).
- **Phenomenon and study area:** Abstract wildland fire on flat terrain with no wind.
- **Model:**
  - Three states: vegetation, burning, burnt.
  - An effective spread probability combines three probabilities: vegetation proportion, burn-out probability, and neighbour-spread probability.
  - Monte Carlo simulation finds a critical line in parameter space separating propagating from non-propagating fires.
- **Inputs:** None (synthetic lattice).
- **Parameters:** Three probabilities, explored by parameter sweeps.
- **Code:** not found.
- **Validation:** Phase diagram (critical line).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** HAZ-01 didactic mode: a "percolation threshold" slider before switching to real data.

### drossel1992selforganized — Self-organized critical forest-fire model
- **Citation:** Drossel, B., Schwabl, F. (1992). Self-organized critical forest-fire model. *Physical Review Letters* 69(11), 1629–1632. DOI: 10.1103/physrevlett.69.1629 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Abstract self-organised criticality, with no geographic setting.
- **Model:**
  - Cells are empty, tree or burning, on a square lattice with a von Neumann neighbourhood.
  - Synchronous rules: burning → empty; a tree with a burning neighbour → burning; a tree ignites spontaneously with probability f; an empty cell grows a tree with probability p.
  - Criticality appears as f → 0 with time-scale separation f ≪ p.
- **Inputs:** none.
- **Parameters:** p and f (the ratio p/f controls behaviour).
- **Code:** no official code. The rules are trivial to implement.
- **Validation:** Scaling laws and critical exponents (values not seen).
- **Reimplementability:** S1 1 (the rules are completely known from the abstract and an encyclopedic description, but the paper itself was not read, so capped at 1), S2 1, S3 0, S4 2, S5 1 → **5, C**. Assessed from: abstract + encyclopedic description. A full read would very likely give S1 2.
- **Browser fit:** Excellent. A classic WebGL demo.
- **Relevance to ca-geo:** HAZ-01 / ECO-02 "fire regime" teaching model: frequency–area power laws. Millington 2009 uses the same power-law exponent for calibration.

### hargrove2000simulating — Simulating fire patterns in heterogeneous landscapes
- **Citation:** Hargrove, W.W., Gardner, R.H., Turner, M.G., Romme, W.H., Despain, D.G. (2000). Simulating fire patterns in heterogeneous landscapes. *Ecological Modelling* 135(2–3), 243–263. DOI: 10.1016/s0304-3800(00)00368-9 (verified: Crossref)
- **Access:** OA via USDA Treesearch, according to catalogue records. Not read.
- **Phenomenon and study area:** Large fires on the subalpine plateau of Yellowstone NP (the EMBYR model).
- **Model:**
  - Each burning cell independently tries to ignite its 8 neighbours with a probability that depends on fuel type, fuel moisture and wind.
  - Firebrands are distributed to downwind cells.
  - The critical spread probability for crossing the landscape by adjacent spread alone is about 0.25. Firebrands speed up spread about 4×, and about 8× with moderate wind.
- **Inputs:** Fuel map, weather/moisture scenarios.
- **Parameters:** Scenario tables (not read).
- **Code:** not found.
- **Validation:** Area-burned distributions per scenario.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional). The OA full text could raise S1, S2 and S5.
- **Browser fit:** Very good.
- **Relevance to ca-geo:** HAZ-01 landscape-scale stochastic fire with spotting. A second-round full-text priority.

### yassemi2008design — Design and implementation of an integrated GIS-based cellular automata model to characterize forest fire behaviour
- **Citation:** Yassemi, S., Dragićević, S., Schmidt, M. (2008). Design and implementation of an integrated GIS-based cellular automata model to characterize forest fire behaviour. *Ecological Modelling* 210(1–2), 71–84. DOI: 10.1016/j.ecolmodel.2007.07.020 (verified: Crossref)
- **Access:** paywall; an author PDF is hosted by SFU (not read).
- **Phenomenon and study area:** 2001 Dogrib fire, Alberta, Canada.
- **Model:** GIS-integrated CA using topography, fuel and weather. Spread rates are FBP-based, according to secondary sources.
- **Inputs:** DEM, fuel map, weather.
- **Parameters:** Not seen.
- **Code:** not found (GIS-embedded tool).
- **Validation:** Comparison with Prometheus showed comparable agreement.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01. A GIS-CA integration example; mostly superseded by Cell2Fire.

### alexandridis2011wildland — Wildland fire spread modelling using cellular automata: evolution in large-scale spatially heterogeneous environments under fire suppression tactics
- **Citation:** Alexandridis, A., Russo, L., Vakalis, D., Bafas, G.V., Siettos, C.I. (2011). Wildland fire spread modelling using cellular automata: evolution in large-scale spatially heterogeneous environments under fire suppression tactics. *International Journal of Wildland Fire* 20(5), 633–647. DOI: 10.1071/wf09119 (verified: Crossref)
- **Access:** OA according to the earlier OpenAlex record (not read).
- **Phenomenon and study area:** June 2007 fire on Mt Parnitha, Greece.
- **Model:** Extends the 2008 CA with GIS terrain, vegetation, wind fields, fuel humidity and a spotting mechanism, plus air-tanker suppression modelled from aircraft specifications.
- **Inputs:** DEM, vegetation, wind field data, humidity.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** Adequate agreement with the actual fire (qualitative in the abstract).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 suppression extension: drop a water line and see the fire stall. A good interactive feature.

### johnston2008efficient — Efficient simulation of wildfire spread on an irregular grid
- **Citation:** Johnston, P., Kelso, J., Milne, G.J. (2008). Efficient simulation of wildfire spread on an irregular grid. *International Journal of Wildland Fire* 17(5), 614–627. DOI: 10.1071/wf06147 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Wildfire shape distortion (Australia; the Australis simulator).
- **Model:** Cells on an irregular (randomised) grid, so the grid error becomes random and the fire shape no longer depends on wind direction relative to the grid. Implemented as discrete-event simulation: each cell has an ignition time and only active fronts are updated.
- **Inputs:** Fuel, terrain, weather.
- **Parameters:** Not seen.
- **Code:** not found (Australis is not open).
- **Validation:** Accuracy comparable to front-propagation schemes, at much higher speed.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good. An event queue of arrival times is essentially Dijkstra / fast marching on a graph.
- **Relevance to ca-geo:** HAZ-01 anisotropy remedy. It links to the "front over a cost raster" mechanism shared with accessibility and dispersal models (MOV, ECO).

### trunfio2011new — A New Algorithm for Simulating Wildfire Spread through Cellular Automata
- **Citation:** Trunfio, G.A., D'Ambrosio, D., Rongo, R., Spataro, W., Di Gregorio, S. (2011). A New Algorithm for Simulating Wildfire Spread through Cellular Automata. *ACM Transactions on Modeling and Computer Simulation* 22(1), 1–26. DOI: 10.1145/2043635.2043641 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Fire shape distortion. Homogeneous tests and two heterogeneous landscapes compared with FARSITE (Italian CA group).
- **Model:** CA in which spread directions are not restricted to the lattice angles of the neighbourhood, which reduces shape distortion.
- **Inputs:** Fuel, DEM, wind.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** More accurate than a reference CA; burned areas practically equivalent to FARSITE at much lower cost.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 anisotropy remedy, as an alternative to Ghisu's correction factors.

### millington2009modelling — Modelling Mediterranean landscape succession-disturbance dynamics: A landscape fire-succession model
- **Citation:** Millington, J.D.A., Wainwright, J., Perry, G.L.W., Romero-Calcerrada, R., Malamud, B.D. (2009). Modelling Mediterranean landscape succession-disturbance dynamics: A landscape fire-succession model. *Environmental Modelling & Software* 24(10), 1196–1208. DOI: 10.1016/j.envsoft.2009.03.013 (verified: Crossref)
- **Access:** author version in the Durham repository (not read).
- **Phenomenon and study area:** Mediterranean landscapes (central Spain). Fire regime coupled to vegetation succession.
- **Model:** Rule-based succession with plant functional types, competing for water and light, plus a fire-spread CA that uses flammability, slope, wind and moisture. Calibrated with a pattern-oriented approach against the frequency–area power-law exponent of wildfires.
- **Inputs:** Land cover, DEM, soil moisture.
- **Parameters:** Calibrated (values not seen).
- **Code:** not found.
- **Validation:** Pattern-oriented calibration.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good. Long runs over years.
- **Relevance to ca-geo:** HAZ-01 + ECO-02 (link L4) and LND-02 (link L9). Overlaps with the ecology domain.

### jiang2021modelling — Modelling of wildland-urban interface fire spread with the heterogeneous cellular automata model
- **Citation:** Jiang, W., Wang, F., Fang, L., Zheng, X., Qiao, X., Li, Z., Meng, Q. (2021). Modelling of wildland-urban interface fire spread with the heterogeneous cellular automata model. *Environmental Modelling & Software* 135, 104895. DOI: 10.1016/j.envsoft.2020.104895 (verified: Crossref)
- **Access:** OA (ScienceDirect blocked automated fetching).
- **Phenomenon and study area:** A real WUI fire in California.
- **Model:** Heterogeneous CA that couples a forest-fire sub-model and a house-fire sub-model, based on thermal principles and empirical statistics.
- **Inputs:** Vegetation, buildings, weather.
- **Parameters:** Not seen.
- **Code:** not found (a software platform is mentioned).
- **Validation:** Comparison with FlamMap 6, reporting competitive accuracy.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 ↔ URB-03 bridge: a wildfire reaching a village.

### wang2025procedure — A procedure to simulate spread of post-earthquake fire in urban area considering seismic damage to buildings
- **Citation:** Wang, Q., Lin, X., Ni, S., Zhong, J., Yang, N. (2025). A procedure to simulate spread of post-earthquake fire in urban area considering seismic damage to buildings. *Natural Hazards* 121(3), 3195–3218. DOI: 10.1007/s11069-024-06778-9 (verified: Crossref; published online 2024)
- **Access:** preprint on Research Square (text not retrievable).
- **Phenomenon and study area:** Fires after the 1995 Kobe earthquake.
- **Model:** Building damage states from elastoplastic time-history analysis feed key parameters of a building-level CA, together with building properties and weather.
- **Inputs:** Building inventory, structural models, weather.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** Overall spread pattern and reach similar to the actual Kobe fires. Runtime about 5 min.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** The CA part is fine; the structural pre-analysis is not.
- **Relevance to ca-geo:** URB-03 variant (cascade: earthquake → fire). Low priority for CZ.

### zhao2011simulation — Simulation of Mass Fire-Spread in Urban Densely Built Areas Based on Irregular Coarse Cellular Automata
- **Citation:** Zhao, S. (2011). Simulation of Mass Fire-Spread in Urban Densely Built Areas Based on Irregular Coarse Cellular Automata. *Fire Technology* 47(3), 721–749. DOI: 10.1007/s10694-010-0187-4 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Mass fire after the 1995 Hanshin earthquake, Kobe.
- **Model:**
  - Irregular coarse cells that are effectively buildings.
  - Within-building fire passes through 5 stages, which are the cell states.
  - Inter-building spread has two patterns with separate neighbourhoods and rules: short range (flame contact, radiation, convection) and long range (firebrands).
  - Ensembles of 100 random runs.
- **Inputs:** Building footprints and attributes, wind.
- **Parameters:** None in the abstract.
- **Code:** not found.
- **Validation:** General spread features agree with observations; includes a loss assessment.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → **3, D**. Assessed from: abstract (provisional).
- **Browser fit:** Very good (vector buildings as graph nodes).
- **Relevance to ca-geo:** URB-03 core design idea: buildings as irregular cells with stage-based states. Get the full text in round 2.

### mahmoud2017probabilistic — A Probabilistic Cellular Automata Framework for Assessing the Impact of WUI Fires on Communities
- **Citation:** Mahmoud, H., Chulahwat, A. (2017). A Probabilistic Cellular Automata Framework for Assessing the Impact of WUI Fires on Communities. *Procedia Engineering* 198, 1111–1122. DOI: 10.1016/j.proeng.2017.07.153 (verified: Crossref)
- **Access:** OA (not read).
- **Phenomenon and study area:** Wildland–urban interface fire exposure of communities (USA context).
- **Model:** Probabilistic CA with convection and ember-travel rules, considering humidity, vegetation and topography.
- **Inputs:** Vegetation, topography, structures.
- **Parameters:** Tunable (not seen).
- **Code:** not found.
- **Validation:** Not evident.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 0 → **3, D**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** URB-03 / HAZ-01 secondary.

### karafyllidis1997model — A model for predicting forest fire spreading using cellular automata
- **Citation:** Karafyllidis, I., Thanailakis, A. (1997). A model for predicting forest fire spreading using cellular automata. *Ecological Modelling* 99(1), 87–97. DOI: 10.1016/s0304-3800(96)01942-4 (verified: Crossref)
- **Access:** paywall. No abstract was available in Crossref or Semantic Scholar.
- **Phenomenon and study area:** Fire spread in homogeneous and inhomogeneous hypothetical forests.
- **Model:** Square-grid CA in which each cell carries a continuous burned-area fraction. It is updated from neighbours, which transfer burned area in proportion to spread rates. Wind and terrain are included through rate modification. This summary comes from later papers that describe the model; it was not read.
- **Inputs:** Rate-of-spread map, wind, topography.
- **Parameters:** unknown.
- **Code:** not found.
- **Validation:** Qualitative fire shapes.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → **3, D**. Assessed from: metadata + secondary descriptions (provisional). The most-cited fire CA, and it should be read in round 2.
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** HAZ-01 foundation of the deterministic "fractional area" family.

### berjak2002improved — An improved cellular automaton model for simulating fire in a spatially heterogeneous Savanna system
- **Citation:** Berjak, S.G., Hearne, J.W. (2002). An improved cellular automaton model for simulating fire in a spatially heterogeneous Savanna system. *Ecological Modelling* 148(2), 133–151. DOI: 10.1016/s0304-3800(01)00423-9 (verified: Crossref)
- **Access:** paywall. No abstract available.
- **Phenomenon and study area:** Savanna fire, South Africa (Mkuze Game Reserve, per a related paper).
- **Model:** Extends the Karafyllidis fractional-area CA with Rothermel spread rates and terrain/wind effects (from secondary descriptions).
- **Inputs:** Fuel, DEM, wind.
- **Parameters:** unknown.
- **Code:** not found.
- **Validation:** unknown.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 0 → **2, D**. Assessed from: metadata + secondary descriptions (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 Rothermel–CA coupling template; read in round 2.

### ohgai2007cellular — Cellular automata modeling of fire spread in built-up areas—A tool to aid community-based planning for disaster mitigation
- **Citation:** Ohgai, A., Gohnai, Y., Watanabe, K. (2007). Cellular automata modeling of fire spread in built-up areas—A tool to aid community-based planning for disaster mitigation. *Computers, Environment and Urban Systems* 31(4), 441–460. DOI: 10.1016/j.compenvurbsys.2006.10.001 (verified: Crossref)
- **Access:** paywall. No abstract retrieved.
- **Phenomenon and study area:** Fire spread in historical wooden built-up areas, Japan, for community disaster planning. Context from the KAKEN grant summary.
- **Model:** Grid CA of building fire spread (details unknown).
- **Inputs:** Building data.
- **Parameters:** unknown.
- **Code:** not found.
- **Validation:** unknown.
- **Reimplementability:** S1 0, S2 0, S3 0, S4 1, S5 0 → **1, D**. Assessed from: metadata only (provisional).
- **Browser fit:** probably good.
- **Relevance to ca-geo:** URB-03 (historic town fire). A thematically ideal source, so a round-2 full-text priority.

### sullivan2009wildland — Wildland surface fire spread modelling, 1990–2007. 3: Simulation and mathematical analogue models
- **Citation:** Sullivan, A.L. (2009). Wildland surface fire spread modelling, 1990–2007. 3: Simulation and mathematical analogue models. *International Journal of Wildland Fire* 18(4), 387–403. DOI: 10.1071/wf06144 (verified: Crossref)
- **Access:** paywall.
- **Content:** Survey of simulation models (2-D implementations of empirical spread models) and mathematical-analogue models, including CA, percolation and others. Parts 1 and 2 (DOIs 10.1071/wf06143, 10.1071/wf06142) cover physical and empirical ROS models.
- **Reimplementability:** n/a. A review entry point for the whole domain, with a taxonomy and pre-2007 CA references.
- **Relevance to ca-geo:** HAZ-01 background.

### rothermel1972mathematical — A mathematical model for predicting fire spread in wildland fuels
- **Citation:** Rothermel, R.C. (1972). A mathematical model for predicting fire spread in wildland fuels. USDA Forest Service Research Paper INT-115. DOI: 10.2737/int-rp-115 (verified: Crossref)
- **Access:** OA (USFS publication).
- **Content:** The semi-empirical 1-D surface rate-of-spread model, as a function of fuel bed properties, moisture, wind and slope. It is used as the spread-rate sub-model in many fire CA (Berjak 2002, Ghisu 2015, the PROPAGATOR option).
- **Reimplementability:** n/a (not a CA). It is the standard sub-model that turns a CA into a fire-behaviour CA. Its fuel models are tied to Anderson / Scott & Burgan fuel classes. An R package `rothermel` exists on CRAN (DOI 10.32614/cran.package.rothermel, listed in Crossref; code not checked).
- **Relevance to ca-geo:** HAZ-01 sub-model if a physically based rate is needed.

### kudlackova2024using — Using FlamMap to assess wildfire behavior in Bohemian Switzerland National Park
- **Citation:** Kudláčková, L., Poděbradská, M., Bláhová, M., Cienciala, E., Beranová, J., McHugh, C., Finney, M., Novotný, J. (2024). Using FlamMap to assess wildfire behavior in Bohemian Switzerland National Park. *Natural Hazards* 120(4), 3943–3977. DOI: 10.1007/s11069-023-06361-8 (verified: Crossref). Preprint: DOI 10.21203/rs.3.rs-3157719/v1.
- **Access:** paywall; preprint on Research Square.
- **Content:** FlamMap reconstruction of the 2022 Bohemian Switzerland NP fire, the largest in 30 years of CZ records at more than 1000 ha. Most of the burned area was bark-beetle-killed spruce. The study calibrates FlamMap to the observed perimeter and behaviour, then runs scenarios: dead trees removed, clearcuts, healthy spruce, deciduous forest, other weather. Without the dead standing trees, the fire would likely still have reached the perimeter, at lower intensity and in a shorter time. With closed healthy canopy it would have reached about half the area.
- **Reimplementability:** n/a (FlamMap is not a CA, though its minimum-travel-time spread is grid-based). It is the key **CZ calibration reference**: observed perimeter, fuel-model choices for Central European stands, and scenarios to reproduce with a CA.
- **Relevance to ca-geo:** HAZ-01 CZ case (the longlist's České Švýcarsko item, now verified), link L2 (drought → bark beetle → fire hazard). Overlaps with the ecology domain.

## Most reimplementable (top picks)

1. `xia2025pytorchfire` (10, A): full equations, open MIT code, open data and quantitative Jaccard tables. The cleanest modern statement of the Alexandridis rule.
2. `trucchia2020propagator` (9, A): European operational simulator with open EUPL code that contains the full fuel-class parameter table. It outputs probability maps, which suit a demo.
3. `freire2019using` (8, B): OA full text with all parameters, CORINE-based fuel loadings and quantitative timing metrics, plus a wind-driven non-local spread rule. EU case.
4. `alexandridis2008cellular` (8, B): the base stochastic rule. Parameters are fully published and several third-party open implementations exist.
5. `pais2021cell2fire` (9, A): open cell-based elliptical-ROS simulator with quantitative validation. The reference for anisotropy-free grid spread; needs a fuel-system mapping for CZ.
6. `ghisu2015improved` / `ghisu2015optimal` (5, C provisional): the most promising cheap fix for grid anisotropy if the correction-factor tables are confirmed.
7. `tan2019fire` (5, C provisional): the closest template for URB-03 (wind + building material), with accuracy and kappa reported.

## Gaps and unverified leads

**Unverified (not found in Crossref; OpenAlex unavailable on 2026-10-12):**
- Clarke, Brass & Riggan (1994), the CA wildfire propagation/extinction model (Photogrammetric Engineering & Remote Sensing). No Crossref record found. Retry in OpenAlex.
- Henley (1989), the original forest-fire model abstract (Bull. Am. Phys. Soc.). No DOI expected.
- "Tropical cellular automata: why urban fires propagate according to polyhedral balls" (HAL preprint, found by web search). Not in Crossref. Possibly relevant to the theory of urban-fire anisotropy.

**Verified in Crossref but not assessed (candidates for round 2):**
- Bak, Chen & Tang (1990). A forest-fire model and some thoughts on turbulence. *Physics Letters A* 147(5–6), 297–300. DOI 10.1016/0375-9601(90)90451-s
- Hernández Encinas, L. et al. (2007). Modelling forest fire spread using hexagonal cellular automata. *Applied Mathematical Modelling* 31(6), 1213–1227. DOI 10.1016/j.apm.2006.04.001 (OA). Also Hernández Encinas, A. et al. (2007), *Adv. Eng. Softw.* 38(6), 372–378, DOI 10.1016/j.advengsoft.2006.09.002. Hexagonal grids as an anisotropy remedy.
- Trunfio (2004). Predicting Wildfire Spreading Through a Hexagonal Cellular Automata Model. LNCS, 385–394. DOI 10.1007/978-3-540-30479-1_40
- Collin, Bernardin & Séro-Guillaume (2011). A Physical-Based Cellular Automaton Model for Forest-Fire Propagation. *Combust. Sci. Technol.* 183(4), 347–369. DOI 10.1080/00102202.2010.508476
- Achtemeier (2013). Field validation of a free-agent CA model of fire spread with fire–atmosphere coupling. *IJWF* 22(2), 148–156. DOI 10.1071/wf11055
- Perryman et al. (2013). A CA model to link surface fires to firebrand lift-off and dispersal. *IJWF* 22(4), 428–439. DOI 10.1071/wf11045
- Zheng et al. (2017). Forest fire spread simulating model using CA with extreme learning machine. *Ecol. Model.* 348, 33–43. DOI 10.1016/j.ecolmodel.2016.12.022
- Mutthulakshmi et al. (2020). Simulating forest fire spread and fire-fighting using CA. *Chinese J. Phys.* 65, 642–650. DOI 10.1016/j.cjph.2020.04.001
- Kelso et al. (2015). Techniques for evaluating wildfire simulators via the simulation of historical fires (Australis). *IJWF* 24(6), 784–797. DOI 10.1071/wf14047. Useful validation-metrics source.
- Trucchia et al. (2024), PROPAGATOR lessons learnt, Wiley book chapter, DOI 10.1002/9781119741374.ch3. Sahila et al. (2025), statistical dynamics of burned area from CA simulators, *Sci. Rep.*, DOI 10.1038/s41598-025-30851-3.
- Urban: Meng & Zhao (2011), DOI 10.4028/www.scientific.net/amr.368-373.732; Sun, Chen & Guo (2025), GIS-based urban fire spread probability model, *IJDRR* 129, 105779, DOI 10.1016/j.ijdrr.2025.105779; Cao et al. (2025), CA–Unity urban fire, Altadena 2025 wildfire, *Sustainable Cities and Society*, DOI 10.1016/j.scs.2025.106961 (verified in OpenAlex before the rate limit); González-Villa et al. (2025), WUI CA + reinforcement learning, *Machine Learning with Applications*, DOI 10.1016/j.mlwa.2025.100779 (verified in OpenAlex).
- Context, not CA: Lee & Davidson (2010), physics-based post-earthquake fire spread, *J. Earthquake Eng.* 14(5), DOI 10.1080/13632460903336928.

**Gaps:**
- **No CZ or central-European fire CA was found.** The only CZ modelling study is FlamMap-based (`kudlackova2024using`). A CZ CA demo calibrated on the 2022 Bohemian Switzerland perimeter would be novel. A round-2 search should look for Czech-language theses (dspace.cvut.cz, is.muni.cz, theses.cz) and for German or Polish work.
- Many key papers (Elsevier, MDPI, Springer) could not be fetched automatically, so their S1/S2 scores are provisional. Round-2 full-text priorities: Ghisu 2015 (correction factors), Karafyllidis 1997, Hargrove 2000 (OA on Treesearch), Zhao 2011 and Ohgai 2007 (URB-03), Tan 2019 (OA PDF), PROPAGATOR 2020 paper (S5 metrics).
- Historic town fire (URB-03): no European historic-town fire CA was found. Japanese and Chinese building-based CA are the templates.
- Fuel mapping for CZ: needs a translation from CORINE / Urban Atlas / forest stand maps to PROPAGATOR classes or Scott & Burgan fuels. Kudláčková 2024 is the lead.
- Overlaps: ECO (fire–succession `millington2009modelling`, bark beetle → fire link L2), GEN (GPU/differentiable CA `xia2025pytorchfire`, event-driven "front over a cost raster" `johnston2008efficient`), MOV (evacuation after fire), ATM (smoke).
