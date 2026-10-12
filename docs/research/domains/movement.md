# Movement of people and vehicles — literature survey

Survey round: 1 (breadth-first), date 2026-10-12. Scoring per ../reimplementability-criteria.md.
Domain code: `mov`. BibTeX keys as in the `mov` fragment of `/references.bib`.

**Verification note.** The OpenAlex daily quota was exhausted early in this round
(HTTP 429, `Retry-After` ≈ 14 h, shared with the other domain agents). The first five
queries ran on OpenAlex; everything else was searched and verified through the
**Crossref** API (`api.crossref.org/works/<DOI>`). Title, authors, year, venue, volume,
pages and DOI below all come from Crossref metadata. Abstracts and OA links come from
Crossref and the Semantic Scholar Graph API. Full texts were read only where an arXiv
preprint was reachable through WebFetch. Publisher sites (ScienceDirect, MDPI, Springer,
Nature, the U. Chile repository) blocked automated access, so most non-arXiv entries are
scored from the abstract, and a few from bibliographic metadata only. These are marked
as provisional.

## Search log

Date of all searches: 2026-10-12.

| Query | Source | Hits | Notes |
|---|---|---|---|
| cellular automaton model for freeway traffic | OpenAlex | 1 562 | NaSch 1992 found (3 871 cites); Emmerich–Rank, Nagatani variants |
| floor field cellular automaton pedestrian dynamics | OpenAlex | 797 | Burstedde 2001, Lovreglio 2015, Nowak 2012, Luo 2017, Lu 2016, Xing 2023 |
| lattice gas model pedestrian evacuation | OpenAlex | 699 | Guo & Huang 2008, Guo 2012/2013 heterogeneous LG |
| cellular automaton evacuation tsunami GIS | OpenAlex | 61 | no genuine CA tsunami evacuation model; mostly ABM/GIS least-cost |
| cellular automata traffic flow review | OpenAlex | 7 231 | Maerivoet 2005, Daganzo 2006, Tian 2020 synchronized-flow review |
| (OpenAlex quota exhausted from here on) | — | — | switched to Crossref `query.bibliographic` |
| Biham Middleton Levine self-organization | Crossref | 93 637 (unranked) | BML 1992 verified |
| two-lane traffic CA lane changing rules | OpenAlex/Crossref | 1 601 | Nagel 1998, Rickert 1996, Belitsky 2001 |
| cellular automaton evacuation wildfire (coupled) | Crossref + web | noisy | no single-engine CA fire+evacuation found; Liu 2023 (FDS+CA), Soga et al. report (not in Crossref) |
| cellular automaton evacuation flood | Crossref | noisy | Zheng 2019 (underground flood + FFCA) |
| CA travel time / accessibility raster; cost distance CA | Crossref + web | noisy | Duff 2015 (DES-CA travel time), Wood & Schmidtlein 2012 (anisotropic path distance), Weiss 2018 (friction surface) |
| shortest path cellular automata raster | Crossref | noisy | Adamatzky 1996 (abstract CA, context only) |
| Microscopic simulation urban traffic CA (Esser) | Crossref | — | Esser 1997, Wahle 1998 online simulation |
| CA car traffic 2D street network (Chopard) | Crossref | — | Chopard 1996 |
| realistic microscopic highway traffic (Knospe) | Crossref | — | Knospe 2000, 2002 |
| friction clogging CA pedestrian | Crossref | — | Kirchner 2003 |
| Blue Adler bidirectional walkways | Crossref | — | Blue & Adler 2001 |
| statistical physics vehicular traffic | Crossref | — | Chowdhury 2000 review |
| crowd evacuation seven approaches | Crossref | — | Zheng 2009 review |
| TRANSIMS parallel micro-simulation | Crossref | — | Nagel & Rickert 2001 |
| metastable states / slow-to-start | Crossref | — | Barlovic 1998 (VDR) |
| self-organization traffic jams cities (ChSch) | Crossref | — | Chowdhury & Schadschneider 1999 |
| Potuzak road traffic simulation | Crossref | — | CZ (ZČU) distributed traffic simulation papers; CA basis not confirmed |
| floor field / lattice gas / Nagel–Schreckenberg / BML | GitHub (API + `gh`) | 0 / 1 / 132 / 19 repos | many third-party NaSch & BML implementations; no author-published FFCA repo found |
| web searches (tsunami CA, WUI fire + evacuation CA, CA accessibility, FFCA code) | WebSearch | — | leads listed under "Gaps" |

## Model families

1. **Floor-field cellular automata (FFCA) for pedestrians.** One pedestrian per cell of
   about 0.4 × 0.4 m, Moore neighbourhood, at most one cell per step (about 0.3 s per
   step). Moves are drawn from probabilities proportional to exp(kS·S)·exp(kD·D). The
   static field S is the distance to the exit. The dynamic field D is a decaying,
   diffusing trace left by walkers. Updates are parallel, and conflicts over the same
   target cell are resolved at random, optionally with a "friction" μ. Core papers:
   `burstedde2001simulation`, `kirchner2002simulation`, `kirchner2003friction`. Variants
   and calibration: `varas2007cellular`, `nowak2012quantitative`,
   `lovreglio2015calibrating`. **Hazard-coupled FFCA:** extra floor fields or speed
   reductions driven by a hazard layer (`zheng2019simulation` flood depth,
   `liu2023cellular` smoke/CO from FDS, `guo2013modeling` fire).
2. **Lattice-gas / biased-random-walk pedestrian models.** A walker moves to an empty
   neighbour with a drift towards its target. These are the forerunners of FFCA, used
   for counterflow and evacuation (`muramatsu1999jamming`, `guo2008mobile`,
   `guo2013modeling`). `blue2001cellular` covers rule-based bidirectional walkway CA.
3. **Single-lane stochastic traffic CA.** NaSch: acceleration, braking to the gap,
   random slowdown with probability p, then movement; 7.5 m cells, 1 s steps,
   vmax = 5 (`nagel1992cellular`). Slow-to-start / VDR
   (`barlovic1998metastable`). Brake-light / comfortable-driving model with empirical
   calibration (`knospe2000towards`).
4. **Multi-lane traffic CA.** Lane change is a separate sub-step with look-ahead,
   look-back and a change probability (`rickert1996two`, `nagel1998twolane`).
5. **City / network traffic CA.** BML: two species on a torus that move on alternate
   steps (`biham1992selforganization`). ChSch: BML intersections joined by NaSch street
   segments with signal periods (`chowdhury1999selforganization`). Rotary junctions on a
   Manhattan grid (`chopard1996cellular`). Real networks built from links and nodes:
   Duisburg (`esser1997microscopic`), TRANSIMS on regional networks
   (`nagel2001parallel`).
6. **Front spreading / travel-time surfaces (accessibility).** A front moves outward
   from sources over a raster cost or friction surface. This is CA-like (each cell's
   arrival time follows from its neighbours) and in practice equals Dijkstra-type
   cost-distance. Examples: `duff2015using` (discrete-event CA for fire-crew travel
   times, on and off road), `wood2012anisotropic` (slope-anisotropic pedestrian
   evacuation time to high ground for tsunamis), `weiss2018global` (global friction
   surface and travel time to cities). The geographic evacuation literature (tsunami,
   flood) mostly uses this least-cost approach or agent-based models, not true CA.
7. **CA on real outdoor geometry.** Only a few verified items: `velasquez2021outdoors`
   (CA plus graph on Google elevation tiles for hill evacuation routes) and
   `dang2021chain` (multi-floor CA navigation grid for VR crowd evacuation).
8. **Reviews / entry points:** `chowdhury2000statistical`, `maerivoet2005cellular`
   (traffic). `schadschneider2009evacuation`, `zheng2009modeling`,
   `pelechano2008evacuation` (pedestrians/evacuation).

## Catalogue

| Key | Year | Short title | Phenomenon | CA design (grid / neighbourhood / states / det. or stoch.) | S1 S2 S3 S4 S5 | Total | Class | Code | Access | Assessed from |
|---|---|---|---|---|---|---|---|---|---|---|
| nagel1992cellular | 1992 | NaSch freeway CA | single-lane traffic | 1D, 7.5 m cells, look-ahead vmax; v∈{0..5}; stochastic | 2 2 1 2 2 | 9 | A | third-party (GitHub) | OA (HAL, bot-blocked) | review full text (maerivoet2005) |
| biham1992selforganization | 1992 | BML city traffic | 2D grid jamming | 2D torus, 2 species, alternate update; deterministic | 2 2 1 2 2 | 9 | A | third-party JS | OA (arXiv) | abstract + review full text |
| kirchner2002simulation | 2002 | Bionics FFCA evacuation | room evacuation | 2D 0.4 m, Moore, static+dynamic field; stochastic parallel | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| kirchner2003friction | 2003 | Friction & clogging in FFCA | bottleneck clogging | as above + friction μ | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| rickert1996two | 1996 | Two-lane CA traffic | multi-lane traffic | 2 × 1D NaSch + lane-change sub-step; stochastic | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| knospe2000towards | 2000 | Brake-light (comfortable driving) CA | highway traffic phases | 1D, 1.5 m cells, vmax 20, brake lights, anticipation; stochastic | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| chowdhury1999selforganization | 1999 | ChSch city CA | urban grid with signals | 2D street lattice, NaSch on links, signals period T | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| weiss2018global | 2018 | Global travel time to cities | accessibility | 1 km friction raster, least-cost front from cities | 1 1 1 2 2 | 7 | B | GEE assets (closed platform); data open | OA (repository) | abstract + web summary (provisional) |
| burstedde2001simulation | 2001 | 2D CA pedestrian dynamics | lane formation, evacuation | 2D 0.4 m, Moore, preference matrix + floor fields | 2 1 0 2 1 | 6 | C | not found | OA (arXiv) | full text |
| nowak2012quantitative | 2012 | FFCA counterflow | bidirectional flow | FFCA, 2 species, anticipation | 1 1 0 2 2 | 6 | C | not found | OA (arXiv) | abstract (provisional) |
| wood2012anisotropic | 2012 | Anisotropic path tsunami evacuation | tsunami pedestrian evacuation time | raster least-cost, slope-direction anisotropy | 1 1 1 2 1 | 6 | C | closed (ArcGIS tool) | OA (Springer) | abstract (provisional) |
| nagel1998twolane | 1998 | Systematic two-lane rules | lane changing | NaSch + lane-change scheme | 1 1 0 2 1 | 5 | C | not found | OA (arXiv) | abstract (provisional) |
| barlovic1998metastable | 1998 | VDR slow-to-start | metastability, hysteresis | NaSch with velocity-dependent p | 1 1 0 2 1 | 5 | C | not found | OA (arXiv) | abstract (provisional) |
| chopard1996cellular | 1996 | CA street network with rotaries | Manhattan city traffic | 2D street lattice, rotary junctions | 1 1 0 2 1 | 5 | C | not found | OA (UNIGE repository) | abstract (provisional) |
| liu2023cellular | 2023 | CA evacuation with fire products | building fire evacuation | FFCA with speed reduced by visibility/CO from FDS | 1 1 0 1 2 | 5 | C | not found | OA (MDPI) | abstract (provisional) |
| blue2001cellular | 2001 | Bidirectional walkway CA | pedestrian counterflow | 2D rule-based CA, multi-speed | 1 0 0 2 1 | 4 | C | not found | paywall | metadata only (provisional) |
| muramatsu1999jamming | 1999 | Counterflow lattice gas | pedestrian jamming | 2D biased random walk, 2 species | 1 0 0 2 1 | 4 | C | not found | paywall | metadata only (provisional) |
| guo2008mobile | 2008 | Mobile lattice gas evacuation | room evacuation | 2D lattice gas, multi-step per tick | 1 0 0 2 1 | 4 | C | not found | paywall | metadata only (provisional) |
| varas2007cellular | 2007 | CA evacuation with obstacles | evacuation around obstacles | 2D FFCA-like, obstacle floor field | 1 0 0 2 1 | 4 | C | not found | OA (U. Chile, bot-blocked) | metadata only (provisional) |
| lovreglio2015calibrating | 2015 | Likelihood calibration of FFCA | parameter calibration | FFCA; MLE of kS, kD etc. | 1 1 0 1 1 | 4 | C | not found | paywall | metadata only (provisional) |
| zheng2019simulation | 2019 | FFCA + underground flood | subway flood evacuation | FFCA with height/support/danger/flow fields; rising water | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| esser1997microscopic | 1997 | Urban CA traffic (Duisburg) | city network traffic | NaSch links + junction building blocks | 1 1 0 1 1 | 4 | C | not found | paywall | abstract (provisional) |
| nagel2001parallel | 2001 | TRANSIMS parallel micro-simulation | regional network traffic | NaSch-type CA on links, domain decomposition | 1 1 0 1 1 | 4 | C | lead not verified | OA (arXiv) | abstract (provisional) |
| duff2015using | 2015 | DES-CA travel times to wildfires | crew travel time / accessibility | raster CA front from fire, road + off-road | 1 0 0 2 1 | 4 | C | not found | paywall | abstract (provisional) |
| dang2021chain | 2021 | Chain navigation grid CA (VR) | multi-floor crowd evacuation | CA grid linked across floors | 1 0 0 1 2 | 4 | C | not found | OA (Elsevier) | abstract (provisional) |
| guo2013modeling | 2013 | Heterogeneous lattice gas + fire | fire evacuation | lattice gas with fire/smoke influence | 1 0 0 1 1 | 3 | D | not found | paywall | metadata only (provisional) |
| velasquez2021outdoors | 2021 | Outdoor evacuation routes CA + graph | hill/wildfire evacuation routes | 3D CA on elevation tiles + graph search | 1 0 0 1 1 | 3 | D | not found | OA (MDPI) | abstract (provisional) |
| chowdhury2000statistical | 2000 | Statistical physics of vehicular traffic | review (traffic) | — | n/a | — | n/a | — | OA (arXiv) | abstract |
| maerivoet2005cellular | 2005 | CA models of road traffic | review (traffic) | — | n/a | — | n/a | — | OA (arXiv) | full text |
| schadschneider2009evacuation | 2009 | Evacuation dynamics | review (pedestrians) | — | n/a | — | n/a | — | paywall | metadata |
| zheng2009modeling | 2009 | Crowd evacuation: seven approaches | review (evacuation) | — | n/a | — | n/a | — | paywall | metadata |
| pelechano2008evacuation | 2008 | CA for high-rise evacuation: challenges | critique/review | — | n/a | — | n/a | — | OA (UPC repository) | metadata |

## Entries

### Pedestrian dynamics and evacuation

### burstedde2001simulation — Simulation of pedestrian dynamics using a two-dimensional cellular automaton
- **Citation:** Burstedde, C., Klauck, K., Schadschneider, A., Zittartz, J. (2001). Simulation of pedestrian dynamics using a two-dimensional cellular automaton. *Physica A: Statistical Mechanics and its Applications* 295(3–4), 507–525. DOI: 10.1016/s0378-4371(01)00141-8 (verified: OpenAlex + Crossref)
- **Access:** OA preprint, arXiv cond-mat/0102397.
- **Phenomenon and study area:** Generic pedestrian flows: lane formation in counterflow, oscillations at doors, evacuation of a room with poor visibility. No real geography.
- **Model:** Square grid of about 40 × 40 cm cells, each holding at most one pedestrian. Moore neighbourhood with 9 targets including staying put; vmax = 1. Each walker has a 3 × 3 preference matrix M. The move probability is p_ij = N·M_ij·D_ij·S_ij·(1−n_ij), where S is a static field, D is a dynamic "boson" field with diffusion and decay, and n is occupancy. The update is fully parallel. In a conflict, one walker wins with probability proportional to its own transition probability. Walkers drop D on the cell they leave. One step is about 0.3 s, so 0.4 m per step gives about 1.3 m/s. The boundary is periodic or walls, depending on the scenario.
- **Inputs:** Floor plan (walls, exits). Generic.
- **Parameters:** Defined, but values are tied to each example. There is no single parameter table. The detailed treatment of the discrete-field variant is given only for illustrations.
- **Code:** not found.
- **Validation:** Qualitative reproduction of collective phenomena.
- **Reimplementability:** S1 2 – complete update steps, conflict rule, cell size and timescale. S2 1 – values per example only. S3 0. S4 2 – synthetic geometry. S5 1 – mostly qualitative → **6, C**. Assessed from: full text.
- **Browser fit:** Excellent. O(N) local rules, thousands of agents in real time.
- **Relevance to ca-geo:** MOV-01 core. The floor-field concept transfers directly to a static field computed as distance to safe areas on a geographic raster.

### kirchner2002simulation — Simulation of evacuation processes using a bionics-inspired cellular automaton model for pedestrian dynamics
- **Citation:** Kirchner, A., Schadschneider, A. (2002). Simulation of evacuation processes using a bionics-inspired cellular automaton model for pedestrian dynamics. *Physica A* 312(1–2), 260–276. DOI: 10.1016/s0378-4371(02)00857-9 (verified: Crossref)
- **Access:** OA preprint, arXiv cond-mat/0203461.
- **Phenomenon and study area:** Evacuation of a large room with one or two doors (synthetic).
- **Model:** This is the standard FFCA formulation. p_ij = N·exp(kD·D_ij)·exp(kS·S_ij)·(1−n_ij)·ξ_ij, where ξ masks walls. S is the static distance-to-door field, built with a stated metric (appendix). D is the dynamic field: walkers deposit bosons, which decay with probability δ and diffuse with probability α. Updates are parallel with the usual conflict resolution. One step is about 0.3 s.
- **Inputs:** Room geometry only.
- **Parameters:** All given. kS, kD, α, δ and density ρ are swept, for example ρ = 0.3 on a 63 × 63 grid with a one-cell door. The two-door case uses a 102 × 102 grid. Results are averaged over 500 runs.
- **Code:** not found (no author repository; GitHub search returned no FFCA repo matching this paper).
- **Validation:** Parameter studies. Three regimes (ordered, optimal, disordered/panic). Non-monotonic dependence of evacuation time on kD.
- **Reimplementability:** S1 2. S2 2. S3 0. S4 2. S5 2 – mean evacuation times as curves over (kS, kD, α, δ, ρ), which can be read off figures → **8, B**. Assessed from: full text.
- **Browser fit:** Excellent. 100 × 100 grids with ~1 000 agents are trivial. Ensembles of 500 runs are feasible in a Web Worker.
- **Relevance to ca-geo:** MOV-01 reference implementation. Its curves serve as a unit-test benchmark before the model is moved onto OSM building/street rasters.

### kirchner2003friction — Friction effects and clogging in a cellular automaton model for pedestrian dynamics
- **Citation:** Kirchner, A., Nishinari, K., Schadschneider, A. (2003). Friction effects and clogging in a cellular automaton model for pedestrian dynamics. *Physical Review E* 67(5), 056122. DOI: 10.1103/physreve.67.056122 (verified: Crossref)
- **Access:** OA preprint, arXiv cond-mat/0209383.
- **Phenomenon and study area:** Clogging at a single exit (synthetic 63 × 63 room).
- **Model:** The kirchner2002 FFCA plus a friction parameter μ. With probability μ, all walkers involved in a conflict are blocked for that step. The paper argues that parallel update is required so that conflicts actually occur.
- **Inputs:** Room geometry.
- **Parameters:** μ, kS, kD, α, δ, ρ all given. Evacuation times averaged over 500 samples.
- **Code:** not found.
- **Validation:** Evacuation time versus μ and density in the three regimes. Faster-is-slower type effects.
- **Reimplementability:** S1 2. S2 2. S3 0. S4 2. S5 2 → **8, B**. Assessed from: full text.
- **Browser fit:** Excellent.
- **Relevance to ca-geo:** MOV-01. A single extra parameter gives realistic bottleneck clogging at bridges, gates and narrow streets.

### varas2007cellular — Cellular automaton model for evacuation process with obstacles
- **Citation:** Varas, A., Cornejo, M.D., Mainemer, D., Toledo, B., Rogan, J., Muñoz, V., Valdivia, J.A. (2007). Cellular automaton model for evacuation process with obstacles. *Physica A* 382(2), 631–642. DOI: 10.1016/j.physa.2007.04.006 (verified: OpenAlex/Crossref)
- **Access:** OA author copy in the U. Chile repository (bot-protected, not readable automatically).
- **Phenomenon and study area:** Room evacuation with obstacles (synthetic).
- **Model:** CA with an obstacle-aware static floor field. Exact rules not seen.
- **Inputs:** Floor plan. **Parameters:** not seen. **Code:** not found. **Validation:** not seen.
- **Reimplementability:** S1 1. S2 0. S3 0. S4 2. S5 1 → **4, C**. Assessed from: metadata only (provisional).
- **Browser fit:** Good. **Relevance to ca-geo:** MOV-01. Computing a static field around obstacles maps to buildings on a raster. Highly cited (374).

### nowak2012quantitative — Quantitative analysis of pedestrian counterflow in a cellular automaton model
- **Citation:** Nowak, S., Schadschneider, A. (2012). Quantitative analysis of pedestrian counterflow in a cellular automaton model. *Physical Review E* 85(6), 066128. DOI: 10.1103/physreve.85.066128 (verified: OpenAlex/Crossref)
- **Access:** OA, arXiv 1206.3084.
- **Phenomenon and study area:** Bidirectional corridor flow.
- **Model:** FFCA with two species. Adds an order parameter for lanes and an anticipation mechanism that reduces gridlock.
- **Inputs:** Corridor geometry. **Parameters:** partly in abstract. **Code:** not found.
- **Validation:** Phase diagram with free flow, disorder, lanes and gridlock. Compared with experimental bounds.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 2. S5 2 – the phase diagram is a quantitative check → **6, C**. Assessed from: abstract (provisional). Full text is on arXiv; read it in round 2.
- **Browser fit:** Good. **Relevance to ca-geo:** MOV-01 counterflow on streets, for example people moving towards a hazard while others flee.

### lovreglio2015calibrating — Calibrating floor field cellular automaton models for pedestrian dynamics by using likelihood function optimization
- **Citation:** Lovreglio, R., Ronchi, E., Nilsson, D. (2015). Calibrating floor field cellular automaton models for pedestrian dynamics by using likelihood function optimization. *Physica A* 438, 308–320. DOI: 10.1016/j.physa.2015.06.040 (verified: OpenAlex/Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Calibrating FFCA parameters from trajectory data.
- **Model:** FFCA. The calibration method is maximum likelihood (title-level information only).
- **Inputs:** Pedestrian trajectories. **Parameters:** calibration procedure (not seen). **Code:** not found. **Validation:** not seen.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 1. S5 1 → **4, C**. Assessed from: metadata only (provisional).
- **Browser fit:** n/a (offline calibration). **Relevance to ca-geo:** MOV-01 calibration methodology. Overlaps with `gen` (calibration methods).

### blue2001cellular — Cellular automata microsimulation for modeling bi-directional pedestrian walkways
- **Citation:** Blue, V.J., Adler, J.L. (2001). Cellular automata microsimulation for modeling bi-directional pedestrian walkways. *Transportation Research Part B: Methodological* 35(3), 293–312. DOI: 10.1016/s0191-2615(99)00052-1 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Bidirectional walkway flow, a classic transport-engineering CA.
- **Model:** Rule-based 2D CA with lane-change and step sub-rules (details not seen).
- **Inputs:** Walkway geometry. **Parameters:** not seen. **Code:** not found. **Validation:** fundamental diagrams (according to the title/venue; not checked).
- **Reimplementability:** S1 1. S2 0. S3 0. S4 2. S5 1 → **4, C**. Assessed from: metadata only (provisional).
- **Browser fit:** Good. **Relevance to ca-geo:** MOV-01. An alternative rule family to FFCA for sidewalks.

### muramatsu1999jamming — Jamming transition in pedestrian counter flow
- **Citation:** Muramatsu, M., Irie, T., Nagatani, T. (1999). Jamming transition in pedestrian counter flow. *Physica A* 267(3–4), 487–498. DOI: 10.1016/s0378-4371(99)00018-7 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Counterflow in a channel (lattice gas).
- **Model:** Biased random walkers of two species on a square lattice (family-level knowledge, not checked in the text).
- **Inputs/Parameters/Code/Validation:** not seen / not found.
- **Reimplementability:** S1 1. S2 0. S3 0. S4 2. S5 1 → **4, C**. Assessed from: metadata only (provisional).
- **Browser fit:** Excellent. **Relevance to ca-geo:** MOV-01. The simplest pedestrian lattice gas, a good teaching baseline.

### guo2008mobile — A mobile lattice gas model for simulating pedestrian evacuation
- **Citation:** Guo, R.Y., Huang, H.J. (2008). A mobile lattice gas model for simulating pedestrian evacuation. *Physica A* 387(2–3), 580–586. DOI: 10.1016/j.physa.2007.10.001 (verified: OpenAlex/Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Room evacuation.
- **Model:** Lattice gas in which walkers can move more than one cell per step ("mobile"). Details not seen.
- **Reimplementability:** S1 1. S2 0. S3 0. S4 2. S5 1 → **4, C**. Assessed from: metadata only (provisional).
- **Browser fit:** Excellent. **Relevance to ca-geo:** MOV-01 variant.

### guo2013modeling — Modeling of pedestrian evacuation under fire emergency based on an extended heterogeneous lattice gas model
- **Citation:** Guo, X., Chen, J., You, S., Wei, J. (2013). Modeling of pedestrian evacuation under fire emergency based on an extended heterogeneous lattice gas model. *Physica A* 392(9), 1994–2006. DOI: 10.1016/j.physa.2012.12.033 (verified: OpenAlex/Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Building evacuation while a fire spreads.
- **Model:** Heterogeneous lattice gas whose movement responds to the fire (details not seen).
- **Reimplementability:** S1 1. S2 0. S3 0. S4 1. S5 1 → **3, D**. Assessed from: metadata only (provisional).
- **Browser fit:** Good. **Relevance to ca-geo:** chain L12 (fire → evacuation) at building scale. Overlaps with `fire`.

### zheng2019simulation — Simulation of pedestrians' evacuation dynamics with underground flood spreading based on cellular automaton
- **Citation:** Zheng, Y., Li, X.-G., Jia, B., Jiang, R. (2019). Simulation of pedestrians' evacuation dynamics with underground flood spreading based on cellular automaton. *Simulation Modelling Practice and Theory* 94, 149–161. DOI: 10.1016/j.simpat.2019.03.001 (verified: OpenAlex/Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Evacuation of a subway platform with rising floodwater.
- **Model:** FFCA with five fields: static (exit), height (higher ground), support (grab objects), danger (avoid deep water) and water-flow (move with the current). Behaviour has four stages as water depth rises: normal walking, slow walking, moving to a shelter, waiting for rescue.
- **Inputs:** Platform layout and a water-depth rise rate. **Parameters:** some in the abstract (density, rise rate). **Code:** not found.
- **Validation:** Sensitivity studies. No empirical validation mentioned.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 1. S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Good.
- **Relevance to ca-geo:** **Chain L12 (HYD-02 → MOV-01)**. A template for coupling a flood CA depth raster to evacuees through extra floor fields: a height field from the DEM and a danger field from water depth.

### liu2023cellular — Cellular Automaton Model for Pedestrian Evacuation Considering Impacts of Fire Products
- **Citation:** Liu, Y., Li, J., Sun, C. (2023). Cellular Automaton Model for Pedestrian Evacuation Considering Impacts of Fire Products. *Fire* 6(8), 320. DOI: 10.3390/fire6080320 (verified: Crossref)
- **Access:** OA (MDPI; automated access blocked).
- **Phenomenon and study area:** Single-room and multi-room building fire.
- **Model:** CA evacuation in which walking speed and familiarity change over time with visibility and CO concentration. These are imported from FDS smoke simulations, giving one-way coupling.
- **Inputs:** FDS output fields. **Parameters:** partly in the abstract (densities 0.1–0.5 p/m², CO yield). **Code:** not found.
- **Validation:** Quantitative scenario results (percentage changes in efficiency), not validated against data.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 1. S5 2 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** The CA part fits. The FDS fields would have to be precomputed.
- **Relevance to ca-geo:** L12 pattern. Hazard-field → speed-reduction coupling, the same idea as using a gas plume (ATM-03) to slow or block evacuees.

### velasquez2021outdoors — Outdoors Evacuation Routes Algorithm Using Cellular Automata and Graph Theory for Uphills and Downhills
- **Citation:** Velasquez, W., Alvarez-Alvarado, M.S. (2021). Outdoors Evacuation Routes Algorithm Using Cellular Automata and Graph Theory for Uphills and Downhills. *Sustainability* 13(9), 4731. DOI: 10.3390/su13094731 (verified: OpenAlex/Crossref)
- **Access:** OA (MDPI; automated access blocked).
- **Phenomenon and study area:** Outdoor evacuation routes in hilly terrain (wildfire, climbing).
- **Model:** Fetches Google map tiles and elevations, builds a 3D CA over them, and combines it with graph search to get routes.
- **Inputs:** Google Maps tiles and elevation (proprietary service; a DEM could substitute). **Parameters:** not stated. **Code:** not found.
- **Validation:** Computation-time claims only.
- **Reimplementability:** S1 1. S2 0. S3 0. S4 1. S5 1 → **3, D**. Assessed from: abstract (provisional).
- **Browser fit:** Good concept. **Relevance to ca-geo:** MOV-01/MOV-03 on a DEM. One of the few CA works on real terrain, but weak in specification.

### dang2021chain — A chain navigation grid based on cellular automata for large-scale crowd evacuation in virtual reality
- **Citation:** Dang, P., Zhu, J., Pirasteh, S., Li, W., You, J., Xu, B. et al. (2021). A chain navigation grid based on cellular automata for large-scale crowd evacuation in virtual reality. *International Journal of Applied Earth Observation and Geoinformation* 103, 102507. DOI: 10.1016/j.jag.2021.102507 (verified: OpenAlex/Crossref)
- **Access:** OA (Elsevier; automated access blocked).
- **Phenomenon and study area:** Large-crowd, multi-floor evacuation visualised in VR.
- **Model:** A chain navigation grid links the CA grids of several floors and turns discrete CA steps into continuous motion for rendering. Adds an environment-familiarity factor.
- **Inputs:** Building/scene model. **Parameters:** not seen. **Code:** not found.
- **Validation:** Compared with Pathfinder software (about 6% efficiency gain reported).
- **Reimplementability:** S1 1. S2 0. S3 0. S4 1. S5 2 → **4, C**. Assessed from: abstract via web summary (provisional).
- **Browser fit:** The idea of smoothing discrete CA motion for display is useful for a WebGL front end.
- **Relevance to ca-geo:** MOV-01 visualisation. Overlaps with `gen` (CA visualisation).

### Traffic flow

### nagel1992cellular — A cellular automaton model for freeway traffic
- **Citation:** Nagel, K., Schreckenberg, M. (1992). A cellular automaton model for freeway traffic. *Journal de Physique I* 2(12), 2221–2229. DOI: 10.1051/jp1:1992277 (verified: OpenAlex + Crossref)
- **Access:** OA via HAL (jpa-00246697). The HAL copy is behind bot protection, so the rules were read in the full text of maerivoet2005cellular (§3.2.1).
- **Phenomenon and study area:** Spontaneous jams on a single-lane freeway (ring road).
- **Model:** 1D lattice, each cell empty or holding a car with speed 0..vmax. Parallel update in four steps: (1) accelerate by 1 up to vmax and brake to the gap, v ← min(v+1, gap, vmax); (2) with probability p slow down by 1; (3) move by v. Usual conventions: cell 7.5 m, step 1 s, vmax = 5 (≈135 km/h). Periodic boundary, or open with injection/removal.
- **Inputs:** Road length and density only. On a network the links come from a road graph.
- **Parameters:** vmax, p, density. Standard values are widely documented. Free-flow mean speed is vmax − p.
- **Code:** third-party open implementations verified, for example https://github.com/morethanoneanimal/Nagel-Schreckenberg-simulation, https://github.com/jstitch/NaSch.py, https://github.com/yohm/sim_ns_model. These are not by the authors.
- **Validation:** Fundamental diagram and space-time plots, with analytical limits known.
- **Reimplementability:** S1 2. S2 2. S3 1 – third-party code only. S4 2. S5 2 → **9, A**. Assessed from: full text of review (maerivoet2005cellular) plus abstract.
- **Browser fit:** Trivial. Millions of cell updates per second in JS.
- **Relevance to ca-geo:** MOV-02 lead **confirmed**. Run on OSM road links as 1D lattices with junction rules (see esser1997microscopic). Needs a rasterised or graph representation, not a 2D raster CA.

### barlovic1998metastable — Metastable states in cellular automata for traffic flow
- **Citation:** Barlovic, R., Santen, L., Schadschneider, A., Schreckenberg, M. (1998). Metastable states in cellular automata for traffic flow. *The European Physical Journal B* 5(3), 793–800. DOI: 10.1007/s100510050504 (verified: Crossref)
- **Access:** OA, arXiv cond-mat/9804170.
- **Phenomenon and study area:** High-flow metastable states and hysteresis.
- **Model:** NaSch with velocity-dependent randomisation (VDR). Stopped cars get a higher slowdown probability p0 than moving cars (p), a slow-to-start rule.
- **Parameters:** p0, p, vmax (values not checked). **Code:** not found by the authors. Trivial extension of NaSch implementations.
- **Validation:** Hysteresis in the fundamental diagram.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 2. S5 1 → **5, C**. Assessed from: abstract (provisional). The rule is also summarised in maerivoet2005cellular §3.3, so it is likely B after round-2 reading.
- **Browser fit:** Trivial. **Relevance to ca-geo:** MOV-02 option for realistic jam outflow.

### knospe2000towards — Towards a realistic microscopic description of highway traffic
- **Citation:** Knospe, W., Santen, L., Schadschneider, A., Schreckenberg, M. (2000). Towards a realistic microscopic description of highway traffic. *Journal of Physics A: Mathematical and General* 33(48), L477–L485. DOI: 10.1088/0305-4470/33/48/103 (verified: Crossref)
- **Access:** OA, arXiv cond-mat/0012204.
- **Phenomenon and study area:** Three traffic phases (free, synchronised, stop-and-go). Compared with single-vehicle loop data from a German motorway.
- **Model:** Brake-light ("comfortable driving") CA. Cells are 1.5 m, cars are 5 cells long, steps are 1 s. Each car has a brake-light state. The slowdown probability is chosen from p0 (standing), pb (brake light ahead within horizon t_s = min(v, h)) or pd (otherwise). An effective gap with anticipation of the leader's next speed is used. The paper gives pseudocode for the five steps.
- **Parameters:** Full set given: vmax = 20 cells/s (108 km/h), pd = 0.1, p0 = 0.5, pb = 0.94, gap_security = 7, h = 6. Ring of 50 000 cells.
- **Code:** not found.
- **Validation:** Fundamental diagram, time-headway distributions and gap–speed relation against empirical data. Jam front speed about 12.75 km/h.
- **Reimplementability:** S1 2. S2 2. S3 0. S4 2. S5 2 → **8, B**. Assessed from: full text.
- **Browser fit:** Easy.
- **Relevance to ca-geo:** MOV-02 "realistic" option. Matches empirical highway data. Useful if evacuation traffic on motorways is modelled.

### rickert1996two — Two lane traffic simulations using cellular automata
- **Citation:** Rickert, M., Nagel, K., Schreckenberg, M., Latour, A. (1996). Two lane traffic simulations using cellular automata. *Physica A* 231(4), 534–550. DOI: 10.1016/0378-4371(95)00442-4 (verified: Crossref)
- **Access:** OA, arXiv cond-mat/9512119.
- **Phenomenon and study area:** Two-lane freeway (ring), symmetric and asymmetric (keep-right) rules.
- **Model:** Two NaSch lanes. Each step has two sub-steps: (1) sideways lane changes only, (2) independent NaSch updates. A car changes lane if (T1) its own gap < l, (T2) the gap on the other lane > lo, (T3) the gap behind on the other lane > lo,back, and (T4) rand < p_change.
- **Parameters:** Given: l = v+1, lo = l, lo,back = vmax = 5, p_change = 1 (base case), plus stochastic variants. Lattice of 12 000 sites.
- **Code:** not found.
- **Validation:** Flow–density per lane. Two-lane maximum flow above twice the single-lane value at density ≈ 0.08. Lane-change and ping-pong frequencies.
- **Reimplementability:** S1 2. S2 2. S3 0. S4 2. S5 2 → **8, B**. Assessed from: full text.
- **Browser fit:** Trivial. **Relevance to ca-geo:** MOV-02 multi-lane roads from OSM `lanes` tag.

### nagel1998twolane — Two-lane traffic rules for cellular automata: A systematic approach
- **Citation:** Nagel, K., Wolf, D.E., Wagner, P., Simon, P. (1998). Two-lane traffic rules for cellular automata: A systematic approach. *Physical Review E* 58(2), 1425–1437. DOI: 10.1103/physreve.58.1425 (verified: OpenAlex/Crossref)
- **Access:** OA, arXiv cond-mat/9712196.
- **Phenomenon and study area:** Lane-changing rules and density inversion.
- **Model:** General scheme for lane-change rules on top of NaSch, tested with several rule sets.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 2. S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Trivial. **Relevance to ca-geo:** MOV-02. Theory behind the rickert1996two rules.

### biham1992selforganization — Self-organization and a dynamical transition in traffic-flow models
- **Citation:** Biham, O., Middleton, A.A., Levine, D. (1992). Self-organization and a dynamical transition in traffic-flow models. *Physical Review A* 46(10), R6124–R6127. DOI: 10.1103/physreva.46.r6124 (verified: Crossref)
- **Access:** OA, arXiv cond-mat/9206001.
- **Phenomenon and study area:** Abstract city grid. Sharp jamming transition.
- **Model:** 2D torus with two car species (east-bound and north-bound). Species move on alternate steps, one cell if the target is empty. Deterministic apart from the random initial condition. Rules confirmed in maerivoet2005cellular §5.2.1.
- **Parameters:** Density only.
- **Code:** third-party, for example https://github.com/MaciekBaron/BMLTrafficJS (JavaScript) and https://github.com/kdelrosso/traffic-flow-sim (verified URLs).
- **Validation:** Transition from free flow to global gridlock at a critical density.
- **Reimplementability:** S1 2. S2 2. S3 1. S4 2. S5 2 → **9, A**. Assessed from: abstract + review full text.
- **Browser fit:** Trivial. Ideal as a teaching demo.
- **Relevance to ca-geo:** MOV-02 conceptual demo. Not geographic as such, but it is the bridge from 2D raster CA to traffic.

### chowdhury1999selforganization — Self-organization of traffic jams in cities: Effects of stochastic dynamics and signal periods
- **Citation:** Chowdhury, D., Schadschneider, A. (1999). Self-organization of traffic jams in cities: Effects of stochastic dynamics and signal periods. *Physical Review E* 59(2), R1311–R1314. DOI: 10.1103/physreve.59.r1311 (verified: Crossref)
- **Access:** OA, arXiv cond-mat/9810099.
- **Phenomenon and study area:** Gridlock in a signalised Manhattan grid.
- **Model:** N × N grid of crossings with D cells between them. Streets run NaSch rules (V = 0..Vmax, random slowdown p). Signals are synchronised: green for one direction for T steps, then the other. No turning, periodic boundaries. Cars may roll up to a red crossing.
- **Parameters:** Given, for example Vmax = 5, p = 0.1, D = 100, T = 20/100, density c.
- **Code:** not found.
- **Validation:** Mean speed over time in green/red phases, an analytical approximation, and a jamming transition c*(D, T).
- **Reimplementability:** S1 2. S2 2. S3 0. S4 2. S5 2 → **8, B**. Assessed from: full text.
- **Browser fit:** Trivial.
- **Relevance to ca-geo:** MOV-02. The minimal signalised-network CA. Could be laid over an OSM street grid with signal nodes.

### chopard1996cellular — Cellular automata model of car traffic in a two-dimensional street network
- **Citation:** Chopard, B., Luthi, P.O., Queloz, P.-A. (1996). Cellular automata model of car traffic in a two-dimensional street network. *Journal of Physics A: Mathematical and General* 29(10), 2325–2336. DOI: 10.1088/0305-4470/29/10/012 (verified: Crossref)
- **Access:** OA via UNIGE archive (archive-ouverte.unige.ch/unige:121437; not opened).
- **Phenomenon and study area:** Manhattan-like city. Queue dynamics.
- **Model:** Cars move in four directions. Crossings are rotary junctions, with turning strategies as parameters.
- **Validation:** Flow diagrams and density profiles, compared with a continuous simulation.
- **Reimplementability:** S1 1. S2 1. S3 0. S4 2. S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Browser fit:** Trivial. **Relevance to ca-geo:** MOV-02. A roundabout-junction rule as an alternative to signals.

### esser1997microscopic — Microscopic Simulation of Urban Traffic Based on Cellular Automata
- **Citation:** Esser, J., Schreckenberg, M. (1997). Microscopic Simulation of Urban Traffic Based on Cellular Automata. *International Journal of Modern Physics C* 8(5), 1025–1036. DOI: 10.1142/s0129183197000904 (verified: Crossref)
- **Access:** paywall.
- **Phenomenon and study area:** Urban road network (Duisburg, Germany, EU).
- **Model:** NaSch on links. Roads and crossings of any kind are composed from a few basic elements. Parking and public transport are included. Vehicles follow route plans or random turning.
- **Inputs:** Real network, signal plans, route data. **Parameters:** not seen. **Code:** not found.
- **Validation:** Application to the city network (details not seen).
- **Reimplementability:** S1 1. S2 1. S3 0. S4 1. S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Feasible for a city district.
- **Relevance to ca-geo:** MOV-02 **EU real-network template**: the building-block approach for turning OSM ways and junctions into NaSch lattices.

### nagel2001parallel — Parallel implementation of the TRANSIMS micro-simulation
- **Citation:** Nagel, K., Rickert, M. (2001). Parallel implementation of the TRANSIMS micro-simulation. *Parallel Computing* 27(12), 1611–1639. DOI: 10.1016/s0167-8191(01)00106-5 (verified: Crossref)
- **Access:** OA, arXiv cs/0105004.
- **Phenomenon and study area:** Regional-scale network traffic. TRANSIMS uses a CA micro-simulation on links.
- **Model:** CA traffic on a partitioned network graph, with domain decomposition, boundary exchange and adaptive load balancing. Includes a performance prediction model.
- **Code:** TRANSIMS was released as open source (SourceForge project page returned 403 to automated checks, so **not verified**).
- **Reimplementability:** S1 1. S2 1. S3 0. S4 1. S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** The parallel design is irrelevant at browser scale, but the link/node CA structure is relevant.
- **Relevance to ca-geo:** MOV-02 at city/region scale. Shows that CA traffic scales to real networks.

### Accessibility and travel-time fronts

### duff2015using — Using discrete event simulation cellular automata models to determine multi-mode travel times and routes of terrestrial suppression resources to wildland fires
- **Citation:** Duff, T.J., Chong, D.M., Tolhurst, K.G. (2015). Using discrete event simulation cellular automata models to determine multi-mode travel times and routes of terrestrial suppression resources to wildland fires. *European Journal of Operational Research* 241(3), 763–770. DOI: 10.1016/j.ejor.2014.09.019 (verified: Crossref; erratum 10.1016/j.ejor.2015.03.025)
- **Access:** paywall.
- **Phenomenon and study area:** Travel time of fire-suppression vehicles from bases to fires (Australia), on and off road.
- **Model:** Raster cost-distance computed with a discrete-event CA. A front spreads outward from the fire cell, each cell records its arrival time and a parent, and the fastest route is traced back along the parent chain.
- **Inputs:** Road network and terrain/vegetation rasters (generic). **Parameters:** speeds per surface (not seen). **Code:** not found.
- **Validation:** Matches network analysis on roads. Plausible routes in complex terrain.
- **Reimplementability:** S1 1. S2 0. S3 0. S4 2. S5 1 → **4, C**. Assessed from: abstract (provisional).
- **Browser fit:** Very good. A priority-queue front over a raster.
- **Relevance to ca-geo:** **MOV-03 core**. It is the same "front over a cost raster" mechanism as fire spread (a discrete-event CA in the PHOENIX lineage) and directly supports chain L12 (accessibility of emergency services). Overlaps with `fire`.

### wood2012anisotropic — Anisotropic path modeling to assess pedestrian-evacuation potential from Cascadia-related tsunamis in the US Pacific Northwest
- **Citation:** Wood, N.J., Schmidtlein, M.C. (2012). Anisotropic path modeling to assess pedestrian-evacuation potential from Cascadia-related tsunamis in the US Pacific Northwest. *Natural Hazards* 62(2), 275–300. DOI: 10.1007/s11069-011-9994-2 (verified: Crossref; online 2011, print 2012)
- **Access:** OA (Springer). Automated access redirected to login.
- **Phenomenon and study area:** Pedestrian evacuation time to high ground before tsunami arrival, Long Beach Peninsula, Washington, USA.
- **Model:** Least-cost path distance on a raster. Travel cost depends on land cover and on slope direction, so uphill and downhill differ. Not a CA as such, but a cost-distance front equivalent to the MOV-03 mechanism.
- **Inputs:** Elevation (several resolutions, including lidar), land cover, safe-zone boundary. **Parameters:** travel speeds (varied in sensitivity tests). **Code:** ArcGIS path-distance tool (closed). The USGS Pedestrian Evacuation Analyst page returned 403 and was not verified.
- **Validation:** Sensitivity of travel times and exposed population to resolution and speed assumptions.
- **Reimplementability:** S1 1. S2 1. S3 1. S4 2. S5 1 → **6, C**. Assessed from: abstract (provisional).
- **Browser fit:** Very good.
- **Relevance to ca-geo:** MOV-03 + MOV-01 on a DEM. Direct template for "time to safe ground" maps from a flood extent (HYD-02) or other hazard. CZ DEM (DMR 5G) and land cover would fit.

### weiss2018global — A global map of travel time to cities to assess inequalities in accessibility in 2015
- **Citation:** Weiss, D.J., Nelson, A., Gibson, H.S., Temperley, W., Peedell, S., Lieber, A., Hancher, M., Poyart, E. et al. (2018). A global map of travel time to cities to assess inequalities in accessibility in 2015. *Nature* 553(7688), 333–336. DOI: 10.1038/nature25181 (verified: OpenAlex/Crossref)
- **Access:** Author version in a repository (U. Twente, per Semantic Scholar). The Nature page needs a login.
- **Phenomenon and study area:** Global accessibility (travel time to the nearest city).
- **Model:** About 1 km friction raster (minutes per metre) built from roads (OSM, Google), rail, rivers, water bodies, land cover, slope, elevation and borders. Least-cost accumulation from city cells (Google Earth Engine; R for high latitudes). Not a CA, but the same front mechanism.
- **Inputs:** Open global layers. **Parameters:** speed tables (in supplementary material; not seen).
- **Code / data:** Friction surface and accessibility GeoTIFFs in DANS (https://doi.org/10.17026/dans-ztx-2sd2, verified 200). Earth Engine assets `Oxford/MAP/friction_surface_2015_v1_0` and `Oxford/MAP/accessibility_to_cities_2015_v1_0` (catalog pages verified 200). No standalone code repository found.
- **Validation:** Comparison with Google Maps travel times (as reported in summaries; not checked).
- **Reimplementability:** S1 1. S2 1. S3 1. S4 2. S5 2 – the open output raster is a direct reference → **7, B**. Assessed from: abstract + web summaries (provisional).
- **Browser fit:** Good for a regional clip (e.g. CZ at 1 km is about 80 000 cells).
- **Relevance to ca-geo:** MOV-03. The open friction surface is a ready-made cost raster, and its accessibility map is a benchmark for our own front-propagation CA.

### Reviews and entry points

### chowdhury2000statistical — Statistical physics of vehicular traffic and some related systems
- **Citation:** Chowdhury, D. et al. (2000). Statistical physics of vehicular traffic and some related systems. *Physics Reports* 329(4–6), 199–329. DOI: 10.1016/s0370-1573(99)00117-9 (verified: Crossref. Crossref lists only the first author. The arXiv version cond-mat/0007053 should be checked for the full author list before final citation.)
- **Access:** OA, arXiv cond-mat/0007053.
- **Reimplementability:** n/a. A large review of particle-hopping/CA traffic models (NaSch family, BML-type city models) with analytical results. It also covers related systems such as pedestrians and ant trails. It is the main entry point for the physics side of MOV-02.

### maerivoet2005cellular — Cellular automata models of road traffic
- **Citation:** Maerivoet, S., De Moor, B. (2005). Cellular automata models of road traffic. *Physics Reports* 419(1), 1–64. DOI: 10.1016/j.physrep.2005.08.005 (verified: OpenAlex/Crossref)
- **Access:** OA, arXiv physics/0509082.
- **Reimplementability:** n/a. Full text read. It gives consistent notation and explicit rule sets for CA-184, deterministic and stochastic Fukui–Ishibashi, NaSch (STCA), TASEP, Emmerich–Rank, slow-to-start variants (T², BJH, VDR, TOCA), multi-cell models (brake-light/Knospe, KKW), lane changing, city grid models (BML, ChSch) and explicit intersections. It also covers measurement procedures and conversion to real units. **This is the best single source for implementing MOV-02.** It notes that most network applications lack calibration of intersection delays.

### schadschneider2009evacuation — Evacuation Dynamics: Empirical Results, Modeling and Applications
- **Citation:** Schadschneider, A., Klingsch, W., Klüpfel, H., Kretz, T., Rogsch, C., Seyfried, A. (2009). Evacuation Dynamics: Empirical Results, Modeling and Applications. In *Encyclopedia of Complexity and Systems Science*, 3142–3176. DOI: 10.1007/978-0-387-30440-3_187 (verified: Crossref)
- **Access:** paywall (there is a 2011 reprint, DOI 10.1007/978-1-4419-7695-6_29).
- **Reimplementability:** n/a. A review of empirical pedestrian data (fundamental diagrams, bottleneck flows) and model classes, FFCA included. Useful for choosing reference values (speeds, specific flows) to validate MOV-01.

### zheng2009modeling — Modeling crowd evacuation of a building based on seven methodological approaches
- **Citation:** Zheng, X., Zhong, T., Liu, M. (2009). Modeling crowd evacuation of a building based on seven methodological approaches. *Building and Environment* 44(3), 437–445. DOI: 10.1016/j.buildenv.2008.04.002 (verified: Crossref)
- **Access:** paywall.
- **Reimplementability:** n/a. A comparative overview of seven evacuation modelling approaches, CA and lattice gas among them. Useful for situating CA against social-force and agent-based models.

### pelechano2008evacuation — Evacuation simulation models: Challenges in modeling high rise building evacuation with cellular automata approaches
- **Citation:** Pelechano, N., Malkawi, A. (2008). Evacuation simulation models: Challenges in modeling high rise building evacuation with cellular automata approaches. *Automation in Construction* 17(4), 377–385. DOI: 10.1016/j.autcon.2007.06.005 (verified: Crossref)
- **Access:** OA (UPC repository hdl.handle.net/2117/11066, per Semantic Scholar; not opened).
- **Reimplementability:** n/a. A critical view of the limits of CA evacuation tools (grid artefacts, behaviour). Useful for stating the limitations of a browser CA demo.

## Most reimplementable (top picks)

1. **nagel1992cellular (A, 9).** Four-line rule, standard parameters, analytical checks. The baseline for MOV-02 on OSM links.
2. **biham1992selforganization (A, 9).** A 2D grid traffic CA with a sharp jamming transition. An ideal browser demo and test case.
3. **kirchner2002simulation (B, 8).** The canonical FFCA with full parameters and evacuation-time curves. The reference for MOV-01.
4. **kirchner2003friction (B, 8).** Adds one parameter (μ) for realistic clogging at bottlenecks.
5. **knospe2000towards (B, 8).** Complete parameter set, calibrated against empirical motorway data.
6. **chowdhury1999selforganization (B, 8).** The minimal signalised city-network CA with parameters.
7. **rickert1996two (B, 8).** Explicit two-lane rules with parameters.
8. **weiss2018global (B, 7).** Not a CA, but an open friction raster and a reference output for MOV-03.

For geographic evacuation (MOV-01 on real maps), no single verified paper scores B or
better. The practical route is to combine the FFCA rules (kirchner2002/2003) with a static
field computed as an anisotropic cost-distance on a DEM and land cover (the
wood2012anisotropic / duff2015using mechanism), plus hazard-driven extra floor fields
(zheng2019simulation).

## Gaps and unverified leads

- **Tooling problem:** OpenAlex was rate-limited (daily budget exhausted) for most of the
  round, and publisher pages blocked automated reads. Re-run the OpenAlex queries in round
  2 for citation counts and OA links. Read the full texts of nowak2012quantitative,
  barlovic1998metastable, nagel1998twolane, chopard1996cellular and nagel2001parallel
  (all on arXiv or OA) to raise their provisional scores.
- **Metadata-only entries** (blue2001cellular, muramatsu1999jamming, guo2008mobile,
  guo2013modeling, varas2007cellular, lovreglio2015calibrating) need at least their
  abstracts checked.
- **True CA evacuation on real geography (tsunami, flood, wildfire) is rare.** Tsunami and
  flood evacuation studies found are mainly least-cost-distance or agent-based (e.g.
  MATSim). Leads not yet verified: Soga, Comfort, Zhao, Lorusso, Soysal (2021) UC
  Berkeley ITS report coupling a CA fire-spread model with spatial-queue evacuation
  traffic for Paradise and Bolinas, CA (no DOI found in Crossref); Kita et al. 2014 IEEE
  CANDAR "Traffic Network Design for Disaster Evacuation by Cellular Automata Simulation"
  (DOI 10.1109/candar.2014.31, seen in Crossref but not assessed); Lämmel, Rieser, Nagel
  2009 "Large Scale Microscopic Evacuation Simulation" (PED 2008, DOI
  10.1007/978-3-642-04504-2_48, queue-based, not CA).
- **Review with an implementation guide:** Toprakli (2024), "A Review and Implementation
  Guide for Basic Cellular Automata Models in Pedestrian Evacuation Simulation", Gazi
  University Journal of Science Part B. Seen on the web, **not found in Crossref**, so
  unverified.
- **Code:** no author-published open FFCA or lattice-gas code was found. Vadere (GPLv3,
  gitlab.lrz.de/vadere/vadere, verified 200; paper DOI 10.17815/cd.2019.21) implements
  optimal-steps, gradient-navigation and social-force models; no CA was confirmed.
  JuPedSim (github.com/PedestrianDynamics/jupedsim, verified 200) is not CA-based.
  TRANSIMS source (SourceForge) could not be verified (HTTP 403).
- **CZ/EU:** No Czech CA traffic or evacuation paper was found. T. Potuzak (ZČU Plzeň)
  publishes on distributed road traffic simulation and network division (e.g. DOI
  10.1109/ds-rt55542.2022.9932112). Check in round 2 whether his traffic model is
  NaSch-based. EU items: esser1997microscopic (Duisburg) and the Duisburg/NRW online
  traffic simulation (Wahle et al. 1998, DOI 10.1007/978-1-4471-1281-5_17; Santen et al.
  1998, DOI 10.1016/b978-008043430-8/50029-0), not assessed.
- **Further families for round 2:** Kretz & Schreckenberg F.A.S.T. model (DOI
  10.1007/11861201_85, multi-speed FFCA); Nishinari et al. extended FFCA (DOI
  10.1007/3-540-28091-x_40); Daganzo 2006 "In traffic flow, cellular automata = kinematic
  waves" (DOI 10.1016/j.trb.2005.05.004, OA); synchronized-flow CA review Tian et al.
  2020 (DOI 10.1080/23249935.2020.1810820); Adamatzky 1996 shortest path in CA (DOI
  10.1016/0895-7177(96)00006-4) as theory for MOV-03; Tobler's hiking function as a
  slope–speed rule (find a citable, verifiable source).
- **Overlaps:** `fire` (duff2015using, guo2013modeling, liu2023cellular, WUI fire–evacuation
  coupling); `hyd` (zheng2019simulation, flood → evacuation chain L12); `gen`
  (lovreglio2015calibrating calibration, dang2021chain visualisation,
  maerivoet2005cellular as a CA methods review); `eco` (front over a cost raster also used
  for animal dispersal, ECO-04).
