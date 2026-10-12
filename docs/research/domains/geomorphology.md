# Geomorphology and mass movements — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.

Domain code `geo`. Longlist items covered: HYD-05 (soil erosion), HYD-07 (river channel
morphodynamics), HAZ-02 (landslides and debris flows), HAZ-03 (snow avalanche runout),
HAZ-05 (lava flow); cross-link L7 (landslide → river blockage).

> **Verification note.** The OpenAlex API daily quota for this machine ran out early in the
> session (HTTP 429, budget 0 for ~14 h). The first searches were done in OpenAlex; all
> later searches and **every bibliographic record below were verified against Crossref**
> (`api.crossref.org/works/<DOI>`). Abstracts were taken from Crossref or Semantic Scholar
> where the publisher deposited them. Several publishers (Elsevier, Springer, Nature,
> T&F) withheld abstracts, so a number of entries are assessed from **metadata only**
> (title, venue, plus what other verified papers in this list say about them); these
> scores are provisional and deliberately low (S1, S2 ≤ 1).

## Search log

Date: 2026-10-12. "Hits" = total result count reported by the API (Crossref counts are
relevance-ranked over the whole index and therefore huge; only the top 5–10 were screened).

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular model braided rivers | OpenAlex | 1 772 | Murray & Paola 1994; Thomas/Nicholas braided-river cellular models |
| cellular automaton landscape evolution model | OpenAlex / Crossref | 4 173 / – | CAESAR family (Van De Wiel 2007) |
| CAESAR cellular landscape evolution model | OpenAlex | 1 073 | CAESAR-Lisflood sensitivity papers (Skinner 2018, 2023), SIBERIA comparison |
| cellular automaton soil erosion | OpenAlex | 1 306 | Eltner 2025 (RillGrow, CTU Prague data); hexagonal soil-erosion CA (D'Ambrosio group, no DOI) |
| cellular automata lava flow simulation | OpenAlex / Crossref | 434 / – | MAGFLOW, SCIARA, Korean implementation |
| SCIARA lava flow cellular automata | OpenAlex / Crossref | 94 / – | SCIARA releases γ2, fv2, fv3, review 2016 |
| MAGFLOW cellular automata lava | OpenAlex | 84 | MAGFLOW applications, CUDA port, hazard map validation |
| cellular automata debris flow | OpenAlex | 1 183 | SCIDDICA S2, S3-hex, GA calibration, Swii2 WebGL viewer |
| cellular automata landslide | OpenAlex | 2 139 | Guthrie 2007/08, Lai 2013, Calidonna 2001 |
| *(OpenAlex quota exhausted — switched to Crossref)* | | | |
| cellular automata snow avalanche | Crossref | top 10 | Kronholm 2005, Bolgov 2022, Barpi 2007 (next query) |
| cellular automaton rockfall simulation | Crossref | top 10 | nothing relevant — rockfall CA not found |
| cellular automaton sand dunes model | Crossref | top 10 | Zhang/Narteau 2010, Endo 2016 |
| self-organized criticality sandpile Bak Tang Wiesenfeld | Crossref | top 10 | BTW 1987/1988, Dhar 1992 |
| landslide runout cellular automata | Crossref | top 10 | runoutSIM (random walk, 2025 preprint) |
| CAESAR-Lisflood landscape evolution model | Crossref | top 10 | Coulthard 2013, Li 2023 SLIDE coupling, Skinner 2023 |
| Werner eolian dunes simple model | Crossref | top 6 | Werner 1995 |
| Narteau … cellular automaton dune model | Crossref | top 6 | Narteau 2009, Zhang 2010, Rozier & Narteau 2014 (ReSCAL) |
| Nield Baas DECAL vegetated dune | Crossref | top 6 | Baas & Nield 2007, Nield & Baas 2008, Baas 2002 |
| Coulthard Macklin Kirkby cellular model Holocene | Crossref | top 6 | Coulthard 2002, 1998 (HESS), 2000 |
| Favis-Mortlock RillGrow | Crossref | top 6 | Favis-Mortlock 1998, 2000 |
| Miyamoto Sasaki lava cellular automata | Crossref | top 6 | Miyamoto 1997; Barca 1994; Avolio "blocks" 2004 |
| MOLASSES / Q-LavHA lava | Crossref | top 6 | no MOLASSES paper found; Connor 2012 (same group), Q-LavHA application 2025 |
| Flow-Py gravitational mass flow | Crossref | top 6 | Flow-Py GMD 2022 |
| Barpi / VALANCA avalanche CA | Crossref | top 6 | Barpi 2007, Avolio 2010; "VALANCA" name not found |
| Segre Deangeli cellular automaton | Crossref | top 6 | Segre & Deangeli 1995 |
| Hergarten SOC landslide | Crossref | top 6 | Hergarten & Neugebauer 1998 |
| Di Gregorio Serra macroscopic CA | Crossref | top 6 | Di Gregorio & Serra 1999 (MCA methodology) |
| SCAVATU / soil erosion CA | Crossref | top 6 | Heung 2013 (USLE+CA), Ma 2009, Sun 2022, Tang 2022 |
| landscape evolution review | Crossref | top 6 | Tucker & Hancock 2010, Coulthard 2001 |
| GitHub repository search (CAESAR-Lisflood, ReSCAL, MOLASSES, SCIARA, SCIDDICA, RillGrow, DECAL, braided) | GitHub API | – | see Code column; GitHub API rate limit hit after 11 queries |

### Round 2

Crossref only (OpenAlex still quota-blocked), ≥1 s between requests. Full texts via Semantic
Scholar `openAccessPdf`, Copernicus/BMC/arXiv PDFs (curl + pdftotext, scratchpad only, deleted
after extraction). Elsevier, Springer LNCS, De Gruyter, Nature, APS and GSA were not reachable.

| Query | Source | Hits | Notes |
|---|---|---|---|
| openAccessPdf for connor2012probabilistic, spataro2010latest, bak1987, murray1994, werner1995 | Semantic Scholar API | 5 | Connor 2012 read in full (BMC PDF); SCIARA OA link 403; Bak/Murray/Werner closed |
| "The latest release of the lava flows simulation model SCIARA" pdf | WebSearch | 9 | Only repository records; Rongo et al. 2011 (SIMULTECH, 10.5220/0003575900370044) read as a secondary source |
| Bak Tang Wiesenfeld 1987 pdf | WebSearch | 10 | Course-hosted scan found, image-only (no text layer, no OCR tool) – not assessable |
| MOLASSES lava flow simulator cellular automata | Crossref + GitHub | 1.6 M / repo | No MOLASSES method paper; repo source tree and test DEMs inspected |
| Dietterich benchmarking … lava flow simulation | Crossref | 1 | Dietterich et al. 2017 (J. Appl. Volcanol., OA) read: MOLASSES benchmarked with NRMSE |
| Gallant MOLASSES lava probabilistic | Crossref | 1 | Gallant et al. 2018 (Geology) – seen, not catalogued |
| rockfall cellular automata simulation | Crossref | 1.5 M | Noise; no rockfall CA |
| rockfall propagation cellular automata model DEM | WebSearch | 10 | Only discrete-element (non-CA) rockfall models; no CA |
| Gravitational Process Path GPP model | Crossref | 3 | Wichmann 2017 (GMD, OA) read in full – random-walk + friction raster model incl. rockfall |
| Flow-R susceptibility mapping debris flows | Crossref | 2 | Horton et al. 2013 (NHESS, OA) read in full |
| TopRunDF debris flow random walk | Crossref | 3 | Korean random-walk applications only |
| cellular automata debris flow Czech Republic / landslide Carpathians / soil erosion Central Europe | Crossref | 0.6–1.9 M | No Central-European CA mass-movement study |
| Flow-R / debris flow Czech (Krkonoše, Jeseníky) | WebSearch | 9 | No Czech Flow-R/CA study; Storm Boris 2024 inventory (Tichavský et al. 2026, verified) and Krkonoše avalanche GIS map (not verified) |
| avalanche Krkonose runout model / debris flow runout Czech flysch | Crossref | 3–4 M | Noise |
| cellular automata gully erosion model | Crossref | 3.7 M | Liu & Yuan 2012 rill-erosion CA (IEEE); loess-gully CA EGU abstract 2020 (not catalogued) |
| cellular automata debris flow Alps hazard | Crossref | 2.6 M | Swii2 HTML5/WebGL SCIDDICA viewer (Parise et al. 2012) |
| cellular automata mining subsidence | Crossref | 0.96 M | Chen et al. 2020 (Open Geosciences, OA; PDF blocked) + two minor papers |
| cellular automata sinkhole / karst | Crossref + WebSearch | 1.5 M / 10 | Yizhaq et al. 2017 (GRL; arXiv preprint read); no karst-landscape CA |
| cellular automaton limestone dissolution karst conduit | Crossref | 0.6 M | Non-CA karst models only |
| Van De Wiel Coulthard SOC river basins | Crossref | 2 | Van De Wiel & Coulthard 2010 (Geology), Coulthard & Van De Wiel 2007 – seen, not catalogued |

## Model families

1. **Sandpile / self-organised criticality (SOC) automata** — threshold toppling of a
   slope or height variable to neighbours; the conceptual root of most mass-movement CA.
   `bak1987selforganized`, `hergarten1998selforganized` (PDE counterpart),
   `segre1995cellular` (a "realistic" sandpile for landslides), `guthrie2008exploring`,
   `kronholm2005integrating`.
2. **Reduced-complexity fluvial CA and cellular landscape evolution models** — water
   routed cell-to-cell by slope (multiple flow directions or a simplified 2-D flow
   solver), sediment eroded/deposited with transport laws; braided and meandering
   channels emerge. `murray1994cellular`, CAESAR / CAESAR-Lisflood
   (`coulthard2002cellular`, `coulthard2006cellular`, `vandewiel2007embedding`,
   `coulthard2013integrating`, `skinner2018global`, `skinner2023testing`, `li2023integrating`);
   reviews `coulthard2007cellular`, `tucker2010modelling`.
3. **Soil erosion CA** — hillslope-scale: RillGrow (`favismortlock1998selforganizing`,
   `eltner2025using`), where rills self-organise from microtopography; landscape-scale:
   USLE coupled with a CA redistribution rule (`heung2013modelling`).
4. **Macroscopic cellular automata (MCA) for surface flows — "Calabrian school"** — cell
   substates (altitude, thickness, temperature, energy…), outflows computed by the
   *minimisation of differences* algorithm (`digregorio1999empirical`), elementary
   processes composed into the transition function, parameters calibrated by GA.
   Debris flows / landslides: SCIDDICA (`dambrosio2003simulating`, `avolio2013sciddica`);
   lava: SCIARA (`barca1994cellular`, `crisci2004simulation`, `spataro2010latest`);
   snow avalanches (`avolio2010development`).
5. **Other lava-flow CA** — MAGFLOW (Bingham-rheology flux between cells, thermal
   solidification; `vicari2007modeling`, `bilotta2012sensitivity`), Miyamoto & Sasaki
   (`miyamoto1997simulating`), and the very simple probabilistic "residual thickness"
   spreading CA of the Connor group (`connor2012probabilistic`; code MOLASSES).
6. **Landslide susceptibility/run-out CA on DEMs** — rule-based spreading of failed mass
   along slope (`clerici2000simulation`, `lai2013integration`, `li2023integrating`).
7. **Gravitational mass-flow routing on grids (CA-like)** — empirical runout-angle
   stopping plus slope/persistence-weighted flux splitting to the 8 neighbours; applicable to
   avalanches, rockfall, debris flows: `damboise2022flowpy`. Also physically-flavoured
   avalanche CA: `barpi2007cellular`; release-zone fracture CA: `kronholm2005integrating`.
8. **Aeolian dune CA** — slab models (sand slabs eroded/deposited stochastically,
   avalanching at angle of repose; `werner1995eolian`), vegetated dunes DECAL
   (`baas2007modelling`), and 3-D stochastic "real-space" CA coupled with a lattice-gas flow
   (ReSCAL: `narteau2009setting`, `rozier2014real`, `kochanski2019rescal`).

Rockfall-specific CA were **not found** (see Gaps); Flow-Py covers rockfall as one
gravitational process.

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| damboise2022flowpy | 2022 | Flow-Py v1.0 | avalanche, rockfall, debris-flow runout | square raster / Moore 8 / flux, energy-line height / det. | 2 2 2 2 2 | 10 | A | yes | OA | full text |
| eltner2025using | 2025 | RillGrow calibrated with 4D SfM (CTU Prague) | rill/interrill soil erosion | DEM cm-grid / 4–8 nbr (D8 steepest) / water depth, sediment, layers / stoch. (rain drops, detachment) | 1 2 2 2 2 | 9 | A | yes | OA | full text |
| connor2012probabilistic | 2012 | Probabilistic lava inundation, Armenia | lava flow hazard | 100 m SRTM grid / 8 nbr / lava thickness vs residual, parent link / stoch. (vents, volumes, residual) | 2 2 2 2 1 | 9 | A | MOLASSES (same authors, GPL, verified) | OA | full text |
| wichmann2017gpp | 2017 | GPP model (SAGA) (r2) | rockfall, debris-flow, avalanche process paths and runout | raster / Moore 8 / visited flag, velocity, deposit / stoch. random walk + friction model | 2 1 2 2 1 | 8 | B | SAGA GIS (GPL; GitHub mirror verified) | OA | full text |
| dietterich2017benchmarking | 2017 | Lava-model benchmarks incl. MOLASSES (r2) | lava flow (benchmark) | MOLASSES CA: Moore / thickness vs critical thickness / det. per run | 1 1 2 2 2 | 8 | B | MOLASSES (verified) | OA | full text |
| horton2013flowr | 2013 | Flow-R (r2) | debris-flow (and rockfall, avalanche) susceptibility and runout | raster / Moore 8 / susceptibility, kinetic energy / det. (MFD + persistence + energy line) | 2 1 1 2 1 | 7 | B | free binary (flow-r.org), not open source | OA | full text |
| yizhaq2017scalefree | 2017 | Dead Sea sinkholes CA (r2) | sinkhole formation and size statistics | square 1024² / von Neumann / two layers: cavity, sinkhole / stoch. | 2 1 0 2 2 | 7 | B | no | paywall (arXiv preprint) | full text (preprint) |
| dambrosio2003simulating | 2003 | SCIDDICA S3-hex | debris flows (Sarno 1998) | hexagonal / 6+1 / altitude, thickness, energy, soil depth, outflows / det. | 2 2 1 1 2 | 8 | B | partial (SciddicaT in OpenCAL) | OA | full text |
| skinner2023testing | 2023 | CAESAR-Lisflood vs grid size | landscape evolution, sediment yield | square DEM / 4 nbr flow (LISFLOOD-FP) / water, multi-fraction sediment / det. | 1 1 2 2 2 | 8 | B | yes | OA | full text (summary) |
| coulthard2013integrating | 2013 | LISFLOOD-FP inside CAESAR | landscape evolution + floods | square / 4 nbr / water depth, discharge, sediment / det. | 1 1 2 2 1 | 7 | B | yes | paywall | abstract (provisional) |
| kochanski2019rescal | 2019 | Rescal-snow | snow/sand dunes | 3-D cubic lattice / nearest nbr / cell types (sand, air, flow) / stoch. | 1 2 2 2 1 | 8 | B | yes | OA | full text (see atmosphere-other.md) + repo |
| skinner2018global | 2018 | Global SA of LEM parameters | landscape evolution | as CAESAR-Lisflood | 1 1 2 1 1 | 6 | C | yes | OA | abstract (provisional) |
| favismortlock1998selforganizing | 1998 | RillGrow origin | rill initiation | DEM grid / steepest nbr / water, sediment / stoch. | 1 1 2 1 1 | 6 | C | yes | paywall | metadata only (provisional) |
| narteau2009setting | 2009 | ReSCAL dune scales | barchan/transverse dunes | 3-D lattice / nearest nbr / cell states + lattice gas flow / stoch. (continuous time) | 1 1 1 2 1 | 6 | C | partial | paywall | abstract (provisional) |
| rozier2014real | 2014 | ReSCAL laboratory | generic geomorphic CA software | 3-D / nearest nbr / doublet transitions / stoch. | 1 1 1 2 1 | 6 | C | partial | paywall | abstract (provisional) |
| murray1994cellular | 1994 | Braided rivers cellular model | braided channels | square / downstream 3 cells / water, elevation / det. | 1 1 1 1 1 | 5 | C | 3rd-party reimpl. | paywall | metadata only (provisional) |
| coulthard2002cellular | 2002 | CAESAR Holocene basin & fan | catchment & alluvial fan evolution | square 3 m / multiple flow directions / water, grain-size layers / det. | 1 1 1 1 1 | 5 | C | descendant only | paywall | abstract (provisional) |
| vandewiel2007embedding | 2007 | Reach-scale dynamics in CAESAR | river reach morphodynamics | square / scanning routing / water, sediment / det. | 1 1 1 1 1 | 5 | C | descendant only | paywall | metadata only (provisional) |
| coulthard2006cellular | 2006 | Cellular meandering | river meandering | square / curvature from regional window / det. | 1 1 1 1 1 | 5 | C | descendant only | paywall | abstract (provisional) |
| li2023integrating | 2023 | SLIDE in CAESAR-Lisflood | rainfall–landslide–flash-flood chain | square / as CAESAR-Lisflood + infinite-slope stability / det. | 1 1 1 1 1 | 5 | C | base model only | paywall | metadata only (provisional) |
| spataro2010latest | 2010 | SCIARA-fv2 | lava flows (Etna 2006) | square / Moore / altitude, thickness, temperature, solidified lava, outflows / det. | 1 1 1 1 1 | 5 | C | 3rd-party CUDA | OA (blocked) | abstract + secondary (rongo 2011) (provisional) |
| kronholm2005integrating | 2005 | Spatial patterns in avalanche CA | slab-avalanche fracture propagation | square / nearest nbr / stress, strength / threshold | 1 1 0 2 1 | 5 | C | no | paywall | abstract (provisional) |
| bak1987selforganized | 1987 | BTW sandpile / SOC | foundation (avalanches of grains) | square / von Neumann / integer height / det. toppling, random driving | 1 1 0 2 1 | 5 | C | no | paywall | metadata only (provisional) |
| hergarten1998selforganized | 1998 | SOC landslide model | landslide magnitude–frequency | grid PDE (not CA) | 1 1 0 2 1 | 5 | C | no | paywall | abstract (provisional) |
| werner1995eolian | 1995 | Eolian dunes simulation | dune types | square / slab hopping + angle-of-repose avalanching / stoch. | 1 1 0 2 1 | 5 | C | no | paywall | metadata only (provisional) |
| baas2007modelling | 2007 | DECAL vegetated dunes | parabolic & nebkha dunes | square / slab model + vegetation / stoch. | 1 1 0 2 1 | 5 | C | no (post-processing only) | paywall | abstract (provisional) |
| segre1995cellular | 1995 | Realistic landslide CA | debris flow over 3-D topography | square / nbr / mass, energy / sandpile-derived | 1 1 0 1 1 | 4 | C | no | OA (scan) | abstract (provisional) |
| chen2020dynamic | 2020 | Mining subsidence CA (r2) | subsidence basin growth above coal mining | raster / nbr / subsidence / det. (ArcGIS + Python) | 1 1 0 1 1 | 4 | C | no | OA (PDF blocked) | abstract (provisional) |
| heung2013modelling | 2013 | USLE + CA sheet erosion | soil redistribution | raster / nbr / soil depth / det. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| guthrie2008exploring | 2008 | Magnitude–frequency CA for landslides | landslide size statistics | raster / nbr / stoch. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| lai2013integration | 2013 | MCE + CA landslide simulation | landslide spreading | raster / nbr / susceptibility-weighted | 1 1 0 1 1 | 4 | C | no | OA (bronze) | metadata only (provisional) |
| clerici2000simulation | 2000 | Corniglio landslide / Parma blockage | earth-flow run-out, river damming | raster / nbr / det. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| avolio2013sciddica | 2013 | SCIDDICA-SS3 | fast-moving landslides | MCA, square / Moore / incl. momentum | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| barca1994cellular | 1994 | Early lava CA (Etna) | lava flows | MCA, hexagonal / det. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| crisci2004simulation | 2004 | SCIARA: Etna 1991 & 2001 | lava flows | MCA, hexagonal / det. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| vicari2007modeling | 2007 | MAGFLOW Etna 2001 | lava flows | square / 8 nbr / thickness, heat / det. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| bilotta2012sensitivity | 2012 | MAGFLOW sensitivity analysis | lava flows | as MAGFLOW | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| miyamoto1997simulating | 1997 | Improved lava CA | lava flows | square / nbr / Bingham / det. | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| barpi2007cellular | 2007 | CA for dense-snow avalanches | avalanche path & deposit, Susa Valley | 3-D CA on DTM / erosion–deposition | 1 1 0 1 1 | 4 | C | no | green OA (repo) | abstract (provisional) |
| liu2012cellular | 2012 | Rill-erosion CA (r2) | rill erosion | raster / – / – | 1 0 0 1 1 | 3 | D | no | paywall | metadata only (provisional) |
| parise2012swii2 | 2012 | Swii2 HTML5/WebGL SCIDDICA viewer (r2) | debris flows (browser visualisation) | MCA (SCIDDICA) in browser | 1 0 0 1 0 | 2 | D | not found | paywall | metadata only (provisional) |
| avolio2010development | 2010 | Preliminary avalanche MCA | snow avalanches | MCA | 1 1 0 1 1 | 4 | C | no | paywall | metadata only (provisional) |
| digregorio1999empirical | 1999 | MCA modelling method | methodology (surface flows) | framework | – | n/a | n/a | – | paywall | metadata + citing papers |
| coulthard2007cellular | 2007 | Cellular modelling of catchments & reaches | review | – | – | n/a | n/a | – | paywall | metadata only |
| tucker2010modelling | 2010 | Modelling landscape evolution | review | – | – | n/a | n/a | – | paywall | abstract |
| tichavsky2026hydrogeomorphic | 2026 | Storm Boris 2024 effects, NE Czechia (r2) | debris flows, floods (event inventory, not CA) | – | – | n/a | n/a | – | paywall? | metadata only |

Count (after round 2): 46 verified publications. 42 scored: A 3, B 8, C 29, D 2. 4 n/a.

## Entries

### damboise2022flowpy — Flow-Py v1.0: a customizable, open-source simulation tool to estimate runout and intensity of gravitational mass flows
- **Citation:** D'Amboise, C. J. L., Neuhauser, M., Teich, M., Huber, A., Kofler, A., Perzl, F., Fromm, R., Kleemayr, K., Fischer, J.-T. (2022). Flow-Py v1.0: a customizable, open-source simulation tool to estimate runout and intensity of gravitational mass flows. *Geoscientific Model Development* 15(6), 2423–2439. DOI: 10.5194/gmd-15-2423-2022 (verified: Crossref)
- **Access:** OA (CC BY) — https://gmd.copernicus.org/articles/15/2423/2022/
- **Phenomenon and study area:** runout and intensity of snow avalanches, rockfall, landslides/debris flows; regional avalanche case in Tyrol (Austria, EU, ~105 km²).
- **Model:** square raster; from each active cell the flux is passed to the 8 neighbours, split by a slope-based terrain weight raised to an exponent and multiplied by a persistence weight (cosine of direction change relative to the parent); weights normalised so flux is conserved. Propagation stops when the energy-line height drops below zero (runout angle α) or when flux falls below a cutoff. Deterministic, cell-by-cell (breadth-first from release cells). The paper does not call it a CA, but it is a local neighbourhood rule.
- **Inputs:** DEM and release-area raster on the same grid (tested at 5 m and 10 m).
- **Parameters:** 4 core parameters with example values (α, exponent, flux cutoff, max energy-line height).
- **Code:** https://github.com/avaframe/FlowPy (verified, licence file present; Python). Related framework https://github.com/avaframe/AvaFrame (verified).
- **Validation:** analytical α-line solution on three generic slopes (RMSE reported), regional avalanche case, runtime comparison with a physical model.
- **Reimplementability:** S1 2 – full routing and stopping equations; S2 2 – parameter values listed; S3 2 – open repo; S4 2 – runs on any DEM + release mask; S5 2 – analytical test cases. → 10, A. Assessed from: full text.
- **Browser fit:** excellent — one sweep per release area, trivially fast on 10 m DEMs.
- **Relevance to ca-geo:** HAZ-03 (primary), HAZ-02 (debris flow / rockfall runout); a generic "gravity-driven runout" component for Czech mountains (Krkonoše avalanche paths, flysch debris flows). Shares the gravity-driven-flow mechanism family.

### eltner2025using — Using 3D observations with high spatio-temporal resolution to calibrate and evaluate a process-focused cellular automaton model of soil erosion by water
- **Citation:** Eltner, A., Favis-Mortlock, D., Grothum, O., Neumann, M., Laburda, T., Kavka, P. (2025). Using 3D observations with high spatio-temporal resolution to calibrate and evaluate a process-focused cellular automaton model of soil erosion by water. *SOIL* 11(1), 413–434. DOI: 10.5194/soil-11-413-2025 (verified: OpenAlex + Crossref)
- **Access:** OA — https://soil.copernicus.org/articles/11/413/2025/
- **Phenomenon and study area:** rill and interrill erosion on a field plot and a laboratory sample using the Czech Technical University (CTU) Prague rainfall simulator. **CZ/EU.**
- **Model:** RillGrow CA on a cm-resolution DEM: raindrops hit random cells, optional Green–Ampt infiltration, overland flow to the steepest neighbour (D8) with ponding, Manning/Darcy–Weisbach flow speed, transport capacity and probabilistic detachment, splash diffusion, slumping/toppling; three grain-size fractions over a basement. Time step controlled by Courant condition (hundredths of a second). Equations are mostly cited from source papers rather than restated.
- **Inputs:** SfM-photogrammetry DEMs (field 3 cm, lab 1.5 cm), rainfall intensity.
- **Parameters:** 7 calibrated (from 12 screened) by Latin hypercube sampling with ten objective functions.
- **Code:** https://github.com/davefavismortlock/RillGrow and https://doi.org/10.5281/zenodo.15576594 (both verified); data and evaluation code https://doi.org/10.25532/OPARA-602 (verified).
- **Validation:** elevation change and sediment yield vs. 4D SfM observations (RMSE, DTW, NSE, CLIP image similarity).
- **Reimplementability:** S1 1 – processes listed, details deferred to cited papers; S2 2 – reproducible calibration procedure; S3 2; S4 2 – open data; S5 2 – quantitative observations. → 9, A. Assessed from: full text (tool summary).
- **Browser fit:** plot scale only (a few m², tiny time step) — fine as a "micro" demo, not for catchments.
- **Relevance to ca-geo:** HYD-05; Czech partner (CTU) data are open — ideal for a CZ-anchored erosion demo, and a direct check of a reimplementation.

### dambrosio2003simulating — Simulating debris flows through a hexagonal cellular automata model: SCIDDICA S3-hex
- **Citation:** D'Ambrosio, D., Di Gregorio, S., Iovine, G. (2003). Simulating debris flows through a hexagonal cellular automata model: SCIDDICA S3-hex. *Natural Hazards and Earth System Sciences* 3(6), 545–559. DOI: 10.5194/nhess-3-545-2003 (verified: OpenAlex + Crossref)
- **Access:** OA — https://nhess.copernicus.org/articles/3/545/2003/
- **Phenomenon and study area:** debris flows of May 1998 at Pizzo d'Alvano (Sarno, Campania, Italy, EU).
- **Model:** hexagonal cells, neighbourhood = centre + 6. Substates: altitude, debris thickness, kinetic head/energy, erodable soil depth, outflows. Elementary processes: mobilisation/erosion triggering, debris outflows by the minimisation-of-differences algorithm with relaxation rate, run-up correction, thickness/energy update, energy loss. Synchronous update; deterministic. Some details of the minimisation algorithm are referenced to Di Gregorio & Serra (1999).
- **Inputs:** DEM, source areas, soil-cover depth.
- **Parameters:** 7 global parameters with optimal values given in the text (trial-and-error calibration).
- **Code:** paper's model not released; a simplified didactic SCIDDICA-T exists in OpenCAL tests: https://github.com/OpenCALTeam/opencal/tree/master/tests/sciddicaT (verified). Third-party student implementations exist (e.g. SimulationEverywhere-Models/CDPP-LANDSLIDE).
- **Validation:** areal fitness indicators e1 = sqrt(|R∩S|/|R∪S|) and e2 = sqrt(|R∩S|/|R|) for three landslides (values 0.64–0.82 and 0.85–0.97).
- **Reimplementability:** S1 2 – full rule set; S2 2 – values given; S3 1 – only simplified relative in OpenCAL; S4 1 – inputs described, not available; S5 2 – quantitative areal indices. → 8, B. Assessed from: full text.
- **Browser fit:** good; hex grid needs resampling of DEM; tens of thousands of cells, thousands of steps.
- **Relevance to ca-geo:** HAZ-02; the canonical MCA "minimisation algorithm" template reusable for lava, mud, and water flows. Czech flysch debris flows (Beskydy) could use the same rules with a generic DEM.

### skinner2023testing — Testing the sensitivity of the CAESAR-Lisflood landscape evolution model to grid cell size
- **Citation:** Skinner, C. J., Coulthard, T. J. (2023). Testing the sensitivity of the CAESAR-Lisflood landscape evolution model to grid cell size. *Earth Surface Dynamics* 11(4), 695–711. DOI: 10.5194/esurf-11-695-2023 (verified: OpenAlex + Crossref)
- **Access:** OA
- **Phenomenon and study area:** landscape evolution, sediment yield, Tin Camp Creek (Australia, 0.5 km²).
- **Model:** CAESAR-Lisflood v1.9: TOPMODEL runoff, LISFLOOD-FP inertial flow on a regular grid with adaptive (Courant) time step, multi-fraction sediment transport (Wilcock–Crowe, Einstein, Meyer-Peter–Müller), bedload distributed to lower neighbours, active layer stratigraphy. Equations are referenced, not restated.
- **Inputs:** DEM (2–50 m), hourly rainfall series.
- **Parameters:** parameter table (Table 1 / Appendix A1), Morris method over 7 parameters + cell size.
- **Code:** https://sourceforge.net/projects/caesar-lisflood/ (verified); https://github.com/tcoulthard/caesar-lisflood (verified, source zip v1.9b); data https://doi.org/10.5281/zenodo.7908491 (verified).
- **Validation:** sensitivity of 15 model functions (sediment yield, internal geomorphology, discharge, efficiency).
- **Reimplementability:** S1 1; S2 1 – ranges rather than one calibrated set; S3 2; S4 2; S5 2 – published outputs on Zenodo. → 8, B. Assessed from: full text (tool summary).
- **Browser fit:** medium — LISFLOOD-FP loop is GPU-friendly, but multi-decade runs are long; demo on small catchments.
- **Relevance to ca-geo:** HYD-07, HYD-05; overlaps with hydrology domain (LISFLOOD-FP).

### coulthard2013integrating — Integrating the LISFLOOD-FP 2D hydrodynamic model with the CAESAR model: implications for modelling landscape evolution
- **Citation:** Coulthard, T. J., Neal, J. C., Bates, P. D., Ramirez, J., de Almeida, G. A. M., Hancock, G. R. (2013). *Earth Surface Processes and Landforms* 38(15), 1897–1906. DOI: 10.1002/esp.3478 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** landscape evolution with non-steady flood hydraulics.
- **Model:** replaces CAESAR's steady flow routing with the simplified shallow-water LISFLOOD-FP scheme on the same grid, enabling flood-wave effects inside a LEM.
- **Inputs:** DEM, rainfall/discharge.
- **Parameters:** not assessable from abstract.
- **Code:** CAESAR-Lisflood (see skinner2023testing; verified). Round 2: also Zenodo 10.5281/zenodo.321820 (v1.9b) and parameter listings 10.5281/zenodo.6594745 (verified via Zenodo API).
- **Validation:** not assessable from abstract. Round 2: still no OA copy; unchanged (harmonised with hydrology.md).
- **Reimplementability:** S1 1; S2 1; S3 2; S4 2; S5 1 → 7, B. Assessed from: abstract (provisional).
- **Browser fit:** medium (see above).
- **Relevance to ca-geo:** HYD-07; the reference description of CAESAR-Lisflood.

### kochanski2019rescal — Rescal-snow: Simulating snow dunes with cellular automata
- **Citation:** Kochanski, K., Defazio, G.-C., Green, E., Barnes, R., Downie, C., Rubin, A., Rountree, B. (2019). *Journal of Open Source Software* 4(42), 1699. DOI: 10.21105/joss.01699 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** snow and sand dune / bedform formation, idealised.
- **Model:** 3-D stochastic lattice CA (C code) with Python setup/analysis tools; the repository README states it builds on the ReSCAL dune model (relation to Narteau's ReSCAL stated in repo, not on the JOSS page).
- **Inputs:** synthetic initial beds; no geodata needed.
- **Parameters:** in configuration files of the examples.
- **Code:** https://github.com/kellykochanski/rescal-snow (verified), archive https://doi.org/10.5281/zenodo.3517217 (verified).
- **Validation:** example runs.
- **Reimplementability:** S1 1; S2 2 – parameters documented in the JOSS full text (harmonised with the full-text assessment in atmosphere-other.md); S3 2; S4 2; S5 1 → 8, B. Assessed from: full text (via atm survey) + README.
- **Browser fit:** 3-D lattice is heavy; a 2.5-D reduction would be needed.
- **Relevance to ca-geo:** dunes not on the longlist; also snow drift (atm domain overlap).

### skinner2018global — Global sensitivity analysis of parameter uncertainty in landscape evolution models
- **Citation:** Skinner, C. J., Coulthard, T. J., Schwanghart, W., Van De Wiel, M. J., Hancock, G. (2018). *Geoscientific Model Development* 11(12), 4873–4888. DOI: 10.5194/gmd-11-4873-2018 (verified: OpenAlex + Crossref)
- **Access:** OA
- **Phenomenon:** CAESAR-Lisflood parameter sensitivity, two contrasting catchments.
- **Model:** CAESAR-Lisflood; Morris method using "model functions".
- **Parameters:** parameter set and ranges (15 parameters per skinner2023testing); sediment transport law is the most influential choice.
- **Code:** CAESAR-Lisflood (verified).
- **Validation:** sensitivity indices.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** as CAESAR-Lisflood.
- **Relevance to ca-geo:** tells which parameters to expose as sliders in a demo (HYD-07).

### favismortlock1998selforganizing — A self-organizing dynamic systems approach to the simulation of rill initiation and development on hillslopes
- **Citation:** Favis-Mortlock, D. (1998). *Computers & Geosciences* 24(4), 353–372. DOI: 10.1016/s0098-3004(97)00116-7 (verified: Crossref)
- **Access:** paywall
- **Phenomenon:** rill initiation and growth (origin of RillGrow).
- **Model:** see eltner2025using for the current version; 1998 details not assessed.
- **Code:** https://github.com/davefavismortlock/RillGrow (verified; current version).
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: metadata only (provisional).
- **Browser fit / relevance:** HYD-05; historical root of the A-class entry above.

### narteau2009setting — Setting the length and time scales of a cellular automaton dune model from the analysis of superimposed bed forms
- **Citation:** Narteau, C., Zhang, D., Rozier, O., Claudin, P. (2009). *Journal of Geophysical Research: Earth Surface* 114(F3). DOI: 10.1029/2008jf001127 (verified: Crossref)
- **Access:** paywall
- **Phenomenon:** barchan and transverse dunes, superimposed bedforms.
- **Model:** 3-D CA in which erosion, deposition and transport are nearest-neighbour stochastic transitions in continuous time, coupled to a lattice-gas CA for the flow; erosion proportional to bed shear stress. Physical length/time scales fixed via linear stability of a flat bed.
- **Inputs:** synthetic.
- **Code:** ReSCAL (GNU-licensed per rozier2014real); original download page not reachable (round 2); derived rescal-snow verified.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** heavy in 3-D.
- **Relevance:** dunes (not longlisted); method for scaling CA units to physical units — useful generally.

### rozier2014real — A real-space cellular automaton laboratory
- **Citation:** Rozier, O., Narteau, C. (2014). *Earth Surface Processes and Landforms* 39(1), 98–109. DOI: 10.1002/esp.3479 (verified: Crossref)
- **Access:** paywall
- **Model:** ReSCAL — generator of 3-D stochastic CA models built from local transition rules; released under GNU licence.
- **Code:** official site not verified; rescal-snow fork verified.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 2; S5 1 → 6, C. Assessed from: abstract (provisional).
- **Relevance:** framework idea for ca-geo (rule tables of doublet transitions); overlap with `gen`.

### murray1994cellular — A cellular model of braided rivers
- **Citation:** Murray, A. B., Paola, C. (1994). *Nature* 371(6492), 54–57. DOI: 10.1038/371054a0 (verified: OpenAlex + Crossref)
- **Access:** paywall
- **Phenomenon:** emergence of braided channel patterns.
- **Model:** foundational reduced-complexity cellular model of braided rivers (rules not assessed — abstract unavailable).
- **Code:** no original; third-party reimplementation https://github.com/evan-greenbrg/CellularBraidedRiver (verified, unofficial).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: metadata only (provisional). Round 2: Semantic Scholar reports closed access; no OA copy found; unchanged.
- **Browser fit:** very good (small grid, simple rules).
- **Relevance to ca-geo:** HYD-07 — likely the simplest attractive braided-river demo.

### coulthard2002cellular — A cellular model of Holocene upland river basin and alluvial fan evolution
- **Citation:** Coulthard, T. J., Macklin, M. G., Kirkby, M. J. (2002). *Earth Surface Processes and Landforms* 27(3), 269–288. DOI: 10.1002/esp.318 (verified: Crossref)
- **Access:** paywall
- **Phenomenon:** 9 200 years of flood-driven evolution of a 4.2 km² upland catchment and its alluvial fan (UK).
- **Model:** CAESAR at 3 m grid, every flood simulated, rainfall reconstructed from proxies, land-cover history.
- **Code:** only the descendant CAESAR-Lisflood (verified).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract (provisional).
- **Relevance:** HYD-07, HYD-05; land-cover-change scenario idea (deforestation increases sediment yield).

### vandewiel2007embedding — Embedding reach-scale fluvial dynamics within the CAESAR cellular automaton landscape evolution model
- **Citation:** Van De Wiel, M. J., Coulthard, T. J., Macklin, M. G., Lewin, J. (2007). *Geomorphology* 90(3–4), 283–301. DOI: 10.1016/j.geomorph.2006.10.024 (verified: OpenAlex + Crossref)
- **Access:** paywall
- **Model:** reach-scale flow and sediment routines inside CAESAR (details not assessed).
- **Code:** descendant only.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: metadata only (provisional). Likely the most detailed CAESAR rule description — read in round 2.
- **Relevance:** HYD-07.

### coulthard2006cellular — A cellular model of river meandering
- **Citation:** Coulthard, T. J., Van De Wiel, M. J. (2006). *Earth Surface Processes and Landforms* 31(1), 123–132. DOI: 10.1002/esp.1315 (verified: Crossref)
- **Access:** paywall
- **Model:** cell-by-cell bend curvature estimate (regional information transferred to local cells) driving lateral erosion in CAESAR; point-bar deposition and cut-offs identified as difficulties.
- **Reimplementability:** 1 1 1 1 1 → 5, C. Assessed from: abstract (provisional).
- **Relevance:** HYD-07 (meandering variant).

### li2023integrating — Integrating the SLIDE model within CAESAR-Lisflood: rainfall–landslide–flash flood disaster chain
- **Citation:** Li, C., Wang, M., Chen, F., Coulthard, T. J., Wang, L. (2023). *CATENA* 227, 107124. DOI: 10.1016/j.catena.2023.107124 (verified: Crossref)
- **Access:** paywall
- **Model:** couples a slope-stability (SLIDE) landslide module with CAESAR-Lisflood (details not assessed).
- **Reimplementability:** 1 1 1 1 1 → 5, C. Assessed from: metadata only (provisional).
- **Relevance:** longlist link L7 (landslide → river blockage → flood) — a ready-made coupling concept.

### spataro2010latest — The latest release of the lava flows simulation model SCIARA
- **Citation:** Spataro, W., Avolio, M. V., Lupiano, V., Trunfio, G. A., Rongo, R., D'Ambrosio, D. (2010). *Procedia Computer Science* 1(1), 17–26. DOI: 10.1016/j.procs.2010.04.004 (verified: Crossref)
- **Access:** OA (gold, CC BY-NC-ND) — publisher page returned 403 to the fetcher.
- **Phenomenon:** 2006 Etna lava flows; anisotropy test on a 5° inclined plane.
- **Model:** deterministic MCA, square grid with Moore neighbourhood (replacing hexagons), Bingham-like rheology inside the minimisation algorithm, improved cooling/solidification.
- **Code:** no official code; third-party CUDA implementation https://github.com/knotman90/SCIARA_FV2_CUDA (verified, unofficial).
- **Round 2 (secondary source):** Rongo et al. 2011 (SIMULTECH proceedings, DOI 10.5220/0003575900370044, verified; scitepress PDF read through WebFetch) restates SCIARA-fv2: substates altitude, thickness, temperature and 8 outflows; Moore neighbourhood; outflows by the minimisation algorithm with a critical thickness hc (Bingham-like); relaxation rate r and hc both log-linear in temperature between the solidus and vent values; diagonal neighbour altitudes sampled on a circle of radius one cell to remove anisotropy. Parameter names are listed but no values; cooling formula not restated.
- **Reimplementability:** S1 1; S2 1; S3 1; S4 1; S5 1 → 5, C. Assessed from: abstract + secondary (provisional). Round 2: no change; Elsevier still blocks the OA PDF.
- **Browser fit:** good (MCA is GPU/WebGL friendly).
- **Relevance:** HAZ-05.

### connor2012probabilistic — Probabilistic approach to modeling lava flow inundation: a lava flow hazard assessment for a nuclear facility in Armenia
- **Citation:** Connor, L. J., Connor, C. B., Meliksetian, K., Savov, I. (2012). *Journal of Applied Volcanology* 1(1), 3. DOI: 10.1186/2191-5040-1-3 (verified: Crossref)
- **Access:** OA (CC BY) — round 2: BMC PDF read in full.
- **Phenomenon:** lava-flow hazard for the Armenian nuclear power plant site (Shamiram Plateau, Aragats): vent-location probability (kernel density, SAMSE bandwidth, 18 volcanic centres) + lava inundation simulation, 10 000 Monte Carlo runs.
- **Model:** total erupted volume is added at the vent in pulses (10⁵ m³ per iteration on a 100 m grid, i.e. 10 m of thickness). Every inundated cell keeps a residual thickness (≈ modal flow thickness) before it passes lava on. Active cells keep a list entry with their parent cell; a neighbour qualifies only if its effective elevation (ground + lava) is below the active cell's and it is not the parent. Excess lava is shared among qualifying neighbours in proportion to the effective-elevation difference (L_n = X_a·D_n/ΣD). Iterations stop when the volume is used up. Deterministic per run; stochastic over runs. Iterations are only loosely linked to time (10³–10⁴ s per pulse for 10–100 m³/s).
- **Inputs:** SRTM (CGIAR-CSI) DEM resampled to 100 m; spatial density grid of vents.
- **Parameters:** configuration table given: residual thickness from a truncated normal (mean 7–8 m, SD 1–3 m, 4–15 m), log₁₀ volume truncated normal (mean 7.2, SD 0.5, 6–9), pulse 10⁵ m³, 10 000 runs, area of interest.
- **Code:** the PERL code of the paper is not released. Its successor MOLASSES (C, GPL-3, © L. Connor, J. Richardson, C. Connor; https://github.com/geoscience-community-codes/MOLASSES, verified) implements the same residual/parent/proportional-to-slope rule (modules `distribute_proportional2slope*`, `pulse`, `neighbor_*`) and ships test DEMs (flat, dipping planes) with configuration files. Dietterich et al. 2017 state that MOLASSES is based on this paper's algorithm.
- **Validation:** conditional and annual inundation probabilities for the site; simulated flow lengths compared with observed volume-limited flows (qualitative).
- **Reimplementability:** S1 2 – rule, stopping and stochastic inputs explicit (one small ambiguity: the text says "up to 3" neighbours); S2 2 – configuration table; S3 2 – authors' own successor code; S4 2 – SRTM; S5 1 – probabilities only, no test case → 9, A. Round 2: re-assessed from full text — S 2 2 2 2 1 (was 1 1 1 1 1).
- **Browser fit:** excellent — a few hundred lines; Monte Carlo ensembles of thousands of runs are feasible in a worker or on the GPU.
- **Relevance:** HAZ-05 primary candidate (simplest complete lava CA). The same residual-thickness rule could serve for mud or tailings spreading. For quantitative checks use `dietterich2017benchmarking`.

### kronholm2005integrating — Integrating spatial patterns into a snow avalanche cellular automata model
- **Citation:** Kronholm, K., Birkeland, K. W. (2005). *Geophysical Research Letters* 32(19). DOI: 10.1029/2005gl024373 (verified: Crossref)
- **Access:** paywall
- **Phenomenon:** fracture propagation in weak snow layers (slab-avalanche release), idealised.
- **Model:** CA with spatially structured shear strength; large-scale spatial structure favours wide fracture propagation.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2 (synthetic fields); S5 1 → 5, C. Assessed from: abstract (provisional).
- **Relevance:** HAZ-03 release-area concept; SOC family.

### bak1987selforganized — Self-organized criticality: An explanation of the 1/f noise
- **Citation:** Bak, P., Tang, C., Wiesenfeld, K. (1987). *Physical Review Letters* 59(4), 381–384. DOI: 10.1103/physrevlett.59.381 (verified: Crossref)
- **Access:** paywall
- **Model:** the sandpile automaton that defines SOC (rules not assessed from this source — abstract withheld).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2; S5 1 → 5, C. Assessed from: metadata only (provisional). Round 2: only an image-only scan was found (no text layer); not re-assessed.
- **Browser fit:** trivial.
- **Relevance:** foundation for landslide/avalanche magnitude–frequency demos; teaching baseline.

### hergarten1998selforganized — Self-organized criticality in a landslide model
- **Citation:** Hergarten, S., Neugebauer, H. J. (1998). *Geophysical Research Letters* 25(6), 801–804. DOI: 10.1029/98gl50419 (verified: Crossref)
- **Access:** paywall
- **Model:** physically based slope-stability + mass-movement model formulated with PDEs (explicitly **not** a CA) that still shows SOC and power-law landslide sizes.
- **Reimplementability:** 1 1 0 2 1 → 5, C. Assessed from: abstract (provisional).
- **Relevance:** context for HAZ-02 trigger statistics; a discretised version would be CA-like.

### werner1995eolian — Eolian dunes: Computer simulations and attractor interpretation
- **Citation:** Werner, B. T. (1995). *Geology* 23(12), 1107. DOI: 10.1130/0091-7613(1995)023<1107:EDCSAA>2.3.CO;2 (verified: Crossref)
- **Access:** paywall
- **Model:** foundational slab-based dune CA (rules not assessed — abstract withheld).
- **Reimplementability:** 1 1 0 2 1 → 5, C. Assessed from: metadata only (provisional). Round 2: closed access; unchanged.
- **Relevance:** dunes; very browser-friendly family.

### baas2007modelling — Modelling vegetated dune landscapes
- **Citation:** Baas, A. C. W., Nield, J. M. (2007). *Geophysical Research Letters* 34(6). DOI: 10.1029/2006gl029152 (verified: Crossref)
- **Access:** paywall
- **Model:** self-organising CA (DECAL) for dunes with plant responses; reproduces parabolic and nebkha dunes; phase diagram vs. vegetation vitality.
- **Code:** only post-processing scripts https://github.com/robintw/DunesGIS (verified; not the model).
- **Reimplementability:** 1 1 0 2 1 → 5, C. Assessed from: abstract (provisional).
- **Relevance:** coastal dunes; eco-geomorphic coupling (overlap with `eco`).

### segre1995cellular — Cellular automaton for realistic modelling of landslides
- **Citation:** Segre, E., Deangeli, C. (1995). *Nonlinear Processes in Geophysics* 2(1), 1–15. DOI: 10.5194/npg-2-1-1995 (verified: Crossref)
- **Access:** OA (scanned PDF, text not machine-readable here)
- **Model:** debris-flow CA over 3-D topography derived from sandpile automata; validated against field data; intermittent statistics.
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance:** HAZ-02; bridge between SOC sandpiles and realistic runout.

### heung2013modelling — Modelling the dynamics of soil redistribution induced by sheet erosion using the USLE and cellular automata
- **Citation:** Heung, B., Bakker, L., Schmidt, M. G., Dragićević, S. (2013). *Geoderma* 202–203, 112–125. DOI: 10.1016/j.geoderma.2013.03.019 (verified: Crossref)
- **Access:** paywall
- **Model:** USLE soil loss combined with a CA redistribution rule (details not assessed).
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HYD-05 — USLE factors (R, K, LS, C, P) exist for CZ; good candidate for a landscape-scale demo once rules are confirmed.

### guthrie2008exploring — Exploring the magnitude–frequency distribution: a cellular automata model for landslides
- **Citation:** Guthrie, R. H., Deadman, P. J., Cabrera, A. R., Evans, S. G. (2008). *Landslides* 5(1), 151–159. DOI: 10.1007/s10346-007-0104-1 (verified: OpenAlex [2007 online] + Crossref)
- **Access:** paywall
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-02 statistics (SOC family).

### lai2013integration — Integration of multicriteria evaluation and cellular automata methods for landslide simulation modelling
- **Citation:** Lai, T., Dragićević, S., Schmidt, M. (2013). *Geomatics, Natural Hazards and Risk* 4(4), 355–375. DOI: 10.1080/19475705.2012.746243 (verified: OpenAlex + Crossref)
- **Access:** OA (bronze) — publisher returned 403 to the fetcher.
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-02; MCE susceptibility (slope, geology, land cover) as CA input — fits CZ open layers. Priority for round 2 full-text reading.

### clerici2000simulation — Simulation of the Parma River blockage by the Corniglio landslide (Northern Italy)
- **Citation:** Clerici, A., Perego, S. (2000). *Geomorphology* 33(1–2), 1–23. DOI: 10.1016/s0169-555x(99)00095-1 (verified: Crossref)
- **Access:** paywall
- **Model:** CA simulation of an earth-flow advancing into a river (details not assessed; CA nature from search context).
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** L7 chain (landslide → river blockage).

### avolio2013sciddica — SCIDDICA-SS3: a new version of cellular automata model for simulating fast moving landslides
- **Citation:** Avolio, M. V., Di Gregorio, S., Lupiano, V., Mazzanti, P. (2013). *The Journal of Supercomputing* 65(2), 682–696. DOI: 10.1007/s11227-013-0948-1 (verified: Crossref)
- **Access:** paywall
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-02; successor of S3-hex with inertial effects.

### barca1994cellular — Cellular automata for simulating lava flows: A method and examples of the Etnean eruptions
- **Citation:** Barca, D., Crisci, G. M., Di Gregorio, S., Nicoletta, F. (1994). *Transport Theory and Statistical Physics* 23(1–3), 195–232. DOI: 10.1080/00411459408203862 (verified: Crossref)
- **Access:** paywall
- **Model:** first lava application of the minimisation-of-differences outflow scheme (as stated in dambrosio2003simulating).
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-05, historical.

### crisci2004simulation — The simulation model SCIARA: the 1991 and 2001 lava flows at Mount Etna
- **Citation:** Crisci, G. M., Rongo, R., Di Gregorio, S., Spataro, W. (2004). *Journal of Volcanology and Geothermal Research* 132(2–3), 253–267. DOI: 10.1016/s0377-0273(03)00349-4 (verified: Crossref)
- **Access:** paywall
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-05.

### vicari2007modeling — Modeling of the 2001 lava flow at Etna volcano by a Cellular Automata approach
- **Citation:** Vicari, A., Herault, A., Del Negro, C., Coltelli, M., Marsella, M., Proietti, C. (2007). *Environmental Modelling & Software* 22(10), 1465–1471. DOI: 10.1016/j.envsoft.2006.10.005 (verified: OpenAlex + Crossref)
- **Access:** paywall
- **Model:** MAGFLOW CA (details not assessed).
- **Code:** not found (GPU ports are described in Annals of Geophysics 2011 papers, seen in OpenAlex search; code not public).
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-05; alternative to SCIARA.

### bilotta2012sensitivity — Sensitivity analysis of the MAGFLOW Cellular Automaton model for lava flow simulation
- **Citation:** Bilotta, G., Cappello, A., Hérault, A., Vicari, A., Russo, G., Del Negro, C. (2012). *Environmental Modelling & Software* 35, 122–131. DOI: 10.1016/j.envsoft.2012.02.015 (verified: Crossref)
- **Access:** paywall
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-05; likely the best source for MAGFLOW parameter ranges (round 2).

### miyamoto1997simulating — Simulating lava flows by an improved cellular automata method
- **Citation:** Miyamoto, H., Sasaki, S. (1997). *Computers & Geosciences* 23(3), 283–292. DOI: 10.1016/s0098-3004(96)00089-1 (verified: Crossref)
- **Access:** paywall
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-05.

### barpi2007cellular — Cellular-Automata Model for Dense-Snow Avalanches
- **Citation:** Barpi, F., Borri-Brunetto, M., Delli Veneri, L. (2007). *Journal of Cold Regions Engineering* 21(4), 121–140. DOI: 10.1061/(ASCE)0887-381X(2007)21:4(121) (verified: Crossref)
- **Access:** green OA in the Politecnico di Torino repository (hdl.handle.net/11583/1514984, per Semantic Scholar; not fetched — 403)
- **Phenomenon:** three documented dense-snow avalanches, Susa Valley (Italian Alps, EU).
- **Model:** 3-D CA on a DTM including snowpack erosion and deposition; calibrated on qualitative observations; reproduces path and deposit volume order of magnitude.
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance:** HAZ-03 (physically richer alternative to Flow-Py).

### avolio2010development — Development and Calibration of a Preliminary Cellular Automata Model for Snow Avalanches
- **Citation:** Avolio, M. V., Errera, A., Lupiano, V., Mazzanti, P., Di Gregorio, S. (2010). In: *Lecture Notes in Computer Science*, pp. 83–94. Springer. DOI: 10.1007/978-3-642-15979-4_9 (verified: Crossref)
- **Access:** paywall
- **Reimplementability:** 1 1 0 1 1 → 4, C. Assessed from: metadata only (provisional).
- **Relevance:** HAZ-03; MCA family applied to avalanches.

### digregorio1999empirical — An empirical method for modelling and simulating some complex macroscopic phenomena by cellular automata
- **Citation:** Di Gregorio, S., Serra, R. (1999). *Future Generation Computer Systems* 16(2–3), 259–271. DOI: 10.1016/s0167-739x(99)00051-5 (verified: Crossref)
- **Access:** paywall
- **Value as entry point:** methodological basis of the MCA family (substates, elementary processes, minimisation of differences); cited by SCIDDICA and SCIARA papers for the algorithm's theorems. Needed to resolve the remaining ambiguities in S3-hex. **Reimplementability: n/a.**

### coulthard2007cellular — Cellular modelling of river catchments and reaches: Advantages, limitations and prospects
- **Citation:** Coulthard, T. J., Hicks, D. M., Van De Wiel, M. J. (2007). *Geomorphology* 90(3–4), 192–207. DOI: 10.1016/j.geomorph.2006.10.030 (verified: Crossref)
- **Access:** paywall
- **Value as entry point:** review of reduced-complexity cellular fluvial models (catchment and reach scale). **n/a.**

### tucker2010modelling — Modelling landscape evolution
- **Citation:** Tucker, G. E., Hancock, G. R. (2010). *Earth Surface Processes and Landforms* 35(1), 28–50. DOI: 10.1002/esp.1952 (verified: Crossref)
- **Access:** paywall
- **Value as entry point:** broad review of LEMs and geomorphic transport laws; places cellular models among continuum LEMs. **n/a.**

### dietterich2017benchmarking — Benchmarking computational fluid dynamics models of lava flow simulation for hazard assessment, forecasting, and risk management (round 2)
- **Citation:** Dietterich, H. R., Lev, E., Chen, J., Richardson, J. A., Cashman, K. V. (2017). *Journal of Applied Volcanology* 6, 9. DOI: 10.1186/s13617-017-0061-x (verified: Crossref)
- **Access:** OA (CC BY), BMC PDF read in full.
- **Content:** Four benchmarks for lava-flow codes with analytical or laboratory references: BM-A isothermal isoviscous sloping flow, BM-B the same with obstacles, BM-C cooling axisymmetric flow, BM-D cooling and solidifying molten basalt on a slope. Several codes, including FLOW-3D, OpenFOAM and **MOLASSES** (a CA based on connor2012probabilistic; Moore neighbourhood, spreading proportional to slope above a critical thickness, volume steps as time steps).
- **Results:** NRMSE of flow length, width and thickness for every code; MOLASSES reaches about 4–12 % on the isothermal cases and reproduces flow around obstacles.
- **Reimplementability (of the MOLASSES set-up):** S1 1 – CA rules only summarised; S2 1; S3 2 – MOLASSES open; S4 2 – synthetic benchmark geometries; S5 2 – NRMSE tables → 8, B. Assessed from: full text.
- **Relevance:** HAZ-05. Ready-made quantitative checks for a ca-geo lava CA (BM-A/B need only a sloping plane and an obstacle).

### wichmann2017gpp — The Gravitational Process Path (GPP) model (v1.0) – a GIS-based simulation framework for gravitational processes (round 2)
- **Citation:** Wichmann, V. (2017). *Geoscientific Model Development* 10(9), 3309–3327. DOI: 10.5194/gmd-10-3309-2017 (verified: Crossref)
- **Access:** OA (CC BY), full text read.
- **Phenomenon:** process paths, runout and deposition of rockfall, debris flows and snow avalanches on a raster DTM; examples from the Alps.
- **Model:** a mass point moves cell to cell over the 8 neighbours. Path options: steepest descent or a random walk in which lower neighbours are admitted by a slope threshold and a divergence exponent a (Gamma-like criterion), then chosen with probability proportional to slope × a persistence factor p for the previous direction; many repetitions per start cell. Runout by geometric gradient, Fahrböschung, shadow angle, or one- and two-parameter friction models (velocity along the path); optional sink filling and deposition. Not called a CA, but every step is a local neighbourhood rule.
- **Parameters:** tables of typical configurations and parameter ranges for rockfall (e.g. divergence exponent 1.5–2.0, persistence 1.0–1.6), debris flow and avalanche, plus friction coefficients per land cover (e.g. rockfall material, meadow, alpine shrubs, forest); full parameter list in Appendix A.
- **Code:** in SAGA GIS (GPL), "Geomorphology" tool library; SourceForge https://sourceforge.net/projects/saga-gis/ (bot-blocked) and GitHub https://github.com/saga-gis/saga-gis (HTTP 200).
- **Validation:** sensitivity figures and application examples; no quantitative test set in the paper.
- **Reimplementability:** S1 2; S2 1 – ranges, not one calibrated set; S3 2; S4 2 – DTM + release areas; S5 1 → 8, B. Assessed from: full text.
- **Browser fit:** very good (independent random walks, embarrassingly parallel).
- **Relevance to ca-geo:** HAZ-02, HAZ-03 and **rockfall** (new phenomenon candidate). An alternative to Flow-Py with stochastic paths; friction per land cover fits CZ land-cover layers.

### horton2013flowr — Flow-R, a model for susceptibility mapping of debris flows and other gravitational hazards at a regional scale (round 2)
- **Citation:** Horton, P., Jaboyedoff, M., Rudaz, B., Zimmermann, M. (2013). *Natural Hazards and Earth System Sciences* 13(4), 869–885. DOI: 10.5194/nhess-13-869-2013 (verified: Crossref)
- **Access:** OA (CC BY), full text read.
- **Phenomenon:** regional debris-flow source identification and propagation (also used for rockfall, avalanches); Swiss case studies (Solalex and others).
- **Model:** sources from thresholds on slope, flow accumulation, lithology and land use; spreading by a modified Holmgren multiple-flow-direction rule (exponent x, central-cell raise dh to reduce DEM noise), weighted by a persistence function (three variants, tabulated); runout from a simple energy balance with a minimum travel angle and a maximum velocity. Propagation from each source with an active-cell list.
- **Parameters:** recommended exponents, travel angles (e.g. about 11° for Alpine debris flows) and velocity limits; 10 m DEM recommended.
- **Code:** free stand-alone Matlab-compiled application, http://www.flow-r.org (HTTP 200) and https://wp.unil.ch/risk/flow-r/ (HTTP 200); source not open → S3 1.
- **Validation:** qualitative comparison with mapped events; sensitivity to DEM resolution and parameters.
- **Reimplementability:** S1 2; S2 1; S3 1; S4 2; S5 1 → 7, B. Assessed from: full text.
- **Browser fit:** very good (single sweep per source).
- **Relevance:** HAZ-02. Inventories from the Hrubý Jeseník (Storm Boris 2024, `tichavsky2026hydrogeomorphic`) could serve as a CZ check for Flow-R-like or Flow-Py-like runout.

### yizhaq2017scalefree — Scale-free distribution of Dead Sea sinkholes: Observations and modeling (round 2)
- **Citation:** Yizhaq, H., Ish-Shalom, C., Raz, E., Ashkenazy, Y. (2017). *Geophysical Research Letters* 44(10), 4944–4952. DOI: 10.1002/2017gl073655 (verified: Crossref)
- **Access:** paywall; author preprint arXiv:1611.00940 read in full.
- **Phenomenon:** formation and growth of collapse sinkholes along the Dead Sea shore; sinkhole-area statistics from field mapping.
- **Model:** two-layer stochastic CA on a 1024 × 1024 grid. Lower layer (salt): cells become cavities with a probability that grows with the number of cavity neighbours (von Neumann) and with the size of the cavity cluster (dissolution efficiency parameter). Upper layer (soil): cells above a cavity collapse with a probability that grows with the cavity size (soil-strength parameter). Explicit five-step update order.
- **Parameters:** initial cavity probability and the two process parameters; ranges that match the field statistics are shown.
- **Code:** not found.
- **Validation:** sinkhole-area distributions follow power laws with exponent ≈ 1.9–2.0 in the model and 1.5–2.0 in the field.
- **Reimplementability:** S1 2; S2 1; S3 0; S4 2 – synthetic grids; S5 2 – power-law exponents → 7, B. Assessed from: full text (preprint).
- **Browser fit:** trivial.
- **Relevance:** new phenomenon candidate (sinkholes / collapse). Not geo-referenced; would need a DEM-based susceptibility layer for a CZ demo.

### chen2020dynamic — Dynamic simulation for the process of mining subsidence based on cellular automata model (round 2)
- **Citation:** Chen, Q., Li, J., Hou, E. (2020). *Open Geosciences* 12(1), 832–839. DOI: 10.1515/geo-2020-0172 (verified: Crossref)
- **Access:** OA (CC BY); De Gruyter blocked the PDF; abstract via Semantic Scholar.
- **Phenomenon:** time evolution of a subsidence basin above a coal mine (East China), as a basis for land-reclamation planning.
- **Model:** CA built from mining-subsidence theory, implemented with ArcGIS and Python; prediction reported to agree with observations. Rules not read.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance:** new phenomenon candidate (mining subsidence), highly relevant to the Ostrava–Karviná coalfield; could feed LND-03-style flooding of subsidence troughs.

### liu2012cellular — A cellular automata model for the process of rill erosion (round 2)
- **Citation:** Liu, X., Yuan, L. (2012). In: *2012 International Symposium on Geomatics for Integrated Water Resource Management*, 1–3. IEEE. DOI: 10.1109/giwrm.2012.6349546 (verified: Crossref)
- **Access:** paywall; abstract withheld.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D. Assessed from: metadata only (provisional).
- **Relevance:** HYD-05; a short alternative to RillGrow, not assessable.

### parise2012swii2 — Swii2, a HTML5/WebGL Application for Cellular Automata Debris Flows Simulation (round 2)
- **Citation:** Parise, R., D'Ambrosio, D., Spingola, G., Filippone, G., Rongo, R., Trunfio, G. A., Spataro, W. (2012). In: *Lecture Notes in Computer Science* (ACRI 2012), 444–453. Springer. DOI: 10.1007/978-3-642-33350-7_46 (verified: Crossref)
- **Access:** paywall; abstract withheld.
- **Content:** a browser (HTML5/WebGL) application for SCIDDICA debris-flow simulation (from the title; details not read).
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 0 → 2, D. Assessed from: metadata only.
- **Relevance:** **direct browser precedent** for ca-geo (MCA in WebGL, 2012); worth a manual read for architecture lessons. Overlap with `gen`.

### tichavsky2026hydrogeomorphic — Hydrogeomorphic effects of Storm Boris (2024) in the rainfall epicentre (NE Czechia) and a century of extreme rainfall patterns (round 2)
- **Citation:** Tichavský, R., Rozsívalová, E., Tolasz, R. (2026). *Natural Hazards* 122(4). DOI: 10.1007/s11069-025-07960-3 (verified: Crossref)
- **Content (from search snippet, not read):** field inventory of new debris-flow paths in the Hrubý Jeseník after the September 2024 storm, related to topographic indices. Not a CA.
- **Reimplementability:** n/a (data source). Value: a recent **CZ** event inventory to check HAZ-02 runout demos (Flow-Py / GPP / SCIDDICA-like) on Czech terrain.

## Most reimplementable (top picks)

1. **damboise2022flowpy** (A, 10) — open Python code, 4 parameters, analytical tests; DEM + release mask only; covers avalanches, rockfall and debris-flow runout (HAZ-03, HAZ-02).
2. **eltner2025using** (A, 9) — RillGrow open code + open CZ (CTU Prague) observation data; quantitative checks; plot scale only (HYD-05).
3. **dambrosio2003simulating** (B, 8) — complete SCIDDICA S3-hex rules with parameter values and areal fitness metrics; the MCA template for all surface flows (HAZ-02, reusable for HAZ-05).
4. **skinner2023testing / coulthard2013integrating** (B, 8/7) — CAESAR-Lisflood open source with open test data; best route to river morphodynamics (HYD-07).
5. **kochanski2019rescal** (B, 8) — open dune CA code; needs 2-D reduction for the browser.
6. **connor2012probabilistic + MOLASSES** (A, 9; round 2) — the simplest complete lava CA (residual thickness, parent cell, slope-proportional sharing) with the authors' GPL successor code; quantitative checks in `dietterich2017benchmarking` (B 8). Best HAZ-05 candidate.
7. **wichmann2017gpp** (B, 8; round 2) — open SAGA random-walk + friction runout model with parameter ranges for rockfall, debris flows and avalanches.
8. **horton2013flowr** (B, 7; round 2) — complete MFD + persistence + energy-line runout rules; free binary only.

Still expected to climb if full texts become available: bak1987selforganized (scan only),
murray1994cellular, werner1995eolian (closed access), spataro2010latest (Elsevier OA blocked).

## Gaps and unverified leads

- **OpenAlex quota exhausted** — no OpenAlex citation counts after the first ~9 queries;
  all metadata verified via Crossref instead. Round 2 should re-run the searches in
  OpenAlex for hit counts and OA links.
- **Abstract-withheld papers** (Elsevier, Springer, Nature, T&F): 17 entries assessed from
  metadata only. Round 2: obtain full texts (library access) for Murray & Paola 1994,
  Werner 1995, Bak et al. 1987, Van De Wiel 2007, Heung 2013, Lai 2013, Clerici 2000,
  MAGFLOW papers, Miyamoto 1997.
- **Rockfall CA:** round 2 again found no rockfall CA (Crossref and web); only discrete-element
  models (non-CA). Rockfall is best covered by raster runout tools with local rules:
  `damboise2022flowpy` (A) and `wichmann2017gpp` (B), and by `horton2013flowr` (B).
- **MOLASSES:** round 2 confirmed it is the authors' successor of connor2012probabilistic and is
  benchmarked in `dietterich2017benchmarking` (verified). Still no method paper of its own;
  Gallant et al. 2018 (Geology, 10.1130/g45123.1, seen in Crossref, not read) applies it.
  Dietterich et al. cite an older repository URL (github.com/usfvolcanology/molasses, not checked).
- **Q-LavHA** (QGIS lava hazard plugin): only a 2025 application paper seen (Volcanica,
  DOI prefix 10.30909); the plugin URL tried returned 404. Unverified.
- **ReSCAL original distribution** (Narteau, IPGP) — URL unreachable; only the rescal-snow
  fork verified.
- **SCIDDICA / SCIARA official code:** only OpenCAL's SciddicaT and third-party
  implementations verified; ask authors or search OpenCAL examples further.
- **Additional leads seen in searches but not catalogued:** Thomas & Nicholas braided
  cellular models (Geomorphology 2007; book chapter 2006), Coulthard et al. 1998 HESS (OA,
  nonlinearity and resolution in CAESAR), Coulthard 2001 LEM software review, Van De Wiel &
  Coulthard 2010 (SOC in river basins), Hancock et al. 2010 (SIBERIA vs CAESAR), Zhang et al.
  2010 (barchan dunes CA), Nield & Baas 2008 (parabolic/nebkha), Bolgov 2022 (avalanche CA,
  Russia), D'Ambrosio et al. 2006 (parallel GA calibration of SCIDDICA), Parise et al. 2012
  (Swii2 HTML5/WebGL debris-flow viewer — direct browser precedent!), Rongo et al. 2016
  (SCIARA review), Cappello et al. 2011 (MAGFLOW hazard-map validation, OA), Ma et al. 2009,
  Sun et al. 2022, Tang et al. 2022 (soil erosion CA, China), runoutSIM 2025 preprint
  (random-walk landslide runout in R).
- **CZ studies:** round 2 (Crossref + Czech/English web search) still found no Czech or
  Central-European CA mass-movement study and no Czech Flow-R/Flow-Py application. CZ
  anchors now: CTU erosion data (`eltner2025using`), the open CTU erosion code SMODERP2D
  (`landa2019smoderp2d`, in hydrology.md), the Storm Boris debris-flow inventory
  (`tichavsky2026hydrogeomorphic`) and earlier Hrubý Jeseník / Krkonoše debris-flow and avalanche
  studies (seen in search: Křížek et al. 2018 map of debris-flow paths; a GRASS-based Krkonoše
  avalanche susceptibility map; neither verified). Mining subsidence (Ostrava–Karviná) is a new CZ
  phenomenon candidate (`chen2020dynamic`).
- **Karst / river ice:** no karst-landscape CA (dolines, conduits) found; only the Dead Sea
  sinkhole CA (`yizhaq2017scalefree`). No river-ice CA found (see hydrology.md).
- **Swii2** (`parise2012swii2`): browser precedent; full text needed (Springer LNCS).
- **Overlaps:** CAESAR-Lisflood and LISFLOOD-FP with `hyd`; Rescal-snow and snow drift with
  `atm`; DECAL vegetation–dune coupling with `eco`; OpenCAL, ReSCAL, MCA methodology and
  GPU/WebGL ports (Swii2, MAGFLOW CUDA) with `gen`.

## Round 2 changes

| Key | Old score / class | New score / class | Reason |
|---|---|---|---|
| connor2012probabilistic | 1 1 1 1 1 = 5 C | 2 2 2 2 1 = 9 A | Full text read: complete rule and configuration table; MOLASSES confirmed as the authors' successor code |
| spataro2010latest | 5 C | 5 C (unchanged) | Only a secondary restatement (Rongo et al. 2011) read; parameter values still missing |
| coulthard2013integrating | 7 B | 7 B (unchanged) | Zenodo code and parameter listings verified; no full text |
| bak1987selforganized, murray1994cellular, werner1995eolian | 5 C | 5 C (unchanged) | No readable full text (closed / image-only scan) |
| wichmann2017gpp (new) | – | 2 1 2 2 1 = 8 B | OA, open SAGA code, rockfall included |
| dietterich2017benchmarking (new) | – | 1 1 2 2 2 = 8 B | Lava benchmarks with NRMSE for the MOLASSES CA |
| horton2013flowr (new) | – | 2 1 1 2 1 = 7 B | OA, full rules; binary-only code |
| yizhaq2017scalefree (new) | – | 2 1 0 2 2 = 7 B | Sinkhole CA, full rules (preprint) |
| chen2020dynamic (new) | – | 1 1 0 1 1 = 4 C | Mining-subsidence CA, abstract only |
| liu2012cellular (new) | – | 1 0 0 1 1 = 3 D | metadata only |
| parise2012swii2 (new) | – | 1 0 0 1 0 = 2 D | metadata only; browser precedent |
| tichavsky2026hydrogeomorphic (new) | – | n/a | CZ event inventory (data source) |

## New phenomena candidates (round 2)

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| Rockfall runout | Paths and stopping of falling blocks from cliff cells downslope (random walk or MFD + friction / energy line) | Very cheap, visual; forest as protection (friction per land cover) | High: sandstone rock towns (Labské pískovce, Adršpach), rockfalls on roads and railways in the Bohemian Massif valleys | `wichmann2017gpp` B, `damboise2022flowpy` A, `horton2013flowr` B | HAZ-02 covers landslides/debris flows only; could be a separate item or a HAZ-02 variant |
| Collapse sinkholes | Cavity growth in a soluble or undermined layer and collapse of the cover; size statistics | Simple two-layer stochastic CA with clear power-law check | Medium: Moravian Karst dolines; collapse pits above old mines (e.g. Kutná Hora, Ostrava) | `yizhaq2017scalefree` B | Synthetic grid only; needs a susceptibility layer for geodata |
| Mining subsidence | Growth of a subsidence basin above underground coal mining | Couples with WAT ponding (subsidence lakes) and LND-03 | High: Ostrava–Karviná coalfield | `chen2020dynamic` C | Also listed in hydrology.md |
| Aeolian dunes (incl. vegetated dunes) | Sand slabs eroded, transported and deposited by wind; avalanching at the angle of repose; vegetation stabilisation | Classic, very browser-friendly CA family; strong teaching value | Low–medium: inland dune fields (e.g. Bzenec "Moravian Sahara", Labe terraces), mostly stabilised | `kochanski2019rescal` B, `werner1995eolian` C, `baas2007modelling` C | Found in round 1 but not on the longlist |
