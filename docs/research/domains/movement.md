# Movement of people and vehicles — literature survey

Survey rounds: 1 (breadth-first, 2026-10-12), 2 (deepening, 2026-10-12). Scoring per ../reimplementability-criteria.md.
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

### Round 2

OpenAlex was still quota-blocked; searches and metadata checks used Crossref (paced, occasional HTTP 429 retried) and Semantic Scholar. Full texts came from arXiv, Springer OA PDFs, Nature OA PDFs, MDPI (in-app browser), IntechOpen and an author PDF at VUT Brno. HAL (Anubis check), ScienceDirect (CAPTCHA) and the U. Twente repository (Cloudflare check) blocked access; we did not try to get past these checks. Downloaded PDFs stayed in the agent scratchpad and were deleted after text extraction.

| Query | Source | Hits | Notes |
|---|---|---|---|
| OA-PDF lookup: NaSch, BML, Wood 2012, Zheng 2019, Weiss 2018 | Semantic Scholar | 5 | BML (arXiv) and Wood 2012 (Springer OA) read. NaSch (HAL) and Weiss 2018 (U. Twente) blocked by bot checks. Zheng 2019 closed. |
| Full text: Liu 2023 | MDPI (in-app browser) | 1 | Read, including speed-reduction equations. |
| `Potuzak road traffic simulation cellular automaton`; `Potuzak distributed traffic simulation Nagel Schreckenberg` | Crossref; Semantic Scholar | 6 + 6 | ZČU papers are on network division and communication protocols for distributed simulation. The 2026 OA paper was read: it uses a static traffic-assignment benchmark, no CA. Lead closed. |
| `Potuzak … Nagel-Schreckenberg … West Bohemia` | web search | – | No ZČU CA link. Found CZ work at VUT Brno instead: Korček, Sekanina & Fučík (CA traffic, calibrated on Czech road data), a VUT CA traffic simulator (software result) and a VUT bachelor thesis on NaSch. |
| `Korcek cellular automata traffic simulation GPU` | Crossref | 3 relevant | Korček et al. 2011 (IEEE IV), 2012 (ITSC; author PDF read), 2012 (LNCS, travel-time calibration, not assessed). |
| `Toprakli … cellular automata … pedestrian evacuation` (3 variants) | Crossref | 0 | Still not in Crossref. Found on the Gazi University portal (journal article, 2024); stays an unverified lead. |
| `cellular automata tsunami evacuation real map`; `… flood evacuation residents town`; `floor field … GIS urban area earthquake shelter`; `… OpenStreetMap city scale` | Crossref | ranked | No CA evacuation on real city maps beyond round-1 items. Arai et al. 2011 (NaSch-based evacuation traffic, Sidoarjo mudflow, Indonesia) added. |
| `cellular automata wildfire evacuation traffic coupled` | Crossref | ranked | Kita 2014 (already a lead), Arai 2011, Li, Cova & Dennison 2018 (fire + traffic coupling, not CA; not assessed). |
| `cellular automaton accessibility … travel time`; Weiss 2020 / Nelson 2019 lookups | Crossref; Nature OA | ranked | Weiss 2020 (healthcare travel time) and Nelson 2019 (accessibility suite with open R code) read; both cost-distance fronts, not CA. |
| `Was Lubas cellular automata crowd …`; `Bazior Palka Was …`; `Porzycki … stadium` | Crossref | 3 + 3 + 3 | AGH Kraków (PL) CA crowd group: Lubaś 2016 (Allianz Arena stadium model), Bazior 2020 (multi-cell pedestrians), Porzycki 2014 (NIST TN 1822 tests applied to CA). |
| `wildlife vehicle collision cellular automaton road` | Crossref | ranked | No CA found. Bénard et al. 2023 (individual-based model, bioRxiv) noted as a new-phenomenon reference. |
| `cellular automata crowd mass event festival stadium` | Crossref | ranked | Carneiro 2013 (stadium CA, not assessed), Lubaś 2016. |

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
3. **Single-lane stochastic traffic CA.** Round 2 CZ example: an extended NaSch with ten
   parameters calibrated by a genetic algorithm on Czech road data (`korcek2012evolutionary`). NaSch: acceleration, braking to the gap,
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
   Round 2: `nelson2019suite` (open R scripts with gdistance) and `weiss2020global` (walking-only
   and motorised friction surfaces) are fully open versions of the Weiss 2018 method.
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
| biham1992selforganization | 1992 | BML city traffic | 2D grid jamming | 2D torus, 2 species, alternate update; deterministic | 2 2 1 2 2 | 9 | A | third-party JS | OA (arXiv) | full text (r2) |
| kirchner2002simulation | 2002 | Bionics FFCA evacuation | room evacuation | 2D 0.4 m, Moore, static+dynamic field; stochastic parallel | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| kirchner2003friction | 2003 | Friction & clogging in FFCA | bottleneck clogging | as above + friction μ | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| rickert1996two | 1996 | Two-lane CA traffic | multi-lane traffic | 2 × 1D NaSch + lane-change sub-step; stochastic | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| knospe2000towards | 2000 | Brake-light (comfortable driving) CA | highway traffic phases | 1D, 1.5 m cells, vmax 20, brake lights, anticipation; stochastic | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| chowdhury1999selforganization | 1999 | ChSch city CA | urban grid with signals | 2D street lattice, NaSch on links, signals period T | 2 2 0 2 2 | 8 | B | not found | OA (arXiv) | full text |
| weiss2018global | 2018 | Global travel time to cities | accessibility | 1 km friction raster, least-cost front from cities | 1 1 1 2 2 | 7 | B | GEE assets (closed platform); data open | OA (repository) | abstract + web summary (provisional) |
| burstedde2001simulation | 2001 | 2D CA pedestrian dynamics | lane formation, evacuation | 2D 0.4 m, Moore, preference matrix + floor fields | 2 1 0 2 1 | 6 | C | not found | OA (arXiv) | full text |
| nowak2012quantitative | 2012 | FFCA counterflow | bidirectional flow | FFCA, 2 species, anticipation | 1 1 0 2 2 | 6 | C | not found | OA (arXiv) | abstract (provisional) |
| wood2012anisotropic | 2012 | Anisotropic path tsunami evacuation | tsunami pedestrian evacuation time | raster least-cost, slope-direction anisotropy (Tobler) | 2 2 1 2 1 | 8 | B | closed (ArcGIS tool) | OA (Springer) | full text (r2) |
| nagel1998twolane | 1998 | Systematic two-lane rules | lane changing | NaSch + lane-change scheme | 1 1 0 2 1 | 5 | C | not found | OA (arXiv) | abstract (provisional) |
| barlovic1998metastable | 1998 | VDR slow-to-start | metastability, hysteresis | NaSch with velocity-dependent p | 1 1 0 2 1 | 5 | C | not found | OA (arXiv) | abstract (provisional) |
| chopard1996cellular | 1996 | CA street network with rotaries | Manhattan city traffic | 2D street lattice, rotary junctions | 1 1 0 2 1 | 5 | C | not found | OA (UNIGE repository) | abstract (provisional) |
| liu2023cellular | 2023 | CA evacuation with fire products | building fire evacuation | 0.4 m Moore CA; dwell time scaled by visibility/CO factors from FDS | 1 1 0 1 2 | 5 | C | not found | OA (MDPI) | full text (r2) |
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
| nelson2019suite | 2019 | Global accessibility indicators (r2) | travel time to settlements of 9 size classes | 30″ friction raster, least-cost (gdistance); not CA | 2 1 2 2 2 | 9 | A | yes (R scripts, figshare) | OA | full text (r2) |
| weiss2020global | 2020 | Travel time to healthcare (r2) | accessibility to hospitals/clinics, motorised and walking | friction raster, Dijkstra (GEE / gdistance); not CA | 2 1 1 2 2 | 8 | B | stated on project page (not inspected) | OA | full text (r2) |
| korcek2012evolutionary | 2012 | GA calibration of CA traffic, CZ data (r2) | road traffic, Czech road segments | 1D, 7.5 m cells, extended NaSch (p1–p10) | 2 2 0 1 2 | 7 | B | not found | author PDF (VUT) | full text (r2) |
| placzek2010fuzzy | 2010 | Fuzzy cellular traffic model (r2) | queue discharge at signals (PL) | 1D cellular, fuzzy-number vehicle states | 1 1 0 2 1 | 5 | C | not found | preprint (arXiv 1112.4055) | abstract (provisional) |
| bazior2020using | 2020 | Multi-cell pedestrians, high density (r2) | dense crowds (PL) | 2D fine grid, pedestrian = several cells | 1 1 0 2 1 | 5 | C | not found | OA (Springer) | abstract (provisional) |
| korcek2011scalable | 2011 | Scalable CA traffic simulation (r2) | large networks, CZ group | 1D CA, bit-level states, smoother braking | 1 1 0 1 1 | 4 | C | not found (VUT software result, licence required) | paywall | abstract (provisional) |
| arai2011cellular | 2011 | CA evacuation traffic, Sidoarjo mudflow (r2) | vehicular evacuation from a disaster area (Indonesia) | NaSch-based, lane changing, driver types | 1 1 0 1 1 | 4 | C | not found | OA (IntechOpen) | full text (r2) |
| lubas2016cellular | 2016 | CA basis for crowd ABM, stadium (r2) | large-scale crowd (stadium) (PL) | non-homogeneous asynchronous CA + agents | 1 0 0 1 1 | 3 | D | not found | paywall | abstract via catalogue summary (provisional) |
| ronchi2013process | 2013 | NIST TN 1822 evacuation-model tests (r2) | verification & validation suite | — | n/a | — | n/a | — | OA (NIST) | full text (test list) |
| porzycki2014application | 2014 | NIST TN 1822 applied to CA (r2) | V&V of CA crowd models (PL) | — | n/a | — | n/a | — | paywall | metadata |
| vanetten2017gdistance | 2017 | R package gdistance (r2) | cost-distance on grids (software paper) | — | n/a | — | n/a | yes (CRAN) | OA | metadata |
| potuzak2026benchmark | 2026 | Road-network division benchmark, ZČU (r2) | distributed traffic simulation (CZ), not CA | — | n/a | — | n/a | yes (GitLab, RONDIBET) | OA | full text (r2) |

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
- **Round 2:** no OA copy found (Semantic Scholar: closed). Score unchanged.

### liu2023cellular — Cellular Automaton Model for Pedestrian Evacuation Considering Impacts of Fire Products
- **Citation:** Liu, Y., Li, J., Sun, C. (2023). Cellular Automaton Model for Pedestrian Evacuation Considering Impacts of Fire Products. *Fire* 6(8), 320. DOI: 10.3390/fire6080320 (verified: Crossref)
- **Access:** OA (MDPI). Round 2: full text read in the in-app browser.
- **Phenomenon and study area:** Single-room (13.2 × 10.4 m) and multi-room (38 × 18.4 m) building with a 4 MW fire.
- **Model:** CA evacuation in which walking speed and familiarity change over time with visibility and CO concentration. These are imported from FDS/Pyrosim smoke simulations, giving one-way coupling.
  - 0.4 m cells, Moore neighbourhood, free speed 1.2 m/s. Speed is turned into a dwell time per cell, ST = S / (v · f_s · f_CO).
  - Visibility factor f_s = min(1, max(0.2, 1 − 0.34·(3 − VIS))). CO factor f_CO is 1 below 0.1% CO, falls with concentration and exposure time between 0.1% and 0.25%, and is 0 above.
  - Visibility range uses a line-of-sight check against obstacles and the lowest visibility along the line. Unfamiliar pedestrians follow the densest visible cluster (density-peak clustering).
- **Inputs:** FDS output fields. **Parameters:** partly in the abstract (densities 0.1–0.5 p/m², CO yield). **Code:** not found.
- **Validation:** Quantitative scenario results (percentage changes in efficiency), not validated against data.
- **Reimplementability:** S1 1 – the speed coupling is explicit, but the movement rule and conflict handling are only sketched; S2 1; S3 0; S4 1; S5 2 – evacuation times for densities 0.1–0.5 in a table → **5, C**. Round 2: re-assessed from full text — score unchanged.
- **Browser fit:** The CA part fits. The FDS fields would have to be precomputed.
- **Relevance to ca-geo:** L12 pattern. Hazard-field → speed-reduction coupling, the same idea as using a gas plume (ATM-03) to slow or block evacuees. The f_s and f_CO factors are a ready formula for slowing evacuees in a smoke or gas raster.

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
- **Reimplementability:** S1 2. S2 2. S3 1 – third-party code only. S4 2. S5 2 → **9, A**. Assessed from: full text of review (maerivoet2005cellular) plus abstract. Round 2: the HAL copy is behind an automated-browser check (Anubis), which we did not try to pass; score unchanged.
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
- **Access:** OA, arXiv cond-mat/9206001. Round 2: full text read.
- **Phenomenon and study area:** Abstract city grid. Sharp jamming transition.
- **Model:** 2D torus with two car species (east-bound and north-bound). Species move on alternate steps, one cell if the target is empty (a blocked car does not move even if the blocker leaves in the same step). Deterministic apart from the random initial condition. Rules confirmed in maerivoet2005cellular §5.2.1. The paper also defines a stochastic variant without the alternating "traffic light" (random choice in conflicts; p_c ≈ 0.10 at 512 × 512) and an overlap variant with a continuous transition.
- **Parameters:** Density only.
- **Code:** third-party, for example https://github.com/MaciekBaron/BMLTrafficJS (JavaScript) and https://github.com/kdelrosso/traffic-flow-sim (verified URLs).
- **Validation:** Transition from free flow (v = 1) to global gridlock (v = 0) at a critical density, shown for 16 × 16 to 512 × 512 lattices; p_c(N) decreases with N and its infinite-size limit is left open. The 1D analogue has v = 1 for p < 1/2 and v = (1 − p)/p above.
- **Reimplementability:** S1 2. S2 2. S3 1. S4 2. S5 2 → **9, A**. Round 2: re-assessed from full text — scores confirmed (was assessed from abstract + review).
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
- **Access:** OA (Springer, CC BY-NC). Round 2: full text read.
- **Phenomenon and study area:** Pedestrian evacuation time to high ground before tsunami arrival, Long Beach Peninsula, Washington, USA.
- **Model:** Least-cost distance from the safe zone outward over a raster. Four variants are compared: straight-line, road-network only, isotropic slope + land cover, and anisotropic slope + land cover.
  - Each cell gets a "speed conservation value" (SCV, the fraction of maximum walking speed). Slope SCV comes from Tobler's hiking function, speed = 6·exp(−3.5·|slope + 0.05|) km/h, divided by its maximum. Land-cover SCV comes from Soule & Goldman terrain coefficients: Table 1 maps NLCD classes to values (roads 1.0; developed 0.91; forest, grass and crops 0.83; shrub 0.67; barren and wetlands 0.56; water impassable).
  - The anisotropic variant computes the slope between each cell and each neighbour and looks up the Tobler-based cost by direction. Because the search runs from safety into the hazard zone, the sign of the slope is reversed.
  - Distance surfaces are turned into time with a base speed of 1.1 m/s (15th percentile of walking speeds of a mixed population).
- **Inputs:** Lidar DEM (1 m, also coarser versions), land cover, roads, tsunami inundation line (safe-zone boundary), population.
- **Parameters:** All given (Tobler formula, SCV table, base speed). Sensitivity to DEM and land-cover resolution is tested.
- **Code:** ArcGIS Path Distance tool (closed). The USGS Pedestrian Evacuation Analyst page was not verified.
- **Validation:** Difference maps (minutes) between model variants and between resolutions; for example, in one resolution test half of the cells showed no change and 40% were overestimated by up to 15 min. No observed evacuation data.
- **Reimplementability:** S1 2 – complete cost model and direction handling; S2 2 – all values tabulated; S3 1 – closed tool only; S4 2 – DEM and land cover are generic; S5 1 – results are tied to local US data, so they cannot be reproduced exactly → **8, B** (was 6, C provisional). Round 2: re-assessed from full text — S1 2, S2 2 (were 1, 1).
- **Browser fit:** Very good. A Dijkstra or fast-marching front with 8 neighbours and a direction-dependent cost.
- **Relevance to ca-geo:** MOV-03 + MOV-01 on a DEM. The SCV table maps directly to CORINE / Urban Atlas classes, and Tobler plus the direction reversal is exactly what a "time to safe ground" front needs. Direct template for a flood (HYD-02) or fire (HAZ-01) evacuation-time map on CZ DMR 5G.

### weiss2018global — A global map of travel time to cities to assess inequalities in accessibility in 2015
- **Citation:** Weiss, D.J., Nelson, A., Gibson, H.S., Temperley, W., Peedell, S., Lieber, A., Hancher, M., Poyart, E. et al. (2018). A global map of travel time to cities to assess inequalities in accessibility in 2015. *Nature* 553(7688), 333–336. DOI: 10.1038/nature25181 (verified: OpenAlex/Crossref)
- **Access:** Author version in a repository (U. Twente, per Semantic Scholar). The Nature page needs a login.
- **Phenomenon and study area:** Global accessibility (travel time to the nearest city).
- **Model:** About 1 km friction raster (minutes per metre) built from roads (OSM, Google), rail, rivers, water bodies, land cover, slope, elevation and borders. Least-cost accumulation from city cells (Google Earth Engine; R for high latitudes). Not a CA, but the same front mechanism.
- **Inputs:** Open global layers. **Parameters:** speed tables (in supplementary material; not seen).
- **Code / data:** Friction surface and accessibility GeoTIFFs in DANS (https://doi.org/10.17026/dans-ztx-2sd2, verified 200). Earth Engine assets `Oxford/MAP/friction_surface_2015_v1_0` and `Oxford/MAP/accessibility_to_cities_2015_v1_0` (catalog pages verified 200). No standalone code repository found.
- **Validation:** Comparison with Google Maps travel times (as reported in summaries; not checked).
- **Reimplementability:** S1 1. S2 1. S3 1. S4 2. S5 2 – the open output raster is a direct reference → **7, B**. Assessed from: abstract + web summaries (provisional). Round 2: the U. Twente author copy is behind a Cloudflare check, so still not read. The method is restated in the OA follow-ups `nelson2019suite` and `weiss2020global`.
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

### Round 2 additions

### korcek2012evolutionary — Evolutionary approach to calibration of cellular automaton based traffic simulation models (round 2)
- **Citation:** Korcek, P., Sekanina, L., Fucik, O. (2012). Evolutionary approach to calibration of cellular automaton based traffic simulation models. In *2012 15th International IEEE Conference on Intelligent Transportation Systems*, 122–129. DOI: 10.1109/itsc.2012.6338759 (verified: Crossref)
- **Access:** author PDF at VUT Brno FIT (https://www.fit.vut.cz/research/publication-file/9898/itsc2012.pdf). Round 2: full text read (text extraction; tables partly garbled).
- **Phenomenon and study area:** Road traffic on three Czech road sections measured by detectors in 2010 (data from industrial partners): among them a winding segment with a 50 km/h limit and a section with climbing lanes; a 130 km/h motorway limit is also mentioned (the extracted text is partly garbled). **CZ study.**
- **Model:** Single-lane CA in the NaSch family with 7.5 m cells and a step of 0.6–1.5 s. The authors' earlier update (`korcek2011scalable`) adds parameters p1–p10 to the transition function, for example probabilistic acceleration and anticipation of the leader's speed, so that a car cannot drop from top speed to zero in one step. Pseudocode of the updated rule is given.
- **Calibration:** A genetic algorithm (population of 60, up to 125 000 iterations) fits the CA parameters and traffic-stream parameters. The objective is the normalised orthogonal distance between simulated and measured flow–speed–density points, using the Van Aerde functional form.
- **Inputs:** Detector flow, speed and occupancy (not public); road geometry.
- **Parameters:** Table I lists the model parameters; Table III gives the evolved values and per-point errors for each data set.
- **Code:** not found (the simulator is a VUT software result that requires a licence; see gaps).
- **Validation:** About 20% lower error than a manually tuned model; fundamental diagrams compared with field data.
- **Reimplementability:** S1 2; S2 2 – values per data set; S3 0; S4 1 – detector data not public, but the method runs on any loop-detector series (e.g. Czech national traffic information system data, to be checked); S5 2 → **7, B**. Assessed from: full text.
- **Browser fit:** Easy; the GA calibration would run offline or in a Web Worker.
- **Relevance to ca-geo:** MOV-02. The only verified CA traffic study calibrated on Czech data. Gives a reference parameter set for Czech motorway and urban traffic.

### korcek2011scalable — A scalable cellular automata based microscopic traffic simulation (round 2)
- **Citation:** Korcek, P., Sekanina, L., Fucik, O. (2011). A scalable cellular automata based microscopic traffic simulation. In *2011 IEEE Intelligent Vehicles Symposium (IV)*, 13–18. DOI: 10.1109/ivs.2011.5940393 (verified: Crossref)
- **Access:** paywall (IEEE). Abstract from the VUT FIT publication record.
- **Phenomenon and study area:** Very large road networks (VUT Brno group, CZ).
- **Model:** CA traffic model extended to avoid unrealistic stops from top speed in one step; bit-level state encoding for memory efficiency; OpenMP parallel version with near-linear speed-up.
- **Validation:** Compared with fundamental diagrams.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: abstract (provisional). The rule is restated in `korcek2012evolutionary`.
- **Relevance to ca-geo:** MOV-02 background for the CZ calibration paper; bit-packing idea for large browser networks.

### placzek2010fuzzy — Fuzzy Cellular Model for On-Line Traffic Simulation (round 2)
- **Citation:** Płaczek, B. (2010). Fuzzy Cellular Model for On-Line Traffic Simulation. In *Lecture Notes in Computer Science* (PPAM 2009), 553–560. DOI: 10.1007/978-3-642-14403-5_59 (verified: Crossref)
- **Access:** preprint on arXiv (1112.4055).
- **Phenomenon and study area:** Queue discharge at a signal, for on-line traffic control (Polish author).
- **Model:** Cellular traffic model in which vehicle parameters are fuzzy numbers, to carry input uncertainty into the result. Compared with NaSch.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** MOV-02 variant. Low priority; shows a Central European line of CA traffic work.

### bazior2020using — Using Cellular Automata to Model High Density Pedestrian Dynamics (round 2)
- **Citation:** Bazior, G., Pałka, D., Wąs, J. (2020). Using Cellular Automata to Model High Density Pedestrian Dynamics. In *Lecture Notes in Computer Science* (ICCS 2020), 486–498. DOI: 10.1007/978-3-030-50371-0_36 (verified: Crossref)
- **Access:** OA (Springer).
- **Phenomenon and study area:** Very dense crowds (AGH Kraków group, PL).
- **Model:** A pedestrian occupies several small cells, with shapes for a person with a backpack, a wheeled suitcase or a bicycle, instead of one 0.4 m cell. Movement mechanisms are defined for these shapes.
- **Reimplementability:** S1 1, S2 1, S3 0, S4 2, S5 1 → **5, C**. Assessed from: abstract (provisional).
- **Relevance to ca-geo:** MOV-01 at high density (mass events). Shows how to go beyond one-person-per-cell FFCA.

### lubas2016cellular — Cellular Automata as the basis of effective and realistic agent-based models of crowd behavior (round 2)
- **Citation:** Lubaś, R., Wąs, J., Porzycki, J. (2016). Cellular Automata as the basis of effective and realistic agent-based models of crowd behavior. *The Journal of Supercomputing* 72(6), 2170–2196. DOI: 10.1007/s11227-016-1718-7 (verified: Crossref)
- **Access:** paywall. Abstract seen only as a catalogue summary (CoMSES).
- **Phenomenon and study area:** Large-scale crowd simulation, applied to a model of the Allianz Arena stadium (Munich) (AGH Kraków group, PL).
- **Model:** Non-homogeneous, asynchronous CA combined with agents; architecture, synchronisation, object hierarchy and a new conflict-resolution method for agents.
- **Reimplementability:** S1 1, S2 0, S3 0, S4 1, S5 1 → **3, D**. Assessed from: abstract via catalogue summary (provisional).
- **Relevance to ca-geo:** New-phenomenon lead (crowds at mass events). Related: Porzycki et al. (2014) applied the NIST TN 1822 tests to CA crowd models (`porzycki2014application`).

### arai2011cellular — Cellular Automata for Traffic Modelling and Simulations in a Situation of Evacuation from Disaster Areas (round 2)
- **Citation:** Arai, K., Harsono, T., Basuki, A. (2011). Cellular Automata for Traffic Modelling and Simulations in a Situation of Evacuation from Disaster Areas. In *Cellular Automata – Simplicity Behind Complexity* (InTech). DOI: 10.5772/15769 (verified: Crossref)
- **Access:** OA (IntechOpen). Round 2: full text read (text extraction).
- **Phenomenon and study area:** Vehicle evacuation from the area of the Sidoarjo (LUSI) hot mudflow, East Java, Indonesia.
- **Model:** NaSch-based stochastic traffic CA with lane changing and a modified car-following term that separates "usual" and "diligent" drivers; an optimal-velocity continuous model is discussed alongside.
- **Inputs:** Road segment geometry; a 24-hour speed survey on the Porong road (speed distributions by vehicle type).
- **Parameters:** Survey distributions given; several CA parameters are left as tuning weights.
- **Code:** not found.
- **Validation:** Survey statistics; evacuation-time scenarios (qualitative to semi-quantitative).
- **Reimplementability:** S1 1, S2 1, S3 0, S4 1, S5 1 → **4, C**. Assessed from: full text.
- **Relevance to ca-geo:** Chain L12 (hazard → vehicle evacuation on a real road). Weakly specified, but one of the few CA traffic studies tied to a real hazard zone.

### nelson2019suite — A suite of global accessibility indicators (round 2)
- **Citation:** Nelson, A., Weiss, D.J., van Etten, J., Cattaneo, A., McMenomy, T.S., Koo, J. (2019). A suite of global accessibility indicators. *Scientific Data* 6, 266. DOI: 10.1038/s41597-019-0265-5 (verified: Crossref)
- **Access:** OA. Round 2: full text read (methods and code sections).
- **Phenomenon and study area:** Travel time from every location to the nearest settlement in nine size classes (from 5 000 people to 5 million), global, 2015, about 1 km resolution.
- **Model:** Not a CA. Least-cost accumulation over the Weiss 2018 friction surface (time to cross one metre). The R package gdistance builds an 8-neighbour transition matrix of conductances (mean of neighbouring pixel values, inverted from resistance) and accumulates cost from source pixels. Processing runs zone by zone because of raster size.
- **Inputs:** The open 2015 friction surface and settlement point/extent data.
- **Parameters:** Friction values come from Weiss 2018 (supplementary speed tables not seen); processing steps are fully described.
- **Code:** R scripts for the layers and for validation on figshare, DOI 10.6084/m9.figshare.7638134.v3 (resolves).
- **Validation:** Compared with travel times from a routing API (validation scripts included). The nine output rasters are open.
- **Reimplementability:** S1 2; S2 1; S3 2; S4 2; S5 2 → **9, A**. Assessed from: full text. Not a CA, but the same front mechanism as MOV-03.
- **Browser fit:** Good for a CZ clip at 1 km (about 80 000 cells).
- **Relevance to ca-geo:** MOV-03 benchmark. Clip the open rasters to CZ and compare with a browser front on the same friction surface.

### weiss2020global — Global maps of travel time to healthcare facilities (round 2)
- **Citation:** Weiss, D.J., Nelson, A., Vargas-Ruiz, C.A., Gligorić, K., Bavadekar, S., Gabrilovich, E. et al. (2020). Global maps of travel time to healthcare facilities. *Nature Medicine* 26(12), 1835–1838. DOI: 10.1038/s41591-020-1059-1 (verified: Crossref)
- **Access:** OA. Round 2: full text read (methods).
- **Phenomenon and study area:** Travel time to the nearest hospital or clinic, global, with and without motorised transport. Facility locations from OpenStreetMap, Google Maps and academic sources.
- **Model:** Not a CA. Dijkstra least-cost on gridded friction surfaces (Google Earth Engine `cumulativeCost`, R gdistance `accCost`). In the walking-only surface every road is walked at 5 km/h and water is crossed at 1 km/h.
- **Parameters:** Speed assignments per surface type are in the supplementary material (not seen).
- **Code / data:** Friction surfaces and travel-time maps as GeoTIFF; the paper states that source code is at https://malariaatlas.org/research-project/accessibility_to_healthcare/ (page checked 200, code not inspected).
- **Validation:** Population shares within one hour (8.9% cannot reach care within 1 h with motorised transport, 43.3% on foot).
- **Reimplementability:** S1 2; S2 1; S3 1 – code location stated but not verified; S4 2; S5 2 – open output rasters → **8, B**. Assessed from: full text.
- **Relevance to ca-geo:** MOV-03 "emergency service reach". The walking-only friction surface is a ready input for a CZ demo of time to hospital on foot or by car.

### ronchi2013process — The Process of Verification and Validation of Building Fire Evacuation Models (round 2)
- **Citation:** Ronchi, E., Kuligowski, E.D., Reneke, P.A., Peacock, R.D., Nilsson, D. (2013). The Process of Verification and Validation of Building Fire Evacuation Models. NIST Technical Note 1822. DOI: 10.6028/nist.tn.1822 (verified: Crossref)
- **Access:** OA (NIST). Round 2: test list checked in the full text.
- **Content:** A suite of verification tests for evacuation models, many adapted from the IMO tests (for example exit-route allocation, maximum flow rates, demographic parameters), plus validation procedures and convergence criteria for stochastic runs.
- **Reimplementability:** n/a. A benchmark source: the tests are geometry-plus-expected-behaviour checks that a browser FFCA can be run against. Porzycki et al. (2014, `porzycki2014application`, DOI 10.1007/978-3-319-11520-7_46, metadata only) applied it to CA crowd models.
- **Relevance to ca-geo:** MOV-01 test suite; complements the Kirchner evacuation-time curves.

### vanetten2017gdistance — R Package gdistance: Distances and Routes on Geographical Grids (round 2)
- **Citation:** van Etten, J. (2017). R Package gdistance: Distances and Routes on Geographical Grids. *Journal of Statistical Software* 76(13). DOI: 10.18637/jss.v076.i13 (verified: Crossref)
- **Content:** Software paper for the cost-distance package used by Weiss 2018/2020 and Nelson 2019 (transition matrices, accumulated cost, least-cost paths, random-walk distances on grids). OA.
- **Reimplementability:** n/a (software reference). Documents the transition-matrix formulation.
- **Relevance to ca-geo:** MOV-03 algorithm reference for a JavaScript port.

### potuzak2026benchmark — Benchmark of road network division methods for distributed or parallel road traffic simulation (round 2)
- **Citation:** Potuzak, T. (2026). Benchmark of road network division methods for distributed or parallel road traffic simulation. *The Journal of Supercomputing* 82. DOI: 10.1007/s11227-026-08542-1 (verified: Crossref)
- **Access:** OA (CC BY). Round 2: full text checked.
- **Content:** University of West Bohemia (ZČU Plzeň). A benchmark for dividing road networks into sub-networks before distributed simulation, run on four public test networks (Transportation Networks for Research). Uses static traffic assignment flows; no cellular automaton. Tool RONDIBET on GitLab (https://gitlab.com/tpotuzak/rondibet, checked 200).
- **Reimplementability:** n/a (not a CA).
- **Relevance to ca-geo:** Closes the round-1 lead: the ZČU traffic work is about distributed simulation infrastructure, not CA rules. Possible local contact for traffic-simulation questions.

## Most reimplementable (top picks)

1. **nagel1992cellular (A, 9).** Four-line rule, standard parameters, analytical checks. The baseline for MOV-02 on OSM links.
2. **biham1992selforganization (A, 9).** A 2D grid traffic CA with a sharp jamming transition; round 2 confirmed from the full text. An ideal browser demo and test case.
3. **nelson2019suite (A, 9; round 2, not a CA).** Open R code and open output rasters for travel time over a friction surface. The benchmark for a MOV-03 front.
4. **kirchner2002simulation (B, 8).** The canonical FFCA with full parameters and evacuation-time curves. The reference for MOV-01.
5. **kirchner2003friction (B, 8).** Adds one parameter (μ) for realistic clogging at bottlenecks.
6. **wood2012anisotropic (B, 8; round 2 up from 6).** Complete anisotropic evacuation-time recipe: Tobler slope function, land-cover speed table, direction reversal, base speed. The static field for MOV-01 on a DEM.
7. **knospe2000towards (B, 8).** Complete parameter set, calibrated against empirical motorway data.
8. **chowdhury1999selforganization (B, 8)** and **rickert1996two (B, 8).** Signalised city network and two-lane rules with parameters.
9. **korcek2012evolutionary (B, 7; round 2, CZ).** Extended NaSch calibrated on Czech road detector data.
10. **weiss2020global (B, 8)** and **weiss2018global (B, 7).** Open friction surfaces (including walking-only) and reference travel-time maps.

For geographic evacuation (MOV-01 on real maps), there is still no verified CA paper that scores B or
better. The practical route is unchanged but better documented: FFCA rules (kirchner2002/2003)
with a static field computed as an anisotropic cost distance on a DEM and land cover
(wood2012anisotropic, now fully specified), hazard-driven extra floor fields
(zheng2019simulation) and speed factors for smoke or gas (liu2023cellular), checked against
the NIST TN 1822 tests (ronchi2013process).

## Gaps and unverified leads

- **Tooling problem:** OpenAlex was still rate-limited in round 2. Bot checks blocked HAL
  (NaSch original), ScienceDirect and the U. Twente repository (Weiss 2018); we did not try to
  get past them. The arXiv full texts of nowak2012quantitative, barlovic1998metastable,
  nagel1998twolane and nagel2001parallel and the UNIGE copy of chopard1996cellular were not
  read in round 2 (priority went to geography-bound items); they remain cheap upgrades.
- **Metadata-only entries** (blue2001cellular, muramatsu1999jamming, guo2008mobile,
  guo2013modeling, varas2007cellular, lovreglio2015calibrating, porzycki2014application)
  still need at least their abstracts checked.
- **True CA evacuation on real geography (tsunami, flood, wildfire) is still rare.** Round 2
  searches (tsunami, flood, earthquake shelter, OSM city scale) found nothing beyond round 1
  except arai2011cellular (vehicle evacuation, weakly specified). Leads not verified or not
  assessed: Soga, Comfort, Zhao, Lorusso, Soysal (2021) UC Berkeley ITS report coupling a CA
  fire-spread model with spatial-queue evacuation traffic (no DOI found); Kita et al. 2014 IEEE
  CANDAR (DOI 10.1109/candar.2014.31, verified, not assessed); Li, Cova & Dennison (2018),
  wildfire evacuation triggers by coupling fire and traffic simulation, *Fire Technology* 55,
  617–642, DOI 10.1007/s10694-018-0771-6 (verified, not assessed; probably not CA); Lämmel,
  Rieser, Nagel 2009 (DOI 10.1007/978-3-642-04504-2_48, queue-based, not CA); Carneiro et al.
  2013, crowd evacuation CA in a soccer stadium (DOI 10.1109/svr.2013.29, verified, not
  assessed); Schadschneider et al. 2011, towards a calibration of the FFCA (PED 2010, DOI
  10.1007/978-1-4419-9725-8_50, verified, not assessed).
- **Toprakli (2024)**, "A Review and Implementation Guide for Basic Cellular Automata Models in
  Pedestrian Evacuation Simulation", *Gazi University Journal of Science Part B* 12(3),
  517–530. Still **not in Crossref** (three query variants). Listed on the Gazi University
  research portal (https://avesis.gazi.edu.tr/yayin/b23b7dc5-ce12-4b57-91c0-a3a427d9b539/a-review-and-implementation-guide-for-basic-cellular-automata-models-in-pedestrian-evacuation-simulation,
  checked 200). Covers FFCA and social-force CA with an implementation workflow. Kept as an
  unverified lead until a DOI is found.
- **Code:** no author-published open FFCA or lattice-gas code was found (round 1 and a quick
  round-2 GitHub check). Vadere and JuPedSim are not CA-based (see round 1).
- **CZ/EU:**
  - Resolved: the ZČU lead (T. Potuzak) is distributed-simulation infrastructure, not CA
    (`potuzak2026benchmark`).
  - New CZ CA traffic work at VUT Brno: `korcek2011scalable`, `korcek2012evolutionary`, and a
    travel-time calibration paper (Korček, Sekanina & Fučík 2012, LNCS, DOI
    10.1007/978-3-642-33350-7_84, verified, not assessed). Grey literature, no DOI: VUT
    software result "Microscopic CA-based traffic simulator" (Korček & Fülöp, NaSch-based,
    version 2 in 2016, licence required; https://www.fit.vutbr.cz/research/view_product.php?id=314,
    checked 200); Hodaňová (2010), bachelor thesis on CA traffic modelling with a Java NaSch
    simulator, VUT FIT (http://hdl.handle.net/11012/56081, checked 200).
  - Central Europe (PL): AGH Kraków crowd CA group (`lubas2016cellular`, `bazior2020using`,
    `porzycki2014application`; also Wąs & Lubaś 2014, *Neurocomputing* 146, 199–209, DOI
    10.1016/j.neucom.2014.04.057, and Wąs et al. 2016, *Acta Phys. Pol. B Proc. Suppl.* 9,
    133, DOI 10.5506/aphyspolbsupp.9.133, both verified, not assessed); Płaczek
    (`placzek2010fuzzy`).
  - EU items from round 1 (esser1997microscopic; Wahle et al. 1998; Santen et al. 1998) still
    not assessed.
- **Further families (from round 1, not yet done):** Kretz & Schreckenberg F.A.S.T. (DOI
  10.1007/11861201_85); Nishinari et al. extended FFCA (DOI 10.1007/3-540-28091-x_40); Daganzo
  2006 (DOI 10.1016/j.trb.2005.05.004, OA); Tian et al. 2020 (DOI
  10.1080/23249935.2020.1810820); Adamatzky 1996 (DOI 10.1016/0895-7177(96)00006-4).
  **Tobler's hiking function:** the formula is now available from a verified source
  (`wood2012anisotropic`, eq. 1). The original (Tobler 1993, NCGIA technical report) has no
  DOI; Goodchild (2020), "Beyond Tobler's Hiking Function", *Geographical Analysis* 52,
  558–569, DOI 10.1111/gean.12253 (verified, not assessed) discusses it.
- **Overlaps:** `fire` (duff2015using, guo2013modeling, liu2023cellular, WUI fire–evacuation
  coupling); `hyd` (zheng2019simulation, flood → evacuation chain L12); `gen`
  (lovreglio2015calibrating calibration, dang2021chain visualisation, maerivoet2005cellular as
  a CA methods review, vanetten2017gdistance); `eco` (front over a cost raster also used for
  animal dispersal, ECO-04; wildlife–vehicle collisions, below).

## Round 2 changes

| Key | Old score / class | New score / class | Reason |
|---|---|---|---|
| wood2012anisotropic | 6, C (provisional) | 8, B | Full text read: complete cost model and SCV table (S1, S2 1 → 2). |
| biham1992selforganization | 9, A | 9, A | Full text read; scores confirmed, "assessed from" updated. |
| liu2023cellular | 5, C (provisional) | 5, C | Full text read; speed-coupling formulas added, score unchanged. |
| nagel1992cellular, weiss2018global, zheng2019simulation | unchanged | unchanged | Full text attempted, no access. |
| nelson2019suite | – | 9, A (new) | Open code and outputs for travel-time fronts. |
| weiss2020global | – | 8, B (new) | Healthcare travel time; walking-only friction surface. |
| korcek2012evolutionary | – | 7, B (new) | CZ-calibrated CA traffic model. |
| placzek2010fuzzy, bazior2020using | – | 5, C (new, provisional) | Central European CA traffic / crowd variants. |
| korcek2011scalable, arai2011cellular | – | 4, C (new) | CZ scalable CA traffic; hazard evacuation traffic. |
| lubas2016cellular | – | 3, D (new, provisional) | Stadium crowd CA (mass events). |
| ronchi2013process, porzycki2014application, vanetten2017gdistance, potuzak2026benchmark | – | n/a (new) | Benchmark suite, its CA application, software reference, CZ lead closed. |

## New phenomena candidates (round 2)

| Phenomenon | Short description (what is simulated) | Why interesting | CZ relevance | Best verified reference key(s) + class | Note |
|---|---|---|---|---|---|
| Crowd flows at mass events (ingress / egress) | Pedestrians entering or leaving a stadium, festival ground or square through gates and streets, in normal operation rather than emergency; bottlenecks and waiting times. | Same FFCA engine as MOV-01, but a different, everyday question (gate capacity, crowd density); high-density CA variants exist. | Football stadiums, festivals, Christmas markets and New Year crowds in Prague and other cities. | `lubas2016cellular` (D, provisional), `bazior2020using` (C, provisional); test suite `ronchi2013process` (n/a) | Close to MOV-01, which is framed as evacuation only. |
| Wildlife–vehicle collisions | Animals moving across a landscape raster meet traffic on roads; collision risk per road segment depends on animal movement, traffic volume and speed. | Couples ECO-04 (animal movement) with MOV-02 (traffic); clear map output (roadkill hot-spots). | High: wildlife collisions are frequent on Czech roads. | `benard2023biologically` (n/a; individual-based model, bioRxiv preprint, not CA) | No CA found. A CA version (random walk on a habitat raster crossing a NaSch road) would be our own design. |
