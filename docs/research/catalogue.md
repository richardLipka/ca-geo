# Catalogue of geographic CA models — rounds 1–2

Cross-domain summary of the literature survey, the basis for selecting models to
implement. Round 1 (breadth-first) and round 2 (deepening, gap searches, horizon scan)
were both run on 2026-10-12. Details, full entries and search logs are in
`domains/*.md`; scoring follows `reimplementability-criteria.md`; all references are in
`/references.bib`.

## How to read this

- **Class** A–D = reimplementability (A: direct reimplementation, B: minor assumptions,
  C: template for our own variant, D: inspiration only). `n/a` = review / framework /
  method / data source.
- **Many scores are still provisional** (abstract only), mainly because publishers block
  automated full-text access. Round 2 re-assessed about 90 entries; roughly a third
  reached full text or complete open code. Class C remains over-represented.
- **Code** = open code verified to exist. Third-party-only implementations count as S3 = 1.
- Longlist IDs refer to `docs/brainstorm/longlist.md` (43 items); `WAT` = water model with
  scenarios.

## Overview

| Domain | File | Rows | A | B | C | D | n/a |
|---|---|---|---|---|---|---|---|
| Hydrology and floods | `domains/hydrology.md` | 37 | 3 | 7 | 16 | 5 | 6 |
| Fire | `domains/fire.md` | 32 | 3 | 3 | 17 | 5 | 4 |
| Land use and urban growth | `domains/land-use.md` | 47 | 2 | 4 | 34 | 3 | 4 |
| Geomorphology and mass movements | `domains/geomorphology.md` | 46 | 3 | 8 | 29 | 2 | 4 |
| Ecology and forestry | `domains/ecology.md` | 48 | 3 | 10 | 24 | 1 | 10 |
| Epidemics and populations | `domains/epidemics.md` | 42 | 3 | 10 | 23 | 1 | 5 |
| Movement of people and vehicles | `domains/movement.md` | 44 | 3 | 9 | 20 | 3 | 9 |
| Atmosphere, climate, water bodies, other | `domains/atmosphere-other.md` | 46 | 4 | 7 | 27 | 8 | 0 |
| Cross-cutting (reviews, frameworks, methods) | `domains/general.md` | 59 | 4 | 5 | 9 | 1 | 40 |
| **Total (with cross-domain duplicates)** | | **401** | **28** | **63** | **199** | **29** | **82** |

Plus `domains/new-phenomena.md`: horizon scan of 25 phenomena outside the longlist
(35 references, 2 × class B, the rest C/D, mostly provisional).

After deduplication the bibliography holds **418 entries** (including 3 grey-literature
items without DOI). Distinct class A/B models across domains: **86** (26 A, 60 B), plus
2 B in the horizon scan.

## What changed in round 2

- **Upgrades to class A:** WCA2D flood CA (`guidolin2016weighted`, via open caflood
  kernels), lava CA (`connor2012probabilistic`, with MOLASSES code), Saxon Switzerland
  bark-beetle CA (`pietzsch2023nonparametric`, A 10), dryland grazing CA
  (`schneider2016spatially`), Xylella spread (`white2017modelling`), coastline model
  (`ashton2006highangle`, A 10), fuzzy kappa (`hagenzanker2009improved`); PROPAGATOR and
  SLEUTH raised to 10.
- **Upgrades to class B:** LISFLOOD-FP local inertial rule (`bates2010simple`), EMBYR fire
  with firebrands (`hargrove2000simulating`), anisotropic evacuation cost
  (`wood2012anisotropic`), traffic-pollution CA (`sonnenschein2025hybrid`, open code),
  local facilitation CA (`kefi2007local`); MigClim and KISSMig raised to 8.
- **Biggest gap closed:** cold-air pooling (ATM-02) now has three grid models of class B
  (`nowatschin2006gpubased` — GPU shader, ports to WebGL; `conrad2020coldairflow` — SAGA
  tool, grey literature; `sievers2016cold` — KLAM_21) and Central European cases
  (`dobos2025terrainbased`, `uiboupin2025how`).
- **New Czech / border-area material:** SMODERP2D runoff and erosion, ČVUT, open code
  (`landa2019smoderp2d`, B); TANABBO bark-beetle model validated in the Bohemian Forest
  (`duraciova2020bark`, C); CA traffic calibrated on Czech detector data, VUT Brno
  (`korcek2012evolutionary`, B); reservoir-bank abrasion method (`slezingr2013verification`);
  Ostravice flood CA read in full (`cirbus2013cellular`); beaver expansion in the Morava
  basin (`john2010habitat`, data source); CZ hydro-geomorphic event inventory
  (`tichavsky2026hydrogeomorphic`, data source).
- **Benchmarks found:** UK EA 2D flood benchmark (`neelz2010benchmarking`, grey literature),
  lava benchmarks (`dietterich2017benchmarking`), NIST evacuation-model test suite
  (`ronchi2013process`), travel-time reference (`nelson2019suite`, A, not CA).
- **Still empty:** no peer-reviewed geographic CA running fully in the browser (only hobby
  repositories) — ca-geo would be novel in this respect; no CA coupling landscape fire and
  smoke; no CA for oil spills on rivers, post-mining lake filling, river/lake ice,
  windthrow, beaver wetlands or heavy gas over terrain; no peer-reviewed Czech fire or
  land-use CA.

## Shortlist — class A and B models (deduplicated)

Generated from the domain catalogues; sorted by domain, then score. "r2" = added in
round 2 (re-scored entries are listed in each domain file under "Round 2 changes"). Columns *Code* and *Assessed from* are abbreviated from the domain files.

| Key | Class (score) | Model | Phenomenon | Code | Assessed from | Domain(s) |
|---|---|---|---|---|---|---|
| `barnes2021computing` | A (10) | Fill–Spill–Merge | Depression filling and spilling (steady state) | GitHub + Zenodo (verified) | full text | hydrology |
| `callaghan2019computing` | A (9) | FlowFill | Runoff routing that floods depressions | GitHub (verified) | full text | hydrology |
| `guidolin2016weighted` | A (9) | WCA2D weighted CA | Pluvial/fluvial inundation | GitHub AlbertChenExeter/caflood (co-author, verified) | open source code + abstract (paper text still unread) | hydrology |
| `shaw2021lisflood` | B (8) | LISFLOOD-FP 8.0 | Fluvial/pluvial inundation (ACC, FV1, DG2 solvers) | LISFLOOD-FP (GPL; Zenodo 10.5281/zenodo.13121102 v8.2) | full text (first 60 %) | hydrology · r2 |
| `barnes2014priority` | B (7) | Priority-Flood | Depression filling | GitHub (verified) | abstract (provisional) | hydrology |
| `bates2010simple` | B (7) | LISFLOOD-FP local inertial | Floodplain inundation | LISFLOOD-FP (GPL; Zenodo, verified) | metadata + OA restatement in shaw2021lisflood (provisional) | hydrology |
| `coulthard2013integrating` | B (7) | CAESAR-Lisflood | Flood hydrodynamics + landscape evolution | SourceForge (verified) | abstract (provisional) | hydrology, geomorphology |
| `dealmeida2012improving` | B (7) | Stable local inertial scheme (θ) | Floodplain inundation | LISFLOOD-FP (same group) | metadata only (provisional) | hydrology · r2 |
| `landa2019smoderp2d` | B (7) | SMODERP2D (CZ, CTU) | Runoff and soil erosion on farmland | GitHub storm-fsv-cvut/smoderp2d (GPL-3.0, verified) | full text | hydrology · r2 |
| `wijaya2023rapid` | B (7) | Hybrid Inundation Model (HIM) | Urban pluvial + 1D drainage | not found ("N.A.") | full text | hydrology |
| `trucchia2020propagator` | A (10) | PROPAGATOR | wildfire, Italy/Spain | yes (EUPL-1.2) | full text (r2) + source code/docs | fire |
| `xia2025pytorchfire` | A (10) | PyTorchFire | wildfire, California | yes (MIT) | full text (arXiv) | fire, general |
| `pais2021cell2fire` | A (9) | Cell2Fire | wildfire, Canada | yes (GPL-3.0) | full text | fire |
| `alexandridis2008cellular` | B (8) | CA forest fire, Spetses 1990 | wildfire, Greece | third-party (BSD, MIT) | secondary full texts (Freire 2019, Xia 2025) + code | fire |
| `freire2019using` | B (8) | CA wildfire, Tavira 2012 | wildfire, Portugal | third-party (BSD) | full text | fire |
| `hargrove2000simulating` | B (7) | EMBYR | large fires, Yellowstone | dead link (Fortran 77) | full text (r2) | fire |
| `clarke1997selfmodifying` | A (10) | Self-modifying CA, SF Bay (SLEUTH origin) | urban growth | C source (Gigalopolis, verified) | abstract + official docs (rule pseudocode, r2) | land-use |
| `roodposhti2020towards` | A (10) | Automatic calibration of neighbourhood (SIMLANDER) | urban growth | SIMLANDER (verified) + suppl. script | full text | land-use, general |
| `liang2021understanding` | B (8) | PLUS model, Wuhan | multi-LU change | Windows binary + mcPLUS Linux binary with Wuhan data (ver… | full text + repos (r2) | land-use |
| `petrasova2016open` | B (8) | FUTURES in GRASS GIS (open source) | urban growth | r.futures (verified) | full text | land-use |
| `zhou2019highresolution` | B (8) | Global SLEUTH projection (GUGPS) | urban growth, global | R scripts + modified SLEUTH (figshare) | full text | land-use |
| `hewitt2019cellular` | B (7) | SIMLANDER R CA model | urban / multi-LU | R script + demo data (verified download) | abstract + project site | land-use, general |
| `damboise2022flowpy` | A (10) | Flow-Py v1.0 | avalanche, rockfall, debris-flow runout | yes | full text | geomorphology |
| `connor2012probabilistic` | A (9) | Probabilistic lava inundation, Armenia | lava flow hazard | MOLASSES (same authors, GPL, verified) | full text | geomorphology |
| `eltner2025using` | A (9) | RillGrow calibrated with 4D SfM (CTU Prague) | rill/interrill soil erosion | yes | full text | geomorphology |
| `dambrosio2003simulating` | B (8) | SCIDDICA S3-hex | debris flows (Sarno 1998) | partial (SciddicaT in OpenCAL) | full text | geomorphology |
| `dietterich2017benchmarking` | B (8) | Lava-model benchmarks incl. MOLASSES | lava flow (benchmark) | MOLASSES (verified) | full text | geomorphology · r2 |
| `kochanski2019rescal` | B (8) | Rescal-snow | snow/sand dunes | yes | full text (see atmosphere-other.md) + repo | geomorphology, atmosphere-other |
| `skinner2023testing` | B (8) | CAESAR-Lisflood vs grid size | landscape evolution, sediment yield | yes | full text (summary) | geomorphology |
| `wichmann2017gpp` | B (8) | GPP model (SAGA) | rockfall, debris-flow, avalanche process paths and runout | SAGA GIS (GPL; GitHub mirror verified) | full text | geomorphology · r2 |
| `horton2013flowr` | B (7) | Flow-R | debris-flow (and rockfall, avalanche) susceptibility and … | free binary (flow-r.org), not open source | full text | geomorphology · r2 |
| `yizhaq2017scalefree` | B (7) | Dead Sea sinkholes CA | sinkhole formation and size statistics | no | full text (preprint) | geomorphology · r2 |
| `pietzsch2023nonparametric` | A (10) | IBM → Markov-chain metamodel, Ips typographus | bark beetle spread (Saxon Switzerland NP, DE/CZ border) | GitHub | full text + code (r2) | ecology |
| `liu2025multiscale` | A (9) | Multiscale stochastic CA for mountain pine beetle | insect outbreak dispersion | GitHub | full text | ecology |
| `schneider2016spatially` | A (9) | Spatially heterogeneous grazing pressure | dryland degradation | GitHub (authors) + caspr | full text (r2) | ecology |
| `engler2012migclim` | B (8) | MIGCLIM R package | dispersal-limited range shift | CRAN archive / GitHub mirror | package user guide (full algorithm) (r2) | ecology |
| `kautz2016dispersal` | B (8) | IPS individual-based beetle dispersal | Ips typographus dispersal, virtual stand | supplement (ODD + model version) | full text (keyword-guided) | ecology · r2 |
| `nobis2014kissmig` | B (8) | KISSMig | range dynamics, migration lag | CRAN | abstract + source code (r2) | ecology |
| `bocedi2021rangeshifter` | B (7) | RangeShifter 2.0 | range expansion, connectivity | GitHub | abstract (provisional) | ecology |
| `kefi2007local` | B (7) | Local facilitation, bistability (TPB) | dryland vegetation | derived variant in caspr | rule + base parameters restated in schneider2016spatially… | ecology |
| `moenickes2013shapes` | B (7) | Giant hogweed matrix model + CA | plant invasion (8 DE sites) | not found | full text | ecology |
| `rademacher2004reconstructing` | B (7) | BEFORE beech forest model | beech mosaic cycle, storms (Central Europe) | not found | third-party ODD (full) | ecology |
| `seidl2014simulating` | B (7) | Wind disturbance at tree level (iLand) | windthrow (Sweden) | iLand GitHub | abstract (provisional) | ecology |
| `seidl2017climate` | B (7) | Wind × bark beetle interactions in iLand | windthrow + beetle (Kalkalpen, AT) | iLand GitHub | full text | ecology |
| `thiery1995model` | B (7) | Banded vegetation genesis CA | tiger bush, Niger | not found | full text | ecology |
| `bradshaw2021stochastic` | A (10) | Stochastic peopling of Sahul | human colonisation, Sahul | GitHub (GPL-3) | full text | epidemics |
| `gregoriodesouza2021reassessing` | A (9) | Tupi expansion CA | farmer expansion, S. America | Zenodo (Python + R) | full text | epidemics |
| `white2017modelling` | A (9) | Xylella spread and control, Apulia | X. fastidiosa in olives | GitHub + Zenodo (MIT) | full text + code (r2) | epidemics |
| `jones2021iteratively` | B (8) | PoPS forecasting platform | pests and pathogens (SLF, SOD) | GitHub (PoPS Core, rpops, r.pops.spread) | full text | epidemics |
| `li2012consequences` | B (8) | Landscape fragmentation and Lyme risk | Lyme / I. ricinus, Belgium | no (Repast) | full text | epidemics |
| `smith2002predicting` | B (8) | Rabies on heterogeneous landscapes | raccoon rabies, Connecticut | dead link | full text | epidemics |
| `white2007modeling` | B (8) | Modeling epidemics using CA | generic SIR + vaccination | no | full text | epidemics |
| `bradshaw2023directionally` | B (7) | Directionally supervised Sahul CA | human colonisation, Sahul | GitHub + Zenodo | abstract + repo (provisional) | epidemics |
| `croft2020modelling` | B (7) | ASF in an isolated boar population | ASF, Forest of Dean (UK) | supplementary (Python 2) | full text (partial) | epidemics |
| `davidson2024methodological` | B (7) | Geographic Cell-DEVS disease models | COVID-19, Ontario regions | GitHub | abstract + repo docs (provisional) | epidemics |
| `martins2000cellular` | B (7) | CA for citrus variegated chlorosis | CVC in orange groves, São Paulo | no | full text (preprint) | epidemics |
| `ortigoza2020modelling` | B (7) | Chikungunya on triangular CA | chikungunya, Réunion | not public (C++) | full text | epidemics |
| `schimit2021model` | B (7) | PCA: social isolation, Brazil | COVID-19 | no | full text | epidemics |
| `biham1992selforganization` | A (9) | BML city traffic | 2D grid jamming | third-party JS | full text (r2) | movement |
| `nagel1992cellular` | A (9) | NaSch freeway CA | single-lane traffic | third-party (GitHub) | review full text (maerivoet2005) | movement |
| `nelson2019suite` | A (9) | Global accessibility indicators | travel time to settlements of 9 size classes | yes (R scripts, figshare) | full text (r2) | movement · r2 |
| `chowdhury1999selforganization` | B (8) | ChSch city CA | urban grid with signals | not found | full text | movement |
| `kirchner2002simulation` | B (8) | Bionics FFCA evacuation | room evacuation | not found | full text | movement |
| `kirchner2003friction` | B (8) | Friction & clogging in FFCA | bottleneck clogging | not found | full text | movement |
| `knospe2000towards` | B (8) | Brake-light (comfortable driving) CA | highway traffic phases | not found | full text | movement |
| `rickert1996two` | B (8) | Two-lane CA traffic | multi-lane traffic | not found | full text | movement |
| `weiss2020global` | B (8) | Travel time to healthcare | accessibility to hospitals/clinics, motorised and walking | stated on project page (not inspected) | full text (r2) | movement · r2 |
| `wood2012anisotropic` | B (8) | Anisotropic path tsunami evacuation | tsunami pedestrian evacuation time | closed (ArcGIS tool) | full text (r2) | movement |
| `korcek2012evolutionary` | B (7) | GA calibration of CA traffic, CZ data | road traffic, Czech road segments | not found | full text (r2) | movement · r2 |
| `weiss2018global` | B (7) | Global travel time to cities | accessibility | GEE assets (closed platform); data open | abstract + web summary (provisional) | movement |
| `ashton2006highangle` | A (10) | High-angle wave instability 1 | spits, capes, sand waves | cem-old (C) | full text (r2) | atmosphere-other |
| `palermo2024newts` | A (9) | NEWTS1.0 coastal erosion by waves | lake/sea coast erosion | USGS code release | full text | atmosphere-other |
| `ravazzani2011macroscopic` | A (9) | MCA for groundwater | unconfined aquifer flow | FEST repo (chiselapp) | abstract + model manual | atmosphere-other |
| `sharma2019understanding` | A (9) | Snow bedforms with sintering | snow dunes / wind drift | rescal-snow (GPL) | full text | atmosphere-other |
| `sievers2016cold (r2)` | B (8) | KLAM_21 cold air drainage model | cold-air drainage, ponding, urban ventilation | binary from DWD (closed) | full text (r2) | atmosphere-other |
| `sonnenschein2025hybrid` | B (8) | Hybrid CA air pollution for traffic | NO2 off-road dispersion | CellAutDisp (GPL-3.0, Python) | abstract + code repository (r2) | atmosphere-other |
| `ashton2001formation` | B (7) | Coastline features from high-angle waves | sandy coastline shape | cem-old (C) | abstract (provisional); model spec now via ashton2006high… | atmosphere-other |
| `bernhardt2010snowslide (r2)` | B (7) | SnowSlide gravitational snow transport | snow redistribution on steep terrain | Fortran on request; CHM reimplementation (GPL) | full text (r2) | atmosphere-other |
| `conrad2020coldairflow (r2)` | B (7) | SAGA Cold Air Flow tool (grey lit.) | cold-air drainage | SAGA GIS (GPL, C++) | code + documentation (r2) | atmosphere-other |
| `nowatschin2006gpubased (r2)` | B (7) | GPU cold air flow simulation | cold-air drainage with land use | not found | full text (r2) | atmosphere-other |
| `hagenzanker2009improved` | A (9) | Improved Fuzzy Kappa | validation metric | MATLAB, MIT (ahhz/fuzzy_kappa_matlab, verified) + MCK | full text (r2) | general |
| `pontius2011death` | A (9) | Death to Kappa | validation metric (quantity / allocation disagreement) | diffeR (R, CRAN/GitHub) | abstract (provisional) | general |
| `pontius2011comparison` | B (8) | Three maps at multiple resolutions | validation metric | diffeR (R) | abstract (provisional) | general |
| `pontius2014quantity` | B (8) | Quantity, exchange and shift components | validation metric | diffeR (R, verified functions) | metadata + diffeR source (provisional) | general · r2 |
| `hagenzanker2008neutral` | B (7) | Neutral models of landscape change as benchmarks | validation method (null models) | not found | full text | general · r2 |
| `vanvliet2011revisiting` | B (7) | Kappa Simulation | validation metric | MCK 3.2.2 (closed) | abstract (provisional) | general |

Horizon scan (`domains/new-phenomena.md`), class B: `patriarca2009influence` (language
competition over geography), `fernandezgracia2014voter` (voting patterns with commuting,
network of municipalities).

## Coverage of the longlist

*Best* = best class found; *Template* = recommended starting reference(s).

| Longlist | Proposed group | Best | Template | Comment |
|---|---|---|---|---|
| WAT water / flooding | core ★ | A | `callaghan2019computing`, `guidolin2016weighted`, `bates2010simple`, `shaw2021lisflood` | EA benchmark tests (`neelz2010benchmarking`) for validation. CZ: `landa2019smoderp2d` (B, open), `cirbus2013cellular`. |
| HAZ-01 wildfire | core ★ | A | `xia2025pytorchfire`, `trucchia2020propagator`, `pais2021cell2fire`, `freire2019using` | Firebrands: `hargrove2000simulating`, `lopezdecastro2024firespotting`. No CZ fire CA; calibration target `kudlackova2024using`. |
| ATM-02 cold-air pooling | core (proposed) | B | `nowatschin2006gpubased`, `conrad2020coldairflow`, `sievers2016cold` | Gap closed in round 2; CA-like grid models, not CA in the strict sense. |
| ECO-01 bark beetle | core (proposed) | A | `pietzsch2023nonparametric`, `liu2025multiscale`, `kautz2016dispersal` | CZ: `duraciova2020bark` (Bohemian Forest), `dolezal2016fine`, `berec2013population`. |
| LND-01 urban growth | core (proposed) | A | `clarke1997selfmodifying`, `roodposhti2020towards`, `petrasova2016open`, `liang2021understanding` | Central Europe: `koenig2011cellularautomatabased` (Vienna), `indrova2015land` (Prague). |
| MOV-03 accessibility (+ECO-04) | extension | A* | `nelson2019suite`*, `wood2012anisotropic`, `weiss2020global` | *Cost-distance, not CA. Lynx connectivity `kramerschadt2004fragmented`. |
| HAZ-02 landslide (+HAZ-03 avalanche) | extension | A | `damboise2022flowpy`, `wichmann2017gpp`, `dambrosio2003simulating`, `horton2013flowr` | Rockfall now covered (`wichmann2017gpp`). |
| MOV-01 evacuation | extension | B | `kirchner2002simulation`, `kirchner2003friction`, `wood2012anisotropic` | Test suite `ronchi2013process`. |
| ECO-03 invasive species | extension | B | `moenickes2013shapes`, `jones2021iteratively` | CZ: `nehrbass2007simulation`. |
| ATM-01 pollution / smoke | extension | B | `sonnenschein2025hybrid` | Open GPL code (CellAutDisp); street scale. |
| HYD-05 erosion / muddy floods | extension | A | `eltner2025using`, `landa2019smoderp2d` | Both with Czech (ČVUT) involvement. |
| URB-03 urban fire (→ HAZ-01) | scenario | C | `tan2019fire`, `ohgai2007cellular` | — |
| HYD-08 shoreline erosion † | not evaluated | A | `palermo2024newts`, `ashton2006highangle` | CZ abrasion method `slezingr2013verification`. |
| HYD-09 groundwater † | not evaluated | A | `ravazzani2011macroscopic` | Also `furnari2021asynchronous`, `mendicino2006threedimensional` (C). |
| HYD-10 oil spill † | not evaluated | D | `karafyllidis1997oil` | Nothing for rivers / lakes. |
| ECO-09 plant pest / pathogen † | not evaluated | A | `white2017modelling`, `jones2021iteratively` | Ash dieback `fritsch2026mechanistic` (C). |
| ATM-05 snow drift † | not evaluated | A | `sharma2019understanding` (3D), `bernhardt2010snowslide` (B, 2D) | — |
| EPI-04 population dispersal † | not evaluated | A | `bradshaw2021stochastic`, `gregoriodesouza2021reassessing` | Wolf `marucco2010predicting`, beaver `graham2022monitoring`, CZ beaver `john2010habitat`. |
| HAZ-05 lava | out of scope | A | `connor2012probabilistic`, `dietterich2017benchmarking` | Now A with code and benchmarks. |
| MOV-02 traffic | out of scope | A | `nagel1992cellular`, `biham1992selforganization`, `korcek2012evolutionary` | CZ-calibrated variant exists. |
| ECO-08 vegetation patterns | out of scope | A | `schneider2016spatially`, `kefi2007local`, `thiery1995model` | — |
| EPI-01 spatial epidemic | out of scope | B | `white2007modeling`, `davidson2024methodological` | — |
| EPI-02 ASF | out of scope | B | `croft2020modelling`, `smith2002predicting` | No pure CA; no CZ grid model. |
| EPI-03 tick risk | out of scope | B | `li2012consequences` | — |
| ECO-07 range shift | out of scope | B | `engler2012migclim`, `nobis2014kissmig` | — |
| ECO-02 succession | out of scope | B | `rademacher2004reconstructing` | — |
| HYD-07 morphodynamics | out of scope | B | `skinner2023testing`, `coulthard2013integrating` | — |
| HAZ-04 windthrow | out of scope | B | `seidl2014simulating` | Individual-tree; no windthrow CA found. |
| ECO-06 predator–prey | out of scope | C | `pascual2002cluster` | — |
| HYD-06 snowmelt | out of scope | C | `pardoiguzquiza2017estimation`, `colladoslara2019distributed` | Rules still unread. |
| URB-01 heat island | out of scope | C | `kazak2018use` | — |
| ATM-03 heavy gas | out of scope | C | `folch2009twodee2`, `folch2017highresolution` | Shallow-layer physics, not CA. |
| ATM-04, ECO-05, LND-02, URB-04 | out of scope | C or none | see domain files | Farmland abandonment: see `land-use.md` round-2 entries. |

## New phenomena candidates (round 2)

Collected from `domains/new-phenomena.md` and the "New phenomena candidates" sections of
the domain files. Not yet added to the longlist — **author decision pending**.

### Recommended by the horizon scan

| Proposed ID | Phenomenon | Best ref + class | CZ relevance |
|---|---|---|---|
| HAZ-06 | Surface subsidence above underground mining (incl. flooded troughs) | `chen2020dynamic` C | High — Ostrava–Karviná coal basin; chains to LND-03, HYD-09. |
| ECO-10 | Raised-bog patterning (hummock–hollow, string–flark) | `couwenberg2005selforganization` C | Bogs in Šumava, Krušné hory, Krkonoše. |
| HYD-11 | Riparian vegetation zones below regulated rivers | `ye2010modelling` C | Rivers below Czech dams (to be verified). |
| SOC-01 | Spatial competition of languages | `patriarca2009influence` B | Historical language border in Bohemia (to be verified). |
| SOC-02 | Voting patterns from imitation and commuting | `fernandezgracia2014voter` B | Czech election and commuting data (to be verified); network, not raster. |

### Other candidates with at least class B support

| Phenomenon | Best ref + class | Source file | Note |
|---|---|---|---|
| Rockfall runout | `wichmann2017gpp` B, `damboise2022flowpy` A | geomorphology | Could become a HAZ-02 scenario. |
| Collapse sinkholes | `yizhaq2017scalefree` B | geomorphology | — |
| Gravitational snow redistribution | `bernhardt2010snowslide` B | atmosphere-other | Close to ATM-05 / HAZ-03. |
| Cold-air ventilation corridors of towns | `sievers2016cold` B, `nowatschin2006gpubased` B | atmosphere-other | Urban scenario of ATM-02. |
| Wildlife rabies front with vaccination barriers | `smith2002predicting` B | epidemics | — |

### Borderline / weakly supported

Natural CO₂ degassing pooling in depressions (Cheb basin mofettes — CZ-specific;
`folch2009twodee2` C); cyanobacterial bloom drift (`ling2018modelling` C); livestock farm
epidemics (C); West Nile virus with migratory hosts (C); river-network colonisation (C);
WUI fire (C); crowd flows at mass events (C/D); deforestation frontier (C); residential
segregation on a real city (C); PV adoption diffusion (C); settlement redistribution (C);
earthquake SOC on fault grids (C); burglary hotspots (C); gentrification (C); dunes with
vegetation (C); periglacial sorted patterns (C); smouldering peat fire (C); shrub
encroachment (C); outdoor sound propagation (C); submerged lake vegetation (C).
Not suitable: real-estate investment, historical state expansion, pyroclastic flows (fold
into HAZ-05), tsunami, coral reefs, Balinese irrigation, soil salinisation.
No CA found: river-ice jams, wildlife–vehicle collisions, airborne spore incursion.

## Reusable building blocks and methods

- **Outflow distribution (minimisation of differences)** — `digregorio1999empirical`,
  `avolio2012theorem`; weighted variant `guidolin2016weighted` (open kernels).
- **Local inertial flow** — `bates2010simple`, `shaw2021lisflood`.
- **Gravitational runout with energy line** — `damboise2022flowpy`, `wichmann2017gpp`,
  `horton2013flowr` (avalanche, rockfall, debris flow).
- **Stochastic contagious spread** — `xia2025pytorchfire`, `alexandridis2008cellular`,
  `pietzsch2023nonparametric`, `white2017modelling`.
- **Front over a cost surface** — `wood2012anisotropic`, `nelson2019suite`; anisotropy
  correction `ghisu2015optimal`, `ghisu2015improved` (tables still unread), `pais2021cell2fire`.
- **Population growth + emigration** — `bradshaw2021stochastic`, `gregoriodesouza2021reassessing`.
- **Validation metrics** — `pontius2011death`, `pontius2011comparison`,
  `hagenzanker2009improved` (fuzzy kappa, open code), `hagenzanker2008neutral` (neutral
  models as benchmarks), `pontius2007comparing`, `varga2019intensity` (figure of merit).
- **Benchmarks** — `neelz2010benchmarking` (floods), `dietterich2017benchmarking` (lava),
  `ronchi2013process` (evacuation); analytical tests in `damboise2022flowpy`,
  `ravazzani2011macroscopic`, `palermo2024newts`.
- **Reference frameworks** (not scored) — Landlab / CellLab-CTS (`hobley2017creative`,
  `tucker2016celllab`), PCRaster (`karssenberg2010software`), OpenCAL (`derango2021opencal`).
- **Browser precedent** — `parise2012swii2` (WebGL CA, metadata only); no peer-reviewed
  fully in-browser geographic CA found.

## Observations relevant to the scope decision

Observations, **not decisions** — the grouping in `docs/review/evaluation-matrix.md` is
still pending author approval.

1. **All five proposed core models are now supported by class A or B references**,
   including ATM-02 after round 2.
2. **Czech-specific support** is strongest for WAT / HYD-05 (SMODERP2D, RillGrow data),
   ECO-01 (TANABBO, Šumava parameter studies) and traffic (Brno); weakest for fire and
   land use.
3. **Several "out of scope" items reach class A** (lava, traffic, vegetation patterns), and
   all † additions except oil spill have A-class support. If reimplementability is added
   as a criterion, the evaluation matrix should be revisited.
4. **Shared building blocks are confirmed by literature**: one gravity-flow family (water,
   debris, lava, snow, cold air), one stochastic-spread family (fire, beetle, pathogens),
   one front / cost-distance family, one population family.

## Quality control

Round 1:
- All 310 DOIs re-verified in Crossref (status, title similarity ≥ 0.6, year ± 1): no problems.
- 66 code URLs re-checked: all HTTP 200 except SourceForge (bot block, 403).
- Harmonisation: third-party-only code S3 = 1 (`alexandridis2008cellular`,
  `freire2019using` A → B; `kubo1996forest`, `pascual2002cluster` B → C);
  `kochanski2019rescal` aligned to the full-text assessment; key collisions resolved.

Round 2:
- All 105 new DOIs re-verified in Crossref with the same checks: no problems.
- 23 new code / grey-literature URLs re-checked: all reachable except SourceForge
  (saga-gis, bot block, 403); one false alarm (trailing character in a URL).
- Catalogue keys match BibTeX keys in every domain file; one duplicate between agents
  (`chen2020dynamic`, same DOI) merged.
- Grey literature without DOI (URL verified): `neelz2010benchmarking`,
  `clarke1994cellular`, `conrad2020coldairflow`.

Limitations: OpenAlex was quota-blocked for most of both rounds (Crossref and web search
were used instead, so keyword recall is lower); many publishers block automated full-text
access; temporary PDFs were extracted only outside the repository and deleted (a few
remain in the tool cache outside the repository).

## Round 3 — suggested tasks

1. **Manual full-text reading** of high-value provisional entries that automated access
   could not reach: `ghisu2015optimal` / `ghisu2015improved` (anisotropy tables),
   `alexandridis2008cellular` original, WCA2D paper text, SCIARA papers, snow-cover CA
   (`pardoiguzquiza2017estimation`), `nagel1992cellular` original,
   `couwenberg2005selforganization`. Best done by the author through university access.
2. Re-run keyword searches in OpenAlex (once the quota allows) as a recall check.
3. Decide on the new phenomena above and re-evaluate the matrix with reimplementability.
4. For each selected model, pick one primary reference and extract the exact rule and
   parameters into the model card.
