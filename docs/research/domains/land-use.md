# Land use and urban growth — literature survey

Survey round: 1 (breadth-first), date 2026-10-12. Scoring per ../reimplementability-criteria.md.

## Search log

Date: 2026-10-12. OpenAlex was the primary source for the first queries. After about 14 requests,
OpenAlex started returning HTTP 429: the free daily budget shared by the whole network IP was used
up, and it resets at midnight UTC. From then on, all search and **all metadata verification were
done through the Crossref REST API** (`/works?query.bibliographic=` and `/works/<DOI>`). Abstracts
came from Crossref, or from Semantic Scholar (abstract / TLDR field) where Crossref had none. Hit
counts for Crossref bibliographic queries are relevance-ranked totals over the whole index, so they
are not meaningful. Only the top 3–8 results were screened.

| Query | Source | Hits | Notes |
|---|---|---|---|
| SLEUTH urban growth cellular automaton self-modification | OpenAlex | 152 | SLEUTH applications; Zhou 2019 global SLEUTH |
| self-modifying cellular automaton historical urbanization San Francisco | OpenAlex | 483 | Clarke 1997, Clarke & Gaydos 1998, Li & Yeh 2002, Wu 2002 |
| cellular automata urban growth | OpenAlex | 13 800 | too broad when sorted by citations |
| constrained cellular automata land use | OpenAlex | 4 268 | (results lost to encoding error, re-run in Crossref) |
| CA-Markov land use change | OpenAlex | 38 794 | many applied CA–Markov case studies (Hamad 2018 etc.) |
| Dinamica EGO / ANN CA land use / calibration CA land use | OpenAlex | 3 638 / 5 707 / 4 867 | citation sort gave off-topic items; then rate limit |
| constrained CA high-resolution urban land-use dynamics White Engelen | Crossref | n/m | White 1993, White 1997, MOLAND chapters, Straatman 2004 |
| constrained CA sustainable urban development Li Yeh | Crossref | n/m | Li & Yeh 2000 |
| neural-network-based CA multiple land use | Crossref | n/m | Li & Yeh 2002 |
| calibration of stochastic CA rural-urban | Crossref | n/m | Wu 2002, Roodposhti 2020, Dietzel & Clarke 2006 |
| logistic-regression-based CA urban growth | Crossref | n/m | Mustafa 2017 (HUEM) |
| FLUS future land use simulation | Crossref | n/m | Liu 2017 |
| patch-generating land use simulation PLUS | Crossref | n/m | Liang 2021 |
| Dinamica (EGO) Soares-Filho | Crossref | n/m | Soares-Filho 2002 |
| SIMLANDER / open-source CA land-use model R | Crossref, web | n/m | Hewitt 2019 (SocArXiv), Hewitt 2017 |
| FUTURES Meentemeyer / r.futures GRASS | Crossref, GRASS manual | n/m | Meentemeyer 2013, Petrasova 2016 |
| random forest CA urban growth | Crossref | n/m | Kamusoko & Gamba 2015 |
| Jokar Arsanjani logistic Markov CA | Crossref | n/m | Jokar Arsanjani 2013 |
| Barredo MOLAND CA scenarios | Crossref | n/m | Barredo 2003 |
| Dietzel / Silva SLEUTH calibration | Crossref | n/m | Dietzel 2007, Silva & Clarke 2002 |
| Santé review urban CA | Crossref | n/m | Santé 2010, García 2011 |
| Verburg land use modelling review | Crossref | n/m | Verburg 2004 |
| Metronamica calibration | Crossref, GitHub | n/m | Newland 2018 |
| CA land use CORINE Europe / Urban Atlas | Crossref | n/m | Bastos Moroz 2024, Saganeiti 2021, Mustafa 2017/2018, Rienow 2015/2021 |
| urban sprawl CA Czech / suburbanisation Prague / Dyna-CLUE Czech | Crossref | n/m | Indrová & Kupková 2015 (Prague); Pokojska 2019 (Warsaw) |
| MOLUSCE QGIS plugin | Crossref, GitHub | n/m | Muhammad 2022; nextgis/qgis_molusce |
| GitHub repository search: "land use cellular automata", "urban growth cellular automata", "SLEUTH urban", "PLUS land use simulation", "molusce", "SIMLANDER", "Metronamica" | GitHub API | 30 / 15 / 11 / 4 / 11 / 2 / 4 | code links checked individually (HTTP 200) |

n/m = not meaningful (Crossref relevance total).

## Model families

1. **Rule-based urban growth CA with self-modification (SLEUTH family).** Binary urban/non-urban
   grid. Four growth rules are applied each year: spontaneous growth, new spreading centres, edge
   growth and road-influenced growth. They are controlled by five coefficients (dispersion, breed,
   spread, slope resistance, road gravity), and coefficients change themselves during boom and bust
   phases. Calibration is brute-force Monte Carlo against historical maps. The open C code, the demo
   data and the reference outputs make SLEUTH the most directly reimplementable classic.
   Keys: `clarke1997selfmodifying`, `clarke1998loose`, `silva2002calibration`,
   `dietzel2007toward`, `chaudhuri2019modeling`, `zhou2019highresolution`, `rienow2015supporting`.
2. **Constrained (demand-driven) multi-land-use CA (White–Engelen / MOLAND / Metronamica
   family).** Several active land uses compete for cells. Transition potential combines a weighted
   distance-decay neighbourhood effect (attraction or repulsion between land uses), suitability,
   zoning, accessibility and a Weibull-type random term. Cells are allocated by ranking until the
   exogenous demand per class is met. Commercial implementations (Metronamica) are closed. SIMLANDER
   (R) is an open, simplified re-implementation of the same logic.
   Keys: `white1993cellular`, `white1997use`, `barredo2003modelling`, `straatman2004towards`,
   `newland2018multiobjective`, `hewitt2019cellular`, `hewitt2017stable`, `roodposhti2020towards`.
3. **Statistically / ML-derived transition potential + CA.** Logistic regression, ANN, SVM or
   random forest estimates a development-probability surface from drivers such as distance to roads
   and centres, slope and zoning. A CA neighbourhood term and a stochastic term are multiplied in,
   and demand is often taken from a Markov chain.
   Keys: `wu2002calibration`, `li2000modelling`, `li2002neuralnetworkbased`,
   `jokararsanjani2013integration`, `kamusoko2015simulating`, `mustafa2017coupling`,
   `mustafa2018comparing`, `saganeiti2021modeling`, `bastosmoroz2024spatial`.
4. **CA–Markov.** A Markov chain gives class-to-class transition quantities. A CA filter, usually a
   5×5 contiguity filter, plus suitability maps place them in space. This approach is very
   widespread through IDRISI/TerrSet, the QGIS MOLUSCE plugin and Land Change Modeler, but papers
   seldom document the rules beyond the software defaults.
   Keys: `hamad2018predicting`, `muhammad2022spatiotemporal`, `indrova2015land` (LCM).
5. **Patch-based land-use CA (multi-class, demand-driven).** FLUS uses an ANN for suitability, plus
   an adaptive inertia term and a roulette wheel. PLUS adds random-forest rule mining on land
   expansion and multi-type random patch seeds with a descending threshold. FUTURES grows patches
   stochastically from a multilevel logistic potential. MUSE uses several patch generators.
   Keys: `liu2017future`, `liang2021understanding`, `meentemeyer2013futures`, `petrasova2016open`,
   `yang2023simulating`.
6. **Landscape-dynamics CA platforms.** DINAMICA / Dinamica EGO uses weights-of-evidence transition
   probabilities with expander and patcher functions. Key: `soaresfilho2002dinamica`.
7. **Non-CA allocation models used for the same questions (context only).** CLUE-S / Dyna-CLUE
   does iterative demand allocation over logistic suitability. It appears in the CZ and PL studies.
   Keys: `indrova2015land`, `pokojska2019simulating`.
8. **Reviews:** `sante2010cellular` (urban CA), `verburg2004land` (land-use modelling in general).

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| clarke1997selfmodifying | 1997 | Self-modifying CA, SF Bay (SLEUTH origin) | urban growth | square / Moore + road search / urban–non-urban (+LU via deltatron) / stochastic, Monte Carlo | 1 2 2 2 2 | 9 | A | C source (Gigalopolis, verified) | paywall | abstract + official docs |
| clarke1998loose | 1998 | Loose-coupling CA and GIS, SF & Washington/Baltimore | urban growth | as SLEUTH | 1 1 2 1 1 | 6 | C | SLEUTH code | paywall | abstract (TLDR) |
| silva2002calibration | 2002 | SLEUTH calibration Lisbon & Porto | urban growth (EU) | as SLEUTH | 1 1 2 1 1 | 6 | C | SLEUTH code | paywall | metadata only (provisional) |
| dietzel2007toward | 2007 | Optimal calibration of SLEUTH (OSM metric) | calibration | as SLEUTH | 1 1 2 1 1 | 6 | C | SLEUTH code | paywall | abstract (provisional) |
| chaudhuri2019modeling | 2019 | Adapting SLEUTH for Kolkata | urban growth | as SLEUTH, 100 m | 1 1 2 1 1 | 6 | C | SLEUTH code | OA (green) | full text (partial reading) |
| zhou2019highresolution | 2019 | Global SLEUTH projection (GUGPS) | urban growth, global | SLEUTH, 30″ grid, per-window calibration | 1 2 2 1 2 | 8 | B | R scripts + modified SLEUTH (figshare) | OA | full text |
| rienow2015supporting | 2015 | Supporting SLEUTH with SVM | urban growth (EU?) | SLEUTH + SVM probability | 1 1 1 1 1 | 5 | C | not found | paywall | metadata only (provisional) |
| white1993cellular | 1993 | CA and fractal urban form | urban land-use pattern | square / large radius / several LU / stochastic | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| white1997use | 1997 | Constrained CA, Cincinnati | urban land use | square / 113-cell circular / multi-LU / stochastic, demand-constrained | 1 1 1 1 1 | 5 | C | closed (Metronamica lineage) | paywall | abstract (provisional) |
| barredo2003modelling | 2003 | MOLAND urban scenarios via CA | urban land use (EU) | constrained CA, multi-LU | 1 1 1 1 1 | 5 | C | closed | paywall | abstract (TLDR) |
| straatman2004towards | 2004 | Automatic calibration of constrained CA | calibration | additive neighbourhood rules | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (TLDR) |
| li2000modelling | 2000 | Constrained CA + GIS for sustainable development | urban growth | constrained (environmental) CA | 1 1 0 1 1 | 4 | C | not found | paywall | metadata only (provisional) |
| li2002neuralnetworkbased | 2002 | ANN-based CA, multiple land uses | multi-LU change | ANN transition probabilities, stochastic | 1 1 0 1 1 | 4 | C | not found | OA (bronze, publisher) | abstract (TLDR) |
| wu2002calibration | 2002 | Calibration of stochastic CA, rural–urban | urban conversion | logistic initial probability + dynamic neighbourhood, stochastic | 1 1 0 1 1 | 4 | C | not found | OA (bronze, publisher) | abstract (TLDR) |
| jokararsanjani2013integration | 2013 | Logistic + Markov + CA, Tehran | urban expansion | logistic suitability + Markov quantity + CA | 1 1 1 1 1 | 5 | C | closed tools | paywall | abstract (TLDR) |
| hamad2018predicting | 2018 | CA-Markov scenarios, Kurdistan NP | LULC change | CA-Markov | 1 1 0 1 1 | 4 | C | not found | OA | abstract |
| kamusoko2015simulating | 2015 | RF-CA urban growth | urban growth | RF potential + CA | 1 1 0 1 2 | 5 | C | not found | OA | abstract |
| liu2017future | 2017 | FLUS model | multi-LU scenarios | ANN suitability + inertia + roulette CA | 1 1 1 1 1 | 5 | C | binary software (site unreachable) | paywall | abstract (TLDR) |
| liang2021understanding | 2021 | PLUS model, Wuhan | multi-LU change | 30 m / 3×3 Moore / 7 LU / stochastic patch seeds | 1 2 1 1 2 | 7 | B | Windows binary on GitHub (verified) | preprint (arXiv) | full text |
| soaresfilho2002dinamica | 2002 | DINAMICA, Amazon frontier | deforestation / landscape | stochastic CA, expander/patcher | 1 1 1 1 1 | 5 | C | Dinamica EGO (free, closed) | paywall | abstract (TLDR) |
| meentemeyer2013futures | 2013 | FUTURES patch-growing | urban–rural growth | stochastic patch growing on logistic potential | 1 1 2 1 1 | 6 | C | GRASS add-on r.futures (verified) | paywall | metadata + GRASS manual |
| petrasova2016open | 2016 | FUTURES in GRASS GIS (open source) | urban growth | 30 m, patch growing, demand by subregion | 1 2 2 2 1 | 8 | B | r.futures (verified) | OA | full text |
| hewitt2019cellular | 2019 | SIMLANDER R CA model | urban / multi-LU | constrained CA (N·A·S·v), demand allocation | 1 1 2 2 1 | 7 | B | R script + demo data (verified download) | OA (preprint) | abstract + project site |
| roodposhti2020towards | 2020 | Automatic calibration of neighbourhood (SIMLANDER) | urban growth | 300 m / up to 11×11 distance-decay / urban–non-urban / Weibull noise | 2 2 2 2 2 | 10 | A | SIMLANDER (verified) + suppl. script | OA (accepted ms) | full text |
| hewitt2017stable | 2017 | Sensitivity analysis of CA urban model | urban LU (EU?) | constrained CA | 1 1 2 1 1 | 6 | C | SIMLANDER | paywall | metadata only (provisional) |
| newland2018multiobjective | 2018 | Multi-objective calibration of CA LU models | calibration | Metronamica-type constrained CA | 1 1 1 1 1 | 5 | C | optimiser repo (verified), model closed | paywall | metadata only (provisional) |
| mustafa2017coupling | 2017 | HUEM: ABM + CA + logit, Wallonia | urban expansion (EU) | 100 m CORINE / radius 1–8 / urban–non-urban / stochastic, GA calibration | 1 2 0 1 2 | 6 | C | not found | OA (green preprint) | full text |
| mustafa2018comparing | 2018 | CA-SVM vs CA-logit, Wallonia | urban LU change (EU) | ML potential + CA | 1 1 0 1 1 | 4 | C | not found | OA (CC BY) | abstract |
| bastosmoroz2024spatial | 2024 | Spatial constraints in CA urban growth models | urban growth | ML classifiers + CA | 1 1 2 1 1 | 6 | C | Mendeley Data, CC BY (verified) | paywall | metadata + data repo |
| yang2023simulating | 2023 | Urban demand explicit CA (MUSE) | urban expansion | patch-generating CA engines | 1 1 2 1 1 | 6 | C | MUSE, Python, MIT (verified) | paywall | metadata + repo README |
| saganeiti2021modeling | 2021 | Urban sprinkling CA, Basilicata | dispersed urbanisation (EU) | CA + multinomial logit, building density | 1 1 0 1 1 | 4 | C | not found | paywall | abstract |
| indrova2015land | 2015 | Prague suburban LU prediction (LCM vs Dyna-CLUE) | suburbanisation (CZ) | LCM (MLP + Markov) / Dyna-CLUE allocation | 0 1 1 1 1 | 4 | C | commercial / free closed | OA | full text |
| pokojska2019simulating | 2019 | Dyna-CLUE, Warsaw metropolitan area | suburbanisation (EU) | Dyna-CLUE allocation | 0 1 1 1 1 | 4 | C | free closed | OA | abstract |
| muhammad2022spatiotemporal | 2022 | CA-ANN in QGIS MOLUSCE, Linyi | LULC change | MOLUSCE CA-ANN | 1 1 2 1 1 | 6 | C | qgis_molusce GPL-2 (verified) | OA | abstract |
| sante2010cellular | 2010 | Review: urban CA for real-world processes | review | – | n/a | – | n/a | – | paywall | abstract (TLDR) |
| verburg2004land | 2004 | Land use change modelling: practice & priorities | review | – | n/a | – | n/a | – | OA (green) | metadata |

## Entries

### clarke1997selfmodifying — A Self-Modifying Cellular Automaton Model of Historical Urbanization in the San Francisco Bay Area
- **Citation:** Clarke, K.C., Hoppen, S., Gaydos, L. (1997). A Self-Modifying Cellular Automaton Model of Historical Urbanization in the San Francisco Bay Area. *Environment and Planning B: Planning and Design*, 24(2), 247–261. DOI: 10.1068/b240247 (verified: Crossref; also seen in OpenAlex before rate limit)
- **Access:** paywall. The official documentation (Project Gigalopolis, https://www.ncgia.ucsb.edu/projects/gig/) is open.
- **Phenomenon and study area:** historical urbanisation of the San Francisco Bay Area from 1900, calibrated against maps of 1940–1990.
- **Model:** urban/non-urban cells. Each annual cycle applies four rules in order: spontaneous growth (random cells), new spreading centres (some spontaneous cells start clusters), edge growth (cells next to existing urban cells) and road-influenced growth (search along roads, then local spread). Slope reduces the probability of growth above a critical slope, and excluded areas are never urbanised. Coefficients self-modify: if the yearly growth rate goes above a critical-high threshold, dispersion, breed and spread are multiplied by a factor above 1; below critical-low they are multiplied by a factor below 1. Monte Carlo repetitions give probability maps. In the paper itself, verified only at abstract level.
- **Inputs:** Slope, Land use, Exclusion, Urban extent (several dates), Transportation and Hillshade (the "SLEUTH" acronym).
- **Parameters:** five coefficients (0–100) plus self-modification constants in a scenario file. Brute-force calibration (coarse → fine → final) against historical urban extents, using a set of fit statistics, is documented on the project site.
- **Code:** SLEUTH 3.0 C source, tarball https://www.ncgia.ucsb.edu/projects/gig/Dnload/SLEUTH3.0beta_p01.tar.gz (HTTP 200, about 4.8 MB, not downloaded). Also SLEUTH-3r at https://egscbeowulf.er.usgs.gov/geninfo/downloads (200). The Python wrapper sostenibilidad-unam/sleuth_automation is on GitHub.
- **Validation:** fit to historical maps. The distribution includes the `demo200` test scenario with expected outputs for checking an installation (https://www.ncgia.ucsb.edu/projects/gig/Imp/imVerTestResults.htm).
- **Reimplementability:** S1 1 – the paper (paywalled) is not fully specified, but the open C code plus web documentation define the rules, so S1 would be 2 if the code is taken as the specification. S2 2 – calibration procedure fully documented. S3 2 – open source. S4 2 – generic layers (urban extent, roads, slope, exclusion) plus demo data. S5 2 – demo reference outputs and calibration statistics → 9, A. Assessed from: abstract + official documentation.
- **Browser fit:** very good. Binary grid, simple local rules; a few hundred thousand cells × 30–50 years × 10–100 Monte Carlo runs is feasible in JS / WebGL. Brute-force calibration would have to be offline or reduced.
- **Relevance to ca-geo:** LND-01 (urban growth / suburbanisation) primary candidate. Inputs map well to CZ data: urban extent from CORINE / Urban Atlas, roads, a DEM-derived slope, exclusion from protected areas and water. Also feeds chain L8.

### clarke1998loose — Loose-coupling a cellular automaton model and GIS
- **Citation:** Clarke, K.C., Gaydos, L.J. (1998). Loose-coupling a cellular automaton model and GIS: long-term urban growth prediction for San Francisco and Washington/Baltimore. *International Journal of Geographical Information Science*, 12(7), 699–714. DOI: 10.1080/136588198241617 (verified: Crossref)
- **Access:** paywall (the publisher PDF is listed as OA in OpenAlex, but access was blocked).
- **Phenomenon and study area:** long-term urban growth forecasts for two US regions.
- **Model:** the SLEUTH (then "UGM") CA, coupled loosely with GIS for data preparation and display.
- **Inputs:** historical urban maps, roads, slope, exclusion.
- **Parameters:** calibrated from historical maps; values not checked.
- **Code:** SLEUTH code (see above).
- **Validation:** calibration against historical urban extents.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** as SLEUTH.
- **Relevance to ca-geo:** LND-01. A second classic reference for SLEUTH and for the GIS-coupling architecture.

### silva2002calibration — Calibration of the SLEUTH urban growth model for Lisbon and Porto, Portugal
- **Citation:** Silva, E.A., Clarke, K.C. (2002). Calibration of the SLEUTH urban growth model for Lisbon and Porto, Portugal. *Computers, Environment and Urban Systems*, 26(6), 525–552. DOI: 10.1016/s0198-9715(01)00014-x (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban growth of two Portuguese metropolitan areas (EU).
- **Model:** SLEUTH. The paper is the standard reference for sequential brute-force calibration (it is cited for this in chaudhuri2019modeling).
- **Inputs:** SLEUTH layers for Lisbon / Porto.
- **Parameters:** calibrated coefficient sets for both cities are expected but were not seen.
- **Code:** SLEUTH code.
- **Validation:** calibration statistics.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: metadata only (provisional; no abstract was available).
- **Browser fit:** as SLEUTH.
- **Relevance to ca-geo:** LND-01; a European calibration precedent. Worth reading in full in round 2 for coefficient values for comparable European cities.

### dietzel2007toward — Toward Optimal Calibration of the SLEUTH Land Use Change Model
- **Citation:** Dietzel, C., Clarke, K.C. (2007). Toward Optimal Calibration of the SLEUTH Land Use Change Model. *Transactions in GIS*, 11(1), 29–45. DOI: 10.1111/j.1467-9671.2007.01031.x (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** methodological work on SLEUTH calibration.
- **Model:** runs the full brute-force parameter space and reduces it with a self-organising map. Proposes one composite metric (the "Optimal SLEUTH Metric", OSM) to replace the 13 standard fit statistics.
- **Inputs:** a SLEUTH test region.
- **Parameters:** the paper is about the calibration procedure itself.
- **Code:** SLEUTH code.
- **Validation:** comparison of the metrics.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** the metric is cheap to compute; the brute-force search is not suited to the browser.
- **Relevance to ca-geo:** LND-01. Gives a single goodness-of-fit score that a demo could show after a historical back-cast.

### chaudhuri2019modeling — Modeling an Indian megalopolis – A case study on adapting SLEUTH urban growth model
- **Citation:** Chaudhuri, G., Clarke, K.C. (2019). Modeling an Indian megalopolis– A case study on adapting SLEUTH urban growth model. *Computers, Environment and Urban Systems*, 77, 101358. DOI: 10.1016/j.compenvurbsys.2019.101358 (verified: Crossref)
- **Access:** OA (green) at https://escholarship.org/content/qt0rr18266/qt0rr18266.pdf
- **Phenomenon and study area:** urban growth of the Kolkata urban agglomeration.
- **Model:** SLEUTH with modified exclusion and slope layers. Socio-economic drivers and road centrality (degree centrality in a dual graph) are encoded in these layers. The paper restates the four growth rules, the five coefficients and the critical-slope logic (no growth above about 25–30 % slope).
- **Inputs:** 100 m layers (urban extent, roads from OSM / DIVA-GIS, rail, towns, river, slope).
- **Parameters:** sequential brute-force calibration with the OSM metric. The table of values was not checked in this round.
- **Code:** SLEUTH code.
- **Validation:** calibration and validation against observed growth.
- **Reimplementability:** S1 1 – readable restatement of the rules, but details are left to SLEUTH documentation; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: full text (partial reading).
- **Browser fit:** as SLEUTH.
- **Relevance to ca-geo:** LND-01. Shows how to put extra drivers into SLEUTH through the exclusion and slope layers, a cheap trick for CZ planning layers.

### zhou2019highresolution — High-resolution global urban growth projection based on multiple applications of the SLEUTH urban growth model
- **Citation:** Zhou, Y., Varquez, A.C.G., Kanda, M. (2019). High-resolution global urban growth projection based on multiple applications of the SLEUTH urban growth model. *Scientific Data*, 6(1), 34. DOI: 10.1038/s41597-019-0048-z (verified: Crossref; also seen in OpenAlex)
- **Access:** OA.
- **Phenomenon and study area:** global urban growth 2020–2050, run in 50′ windows on a 30″ grid.
- **Model:** SLEUTH calibrated per window over 2000–2013. Urban cover is proxied from LandScan population. Windows with a low urban growth index use a simplified calibration with dispersion, breed and spread fixed at 1. Runs were automated with sleuth-automation.
- **Inputs:** LandScan-derived urban maps, roads (gROADS + OSM), slope, exclusion.
- **Parameters:** calibration procedure fully described (full vs simplified mode, thresholds).
- **Code:** R scripts and modified SLEUTH on figshare, DOI 10.26188/5c2c5d0ed52d7 (https://figshare.unimelb.edu.au/articles/code/Source_code_for_GUGPS_dataset/7539113 answered HTTP 202, so it exists).
- **Validation:** comparison with independent urban extent products (MODIS etc.). Annual GeoTIFF probability maps are published.
- **Reimplementability:** S1 1 (rules by reference to SLEUTH); S2 2; S3 2; S4 1 (LandScan is licensed, not fully open); S5 2 (a published global output dataset covering Czechia can serve as a reference) → 8, B. Assessed from: full text.
- **Browser fit:** one window (about 100 × 100 km at 1 km) is very light.
- **Relevance to ca-geo:** LND-01. The GUGPS probability rasters for Czechia could serve as a ready-made comparison layer.

### rienow2015supporting — Supporting SLEUTH – Enhancing a cellular automaton with support vector machines for urban growth modeling
- **Citation:** Rienow, A., Goetzke, R. (2015). Supporting SLEUTH – Enhancing a cellular automaton with support vector machines for urban growth modeling. *Computers, Environment and Urban Systems*, 49, 66–81. DOI: 10.1016/j.compenvurbsys.2014.05.001 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban growth. Web search links the same author's dissertation to the Ruhr area (Germany), but the study area of this paper was not confirmed.
- **Model:** SLEUTH with an SVM-derived suitability or probability layer added.
- **Inputs:** not checked.
- **Parameters:** not checked.
- **Code:** not found (SLEUTH itself is open).
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: metadata only (provisional).
- **Browser fit:** SVM inference on precomputed rasters is fine; training would be offline.
- **Relevance to ca-geo:** LND-01; a possible German (EU) SLEUTH precedent. Verify in round 2.

### white1993cellular — Cellular Automata and Fractal Urban Form
- **Citation:** White, R., Engelen, G. (1993). Cellular Automata and Fractal Urban Form: A Cellular Modelling Approach to the Evolution of Urban Land-Use Patterns. *Environment and Planning A: Economy and Space*, 25(8), 1175–1199. DOI: 10.1068/a251175 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** emergence of urban land-use structure, compared with fractal dimensions of US cities.
- **Model:** multi-state land-use CA with a distance-weighted neighbourhood. Realistic parameter values produce fractal or bifractal patterns. Precursor of the constrained CA family.
- **Inputs:** largely stylised; data on US cities used for comparison only.
- **Parameters:** not checked.
- **Code:** not found.
- **Validation:** fractal dimension comparison.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** excellent. A synthetic grid works as an interactive teaching toy.
- **Relevance to ca-geo:** LND-01 (didactic variant). Neighbourhood attraction/repulsion as an intuitive demo.

### white1997use — The Use of Constrained Cellular Automata for High-Resolution Modelling of Urban Land-Use Dynamics
- **Citation:** White, R., Engelen, G., Uljee, I. (1997). The Use of Constrained Cellular Automata for High-Resolution Modelling of Urban Land-Use Dynamics. *Environment and Planning B: Planning and Design*, 24(3), 323–343. DOI: 10.1068/b240323 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** land-use pattern of Cincinnati, Ohio.
- **Model:** cell states are land uses. Transition potential is a function of the land uses in a 113-cell circular neighbourhood and of the cell's suitability for each use. Total cells per land use is constrained exogenously ("constrained CA"), and a random term is included. Sensitivity analysis is reported.
- **Inputs:** land-use map, suitability.
- **Parameters:** neighbourhood weight functions per pair of land uses (many parameters); values not checked.
- **Code:** no open code; this lineage is implemented in commercial Metronamica (closed).
- **Validation:** visual realism and sensitivity analysis (from the abstract).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract (provisional). The same rule structure is fully written out in roodposhti2020towards and hewitt2019cellular.
- **Browser fit:** good; a 113-cell kernel per class is fine on GPU.
- **Relevance to ca-geo:** LND-01 and LND-02 (multi-class competition: urban vs agriculture vs forest vs abandonment). The conceptual core for a multi-land-use demo.

### barredo2003modelling — Modelling dynamic spatial processes: simulation of urban future scenarios through cellular automata
- **Citation:** Barredo, J.I., Kasanko, M., McCormick, N., Lavalle, C. (2003). Modelling dynamic spatial processes: simulation of urban future scenarios through cellular automata. *Landscape and Urban Planning*, 64(3), 145–160. DOI: 10.1016/s0169-2046(02)00218-9 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** future urban land-use scenarios for a European city, produced by EC JRC (MOLAND). The specific city was not confirmed from metadata.
- **Model:** bottom-up constrained CA that integrates land-use factors (suitability, zoning, accessibility, neighbourhood).
- **Inputs:** MOLAND land-use database (high-resolution urban land use).
- **Parameters:** not checked.
- **Code:** closed (MOLAND / Metronamica-type).
- **Validation:** reported as realistic and relatively accurate (TLDR).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** as constrained CA.
- **Relevance to ca-geo:** LND-01; the EU / JRC lineage that led to Urban Atlas-based modelling. Round 2: check whether the MOLAND class scheme maps onto Urban Atlas.

### straatman2004towards — Towards an automatic calibration procedure for constrained cellular automata
- **Citation:** Straatman, B., White, R., Engelen, G. (2004). Towards an automatic calibration procedure for constrained cellular automata. *Computers, Environment and Urban Systems*, 28(1–2), 149–170. DOI: 10.1016/s0198-9715(02)00068-6 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** calibration methodology.
- **Model:** for CA with additive transition rules, randomly generated rule sets are systematically modified until they reproduce a series of test maps.
- **Inputs:** test map series.
- **Parameters:** the paper is itself a calibration procedure.
- **Code:** not found.
- **Validation:** replication of test maps.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** iterative calibration would be offline.
- **Relevance to ca-geo:** background for calibrating neighbourhood rules; see roodposhti2020towards for an open, documented alternative.

### li2000modelling — Modelling sustainable urban development by the integration of constrained cellular automata and GIS
- **Citation:** Li, X., Yeh, A.G.O. (2000). Modelling sustainable urban development by the integration of constrained cellular automata and GIS. *International Journal of Geographical Information Science*, 14(2), 131–152. DOI: 10.1080/136588100240886 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban development under environmental constraints in a fast-growing area of southern China (study area not confirmed from metadata).
- **Model:** CA whose development probability is reduced by environmental and agricultural constraint scores, used to compare development forms.
- **Inputs:** not checked.
- **Parameters:** not checked.
- **Code:** not found.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: metadata only (provisional).
- **Browser fit:** good.
- **Relevance to ca-geo:** LND-01 scenario idea, for example protecting high-quality farmland (in CZ the soil-protection classes BPEJ) as a constraint layer.

### li2002neuralnetworkbased — Neural-network-based cellular automata for simulating multiple land use changes using GIS
- **Citation:** Li, X., Yeh, A.G.O. (2002). Neural-network-based cellular automata for simulating multiple land use changes using GIS. *International Journal of Geographical Information Science*, 16(4), 323–343. DOI: 10.1080/13658810210137004 (verified: Crossref)
- **Access:** listed as bronze OA at the publisher; automated access was blocked.
- **Phenomenon and study area:** multiple land-use changes in a fast-growing area of southern China.
- **Model:** a three-layer neural network with one output neuron per land use gives competing conversion probabilities. A stochastic CA step converts cells.
- **Inputs:** GIS driver layers and land-use maps.
- **Parameters:** ANN weights trained from data.
- **Code:** not found.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** fine with precomputed probability rasters; training offline.
- **Relevance to ca-geo:** origin of the ANN-CA design used in FLUS and MOLUSCE.

### wu2002calibration — Calibration of stochastic cellular automata: the application to rural-urban land conversions
- **Citation:** Wu, F. (2002). Calibration of stochastic cellular automata: the application to rural-urban land conversions. *International Journal of Geographical Information Science*, 16(8), 795–818. DOI: 10.1080/13658810210157769 (verified: Crossref)
- **Access:** listed as bronze OA at the publisher; automated access was blocked.
- **Phenomenon and study area:** rural-to-urban land conversion (Chinese city; not confirmed).
- **Model:** initial conversion probability from observed land-use data (logistic). It is updated each step from the strength of neighbourhood development, followed by a stochastic conversion.
- **Inputs:** sequential land-use maps and drivers.
- **Parameters:** calibrated from data.
- **Code:** not found.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** good.
- **Relevance to ca-geo:** the template "logistic probability × neighbourhood × random" that most later CA follow; easy to build on CZ layers.

### jokararsanjani2013integration — Integration of logistic regression, Markov chain and cellular automata models to simulate urban expansion
- **Citation:** Jokar Arsanjani, J., Helbich, M., Kainz, W., Darvishi Boloorani, A. (2013). Integration of logistic regression, Markov chain and cellular automata models to simulate urban expansion. *International Journal of Applied Earth Observation and Geoinformation*, 21, 265–275. DOI: 10.1016/j.jag.2011.12.014 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** built-up expansion of Tehran, with projections to 2016 and 2026.
- **Model:** logistic regression gives the probability surface, a Markov chain gives quantities, and a CA allocates.
- **Inputs:** multi-date land-use maps, drivers.
- **Parameters:** regression coefficients (from data).
- **Code:** closed GIS tools (not verified).
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** good.
- **Relevance to ca-geo:** LND-01; a widely cited "hybrid" template.

### hamad2018predicting — Predicting Land Use/Land Cover Changes Using a CA-Markov Model under Two Different Scenarios
- **Citation:** Hamad, R., Balzter, H., Kolo, K. (2018). Predicting Land Use/Land Cover Changes Using a CA-Markov Model under Two Different Scenarios. *Sustainability*, 10(10), 3421. DOI: 10.3390/su10103421 (verified: Crossref; also seen in OpenAlex)
- **Access:** OA (MDPI; automated full-text access blocked).
- **Phenomenon and study area:** land-use/land-cover dynamics of a national park core zone in Kurdistan (Iraq), Landsat 1993–2017, two business-as-usual scenarios.
- **Model:** a CA-Markov chain projects the class transition matrix; a CA allocates.
- **Inputs:** classified Landsat time series.
- **Parameters:** transition matrices from the data.
- **Code:** not found; CA-Markov is typically run in commercial IDRISI/TerrSet (not verified for this paper).
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract.
- **Browser fit:** trivial.
- **Relevance to ca-geo:** a representative of the very common CA–Markov family. Useful as a baseline demo with CORINE transitions 2000→2018, but scientifically thin.

### kamusoko2015simulating — Simulating Urban Growth Using a Random Forest-Cellular Automata (RF-CA) Model
- **Citation:** Kamusoko, C., Gamba, J. (2015). Simulating Urban Growth Using a Random Forest-Cellular Automata (RF-CA) Model. *ISPRS International Journal of Geo-Information*, 4(2), 447–470. DOI: 10.3390/ijgi4020447 (verified: Crossref)
- **Access:** OA (MDPI; automated full-text access blocked).
- **Phenomenon and study area:** urban growth (built-up vs non-built-up), African metropolitan area (not confirmed).
- **Model:** a random forest transition potential plus CA allocation, compared with SVM-CA and LR-CA.
- **Inputs:** land-cover maps and drivers.
- **Parameters:** RF hyper-parameters; not checked.
- **Code:** not found.
- **Validation:** Kappa-simulation 0.51 and figure of merit 47 % for RF-CA, versus 0.39 / 39 % for SVM-CA and −0.22 / 6 % for LR-CA (from the abstract).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 2 → 5, C. Assessed from: abstract.
- **Browser fit:** fine with precomputed RF probability maps.
- **Relevance to ca-geo:** LND-01; the validation metrics (Kappa-simulation, figure of merit) are worth adopting.

### liu2017future — A future land use simulation model (FLUS)
- **Citation:** Liu, X., Liang, X., Li, X., Xu, X., Ou, J., Chen, Y., Li, S., Wang, S., Pei, F. (2017). A future land use simulation model (FLUS) for simulating multiple land use scenarios by coupling human and natural effects. *Landscape and Urban Planning*, 168, 94–116. DOI: 10.1016/j.landurbplan.2017.09.019 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** long-term trajectories of multiple land uses under scenarios (China).
- **Model:** ANN-derived suitability for each class. A CA uses neighbourhood effects, an adaptive inertia coefficient and roulette-wheel competition. Reported as more accurate than CLUE-S and plain CA (TLDR). PLUS (liang2021understanding) restates the FLUS equations.
- **Inputs:** land-use maps and drivers.
- **Parameters:** not checked.
- **Code:** GeoSOS-FLUS software (Windows binary). The project URL http://www.geosimulation.cn/FLUS.html did not respond, so the code is not verified.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** good (roulette per cell, several classes).
- **Relevance to ca-geo:** LND-01 / LND-02 multi-class scenarios.

### liang2021understanding — Understanding the drivers of sustainable land expansion using a patch-generating land use simulation (PLUS) model
- **Citation:** Liang, X., Guan, Q., Clarke, K.C., Liu, S., Wang, B., Yao, Y. (2021). Understanding the drivers of sustainable land expansion using a patch-generating land use simulation (PLUS) model: A case study in Wuhan, China. *Computers, Environment and Urban Systems*, 85, 101569. DOI: 10.1016/j.compenvurbsys.2020.101569 (verified: Crossref)
- **Access:** preprint, arXiv:2010.11541 (https://arxiv.org/abs/2010.11541).
- **Phenomenon and study area:** seven land-use classes in Wuhan, 2003–2013 calibration, scenarios to 2035.
- **Model:** (1) LEAS: a random forest classifier per class is trained on cells that converted to that class, giving a growth probability per class. (2) CARS: overall probability = growth probability × neighbourhood share of that class in an n×n window (with class weights) × an adaptive demand coefficient (inertia rule as in FLUS). Roulette-wheel selection follows. Where the neighbourhood share is 0, new patches can be seeded by Monte Carlo when the growth probability exceeds a random-scaled threshold. A descending threshold (decay factor, decay steps) limits conversions, and a conversion matrix forbids some transitions. Iterations continue until demand is met. Boundary handling and the exact iteration and update order are not explicit.
- **Inputs:** 30 m land use (2931 × 2931 cells); 14 drivers (roads, rail, distance to government, population, GDP, soil, climate, DEM, slope) from OSM, SRTM, WorldClim and Chinese sources.
- **Parameters:** 3×3 Moore neighbourhood, patch-seed threshold 0.1, decay factor 0.9, demand step 500, RF with 50 trees and 5 % sampling. Set by trial and error.
- **Code:** https://github.com/HPSCIL/Patch-generating_Land_Use_Simulation_Model (verified). It contains a Windows executable, test data and tutorials, but no source code. A third-party "clean-room Python approximation" exists (ranielZhang/openplus-landuse-python, not assessed).
- **Validation:** figure of merit (FoM) 0.2642 for PLUS vs FLUS and two reduced variants; landscape metrics.
- **Reimplementability:** S1 1 – equations given but some update details unclear; S2 2 – all parameters listed; S3 1 – binary only; S4 1 – the land-use product is not openly linked (drivers mostly open); S5 2 – FoM values → 7, B. Assessed from: full text (arXiv preprint).
- **Browser fit:** CA part feasible (a few million cells, roulette wheel). RF probabilities would be precomputed offline.
- **Relevance to ca-geo:** LND-01 and LND-02. Its patch-seed mechanism gives realistic new settlements and forest patches. A candidate for a multi-class CORINE demo, with CORINE 2000/2006 for calibration and 2012/2018 for validation.

### soaresfilho2002dinamica — dinamica — a stochastic cellular automata model designed to simulate the landscape dynamics in an Amazonian colonization frontier
- **Citation:** Soares-Filho, B.S., Coutinho Cerqueira, G., Lopes Pennachin, C. (2002). dinamica—a stochastic cellular automata model designed to simulate the landscape dynamics in an Amazonian colonization frontier. *Ecological Modelling*, 154(3), 217–235. DOI: 10.1016/s0304-3800(02)00059-5 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** deforestation and land-use dynamics at a smallholder colonisation frontier, Amazonia.
- **Model:** stochastic CA. Transition probabilities from weights of evidence; "expander" (growth of existing patches) and "patcher" (new patches) transition functions (from general knowledge of the platform; detail not checked here).
- **Inputs:** land-cover maps and drivers.
- **Parameters:** not checked.
- **Code:** Dinamica EGO is free but closed source (https://dinamicaego.com, HTTP 200).
- **Validation:** spatial pattern validation reported as good (TLDR).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract (TLDR, provisional).
- **Browser fit:** good.
- **Relevance to ca-geo:** the expander/patcher idea also suits LND-02 (forest regrowth patches). Overlaps with the eco domain.

### meentemeyer2013futures — FUTURES: Multilevel Simulations of Emerging Urban–Rural Landscape Structure Using a Stochastic Patch-Growing Algorithm
- **Citation:** Meentemeyer, R.K., Tang, W., Dorning, M.A., Vogler, J.B., Cunniffe, N.J., Shoemaker, D.A. (2013). FUTURES: Multilevel Simulations of Emerging Urban–Rural Landscape Structure Using a Stochastic Patch-Growing Algorithm. *Annals of the Association of American Geographers*, 103(4), 785–807. DOI: 10.1080/00045608.2012.707591 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban–rural development in the Charlotte region (NC, USA), per petrasova2016open.
- **Model:** three submodels. DEMAND converts population projections into a number of cells per subregion and step. POTENTIAL is a multilevel logistic regression including a dynamic development-pressure term. PGA picks seeds by probability and grows patches with a size distribution and compactness parameters calibrated on historical patches.
- **Inputs:** land-cover time series (NLCD), predictors, subregions, population.
- **Parameters:** patch library, compactness, development-pressure gamma, incentive power and so on. The calibration tools exist as GRASS modules.
- **Code:** GRASS add-on r.futures, https://github.com/OSGeo/grass-addons/tree/grass8/src/raster/r.futures (verified); manual at https://grass.osgeo.org/grass-stable/manuals/addons/r.futures.html.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: metadata + GRASS manual.
- **Browser fit:** patch growing is cheap; development pressure is a convolution (GPU friendly).
- **Relevance to ca-geo:** LND-01. Patch-based growth looks more like real suburban development (whole housing estates) than single-cell CA.

### petrasova2016open — Open Source Approach to Urban Growth Simulation
- **Citation:** Petrasova, A., Petras, V., Van Berkel, D., Harmon, B.A., Mitasova, H., Meentemeyer, R.K. (2016). Open Source Approach to Urban Growth Simulation. *ISPRS – International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, XLI-B7, 953–959. DOI: 10.5194/isprsarchives-xli-b7-953-2016 (verified: Crossref)
- **Access:** OA.
- **Phenomenon and study area:** urban growth in the Asheville metropolitan area (NC, USA), 30 m, projected to 2035.
- **Model:** FUTURES re-implemented as GRASS GIS modules: r.futures.demand, .devpressure, .potential (multilevel logistic via R), .calib (patch size and shape calibration) and .pga/.simulation. Demand and potential are computed per subregion, and development pressure is fed back at each step.
- **Inputs:** NLCD 2001/2006/2011, NED elevation, roads, protected areas, county population and projections.
- **Parameters:** obtained with the automated calibration modules (a reproducible procedure).
- **Code:** r.futures (verified). Workshop tutorial with data: https://grasswiki.osgeo.org/wiki/Workshop_on_urban_growth_modeling_with_FUTURES (HTTP 200).
- **Validation:** mainly a demonstration (maps); the paper does not focus on quantitative validation.
- **Reimplementability:** S1 1 (algorithm is described at a high level; the open C code is the full spec); S2 2; S3 2; S4 2; S5 1 → 8, B. Assessed from: full text.
- **Browser fit:** good; patch growing plus convolution.
- **Relevance to ca-geo:** LND-01. Its workflow (demand → potential → patch growth) transfers directly to CZ: ČSÚ population projections, CORINE / Urban Atlas, a DEM, OSM roads.

### hewitt2019cellular — A cellular automata land use model for the R software environment (SIMLANDER)
- **Citation:** Hewitt, R.J., Díaz-Pacheco, J., Moya-Gómez, B. (2019). A cellular automata land use model for the R software environment. SocArXiv preprint. DOI: 10.31235/osf.io/suy2c (verified: Crossref)
- **Access:** OA (preprint, user documentation).
- **Phenomenon and study area:** generic land-use / urban growth (documentation with a step-by-step example).
- **Model:** constrained CA in R. Transition potential is the product of neighbourhood (N), accessibility (A), suitability (S) and randomness (v). Cells with the highest potential are allocated per step until demand is met (description taken from roodposhti2020towards).
- **Inputs:** land-use maps, distance-to-road, suitability layers.
- **Parameters:** user-set; documentation explains calibration.
- **Code:** project site https://simlander.wordpress.com/ (200). It links SIMLANDER v2.1.1 and v2.0 zip files (R scripts, demo data, README); the download link answered HTTP 303 (redirect to file). License not stated. The related multi-class model APoLUS is at https://simlander.wordpress.com/apolus/.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 2; S5 1 → 7, B. Assessed from: abstract + project site. The PDF text could not be extracted because of font encoding.
- **Browser fit:** very good; the rules are elementwise products plus one kernel sum.
- **Relevance to ca-geo:** LND-01. The most compact open template of the White–Engelen logic. APoLUS (multi-class) is worth checking for LND-02.

### roodposhti2020towards — Towards automatic calibration of neighbourhood influence in cellular automata land-use models
- **Citation:** Roodposhti, M.S., Hewitt, R.J., Bryan, B.A. (2020). Towards automatic calibration of neighbourhood influence in cellular automata land-use models. *Computers, Environment and Urban Systems*, 79, 101416. DOI: 10.1016/j.compenvurbsys.2019.101416 (verified: Crossref)
- **Access:** OA (accepted manuscript in the Deakin repository, https://dro.deakin.edu.au/articles/journal_contribution/Towards_automatic_calibration_of_neighbourhood_influence_in_cellular_automata_land-use_models/20739397).
- **Phenomenon and study area:** urban growth of Ahvaz (Iran) 2000–2015; 7 920-cell raster at 300 m; urban / non-urban.
- **Model:** SIMLANDER (R script v1.0.5) with modifications.
  - **Transition potential:** P = N·A·S·v.
  - **Neighbourhood N:** distance-decay weights in square windows up to 11×11, w = x₀·β^(d/cell width).
  - **Accessibility A:** cosine-sigmoid decay with distance to major roads, 1 below 300 m and 0 beyond 1 500 m.
  - **Suitability S:** slope classes scored 1.0 / 0.7 / 0.5 / 0.3 / 0.1 / 0.0.
  - **Randomness v:** Weibull-type term 1 + (−ln(1−rand))^α with α = 0.5.
  - **Allocation:** the yearly demand (observed new cells ÷ years) is allocated to the highest-potential cells.
  - **Calibration:** the ARD procedure searches window size and decay (randomised vs grid search) and ranks rule sets by several metrics.
- **Inputs:** ESA CCI land cover (300 m), SRTM slope, road network.
- **Parameters:** all values given (thresholds, slope table, α, search ranges for x₀ ∈ [5, 50] and β ∈ (0, 1)).
- **Code:** SIMLANDER base script (verified, see above). The ARD calibration script is in the journal's supplementary material (not verified).
- **Validation:** AUC, accuracy and landscape-metric differences (shape index, fractal dimension, clumpiness, edge density). Tables of the best and worst rule sets are given.
- **Reimplementability:** S1 2 – complete equations and allocation rule; S2 2 – all values tabulated; S3 2 – the base model is openly downloadable (license unstated; supplementary script not verified); S4 2 – open global inputs; S5 2 – quantitative metrics → 10, A. Assessed from: full text.
- **Browser fit:** excellent. Tiny grid in the paper; even a 1 000 × 1 000 CZ grid with an 11×11 kernel is trivial on WebGL.
- **Relevance to ca-geo:** **LND-01 top pick**. Directly portable to CZ: CCI or CORINE land cover, Copernicus DEM, OSM roads. Its calibration method gives a demo "fit the neighbourhood" interaction.

### hewitt2017stable — Stable models for metastable systems? Lessons from sensitivity analysis of a Cellular Automata urban land use model
- **Citation:** Hewitt, R., Díaz-Pacheco, J. (2017). Stable models for metastable systems? Lessons from sensitivity analysis of a Cellular Automata urban land use model. *Computers, Environment and Urban Systems*, 62, 113–124. DOI: 10.1016/j.compenvurbsys.2016.10.011 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban land use. Madrid (EU) is likely, since roodposhti2020towards refers to earlier Madrid rule-set work, but this was not confirmed.
- **Model:** sensitivity analysis of a constrained CA (SIMLANDER lineage).
- **Inputs:** not checked.
- **Parameters:** not checked.
- **Code:** SIMLANDER.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: metadata only (provisional).
- **Browser fit:** as SIMLANDER.
- **Relevance to ca-geo:** LND-01; a European case and a sensitivity study (stochastic term vs neighbourhood).

### newland2018multiobjective — Multi-objective optimisation framework for calibration of Cellular Automata land-use models
- **Citation:** Newland, C.P., Maier, H.R., Zecchin, A.C., Newman, J.P., van Delden, H. (2018). Multi-objective optimisation framework for calibration of Cellular Automata land-use models. *Environmental Modelling & Software*, 100, 175–200. DOI: 10.1016/j.envsoft.2017.11.012 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** calibration of Metronamica-type constrained CA (case study not confirmed).
- **Model:** multi-objective search over neighbourhood-rule parameters, using location-agreement and landscape-pattern objectives.
- **Inputs:** not checked.
- **Parameters:** not checked.
- **Code:** https://github.com/jeffrey-newman/Charles-Metronamica-Optimiser (verified to exist; a co-author's account, so its link to this paper is inferred). Metronamica itself is closed.
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: metadata only (provisional).
- **Browser fit:** optimisation is offline.
- **Relevance to ca-geo:** calibration background for multi-class CA.

### mustafa2017coupling — Coupling agent-based, cellular automata and logistic regression into a hybrid urban expansion model (HUEM)
- **Citation:** Mustafa, A., Cools, M., Saadi, I., Teller, J. (2017). Coupling agent-based, cellular automata and logistic regression into a hybrid urban expansion model (HUEM). *Land Use Policy*, 69, 529–540. DOI: 10.1016/j.landusepol.2017.10.009 (verified: Crossref)
- **Access:** OA (green preprint, https://orbi.uliege.be/bitstream/2268/215176/1/HUEM_pre.pdf).
- **Phenomenon and study area:** urban expansion in Wallonia (Belgium, EU), 1990–2000.
- **Model:** 100 m grid. A logit gives global probability, and a CA neighbourhood term (radius 1–8 cells, weights calibrated per distance and land-use class) gives local probability. Developer, farmer and planning-authority agents decide conversion, with farmer satisfaction thresholds and zoning approval. Calibration uses a genetic algorithm.
- **Inputs:** CORINE Land Cover (100 m), zoning plans, Navteq streets 2002 (proprietary), DEM-type drivers.
- **Parameters:** tables of calibrated neighbourhood weights (Table 2) and logit coefficients (Table 3).
- **Code:** not found.
- **Validation:** cell-to-cell agreement (Table 4), compared with other models in the literature.
- **Reimplementability:** S1 1 (the agent rules add ambiguity); S2 2; S3 0; S4 1 (streets proprietary, CLC open); S5 2 → 6, C. Assessed from: full text (preprint).
- **Browser fit:** the CA + logit part is easy; the agent layer adds moderate complexity.
- **Relevance to ca-geo:** LND-01; a **CORINE-based EU precedent** with published neighbourhood weights that could be reused as a starting point for CZ.

### mustafa2018comparing — Comparing support vector machines with logistic regression for calibrating cellular automata land use change models
- **Citation:** Mustafa, A., Rienow, A., Saadi, I., Cools, M., Teller, J. (2018). Comparing support vector machines with logistic regression for calibrating cellular automata land use change models. *European Journal of Remote Sensing*, 51(1), 391–401. DOI: 10.1080/22797254.2018.1442179 (verified: Crossref)
- **Access:** OA (CC BY; automated access blocked).
- **Phenomenon and study area:** urban land-use change in Wallonia (Belgium), 2000–2010.
- **Model:** a CA whose transition rules are calibrated with SVM or logistic regression.
- **Inputs:** geophysical and proximity drivers.
- **Parameters:** not checked.
- **Code:** not found.
- **Validation:** ROC and fuzzy map comparison. CA-SVM slightly beats CA-logit, and roads are the main driver.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract.
- **Browser fit:** good.
- **Relevance to ca-geo:** LND-01; EU case. A related Wallonia RF-vs-SVM study (Rienow et al. 2021, *Transactions in GIS*, DOI 10.1111/tgis.12756, verified in Crossref) is noted for round 2.

### bastosmoroz2024spatial — Spatial constraints in cellular automata-based urban growth models
- **Citation:** Bastos Moroz, C., Sieg, T., Thieken, A.H. (2024). Spatial constraints in cellular automata-based urban growth models: A systematic comparison of classifiers and input urban maps. *Computers, Environment and Urban Systems*, 110, 102118. DOI: 10.1016/j.compenvurbsys.2024.102118 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban growth (Universität Potsdam group; study area not confirmed).
- **Model:** systematic comparison of classifiers for transition potential and of input urban maps (built-up products) in CA urban growth models.
- **Inputs:** various urban maps (not checked).
- **Parameters:** not checked.
- **Code:** Mendeley Data "data and code repository", CC BY 4.0, DOI 10.17632/p9rsyr9r4x.2 (https://data.mendeley.com/datasets/p9rsyr9r4x/2, HTTP 200).
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: metadata + data repository page.
- **Browser fit:** probably good.
- **Relevance to ca-geo:** LND-01. Its finding on which input urban map to use matters for choosing CORINE vs Urban Atlas vs GHSL vs the Czech building footprint data. **Priority to read in round 2.**

### yang2023simulating — Simulating urban expansion using cellular automata model with spatiotemporally explicit representation of urban demand
- **Citation:** Yang, J., Tang, W., Gong, J., Shi, R., Zheng, M., Dai, Y. (2023). Simulating urban expansion using cellular automata model with spatiotemporally explicit representation of urban demand. *Landscape and Urban Planning*, 231, 104640. DOI: 10.1016/j.landurbplan.2022.104640 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** urban expansion (China, not confirmed).
- **Model:** patch-based CA with spatiotemporally explicit urban demand. Implemented in MUSE with four patch-generating engines (distance-, neighbourhood- and spatially-constrained, and a parameterised region-growing engine after Brookes 1997) and patch-size controllers (lognormal, power law, historical), according to the README.
- **Inputs:** not checked.
- **Parameters:** not checked.
- **Code:** https://github.com/LandInsightLab/MUSE (verified; Python, MIT license).
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: metadata + repository README.
- **Browser fit:** patch engines are cheap; the Python source can be read as a specification.
- **Relevance to ca-geo:** LND-01; an open patch-generation code base. A good alternative to the closed PLUS binary.

### saganeiti2021modeling — Modeling urban sprinkling with cellular automata
- **Citation:** Saganeiti, L., Mustafa, A., Teller, J., Murgante, B. (2021). Modeling urban sprinkling with cellular automata. *Sustainable Cities and Society*, 65, 102586. DOI: 10.1016/j.scs.2020.102586 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** "urban sprinkling" (scattered low-density urbanisation) in Basilicata, southern Italy (EU). Building data 1989 / 1998 / 2013.
- **Model:** CA coupled with multinomial logistic regression on building-density classes.
- **Inputs:** regional building datasets converted to density maps; drivers chosen from a review of 19 articles.
- **Parameters:** not checked.
- **Code:** not found.
- **Validation:** calibration and validation on the three building snapshots.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract.
- **Browser fit:** good.
- **Relevance to ca-geo:** LND-01. Scattered suburbanisation resembles CZ rural municipalities around Prague. Building density from CZ footprint data (RÚIAN) is a nice input analogue.

### indrova2015land — Land use changes in Prague suburban area according to different prediction modelling approaches
- **Citation:** Indrová, M., Kupková, L. (2015). Land use changes in Prague suburban area according to different prediction modelling approaches. *Geografie*, 120(3), 422–443. DOI: 10.37040/geografie2015120030422 (verified: Crossref)
- **Access:** OA (https://geografie.cz/120/3/0422/), in Czech with an English abstract.
- **Phenomenon and study area:** residential and commercial suburbanisation in cadastres south-east of Prague (Průhonice, Čestlice, Dobřejovice, Modletice, Jažlovice; about 19 km²), 1994 → 2007, prediction to 2020.
- **Model:** compares Land Change Modeler (IDRISI; MLP transition potential + Markov quantities) with Dyna-CLUE (logistic regression + iterative allocation). It is not a CA in the strict sense, although the paper reviews CA, Markov chains, logistic regression and ANN.
- **Inputs:** land use vectorised from QuickBird imagery (2.4 m) for 1994 and 2007, ZABAGED contours (elevation, slope), municipal land-use plans, soil protection classes (BPEJ; protection class 1 excluded). Seven driver maps: distances to existing and unfinished residential/commercial areas, to roads, elevation and slope.
- **Parameters:** derived inside the software (Cramér's V, logistic regression with ROC check).
- **Code:** LCM is commercial; Dyna-CLUE is free but closed.
- **Validation:** comparison of predicted maps with plans; models respect constraints; commercial areas were under-allocated.
- **Reimplementability:** S1 0; S2 1; S3 1; S4 1; S5 1 → 4, C. Assessed from: full text.
- **Browser fit:** the area is small (about 2 000 ha), so it is ideal as a demo extent.
- **Relevance to ca-geo:** **LND-01 CZ anchor**. Defines a realistic study area along the D1 motorway, a driver set and planning constraints. A CA from this survey (SIMLANDER / FUTURES / SLEUTH) could be run on the same area for comparison.

### pokojska2019simulating — Simulating land use change in the southern part of Warsaw Metropolitan Area with application of Dyna-CLUE model
- **Citation:** Pokojska, P. (2019). Simulating land use change in the southern part of Warsaw Metropolitan Area with application of Dyna-CLUE model. *Geografie*, 124(1), 57–82. DOI: 10.37040/geografie2019124010057 (verified: Crossref)
- **Access:** OA (Geografie).
- **Phenomenon and study area:** urban sprawl in Piaseczno county, Warsaw Metropolitan Area (Poland), scenarios over 20 and 35 years.
- **Model:** Dyna-CLUE (non-CA allocation) with 8 driving factors and population-based scenarios.
- **Inputs:** land-use maps, 8 drivers.
- **Parameters:** not checked.
- **Code:** Dyna-CLUE (free, closed).
- **Validation:** not checked.
- **Reimplementability:** S1 0; S2 1; S3 1; S4 1; S5 1 → 4, C. Assessed from: abstract.
- **Browser fit:** n/a (allocation model).
- **Relevance to ca-geo:** LND-01; a Central European suburbanisation case; scenario design driven by population projections.

### muhammad2022spatiotemporal — Spatiotemporal Change Analysis and Prediction of Future Land Use and Land Cover Changes Using QGIS MOLUSCE Plugin
- **Citation:** Muhammad, R., Zhang, W., Abbas, Z., Guo, F., Gwiazdzinski, L. (2022). Spatiotemporal Change Analysis and Prediction of Future Land Use and Land Cover Changes Using QGIS MOLUSCE Plugin and Remote Sensing Big Data: A Case Study of Linyi, China. *Land*, 11(3), 419. DOI: 10.3390/land11030419 (verified: Crossref)
- **Access:** OA.
- **Phenomenon and study area:** LULC change in Linyi (China), 1990–2020 at 10-year steps, projections to 2050.
- **Model:** CA-ANN in the QGIS MOLUSCE plugin: an ANN transition potential from DEM, slope and distance to roads, with CA allocation.
- **Inputs:** classified remote sensing, DEM, roads.
- **Parameters:** not checked.
- **Code:** https://github.com/nextgis/qgis_molusce (verified; Python, GPL-2.0+, active).
- **Validation:** not checked.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: abstract.
- **Browser fit:** good; the MOLUSCE source can serve as a reference implementation of CA-ANN and of its validation statistics.
- **Relevance to ca-geo:** LND-01 / LND-02. MOLUSCE is the most-used open CA-ANN / CA-Markov tool, so its code defines the "standard" CA–Markov behaviour.

### sante2010cellular — Cellular automata models for the simulation of real-world urban processes: A review and analysis
- **Citation:** Santé, I., García, A.M., Miranda, D., Crecente, R. (2010). Cellular automata models for the simulation of real-world urban processes: A review and analysis. *Landscape and Urban Planning*, 96(2), 108–122. DOI: 10.1016/j.landurbplan.2010.03.001 (verified: Crossref)
- **Access:** paywall.
- **Content:** a review and classification of urban CA models applied to real cities by their main characteristics (cell space, neighbourhood, transition rules, calibration), with their strengths and weaknesses.
- **Reimplementability:** n/a (review). Entry point for model families 1–3. The same group's companion papers on the stochastic component (García et al. 2011, DOI 10.1016/j.compenvurbsys.2010.11.001, verified) and small Galician towns are useful follow-ups.
- **Relevance to ca-geo:** checklist of design choices for LND-01.

### verburg2004land — Land use change modelling: current practice and research priorities
- **Citation:** Verburg, P.H., Schot, P.P., Dijst, M.J., Veldkamp, A. (2004). Land use change modelling: current practice and research priorities. *GeoJournal*, 61(4), 309–324. DOI: 10.1007/s10708-004-4946-y (verified: Crossref)
- **Access:** OA (green, WUR repository).
- **Content:** overview of land-use change modelling approaches (CA, statistical, allocation models such as CLUE) and open research issues (scale, driving forces, neighbourhood, temporal dynamics).
- **Reimplementability:** n/a (review). Entry point for the CA vs allocation-model distinction (Dyna-CLUE in indrova2015land and pokojska2019simulating).
- **Relevance to ca-geo:** framing for LND-01 / LND-02.

## Most reimplementable (top picks)

1. **roodposhti2020towards (10, A)**: SIMLANDER constrained CA with every equation and value printed, an openly downloadable R base model and open global inputs. The fastest route to a calibrated CZ urban-growth demo.
2. **clarke1997selfmodifying / SLEUTH (9, A)**: open C source, demo dataset with expected outputs and a documented calibration. The classic "urban growth" demo, with self-modification as an attractive visual feature.
3. **petrasova2016open / FUTURES (8, B)**: open GRASS implementation with tutorial data and a demand → potential → patch-growth workflow. Realistic patch-shaped suburban development.
4. **zhou2019highresolution (8, B)**: SLEUTH at global scale with open scripts and a published probability dataset that covers Czechia, usable as a reference layer.
5. **liang2021understanding / PLUS (7, B)**: complete parameter set and FoM results for multi-class patch-generating CA. The binary is closed, but the equations suffice for a JS re-implementation. MUSE (yang2023simulating, open Python) is an open alternative for patch engines.
6. **hewitt2019cellular / SIMLANDER (7, B)**: the base script with demo data behind pick 1. APoLUS adds multiple land-use classes for LND-02.

## Gaps and unverified leads

- **OpenAlex budget exhausted** after the first queries (HTTP 429, shared daily IP budget). All verification was then done through Crossref, so cited-by counts in this file come from Crossref where noted, not OpenAlex. Round 2 could re-check OA status and citations in OpenAlex.
- **Paywalled classics assessed only from abstracts or TLDRs:** white1997use, barredo2003modelling, li2002neuralnetworkbased, wu2002calibration, liu2017future, meentemeyer2013futures, silva2002calibration, rienow2015supporting, bastosmoroz2024spatial. Publisher sites (T&F, Elsevier, MDPI) blocked automated access, even for OA items (MDPI, T&F bronze). A manual read could raise S1 / S2 for several of them, especially White 1997 (rule equations) and Wu 2002.
- **Czech CA studies:** no peer-reviewed CA urban growth model for a Czech area was found in Crossref. The only CZ item is indrova2015land (LCM / Dyna-CLUE). Leads for round 2: Czech theses (e.g. Charles University, Masaryk University, VŠB) on SLEUTH / CA-Markov for Prague, Brno or Ostrava; the Sýkora & Mulíček chapter on Prague suburbanisation (DOI 10.1002/9781118295861.ch5, found in Crossref, context only).
- **CORINE-based EU applications:** mustafa2017coupling uses CLC 100 m. A CORINE-based Estonian urban expansion CA (Pour & Oja 2020, DOI 10.1145/3397056.3397057) and Lagarias 2015 (Thessaloniki, DOI 10.1080/10106049.2015.1013066) were found in Crossref but not assessed.
- **Code leads not tied to a verified publication:**
  - Alamanos (2023), CA-Markov in Python with data and validation, https://github.com/Alamanos11/Land_uses_prediction (verified repo). Its DOI 10.13140/RG.2.2.20309.19688 is registered at DataCite, not in OpenAlex or Crossref, so it was not catalogued.
  - johanlahti/urban-lu-model (CA + ABM, Python, MIT).
  - adamlilith/urbanSleuth (SLEUTH modifications).
  - ranielZhang/openplus-landuse-python (PLUS approximation).
  - HPSCIL/Open-Space-Cellular_Automata (binary).
- **FLUS software:** the GeoSOS-FLUS download page did not respond, so the code is unverified.
- **Metronamica / MOLAND:** closed software. JRC's later LUISA platform (EU-wide, CORINE-based) was not searched. Worth a round-2 query, since it is the main EU-wide land-use allocation model.
- **SIMLANDER preprint PDF:** text could not be extracted (font encoding), so the full rule description was taken from roodposhti2020towards.
- **Not covered in depth:** CLUE-S / Dyna-CLUE as a non-CA alternative; deep-learning CA (ConvLSTM-CA etc.); vector / irregular CA (Pinto et al. 2017, DOI 10.1016/j.compenvurbsys.2017.05.005, found in Crossref, not assessed).
- **Overlaps with other domains:**
  - Farmland abandonment and forest regrowth (LND-02) overlaps with eco (succession).
  - DINAMICA overlaps with eco (deforestation).
  - Calibration methods (Straatman, Newland, Roodposhti, Dietzel) and review papers overlap with gen.
  - Urban growth feeding pluvial flooding and heat island (chain L8) overlaps with hyd and atm.
