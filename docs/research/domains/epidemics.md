# Epidemics and populations — literature survey

Survey round: 1 (breadth-first), date 2026-10-12. Scoring per ../reimplementability-criteria.md.
Domain code: `epi`. BibTeX keys as in the `epi` fragment (scratchpad `bib/epi.bib`, to be merged into `/references.bib`).

**Verification note.** The first OpenAlex queries in this round worked. After that the shared
anonymous OpenAlex daily budget ran out (HTTP 429, budget exhausted until midnight UTC),
and the Semantic Scholar API was rate-limited as well. From that point on, every publication
was verified through the **Crossref** API (`api.crossref.org/works/<DOI>`), and title,
authors, year, venue, volume, pages and DOI below come from Crossref metadata. Crossref
`query.bibliographic` search is very noisy, so candidates were mostly found through web
search and earlier OpenAlex hit lists, then verified by DOI. Abstracts came from Crossref or
the Europe PMC REST API. Full texts were read through the Europe PMC full-text XML service,
PMC/arXiv (ar5iv) pages, or GitHub READMEs. ScienceDirect, Wiley, SAGE and MDPI blocked
automated access, and the PMC web front end started showing a bot check part-way through.
Entries assessed from an abstract, highlights or a secondary description are marked
*provisional*.

## Search log

Date of all searches: 2026-10-12.

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automata epidemic SIR (fulltext search) | OpenAlex | 946 | very noisy; ranked by citations |
| "cellular automata" epidemic (title+abstract) | OpenAlex | 288 | White 2007, Mikler 2005, Ahmed & Agiza 1998, Schneckenreither 2008, Sharma 2017 |
| "cellular automaton" epidemic (title+abstract) | OpenAlex | 99 | Sirakoulis 2000 (233 cites, the top CA epidemic paper) |
| "cellular automata" COVID-19 | OpenAlex | 109 | Ghosh 2020, Schimit 2021, Jithesh 2021, Davidson 2024 (geographic Cell-DEVS), Liu 2021 |
| "cellular automata" SEIR | OpenAlex | 34 | Holko 2016 (population density map), Cissé 2025 (WNV) |
| (OpenAlex budget exhausted; Semantic Scholar rate-limited) | — | — | switched to Crossref + web search |
| CA dengue / mosquito / West Nile / tick / ASF / rabies / FMD / plant disease / crop pest / range expansion | Crossref `query.bibliographic` | 0.9–5 M each (unranked) | almost all noise. Useful hits: Cissé 2024 (WNV), Ward 2009 (FMD), "Modelling the spatial diffusion of past populations" (SocArXiv) |
| cellular automata African swine fever wild boar | web | 9 | WiBISS (Italy) is the only explicit CA. Others (Croft 2020, Danish ABM, ANSES) are IBM/ABM |
| cellular automata dengue Aedes GIS | web | 10 | DengueME, Enduri & Jolad, a mosquito-borne CA review (not found in Crossref) |
| cellular automaton plant disease crop | web | 9 | Martins 2000 (CVC), Kleczkowski 1997 |
| cellular automata rabies fox raccoon | web | 9 | Benyoussef 1999, Smith 2002, Jeltsch (Eco. Model. 1999) |
| PoPS Pest or Pathogen Spread GRASS | web | 10 | r.pops.spread, PoPS Core, Jones 2021 |
| cellular automata Xylella Apulia | web | 9 | White 2017 (grid model, code on GitHub/Zenodo) |
| cellular automata tick Ixodes landscape | web | 9 | Li 2012 (Belgium), Madhav 2004 |
| CA human population dispersal Neolithic | web | 9 | dispeRse R package, Fort 2012, Souza 2021, Bradshaw 2021/2023, Hewitt 2025 |
| African swine fever Czech Republic Zlín model | web | 9 | EFSA white-zone IBM (Lange 2021), calibrated on CZ 2017 among others |
| title look-ups for ~40 candidate papers | Crossref | — | DOI verification; see entries |
| abstracts / PMC IDs for ~35 DOIs | Europe PMC REST | — | abstracts where Crossref had none |
| code: GitHub search API ("Geography-Based SEIRDS", "Sahul cellular automaton", "DISPERSCA") | GitHub | — | repos verified with HTTP 200 |

## Model families

1. **Population-fraction SIR/SEIR CA on a lattice.** Each cell holds the S/I/R fractions of a local
   population, and infection passes to neighbours weighted by population ratio and connectivity. This
   is the classic template for EPI-01 (`sirakoulis2000cellular`, `white2007modeling`,
   `mikler2005modeling`). White 2007 has a complete, closed-form rule.
2. **Geographic / irregular-cell epidemic CA.** Cells are administrative regions or density-map
   pixels, with local plus long-range (gravity or commuting) coupling: `zhong2009simulation`,
   `holko2016epidemiological`, `liu2021simulation`, `davidson2024methodological` (open Cell-DEVS code,
   Ontario regions), and `smith2002predicting` (townships as cells, river barriers).
3. **Individual-level probabilistic CA (one person per cell)** with contact radius and long-range
   contacts, fitted to national COVID-19 curves: `schimit2021model`, `jithesh2021model`. Spatially
   explicit but not geographic.
4. **Host–vector CA (mosquito, tick, triatomine).** Two coupled layers, humans/birds and vectors,
   with seasonality from surveillance data: `enduri2018dynamics`, `ortigoza2020modelling` (GIS
   triangular mesh), `cisse2024modeling`/`cisse2025exploring` (West Nile, Ontario), and the
   `delima2016dengueme` framework. Ticks: `madhav2004dispersal` (range expansion),
   `li2012consequences` (land-cover-driven Lyme risk, Belgium).
5. **Wildlife and livestock disease on landscape grids.** FMD (`doran2005simulating`,
   `ward2009modelling`), rabies (`benyoussef1999lattice`, `smith2002predicting`), and African swine
   fever. Wild-boar group-cell IBMs (`lange2017elucidating`, `lange2021modelling`) and a polygon IBM
   (`croft2020modelling`) are CA-like rather than pure CA. `ibanezporras2025wibiss` is an explicit
   but very simple CA. `hayes2021mechanistic` is the ASF review entry point.
6. **Plant disease and pest spread.** Plant-level lattices (`kleczkowski1997scaling`,
   `martins2000cellular`) and landscape host-raster models with dispersal kernels and weather
   (`meentemeyer2011epidemiological` → PoPS `jones2021iteratively`; `white2017modelling` for
   Xylella in Apulia). The landscape models are effectively stochastic CA with long-range kernels,
   and the most reusable ones have open code.
7. **Population dispersal and range expansion (demic diffusion).** Logistic or Ricker growth per
   cell, density-dependent emigration to neighbours, carrying capacity from NPP or biome maps,
   corridors and barriers: `fort2012modelling`, `gregoriodesouza2021reassessing`,
   `bradshaw2021stochastic`, `bradshaw2023directionally`. `hewitt2025modelling` covers CA-style
   mobility walks.

Reviews: `wang2022simulation` (COVID-19 spatio-temporal models, including CA) and
`hayes2021mechanistic` (ASF).

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| sirakoulis2000cellular | 2000 | CA: population movement and vaccination | generic epidemic | square lattice / local + moving fractions / S-I-immune / stoch. | 1 0 0 2 1 | 4 | C | no | paywall | secondary description (provisional) |
| mikler2005modeling | 2005 | Global stochastic CA (GSCA) | generic SIR with GIS gravity | cells with population / global gravity interaction / SIR / stoch. | 1 0 0 1 1 | 3 | D | no | paywall | abstract (provisional) |
| white2007modeling | 2007 | Modeling epidemics using CA | generic SIR + vaccination | 50×50 / von Neumann or Moore / S,I,R fractions (0.01 steps) / det. | 2 2 0 2 2 | 8 | B | no | OA (PMC) | full text |
| zhong2009simulation | 2009 | Spread in a geographical environment | SARS-type epidemic, Beijing (likely) | geo-entity (region) cells / spatial weighting local + global / SIR subclasses / det. | 1 1 1 1 1 | 5 | C | third-party (Cadmium) | OA (PMC, scanned) | abstract (provisional) |
| holko2016epidemiological | 2016 | Population-density-map CA | SEIR on real density map (Poland) | density raster / local + mobility / SEIR-IBM / stoch. | 1 1 0 1 1 | 4 | C | no | paywall | highlights (provisional) |
| schimit2021model | 2021 | PCA: social isolation, Brazil | COVID-19 | 14 500² lattice (1 person/cell) / Moore radius 8, 32 contacts / 8 states / stoch. | 2 1 0 2 2 | 7 | B | no | OA (PMC) | full text |
| jithesh2021model | 2021 | PCA: lockdown, migration, vaccination | COVID-19 cluster | lattice / custom transmittable neighbourhoods / SEIR-type / stoch. | 1 1 0 1 1 | 4 | C | no | OA (PMC) | abstract (provisional) |
| liu2021simulation | 2021 | SEIR + SD + CA, China | COVID-19 and regional economy | geographic grid of China / migration-weighted / SEIR / det. | 1 1 0 1 1 | 4 | C | no | OA | abstract (provisional) |
| davidson2024methodological | 2024 | Geographic Cell-DEVS disease models | COVID-19, Ontario regions | irregular regions (PHUs, DAs) / shared-border + correlation weights / SEIRDS(+V) / det. | 1 1 2 2 1 | 7 | B | GitHub | OA (CC BY-NC) | abstract + repo docs (provisional) |
| wang2022simulation | 2022 | Review: spatio-temporal COVID-19 models | review | — | n/a | n/a | n/a | — | OA | abstract |
| enduri2018dynamics | 2018 | Dengue with human and vector mobility | dengue, Ahmedabad | 500×500 (10 m cells) two overlapping lattices / diffusion + exponential steps / SEIR + SEI / stoch. | 1 2 0 1 1 | 5 | C | no | preprint (arXiv) | full text (preprint) |
| delima2016dengueme | 2016 | DengueME framework | dengue + Aedes, urban | TerraME cellular spaces + agents (framework) | n/a | n/a | n/a | GitHub (BSD-2) | OA | full text |
| ortigoza2020modelling | 2020 | Chikungunya on triangular CA | chikungunya, Réunion | GIS triangular mesh / 3-neighbour / SEIR + sei counts / stoch. | 2 2 1 1 1 | 7 | B | not public (C++) | OA (PMC) | full text |
| cisse2024modeling | 2024 | West Nile CA, birds and humans | WNV, eastern Ontario | 45×45 (2×2 km) / Moore, inverse-distance weights / SEIRDS birds+humans, SEI mosquitoes / det. | 2 1 1 1 1 | 6 | C | not shared (MATLAB) | OA (PMC) | full text |
| cisse2025exploring | 2025 | WNV reintroduction scenarios | WNV, Canada | as cisse2024 | 1 1 0 1 1 | 4 | C | no | paywall | abstract (provisional) |
| madhav2004dispersal | 2004 | Tick range expansion CA | Ixodes scapularis spread via hosts | simple landscape grid / host-mediated dispersal / tick stages / det. | 1 1 0 2 1 | 5 | C | no | paywall | abstract (provisional) |
| li2012consequences | 2012 | Landscape fragmentation and Lyme risk | Lyme / I. ricinus, Belgium | 50×50 (1 ha), torus / host movement ranges / tick stages × infection + hosts / det. | 2 2 0 2 2 | 8 | B | no (Repast) | OA (PLoS ONE) | full text |
| benyoussef1999lattice | 1999 | Lattice models of fox rabies | rabies in foxes | 1D CML + 2D automata network / short-range + rabid diffusion / S, incubating, rabid / stoch. | 1 0 0 2 1 | 4 | C | no | preprint (arXiv) | abstract (provisional) |
| smith2002predicting | 2002 | Rabies on heterogeneous landscapes | raccoon rabies, Connecticut | 169 townships / shared border / infected yes/no / stoch. (Gillespie) | 2 2 1 1 2 | 8 | B | dead link | OA (PMC) | full text |
| doran2005simulating | 2005 | FMD in feral pigs and livestock | FMD, Queensland | raster CA / local / SIR / stoch. | 1 1 0 1 1 | 4 | C | no | paywall | abstract (provisional) |
| ward2009modelling | 2009 | FMD in deer and feral pigs | FMD, southern Texas | geographic automata on animal distributions / local / SLIR / stoch. | 1 1 0 1 1 | 4 | C | no | paywall | abstract (provisional) |
| lange2017elucidating | 2017 | ASF carcass transmission IBM | ASF in wild boar | 3×3 km group cells / neighbouring groups + carcasses / IBM states / stoch. | 1 1 0 1 1 | 4 | C | not found (ODD only) | paywall | secondary descriptions (provisional) |
| lange2021modelling | 2021 | ASF white-zone management (EFSA) | ASF in wild boar, EE/LV/CZ/FR | spatially explicit IBM on habitat cells | 1 1 0 1 1 | 4 | C | no | OA (EFSA) | search-engine abstract (provisional) |
| croft2020modelling | 2020 | ASF in an isolated boar population | ASF, Forest of Dean (UK) | irregular habitat polygons (~3.9 km²) / group overlap / IBM / stoch. | 1 2 2 1 1 | 7 | B | supplementary (Python 2) | OA (PMC) | full text (partial) |
| ibanezporras2025wibiss | 2025 | WiBISS ASF vaccination CA | ASF vaccination, N. Italy | outbreak points + municipalities / radius (haversine) or shared border / 3 states / stoch. | 1 2 0 1 1 | 5 | C | no | OA (PMC) | full text |
| hayes2021mechanistic | 2021 | Review: mechanistic ASF models | review | — | n/a | n/a | n/a | — | paywall | abstract |
| kleczkowski1997scaling | 1997 | Plant–pathogen scaling | soil-borne plant disease | plant lattice / contact process / S-I / stoch. | 1 1 0 1 1 | 4 | C | no | paywall (archive) | secondary description (provisional) |
| martins2000cellular | 2000 | CA for citrus variegated chlorosis | CVC in orange groves, São Paulo | L=200 lattice, null boundary / Lévy-flight vectors / 2 binary vars / stoch. | 2 2 0 1 2 | 7 | B | no | preprint (arXiv) | full text (preprint) |
| meentemeyer2011epidemiological | 2011 | Sudden oak death, California | Phytophthora ramorum | 250 m host raster, weekly / dispersal kernel / S-I host units / stoch. | 1 1 2 1 1 | 6 | C | r.spread.sod → PoPS | OA (Ecosphere) | secondary descriptions (provisional) |
| white2017modelling | 2017 | Xylella spread and control, Apulia | X. fastidiosa in olives | 1 km² cells, annual / exp. kernel + long-distance jumps / infected fraction / stoch. | 2 1 2 1 2 | 8 | B | GitHub + Zenodo (MIT) | OA (PMC) | full text |
| jones2021iteratively | 2021 | PoPS forecasting platform | pests and pathogens (SLF, SOD) | host raster / kernels + weather / S-I hosts / stoch. | 1 2 2 1 2 | 8 | B | GitHub (PoPS Core, rpops, r.pops.spread) | OA (PMC) | full text |
| fort2012modelling | 2012 | Neolithic transition model | demic diffusion, Near East–Europe | grid / dispersal + sea travel / population / det. | 1 1 0 1 1 | 4 | C | reimpl. in dispeRse | paywall | abstract (provisional) |
| bradshaw2021stochastic | 2021 | Stochastic peopling of Sahul | human colonisation, Sahul | 0.5° grid (86×87) / adjacent emigration + long-distance / abundance (Ricker) / stoch. | 2 2 2 2 2 | 10 | A | GitHub (GPL-3) | OA (PMC) | full text |
| bradshaw2023directionally | 2023 | Directionally supervised Sahul CA | human colonisation, Sahul | as bradshaw2021 + superhighway weights | 1 1 2 2 1 | 7 | B | GitHub + Zenodo | preprint (OSF) | abstract + repo (provisional) |
| gregoriodesouza2021reassessing | 2021 | Tupi expansion CA | farmer expansion, S. America | biome raster / density-dependent emigration / population / stoch. | 2 2 2 1 2 | 9 | A | Zenodo (Python + R) | OA (PMC) | full text |
| hewitt2025modelling | 2025 | DISPERSCA hunter-gatherer mobility | mobility walks, central Iberia | slope raster / square or hex decision neighbourhood / walker position | 1 1 1 2 1 | 6 | C | figshare link (not fully verified) | OA (PMC) | full text (partial) |

Class counts (scored entries): A 2, B 11, C 19, D 1; n/a 3 (36 entries total).

## Entries

### sirakoulis2000cellular — A cellular automaton model for the effects of population movement and vaccination on epidemic propagation
- **Citation:** Sirakoulis, G.Ch., Karafyllidis, I., Thanailakis, A. (2000). A cellular automaton model for the effects of population movement and vaccination on epidemic propagation. *Ecological Modelling* 133(3), 209–223. DOI: 10.1016/s0304-3800(00)00294-5 (verified: Crossref; also OpenAlex hit list)
- **Access:** paywall
- **Phenomenon and study area:** generic epidemic spread on a synthetic lattice, with population movement and vaccination.
- **Model:** each cell is a segment of the population in one of three conditions (susceptible, infected, immune). Infection spreads locally, and parts of the population move randomly across the lattice to carry it further. Vaccination converts susceptibles to immune.
- **Inputs:** synthetic lattice only.
- **Parameters:** unknown (no abstract or full text available).
- **Code:** not found.
- **Validation:** qualitative (from secondary description).
- **Reimplementability:** S1 1 – concept clear, rule not seen; S2 0 – values unknown; S3 0; S4 2 – no data needed; S5 1 → 4, C. Assessed from: secondary description in a citing paper (provisional). Crossref and Semantic Scholar have no abstract (publisher elided).
- **Browser fit:** trivially feasible.
- **Relevance to ca-geo:** EPI-01. The most-cited CA epidemic paper (about 200 Crossref citations). Its movement and vaccination ideas are covered with full equations in `white2007modeling`.

### mikler2005modeling — Modeling infectious diseases using global stochastic cellular automata
- **Citation:** Mikler, A.R., Venkatachalam, S., Abbas, K. (2005). Modeling infectious diseases using global stochastic cellular automata. *Journal of Biological Systems* 13(04), 421–439. DOI: 10.1142/s0218339005001604 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** generic SIR spread with heterogeneous population, framed for GIS use.
- **Model:** a "global stochastic CA" in which any two cells can interact. Interaction strength depends on population density and Euclidean distance, following a GIS gravity model, and can include geographic, demographic and migration constraints. The authors show it behaves like classic SIR when homogeneous.
- **Inputs:** population per cell (described, not specified).
- **Parameters:** not given in the abstract.
- **Code:** not found.
- **Validation:** comparison with SIR curves.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 1; S5 1 → 3, D. Assessed from: abstract (provisional).
- **Browser fit:** all-pairs gravity coupling is O(n²). It needs a distance cut-off or a coarse grid.
- **Relevance to ca-geo:** EPI-01. A gravity-model long-range coupling term that could be added to a population raster.

### white2007modeling — Modeling epidemics using cellular automata
- **Citation:** White, S.H., Martín del Rey, A., Rodríguez Sánchez, G. (2007). Modeling epidemics using cellular automata. *Applied Mathematics and Computation* 186(1), 193–202. DOI: 10.1016/j.amc.2006.06.126 (verified: Crossref; OpenAlex)
- **Access:** OA (PMC7127728, Elsevier COVID-19 collection)
- **Phenomenon and study area:** theoretical SIR epidemic with vaccination, synthetic 50×50 grid.
- **Model:** each cell is a patch of land with constant population N and S/I/R fractions summing to 1, discretised to 0.01. Neighbourhood is von Neumann or Moore, and boundaries are null (absorbing). New infections in a cell come from within-cell contact (virulence × S × I) plus inflow from neighbours. The inflow is weighted by the population ratio, a connection factor (1 / 0.6 / 0.3 / 0 for three, two, one or no transport modes) and a movement factor. A fixed fraction ε of the infected recover each step. Vaccination moves a fraction ω of the susceptibles to R. Synchronous update, abstract time step.
- **Inputs:** synthetic population and connection layouts (uniform, east–west gradient, four quadrants).
- **Parameters:** all given: v=0.6, ε=0.4, m=0.5, c per scenario, ω ∈ {0, 0.2, 0.3, 0.4}. The authors call the values arbitrary.
- **Code:** not found.
- **Validation:** none against data. Outbreak-threshold table (minimum initial infected fraction for spread) plus figures of fronts and SIR curves.
- **Reimplementability:** S1 2 – full equations, neighbourhood, boundary, discretisation; S2 2 – all values; S3 0; S4 2 – synthetic, but it maps directly to a population raster plus a connectivity layer; S5 2 – the threshold table and infection-curve peak times (t=44 von Neumann, t=27 Moore) are checkable → 8, B. Assessed from: full text.
- **Browser fit:** excellent. Pure local arithmetic, and it scales to national rasters.
- **Relevance to ca-geo:** EPI-01 core template. Replace N_ij with a population grid (e.g. GEOSTAT 1 km), c with road or rail connectivity, and add long-range commuting.

### zhong2009simulation — Simulation of the spread of infectious diseases in a geographical environment
- **Citation:** Zhong, S., Huang, Q., Song, D. (2009). Simulation of the spread of infectious diseases in a geographical environment. *Science in China Series D: Earth Sciences* 52(4), 550–561. DOI: 10.1007/s11430-009-0044-9 (verified: Crossref)
- **Access:** OA (PMC7088542, scanned PDF; text extraction only gave the abstract)
- **Phenomenon and study area:** generic infectious disease in real geographic regions. The references point to SARS in Beijing.
- **Model:** geo-entity CA in which real geographic regions are the cells. Each region's population is split into S/I/R with subclasses. Transition formulas move people between subclasses. Spatial weighting functions give both local (neighbouring) and global (transport-induced) contagion.
- **Inputs:** regional population and boundaries (from abstract).
- **Parameters:** not visible.
- **Code:** no author code. An open third-party implementation and extension (SIRDS, then SEIRDS) is in the Cadmium Cell-DEVS models: https://github.com/SimulationEverywhere-Models/Geography-Based-SEIRDS (verified 200). Its README cites the Zhong model as the basis.
- **Validation:** qualitative consistency claimed.
- **Reimplementability:** S1 1; S2 1; S3 1 – third-party code only; S4 1; S5 1 → 5, C. Assessed from: abstract (provisional).
- **Browser fit:** good, since the cells are polygons (municipalities/districts) with an adjacency graph.
- **Relevance to ca-geo:** EPI-01 on CZ municipalities/ORP districts. This is the ancestor of `davidson2024methodological`.

### holko2016epidemiological — Epidemiological modeling with a population density map-based cellular automata simulation system
- **Citation:** Holko, A., Mędrek, M., Pastuszak, Z., Phusavat, K. (2016). Epidemiological modeling with a population density map-based cellular automata simulation system. *Expert Systems with Applications* 48, 1–8. DOI: 10.1016/j.eswa.2015.08.018 (verified: Crossref; OpenAlex)
- **Access:** paywall
- **Phenomenon and study area:** SEIR epidemic on real geographical and demographic data (Polish authors; the country is not confirmed from the highlights).
- **Model:** CA framework running an SEIR individual-based model on a population density map, with parameters for population dynamics (mobility). Individual mobility affects spread.
- **Inputs:** population density raster.
- **Parameters:** not visible.
- **Code:** not found.
- **Validation:** unknown.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: highlights via search engine (provisional). Abstract elided by publisher.
- **Browser fit:** good.
- **Relevance to ca-geo:** EPI-01. Closest EU example of a CA epidemic driven directly by a density map. Full text worth getting in round 2.

### schimit2021model — A model based on cellular automata to estimate the social isolation impact on COVID-19 spreading in Brazil
- **Citation:** Schimit, P.H.T. (2021). A model based on cellular automata to estimate the social isolation impact on COVID-19 spreading in Brazil. *Computer Methods and Programs in Biomedicine* 200, 105832. DOI: 10.1016/j.cmpb.2020.105832 (verified: Crossref)
- **Access:** OA (PMC7836885)
- **Phenomenon and study area:** COVID-19 in Brazil, with hospital and ICU capacity. Not spatially geographic.
- **Model:** one person per cell on a 14 500² torus. Each step a person makes C=32 random contacts within Moore radius r=8, with a layer-weighted probability. Infection probability is 1 − exp(−k·v), where v is a weighted count of infectious contacts. Eight states (S, E, asymptomatic, symptomatic, three severity levels, R) with fixed sojourn periods and branching probabilities. Synchronous update, daily step. A mean-field ODE is derived.
- **Inputs:** national population, hospital beds and ICUs, death counts.
- **Parameters:** table of about 14 values. k=0.15 was fitted by hand to the first 25 days of deaths. There are two internal inconsistencies (T_CIS1 14 vs 31 days; P_n).
- **Code:** not mentioned.
- **Validation:** fit to cumulative deaths, then scenario grid (648 isolation scenarios) with quantitative outputs.
- **Reimplementability:** S1 2; S2 1 – inconsistencies; S3 0; S4 2 – public national data; S5 2 → 7, B. Assessed from: full text.
- **Browser fit:** 2×10⁸ cells is too large. A scaled-down lattice is feasible.
- **Relevance to ca-geo:** EPI-01 (state structure and the healthcare-capacity idea). A geographic version would need a density map instead of a uniform lattice.

### jithesh2021model — A model based on cellular automata for investigating the impact of lockdown, migration and vaccination on COVID-19 dynamics
- **Citation:** Jithesh, P.K. (2021). A model based on cellular automata for investigating the impact of lockdown, migration and vaccination on COVID-19 dynamics. *Computer Methods and Programs in Biomedicine* 211, 106402. DOI: 10.1016/j.cmpb.2021.106402 (verified: Crossref)
- **Access:** OA (PMC8423711)
- **Phenomenon and study area:** COVID-19 within a cluster (synthetic lattice).
- **Model:** probabilistic CA starting from S and E cells. Custom "transmittable" and "transition" neighbourhoods select the most likely contacts of each infected host. Lockdown, migration and vaccination are added as scenarios.
- **Inputs:** none geographic.
- **Parameters:** latent and recovery periods, range, lattice size (values not seen).
- **Code:** not mentioned.
- **Validation:** visual match to actual data.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** good.
- **Relevance to ca-geo:** EPI-01. Minor. Ideas for intervention toggles.

### liu2021simulation — Simulation of spatiotemporal relationship between COVID-19 propagation and regional economic development in China
- **Citation:** Liu, D., Zheng, X., Zhang, L. (2021). Simulation of Spatiotemporal Relationship between COVID-19 Propagation and Regional Economic Development in China. *Land* 10(6), 599. DOI: 10.3390/land10060599 (verified: Crossref)
- **Access:** OA (CC BY). The MDPI page blocked automated reading.
- **Phenomenon and study area:** COVID-19 spread across China, with migration from Hubei.
- **Model:** SEIR coupled with system dynamics and a CA ("SDPM"). Spread depends on regional development and short-range migration, and isolation measures are scenarios.
- **Inputs:** regional economy and migration data (from abstract).
- **Parameters:** not visible.
- **Code:** not found.
- **Validation:** comparison with reported spread (details unknown).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Browser fit:** probably fine (national grid).
- **Relevance to ca-geo:** EPI-01. Example of covariate-weighted (economy) transmission on a national grid.

### davidson2024methodological — A methodological approach for modeling the spread of disease using geographical discrete-event spatial models
- **Citation:** Davidson, G., Fahlman, A., Mereu, E., Ruiz Martin, C., Wainer, G., Dobias, P., Rempel, M. (2024). A methodological approach for modeling the spread of disease using geographical discrete-event spatial models. *SIMULATION* 100(1), 39–70. DOI: 10.1177/00375497231152458 (verified: Crossref)
- **Access:** OA (CC BY-NC 4.0). SAGE blocked automated reading.
- **Phenomenon and study area:** COVID-19 across Ontario public-health units and Ottawa dissemination areas.
- **Model:** geography-based Cell-DEVS. Cells are irregular regions read from GIS and coupled to adjacent regions, with population-weighted correlation. Compartments are SEIRDS, with variants for asymptomatic cases, movement restriction or non-compliance, and vaccination stages with waning immunity. Scenarios are generated from geodata as JSON.
- **Inputs:** region polygons, population. Public data repos: https://github.com/glenndavidson0/Ontario-PHU-COVID19-Data (verified 200).
- **Parameters:** in the repo config/default.json and manual (not inspected in detail).
- **Code:** https://github.com/SimulationEverywhere-Models/Geography-Based-SEIRDS and …/Geography-Based-SEIRDS-Vaccinated (both verified 200; C++17 + Cadmium, Python scenario generator, web GIS viewer).
- **Validation:** comparison with Ontario case data (details not read).
- **Reimplementability:** S1 1 – abstract only, but the repo includes a model document; S2 1; S3 2; S4 2; S5 1 → 7, B. Assessed from: abstract + repository README (provisional). Full text should push S1/S2 up.
- **Browser fit:** very good. Polygon CA with an adjacency list, and the authors already ship a web GIS viewer.
- **Relevance to ca-geo:** EPI-01 strongest candidate for "SIR over municipalities". Their GeoJSON → cell-space pipeline is a direct template for CZ obce/ORP from ČSÚ data.

### wang2022simulation — Simulation and forecasting models of COVID-19 taking into account spatio-temporal dynamic characteristics: A review
- **Citation:** Wang, P., Zheng, X., Liu, H. (2022). Simulation and forecasting models of COVID-19 taking into account spatio-temporal dynamic characteristics: A review. *Frontiers in Public Health* 10, 1033432. DOI: 10.3389/fpubh.2022.1033432 (verified: Crossref)
- **Access:** OA (PMC9623320)
- **Value as entry point:** classifies COVID-19 spatio-temporal models into macro (compartmental, metapopulation) and micro (CA, ABM) and summarises the data used. A good source of further geographic CA COVID papers for round 2.
- **Reimplementability:** n/a.

### enduri2018dynamics — Dynamics of dengue disease with human and vector mobility
- **Citation:** Enduri, M.K., Jolad, S. (2018). Dynamics of dengue disease with human and vector mobility. *Spatial and Spatio-temporal Epidemiology* 25, 57–66. DOI: 10.1016/j.sste.2018.03.001 (verified: Crossref). Preprint: arXiv 1409.0965.
- **Access:** paywall. Preprint read via ar5iv.
- **Phenomenon and study area:** dengue (single serotype), with Ahmedabad (India) mosquito density as a seasonal driver.
- **Model:** stochastic CA with two overlapping lattices. The human lattice holds several agents per cell (S/E/I/R). In the vector lattice, Poisson-distributed mosquitoes per cell (S/E/I) follow monthly density data. Vectors diffuse, humans take exponentially distributed steps. Transition probabilities come from field studies. Runs on 500×500 (10 m cells, about 25 km²) and 100×100 lattices. A reaction–diffusion PDE version is also given.
- **Inputs:** monthly mosquito density and dengue cases 2006–2012 (municipal corporation, not open).
- **Parameters:** Table 2 lists the CA parameters.
- **Code:** not found.
- **Validation:** visual comparison with Ahmedabad cases. Box plots of final size vs mobility.
- **Reimplementability:** S1 1 – rules described but some details only verbal; S2 2; S3 0; S4 1; S5 1 → 5, C. Assessed from: full text (preprint).
- **Browser fit:** fine at 100×100 to 500×500.
- **Relevance to ca-geo:** template for host–vector two-layer CA (relevant to EPI-03 as a structure).

### delima2016dengueme — DengueME: A tool for the modeling and simulation of dengue spatiotemporal dynamics
- **Citation:** De Lima, T., Lana, R., De Senna Carneiro, T., Codeço, C., Machado, G., Ferreira, L., De Castro Medeiros, L., Davis Junior, C. (2016). DengueME: A Tool for the Modeling and Simulation of Dengue Spatiotemporal Dynamics. *International Journal of Environmental Research and Public Health* 13(9), 920. DOI: 10.3390/ijerph13090920 (verified: Crossref)
- **Access:** OA (PMC5036753)
- **Value as entry point:** open platform on TerraME (Lua cellular spaces) with a model library for Aedes population dynamics, human mobility and dengue transmission, integrated with a GIS database. It includes adapted models of Medeiros et al. 2011 and Lana et al. Code: https://github.com/ufopleds/DengueME (verified 200, BSD-2-Clause; last push 2018).
- **Reimplementability:** n/a (framework). The individual library models would need separate scoring in round 2.
- **Relevance to ca-geo:** reference implementation for vector-borne CA rules. Shows how a GIS-coupled CA platform is organised.

### ortigoza2020modelling — Modelling and simulating Chikungunya spread with an unstructured triangular cellular automata
- **Citation:** Ortigoza, G., Brauer, F., Neri, I. (2020). Modelling and simulating Chikungunya spread with an unstructured triangular cellular automata. *Infectious Disease Modelling* 5, 197–220. DOI: 10.1016/j.idm.2019.12.005 (verified: Crossref)
- **Access:** OA (PMC6993010)
- **Phenomenon and study area:** chikungunya. Test domain Réunion Island (2005–06 outbreak), mesh built from a GIS outline.
- **Model:** unstructured triangular mesh, where each triangle holds counts of humans (S,E,I,R) and vectors (s,e,i). Neighbourhood is the three edge neighbours (von Neumann analogue), with closed boundaries. Probabilistic rules: susceptibles become exposed with probability 1−(1−p)^(infected vectors in neighbourhood), and the vector side mirrors this. Vector births and deaths, extrinsic incubation, and environment-dependent rates are included. Human mobility adds global interaction.
- **Inputs:** domain polygon, human and vector density per cell (synthetic heterogeneity scenarios).
- **Parameters:** Table 1 (rates from the literature, e.g. β=0.14, βv=0.4).
- **Code:** C++ CA plus Python visualisation, not published.
- **Validation:** qualitative. Peak size and timing tables across heterogeneity scenarios.
- **Reimplementability:** S1 2; S2 2; S3 1; S4 1; S5 1 → 7, B. Assessed from: full text (extracted paragraphs).
- **Browser fit:** good. Triangular meshes are fine, and a raster version is simpler.
- **Relevance to ca-geo:** host–vector rule set ready to port to a raster. Shows CA on irregular GIS meshes.

### cisse2024modeling — Modeling West Nile virus transmission in birds and humans: advantages of using a cellular automata approach
- **Citation:** Cissé, B., Lapen, D.R., Chalvet-Monfray, K., Ogden, N.H., Ludwig, A. (2024). Modeling West Nile Virus transmission in birds and humans: Advantages of using a cellular automata approach. *Infectious Disease Modelling* 9(1), 278–297. DOI: 10.1016/j.idm.2024.01.002 (verified: Crossref)
- **Access:** OA (PMC10847944)
- **Phenomenon and study area:** West Nile virus, 45×45 cells (2×2 km) in eastern Ontario.
- **Model:** deterministic CA with per-cell SEIRDS compartments for birds and humans and SEI for mosquitoes (equations 1–13). Moore neighbourhood with inverse-distance weights. Only birds move between cells (dispersal probability, time fraction τ=0.4). Seasonal phases by day of year, daily rates, 10-year runs.
- **Inputs:** eBird robin observations (habitat suitability, five entry cells), Breeding Bird Survey indices, Public Health Ontario mosquito surveillance, StatCan demography.
- **Parameters:** Table 1, about 26 parameters with sources. Some lack numeric values.
- **Code:** MATLAB, not shared.
- **Validation:** visual and qualitative agreement with WNV-positive mosquito pools. ±5 % sensitivity analysis.
- **Reimplementability:** S1 2; S2 1; S3 1; S4 1 – eBird is public, surveillance data are not; S5 1 → 6, C. Assessed from: full text.
- **Browser fit:** good (2 000 cells).
- **Relevance to ca-geo:** template for vector-borne disease with migratory hosts. WNV is present in southern CZ, which makes it a possible EPI extension.

### cisse2025exploring — Exploring factors affecting the reintroduction and amplification of West Nile virus in heterogeneous landscapes in Canada, using a cellular automata approach
- **Citation:** Cisse, B., Lapen, D.R., Chalvet-Monfray, K., Ogden, N.H., Ludwig, A. (2025). Exploring factors affecting the reintroduction and amplification of West Nile virus in heterogeneous landscapes in Canada, using a cellular automata approach. *Journal of Medical Entomology* 62(5), 1101–1115. DOI: 10.1093/jme/tjaf068 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** WNV scenarios (infected migrant birds, overwintering mosquitoes, bird abundance, feeding shift), Canada.
- **Model:** same SEIR CA as `cisse2024modeling`, used for scenario experiments.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** scenario ideas only.

### madhav2004dispersal — A dispersal model for the range expansion of blacklegged tick (Acari: Ixodidae)
- **Citation:** Madhav, N.K., Brownstein, J.S., Tsao, J.I., Fish, D. (2004). A Dispersal Model for the Range Expansion of Blacklegged Tick (Acari: Ixodidae). *Journal of Medical Entomology* 41(5), 842–852. DOI: 10.1603/0022-2585-41.5.842 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** range expansion of *Ixodes scapularis* across a simple synthetic landscape.
- **Model:** deterministic, spatially explicit CA. Host contribution to tick dispersal is a function of tick burden, home range and density for deer, mice and robins.
- **Parameters:** from published and unpublished data (values not seen).
- **Code:** not found.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 2 – synthetic landscape; S5 1 → 5, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** EPI-03 (tick spread rather than static suitability), and links to ECO-07 range shift.

### li2012consequences — Consequences of landscape fragmentation on Lyme disease risk: a cellular automata approach
- **Citation:** Li, S., Hartemink, N., Speybroeck, N., Vanwambeke, S.O. (2012). Consequences of Landscape Fragmentation on Lyme Disease Risk: A Cellular Automata Approach. *PLoS ONE* 7(6), e39612. DOI: 10.1371/journal.pone.0039612 (verified: Crossref)
- **Access:** OA
- **Phenomenon and study area:** *Ixodes ricinus* / *B. burgdorferi* risk in southern Belgium (EU) and in 160 artificial fragmentation landscapes.
- **Model:** 50×50 grid of 1 ha cells on a torus, weekly step, 30 years. Three layers: ticks (larva, nymph, adult; questing/feeding; infected), hosts (reservoir rodents, reproduction hosts such as deer) and land cover (woodland, grassland, non-vegetated). Each week, in order: development and survival (grassland survival × 0.93), attachment proportional to host density, SI-type transmission (efficiencies 0.6 / 0.9, transovarial 0.01), then host movement (rodents ≤1 cell, deer ≤5 cells, 35 % of time in grassland) carrying feeding ticks. Fixed W→E, S→N scan with simultaneous write-back. Formulae in Appendix S1, movement in S2.
- **Inputs:** land-cover map (Belgian sites, not open). Artificial maps (woodland 20–80 %, block sizes 1–10 cells) are reproducible.
- **Parameters:** Table 1 with 24 parameters and literature sources. Host densities come from Belgian data.
- **Code:** Repast Simphony (Java), not shared.
- **Validation:** against field data. Nymph infection prevalence simulated 22.5 % vs observed 22.3 %, adult/nymph ratio 0.11 vs 0.10. Fails at 10×10 block level. Log sensitivity indices.
- **Reimplementability:** S1 2; S2 2; S3 0; S4 2 – runs on any land-cover raster; S5 2 → 8, B. Assessed from: full text.
- **Browser fit:** good (2 500 cells × several layers, 1 560 steps).
- **Relevance to ca-geo:** **EPI-03 best fit**. Rules are driven by CORINE/land-cover classes, with tick-borne encephalitis/Lyme as the CZ narrative. It turns the "suitability only" item into a real dynamic CA.

### benyoussef1999lattice — Lattice three-species models of the spatial spread of rabies among foxes
- **Citation:** Benyoussef, A., Boccara, N., Chakib, H., Ez-Zahraouy, H. (1999). Lattice three-species models of the spatial spread of rabies among foxes. *International Journal of Modern Physics C* 10(06), 1025–1038. DOI: 10.1142/s0129183199000826 (verified: Crossref)
- **Access:** preprint (arXiv adap-org/9904005)
- **Phenomenon and study area:** fox rabies, abstract lattice.
- **Model:** a 1D coupled-map lattice and a 2D automata network with susceptible, incubating and rabid foxes. Susceptible and incubating foxes are territorial, while rabid ones diffuse out of their territory. Front speed depends on carrying capacity and the diffusion of rabid foxes, and below a threshold the disease dies out.
- **Reimplementability:** S1 1; S2 0; S3 0; S4 2; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** wildlife-disease front with a carrying-capacity raster. Rabies is historically relevant to CZ (oral vaccination campaigns).

### smith2002predicting — Predicting the spatial dynamics of rabies epidemics on heterogeneous landscapes
- **Citation:** Smith, D.L., Lucey, B., Waller, L.A., Childs, J.E., Real, L.A. (2002). Predicting the spatial dynamics of rabies epidemics on heterogeneous landscapes. *Proceedings of the National Academy of Sciences* 99(6), 3668–3672. DOI: 10.1073/pnas.042400799 (verified: Crossref)
- **Access:** OA (PMC122581)
- **Phenomenon and study area:** raccoon rabies across the 169 townships of Connecticut, 1991 onward.
- **Model:** cells are townships, with adjacency defined as sharing a border point. Each uninfected township has hazard μ (long-distance translocation) plus the sum of λ_ij over infected neighbours. Waiting times are exponential, and the next township is chosen proportionally (Gillespie). Five variants make λ depend on human density and/or a river crossing.
- **Inputs:** township polygons, monthly first-case dates, log human density, major rivers.
- **Parameters:** Table 1 for all variants, e.g. River model α=0.66, β=0.09 (about 7-fold reduction across rivers), μ=2×10⁻⁴. Fitted by stochastic optimisation of χ² over 5 000 simulations.
- **Code:** stated URL (medschool.umaryland.edu/…/dsmith/rabies.html) returns 404.
- **Validation:** χ² goodness of fit and residual analysis. Rivers improve fit by about 10 %.
- **Reimplementability:** S1 2; S2 2; S3 1 – dead link; S4 1 – arrival dates are only in the paper's figures; S5 2 → 8, B. Assessed from: full text.
- **Browser fit:** excellent (169 polygons).
- **Relevance to ca-geo:** EPI-02 analogue. Polygon-CA with barrier-modified rates is exactly the "rivers/fences/motorways as semipermeable barriers" demo. Connects to ECO-04 (L13 chain).

### doran2005simulating — Simulating the spatial dynamics of foot and mouth disease outbreaks in feral pigs and livestock in Queensland, Australia, using a susceptible-infected-recovered cellular automata model
- **Citation:** Doran, R.J., Laffan, S.W. (2005). Simulating the spatial dynamics of foot and mouth disease outbreaks in feral pigs and livestock in Queensland, Australia, using a susceptible-infected-recovered cellular automata model. *Preventive Veterinary Medicine* 70(1–2), 133–152. DOI: 10.1016/j.prevetmed.2005.03.002 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** FMD in feral pigs and unfenced livestock, two Queensland regions.
- **Model:** SIR CA on animal-distribution rasters, with sensitivity analysis of the infectious-state durations. Scenarios cover pigs only vs pigs plus livestock and wet vs dry season start.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** EPI-02 analogue (livestock + wild suids, seasonality). Foundation of the "geographic automata" line continued in `ward2009modelling`.

### ward2009modelling — Modelling spread of foot-and-mouth disease in wild white-tailed deer and feral pig populations using a geographic-automata model and animal distributions
- **Citation:** Ward, M.P., Laffan, S.W., Highfield, L.D. (2009). Modelling spread of foot-and-mouth disease in wild white-tailed deer and feral pig populations using a geographic-automata model and animal distributions. *Preventive Veterinary Medicine* 91(1), 55–63. DOI: 10.1016/j.prevetmed.2009.05.005 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** FMD in deer and feral pigs, southern Texas.
- **Model:** susceptible-latent-infected-recovered geographic automaton on spatially referenced herd distributions. 100 random incursion sites × 50 runs. Outbreak size correlates with local deer numbers (r>0.95) but only moderately for patchy pigs.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** EPI-02. Shows that patchy host distribution (like wild boar) makes spread less predictable, a useful demo message.

### lange2017elucidating — Elucidating transmission parameters of African swine fever through wild boar carcasses by combining spatio-temporal notification data and agent-based modelling
- **Citation:** Lange, M., Thulke, H.-H. (2017). Elucidating transmission parameters of African swine fever through wild boar carcasses by combining spatio-temporal notification data and agent-based modelling. *Stochastic Environmental Research and Risk Assessment* 31(2), 379–391. DOI: 10.1007/s00477-016-1358-8 (verified: Crossref)
- **Access:** paywall
- **Phenomenon and study area:** ASF in wild boar, fitted to European notification data.
- **Model:** spatially explicit IBM in which wild boar groups occupy 3×3 km habitat cells, as described by `croft2020modelling`. Transmission runs within groups, between neighbouring groups, and via carcasses. Pattern-oriented fitting suggested a low per-carcass infection probability.
- **Parameters:** ASF parameters reused by later models (e.g. Table 1 of Croft 2020).
- **Code:** CoMSES lists an ODD mathematical description but no code (https://catalog.comses.net/publications/106154, verified 200).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: secondary descriptions (provisional). The paper itself was not read.
- **Browser fit:** good. A grid of boar-group cells is CA-like.
- **Relevance to ca-geo:** **EPI-02 core reference**. Group-per-cell on a habitat raster, carcass pathway, fences and culling zones. ODD should be obtained in round 2.

### lange2021modelling — Modelling wild boar management for controlling the spread of ASF in the areas called white zones (zones blanche)
- **Citation:** Lange, M., Reichold, A., Thulke, H.-H. (2021). Modelling wild boar management for controlling the spread of ASF in the areas called white zones (zones blanche). *EFSA Supporting Publications* 18(5). DOI: 10.2903/sp.efsa.2021.en-6573 (verified: Crossref)
- **Access:** OA (EFSA)
- **Phenomenon and study area:** ASF white-zone (depopulation buffer) strategies, fitted to four EU cases: Estonia 2014, Latvia 2016, **Czech Republic 2017 (Zlín)** and France 2018.
- **Model:** individual-based, spatially explicit model (family of `lange2017elucidating`). Results relate white-zone distance and width to boar density and depopulation timing.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: search-engine abstract (provisional).
- **Relevance to ca-geo:** **EPI-02, CZ case**. The Zlín outbreak is a documented calibration target. The EFSA report (and its 2018 predecessor, DOI 10.2903/sp.efsa.2018.en-1521, verified) should be read in round 2.

### croft2020modelling — Modelling spatial and temporal patterns of African swine fever in an isolated wild boar population to support decision-making
- **Citation:** Croft, S., Massei, G., Smith, G.C., Fouracre, D., Aegerter, J.N. (2020). Modelling Spatial and Temporal Patterns of African Swine Fever in an Isolated Wild Boar Population to Support Decision-Making. *Frontiers in Veterinary Science* 7, 154. DOI: 10.3389/fvets.2020.00154 (verified: Crossref)
- **Access:** OA (PMC7156605)
- **Phenomenon and study area:** hypothetical ASF in the Forest of Dean boar population (about 4 500 km² study area, England).
- **Model:** IBM (individual boar with demography) on irregular habitat polygons (mean 3.9 km²) built from real land cover. Group overlap of 1.35 km sets contact and carcass risk. ASF parameters come from Lange & Thulke. Hunting, culling and carcass removal are scenarios.
- **Parameters:** Table 1 plus references to Croft et al. (earlier FMD boar model).
- **Code:** Python 2 code files in the Supplementary Material (per the paper; not downloaded).
- **Validation:** none possible (no outbreak). Scenario outputs: about 1 km/week initial spread, median burn-out about 14 weeks.
- **Reimplementability:** S1 1 – demographic details deferred to an earlier paper; S2 2; S3 2; S4 1; S5 1 → 7, B. Assessed from: full text (partial).
- **Browser fit:** individual boar are heavier. A group-level version is feasible.
- **Relevance to ca-geo:** EPI-02. Open code for a boar/ASF landscape model is rare. Not a pure CA.

### ibanezporras2025wibiss — WiBISS: a tool to estimate avoided lost revenue of African swine fever wild boar vaccination at municipality level
- **Citation:** Ibáñez-Porras, P., Bosch, J., Feliziani, F., Maresca, C., Sánchez-Vizcaíno, J.M., Iglesias, I., Aguilar-Vega, C., Martínez-Avilés, M. (2025). WiBISS: a tool to estimate avoided lost revenue of African swine fever wild boar vaccination at municipality level. *Frontiers in Veterinary Science* 12, 1667173. DOI: 10.3389/fvets.2025.1667173 (verified: Crossref)
- **Access:** OA (PMC12591982)
- **Phenomenon and study area:** hypothetical ASF vaccination of wild boar, Northern Italy, 2022–2024 outbreak data.
- **Model:** two CA modules. (1) 2 130 notified cases as point cells (unvaccinated / infected / vaccinated). Infection occurs at the observed date, vaccination applies within a radius (0–50 km, haversine) after a response delay, with efficacy decay and reversion. (2) 597 municipalities with FREE / RZ2 / RZ1 states via shared borders. Weekly steps.
- **Inputs:** WAHIS outbreak points and national pig data (on request).
- **Parameters:** listed (efficacy 92 %, delay 0/8 weeks, rates 25–75 %).
- **Code:** not available.
- **Validation:** none. Scenario and economic outputs.
- **Reimplementability:** S1 1 – some rule details ambiguous; S2 2; S3 0; S4 1; S5 1 → 5, C. Assessed from: full text.
- **Browser fit:** trivial.
- **Relevance to ca-geo:** EPI-02. The municipality restriction-zone CA (free / buffer / infected) is an easy add-on for a CZ ASF demo. Weak epidemiology.

### hayes2021mechanistic — Mechanistic modelling of African swine fever: A systematic review
- **Citation:** Hayes, B.H., Andraud, M., Salazar, L.G., Rose, N., Vergne, T. (2021). Mechanistic modelling of African swine fever: A systematic review. *Preventive Veterinary Medicine* 191, 105358. DOI: 10.1016/j.prevetmed.2021.105358 (verified: Crossref)
- **Access:** paywall (arXiv preprint 2011.10126 exists)
- **Value as entry point:** 34 ASF models classified by objective and framework (population, metapopulation, individual-based). Wild-boar models are mostly IBMs. It is the map for choosing an EPI-02 rule set.
- **Reimplementability:** n/a.

### kleczkowski1997scaling — Scaling and spatial dynamics in plant–pathogen systems: from individuals to populations
- **Citation:** Kleczkowski, A., Gilligan, C.A., Bailey, D.J. (1997). Scaling and spatial dynamics in plant–pathogen systems: from individuals to populations. *Proceedings of the Royal Society of London B* 264(1384), 979–984. DOI: 10.1098/rspb.1997.0135 (verified: Crossref)
- **Access:** paywall (Royal Society archive)
- **Phenomenon and study area:** soil-borne fungal pathogen in plant populations (experimental).
- **Model:** transmission components estimated from single-plant experiments feed a probabilistic spatial contact process (plant-level CA), which predicts epidemic progress with spatial correlation from restricted soil movement.
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: secondary description (provisional). No abstract in Crossref or Europe PMC.
- **Relevance to ca-geo:** foundational for field-scale crop disease CA. Little geography.

### martins2000cellular — Cellular automata model for citrus variegated chlorosis
- **Citation:** Martins, M.L., Ceotto, G., Alves, S.G., Bufon, C.C.B., Silva, J.M., Laranjeira, F.F. (2000). Cellular automata model for citrus variegated chlorosis. *Physical Review E* 62(5), 7024–7030. DOI: 10.1103/physreve.62.7024 (verified: Crossref)
- **Access:** preprint (arXiv cond-mat/0008203, read via ar5iv)
- **Phenomenon and study area:** CVC (Xylella) in São Paulo orange groves (four observed groves).
- **Model:** square lattice of trees (L=200), null fixed boundaries. Two binary variables per tree (diseased; stressed). Infection is carried by sharpshooter vectors performing Lévy flights, with seasonal (12-month sinusoid) vector activity and stress-dependent susceptibility. Diseased trees become stressed. Synchronous update, monthly step. Random initial infection p_inf and stress p_st(0).
- **Inputs:** none spatial beyond grove geometry.
- **Parameters:** Table 2 gives the five fitted CA parameters (n0, p_inf, p_min, μ, a) per grove. T=12, φ=−60°.
- **Code:** not found.
- **Validation:** quantitative. Simulated vs observed double-sigmoid disease progress curves (Table 1 logistic fits, R²), cluster-size power-law exponents and Hurst exponents.
- **Reimplementability:** S1 2; S2 2; S3 0; S4 1 – observed curves only as figures and tables; S5 2 → 7, B. Assessed from: full text (preprint).
- **Browser fit:** excellent.
- **Relevance to ca-geo:** plant-disease CA with long-range (Lévy) jumps. Rules transfer to orchard or vineyard rasters, with an EU link to Xylella (`white2017modelling`).

### meentemeyer2011epidemiological — Epidemiological modeling of invasion in heterogeneous landscapes: spread of sudden oak death in California (1990–2030)
- **Citation:** Meentemeyer, R.K., Cunniffe, N.J., Cook, A.R., Filipe, J.A.N., Hunter, R.D., Rizzo, D.M., Gilligan, C.A. (2011). Epidemiological modeling of invasion in heterogeneous landscapes: spread of sudden oak death in California (1990–2030). *Ecosphere* 2(2), art17. DOI: 10.1890/es10-00192.1 (verified: Crossref)
- **Access:** OA (Ecosphere). The publisher page blocked automated reading.
- **Phenomenon and study area:** *Phytophthora ramorum* in California forests, hindcast 1990 to forecast 2030.
- **Model:** 250 m lattice of susceptible/infected host units, weekly step. Infected cells produce inoculum modulated by weather, which disperses via a fitted kernel and infects with a host-availability-dependent probability. 1 000 stochastic replicates. Kernel parameters estimated by MCMC.
- **Inputs:** host vegetation map, weather (moisture/temperature) series.
- **Code:** implemented in GRASS add-on r.spread.sod, later generalised into PoPS (see `jones2021iteratively`).
- **Validation:** against 784 field plots.
- **Reimplementability:** S1 1; S2 1; S3 2; S4 1; S5 1 → 6, C. Assessed from: secondary descriptions (provisional). Likely higher with the full text.
- **Browser fit:** good at regional scale. Many replicates are needed for risk maps.
- **Relevance to ca-geo:** the reference "host raster + weather + dispersal kernel" pathogen CA. It transfers to bark beetle (ECO-01 overlap) or ash dieback in CZ.

### white2017modelling — Modelling the spread and control of Xylella fastidiosa in the early stages of invasion in Apulia, Italy
- **Citation:** White, S.M., Bullock, J.M., Hooftman, D.A.P., Chapman, D.S. (2017). Modelling the spread and control of Xylella fastidiosa in the early stages of invasion in Apulia, Italy. *Biological Invasions* 19(6), 1825–1837. DOI: 10.1007/s10530-017-1393-5 (verified: Crossref)
- **Access:** OA (PMC6979717)
- **Phenomenon and study area:** *X. fastidiosa* in olive groves, Apulia (EU).
- **Model:** 1 km² grid, annual step. The state is the infected fraction of hosts. Carrying capacity is K = Φ + a(1−Φ), with Φ the olive cover. Local growth follows a discretised Gompertz curve (A=3, B=14.069). Short-range spread uses an exponential kernel (mean 100 m, FFT convolution). Long-distance jumps happen when the scaled infected fraction exceeds p=0.2, sending 1–5 dispersers with a Gaussian scale of 20 km, never into the sea. Control zones remove detected infected cells.
- **Inputs:** olive cover (0.01 km² presence/absence, InnovaPuglia), positive test locations, initial outbreak location.
- **Parameters:** table above. ρ and a are not reported numerically.
- **Code:** https://github.com/drsmwhite/Xylella-spread-model (verified 200, MIT, MATLAB). Zenodo 10.5281/zenodo.192974 (verified).
- **Validation:** continuous Boyce index 0.951 against positive test locations (10 000 runs, 5-year horizon).
- **Reimplementability:** S1 2; S2 1; S3 2; S4 1 – olive cover data not open, but CORINE olive class is a proxy; S5 2 → 8, B. Assessed from: full text.
- **Browser fit:** good. A 1 km grid over a region, FFT or small-kernel convolution, ensembles in a worker.
- **Relevance to ca-geo:** strong template for "stratified dispersal on a host-cover raster with control buffer zones". It also fits EPI-02-style containment zones.

### jones2021iteratively — Iteratively forecasting biological invasions with PoPS and a little help from our friends
- **Citation:** Jones, C.M., Jones, S., Petrasova, A., Petras, V., Gaydos, D., Skrip, M.M., Takeuchi, Y., Bigsby, K., Meentemeyer, R.K. (2021). Iteratively forecasting biological invasions with PoPS and a little help from our friends. *Frontiers in Ecology and the Environment* 19(7), 411–418. DOI: 10.1002/fee.2357 (verified: Crossref)
- **Access:** OA (PMC8453564)
- **Phenomenon and study area:** species-agnostic pest/pathogen spread. Case studies are spotted lanternfly (eastern US) and sudden oak death (Oregon).
- **Model:** spatially explicit discrete-time host-raster model. Each cell holds infected/susceptible hosts. Reproduction rate β is modulated by infected count and weather, dispersal uses short and long kernels, and establishment depends on host and environment. Modules can be switched on or off, and the time step is daily to yearly.
- **Inputs:** host maps, weather coefficients, occurrence surveys.
- **Parameters:** calibrated by ABC (sequential MCMC) with iterative Bayesian updating of β, λ, α1, α2.
- **Code:** https://github.com/ncsu-landscape-dynamics/PoPS, …/pops-core, …/rpops, …/r.pops.spread (all verified 200). GRASS manual verified. Web interface popsmodel.org (200).
- **Validation:** hindcasting with quantity and configuration disagreement (Pickard et al.), showing improvement with recalibration.
- **Reimplementability:** S1 1 – the full equations are in the docs and source, not the paper; S2 2; S3 2; S4 1; S5 2 → 8, B. Assessed from: full text.
- **Browser fit:** the core loop is simple and portable. ABC calibration is not for the browser.
- **Relevance to ca-geo:** best open-source reference for crop and forest pest spread CA (ECO-01/ECO-03 overlap). The C++ core is small enough to port to JS.

### fort2012modelling — Modelling the Neolithic transition in the Near East and Europe
- **Citation:** Fort, J., Pujol, T., Vander Linden, M. (2012). Modelling the Neolithic Transition in the Near East and Europe. *American Antiquity* 77(2), 203–219. DOI: 10.7183/0002-7316.77.2.203 (verified: Crossref; Crossref lists the third author's family name as "Linden")
- **Access:** paywall
- **Phenomenon and study area:** spread of farming from the Near East across Europe.
- **Model:** computational front-propagation model compared with interpolated radiocarbon isochrones. The best fit comes from starting at PPNB/C sites with sea travel up to 150 km. Mountains have little effect at continental scale.
- **Code:** none from the authors. Reimplemented as a benchmark in the R package dispeRse (https://cran.r-project.org/package=dispeRse; https://github.com/jgregoriods/dispeRse, both verified).
- **Reimplementability:** S1 1; S2 1; S3 0; S4 1; S5 1 → 4, C. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** population range-expansion demo for Europe including CZ (LBK spread), with sea-jump and barrier toggles.

### bradshaw2021stochastic — Stochastic models support rapid peopling of Late Pleistocene Sahul
- **Citation:** Bradshaw, C.J.A., Norman, K., Ulm, S., Williams, A.N., Clarkson, C., Chadœuf, J., Lin, S.C., Jacobs, Z., Roberts, R.G., Bird, M.I., Weyrich, L.S., Haberle, S.G., O'Connor, S., Llamas, B., Cohen, T.J., Friedrich, T., Veth, P., Leavesley, M., Saltré, F. (2021). Stochastic models support rapid peopling of Late Pleistocene Sahul. *Nature Communications* 12, 2440. DOI: 10.1038/s41467-021-21551-3 (verified: Crossref)
- **Access:** OA (PMC8085232)
- **Phenomenon and study area:** first human colonisation of Sahul (Australia–New Guinea), 75–50 ka.
- **Model:** fully stochastic CA on a 0.5° grid (86×87). Exposed land changes in 1 000-year sea-level slices. Per-cell Ricker dynamics N_{t+1} = N_t·exp(r_m(1−N_t/K)) − E + I, with generation time 27.9 years. Emigration to adjacent cells is triggered by N/K thresholds and modulated by hydrology, plus long-distance dispersal. K comes from LOVECLIM net primary production via three alternative functional forms. 120 scenarios of entry point and time.
- **Inputs:** palaeo-NPP, sea level, palaeo-hydrology, archaeological dates (bias-corrected arrival layer).
- **Parameters:** twelve parameters in a Latin-hypercube sensitivity analysis with a BRT emulator. Defaults are in the methods and supplement.
- **Code:** https://github.com/cjabradshaw/SahulHumanSpread (verified 200, GPL-3, R). The paper states that all code and data are provided.
- **Validation:** Spearman correlation between simulated and archaeological first-arrival layers. Saturation time 156–208 generations, spread rate 0.71–0.92 km/yr.
- **Reimplementability:** S1 2; S2 2; S3 2; S4 2; S5 2 → 10, A. Assessed from: full text.
- **Browser fit:** very good (7 500 cells, 300 generations, 100 replicates).
- **Relevance to ca-geo:** **top pick for "population dispersal / range expansion"**. Grow–saturate–emigrate is directly reusable with K from land cover, e.g. species recolonising CZ (ECO-04/ECO-07 overlap) or historical settlement.

### bradshaw2023directionally — Directionally supervised cellular automaton for the initial peopling of Sahul
- **Citation:** Bradshaw, C.J.A., Crabtree, S.A., White, D.A., Ulm, S., Bird, M.I., Williams, A.N., Saltré, F. (2023). Directionally supervised cellular automaton for the initial peopling of Sahul. *Quaternary Science Reviews* 303, 107971. DOI: 10.1016/j.quascirev.2023.107971 (verified: Crossref). Preprint DOI 10.31219/osf.io/a45fw (Crossref record seen).
- **Access:** preprint (OSF)
- **Phenomenon and study area:** as `bradshaw2021stochastic`, with movement weighted by least-cost "superhighways".
- **Model:** the 2021 demographic CA, with emigration direction biased by superhighway route rasters. Saturation time roughly doubles to about 10 000 years and fits the archaeological layer better.
- **Code:** https://github.com/cjabradshaw/SuperhighwaysSpreadModel (verified 200; Zenodo 10.5281/zenodo.7542562 badge).
- **Reimplementability:** S1 1; S2 1; S3 2; S4 2; S5 1 → 7, B. Assessed from: abstract + repository README (provisional).
- **Relevance to ca-geo:** shows how to add anisotropic, cost-surface-driven emigration (link to movement/accessibility).

### gregoriodesouza2021reassessing — Reassessing the role of climate change in the Tupi expansion (South America, 5000–500 BP)
- **Citation:** Gregorio de Souza, J., Noelli, F.S., Madella, M. (2021). Reassessing the role of climate change in the Tupi expansion (South America, 5000–500 BP). *Journal of The Royal Society Interface* 18(183), 20210499. DOI: 10.1098/rsif.2021.0499 (verified: Crossref)
- **Access:** OA (PMC8492182)
- **Phenomenon and study area:** expansion of Tupi forest farmers across lowland South America.
- **Model:** CA on a biome raster from HadCM3-based palaeovegetation (1 000-year slices). Per-cell logistic growth (default 2.5 %/yr, generation 30 years) and density-dependent emigration (threshold function, Best et al. form). Settlement is unrestricted (null) or limited to tropical moist forest. Compared with an equation-based front model (Fisher with time delay).
- **Inputs:** published palaeo-biome maps (Costa et al.), radiocarbon dates.
- **Parameters:** default values with tested ranges in the methods.
- **Code:** Zenodo 10.5281/zenodo.4964642 ("jgregoriods/tupi-expansion", record page verified; DOI resolver timed out once with 504). Python CA plus R EBM.
- **Validation:** RMSE between simulated arrival times and 14C dates vs distance from origin.
- **Reimplementability:** S1 2; S2 2; S3 2; S4 1 – the palaeo-biome input is published but whether it is redistributed in the repo was not checked; S5 2 → 9, A. Assessed from: full text.
- **Browser fit:** very good.
- **Relevance to ca-geo:** same family as dispeRse and Fort 2012. Easiest open template for "spread with habitat restriction".

### hewitt2025modelling — Modelling mobility of hunter-gatherer populations: a dynamic simulation approach based on cellular automata
- **Citation:** Hewitt, R.J., Alcaraz-Castaño, M., Hernandez, V.C., Morley, M.W. (2025). Modelling Mobility of Hunter-Gatherer Populations: A Dynamic Simulation Approach Based on Cellular Automata. *Journal of Archaeological Method and Theory* 32(4), 57. DOI: 10.1007/s10816-025-09726-4 (verified: Crossref)
- **Access:** OA (PMC12317925)
- **Phenomenon and study area:** Late Pleistocene mobility in central Iberia (EU).
- **Model:** DISPERSCA. Walkers move across a slope-based fitness raster, at each step choosing within a square or hexagonal "decision catchment" (the CA neighbourhood) of 100–1 000 m. Many runs give walk-density maps, an exploratory alternative to least-cost paths.
- **Inputs:** DEM-derived slope.
- **Code:** figshare link in the data availability statement (https://figshare.com/s/b4ed21c7ab4887e1f814, which returned HTTP 202, probably a bot check; not fully verified).
- **Reimplementability:** S1 1; S2 1; S3 1; S4 2; S5 1 → 6, C. Assessed from: full text (partial).
- **Relevance to ca-geo:** minor for EPI. Overlaps with the movement domain (cost-surface walks).

## Most reimplementable (top picks)

1. `bradshaw2021stochastic` (A, 10) – complete Ricker + emigration CA, open R code and data, quantitative fit. Template for population dispersal and range expansion on a carrying-capacity raster.
2. `gregoriodesouza2021reassessing` (A, 9) – compact growth/emigration CA with habitat restriction, open Python code, RMSE check.
3. `white2007modeling` (B, 8) – complete SIR fraction CA with connectivity and vaccination. The cleanest EPI-01 rule, easily put on a CZ population grid.
4. `li2012consequences` (B, 8) – land-cover-driven tick/Lyme CA with a 24-parameter table and field validation. Turns EPI-03 into a dynamic model.
5. `white2017modelling` (B, 8) – Xylella host-cover CA with stratified dispersal, control zones, MIT code and Boyce-index validation.
6. `smith2002predicting` (B, 8) – polygon CA with barrier-modified rates and a parameter table. The rivers/fences barrier demo (EPI-02/ECO-04).
7. `jones2021iteratively` (B, 8) – PoPS, a mature open pest/pathogen spread engine with documented calibration.
8. `davidson2024methodological` (B, 7) – open geographic Cell-DEVS SEIRDS over real regions with a GeoJSON pipeline. Closest to a municipality-level EPI-01 demo.

## Gaps and unverified leads

- **No pure CA for ASF in wild boar** was found. The literature is IBM-dominated (Lange & Thulke family, Croft 2020, Danish ABM). For EPI-02, the practical route is a boar-group-per-cell CA derived from the Lange & Thulke ODD (3×3 km cells). Round 2: read EFSA 2018 (10.2903/sp.efsa.2018.en-1521) and EFSA 2021 in full, and get the ODD from CoMSES.
- **CZ-specific epidemic CA:** none found. EFSA 2021 uses CZ 2017 (Zlín) as a calibration case. Tick-borne encephalitis in CZ: no CA found. `li2012consequences` is the closest transferable model.
- **Paywalled foundational papers not read** (abstracts elided by Elsevier in Crossref/Semantic Scholar): Sirakoulis 2000, Holko 2016, Doran & Laffan 2005, Ward 2009, Madhav 2004, Fort 2012, Kleczkowski 1997. Scores are provisional.
- **Verified in Crossref but not catalogued** (no abstract or full text reachable): Slimi et al. 2009 "A cellular automata model for Chagas disease" (*Appl. Math. Model.* 33(2), DOI 10.1016/j.apm.2007.12.028); Schneckenreither et al. 2008 ODE/PDE/CA SIR comparison (*Simul. Model. Pract. Theory* 16(8), DOI 10.1016/j.simpat.2008.05.015); Sharma & Gupta 2017 SEIR CA with delay (*Physica A* 471, DOI 10.1016/j.physa.2016.12.010); Ahmed & Agiza 1998 latency CA (*Physica A* 253, DOI 10.1016/s0378-4371(97)00665-1); Ghosh & Bhattacharya 2020 GA-fitted PCA for 40 countries (*Appl. Soft Comput.* 96, DOI 10.1016/j.asoc.2020.106692); Cárdenas et al. 2021 Cell-DEVS COVID (LNCS, DOI 10.1007/978-3-030-69480-7_24); Chowdhury et al. 2022 CA COVID India (*EPJ ST*, DOI 10.1140/epjs/s11734-022-00619-1); Bin et al. 2019 SLIRDS CA (*IJERPH*, DOI 10.3390/ijerph16234683, non-geographic); Shaw et al. 2024 ASF wild boar network models (*R. Soc. Open Sci.*, DOI 10.1098/rsos.231319, network not CA); Jeltsch et al. 1999 rabies scaling-down (*Ecol. Model.*, DOI 10.1016/s0304-3800(98)00198-7).
- **Unverified leads (not found in Crossref):** "Mosquito borne diseases simulated by cellular automata: a review" (Universidad Veracruzana PDF, likely Ortigoza et al.); Medeiros et al. 2011 dengue CA (basis of DengueME); Vshivkova et al. 2013 Ixodes tick CA (Russian, *Problemy Upravleniya*); Souza et al. 2020 PLOS ONE demic-diffusion CA (cited in dispeRse); the Fierro/Liccardo/Porcelli lattice model for Xylella vectors; "Modelling the spatial diffusion of past populations – a cellular automata approach" (SocArXiv 10.31235/osf.io/wqzjb, Crossref hit, not assessed).
- **Round 2 suggestions:** full texts of Meentemeyer 2011 and Davidson 2024 (likely S1/S2 → 2); score the individual DengueME library models; search avian influenza / poultry CA and bluetongue (vector-borne livestock, EU); rerun the OpenAlex searches once the quota resets, for citation counts and missed foundational papers; look for a ČSÚ commuting-matrix-coupled SIR (EPI-01 long-range links).
- **Process note:** one WebFetch call on an EFSA report link auto-saved a PDF (about 4 MB) into the Claude tool-results cache (`C:\Users\richa\.claude\projects\C--Users-richa\c2e3fadf-...\tool-results\webfetch-1791800471974-54apu1.pdf`). It was not used and can be deleted.
- **Overlaps with other domains:** PoPS and sudden oak death (ECO-01 bark beetle, ECO-03 invasive species); Bradshaw/Souza demographic CA (ECO-07 range shift, ECO-04 connectivity); DISPERSCA and Sahul superhighways (movement / accessibility); Xylella and wild boar containment zones (land use / management).
