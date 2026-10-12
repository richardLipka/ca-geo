# Atmosphere, climate, water bodies and other — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.

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

### Round 2

OpenAlex still quota-blocked; metadata via Crossref (≥ 2 s between requests), abstracts and OA
links via Semantic Scholar API and Europe PMC, full texts via publisher/author/repository PDFs
(extracted in the scratchpad, deleted right after). Digibug (Granada) was down (HTTP 504),
digital.csic.es and MDPI blocked automated access (bot check / HTTP 403); not bypassed.

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automata cold air drainage; cold air pooling DEM simulation; frost hollow terrain GIS; CA katabatic | Crossref | 1.5 M–6 M (noisy) | → `dobos2025terrainbased` (HU karst sinkhole); no CA paper |
| GIS model cold air drainage flow accumulation DEM frost hollow (KLAM / "cold air flow") | Web search | — | → SAGA "Cold Air Flow" tool (GPL code read), Chung & Yun AMS paper, KLAM_21 |
| Chung Yun cold air accumulation; Kim Yun closed catchment cold pool | Crossref | — | → `chung2006minimum`; Kim & Yun 2011 (KJAFM, lead) |
| GIS-based nocturnal cold air flow simulation relief analysis | Crossref | — | → `nowatschin2006gpubased` (full text via Univ. Siegen copy), `uiboupin2025how` |
| Sievers Kossmann KLAM_21 model formulation | Crossref + metsoc.org.nz PDF | 1 | → `sievers2016cold` (full text) |
| frost hollow / cold air pool Šumava, Czech basins; Dinaric frost hollows | Crossref + web | — | no peer-reviewed CZ modelling study; Ogrin et al. 2026 Dinaric frost hollows (observational, lead) |
| TWODEE-2 dense gas complex topography; Lake Nyos TWODEE-2.1 | Crossref | — | → `folch2009twodee2`, `folch2017highresolution` (full text); VIGIL wrapper (GPL) on GitHub |
| CA toxic gas dispersion emergency; CA heavy/dense gas leakage | Crossref | 2 M | Sarkar & Abbasi 2006, Cao et al. 2016 (metadata only → leads) |
| SnowSlide gravitational snow transport; SnowTran-3D; LB snow drift fence; CA snow drift | Crossref + web | — | → `bernhardt2010snowslide` (full text, usask copy), `masselot1998lattice`, `chopard1999cellular` |
| Collados-Lara / Pardo-Igúzquiza CA snow (all) | Crossref | 6 relevant | → `hidalgohidalgo2025coupled` (OA full text); 2021 STOTEN + 2017 chapter as leads |
| Ashton Murray 2006 PDF | Web search + Wayback | — | UF Water Institute copy (404 live, read via web.archive.org) → full text |
| Sonnenschein hybrid CA code | Web + GitHub API | 1 | → CellAutDisp repository (GPL-3.0, PyPI) |
| Karafyllidis 1997 full text | Web search | — | none; secondary description in `zhang2025method` full text |
| Zhang & Li 2025 MethodsX | Europe PMC (PMC12273250) | 1 | full text read |
| reservoir shore abrasion Czech; Nechranice/Vranov; Kachugin | Crossref + web | — | → `slezingr2013verification` (CZ, full text); Wierzbicki et al. 2025 (PL, lead); no CA |
| lake shoreline erosion CA | Crossref | 0 relevant | nothing beyond NEWTS / CEM |
| post-mining pit lake filling (Medard, Most, Lusatia) | Crossref | — | only monitoring (Valvoda et al. 2012, Medard) — no CA / grid filling model |
| CA groundwater flow; CA contaminant transport aquifer; 3D unsaturated CA | Crossref | — | → `mendicino2006threedimensional`, `furnari2021asynchronous` (OpenCAL) |
| CA oil spill river / lake; CA pollutant spill river | Crossref + web | — | no river/lake oil-spill CA found; Cell-DEVS coastal spill (Carleton 2018, lead) |
| CA heat transfer urban surface temperature | Crossref | — | → `leskovar2026modeling` (now verified; abstract) |
| CA cyanobacteria / algal bloom reservoir; CA eutrophication lake | Crossref | — | → `ling2018modelling` (full text, EasyChair); Alfa et al. 2025 Heron Lake CA water quality (lead) |
| CA lake ice; CA river ice jam | Crossref | 0 relevant | still nothing |
| CA air pollution Czech Republic / Poland; cold air simulation Czech | Crossref | 0 relevant | no CZ CA study in this domain |

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
8. **(Round 2) Cold-air drainage and dense-gas flows on DEM grids.** Not called "CA" in the
   literature, but all are explicit local grid updates of a layer thickness moved downslope by
   gravity — directly CA-like: SAGA Cold Air Flow (`conrad2020coldairflow`, GPL code),
   GPU height-field model with land-use production/resistance tables (`nowatschin2006gpubased`),
   the DWD single-layer model KLAM_21 (`sievers2016cold`, applied near the CZ border in
   `uiboupin2025how`), static D8 cold-air accumulation (`chung2006minimum`), and the
   shallow-layer dense-gas model TWODEE-2 (`folch2009twodee2`, `folch2017highresolution`).
   Gravitational snow redistribution on a DEM (`bernhardt2010snowslide`) uses the same
   "excess above a holding capacity flows to lower neighbours" scheme.

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| palermo2024newts | 2024 | NEWTS1.0 coastal erosion by waves | lake/sea coast erosion | square / 4- or 8-connected shoreline, ray-cast fetch / land–lake + strength / det. | 2 1 2 2 2 | 9 | A | USGS code release | OA | full text |
| ravazzani2011macroscopic | 2011 | MCA for groundwater | unconfined aquifer flow | square / von Neumann / hydraulic head / det. | 2 1 2 2 2 | 9 | A | FEST repo (chiselapp) | paywall | abstract + model manual |
| sharma2019understanding | 2019 | Snow bedforms with sintering | snow dunes / wind drift | 3D cubic / nearest-neighbour doublets / air, mobile, deposited snow (+age) / stoch. (Poisson) | 1 2 2 2 2 | 9 | A | rescal-snow (GPL) | OA | full text |
| kochanski2019rescal | 2019 | Rescal-snow software | snow dunes | as above (ReSCAL LGCA) | 1 2 2 2 1 | 8 | B | GitHub | OA | full text + repo docs |
| ashton2001formation | 2001 | Coastline features from high-angle waves | sandy coastline shape | 2D cells with fractional sand fill / along-shore neighbours / stoch. wave angle | 1 1 2 2 1 | 7 | B | cem-old (C) | paywall | abstract (provisional); model spec now via ashton2006highangle |
| ashton2006highangle | 2006 | High-angle wave instability 1 | spits, capes, sand waves | 2D cells with fractional land fill F / boundary fluxes between shoreline neighbours + shadow search / stoch. wave angle | 2 2 2 2 2 | 10 | A | cem-old (C) | free copy (UF, via Wayback) | full text (r2) |
| milasinovic2019coupled | 2019 | CA groundwater flow + pollution | contaminant transport | square / neighbours / head + concentration / det. | 1 1 0 2 2 | 6 | C | not found | preprint (repository, blocked) | abstract (provisional) |
| wang2023novel | 2023 | STMCA solute transport in floods | solute (E. coli) in floods | square / neighbours / depth, velocity, concentration / det. | 1 1 0 2 2 | 6 | C | not found | OA | abstract (provisional) |
| korsnes2004scaling | 2004 | Fracture and refreezing of sea ice | sea-ice floe sizes | lattice / neighbours / ice–crack / stoch. | 1 1 0 2 2 | 6 | C | not found | OA (arXiv) | abstract (provisional) |
| pardoiguzquiza2017estimation | 2017 | Snow covered area by CA | daily snow cover | DEM cells / neighbourhood / snow–no snow / calibrated rules | 1 1 0 2 1 | 5 | C | not found | OA (repository) | abstract (provisional) |
| colladoslara2019distributed | 2019 | Distributed CA, climate change on snow | snow cover under scenarios | as above, distributed by elevation band | 1 1 0 2 1 | 5 | C | not found | OA (repository) | abstract (provisional) |
| sonnenschein2025hybrid | 2025 | Hybrid CA air pollution for traffic | NO2 off-road dispersion | 50 m raster / wind-weighted moving window (n×n) / concentration / det., GA-calibrated | 2 1 2 1 2 | 8 | B | CellAutDisp (GPL-3.0, Python) | OA | abstract + code repository (r2) |
| liu2022simulating | 2022 | Offshore oil spills by CA | oil slick drift & spreading | square / Moore / oil state / det. | 1 1 0 2 1 | 5 | C | not found | OA | abstract (provisional) |
| zhang2025method | 2025 | Logistic regression + CA oil spill | oil slick extent | 6 m raster / Moore 3×3–7×7 / oil–no oil / stoch. | 2 1 0 1 2 | 6 | C | not found | OA | full text (r2, Europe PMC) |
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
| sievers2016cold (r2) | 2016 | KLAM_21 cold air drainage model | cold-air drainage, ponding, urban ventilation | Arakawa-C grid 10–500 m / 4-neighbour fluxes, upstream donor cell / heat deficit E, layer depth H, u, v / det. | 1 2 1 2 2 | 8 | B | binary from DWD (closed) | free PDF | full text (r2) |
| nowatschin2006gpubased (r2) | 2006 | GPU cold air flow simulation | cold-air drainage with land use | staggered square grid / von Neumann / cold-air height k / det. explicit | 2 2 0 2 1 | 7 | B | not found | free copy (Univ. Siegen) | full text (r2) |
| conrad2020coldairflow (r2) | 2020 | SAGA Cold Air Flow tool (grey lit.) | cold-air drainage | DEM grid / 8 neighbours, multiple-flow to lower surface / cold-air height / det., CFL step | 2 1 2 2 0 | 7 | B | SAGA GIS (GPL, C++) | OA docs + code | code + documentation (r2) |
| bernhardt2010snowslide (r2) | 2010 | SnowSlide gravitational snow transport | snow redistribution on steep terrain | DEM grid / 8 lower neighbours, processed highest→lowest / snow depth vs holding depth / det. | 2 1 1 2 1 | 7 | B | Fortran on request; CHM reimplementation (GPL) | free copy (usask) | full text (r2) |
| folch2009twodee2 (r2) | 2009 | TWODEE-2 dense gas on complex topography | heavy-gas cloud over terrain | regular grid FD / shallow-layer depth-averaged / h, density, u / det. | 1 1 1 2 1 | 6 | C | Fortran, not public (VIGIL wrapper GPL) | paywall | abstract + 2017 full text (r2) |
| folch2017highresolution (r2) | 2017 | TWODEE-2.1, Lake Nyos CO2 | limnic CO2 cloud over valleys | as above + 4D wind input | 1 1 1 1 2 | 6 | C | as above | OA | full text (r2) |
| chung2006minimum (r2) | 2006 | Cold-air accumulation potential, Tmin | frost-prone spots (static) | 10 m DEM / D8 flow accumulation + 5-cell focal mean / static | 1 1 0 2 2 | 6 | C | not found | paywall | abstract-level + conference version (r2) |
| slezingr2013verification (r2) | 2013 | Erosion terminant for reservoir banks (CZ) | reservoir shore abrasion | not CA: cross-section equation (abrasion stop level) | 1 1 0 1 2 | 5 | C | — | OA | full text (r2) |
| hidalgohidalgo2025coupled (r2) | 2025 | Coupled CA – Snowmelt Runoff Model | snow cover + streamflow | 5 km climate grid on DEM cells / predefined neighbour configuration / snow–no snow / calibrated rules | 1 1 0 2 2 | 6 | C | not found | OA | full text (r2) |
| masselot1998lattice (r2) | 1998 | LB model for particle transport and deposition | snow/sand drift, deposition behind fences | 2D lattice Boltzmann + CA particles | 1 0 0 2 1 | 4 | C | not found | paywall | abstract (provisional) |
| chopard1999cellular (r2) | 1999 | CA + LB for snow transport | snow erosion, transport, deposition | as above | 1 0 0 2 1 | 4 | C | not found | paywall | abstract (provisional) |
| mendicino2006threedimensional (r2) | 2006 | 3D unsaturated flow by macroscopic CA | vadose-zone flow (Richards) | 3D cubic / face neighbours / pressure head / det. explicit | 1 1 0 2 1 | 5 | C | not found | paywall | abstract (provisional) |
| furnari2021asynchronous (r2) | 2021 | Asynchronous CA subsurface flow | 2D/3D subsurface flow | as above + activation threshold on head difference / async. | 1 1 1 2 1 | 6 | C | OpenCAL library (LGPL-3.0; model code not confirmed) | paywall | abstract (provisional) |
| ling2018modelling (r2) | 2018 | CA + GP cyanobacteria, Lake Taihu | cyanobacteria abundance | monitoring-site polygons / Moore-like, wind-selected neighbours / biomass / GP rule | 1 1 0 1 2 | 5 | C | not found | OA | full text (r2) |
| dobos2025terrainbased (r2) | 2025 | Cold-air pool frost risk, karst sinkhole (HU) | cold-air pooling | uses SAGA Cold Air Flow + terrain indices on UAV DSM | 0 1 1 2 1 | 5 | C | third-party tools (SAGA) | OA | abstract (provisional) |
| uiboupin2025how (r2) | 2025 | KLAM_21 urban trees, Plauen (DE) | nocturnal ventilation of a valley town | KLAM_21 at 7/35 m | 0 1 1 2 1 | 5 | C | KLAM_21 (closed) | OA | full text, partial (r2) |
| leskovar2026modeling (r2) | 2026 | 3D CA urban heat transfer | city-block temperature | 3D cells, 5 material classes / 8 sequential physics layers | 1 0 0 1 1 | 3 | D | not found | OA (book chapter) | abstract (provisional) |

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
- **Reimplementability:** S1 2 – full algorithm incl. update order and boundaries; S2 1 – some constants unspecified; S3 2; S4 2 – runs on any DEM + water level; S5 2 – analytical benchmarks → 9, A. Assessed from: full text. Round 2: confirmed, unchanged; for Czech reservoirs the CZ erosion-terminant method (`slezingr2013verification`) can supply a per-cell stop level (erosion ceases below the computed terminant), and CEM (`ashton2006highangle`) is the sandy-shore counterpart.
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
- **Reimplementability:** S1 2 – complete local rule in manual; S2 1 – stability/Δt choice not given; S3 2; S4 2 – Theis test is generic; S5 2 – analytical benchmark → 9, A. Assessed from: abstract + model documentation (paper full text not read). Round 2: paper still not accessible (Elsevier); score unchanged. Related verified CA groundwater work added: `mendicino2006threedimensional`, `furnari2021asynchronous` (unsaturated/3D); no CA or grid model of post-mining lake filling found (LND-03 will need ravazzani-type heads + a lake-level bucket of our own design).
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
- **Reimplementability:** S1 1; S2 1 (abstract caps); S3 2; S4 2 – synthetic coast + 2 wave parameters; S5 1 → 7, B. Assessed from: abstract (provisional). Round 2: Nature full text still not accessible; score kept — cite `ashton2006highangle` (A 10) as the model specification.
- **Browser fit:** Very good (1D-ish shoreline on a 2D grid, cheap per step, visually striking).
- **Relevance to ca-geo:** new "coastline" item; not CZ but a classic, well-documented CA-like geomorphic model. Overlaps `geo`.

### ashton2006highangle — High-angle wave instability and emergent shoreline shapes: 1. Modeling of sand waves, flying spits, and capes
- **Citation:** Ashton, A. D., Murray, A. B. (2006). High-angle wave instability and emergent shoreline shapes: 1. Modeling of sand waves, flying spits, and capes. *Journal of Geophysical Research: Earth Surface* 111(F4). DOI: 10.1029/2005JF000422 (verified: Crossref)
- **Access:** AGU site blocked automated access; free copy formerly hosted by the UF Water Institute (live link now 404) read via web.archive.org.
- **Phenomenon and study area:** Same model as above, full description and parameter exploration; idealised coasts.
- **Model:** Plan-view grid of square cells of width ΔW (100 m); each cell holds the fraction F of its area that is land (F = 1 land, 0 sea, 0 < F < 1 shoreline). Shoreline position and local orientation are interpreted from F and the land cells behind/beside each shoreline cell (special cases for spits). Each step: draw a deepwater wave angle from a 4-bin PDF set by U (fraction of high-angle waves) and A (asymmetry); refract/shoal over shore-parallel contours to breaking; compute alongshore flux across each cell boundary with the CERC formula Qs = K1·Hb^(5/2)·cos(φb−θ)·sin(φb−θ) using a blend of upwind/central boundary angles, with the flux maximum enforced at high-to-low-angle transitions; a linear search toward the wave source marks shadowed cells (no transport into/out of shadow from wave forcing). F changes by (Qin − Qout)·Δt / ((Dsf + B)·ΔW²); shoreface depth Dsf from intersection of a shoreface slope (0.01) and shelf slope (0.001), eroding down to Dmin = 10 m; a schematised barrier overwash keeps a minimum barrier width (analytical solution in Appendix A). Periodic lateral boundaries; initial straight coast with white-noise perturbation.
- **Inputs:** Wave climate (H0, T, U, A); initial shoreline; no DEM required (a bathymetry/coast raster could be used for a lake/reservoir variant).
- **Parameters:** K1, slopes, Dmin, ΔW, berm height and wave parameters stated; time step only bounded by stability.
- **Code:** as above (cem-old, C).
- **Validation:** Linear-stability prediction (instability for deepwater angles beyond the flux maximum, roughly 45°) checked by simulations; regime diagram of shapes (cuspate bumps, sand waves, reconnecting/flying spits) as a function of U and A; power-law growth of feature wavelength and aspect ratio; insensitivity to grid size, time step and initial noise reported. Part 2 (DOI 10.1029/2005JF000423) compares wave-climate metrics with real coasts (e.g. Long Point, Lake Erie).
- **Reimplementability:** S1 2 – complete cell interpretation, flux, shadowing, update and boundary rules; S2 2 – all constants given; S3 2; S4 2 – synthetic coast + 2 wave-climate parameters; S5 2 – stability threshold, regime diagram and wavelength scaling are quantitative checks → 10, A. Round 2: re-assessed from full text — S1 2 S2 2 S3 2 S4 2 S5 2 = 10 A (was 7 B).
- **Browser fit:** as above — excellent; shadow search is O(n) per cell but grids are small.
- **Relevance to ca-geo:** primary spec document for a CEM port; HYD-08 variant for large reservoirs or post-mining lakes (with a smaller cell size, as the authors suggest for lacustrine settings).

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
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2 – DEM + ERA5/E-OBS + MODIS snow are open, S5 1 → 5, C. Assessed from: abstract (provisional). Round 2: author copy (Digibug) down (HTTP 504), CSIC copy behind a bot check — full text not read. The OA follow-up `hidalgohidalgo2025coupled` confirms the rule inputs (cell elevation, daily P and T indices, own previous state, previous states of a predefined neighbour configuration; binary state) but refers back for the exact rules; score unchanged.
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
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → 5, C. Assessed from: abstract (provisional). Round 2: full text not reachable (same repositories as above); score unchanged. The CA has since been reused at 5 km resolution with SCA skill R² 0.77, NSE 0.72 (`hidalgohidalgo2025coupled`).
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** HYD-06 climate-scenario slider ("+2 °C").

### sonnenschein2025hybrid — Hybrid cellular automata-based air pollution model for traffic scenario microsimulations
- **Citation:** Sonnenschein, T. S., Yuan, Z., Khan, J., Kerckhoffs, J., Vermeulen, R. C. H., Scheider, S. (2025). Hybrid cellular automata-based air pollution model for traffic scenario microsimulations. *Environmental Modelling & Software* 186, 106356. DOI: 10.1016/j.envsoft.2025.106356 (verified: Crossref)
- **Access:** OA (ScienceDirect blocked automated reading)
- **Phenomenon and study area:** NO2 from traffic, Amsterdam (NL, EU).
- **Model:** Land-use-regression baseline + on-road emissions; the CA step (from the authors' code) is an iterated focal weighted average over an n×n window whose weights depend on distance and on alignment with the wind direction (windward weights multiplied, leeward divided by a wind-speed-dependent disparity factor; optional temperature/rain terms; 9 meteorological parameters), with on-road cells reset to the emission values each iteration, an optional morphology-based adjuster (building/green features) and scaling coefficients for baseline and traffic parts. Number of iterations per hour is a parameter.
- **Inputs:** 50 m raster, traffic emissions (from an agent-based traffic model), LUR baseline, hourly meteorology, morphology layers.
- **Parameters:** Calibrated by genetic algorithm (calibration module in the code); fitted values not seen (paper full text blocked).
- **Code:** https://github.com/TabeaSonnenschein/CellAutDisp (GPL-3.0, Python; HTTP 200; also on PyPI as `CellAutDisp`, HTTP 200), with example scripts for data preparation, calibration and prediction.
- **Validation:** External R² 0.60 vs mobile and fixed NO2 monitoring; lockdown scenario R² 0.57; 0.48 s runtime.
- **Reimplementability:** S1 2 – rule fully determined by the open code and README; S2 1 – GA procedure reproducible but fitted values unseen; S3 2; S4 1 – emission and LUR inputs are case-specific; S5 2 → 8, B. Round 2: re-assessed from abstract + code repository — S1 2 S2 1 S3 2 S4 1 S5 2 = 8 B (was 5 C); paper full text still blocked (ScienceDirect, Elsevier API).
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
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → 5, C. Assessed from: abstract (provisional). Round 2: journal PDF (jmstt.ntou.edu.tw) still refuses automated access (HTTP 403); unchanged.
- **Browser fit:** Good.
- **Relevance to ca-geo:** template for a river/lake spill variant (Labe/Vltava accident scenario).

### zhang2025method — A method to modelling oil spill using combination of logistic regression and cellular automata
- **Citation:** Zhang, Y., Li, S. (2025). A method to modelling oil spill using combination of logistic regression and cellular automata. *MethodsX* 15, 103474. DOI: 10.1016/j.mex.2025.103474 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** Oil slick extent, DeepSpill experiment data.
- **Model:** Stochastic binary CA (oil / non-oil): P_g = logistic function of a linear combination of five drivers (distance to source, currents, wind, salinity, temperature); neighbourhood term Ω = share of oil cells in the window; stochastic term RA = 1 + (−ln r)^a; change probability P_d = P_g·Ω·RA; a non-oil cell becomes oil if P_d exceeds a threshold; iterate until simulated oil area equals the verification image. Step-by-step GIS (ArcGIS + SPSS) workflow given.
- **Inputs:** Rasters of drivers (DeepSpill experiment), initial and verification slick images, resampled (6 m optimal).
- **Parameters:** LR coefficients tabulated for all sampling ratios and oil proportions; threshold and dispersion exponent a not clearly stated.
- **Code:** not found ("can be done in C# or Python").
- **Validation:** Accuracy 96.3–97.4 % across sampling ratios, scales and neighbourhoods (best 7×7 Moore at 6 m).
- **Reimplementability:** S1 2 – complete rule and stopping criterion; S2 1 – threshold/a missing; S3 0; S4 1 – DeepSpill rasters not open; S5 2 → 6, C. Round 2: re-assessed from full text (Europe PMC PMC12273250) — S1 2 S2 1 S3 0 S4 1 S5 2 = 6 C (was 5 C). Note: accuracy is inflated by the many unchanged cells; the rule is a land-use-style suitability CA, not a physical spreading model.
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
- **Reimplementability:** S1 0, S2 1, S3 1, S4 1, S5 1 → 4, C. Assessed from: abstract (provisional). Round 2: MDPI blocks automated download (HTTP 403); unchanged. Still the only CZ-near UHI item; genuine thermal CA for URB-01 remains limited to `wagner2015cellular` and `leskovar2026modeling` (both weak).
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
- **Model:** Classic CA oil-spill model by the author of a well-known CA fire model; rules not seen. Per the literature review in `zhang2025method` (full text) it includes wind, sea currents, boundary effects and evaporation and was checked against experimental data.
- **Code:** not found.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: metadata + secondary description. Round 2: no full text found (no repository copy); score unchanged.
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
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: abstract (provisional). Round 2: no full text; the same group's later CA + genetic-programming model is OA (`ling2018modelling`, C 5) and is the better template.
- **Browser fit:** CA part cheap; drivers would need simplification.
- **Relevance to ca-geo:** cyanobacteria bloom in Czech reservoirs/fishponds (new idea) — water-body CA family; overlaps `eco`.

### sievers2016cold — The cold air drainage model KLAM_21 – Model formulation and comparison with observations (round 2)
- **Citation:** Sievers, U., Kossmann, M. (2016). The cold air drainage model KLAM_21 – Model formulation and comparison with observations. *Weather and Climate* 36, 2–24. DOI: 10.2307/26779385 (verified: Crossref; author initials from the PDF)
- **Access:** free PDF on the Meteorological Society of New Zealand site (https://www.metsoc.org.nz/resources/Documents/weather_and_climate/2-24_sievers-and-kossmann_2016.pdf, read)
- **Phenomenon and study area:** Nocturnal cold-air production, drainage and ponding in hilly terrain; evaluation at two German sites and Christchurch (NZ).
- **Model:** Single-layer (2D) model. Prognostic total heat deficit E of the cold layer, changed by a constant local heat-loss rate P = a·Pmax (a per land-use class, Pmax = 30 W/m²) and horizontal advection; layer depth H diagnosed from E via a prescribed temperature-deficit profile; vertically averaged momentum equation with gravity (slope of the cold-layer top), friction (roughness, buildings, trees via volume friction) and optional ambient wind. Arakawa-C grid, centred gradients, upstream donor-cell advection, dynamic time step; optional passive tracer.
- **Inputs:** DEM and land use (~20 predefined classes, editable); optional buildings and regional wind.
- **Parameters:** Table of class parameters (z0, building/tree fractions and heights, LAI, heat-loss fraction a).
- **Code:** Binaries with GUI distributed by DWD; not open source (S3 1).
- **Validation:** Cold-layer depth, near-surface wind speed/direction and drainage patterns compared with observations (profiles and time series).
- **Reimplementability:** S1 1 – core equations and numerics given, some closures only referenced to the German manual; S2 2; S3 1; S4 2 – DEM + CORINE/Urban Atlas style land cover; S5 2 → 8, B. Assessed from: full text (r2)
- **Browser fit:** Good (2D explicit, donor-cell; 10–500 m grids typical).
- **Relevance to ca-geo:** **ATM-02** physically based reference; a simplified KLAM-like layer model is the natural "advanced" mode after a SAGA/Nowatschin-style CA.

### nowatschin2006gpubased — GPU-based simulation of cold air flow for environmental planning (round 2)
- **Citation:** Nowatschin, S., Bertram, M., Garth, C. (2006). GPU-based simulation of cold air flow for environmental planning. *Proceedings of the 22nd Spring Conference on Computer Graphics (SCCG '06)*, 191–198. ACM. DOI: 10.1145/2602161.2602184 (verified: Crossref)
- **Access:** free copy on the Univ. Siegen VMV 2010 site (linked from the RPTU Kaiserslautern repository record), read
- **Phenomenon and study area:** Cold-air drainage around the town of Manubach (Geisbachtal, DE), land-use planning scenarios.
- **Model:** Square grid, cold-air height k per cell; staggered velocities between 4-neighbours v = (h_i + k_i − h_j − k_j)/w (no inertia; w = flow resistance of the land use); outflow v·k from the donor cell, limited so that outgoing velocities per cell sum to ≤ 1; new k = k + p (production) + net in/outflow; mass-conserving, no divergence projection needed; open domain boundaries. Implemented as fragment shaders (two passes per step + render pass).
- **Inputs:** DEM, land-use map (meadow, field, vineyard, forest, settlement).
- **Parameters:** Tables of cold-air production per land use (e.g. 12 m³/(m²·h) for fields, 1 for forest, 0 for settlements) and resistance (%); the resistance table contains an apparent typo (two "settlement" rows).
- **Code:** not found.
- **Validation:** Qualitative hourly maps (pooling in valleys, retention by settlement and forest).
- **Reimplementability:** S1 2 – complete explicit update and boundary rule; S2 2 – tables; S3 0; S4 2 – DEM + land cover; S5 1 → 7, B. Assessed from: full text (r2)
- **Browser fit:** Excellent — a GPU fragment-shader CA, maps 1:1 onto WebGL.
- **Relevance to ca-geo:** **ATM-02** — best ready-made CA rule found for cold-air pooling; land-use-dependent production fits CORINE/ZABAGED.

### conrad2020coldairflow — Cold Air Flow, SAGA GIS tool (round 2, grey literature)
- **Citation:** Conrad, O., Dietrich, H. (2020). Cold Air Flow (SAGA tool library sim_air_flow, tool 0). SAGA GIS. Grey literature, no DOI. Documentation: https://saga-gis.sourceforge.io/saga_tool_doc/9.13.0/sim_air_flow_0.html (HTTP 200); source: https://github.com/saga-gis/saga-gis, file `saga-gis/src/tools/simulation/sim_air_flow/cold_air_flow.cpp` (HTTP 200, GPL).
- **Access:** OA (documentation + source code read)
- **Phenomenon and study area:** Generic nocturnal cold-air drainage; cites Schwab (2000) and Bendix (2005) relief-analytic methods.
- **Model:** Grid of cold-air height on top of the DEM. Per cell: if air > 0, velocity v = sqrt(g·ΔT/T · h/friction · sin(slope of the air surface)) (ΔT from ambient vs cold-air temperature); the moved volume h·v·Δt/Δx (capped at h) is split among the 8 neighbours with lower air surface in proportion to the drop; production added each step; Δt = delay × cellsize / v_max (CFL-like); open or closed edges.
- **Inputs:** DEM; optional production [m/h] and friction grids.
- **Parameters:** Defaults (production 1, friction 1, 6 h, T_air 15 °C, T_cold 5 °C, delay 0.5) — not calibrated.
- **Code:** as above (C++, GPL).
- **Validation:** none reported; used in `dobos2025terrainbased` alongside measurements.
- **Reimplementability:** S1 2 – rule fully defined by short open source; S2 1 – defaults only; S3 2; S4 2; S5 0 → 7, B. Assessed from: code + documentation (r2)
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** **ATM-02** — open reference implementation to test our port against.

### chung2006minimum — Minimum temperature mapping over complex terrain by estimating cold air accumulation potential (round 2)
- **Citation:** Chung, U., Seo, H. H., Hwang, K. H., Hwang, B. S., Choi, J., Lee, J. T., Yun, J. I. (2006). Minimum temperature mapping over complex terrain by estimating cold air accumulation potential. *Agricultural and Forest Meteorology* 137(1–2), 15–24. DOI: 10.1016/j.agrformet.2005.12.011 (verified: Crossref)
- **Access:** paywall; method read in the authors' AMS conference paper (https://ams.confex.com/ams/pdfpapers/79839.pdf, grey literature).
- **Phenomenon and study area:** Frost-prone spots, 2.1 × 2.1 km slope of Mt. Jiri (KR); 14 temperature loggers + tethered balloon profiles.
- **Model:** Static (not dynamic): D8 flow direction and flow accumulation (count of inflowing cells) on a 10 m DEM, smoothed by a 5-cell-radius focal mean; temperature correction = (R/Rmax)·f(log10 FA5) for cold-air accumulation plus an exponential thermal-belt term above the inversion base, added to lapse-rate IDW interpolation.
- **Inputs:** DEM, station minimum temperatures, daily temperature range.
- **Parameters:** Regression coefficients fitted on 8 loggers (r² 0.78 at 5-cell radius).
- **Code:** not found.
- **Validation:** 6 independent loggers; captures sub-zero minima missed by lapse-rate interpolation.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 2 → 6, C. Assessed from: abstract-level + conference version (r2; journal full text not read)
- **Browser fit:** Excellent (one flow-accumulation pass).
- **Relevance to ca-geo:** ATM-02 "static baseline" layer to compare with the dynamic CA; validation idea with ČHMÚ / amateur frost-hollow stations (e.g. Šumava bogs).

### dobos2025terrainbased — Terrain-Based High-Resolution Microclimate Modeling for Cold-Air-Pool-Induced Frost Risk Assessment in Karst Depressions (round 2)
- **Citation:** Dobos, A., Farkas, R., Dobos, E. (2025). Terrain-Based High-Resolution Microclimate Modeling for Cold-Air-Pool-Induced Frost Risk Assessment in Karst Depressions. *Climate* 13(10), 205. DOI: 10.3390/cli13100205 (verified: Crossref)
- **Access:** OA (MDPI blocked automated reading)
- **Phenomenon and study area:** Cold-air pool in the Mohos sinkhole, Bükk Plateau (Hungary, Central Europe), the Hungarian cold pole.
- **Model:** Combination of SAGA terrain tools (Sky-View Factor, Wind Exposition, Cold Air Flow, Diurnal Anisotropic Heat) on a UAV-derived DSM; not a new model.
- **Inputs:** UAV DSM, multi-level temperature loggers, thermal imagery.
- **Code:** third-party (SAGA) only → S3 1.
- **Validation:** Against logger profiles and thermal images (metrics not seen); companion observational paper in *Időjárás* 129(3), 2025 (DOI 10.28974/idojaras.2025.3.3, verified in Crossref).
- **Reimplementability:** S1 0, S2 1, S3 1, S4 2, S5 1 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** n/a (workflow).
- **Relevance to ca-geo:** ATM-02 Central-European validation case; shows SAGA Cold Air Flow is used in practice.

### uiboupin2025how — How strong do urban trees affect the nocturnal ventilation potential? … Plauen (Germany) using the cold air drainage model KLAM_21 (round 2)
- **Citation:** Uiboupin, K., Goldberg, V. (2025). How strong do urban trees affect the nocturnal ventilation potential? – a simulation study for the city of Plauen (Germany) using the cold air drainage model KLAM_21. *Meteorologische Zeitschrift* (online first). DOI: 10.1127/metz/1274 (verified: Crossref)
- **Access:** OA (Schweizerbart PDF, partially read)
- **Phenomenon and study area:** Nocturnal cold-air ventilation of Plauen (Saxony, close to the CZ border, Weiße Elster valley) under a tree-planting scenario.
- **Model:** KLAM_21 at 7 m (core) / 35 m; land-use classes adapted (urban trees, potential trees, semi-sealed); output density of cold-air volume flow.
- **Inputs:** Open state DEM, DLM land use, buildings (Saxony/Thuringia geodata).
- **Code:** KLAM_21 (closed) → S3 1.
- **Validation:** none new; cites earlier KLAM_21 evaluations.
- **Reimplementability:** S1 0, S2 1, S3 1, S4 2, S5 1 → 5, C. Assessed from: full text, partial (r2)
- **Browser fit:** n/a.
- **Relevance to ca-geo:** ATM-02 urban-planning variant just across the border; scenario idea "plant trees vs keep the cold-air corridor open".

### folch2009twodee2 — TWODEE-2: A shallow layer model for dense gas dispersion on complex topography (round 2)
- **Citation:** Folch, A., Costa, A., Hankin, R. K. S. (2009). twodee-2: A shallow layer model for dense gas dispersion on complex topography. *Computers & Geosciences* 35(3), 667–674. DOI: 10.1016/j.cageo.2007.12.017 (verified: Crossref)
- **Access:** paywall; equations restated in the OA `folch2017highresolution`.
- **Phenomenon and study area:** Dense-gas (CO2) clouds flowing over topography (volcanic/limnic degassing).
- **Model:** Depth-averaged shallow-layer equations for cloud depth h, density and velocity with entrainment of ambient air, terrain-slope gravity term, surface drag and turbulent shear (closures from Hankin & Britter 1999), finite differences on a regular grid; vertical concentration profile reconstructed from an exponential law.
- **Inputs:** DEM, roughness, wind field (diagnostic wind model), source term.
- **Code:** Fortran 90; not publicly downloadable (the GPL Python workflow tool VIGIL, https://github.com/BritishGeologicalSurvey/VIGIL, HTTP 200, drives it but does not contain it) → S3 1.
- **Validation:** Earlier TWODEE validated on the Thorney Island trials (Hankin & Britter 1999).
- **Reimplementability:** S1 1, S2 1, S3 1, S4 2, S5 1 → 6, C. Assessed from: abstract + 2017 full text (r2)
- **Browser fit:** Medium (shallow-water solver; a simplified CA analogue — layer redistribution plus dilution — is feasible).
- **Relevance to ca-geo:** **ATM-03** physical reference model; a CA version can borrow the SAGA/Nowatschin layer-flow rule plus an entrainment (dilution) term.

### folch2017highresolution — High-resolution modelling of atmospheric dispersion of dense gas using TWODEE-2.1: application to the 1986 Lake Nyos limnic eruption (round 2)
- **Citation:** Folch, A., Barcons, J., Kozono, T., Costa, A. (2017). High-resolution modelling of atmospheric dispersion of dense gas using TWODEE-2.1: application to the 1986 Lake Nyos limnic eruption. *Natural Hazards and Earth System Sciences* 17(6), 861–879. DOI: 10.5194/nhess-17-861-2017 (verified: Crossref)
- **Access:** OA (full text read)
- **Phenomenon and study area:** CO2 cloud from the Lake Nyos eruption (Cameroon) draining into valleys.
- **Model:** TWODEE-2.1 (as above) driven by WRF winds downscaled to 50 m with CFD transfer functions; time-dependent source; fatality-probability criterion from concentration and exposure time.
- **Inputs:** DEM, roughness, 4D wind, source scenarios (62 tested).
- **Code:** see above (not public).
- **Validation:** Point-by-point comparison of predicted fatality probability with reported fatality percentages at 53 locations (binned χ² and MAE; best run MAE 34.7 %, 0.86 Tg CO2 in 3 h).
- **Reimplementability:** S1 1 – closures referenced; S2 1; S3 1; S4 1 – heavy wind chain; S5 2 → 6, C. Assessed from: full text (r2)
- **Browser fit:** Only as a simplified analogue.
- **Relevance to ca-geo:** ATM-03 benchmark story (dense gas pooling in depressions); CZ analogue: natural CO2 degassing (see new phenomena).

### bernhardt2010snowslide — SnowSlide: A simple routine for calculating gravitational snow transport (round 2)
- **Citation:** Bernhardt, M., Schulz, K. (2010). SnowSlide: A simple routine for calculating gravitational snow transport. *Geophysical Research Letters* 37(11). DOI: 10.1029/2010GL043086 (verified: Crossref)
- **Access:** paywall; copy hosted by Univ. Saskatchewan (CRHM papers), read.
- **Phenomenon and study area:** Removal of snow from steep faces and accumulation at their base; Watzmann massif, Berchtesgaden (DE, Alps), 30 m DEM.
- **Model:** Cells processed from the highest to the lowest (on the snow surface = DEM + snow depth). If slope > Sm (25°) and snow depth > holding depth Shd(slope) (exponential decrease with slope, minimum 5 cm SWE from 75°, or a vegetation-based holding depth if larger), the excess is passed to all lower neighbours in proportion to their elevation drop; mass-conserving; runs at each time step of the host snow model.
- **Inputs:** DEM, snow depth/SWE from a host model (SnowModel), land cover.
- **Parameters:** Sm and minimum Shd given; the exponential Shd curve only as a figure (the open CHM reimplementation lists holding depths from 3.08 m at 30° to 0.15 m at 75°).
- **Code:** Fortran "available from the authors" (S3 1); third-party reimplementation in the Canadian Hydrological Model, https://github.com/Chrismarsh/CHM (GPL-3.0, HTTP 200; docs https://chm.readthedocs.io, HTTP 200).
- **Validation:** Synthetic slopes/walls (qualitative); visual comparison with a Landsat snow map and aerial imagery.
- **Reimplementability:** S1 2, S2 1, S3 1, S4 2, S5 1 → 7, B. Assessed from: full text (r2)
- **Browser fit:** Excellent (one sorted sweep per step).
- **Relevance to ca-geo:** ATM-05 / HYD-06 / HAZ-03 bridge — gravitational redistribution in Krkonoše cirques (Úpská jáma, Labský důl); easily combined with a snow-cover CA.

### masselot1998lattice — A lattice Boltzmann model for particle transport and deposition (round 2)
- **Citation:** Masselot, A., Chopard, B. (1998). A lattice Boltzmann model for particle transport and deposition. *Europhysics Letters* 42(3), 259–264. DOI: 10.1209/epl/i1998-00239-3 (verified: Crossref)
- **Access:** paywall (Geneva repository record, restricted)
- **Phenomenon and study area:** Wind erosion, transport and deposition of snow/sand particles, ripples, deposits behind obstacles (2D slice).
- **Model:** Lattice Boltzmann wind flow + CA particles that are advected, settle by gravity, deposit and are eroded.
- **Code:** not found.
- **Validation:** Qualitative deposition patterns, ripples.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 2, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** Good in 2D (LB is GPU-friendly).
- **Relevance to ca-geo:** ATM-05 — the classic 2D CA/LB snow-drift reference (fence / road-cut demo).

### chopard1999cellular — Cellular automata and lattice Boltzmann methods: a new approach to computational fluid dynamics and particle transport (round 2)
- **Citation:** Chopard, B., Masselot, A. (1999). Cellular automata and lattice Boltzmann methods: a new approach to computational fluid dynamics and particle transport. *Future Generation Computer Systems* 16(2–3), 249–257. DOI: 10.1016/S0167-739X(99)00050-3 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Snow transport, erosion and deposition by wind (same model, longer description).
- **Model / Code / Validation:** as `masselot1998lattice`; no code found.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 2, S5 1 → 4, C. Assessed from: abstract (provisional)
- **Browser fit:** Good.
- **Relevance to ca-geo:** ATM-05 second reference; read the full text if access appears.

### hidalgohidalgo2025coupled — Coupled Cellular automata – Snowmelt Runoff Model: A Novel Framework for Assessing Climate Change Impacts on Streamflow (round 2)
- **Citation:** Hidalgo-Hidalgo, J.-D., Pulido-Velazquez, D., Collados-Lara, A.-J. (2025). Coupled Cellular automata – Snowmelt Runoff Model: A Novel Framework for Assessing Climate Change Impacts on Streamflow. *Earth Systems and Environment* 10(6), 6785–6804. DOI: 10.1007/s41748-025-00975-7 (verified: Crossref)
- **Access:** OA (CC BY), full text read
- **Phenomenon and study area:** Daily snow cover and snowmelt streamflow, Mediterranean catchment in the Sierra Nevada (Spain, EU).
- **Model:** The calibrated snow-cover CA of `colladoslara2019distributed` (binary state; rules on elevation, P and T indices, own and neighbours' previous state) produces daily SCA, which feeds the degree-day Snowmelt Runoff Model (12 parameters, SCE-UA calibration).
- **Inputs:** AEMET 5 km gridded P/T, DEM, MODIS SCA, streamflow.
- **Parameters:** SRM parameter table; CA parameters referred to the 2019 paper.
- **Code:** not found.
- **Validation:** SCA R² 0.77, NSE 0.72, pBIAS −13.8 %; streamflow NSE/KGE reported.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 2 → 6, C. Assessed from: full text (r2)
- **Browser fit:** Excellent (CA) + trivial bucket model.
- **Relevance to ca-geo:** HYD-06 → L6 chain template (snow CA feeding runoff) with quantitative targets.

### slezingr2013verification — Verification and proposal of the modification of "The method for the establishment of the erosion terminant" (round 2)
- **Citation:** Šlezingr, M., Pilařová, P., Pelikán, P., Zeleňáková, M. (2013; journal issue dated 2012). Verification and proposal of the modification of "The method for the establishment of the erosion terminant". *Acta Universitatis Agriculturae et Silviculturae Mendelianae Brunensis* 60(6), 303–308. DOI: 10.11118/actaun201260060303 (verified: Crossref)
- **Access:** OA (journal PDF read)
- **Phenomenon and study area:** Wave abrasion of reservoir banks: Brno reservoir, Bílovec reservoir, Vranov (CZ) and Liptovská Mara (SK), monitoring 2002–2011.
- **Model:** Not CA. Czech engineering method (Linhart, Kratochvíl): elevation of the "erosion terminant" (level below which bank retreat stops) from the most frequent water level, half the design wave height, the wave centre line and wind set-up; bank retreat follows from intersecting this level with the bank profile. The paper proposes a correction from measured vs computed levels.
- **Inputs:** Water-level statistics, fetch-based design wave, bank cross-sections.
- **Code:** none.
- **Validation:** Measured vs computed terminant levels at 10 profiles.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → 5, C. Assessed from: full text (r2)
- **Browser fit:** Trivial (per shoreline cell).
- **Relevance to ca-geo:** **HYD-08** Czech calibration / stop rule for a NEWTS-like reservoir shore CA (e.g. Vranov, Nechranice, Brno dam).

### mendicino2006threedimensional — Three-dimensional unsaturated flow modeling using cellular automata (round 2)
- **Citation:** Mendicino, G., Senatore, A., Spezzano, G., Straface, S. (2006). Three-dimensional unsaturated flow modeling using cellular automata. *Water Resources Research* 42(11). DOI: 10.1029/2005WR004472 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Richards-equation flow in partially saturated soils (Italy, EU).
- **Model:** Macroscopic CA with physically meaningful local laws (Darcy fluxes between face neighbours, nonlinear capacity and conductivity), explicit update; companion parallel version Folino et al. 2006 (*Parallel Computing*, DOI 10.1016/j.parco.2006.06.003, verified in Crossref).
- **Code:** not found.
- **Validation:** Against standard numerical solutions (details not seen).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → 5, C. Assessed from: abstract (provisional)
- **Browser fit:** 2D vertical slice feasible.
- **Relevance to ca-geo:** HYD-09 / ATM-04 infiltration–recharge layer; same family as `ravazzani2011macroscopic`.

### furnari2021asynchronous — Asynchronous cellular automata subsurface flow simulations in two- and three-dimensional heterogeneous soils (round 2)
- **Citation:** Furnari, L., Senatore, A., De Rango, A., De Biase, M., Straface, S., Mendicino, G. (2021). Asynchronous cellular automata subsurface flow simulations in two- and three-dimensional heterogeneous soils. *Advances in Water Resources* 153, 103952. DOI: 10.1016/j.advwatres.2021.103952 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Wetting-front propagation and drip-irrigation cycles in heterogeneous soils.
- **Model:** Macroscopic CA (as above) with an activation/deactivation rule: a cell is updated only if the total-head difference to its neighbourhood exceeds a threshold (asynchronous CA); implemented in the OpenCAL library.
- **Code:** OpenCAL, https://github.com/OpenCALTeam/opencal (LGPL-3.0, HTTP 200) — library only, model code not confirmed → S3 1.
- **Validation:** Hundreds of probabilistic wet-front simulations vs synchronous CA (speed-up and error).
- **Reimplementability:** S1 1, S2 1, S3 1, S4 2, S5 1 → 6, C. Assessed from: abstract (provisional)
- **Browser fit:** Good; the activation threshold is a useful performance trick for any WebGL/JS diffusion CA.
- **Relevance to ca-geo:** HYD-09 performance idea (skip quiescent cells).

### ling2018modelling — Modelling Spatial-Temporal Dynamics of Cyanobacteria Abundance in Lakes by Integrating Cellular Automata and Genetic Programming (round 2)
- **Citation:** Ling, Y., Wang, M., Chen, Q., Mynett, A. (2018). Modelling Spatial-Temporal Dynamics of Cyanobacteria Abundance in Lakes by Integrating Cellular Automata and Genetic Programming. *EPiC Series in Engineering* 3 (HIC 2018, 13th Int. Conf. on Hydroinformatics). DOI: 10.29007/dl2b (verified: Crossref; year from the proceedings, Crossref has no issued date)
- **Access:** OA (EasyChair PDF read)
- **Phenomenon and study area:** Cyanobacteria abundance at monitoring sites in Lake Taihu (CN).
- **Model:** Lake divided into polygons around monitoring sites; a GP-derived rule predicts next-step cyanobacteria from physico-chemical variables, plus a weighted contribution (weight 0.3, distance-scaled) of neighbouring sites selected by the prevailing wind-driven flow direction.
- **Inputs:** Monitoring data (nutrients, temperature, etc.).
- **Code:** not found.
- **Validation:** r² > 0.54 at hypereutrophic sites; lower elsewhere.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 2 → 5, C. Assessed from: full text (r2)
- **Browser fit:** Good.
- **Relevance to ca-geo:** algal-bloom candidate (see new-phenomena.md, `algal-bloom`): wind-driven neighbour drift of biomass is a simple rule transferable to Czech reservoirs with Sentinel-2 chlorophyll maps.

### leskovar2026modeling — Modeling Heat Transfer in an Urban Settlement with 3D Cellular Automata and Artificial Intelligence (round 2)
- **Citation:** Leskovar, R. (2026). Modeling Heat Transfer in an Urban Settlement with 3D Cellular Automata and Artificial Intelligence. In *Artificial Intelligence and Environmental Challenges*, 151–162. University of Maribor Press. DOI: 10.18690/um.fov.5.2026.8 (verified: Crossref)
- **Access:** OA book chapter (press.um.si; not read)
- **Phenomenon and study area:** Synthetic 50 × 50 × 20 m city block at 46° N (Slovenia, EU), 30 days in May.
- **Model:** 3D CA, five material classes (air, asphalt, grass, concrete, indoor air); eight sequential physics layers (conduction, solar heating, nocturnal radiative cooling, relaxation to the free atmosphere, asphalt plume convection, Newton cooling, ventilation, boundaries). Code generated with an LLM assistant.
- **Code:** not found.
- **Validation:** Plausibility only (street 4–6 °C warmer than park at noon).
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → 3, D. Assessed from: abstract (provisional)
- **Browser fit:** 2D reduction feasible.
- **Relevance to ca-geo:** URB-01 — the only "genuine thermal CA" for UHI found besides `wagner2015cellular`; confirms the gap.

## Most reimplementable (top picks)

Updated in round 2.

1. **ashton2006highangle** (A, 10; r2 full text) — CEM fully specified (cell interpretation, CERC fluxes, shadowing, overwash, constants), open C code, quantitative regime and scaling checks. Primary spec for a coastline / large-reservoir shore demo.
2. **palermo2024newts** (A, 9) — complete algorithm, open USGS code, analytical test cases; any DEM + water level. HYD-08 core; CZ stop rule from `slezingr2013verification`.
3. **ravazzani2011macroscopic** (A, 9) — physically based MCA groundwater stencil fully documented in the FEST manual, Theis benchmark; trivial in WebGL (HYD-09, LND-03).
4. **sonnenschein2025hybrid** (B, 8; r2 code found) — open GPL Python implementation of the wind-weighted moving-window CA with GA calibration and external R² 0.60; the ATM-01 template.
5. **ATM-02 cold-air cluster** (all B 7–8, new in r2): `nowatschin2006gpubased` (complete shader-CA rule + land-use tables), `conrad2020coldairflow` (open GPL code), `sievers2016cold` (KLAM_21 physics + observations). Together they close the round-1 "no model" gap; `chung2006minimum` (C 6) gives a static baseline with logger validation.
6. **bernhardt2010snowslide** (B, 7; r2) — DEM-only gravitational snow redistribution, open third-party code (CHM); combine with the snow-cover CA for HYD-06/ATM-05.
7. **sharma2019understanding / kochanski2019rescal** (A 9 / B 8) — open GPL code with documented parameters; 3D and micro-scale, poor browser fit. For a 2D snow-drift demo `masselot1998lattice` (C 4) is the conceptual template.
8. **pardoiguzquiza2017estimation + colladoslara2019distributed** (C, 5) — still the best HYD-06 fit with open European inputs, but exact rules remain unread (repositories down/blocked); `hidalgohidalgo2025coupled` (C 6, OA) adds quantitative targets.

## Gaps and unverified leads

Updated in round 2.

- **ATM-02 (cold-air pooling):** gap closed by grid models (see top picks), but none is labelled "CA" and none is Czech. No peer-reviewed CZ modelling study of frost hollows found (Šumava bogs such as Jezerní slať appear only in news/amateur records — not usable as references). Leads: Kim & Yun 2011, cold-pool capacity of closed catchments (*Korean J. Agric. Forest Meteorol.* 13(4), DOI 10.5532/kjafm.2011.13.4.176, verified, not read); Ogrin et al. 2026, Dinaric frost hollows (book chapter, DOI 10.1007/978-3-031-99017-5_27, verified, observational); Schwab (2000) relief-analytic cold-air methods (Freiburger Geographische Hefte, no DOI).
- **ATM-03 (heavy gas):** no CA over terrain found; reference physics in TWODEE-2 (C). Leads verified in Crossref but not read: Sarkar & Abbasi 2006, CA forecasting of fire and toxic dispersion in process industries (*J. Hazard. Mater.* 137, DOI 10.1016/j.jhazmat.2006.01.081); Cao et al. 2016, CA-based emergency response for toxic gas releases (*Ann. Oper. Res.* 255, DOI 10.1007/s10479-016-2125-4); Hankin & Britter 1999, TWODEE parts 1 and 3 (*J. Hazard. Mater.* 66, DOIs 10.1016/S0304-3894(98)00269-6, 10.1016/S0304-3894(98)00270-2); Venetsanos et al. 2003, DISPLAY-2 shallow-layer model (DOI 10.1016/S0304-3894(03)00011-6). Salcido 1993, Korean CA system and the *Fire* 2025 frontal CA remain unverified.
- **ATM-05 (snow drift):** 2D CA/LB references exist (`masselot1998lattice`, `chopard1999cellular`, C 4, paywalled); SnowTran-3D / SnowModel (Liston & Sturm 1998) not verified in this round (Crossref rate limit); Bernhardt et al. 2010, snow transport with downscaled MM5 winds (*The Cryosphere* 4, DOI 10.5194/tc-4-99-2010, verified, OA, not read).
- **HYD-08 (reservoir shore abrasion):** no CA for reservoir shores besides NEWTS/CEM. CZ engineering method `slezingr2013verification`; lead Wierzbicki et al. 2025, Kachugin abrasion + slope stability for large Polish reservoirs (*Water* 17(11), 1576, DOI 10.3390/w17111576, verified, not read); Czech theses on Vranov/Boskovice (VUT Brno dspace, grey literature, not assessed).
- **HYD-09 / LND-03 (groundwater, post-mining lakes):** CA groundwater references are Italian/Serbian (`ravazzani2011macroscopic`, `milasinovic2019coupled`, `mendicino2006threedimensional`, `furnari2021asynchronous`). No CA or simple grid model of pit-lake filling found; only monitoring (Valvoda et al. 2012, Medard pit lake, *iSET Journal* 52(4), DOI 10.66829/zhu.2012.018, verified, CZ). LND-03 will combine an MCA aquifer with a lake-level/volume curve from the DEM — own design.
- **HYD-10 (oil spill on rivers/lakes):** no river or lake CA found; all CA spill models are marine. A river variant must adapt `karafyllidis1997oil`/`liu2022simulating`-type drift rules to channel flow from the WAT model. Lead: Boi-Ukeme, Echegini & Wainer 2018, Cell-DEVS coastal oil spill (Carleton publication page, not verified in Crossref).
- **URB-01 (UHI):** genuine thermal CA only `wagner2015cellular` (C 4) and `leskovar2026modeling` (D 3, now verified). Land-use CA + LST regression papers stay with `lu`.
- **Algal blooms:** `ling2018modelling` (C 5, OA) improves on `chen2006modelling`; lead Alfa et al. 2025, CA water-quality model for Heron Lake (41st IAHR World Congress, DOI 10.64697/978-90-835589-7-4_41wc-p2011-cd, verified, not read). No Czech CA study.
- **Lake/river ice, glacier flow, thermokarst, fog, heat waves:** still no CA found (round 2 Crossref checks confirmed).
- **Snow-cover CA full texts:** Digibug (Granada) down and digital.csic.es behind a bot check during round 2 — retry later. Further verified leads: Collados-Lara et al. 2021 (*Sci. Total Environ.* 788, DOI 10.1016/j.scitotenv.2021.147776); Pardo-Igúzquiza et al. 2017 chapter (DOI 10.1007/978-3-319-69356-9_31).
- **Unverified / not yet assessed leads (from round 1, still open):** Guariso, Maniezzo & Salomoni 1996 (DOI 10.1016/0096-3003(95)00214-6); Hamoudzadeh & Behzadi 2021 (DOI 10.36909/jer.13749); Troisi 2015 (IJMPC); Chen, Mynett & Minns 2002 (DOI 10.1016/S0304-3800(01)00428-8); NOAA habitat-recovery CA (DOI 10.7901/2169-3358-2005-1-533); Rybak et al. 2019 (DOI 10.33075/2220-5861-2019-4-72-80); Hawick 2014 (DOI 10.2316/p.2014.821-005); RUSICA; Seghir, Marcou & El Yacoubi 2018; Milašinović et al. 2018 (DOI 10.1007/978-3-319-99867-1_132, now verified in Crossref); Wang et al. 2024 (NHESS preprint 10.5194/nhess-2024-131); Gilbués desertification thesis; CATGRaSS; later CA cloud models; mangrove CA studies; Pearl River storm-surge CA.
- **Round 3 suggestions:** retry Digibug/CSIC for the snow-cover CA rules (likely C→B); read the Sonnenschein paper for fitted parameters (B→A possible); obtain Karafyllidis 1997 and Guariso 1992 via a library; read Bernhardt et al. 2010 (TC, OA) for wind-drift coupling.

## Round 2 changes

| Key | Old score/class | New score/class | Reason |
|---|---|---|---|
| ashton2006highangle | 7 B (provisional) | 10 A | full text read: complete rule, constants, quantitative regime/scaling checks |
| sonnenschein2025hybrid | 5 C (provisional) | 8 B | open GPL code (CellAutDisp) found and inspected; rule fully defined by code |
| zhang2025method | 5 C (provisional) | 6 C | full text (Europe PMC): complete rule; threshold/exponent values missing |
| ashton2001formation | 7 B | 7 B (unchanged) | Nature full text still inaccessible; model spec now taken from ashton2006highangle |
| palermo2024newts | 9 A | 9 A (unchanged) | confirmed; linked to CZ erosion-terminant method |
| ravazzani2011macroscopic | 9 A | 9 A (unchanged) | paper still paywalled; manual-based score kept |
| pardoiguzquiza2017estimation | 5 C | 5 C (unchanged) | repositories down/blocked; rule inputs confirmed by an OA follow-up |
| colladoslara2019distributed | 5 C | 5 C (unchanged) | as above; skill metrics from follow-up added |
| karafyllidis1997oil | 3 D | 3 D (unchanged) | no full text; secondary description added |
| liu2022simulating | 5 C | 5 C (unchanged) | journal PDF still blocked (HTTP 403) |
| kazak2018use | 4 C | 4 C (unchanged) | MDPI blocked (HTTP 403) |
| chen2006modelling | 3 D | 3 D (unchanged) | no full text; superseded by ling2018modelling |

## New phenomena candidates (round 2)

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| Natural CO2 degassing and pooling in depressions | CO2 from mofettes/springs flows as a dense layer into hollows, cellars and valley floors, diluting with time | Same dense-layer CA as ATM-03 but a natural, non-sensitive hazard with real sites | High: mofettes of the Cheb basin (Soos, Hartoušov, Bublák) — to be verified as a case | `folch2009twodee2` C, `folch2017highresolution` C | Could replace or complement ATM-03 as the "illustrative" dense-gas demo |
| Gravitational snow redistribution | Snow exceeding a slope-dependent holding depth slides to lower cells, filling cirques and couloirs | One-sweep DEM rule; links snow cover (HYD-06), drifts (ATM-05) and avalanche release (HAZ-03) | Medium–high: Krkonoše cirques (Úpská jáma, Labský důl) | `bernhardt2010snowslide` B | Could be a sub-mode of HYD-06 rather than a separate item |
| Nocturnal cold-air ventilation of towns (cold-air corridors) | Cold-air production on fields/meadows, drainage along valleys and blocking by settlements, trees or embankments | Planning scenario ("build here / plant trees here?") on the ATM-02 engine | High: valley towns (Ústí n. L., Karlovy Vary, Plzeň basin); border analogue Plauen | `nowatschin2006gpubased` B, `sievers2016cold` B, `uiboupin2025how` C | Variant of ATM-02 with an urban-planning output (volume flux through a cross-section) |
| Cyanobacterial bloom drift in reservoirs | Biomass growth from local conditions plus wind-driven drift to neighbouring cells | Visual, topical, Sentinel-2 chlorophyll maps for checks | High (Czech reservoirs and ponds) | `ling2018modelling` C, `chen2006modelling` D | Already proposed in new-phenomena.md (`algal-bloom`); listed here only to add `ling2018modelling` |
