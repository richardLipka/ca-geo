# Hydrology and floods — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.

Domain code `hyd`. Longlist items covered: HYD-01, HYD-02, HYD-03, HYD-04, URB-02, LND-03
(evaluated together as `WAT` / `water-flow-flooding`), plus HYD-05 (erosion) context.

## Search log

Date: 2026-10-12. OpenAlex was used for the first 7 queries. After that the shared free daily
OpenAlex budget for our IP was used up (HTTP 429, "Insufficient budget", resets at midnight UTC).
All further searching and **all metadata verification** was done through the Crossref REST API
(`query.bibliographic` search and `/works/<DOI>`). Every catalogue entry below has a DOI checked
against Crossref. GitHub's search API was also rate-limited. Code was found by web search and
checked with HTTP status requests.

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automata flood inundation | OpenAlex | 1252 | Core set: WCA2D, Dottori & Todini, Liu 2015, CA-ffé, Wijaya, Chang, Ghimire |
| cellular automata surface runoff | OpenAlex | 2928 | RunCA, Caviedes-Voullième 2018, Dai 2018, Feng 2023 |
| cellular automata urban pluvial flooding | OpenAlex | 463 | Ghimire 2012, CADDIES, Gibson 2016, CNN-WCA, Li & Willems |
| cellular automata GPU flood | OpenAlex | 468 | Yu & Chang GPU, Gibson thesis, Chang 2022 DWCA |
| cellular automata rainfall-runoff | OpenAlex | 2359 | Coppola 2007, Yao 2021, Ma 2009 |
| cellular automata dam break | OpenAlex | 887 | Li et al. 2013 (dam break), VGE dam-break papers |
| minimization of differences cellular automata flow | OpenAlex | 8507 | Avolio 2012 theorem; mostly noise |
| cellular automata model of surface water flow | Crossref | 7.6 M (relevance-ranked) | Parsons & Fonstad 2007, HydroCAL |
| Cellular automata for the flow simulations on the earth surface | Crossref | 3.8 M | Cirbus & Podhoranyi 2013 (CZ, VŠB Ostrava) |
| depression filling cellular automata DEM | Crossref | 1.1 M | Noise. Used direct queries below instead |
| rapid flood spreading method | Crossref | 2.6 M | Lhomme 2008, Liu & Pender 2012 (RFSM-CA, Carlisle) |
| CAESAR-Lisflood landscape evolution model hydrodynamic | Crossref | 4.4 M | Coulthard et al. 2013 |
| Cellular Automata and Finite Volume solvers converge shallow flow | Crossref | 3.7 M | Caviedes-Voullième et al. 2018 |
| fast simple accurate algorithm to fill depressions DEM | Crossref | 4.0 M | Planchon & Darboux 2002, Priority-Flood variants |
| Fill-Spill-Merge flow routing depression hierarchies | Crossref | 1.5 M | Barnes et al. 2021 |
| Priority-flood optimal depression-filling | Crossref | 0.9 M | Barnes et al. 2014 |
| FlowFill hydrologic flow routing depressions | Crossref | 1.1 M | Callaghan & Wickert 2019 (found via Barnes 2021 references) |
| simple inertial formulation shallow water flood inundation | Crossref | 2.8 M | Bates et al. 2010 (LISFLOOD-FP inertial) |
| Benchmarking 2D hydraulic models (author Neelz) | Crossref | 4 | Hunter et al. 2008 (Glasgow benchmark) |
| Dottori Todini testing simple 2D hydraulic model urban flood experiment | Crossref | 113 k | Dottori & Todini 2012 |
| minimization of differences algorithm Di Gregorio | Crossref | 3.2 M | Avolio 2012. A separate query found Di Gregorio & Serra 1999 |
| cellular automata flash flood catchment | Crossref | 0.7 M | Douvinet et al. 2014 (RuiCells, France) |
| Podhoranyi flood modelling cellular | Crossref | 1.2 M | CZ: only hydraulic (non-CA) Floreon+ papers besides Cirbus 2013 |
| cellular automata inundation pond dike breach | Crossref | 0.6 M | Nothing CA-specific for pond/dike breach |
| Web: CADDIES caflood WCA2D source code | WebSearch | – | Exeter CADDIES page (binaries + framework source) |
| Web: RunCA, DWCA (Chang 2022), HydroCAL code | WebSearch | – | No public code found |
| Web: Néelz & Pender 2013 EA benchmark | WebSearch | – | Grey literature, gov.uk page verified (not in Crossref) |

Crossref hit counts are inflated because ranking is by relevance and no filtering is done.
Only the top 6 to 20 results per query were screened.

**Full-text access:** Elsevier, Wiley, IWA, T&F and Springer subscription pages returned
HTTP 403 to our tools, even for some articles that are open access. Full text was read for
Liu 2015 (NHESS), Wijaya 2023 (Europe PMC), Yang 2024 (Springer OA PDF), Callaghan & Wickert 2019,
Barnes 2021, Douvinet 2014 (partly), Hunter 2008 (White Rose eprint) and the Yu & Chang NHESS
discussion preprint (nhess-2024-131). Everything else is assessed from the abstract or metadata,
and those scores are provisional.

### Round 2

Crossref only (OpenAlex still quota-blocked), ≥1 s between requests. Full texts were fetched
through Semantic Scholar `openAccessPdf` links and publisher/repository PDFs with `curl`;
Elsevier, IWA, MDPI, De Gruyter and Exeter ORE still refused automated access (403/202/401).
PDFs were stored only in the agent scratchpad and deleted right after text extraction.

| Query | Source | Hits | Notes |
|---|---|---|---|
| openAccessPdf for 10 round-1 DOIs (WCA2D, Bates 2010, Coulthard 2013, Ghimire 2012, Cirbus 2013, …) | Semantic Scholar API | 10 | Cirbus 2013 green PDF read in full; WCA2D/Ghimire OA links blocked (403) |
| caflood | GitHub repository search | 8 | **AlbertChenExeter/caflood** (co-author's repo, WCA2D `.ca` rule files), WaterDesk/caflood (MIT), FluiditLtd/caddies-caflood |
| Guidolin "weighted cellular automata 2D inundation model" pdf | WebSearch | 9 | Only ORE handle + REF 2021 records; no readable PDF |
| LISFLOOD-FP 8.0 Shaw | Crossref | 141 k | Shaw et al. 2021 (GMD, OA) – restates the local inertial (ACC) scheme, EA Tests 4 and 5 |
| improving the stability … shallow water equations 2-D flood modeling de Almeida | Crossref | 376 k | de Almeida et al. 2012 (WRR); green OA copy at Southampton returned 401 |
| LISFLOOD-FP / CAESAR-Lisflood | Zenodo API | 10 | LISFLOOD-FP v8.2 software (10.5281/zenodo.13121102, GPL-2.0), v7.1, CAESAR-Lisflood 1.9b (10.5281/zenodo.321820) |
| gov.uk benchmarking 2D hydraulic flood modelling packages | gov.uk page + report PDF | 1 | SC080035/SR2 (Néelz & Pender 2010) read: Tests 1–8B listed; 2013 update only as zip (LIT 8570) |
| Wijaya & Yang 2021 (10.3390/w13091311) | Crossref | 1 | Verified; abstract from Crossref, MDPI PDF 403 |
| celulární automat simulace povodně / odtoku / eroze | WebSearch (Czech) | 10 | Only Cirbus (VŠB thesis + AMIS paper); no other Czech CA flood/runoff work |
| SMODERP2D erosion model CTU Prague | WebSearch + Crossref | – | Landa et al. 2019 (ISPRS Archives, OA) read in full; GitHub storm-fsv-cvut/smoderp2d (GPL-3.0) |
| cellular automata runoff Czech Republic catchment | Crossref | 0.9 M | Noise (non-CA Czech catchment models) |
| cellular automata dam breach flood simulation | Crossref | 1.7 M | No CA breach-development rule; only hydraulic dam-breach papers |
| cellular automaton river ice jam | Crossref | 1.0 M | No river-ice CA found |
| Neal 2011 how much physical complexity flood inundation | Crossref | 6.8 M | Verified (10.1002/hyp.8339), green OA link at Birmingham not fetched; not catalogued |

## Model families

1. **Minimisation-of-differences (MoD) water distribution.** This rule comes from Di Gregorio & Serra's
   lava and debris CA. Outflow from a cell is split so that the central cell and the receiving
   neighbours end up as close to a common level as possible. The neighbours above the running
   mean are removed iteratively. Hydrological variants add a Manning velocity to set the time step
   or the outflow limit: Liu et al. 2015, RunCA (Shao 2015), Cirbus & Podhoranyi 2013 (CZ).
   Keys: `digregorio1999empirical`, `avolio2012theorem`, `liu2015developing`, `shao2015runca`,
   `cirbus2013cellular`.
2. **Exeter CA2D / WCA2D family (weight-based distribution).** Ghimire et al. used a ranking-based
   CA2D. Guidolin et al.'s WCA2D gives each lower neighbour a weight proportional to its available
   storage capacity, part of the transferable volume stays in the central cell, and the velocity
   and time step are updated each step. Round 2: the exact rule was read from the authors' open caflood
   source (`outflowWCA2Dv2.ca`, see the WCA2D entry). It is implemented in the open CADDIES/caflood
   framework (CPU, OpenMP, OpenCL/GPU) and tested on UK Environment Agency benchmark cases.
   Keys: `ghimire2012formulation`, `guidolin2016weighted`, `gibson2016accuracy`,
   `yang2024convolutional`.
3. **Diffusive / zero-inertia "cell" models written as CA.** Fluxes between orthogonal neighbours
   come from Manning's equation with the water-surface slope, plus an explicit mass update and a
   stability-limited time step. Dottori & Todini's model and the CA-4D module of Wijaya's HIM belong
   here. Caviedes-Voullième et al. show that these CA schemes reduce to finite-volume zero-inertia
   solvers. LISFLOOD-FP (Bates 2010) is the closely related storage-cell / local-inertial scheme,
   also used inside CAESAR-Lisflood.
   Keys: `dottori2011developments`, `dottori2012testing`, `wijaya2023rapid`,
   `caviedesvoullieme2018cellular`, `bates2010simple`, `coulthard2013integrating`, `parsons2007cellular`.
4. **Dynamic-wave CA.** Chang, Yu et al. use the Bernoulli head and a velocity-update step so that
   the CA reproduces transcritical flow and wet/dry fronts. Later versions add 1D sewer/gully
   coupling, solute transport and GPU parallelisation.
   Keys: `chang2022dynamic`, `chang2021overland`, `yu2025high`.
5. **Rapid flood models based on depressions or steady state (fill-and-spill).** These do not
   resolve time, or resolve it only coarsely. Water fills topographic depressions and spills over
   to the next. Examples: RFSM (Lhomme 2008), RFSM-CA (Liu & Pender 2012), CA-ffé (Jamali 2019),
   iterative CA-like FlowFill (Callaghan & Wickert 2019) and Fill–Spill–Merge (Barnes 2021). Classic
   depression filling (Planchon & Darboux 2002, Priority-Flood) gives the reference "full ponding"
   surface.
   Keys: `lhomme2008recent`, `liu2012carlisle`, `jamali2019cellular`, `callaghan2019computing`,
   `barnes2021computing`, `planchon2002fast`, `barnes2014priority`.
6. **Catchment rainfall–runoff CA and integrated hydrology.** RuiCells uses triangular cells built
   from the DEM (France). HydroCAL couples 2D surface CA with 3D Richards subsurface flow (Italy).
   Coppola et al. use CA for drainage-network extraction and rainfall assimilation (Italy).
   Keys: `douvinet2014flash`, `furnari2024hydrocal`, `coppola2007cellular`.
7. **Dam-break CA.** Keys: `li2013spatiotemporal`. Nothing CA-specific was found for dike or pond
   breach. HYD-04 would have to combine a breach hydrograph with family 2 or 3.
8. **Benchmarks and reviews.** Keys: `hunter2008benchmarking`, `bates2022flood`. The 2013 EA
   benchmark report is grey literature, listed under gaps.

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| barnes2021computing | 2021 | Fill–Spill–Merge | Depression filling and spilling (steady state) | Raster DEM + depression hierarchy (not local CA) / D8 / water volume per depression / det. | 2 2 2 2 2 | 10 | A | GitHub + Zenodo (verified) | OA | full text |
| callaghan2019computing | 2019 | FlowFill | Runoff routing that floods depressions | Square raster / Moore (D8 steepest) / water depth / det., iterative | 2 2 2 2 1 | 9 | A | GitHub (verified) | OA | full text |
| guidolin2016weighted | 2016 | WCA2D weighted CA | Pluvial/fluvial inundation | Square raster / von Neumann / depth, level, velocity / det., adaptive Δt | 2 1 2 2 2 | 9 | A | GitHub AlbertChenExeter/caflood (co-author, verified) | OA (CC BY), publisher blocked | open source code + abstract (paper text still unread) |
| shaw2021lisflood | 2021 | LISFLOOD-FP 8.0 (r2) | Fluvial/pluvial inundation (ACC, FV1, DG2 solvers) | Raster storage cells, staggered fluxes / von Neumann / depth, unit discharge / det., Courant Δt | 1 1 2 2 2 | 8 | B | LISFLOOD-FP (GPL; Zenodo 10.5281/zenodo.13121102 v8.2) | OA | full text (first 60 %) |
| landa2019smoderp2d | 2019 | SMODERP2D (CZ, CTU) (r2) | Runoff and soil erosion on farmland | Raster / D8 / water level, sheet + rill flow / det., CFL Δt | 1 1 2 2 1 | 7 | B | GitHub storm-fsv-cvut/smoderp2d (GPL-3.0, verified) | OA | full text |
| dealmeida2012improving | 2012 | Stable local inertial scheme (θ) (r2) | Floodplain inundation | Raster / von Neumann / depth, discharge / det., Courant Δt | 1 1 2 2 1 | 7 | B | LISFLOOD-FP (same group) | green OA (blocked) | metadata only (provisional) |
| wijaya2023rapid | 2023 | Hybrid Inundation Model (HIM) | Urban pluvial + 1D drainage | Coarse raster CA-4D (Manning) + fine-DEM flat-water fill / von Neumann / det. | 1 2 0 2 2 | 7 | B | not found ("N.A.") | OA | full text |
| coulthard2013integrating | 2013 | CAESAR-Lisflood | Flood hydrodynamics + landscape evolution | Raster / von Neumann / depth, discharge, sediment / det. | 1 1 2 2 1 | 7 | B | SourceForge (verified) | paywall | abstract (provisional) |
| barnes2014priority | 2014 | Priority-Flood | Depression filling | Raster / D8 / filled elevation (priority queue, not CA) / det. | 1 1 2 2 1 | 7 | B | GitHub (verified) | paywall | abstract (provisional) |
| liu2015developing | 2015 | Urban CA (Guangzhou) | Urban pluvial flood | 5 m raster / von Neumann / water surface elevation, depth / det., MoD + Manning Δt | 1 2 0 2 1 | 6 | C | not found | OA | full text |
| wijaya2021novel | 2021 | HIM origin: CA + DEM hybrid (r2) | Rapid flood assessment | Coarse CA + fine DEM fill / von Neumann / depth / det. | 1 1 0 2 2 | 6 | C | not found | OA (MDPI blocked) | abstract (provisional) |
| yang2024convolutional | 2024 | CNN-WCA | Urban pluvial flood (Zhengzhou) | Raster / Moore / depth / det. WCA + 1D CNN | 1 1 1 1 2 | 6 | C | on request | OA | full text |
| bates2010simple | 2010 | LISFLOOD-FP local inertial | Floodplain inundation | Raster storage cells / von Neumann / depth, discharge / det. | 1 1 2 2 1 | 7 | B | LISFLOOD-FP (GPL; Zenodo, verified) | paywall | metadata + OA restatement in shaw2021lisflood (provisional) |
| planchon2002fast | 2002 | Planchon–Darboux filling | Depression filling | Raster / Moore / water-surface elevation / det., iterative | 1 1 0 2 1 | 5 | C | not verified | paywall | metadata only (provisional) |
| chang2022dynamic | 2022 | Dynamic-wave CA (SWFCA) | Shallow-water flows incl. discontinuities | Square raster / von Neumann / Bernoulli head, depth, velocity / det., CFL Δt | 1 1 0 2 1 | 5 | C | not found | OA (CC BY), publisher blocked | secondary (preprint + web) (provisional) |
| yu2025high | 2025 | GPU CA flow + pollutant | Pluvial/fluvial flood + solute | Same as SWFCA + solute CA / GPU | 1 1 0 1 2 | 5 | C | not found | OA? (not checked) | discussion preprint full text (provisional) |
| douvinet2014flash | 2014 | RuiCells flash floods | Flash floods in dry valleys (N France, EU) | Triangular DEM cells / directed links / water height / det., 3 rules | 1 2 0 1 1 | 5 | C | not found | OA (CC BY) | full text (partial read) |
| gibson2016accuracy | 2016 | CA accuracy and efficiency (caflood) | Urban surface flood | Raster / von Neumann / depth / det. | 1 1 2 1 1 | 6 | C | caflood (see WCA2D, verified) | OA | abstract (provisional) |
| parsons2007cellular | 2007 | CA model of surface water flow | Unsteady watershed flood wave | Raster / – / depth / det., Manning + timing delay | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| ghimire2012formulation | 2012 | Fast 2D urban pluvial CA (CA2D) | Urban pluvial flood | Raster / von Neumann / depth / det., synchronous | 1 1 0 1 1 | 4 | C | not found | OA (CC BY-NC-ND), publisher blocked | abstract (provisional) |
| dottori2012testing | 2012 | Simple 2D model, urban lab experiment | Urban flood (physical model) | Raster / von Neumann / depth / det., diffusive | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| jamali2019cellular | 2019 | CA-ffé | Max urban flood depth (fast) | Raster / – / depth / det. | 1 1 0 1 1 | 4 | C | not found | OA (bronze), publisher blocked | abstract (provisional) |
| shao2015runca | 2015 | RunCA | Surface runoff, multi-scale | Raster / – / elevation + depth / det., MoD + Manning | 1 1 0 1 1 | 4 | C | not found | paywall | web abstracts (provisional) |
| cirbus2013cellular | 2013 | CA flow on Earth surface (CZ) | River flood spreading (Ostravice) | 10 m raster / Moore, multi-direction / depth / det., Manning + Δt halving, Green–Ampt | 1 1 0 1 2 | 5 | C | not found | green OA (publisher PDF) | full text |
| chang2021overland | 2021 | Overland–gully–sewer CA | Urban inundation + SWMM | Raster CA 2D + 1D SWMM / det. | 1 1 0 1 1 | 4 | C | not found | green OA (Exeter, blocked) | abstract (provisional) |
| furnari2024hydrocal | 2024 | HydroCAL | Integrated surface–subsurface hydrology | 2D surface CA + 3D Richards CA (OpenCAL, asynchronous XCA) | 1 1 0 1 1 | 4 | C | not found | green OA, publisher blocked | web abstracts (provisional) |
| dottori2011developments | 2011 | CA flood inundation model developments | Fluvial inundation | Raster / von Neumann / depth / det. | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only (provisional) |
| li2013spatiotemporal | 2013 | Dam-break flooding CA | Dam break + risk | Raster / – / depth / det. | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only (provisional) |
| liu2012carlisle | 2012 | RFSM-CA Carlisle 2005 | Urban fluvial flood (UK) | Impact zones / CA spreading / det. | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only (provisional) |
| coppola2007cellular | 2007 | CA drainage network extraction | Drainage network, rainfall assimilation (Italy) | Raster / Moore / – / det. | 1 0 0 1 1 | 3 | D | not found | bronze OA, blocked | metadata only (provisional) |
| lhomme2008recent | 2008 | RFSM | Rapid flood spreading | Impact zones from DEM depressions / det. | 1 0 0 1 0 | 2 | D | not found | paywall | metadata only (provisional) |
| digregorio1999empirical | 1999 | MoD empirical method | Method (lava, debris; reused for water) | Macroscopic CA, MoD distribution | n/a | n/a | n/a | – | paywall | secondary (Liu 2015) |
| avolio2012theorem | 2012 | Theorem on MoD | Method (MoD properties, multicomponent) | – | n/a | n/a | n/a | – | paywall | metadata only |
| caviedesvoullieme2018cellular | 2018 | CA and FV converge | Theory / review | – | n/a | n/a | n/a | – | paywall | abstract |
| hunter2008benchmarking | 2008 | Glasgow urban benchmark | Benchmark of 6 2D codes | – | n/a | n/a | n/a | – | green OA | full text |
| bates2022flood | 2022 | Flood inundation prediction | Review | – | n/a | n/a | n/a | – | OA | abstract |
| neelz2010benchmarking | 2010 | EA 2D benchmark tests 1–8B (r2) | Benchmark (grey literature, no DOI) | – | n/a | n/a | n/a | – | public (gov.uk) | full text |

Count (after round 2): 36 Crossref-verified publications + 1 grey-literature report. 31 scored: A 3, B 7, C 16, D 5. 6 n/a (incl. the grey-literature benchmark).

## Entries

### barnes2021computing — Computing water flow through complex landscapes – Part 3: Fill–Spill–Merge: flow routing in depression hierarchies
- **Citation:** Barnes, R., Callaghan, K. L., Wickert, A. D. (2021). Computing water flow through complex landscapes – Part 3: Fill–Spill–Merge: flow routing in depression hierarchies. *Earth Surface Dynamics* 9(1), 105–121. DOI: 10.5194/esurf-9-105-2021 (verified: Crossref)
- **Access:** OA (Copernicus).
- **Phenomenon and study area:** Steady-state distribution of a given runoff depth into the depressions of a DEM, which fill, spill into neighbours and merge. Continental-scale and regional DEMs (North America).
- **Model:** This is not a local CA. It uses a precomputed depression hierarchy (a tree of nested depressions) and moves runoff volume through the hierarchy until every depression is either full and overflowing or holds a partial lake. D8 flow directions outside depressions. A deterministic, one-shot algorithm.
- **Inputs:** DEM, runoff depth (uniform or raster).
- **Parameters:** Essentially none apart from the runoff field.
- **Code:** https://github.com/r-barnes/Barnes2020-FillSpillMerge (HTTP 200), also Zenodo 10.5281/zenodo.3755142. C++17 with GDAL and an extensive test suite.
- **Validation:** Compared with FlowFill (same lake outcome, large speed-up). Correctness tests are included in the code.
- **Reimplementability:** S1 2 – detailed algorithm description and open code; S2 2 – parameter-free; S3 2; S4 2 – any DEM; S5 2 – quantitative comparison with FlowFill plus tests → 10, A. Assessed from: full text.
- **Browser fit:** Algorithmically heavy (hierarchy building), but O(N log N). A JS port is feasible on DEMs of about 10⁶ cells. Not a time-stepping CA.
- **Relevance to ca-geo:** WAT (HYD-01 ponding, LND-03 pit filling). Gives the **reference end state** for the ponding scenario: a CA run to equilibrium can be checked against FSM lake extents.

### callaghan2019computing — Computing water flow through complex landscapes – Part 1: Incorporating depressions in flow routing using FlowFill
- **Citation:** Callaghan, K. L., Wickert, A. D. (2019). Computing water flow through complex landscapes – Part 1: Incorporating depressions in flow routing using FlowFill. *Earth Surface Dynamics* 7(3), 737–753. DOI: 10.5194/esurf-7-737-2019 (verified: Crossref)
- **Access:** OA.
- **Phenomenon and study area:** A prescribed runoff depth is routed over a DEM so that depressions flood when enough water arrives. Lidar DEMs in Illinois, USA, and a second region.
- **Model:** Square raster with water depth per cell. In each iteration the cells are visited from the highest water surface down. Each cell sends water to its steepest D8 downslope neighbour. The amount moved is the smaller of the available water and half of the water-surface difference, which prevents oscillation. Water leaving the domain edge is lost. Iterations stop when the maximum per-iteration move |Δh_max| stays below a threshold (0.01 mm in the example) for 20 000 iterations. A final clean-up raises residual pits to the level of their water-containing neighbour (capped at 1/10 000 of the runoff). Deterministic, mass-conserving.
- **Inputs:** DEM, uniform or spatial runoff depth.
- **Parameters:** Runoff depth, convergence threshold, plateau length, tie-breaking option. All given.
- **Code:** https://github.com/KCallaghan/FlowFill (HTTP 200). A GRASS GIS extension r.flowfill is mentioned.
- **Validation:** Maps of filled and unfilled depressions for a range of runoff depths, plus convergence curves. No observed lake data. Later compared with Fill–Spill–Merge.
- **Reimplementability:** S1 2 – rule, ordering, stopping and fix-up are explicit; S2 2; S3 2; S4 2 – generic DEM; S5 1 – mainly qualitative maps and convergence plots → 9, A. Assessed from: full text.
- **Browser fit:** Very good. A simple local rule that suits a GPU/WebGL ping-pong scheme (with Jacobi-style synchronous updates instead of sorted order), but many iterations are needed. Progressive visualisation of filling is a natural demo.
- **Relevance to ca-geo:** WAT core rule candidate for HYD-01 (ponding) and LND-03 (pit lake). The "move half the difference" rule is the simplest mass-conserving water rule found.

### guidolin2016weighted — A weighted cellular automata 2D inundation model for rapid flood analysis
- **Citation:** Guidolin, M., Chen, A. S., Ghimire, B., Keedwell, E. C., Djordjević, S., Savić, D. A. (2016). A weighted cellular automata 2D inundation model for rapid flood analysis. *Environmental Modelling & Software* 84, 378–394. DOI: 10.1016/j.envsoft.2016.07.008 (verified: Crossref)
- **Access:** OA (CC BY, hybrid), but the publisher site blocked our fetch. Exeter ORE handle 10871/22670 also blocked.
- **Phenomenon and study area:** 2D pluvial and fluvial inundation. Tested against an analytical solution, four hypothetical cases and one real-world case. The wider literature reports UK Environment Agency benchmark cases for WCA2D.
- **Model (round 2: read from the authors' caflood source, `outflowWCA2Dv2.ca`, `velocityWCA2Dv1.ca`, `Setup.cpp`):** Square grid, von Neumann neighbourhood, synchronous update. Cells with depth below `ignore_wd` are skipped. For each neighbour k the available level drop is ΔL_k = min(WL_0 − WL_k, d_0). Neighbours with ΔL_k above a tolerance get a weight w_k = ΔL_k·A_k (storage volume); the smallest such weight w_min is added to the total W = Σw_k + w_min, so this share is the volume that stays in the centre cell. The total outflow is the smallest of (i) w_min plus the inflow of the previous step, (ii) a velocity limit V_max·W/w_max with V_max = v·d_0·Δt·Δx, where v = min(20 m/s, Manning velocity on the steepest-drop edge), and (iii) the water in the cell. Each neighbour gets the outflow × w_k/W. A separate velocity step (every "update DT") takes the minimum of the flux-derived velocity, the Manning velocity and the critical velocity. Δt is adapted from these velocities with a factor α between "Min DT" and "Max DT". Code defaults: tolerance 0.001 m, slope tolerance 0.1 %, ignore depth 0.001 m.
- **Inputs:** DEM, rainfall or inflow hydrograph, roughness.
- **Parameters:** Manning n per case, tolerance, slope tolerance, α, min/max/update Δt. Defaults are in the code; the values used in the paper's test cases were not read.
- **Code:** https://github.com/AlbertChenExeter/caflood (HTTP 200; owner A. S. Chen is a co-author; C++ host code plus `.ca` rule kernels for WCA2Dv1/v2 and a diffusive variant). The LICENSE file says MIT, but the `.ca` file headers carry a GPL-3 notice (cafloodpro), so the licence is still inconsistent. Mirrors: https://github.com/WaterDesk/caflood (MIT, HTTP 200) and FluiditLtd/caddies-caflood. Binaries and examples on the Exeter CADDIES page https://www.exeter.ac.uk/research/centres/cws/resources/caddies/ (HTTP 200).
- **Validation:** Analytical solution plus comparison of depth and velocity with a commercial 2D model. Up to 8× faster in the real-world case.
- **Reimplementability:** S1 2 – the complete rule, edge cases and Δt logic are readable in the authors' open kernels; S2 1 – defaults in code, per-case values not read; S3 2; S4 2 – EA benchmark data are public; S5 2 – analytical and benchmark comparisons (per abstract) → 9, A. Round 2: re-assessed from open source code — S 2 1 2 2 2 (was 1 1 1 2 2). The paper text is still unread (Elsevier and ORE block automated access).
- **Browser fit:** Excellent. Von Neumann stencil, explicit and GPU-native. Adaptive Δt needs a global min-reduction.
- **Relevance to ca-geo:** **Primary WAT candidate** for HYD-01/02/03 and URB-02. The kernel is about 60 lines and maps directly to a WebGL/WebGPU fragment or compute shader. Remaining step: read the paper for the test-case parameters.

### wijaya2023rapid — A rapid flood inundation model for urban flood analyses
- **Citation:** Wijaya, O. T., Yang, T.-H., Hsu, H.-M., Gourbesville, P. (2023). A rapid flood inundation model for urban flood analyses. *MethodsX* 10, 102202. DOI: 10.1016/j.mex.2023.102202 (verified: Crossref)
- **Access:** OA (PMC10173199).
- **Phenomenon and study area:** Urban pluvial flooding with drainage. UK EA benchmark Test 8A and Chiayi County, Taiwan (5 m DEM, about 543 k cells).
- **Model:** HIM. A CA-4D module on a coarse grid computes Manning fluxes Q = Δx·h^(5/3)·S_f^(1/2)/n to the 4 orthogonal neighbours, followed by an explicit update of the water surface. If total outflow exceeds the available volume, the fluxes are scaled down. A "D-Flat" module redistributes each coarse cell's volume onto a finer DEM inside its impact zone by raising a flat water level in increments (IC). A 1D Saint-Venant drainage model is coupled two-way.
- **Inputs:** Coarse and fine DEM, rainfall, Manning n, drainage network.
- **Parameters:** DEM ratio (2–10) and increment constant (0.0001–0.1 m), studied by sensitivity analysis. Optimal values are reported.
- **Code:** "Resource availability: N.A." Not found.
- **Validation:** FIT (area overlap), TPR, FDR, NSE, relative peak error and RMSE against the fine-grid CA-4D run, on EA Test 8A and Chiayi.
- **Reimplementability:** S1 1 – CA-4D equations given; the time-step rule and further details are in Wijaya & Yang 2021 (Water, not verified this round); S2 2; S3 0; S4 2 – EA test 8A is public; S5 2 – metrics on a public benchmark → 7, B. Assessed from: full text.
- **Browser fit:** Good. The CA-4D step is a simple stencil, and D-Flat is a per-block fill.
- **Relevance to ca-geo:** WAT, URB-02. Coarse CA plus fine-grid downscaling is a useful trick for showing detail without a fine-grid simulation.

### coulthard2013integrating — Integrating the LISFLOOD-FP 2D hydrodynamic model with the CAESAR model
- **Citation:** Coulthard, T. J., Neal, J. C., Bates, P. D., Ramirez, J., de Almeida, G. A. M., Hancock, G. R. (2013). Integrating the LISFLOOD-FP 2D hydrodynamic model with the CAESAR model: implications for modelling landscape evolution. *Earth Surface Processes and Landforms* 38(15), 1897–1906. DOI: 10.1002/esp.3478 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Flood hydrodynamics inside a cellular landscape evolution model (CAESAR). Basin scale.
- **Model:** The LISFLOOD-FP simplified (local inertial) 2D flow scheme replaces CAESAR's steady flow routing. Explicit flux updates between raster cells, coupled with sediment transport.
- **Inputs:** DEM, rainfall/hydrograph, grain sizes.
- **Parameters:** Many (hydrology, sediment). Defaults ship with the software.
- **Code:** https://sourceforge.net/projects/caesar-lisflood/ (round-1 HTTP 200; blocks bots in round 2). Round 2: also verified on Zenodo – CAESAR-Lisflood 1.9b (10.5281/zenodo.321820) and a dataset of parameter listings for existing applications (10.5281/zenodo.6594745).
- **Validation:** Not read (abstract only). Round 2: no OA copy found (Semantic Scholar: closed); score unchanged.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 2; S5 1 → 7, B (provisional).
- **Browser fit:** The hydrodynamic part is feasible. The full LEM is heavy.
- **Relevance to ca-geo:** WAT and HYD-05 (erosion), overlap with `geo`. The open code is a reference implementation of the inertial flux rule.

### barnes2014priority — Priority-flood: An optimal depression-filling and watershed-labeling algorithm for digital elevation models
- **Citation:** Barnes, R., Lehman, C., Mulla, D. (2014). Priority-flood: An optimal depression-filling and watershed-labeling algorithm for digital elevation models. *Computers & Geosciences* 62, 117–127. DOI: 10.1016/j.cageo.2013.04.024 (verified: Crossref)
- **Access:** paywall. A preprint is likely on arXiv but was not verified.
- **Model:** Floods the DEM inwards from its edges using a priority queue, which yields a depression-free surface and watershed labels. This is not a CA, but it gives the "infinite rain" ponding limit.
- **Code:** https://github.com/r-barnes/Barnes2013-Depressions and https://github.com/r-barnes/richdem (both HTTP 200).
- **Reimplementability:** S1 1 (abstract); S2 1; S3 2; S4 2; S5 1 → 7, B (provisional).
- **Browser fit:** Trivial in JS (heap-based). Runs in milliseconds to seconds on 10⁶ cells.
- **Relevance to ca-geo:** WAT preprocessing and maximum-ponding layer. A useful check for the steady state of any CA.

### liu2015developing — Developing an effective 2-D urban flood inundation model for city emergency management based on cellular automata
- **Citation:** Liu, L., Liu, Y., Wang, X., Yu, D., Liu, K., Huang, H., Hu, G. (2015). Developing an effective 2-D urban flood inundation model for city emergency management based on cellular automata. *Natural Hazards and Earth System Sciences* 15(3), 381–391. DOI: 10.5194/nhess-15-381-2015 (verified: Crossref)
- **Access:** OA.
- **Phenomenon and study area:** Urban pluvial flooding in a 0.2 km² catchment, Panyu, Guangzhou (China).
- **Model:** CA = ⟨L, N, P, T⟩ on a 5 m raster with a von Neumann neighbourhood. Diagonal exchange happens over two iterations. State per cell: water-surface elevation and depth. Order within each step: (i) add rain; (ii) subtract infiltration (constant rate per land cover up to a threshold) or inlet drainage (orifice formula Q = w·C·√(2gh)·k); (iii) compute a Manning velocity per cell and set the global Δt to the minimum of cell size / velocity; (iv) distribute movable water with the **minimisation algorithm**. The algorithm averages the water levels of the centre and its neighbours, drops neighbours above the average, repeats, then fills the remaining neighbours to a common level. Buildings are raised 10 m. Deterministic and synchronous. Boundary handling and the treatment of simultaneous outflows are not fully stated.
- **Inputs:** 5 m DEM, land-cover map (4 classes), inlet locations (96), rain-gauge hyetograph.
- **Parameters:** Manning n per class (0.01–0.04) and grassland infiltration (5.8 or 11.7 mm/h), calibrated by a 512-run grid search. Inlet drainage 4.6 mm/s derived from given coefficients.
- **Code:** not found.
- **Validation:** Calibrated on 19 April 2012 and validated on 4 September 2012. Outlet depth time series from CCTV (±4 cm). Compared with FloodMap.
- **Reimplementability:** S1 1 – the MoD steps and process order are explicit, but boundary handling and simultaneous exchange are not; S2 2 – full calibration grid and chosen values; S3 0; S4 2 – runs on a generic DEM and land cover; S5 1 – outlet hydrograph figures only, local data not public → 6, C. Assessed from: full text.
- **Browser fit:** Very good. A small stencil and simple processes.
- **Relevance to ca-geo:** URB-02 and HYD-01. The best fully written-out description of the MoD rule applied to water. Its process order (rain → losses → Δt → distribution) can serve as a template for ca-geo.

### yang2024convolutional — A Convolutional Neural Network-Weighted Cellular Automaton Model for the Fast Prediction of Urban Pluvial Flooding Processes
- **Citation:** Yang, J., Liu, K., Wang, M., Zhao, G., Wu, W., Yue, Q. (2024). *International Journal of Disaster Risk Science* 15(5), 754–768. DOI: 10.1007/s13753-024-00592-4 (verified: Crossref)
- **Access:** OA.
- **Phenomenon and study area:** Urban pluvial flooding, Zhengzhou, 20 July 2021 storm.
- **Model:** A WCA after Ghimire/Guidolin in 5 steps: find lower Moore neighbours, compute storage-based weights, compute total outflow, distribute volume, update velocity and Δt. The rules are described verbally only. A 1D CNN is trained on WCA and LISFLOOD-FP outputs, with a loss weighted 0.7/0.1/0.2.
- **Inputs:** DEM, design storms, land use.
- **Parameters:** CNN architecture given. WCA parameters not tabulated.
- **Code:** "available by email". Not public.
- **Validation:** MAE (mostly < 5 mm), RMSE, NSE, precision/recall/F1 against LISFLOOD-FP.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 2 → 6, C. Assessed from: full text.
- **Browser fit:** The WCA part fits well. The CNN is unnecessary for ca-geo.
- **Relevance to ca-geo:** URB-02. Secondary source for the WCA rules. Shows that WCA uses a Moore neighbourhood in some implementations.

### bates2010simple — A simple inertial formulation of the shallow water equations for efficient two-dimensional flood inundation modelling
- **Citation:** Bates, P. D., Horritt, M. S., Fewtrell, T. J. (2010). *Journal of Hydrology* 387(1–2), 33–45. DOI: 10.1016/j.jhydrol.2010.03.027 (verified: Crossref)
- **Access:** paywall.
- **Model:** Raster storage-cell model. Inter-cell discharge is updated explicitly with a local-inertia term and friction, and the time step is CFL-limited. Conceptually a deterministic CA with a von Neumann stencil (context, not labelled CA by its authors). Details not read.
- **Code:** Round 2: LISFLOOD-FP releases on Zenodo verified through the Zenodo API: v7.1 (10.5281/zenodo.4268656) and v8.2 (10.5281/zenodo.13121102, GPL-2.0). Documentation for v8.0 at https://www.seamlesswave.com/LISFLOOD8.0 (HTTP 200). The github.com/LISFLOOD-FP organisation is still not considered official.
- **Rule (secondary, from shaw2021lisflood, OA):** depth update from the net face discharges; face discharge updated from its previous value minus a gravity term driven by the water-surface gradient, divided by a semi-implicit Manning friction factor using the flow depth at the face; Δt from a Courant condition (default 0.7 in v8.0). The θ-weighted stabilisation is in dealmeida2012improving.
- **Reimplementability:** S1 1 (paper still unread); S2 1; S3 2 – authors' group code; S4 2; S5 1 → 7, B. Round 2: re-assessed from OA restatement + verified code — S 1 1 2 2 1 (was 1 1 0 2 1). Still provisional.
- **Browser fit:** Excellent (two flux arrays and one depth array).
- **Relevance to ca-geo:** WAT HYD-02 (fluvial). Probably the strongest physics-based local rule. Round 2: read the full text and verify the open LISFLOOD-FP code.

### planchon2002fast — A fast, simple and versatile algorithm to fill the depressions of digital elevation models
- **Citation:** Planchon, O., Darboux, F. (2002). *CATENA* 46(2–3), 159–176. DOI: 10.1016/s0341-8162(01)00164-3 (verified: Crossref)
- **Access:** paywall.
- **Model:** Iterative depression filling (CA-like local relaxation of a water surface). Details not read this round.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2; S5 1 → 5, C (metadata only, provisional).
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** HYD-01 and LND-03 (steady-state ponding). Fits CA style better than Priority-Flood because it is iterative and local.

### chang2022dynamic — Dynamic-wave cellular automata framework for shallow water flow modeling
- **Citation:** Chang, T.-J., Yu, H.-L., Wang, C.-H., Chen, A. S. (2022). *Journal of Hydrology* 613, 128449. DOI: 10.1016/j.jhydrol.2022.128449 (verified: Crossref)
- **Access:** OA (CC BY), but the publisher site blocked our fetch.
- **Model (from the Yu & Chang NHESS discussion preprint and web summary):** SWFCA. Square cells with a von Neumann neighbourhood. Five sequential steps: flow direction and condition from the Bernoulli head; mass flux from Manning or weir equations; predicted depth; velocity from a modified energy equation; state update. Then boundary conditions and a CFL time step. Behaves like a dynamic wave (transcritical flow, wet/dry fronts).
- **Validation:** 4 regular-flow cases and 6 benchmark cases with strong discontinuities (per secondary sources).
- **Code:** not found.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2 – standard benchmark cases; S5 1 → 5, C (provisional).
- **Browser fit:** Good (explicit stencil), with more state per cell.
- **Relevance to ca-geo:** HYD-04 (pond breach) and dam break, where a dynamic wave matters.

### yu2025high — A high-performance approach with cellular automata framework and GPU parallelization for real-time waterflows and pollutant transport simulations of pluvial and fluvial floods
- **Citation:** Yu, H.-L., Chang, T.-J. (2025). *Water Research X* 28, 100397. DOI: 10.1016/j.wroa.2025.100397 (verified: Crossref)
- **Access:** not checked. The NHESS discussion preprint (nhess-2024-131, CC BY) was read instead. Its title differs, so it is probably a precursor.
- **Model:** SWFCA (above) coupled with an advanced solute-transport CA (weighted diffusion/advection with an oscillation limiter, tolerance 10⁻⁸) on the GPU. Verification cases include analytical problems, a laboratory case and a Taiwanese urban event, plus an efficiency case with a levee breach hydrograph.
- **Code:** The preprint's code-availability section only points to the method descriptions. No repository.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1 – data on an NTU file share (not checked); S5 2 → 5, C (provisional).
- **Relevance to ca-geo:** GPU design patterns. A levee breach is used as a test (HYD-02/HYD-04). Overlap with `atm` (pollutant transport).

### douvinet2014flash — A flash flood hazard assessment in dry valleys (northern France) by cellular automata modelling
- **Citation:** Douvinet, J., Van De Wiel, M. J., Delahaye, D., Cossart, E. (2014). *Natural Hazards* 75(3), 2905–2929. DOI: 10.1007/s11069-014-1470-3 (verified: Crossref)
- **Access:** OA (CC BY).
- **Phenomenon and study area:** Flash floods in 148 small dry-valley basins in Seine-Maritime, France (EU), under 16 rainfall intensities.
- **Model:** RuiCells. Cells are triangles derived from the DEM, with flow links directed by topography. Three deterministic hydrological rules. Six flow parameters (e.g. the water height required to move, velocity limits for negligible and steep slopes, given as v0 = 0.2 and v1 = 60). The full model is described in earlier (French) publications.
- **Inputs:** DEM, CORINE land cover combined with a regional land-use map, infiltration per land-use class (table).
- **Parameters:** Table of land-use parameters from several sources. Calibrated on one 1997 event.
- **Code:** not found.
- **Validation:** Peak flows, specific discharges and lag times. Compared with historical flood occurrence.
- **Reimplementability:** S1 1 – full rules are in other papers; S2 2; S3 0; S4 1; S5 1 → 5, C. Assessed from: full text (partial read).
- **Browser fit:** Moderate (irregular triangle mesh).
- **Relevance to ca-geo:** HYD-03 (flash floods on small catchments). An EU case. The muddy-flood setting is close to Czech loess landscapes (HYD-05).

### gibson2016accuracy — Accuracy and Computational Efficiency of 2D Urban Surface Flood Modelling Based on Cellular Automata
- **Citation:** Gibson, M. J., Savic, D. A., Djordjevic, S., Chen, A. S., Fraser, S., Watson, T. (2016). *Procedia Engineering* 154, 801–810. DOI: 10.1016/j.proeng.2016.07.409 (verified: Crossref)
- **Access:** OA (gold). The publisher blocked our fetch.
- **Model:** Exeter CA flood model on a regular grid, applied to burst or surcharge flows from pipes over lidar terrain.
- **Reimplementability:** S1 1; S2 1; S3 2 – caflood source now verified (see WCA2D); S4 1; S5 1 → 6, C (abstract). Round 2: S3 1→2 only.
- **Relevance to ca-geo:** URB-02 (water main burst scenario idea). Accuracy and efficiency figures for caflood.

### parsons2007cellular — A cellular automata model of surface water flow
- **Citation:** Parsons, J. A., Fonstad, M. A. (2007). *Hydrological Processes* 21(16), 2189–2195. DOI: 10.1002/hyp.6587 (verified: Crossref)
- **Access:** paywall.
- **Model:** Unsteady-flow CA. Mass conservation and Manning's equation are combined with an algorithm that delays moving water to the next pixel until the travel time has elapsed. Hydrographs are compared with Walnut Gulch observations.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (abstract).
- **Relevance to ca-geo:** HYD-03. The travel-time delay idea is an alternative to a global adaptive Δt.

### ghimire2012formulation — Formulation of a fast 2D urban pluvial flood model using a cellular automata approach
- **Citation:** Ghimire, B., Chen, A. S., Guidolin, M., Keedwell, E. C., Djordjević, S., Savić, D. A. (2012). *Journal of Hydroinformatics* 15(3), 676–686. DOI: 10.2166/hydro.2012.245 (verified: Crossref)
- **Access:** OA (CC BY-NC-ND per Semantic Scholar). The publisher blocked our fetch.
- **Model:** Regular grid, generic local rules, synchronous update. Tested on a hypothetical terrain and a real urban area against a hydraulic model.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (abstract).
- **Relevance to ca-geo:** Predecessor of WCA2D (ranking-based CA2D). Read together with Guidolin 2016.

### dottori2012testing — Testing a simple 2D hydraulic model in an urban flood experiment
- **Citation:** Dottori, F., Todini, E. (2012). *Hydrological Processes* 27(9), 1301–1320. DOI: 10.1002/hyp.9370 (verified: Crossref)
- **Access:** paywall.
- **Model:** The 2D diffusive CA model of Dottori & Todini is tested on laboratory experiments with a physical model of an urban district that has measured water levels. Porosity-based and increased-roughness representations of buildings are also tested.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (abstract). S5 may rise if the lab data are public.
- **Relevance to ca-geo:** URB-02. Simplified building representation (porosity/roughness) is relevant at coarse browser resolutions.

### jamali2019cellular — A Cellular Automata Fast Flood Evaluation (CA-ffé) Model
- **Citation:** Jamali, B., Bach, P. M., Cunningham, L., Deletic, A. (2019). *Water Resources Research* 55(6), 4936–4953. DOI: 10.1029/2018wr023679 (verified: Crossref)
- **Access:** bronze OA. The publisher blocked our fetch.
- **Model:** Fast CA that predicts maximum urban flood depth without the depression pre- and post-processing of rapid flood models. Compared with HEC-RAS and TUFLOW in 20 experiments on 5 urban subcatchments. Weak where floodwater momentum is high, and it does not give a time evolution.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (abstract).
- **Relevance to ca-geo:** URB-02. A "max depth in seconds" mode for interactive what-if scenarios.

### shao2015runca — RunCA: A cellular automata model for simulating surface runoff at different scales
- **Citation:** Shao, Q., Weatherley, D., Huang, L., Baumgartl, T. (2015). *Journal of Hydrology* 529, 816–829. DOI: 10.1016/j.jhydrol.2015.09.003 (verified: Crossref)
- **Access:** paywall.
- **Model (from web abstract summaries):** Rectangular cells. The cell state combines elevation and water depth. Water balance covers rain, interception, infiltration and in/outflow. Distribution uses minimisation-of-differences with spatially varying Manning velocities. Validated on two US basins with literature data.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (provisional).
- **Relevance to ca-geo:** HYD-01. MoD with infiltration. Also applied to mine-site rehabilitation (LND-03 context).

### cirbus2013cellular — Cellular Automata for the Flow Simulations on the Earth Surface, Optimization Computation Process
- **Citation:** Cirbus, J., Podhoranyi, M. (2013). *Applied Mathematics & Information Sciences* 7(6), 2149–2158. DOI: 10.12785/amis/070605 (verified: Crossref)
- **Access:** green OA – publisher PDF via Semantic Scholar (naturalspublishing.com), read in full in round 2. A related VŠB master's thesis by the first author (in Slovak) is listed at https://dspace.vsb.cz/items/5584cc47-558b-4716-a44e-0b50684f8587 (seen in search, not opened).
- **Phenomenon and study area:** Flood spreading along a 1.5 × 1.5 km reach of the **Ostravice river** (Czech Republic; VŠB – Technical University of Ostrava, IT4Innovations), 10 m photogrammetric DEM (2007).
- **Model:** Pre-processing builds a slope layer (8-neighbour finite differences) and a multi-direction flow-direction layer (all lowest neighbours, bit-coded). A roving window visits all cells; a temporary grid makes the update effectively synchronous. Water moves from a cell to its lower neighbours when the cell is "flooded". Velocity v = d^(2/3)·s^(1/2)/n (Manning, with terrain slope); transfer time T = Δx/v; volume moved per iteration W = d·Δx·v·Δt. Δt starts at 1 s and is halved whenever the condition T > Δt is violated. Infiltration by Green–Ampt; absorbing boundaries. How the volume is split among several lower neighbours is not fully specified.
- **Inputs:** DEM, source cells (river inflow as a fixed water column), optional roughness and infiltration rasters.
- **Parameters:** n = 0.04 for the whole area, zero infiltration, no rain; source 0.7 m over 3 cells (plus 0.2 m and 0.3 m tributary sources in the second run); 6 h simulated.
- **Code:** not found (Python implementation mentioned).
- **Validation:** 11 surveyed water levels every 200 m between two gauges (Q = 154 m³/s) vs simulated levels (table): Pearson r 0.556 without and 0.976 with the two tributaries.
- **Optimisations:** elevation mask (cells above the source level are excluded), watershed mask, raster caching plus multiprocessing; large reductions of the 2 h 50 min base run time are reported.
- **Reimplementability:** S1 1 – main equations and order given, distribution among several receivers unclear; S2 1 – values for the case only; S3 0; S4 1 – DEM not public (DMR 5G would be a substitute); S5 2 – tabulated measured vs simulated levels → 5, C. Round 2: re-assessed from full text — S 1 1 0 1 2 (was 1 1 0 1 1).
- **Relevance to ca-geo:** **CZ** precedent for WAT (HYD-02) with a small published check table. The elevation-mask optimisation (skip cells that can never be reached) is directly useful in the browser.

### chang2021overland — Overland-gully-sewer (2D-1D-1D) urban inundation modeling based on cellular automata framework
- **Citation:** Chang, T.-J., Yu, H.-L., Wang, C.-H., Chen, A. S. (2021). *Journal of Hydrology* 603, 127001. DOI: 10.1016/j.jhydrol.2021.127001 (verified: Crossref)
- **Access:** green OA (Exeter ORE 10871/127256), blocked for our tools.
- **Model:** A CA replaces the non-inertia SWE overland model, linked with SWMM gully and sewer models. Two Taipei events.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (abstract).
- **Relevance to ca-geo:** URB-02 (drainage coupling, only if a simple sink term is not enough).

### furnari2024hydrocal — HydroCAL: A novel integrated surface–subsurface hydrological model based on the Cellular Automata paradigm
- **Citation:** Furnari, L., De Rango, A., Senatore, A., Mendicino, G. (2024). *Advances in Water Resources* 185, 104623. DOI: 10.1016/j.advwatres.2024.104623 (verified: Crossref)
- **Access:** green OA (per Semantic Scholar), blocked.
- **Model (from EGU abstracts and web summary):** A diffusive-like 2D surface routing CA coupled with a 3D variably saturated (Richards) subsurface CA. Built on the OpenCAL library with asynchronous (extended CA) activation by a head-difference threshold. Event-based, applied to a Mediterranean headwater catchment (Italy, EU). Streamflow NSE 0.86 and KGE 0.88 reported.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C (provisional).
- **Relevance to ca-geo:** HYD-03 and infiltration-excess vs saturation-excess runoff. Overlap with `atm` (groundwater).

### dottori2011developments — Developments of a flood inundation model based on the cellular automata approach: Testing different methods to improve model performance
- **Citation:** Dottori, F., Todini, E. (2011). *Physics and Chemistry of the Earth, Parts A/B/C* 36(7–8), 266–280. DOI: 10.1016/j.pce.2011.02.004 (verified: Crossref)
- **Access:** paywall. No abstract available through our sources.
- **Model:** Flood inundation CA (diffusive). The paper compares methods for improving performance. Details not available.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D (metadata only, provisional).
- **Relevance to ca-geo:** HYD-02. A foundational fluvial CA paper (EU, Italy). Read in round 2.

### li2013spatiotemporal — Spatiotemporal simulation and risk analysis of dam-break flooding based on cellular automata
- **Citation:** Li, Y., Gong, J., Zhu, J., Song, Y., Hu, Y., Ye, L. (2013). *International Journal of Geographical Information Science* 27(10), 2043–2059. DOI: 10.1080/13658816.2013.786081 (verified: Crossref)
- **Access:** paywall.
- **Model:** Dam-break flood CA with risk analysis. Details not available.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D (metadata only, provisional).
- **Relevance to ca-geo:** HYD-04 (pond/dam breach). The only CA dam-break paper found.

### liu2012carlisle — Carlisle 2005 urban flood event simulation using cellular automata-based rapid flood spreading model
- **Citation:** Liu, Y., Pender, G. (2012). *Soft Computing* 17(1), 29–37. DOI: 10.1007/s00500-012-0898-1 (verified: Crossref)
- **Access:** paywall.
- **Model:** RFSM-type spreading formulated as a CA. Applied to the Carlisle 2005 fluvial flood, a UK benchmark event.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D (metadata only, provisional).
- **Relevance to ca-geo:** HYD-02 (validating flood extents against observed outlines).

### coppola2007cellular — Cellular automata algorithms for drainage network extraction and rainfall data assimilation
- **Citation:** Coppola, E., Tomassetti, B., Mariotti, L., Verdecchia, M., Visconti, G. (2007). *Hydrological Sciences Journal* 52(3), 579–592. DOI: 10.1623/hysj.52.3.579 (verified: Crossref)
- **Access:** bronze OA (T&F), blocked.
- **Model:** CA for drainage-network extraction from a DEM and for rainfall data assimilation (Italy). Details not read.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D (metadata only, provisional).
- **Relevance to ca-geo:** Preprocessing of the WAT river network (HYD-02).

### lhomme2008recent — Recent development and application of a rapid flood spreading method
- **Citation:** Lhomme, J., Sayers, P., Gouldby, B., Wills, M., Mulet-Marti, J. (2008). In: *Flood Risk Management: Research and Practice*, 15–24. DOI: 10.1201/9780203883020.ch2 (verified: Crossref)
- **Access:** paywall.
- **Model:** RFSM. Spreads flood volume among DEM-derived depression "impact zones" to find the final extent. Not time-resolved.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 0 → 2, D (metadata only).
- **Relevance to ca-geo:** HYD-02 fast mode. Context for CA-ffé and HIM.

### digregorio1999empirical — An empirical method for modelling and simulating some complex macroscopic phenomena by cellular automata
- **Citation:** Di Gregorio, S., Serra, R. (1999). *Future Generation Computer Systems* 16(2–3), 259–271. DOI: 10.1016/s0167-739x(99)00051-5 (verified: Crossref)
- **Access:** paywall.
- **Content:** Introduces the macroscopic CA methodology and the minimisation-of-differences distribution (applied to lava flows, SCIARA). The algorithm as reused for water is restated step by step in `liu2015developing`.
- **Reimplementability:** n/a (method). Value: origin of family 1. The same rule is used in the `geo` domain (lava, debris flows, SCIDDICA).

### avolio2012theorem — A Theorem about the Algorithm of Minimization of Differences for Multicomponent Cellular Automata
- **Citation:** Avolio, M. V., Di Gregorio, S., Spataro, W., Trunfio, G. A. (2012). In: *Lecture Notes in Computer Science* (ACRI 2012), 289–298. DOI: 10.1007/978-3-642-33350-7_30 (verified: Crossref)
- **Access:** paywall.
- **Content:** A formal property of MoD for multicomponent CA, relevant to mass conservation and to the correctness of the distribution step. Not read.
- **Reimplementability:** n/a (theory).

### caviedesvoullieme2018cellular — Cellular Automata and Finite Volume solvers converge for 2D shallow flow modelling for hydrological modelling
- **Citation:** Caviedes-Voullième, D., Fernández-Pato, J., Hinz, C. (2018). *Journal of Hydrology* 563, 411–417. DOI: 10.1016/j.jhydrol.2018.06.021 (verified: Crossref)
- **Access:** paywall.
- **Content:** Reviews cell-based (CA) surface-flow simulators and zero-inertia FV solvers, and shows mathematically that, with suitable choices, they are the same scheme. Error and stability properties therefore carry over.
- **Reimplementability:** n/a. Value: a theoretical justification and stability guide for choosing the WAT rule and Δt. Useful for presenting the CA as numerically sound.

### hunter2008benchmarking — Benchmarking 2D hydraulic models for urban flooding
- **Citation:** Hunter, N. M., Bates, P. D., Neelz, S., Pender, G., Villanueva, I., Wright, N. G., Liang, D., Falconer, R. A., Lin, B., Waller, S., Crossley, A. J., Mason, D. C. (2008). *Proceedings of the ICE – Water Management* 161(1), 13–30. DOI: 10.1680/wama.2008.161.1.13 (verified: Crossref)
- **Access:** green OA (White Rose eprint 77249).
- **Content:** Six 2D codes (DIVAST, DIVAST-TVD, TUFLOW, JFLOW, TRENT, LISFLOOD-FP) on an identical 2 m lidar plus map grid of a 1.0 × 0.4 km Glasgow district, flood of 30 July 2002, with sensitivity experiments. Buildings raised in the DEM.
- **Reimplementability:** n/a (benchmark). Value: a setup for an urban test case. Data availability not confirmed.

### bates2022flood — Flood Inundation Prediction
- **Citation:** Bates, P. D. (2022). *Annual Review of Fluid Mechanics* 54(1), 287–315. DOI: 10.1146/annurev-fluid-030121-113138 (verified: Crossref)
- **Access:** OA.
- **Content:** Review of inundation physics, simplified numerical schemes, HPC, big data and global flood models.
- **Reimplementability:** n/a. Value: an entry point placing CA and simplified schemes among other inundation models.

### shaw2021lisflood — LISFLOOD-FP 8.0: the new discontinuous Galerkin shallow-water solver for multi-core CPUs and GPUs (round 2)
- **Citation:** Shaw, J., Kesserwani, G., Neal, J., Bates, P., Sharifian, M. K. (2021). LISFLOOD-FP 8.0: the new discontinuous Galerkin shallow-water solver for multi-core CPUs and GPUs. *Geoscientific Model Development* 14(6), 3577–3602. DOI: 10.5194/gmd-14-3577-2021 (verified: Crossref)
- **Access:** OA (CC BY).
- **Phenomenon and study area:** Fluvial and pluvial inundation. EA benchmark Tests 4 (slow wave over a flat floodplain) and 5 (valley flooding), and a 2500 km² rain-on-grid run of Storm Desmond (Eden catchment, UK).
- **Model:** Compares three solvers in one code: ACC (the Bates/de Almeida local inertial scheme: explicit depth update from face discharges, discharge update from the water-surface gradient with a semi-implicit Manning friction term, staggered C-grid), FV1 (first-order finite volume) and DG2 (second-order discontinuous Galerkin). The ACC equations are restated; the Δt formula is only described (Courant number 0.7) in the part read.
- **Inputs:** DEM, inflow hydrographs or rainfall, Manning n.
- **Parameters:** Manning n and Courant number per test given.
- **Code:** LISFLOOD-FP, GPL; documentation https://www.seamlesswave.com/LISFLOOD8.0 (HTTP 200); software releases on Zenodo (v8.2: 10.5281/zenodo.13121102, verified); simulation results on Zenodo (10.5281/zenodo.4661888, verified).
- **Validation:** Water levels and velocities at EA gauge points against the other solvers; run times and multi-core scaling (ACC ≈ 7× on 16 cores).
- **Reimplementability:** S1 1 – ACC equations given but Δt and wet/dry details are in earlier papers; S2 1; S3 2; S4 2 – EA tests public; S5 2 – quantitative point comparisons and published outputs → 8, B. Assessed from: full text (first ~60 % of the HTML).
- **Browser fit:** ACC is the cheapest physically based rule (one depth and two flux arrays), very GPU-friendly.
- **Relevance to ca-geo:** HYD-02 and URB-02. The best open, citable restatement of the local inertial rule, with outputs on public benchmarks that a WebGPU port can be checked against.

### landa2019smoderp2d — SMODERP2D soil erosion model entering an open source era with GPU-based parallelization (round 2)
- **Citation:** Landa, M., Jeřábek, J., Pešek, O., Kavka, P. (2019). SMODERP2D soil erosion model entering an open source era with GPU-based parallelization. *ISPRS Archives* XLII-4/W14, 143–149. DOI: 10.5194/isprs-archives-XLII-4-W14-143-2019 (verified: Crossref)
- **Access:** OA (CC BY).
- **Phenomenon and study area:** Event-based surface runoff and soil erosion on agricultural land and small catchments. **CZ** (Czech Technical University in Prague, Dept. of Landscape Water Conservation); performance tests on a 0.5 km² monitored Czech catchment.
- **Model:** Raster cell-by-cell mass balance: storage change = inflow (effective rain + inflow from upslope neighbours) − outflow (infiltration, outflow, surface retention). Flow directions by D8. Surface flow is split into sheet flow q = X·I^Y·h^b (empirical X, Y, b; I = slope) and rill flow by Manning once a critical sheet-flow depth is exceeded. Δt limited by the CFL criterion. Stream routing on a predefined polyline network. The paper does not call it a CA, but the rule is a local neighbour exchange on a grid.
- **Inputs:** DEM, soil and land-use maps (parameter tables per class), rainfall.
- **Parameters:** Empirical sheet-flow coefficients and soil parameters come from the model's parameter database (manual); not listed in this paper.
- **Code:** https://github.com/storm-fsv-cvut/smoderp2d (HTTP 200, GPL-3.0, active 2026); project page https://smoderp.fsv.cvut.cz/ (seen in search).
- **Validation:** Only CPU/GPU run-time tests in this paper; hydrological validation is in other SMODERP publications (not verified).
- **Reimplementability:** S1 1 – core equations given, details in the reference manual; S2 1; S3 2; S4 2 – generic DEM, soil and land-use layers (Czech soil data exist); S5 1 → 7, B. Assessed from: full text.
- **Browser fit:** Good (D8 stencil, explicit, CFL-limited Δt).
- **Relevance to ca-geo:** HYD-01 and HYD-05 (muddy floods on Czech farmland). The only open Czech raster runoff–erosion code found; its parameter database could feed a ca-geo erosion demo. Overlap with `geo` (erosion).

### dealmeida2012improving — Improving the stability of a simple formulation of the shallow water equations for 2-D flood modeling (round 2)
- **Citation:** de Almeida, G. A. M., Bates, P., Freer, J. E., Souvignet, M. (2012). Improving the stability of a simple formulation of the shallow water equations for 2-D flood modeling. *Water Resources Research* 48(5). DOI: 10.1029/2011wr011570 (verified: Crossref)
- **Access:** green OA copy listed by Semantic Scholar (eprints.soton.ac.uk) returned HTTP 401; publisher closed.
- **Model:** Adds a θ-weighted spatial averaging of neighbouring discharges to the Bates 2010 local inertial update, which damps the checkerboard oscillations at low friction. This is the version used in current LISFLOOD-FP ACC.
- **Code:** LISFLOOD-FP (same group; see bates2010simple).
- **Reimplementability:** S1 1; S2 1; S3 2; S4 2; S5 1 → 7, B. Assessed from: metadata only (provisional).
- **Relevance to ca-geo:** HYD-02. Needed for a stable inertial WAT rule in shallow, low-friction areas.

### wijaya2021novel — A Novel Hybrid Approach Based on Cellular Automata and a Digital Elevation Model for Rapid Flood Assessment (round 2)
- **Citation:** Wijaya, O. T., Yang, T.-H. (2021). A Novel Hybrid Approach Based on Cellular Automata and a Digital Elevation Model for Rapid Flood Assessment. *Water* 13(9), 1311. DOI: 10.3390/w13091311 (verified: Crossref)
- **Access:** OA (MDPI), but the PDF returned 403 to our tools; abstract from Crossref.
- **Model:** The original HIM: a CA computes the temporal flood evolution on a coarse grid; a DEM-based fill step downscales the result onto a fine grid. The CA-4D equations are restated in wijaya2023rapid.
- **Validation:** Three UK EA benchmark tests and an observed event (depth RMSE 0.388–0.400 m).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2; S5 2 – EA benchmarks plus RMSE → 6, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** URB-02, HYD-02. Companion to wijaya2023rapid.

### neelz2010benchmarking — Benchmarking of 2D Hydraulic Modelling Packages (round 2)
- **Citation:** Néelz, S., Pender, G. (2010). *Benchmarking of 2D Hydraulic Modelling Packages*. Environment Agency Science Report SC080035/SR2, Bristol, ISBN 978-1-84911-190-4. Grey literature, no DOI. PDF: https://assets.publishing.service.gov.uk/media/5a75765c40f0b6360e4744dd/scho0510bsno-e-e.pdf (HTTP 200, read in round 2), listed on https://www.gov.uk/government/publications/benchmarking-the-latest-generation-of-2d-hydraulic-flood-modelling-packages (HTTP 200).
- **Content:** Eight test cases with specified inputs and the results of many 2D packages: Test 1 flooding a disconnected water body; 2 filling of floodplain depressions; 3 momentum conservation over a small obstruction; 4 speed of flood propagation over an extended floodplain; 5 valley flooding; 6A/6B dam break (laboratory scale and ×20 scale, after Soares-Frazão & Zech 2002); 7 river and floodplain linking; 8A rainfall and point source surface flow in urban areas; 8B surface flow from a surcharging sewer. The 2013 update (Néelz & Pender, SC120002, report LIT 8570) is offered on the same page as a 7.6 MB zip together with the model data (not downloaded).
- **Reimplementability:** n/a (benchmark). Value: the standard quantitative S5 source for any WAT implementation. Test 2 checks ponding (HYD-01), Tests 4–5 fluvial spreading (HYD-02), Test 6 a dam break (HYD-04), Test 8A urban pluvial flow (URB-02).

## Most reimplementable (top picks)

1. **callaghan2019computing (FlowFill), A 9.** A local, mass-conserving water rule (move half the difference to the steepest neighbour) with open code. The ideal first WAT ponding demo.
2. **barnes2021computing (Fill–Spill–Merge), A 10.** Not a CA, but open, tested code. Use it as the reference steady-state solution to check ca-geo ponding results.
3. **guidolin2016weighted (WCA2D), A 9 (round 2).** The de facto standard fast flood CA. The complete rule is now readable in the co-author's open caflood kernels (GitHub), it is GPU-native and can be checked against the public EA benchmark tests (`neelz2010benchmarking`). Primary candidate for the dynamic WAT model.
4. **wijaya2023rapid (HIM / CA-4D), B 7.** Explicit Manning-flux CA with metrics on EA Test 8A. The coarse-plus-fine downscaling idea is useful for the browser.
5. **liu2015developing (MoD + Manning), C 6.** The most complete open description of the minimisation-of-differences rule with rain, infiltration and drain sinks. A good template if WCA2D details are unavailable.
6. **shaw2021lisflood / bates2010simple / dealmeida2012improving (B 8/7/7).** The local-inertial (LISFLOOD-FP ACC) rule, restated in an OA paper, with open LISFLOOD-FP and CAESAR-Lisflood code on Zenodo and published outputs for EA Tests 4 and 5. Best physics per line of code for fluvial HYD-02.
7. **landa2019smoderp2d (SMODERP2D), B 7 — CZ.** Open Czech raster runoff–erosion code (CTU Prague) with a soil-parameter database; the best CZ anchor for HYD-01/HYD-05.
8. **cirbus2013cellular, C 5 — CZ.** Czech (Ostrava) water-spreading CA with a small published check table (11 surveyed water levels).

## Gaps and unverified leads

- **Full texts not read** (publisher 403, still in round 2): Guidolin 2016, Ghimire 2012, Jamali 2019, Chang 2022, Gibson 2016 (all OA), Wijaya & Yang 2021 (MDPI). The WCA2D rule is now covered by the open code (round 2); the paper's test-case parameters are still missing. Manual download by the user would close this.
- **caflood licence:** round 2 found the source on GitHub (AlbertChenExeter/caflood), but LICENSE (MIT) and file headers (GPL-3) disagree. Ask the authors before reusing code; a clean-room reimplementation from the rule description avoids the issue.
- **UK EA benchmark:** round 2 read the 2010 report (now entry `neelz2010benchmarking`, Tests 1–8B). The 2013 update (SC120002, LIT 8570) and the model-data zip were not downloaded (data download not allowed in this phase); confirm the 2013 test list and data format before implementation.
- **LISFLOOD-FP code:** verified on Zenodo in round 2 (v7.1, v8.2). The github.com/LISFLOOD-FP organisation is still not the official one.
- **CZ studies:** round 2 found no further Czech CA flood/runoff paper (Crossref and Czech-language web search). Added the open CTU code SMODERP2D (`landa2019smoderp2d`, raster but not labelled CA). Leads not followed: the first author's VŠB thesis (dspace.vsb.cz item above), Floreon+ (non-CA), SMODERP validation papers. ZČU and ČVUT CA flood work was not found.
- **Pond cascade / dike breach (HYD-04):** round 2 searches again found no CA breach-development rule. Usable pieces: EA Test 6 dam break (`neelz2010benchmarking`) as a check, a breach hydrograph as inflow, and WCA2D or a dynamic-wave CA (`chang2022dynamic`) for the spreading.
- **River ice:** no CA for ice jams or ice-jam floods was found (Crossref); only hydraulic models (e.g. Lindenschmidt 2024 book chapter, seen, not catalogued).
- **Other leads seen in results but not catalogued:** Dai et al. 2018 (J. Hydrol., CA rainfall-runoff plus NPS pollution), Yao et al. 2021 (WRM, CA rainfall-runoff under land uses), Feng et al. 2023 (J. Hydrol., urban CA hydrological model), Issermann et al. 2020 (Water, motion-cost fields), Tavakolifar et al. 2020 (1D–2D CA), Zhang & Che 2023 (overland flow plus sediment CA, overlap `geo`), Li & Willems 2020 (WRR, hybrid probabilistic pluvial), Bermúdez et al. 2018 (surrogates), Ma et al. 2009 (hillslope runoff and erosion CA), Wang et al. 2023 (CA solute transport, Water 16, 129), Armal & Al-Suhili 2019 (urban CA), Nkwunonwo et al. 2019 (CA plus semi-implicit FD). Most are verified in Crossref or OpenAlex search results but not assessed.
- **Ownership caveat:** A web search mentioned an unofficial Python "WeightedCA" reimplementation hosted on IPFS. It was not checked and is not a citable source.
- **Neal et al. 2011** (Hydrol. Process., 10.1002/hyp.8339, verified) compares simplified and full shallow-water models on benchmarks; green OA (Birmingham) not fetched. Useful to justify the choice of rule.
- **Overlaps:** `geo` (MoD rule from SCIARA/SCIDDICA, CAESAR-Lisflood, sediment and erosion CA), `atm` (pollutant transport in floods, groundwater/HydroCAL, cold-air drainage reusing water routing), `gen` (CADDIES/OpenCAL frameworks, GPU CA).

## Round 2 changes

| Key | Old score / class | New score / class | Reason |
|---|---|---|---|
| guidolin2016weighted | 1 1 1 2 2 = 7 B | 2 1 2 2 2 = 9 A | Complete rule read in the co-author's open caflood kernels (GitHub); paper text still blocked |
| bates2010simple | 1 1 0 2 1 = 5 C | 1 1 2 2 1 = 7 B | LISFLOOD-FP code verified on Zenodo; rule restated in OA shaw2021lisflood |
| cirbus2013cellular | 1 1 0 1 1 = 4 C | 1 1 0 1 2 = 5 C | Full text read (CZ, Ostravice): equations, parameters and a measured-vs-simulated table |
| gibson2016accuracy | 1 1 1 1 1 = 5 C | 1 1 2 1 1 = 6 C | caflood source verified |
| coulthard2013integrating | 7 B | 7 B (unchanged) | Zenodo releases and parameter listings verified; still no full text |
| shaw2021lisflood (new) | – | 1 1 2 2 2 = 8 B | OA, open code, EA tests |
| landa2019smoderp2d (new, CZ) | – | 1 1 2 2 1 = 7 B | OA, open GPL code |
| dealmeida2012improving (new) | – | 1 1 2 2 1 = 7 B | metadata only, provisional |
| wijaya2021novel (new) | – | 1 1 0 2 2 = 6 C | abstract only |
| neelz2010benchmarking (new) | – | n/a | grey-literature benchmark (Tests 1–8B) |

## New phenomena candidates (round 2)

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| Mining subsidence and flooded subsidence troughs | Growth of a ground-surface subsidence basin above longwall mining, followed by water filling the depression | Couples a geotechnical CA with the existing WAT ponding rule; strong local link | High: Ostrava–Karviná coalfield (subsidence lakes), North Bohemian lignite basin; extends LND-03 | `chen2020dynamic` (geomorphology.md) C 4 | Only an abstract-level CA source; filling part reuses FlowFill / WCA2D |
| River-ice jams | Ice accumulation at constrictions and backwater flooding | Winter flood type not covered by HYD-02 | Medium (ice floods on Czech rivers in cold winters) | none found | No CA found in round 2; keep as gap |
