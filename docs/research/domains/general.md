# Cross-cutting: reviews, frameworks, methods — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.

Domain code: `gen`. Scope: review papers on geographic / environmental CA, theory of geographic CA
(relaxed classical assumptions), CA–GIS integration, open-source CA frameworks, parallel / GPU / web
CA, calibration and validation (map comparison) methods, sensitivity / uncertainty analysis,
coupling, educational tools.

**Scoring conventions used in this file**

- Reviews, theory papers and software frameworks are not scored (`n/a`); their value is described as
  an entry point or, for frameworks, as a reference for the ca-geo JavaScript core.
- Map-comparison metrics and calibration procedures are *algorithms* rather than CA models. They are
  scored with the same five sub-criteria, read as: S1 = the metric / procedure is fully defined,
  S2 = no free parameters or their values are given, S3 = open implementation exists,
  S4 = can be applied to generic maps, S5 = worked examples with numbers usable as test cases.
- Years and bibliographic fields come from Crossref (`issued` year); OpenAlex was used for
  abstracts, open-access status and citation counts. Where the two disagree by one year
  (online-first vs. issue), the Crossref year is used.

## Search log

Date: 2026-10-12.

Note on sources: the shared OpenAlex free daily search budget was exhausted early in this session
(HTTP 429, "insufficient budget"), so **search** was done with Crossref `query.bibliographic`
(relevance ranked; total-hit counts from Crossref are huge and not meaningful), web search and the
GitHub search API. **Verification** of every included work was done twice: Crossref record (title,
authors, venue, volume, pages, DOI) and OpenAlex single-work lookup by DOI (still available;
abstract, OA status, citations). Missing abstracts were filled from the Semantic Scholar API where
available.

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automata geographical modelling review | Crossref | 8.7 M (ranked) | top hits dominated by Liu (2008) book chapters; not a useful entry point |
| cellular automata urban growth review | Crossref | 10.2 M (ranked) | mostly case studies; reviews found by targeted title queries below |
| cellular automata land use change review | Crossref | 11.0 M (ranked) | found Addae & Dragićević spherical CA (2022) |
| targeted title+author queries for 17 classic review / theory / CA–GIS papers (Couclelis, Batty & Xie, Santé, Torrens & O'Sullivan, O'Sullivan, Moreno, Stevens, Takeyama, Wagner, Clarke & Gaydos, Torrens & Benenson, Tobler, Di Gregorio & Serra, Tong & Feng, van Vliet, Aburas, White & Engelen) | Crossref | 17/17 found | all verified, see catalogue (White & Engelen and Wagner left out to limit overlap / size) |
| targeted queries for validation metrics (Pontius ×4, Costanza, Hagen, Hagen-Zanker, van Vliet) | Crossref | 7/8 found | Pontius (2000, 2002) PERS papers not found in Crossref, see gaps |
| targeted queries for sensitivity / uncertainty (Kocabas, Ménard, Yeh & Li, Hewitt, García-Álvarez) | Crossref | 5/5 | García-Álvarez (2021) not included (round 2) |
| targeted queries for frameworks (DINAMICA, TerraME, PCRaster, Landlab, CellLab-CTS, simecol, CellPyLib, OpenCAL, pRPL, LUE) | Crossref | 9/10 | LUE only as EGU abstracts (no journal paper found) |
| GPU CUDA parallel geographic cellular automata urban land use | web search | ~10 | Li et al. (2012), Guan et al. (2015), Xia et al. (2017), Blečić et al. (2012), mcPLUS repo |
| WebGL browser-based cellular automata flood OR wildfire | web search | ~9 | Swii2 (2012) found; no peer-reviewed fully client-side geographic CA |
| multi-hazard cascading cellular automata coupled | web search | ~9 | no CA-based multi-hazard coupling paper found (only non-CA chains) |
| review cellular automata natural hazards lava debris flow | web search | ~9 | macroscopic CA family (SCIARA / SCIDDICA); Avolio et al. (2012) theorem paper verified |
| educational interactive cellular automata teaching geography | web search | ~9 | Geographic Automata Tool (2024) found; NetLogo |
| open-source Python geospatial CA raster land use | web search | ~10 | landscapeR (R) — not CA-rule based, not included |
| cellular automata review environmental geosciences 2020–2023 | web search | ~10 | Ghosh et al. (2017) CA–Markov review; Crooks (2017) encyclopedia entry (verified, not included) |
| "minimization algorithm of the differences" Di Gregorio Serra | web search | ~9 | confirms MAD attribution; led to Avolio et al. (2012) |
| SIMLANDER R cellular automata | web search + Crossref | — | Hewitt et al. (2019) preprint and Roodposhti et al. (2020) |
| Map Comparison Kit | site check + Crossref | — | mck.riks.nl live; Visser & de Nijs (2006) verified |
| cellular automata webgl / webgpu / flood javascript / wildfire javascript / land use python | GitHub API | 36 / 19 / 0 / 1 / 3 | only generic (non-geographic) WebGL / WebGPU CA engines; see gaps |

### Round 2

OpenAlex still quota-blocked. Search via Crossref `query.bibliographic`, web search, GitHub API;
OA status via Semantic Scholar; full texts via author repositories and arXiv. Clark Digital Commons,
WUR, SAGE and ScienceDirect author manuscripts returned HTTP 403/503 to automated access.

| Query | Source | Hits | Notes |
|---|---|---|---|
| OA copies for hagen2003, hagenzanker2009, pontius2007, pontius2011death, pontius2011comparison, varga2019 | Semantic Scholar, repositories | 6 | only Hagen-Zanker 2009 (Surrey) readable |
| fuzzy kappa / figure of merit / map comparison code | GitHub API | 6 / 1 / 0 | ahhz/fuzzy_kappa_matlab (MIT, author's account) |
| diffeR source (R/ directory) | GitHub API | 13 files | quantity / exchange / shift + multiresolution functions inspected |
| validation of stochastic CA: path dependence, neutral models, stochastic component, fuzzy accuracy, quantity-exchange-shift | Crossref | 5/5 | Brown 2005, Hagen-Zanker & Lajoie 2008 (OA, read), García 2011, van Vliet 2013, Pontius & Santacruz 2014 |
| WebGPU geospatial simulation / WebGL flood simulation browser / browser wildfire WebGL | Crossref | n/m | no peer-reviewed client-side geographic CA |
| web-based CA client-side land use / flood / wildfire | web (extended) | ~10 | only Swii2 (server-side CA) and generic WebGL / WebGPU CA demos |
| GitHub: wildfire+simulation+webgl, webgpu+flood+simulation, cellular+automata+leaflet / maplibre / geotiff, gpu+cellular+automata+geospatial | GitHub API | 5 / 1 / 1 / 0 / 0 / 0 | yesca (TS, MIT, GPU wildfire on real terrain), deluge-flood-sim (TS, MIT, WebGPU shallow water) — 2026 hobby repos, no paper |
| web-based cellular automata urban growth platform | Crossref | n/m | Liu & He 2009 (SPIE, metadata only) |
| GPU cellular automata framework geoscience / differentiable CA | Crossref | n/m | PyTorchFire (EMS 2025, key from `fire`); Yu & Chang 2024 NHESS preprint (coupled flow + solute CA on GPU, belongs to `hyd`) |
| LUE asynchronous many-task framework | Crossref, GitHub | 3 | de Jong et al. 2021 (EMS, CC BY); repo computationalgeography/lue (MIT, active) |
| coupled CA cascading hazards / post-fire debris flow CA / multi-hazard CA | web, Crossref | ~9 | no coupled multi-hazard CA framework; Douvinet 2023 (RuiCells, post-fire runoff); SCIDDICA / LLUNPIY lineage (lahars incl. ice melt — `geo`) |
| interactive / educational CA land-use tool | Crossref | n/m | Hasbani et al. 2011 (InTech chapter, interactive rule creation; not assessed) |
| framework repositories (Landlab, OpenCAL, PCRaster, LUE, PyTorchFire) | GitHub API | 5 | Landlab MIT, last push 2026-10; PCRaster GPL-3.0, 2026-10; OpenCAL LGPL-3.0, last push 2019-11 (inactive); LUE MIT, 2026-09 |

## Model families

The cross-cutting literature does not describe one phenomenon but the **machinery** shared by all
geographic CA. Main strands:

1. **Foundations and reviews of geographic CA.** Tobler's "cellular geography" introduced CA-like
   local map transformations to geography (`tobler1979cellular`); urban CA took off in the 1990s
   (`batty1994cells`). Couclelis argued that geographic CA necessarily relax the classical formalism
   and need a theory of "proximal space" (`couclelis1997cellular`); Torrens & O'Sullivan set the
   research agenda (`torrens2001cellular`). Reviews of urban / land CA: `sante2010cellular`,
   `aburas2016simulation`, CA–Markov in environmental modelling `ghosh2017application`, assessment
   methods `tong2019review`, calibration / validation practice `vanvliet2016review`. No recent
   all-domain review of environmental / hazard CA was verified (gap).
2. **Relaxed CA assumptions (theory).** Irregular cells and graph neighbourhoods
   (`osullivan2001exploring`), parcel-based irregular CA with asynchronous updating
   (`stevens2007gis`), vector CA with dynamic neighbourhood and changing object geometry
   (`moreno2009implementation`), CA plus agents in a unified "geographic automata" formalism
   (`torrens2005geographic`), CA on a spherical (global) grid (`addae2022modelling`).
3. **Macroscopic CA for surface flows.** The Di Gregorio–Serra empirical method with the
   *minimisation algorithm of the differences* (MAD) for distributing outflows between neighbours
   (`digregorio1999empirical`, formal property proved in `avolio2012theorem`) underlies the
   SCIARA / SCIDDICA lava and debris-flow models and is directly relevant to every gravity-driven
   flow model in ca-geo.
4. **CA–GIS integration.** Geo-Algebra as a formal extension of map algebra for CA
   (`takeyama1997map`); loose coupling of a CA (SLEUTH) with GIS (`clarke1998loose`); GIS-embedded
   CA tools (`vanduynhoven2024geographic`).
5. **Software frameworks.** Map-algebra / scripting frameworks (PCRaster `karssenberg2010software`),
   Python Earth-surface toolkits with CA support (Landlab `hobley2017creative`,
   `barnhart2020landlab`, CellLab-CTS `tucker2016celllab`), land-change platforms (DINAMICA
   `soaresfilho2002dinamica`, TerraME `carneiro2013extensible`, SIMLANDER `hewitt2019cellular`),
   generic libraries (simecol `petzoldt2007simecol`, CellPyLib `antunes2021cellpylib`), parallel CA
   libraries (OpenCAL `derango2021opencal`, pRPL `guan2010general`, `guan2014prpl`), and NetLogo
   (software, no DOI).
6. **Parallel / GPU / web acceleration.** Cluster and GPU versions of urban CA
   (`guan2010general`, `li2012gpuca`, `blecic2012parallel`, `guan2015hybrid`, vectorised CA
   `xia2017high`); a browser front-end for a debris-flow CA (`parise2012swii2`).
7. **Calibration and validation (map comparison).** Multiple-resolution goodness of fit
   (`costanza1989model`, `pontius2011comparison`), figure of merit and null resolution
   (`pontius2007comparing`, FoM components `varga2019intensity`), quantity vs. allocation
   disagreement replacing kappa (`pontius2011death`), Kappa Simulation (`vanvliet2011revisiting`),
   Fuzzy Kappa (`hagen2003fuzzy`, `hagenzanker2009improved`), software implementing them
   (`visser2006map`), automatic calibration of neighbourhood rules (`roodposhti2020towards`).
8. **Sensitivity and uncertainty.** Neighbourhood size / type sensitivity (`kocabas2006assessing`),
   cell size and neighbourhood scale sensitivity (`menard2005exploration`), error propagation and
   stochastic uncertainty (`yeh2006errors`), parameter variability and metastability
   (`hewitt2017stable`).
9. **Coupling / multi-hazard and education.** No peer-reviewed CA-specific multi-hazard coupling
   framework was verified in this round; Landlab's component coupling (`hobley2017creative`) and
   PCRaster's script-level coupling are the closest reusable patterns. Educational use is reported
   for Landlab, the Geographic Automata Tool and NetLogo.

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| tobler1979cellular | 1979 | Cellular geography | theory (map transformation) | raster / local neighbourhood / any | n/a | n/a | n/a | – | paywall | metadata |
| batty1994cells | 1994 | From cells to cities | urban growth (review + generic model) | raster / Moore-type / developed-undeveloped / det.+stoch. | n/a | n/a | n/a | – | paywall | abstract |
| couclelis1997cellular | 1997 | From CA to urban models | theory (relaxing CA) | proximal space, geo-algebra | n/a | n/a | n/a | – | paywall | abstract |
| takeyama1997map | 1997 | Map dynamics / Geo-Algebra | CA–GIS theory | generalised neighbourhoods via map algebra | n/a | n/a | n/a | – | paywall | abstract |
| clarke1998loose | 1998 | Loose-coupling CA and GIS (SLEUTH) | urban growth | raster / Moore / urban-non-urban / stoch. | 1 1 2 1 1 | 6 | C | yes (NCGIA page) | OA | abstract (provisional) |
| digregorio1999empirical | 1999 | Empirical method for macroscopic CA | surface flows (theory) | raster or hex / von Neumann-Moore / multi-substate / det. | n/a | n/a | n/a | – | paywall | metadata + secondary sources |
| osullivan2001exploring | 2001 | Irregular CA and spatial process dynamics | theory (irregular CA) | graph / irregular / binary / stoch. | n/a | n/a | n/a | – | paywall | abstract |
| torrens2001cellular | 2001 | CA and urban simulation: where next? | review / agenda | – | n/a | n/a | n/a | – | OA | metadata |
| soaresfilho2002dinamica | 2002 | DINAMICA | landscape / deforestation (platform) | raster / patcher-expander / multi-class / stoch. | n/a | n/a | n/a | free, closed (dinamicaego.com) | paywall | TLDR |
| menard2005exploration | 2005 | Spatial scale sensitivity of GCA | land-cover change (method) | raster 100–1000 m / 6 neighbourhoods / stoch. | n/a | n/a | n/a | – | paywall | abstract |
| torrens2005geographic | 2005 | Geographic automata systems | theory (CA + agents) | fixed and mobile automata | n/a | n/a | n/a | – | paywall | abstract |
| kocabas2006assessing | 2006 | CA behaviour via sensitivity analysis | urban growth (method) | raster / varied neighbourhood size+type | n/a | n/a | n/a | – | paywall | TLDR |
| visser2006map | 2006 | The Map Comparison Kit | map comparison software | – | n/a | n/a | n/a | free, closed (mck.riks.nl) | paywall | metadata + website |
| yeh2006errors | 2006 | Errors and uncertainties in urban CA | uncertainty (method) | – | n/a | n/a | n/a | – | paywall | TLDR |
| petzoldt2007simecol | 2007 | simecol (R) | ecological models incl. grid CA | raster / user-defined | n/a | n/a | n/a | yes (CRAN) | OA | abstract |
| stevens2007gis | 2007 | GIS-based irregular CA (iCity) | land use at parcel level | irregular parcels / adjacency / land-use classes / async. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| pontius2007comparing | 2007 | Input, output, validation maps of 13 land-change applications | validation metric (FoM, null resolution) | – | 1 2 0 2 1 | 6 | C | not found | OA (repository record) | abstract (provisional) |
| moreno2009implementation | 2009 | Dynamic neighbourhood in vector CA (VecGCA) | land-use change | vector objects / dynamic whole-space neighbourhood / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| hagen2003fuzzy | 2003 | Fuzzy set map comparison (Fuzzy Kappa) | validation metric | distance-decay neighbourhood, category similarity | 1 1 1 2 1 | 6 | C | MCK (closed) | OA | abstract (provisional) |
| costanza1989model | 1989 | Multiple-resolution goodness of fit | validation metric | moving windows of growing size | 1 1 0 2 1 | 5 | C | not found | paywall | TLDR (provisional) |
| hagenzanker2009improved | 2009 | Improved Fuzzy Kappa | validation metric | as above + autocorrelation-aware expectation | 2 2 2 2 1 | 9 | A | MATLAB, MIT (ahhz/fuzzy_kappa_matlab, verified) + MCK | OA (green, Surrey) | full text (r2) |
| karssenberg2010software | 2010 | PCRaster Python framework | modelling framework | raster map algebra, Monte Carlo, particle filter | n/a | n/a | n/a | yes (GitHub, GPL-3.0) | OA | TLDR |
| guan2010general | 2010 | pRPL + pSLEUTH | parallel raster / CA library | raster, domain decomposition, MPI | n/a | n/a | n/a | yes (GitHub) | paywall | abstract |
| sante2010cellular | 2010 | Review of real-world urban CA | review | – | n/a | n/a | n/a | – | paywall | TLDR |
| pontius2011death | 2011 | Death to Kappa | validation metric (quantity / allocation disagreement) | cross-tabulation | 2 2 2 2 1 | 9 | A | diffeR (R, CRAN/GitHub) | OA (author manuscript) | abstract (provisional) |
| pontius2011comparison | 2011 | Three maps at multiple resolutions | validation metric | nested coarse squares | 1 2 2 2 1 | 8 | B | diffeR (R) | paywall | abstract (provisional) |
| vanvliet2011revisiting | 2011 | Kappa Simulation | validation metric | transition-based expected agreement | 1 2 1 2 1 | 7 | B | MCK 3.2.2 (closed) | OA (repository record) | abstract (provisional) |
| blecic2012parallel | 2012 | Urban dynamics on the GPU | GPU acceleration | constrained urban CA | n/a | n/a | n/a | – | paywall | TLDR |
| li2012gpuca | 2012 | GPU-CA for large-scale land use | GPU acceleration | raster / CUDA | n/a | n/a | n/a | – | OA | abstract |
| parise2012swii2 | 2012 | Swii2 HTML5/WebGL debris-flow app | web front-end for CA | SCIDDICA-k0 (server side) | n/a | n/a | n/a | – | paywall | TLDR |
| avolio2012theorem | 2012 | Theorem about MAD | theory (outflow distribution) | multicomponent macroscopic CA | n/a | n/a | n/a | – | paywall | TLDR |
| carneiro2013extensible | 2013 | TerraME toolbox | modelling platform (CA + ABM) | raster cellular spaces, Lua | n/a | n/a | n/a | yes (GitHub, LGPL-3.0) | OA | TLDR |
| guan2014prpl | 2014 | pRPL 2.0 | parallel raster library | MPI | n/a | n/a | n/a | yes (GitHub) | paywall | metadata |
| guan2015hybrid | 2015 | Hybrid GPU/CPU parallel urban CA | GPU acceleration | raster / SLEUTH-like | n/a | n/a | n/a | – | paywall | abstract |
| tucker2016celllab | 2016 | CellLab-CTS (Landlab) | continuous-time stochastic CA library | square or hex / pair transitions / Gillespie-type | n/a | n/a | n/a | yes (GitHub, MIT) | OA | abstract |
| aburas2016simulation | 2016 | Review: urban growth CA | review | – | n/a | n/a | n/a | – | paywall | TLDR |
| vanvliet2016review | 2016 | Review of calibration / validation practice | review | – | n/a | n/a | n/a | – | OA (repository record) | TLDR |
| hobley2017creative | 2017 | Landlab | modelling framework | regular + irregular grids, CA tools | n/a | n/a | n/a | yes (GitHub, MIT) | OA | abstract |
| ghosh2017application | 2017 | Review: CA–Markov in environmental modelling | review | – | n/a | n/a | n/a | – | paywall | TLDR |
| hewitt2017stable | 2017 | Sensitivity analysis / metastability | uncertainty (method) | constrained land-use CA | n/a | n/a | n/a | – | paywall | TLDR |
| xia2017high | 2017 | Vectorised + parallel urban CA | acceleration | raster 5 m / 3×3 | n/a | n/a | n/a | – | paywall | abstract |
| hewitt2019cellular | 2019 | SIMLANDER (R) | land-use change | raster / neighbourhood rules + suitability + accessibility + zoning / stoch. | 1 1 2 2 1 | 7 | B | R script + demo data (project site, verified in land-use.md) | OA (preprint) | abstract + project site (harmonised r2) |
| tong2019review | 2019 | Review of CA assessment methods | review | – | n/a | n/a | n/a | – | paywall | abstract |
| varga2019intensity | 2019 | Intensity Analysis + FoM components | validation metric | – | 1 2 0 2 1 | 6 | C | not verified | OA (author manuscript) | abstract (provisional) |
| barnhart2020landlab | 2020 | Landlab v2.0 | modelling framework | as Landlab | n/a | n/a | n/a | yes (GitHub, MIT) | OA | metadata |
| roodposhti2020towards | 2020 | Automatic calibration of neighbourhood rules | calibration procedure | SIMLANDER CA | 2 2 2 2 2 | 10 | A | SIMLANDER (verified) + suppl. script | OA (accepted ms) | full text (harmonised r2 with land-use.md) |
| derango2021opencal | 2021 | OpenCAL extension | parallel CA library | 2D/3D structured grids, OpenMP/OpenCL/MPI | n/a | n/a | n/a | yes (GitHub, LGPL-3.0) | OA | abstract |
| antunes2021cellpylib | 2021 | CellPyLib | generic CA library | 1D/2D / Moore, von Neumann / discrete+continuous | n/a | n/a | n/a | yes (GitHub, Apache-2.0) | OA | abstract |
| addae2022modelling | 2022 | Spherical CA for global urban change | urban land use (global) | geodesic grid on sphere | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only (provisional) |
| vanduynhoven2024geographic | 2024 | Geographic Automata Tool (ArcGIS Pro) | GIS-embedded CA framework | binary / multi-class CA | n/a | n/a | n/a | not verified | OA | abstract |
| hagenzanker2008neutral | 2008 | Neutral models of landscape change as benchmarks (r2) | validation method (null models) | random constraint match; growing clusters; multi-scale criteria | 2 2 0 2 1 | 7 | B | not found | OA (green, Surrey) | full text |
| pontius2014quantity | 2014 | Quantity, exchange and shift components (r2) | validation metric | cross-tabulation | 1 2 2 2 1 | 8 | B | diffeR (R, verified functions) | paywall | metadata + diffeR source (provisional) |
| vanvliet2013fuzzy | 2013 | Fuzzy accuracy of land-use simulations (r2) | validation metric (fuzzy) | details unknown | 1 1 0 2 1 | 5 | C | not verified | paywall | metadata only (provisional) |
| brown2005path | 2005 | Path dependence and validation of stochastic land-use models (r2) | validation of stochastic models | – | n/a | n/a | n/a | – | OA (bronze, blocked) | metadata (provisional) |
| garcia2011analysis | 2011 | Effect of the stochastic component of urban CA (r2) | uncertainty (stochastic term) | urban CA | n/a | n/a | n/a | – | paywall | metadata (provisional) |
| xia2025pytorchfire | 2025 | PyTorchFire: GPU differentiable wildfire CA (r2) | GPU CA + gradient calibration | raster / Moore 3×3 / burnable-burning-burned / stoch. | 2 2 2 2 2 | 10 | A | GitHub MIT + Zenodo (verified) | OA (CC BY; arXiv) | full text (arXiv, key from `fire`) |
| dejong2021environmental | 2021 | LUE: asynchronous many-task modelling framework (r2) | modelling framework (map algebra, HPC) | raster, AMT (HPX) | n/a | n/a | n/a | yes (GitHub, MIT) | OA (CC BY) | metadata + repository |
| liu2009developing | 2009 | Web-based CA for urban growth (r2) | web CA (architecture unknown) | – | n/a | n/a | n/a | – | paywall | metadata only |
| douvinet2023postfire | 2023 | Post-fire runoff concentration with RuiCells CA (r2) | hazard chain: fire → runoff / debris flow | raster runoff-concentration CA | 1 1 1 1 1 | 5 | C | RuiCells (closed, ©) | OA (IntechOpen) | abstract |
| netlogo | – | NetLogo | agent / patch modelling environment | patch grid, user rules | n/a | n/a | n/a | yes (GitHub, GPL-2.0) | software, no DOI | website + repository |

Total: 50 verified publications + 1 software item without DOI (NetLogo) after round 1; round 2 adds 9 rows (8 new DOIs + 1 key reused from `fire`), total 59.
Classes after round 2: A 4, B 5, C 9, D 1, n/a 40 (+ NetLogo, n/a).

## Entries

### Reviews and foundations

### tobler1979cellular — Cellular Geography
- **Citation:** Tobler, W. R. (1979). Cellular Geography. In *Philosophy in Geography* (Theory and Decision Library), pp. 379–386. DOI: 10.1007/978-94-009-9394-5_18 (verified: Crossref, OpenAlex)
- **Access:** paywall (book chapter).
- **Phenomenon and study area:** conceptual; geographic change as local transformations of a cell array.
- **Model / value:** the origin point cited by virtually all geographic CA papers; frames land-use change as a function of a cell's state and that of its neighbours. No abstract available; assessed from metadata only.
- **Reimplementability:** n/a. Entry point and historical anchor for the ca-geo background chapter.
- **Relevance to ca-geo:** general framing.

### batty1994cells — From Cells to Cities
- **Citation:** Batty, M., Xie, Y. (1994). From Cells to Cities. *Environment and Planning B: Planning and Design* 21(7), S31–S48. DOI: 10.1068/b21s031 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** reviews CA in general and in urban systems, proposes a general class of urban CA and illustrates it on the historical grid city of Savannah, a hypothetical case, and a suburban area of a North American city.
- **Reimplementability:** n/a (review + illustrative models). Entry point for urban CA; land-use domain (`lu`) should cover the model itself.
- **Relevance to ca-geo:** LND-01.

### couclelis1997cellular — From Cellular Automata to Urban Models: New Principles for Model Development and Implementation
- **Citation:** Couclelis, H. (1997). *Environment and Planning B: Planning and Design* 24(2), 165–174. DOI: 10.1068/b240165 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** argues that GIS-integrated CA lose the formal integrity of the classical CA through successive relaxations (non-uniform cells, non-stationary rules, external constraints, action at a distance), proposes "proximal space" as the theoretical answer and geo-algebra as the practical formalism.
- **Reimplementability:** n/a. Key theory reference: it legitimises the ca-geo design choice of *heterogeneous* cells (each cell carrying DEM, land-cover, soil attributes) and non-local inputs.
- **Relevance to ca-geo:** architecture (cell = vector of layer values; rules may read layers).

### torrens2001cellular — Cellular Automata and Urban Simulation: Where Do We Go from Here?
- **Citation:** Torrens, P. M., O'Sullivan, D. (2001). *Environment and Planning B: Planning and Design* 28(2), 163–168. DOI: 10.1068/b2802ed (verified: Crossref, OpenAlex)
- **Access:** OA (publisher PDF).
- **Content:** editorial setting the research agenda for urban CA (theory, validation, space-time representation, links to other model types). No abstract; assessed from metadata.
- **Reimplementability:** n/a. Entry point.

### sante2010cellular — Cellular automata models for the simulation of real-world urban processes: A review and analysis
- **Citation:** Santé, I., García, A. M., Miranda, D., Crecente, R. (2010). *Landscape and Urban Planning* 96(2), 108–122. DOI: 10.1016/j.landurbplan.2010.03.001 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** reviews and classifies urban CA applied to real cases by their main characteristics (cell space, neighbourhood, transition rules, calibration), with strengths and weaknesses.
- **Reimplementability:** n/a. Most-cited urban CA review (~750 citations in OpenAlex); useful to pick land-use models with full specifications.
- **Relevance to ca-geo:** LND-01, LND-02.

### aburas2016simulation — The simulation and prediction of spatio-temporal urban growth trends using cellular automata models: A review
- **Citation:** Aburas, M. M., Ho, Y. M., Ramli, M. F., Ash'aari, Z. H. (2016). *International Journal of Applied Earth Observation and Geoinformation* 52, 380–389. DOI: 10.1016/j.jag.2016.07.007 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** review of CA urban growth models, their structure and hybrid extensions.
- **Reimplementability:** n/a. Secondary entry point (more recent than Santé et al.).
- **Relevance to ca-geo:** LND-01.

### ghosh2017application — Application of Cellular automata and Markov-chain model in geospatial environmental modeling — A review
- **Citation:** Ghosh, P., Mukhopadhyay, A., Chanda, A., Mondal, P., Akhand, A., Mukherjee, S., Nayak, S. K., Ghosh, S., Mitra, D., Ghosh, T., Hazra, S. (2017). *Remote Sensing Applications: Society and Environment* 5, 64–77. DOI: 10.1016/j.rsase.2017.01.005 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** concepts of CA–Markov modelling and a classification of applications (land use / cover, forest, wetlands, watershed and coastal management).
- **Reimplementability:** n/a. Entry point for CA–Markov, the most widely applied (and least formally specified) environmental CA variant.
- **Relevance to ca-geo:** LND-01/02, ECO-02.

### tong2019review — A review of assessment methods for cellular automata models of land-use change and urban growth
- **Citation:** Tong, X., Feng, Y. (2019). *International Journal of Geographical Information Science* 34(5), 866–898. DOI: 10.1080/13658816.2019.1684499 (verified: Crossref, OpenAlex; issue year 2020)
- **Access:** paywall.
- **Content:** systematic review of 347 CA articles (1999–2018): 89 % report some assessment, using more than ten methods; cell-by-cell comparison and landscape metrics dominate, overall accuracy and standard kappa are the most frequent metrics; end-state comparison is criticised; five recommendations for method choice.
- **Reimplementability:** n/a. Best single entry point for the validation module of ca-geo.
- **Relevance to ca-geo:** shared validation component.

### vanvliet2016review — A review of current calibration and validation practices in land-change modeling
- **Citation:** van Vliet, J., Bregt, A. K., Brown, D. G., van Delden, H., Heckbert, S., Verburg, P. H. (2016). *Environmental Modelling & Software* 82, 174–182. DOI: 10.1016/j.envsoft.2016.04.017 (verified: Crossref, OpenAlex)
- **Access:** OA (Wageningen repository record).
- **Content:** reviews calibration / validation in land-change modelling and highlights uncertainty, non-stationarity, equifinality and multifinality as challenges.
- **Reimplementability:** n/a. Entry point; supports the ca-geo position that a demo should show ensembles and multiple metrics rather than one "accuracy" number.

### Theory: relaxed CA assumptions

### osullivan2001exploring — Exploring Spatial Process Dynamics Using Irregular Cellular Automaton Models
- **Citation:** O'Sullivan, D. (2001). *Geographical Analysis* 33(1), 1–18. DOI: 10.1111/j.1538-4632.2001.tb00433.x (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** proposes a framework to test how CA behaviour depends on the spatial structure (irregular lattices / graphs instead of grids); introduces an entropy-based "spatial information" measure; finds spatially robust vs. fragile processes.
- **Reimplementability:** n/a (method). The spatial-information measure could be a cheap pattern metric for ca-geo.
- **Relevance to ca-geo:** design decision on grid vs. graph topology; robustness checks.

### stevens2007gis — A GIS-Based Irregular Cellular Automata Model of Land-Use Change
- **Citation:** Stevens, D., Dragićević, S. (2007). *Environment and Planning B: Planning and Design* 34(4), 708–724. DOI: 10.1068/b32098 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Phenomenon and study area:** land-use change at the rural–urban fringe; a mid-sized Canadian city.
- **Model:** cells = irregular land parcels; neighbourhood by parcel adjacency; combination of synchronous and asynchronous development; scenario parameters for subdivision design, population growth, buyer preferences.
- **Inputs:** high-resolution parcel data.
- **Parameters:** not visible in abstract.
- **Code:** prototype in a desktop GIS; not found.
- **Validation:** not described in abstract.
- **Reimplementability:** S1 1 – main logic only from abstract; S2 1 – provisional; S3 0; S4 1 – cadastral parcels (CZ RÚIAN parcels would be an analogue); S5 1 → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** parcel graphs of thousands of polygons are feasible; needs vector support.
- **Relevance to ca-geo:** LND-01; reference if ca-geo ever supports vector cells.

### moreno2009implementation — Implementation of a dynamic neighborhood in a land-use vector-based cellular automata model
- **Citation:** Moreno, N., Wang, F., Marceau, D. J. (2009). *Computers, Environment and Urban Systems* 33(1), 44–54. DOI: 10.1016/j.compenvurbsys.2008.09.008 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Phenomenon and study area:** land-use / land-cover change in two regions of Quebec and Alberta, Canada.
- **Model:** VecGCA — space is a set of irregular geographic objects; the neighbourhood is the whole space but dynamic: two objects are neighbours if the objects between them favour the transition; objects change shape and area via a transition function.
- **Inputs:** vector land-use maps.
- **Parameters:** not visible in abstract.
- **Code:** not found.
- **Validation:** visual / pattern similarity with reference land-use maps.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** geometry operations per step make it heavy; not a priority.
- **Relevance to ca-geo:** illustrates removing cell-size dependency; mainly a theory reference.

### torrens2005geographic — Geographic Automata Systems
- **Citation:** Torrens, P. M., Benenson, I. (2005). *International Journal of Geographical Information Science* 19(4), 385–412. DOI: 10.1080/13658810512331325139 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** formal framework that unifies CA and multi-agent systems for geographic objects (fixed and mobile automata, with explicit location and neighbourhood rules); illustrated with an object-based urban simulation environment and a segregation model.
- **Reimplementability:** n/a. Conceptual model for ca-geo's possible extension to agents (evacuation MOV-01, wild boar EPI-02).

### addae2022modelling — Modelling global urban land-use change process using spherical cellular automata
- **Citation:** Addae, B., Dragićević, S. (2022). *GeoJournal* 88(3), 2737–2754. DOI: 10.1007/s10708-022-10776-4 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Phenomenon and study area:** global urban land-use change on a spherical (geodesic) grid.
- **Model / inputs / parameters:** no abstract available in Crossref, OpenAlex or Semantic Scholar; only the title and venue were verified.
- **Code:** not found.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D. Assessed from: metadata only (provisional).
- **Relevance to ca-geo:** out of scope for CZ-scale rasters; listed as the representative of non-planar CA grids.

### digregorio1999empirical — An empirical method for modelling and simulating some complex macroscopic phenomena by cellular automata
- **Citation:** Di Gregorio, S., Serra, R. (1999). *Future Generation Computer Systems* 16(2–3), 259–271. DOI: 10.1016/s0167-739x(99)00051-5 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** defines the "macroscopic CA" methodology for large-scale surface flows: cells with multiple substates (e.g. altitude, thickness, energy), elementary processes applied in sequence, and the *minimisation algorithm of the differences* (MAD) that distributes outflows from a cell to its neighbours so as to reduce local disequilibrium. Secondary sources (Avolio et al. 2012 and SCIARA / SCIDDICA papers found in the web search) confirm this attribution. No abstract available; full text not read.
- **Reimplementability:** n/a (methodology). Essential reference for every gravity-driven flow model in ca-geo (water, debris, lava, cold air, heavy gas).
- **Relevance to ca-geo:** HYD-01..04, HAZ-02, HAZ-05, ATM-02, ATM-03; shared component "gravity-driven outflow distribution".

### avolio2012theorem — A Theorem about the Algorithm of Minimization of Differences for Multicomponent Cellular Automata
- **Citation:** Avolio, M. V., Di Gregorio, S., Spataro, W., Trunfio, G. A. (2012). In *Cellular Automata (ACRI 2012)*, Lecture Notes in Computer Science, pp. 289–298. DOI: 10.1007/978-3-642-33350-7_30 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** proves a fundamental property of MAD for multicomponent CA (extending an earlier theorem).
- **Reimplementability:** n/a. Formal backing for using MAD as a shared outflow kernel; good test-case source if the full text is obtained.
- **Relevance to ca-geo:** same as `digregorio1999empirical`.

### CA–GIS integration

### takeyama1997map — Map dynamics: integrating cellular automata and GIS through Geo-Algebra
- **Citation:** Takeyama, M., Couclelis, H. (1997). *International Journal of Geographical Information Science* 11(1), 73–91. DOI: 10.1080/136588197242509 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** generalises CA within Geo-Algebra, a mathematical extension of map algebra, so that spatial data manipulation and dynamic models share one framework ("map dynamics").
- **Reimplementability:** n/a. Conceptual basis for a ca-geo API where CA rules are composed from map-algebra operations (local / focal / zonal).

### clarke1998loose — Loose-coupling a cellular automaton model and GIS: long-term urban growth prediction for San Francisco and Washington/Baltimore
- **Citation:** Clarke, K. C., Gaydos, L. J. (1998). *International Journal of Geographical Information Science* 12(7), 699–714. DOI: 10.1080/136588198241617 (verified: Crossref, OpenAlex)
- **Access:** OA (publisher PDF link in OpenAlex).
- **Phenomenon and study area:** urban growth, San Francisco Bay and Washington/Baltimore, USA.
- **Model:** the CA later known as SLEUTH, calibrated on historical urban maps; GIS used only for input / output (loose coupling).
- **Inputs:** historical urban extent, slope, roads, exclusion, hillshade (standard SLEUTH layers; details in abstract are general).
- **Parameters:** control parameters compared between the two regions; calibration procedure described.
- **Code:** SLEUTH project page verified: http://www.ncgia.ucsb.edu/projects/gig/ (HTTP 200).
- **Validation:** calibration fit and comparison with other models / observed growth.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: abstract (provisional). The land-use domain should give the full SLEUTH assessment.
- **Browser fit:** grid of a few million cells and Monte Carlo runs feasible with Web Workers.
- **Relevance to ca-geo:** LND-01; the loose-coupling pattern (CA engine separate from GIS I/O) is what ca-geo does with GeoTIFF / COG inputs.

### vanduynhoven2024geographic — The Geographic Automata Tool: A New General-Purpose Geosimulation Extension for ArcGIS Pro
- **Citation:** van Duynhoven, A., Dragićević, S. (2024). *Applied Sciences* 14(15), 6530. DOI: 10.3390/app14156530 (verified: Crossref, OpenAlex)
- **Access:** OA (MDPI; full-text page returned HTTP 403 to automated fetch).
- **Content:** a general-purpose CA framework as an ArcGIS Pro add-in, with generic functions for binary and multi-class CA and end-to-end projects using built-in GIS tools; two case studies; explicitly intended also for education.
- **Code:** a public download location was not verified (story map exists, no link extracted).
- **Reimplementability:** n/a. As a reference for ca-geo: shows which generic building blocks a GIS user expects (suitability, neighbourhood, constraint, stochastic term, multi-class). Proprietary host platform.
- **Relevance to ca-geo:** educational positioning; feature checklist.

### Software frameworks

### karssenberg2010software — A software framework for construction of process-based stochastic spatio-temporal models and data assimilation
- **Citation:** Karssenberg, D., Schmitz, O., Salamon, P., de Jong, K., Bierkens, M. F. P. (2010). *Environmental Modelling & Software* 25(4), 489–502. DOI: 10.1016/j.envsoft.2009.10.004 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** PCRaster Python framework: map-algebra operations on 2D maps and 3D blocks combined in Python scripts with a time-iteration framework, Monte Carlo simulation and data assimilation (particle filter / ensemble Kalman filter).
- **Code:** https://github.com/pcraster/pcraster (C++, GPL-3.0, active 2026); site https://pcraster.geo.uu.nl.
- **Reimplementability:** n/a. **Reuse for ca-geo:** high as a design reference — the "initial / dynamic step + Monte Carlo wrapper" model template and the operation set (local drain direction, accuflux, spread, window operations) map well onto a JS core; GPL licence means design reuse rather than code copying.
- **Relevance to ca-geo:** core architecture; HYD-01 (ldd / accuflux), MOV-03 (spread = travel-time front).

### hobley2017creative — Creative computing with Landlab
- **Citation:** Hobley, D. E. J., Adams, J. M., Nudurupati, S. S., Hutton, E. W. H., Gasparini, N. M., Istanbulluoglu, E., Tucker, G. E. (2017). Creative computing with Landlab: an open-source toolkit for building, coupling, and exploring two-dimensional numerical models of Earth-surface dynamics. *Earth Surface Dynamics* 5(1), 21–46. DOI: 10.5194/esurf-5-21-2017 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** Python framework with regular and irregular grids, interoperable process components, I/O and visualisation tools; supports CA and coupling of CA with differential-equation components; examples include landform evolution, a cellular ecohydrology model and flood-wave routing; intended also for classroom use.
- **Code:** https://github.com/landlab/landlab (Python, MIT, active 2026).
- **Reimplementability:** n/a. **Reuse for ca-geo:** very high — MIT licence, a clean component interface (named fields on grid nodes, `run_one_step(dt)`), and existing components (flow routing, overland flow, fire / vegetation CA) can serve as reference implementations and numerical test oracles for the JS ports.
- **Relevance to ca-geo:** coupling architecture for chains L1–L14; ECO-02, HYD-01, HYD-05.

### barnhart2020landlab — Landlab v2.0
- **Citation:** Barnhart, K. R., Hutton, E. W. H., Tucker, G. E., Gasparini, N. M., Istanbulluoglu, E., Hobley, D. E. J., et al. (2020). Short communication: Landlab v2.0: a software package for Earth surface dynamics. *Earth Surface Dynamics* 8(2), 379–397. DOI: 10.5194/esurf-8-379-2020 (verified: Crossref)
- **Access:** OA.
- **Content:** describes the v2 API and component catalogue (assessed from metadata only).
- **Reimplementability:** n/a; companion to `hobley2017creative`.

### tucker2016celllab — CellLab-CTS 2015: continuous-time stochastic cellular automaton modeling using Landlab
- **Citation:** Tucker, G. E., Hobley, D. E. J., Hutton, E., Gasparini, N. M., Istanbulluoglu, E., Adams, J. M., Nudurupati, S. S. (2016). *Geoscientific Model Development* 9(2), 823–839. DOI: 10.5194/gmd-9-823-2016 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** Python library for continuous-time stochastic CA: integer node states, transitions defined on pairs of adjacent nodes with average rates, event-driven (asynchronous) update, square or hexagonal grids, moving-particle states, user callbacks after each transition.
- **Code:** https://github.com/landlab/landlab/tree/master/src/landlab/ca (verified; MIT).
- **Reimplementability:** n/a (library). **Reuse for ca-geo:** high — the cleanest published specification of an asynchronous, rate-based CA update scheme; a good alternative to synchronous stepping for slow processes (weathering, succession, spread with rates). Event-queue design ports easily to JS.
- **Relevance to ca-geo:** ECO-02, ECO-03, HYD-05; update-scheme options in the core.

### soaresfilho2002dinamica — DINAMICA — a stochastic cellular automata model designed to simulate the landscape dynamics in an Amazonian colonization frontier
- **Citation:** Soares-Filho, B. S., Coutinho Cerqueira, G., Lopes Pennachin, C. (2002). *Ecological Modelling* 154(3), 217–235. DOI: 10.1016/s0304-3800(02)00059-5 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** stochastic CA of landscape (deforestation) dynamics; the precursor of the Dinamica EGO platform; validated with pattern-based methods.
- **Code:** platform site https://dinamicaego.com verified (free to use; source availability not confirmed → treat as closed).
- **Reimplementability:** n/a (platform). **Reuse for ca-geo:** medium — the well-known "expander / patcher" allocation functions and weights-of-evidence transition probabilities are documented reference algorithms; detailed assessment belongs to the land-use domain.
- **Relevance to ca-geo:** LND-01, LND-02.

### carneiro2013extensible — An extensible toolbox for modeling nature–society interactions
- **Citation:** Carneiro, T. G. S., Andrade, P. R., Câmara, G., Monteiro, A. M. V., Pereira, R. R. (2013). *Environmental Modelling & Software* 46, 104–117. DOI: 10.1016/j.envsoft.2013.03.002 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** TerraME, an open toolbox (Lua scripting over a C++ core) combining CA, agent-based, system-dynamics and discrete-event paradigms on cellular spaces at multiple scales.
- **Code:** https://github.com/TerraME/terrame (Lua, LGPL-3.0, last push 2023); https://www.terrame.org.
- **Reimplementability:** n/a. **Reuse for ca-geo:** medium — the scripting-language-over-native-core pattern and the multi-paradigm scheduler are relevant; the project looks inactive.

### petzoldt2007simecol — simecol: An Object-Oriented Framework for Ecological Modeling in R
- **Citation:** Petzoldt, T., Rinke, K. (2007). *Journal of Statistical Software* 22(9). DOI: 10.18637/jss.v022.i09 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** R package with an object model (equations, parameters, inputs, solver) for sharing ecological models; reference applications include grid (CA) models.
- **Code:** https://cran.r-project.org/package=simecol (verified).
- **Reimplementability:** n/a. **Reuse for ca-geo:** low-medium — useful idea of a self-describing model object (parameters + init + step + solver) that ca-geo model cards could mirror.

### antunes2021cellpylib — CellPyLib: A Python Library for working with Cellular Automata
- **Citation:** Antunes, L. M. (2021). *Journal of Open Source Software* 6(67), 3608. DOI: 10.21105/joss.03608 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** generic 1D / 2D CA library: discrete or continuous states, adjustable radius, Moore / von Neumann neighbourhoods, totalistic rules, asynchronous and reversible CA.
- **Code:** https://github.com/lantunes/cellpylib (Python, Apache-2.0).
- **Reimplementability:** n/a. **Reuse for ca-geo:** low (not geographic) but a compact API reference for neighbourhood and update-scheme abstractions; permissive licence.

### hewitt2019cellular — A cellular automata land use model for the R software environment (SIMLANDER)
- **Citation:** Hewitt, R. J., Díaz-Pacheco, J., Moya-Gómez, B. (2019). A cellular automata land use model for the R software environment. SocArXiv preprint. DOI: 10.31235/osf.io/suy2c (verified: Crossref, OpenAlex)
- **Access:** OA (preprint).
- **Phenomenon and study area:** land-use change (developed and applied in Spain / Madrid; later used elsewhere).
- **Model:** SIMLANDER — prototype CA land-use model in R; the preprint is a model description and full user documentation with a step-by-step guide. From the related paper (`roodposhti2020towards`) the transition potential combines accessibility (A), suitability (S), neighbourhood (N) and zoning, in the constrained-CA tradition.
- **Inputs:** generic land-use maps, accessibility, suitability, zoning layers.
- **Parameters:** neighbourhood rules calibrated per case.
- **Code:** a public repository could not be located (GitHub search found only third-party projects using SIMLANDER).
- **Validation:** not visible in abstract.
- **Reimplementability:** S1 1 – full description promised but not read; S2 1; S3 2 – R script and demo data on the project site https://simlander.wordpress.com/ (verified in land-use.md); S4 2 – generic open layers; S5 1 → 7, B. Assessed from: abstract + project site.
- **Round 2:** harmonised with land-use.md — S3 1→2, total 7 B (was 6 C). The preprint PDF is still unreadable (font encoding); the full equations are in `roodposhti2020towards`.
- **Browser fit:** constrained land-use CA on 100 m grids is light.
- **Relevance to ca-geo:** LND-01; EU origin; open-source alternative to Metronamica-type models.

### netlogo — NetLogo (software, no DOI)
- **Citation:** NetLogo multi-agent programmable modelling environment, Center for Connected Learning, Northwestern University. Software, no DOI. Site https://ccl.northwestern.edu/netlogo/ and repository https://github.com/NetLogo/NetLogo verified (Scala, GPL-2.0, active 2026).
- **Content:** patch grid + agents with a simple language; extensive model library used in teaching (fire, diffusion, epidemics); GIS extension for raster / vector input.
- **Reimplementability:** n/a. **Reuse for ca-geo:** high for *pedagogy* (UI conventions: sliders, setup / go, live plots); low for code (desktop JVM, GPL).
- **Relevance to ca-geo:** educational positioning; HAZ-01, EPI-01 classroom models.

### Parallel, GPU and web

### guan2010general — A general-purpose parallel raster processing programming library test application using a geographic cellular automata model
- **Citation:** Guan, Q., Clarke, K. C. (2010). *International Journal of Geographical Information Science* 24(5), 695–722. DOI: 10.1080/13658810902984228 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** pRPL, an MPI C++ library for local / focal / zonal / global raster algorithms with quad-tree-based load balancing and data / task parallelism; demonstrated with pSLEUTH.
- **Code:** https://github.com/HPSCIL/pRPL (C++, last push 2017).
- **Reimplementability:** n/a. **Reuse for ca-geo:** medium — the classification of raster operations by scope (local, neighbourhood, regional, global) is a good guide for deciding which ca-geo operators can run in WebGPU shaders vs. on the CPU.

### guan2014prpl — pRPL 2.0: Improving the Parallel Raster Processing Library
- **Citation:** Guan, Q., Zeng, W., Gong, J., Yun, S. (2014). *Transactions in GIS* 18(S1), 25–52. DOI: 10.1111/tgis.12109 (verified: Crossref)
- **Access:** paywall.
- **Content:** second version of pRPL (assessed from metadata only).
- **Reimplementability:** n/a; companion to `guan2010general`.

### li2012gpuca — GPU-CA model for large-scale land-use change simulation
- **Citation:** Li, D., Li, X., Liu, X., Chen, Y., Li, S., Liu, K., Qiao, J., Zheng, Y., Zhang, Y., Lao, C. (2012). *Chinese Science Bulletin* 57(19), 2442–2452. DOI: 10.1007/s11434-012-5085-3 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** maps a land-use CA to the GPU (CUDA) for provincial-scale simulation of Guangdong; reports about 30× speed-up over a sequential CA.
- **Reimplementability:** n/a (acceleration). **Reuse for ca-geo:** evidence that per-cell transition-probability evaluation is embarrassingly parallel; the same mapping applies to WebGPU compute shaders.

### blecic2012parallel — Parallel Simulation of Urban Dynamics on the GPU
- **Citation:** Blečić, I., Cecchini, A., Trunfio, G. A. (2012). In *Computational Science and Its Applications – ICCSA 2012*, LNCS, pp. 492–507. DOI: 10.1007/978-3-642-31075-1_37 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** GPGPU implementation of a constrained urban CA with results on two GPUs.
- **Reimplementability:** n/a. Reference for GPU porting of constrained CA (the demand-allocation step is the non-local part that is hard to parallelise).

### guan2015hybrid — A hybrid parallel cellular automata model for urban growth simulation over GPU/CPU heterogeneous architectures
- **Citation:** Guan, Q., Shi, X., Huang, M., Lai, C. (2015). *International Journal of Geographical Information Science* 30(3), 494–514. DOI: 10.1080/13658816.2015.1039538 (verified: Crossref, OpenAlex; issue year 2016)
- **Access:** paywall.
- **Content:** hybrid MPI + GPU-thread parallel urban growth CA; a 50-year California simulation dropped from about 13,600 s on one CPU to 32 s on 64 GPU/CPU nodes.
- **Reimplementability:** n/a. Shows that Monte Carlo calibration of SLEUTH-like models is the real compute bottleneck — relevant if ca-geo offers in-browser calibration.

### xia2017high — A high-performance cellular automata model for urban simulation based on vectorization and parallel computing technology
- **Citation:** Xia, C., Wang, H., Zhang, A., Zhang, W. (2017). *International Journal of Geographical Information Science* 32(2), 399–424. DOI: 10.1080/13658816.2017.1390118 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** reformulates neighbourhood computation, transition probability and state transition as vector (array) operations; 5 m, 3×3 neighbourhood case went from about 38,000 s to 800 s vectorised and 480 s with additional parallel partitioning.
- **Reimplementability:** n/a. **Reuse for ca-geo:** the "whole-array" formulation suits typed arrays in JS and fragment / compute shaders.

### parise2012swii2 — Swii2, a HTML5/WebGL Application for Cellular Automata Debris Flows Simulation
- **Citation:** Parise, R., D'Ambrosio, D., Spingola, G., Filippone, G., Rongo, R., Trunfio, G. A., Spataro, W. (2012). In *Cellular Automata (ACRI 2012)*, LNCS, pp. 444–453. DOI: 10.1007/978-3-642-33350-7_46 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** web application where the SCIDDICA-k0 debris-flow CA runs on the server and an HTML5 / JavaScript / WebGL client controls the run and shows results in 3D.
- **Reimplementability:** n/a. **Reuse for ca-geo:** the only peer-reviewed browser front-end for a geographic CA found; ca-geo differs by running the CA client-side. Useful precedent for the "related work" section.
- **Relevance to ca-geo:** HAZ-02; web architecture.

### derango2021opencal — OpenCAL system extension and application to the three-dimensional Richards equation for unsaturated flow
- **Citation:** De Rango, A., Furnari, L., Giordano, A., Senatore, A., D'Ambrosio, D., Spataro, W., Straface, S., Mendicino, G. (2021). *Computers & Mathematics with Applications* 81, 133–158. DOI: 10.1016/j.camwa.2020.05.017 (verified: Crossref, OpenAlex)
- **Access:** OA.
- **Content:** OpenCAL, a C/C++ library implementing the Extended Cellular Automata formalism on structured 2D / 3D grids with OpenMP, OpenCL and MPI back-ends; also usable as an explicit finite-difference / finite-volume solver; demonstrated with a 3D Richards-equation model on GPUs and a cluster; includes a quantisation optimisation (skipping inactive cells).
- **Code:** https://github.com/OpenCALTeam/opencal (C, LGPL-3.0, last push 2019).
- **Reimplementability:** n/a. **Reuse for ca-geo:** high as an API reference for macroscopic CA (substates, elementary processes, active-cell optimisation) — the same group's SCIARA / SCIDDICA models are the most likely ca-geo flow references.
- **Relevance to ca-geo:** HYD-01, HAZ-02, HAZ-05; "active cells" optimisation for fronts.

### Calibration and validation methods

### costanza1989model — Model goodness of fit: A multiple resolution procedure
- **Citation:** Costanza, R. (1989). *Ecological Modelling* 47(3–4), 199–215. DOI: 10.1016/0304-3800(89)90001-x (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Method:** goodness of fit between spatial patterns evaluated over windows of increasing size, so that near-misses count as partial agreement; the fit across resolutions summarises pattern similarity.
- **Code:** not found.
- **Reimplementability (as algorithm):** S1 1 – principle clear, exact weighting not seen; S2 1 – window-size weighting parameter; S3 0; S4 2 – any pair of maps; S5 1 → 5, C. Assessed from: TLDR (provisional).
- **Browser fit:** trivial (box filters / summed-area tables).
- **Relevance to ca-geo:** validation component; classic multiresolution check for fire and flood extents.

### hagen2003fuzzy — Fuzzy set approach to assessing similarity of categorical maps
- **Citation:** Hagen, A. (2003). *International Journal of Geographical Information Science* 17(3), 235–249. DOI: 10.1080/13658810210157822 (verified: Crossref, OpenAlex; author listed as Hagen-Zanker in OpenAlex)
- **Access:** OA (publisher PDF link in OpenAlex).
- **Method:** fuzzy comparison of categorical rasters accounting for fuzziness of location (distance-decay neighbourhood) and of category (similarity matrix); yields a per-cell similarity map (0–1) and an overall statistic corrected for expected similarity, the Fuzzy Kappa.
- **Code:** implemented in the Map Comparison Kit (`visser2006map`), free but closed.
- **Reimplementability (as algorithm):** S1 1 – defined in paper, not read in full; S2 1 – distance-decay function and halving distance must be chosen; S3 1; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional). Likely 7–8 after reading the OA full text.
- **Round 2:** full text still not reached (publisher PDF blocked; no repository copy found). Score unchanged. The local-agreement equations of this method are restated in `hagenzanker2009improved` (read in full), so implementation is possible via that paper; the MIT MATLAB code (ahhz/fuzzy_kappa_matlab) implements the 2009 statistic.
- **Browser fit:** neighbourhood search per cell; fine for 1000×1000 grids.
- **Relevance to ca-geo:** validation component (partial credit for near-miss fire / flood fronts).

### hagenzanker2009improved — An improved Fuzzy Kappa statistic that accounts for spatial autocorrelation
- **Citation:** Hagen-Zanker, A. (2009). *International Journal of Geographical Information Science* 23(1), 61–73. DOI: 10.1080/13658810802570317 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Method:** keeps the local fuzzy agreement of `hagen2003fuzzy` but recomputes the expected agreement so that it accounts for spatial autocorrelation (expected value zero for uncorrelated maps), removing negative values and bias against autocorrelated maps.
- **Code:** Map Comparison Kit (closed).
- **Reimplementability (as algorithm):** S1 2; S2 2; S3 2; S4 2; S5 1 → 9, A. Assessed from: full text (author version, University of Surrey repository).
- **Round 2:** re-assessed from full text — S1 1→2, S2 1→2, S3 1→2; total 9 A (was 6 C). The paper gives the complete chain: (1) fuzzy membership of a cell to each category of the other map = maximum over categories of similarity matrix value × distance-decay of the nearest-neighbour distance to that category (nearest distances via a Euclidean distance transform); (2) local agreement = minimum of the two memberships; (3) expected agreement derived for maps that are not cross-correlated but are spatially autocorrelated, from the distribution of nearest-neighbour distances per category; (4) K = (P − E)/(1 − E). The decay function and similarity matrix are analyst choices, but the examples fix them (exponential decay, halving distance 2 cells, truncated at radius 4 or untruncated). Validation: 600 comparisons of independent synthetic maps give a mean improved Fuzzy Kappa within ±0.03 of zero, and the classic synthetic map pair of Hagen (2003) is recomputed (values in figures, hence S5 1). Code: the paper says C++ is available on request; the author's account hosts an MIT-licensed MATLAB implementation, https://github.com/ahhz/fuzzy_kappa_matlab (HTTP 200).
- **Relevance to ca-geo:** preferred over the 2003 version if Fuzzy Kappa is implemented. Browser fit: one distance transform per category plus a histogram — fine for 1000×1000 grids.

### visser2006map — The Map Comparison Kit
- **Citation:** Visser, H., de Nijs, T. (2006). *Environmental Modelling & Software* 21(3), 346–358. DOI: 10.1016/j.envsoft.2004.11.013 (verified: Crossref)
- **Access:** paywall.
- **Content:** software for raster map comparison: kappa variants, fuzzy set comparison, hierarchical fuzzy pattern matching, moving-window landscape structure; batch tools for Monte Carlo and calibration; version 3.2.2 adds Kappa Simulation (from the tool website http://mck.riks.nl, verified).
- **Reimplementability:** n/a. **Reuse for ca-geo:** high as a *checklist and oracle* — its outputs can validate a JS implementation of the same metrics; Windows binary only.

### pontius2007comparing — Comparing the input, output, and validation maps for several models of land change
- **Citation:** Pontius, R. G., Boersma, W., Castella, J.-C., Clarke, K., de Nijs, T., Dietzel, C., et al. (2007). *The Annals of Regional Science* 42(1), 11–37. DOI: 10.1007/s00168-007-0138-2 (verified: Crossref, OpenAlex; issue year 2008)
- **Access:** OA via Wageningen repository record (no PDF link confirmed).
- **Method:** compares the initial reference map, the later reference map and the simulated later map for 13 applications of 9 models at multiple resolutions; summarises each with the *null resolution* (resolution at which the model beats a no-change null model) and the *figure of merit* (correctly predicted change relative to the union of observed and predicted change). For 12 of 13 applications error exceeded correctly predicted change at native resolution.
- **Code:** not found.
- **Reimplementability (as algorithm):** S1 1 – metric definitions not read in full; S2 2 – parameter-free; S3 0; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** the "three-map" protocol and the null model are essential for honest demo validation (LND-01, ECO-01, HAZ-01).
- **Round 2:** the WUR repository record returned HTTP 503 (curl and WebFetch); no other OA copy found. Score unchanged. `hagenzanker2008neutral` (read) offers fully specified neutral models that complement the no-change null model used here.

### pontius2011death — Death to Kappa: birth of quantity disagreement and allocation disagreement for accuracy assessment
- **Citation:** Pontius, R. G., Millones, M. (2011). *International Journal of Remote Sensing* 32(15), 4407–4429. DOI: 10.1080/01431161.2011.552923 (verified: Crossref, OpenAlex)
- **Access:** OA (author manuscript at Clark University repository; automated fetch blocked).
- **Method:** analyses five kappa indices and recommends replacing them by two components of the cross-tabulation matrix: quantity disagreement and allocation disagreement; the abstract states that the paper shows how to compute both with examples from the literature.
- **Code:** R package diffeR by the first author (metrics of difference for pairs of maps at original and multiple resolutions): https://cran.r-project.org/package=diffeR and https://github.com/amsantac/diffeR (both verified). Function-level mapping not checked.
- **Reimplementability (as algorithm):** S1 2 – closed-form, computation explicitly shown per abstract; S2 2 – parameter-free; S3 2; S4 2; S5 1 – worked examples not yet read → 9, A. Assessed from: abstract (provisional).
- **Browser fit:** trivial (one pass over two rasters).
- **Relevance to ca-geo:** first metric to implement in the shared validation component.
- **Round 2:** the Clark Digital Commons PDF returned HTTP 403 (also via WebFetch), so the paper is still unread; score unchanged (provisional). The diffeR source on GitHub was inspected instead: `diffTablej` / `differenceMR` compute per-category omission, commission and agreement and split the difference into quantity, **exchange** and **shift** components (overall values halved for double counting), at the original and at successively coarser resolutions (factor 2). That newer three-way split is defined in `pontius2014quantity` (added in round 2); allocation disagreement corresponds to the non-quantity part.

### pontius2011comparison — Comparison of Three Maps at Multiple Resolutions: A Case Study of Land Change Simulation in Cho Don District, Vietnam
- **Citation:** Pontius, R. G., Peethambaram, S., Castella, J.-C. (2011). *Annals of the Association of American Geographers* 101(1), 45–62. DOI: 10.1080/00045608.2010.517742 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Method:** three-map comparison (reference t1, reference t2, simulation t2) at native and nested coarser resolutions; a three-dimensional table splits the area into agreement, quantity disagreement, allocation disagreement within coarse squares and allocation disagreement among coarse squares. Example: SAMBA model, 32 m pixels.
- **Code:** diffeR (as above) covers multiple-resolution difference metrics.
- **Reimplementability (as algorithm):** S1 1 – procedure clear from abstract, formulas not read; S2 2; S3 2; S4 2; S5 1 → 8, B. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** multiresolution view of disagreement — shows at what scale a demo model is "right".
- **Round 2:** still paywalled (Semantic Scholar: CLOSED); unchanged. diffeR's `differenceMR` implements the multiple-resolution part (aggregation by factor 2 up to the full extent), confirming S3 2.

### vanvliet2011revisiting — Revisiting Kappa to account for change in the accuracy assessment of land-use change models
- **Citation:** van Vliet, J., Bregt, A. K., Hagen-Zanker, A. (2011). *Ecological Modelling* 222(8), 1367–1375. DOI: 10.1016/j.ecolmodel.2011.01.017 (verified: Crossref, OpenAlex)
- **Access:** OA via Wageningen repository record.
- **Method:** Kappa Simulation (KSimulation): same form as kappa, but the expected agreement is computed from random allocation of *class transitions relative to the initial map*, so a model is not rewarded for persistence when little change occurs.
- **Code:** Map Comparison Kit 3.2.2 (closed).
- **Reimplementability (as algorithm):** S1 1 – exact formula not read; S2 2; S3 1; S4 2; S5 1 → 7, B. Assessed from: abstract + repository summary (provisional).
- **Relevance to ca-geo:** second validation metric; essential for slow processes (land use, succession) where persistence dominates.

### varga2019intensity — Intensity Analysis and the Figure of Merit's components for assessment of a Cellular Automata – Markov simulation model
- **Citation:** Varga, O. G., Pontius, R. G., Singh, S. K., Szabó, S. (2019). *Ecological Indicators* 101, 933–942. DOI: 10.1016/j.ecolind.2019.01.057 (verified: Crossref, OpenAlex)
- **Access:** OA (author manuscript via ScienceDirect).
- **Method:** compares reference change in the calibration interval, simulated change in the validation interval and reference change in the validation interval, using Intensity Analysis (interval, category, transition levels) and the four Figure of Merit components (misses, hits, wrong hits, false alarms); applied to a CA–Markov model in north-east Hungary (five classes, 2000–2006 calibration, 2006–2012 validation). More error came from the CA allocation than from the Markov quantities.
- **Code:** not verified.
- **Reimplementability (as algorithm):** S1 1; S2 2; S3 0; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** EU (Hungary) example; FoM components are simple to display in a demo.
- **Round 2:** the ScienceDirect author manuscript returned HTTP 403; unchanged.

### roodposhti2020towards — Towards automatic calibration of neighbourhood influence in cellular automata land-use models
- **Citation:** Roodposhti, M. S., Hewitt, R. J., Bryan, B. A. (2020). *Computers, Environment and Urban Systems* 79, 101416. DOI: 10.1016/j.compenvurbsys.2019.101416 (verified: Crossref, OpenAlex)
- **Access:** OA (full text blocked to automated fetch).
- **Phenomenon and study area:** urban growth of Ahvaz, Iran, 2000–2015.
- **Model:** SIMLANDER CA (`hewitt2019cellular`) with accessibility, suitability and neighbourhood factors; automatic rule detection (ARD) calibrates neighbourhood rules either by random sampling of parameter space or by stepwise grid search; rule-sets ranked by cross-comparison of multiple goodness-of-fit metrics.
- **Inputs:** open data only (as stated).
- **Parameters:** calibrated by the ARD procedure.
- **Code:** ARD scripts as supplementary material (R / RStudio) — not verified.
- **Validation:** multiple metrics vs. reference map; grid search slightly better but five times slower.
- **Reimplementability:** S1 2; S2 2; S3 2; S4 2; S5 2 → 10, A. Assessed from: full text (as assessed in land-use.md).
- **Round 2:** harmonised with the full-text assessment in land-use.md (accepted manuscript, Deakin repository): every equation and parameter value is printed, the SIMLANDER base model is downloadable, inputs are open global data and quantitative metrics are tabulated → 10 A (was 6 C, provisional).
- **Browser fit:** random-sampling calibration with Web Workers is feasible for small grids; good interactive "calibrate me" demo.
- **Relevance to ca-geo:** calibration module; LND-01.

### Sensitivity and uncertainty

### menard2005exploration — Exploration of Spatial Scale Sensitivity in Geographic Cellular Automata
- **Citation:** Ménard, A., Marceau, D. J. (2005). *Environment and Planning B: Planning and Design* 32(5), 693–714. DOI: 10.1068/b31163 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** stochastic land-cover CA (Maskoutains region, Quebec) with rules from two Landsat images (30 m), resampled to 100–1000 m and run with six neighbourhoods (Moore, von Neumann, circular radii 2–5): 30 scale scenarios; cell size and neighbourhood strongly and non-linearly affect both area and pattern.
- **Reimplementability:** n/a (method study). Strong argument for ca-geo to expose cell size and neighbourhood as user controls and to warn about scale effects.

### kocabas2006assessing — Assessing cellular automata model behaviour using a sensitivity analysis approach
- **Citation:** Kocabas, V., Dragićević, S. (2006). *Computers, Environment and Urban Systems* 30(6), 921–953. DOI: 10.1016/j.compenvurbsys.2006.01.001 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** sensitivity analysis of a GIS-based urban CA to neighbourhood size and type; both have a significant influence on output.
- **Reimplementability:** n/a. Same message as `menard2005exploration`; template for a built-in "neighbourhood sweep" experiment.

### yeh2006errors — Errors and uncertainties in urban cellular automata
- **Citation:** Yeh, A. G.-O., Li, X. (2006). *Computers, Environment and Urban Systems* 30(1), 10–28. DOI: 10.1016/j.compenvurbsys.2004.05.007 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** classifies error sources in urban CA (data errors propagated through iterations, model structure, stochastic transitions) and notes characteristics unique to CA compared with static GIS models.
- **Reimplementability:** n/a. Supports ensemble runs and input-perturbation experiments in ca-geo.

### hewitt2017stable — Stable models for metastable systems? Lessons from sensitivity analysis of a Cellular Automata urban land use model
- **Citation:** Hewitt, R., Díaz-Pacheco, J. (2017). *Computers, Environment and Urban Systems* 62, 113–124. DOI: 10.1016/j.compenvurbsys.2016.10.011 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Content:** sensitivity analysis of a constrained urban land-use CA (Madrid context); argues that calibration presupposes metastability, which conflicts with simulating genuinely complex change; output variability may indicate how suitable a model is.
- **Reimplementability:** n/a. EU case; conceptual caution for the demo narrative ("a calibrated model is not a forecast").

### Round 2 additions

### hagenzanker2008neutral — Neutral models of landscape change as benchmarks in the assessment of model performance (round 2)
- **Citation:** Hagen-Zanker, A., Lajoie, G. (2008). Neutral models of landscape change as benchmarks in the assessment of model performance. *Landscape and Urban Planning*, 86(3–4), 284–296. DOI: 10.1016/j.landurbplan.2008.04.002 (verified: Crossref)
- **Access:** OA (green, University of Surrey repository; read in full).
- **Method:** a model's goodness of fit is judged relative to "neutral models of landscape change" that reach the same class composition as the simulated map while changing as little as possible: (1) *random constraint match* converts randomly chosen cells of over-represented classes (speckled result); (2) *growing clusters* converts cells along edges between over- and under-represented classes (blobby result). Pseudocode for both is in the appendix. Criteria (presence agreement, patch size, fractal dimension, wavelet-based structure) are evaluated at multiple scales (1×1 to 128×128) and normalised against the neutral models. Application: the White–Engelen constrained CA for La Réunion; the CA beats the neutral models on location only at coarse scales but on pattern structure at almost all scales. The paper also restates the constrained-CA potential equation (random term, neighbourhood effect, suitability, accessibility, zoning).
- **Code:** not found.
- **Reimplementability (as algorithm):** S1 2 – pseudocode; S2 2 – parameter-free; S3 0; S4 2 – any pair of categorical maps; S5 1 – tables for a non-open case → 7, B. Assessed from: full text.
- **Browser fit:** both neutral models are single passes over the grid; trivial.
- **Relevance to ca-geo:** validation component and **ensemble / stochastic CA validation**: a demo can show "our CA vs. a random allocation vs. a growing-clusters allocation" with the same amount of change — a clear, honest benchmark for LND-01, ECO-02 and fire scars.

### pontius2014quantity — Quantity, exchange, and shift components of difference in a square contingency table (round 2)
- **Citation:** Pontius, R. G., Santacruz, A. (2014). Quantity, exchange, and shift components of difference in a square contingency table. *International Journal of Remote Sensing*, 35(21), 7543–7554. DOI: 10.1080/2150704x.2014.969814 (verified: Crossref)
- **Access:** paywall.
- **Method:** splits total difference between two categorical maps into quantity, exchange and shift components (successor of the quantity / allocation split of `pontius2011death`). Definitions read only from the diffeR source (functions `quantityDj`, `exchangeDj`, `shiftDj`, overall values halved for double counting); paper not read.
- **Code:** R package diffeR (https://github.com/amsantac/diffeR, verified; source inspected).
- **Reimplementability (as algorithm):** S1 1 – paper not read; S2 2; S3 2; S4 2; S5 1 → 8, B. Assessed from: metadata + diffeR source (provisional).
- **Relevance to ca-geo:** the current form of the Pontius metrics; port diffeR's functions to JS and test against diffeR outputs.

### vanvliet2013fuzzy — A fuzzy set approach to assess the predictive accuracy of land use simulations (round 2)
- **Citation:** van Vliet, J., Hagen-Zanker, A., Hurkens, J., van Delden, H. (2013). A fuzzy set approach to assess the predictive accuracy of land use simulations. *Ecological Modelling*, 261–262, 32–42. DOI: 10.1016/j.ecolmodel.2013.03.019 (verified: Crossref)
- **Access:** paywall (abstract not available in Crossref or Semantic Scholar).
- **Method:** per the title, a fuzzy-set accuracy measure for land-use simulations; details not checked.
- **Code:** not verified (MCK lineage likely, unconfirmed).
- **Reimplementability (as algorithm):** S1 1; S2 1; S3 0; S4 2; S5 1 → 5, C. Assessed from: metadata only (provisional).
- **Relevance to ca-geo:** candidate fuzzy metric for land-use validation; read before finalising the metric set.

### brown2005path — Path dependence and the validation of agent-based spatial models of land use (round 2)
- **Citation:** Brown, D. G., Page, S., Riolo, R., Zellner, M., Rand, W. (2005). *International Journal of Geographical Information Science*, 19(2), 153–174. DOI: 10.1080/13658810410001713399 (verified: Crossref)
- **Access:** listed as bronze OA (publisher PDF); abstract elided in metadata; automated access not attempted further.
- **Content:** per the title, validation of path-dependent (stochastic) agent-based land-use models; content not checked (provisional, read in round 3).
- **Reimplementability:** n/a (method). Assessed from: metadata only.
- **Relevance to ca-geo:** argument and design for **ensemble validation of stochastic CA** (probability-of-change maps from many runs, comparison with one observed history).

### garcia2011analysis — An analysis of the effect of the stochastic component of urban cellular automata models (round 2)
- **Citation:** García, A. M., Santé, I., Crecente, R., Miranda, D. (2011). *Computers, Environment and Urban Systems*, 35(4), 289–296. DOI: 10.1016/j.compenvurbsys.2010.11.001 (verified: Crossref)
- **Access:** paywall (abstract elided).
- **Content:** analysis of how the random term in urban CA affects results (title; content not checked).
- **Reimplementability:** n/a (method). Assessed from: metadata only.
- **Relevance to ca-geo:** together with `yeh2006errors` and `hewitt2017stable`, the basis for exposing the stochastic-term strength (e.g. the Weibull α of SIMLANDER) as a user control and showing ensemble spread.

### xia2025pytorchfire — PyTorchFire: A GPU-accelerated wildfire simulator with Differentiable Cellular Automata (round 2)
- **Citation:** Xia, Z., Cheng, S. (2025). *Environmental Modelling & Software*, 188, 106401. DOI: 10.1016/j.envsoft.2025.106401 (verified: Crossref; key already in references.bib from `fire`)
- **Access:** OA (CC BY; arXiv 2502.18738, read).
- **Model:** three-state wildfire CA (burnable, burning, burned) building on Alexandridis et al.: a burnable cell ignites with some probability if at least one neighbour burns; the probability combines a base propagation probability with scaling factors for wind velocity, wind direction and slope to each of the 8 neighbours (plus vegetation / density inputs); a burning cell keeps burning with probability p_continue, a burned cell stays burned. Everything is written as tensor operations on the GPU. The stochastic update is made differentiable so that the parameters can be calibrated by gradient descent (AdamW) against observed burned areas, with clamping of parameters.
- **Inputs:** vegetation, density, wind speed and direction, slope tensors, initial ignition; dataset on Mendeley Data (DOI 10.17632/nx2wsksp9k.1, from the README).
- **Code:** https://github.com/xiazeyu/PyTorchFire (MIT, active 2026-09; Zenodo DOI 10.5281/zenodo.13132218).
- **Validation:** Jaccard index and burned-area match over time; 32 simulated events at three Californian sites and the Bear (2020) and Pier (2017) fires; millisecond-level step times on GPU.
- **Reimplementability:** S1 2; S2 2; S3 2; S4 2; S5 2 → 10, A. Assessed from: full text (arXiv; skimmed sections on model, calibration and metrics).
- **Browser fit:** the forward CA is a direct WebGPU / WebGL target; gradient-based calibration in the browser would need a small autodiff layer (feasible with ensembles of a few runs).
- **Relevance to ca-geo:** cross-cutting reference for **GPU CA + in-browser calibration** (detailed scoring belongs to `fire`). Shows a route for fitting parameters interactively instead of brute-force Monte Carlo.

### dejong2021environmental — An environmental modelling framework based on asynchronous many-tasks: Scalability and usability (round 2)
- **Citation:** de Jong, K., Panja, D., van Kreveld, M., Karssenberg, D. (2021). *Environmental Modelling & Software*, 139, 104998. DOI: 10.1016/j.envsoft.2021.104998 (verified: Crossref)
- **Access:** OA (CC BY).
- **Content:** LUE, the successor framework to PCRaster from the same group: map-algebra operations implemented on an asynchronous many-task runtime for scalability from laptop to cluster (assessed from metadata and repository; paper not read).
- **Code:** https://github.com/computationalgeography/lue (MIT, active 2026-09).
- **Reimplementability:** n/a (framework). **Reuse for ca-geo:** medium — MIT-licensed operator set (local / focal / zonal / flow accumulation) and the idea of composing operations into a task graph are relevant to scheduling WebGPU passes; closes the round-1 gap "LUE only as EGU abstracts".

### liu2009developing — Developing a web-based cellular automata model for urban growth simulation (round 2)
- **Citation:** Liu, Y., He, J. (2009). *SPIE Proceedings*, 7492, 74925C. DOI: 10.1117/12.838657 (verified: Crossref)
- **Access:** paywall; no abstract in metadata.
- **Content:** a web-based urban growth CA (2009, so very likely server-side computation with a web front-end; not checked).
- **Reimplementability:** n/a. Assessed from: metadata only.
- **Relevance to ca-geo:** related-work item for web CA, alongside `parise2012swii2`.

### douvinet2023postfire — Post-Fire Debris Flow Susceptibility Assessment Tracking the "Cauliflower Effect" (round 2)
- **Citation:** Douvinet, J. (2023). In *Flood Risk in a Climate Change Context – Exploring Current and Emerging Drivers*, IntechOpen. DOI: 10.5772/intechopen.107510 (verified: Crossref)
- **Access:** OA (IntechOpen).
- **Phenomenon and study area:** runoff concentration in five burned catchments above Montecito (California) before the 2018 post-fire debris flows.
- **Model:** the runoff-concentration CA RuiCells, previously used for flash-flood susceptibility (reported 43 % success rate in sedimentary areas), applied to burned catchments to relate catchment shape to concentration of surface flow (abstract).
- **Code:** RuiCells is proprietary (©).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract.
- **Relevance to ca-geo:** the only verified CA paper that explicitly addresses a **fire → runoff → debris-flow chain** (longlist chain L1), even if only as susceptibility, not as dynamic coupling.

### Frameworks — round 2 check (no score changes)
Repositories re-checked via the GitHub API on 2026-10-12: Landlab (MIT, last push 2026-10-09; CellLab-CTS inside), PCRaster (GPL-3.0, 2026-10-05), OpenCAL (LGPL-3.0, last push 2019-11 — inactive, use as design reference only), LUE (MIT, 2026-09). No peer-reviewed JavaScript / WebGL / WebGPU **geographic** CA framework was found; recent hobby repositories show the stack is feasible: `miguelgarglez/yesca` (TypeScript, MIT, GPU wildfire on real terrain and live wind) and `rkottomt/deluge-flood-sim` (TypeScript, MIT, WebGPU shallow-water flood on USGS terrain) — both verified (HTTP 200), no publication, not reviewed in depth.

## Most reimplementable (top picks)

For this cross-cutting domain the "top picks" are reusable algorithms and reference frameworks rather
than phenomenon models:

1. `pontius2011death` (A, 9) — quantity and allocation disagreement: closed-form, parameter-free, open R reference (diffeR). First metric for the ca-geo validation component.
2. `pontius2011comparison` (B, 8) — three-map, multiple-resolution comparison; same open reference code; shows the scale at which a model is right.
3. `vanvliet2011revisiting` (B, 7) — Kappa Simulation; corrects kappa for persistence; MCK can serve as a test oracle.
4. `hagenzanker2009improved` (A, 9; r2, full text) — improved Fuzzy Kappa with complete equations and an MIT MATLAB reference implementation; partial credit for near-miss fronts (fire, flood). `hagen2003fuzzy` (C, 6) is its predecessor.
5. `roodposhti2020towards` (A, 10; harmonised r2) — fully specified automatic calibration of neighbourhood rules; basis for a "calibrate me" demo.
6. `xia2025pytorchfire` (A, 10; r2, key from `fire`) — GPU CA with gradient-based calibration; template for fast in-browser fitting.
7. `pontius2014quantity` (B, 8; r2) — quantity / exchange / shift, as implemented in diffeR (test oracle).
8. `hagenzanker2008neutral` (B, 7; r2, full text) — neutral models of landscape change as benchmarks; parameter-free, pseudocode given.
9. `pontius2007comparing` + `varga2019intensity` (C, 6) — figure of merit, its components and the null model; simple to compute and explain in a demo.

Reference frameworks with the highest reuse value for the JS core (not scored):
`hobley2017creative` / `tucker2016celllab` (Landlab, MIT, component coupling and asynchronous CA),
`karssenberg2010software` (PCRaster operator set and Monte Carlo template),
`derango2021opencal` (macroscopic CA API, active-cell optimisation),
`digregorio1999empirical` + `avolio2012theorem` (MAD outflow kernel shared by all flow models),
`dejong2021environmental` (LUE, MIT; r2).

## Gaps and unverified leads

- **No peer-reviewed, fully client-side (WebGL / WebGPU / JavaScript) geographic CA framework was
  found.** Swii2 (`parise2012swii2`) runs the CA on the server. A 2014 thesis on WebGL apps for
  SCIDDICA / SCIARA / ABBAMPAU and a recent (2026) web platform for wildfire CA from AUEB were
  seen only as search snippets — not verified (round 2). GitHub has generic, non-geographic WebGL /
  WebGPU CA engines (e.g. `soogbet/utomata`, `WonderYard/vivarium`, `dawidgorny/webgpu-cca`) — useful
  only as shader-pattern references; repositories seen via GitHub API, not reviewed. This gap is a
  positive novelty argument for ca-geo.
- **CA-based multi-hazard coupling:** nothing verified. Non-CA multi-hazard chain models were seen
  (NHESS 2022 process-chain model; iCRESTRIGRS) — not CA, not included. Round 2: search
  "post-fire debris flow cellular automata", "coupled cellular automata hazard chain".
- **Recent all-domain review of environmental / hazard CA** (2020+): not found; the
  natural-computing review on arXiv (1808.00260) and Wittmann's "cellular systems" paper were seen
  only as snippets.
- **Pontius (2000)** "Quantification error versus location error …" and **Pontius (2002)**
  multiple-resolution PERS papers: not found in Crossref (PERS DOIs before ~2005 are sparse);
  check in OpenAlex when the search budget resets.
- **Educational CA tools:** no peer-reviewed evaluation of a geography CA teaching tool was found.
  Leads: a 2002 GSA abstract on a web-based CA landform-evolution teaching model; SPEEDSim
  (iPad app); Crooks (2017) encyclopedia entry (verified DOI 10.1002/9781118786352.wbieg0578, not
  included).
- **Not included but verified (round-2 candidates):** White & Engelen (2000) constrained CA
  (10.1016/s0198-9715(00)00012-0) and Wagner (1997) CA and GIS (10.1068/b240219) — overlap with
  land-use; Straatman, White & Engelen (2004) automatic calibration (10.1016/s0198-9715(02)00068-6);
  Li et al. (2010) parallel urban CA with load balancing (10.1080/13658810903107464);
  García-Álvarez & Camacho Olmedo (2021) sensitivity to input resampling
  (10.1080/03736245.2021.1872413); van Vliet et al. (2013) fuzzy accuracy of land-use simulations
  (10.1016/j.ecolmodel.2013.03.019); Verstegen et al. (2014) Bayesian data assimilation for a
  land-use CA (10.1016/j.envsoft.2013.11.009); Pontius et al. (2004) validation techniques
  (10.1016/j.ecolmodel.2004.05.010); Trunfio (2004) hexagonal wildfire CA
  (10.1007/978-3-540-30479-1_40) — belongs to `fire`; Guidolin et al. (2016) WCA2D
  (10.1016/j.envsoft.2016.07.008) — belongs to `hyd`.
- **Other software leads (URLs verified, no paper assessed):** mcPLUS parallel PLUS model
  (https://github.com/HPSCIL/mcPLUS); lulcc R package (https://github.com/simonmoulds/lulcc);
  landscapemetrics R package for pattern-based validation
  (https://github.com/r-spatialecology/landscapemetrics); GRASS GIS r.futures
  (https://grass.osgeo.org/grass-stable/manuals/addons/r.futures.html); LUE framework (EGU
  abstracts only).
- **Full-text reads pending** (all OA, blocked to automated fetch or not attempted): Hagen (2003),
  Pontius & Millones (2011), van Vliet et al. (2011), Varga et al. (2019), Roodposhti et al. (2020),
  Geographic Automata Tool (2024). Reading them would likely raise S1 / S5 for the metric entries.
- **Round 2 status of the gaps above:**
  - Client-side geographic CA: still no peer-reviewed framework or paper (Crossref, web, GitHub). Only hobby repositories (yesca, deluge-flood-sim; see "Frameworks — round 2 check") and the server-side Swii2 / web CA of Liu & He (2009). The novelty argument for ca-geo stands. The 2014 WebGL SCIDDICA / SCIARA thesis and the 2026 AUEB wildfire platform were not found again.
  - Multi-hazard coupling: no coupled CA framework verified. Closest items: `douvinet2023postfire` (fire → runoff susceptibility, closed CA), the SCIDDICA / LLUNPIY macroscopic-CA lineage (lahars including ice melt; Lupiano et al. 2017, *Natural Computing*, DOI 10.1007/s11047-017-9632-3, verified, belongs to `geo`), and Yu & Chang (2024) coupled GPU dynamic-wave flow + solute transport CA (NHESS preprint, DOI 10.5194/nhess-2024-131, verified, belongs to `hyd`). Coupling in ca-geo will have to follow framework patterns (Landlab components, PCRaster scripts) rather than a CA-specific precedent.
  - Validation of stochastic CA: now covered by `hagenzanker2008neutral` (read), `brown2005path`, `garcia2011analysis`, `vanvliet2013fuzzy` (metadata only — read in round 3), plus round-1 `yeh2006errors`, `hewitt2017stable`.
  - Still unread although OA-listed: Pontius & Millones 2011 (Clark, 403), Pontius et al. 2007 (WUR, 503), Varga et al. 2019 (Elsevier AM, 403), Hagen 2003 (T&F), Geographic Automata Tool 2024 (MDPI 403). Manual reading needed.
  - Educational tools: no peer-reviewed evaluation found; Hasbani et al. (2011), interactive creation of land-use CA rules, InTech chapter, DOI 10.5772/16073 (seen in Crossref results; not assessed).
  - Pontius (2000, 2002) PERS papers: not re-searched (OpenAlex still blocked).
- **Overlaps:** SLEUTH, DINAMICA, SIMLANDER and constrained CA → `lu`; MAD / SCIARA / SCIDDICA /
  OpenCAL → `geo` and `hyd`; Landlab CellLab-CTS examples → `geo`, `eco`.

## Round 2 changes

| Key | Old score / class | New score / class | Reason |
|---|---|---|---|
| hagenzanker2009improved | 6, C (abstract) | 9, A (full text) | complete equations and worked examples read; MIT MATLAB implementation by the author verified |
| roodposhti2020towards | 6, C (abstract) | 10, A (full text) | harmonised with the full-text assessment in land-use.md |
| hewitt2019cellular | 6, C | 7, B | harmonised with land-use.md (code and demo data verified on the project site) |
| hagen2003fuzzy | 6, C | 6, C | still unread; equations available via hagenzanker2009improved |
| pontius2011death | 9, A (provisional) | 9, A (provisional) | still unread (403); diffeR source inspected, consistent |
| pontius2011comparison | 8, B | 8, B | still paywalled; diffeR multiresolution function confirmed |
| pontius2007comparing, varga2019intensity | 6, C | 6, C | repository / manuscript access failed (503 / 403) |
| new: 9 rows | – | see catalogue (r2) | A 1 (PyTorchFire, shared key), B 2, C 2, n/a 4 |

## New phenomena candidates (round 2)

No new geography-bound phenomena came up in the cross-cutting searches beyond those recorded in
land-use.md (deforestation, residential segregation, PV adoption diffusion, population-density
redistribution). The fire → runoff → debris-flow item (`douvinet2023postfire`) is a chain of
existing longlist items (L1), not a new phenomenon.

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| – | – | – | – | – | see land-use.md |
