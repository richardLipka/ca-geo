# Atmosphere, climate, water bodies and other — literature survey

Survey round: 1 (breadth-first), date 2026-10-12. Scoring per ../reimplementability-criteria.md.

> **Verification note.** The OpenAlex API was usable only for the first ~10 queries of this
> run; after that it returned HTTP 429 (daily free budget for the shared network IP exhausted,
> reset at midnight UTC). All bibliographic metadata below (title, authors, year, venue, volume,
> pages, DOI) was therefore verified via **Crossref** (`api.crossref.org/works/<DOI>`). Several
> publisher sites (ScienceDirect, MDPI, HAL, digibug.ugr.es, a Serbian repository) blocked
> automated full-text access, so most scores are **provisional (abstract)**. Full text could be
> read only for Copernicus (GMD, The Cryosphere) and JOSS papers plus model documentation.

## Search log

Date: 2026-10-12. "Hits" = total reported by the source (Crossref counts are relevance-ranked
totals and are only indicative).

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automata air pollution dispersion (sorted by citations) | OpenAlex | 717 | top hits off-topic (climate models); relevance mode used afterwards |
| title: cellular automata air pollution | OpenAlex | 3 | → sonnenschein2025hybrid |
| title: cellular automaton pollutant dispersion | OpenAlex | 0 | |
| title: cellular automata smoke | OpenAlex | 4 | only evacuation/field-burning conference items |
| cellular automata atmospheric dispersion advection diffusion | OpenAlex | 140 | → lauret2016atmospheric |
| cellular automata atmospheric dispersion | OpenAlex | 1037 | Lauret, oil spill CA, anthropogenic heat CA |
| cellular automata pollutant transport wind | OpenAlex | 487 | traffic-CA emissions, solute transport CA |
| cellular automata urban heat island land surface temperature | OpenAlex | 1705 | almost all CA–Markov land-use + LST regression |
| cellular automata snow cover / snowmelt / glacier | OpenAlex | 1781 / 338 / 719 | → pardoiguzquiza2017estimation; glacier: no CA ice-flow model |
| (OpenAlex budget exhausted from here on) | — | — | switched to Crossref + web search |
| cellular automata air pollutant dispersion | Crossref | 1.31 M | noisy; Guariso 1992 found via targeted query |
| cellular automata oil spill | Crossref | 1.19 M | Gług 2018, Zhang 2025, NOAA habitat CA |
| cellular automata snow cover | Crossref | 1.03 M | Collados-Lara 2019, Sharma 2019 |
| targeted title queries (Pardo-Igúzquiza, Karafyllidis, Guariso, Milašinović, Ashton, Dearing, Bentley, Nagel, Lin/Chen/Mynett, Liu 2022, Korsnes, Song, STMCA, anthropogenic heat, DESERTICAS, Rusinovic, Ashton 2006) | Crossref | — | DOI and metadata verification |
| cellular automata cold air drainage frost hollow | Crossref | 1.64 M | no CA model found (only classical meteorology papers) |
| cellular automata lake ice OR river ice | Crossref | 2.17 M | nothing relevant |
| cellular automata storm surge / sea level rise / coastal flood incursion | Crossref | 50 k–234 k | Hawick 2014 conference paper only (not assessed) |
| CA coastal erosion shoreline cliff | Web search | — | RUSICA, NEWTS, Seghir 2018 |
| CA salt marsh wetland sea level rise | Web search | — | Mariotti 2020, Bentley & Karunarathna |
| CA cold air drainage frost terrain | Web search | — | no CA; KLAM_21 (DWD, non-CA) as context |
| CA groundwater contaminant transport | Web search | — | Milašinović 2019, Ravazzani 2011, LGA 1995 |
| CA oil spill sea | Web search | — | Liu 2022, Zhang 2016/2025, Rušinović 2006, Karafyllidis 1997 |
| CA desertification | Web search | — | DESERTICAS, several theses |
| CA snow cover Sierra Nevada; ReSCAL snow | Web search | — | Collados-Lara/Pardo-Igúzquiza cluster; rescal-snow repo |
| CA air quality Guariso Maniezzo | Web search | — | Guariso 1992, follow-up 1996 |
| CA algal bloom lake | Web search | — | Chen & Mynett 2006, Taihu CA–GP |
| CA permafrost thermokarst | Web search | — | no CA (stochastic / process models only) |
| Coastline Evolution Model Ashton Murray | Web search | — | CSDMS CEM, cem-old repo |
| CA drought soil moisture | Web search | — | Song 2016, CATGRaSS (Landlab, overlaps eco) |
| CA glacier ice flow | Web search | — | no CA ice-flow paper; D8-routing glacier package (not CA) |
| CA sea level rise inundation GIS | Web search | — | CA mostly for urban growth + static bathtub |
| CA heavy gas dispersion terrain | Web search | — | Salcido 1993 lattice gas (not verifiable), Korean emergency CA, Fire 2025 |
| CA urban heat island diffusion green space | Web search | — | Kazak 2018 (PL), 3D CA chapter (2026, not verifiable) |
| CA sea ice floes; CA cloud formation; CA mangrove | Web search | — | Korsnes 2004; Nagel & Raschke 1992; Tomaz 2019 |
| GitHub: oil spill / snow / marsh / air pollution CA | GitHub (gh CLI) | 0–1 | only a student oil-spill repo; unauthenticated API rate-limited |

## Model families

1. **Pollutant / heat dispersion CA (advection–diffusion analogues).** Cell holds a concentration
   (or temperature); each step it exchanges mass with neighbours according to wind-weighted
   transfer coefficients plus decay. Classic: `guariso1992air`; data-driven rules:
   `lauret2016atmospheric` (ANN trained on CFD), `sonnenschein2025hybrid` (LUR baseline + CA
   off-road dispersion, GA calibration); micro-scale heat: `wagner2015cellular`. Urban heat island
   work is dominated by CA–Markov land-use projections combined with LST regression rather than a
   thermal CA (`kazak2018use`, EU/PL example). Cloud cover as a percolation-type CA:
   `nagel1992selforganizing`.
2. **Snow and ice.** Elevation/temperature/precipitation-driven snow-cover CA calibrated on MODIS
   (`pardoiguzquiza2017estimation`, `colladoslara2019distributed`); lattice-gas CA for wind-blown
   snow bedforms with open code (`sharma2019understanding`, `kochanski2019rescal`); sea-ice
   fracture/refreeze CA (`korsnes2004scaling`). No CA glacier-flow, lake-ice or cold-air-pooling
   model was found.
3. **Groundwater and solute transport (macroscopic / physically based CA).** Darcy fluxes between
   von Neumann neighbours with explicit head update (`ravazzani2011macroscopic`), coupled flow +
   contaminant transport CA benchmarked against MODFLOW/MT3DMS (`milasinovic2019coupled`),
   advection–diffusion–decay of solutes on flood CA (`wang2023novel`, overlaps `hyd`).
4. **Oil spill CA.** Oil mass per cell spreading to neighbours, shifted by wind/current drift,
   sometimes with weathering: `karafyllidis1997oil` (classic), `rusinovic2006cellular` (3D),
   `glug2018modeling` (CA + Lagrangian particles), `liu2022simulating` (Moore neighbourhood,
   NOAA wind/current), `zhang2025method` (logistic-regression-weighted stochastic CA).
5. **Coastal morphodynamics.** Cellular one-line shoreline model driven by wave-angle
   distribution (`ashton2001formation`, `ashton2006highangle`, open C code); cellular erosion of
   lake/sea coasts by fetch-dependent waves (`palermo2024newts`, open code, analytical tests);
   estuarine CA (`dearing2006modelling`, `bentley2012novel`).
6. **Wetlands, marshes, mangroves under sea-level rise.** Pond formation/expansion/drainage CA
   with elevation PDEs (`mariotti2020modeling`); mangrove migration by elevation thresholds versus
   rising sea level (`tomaz2019predicting`).
7. **Drought, soil moisture, desertification, water quality.** Data-driven soil-moisture CA
   (`song2016modeling`), MEDALUS-coupled desertification CA (`kone2021deserticas`), fuzzy-CA algal
   bloom model on top of a hydrodynamic water-quality model (`chen2006modelling`).

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| palermo2024newts | 2024 | NEWTS1.0 coastal erosion by waves | lake/sea coast erosion | square / 4- or 8-connected shoreline, ray-cast fetch / land–lake + strength / det. | 2 1 2 2 2 | 9 | A | USGS code release | OA | full text |
| ravazzani2011macroscopic | 2011 | MCA for groundwater | unconfined aquifer flow | square / von Neumann / hydraulic head / det. | 2 1 2 2 2 | 9 | A | FEST repo (chiselapp) | paywall | abstract + model manual |
| sharma2019understanding | 2019 | Snow bedforms with sintering | snow dunes / wind drift | 3D cubic / nearest-neighbour doublets / air, mobile, deposited snow (+age) / stoch. (Poisson) | 1 2 2 2 2 | 9 | A | rescal-snow (GPL) | OA | full text |
| kochanski2019rescal | 2019 | Rescal-snow software | snow dunes | as above (ReSCAL LGCA) | 1 2 2 2 1 | 8 | B | GitHub | OA | full text + repo docs |
| ashton2001formation | 2001 | Coastline features from high-angle waves | sandy coastline shape | 2D cells with fractional sand fill / along-shore neighbours / stoch. wave angle | 1 1 2 2 1 | 7 | B | cem-old (C) | paywall | abstract (provisional) |
| ashton2006highangle | 2006 | High-angle wave instability 1 | spits, capes, sand waves | as above (CEM) | 1 1 2 2 1 | 7 | B | cem-old (C) | paywall | abstract-level (provisional) |
| milasinovic2019coupled | 2019 | CA groundwater flow + pollution | contaminant transport | square / neighbours / head + concentration / det. | 1 1 0 2 2 | 6 | C | not found | preprint (repository, blocked) | abstract (provisional) |
| wang2023novel | 2023 | STMCA solute transport in floods | solute (E. coli) in floods | square / neighbours / depth, velocity, concentration / det. | 1 1 0 2 2 | 6 | C | not found | OA | abstract (provisional) |
| korsnes2004scaling | 2004 | Fracture and refreezing of sea ice | sea-ice floe sizes | lattice / neighbours / ice–crack / stoch. | 1 1 0 2 2 | 6 | C | not found | OA (arXiv) | abstract (provisional) |
| pardoiguzquiza2017estimation | 2017 | Snow covered area by CA | daily snow cover | DEM cells / neighbourhood / snow–no snow / calibrated rules | 1 1 0 2 1 | 5 | C | not found | OA (repository) | abstract (provisional) |
| colladoslara2019distributed | 2019 | Distributed CA, climate change on snow | snow cover under scenarios | as above, distributed by elevation band | 1 1 0 2 1 | 5 | C | not found | OA (repository) | abstract (provisional) |
| sonnenschein2025hybrid | 2025 | Hybrid CA air pollution for traffic | NO2 off-road dispersion | 50 m raster / neighbours / concentration / det., GA-calibrated | 1 1 0 1 2 | 5 | C | not found | OA | abstract (provisional) |
| liu2022simulating | 2022 | Offshore oil spills by CA | oil slick drift & spreading | square / Moore / oil state / det. | 1 1 0 2 1 | 5 | C | not found | OA | abstract (provisional) |
| zhang2025method | 2025 | Logistic regression + CA oil spill | oil slick extent | 6 m raster / Moore 3×3–7×7 / oil–no oil / stoch. | 1 1 0 1 2 | 5 | C | not found | OA | abstract (provisional) |
| tomaz2019predicting | 2019 | SLR on Amazon mangrove coast | mangrove migration / loss | GIS raster / neighbours / mangrove, water, land / det. thresholds | 1 1 0 1 2 | 5 | C | not found | OA | abstract (provisional) |
| wagner2015cellular | 2015 | CA anthropogenic heat | urban micro-scale heat | 3D cubic 0.15 m / neighbours / temperature / det. | 1 1 0 1 1 | 4 | C | not found | OA | abstract (provisional) |
| kazak2018use | 2018 | DSS for UHI, Wrocław | UHI exposure of land-use scenarios | Metronamica land-use CA + indicator overlay | 0 1 1 1 1 | 4 | C | closed tool | OA | abstract (provisional) |
| nagel1992selforganizing | 1992 | SOC in cloud formation? | cloud cluster formation | lattice / neighbours / active–cloud / stoch. percolation-like | 1 0 0 2 1 | 4 | C | not found | paywall | metadata + secondary descriptions |
| dearing2006modelling | 2006 | CA for coastal simulation | estuarine sedimentation, SLR | 1D/2D cells / neighbours / water, sediment / det. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| bentley2012novel | 2012 | Novel CA estuarine morphodynamics | estuary bathymetry, salt marsh | rectangular cells / routing neighbours / depth, marsh / det. | 1 1 0 1 1 | 4 | C | not found | OA | abstract (provisional) |
| mariotti2020modeling | 2020 | Marsh ponds, New England | pond dynamics under SLR | raster / neighbours / marsh–pond–mudflat + elevation PDE / stoch. | 1 1 0 1 1 | 4 | C | not found | preprint | abstract (provisional) |
| song2016modeling | 2016 | Deep-learning CA soil moisture | soil moisture field | macroscopic CA / neighbours / continuous SMC / DBN rule | 1 0 0 1 2 | 4 | C | not found | OA | abstract (secondary) |
| guariso1992air | 1992 | Air quality simulation through CA | air pollutant dispersion | (not assessable) | 1 0 0 1 1 | 3 | D | not found | paywall | metadata + secondary descriptions |
| lauret2016atmospheric | 2016 | ANN-based CA dispersion | near-field gas dispersion, industrial site | grid / neighbours / concentration / ANN rule trained on CFD | 1 0 0 1 1 | 3 | D | not found | preprint (HAL, blocked) | secondary descriptions |
| karafyllidis1997oil | 1997 | Oil slick movement by CA | oil slick | (not assessable) | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only |
| rusinovic2006cellular | 2006 | CA oil slick behaviour | 3D oil weathering & transport | 3D cells / neighbours / oil fractions | 1 0 0 1 1 | 3 | D | not found | paywall | metadata + secondary snippet |
| glug2018modeling | 2018 | Lagrangian particles + CA oil spill | oil slick | hybrid particle–CA | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only |
| kone2021deserticas | 2021 | DESERTICAS | desertification | continuous CA + MEDALUS indices | 1 0 0 1 1 | 3 | D | not found | paywall | metadata + secondary snippet |
| chen2006modelling | 2006 | Fuzzy CA algal blooms | algal bloom (chlorophyll-a) | Delft3D-WAQ grid / neighbours / biomass / fuzzy rules | 1 0 0 1 1 | 3 | D | not found | paywall (repository record) | abstract (provisional) |

## Entries

### palermo2024newts — NEWTS1.0: Numerical model of coastal Erosion by Waves and Transgressive Scarps
- **Citation:** Palermo, R. V., Perron, J. T., Soderblom, J. M., Birch, S. P. D., Hayes, A. G., Ashton, A. D. (2024). NEWTS1.0: Numerical model of coastal Erosion by Waves and Transgressive Scarps. *Geoscientific Model Development* 17(8), 3433–3445. DOI: 10.5194/gmd-17-3433-2024 (verified: Crossref)
- **Access:** OA (https://gmd.copernicus.org/articles/17/3433/2024/)
- **Phenomenon and study area:** Long-term retreat of coasts of closed basins (lakes, flooded topography; motivated by Titan's lakes); qualitative comparison with Lake Rotoehu (NZ) and Plitvice lakes (HR, EU).
- **Model:** Square raster, binary land/lake cells set by lake level; each land cell carries a "strength". Shoreline cells (4-connected recommended) lose strength by (a) uniform erosion at constant rate scaled by number of exposed sides/corners and (b) wave erosion proportional to the integral of fetch × cos(wave angle − shoreline azimuth); fetch computed by casting rays every ~2° across the lake. A cell with zero strength becomes lake and the shoreline is retraced; leftover time is passed to new shoreline neighbours. Lakes are found by 8-connected labelling and processed hierarchically. Order per step: lake-level change → wave erosion → uniform erosion; adaptive sub-stepping; periodic grid.
- **Inputs:** DEM (synthetic fractal terrain in the paper), lake level history, wave-erosion and uniform-erosion coefficients.
- **Parameters:** k_wave, k_uniform, ray angle, ray step, threshold α given in text; S0, A0, Δx, scarp depth not fixed numerically.
- **Code:** https://code.usgs.gov/spcmsc/newts (via USGS DOI 10.5066/P9Q6GDGP; link checked, HTTP 200; language not confirmed).
- **Validation:** Circular-lake tests against analytical solutions for uniform (r = r0 + k t) and wave erosion; area error < 2 % with 4-connectivity, ~7 % with 8-connectivity; fetch convergence tests; resolution independence.
- **Reimplementability:** S1 2 – full algorithm incl. update order and boundaries; S2 1 – some constants unspecified; S3 2; S4 2 – runs on any DEM + water level; S5 2 – analytical benchmarks → 9, A. Assessed from: full text
- **Browser fit:** Good for moderate grids; ray casting per shoreline cell is the cost driver (can be reduced with fewer rays). Strong interactive demo: raise water level, watch coast erode.
- **Relevance to ca-geo:** new item (coastal / reservoir shore erosion; could apply to Czech reservoirs, LND-03 post-mining lakes shore retreat). Analytical tests are ideal for our test suite.

### ravazzani2011macroscopic — Macroscopic cellular automata for groundwater modelling: A first approach
- **Citation:** Ravazzani, G., Rametta, D., Mancini, M. (2011). Macroscopic cellular automata for groundwater modelling: A first approach. *Environmental Modelling & Software* 26(5), 634–643. DOI: 10.1016/j.envsoft.2010.11.011 (verified: Crossref)
- **Access:** paywall; model equations documented openly in the FEST manual (https://www.fest.polimi.it/reference/groundwater.html).
- **Phenomenon and study area:** 2D flow in unconfined aquifers; tests against Theis solution and MODFLOW-2000; FEST applied in northern Italy (Po valley, EU).
- **Model:** Square cells; von Neumann neighbourhood; flux between neighbours = harmonic mean of transmissivities × head difference (Darcy); head update h(t+1) = h(t) + Q·Δt/(S_y·Δs²); sources/sinks; Dirichlet and Neumann boundary cells; river–aquifer exchange via streambed conductance. Deterministic, explicit.
- **Inputs:** Hydraulic conductivity, specific yield, aquifer bottom elevation, initial heads, recharge.
- **Parameters:** Physically based (no calibration of CA weights); time step 4000 s in tests, no stated stability criterion.
- **Code:** FEST repository https://chiselapp.com/user/giovanni.ravazzani/repository/fest/ (HTTP 200; FEST docs describe GPL licence — not independently confirmed).
- **Validation:** Theis drawdown and river-stage response vs analytical solution and MODFLOW-2000.
- **Reimplementability:** S1 2 – complete local rule in manual; S2 1 – stability/Δt choice not given; S3 2; S4 2 – Theis test is generic; S5 2 – analytical benchmark → 9, A. Assessed from: abstract + model documentation (paper full text not read)
- **Browser fit:** Excellent (simple explicit stencil, WebGL-friendly).
- **Relevance to ca-geo:** LND-03 (post-mining lake filling from groundwater), ATM-04 (drought/groundwater), contaminant-plume demo. Same numerical skeleton as the WAT model.

### sharma2019understanding — Understanding snow bedform formation by adding sintering to a cellular automata model
- **Citation:** Sharma, V., Braud, L., Lehning, M. (2019). Understanding snow bedform formation by adding sintering to a cellular automata model. *The Cryosphere* 13(12), 3239–3260. DOI: 10.5194/tc-13-3239-2019 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** Wind-driven snow dunes/barchans; idealised domain (~325 m × 6.5 m).
- **Model:** ReSCAL: 3D lattice with air / mobile snow / deposited snow cells; transitions on neighbour pairs (deposition, erosion, transport, gravity, diffusion, avalanching) with rates Λ, stochastic Poisson time step; flow from a lattice-gas CA providing shear stress. Sintering: erodibility of deposited cells decreases linearly with age, zero after 24 h.
- **Inputs:** None geographic; initial snow cone/flat bed; wind strength parameter.
- **Parameters:** Physical and model constants given (cell aspect, length scale, densities, grain size, τ thresholds, sintering time).
- **Code:** ReSCAL original site http://rescal.geophysx.org/ is dead (HTTP 410); the snow fork https://github.com/kellykochanski/rescal-snow (GPL-3.0, HTTP 200) implements the sintering parameter.
- **Validation:** Fastest-growing wavelength matches linear stability theory; dune speeds vs field observations; maximum mobile bedform lengths per wind class.
- **Reimplementability:** S1 1 – full transition table delegated to Narteau et al. 2009; S2 2; S3 2; S4 2; S5 2 → 9, A. Assessed from: full text
- **Browser fit:** Heavy (3D LGCA, many steps); a 2D slice would be feasible but is a different model.
- **Relevance to ca-geo:** HYD-06 (snow) only loosely — micro-scale snow drift, not catchment snow cover. Best as an "unusual" showcase.

### kochanski2019rescal — Rescal-snow: Simulating snow dunes with cellular automata
- **Citation:** Kochanski, K., Defazio, G.-C., Green, E., Barnes, R., Downie, C., Rubin, A., Rountree, B. (2019). Rescal-snow: Simulating snow dunes with cellular automata. *Journal of Open Source Software* 4(42), 1699. DOI: 10.21105/joss.01699 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** Snow dunes and snow waves; idealised.
- **Model:** ReSCAL lattice-gas CA (C core) extended with snowfall (λ_I), sintering (λ_S, λ_F), settling (Coef_A); boundary modes open/periodic/reinjection.
- **Inputs:** Parameter and run files; non-dimensional with a "real data" conversion file.
- **Parameters:** Documented in `docs/rescal-snow-inputs.md` with example parameter files.
- **Code:** https://github.com/kellykochanski/rescal-snow (GPL-3.0-or-later, C + Python; HTTP 200); Zenodo archive DOI 10.5281/zenodo.3517217 resolves.
- **Validation:** Example runs and calibration notes; quantitative checks are in companion papers.
- **Reimplementability:** S1 1 – rules referenced to Narteau 2009 rather than restated; S2 2; S3 2; S4 2; S5 1 → 8, B. Assessed from: full text + repository docs
- **Browser fit:** Heavy; reference implementation rather than a browser candidate.
- **Relevance to ca-geo:** reference code for snow drift; pairs with sharma2019understanding.

### ashton2001formation — Formation of coastline features by large-scale instabilities induced by high-angle waves
- **Citation:** Ashton, A., Murray, A. B., Arnoult, O. (2001). Formation of coastline features by large-scale instabilities induced by high-angle waves. *Nature* 414(6861), 296–300. DOI: 10.1038/35104541 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Emergence of capes, cuspate forelands and spits on sandy coasts; Carolina coast (USA) wave data.
- **Model:** Cellular plan-view shoreline model (CEM): cells hold a fraction of sand; along-shore sediment flux depends on local shoreline angle relative to wave approach (CERC-type), with waves drawn from a distribution controlled by asymmetry and fraction of high-angle waves; cells fill/empty as flux converges/diverges.
- **Inputs:** Initial shoreline, wave climate (2 parameters).
- **Parameters:** Wave climate parameters; transport constants (details in 2006 JGR papers).
- **Code:** https://github.com/csdms/cem-old (C, MIT/GPL, parameter files `cem.prm`, `waves.prm`; HTTP 200). CSDMS model page not reachable during this run.
- **Validation:** Qualitative resemblance to Carolina capes; wave-data support.
- **Reimplementability:** S1 1; S2 1 (abstract caps); S3 2; S4 2 – synthetic coast + 2 wave parameters; S5 1 → 7, B. Assessed from: abstract (provisional)
- **Browser fit:** Very good (1D-ish shoreline on a 2D grid, cheap per step, visually striking).
- **Relevance to ca-geo:** new "coastline" item; not CZ but a classic, well-documented CA-like geomorphic model. Overlaps `geo`.

### ashton2006highangle — High-angle wave instability and emergent shoreline shapes: 1. Modeling of sand waves, flying spits, and capes
- **Citation:** Ashton, A. D., Murray, A. B. (2006). High-angle wave instability and emergent shoreline shapes: 1. Modeling of sand waves, flying spits, and capes. *Journal of Geophysical Research: Earth Surface* 111(F4). DOI: 10.1029/2005JF000422 (verified: Crossref)
- **Access:** paywall (AGU; older AGU papers often free to read — check in round 2)
- **Phenomenon and study area:** Same model as above, full description and parameter exploration.
- **Model / Inputs / Parameters:** CEM; CSDMS names this paper as the full theory and parameter reference.
- **Code:** as above (cem-old).
- **Validation:** Model experiments on emergent shapes; part 2 (DOI 10.1029/2005JF000423) compares with nature.
- **Reimplementability:** S1 1, S2 1 (not read), S3 2, S4 2, S5 1 → 7, B. Assessed from: abstract-level (provisional); likely B→A after full-text reading.
- **Browser fit:** as above.
- **Relevance to ca-geo:** primary spec document for a CEM port.

### milasinovic2019coupled — Coupled groundwater hydrodynamic and pollution transport modelling using Cellular Automata approach
- **Citation:** Milašinović, M., Ranđelović, A., Jaćimović, N., Prodanović, D. (2019). Coupled groundwater hydrodynamic and pollution transport modelling using Cellular Automata approach. *Journal of Hydrology* 576, 652–666. DOI: 10.1016/j.jhydrol.2019.06.062 (verified: Crossref)
- **Access:** paywall; author version in Belgrade repository (grafar.grf.bg.ac.rs, blocked by bot check)
- **Phenomenon and study area:** Contaminant transport under unsteady groundwater conditions driven by surface–groundwater interaction (Serbia, EU candidate country).
- **Model:** CA for groundwater heads coupled with CA advection–dispersion of concentration; explicit neighbour exchange.
- **Inputs:** Aquifer properties, boundary/river stages, source terms.
- **Parameters:** Not visible in abstract.
- **Code:** not found.
- **Validation:** Analytical solutions and MODFLOW + MT3DMS; up to 10× speed-up; best for diffusion-dominated cases.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 2 → 6, C. Assessed from: abstract (provisional)
- **Browser fit:** Good.
- **Relevance to ca-geo:** contaminant plume demo on top of ravazzani2011macroscopic.

### wang2023novel — A Novel Cellular Automata Framework for Modeling Depth-Averaged Solute Transport during Pluvial and Fluvial Floods
- **Citation:** Wang, C.-H., Yu, H.-L., Chang, T.-J. (2023). A Novel Cellular Automata Framework for Modeling Depth-Averaged Solute Transport during Pluvial and Fluvial Floods. *Water* 16(1), 129. DOI: 10.3390/w16010129 (verified: Crossref)
- **Access:** OA (MDPI; automated access blocked)
- **Phenomenon and study area:** Solute (E. coli) transport during floods, Taiwan.
- **Model:** STMCA: explicit algebraic CA equations for advection, turbulent diffusion and decay on top of a flood CA.
- **Inputs:** Flood depths/velocities, initial concentrations.
- **Parameters:** Not visible in abstract.
- **Code:** not found.
- **Validation:** Four benchmark cases vs Godunov FV-TVD; same accuracy, ~3× faster.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 2 → 6, C. Assessed from: abstract (provisional)
- **Browser fit:** Good if coupled to our WAT flow model.
- **Relevance to ca-geo:** pollutant-in-floodwater scenario for WAT; overlaps `hyd`.

### korsnes2004scaling — Scaling in fracture and refreezing of sea ice
- **Citation:** Korsnes, R., Souza, S. R., Donangelo, R., Hansen, A., Paczuski, M., Sneppen, K. (2004). Scaling in fracture and refreezing of sea ice. *Physica A* 331(1–2), 291–296. DOI: 10.1016/S0378-4371(03)00627-7 (verified: Crossref)
- **Access:** OA preprint arXiv:cond-mat/0309447 (abstract page checked)
- **Phenomenon and study area:** Floe-size distribution, Kara Sea satellite data.
- **Model:** Cellular model competing random fracture (strain) and refreezing of cracks.
- **Inputs:** None geographic (statistical comparison only).
- **Parameters:** Fracture/refreeze probabilities (values not seen).
- **Code:** not found.
- **Validation:** Power-law exponent τ = 1.6 ± 0.2 from data vs model.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 2 → 6, C. Assessed from: abstract (provisional)
- **Browser fit:** Excellent (tiny, fast).
- **Relevance to ca-geo:** unusual curiosity; inspiration for lake-ice break-up demo (no lake-ice CA found).

### pardoiguzquiza2017estimation — Estimation of the spatiotemporal dynamics of snow covered area by using cellular automata models
- **Citation:** Pardo-Igúzquiza, E., Collados-Lara, A.-J., Pulido-Velazquez, D. (2017). Estimation of the spatiotemporal dynamics of snow covered area by using cellular automata models. *Journal of Hydrology* 550, 230–238. DOI: 10.1016/j.jhydrol.2017.04.058 (verified: Crossref)
- **Access:** OA author version (digibug.ugr.es handle 10481/101584; server timed out)
- **Phenomenon and study area:** Daily snow covered area, Sierra Nevada (Spain, EU).
- **Model:** Calibrated CA: snow state of a cell changes depending on its altitude, temperature and precipitation indices and the snow state of neighbours.
- **Inputs:** DEM (cell altitude), precipitation and temperature indices; MODIS/Landsat snow maps for calibration.
- **Parameters:** Calibrated against satellite SCA (procedure described, values not seen).
- **Code:** not found.
- **Validation:** Against satellite SCA (metrics not seen).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2 – DEM + ERA5/E-OBS + MODIS snow are open, S5 1 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** Excellent (binary state, daily step, few rules).
- **Relevance to ca-geo:** **HYD-06** snowmelt / snow cover — the best fit for a CZ demo (Krkonoše/Šumava with Copernicus snow products); feeds L6 chain.

### colladoslara2019distributed — A distributed cellular automata model to simulate potential future impacts of climate change on snow cover area
- **Citation:** Collados-Lara, A.-J., Pardo-Igúzquiza, E., Pulido-Velazquez, D. (2019). A distributed cellular automata model to simulate potential future impacts of climate change on snow cover area. *Advances in Water Resources* 124, 106–119. DOI: 10.1016/j.advwatres.2018.12.010 (verified: Crossref)
- **Access:** OA author version (digibug.ugr.es handle 10481/99074; timed out)
- **Phenomenon and study area:** Snow cover under climate scenarios (2071–2100), Sierra Nevada (Spain, EU).
- **Model:** Distributed version of the above (parameters vary with elevation), driven by perturbed climate series.
- **Inputs:** DEM, temperature and precipitation scenarios, MODIS SCA.
- **Parameters:** Calibration/validation procedure.
- **Code:** not found.
- **Validation:** Calibration/validation on satellite SCA; mean SCA reduction 60.4 % reported.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** HYD-06 climate-scenario slider ("+2 °C").

### sonnenschein2025hybrid — Hybrid cellular automata-based air pollution model for traffic scenario microsimulations
- **Citation:** Sonnenschein, T. S., Yuan, Z., Khan, J., Kerckhoffs, J., Vermeulen, R. C. H., Scheider, S. (2025). Hybrid cellular automata-based air pollution model for traffic scenario microsimulations. *Environmental Modelling & Software* 186, 106356. DOI: 10.1016/j.envsoft.2025.106356 (verified: Crossref)
- **Access:** OA (ScienceDirect blocked automated reading)
- **Phenomenon and study area:** NO2 from traffic, Amsterdam (NL, EU).
- **Model:** Land-use-regression baseline + on-road emissions, CA spreads pollution off-road to neighbouring cells (wind and land-use dependent), GA-calibrated.
- **Inputs:** 50 m raster, traffic emissions, LUR baseline, meteorology.
- **Parameters:** Calibrated by genetic algorithm (values not seen).
- **Code:** not found (web search).
- **Validation:** External R² 0.60 vs mobile and fixed NO2 monitoring; lockdown scenario R² 0.57; 0.48 s runtime.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** Very good (fast by design).
- **Relevance to ca-geo:** **ATM-01** — closest modern template for a CZ city (Ostrava/Praha NO2 with ČHMÚ stations). Read full text in round 2 (OA).

### liu2022simulating — Simulating and Predicting Offshore Oil Spills by Using Cellular Automata
- **Citation:** Liu, L., Li, W., Cui, Y., Hu, G., Li, H. (2022). Simulating and Predicting Offshore Oil Spills by Using Cellular Automata. *Journal of Marine Science and Technology* 30(3), 203–216. DOI: 10.51400/2709-6998.2577 (verified: Crossref)
- **Access:** OA (journal PDF link exists; automated access forbidden)
- **Phenomenon and study area:** Offshore oil slick drift and spreading; NOAA wind/current data.
- **Model:** New diffusion and drift rules accounting for wind and current fields; Moore neighbourhood; plus fuzzy severity grading in a software system (OOSIS).
- **Inputs:** Wind and current fields, spill source.
- **Parameters:** Not visible.
- **Code:** not found.
- **Validation:** Demonstration runs (metrics not seen).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** Good.
- **Relevance to ca-geo:** template for a river/lake spill variant (Labe/Vltava accident scenario).

### zhang2025method — A method to modelling oil spill using combination of logistic regression and cellular automata
- **Citation:** Zhang, Y., Li, S. (2025). A method to modelling oil spill using combination of logistic regression and cellular automata. *MethodsX* 15, 103474. DOI: 10.1016/j.mex.2025.103474 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** Oil slick extent, DeepSpill experiment data.
- **Model:** Stochastic CA: transition probability = logistic regression of drivers (currents, wind, salinity, etc.) × neighbourhood density × random term; tested 3×3 to 7×7 Moore neighbourhoods.
- **Inputs:** Rasters of drivers, resampled (6 m optimal).
- **Parameters:** Fitted by LR on Monte Carlo samples; sensitivity to sampling ratio, scale, neighbourhood.
- **Code:** not found.
- **Validation:** Accuracy up to 97.4 % (7×7 neighbourhood).
- **Reimplementability:** S1 1, S2 1 (procedure reproducible, but capped by abstract), S3 0, S4 1, S5 2 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** Good.
- **Relevance to ca-geo:** generic "LR-weighted stochastic CA" recipe (same as many LUCC CA).

### tomaz2019predicting — Predicting the impacts of sea-level rise on the Amazon macrotidal mangrove coast
- **Citation:** Tomaz, R. B., dos Santos, A. L. S., Borges, H. P., Silva Júnior, C. H. L., Bezerra, D. da S. (2019). Predicting the impacts of sea-level rise on the Amazon macrotidal mangrove coast. *Revista Brasileira de Climatologia* 25. DOI: 10.5380/abclima.v25i0.60891 (verified: Crossref)
- **Access:** OA (journal PDF returned HTTP 500 during this run)
- **Phenomenon and study area:** Mangrove inundation and landward migration, eastern Amazon coast.
- **Model:** CA–GIS: 90 incremental SLR events of 3.18 mm/yr (2010–2100); cells convert between mangrove, water and land based on elevation relative to sea level and neighbourhood.
- **Inputs:** DEM, mangrove map.
- **Parameters:** SLR increments given; thresholds not seen.
- **Code:** not found.
- **Validation:** Area statistics only (loss 30.24 %, +301 km² inland).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** Excellent (threshold rule on DEM).
- **Relevance to ca-geo:** "rising water level vs. vegetation belt" demo; transferable to reservoir drawdown/wetland belts.

### wagner2015cellular — Cellular Automata-based Anthropogenic Heat Simulation
- **Citation:** Wagner, M., Viswanathan, V., Pelzer, D., Berger, M., Aydt, H. (2015). Cellular Automata-based Anthropogenic Heat Simulation. *Procedia Computer Science* 51, 2107–2116. DOI: 10.1016/j.procs.2015.05.480 (verified: Crossref)
- **Access:** OA (automated access blocked)
- **Phenomenon and study area:** Dispersion of traffic heat emissions at street scale (Singapore context).
- **Model:** 3D cubic CA, 0.15 m cells; only temperature/heat differences modelled; radiation, convection and turbulence parameterised by scale.
- **Inputs:** Geometry, heat sources (traffic agents).
- **Parameters:** Not visible.
- **Code:** not found.
- **Validation:** Speed comparison with CFD; qualitative.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** Only in 2D reduction.
- **Relevance to ca-geo:** URB-01 thermal-exchange idea (heat diffusing between cells).

### kazak2018use — The Use of a Decision Support System for Sustainable Urbanization and Thermal Comfort … Wrocław Larger Urban Zone (Poland)
- **Citation:** Kazak, J. (2018). The Use of a Decision Support System for Sustainable Urbanization and Thermal Comfort in Adaptation to Climate Change Actions—The Case of the Wrocław Larger Urban Zone (Poland). *Sustainability* 10(4), 1083. DOI: 10.3390/su10041083 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** UHI exposure of future land-use scenarios, Wrocław (PL, EU, near CZ border).
- **Model:** Metronamica land-use CA scenarios + GIS indicator assessment of UHI exposure.
- **Inputs:** Land use (CORINE/Urban Atlas type), zoning, accessibility.
- **Parameters:** Scenario-specific.
- **Code:** Metronamica is a closed commercial tool.
- **Validation:** Scenario comparison only.
- **Reimplementability:** S1 0, S2 1, S3 1, S4 1, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** n/a (land-use CA handled in `lu`).
- **Relevance to ca-geo:** URB-01 — shows that UHI "CA" in literature is usually land-use CA + indicator; a CZ/EU-near example.

### nagel1992selforganizing — Self-organizing criticality in cloud formation?
- **Citation:** Nagel, K., Raschke, E. (1992). Self-organizing criticality in cloud formation? *Physica A* 182(4), 519–531. DOI: 10.1016/0378-4371(92)90018-L (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Cloud cluster formation; fractal perimeter of clouds.
- **Model:** Percolation-like CA where cells are cloud/active based on humidity and vertical velocity; feedback keeps occupation near the percolation threshold (from secondary descriptions).
- **Inputs:** None geographic.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** Perimeter fractal dimension vs observations.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 2, S5 1 → 4, C. Assessed from: metadata + secondary descriptions (provisional)
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** unusual atmospheric demo; later CA cloud models (Silva 2019, Najafi 2021, Cheraghalizadeh 2024) are unverified leads.

### dearing2006modelling — Modelling approaches for coastal simulation based on cellular automata: the need and potential
- **Citation:** Dearing, J. A., Richmond, N., Plater, A. J., Wolf, J., Prandle, D., Coulthard, T. J. (2006). Modelling approaches for coastal simulation based on cellular automata: the need and potential. *Phil. Trans. R. Soc. A* 364(1841), 1051–1071. DOI: 10.1098/rsta.2006.1753 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Estuarine sedimentation, tidal cycle and SLR; Blackwater Estuary (UK).
- **Model:** Prototype integrated cellular coastal model (tide, waves, sediment) — 1D and 2D tests; also a position paper on CA for coasts.
- **Inputs:** Bathymetry, tide levels, wave height.
- **Parameters:** Preliminary parameterisation for the case study.
- **Code:** not found (related to CAESAR lineage via Coulthard).
- **Validation:** Simple tests; water/sediment transport good, tidal current vectors poorly reproduced.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** Medium.
- **Relevance to ca-geo:** entry point for coastal CA; links to CAESAR (likely in `geo`/`hyd`).

### bentley2012novel — A novel cellular automata approach to estuarine morphodynamic modelling
- **Citation:** Bentley, I., Karunarathna, H. (2012). A novel cellular automata approach to estuarine morphodynamic modelling. *Coastal Engineering Proceedings* 33, 27. DOI: 10.9753/icce.v33.sediment.27 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** Estuary morphology over years–decades, incl. salt-marsh ecology.
- **Model:** Rectangular CA cells; tidal flow by a new routing scheme; simplified waves, sediment transport, marsh.
- **Inputs:** Initial bathymetry, tides, waves.
- **Parameters:** Not seen.
- **Code:** not found.
- **Validation:** Tidal routing agrees with a conventional 2D hydrodynamic model.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** Medium.
- **Relevance to ca-geo:** context for coastal/estuarine family.

### mariotti2020modeling — Modeling the spatial dynamics of marsh ponds in New England salt marshes
- **Citation:** Mariotti, G., Spivak, A. C., Luk, S. Y., Ceccherini, G., Tyrrell, M., Eagle Gonneea, M. (2020). Modeling the spatial dynamics of marsh ponds in New England salt marshes. *Geomorphology* 365, 107262. DOI: 10.1016/j.geomorph.2020.107262 (verified: Crossref)
- **Access:** paywall; preprint PDF on WHOI site (not text-extractable by our tools)
- **Phenomenon and study area:** Pond formation, expansion, drainage and recovery under relative SLR; Barnstable marsh (MA, USA).
- **Model:** CA for pond processes (stochastic formation, expansion, drainage when connected to channels) coupled with PDEs for marsh/pond elevation.
- **Inputs:** Marsh map, channel network, sediment supply, SLR rate.
- **Parameters:** Pond formation rate estimated from size distributions; expansion rate from 41-year remote sensing.
- **Code:** not found.
- **Validation:** Modelled vs observed pond size distribution and pond depths.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** Good.
- **Relevance to ca-geo:** wetland CA template; inspiration for ECO-05 (beaver wetlands) pond dynamics.

### song2016modeling — Modeling spatio-temporal distribution of soil moisture by deep learning-based cellular automata model
- **Citation:** Song, X., Zhang, G., Liu, F., Li, D., Zhao, Y., Yang, J. (2016). Modeling spatio-temporal distribution of soil moisture by deep learning-based cellular automata model. *Journal of Arid Land* 8(5), 734–748. DOI: 10.1007/s40333-016-0049-0 (verified: Crossref)
- **Access:** OA (journal PDF)
- **Phenomenon and study area:** Soil moisture over a 22 km² irrigated corn field, NW China.
- **Model:** Macroscopic CA with a deep belief network learning the transition rule; SGS for uncertainty.
- **Inputs:** Soil moisture observations, covariates.
- **Parameters:** Learned network weights (not reproducible from paper).
- **Code:** not found.
- **Validation:** RMSE 18 % lower than MLP-based CA.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 2 → 4, C. Assessed from: abstract (secondary summary; provisional)
- **Browser fit:** Rule would have to be replaced by a simple water balance.
- **Relevance to ca-geo:** ATM-04 — shows soil-moisture CA exists but is data-driven; supports the longlist note that drought is mostly cell-local.

### guariso1992air — Air quality simulation through cellular automata
- **Citation:** Guariso, G., Maniezzo, V. (1992). Air quality simulation through cellular automata. *Environmental Software* 7(3), 131–141. DOI: 10.1016/0266-9838(92)90010-2 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Air pollutant dispersion (Italy).
- **Model:** Early CA for pollutant transport (rules not seen); follow-up on parallel implementation: Guariso, Maniezzo, Salomoni 1996 (DOI 10.1016/0096-3003(95)00214-6).
- **Inputs / Parameters / Validation:** not assessable.
- **Code:** not found.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: metadata + secondary descriptions
- **Browser fit:** likely good.
- **Relevance to ca-geo:** foundational for ATM-01; full text needed (round 2).

### lauret2016atmospheric — Atmospheric dispersion modeling using Artificial Neural Network based cellular automata
- **Citation:** Lauret, P., Heymes, F., Aprin, L., Johannet, A. (2016). Atmospheric dispersion modeling using Artificial Neural Network based cellular automata. *Environmental Modelling & Software* 85, 56–69. DOI: 10.1016/j.envsoft.2016.08.001 (verified: Crossref)
- **Access:** preprint on HAL (hal-01962455; bot protection blocked reading)
- **Phenomenon and study area:** Near-field gas dispersion on an industrial site with obstacles.
- **Model:** CA whose local transition is an ANN trained on CFD (RANS k-ε) results (from companion CET 2013/2014 papers).
- **Inputs:** Site geometry, wind; CFD training database.
- **Parameters:** ANN weights — not reproducible without data.
- **Code:** not found.
- **Validation:** Against CFD (metrics not seen).
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: secondary descriptions (provisional)
- **Browser fit:** Inference is cheap; training data is the obstacle.
- **Relevance to ca-geo:** ATM-03 (heavy gas / industrial release) context.

### karafyllidis1997oil — A model for the prediction of oil slick movement and spreading using cellular automata
- **Citation:** Karafyllidis, I. (1997). A model for the prediction of oil slick movement and spreading using cellular automata. *Environment International* 23(6), 839–850. DOI: 10.1016/S0160-4120(97)00096-2 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Oil slick drift and spreading (sea).
- **Model:** Classic CA oil-spill model by the author of a well-known CA fire model; rules not seen.
- **Code:** not found.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: metadata only
- **Browser fit:** likely excellent.
- **Relevance to ca-geo:** priority full-text read in round 2 (probably B if rules are as complete as in the author's fire CA).

### rusinovic2006cellular — Cellular automata based model for the prediction of oil slicks behavior
- **Citation:** Rusinovic, Z., Bogunovic, N. (2006). Cellular automata based model for the prediction of oil slicks behavior. *28th International Conference on Information Technology Interfaces, 2006*, 569–574. DOI: 10.1109/ITI.2006.1708543 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Hypothetical slick (Croatia, EU).
- **Model:** 3D CA with vertical transport, evaporation, wind/current advection, dissolution, deposition, emulsification (from search snippet).
- **Code:** not found.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: metadata + secondary snippet
- **Browser fit:** 2D surface layer feasible.
- **Relevance to ca-geo:** weathering processes list for an oil-spill demo.

### glug2018modeling — Modeling of oil spill spreading disasters using combination of Langrangian discrete particle algorithm with Cellular Automata approach
- **Citation:** Gług, M., Wąs, J. (2018). Modeling of oil spill spreading disasters using combination of Langrangian discrete particle algorithm with Cellular Automata approach. *Ocean Engineering* 156, 396–405. DOI: 10.1016/j.oceaneng.2018.01.029 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Oil spill spreading (Poland, EU group, AGH Kraków).
- **Model:** Hybrid of Lagrangian particles and CA (details not seen).
- **Code:** not found.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: metadata only
- **Browser fit:** good.
- **Relevance to ca-geo:** EU example; read in round 2.

### kone2021deserticas — DESERTICAS, a Software to Simulate Desertification Based on MEDALUS and Cellular Automata
- **Citation:** Koné, A., Fontaine, A., Loireau, M., Jangorzo, S. N., El Yacoubi, S. (2021). DESERTICAS, a Software to Simulate Desertification Based on MEDALUS and Cellular Automata. *Lecture Notes in Computer Science*, 198–208. DOI: 10.1007/978-3-030-69480-7_20 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Desertification sensitivity dynamics (Sahel).
- **Model:** Continuous CA evolving MEDALUS quality indices (soil, climate, vegetation, management) with neighbourhood influence and anthropogenic factors.
- **Code:** not found (software named but no public link found).
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: metadata + secondary snippet
- **Browser fit:** good.
- **Relevance to ca-geo:** ATM-04 drought/degradation indices — MEDALUS indices could be computed from CZ data.

### chen2006modelling — Modelling algal blooms in the Dutch coastal waters by integrated numerical and fuzzy cellular automata approaches
- **Citation:** Chen, Q., Mynett, A. E. (2006). Modelling algal blooms in the Dutch coastal waters by integrated numerical and fuzzy cellular automata approaches. *Ecological Modelling* 199(1), 73–81. DOI: 10.1016/j.ecolmodel.2006.06.014 (verified: Crossref)
- **Access:** paywall (repository record ir.rcees.ac.cn)
- **Phenomenon and study area:** Algal biomass (chlorophyll-a), Dutch coastal waters (NL, EU), year 1995.
- **Model:** Delft3D-WAQ computes abiotic conditions; fuzzy-rule CA predicts biomass from irradiance, nutrients and neighbour states.
- **Inputs:** Hydrodynamic/water-quality model output.
- **Parameters:** Fuzzy membership functions/rules (expert-defined).
- **Code:** not found.
- **Validation:** Compared with BLOOM II model output.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: abstract (provisional)
- **Browser fit:** CA part cheap; drivers would need simplification.
- **Relevance to ca-geo:** cyanobacteria bloom in Czech reservoirs/fishponds (new idea) — water-body CA family; overlaps `eco`.

## Most reimplementable (top picks)

1. **palermo2024newts** (A, 9) — complete algorithm, open USGS code, analytical test cases; any DEM + water level.
2. **ravazzani2011macroscopic** (A, 9) — physically based MCA groundwater stencil fully documented in the FEST manual, Theis benchmark; trivial in WebGL.
3. **sharma2019understanding / kochanski2019rescal** (A 9 / B 8) — open GPL code with documented parameters, quantitative checks; but 3D and micro-scale, poor browser fit.
4. **ashton2001formation / ashton2006highangle** (B, 7, provisional) — CEM, open C code, two-parameter wave climate; very likely A after reading the JGR paper.
5. **pardoiguzquiza2017estimation + colladoslara2019distributed** (C, 5, provisional) — best match for HYD-06 with open European inputs; OA author versions exist, likely to rise after full-text read.
6. **sonnenschein2025hybrid** (C, 5, provisional) — the strongest modern ATM-01 template (OA, quantitative validation); code to be requested/searched.

## Gaps and unverified leads

- **No CA found** for cold-air drainage/pooling (ATM-02), lake or river ice, glacier flow, thermokarst, heat waves or fog. ATM-02 will have to be designed ourselves (flow routing of cold air on a DEM; KLAM_21 from DWD is a non-CA reference model — not verified as a publication).
- **Heavy gas (ATM-03):** only indirect leads — Salcido (1993) multi-speed lattice gas over complex terrain (WIT Press, no DOI found in Crossref); a Korean CA emergency-response system for chemical releases (J. Korean Inst. Gas, 2018, not verified); a frontal CA for toxic combustion clouds (*Fire*, 2025, MDPI, not verified in Crossref search).
- **Urban heat island (URB-01):** literature is dominated by CA–Markov land-use + LST regression (dozens of papers, e.g. Babol 2018, Ahmedabad 2022 — not catalogued, they belong to `lu`). A 3D thermal CA chapter (Leskovar, Univ. Maribor Press, 2026) was seen but not verified.
- **Unverified / not yet assessed leads:** Guariso, Maniezzo & Salomoni 1996 parallel cellular pollution model (DOI found: 10.1016/0096-3003(95)00214-6); Hamoudzadeh & Behzadi 2021 optimised CA for air pollution, Tehran (OpenAlex hit, DOI 10.36909/jer.13749); Troisi 2015 CA for multiple pollutants (IJMPC); Chen, Mynett & Minns 2002 CA macrophyte competition in Lake Veluwe (DOI 10.1016/S0304-3800(01)00428-8, overlaps `eco`); Lin et al. CA + genetic programming for cyanobacteria in Taihu Lake (EPiC, DOI 10.29007/dl2b); NOAA habitat-recovery CA after oil spills (Beegle-Krause et al. 2005, DOI 10.7901/2169-3358-2005-1-533); Rybak et al. 2019 CA snow redistribution for glacier mass balance (Russian, DOI 10.33075/2220-5861-2019-4-72-80); Hawick 2014 CA flood incursion and coastal erosion (DOI 10.2316/p.2014.821-005); RUSICA CA for beach sand erosion (Italy, CNR); Seghir, Marcou & El Yacoubi 2018 CA–Lattice Boltzmann coastline erosion; Milašinović et al. 2018 2D urban groundwater pollution CA (DOI 10.1007/978-3-319-99867-1_132); Wang et al. 2024 GPU dynamic-wave + solute CA (NHESS preprint 10.5194/nhess-2024-131); Gilbués (Brazil) desertification CA thesis; CATGRaSS (Landlab cellular-automaton vegetation driven by soil moisture/drought, overlaps `eco`); later CA cloud models (Silva 2019, Najafi 2021, Cheraghalizadeh 2024); mangrove CA studies in Iguape Bay (BR) and Iran; storm-surge CA coupled with GIS for Pearl River estuary (not found in Crossref).
- **Round 2 suggestions:** re-run OpenAlex once the daily budget resets (citation counts, OA links, abstracts); read full texts of Karafyllidis 1997, Guariso 1992, Ashton & Murray 2006, Pardo-Igúzquiza 2017 and Sonnenschein 2025 (likely score upgrades); look for CZ/EU snow-cover or air-quality CA (none found in round 1); search for "lattice Boltzmann" and "cellular" variants for cold-air and heavy-gas flows.
