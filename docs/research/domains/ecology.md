# Ecology and forestry — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.

## Search log

Date of all searches: 2026-10-12. The OpenAlex free daily budget for our shared IP address ran out after the first eight queries (HTTP 429, "Insufficient budget"). After that, discovery used Crossref bibliographic search, targeted web search and Europe PMC. **Every listed publication was verified against Crossref `/works/<DOI>` metadata.** Title, authors, year, venue, volume and pages in the entries and in `eco.bib` all come from that metadata. Where Crossref has both an online-first and a print date, the print year is used.

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automata bark beetle | OpenAlex | 157 | mostly remote-sensing detection papers; Seidl & Rammer 2016 iLand |
| cellular automaton bark beetle outbreak spread model | OpenAlex | 39 | Möykkynen & Pukkala 2014, Bone thesis |
| cellular automata insect outbreak forest defoliator | OpenAlex | 40 | Nenzén 2017 (not assessed), reviews |
| Bone Dragicevic cellular automata forest insect infestation | OpenAlex | 46 | Anderson & Dragićević 2016, Harati et al. 2020 |
| Fahse Heurich bark beetle outbreak simulation stand level | OpenAlex | 97 | Seidl 2015, Sommerfeld 2020, Mezei 2017 |
| spatially explicit bark beetle Ips typographus model grid | OpenAlex | 121 | Pietzsch 2022, WINDROT, ORCHIDEE, Hallas 2026 review |
| mountain pine beetle cellular automata | OpenAlex | 162 | Bone et al. 2006 (Ecol. Model.), Liu & Estep 2025 |
| cellular automata forest pest spread pine wilt | OpenAlex | 31 | pine-wilt CA (left to the `epi` domain) |
| cellular automaton forest succession / gap dynamics | OpenAlex | — | HTTP 429, quota exhausted |
| cellular automaton forest succession model | Crossref | 4.0 M (relevance-ranked) | too noisy; switched to targeted title queries |
| ~45 targeted title/author queries (Kéfi, Thiéry, Balzter, BEFORE, LANDIS, MigClim, KISSMig, RangeShifter, Nehrbass, Wadsworth, Pitt, Prasad, Kubo, Pascual, Kramer-Schadt, McRae, Potterf, Kautz, Doležal, Berec, Moenickes, …) | Crossref | top-2 checked | every hit confirmed by DOI lookup |
| cellular automata windthrow / treeline / seed dispersal / predator prey / habitat connectivity | Crossref | — | no specific geographic-CA hits; covered via packages and models instead |
| full text by DOI | Europe PMC REST | 3 PMC hits | Liu & Estep 2025, Seidl & Rammer 2016, Pascual et al. 2002 (metadata only) |
| bark beetle simulation; cellular automata invasive species; cellular automata vegetation pattern | GitHub search API | 3 / 2 / 0 | only student projects; not catalogued |
| abstract and OA-copy lookups (Prasad, Fahse, Potterf, Thiéry, Bone, Kautz, Kéfi, LANDIS-II, Seidl 2014, Nehrbass) | web search | — | used only to find OA copies and abstracts |

Full-text access: Springer OA pages and Europe PMC worked. MDPI, Wiley and ScienceDirect returned HTTP 403 to automated fetches, so those papers were assessed from abstracts unless another OA copy was found.

### Round 2

Date: 2026-10-12. OpenAlex was still quota-blocked, so discovery used Crossref `query.bibliographic`, web search, Semantic Scholar (`openAccessPdf`) and Europe PMC. Every new item was verified by Crossref `/works/<DOI>`. PDFs were fetched only into the agent scratchpad, converted to text and deleted.

| Query | Source | Hits | Notes |
|---|---|---|---|
| OA status for 16 round-2 targets | Semantic Scholar API | 16 | OA PDFs: Schneider & Kéfi 2016 (Springer), Pietzsch 2023 (Springer); Wiley "pdfdirect" links (Nobis, Engler 2012, Dullinger) returned HTML (blocked); Fahse 2011, Bone 2006 closed |
| Kéfi 2007 TPB / Nature full text | WUR repository, Europe PMC | 0 | repository record without file; read the rule via Schneider & Kéfi 2016 instead |
| Bone 2005 MSc thesis (basis of `bone2006fuzzy`) | SFU Summit | 1 PDF | full text read (Chapter 3 = CA model) |
| MigClim user guide; KISSMig C++ source | GitHub CRAN mirrors | 2 | `inst/doc/MigClim_userGuide.pdf` (full algorithm); `src/kissmig_c.cpp` |
| IPS-UPS repository code (neighbour rule) | GitHub | 1 | `Upscaling.R` neighbour rule = 8-neighbourhood |
| cellular automaton treeline dynamics alpine | Crossref | noisy | Zeng & Malanson 2006, Dullinger et al. 2004 |
| cellular automata windthrow forest storm damage spread | Crossref + web | 0 relevant | only fire CA; **no windthrow CA found** |
| cellular automata seed dispersal forest regeneration landscape | Crossref | 0 relevant | covered by TreeMig (`lischke2006treemig`) and treeline models |
| cellular automata Ips typographus Bohemian Forest; Šumava bark beetle spatial model (Hlásny, Jakuš, Modlinger) | Crossref + web | 3 | TANABBO (Duračiová et al. 2020, ČZU co-authors, Bohemian Forest validation); TANABBO II 2024 (not assessed); ŠUMLAND project page (no publication found) |
| Kautz IPS model; Pietzsch IPS-SPREADS | Crossref + web + Europe PMC | 2 | Kautz 2014, Kautz 2016 (OA, PMC4832482); IPS-SPREADS paper not found in Crossref |
| ash dieback / Hymenoscyphus spread model Europe | web + Crossref | 3 | Fritsch et al. 2026 (arXiv full text), Grosdidier et al. 2018 (kernel source); Leeds thesis (grey, not catalogued) |
| pine processionary moth spread model | Crossref | 2 | Robinet et al. 2014 (abstract elided; lead only) |
| cellular automaton invasive plant / knotweed spread Czech | web | 0 relevant | Dunn & Majer 2007 hierarchical patch CA (concept); no Czech CA |
| beaver dam cellular automata wetland; beaver population expansion model | Crossref + web | 4 | no CA of beaver wetlands; beaver colonisation models listed in `epidemics.md` (EPI-04) |
| locust / pollen / bird-stopover CA | web | 0 relevant | nothing verifiable |

## Model families

1. **Contagious insect-outbreak CA and grid models.** Each cell holds a susceptibility value or a beetle density. Infestation spreads to neighbours or along a dispersal kernel, and is often weighted by host share, stress or windthrow.
   - Classic GIS-CA: `bone2006fuzzy`, `anderson2016geosimulation`, `harati2020integrating`, `prasad2010modeling`, `moykkynen2014modelling`.
   - Stochastic multiscale CA with open code: `liu2025multiscale`.
   - Central European Ips typographus models:
     - Individual-tree / agent-based: `fahse2011simulation`, `potterf2017simulating`, `seidl2017climate`.
     - Grid Markov metamodel with neighbour spread and open code: `pietzsch2023nonparametric`.
   - Empirical parameter sources (dispersal distances, phenology): `kautz2011quantifying`, `potterf2019landscape`, `dolezal2016fine`, `berec2013population`.
   - Review: `hallas2026assessing`.
2. **Forest dynamics, gaps, succession and windthrow.**
   - Minimal two-state gap CA: `kubo1996forest`.
   - Rule-based beech mosaic-cycle model with a full ODD: `rademacher2004reconstructing`.
   - Raster forest-landscape models (LANDIS, LANDIS-II): `he1999spatially`, `scheller2007design`.
   - Individual-tree landscape model iLand, with wind and beetle modules: `seidl2014simulating`, `seidl2017climate`, `rammer2024individual`.
3. **Self-organised vegetation patterns (drylands, facilitation, grazing).**
   - Banded vegetation CA with a slope-asymmetric kernel: `thiery1995model`.
   - Kéfi facilitation CA (three states: vegetated / empty / degraded), patch-size power laws as early warnings: `kefi2007local`, `kefi2007spatial`.
   - Its spatial-grazing extension with open code: `schneider2016spatially`.
   - Analysis toolbox: `genin2018monitoring`.
   - Markov-chain CA (STMC): `balzter1998cellular`.
4. **Invasive species spread.** Local kernel plus corridor plus random long-distance dispersal on fine grids:
   - Giant hogweed, Czech and German sites: `nehrbass2007simulation`, `moenickes2013shapes`.
   - Riparian weeds: `wadsworth2000simulating`.
   - Human-assisted spread in GIS (MDiG): `pitt2009predicting`.
   - Insect invaders: `prasad2010modeling`, `moykkynen2014modelling`.
5. **Dispersal-limited range shifts under climate change.** A CA on top of SDM suitability maps:
   - MigClim: `engler2009migclim`, `engler2012migclim`.
   - KISSMig: `nobis2014kissmig`.
   - Individual-based platform: `bocedi2021rangeshifter`.
6. **Spatial predator–prey and antagonistic CA:** `pascual2002cluster`. Theoretical background: `durrett1994importance`.
7. **Habitat connectivity and animal dispersal on grids.**
   - Individual-based lynx dispersal on a habitat raster (Germany, CZ border): `kramerschadt2004fragmented`.
   - Circuit-theory connectivity on resistance grids (context, not CA): `mcrae2008using`.

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| liu2025multiscale | 2025 | Multiscale stochastic CA for mountain pine beetle | insect outbreak dispersion | hex grid / 6-neighbour + interaction neighbourhoods / density [0,1] / stoch. | 2 2 2 2 1 | 9 | A | GitHub | OA | full text |
| pietzsch2023nonparametric | 2023 | IBM → Markov-chain metamodel, Ips typographus | bark beetle spread (Saxon Switzerland NP, DE/CZ border) | 250 m grid / Moore neighbour spread / feature-combination states / stoch. Markov | 2 2 2 2 2 | 10 | A | GitHub | OA | full text + code (r2) |
| seidl2017climate | 2017 | Wind × bark beetle interactions in iLand | windthrow + beetle (Kalkalpen, AT) | 10 m cells, individual trees / 8-neighbour search + kernel / stoch. | 1 1 2 1 2 | 7 | B | iLand GitHub | OA | full text |
| seidl2014simulating | 2014 | Wind disturbance at tree level (iLand) | windthrow (Sweden) | individual trees on grid / upwind gaps / stoch. iterative storm | 1 1 2 1 2 | 7 | B | iLand GitHub | paywall | abstract (provisional) |
| kubo1996forest | 1996 | Forest gap expansion CA | canopy gap dynamics | square lattice / neighbour-gap-dependent death / 2 states / stoch. | 1 1 1 2 1 | 6 | C | caspr (3rd party) | paywall | code documentation (provisional) |
| rademacher2004reconstructing | 2004 | BEFORE beech forest model | beech mosaic cycle, storms (Central Europe) | 14.29 m cells, 54×54 / wind-ordered neighbour light & windfall / 4 height compartments / stoch. | 2 2 0 2 1 | 7 | B | not found | paywall (ODD OA) | third-party ODD (full) |
| thiery1995model | 1995 | Banded vegetation genesis CA | tiger bush, Niger | square grid / 9×3 slope-asymmetric kernel / binary / det. | 1 2 0 2 2 | 7 | B | not found | OA copy (IRD) | full text |
| schneider2016spatially | 2016 | Spatially heterogeneous grazing pressure | dryland degradation | 100×100 torus / von Neumann facilitation + associational resistance / 3 states / stoch., synchronous | 2 2 2 2 1 | 9 | A | GitHub (authors) + caspr | OA (CC BY) | full text (r2) |
| moenickes2013shapes | 2013 | Giant hogweed matrix model + CA | plant invasion (8 DE sites) | 5 m cells, 200×200 / exponential local kernel + corridors + random LDD / stage densities / stoch. | 2 2 0 1 2 | 7 | B | not found | OA author copy | full text |
| engler2012migclim | 2012 | MIGCLIM R package | dispersal-limited range shift | SDM raster / kernel + LDD + barriers / occupied-or-not / stoch. | 2 1 2 2 1 | 8 | B | CRAN archive / GitHub mirror | paywall | package user guide (full algorithm) (r2) |
| nobis2014kissmig | 2014 | KISSMig | range dynamics, migration lag | suitability raster / 3×3 spread / binary or quantitative / det. or stoch. | 2 1 2 2 1 | 8 | B | CRAN | OA | abstract + source code (r2) |
| bocedi2021rangeshifter | 2021 | RangeShifter 2.0 | range expansion, connectivity | habitat raster / IBM dispersal (kernel or SMS) / individuals / stoch. | 1 1 2 2 1 | 7 | B | GitHub | OA | abstract (provisional) |
| pascual2002cluster | 2002 | Cluster size distributions (predator–prey CA) | predator–prey, disturbance–recovery | lattice / 4-neighbour / 3 states / stoch. | 1 1 1 2 1 | 6 | C | caspr (3rd party) | OA (PMC) | abstract + code docs (provisional) |
| scheller2007design | 2007 | LANDIS-II | forest succession + disturbance | raster cells with species-age cohorts / seed dispersal & disturbance spread / stoch. | 1 1 2 1 1 | 6 | C | GitHub | paywall | abstract (provisional) |
| kefi2007local | 2007 | Local facilitation, bistability (TPB) | dryland vegetation | lattice / 4-neighbour facilitation / 3 states / stoch. | 2 1 1 2 1 | 7 | B | derived variant in caspr | paywall | rule + base parameters restated in schneider2016spatially full text (r2) |
| kefi2007spatial | 2007 | Patterns and imminent desertification (Nature) | dryland degradation (ES, GR, MA) | as kefi2007local + grazing / stoch. | 1 1 1 1 2 | 6 | C | derived variant in caspr | paywall | abstract (provisional) |
| pitt2009predicting | 2009 | Argentine ant spread (MDiG) | invasive insect, NZ | GIS raster / local + human-assisted LDD / occupancy / stoch. | 1 1 2 1 1 | 6 | C | MDiG GitHub | paywall | abstract (provisional) |
| engler2009migclim | 2009 | MigClim | plant dispersal under climate change (W Swiss Alps) | SDM raster / kernel + LDD / binary / stoch. | 1 1 2 1 1 | 6 | C | CRAN archive | paywall | abstract (provisional) |
| potterf2017simulating | 2017 | Beetle population response to windthrow | Ips typographus after windthrow | NetLogo ABM on spatial grid / stoch. | 1 1 1 1 1 | 5 | C | publisher supplement (zip) | paywall | abstract (provisional) |
| harati2020integrating | 2020 | Neighbourhood effect + ML for MPB | MPB outbreak (BC, CA) | raster / weighted neighbourhood + GLM/RF transition / binary / prob. | 1 1 0 1 2 | 5 | C | not found | OA | abstract (provisional) |
| nehrbass2007simulation | 2007 | Hogweed IBM, long-distance dispersal | plant invasion (Slavkovský les, CZ) | 5 m cells, 140×140 / Moore + random LDD / individuals / stoch. | 1 1 0 1 2 | 5 | C | not found | OA archive copy | full text |
| he1999spatially | 1999 | LANDIS fire and succession | forest landscape fire + succession | raster / seed dispersal + fire spread / cohorts / stoch. | 1 1 1 1 1 | 5 | C | successor open (LANDIS-II) | paywall | metadata + secondary (provisional) |
| bone2006fuzzy | 2006 | Fuzzy-constrained CA of insect infestation | MPB (central BC) | 1 m raster / 500×500 dispersal + 25×25 attack windows, threshold function of fuzzy susceptibility / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall (thesis OA) | underlying thesis, full text (r2) |
| fahse2011simulation | 2011 | SAMBIA stand-level outbreak model | Ips typographus (Bavarian Forest NP) | spatially explicit agent-based, trees + beetles / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional; r2: no OA copy found) |
| anderson2016geosimulation | 2016 | Geosimulation of EAB, data-scarce | emerald ash borer, hypothetical landscapes | GIS-MCE-CA / neighbourhood / stoch. | 1 1 0 1 1 | 4 | C | not found | OA | abstract (provisional) |
| moykkynen2014modelling | 2014 | Siberian moth spread in Europe | invasive defoliator (EU) | 1 km grid / exp. flight kernel + transport / host-tree counts / stoch. | 1 1 0 1 1 | 4 | C | not found | OA | full text |
| prasad2010modeling | 2010 | EAB risk of spread, cellular model (SHIFT) | emerald ash borer (Ohio) | cells / insect flight + gravity-model human transport / risk / stoch. | 1 1 0 1 1 | 4 | C | not found | OA copy (USFS) | abstract + outline (provisional) |
| balzter1998cellular | 1998 | CA models for vegetation dynamics (STMC) | lawn species dynamics | lattice / spatio-temporal Markov chain / species / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall (figshare copy listed) | abstract (provisional) |
| wadsworth2000simulating | 2000 | Riparian weed spread and control (MIGRATE) | Impatiens, Heracleum (Co. Durham, UK) | GIS grid / multiple dispersal mechanisms / demographic / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| kramerschadt2004fragmented | 2004 | Lynx dispersal and road mortality | habitat connectivity (DE, CZ border) | habitat raster / IBM step rules / individuals / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| duraciova2020bark | 2020 | TANABBO spot initiation / spreading predictor (r2) | Ips typographus, Bohemian Forest (CZ) | 30 m raster / cost distance to last year's spots (max 228 m) + logistic regression / susceptibility [0,1] / one-step, iterable | 1 2 0 1 2 | 6 | C | not found | OA (CC BY-NC) | full text |
| kautz2016dispersal | 2016 | IPS individual-based beetle dispersal (r2) | Ips typographus dispersal, virtual stand | tree positions / perceptual range 15 m, neighbour-tree moves / beetles + tree states / stoch. | 2 2 1 2 1 | 8 | B | supplement (ODD + model version) | OA (PMC) | full text (keyword-guided) |
| kautz2014individual | 2014 | IPS model, individual traits (r2) | Ips typographus dispersal and infestation | IBM on virtual stand / stoch. | 1 1 1 2 1 | 6 | C | via kautz2016 supplement | paywall | secondary (abstract via search) (provisional) |
| dullinger2004modelling | 2004 | Treeline shift of Pinus mugo (r2) | treeline advance (N. Calcareous Alps, AT) | landscape grid / dispersal kernel + invasibility of resident vegetation / stoch. | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| zeng2006endogenous | 2006 | Alpine treeline CA, fractal dynamics (r2) | treeline ecotone advance | lattice / local positive + negative feedbacks / tree–tundra / stoch. | 1 1 0 2 1 | 5 | C | not found | paywall | abstract (provisional) |
| lischke2006treemig | 2006 | TreeMig forest-landscape model (r2) | forest dynamics + species migration | 25 m–1 km grid / seed dispersal between cells / height-class densities per species / stoch. or det. | 1 1 0 1 1 | 4 | C | not verified (docs open) | paywall | secondary (project docs) (provisional) |
| fritsch2026mechanistic | 2026 | Ash dieback expansion, France (r2) | Hymenoscyphus fraxineus spread | 16×16 km quadrats / reaction–diffusion (discretised) + climate + host / leaf and rachis infection / det. + statistical obs. | 2 1 0 1 2 | 6 | C | not found | preprint (arXiv) | full text (preprint, keyword-guided) |
| dunn2007simulating | 2007 | Hierarchical patch-based weed CA (r2) | weed propagation, SW Western Australia (fictitious data) | irregular hierarchical patches / probabilistic network links / occupancy / stoch. | 1 0 0 1 0 | 2 | D | not found | OA (publisher) | full text |
| grosdidier2018tracking | 2018 | Ash dieback spore dispersal kernels (r2) | parameter source: H. fraxineus dispersal (France) | empirical | n/a | n/a | n/a | — | paywall | abstract via search |
| hallas2026assessing | 2026 | Review: Ips typographus risk models | bark beetle models | review | n/a | n/a | n/a | — | OA | full text (searched) |
| rammer2024individual | 2024 | iLand overview | forest landscape model | framework | n/a | n/a | n/a | iLand GitHub | OA | metadata |
| genin2018monitoring | 2018 | spatialwarnings R package | spatial early-warning indicators | analysis toolbox | n/a | n/a | n/a | GitHub / CRAN | paywall | abstract |
| durrett1994importance | 1994 | The importance of being discrete (and spatial) | theory: IPS vs. PDE vs. mean field | review/theory | n/a | n/a | n/a | — | OA (publisher) | abstract |
| mcrae2008using | 2008 | Circuit theory for connectivity | connectivity on resistance grids | method (not CA) | n/a | n/a | n/a | Circuitscape GitHub | paywall | metadata |
| kautz2011quantifying | 2011 | Dispersion of beetle infestations (Bavarian Forest) | parameter source: infestation distances | empirical | n/a | n/a | n/a | — | paywall | secondary |
| potterf2019landscape | 2019 | Beetle spread from windthrow, Tatra NP | parameter source: distances, spot sizes | empirical | n/a | n/a | n/a | — | paywall | abstract |
| dolezal2016fine | 2016 | Powder marking of Ips typographus dispersal | parameter source: dispersal function (Šumava, CZ) | empirical | n/a | n/a | n/a | — | OA | secondary (via review) |
| berec2013population | 2013 | PHENIPS validation, Bohemian Forest | parameter source: phenology / generations (CZ) | empirical / phenology | n/a | n/a | n/a | — | paywall | title + review context |

## Entries

### liu2025multiscale — A multiscale stochastic cellular automata model for dispersion of mountain pine beetles
- **Citation:** Liu, Y., Estep, D. (2025). A multiscale stochastic cellular automata model for dispersion of mountain pine beetles. *Royal Society Open Science* 12(6), 241934. DOI: 10.1098/rsos.241934 (verified: Crossref, OpenAlex)
- **Access:** OA (CC BY), PMC12174937
- **Phenomenon and study area:** Regional dispersion of mountain pine beetle. Mostly synthetic 30×30 and 50×50 domains, plus a calibration on an aerial-survey map from the Crown of the Continent Ecosystem, 2001–2007.
- **Model:**
  - **Cells, states, neighbourhood:** Hexagonal cells hold normalised population density in [0,1]. Each cell has six neighbours. Affected cells and their surroundings form "interaction neighbourhoods" that update independently.
  - **Transition rule:** A Bernoulli draw decides whether a cell takes part in dispersion. Its probability grows with the local density gradient and with the number of affected neighbours. Above-mean cells give a fraction γ1 of their excess to the other included cells. A fraction γ2 settles successfully, subject to a survival probability with parameters φ and ρ. Failing receiver cells are zeroed.
  - **Boundaries and microscale:** Boundaries are absorbing, using auxiliary cells. A microscale stochastic birth–death chain, with carrying capacity C and N sub-steps, runs within each macro step.
- **Inputs:** Synthetic grids. The real case is a rasterised severity bitmap.
- **Parameters:** Defined in Table 1. Settings are in Table 2 (e.g. γ1 = γ2 = 0.8, φ = ρ = 1/3, C = 100, N = 100, b = 1, d = 0.2). Bayesian calibration priors and settings are in Table 3.
- **Code:** https://github.com/Irene-liu-724/MPB-Infestation (verified; redirects to https://github.com/liu-yanjun-dev/MPB-Infestation). The paper states a Zenodo archive.
- **Validation:** Numerical behaviour studies with fitted trends of pattern complexity (R² ≈ 0.97–0.99), statistical tests on dispersion rates, and Bayesian calibration on synthetic and real data. There is no independent map validation.
- **Reimplementability:**
  - S1 2: equations for every macroscale step plus boundary handling.
  - S2 2: parameter tables.
  - S3 2: open code.
  - S4 2: runs on generic synthetic grids.
  - S5 1: mostly pattern statistics, no benchmark map comparison.
  - → 9, A. Assessed from: full text (read through Section 3 and data statement).
- **Browser fit:** Very good. Small hex grids and cheap updates. The microscale chain can be replaced by a logistic step.
- **Relevance to ca-geo:** ECO-01 (bark-beetle outbreak) core dispersal template. A hex-grid option is worth considering.
- **Round 2:** Confirmed as assessed in round 1 (full text, open code). Unchanged (A 9); S5 remains 1 because there is no map-level benchmark.

### pietzsch2023nonparametric — Nonparametric upscaling of bark beetle infestations and management from plot to landscape level
- **Citation:** Pietzsch, B. W., Wudel, C., Berger, U. (2023). Nonparametric upscaling of bark beetle infestations and management from plot to landscape level by combining individual-based with Markov chain models. *European Journal of Forest Research* 142(1), 129–144. DOI: 10.1007/s10342-022-01512-1 (verified: Crossref, OpenAlex)
- **Access:** OA (Springer)
- **Phenomenon and study area:** Ips typographus outbreak 2015–2018 in Saxon Switzerland National Park, Germany. The park borders Czech Bohemian Switzerland.
- **Model:**
  - **Fine scale:** An individual-based model (IPS-SPREADS, 5×5 m patches) is run on 7,524 cells of 250×250 m covering about 14,100 ha of forest.
  - **States:** Each cell is described by a feature combination: mean attractiveness, spruce share and number of infested trees.
  - **Transitions:** Transition probabilities between feature combinations come from IBM replicates. They drive a yearly Markov-chain metamodel (after Cipriotti et al. 2016).
  - **Extensions:** One adds beetle spread to neighbouring cells, another adds spruce dieback. Sanitation-felling scenarios are applied in a buffer zone.
- **Inputs:** Forest stand polygons (Saxon state forest enterprise) and infestation maps for 2015–2017.
- **Parameters:** Transition tables derived from simulations, openly provided in the repository.
- **Code:** https://github.com/bwpietzsch/IPS-UPS (verified 200). It holds the IBM, the metamodel and the data tables.
- **Neighbour rule (round 2):** A cell with spruce whose 8-neighbourhood (checked in `Upscaling.R`) contains at least one cell at the highest infestation level raises its own infestation level by one step per beetle generation (2 or 3 per year by climate scenario), applied simultaneously to all cells before the Markov step. Sanitation felling (0–100 % in 10 % steps) removes infested trees.
- **Validation:** Against observed infestations in 2017 and 2018, per cell, with the macro-averaged F1 score for four metamodel variants (without/with neighbour spread and spruce dieback) across climate × felling scenarios. Neighbour spread raised agreement substantially; dieback only marginally; 2017 fitted better than 2018. Prediction tables per variant are in the repository (`Kappa/`).
- **Reimplementability:**
  - S1 2: complete flowchart, Markov step and neighbour rule (round 2).
  - S2 2: transition tables in the repository.
  - S3 2.
  - S4 2: derived cell tables open.
  - S5 2: per-cell F1 scores against observed 2017/2018 infestations, with prediction outputs in the repository.
  - → 10, A. Round 2: re-assessed from full text + code — S 2 2 2 2 2 (was 1 2 2 2 1, B 8).
- **Browser fit:** Excellent. It is a lookup-table Markov CA on a coarse grid.
- **Relevance to ca-geo:** ECO-01 with direct CZ border relevance. The train-a-CA-from-a-detailed-model pattern could also be reused for HAZ-04 (windthrow) to ECO-01 chains (L3).

### seidl2017climate — Climate change amplifies the interactions between wind and bark beetle disturbances in forest landscapes
- **Citation:** Seidl, R., Rammer, W. (2017). Climate change amplifies the interactions between wind and bark beetle disturbances in forest landscapes. *Landscape Ecology* 32(7), 1485–1498. DOI: 10.1007/s10980-016-0396-4 (verified: Crossref, OpenAlex). Online 2016.
- **Access:** OA (CC BY), PMC5494037
- **Phenomenon and study area:** Wind and Ips typographus interactions in Kalkalpen National Park, Austria (20,856 ha; beetle analysis on the 9,336 ha core zone), 2007–2014.
- **Model:** The iLand bark beetle module works on 10 m cells.
  - **Hosts:** Spruce with dbh ≥ 15 cm.
  - **Infestation sources:** A background infestation probability, or windthrown trees, which are colonised with probability 0.3.
  - **Dispersal:** Beetle cohorts disperse by a symmetric kernel and then search the 8-neighbourhood, preferring windthrown hosts.
  - **Tree defence and population:** Colonisation thresholds depend on tree carbohydrate reserves. Development is phenology-driven, followed by overwinter mortality, with antagonists represented phenomenologically.
  - **Wind:** The wind module is individual-tree and iterative within storms (see `seidl2014simulating`).
- **Inputs:** Vegetation from remote sensing and inventory, climate, and 30 m Landsat-based disturbance maps (Hansen) for evaluation.
- **Parameters:** In online appendices. Only the beetle reproduction rate was calibrated.
- **Code:** iLand is open source at https://github.com/edfm-tum/iland-model (verified 200), with documentation at https://iland-model.org (verified 200).
- **Validation:**
  - Wind: 182 ha simulated vs. 169 ha observed.
  - Beetle: 353 ha simulated vs. 361 ha observed.
  - Patch-size distribution is too fine (95.5 % vs. 81.3 % of patches < 1 ha).
- **Reimplementability:**
  - S1 1: core logic described; details in appendices.
  - S2 1.
  - S3 2.
  - S4 1.
  - S5 2: area and patch metrics.
  - → 7, B. Assessed from: full text.
- **Browser fit:** The full iLand model is too heavy. The beetle-cell rule set (kernel, 8-neighbour search, windthrow preference, colonisation threshold) can be transplanted into a 10–30 m CA.
- **Relevance to ca-geo:** ECO-01, HAZ-04, and chains L2/L3. Its reference numbers are good targets for an Austrian or Šumava-like demo.

### seidl2014simulating — Simulating wind disturbance impacts on forest landscapes: tree-level heterogeneity matters
- **Citation:** Seidl, R., Rammer, W., Blennow, K. (2014). *Environmental Modelling & Software* 51, 1–11. DOI: 10.1016/j.envsoft.2013.09.018 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Storm Gudrun (2005), a 1,391 ha landscape in south-central Sweden.
- **Model:** An individual-tree wind module in iLand. Storms are iterated so that new edges created during an event raise exposure. It accounts for upwind gap size and neighbour shelter, with separate critical wind speeds for uprooting and breakage.
- **Inputs:** Tree-level forest structure, wind speed and direction, soil frost.
- **Parameters:** Not seen; assumed in paper and appendix.
- **Code:** iLand GitHub (verified).
- **Validation:** Against satellite-derived Gudrun damage. Ignoring within-stand heterogeneity under-estimated damage.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 2.
  - S4 1.
  - S5 2: observed damage benchmark.
  - → 7, B. Assessed from: abstract (provisional).
- **Browser fit:** A simplified edge-exposure CA (a gap in the upwind cell raises risk) is feasible.
- **Relevance to ca-geo:** HAZ-04 windthrow. It is the main verified source for "new edges → more damage" rules.

### kubo1996forest — Forest Spatial Dynamics with Gap Expansion: Total Gap Area and Gap Size Distribution
- **Citation:** Kubo, T., Iwasa, Y., Furumoto, N. (1996). *Journal of Theoretical Biology* 180(3), 229–246. DOI: 10.1006/jtbi.1996.0099 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Canopy gap creation and expansion after wind disturbance; theoretical.
- **Model:** A two-state lattice (vegetated / gap). Gaps regrow with rate α. Trees die at an intrinsic rate d plus a rate δ that grows with the number of neighbouring gaps (gap expansion). The model is stochastic.
- **Inputs:** None (abstract lattice).
- **Parameters:** Three (α, δ, d). Values not checked in the paper.
- **Code:** Third-party implementation as model `forestgap` in caspr, https://github.com/fdschneider/caspr (verified 200, MIT licence; Kéfi/Guttal groups).
- **Validation:** Analytical approximations of gap area and size distribution (from title and caspr references).
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 1 (third-party code only, harmonised rule).
  - S4 2.
  - S5 1.
  - → 6, C. Assessed from: caspr documentation (provisional).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-02 and HAZ-04 as a minimal teaching CA. It can be coupled with a real forest mask.

### rademacher2004reconstructing — Reconstructing spatiotemporal dynamics of Central European natural beech forests: the rule-based forest model BEFORE
- **Citation:** Rademacher, C., Neuert, C., Grundmann, V., Wissel, C., Grimm, V. (2004). *Forest Ecology and Management* 194(1–3), 349–368. DOI: 10.1016/j.foreco.2004.02.022 (verified: Crossref)
- **Access:** paywall. A full ODD description is openly available as textbook supplement material (Railsback & Grimm): https://ees4760.jgilligan.org/files/models/chapter_18/ch18_before_ODD.pdf (verified 200).
- **Phenomenon and study area:** The natural beech mosaic cycle (patches of developmental stages and their cyclic succession) in Central Europe.
- **Model:**
  - **Grid:** 14.29 m cells (one large beech; 7×7 cells = 1 ha), 54×54 cells (about 60 ha).
  - **States:** Each cell has four vertical compartments (upper canopy, lower canopy, juveniles, seedlings), with crown cover in eighths. Individual trees are tracked in the two canopy layers.
  - **Time step and schedule:** 15 years, with nine scheduled processes. The last two are neighbourhood interactions: oblique light and windfall. Cells are processed in an order set by the main wind direction.
- **Inputs:** None (generic forest).
- **Parameters:** Given in the ODD (rule probabilities and thresholds).
- **Code:** Not found as an open repository. The CoMSES record lists no code.
- **Validation:** Pattern-oriented (mosaic and cycle patterns); qualitative to semi-quantitative.
- **Reimplementability:**
  - S1 2.
  - S2 2.
  - S3 0.
  - S4 2.
  - S5 1.
  - → 7, B. Assessed from: third-party ODD (full).
- **Browser fit:** Good. It is small, and the 15-year step allows multi-century runs.
- **Relevance to ca-geo:** ECO-02 (forest succession) and HAZ-04 (storm gaps). Central European and pattern-oriented. The wind-ordered sweep is a useful update-scheme example.

### thiery1995model — A Model Simulating the Genesis of Banded Vegetation Patterns in Niger
- **Citation:** Thiery, J. M., D'Herbes, J.-M., Valentin, C. (1995). *The Journal of Ecology* 83(3), 497. DOI: 10.2307/2261602 (verified: Crossref)
- **Access:** OA copy at IRD: https://horizon.documentation.ird.fr/exl-doc/pleins_textes/pleins_textes_6/b_fdi_39-40/43183.pdf (verified 200)
- **Phenomenon and study area:** "Brousse tigrée" banded vegetation, SW Niger.
- **Model:** A Life-like binary CA. A 9×3 interaction matrix gives negative weight to up-slope plants (competition for run-off, coefficient a) and positive weight to lateral and down-slope plants (synergy, coefficient b). The same initial random tree map is iterated.
- **Inputs:** A random initial density. Slope direction is implicit in the kernel orientation.
- **Parameters:** A grid of 3 a-values × 2 b-values plus the number of iterations. Results do not depend on initial density.
- **Code:** Not found.
- **Validation:** Field transect and maps. Table 1 gives quantitative band and group statistics (width, number, velocity) per scenario.
- **Reimplementability:**
  - S1 1: kernel structure clear; exact threshold function not extracted in this round.
  - S2 2.
  - S3 0.
  - S4 2.
  - S5 2.
  - → 7, B. Assessed from: full text (keyword-guided).
- **Browser fit:** Trivial. A kernel orientation taken from DEM aspect would make it geographic.
- **Relevance to ca-geo:** ECO-08 vegetation patterns. The DEM-oriented anisotropic kernel is a nice CZ/EU teaching variant.

### schneider2016spatially — Spatially heterogeneous pressure raises risk of catastrophic shifts
- **Citation:** Schneider, F. D., Kéfi, S. (2016). *Theoretical Ecology* 9(2), 207–217. DOI: 10.1007/s12080-015-0289-1 (verified: Crossref)
- **Access:** OA (CC BY, Springer)
- **Phenomenon and study area:** Dryland degradation under grazing; theoretical.
- **Model (round 2, full text):** An interacting-particle CA with three states (vegetated +, empty 0, degraded −) on a 100×100 grid with periodic boundaries; one step = 1 year; synchronous stochastic update (each cell's transition probabilities compared with one uniform draw). Transition probabilities use the global cover ρ+ and the local von Neumann cover q+|i:
  - regeneration − → 0: r + f·q+|−;
  - colonisation 0 → +: (δ·ρ+ + (1−δ)·q+|0)·(b − c·ρ+);
  - degradation 0 → −: d;
  - mortality + → 0: m0 + g0·(1 − q+|+) (associational resistance; the original Kéfi model has m0 only).
- **Inputs:** None (initial cover 0.8–0.9, half the rest degraded; or near-desert start for recovery runs).
- **Parameters:** All given: r = 0.01, f = 0.9, δ = 0.1, c = 0.2, d = 0.1 (inherited from Kéfi et al. 2007 TPB), m0 = 0.05, g0 between 0 and 0.5, b varied as environmental pressure.
- **Code:** Authors' R code https://github.com/cascade-wp6/2015_schneider_kefi (verified 200; Zenodo 10.5281/zenodo.35034 cited in the paper) and caspr `grazing` model https://github.com/fdschneider/caspr (verified).
- **Validation:** Steady state when mean cover changes by less than 10⁻⁶ between 200-year periods; outputs are cover, local cover, clustering coefficient, largest patch and patch-size distribution class along g0 and b gradients (figures only).
- **Reimplementability:**
  - S1 2: complete rule, neighbourhood, boundaries, update scheme.
  - S2 2: all values.
  - S3 2.
  - S4 2.
  - S5 1: results as bifurcation diagrams and figures; no tables.
  - → 9, A. Round 2: re-assessed from full text — S 2 2 2 2 1 (was 1 1 2 2 1, B 7).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-08. It is the cleanest open, parameterised dryland CA.

### moenickes2013shapes — What shapes giant hogweed invasion? Answers from a spatio-temporal model integrating multiscale monitoring data
- **Citation:** Moenickes, S., Thiele, J. (2013). *Biological Invasions* 15(1), 61–73. DOI: 10.1007/s10530-012-0268-z (verified: Crossref). Online 2012.
- **Access:** OA author manuscript: https://www.uni-muenster.de/imperia/md/content/landschaftsoekologie/oekologischeplanung/team/publikationenjan/what_shapes_giant_hogweed_invasion.pdf
- **Phenomenon and study area:** Heracleum mantegazzianum in eight 1×1 km landscapes in western and southern Germany, monitored 2002 and 2009.
- **Model:**
  - **Grid and states:** 200×200 cells of 5 m. Each cell holds four stage densities (small / medium / large vegetative, flowering).
  - **Time step and demography:** Yearly. A density-dependent stage matrix uses Weibull competition.
  - **Habitat:** Suitability declines linearly by succession over 30 years.
  - **Dispersal:** A fraction p_LD = 1 % of offspring goes to random long-distance cells. The rest disperses locally on a discretised exponential kernel. Offspring that reach a corridor cell move along the corridor's topology: 35 m on roads and rails, 100 m on rivers (rivers one-way), with shift probability p_shift. Management is applied as a probability p_man.
- **Inputs:** Land cover and linear elements mapped from aerial photos (5 m), and GPS monitoring.
- **Parameters:** Table 2 plus a supplement (matrix derivation, local kernel weights). Corridor parameters are rough estimates, covered by a sensitivity analysis.
- **Code:** Not found.
- **Validation:** Modelling efficiency 0.94 for occupied cells and 0.89 for newly colonised cells. Likelihood-ratio tests of nine alternative hypotheses.
- **Reimplementability:**
  - S1 2.
  - S2 2.
  - S3 0.
  - S4 1: field data not open, but runs on generic land cover + OSM-type corridors.
  - S5 2.
  - → 7, B. Assessed from: full text.
- **Browser fit:** Very good. 200×200 cells and 7 steps.
- **Round 2:** Searched for code (none found). Score unchanged; still the best ECO-03 rule description.
- **Relevance to ca-geo:** ECO-03 invasive spread. The best template for corridor plus long-distance spread. Hogweed is a relevant CZ invader, and corridors could come from DIBAVOD rivers and road data.

### engler2012migclim — The MIGCLIM R package – seamless integration of dispersal constraints into projections of species distribution models
- **Citation:** Engler, R., Hordijk, W., Guisan, A. (2012). *Ecography* 35(10), 872–878. DOI: 10.1111/j.1600-0587.2012.07608.x (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Dispersal-limited species range projection; generic.
- **Model:** A CA in which each cell is occupied or not. Colonisation depends on a dispersal kernel, long-distance dispersal, barriers, propagule production (age-dependent) and habitat invasibility taken from SDM suitability maps that change through time.
- **Inputs:** Any SDM suitability raster series, plus barrier layers.
- **Parameters:** User-supplied; flexible.
- **Code:** https://github.com/cran/MigClim (verified; CRAN mirror). The CRAN page https://cran.r-project.org/package=MigClim states the package was archived in 2020 because no maintainer fixed check issues.
- **Algorithm (round 2, from the package user guide `inst/doc/MigClim_userGuide.pdf`):** For each unoccupied suitable target cell, all occupied source cells within the kernel's maximum distance are collected (sources behind a barrier cell are ignored). The target is colonised with probability P_col = (1 − Π_i (1 − P_disp,i · P_prop,i)) · P_inv, where P_disp is a discrete distance kernel, P_prop a discrete function of time since the source was colonised, and P_inv the target's invasibility. Optional long-distance dispersal: from each source with probability lddFreq · P_prop, in a random direction and at a random distance within a range, ignoring barriers. Dispersal steps (usually years) are nested in environmental-change steps; cells that turn unsuitable are cleared after the dispersal stage. A test data set ships with the package.
- **Validation:** Not in the abstract; the guide contains a hands-on test simulation.
- **Reimplementability:**
  - S1 2: full rule in the open user guide.
  - S2 1: user-supplied; only the test-run values documented.
  - S3 2: source available, though archived.
  - S4 2.
  - S5 1: no published reference numbers checked.
  - → 8, B. Round 2: re-assessed from the package user guide — S 2 1 2 2 1 (was 1 1 2 2 1, B 7). Journal full text still blocked (Wiley).
- **Browser fit:** Good. Binary CA on SDM rasters.
- **Relevance to ca-geo:** ECO-07 range shift and ECO-03.

### engler2009migclim — MigClim: Predicting plant distribution and dispersal in a changing climate
- **Citation:** Engler, R., Guisan, A. (2009). *Diversity and Distributions* 15(4), 590–601. DOI: 10.1111/j.1472-4642.2009.00566.x (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Plant migration under climate change, western Swiss Alps.
- **Model:** The original MigClim, with dispersal distance, increasing reproductive potential with age, fragmentation and long-distance dispersal on top of SDM projections.
- **Inputs:** SDM outputs, land cover.
- **Parameters:** Species-specific; listed in the abstract only as types.
- **Code:** As engler2012migclim.
- **Validation:** Compares "suitable" vs. "colonisable" habitat.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 2.
  - S4 1.
  - S5 1.
  - → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** ECO-07. Alpine setting, analogous to Krkonoše and Šumava.

### nobis2014kissmig — KISSMig – a simple model for R to account for limited migration in analyses of species distributions
- **Citation:** Nobis, M. P., Normand, S. (2014). *Ecography* 37(12), 1282–1287. DOI: 10.1111/ecog.00930 (verified: Crossref)
- **Access:** OA (CC BY)
- **Phenomenon and study area:** Migration lag in species ranges; example Quercus cerris (Europe).
- **Model:** A deliberately simple raster CA. From origin cells, occupancy spreads into suitable neighbouring cells each step, deterministically or stochastically. Suitability may be binary or quantitative. The result is an accessibility map.
- **Inputs:** Suitability maps from SDMs.
- **Parameters:** Very few (steps, suitability, stochastic mode).
- **Code:** CRAN `kissmig` v2.0-1 https://cran.r-project.org/package=kissmig (verified; Rcpp + terra).
- **Validation:** Illustrative applications.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 2.
  - S4 2.
  - S5 1.
  - → 7, B. Assessed from: abstract + CRAN description (provisional; S1 is likely 2 once the full text is read).
- **Round 2:** The journal PDF was blocked (Wiley returned HTML), but the C++ core `src/kissmig_c.cpp` (https://github.com/cran/kissmig, verified) fully defines the rule: per iteration, occupied cells go extinct with probability `pe`; suitable cells are colonised from occupied cells in the 3×3 neighbourhood, with corner neighbours weighted by probability `pc`; the outermost raster ring is ignored; suitability layers are looped over time periods with `it` iterations each. S1 → 2. S2 stays 1 (application values in the paper not seen). → 8, B. Round 2: re-assessed from source code — S 2 1 2 2 1 (was 1 1 2 2 1, B 7).
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** ECO-07. The simplest credible range-shift CA for CZ (e.g. tree-line species).

### bocedi2021rangeshifter — RangeShifter 2.0
- **Citation:** Bocedi, G., Palmer, S. C. F., Malchow, A.-K., Zurell, D., et al. (2021). RangeShifter 2.0: an extended and enhanced platform for modelling spatial eco-evolutionary dynamics and species' responses to environmental changes. *Ecography* 44(10), 1453–1462. DOI: 10.1111/ecog.05687 (verified: Crossref)
- **Access:** OA (CC BY)
- **Phenomenon and study area:** Range expansion, connectivity and evolution of dispersal. Examples on a UK landscape and synthetic landscapes.
- **Model:** An individual-based platform on habitat rasters. It covers population dynamics, emigration, transfer (kernel or stochastic movement simulator) and settlement. Version 2.0 adds dynamic landscapes and genetics.
- **Inputs:** Habitat rasters, possibly time-varying.
- **Parameters:** Many, user-defined.
- **Code:** https://github.com/RangeShifter (verified), including RangeShiftR-package (verified).
- **Validation:** Demonstration examples.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 2.
  - S4 2.
  - S5 1.
  - → 7, B. Assessed from: abstract (provisional).
- **Browser fit:** Heavy in full. A reduced population-per-cell variant is feasible.
- **Relevance to ca-geo:** ECO-04 and ECO-07. Shows how to parameterise dispersal on grids.

### pascual2002cluster — Cluster size distributions: signatures of self-organization in spatial ecologies
- **Citation:** Pascual, M., Roy, M., Guichard, F., Flierl, G. (2002). *Philosophical Transactions of the Royal Society B* 357(1421), 657–666. DOI: 10.1098/rstb.2001.0983 (verified: Crossref)
- **Access:** OA (in PMC, PMC1692977)
- **Phenomenon and study area:** Lattice predator–prey and disturbance–recovery systems; theoretical.
- **Model:** Three lattice models of antagonistic interactions. In the predator–prey CA (as documented in caspr), prey reproduce into empty 4-neighbours, predators eat a neighbouring prey and move onto its site, and predators that find no prey starve with probability δ.
- **Inputs:** None.
- **Parameters:** Prey and predator reproduction rates and starvation probability.
- **Code:** caspr `predprey`, https://github.com/fdschneider/caspr (verified).
- **Validation:** Cluster-size and perimeter–area power-law exponents.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 1 (third-party code only, harmonised rule).
  - S4 2.
  - S5 1.
  - → 6, C. Assessed from: abstract + caspr documentation (provisional).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-06 predator–prey. A habitat mask could make it geographic.

### scheller2007design — Design, development, and application of LANDIS-II
- **Citation:** Scheller, R. M., Domingo, J. B., Sturtevant, B. R., Williams, J. S., Rudy, A., Gustafson, E. J., Mladenoff, D. J. (2007). *Ecological Modelling* 201(3–4), 409–419. DOI: 10.1016/j.ecolmodel.2006.10.009 (verified: Crossref)
- **Access:** paywall (USFS Treesearch copy listed, not checked)
- **Phenomenon and study area:** Forest succession and disturbance; boreal application with a pre-industrial fire regime.
- **Model:** A raster landscape model with species-age cohorts per cell. Succession, seed dispersal and disturbance run as extensions with their own time steps.
- **Inputs:** Initial communities, ecoregions, species life-history tables.
- **Parameters:** Extension-specific tables.
- **Code:** https://github.com/LANDIS-II-Foundation (verified).
- **Validation:** Shows that time-step choice changes the estimated pre-industrial conditions.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 2.
  - S4 1.
  - S5 1.
  - → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** Use the "age-only succession" idea as a light browser CA.
- **Relevance to ca-geo:** ECO-02, plus fire coupling with HAZ-01.

### he1999spatially — Spatially explicit and stochastic simulation of forest-landscape fire disturbance and succession
- **Citation:** He, H. S., Mladenoff, D. J. (1999). *Ecology* 80(1), 81–99. DOI: 10.1890/0012-9658(1999)080[0081:SEASSO]2.0.CO;2 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Fire and succession in forest landscapes (LANDIS); northern Wisconsin per secondary sources.
- **Model:** Raster cells with species-age cohorts. Seed dispersal, establishment and fire spread are stochastic.
- **Inputs:** Species maps, landtypes.
- **Parameters:** Not seen.
- **Code:** The original LANDIS was not checked. Its successor LANDIS-II is open (verified).
- **Validation:** Not seen.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 1.
  - S4 1.
  - S5 1.
  - → 5, C. Assessed from: metadata + secondary description (provisional).
- **Browser fit:** Moderate.
- **Relevance to ca-geo:** ECO-02, chain L4.

### kefi2007local — Local facilitation, bistability and transitions in arid ecosystems
- **Citation:** Kéfi, S., Rietkerk, M., van Baalen, M., Loreau, M. (2007). *Theoretical Population Biology* 71(3), 367–379. DOI: 10.1016/j.tpb.2006.09.003 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Arid vegetation; theoretical.
- **Model:** A spatial vegetation CA in which local facilitation drives bistability and patchiness. Strong facilitation lowers the risk of abrupt transitions (paraphrased from the abstract).
- **Inputs:** None.
- **Parameters:** Not seen. caspr's grazing model uses the same parameter set plus grazing terms.
- **Code:** Derived variant in caspr (S3 = 1, because a direct implementation was not confirmed).
- **Validation:** Model analysis only.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 1.
  - S4 2.
  - S5 1.
  - → 6, C. Assessed from: abstract (provisional; the full text is known to give the complete transition rates, so this score likely rises to B).
- **Round 2:** Full text still unreachable (Elsevier; the WUR repository record has no file). `schneider2016spatially` (full text) restates the Kéfi et al. 2007 TPB rule — regeneration r + f·q+|−, colonisation (δρ+ + (1−δ)q+|0)(b − cρ+), degradation d, constant mortality m — and quotes the inherited values r = 0.01, f = 0.9, δ = 0.1, c = 0.2, d = 0.1 (von Neumann neighbourhood). S1 → 2 from that secondary full text; S2 stays 1 because m and the b range of the original paper were not seen. → 7, B. Round 2: re-assessed from secondary full text — S 2 1 1 2 1 (was 1 1 1 2 1, C 6).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-08.

### kefi2007spatial — Spatial vegetation patterns and imminent desertification in Mediterranean arid ecosystems
- **Citation:** Kéfi, S., Rietkerk, M., Alados, C. L., Pueyo, Y., Papanastasis, V. P., ElAich, A., de Ruiter, P. C. (2007). *Nature* 449(7159), 213–217. DOI: 10.1038/nature06111 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Grazed drylands in Spain, Greece and Morocco.
- **Model:** The facilitation CA with grazing mortality. Observed and simulated patch-size distributions follow power laws, which break down near desertification.
- **Inputs:** Aerial photographs of field sites.
- **Parameters:** Not seen.
- **Code:** As kefi2007local.
- **Validation:** Power-law fits on field data.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 1.
  - S4 1.
  - S5 2.
  - → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-08 (EU sites). The patch-size indicator gives an evaluation idea.
- **Round 2:** No OA full text found (WUR record without file). Score unchanged.

### pitt2009predicting — Predicting Argentine ant spread over the heterogeneous landscape using a spatially explicit stochastic model
- **Citation:** Pitt, J. P. W., Worner, S. P., Suarez, A. V. (2009). *Ecological Applications* 19(5), 1176–1186. DOI: 10.1890/08-1777.1 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Linepithema humile in New Zealand since 1990.
- **Model:** A GIS-integrated stochastic dispersal model with local spread plus human-assisted jumps, run as many replicates. It is compared with uniform radial spread.
- **Inputs:** Habitat suitability, human infrastructure layers.
- **Parameters:** Not seen.
- **Code:** MDiG (GRASS-based), https://github.com/ferrouswheel/mdig (verified). The README cites this Argentine ant study.
- **Validation:** Against the historical spread. Radial spread did better early in the invasion, the simulation model better later.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 2.
  - S4 1.
  - S5 1.
  - → 6, C. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** ECO-03. Human-assisted long-distance dispersal along roads.

### potterf2017simulating — Simulating bark beetle population dynamics in response to windthrow events
- **Citation:** Potterf, M., Bone, C. (2017). *Ecological Complexity* 32, 21–30. DOI: 10.1016/j.ecocom.2017.08.003 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Ips typographus transition from endemic to epidemic after windthrow, in Norway spruce.
- **Model:** A spatially explicit agent-based model in NetLogo. Scenarios vary windthrow extent and clustering. Scattered windthrow speeds up the transition; large clusters slow it.
- **Inputs:** Synthetic windthrow patterns.
- **Parameters:** Not seen.
- **Code:** NetLogo code is listed by CoMSES as an Elsevier supplementary zip, reachable only through the publisher (S3 = 1).
- **Validation:** Not seen.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 1.
  - S4 1.
  - S5 1.
  - → 5, C. Assessed from: abstract via search (provisional).
- **Browser fit:** Moderate.
- **Relevance to ca-geo:** HAZ-04 → ECO-01 chain L3.

### harati2020integrating — Integrating Neighborhood Effect and Supervised Machine Learning Techniques to Model and Simulate Forest Insect Outbreaks in British Columbia, Canada
- **Citation:** Harati, S., Perez, L., Molowny-Horas, R. (2020). *Forests* 11(11), 1215. DOI: 10.3390/f11111215 (verified: Crossref)
- **Access:** OA (CC BY)
- **Phenomenon and study area:** Mountain pine beetle mortality across British Columbia, 1999–2014.
- **Model:** A one-way land-change CA. The transition probability comes from GLM or random forest using elevation, aspect, slope, ruggedness and a weighted neighbourhood of infestation. Forecast for 2020.
- **Inputs:** Annual BC Ministry of Forests mortality maps and a DEM.
- **Parameters:** ML-fitted, with cross-validation.
- **Code:** Not found.
- **Validation:** Error metrics for 2008–2014; random forest beats GLM.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 2.
  - → 5, C. Assessed from: abstract (provisional).
- **Browser fit:** Good if a logistic model is used.
- **Relevance to ca-geo:** ECO-01. A data-driven alternative trainable on Czech dieback maps.

### nehrbass2007simulation — A simulation model of plant invasion: long-distance dispersal determines the pattern of spread
- **Citation:** Nehrbass, N., Winkler, E., Müllerová, J., Pergl, J., Pyšek, P., Perglová, I. (2007). *Biological Invasions* 9(4), 383–395. DOI: 10.1007/s10530-006-9040-6 (verified: Crossref). Online 2006.
- **Access:** OA archive copy: https://webarchiv.lib.cas.cz/wayback/20090223190856/http:/www.ibot.cas.cz/personal/pysek/pdf/Nehrbass%20et%20al_Heracleum%20simulation%20_BiolInv2007.pdf
- **Phenomenon and study area:** Giant hogweed at Arnoltov, Slavkovský les Protected Landscape Area, W Bohemia, Czech Republic.
- **Model:**
  - **Grid and habitat:** 700×700 m, 5×5 m cells (19,600). Each cell is suitable or unsuitable from 18 land-use classes; habitat changes are inserted in the year they were observed.
  - **Plants:** Individual-based, yearly. Carrying capacity is 200 plants per suitable cell (ceiling). Fat-tailed seedling production has mean 2.57.
  - **Dispersal:** Fractions of seedlings stay in the home cell, go to the Moore neighbourhood, or go to uniformly random long-distance cells. Detailed life-history rules are in a companion 2006 paper.
- **Inputs:** Aerial photos 1953–2000 (0.5 m orthophotos) and permanent-plot demography.
- **Parameters:** Partly given here, partly in the companion paper. The long-distance fraction is fitted.
- **Code:** Not found.
- **Validation:** Occupied-cell growth rates: simulated 1.16 vs. observed 1.15 per year, with the time series in Table 2.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 2.
  - → 5, C. Assessed from: full text.
- **Browser fit:** Very good. Can be converted to cell densities.
- **Relevance to ca-geo:** ECO-03. A Czech case with historical aerial photos, which could be rebuilt from ČÚZK archival orthophotos.
- **Round 2:** The companion life-history paper was verified in Crossref — Nehrbass, N., Winkler, E., Pergl, J., Perglová, I., Pyšek, P. (2006), *Perspectives in Plant Ecology, Evolution and Systematics* 7(4), 253–262, DOI 10.1016/j.ppees.2005.11.001 — but no OA copy was found, so S2 stays 1. Unchanged.

### Further C-class insect-outbreak and pest-spread models

#### bone2006fuzzy — A fuzzy-constrained cellular automata model of forest insect infestations
- **Citation:** Bone, C., Dragicevic, S., Roberts, A. (2006). *Ecological Modelling* 192(1–2), 107–125. DOI: 10.1016/j.ecolmodel.2005.09.013 (verified: Crossref)
- **Access:** paywall. The underlying MSc thesis (Bone 2005, SFU) is OA at https://summit.sfu.ca/item/4830 (verified 200).
- **Phenomenon and study area:** Mountain pine beetle, central interior of British Columbia.
- **Model:** A GIS-based CA. Fuzzy sets estimate tree susceptibility from geospatial data, and the CA reproduces the spatial pattern of tree mortality.
- **Inputs:** High-resolution remote sensing and GIS layers.
- **Parameters:** Fuzzy membership functions; values not seen.
- **Code:** Not found.
- **Validation:** Not seen.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: thesis abstract (provisional). The thesis full text could raise S1 and S2.
- **Round 2 (thesis full text, Chapter 3):** Two 750×750 m sites, 1 m cells derived from 15 cm imagery. Part I builds a fuzzy susceptibility μ(Su) per pine cell from four fuzzy layers (pine share, distance to deciduous stands, distance to last year's attacks, tree size; membership functions only as figures). Part II: winter mortality removes 98 % (cold winter, −30 °C threshold) or 80 % (mild) of infested trees at random; a dispersal CA with a 500×500-cell window and an attack CA with a 25×25 window turn a tree "attacked" when the share of beetle-containing (or attacked) trees in the window reaches f(μ(Su)), with linear, exponential and power threshold functions tested; the power function (exponent a) was calibrated by mean distance between simulated and observed killed trees and by kills per susceptibility class. Calibration and function choice were mainly visual; membership curves and the number of attack sub-steps are not tabulated. Round 2: re-assessed from thesis full text — S 1 1 0 1 1 (unchanged, C 4). The journal paper itself remains paywalled.
- **Browser fit:** Good.
- **Relevance to ca-geo:** ECO-01. The fuzzy susceptibility layer maps naturally onto CZ inputs (spruce share, drought).

#### fahse2011simulation — Simulation and analysis of outbreaks of bark beetle infestations and their management at the stand level
- **Citation:** Fahse, L., Heurich, M. (2011). *Ecological Modelling* 222(11), 1833–1846. DOI: 10.1016/j.ecolmodel.2011.03.014 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Ips typographus, Bavarian Forest National Park. The park adjoins Šumava NP (CZ).
- **Model:** SAMBIA, an agent-based model of individual trees and beetles. It shows a sharp threshold response: outbreaks become rare when about 80 % of beetles are removed by antagonists or management (summarised from the abstract).
- **Inputs:** Stand data.
- **Parameters:** Not seen.
- **Code:** Not found.
- **Validation:** Not seen.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: abstract via search (provisional).
- **Browser fit:** Moderate.
- **Relevance to ca-geo:** ECO-01. The roughly 80 % removal threshold is a useful qualitative check for a CA.
- **Round 2:** Semantic Scholar lists it as closed; no OA copy found. Unchanged. The same ~80 % felling threshold reappears in `pietzsch2023nonparametric` (full text), which makes it a cross-checked target.

#### anderson2016geosimulation — A Geosimulation Approach for Data Scarce Environments: Modeling Dynamics of Forest Insect Infestation across Different Landscapes
- **Citation:** Anderson, T., Dragicevic, S. (2016). *ISPRS International Journal of Geo-Information* 5(2), 9. DOI: 10.3390/ijgi5020009 (verified: Crossref)
- **Access:** OA (CC BY)
- **Phenomenon and study area:** Emerald ash borer on hypothetical landscape types (urban, rural and others).
- **Model:** GIS plus multi-criteria evaluation (susceptibility) plus CA spread.
- **Inputs:** Hypothetical rasters.
- **Parameters:** Not seen.
- **Code:** Not found.
- **Validation:** Qualitative comparison of landscapes.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** ECO-01 and ECO-03. The MCE susceptibility step is reusable.

#### moykkynen2014modelling — Modelling of the spread of a potential invasive pest, the Siberian moth (Dendrolimus sibiricus) in Europe
- **Citation:** Möykkynen, T., Pukkala, T. (2014). *Forest Ecosystems* 1(1), 10. DOI: 10.1186/s40663-014-0010-7 (verified: Crossref)
- **Access:** OA (CC BY)
- **Phenomenon and study area:** Potential spread of Dendrolimus sibiricus into Europe from Russian border stations over 20 years.
- **Model:** A stochastic, CA-like grid model with 1 km cells.
  - **Host trees:** The number per cell comes from EFI host-species cover × 500 trees/ha.
  - **Flight and acceptance:** Moths fly a truncated negative exponential distance (mean 11 km, max 50 km) in a random direction. A cell is accepted with probability f(ecoclimatic index) × healthy hosts / maximum hosts.
  - **Mating and survival:** Mating probability rises with local density (p_low = 0.1). Survival from predation and parasitism is density-dependent.
  - **Host trees and transport:** An infected tree spreads offspring for 2 years and then dies. Human-assisted transport is weighted by population density.
- **Inputs:** EFI 1 km host maps, CLIMEX ecoclimatic index (present and climate-change scenarios), human population density.
- **Parameters:** Several given in the text. Some response curves are shown only in figures.
- **Code:** Not found.
- **Validation:** None possible (pest not yet present); sensitivity analysis.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: full text.
- **Browser fit:** Good at 1 km EU scale.
- **Relevance to ca-geo:** ECO-03, EU-scale invasive defoliator. A template for a "pest arrives at a border station" demo.

#### prasad2010modeling — Modeling the invasive emerald ash borer risk of spread using a spatially explicit cellular model
- **Citation:** Prasad, A. M., Iverson, L. R., Peters, M. P., Bossenbroek, J. M., Matthews, S. N., Sydnor, T. D., Schwartz, M. W. (2010). *Landscape Ecology* 25(3), 353–369. DOI: 10.1007/s10980-009-9434-9 (verified: Crossref). Online 2009.
- **Access:** OA copies (USFS Treesearch 34719; University of Toledo PDF; found via search, text not extractable here)
- **Phenomenon and study area:** Emerald ash borer, Ohio.
- **Model:** The SHIFT scheme. A cell-based model combines insect flight with human-assisted long-distance movement (a gravity model over campgrounds, roads, wood products and population). It produces a weighted risk map. The front advanced roughly 20 km per year (search summary).
- **Inputs:** Ash abundance, roads, campgrounds, population, quarantine zones.
- **Parameters:** Weighting scheme; values not seen.
- **Code:** Not found.
- **Validation:** Against EAB positives and detection trees.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: abstract + section outline (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** ECO-03. Gravity-model long-distance dispersal is a candidate for human-mediated jumps (e.g. along D1/D5 motorways).

### balzter1998cellular — Cellular automata models for vegetation dynamics
- **Citation:** Balzter, H., Braun, P. W., Köhler, W. (1998). *Ecological Modelling* 107(2–3), 113–125. DOI: 10.1016/S0304-3800(97)00202-0 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Three plant species on a grazed lawn (Germany).
- **Model:** Spatio-temporal Markov chains (STMC), a CA class that adds spatial order (neighbour influence) to a Markov transition matrix. Models of two spatial orders are compared.
- **Inputs:** Grid-cell species records.
- **Parameters:** Transition matrices estimated from data.
- **Code:** Not found.
- **Validation:** Good fit for Glechoma, deviations for Lolium and Trifolium, explained by selective grazing.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-02 and LND-02 (overgrowth). STMC is a principled bridge from CA–Markov land-use models to ecology.

### wadsworth2000simulating — Simulating the spread and management of alien riparian weeds: are they out of control?
- **Citation:** Wadsworth, R. A., Collingham, Y. C., Willis, S. G., Huntley, B., Hulme, P. E. (2000). *Journal of Applied Ecology* 37(s1), 28–38. DOI: 10.1046/j.1365-2664.2000.00551.x (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Impatiens glandulifera and Heracleum mantegazzianum in County Durham, UK.
- **Model:** MIGRATE, a spatially explicit GIS model with demography and multiple dispersal mechanisms, including along rivers. Six control-prioritisation strategies were compared at different treatment intensity, efficiency and timeliness.
- **Inputs:** Topographic, hydrological and land-cover maps.
- **Parameters:** Not seen.
- **Code:** Not found.
- **Validation:** Scenario comparison.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** ECO-03. Management scenarios would make a good interactive "control strategy" toggle.

### kramerschadt2004fragmented — Fragmented landscapes, road mortality and patch connectivity: modelling influences on the dispersal of Eurasian lynx
- **Citation:** Kramer-Schadt, S., Revilla, E., Wiegand, T., Breitenmoser, U. (2004). *Journal of Applied Ecology* 41(4), 711–723. DOI: 10.1111/j.0021-8901.2004.00933.x (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Lynx dispersal between suitable patches in Germany. The model is calibrated on Swiss Jura telemetry.
- **Model:** An individual-based, spatially explicit dispersal model on a dispersal-habitat raster, with road mortality.
- **Inputs:** Habitat map, road network.
- **Parameters:** Calibrated from telemetry; values not seen.
- **Code:** Not found.
- **Validation:** Calibration to telemetry. Under realistic road mortality, only patches along the German–Czech border stay connected.
- **Reimplementability:**
  - S1 1.
  - S2 1.
  - S3 0.
  - S4 1.
  - S5 1.
  - → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** Good. Random walkers on a raster.
- **Relevance to ca-geo:** ECO-04 and EPI-02 (chain L13). Directly relevant to the Šumava–Bavarian Forest corridor.

### duraciova2020bark — A bark beetle infestation predictive model based on satellite data in the frame of decision support system TANABBO (round 2)
- **Citation:** Duračiová, R., Muňko, M., Barka, I., Koreň, M., Resnerová, K., Holuša, J., Blaženec, M., Potterf, M., Jakuš, R. (2020). *iForest – Biogeosciences and Forestry* 13(1), 215–223. DOI: 10.3832/ifor3271-013 (verified: Crossref)
- **Access:** OA (CC BY-NC), PDF at iforest.sisef.org
- **Phenomenon and study area:** Ips typographus spot initiation and spot spreading in managed forests of the Bohemian Forest (Šumava), Czech Republic, yearly steps 2007–2010. Co-authors from the Czech University of Life Sciences Prague (ČZU) and Slovak institutes.
- **Model:**
  - **Grid and inputs:** 30 m raster from Landsat-based vegetation-change time series (beetle-killed spots per year), a 30 m DEM (solar radiation) and forest stand data (age structure, spruce share).
  - **Spot spreading:** Cost distance from the previous year's spots (distance 0 → 1, rescaled), NDVI, solar radiation and stand attributes enter a logistic regression giving a susceptibility value per cell. Cells beyond 228 m from existing spots are excluded from spreading.
  - **Spot initiation:** A separate logistic model without the distance term; spot size from a linear regression.
  - **Time:** One-year forecast; iterating it year by year would turn it into a simple data-driven CA (not done in the paper).
- **Parameters:** Regression coefficients per year in Tab. 3 (logistic) and Tab. 4 (linear spot size); Gini importance of factors in Tab. 1.
- **Code:** Implemented in TANABBO v. 1.9 (Python); no public repository found.
- **Validation:** ROC/AUC per year and module, 0.75–0.82 (Tab. 5), against observed infestations.
- **Reimplementability:**
  - S1 1: regression structure clear; susceptibility-to-infestation conversion and iteration not specified.
  - S2 2: coefficient tables.
  - S3 0.
  - S4 1: Landsat and DEM open; the stand database (forest management plans) not open.
  - S5 2: AUC table.
  - → 6, C. Assessed from: full text.
- **Browser fit:** Excellent (one logistic surface per year).
- **Relevance to ca-geo:** ECO-01. **The only verified bark-beetle spread model with a Czech study area found so far.** Its 228 m spreading limit and AUC values are direct targets for a Šumava demo; its coefficients can be used as a data-driven transition rule.

### kautz2016dispersal — Dispersal variability and associated population-level consequences in tree-killing bark beetles (round 2)
- **Citation:** Kautz, M., Imron, M. A., Dworschak, K., Schopf, R. (2016). *Movement Ecology* 4(1), 9. DOI: 10.1186/s40462-016-0074-9 (verified: Crossref)
- **Access:** OA (PMC4832482)
- **Phenomenon and study area:** Dispersal of Ips typographus in a virtual Norway spruce stand with resistant, susceptible or scattered host susceptibility.
- **Model:** The IPS (Infestation Pattern Simulation) individual-based model in NetLogo. One dispersal wave from a source; beetles move between neighbouring trees with a movement angle, sense host attractiveness within a perceptual range, spend energy, aggregate, and colonise a tree when enough beetles overcome its defence (tree carrying capacity and susceptibility). A detailed ODD and the model version are in Additional file 1.
- **Parameters:** Table 1 lists beetle and tree parameters with sources (e.g. perceptual range 15 m, moving angle 45°, energy level 10 abstract units, consumption efficiency from an exponential distribution).
- **Code:** Supplementary material (model version) per the paper; not downloaded, no public repository found.
- **Validation:** Model experiments only (success rates, infestation counts, distance to source).
- **Reimplementability:**
  - S1 2: ODD available.
  - S2 2: Table 1.
  - S3 1: code only as journal supplement (not verified).
  - S4 2: virtual stands.
  - S5 1.
  - → 8, B. Assessed from: full text (keyword-guided via Europe PMC XML).
- **Browser fit:** Moderate (individual beetles; one dispersal wave is small).
- **Relevance to ca-geo:** ECO-01. Mechanistic background for a CA dispersal kernel; the "scattered susceptibility" result is a qualitative check for a cell-level model. Bavarian Forest group (Kautz 2011 data).

### kautz2014individual — Individual traits as drivers of spatial dispersal and infestation patterns in a host–bark beetle system (round 2)
- **Citation:** Kautz, M., Schopf, R., Imron, M. A. (2014). *Ecological Modelling* 273, 264–276. DOI: 10.1016/j.ecolmodel.2013.11.022 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Introduces the IPS model (see `kautz2016dispersal`) for Ips typographus: dispersal, host selection, aggregation, colonisation or rejection, from a single source in a virtual stand.
- **Validation:** One-factor-at-a-time sensitivity of success rate, number of infestations and maximum infestation distance; host recognition and attack synchrony parameters were most sensitive (from search-engine abstract).
- **Reimplementability:** S1 1; S2 1; S3 1 (model version in the 2016 supplement); S4 2; S5 1 → 6, C. Assessed from: secondary (abstract via search; provisional).
- **Relevance to ca-geo:** ECO-01, parameter sensitivity for a beetle CA.

### dullinger2004modelling — Modelling climate change-driven treeline shifts: relative effects of temperature increase, dispersal and invasibility (round 2)
- **Citation:** Dullinger, S., Dirnböck, T., Grabherr, G. (2004). *Journal of Ecology* 92(2), 241–252. DOI: 10.1111/j.0022-0477.2004.00872.x (verified: Crossref)
- **Access:** paywall (Wiley "bronze" link returned HTML to automated fetch)
- **Phenomenon and study area:** Upslope spread of the shrubby pine *Pinus mugo* at the treeline, Northern Calcareous Alps, Austria.
- **Model:** A temporally and spatially explicit plant-spread model, parameterised from field data, with sensitivity to the climate trend, the spatial distribution of recruits around seed sources (dispersal curve) and the resistance of resident non-woody vegetation to invasion. 1000-year runs; pine cover rose from 10 % to 24–59 % of the landscape (abstract, Europe PMC).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** Good (landscape grid, yearly steps).
- **Relevance to ca-geo:** ECO-07 (treeline shift). Alpine analogue for Krkonoše / Hrubý Jeseník dwarf-pine belt; shows that dispersal and invasibility matter as much as warming.

### zeng2006endogenous — Endogenous Fractal Dynamics at Alpine Treeline Ecotones (round 2)
- **Citation:** Zeng, Y., Malanson, G. P. (2006). *Geographical Analysis* 38(3), 271–287. DOI: 10.1111/j.1538-4632.2006.00686.x (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** Advance of trees into alpine tundra; generic (field-study-based rules).
- **Model:** A cellular automaton with nonlinear local positive and negative feedbacks in tree establishment and mortality. Fourier analysis shows fractal spatial and temporal patterns; landscape-scale correlations between pattern and advance rate emerge from local rules (Crossref abstract). A related dissertation (Zeng, University of Iowa, DOI 10.17077/etd.8n8tphn6, Crossref record seen) may contain the full rule set.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2 (generic lattice, could sit on a DEM); S5 1 → 5, C. Assessed from: abstract (provisional).
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** ECO-07. The only explicit treeline CA found; a DEM-driven variant for Czech mountains is straightforward.

### lischke2006treemig — TreeMig: A forest-landscape model for simulating spatio-temporal patterns from stand to landscape scale (round 2)
- **Citation:** Lischke, H., Zimmermann, N. E., Bolliger, J., Rickebusch, S., Löffler, T. J. (2006). *Ecological Modelling* 199(4), 409–420. DOI: 10.1016/j.ecolmodel.2005.11.046 (verified: Crossref)
- **Access:** paywall (abstract elided by publisher)
- **Phenomenon and study area:** Forest dynamics and tree species migration; Swiss applications (e.g. Holocene runs in Valais on a 1 km grid, per project pages).
- **Model (from WSL project pages):** A grid of linked cells (25 m to 1 km); in each cell a multi-species, height-structured forest model (density per height class, light attenuation, growth, competition, mortality, reproduction); seeds disperse between cells. A model documentation PDF is online: https://treemig.wsl.ch/fileadmin/user_upload/WSL/Microsite/TreeMig/TreeMigDocu_23_Model.pdf (verified 200; not read).
- **Code:** An R package and GUI are described on https://treemig.wsl.ch (verified 200); no download or licence confirmed.
- **Reimplementability:** S1 1; S2 1; S3 0 (availability not verified); S4 1; S5 1 → 4, C. Assessed from: secondary (project documentation pages; provisional). The open documentation PDF could raise S1/S2.
- **Browser fit:** Moderate (several species × height classes per cell).
- **Relevance to ca-geo:** ECO-02 and ECO-07; the main verified **seed-dispersal grid model** for Central European forests.

### fritsch2026mechanistic — Mechanistic-statistical model for the expansion of ash dieback (round 2)
- **Citation:** Fritsch, C., Grosdidier, M., Gégout-Petit, A., Marçais, B. (2026). *Theoretical Population Biology* 171, 1–21. DOI: 10.1016/j.tpb.2026.06.006 (verified: Crossref). Preprint arXiv 2409.06273.
- **Access:** preprint (arXiv, read)
- **Phenomenon and study area:** Spread of *Hymenoscyphus fraxineus* (ash dieback) across France, 2008–2023.
- **Model:** A reaction–diffusion equation for leaf infection (diffusion coefficient D) coupled with a rachis (leaf-litter) colonisation stage, modulated by summer temperature (best index: number of days above 28 °C), spring rainfall and ash density; an Allee term was tested and found unnecessary. Discretised on 16×16 km quadrats; an observation model links simulated infection to presence reports, with Bayesian estimation (AMIS).
- **Parameters:** Five estimated parameters with priors in Table 2 and posterior ranges in figures; correlations in Table 3.
- **Code:** Not found.
- **Validation:** Likelihood and RMSE per year (Table 4) for 2008–2019, with forecasts for later years.
- **Reimplementability:**
  - S1 2: equations and discretisation given.
  - S2 1: posterior values mainly as figures.
  - S3 0.
  - S4 1: French forest-health reports and meteorology described, not redistributed.
  - S5 2: RMSE table.
  - → 6, C. Assessed from: full text (preprint, keyword-guided).
- **Browser fit:** Very good (coarse quadrat grid, explicit finite-difference step = a CA).
- **Relevance to ca-geo:** **ECO-09 (ash dieback)** — the best verified European ash-dieback spread model; ash dieback is widespread in CZ. Kernel values from `grosdidier2018tracking`.

### dunn2007simulating — Simulating Weed Propagation Via Hierarchical, Patch-Based Cellular Automata (round 2)
- **Citation:** Dunn, A. G., Majer, J. D. (2007). In: *Lecture Notes in Computer Science* (ICCS 2007), 762–769. DOI: 10.1007/978-3-540-72584-8_101 (verified: Crossref)
- **Access:** OA (publisher PDF, read)
- **Phenomenon and study area:** Environmental weed spread (bird- and human-dispersed) on fictitious GIS data framed on south-west Western Australia.
- **Model:** An irregular, hierarchical CA: GIS patches at several granularities form a network; each link carries a probability set from patch states and distance; each synchronous step a breadth-first search over the network yields dispersal likelihoods, mimicking short and long-distance dispersal.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 0 → 2, D. Assessed from: full text.
- **Relevance to ca-geo:** ECO-03 concept only: irregular patch cells built from land-cover polygons as an alternative to a raster.

### Reviews, frameworks, tools and parameter sources (not scored)

#### grosdidier2018tracking — Tracking the invasion: dispersal of Hymenoscyphus fraxineus airborne inoculum at different scales (round 2)
- **Citation:** Grosdidier, M., Ioos, R., Husson, C., Cael, O., Scordia, T., Marçais, B. (2018). *FEMS Microbiology Ecology* 94(5), fiy049. DOI: 10.1093/femsec/fiy049 (verified: Crossref)
- **Value:** Spore-trap and symptom data from France. Most inoculum stays within about 50 m of infected ash, yet spores were detected 50–100 km ahead of the symptom front; two Bayesian-fitted kernels (best: inverse power law) with mean dispersal of about 1.4 km (local) and 2.6 km (regional) (from search-engine abstract). Parameter source for an ECO-09 ash-dieback CA. Reimplementability: n/a.

#### hallas2026assessing — Assessing disturbance risks of the European spruce bark beetle under climate change: a review of model approaches and future perspectives
- **Citation:** Hallas, T., Hoch, G., Kirisits, T., Netherer, S. (2026). *European Journal of Forest Research* 145(2), 23. DOI: 10.1007/s10342-025-01841-x (verified: Crossref, OpenAlex)
- **Access:** OA
- **Value:** An up-to-date map of Ips typographus models: phenology (PHENIPS and variants, validated in CZ), dispersal, and landscape models (LANDIS, iLand and others). It points to Czech parameter sources (`dolezal2016fine`, `berec2013population`). Reimplementability: n/a.

#### rammer2024individual — The individual-based forest landscape and disturbance model iLand: Overview, progress, and outlook
- **Citation:** Rammer, W., Thom, D., Baumann, M., Braziunas, K., Dollinger, C., Kerber, J., Mohr, J., Seidl, R. (2024). *Ecological Modelling* 495, 110785. DOI: 10.1016/j.ecolmodel.2024.110785 (verified: Crossref, OpenAlex)
- **Access:** OA
- **Value:** Entry point to iLand modules (wind, bark beetle, fire, BITE). Code at https://github.com/edfm-tum/iland-model (verified). Reimplementability: n/a.

#### genin2018monitoring — Monitoring ecosystem degradation using spatial data and the R package spatialwarnings
- **Citation:** Génin, A., Majumder, S., Sankaran, S., et al. (2018). *Methods in Ecology and Evolution* 9(10), 2067–2075. DOI: 10.1111/2041-210x.13058 (verified: Crossref)
- **Access:** paywall
- **Value:** A workflow and code for spatial early-warning indicators (patch-size distributions, spatial variance and autocorrelation) on rasters and CA output. Code at https://github.com/spatial-ews/spatialwarnings and https://cran.r-project.org/package=spatialwarnings (both verified). Useful as an evaluation layer for ECO-08 demos. Reimplementability: n/a.

#### durrett1994importance — The Importance of Being Discrete (and Spatial)
- **Citation:** Durrett, R., Levin, S. (1994). *Theoretical Population Biology* 46(3), 363–394. DOI: 10.1006/tpbi.1994.1032 (verified: Crossref)
- **Value:** Compares mean-field, patch, reaction–diffusion and interacting-particle (CA-like) formulations on three species-interaction examples. A justification for discrete CA in ECO-06. Reimplementability: n/a.

#### mcrae2008using — Using circuit theory to model connectivity in ecology, evolution, and conservation
- **Citation:** McRae, B. H., Dickson, B. G., Keitt, T. H., Shah, V. B. (2008). *Ecology* 89(10), 2712–2724. DOI: 10.1890/07-1861.1 (verified: Crossref)
- **Value:** The standard resistance-grid connectivity method (not a CA). Implementation Circuitscape at https://github.com/Circuitscape/Circuitscape.jl (verified). Context and comparison baseline for ECO-04. Reimplementability: n/a.

#### kautz2011quantifying — Quantifying spatio-temporal dispersion of bark beetle infestations in epidemic and non-epidemic conditions
- **Citation:** Kautz, M., Dworschak, K., Gruppe, A., Schopf, R. (2011). *Forest Ecology and Management* 262(4), 598–608. DOI: 10.1016/j.foreco.2011.04.023 (verified: Crossref)
- **Value:** Infestation-to-infestation distance distributions from 22 years of colour-infrared imagery in Bavarian Forest NP, using a GIS distance-ring method. A primary source for ECO-01 kernel calibration. Per Hallas et al., most new infestations lie within about 100–500 m of the previous year's. Reimplementability: n/a (parameter source).

#### potterf2019landscape — Landscape-level spread of beetle infestations from windthrown- and beetle-killed trees in the non-intervention zone of the Tatra National Park, Slovakia (Central Europe)
- **Citation:** Potterf, M., Nikolov, C., Kočická, E., Ferenčík, J., et al. (2019). *Forest Ecology and Management* 432, 489–500. DOI: 10.1016/j.foreco.2018.09.050 (verified: Crossref)
- **Value:** Distances from windthrow and beetle sources, spot sizes (40 % < 100 m², 79 % < 500 m²) and infestation probability by outbreak phase, from colour-infrared aerial photos 2005–2015. Reference statistics for the HAZ-04 → ECO-01 chain. Reimplementability: n/a.

#### dolezal2016fine — Fine fluorescent powder marking study of dispersal in the spruce bark beetle, Ips typographus
- **Citation:** Doležal, P., Okrouhlík, J., Davídková, M. (2016). *European Journal of Entomology* 113. DOI: 10.14411/eje.2016.001 (verified: Crossref)
- **Value:** A Czech (Šumava) mark–recapture dispersal function. According to `hallas2026assessing`, 90 % of recaptures fell within 500 m. A direct kernel source for a CZ beetle CA; the primary text is still to be read. Reimplementability: n/a.

#### berec2013population — Population dynamics of Ips typographus in the Bohemian Forest (Czech Republic): Validation of the phenology model PHENIPS and impacts of climate change
- **Citation:** Berec, L., Doležal, P., Hais, M. (2013). *Forest Ecology and Management* 292, 1–9. DOI: 10.1016/j.foreco.2012.12.018 (verified: Crossref)
- **Value:** A temperature-driven count of generations per year for the Bohemian Forest. It can feed a per-cell "beetle generations" layer (from a DEM plus temperature) into an ECO-01 CA. Reimplementability: n/a.

## Most reimplementable (top picks)

Updated in round 2.

1. **pietzsch2023nonparametric (A, 10; was B 8).** 250 m Markov CA with an 8-neighbour spread rule, open transition tables and code, and per-cell F1 validation on the 2017/2018 Ips typographus outbreak at the Czech border. Now the strongest ECO-01 reference.
2. **liu2025multiscale (A, 9).** Full equations, parameter tables and a GitHub repo for a stochastic hex-grid dispersal CA; drop-in ECO-01 dispersal core.
3. **schneider2016spatially (A, 9; was B 7).** Complete three-state dryland CA (rule, all parameters, periodic boundaries, synchronous update) with the authors' R code; the best ECO-08 test oracle. `kefi2007local` (B 7) is its parent rule.
4. **engler2012migclim / nobis2014kissmig (B, 8; were B 7).** Range-shift CAs whose full rules are in open package documentation or source (ECO-07).
5. **kautz2016dispersal (B, 8, new).** ODD-documented beetle IBM; mechanistic basis for ECO-01 kernels.
6. **moenickes2013shapes (B, 7).** Corridor plus long-distance spread with efficiency targets (ECO-03).
7. **rademacher2004reconstructing, thiery1995model (B, 7).** Open ODD beech mosaic CA; anisotropic banded-vegetation kernel.
8. **duraciova2020bark (C, 6, new) — CZ.** Data-driven spot-spreading predictor validated in the Bohemian Forest (AUC 0.75–0.82, 228 m spreading limit); calibration target and alternative rule for a Šumava ECO-01 demo.

## Gaps and unverified leads

- **OpenAlex quota.** It was exhausted after 8 queries, so several families (seed dispersal, treeline, windthrow CA, predator–prey with real landscapes) could not be searched systematically. Round 2 should repeat the OpenAlex queries once the budget resets (or with an API key).
- **Verified in Crossref but not assessed** (no abstract or full text reachable). Candidates for round 2:
  - Wissel (1992) "Modelling the mosaic cycle of a Middle European beech forest", *Ecol. Model.* 63, DOI 10.1016/0304-3800(92)90060-R
  - Jeltsch & Wissel (1994) "Modelling dieback phenomena in natural forests", *Ecol. Model.* 75–76, DOI 10.1016/0304-3800(94)90011-6
  - Hogeweg (1988) "Cellular automata as a paradigm for ecological modeling", DOI 10.1016/0096-3003(88)90100-2
  - Silvertown et al. (1992) CA competition for space, *J. Ecol.*, DOI 10.2307/2260696
  - Dunkerley (1997) banded vegetation CA, *J. Arid Environ.*, DOI 10.1006/jare.1995.0158
  - Hassell, Comins & May (1991) *Nature*, DOI 10.1038/353255a0
  - Wootton (2001) empirically derived CA, *Nature*, DOI 10.1038/35101595
  - Colasanti et al. (2007) simple vegetation CA, DOI 10.1016/j.ecolmodel.2006.12.039
  - Sommerfeld et al. (2021) *J. Ecol.*, DOI 10.1111/1365-2745.13502 (iLand in Central Europe)
  - Honkaniemi et al. (2018) WINDROT, DOI 10.1016/j.ecolmodel.2018.09.014
  - Nenzén et al. (2017), DOI 10.1016/j.ecocom.2017.04.004
  - Ferreri & Venturino (2013) predator–prey CA, DOI 10.1016/j.ecocom.2012.09.006
  - Yoshimoto et al. (2016) CA invasive control, DOI 10.1111/nrm.12101
  - Lausch, Fahse & Heurich (2011), DOI 10.1016/j.foreco.2010.10.012
- **Unverified leads:**
  - A conference abstract "Modeling population dynamics of Ips typographus in the Bohemian Forest (Czech Republic)" (ESA 2014). Not in Crossref and possibly unpublished; check with Czech authors (Berec, Doležal).
  - The Bone (2005) and Liu (thesis) SFU theses are in OpenAlex but have no DOI.
  - Kautz et al. 2014/2016 "IPS" model, the IPS-SPREADS paper (Pietzsch et al. 2021), and Cipriotti et al. 2016 (Markov upscaling, DOI 10.1111/2041-210X.12464 as cited in Pietzsch) are not yet verified.
- **Gaps:**
  - No verified CA for beaver wetlands (ECO-05) or treeline/alpine shifts specific to CZ.
  - Seed-dispersal CA is covered only inside the invasion and range-shift models.
  - Windthrow is covered only by iLand (tree level) and the BEFORE and Kubo gap rules. A raster windthrow CA from the geomorphology/hazard side may exist (overlap with `atm`/`geo`).
- **Round 2 gap-search results:**
  - **Treeline / range shift:** two treeline models added (`zeng2006endogenous` CA, `dullinger2004modelling` Austrian Alps), both abstract-only; no Czech treeline CA found.
  - **Windthrow CA:** still none found (Crossref and web return only wildfire CA). HAZ-04 remains covered by iLand / BEFORE / Kubo; a simple edge-exposure rule would be our own variant.
  - **Seed dispersal:** `lischke2006treemig` (grid forest-landscape model with inter-cell seed dispersal) added; no dedicated seed-dispersal CA found.
  - **Central European bark beetle, CZ authors:** `duraciova2020bark` (ČZU co-authors, Bohemian Forest validation). ŠUMLAND project (Institute of Botany CAS, landscape simulation of Šumava with wind and beetle modules, 2010–2014; seen only as a web-search hit, the project page did not respond to our check) — no peer-reviewed model paper found; unverified lead. TANABBO II (Pirtskhalava-Karpova et al. 2024, *Ecol. Model.* 496, 110814, DOI 10.1016/j.ecolmodel.2024.110814, verified; abstract elided) — phenology + drought risk, not assessed.
  - **Beaver / wetland (ECO-05):** no CA of dam building or wetland formation found. Beaver colonisation models along river networks are listed in `epidemics.md` (EPI-04: `chaputbardy2017network`, `graham2022monitoring`); Czech parameter source `john2010habitat` (Morava basin).
  - **ECO-09 plant pests and pathogens:** ash dieback — `fritsch2026mechanistic` (C 6, France) and kernel source `grosdidier2018tracking`; pine processionary moth — Robinet, Rousselet & Roques (2014), *Ann. For. Sci.* 71(2), 149–160, DOI 10.1007/s13595-013-0287-7 (verified; abstract elided, not assessed). Grey literature: a Leeds PhD thesis on ash-dieback R0 maps for Great Britain (White Rose eTheses 31356; not catalogued).
- **Round 2 full-text status:** reached for `pietzsch2023nonparametric`, `schneider2016spatially`, `bone2006fuzzy` (thesis), and rule-level open material for `engler2012migclim` (user guide) and `nobis2014kissmig` (source). Still blocked: `fahse2011simulation`, `kefi2007local`/`kefi2007spatial` originals, Nobis/Engler journal PDFs (Wiley), `nehrbass2007simulation` companion paper.
- **Full-text priorities (after round 2):** Fahse & Heurich 2011, Kéfi TPB 2007 original, Prasad 2010 (USFS PDF), Kautz 2011, Doležal 2016 (OA at EJE), TreeMig documentation PDF, Zeng (Iowa) dissertation, Duračiová 2020 TANABBO code availability (ask authors).
- **Overlaps with other domains:**
  - Pine-wilt and pest CA (Huang 2012, Liu & Zhang 2022 CA–Markov) belong to `epi`.
  - LANDIS fire, Kéfi grazing and Balzter STMC touch `fire` and `lu`.
  - Kramer-Schadt lynx links to EPI-02 wild boar spread (connectivity).

## Round 2 changes

| Key | Old score / class | New score / class | Reason |
|---|---|---|---|
| pietzsch2023nonparametric | 8 B | 10 A | Neighbour rule read in paper + `Upscaling.R` (Moore); per-cell F1 validation (S1 1→2, S5 1→2) |
| schneider2016spatially | 7 B | 9 A | OA full text: complete rule, all parameters, boundaries, update; authors' GitHub code (S1, S2 1→2) |
| kefi2007local | 6 C | 7 B | Rule and base parameters restated in schneider2016 full text (S1 1→2); original still unread |
| engler2012migclim | 7 B | 8 B | Full algorithm in open package user guide (S1 1→2) |
| nobis2014kissmig | 7 B | 8 B | Full rule in open C++ source (S1 1→2) |
| bone2006fuzzy | 4 C | 4 C | Thesis full text read; rule clearer but functions only in figures, visual calibration (no change) |
| fahse2011simulation | 4 C | 4 C | No OA copy found (no change) |
| liu2025multiscale, moenickes2013shapes, nehrbass2007simulation, kefi2007spatial | — | unchanged | Re-checked; no new material (companion paper of Nehrbass verified but closed) |

## New phenomena candidates (round 2)

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| Airborne long-range spore incursion | Wind-borne transport of pathogen spores from infected regions into disease-free areas, ahead of the visible front | Explains jumps 50–100 km ahead of symptoms; couples ECO-09 with ATM-01 dispersion | Ash dieback is widespread in CZ; Czech airborne-inoculum studies exist (e.g. Dvořák et al. 2015, *Forests* 7(1), 1, DOI 10.3390/f7010001, verified in Crossref, not assessed) | `grosdidier2018tracking` (n/a, parameter source) | Probably a variant of ECO-09 + ATM-01 rather than a separate item; no CA found |

Treeline advance, seed dispersal and ash dieback were met but are already covered by ECO-07, ECO-02 and ECO-09. No verifiable CA for pollen dispersal, locusts or bird-migration stopovers was found.
