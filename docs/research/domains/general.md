# Cross-cutting: reviews, frameworks, methods — literature survey

Survey round: 1 (breadth-first), date 2026-10-12. Scoring per ../reimplementability-criteria.md.

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
| hagenzanker2009improved | 2009 | Improved Fuzzy Kappa | validation metric | as above + autocorrelation-aware expectation | 1 1 1 2 1 | 6 | C | MCK (closed) | paywall | abstract (provisional) |
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
| hewitt2019cellular | 2019 | SIMLANDER (R) | land-use change | raster / neighbourhood rules + suitability + accessibility + zoning / stoch. | 1 1 1 2 1 | 6 | C | not located | OA (preprint) | abstract (provisional) |
| tong2019review | 2019 | Review of CA assessment methods | review | – | n/a | n/a | n/a | – | paywall | abstract |
| varga2019intensity | 2019 | Intensity Analysis + FoM components | validation metric | – | 1 2 0 2 1 | 6 | C | not verified | OA (author manuscript) | abstract (provisional) |
| barnhart2020landlab | 2020 | Landlab v2.0 | modelling framework | as Landlab | n/a | n/a | n/a | yes (GitHub, MIT) | OA | metadata |
| roodposhti2020towards | 2020 | Automatic calibration of neighbourhood rules | calibration procedure | SIMLANDER CA | 1 1 1 2 1 | 6 | C | supplementary scripts (not verified) | OA | abstract (provisional) |
| derango2021opencal | 2021 | OpenCAL extension | parallel CA library | 2D/3D structured grids, OpenMP/OpenCL/MPI | n/a | n/a | n/a | yes (GitHub, LGPL-3.0) | OA | abstract |
| antunes2021cellpylib | 2021 | CellPyLib | generic CA library | 1D/2D / Moore, von Neumann / discrete+continuous | n/a | n/a | n/a | yes (GitHub, Apache-2.0) | OA | abstract |
| addae2022modelling | 2022 | Spherical CA for global urban change | urban land use (global) | geodesic grid on sphere | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only (provisional) |
| vanduynhoven2024geographic | 2024 | Geographic Automata Tool (ArcGIS Pro) | GIS-embedded CA framework | binary / multi-class CA | n/a | n/a | n/a | not verified | OA | abstract |
| netlogo | – | NetLogo | agent / patch modelling environment | patch grid, user rules | n/a | n/a | n/a | yes (GitHub, GPL-2.0) | software, no DOI | website + repository |

Total: 50 verified publications + 1 software item without DOI (NetLogo).
Classes: A 1, B 2, C 10, D 1, n/a 36 (+ NetLogo, n/a).

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
- **Reimplementability:** S1 1 – full description promised but not read; S2 1; S3 1 – code exists, location not verified; S4 2 – generic open layers; S5 1 → 6, C. Assessed from: abstract (provisional).
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
- **Browser fit:** neighbourhood search per cell; fine for 1000×1000 grids.
- **Relevance to ca-geo:** validation component (partial credit for near-miss fire / flood fronts).

### hagenzanker2009improved — An improved Fuzzy Kappa statistic that accounts for spatial autocorrelation
- **Citation:** Hagen-Zanker, A. (2009). *International Journal of Geographical Information Science* 23(1), 61–73. DOI: 10.1080/13658810802570317 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Method:** keeps the local fuzzy agreement of `hagen2003fuzzy` but recomputes the expected agreement so that it accounts for spatial autocorrelation (expected value zero for uncorrelated maps), removing negative values and bias against autocorrelated maps.
- **Code:** Map Comparison Kit (closed).
- **Reimplementability (as algorithm):** S1 1; S2 1; S3 1; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** preferred over the 2003 version if Fuzzy Kappa is implemented.

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

### pontius2011death — Death to Kappa: birth of quantity disagreement and allocation disagreement for accuracy assessment
- **Citation:** Pontius, R. G., Millones, M. (2011). *International Journal of Remote Sensing* 32(15), 4407–4429. DOI: 10.1080/01431161.2011.552923 (verified: Crossref, OpenAlex)
- **Access:** OA (author manuscript at Clark University repository; automated fetch blocked).
- **Method:** analyses five kappa indices and recommends replacing them by two components of the cross-tabulation matrix: quantity disagreement and allocation disagreement; the abstract states that the paper shows how to compute both with examples from the literature.
- **Code:** R package diffeR by the first author (metrics of difference for pairs of maps at original and multiple resolutions): https://cran.r-project.org/package=diffeR and https://github.com/amsantac/diffeR (both verified). Function-level mapping not checked.
- **Reimplementability (as algorithm):** S1 2 – closed-form, computation explicitly shown per abstract; S2 2 – parameter-free; S3 2; S4 2; S5 1 – worked examples not yet read → 9, A. Assessed from: abstract (provisional).
- **Browser fit:** trivial (one pass over two rasters).
- **Relevance to ca-geo:** first metric to implement in the shared validation component.

### pontius2011comparison — Comparison of Three Maps at Multiple Resolutions: A Case Study of Land Change Simulation in Cho Don District, Vietnam
- **Citation:** Pontius, R. G., Peethambaram, S., Castella, J.-C. (2011). *Annals of the Association of American Geographers* 101(1), 45–62. DOI: 10.1080/00045608.2010.517742 (verified: Crossref, OpenAlex)
- **Access:** paywall.
- **Method:** three-map comparison (reference t1, reference t2, simulation t2) at native and nested coarser resolutions; a three-dimensional table splits the area into agreement, quantity disagreement, allocation disagreement within coarse squares and allocation disagreement among coarse squares. Example: SAMBA model, 32 m pixels.
- **Code:** diffeR (as above) covers multiple-resolution difference metrics.
- **Reimplementability (as algorithm):** S1 1 – procedure clear from abstract, formulas not read; S2 2; S3 2; S4 2; S5 1 → 8, B. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** multiresolution view of disagreement — shows at what scale a demo model is "right".

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

### roodposhti2020towards — Towards automatic calibration of neighbourhood influence in cellular automata land-use models
- **Citation:** Roodposhti, M. S., Hewitt, R. J., Bryan, B. A. (2020). *Computers, Environment and Urban Systems* 79, 101416. DOI: 10.1016/j.compenvurbsys.2019.101416 (verified: Crossref, OpenAlex)
- **Access:** OA (full text blocked to automated fetch).
- **Phenomenon and study area:** urban growth of Ahvaz, Iran, 2000–2015.
- **Model:** SIMLANDER CA (`hewitt2019cellular`) with accessibility, suitability and neighbourhood factors; automatic rule detection (ARD) calibrates neighbourhood rules either by random sampling of parameter space or by stepwise grid search; rule-sets ranked by cross-comparison of multiple goodness-of-fit metrics.
- **Inputs:** open data only (as stated).
- **Parameters:** calibrated by the ARD procedure.
- **Code:** ARD scripts as supplementary material (R / RStudio) — not verified.
- **Validation:** multiple metrics vs. reference map; grid search slightly better but five times slower.
- **Reimplementability:** S1 1; S2 1 – procedure is reproducible in principle but details not read; S3 1; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional).
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

## Most reimplementable (top picks)

For this cross-cutting domain the "top picks" are reusable algorithms and reference frameworks rather
than phenomenon models:

1. `pontius2011death` (A, 9) — quantity and allocation disagreement: closed-form, parameter-free, open R reference (diffeR). First metric for the ca-geo validation component.
2. `pontius2011comparison` (B, 8) — three-map, multiple-resolution comparison; same open reference code; shows the scale at which a model is right.
3. `vanvliet2011revisiting` (B, 7) — Kappa Simulation; corrects kappa for persistence; MCK can serve as a test oracle.
4. `hagen2003fuzzy` / `hagenzanker2009improved` (C, 6; likely higher after full-text read) — Fuzzy Kappa for partial credit on near-miss fronts (fire, flood).
5. `pontius2007comparing` + `varga2019intensity` (C, 6) — figure of merit, its components and the null model; simple to compute and explain in a demo.

Reference frameworks with the highest reuse value for the JS core (not scored):
`hobley2017creative` / `tucker2016celllab` (Landlab, MIT, component coupling and asynchronous CA),
`karssenberg2010software` (PCRaster operator set and Monte Carlo template),
`derango2021opencal` (macroscopic CA API, active-cell optimisation),
`digregorio1999empirical` + `avolio2012theorem` (MAD outflow kernel shared by all flow models).

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
- **Overlaps:** SLEUTH, DINAMICA, SIMLANDER and constrained CA → `lu`; MAD / SCIARA / SCIDDICA /
  OpenCAL → `geo` and `hyd`; Landlab CellLab-CTS examples → `geo`, `eco`.
