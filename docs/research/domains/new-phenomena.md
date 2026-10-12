# New phenomena — horizon scan (round 2)

Survey round: 2 (horizon scan, 2026-10-12). Scoring per ../reimplementability-criteria.md.

Scope: phenomena tied to geography that have been modelled with cellular automata (CA) or
could plausibly be, and that are **not** among the 43 items in
`../../brainstorm/longlist.md`. I checked for duplicates against the longlist and the
round-1 catalogue (`../catalogue.md`). Every reference was verified against Crossref
metadata on 2026-10-12. Score notation is `S1 S2 S3 S4 S5 = total class`. "prov." means
provisional: scored from the abstract or metadata only, so S1–S2 ≤ 1 and the lower value
was taken whenever I was unsure. Third-party-only code scores S3 = 1 (harmonised rule).
Keys already in `/references.bib` are reused and marked "(existing key)". All new keys are
in `scratchpad/bib2/nw.bib`.

## Search log

| Query (Crossref `query.bibliographic`, unless noted) | Source | Hits (relevant) | Notes |
|---|---|---|---|
| CA + Schelling segregation real city GIS; Schelling model residential segregation real data | Crossref | 0 direct CA; 1 entity-based (`benenson2002entitybased`) | The segregation literature on real cities is mostly entity- or agent-based. |
| CA gentrification neighbourhood; title search "micro-scale spatial modeling of gentrification" | Crossref | 1 (`osullivan2002toward`) | Generic queries gave noise; found through the title search. |
| CA crime hotspots; "statistical model of criminal behavior" | Crossref | 1 (`short2008statistical`) | Lattice model of burglary hotspots. No arXiv copy found (arXiv API). |
| CA diffusion of innovation / rooftop PV / technology adoption | Crossref | 2 (`kocsis2011cellular`, `rai2015agentbased`); 1 lead (Hägerstrand 1960s reviews, not CA papers) | No CA for PV specifically; the PV models are agent-based. |
| CA language spread geography; "Influence of geography on language competition"; Kandler Celtic languages | Crossref, arXiv, PMC | 2 (`patriarca2009influence` full text from arXiv, `kandler2010language` full text from PMC) | |
| voter model for voters (Fernández-Gracia) | Crossref, arXiv | 1 (`fernandezgracia2014voter`, full text from arXiv) | Metapopulation of counties linked by commuting. |
| CA deforestation frontier; DINAMICA | Crossref | 1 (existing key `soaresfilho2002dinamica`) | Already listed in general.md as a platform. |
| CA mangrove / salt marsh / tidal marsh / sea-level rise / seagrass / coral | Crossref | coral 1 (`langmead2004coral`); others 0 | Not found does not mean absent; low priority for CZ. |
| CA earthquake SOC; OFC title; Georgoudas earthquake CA | Crossref | 2 (`olami1992selforganized`, `georgoudas2007modelling`) | Georgoudas is in an Elsevier open archive, but the full text was blocked (HTTP 403). |
| CA tsunami; CA volcanic ash / tephra; CA pyroclastic flows; lahar CA | Crossref | tsunami 1 (`gullace2014undata`); pyroclastic 1 (`avolio2006pyroclastic`); ash and lahar 0 | |
| CA permafrost / thermokarst / glacier / glacier mass balance | Crossref | 0 | Rejected (see below). |
| CA peatland bog; mire patterning (Couwenberg) | Crossref | 3 (`couwenberg2005selforganization`, `couwenberg2005simulation`, `couwenberg2022genes`) | Strong CZ link (mountain raised bogs). |
| CA karst sinkhole; CA speleogenesis | Crossref | 0 CA (the speleogenesis models are not CA) | Rejected. |
| CA mining subsidence | Crossref, Semantic Scholar | 3 (best: `chen2020dynamic`, OA) | Publisher PDF and HTML were blocked (HTTP 405/empty), so scored from the abstract. |
| CA soil salinization | Crossref | 1 (`lin2012regionalscale`, CA–Markov) | Weak CA, no CZ link. |
| CA river ice jam; CA locust; CA bird migration; CA rumour; CA tourism; CA noise; CA nitrate leaching; CA roadkill | Crossref | 0 relevant | Rejected (see below). |
| CA algal bloom; Chen & Mynett fuzzy CA; underwater macrophytes CA | Crossref | 2 (`chen2006modelling` existing key, `chen2002application`) | |
| TLM outdoor sound propagation | Crossref | 2 (`hofmann2007simulation`, `goestchel2022analysis`) | TLM is a lattice scattering scheme that behaves like a CA. |
| Vegetated dunes (Baas); shrub encroachment CA; riparian vegetation CA | Crossref, Semantic Scholar | 3 (`baas2002chaos`, `caracciolo2016mechanisms`, `ye2010modelling`) | |
| Balinese water temples; Assyrian empire CA; real-estate CA city | Crossref | 3 (`lansing1993emergent`, `parisi1998cellular`, `wu2003simulating`) | |
| Neolithic / prehistoric settlement CA; past populations CA | Crossref, OSF API | 1 preprint (`hewitt2022modelling`) + existing `hewitt2025modelling` | Duplicates EPI-04 (see Rejected). |
| Sorted patterned ground; smouldering peat fire CA | Crossref, Spiral (Imperial) | 2 (`kessler2003selforganization`, `fernandezanez2017twodimensional`) | Only a Word file of the accepted manuscript exists, so it was not downloaded. |
| OA checks for all candidates | Semantic Scholar API | — | 9 OA flags. Full text actually read for 3 (Patriarca, Fernández-Gracia, Kandler). |

## Summary table

| Proposed ID | Slug | Phenomenon | CA modelability (1–5, reason) | Best ref + class | CZ relevance | Recommendation |
|---|---|---|---|---|---|---|
| HAZ-06 | `mining-subsidence` | Surface subsidence above underground mining | 3 — subsidence is mostly a kernel (influence-function) problem; a CA gives the time-stepped spread of the trough | `chen2020dynamic` C (prov.) | **High**: Ostrava–Karviná coal basin; also Kladno and Příbram (to be verified) | **add to longlist** |
| ECO-10 | `raised-bog-patterning` | Hummock–hollow / string–flark patterns in raised bogs | 5 — lattice water flow plus a binary state flip; the rule is genuinely local | `couwenberg2005selforganization` C (prov.) | **High**: Šumava, Krušné hory and Krkonoše bogs (to be verified) | **add to longlist** |
| HYD-11 | `riparian-vegetation` | Riparian vegetation zones below regulated rivers | 4 — cell succession driven by inundation frequency from a hydrograph | `ye2010modelling` C (prov.) | Medium–high: regulated rivers below dams (e.g. Vltava cascade, to be verified) | **add to longlist** |
| SOC-01 | `language-competition` | Spatial competition and shift of languages | 4 — reaction–diffusion on a lattice with barrier potentials (mountains, sea) | `patriarca2009influence` B | Medium: historic Czech–German language border (to be verified); strong didactic value | **add to longlist** |
| SOC-02 | `voter-opinion-dynamics` | Spatial voting patterns from social imitation and commuting | 3 — network over municipalities rather than a raster; each municipality is a "cell" | `fernandezgracia2014voter` B | **High data fit**: municipal election results and census commuting (to be verified) | **add to longlist** (boundary case, network) |
| HAZ-07 | `earthquake-soc` | Earthquake / aftershock statistics on a fault grid (SOC) | 4 — classic CA, but the grid is an abstract fault plane, not a map | `olami1992selforganized` C (prov.) | Low hazard; West Bohemia / Vogtland earthquake swarms as a hook (to be verified) | borderline |
| SOC-03 | `crime-hotspots` | Formation of burglary hotspots | 4 — lattice attractiveness field plus random walkers | `short2008statistical` C (prov.) | Medium: open crime-map data (to be verified); sensitive topic | borderline |
| SOC-04 | `residential-segregation` | Schelling-type segregation on a real city | 4 — Schelling is a textbook CA; real-city versions are entity-based | `benenson2002entitybased` C (prov.) | Medium: socially excluded localities; census grid data (to be verified); sensitive | borderline |
| SOC-05 | `gentrification` | Micro-scale spread of gentrification | 3 — graph/parcel CA; depends on housing data that is rarely open | `osullivan2002toward` C (prov.) | Medium: Prague inner districts (to be verified) | borderline |
| SOC-06 | `innovation-adoption` | Spatial diffusion of an innovation (e.g. rooftop PV) | 3 — neighbourhood imitation CA is simple, but real drivers are economic | `kocsis2011cellular` C (prov.); `rai2015agentbased` C (prov., ABM) | Medium: PV boom around 2010 (to be verified) | borderline |
| HYD-12 | `algal-bloom` | Algal / cyanobacterial bloom patches in lakes and reservoirs | 3 — needs a hydrodynamic and nutrient driver; CA only for the biology | `chen2006modelling` D (existing key) | **High**: cyanobacteria in Czech reservoirs and ponds (to be verified) | borderline |
| ECO-11 | `aquatic-macrophytes` | Competition of submerged plant species in a shallow lake | 4 — local growth/competition CA driven by light and depth layers | `chen2002application` C (prov.) | Medium: fishponds and shallow reservoirs (to be verified) | borderline (could merge with HYD-12) |
| HYD-13 | `vegetated-dunes` | Dune formation with vegetation (coastal or inland) | 4 — slab CA (Werner-type) plus vegetation | `baas2002chaos` C (prov.) | Low–medium: inland sand dunes in south Moravia (to be verified) | borderline (variant of ATM-05) |
| HYD-14 | `patterned-ground` | Self-organised sorted stone circles and stripes (periglacial) | 3 — the model is a particle/feedback model on a grid; small scale | `kessler2003selforganization` C (prov.) | Low–medium: relict periglacial forms in Krkonoše / Jeseníky (to be verified) | borderline |
| HAZ-08 | `peat-smouldering-fire` | Smouldering ground and peat fire spread | 4 — multi-layer stochastic CA | `fernandezanez2017twodimensional` C (prov.) | Medium: ground fires, link to bogs and HAZ-01 (to be verified) | borderline (sub-scenario of HAZ-01) |
| ECO-12 | `shrub-encroachment` | Shrub encroachment into grassland | 4 — probabilistic establishment/mortality CA with a soil-moisture driver | `caracciolo2016mechanisms` C (prov.) | Medium: overgrowth of abandoned grassland (overlaps LND-02) | borderline (reference for LND-02) |
| ATM-06 | `noise-propagation` | Outdoor sound propagation around terrain and buildings | 3 — TLM is a lattice wave scheme; heavy for large 2D maps | `hofmann2007simulation` C (prov.) | Medium: strategic noise maps (to be verified) | borderline |
| LND-04 | `deforestation-frontier` | Deforestation along a colonisation frontier | 4 — same machinery as multi-class land-use CA | `soaresfilho2002dinamica` n/a (existing key, platform) | Low (tropical); mechanism overlaps LND-01 | borderline (scenario of LND-01) |
| URB-05 | `real-estate-cycles` | Fluctuations of real-estate investment in a CA city | 3 — synthetic; weak link to geodata | `wu2003simulating` C (prov.) | Low | not suitable |
| SOC-07 | `state-expansion` | Territorial expansion of a historical state | 2 — very stylised; rules depend on the narrative | `parisi1998cellular` D (prov.) | Low (Great Moravia as speculative case, to be verified) | not suitable |
| HAZ-09 | `pyroclastic-flow` | Pyroclastic flows | 4 — gravity flow CA from the SCIDDICA/SCIARA family | `avolio2006pyroclastic` C (prov.) | None | not suitable (fold into HAZ-05 as a note) |
| HAZ-10 | `tsunami-inundation` | Tsunami propagation and inundation | 3 — shallow-water physics; CA is preliminary | `gullace2014undata` C (prov.) | None (the flood model covers inland inundation) | not suitable |
| ECO-13 | `coral-reef` | Coral reef community dynamics under disturbance | 4 — classic ecological CA | `langmead2004coral` C (prov.) | None | not suitable |
| LND-05 | `irrigation-coordination` | Coordination of irrigation and pests (Balinese water temples) | 3 — coupled cells along a watershed network | `lansing1993emergent` C (prov.) | None; didactically interesting | not suitable |
| LND-06 | `soil-salinisation` | Spread of soil salinisation | 2 — CA–Markov projection, not a process CA | `lin2012regionalscale` D (prov.) | Low | not suitable |

Count: 25 phenomena. 5 to add, 13 borderline, 7 not suitable.

## Phenomena

### mining-subsidence — Surface subsidence above underground mining

- **What is simulated:** the subsidence trough above an extracted coal panel grows in time
  and space. Cells receive vertical displacement from neighbours according to their
  distance from the mined-out area and the face advance. **CA fit:** moderate. The physics
  is usually an influence-function (kernel) calculation, and the CA adds the dynamics of
  the advancing face. The abstract reports good agreement with observations.
  **Data:** DEM, panel geometry and extraction schedule (mine plans are mostly not open),
  overburden thickness, and InSAR deformation for validation (e.g. Copernicus EGMS, to be
  verified). **CZ relevance:** very high (Ostrava–Karviná, with mining-induced lakes),
  links to LND-03 and HYD-09. **Didactic value:** a visible "landscape sinks, water fills
  it" story. **Chains:** HAZ-06 → HYD-01/HYD-02 (new ponding, changed flood paths) →
  LND-03.
- **References:**
  - `chen2020dynamic` — Chen, Li, Hou (2020), *Dynamic simulation for the process of
    mining subsidence based on cellular automata model*, Open Geosciences 12(1), 832–839,
    doi:10.1515/geo-2020-0172 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.), assessed
    from abstract (OA, but the publisher PDF/HTML could not be fetched). Code: none found.
    The authors implemented it in ArcGIS + Python, with no link. Study area: a mine in
    East China.

### raised-bog-patterning — Hummock–hollow and string–flark patterns in raised bogs

- **What is simulated:** a grid on a peat dome, where water flows laterally through the
  acrotelm. Hummocks (low transmissivity, grow when dry) and hollows (high transmissivity,
  grow when wet) switch depending on the local water table. Strings form perpendicular to
  the slope. **CA fit:** excellent, because it is a local rule with lateral water exchange
  and a clean self-organisation demo. **Data:** essentially synthetic (dome slope,
  recharge). Optionally a LiDAR DTM of a real bog (CZ DMR 5G, to be verified).
  **CZ relevance:** high (mountain raised bogs in Šumava, Krušné hory and Krkonoše;
  peatland restoration and rewetting are topical, to be verified). **Didactic value:**
  high — patterns emerge from water feedback. It is a European, wet counterpart to ECO-08.
  **Chains:** ECO-10 ↔ HYD-09 (water table); drainage ditches → pattern loss; HAZ-08
  (peat fire) on drained bog.
- **References:**
  - `couwenberg2005selforganization` — Couwenberg, Joosten (2005), *Self-organization in
    raised bog patterning: the origin of microtope zonation and mesotope diversity*,
    Journal of Ecology 93(6), 1238–1248, doi:10.1111/j.1365-2745.2005.01035.x (verified:
    Crossref) — `1 1 0 2 1 = 5 C` (prov.), assessed from abstract (paywall). Code: none
    found. Inputs are synthetic.
  - `couwenberg2005simulation` — Couwenberg (2005), *A simulation model of mire patterning
    – revisited*, Ecography 28(5), 653–661, doi:10.1111/j.2005.0906-7590.04265.x (verified:
    Crossref) — `1 1 0 2 1 = 5 C` (prov.), assessed from abstract (paywall). It corrects
    the water-flow function of the older Swanson & Grigal (1988) model, so it is the
    preferred spec. Likely to reach B once the full text is read.
  - `couwenberg2022genes` — Couwenberg, Baumann, Lamkowski, Joosten (2022), *From genes to
    landscapes: Pattern formation and self-regulation in raised bogs with an example from
    Tierra del Fuego*, Ecosphere 13(4), doi:10.1002/ecs2.4031 (verified: Crossref) — n/a
    (field study with transect measurements; possible source of parameter ranges). OA, but
    the fetch was blocked (HTTP 403).

### riparian-vegetation — Riparian vegetation evolution under flow regulation

- **What is simulated:** riparian vegetation cells move between vegetation types
  depending on inundation duration and frequency derived from a (regulated) discharge
  regime. The model uses an unstructured (irregular-mesh) CA. **CA fit:** good. Each cell
  follows its own succession rule driven by a hydrological layer, with neighbourhood
  colonisation. **Data:** DEM of the floodplain, a hydrograph or water-level series,
  current riparian vegetation (land cover / habitat mapping, to be verified). **CZ
  relevance:** medium–high (rivers below dams, renaturalisation projects, to be
  verified). **Didactic value:** "a dam changes the vegetation downstream". **Chains:**
  HYD-02 (flood scenarios) → HYD-11 → ECO-02; ECO-05 (beaver).
- **References:**
  - `ye2010modelling` — Ye, Chen, Li (2010), *Modelling the riparian vegetation evolution
    due to flow regulation of Lijiang River by unstructured cellular automata*, Ecological
    Informatics 5(2), 108–114, doi:10.1016/j.ecoinf.2009.08.002 (verified: Crossref) —
    `1 1 0 1 1 = 4 C` (prov.), assessed from metadata (Semantic Scholar points to a
    repository record whose host did not resolve). Code: none found.

### language-competition — Spatial language competition and language shift

- **What is simulated:** two populations speaking different languages diffuse over a
  lattice, grow logistically, and convert between languages according to the
  Abrams–Strogatz rule (status parameter). Geographic barriers enter as a potential that
  modulates diffusion. **CA fit:** good. The full text gives an explicit-Euler lattice
  scheme (square lattice, reflecting or periodic boundaries), which is in effect a
  continuous-state CA. **Data:** in the paper, synthetic (circular islands, barriers). For
  a demo: DEM-derived barrier layer, population grid, historical language census (to be
  verified). **CZ relevance:** medium — the historic Czech–German language border, or
  dialect areas (to be verified). **Didactic value:** high. It shows that geography alone
  can decide which language survives. **Chains:** reuses EPI-04 (population dispersal)
  machinery.
- **References:**
  - `patriarca2009influence` — Patriarca, Heinsalu (2009), *Influence of geography on
    language competition*, Physica A 388(2–3), 174–186, doi:10.1016/j.physa.2008.09.034
    (verified: Crossref) — `2 2 0 2 1 = 7 B`, assessed from full text (arXiv 0807.3100).
    Discretised equations, lattice sizes, time step, rate constant and initial-condition
    parameters are given. Results are figures only. Code: none found.
  - `kandler2010language` — Kandler, Unger, Steele (2010), *Language shift, bilingualism
    and the future of Britain's Celtic languages*, Phil. Trans. R. Soc. B 365(1559),
    3855–3864, doi:10.1098/rstb.2010.0051 (verified: Crossref) — `1 1 0 1 2 = 5 C`,
    assessed from full text (PMC). Reaction–diffusion with bilinguals. Fitted conversion
    rates are in a table, but growth/diffusion values and the spatial domain are not given.
    Quantitative fit to census series. Solved with a finite-element method, so not CA.

### voter-opinion-dynamics — Spatial voting patterns from imitation and commuting

- **What is simulated:** each county (cell) holds voters with a binary opinion. Agents
  imitate others both where they live and where they work (commuting coupling), with
  noise. The model reproduces stationary vote-share dispersion and the logarithmic decay
  of spatial correlations seen in US elections. **CA fit:** medium. It is a CA on an
  irregular network of administrative units rather than a raster, so it is a "graph CA"
  boundary case like URB-04. **Data:** population and commuting matrix per unit, election
  results per unit. In CZ, municipal election results and census commuting flows (both to
  be verified) could make it a very data-rich demo. **CZ relevance:** high for data,
  politically sensitive (purely illustrative). **Didactic value:** high (opinion
  "spreads" along commuting links). **Chains:** shares commuting coupling with EPI-01.
- **References:**
  - `fernandezgracia2014voter` — Fernández-Gracia, Suchecki, Ramasco, San Miguel, Eguíluz
    (2014), *Is the Voter Model a Model for Voters?*, Physical Review Letters 112(15),
    doi:10.1103/physrevlett.112.158701 (verified: Crossref) — `2 2 0 1 2 = 7 B`, assessed
    from full text (arXiv 1309.1131). Rule and the two free parameters (noise D, coupling
    α) are given with a calibration procedure. Inputs are US census commuting and county
    election data, described but not packaged (S4 = 1, lower value chosen). Code: none
    found.

### earthquake-soc — Earthquake statistics on a fault grid (self-organised criticality)

- **What is simulated:** a spring-block lattice. Each cell accumulates stress uniformly
  and topples when it exceeds a threshold, passing a fraction of its stress to its
  neighbours (non-conservative). Avalanches follow a Gutenberg–Richter-like size
  distribution. **CA fit:** excellent as a CA, but the grid is a fault plane, not a map
  layer. Georgoudas et al. adapt a CA to regional seismicity (Greece; full text not
  read). **Data:** synthetic. Validation could use an earthquake catalogue (for CZ,
  regional catalogues of West Bohemia swarms, to be verified). **CZ relevance:** low
  hazard, but swarms are a local curiosity. **Didactic value:** high (SOC and power
  laws, with the same "sandpile" logic as forest-fire SOC). **Chains:** HAZ-07 → HAZ-02
  (earthquake-triggered landslides), as a stretch.
- **References:**
  - `olami1992selforganized` — Olami, Feder, Christensen (1992), *Self-organized
    criticality in a continuous, nonconservative cellular automaton modeling earthquakes*,
    Physical Review Letters 68(8), 1244–1247, doi:10.1103/physrevlett.68.1244 (verified:
    Crossref) — `1 1 0 2 1 = 5 C` (prov.), assessed from metadata only (paywall, no
    abstract in Crossref). The rule is known to be compact, so it is likely B from full
    text (unverified).
  - `georgoudas2007modelling` — Georgoudas, Sirakoulis, Andreadis (2007), *Modelling
    earthquake activity features using cellular automata*, Mathematical and Computer
    Modelling 46(1–2), 124–137, doi:10.1016/j.mcm.2006.12.029 (verified: Crossref) —
    `1 1 0 1 1 = 4 C` (prov.), metadata only (flagged OA, fetch blocked).

### crime-hotspots — Formation of burglary hotspots

- **What is simulated:** lattice sites carry a dynamic "attractiveness" (with
  repeat-victimisation feedback). Criminals are random walkers biased towards attractive
  sites, and burglaries raise local attractiveness, which diffuses to neighbours.
  Depending on parameters, hotspots emerge or the field stays uniform. **CA fit:** good
  (lattice field plus walkers). **Data:** synthetic in the paper. A geographic variant
  would use a building or address density grid and crime statistics (open crime maps for
  CZ, to be verified). **CZ relevance:** medium; the topic is sensitive. **Didactic
  value:** high (pattern formation in social systems). **Chains:** MOV-03 (accessibility)
  as an attractiveness input.
- **References:**
  - `short2008statistical` — Short, D'Orsogna, Pasour, Tita, Brantingham, Bertozzi,
    Chayes (2008), *A statistical model of criminal behavior*, Mathematical Models and
    Methods in Applied Sciences 18(supp01), 1249–1267, doi:10.1142/s0218202508003029
    (verified: Crossref) — `1 1 0 2 1 = 5 C` (prov.), assessed from abstract (no OA copy
    found). The full text probably gives complete discrete rules, so it is a B/A candidate.

### residential-segregation — Schelling-type segregation on a real city

- **What is simulated:** households relocate when the share of unlike neighbours exceeds
  their tolerance. On a real city, the cells are buildings or dwellings with census
  attributes. **CA fit:** good (Schelling is a textbook CA). Real-city implementations are
  entity-based, so this is borderline CA. **Data:** building footprints, census
  population by grid or address (CZ census grid data, to be verified). Ethnicity data are
  sensitive and generally not open. **CZ relevance:** medium (socially excluded
  localities), but the topic is sensitive. **Didactic value:** very high (small
  preferences produce strong segregation). **Chains:** SOC-05 (gentrification),
  LND-01.
- **References:**
  - `benenson2002entitybased` — Benenson, Omer, Hatna (2002), *Entity-based modeling of
    urban residential dynamics: the case of Yaffo, Tel Aviv*, Environment and Planning B
    29(4), 491–512, doi:10.1068/b1287 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.),
    assessed from abstract (paywall). Uses georeferenced 1995 Israeli census data (not
    open).

### gentrification — Micro-scale spread of gentrification

- **What is simulated:** parcels or houses change social status according to the state of
  neighbouring properties and housing-market conditions. The spatial model is
  graph-based. **CA fit:** medium. **Data:** parcel geometry, property values or rents
  (rarely open), census socio-economic indicators. **CZ relevance:** medium (inner Prague
  and Brno districts, to be verified). **Didactic value:** medium–high.
  **Chains:** SOC-04, LND-01.
- **References:**
  - `osullivan2002toward` — O'Sullivan (2002), *Toward micro-scale spatial modeling of
    gentrification*, Journal of Geographical Systems 4(3), 251–274,
    doi:10.1007/s101090200086 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.), assessed
    from metadata only (paywall, no abstract).

### innovation-adoption — Spatial diffusion of an innovation (e.g. rooftop PV)

- **What is simulated:** cells (households) adopt an innovation with a probability that
  grows with the number of adopting neighbours (imitation) and with individual
  attractiveness, in the tradition of Hägerstrand's spatial diffusion. **CA fit:**
  medium. The CA mechanism is trivial, but realistic adoption is driven by economics and
  policy (subsidies). **Data:** building footprints / roof suitability, adoption records
  (PV installations registry for CZ, to be verified), socio-economic grid. **CZ
  relevance:** medium (the solar boom around 2010 and the current rooftop wave, to be
  verified). **Didactic value:** high (the "neighbour effect" visible on a map).
- **References:**
  - `kocsis2011cellular` — Kocsis, Ku (2011), *Cellular Automata Modelling of the Diffusion
    of Innovations*, in: Cellular Automata – Simplicity Behind Complexity, InTech,
    doi:10.5772/15753 (verified: Crossref; the second author's family name appears
    truncated as "Ku" in Crossref) — `1 1 0 2 1 = 5 C` (prov.), metadata only (OA chapter,
    but the landing-page fetch returned a wrong chapter).
  - `rai2015agentbased` — Rai, Robinson (2015), *Agent-based modeling of energy technology
    adoption: Empirical integration of social, behavioral, economic, and environmental
    factors*, Environmental Modelling & Software 70, 163–177,
    doi:10.1016/j.envsoft.2015.04.014 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.),
    metadata only (OA flag, fetch not attempted after Elsevier blocks). It is agent-based
    (PV in Austin, TX), useful for an empirical calibration design.

### algal-bloom — Algal / cyanobacterial bloom patches

- **What is simulated:** a hydrodynamic and water-quality model supplies nutrients, light
  and temperature per cell. A fuzzy CA decides local algal biomass change and spread.
  **CA fit:** medium (the CA is the biological layer on top of a physics model).
  **Data:** reservoir bathymetry, inflow nutrient loads, temperature, and satellite
  chlorophyll for validation (Sentinel-2/3 products, to be verified). **CZ relevance:**
  high (cyanobacteria in bathing waters and reservoirs, to be verified). **Didactic
  value:** medium. **Chains:** HYD-05 (erosion → phosphorus input) → HYD-12; ATM-04
  (drought, warm water).
- **References:**
  - `chen2006modelling` (existing key) — Chen, Mynett (2006), Ecological Modelling,
    doi:10.1016/j.ecolmodel.2006.06.014 — round 1 class `D (3)` in atmosphere-other.md;
    not re-scored here.

### aquatic-macrophytes — Competing submerged plants in a shallow lake

- **What is simulated:** two submerged macrophyte species compete cell by cell under
  light, depth and temperature conditions. Colonisation comes from neighbours.
  **CA fit:** good. **Data:** bathymetry, water transparency, temperature. **CZ
  relevance:** medium (fishpond and reservoir ecology, to be verified). **Didactic
  value:** medium. **Chains:** HYD-12 (turbidity from blooms suppresses macrophytes).
- **References:**
  - `chen2002application` — Chen, Mynett, Minns (2002), *Application of cellular automata
    to modelling competitive growths of two underwater species Chara aspera and
    Potamogeton pectinatus in Lake Veluwe*, Ecological Modelling 147(3), 253–265,
    doi:10.1016/s0304-3800(01)00428-8 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.),
    metadata only (paywall).

### vegetated-dunes — Dune formation with vegetation

- **What is simulated:** sand slabs are picked up and deposited downwind (Werner-type
  slab CA), while vegetation growth stabilises cells, producing parabolic dunes and
  blowouts. **CA fit:** good. **Data:** DEM, wind direction, vegetation cover; inland
  dunes would need historical land cover. **CZ relevance:** low–medium (inland sands in
  south Moravia, to be verified). **Note:** close to ATM-05 (snow/sand drift); it could be
  a scenario of ATM-05 rather than a new item.
- **References:**
  - `baas2002chaos` — Baas (2002), *Chaos, fractals and self-organization in coastal
    geomorphology: simulating dune landscapes in vegetated environments*, Geomorphology
    48(1–3), 309–328, doi:10.1016/s0169-555x(02)00187-3 (verified: Crossref) —
    `1 1 0 2 1 = 5 C` (prov.), metadata only (paywall).

### patterned-ground — Sorted patterned ground (periglacial self-organisation)

- **What is simulated:** freeze–thaw cycles sort stones and soil into circles, polygons
  or stripes through two feedbacks (lateral sorting and squeezing of stone domains),
  depending on slope and stone concentration. **CA fit:** medium. It is a grid-based
  feedback model, but at metre scale, without real geodata. **Data:** synthetic; slope
  from DEM. **CZ relevance:** low–medium (relict periglacial forms in the Krkonoše and
  Hrubý Jeseník summit areas, to be verified). **Didactic value:** high (striking
  patterns, a cold counterpart to ECO-08).
- **References:**
  - `kessler2003selforganization` — Kessler, Werner (2003), *Self-organization of sorted
    patterned ground*, Science 299(5605), 380–383, doi:10.1126/science.1077309 (verified:
    Crossref) — `1 1 0 2 1 = 5 C` (prov.), assessed from abstract (paywall; model details
    are probably in the supplement).

### peat-smouldering-fire — Smouldering peat and ground fire

- **What is simulated:** a multi-layer stochastic CA in which cells pass through drying,
  pyrolysis and oxidation, with spread probabilities depending on moisture and airflow.
  It tests line and radial ignition fronts. **CA fit:** good. **Data:** synthetic. For
  maps: peat/organic soil layer, moisture. **CZ relevance:** medium (ground fires in
  sandstone forests and drained peatlands, to be verified). **Chains:** HAZ-01 →
  HAZ-08, ECO-10 (drained bogs), ATM-01 (smoke).
- **References:**
  - `fernandezanez2017twodimensional` — Fernandez-Anez, Christensen, Rein (2017),
    *Two-dimensional model of smouldering combustion using multi-layer cellular automaton:
    The role of ignition location and direction of airflow*, Fire Safety Journal 91,
    243–251, doi:10.1016/j.firesaf.2017.03.009 (verified: Crossref) — `1 1 0 2 1 = 5 C`
    (prov.), assessed from the repository abstract. The accepted manuscript exists in
    Imperial Spiral as a .doc, not downloaded.

### shrub-encroachment — Shrub encroachment into grassland

- **What is simulated:** a probabilistic CA of grass/shrub/bare cells with
  establishment, mortality and seed dispersal, coupled to an ecohydrological soil-moisture
  model and climate scenarios. **CA fit:** good. **Data:** land cover, climate series,
  soil. **CZ relevance:** medium as a mechanism for overgrowth of abandoned grassland.
  **Note:** probably a reference for LND-02 rather than a new item.
- **References:**
  - `caracciolo2016mechanisms` — Caracciolo, Istanbulluoglu, Noto, Collins (2016),
    *Mechanisms of shrub encroachment into Northern Chihuahuan Desert grasslands and
    impacts of climate change investigated using a cellular automata model*, Advances in
    Water Resources 91, 46–62, doi:10.1016/j.advwatres.2016.03.002 (verified: Crossref) —
    `1 1 0 1 1 = 4 C` (prov.), metadata only (accepted manuscript flagged on
    ScienceDirect, not fetched).

### noise-propagation — Outdoor sound propagation

- **What is simulated:** acoustic pressure pulses scatter between lattice nodes
  (transmission line matrix, TLM), including ground impedance, terrain and barriers.
  **CA fit:** medium. TLM is a local lattice rule, but it is a wave model needing fine
  grids (wavelength-limited), usually in 2D vertical slices. **Data:** DEM, building
  footprints, road/rail sources; strategic noise maps for comparison (to be verified).
  **CZ relevance:** medium. **Didactic value:** medium–high ("how a noise barrier works").
- **References:**
  - `hofmann2007simulation` — Hofmann, Heutschi (2007), *Simulation of outdoor sound
    propagation with a transmission line matrix method*, Applied Acoustics 68(2), 158–172,
    doi:10.1016/j.apacoust.2005.10.006 (verified: Crossref) — `1 1 0 2 1 = 5 C` (prov.),
    metadata only (paywall).
  - `goestchel2022analysis` — Goestchel, Guillaume, Ecotière, Gauvreau (2022), *Analysis
    of the numerical properties of the transmission line matrix model for outdoor sound
    propagation*, Journal of Sound and Vibration 531, 116974,
    doi:10.1016/j.jsv.2022.116974 (verified: Crossref) — `1 1 0 2 1 = 5 C` (prov.),
    metadata only. It probably contains benchmark cases (S5 could rise).

### deforestation-frontier — Deforestation along a colonisation frontier

- **What is simulated:** forest → pasture/crop transitions near roads and existing
  clearings, using expander/patcher functions. **CA fit:** good, but it is the same
  machinery as LND-01. **CZ relevance:** low (tropical). It could serve as a scenario of
  LND-01 / multi-class land use.
- **References:** `soaresfilho2002dinamica` (existing key) — n/a (platform), see
  general.md.

### real-estate-cycles — Real-estate investment cycles in a CA city

- **What is simulated:** developers invest where local profitability in the neighbourhood
  is high, creating new niches and temporal fluctuations. **CA fit:** medium; synthetic.
  **CZ relevance:** low. **Recommendation:** not suitable (weak link to geodata).
- **References:** `wu2003simulating` — Wu (2003), *Simulating temporal fluctuations of real
  estate development in a cellular automata city*, Transactions in GIS 7(2), 193–210,
  doi:10.1111/1467-9671.00140 (verified: Crossref) — `1 1 0 2 1 = 5 C` (prov.), from
  abstract.

### state-expansion — Territorial expansion of a historical state

- **What is simulated:** cells of a historical map are conquered or annexed according to
  neighbourhood rules. **CA fit:** weak (the rules are narrative). **Recommendation:** not
  suitable.
- **References:** `parisi1998cellular` — Parisi (1998), *A cellular automata model of the
  expansion of the Assyrian Empire*, in: Cellular Automata: Research Towards Industry,
  Springer, 194–200, doi:10.1007/978-1-4471-1281-5_18 (verified: Crossref) —
  `1 0 0 1 1 = 3 D` (prov.), metadata only.

### pyroclastic-flow — Pyroclastic flows

- Gravity-driven flow CA from the same family as SCIDDICA/SCIARA (already in the catalogue
  for debris flows and lava). No CZ relevance, so it should be noted under HAZ-05 rather
  than added. Reference: `avolio2006pyroclastic` — Avolio, Crisci, Di Gregorio, Rongo,
  Spataro, D'Ambrosio (2006), *Pyroclastic flows modelling using cellular automata*,
  Computers & Geosciences 32(7), 897–911, doi:10.1016/j.cageo.2005.10.024 (verified:
  Crossref) — `1 1 0 1 1 = 4 C` (prov.), metadata only.

### tsunami-inundation — Tsunami propagation and inundation

- A preliminary CA for tsunami waves. No CZ relevance, and inland inundation is covered by
  the WAT model. Reference: `gullace2014undata` — Gullace, Avolio, Di Gregorio (2014),
  *UNDATA: A preliminary cellular automata model for tsunami simulation*, LNCS, 228–237,
  doi:10.1007/978-3-319-11520-7_24 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.),
  metadata only.

### coral-reef — Coral reef community dynamics

- A classic ecological CA of coral, algae and disturbance. No CZ relevance. Reference:
  `langmead2004coral` — Langmead, Sheppard (2004), *Coral reef community dynamics and
  disturbance: a simulation model*, Ecological Modelling 175(3), 271–290,
  doi:10.1016/j.ecolmodel.2003.10.019 (verified: Crossref) — `1 1 0 1 1 = 4 C` (prov.),
  metadata only.

### irrigation-coordination — Balinese water temple networks

- Coupled subak cells along a watershed choose irrigation schedules, trading off water
  sharing against pest control, and self-organise into coordinated patterns. It is
  didactically interesting (cooperation emerging on a landscape) but has no CZ analogue.
  Reference: `lansing1993emergent` — Lansing, Kremer (1993), *Emergent properties of
  Balinese water temple networks: coadaptation on a rugged fitness landscape*, American
  Anthropologist 95(1), 97–114, doi:10.1525/aa.1993.95.1.02a00050 (verified: Crossref) —
  `1 1 0 1 1 = 4 C` (prov.), from abstract.

### soil-salinisation — Soil salinisation

- A CA–Markov projection of salinised land; it is not a process rule. No CZ relevance.
  Reference: `lin2012regionalscale` — Lin, Zhou, Liu (2012), *Regional-scale assessment and
  simulation of land salinization using cellular automata-Markov model*, ASABE/CSBE North
  Central Intersectional Meeting, doi:10.13031/2013.41320 (verified: Crossref) —
  `1 0 0 1 1 = 3 D` (prov.), metadata only.

## Rejected ideas

- **Spread of agriculture / prehistoric settlement / hunter-gatherer mobility** — duplicate
  of EPI-04 (`gregoriodesouza2021reassessing`, existing `hewitt2025modelling`; new preprint
  `hewitt2022modelling`, Hewitt 2022, SocArXiv/OSF, doi:10.31235/osf.io/wqzjb, verified:
  Crossref, which claims R code in its supplement; OSF page checked, file not checked).
  Better treated as a CZ scenario of EPI-04 (e.g. Neolithic LBK expansion, to be verified).
- **Archaeological site prediction** — a statistical suitability model, not a dynamic CA.
- **Glacier flow / mass balance** — no CA literature found in Crossref; no glaciers in CZ.
- **Permafrost / thermokarst** — no CA found; no CZ relevance (only relict forms, see
  patterned-ground).
- **Karst and sinkholes** — no CA found; speleogenesis models are pipe-network
  simulations. Moravian Karst would be interesting, but there is no template.
- **River ice jams** — the literature is hydraulic (1D), not CA.
- **Sea-level rise inundation, mangroves, salt marsh, seagrass** — no CA hits in Crossref
  (may exist under other terms); no CZ relevance. Inundation is covered by WAT
  (bathtub-with-connectivity scenario).
- **Volcanic ash / tephra fall** — no CA found; the mechanism is advection–diffusion
  (ATM-01).
- **Lahars** — no CA hit; the mechanism equals HAZ-02 (debris flow).
- **Lightning ignition** — an ignition-source layer for HAZ-01, not a separate phenomenon.
- **Drought-induced tree mortality** — no CA found; overlaps ATM-04 and ECO-01.
- **Nitrate / nutrient leaching** — vertical column process, no lateral CA rule; no CA hit.
- **Locust swarms, bird or insect migration** — no CA hits; individual- and flight-based.
- **Wildlife–vehicle collisions** — risk mapping, not CA; an output layer of ECO-04.
- **Tourism crowding** — agent/pedestrian models (MOV-01 family); no CA hit.
- **Light pollution** — radiative transfer models (skyglow), not a local rule.
- **Rumour / information spread** — network models without geography; no CA hit.
- **Urban shrinkage / vacancy spread** — no CA hit (would be an inverse of LND-01).
- **Radionuclide or heavy-metal contamination spread** — no CA hit; it would be a variant
  of HYD-09 / ATM-01 / HYD-05.
- **Reed (Phragmites) expansion in ponds** — no CA hit (it would fit ECO-03 / ECO-11).
- **Rockfall** — already covered by Flow-Py (`damboise2022flowpy`) under HAZ-02/03.

## Gaps and unverified leads

- **Full texts not reached** for the most promising provisional entries: `chen2020dynamic`
  (OA, but De Gruyter blocked automated fetch), `couwenberg2005simulation`,
  `couwenberg2005selforganization`, `olami1992selforganized`, `short2008statistical`,
  `georgoudas2007modelling` (Elsevier open archive, HTTP 403) and `kocsis2011cellular`
  (InTech OA). Raised-bog, OFC and crime-hotspot models are likely to reach B after
  full-text reading.
- **Not checked / leads:** Swanson & Grigal (1988) mire model (Oikos,
  doi:10.2307/3565529, seen in Crossref results, not assessed); Bak–Tang earthquake SOC;
  Hägerstrand innovation diffusion (only 1969 book reviews in Crossref, original
  monograph without DOI); Schelling on real Czech data; CZ-specific CA studies for mining
  subsidence (Ostrava basin) — none found in this scan.
- **CZ data claims** (EGMS InSAR, DMR 5G, census grid and commuting data, municipal
  election results, PV registry, crime maps, cyanobacteria monitoring) are all **to be
  verified**.
- **OpenAlex** was quota-blocked, so the search relied on Crossref bibliographic queries,
  which are noisy for generic terms. Some phenomena marked "no CA found" may have
  literature under other wording.
