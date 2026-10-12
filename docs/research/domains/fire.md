# Fire — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.

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

### Round 2

OpenAlex was still quota-blocked, so all searches and metadata checks used Crossref (with pauses; it returned occasional HTTP 429, retried). Full-text routes tried: Semantic Scholar `openAccessPdf`, Crossref `link`, publisher OA pages, institutional repositories, USDA Treesearch, ASPRS archive. ScienceDirect (Elsevier) and HAL showed bot challenges (CAPTCHA / Anubis); we did not try to get past them. MDPI pages opened in the in-app browser. Downloaded PDFs were kept only in the agent scratchpad and deleted after text extraction.

| Query | Source | Hits | Notes |
|---|---|---|---|
| OA-PDF lookup for 13 priority DOIs | Semantic Scholar | 13 | OA copies found for Tan 2019, Hargrove 2000, PROPAGATOR, Ghisu (Procedia; blocked by ScienceDirect CAPTCHA). Alexandridis 2008, Ghisu 2015 (EMS), Ohgai 2007 and Zhao 2011 listed as closed. |
| Full text: Tan 2019, Hargrove 2000 | ISPRS archive, geobabble.org author copy | 2 | Read. Both re-scored. |
| Full text: PROPAGATOR 2020, Sun 2021 | MDPI (in-app browser) | 2 | Read, including tables (fuel-to-fuel matrix, metrics). |
| Full text: Alexandridis 2008, Ghisu 2015 ×2, Ohgai 2007, Zhao 2011, Alexandridis 2011 | ScienceDirect, Springer, CSIRO, IRIS UniCA / CNR | 0 | No access (paywall, CAPTCHA, or file restricted to repository staff). Scores unchanged. |
| `Clarke Brass Riggan cellular automaton wildfire 1994` | Crossref; web search | 0 in Crossref | Found as grey literature (PE&RS 1994, no DOI) on USDA Treesearch; full text read. |
| `cellular automata wildfire spotting firebrand` | Crossref | ranked | López-De-Castro et al. 2022 and 2024 (spotting models inside PROPAGATOR). |
| `cellular automata wildfire Czech Republic`; `forest fire spread model Central Europe`; `Bohemian Switzerland 2022 wildfire spread simulation`; `forest fire behaviour modelling Czech Republic fuel models` | Crossref | ranked | No CZ fire CA. The only Central European spread-modelling hit is Glasa & Halada (elliptical front model, title-level, not CA; Slovak journal). Trochta 2012 and Boháč 2023 are on the 2022 fire area but do not model spread. |
| `celulární automat šíření požáru` (Czech) | web search | – | Two CZ student theses (VUT Brno FIT bachelor thesis 2013; VŠB-TU Ostrava master thesis 2010 with an ArcGIS Server web CA fire model). Grey literature, listed under leads. |
| `wildfire spread model Slovakia Poland cellular automaton` | Crossref | ranked | Maskeliūnas et al. 2026 (Lithuania, Procedia, no abstract in Crossref/Semantic Scholar), listed as lead. |
| `cellular automaton fire smoke coupling evacuation wildfire`; `cellular automaton wildfire smoke plume transport coupled` | Crossref | ranked | No fire–smoke CA coupling found. Building-scale smoke → evacuation coupling only (Liu 2023, Wang & Zheng 2013; see `movement.md`). |
| `Ohgai … built-up areas pdf`; `Ghisu … optimal … pdf` | web search | – | No legal OA copy found. Tan 2019 restates Ohgai's components. |

## Model families

1. **Abstract forest-fire / percolation models (foundations).**
   - Cells are tree / empty / burning, on a square lattice with a von Neumann neighbourhood. Trees grow with probability p and lightning strikes with probability f.
   - These models study self-organised criticality, not real fires. They are a minimal teaching baseline and give the percolation-threshold intuition: below a critical occupancy fire dies, above it fire crosses the landscape.
   - Keys: `drossel1992selforganized`, `bak1990forestfire` (verified, not assessed), `almeida2011stochastic`, `hargrove2000simulating` (critical spread probability of about 0.25 on an 8-neighbour landscape; round 2: full fuel-to-fuel, wind-bias and firebrand tables, so it is also a full landscape model), `clarke1994cellular` (early GIS fire CA with "firelets", round 2).
2. **Stochastic "probability of burning" CA (Alexandridis family).**
   - Moore neighbourhood with states unburnable / unburnt / burning / burnt.
   - Spread probability is p_burn = p_h·(1+p_veg)·(1+p_den)·p_w·p_s, where wind and slope enter as exponential factors.
   - Run as ensembles, the model gives burn-probability maps. This is the most re-implemented family, with published parameter values and several open implementations.
   - Keys: `alexandridis2008cellular`, `alexandridis2011wildland`, `freire2019using` (Portugal, wind-driven non-local spread), `xia2025pytorchfire` (differentiable GPU version with gradient calibration), `trucchia2020propagator` and `perello2024cellular` (operational Italian system; adds rate-of-spread timing, moisture and fuel-to-fuel probability tables). Round 2: PROPAGATOR's rule p = 1 − (1 − p_n)^α (cumulative binomial) is the same device as EMBYR's wind bias (`hargrove2000simulating`).
   - **Fire spotting (round 2):** embers landing downwind start new ignitions. Three schemes have been compared inside one CA (PROPAGATOR): the Alexandridis 2011 rule, the Perryman 2013 rule and the physics-based RandomFront lognormal landing distribution (`lopezdecastro2024firespotting`). EMBYR uses a simpler negative-exponential landing distance (`hargrove2000simulating`).
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
| `trucchia2020propagator` | 2020 | PROPAGATOR | wildfire, Italy/Spain | square (20 m default) / Moore / stoch. + ROS timing | 2 2 2 2 2 | 10 | A | yes (EUPL-1.2) | OA | full text (r2) + source code/docs |
| `alexandridis2008cellular` | 2008 | CA forest fire, Spetses 1990 | wildfire, Greece | square / Moore / 4 states / stoch. | 2 2 1 2 1 | 8 | B | third-party (BSD, MIT) | OA (publisher) | secondary full texts (Freire 2019, Xia 2025) + code |
| `freire2019using` | 2019 | CA wildfire, Tavira 2012 | wildfire, Portugal | square 100 m / Moore + wind-aligned non-local / 4 states / stoch. | 1 2 1 2 2 | 8 | B | third-party (BSD) | OA | full text |
| `pais2021cell2fire` | 2021 | Cell2Fire | wildfire, Canada | square 100 m / 8 neigh. / elliptical ROS, msg passing / det. | 2 2 2 1 2 | 9 | A | yes (GPL-3.0) | OA | full text |
| `perello2024cellular` | 2024 | PROPAGATOR prescribed fire, Liguria | wildfire + prescribed burns, Italy | as PROPAGATOR | 1 1 2 1 1 | 6 | C | yes (PROPAGATOR) | OA | abstract (provisional) |
| `rui2018forest` | 2018 | CA forest fire, time step | wildfire, NE China | square / 8 neigh. / ROS-driven / det. | 1 1 0 1 2 | 5 | C | not found | paywall | abstract (provisional) |
| `sun2021adaptive` | 2021 | Adaptive time-step CA | wildfire, Sichuan | square 30 m / 8 neigh. / 5 states, ROS-driven, adaptive Δt / det. | 2 1 0 1 2 | 6 | C | not found | OA | full text (r2) |
| `tan2019fire` | 2019 | Probabilistic CA urban fire, Cebu | urban settlement fire, Philippines | square 3 m / von Neumann r ≥ 2 (wind-dependent) / 5 states / stoch. | 1 2 0 1 2 | 6 | C | not found | OA | full text (r2) |
| `ghisu2015optimal` | 2015 | Optimal CA (correction factors) | wildfire, anisotropy | square / extended neigh. / ROS / det. | 1 1 0 2 1 | 5 | C | not found | paywall | abstract (provisional) |
| `ghisu2015improved` | 2015 | Improved CA (Procedia) | wildfire, anisotropy | as above | 1 1 0 2 1 | 5 | C | not found | OA | abstract (provisional) |
| `almeida2011stochastic` | 2011 | Stochastic CA, critical line | abstract wildland fire | square / neigh. n/s / 3 states / stoch. | 1 1 0 2 1 | 5 | C | not found | OA | abstract (provisional) |
| `drossel1992selforganized` | 1992 | SOC forest-fire model | abstract (SOC) | square / von Neumann / 3 states / stoch. | 1 1 0 2 1 | 5 | C | not found (trivial) | paywall | abstract + encyclopedic description |
| `hargrove2000simulating` | 2000 | EMBYR | large fires, Yellowstone | square 50 m / Moore + firebrands / 3 states / stoch. | 2 1 1 1 2 | 7 | B | dead link (Fortran 77) | OA (author copy) | full text (r2) |
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
| `ohgai2007cellular` | 2007 | CA fire spread in built-up areas | urban fire, Japan | square 3 m / wind-dependent reach / stoch. | 1 1 0 1 0 | 3 | D | not found | paywall | secondary full text (Tan 2019) (provisional) |
| `sullivan2009wildland` | 2009 | Review: simulation & analogue models | review | – | n/a | – | n/a | – | preprint (arXiv 0706.4130) | abstract |
| `rothermel1972mathematical` | 1972 | Rothermel spread model | fire behaviour (1-D ROS) | – (sub-model for CA) | n/a | – | n/a | R package exists (not checked) | OA (USFS report) | metadata |
| `kudlackova2024using` | 2024 | FlamMap, Bohemian Switzerland 2022 | wildfire, CZ (not CA) | – | n/a | – | n/a | – | preprint OA | abstract |
| `lopezdecastro2024firespotting` | 2024 | Fire-spotting models in CA (r2) | ember spotting, Molise (Italy) | as PROPAGATOR + 3 spotting schemes / stoch. | 1 1 2 1 1 | 6 | C | yes (PROPAGATOR; analysis scripts on BCAM GitLab) | OA (per repository) | abstract (provisional) |
| `clarke1994cellular` | 1994 | CA wildfire propagation & extinction (r2) | wildfire, California (Lodi Canyon 1986) | square 25 m / Moore "firelets" (DLA-like) / stoch. | 1 1 1 1 1 | 5 | C | not open (C program) | OA (Treesearch), grey literature, no DOI | full text (r2) |
| `glasa2008elliptical` | 2008 | Elliptical spread model (r2) | fire-front geometry (not CA; Slovak group, affiliation not verified) | – (elliptical front model, title-level) | n/a | – | n/a | – | paywall | metadata only |

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
- **Access:** OA (MDPI). Round 2: full text read in the in-app browser, including all tables.
- **Phenomenon and study area:** Wildfire spread for civil protection, tested on five past fires: Avinyó, Blanes and Sant Fruitós de Bages (Catalonia, 30–105 ha) and Monte Fasce and Ittiri (Liguria and Sardinia, 945 and 5131 ha).
- **Model:**
  - Stochastic CA. Spread probability depends on the fuel class of the burning cell and the target cell, through a fuel-to-fuel probability matrix in the code. It is modulated by wind, slope and dead fine fuel moisture.
  - The propagation time per cell comes from a rate-of-spread model. The current code defaults to "wang" and also offers "rothermel".
  - Runs are many independent realisations, and the output is a per-cell burn-probability map at each time step.
  - Firebreaks and fire-fighting actions can be imposed.
  - The current code adds an ember-spotting model and a front-tracking scheduler.
  - Round 2, from the paper: spread probability p_ij = (1 − (1 − p_n)^α_wh) · e_m, a cumulative-binomial form. α_wh = α_w · α_h. The slope and wind factors are given as curves in the paper (formulas in the code). e_m is the Rothermel/Burgan moisture damping with moisture of extinction fixed at 0.3. Each step, wind speed is perturbed by a factor U[0.8, 1.2] and direction by U[−11.25°, 11.25°]. Spread time uses v = v_n · K_w · K_φ with K_w = exp(0.1783 V) and K_φ = exp(3.533 (tan φ)^1.2), following the formulations of Sun et al. cited in the paper (the same constants appear in `sun2021adaptive`) Table 1 of the paper gives the full 6 × 6 fuel-to-fuel p_n matrix (values 0.075–0.475) and v_n per class (60–200 m/min).
- **Inputs:** DEM, a vegetation/fuel raster (7 legacy classes such as broadleaves, shrubs, non-vegetated…), wind speed/direction, moisture, and ignition points. The code repository includes a script that downloads Italian national data.
- **Parameters:** A full table in the code (`constants.py`): nominal ROS v0, dead/live fuel load, heating value, moisture, and a per-class spread-probability matrix. The wind/slope/moisture constants are in `functions.py`. Default cell size is 20 m with 100 realisations.
- **Code:** https://github.com/CIMAFoundation/propagator_sim (EUPL-1.2, Python/Numba, verified 200). There is also a third-party QGIS plugin (GiorgioMeschi/propagator-qgis-plugin, not checked).
- **Validation:** Table 4 gives, per fire, three area-scaled error indicators, the Sørensen coefficient (0.63–0.89 with fire-fighting actions; 0.22 for Avinyó without them), McNemar p-values, sensitivity (0.83–0.98) and specificity (0.92–0.96). The Catalan burned-area shapefiles come from an open regional archive. Runs took about 1–5 min CPU for 12–48 h of fire.
- **Reimplementability:** S1 2 – rule equations in the paper, the remaining curves in open code; S2 2 – fuel matrix and v_n in the paper, all constants in code; S3 2; S4 2 – generic DEM plus fuel classes that map from CORINE-type land cover; S5 2 – quantitative per-fire metrics → **10, A** (was 9, A). Round 2: re-assessed from full text — S5 2 (was 1). Assessed from: full text + source code/docs.
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
- **Reimplementability:** S1 2 – complete rule available via two independent full-text restatements and code; S2 2 – full parameter set published; S3 1 – third-party open code only, no author code (harmonised rule); S4 2 – runs on generic land-cover, DEM and wind layers; S5 1 – only qualitative fit known → **8, B**. Assessed from: secondary full texts (Freire 2019, Xia 2025) and code. The original paper was not read, so scores are provisional on the original. Round 2: still no access (Semantic Scholar lists it as closed; ScienceDirect shows a CAPTCHA). Score unchanged.
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
- **Access:** OA (MDPI). Round 2: full text read in the in-app browser.
- **Phenomenon and study area:** 2020 fire in Mianning County, Sichuan, China.
- **Model:**
  - Square 30 m cells (Landsat grid), 8 neighbours. Five states: unburnt, early burning, full burning (the only state that ignites neighbours), extinguishing, extinguished.
  - Spread rate from the revised Wang Zhengfei model: R = R0 · K_φ · K_θ · K_S · K_r, with R0 = 0.03 T + 0.05 W + 0.01 (100 − RH) − 0.3 (T air temperature, W wind level, RH relative humidity), K_φ = exp(0.1783 v cos φ) and an exponential slope factor. K_S comes from a fuel lookup table in a Chinese source; K_r is a time-correction constant from Rui et al. 2018.
  - Each cell accumulates burned fraction from burning neighbours as Σ R · Δt / L. Δt adapts through a "speed change rate" index, so steps shrink when spread accelerates.
- **Inputs:** DEM, a fuel map from remote sensing, weather (temperature, humidity, wind).
- **Parameters:** R0 coefficients and wind/slope factors given; the K_S table and the K_r value come from cited sources.
- **Code:** not found.
- **Validation:** Accuracy 96.9% and kappa 0.62 against the observed burned area.
- **Reimplementability:** S1 2 – states, spread equation and update are stated; S2 1 – fuel coefficients and K_r are only in cited sources; S3 0; S4 1 – Chinese fuel classes; S5 2 → **6, C** (was 5, C provisional). Round 2: re-assessed from full text — S1 2 (was 1).
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01. The adaptive step suits an animated demo. PROPAGATOR uses the same wind and slope factors (`trucchia2020propagator`), so this is also a cross-check for those constants.

### tan2019fire — Fire spread prediction using probabilistic cellular automata: the case of urban settlements in the Philippines
- **Citation:** Tan, E.E., Vicente, A.J. (2019). Fire Spread Prediction Using Probabilistic Cellular Automata: The Case of Urban Settlements in the Philippines. *The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences* XLII-4/W19, 415–420. DOI: 10.5194/isprs-archives-xlii-4-w19-415-2019 (verified: Crossref)
- **Access:** OA (CC BY). Round 2: full text read.
- **Phenomenon and study area:** Fire in a dense informal settlement: Tamiya, Barangay Basak, Lapu-Lapu City (Cebu), 20 March 2018, more than 300 houses.
- **Model:** An adaptation of Ohgai et al. (2007).
  - Square 3 m cells. Building polygons are transferred to cells by a spatial join with a −0.8 m buffer, so narrow gaps between shanties stay empty.
  - The neighbourhood reach follows Hamada's maximum spread distance D = 1.15(5 + 0.5v), with v the wind speed in m/s (5.75 m at calm). This gives a von Neumann neighbourhood of radius at least 2.
  - States: 0 no structure, 1 burnable, 2 ignited (cannot spread yet), 3 burning (spreads), 4 burnt out. Transitions 2→3 after t1 = 4 min and 3→4 after t2 = 10 min, both from house-burn experiments.
  - Ignition probability P = a · B · H(t) · W. a is a global constant (1 in the case study). B is the material factor: cement 0.01, metal 0.2, wood or plastic 1, mixed 0.7. H(t) is Wakamatsu's indoor-temperature curve of a burning wooden house, a function of burning duration. W is a wind bias: cells in a 90° downwind cone get a positive bias that decreases with distance, upwind cells a negative one.
  - Synchronous 1-minute steps until a set end time. A web tool runs the model on a server.
- **Inputs:** Building footprints with material and height (FireCheck field survey, not public), wind speed and direction.
- **Parameters:** All values above are stated. The material mix for the burnt area was borrowed from a similar neighbourhood.
- **Code:** not found (the web tool is not public).
- **Validation:** Simulated against the observed burnt extent after 77 minutes with 2 m/s wind: accuracy 83.5%, Cohen's kappa 0.67.
- **Reimplementability:** S1 1 – the state machine and update order are clear, but the extracted equations for H(t) and the wind-bias weights are not fully legible, and it is not stated how the heat of several burning neighbours combines; S2 2 – all constants given; S3 0; S4 1 – needs building material per footprint (OSM building tags or a construction-type attribute from the Czech building registers could stand in; to be checked); S5 2 → **6, C** (was 5, C provisional). Round 2: re-assessed from full text — S2 2 (was 1).
- **Browser fit:** Very good. Small grids, one-minute steps.
- **Relevance to ca-geo:** URB-03 template, and the clearest available restatement of the Ohgai 2007 rule set (Hamada distance, 3 m cells, Wakamatsu heat curve). A historic Czech town would need roof/wall material classes in place of the Philippine ones.

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
- **Round 2:** still no access. The CNR and UniCA IRIS records have no public file. Score unchanged; the correction-factor tables remain unconfirmed.

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
- **Round 2:** the CC BY-NC-ND PDF exists on ScienceDirect, but every access returned a CAPTCHA, and the UniCA IRIS copy is restricted to repository staff. Not read; score unchanged. A manual download by the user would settle it.

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
- **Access:** OA author copy (geobabble.org, found through Semantic Scholar). Round 2: full text read.
- **Phenomenon and study area:** Large fires on the subalpine plateau of Yellowstone NP (the EMBYR model). Homogeneous test landscapes, then the real fuel map.
- **Model:**
  - Square 50 m cells. Each burning cell burns for exactly one step and independently tries to ignite each of its 8 neighbours (bond percolation). No diagonal-distance correction, on purpose: the authors show it would bias shapes in the range I = 0.25–0.5 that matters.
  - Base spread probability I comes from a 5 × 5 fuel-to-fuel matrix (four lodgepole-pine successional stages plus non-forest; rock, water and roads do not burn) for each of three 1000-h fuel-moisture classes (<12%, 12–16%, >16%), so 75 values in Table 1.
  - Wind: three speed classes. A directional bias b_j per neighbour turns I into i_wj = 1 − (1 − I)^b_j. The text gives b = 2 (moderate) and 3 (strong) downwind; the full 8-direction bias rose is only in a figure.
  - Firebrands: each burning cell emits a fixed number of brands by fuel type (0, 1, 4, 8, 0). Landing distance follows a negative exponential with mean 150 / 250 / 300 m for the three wind classes. Direction is random at calm, otherwise downwind within a 3° normal spread. A landing brand ignites with a probability by fuel and moisture (Table 2, 0.001–0.1).
  - The step procedure (7 steps) is listed explicitly.
- **Inputs:** Fuel-class map (Yellowstone successional stages), moisture class, wind speed class and direction, ignition points.
- **Parameters:** Tables 1 and 2 are complete. Only the wind-bias rose for the non-downwind directions has to be read from a figure.
- **Code:** Fortran 77 code was published at a University of Maryland URL given in the paper; that URL now returns HTTP 403 (dead link).
- **Validation:** Critical spread probability i_c between 0.250 and 0.251 (50 runs per value on a 300 × 300 grid). Tables 3 and 4 give means and CVs of burned area, time to edge, edge per cell and number of patches for I = 0.3–0.5 with and without firebrands and wind. Firebrands cut time to edge about 4× (8× with moderate wind).
- **Reimplementability:** S1 2 – complete stochastic procedure; S2 1 – all tables except the full wind-bias rose; S3 1 – code existed but the link is dead; S4 1 – the fuel classes are specific to Yellowstone lodgepole pine, so a CZ run needs a new matrix; S5 2 – the percolation threshold and Tables 3–4 are direct numerical test cases → **7, B** (was 4, C provisional). Round 2: re-assessed from full text — S1 2, S3 1, S5 2 (were 1, 0, 1).
- **Browser fit:** Very good. Homogeneous 300 × 300 test runs are instant.
- **Relevance to ca-geo:** HAZ-01. The best-documented landscape-scale stochastic fire CA with spotting. Its homogeneous-landscape tables are ready-made unit tests for a stochastic fire engine (critical threshold ≈ 0.25 for 8-neighbour bond spread). Its moisture-class × fuel matrix is a simple template for a CZ matrix (spruce stages, dead spruce, pine, broadleaves, non-forest).

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
- **Relevance to ca-geo:** URB-03 core design idea: buildings as irregular cells with stage-based states.
- **Round 2:** no access (Springer paywall, no OA copy found). Score unchanged.

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
- **Model:** Grid CA of building fire spread. Round 2: Tan & Vicente (2019) adopt this model and restate its components: 3 m cells chosen as about half of Hamada's no-wind spread distance of 5.75 m, a wind-dependent neighbourhood reach from Hamada's formula, and Wakamatsu's indoor-temperature curve as the heat term. The original was still not accessible.
- **Inputs:** Building data.
- **Parameters:** unknown.
- **Code:** not found.
- **Validation:** unknown.
- **Reimplementability:** S1 1, S2 1 (both via the Tan 2019 restatement), S3 0, S4 1, S5 0 → **3, D** (was 1, D). Assessed from: secondary full text (Tan 2019) (provisional).
- **Browser fit:** probably good.
- **Relevance to ca-geo:** URB-03 (historic town fire). A thematically ideal source, so a round-2 full-text priority.

### sullivan2009wildland — Wildland surface fire spread modelling, 1990–2007. 3: Simulation and mathematical analogue models
- **Citation:** Sullivan, A.L. (2009). Wildland surface fire spread modelling, 1990–2007. 3: Simulation and mathematical analogue models. *International Journal of Wildland Fire* 18(4), 387–403. DOI: 10.1071/wf06144 (verified: Crossref)
- **Access:** paywall; round 2: author preprint on arXiv (0706.4130).
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

### lopezdecastro2024firespotting — Fire-spotting modelling in operational wildfire simulators based on Cellular Automata: A comparison study (round 2)
- **Citation:** López-De-Castro, M., Trucchia, A., Morra di Cella, U., Fiorucci, P., Cardillo, A., Pagnini, G. (2024). Fire-spotting modelling in operational wildfire simulators based on Cellular Automata: A comparison study. *Agricultural and Forest Meteorology* 350, 109989. DOI: 10.1016/j.agrformet.2024.109989 (verified: Crossref). Companion conference abstract: López-De-Castro, M., Trucchia, A., Fiorucci, P., Pagnini, G. (2022). Physical and Non-Physical Fire-Spotting Models: A Comparison Study by a Wildfire Simulator Based on a Cellular Automata Approach. *Environmental Sciences Proceedings* 17(1), 27. DOI: 10.3390/environsciproc2022017027 (verified: Crossref; read).
- **Access:** OA according to the University of Navarra and BCAM repository listings (ScienceDirect not reachable for us). The 2022 abstract is OA (MDPI).
- **Phenomenon and study area:** Ember spotting during the 2021 Campomarino fire, Molise, Italy.
- **Model:** PROPAGATOR (see `trucchia2020propagator`) with three interchangeable spotting schemes: the empirical rule of Alexandridis et al. (2011), the CA rule of Perryman et al. (2013), and RandomFront, in which the downwind landing distance of firebrands is lognormal and its parameters follow from wind, fire-line intensity, fuel density, firebrand radius, maximum loft height and atmospheric stability.
- **Inputs:** As PROPAGATOR.
- **Parameters:** Not seen (abstract level).
- **Code:** PROPAGATOR repository (verified). Data and analysis scripts of the 2022 study: https://gitlab.bcamath.org/malopez/fire-spotting (verified 200).
- **Validation:** Comparison of burn-probability maps between the schemes; RandomFront gives more complex patterns and long-range fluctuations.
- **Reimplementability:** S1 1, S2 1, S3 2, S4 1, S5 1 → **6, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good. Spotting adds random long jumps but no heavy computation.
- **Relevance to ca-geo:** HAZ-01 spotting option. One paper puts three published spotting rules side by side in a CA, which helps choose one.

### clarke1994cellular — A cellular automaton model of wildfire propagation and extinction (round 2)
- **Citation:** Clarke, K.C., Brass, J.A., Riggan, P.J. (1994). A cellular automaton model of wildfire propagation and extinction. *Photogrammetric Engineering and Remote Sensing* 60(11), 1355–1367. **Grey literature, no DOI** (not in Crossref); record and full text at https://research.fs.usda.gov/treesearch/41203 (checked 200).
- **Access:** OA via USDA Treesearch. Round 2: full text read.
- **Phenomenon and study area:** Wildfire spread and burn-out, calibrated on the 1986 Lodi Canyon fire (San Dimas Experimental Forest, California) using airborne thermal-infrared imagery.
- **Model:**
  - Square 25 m cells (30 m DEM resampled; study grid 230 × 232). Fire spreads by "firelets" sent from burning fire centres in a process like diffusion-limited aggregation.
  - Each firelet chooses one of 8 directions from a wind probability table (Table 1 gives the percentages for wind magnitudes 0–7; 12.5% each at calm, concentrated downwind at high wind). The weights are then raised in the uphill direction in proportion to slope and adjusted for remaining fuel.
  - A run continues until no fuel is found or a set length is reached. Run length reflects fuel moisture and pre-heating. New fire centres can form at random, and downwind at high wind (spotting). Centres go out when successive runs find no unburnt fuel.
  - Monte Carlo repetition gives burn-probability maps.
- **Inputs:** Fuel map, DEM (slope, aspect), wind table, wind magnitude/direction, air temperature, humidity, fuel moisture.
- **Parameters:** The wind table is given. The slope weights, self-replication rate and extinction conditions were calibrated, but not all final values are tabulated.
- **Code:** Implemented in C with a graphical interface; not released (S3 1 as a closed tool).
- **Validation:** Shape and pattern comparison with the thermal-infrared fire stages (qualitative to semi-quantitative).
- **Reimplementability:** S1 1 – the procedure is described in prose, with some steps left open; S2 1; S3 1; S4 1; S5 1 → **5, C**. Assessed from: full text.
- **Browser fit:** Good.
- **Relevance to ca-geo:** HAZ-01 history. It is the first well-known GIS-calibrated fire CA (the round-1 unverified lead, now resolved). Its random-walk "firelet" spread is a different mechanism from neighbour-probability CA, but it is less specified than Alexandridis or EMBYR.

### glasa2008elliptical — On elliptical model for forest fire spread modeling and simulation (round 2)
- **Citation:** Glasa, J., Halada, L. (2008). On elliptical model for forest fire spread modeling and simulation. *Mathematics and Computers in Simulation* 78(1), 76–88. DOI: 10.1016/j.matcom.2007.06.001 (verified: Crossref)
- **Access:** paywall. No abstract in Crossref or Semantic Scholar.
- **Content:** Title-level information only: an analysis of the elliptical fire-front model used by vector simulators (FARSITE family). The same authors also published "Analysis of Forest Fire Behaviour by Advanced Computer Fire Simulators" (*Communications – Scientific Letters of the University of Žilina* 13(2), 2011, DOI 10.26552/com.c.2011.2.26-31, verified in Crossref, not assessed).
- **Reimplementability:** n/a (not a CA).
- **Relevance to ca-geo:** The only Central European fire-spread modelling work found (Slovak journal; affiliation not verified in metadata). Context for the anisotropy problem (the ellipse that Cell2Fire and Ghisu try to reproduce on a grid). Not a CA source.

## Most reimplementable (top picks)

1. `trucchia2020propagator` (10, A; round 2 up from 9): European operational simulator. The paper gives the rule, the fuel-to-fuel matrix and per-fire Sørensen/sensitivity/specificity; the open EUPL code has every constant. Outputs probability maps, which suit a demo.
2. `xia2025pytorchfire` (10, A): full equations, open MIT code, open data and quantitative Jaccard tables. The cleanest modern statement of the Alexandridis rule.
3. `pais2021cell2fire` (9, A): open cell-based elliptical-ROS simulator with quantitative validation. The reference for anisotropy-free grid spread; needs a fuel-system mapping for CZ.
4. `freire2019using` (8, B): OA full text with all parameters, CORINE-based fuel loadings and quantitative timing metrics, plus a wind-driven non-local spread rule. EU case.
5. `alexandridis2008cellular` (8, B): the base stochastic rule. Parameters are fully published and several third-party open implementations exist (original still unread).
6. `hargrove2000simulating` (7, B; round 2 up from 4): EMBYR. Complete fuel × moisture spread tables, binomial wind bias and firebrand rules, plus homogeneous-landscape result tables that work as unit tests for any stochastic fire CA.
7. `tan2019fire` (6, C; round 2 up from 5): the closest URB-03 template (building material, wind cone, timed burning stages), with all constants and accuracy/kappa; also the best available restatement of Ohgai 2007.
8. `ghisu2015improved` / `ghisu2015optimal` (5, C provisional): still the most promising cheap fix for grid anisotropy, but the correction-factor tables remain unread (CAPTCHA / paywall).

## Gaps and unverified leads

**Resolved in round 2:**
- Clarke, Brass & Riggan (1994) is now `clarke1994cellular` (grey literature, no DOI, full text on Treesearch).

**Unverified (not found in Crossref):**
- Henley (1989), the original forest-fire model abstract (Bull. Am. Phys. Soc.). No DOI expected.
- "Tropical cellular automata: why urban fires propagate according to polyhedral balls" (HAL preprint, found by web search). Not in Crossref. Possibly relevant to the theory of urban-fire anisotropy.
- Weinhouse & Augustin (2025), CA wildfire model for the 2025 Pacific Palisades fire with NDVI, wind and slope from open data (arXiv 2510.09708; arXiv DOI only, not in Crossref). Reports recall 0.86, precision 0.61, F1 0.71.
- Czech student theses (grey literature, no DOI; content from repository listings and web search, not read): Daniš (2013), forest-fire simulator based on CA, bachelor thesis, VUT Brno FIT (https://dspace.vutbr.cz/handle/11012/54856, returned HTTP 429 to our check, so not verified); Aprias (2010), CA fire-spread model in ArcGIS Server with a web client, master thesis, VŠB-TU Ostrava (https://dspace.vsb.cz/handle/10084/82451, checked 200).

**Verified in Crossref but not assessed (candidates for a later round):**
- Bak, Chen & Tang (1990). A forest-fire model and some thoughts on turbulence. *Physics Letters A* 147(5–6), 297–300. DOI 10.1016/0375-9601(90)90451-s
- Hernández Encinas, L. et al. (2007). Modelling forest fire spread using hexagonal cellular automata. *Applied Mathematical Modelling* 31(6), 1213–1227. DOI 10.1016/j.apm.2006.04.001 (OA). Also Hernández Encinas, A. et al. (2007), *Adv. Eng. Softw.* 38(6), 372–378, DOI 10.1016/j.advengsoft.2006.09.002. Hexagonal grids as an anisotropy remedy.
- Trunfio (2004). Predicting Wildfire Spreading Through a Hexagonal Cellular Automata Model. LNCS, 385–394. DOI 10.1007/978-3-540-30479-1_40
- Collin, Bernardin & Séro-Guillaume (2011). A Physical-Based Cellular Automaton Model for Forest-Fire Propagation. *Combust. Sci. Technol.* 183(4), 347–369. DOI 10.1080/00102202.2010.508476
- Achtemeier (2013). Field validation of a free-agent CA model of fire spread with fire–atmosphere coupling. *IJWF* 22(2), 148–156. DOI 10.1071/wf11055
- Perryman et al. (2013). A CA model to link surface fires to firebrand lift-off and dispersal. *IJWF* 22(4), 428–439. DOI 10.1071/wf11045 (one of the three spotting schemes compared in `lopezdecastro2024firespotting`).
- Zheng et al. (2017). Forest fire spread simulating model using CA with extreme learning machine. *Ecol. Model.* 348, 33–43. DOI 10.1016/j.ecolmodel.2016.12.022
- Mutthulakshmi et al. (2020). Simulating forest fire spread and fire-fighting using CA. *Chinese J. Phys.* 65, 642–650. DOI 10.1016/j.cjph.2020.04.001
- Kelso et al. (2015). Techniques for evaluating wildfire simulators via the simulation of historical fires (Australis). *IJWF* 24(6), 784–797. DOI 10.1071/wf14047. Useful validation-metrics source.
- Trucchia et al. (2024), PROPAGATOR lessons learnt, Wiley book chapter, DOI 10.1002/9781119741374.ch3. Sahila et al. (2025), statistical dynamics of burned area from CA simulators, *Sci. Rep.*, DOI 10.1038/s41598-025-30851-3.
- Maskeliūnas, Krilavičius & Damaševičius (2026). Forest Lattice-Tree Cellular Automaton for Forest Wildfire Spread Modeling. *Procedia Computer Science* 280, 7–14. DOI 10.1016/j.procs.2026.04.003 (OA, Lithuania/EU; no abstract available to us).
- Urban: Meng & Zhao (2011), DOI 10.4028/www.scientific.net/amr.368-373.732; Sun, Chen & Guo (2025), GIS-based urban fire spread probability model, *IJDRR* 129, 105779, DOI 10.1016/j.ijdrr.2025.105779; Cao et al. (2025), CA–Unity urban fire, Altadena 2025 wildfire, *Sustainable Cities and Society*, DOI 10.1016/j.scs.2025.106961 (verified in OpenAlex before the rate limit); González-Villa et al. (2025), WUI CA + reinforcement learning, *Machine Learning with Applications*, DOI 10.1016/j.mlwa.2025.100779 (verified in OpenAlex).
- Context, not CA: Lee & Davidson (2010), physics-based post-earthquake fire spread, *J. Earthquake Eng.* 14(5), DOI 10.1080/13632460903336928. Trochta, Král & Šamonil (2012), effects of wildfire on a pine stand in Bohemian Switzerland NP, *J. For. Sci.* 58, 299–307, DOI 10.17221/68/2011-jfs (CZ field data on fire effects, not spread).

**Gaps:**
- **Still no CZ or Central European fire CA in the peer-reviewed literature.** Round 2 found only CZ student theses (grey) and work on elliptical front models published by Glasa & Halada (`glasa2008elliptical`, not CA). The CZ calibration reference remains `kudlackova2024using` (FlamMap). A CZ CA demo calibrated on the 2022 Bohemian Switzerland perimeter would still be novel.
- **Fire–smoke coupling:** no CA that couples landscape fire spread to smoke transport was found. Building-scale smoke → evacuation coupling exists (`liu2023cellular` in `movement.md`). For chain L11 the practical route is fire CA output (burning cells, intensity) as a source term for a separate dispersion model (ATM-01).
- **Fire spotting in CA:** now covered by `hargrove2000simulating` (simple exponential rule with parameters), `lopezdecastro2024firespotting` (three schemes compared) and `alexandridis2011wildland` (unread).
- **Full texts still missing:** Ghisu 2015 ×2 (correction factors; ScienceDirect CAPTCHA, IRIS files restricted), Alexandridis 2008 and 2011, Ohgai 2007, Zhao 2011, Karafyllidis 1997, Berjak 2002, Jiang 2021. These need a manual download by the user (library access) if they matter for the model card.
- Historic town fire (URB-03): no European historic-town fire CA was found. Tan 2019 (with the Ohgai rule set) is now the most complete template.
- Fuel mapping for CZ: needs a translation from CORINE / Urban Atlas / forest stand maps to PROPAGATOR's 6 classes (whose full p_n matrix is now known) or to Scott & Burgan fuels. Kudláčková 2024 is the lead.
- Overlaps: ECO (fire–succession `millington2009modelling`, bark beetle → fire link L2), GEN (GPU/differentiable CA `xia2025pytorchfire`, event-driven "front over a cost raster" `johnston2008efficient`), MOV (evacuation after fire), ATM (smoke).

## Round 2 changes

| Key | Old score / class | New score / class | Reason |
|---|---|---|---|
| `trucchia2020propagator` | 9, A | 10, A | Full text read: rule equations, fuel matrix and per-fire metrics (S5 1 → 2). |
| `hargrove2000simulating` | 4, C (provisional) | 7, B | Full text read: complete procedure, full spread and firebrand tables, numerical test tables; code link dead (S3 0 → 1). |
| `tan2019fire` | 5, C (provisional) | 6, C | Full text read: all constants given (S2 1 → 2); some equations not legible, so S1 stays 1. |
| `sun2021adaptive` | 5, C (provisional) | 6, C | Full text read: equations and states given (S1 1 → 2); fuel coefficients only in cited sources. |
| `ohgai2007cellular` | 1, D | 3, D | Components restated in Tan 2019 (S1, S2 0 → 1); original still unread. |
| `sullivan2009wildland` | n/a | n/a | Access updated: arXiv preprint found. |
| `alexandridis2008cellular`, `ghisu2015optimal`, `ghisu2015improved`, `zhao2011simulation` | unchanged | unchanged | Full text attempted, no access. |
| `lopezdecastro2024firespotting` | – | 6, C (new, provisional) | Spotting schemes compared inside PROPAGATOR; code open. |
| `clarke1994cellular` | unverified lead | 5, C (new) | Located as grey literature; full text read. |
| `glasa2008elliptical` | – | n/a (new) | Central European fire-spread context, not CA. |

## New phenomena candidates (round 2)

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| Wildland–urban interface (WUI) fire | A wildfire reaches the edge of a settlement and ignites houses by flame contact, radiation and embers; forest cells and building cells follow different sub-rules. | Joins HAZ-01 and URB-03 into one scenario with a clear "what is at risk" output. | Moderate: villages and holiday cottages next to forests, e.g. around the 2022 Bohemian Switzerland fire area. | `jiang2021modelling` (C, provisional), `mahmoud2017probabilistic` (D) | Could be built from existing pieces (fire CA + Tan-style building rule). Not a longlist item; closest are HAZ-01 and URB-03. |
