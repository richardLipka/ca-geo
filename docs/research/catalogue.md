# Catalogue of geographic CA models — round 1 summary

Cross-domain summary of the breadth-first literature survey (round 1, 2026-10-12). It is the
basis for selecting models to implement. Details, full entries and search logs are in
`domains/*.md`; scoring follows `reimplementability-criteria.md`; all references are in
`/references.bib`.

## How to read this

- **Class** A–D = reimplementability (A: direct reimplementation, B: minor assumptions,
  C: template for our own variant, D: inspiration only). `n/a` = review / framework / method.
- **Most scores are provisional.** Many publishers blocked automated full-text reading, so
  a large share of entries was scored from abstracts (S1, S2 capped at 1). Class C is
  therefore over-represented; several C entries are expected to rise after a manual
  full-text read (round 2).
- **Code** = open code verified to exist. Third-party implementations count as S3 = 1
  (harmonised rule, see "Quality control").
- Longlist IDs refer to `docs/brainstorm/longlist.md`; `WAT` = water model with scenarios.

## Overview

| Domain | File | Entries | A | B | C | D | n/a |
|---|---|---|---|---|---|---|---|
| Hydrology and floods | `domains/hydrology.md` | 32 | 2 | 4 | 16 | 5 | 5 |
| Fire | `domains/fire.md` | 29 | 3 | 2 | 16 | 5 | 3 |
| Land use and urban growth | `domains/land-use.md` | 36 | 2 | 4 | 28 | 0 | 2 |
| Geomorphology and mass movements | `domains/geomorphology.md` | 38 | 2 | 4 | 29 | 0 | 3 |
| Ecology and forestry | `domains/ecology.md` | 39 | 1 | 10 | 19 | 0 | 9 |
| Epidemics and populations | `domains/epidemics.md` | 36 | 2 | 11 | 19 | 1 | 3 |
| Movement of people and vehicles | `domains/movement.md` | 32 | 2 | 6 | 17 | 2 | 5 |
| Atmosphere, climate, water bodies, other | `domains/atmosphere-other.md` | 29 | 3 | 3 | 16 | 7 | 0 |
| Cross-cutting (reviews, frameworks, methods) | `domains/general.md` | 50 (+8 software without DOI) | 1 | 2 | 10 | 1 | 36 |
| **Total (with cross-domain duplicates)** | | **321** | **18** | **46** | **170** | **21** | **66** |

310 unique publications (11 appear in two or three domains), plus 8 documented software
packages without a DOI in `general.md`.

## Shortlist — class A and B models

Sorted by domain, then score. *Code*: ✓ = authors' open code, 3rd = third-party only,
– = none found. *Assessed*: F = full text, P = provisional (abstract / secondary source).

| Key | Class (score) | Model / phenomenon | Code | Assessed | Longlist | Note for ca-geo |
|---|---|---|---|---|---|---|
| `barnes2021computing` | A (10) | Fill–Spill–Merge, depression filling | ✓ | F | WAT | Not a CA; reference steady state for ponding tests. |
| `callaghan2019computing` | A (9) | FlowFill, mass-conserving runoff into depressions | ✓ | F | WAT | Simplest local water rule; first WAT demo. |
| `guidolin2016weighted` | B (7) | WCA2D weighted flood CA | ✓ (framework) | P | WAT | De-facto standard fast flood CA; EA benchmark tests. |
| `wijaya2023rapid` | B (7) | Hybrid inundation model, Manning-flux CA | – | F | WAT | Coarse + fine downscaling idea for the browser. |
| `coulthard2013integrating` | B (7) | CAESAR-Lisflood | ✓ | P | WAT, HYD-07 | Local-inertial flow + landscape evolution. |
| `barnes2014priority` | B (7) | Priority-Flood | ✓ | P | WAT | Not a CA; DEM preprocessing (depression filling). |
| `xia2025pytorchfire` | A (10) | PyTorchFire, stochastic wildfire CA | ✓ | F | HAZ-01 | Cleanest modern statement of the classic stochastic rule. |
| `trucchia2020propagator` | A (9) | PROPAGATOR (IT/ES, operational) | ✓ | P | HAZ-01 | EU fuel-class table in code; probability maps. |
| `pais2021cell2fire` | A (9) | Cell2Fire, elliptical spread on grid | ✓ | F | HAZ-01 | Reduces grid anisotropy; Canadian fuels need mapping. |
| `freire2019using` | B (8) | Wildfire CA, Portugal, CORINE fuels | 3rd | F | HAZ-01 | EU case with timing metrics; wind non-local rule. |
| `alexandridis2008cellular` | B (8) | Classic stochastic wildfire CA (Spetses) | 3rd | P | HAZ-01 | Base rule for most later work. |
| `roodposhti2020towards` | A (10) | SIMLANDER, neighbourhood auto-calibration | ✓ | F | LND-01 | Fastest route to a calibrated CZ urban-growth demo. |
| `clarke1997selfmodifying` | A (9) | SLEUTH origin, self-modifying urban CA | ✓ | P | LND-01 | Classic; demo dataset with expected outputs. |
| `petrasova2016open` | B (8) | FUTURES (GRASS GIS) | ✓ | F | LND-01 | Patch-based suburban growth. |
| `zhou2019highresolution` | B (8) | Global SLEUTH projection | ✓ | F | LND-01 | Published probability layer covering Czechia. |
| `liang2021understanding` | B (7) | PLUS, multi-class land use | binary only | F | LND-01, LND-02 | Equations suffice for JS reimplementation. |
| `hewitt2019cellular` | B (7) | SIMLANDER base model | ✓ | P | LND-01 | Base of `roodposhti2020towards`. |
| `damboise2022flowpy` | A (10) | Flow-Py, gravitational runout | ✓ | F | HAZ-02, HAZ-03 | Avalanche, rockfall, debris-flow runout; 4 parameters, analytical tests. |
| `eltner2025using` | A (9) | RillGrow soil erosion, CTU Prague data | ✓ | F | HYD-05 | **CZ observation data**; plot scale only. |
| `dambrosio2003simulating` | B (8) | SCIDDICA S3-hex debris flows | partial | F | HAZ-02 | Macroscopic-CA template for surface flows. |
| `skinner2023testing` | B (8) | CAESAR-Lisflood vs grid size | ✓ | F | HYD-07 | Open test data on Zenodo. |
| `kochanski2019rescal` | B (8) | Rescal-snow dune CA | ✓ | F | — (new) | 3D, micro-scale; poor browser fit. |
| `liu2025multiscale` | A (9) | Stochastic CA, mountain pine beetle | ✓ | F | ECO-01 | Closest drop-in core for bark-beetle model. |
| `pietzsch2023nonparametric` | B (8) | Ips typographus Markov CA, Saxon Switzerland | ✓ | F | ECO-01 | **At the CZ border**; open code and data. |
| `seidl2017climate` | B (7) | iLand wind × bark beetle | ✓ | F | ECO-01, HAZ-04 | Individual-tree scale; heavy. |
| `seidl2014simulating` | B (7) | iLand wind disturbance | ✓ | P | HAZ-04 | — |
| `rademacher2004reconstructing` | B (7) | BEFORE beech forest model | – | F (ODD) | ECO-02, HAZ-04 | Central European forest mosaic. |
| `thiery1995model` | B (7) | Banded vegetation CA | – | F | ECO-08 | Tiny anisotropic kernel. |
| `schneider2016spatially` | B (7) | Dryland grazing CA | ✓ (caspr) | P | ECO-08 | Test oracle in caspr. |
| `moenickes2013shapes` | B (7) | Giant hogweed invasion CA | – | F | ECO-03 | Corridor + long-distance dispersal; fit targets. |
| `engler2012migclim` | B (7) | MigClim range shift | ✓ | P | ECO-07 | — |
| `nobis2014kissmig` | B (7) | KISSMig range shift | ✓ | P | ECO-07 | Very simple 3×3 spread. |
| `bocedi2021rangeshifter` | B (7) | RangeShifter 2.0 | ✓ | P | ECO-07, ECO-04 | Individual-based; reference only. |
| `bradshaw2021stochastic` | A (10) | Stochastic peopling of Sahul, population CA | ✓ | F | — (new) | Population dispersal on carrying-capacity raster. |
| `gregoriodesouza2021reassessing` | A (9) | Farmer expansion CA | ✓ | F | — (new) | Compact growth / emigration CA. |
| `white2007modeling` | B (8) | SIR fraction CA | – | F | EPI-01 | Cleanest SIR CA rule. |
| `li2012consequences` | B (8) | Tick / Lyme CA, Belgium | – | F | EPI-03 | Turns EPI-03 into a dynamic model. |
| `white2017modelling` | B (8) | Xylella spread, Apulia | ✓ | F | ECO-03 | Stratified dispersal + control zones. |
| `smith2002predicting` | B (8) | Raccoon rabies, polygon CA with barriers | dead link | F | EPI-02, ECO-04 | Barrier demo (rivers, fences). |
| `jones2021iteratively` | B (8) | PoPS pest / pathogen platform | ✓ | F | ECO-03 | Mature open engine. |
| `bradshaw2023directionally` | B (7) | Sahul CA with "superhighways" | ✓ | P | — (new) | — |
| `schimit2021model` | B (7) | COVID-19 probabilistic CA, Brazil | – | F | EPI-01 | Very large lattice. |
| `davidson2024methodological` | B (7) | Geographic Cell-DEVS SEIRDS | ✓ | P | EPI-01 | Real regions; GeoJSON pipeline. |
| `ortigoza2020modelling` | B (7) | Chikungunya on triangular GIS mesh | not public | F | EPI-03 | — |
| `croft2020modelling` | B (7) | ASF in wild boar (Forest of Dean) | ✓ (suppl.) | F | EPI-02 | Individual-based, not a pure CA. |
| `martins2000cellular` | B (7) | Citrus chlorosis CA | – | F | — | — |
| `nagel1992cellular` | A (9) | Nagel–Schreckenberg traffic CA | 3rd | P | MOV-02 | Four-line rule; standard parameters. |
| `biham1992selforganization` | A (9) | BML 2D traffic CA | 3rd | P | MOV-02 | Sharp jamming transition; great browser demo. |
| `kirchner2002simulation` | B (8) | Floor-field pedestrian CA | – | F | MOV-01 | Canonical evacuation CA. |
| `kirchner2003friction` | B (8) | Floor field with friction (clogging) | – | F | MOV-01 | One extra parameter. |
| `rickert1996two` | B (8) | Two-lane traffic CA | – | F | MOV-02 | — |
| `knospe2000towards` | B (8) | Brake-light traffic CA | – | F | MOV-02 | Calibrated on motorway data. |
| `chowdhury1999selforganization` | B (8) | City network traffic CA with signals | – | F | MOV-02 | — |
| `weiss2018global` | B (7) | Global travel time to cities | closed platform | P | MOV-03 | Not a CA; open friction raster as reference. |
| `palermo2024newts` | A (9) | NEWTS coastal erosion by waves | ✓ | F | — (new) | Lake / sea shores; analytical tests. |
| `ravazzani2011macroscopic` | A (9) | Macroscopic CA for groundwater | ✓ | P | LND-03 | Theis benchmark; trivial stencil. |
| `sharma2019understanding` | A (9) | Snow bedforms with sintering | ✓ | F | — (new) | 3D; poor browser fit. |
| `ashton2001formation` | B (7) | Coastline Evolution Model | ✓ | P | — (new) | Likely A after full-text read. |
| `ashton2006highangle` | B (7) | CEM high-angle waves | ✓ | P | — (new) | — |
| `pontius2011death` | A (9) | Quantity / allocation disagreement | ✓ | P | (validation) | First metric for the validation component. |
| `pontius2011comparison` | B (8) | Multi-resolution map comparison | ✓ | P | (validation) | — |
| `vanvliet2011revisiting` | B (7) | Kappa Simulation | closed | P | (validation) | — |

## Coverage of the longlist

How well each longlist item is supported by reimplementable literature. *Best* = best
class found; *Template* = recommended starting reference(s).

| Longlist | Proposed group | Best | Template | Comment |
|---|---|---|---|---|
| WAT water / flooding | core ★ | A | `callaghan2019computing`, `guidolin2016weighted`, `liu2015developing`, `bates2010simple` | Well covered; EA benchmark tests (not in Crossref) for validation. CZ study: `cirbus2013cellular`. |
| HAZ-01 wildfire | core ★ | A | `xia2025pytorchfire`, `trucchia2020propagator`, `freire2019using`, `pais2021cell2fire` | Well covered; no CZ fire CA. CZ calibration target: `kudlackova2024using` (Bohemian Switzerland, FlamMap, not CA). |
| ATM-02 cold-air pooling | core (proposed) | — | none | **No CA model found.** Would be our own variant derived from WAT rules — novel, but without literature support. |
| ECO-01 bark beetle | core (proposed) | A | `liu2025multiscale`, `pietzsch2023nonparametric` | Well covered; CZ parameter sources `dolezal2016fine`, `berec2013population`. |
| LND-01 urban growth | core (proposed) | A | `roodposhti2020towards`, `clarke1997selfmodifying`, `petrasova2016open` | Well covered; Prague suburban study `indrova2015land`. |
| MOV-03 accessibility front (+ECO-04) | extension | B | `weiss2018global`, `wood2012anisotropic`, `kramerschadt2004fragmented` | Mostly cost-distance, not CA; lynx connectivity on DE–CZ border. |
| HAZ-02 landslide (+HAZ-03 avalanche) | extension | A | `damboise2022flowpy`, `dambrosio2003simulating` | Flow-Py covers avalanche, rockfall and debris flow. |
| MOV-01 evacuation | extension | B | `kirchner2002simulation`, `kirchner2003friction` | No CA evacuation on real geography scores B; combine floor field + cost-distance. |
| ECO-03 invasive species | extension | B | `moenickes2013shapes`, `white2017modelling`, `jones2021iteratively` | CZ: `nehrbass2007simulation` (giant hogweed, Slavkovský les). |
| ATM-01 pollution / smoke | extension | C | `sonnenschein2025hybrid` | Weakly covered; scores provisional. |
| HYD-05 erosion / muddy floods | extension | A | `eltner2025using` | CZ data; but plot scale (cm), not catchment scale. |
| URB-03 urban fire (→ HAZ-01) | scenario | C | `tan2019fire`, `ohgai2007cellular`, `zhao2011simulation` | Building-based CA from Asia only. |
| HAZ-05 lava | out of scope | C | SCIARA family, `connor2012probabilistic` | Rules likely complete in full texts (round 2). |
| MOV-02 traffic | out of scope | A | `nagel1992cellular`, `biham1992selforganization` | **Among the most reimplementable models found.** |
| EPI-01 spatial epidemic | out of scope | B | `white2007modeling`, `davidson2024methodological` | Clean rule exists. |
| EPI-02 ASF | out of scope | B | `croft2020modelling`, `smith2002predicting` | No pure CA; literature is individual-based. |
| EPI-03 tick risk | out of scope | B | `li2012consequences` | A dynamic CA exists (contradicts "suitability mapping only" assumption). |
| ECO-02 succession | out of scope | B | `rademacher2004reconstructing` | — |
| ECO-06 predator–prey | out of scope | C | `pascual2002cluster` | Third-party code (caspr). |
| ECO-07 range shift | out of scope | B | `nobis2014kissmig`, `engler2012migclim` | — |
| ECO-08 vegetation patterns | out of scope | B | `thiery1995model`, `schneider2016spatially` | — |
| HAZ-04 windthrow | out of scope | B | `seidl2014simulating`, `rademacher2004reconstructing` | Individual-tree models; heavy. |
| HYD-06 snowmelt | out of scope | C | `pardoiguzquiza2017estimation`, `colladoslara2019distributed` | EU inputs; full text pending. |
| HYD-07 morphodynamics | out of scope | B | `skinner2023testing`, `coulthard2013integrating` | — |
| URB-01 heat island | out of scope | C/D | `kazak2018use` | Mostly CA–Markov land use + regression. |
| ATM-03 heavy gas | out of scope | — | none verified | — |
| ATM-04 drought, ECO-05 beaver, LND-02 abandonment, URB-04 infrastructure | out of scope | C or none | see domain files | — |

### Phenomena found in literature but missing from the longlist

| Phenomenon | Best | Template | Note |
|---|---|---|---|
| Coastal / lake-shore erosion | A | `palermo2024newts`, `ashton2001formation` | Lake shores (e.g. reservoirs) could be relevant for CZ — to be verified. |
| Groundwater flow | A | `ravazzani2011macroscopic` | Fits LND-03 (post-mining lake filling). |
| Population dispersal / colonisation | A | `bradshaw2021stochastic`, `gregoriodesouza2021reassessing` | Generic carrying-capacity CA; reusable for animals (ECO-04, ECO-07). |
| Snow / sand dunes | A | `sharma2019understanding`, `kochanski2019rescal` | 3D micro-scale; poor browser fit. |
| Oil slick spreading | C | `karafyllidis1997oil` | Water-surface CA. |
| Plant disease / pest spread | B | `white2017modelling`, `jones2021iteratively` | Close to ECO-03. |

## Reusable building blocks and methods

From `domains/general.md` and cross-domain observations:

- **Outflow distribution (minimisation of differences)** — `digregorio1999empirical`,
  `avolio2012theorem`: one kernel shared by water, debris flow, lava and (potentially) cold air.
- **Validation metrics** — `pontius2011death` (quantity / allocation disagreement),
  `pontius2011comparison` (multi-resolution), `pontius2007comparing` + `varga2019intensity`
  (figure of merit), `hagen2003fuzzy` / `hagenzanker2009improved` (fuzzy kappa for near-miss fronts).
- **Reference frameworks** (not scored) — Landlab / CellLab-CTS (`hobley2017creative`,
  `tucker2016celllab`), PCRaster (`karssenberg2010software`), OpenCAL (`derango2021opencal`).
- **Grid anisotropy correction for fronts** — `ghisu2015optimal`, `ghisu2015improved`,
  `pais2021cell2fire`; anisotropic cost-distance `wood2012anisotropic`.

## Observations relevant to the scope decision

These are observations, **not decisions** — the scope grouping in
`docs/review/evaluation-matrix.md` is still pending author approval.

1. **Both confirmed models are well supported** (several A-class references each, open
   code, benchmarks).
2. **Proposed core models ECO-01 and LND-01 are well supported** (A class, CZ or border-area
   studies).
3. **ATM-02 cold-air pooling has no CA literature.** It would be an original variant —
   attractive as a novelty, risky as a validated demo.
4. **Several "out of scope" items are among the most reimplementable** — traffic
   (NaSch, BML), SIR CA, tick CA, range-shift models. If reimplementability becomes a
   stronger criterion, the evaluation matrix should be revisited.
5. **New phenomena with A-class references** (coastal erosion, groundwater, population
   dispersal) are candidates for adding to the longlist.

## Quality control (round 1)

- **DOI verification:** every DOI in the bibliography was re-checked against Crossref by the
  coordinator after the agents finished (status, title similarity, year); see "Verification
  result" below.
- **Code links:** all 66 code repository URLs in the domain files were re-checked;
  all returned HTTP 200 except SourceForge (CAESAR-Lisflood), which blocks automated
  requests (HTTP 403) — existence plausible but not machine-verified.
- **Key consistency:** catalogue keys and BibTeX keys match 1:1 in every domain.
- **Harmonisation:** third-party-only code scored S3 = 1 everywhere (changed:
  `alexandridis2008cellular`, `freire2019using` A → B; `kubo1996forest`,
  `pascual2002cluster` B → C). `kochanski2019rescal` aligned to the full-text assessment
  (B 8) in both domains. Key collisions resolved (`karafyllidis1997oil`,
  `clarke1998loose`).
- **Limitations:** OpenAlex daily quota was exhausted early (shared IP), so most searching
  used Crossref + web search; most paywalled full texts could not be read automatically.

### Verification result

All **310 unique DOIs** resolved in Crossref (HTTP 200). For every entry the title in
`references.bib` matched the Crossref title (word-overlap similarity ≥ 0.6) and the year
differed by at most one (online vs. print date). No problems found. Checked 2026-10-12.

## Round 2 — suggested tasks

1. Manual full-text reading of provisional entries with high potential (WCA2D, CEM,
   SCIARA / lava, Ghisu anisotropy correction, snow-cover CA, fuzzy kappa, figure of merit).
2. Re-run thin searches once OpenAlex is available: treeline / range shift, windthrow CA,
   seed dispersal, heavy gas, cold-air drainage, CZ-specific studies (e.g. traffic CA
   at ZČU — unverified lead in `movement.md`).
3. Obtain non-Crossref references: EA flood benchmark report, Clarke 1994 (SLEUTH), Toprakli 2024.
4. Revisit the evaluation matrix with reimplementability as input and decide on scope.
5. For each selected model, pick one primary reference and extract the exact rule and
   parameters into the model card.
