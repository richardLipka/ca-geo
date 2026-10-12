# Longlist of phenomena for CA simulation over geodata

Broad, deliberately unfiltered list of phenomena that could be simulated by a cellular
automaton over geographic (raster) data. It is the input for the evaluation in
`docs/review/evaluation-matrix.md`.

Conventions:

- Each item has a stable **ID** (`CAT-NN`) and a kebab-case **slug** that will become the
  file name of a model card if the item is selected.
- ★ = confirmed project model (water flow / flooding, wildfire spread).
  `CZ` = phenomenon with specific relevance for the Czech Republic.
- *Data* lists layer types; concrete sources are only hints and are all **to be verified**
  (availability, licence, resolution, coverage). Source names are given as search leads,
  not as confirmed facts.
- Named models or approaches are leads only, marked **(to be verified)**, without
  bibliographic details. Literature is a later phase (`TODO(literature)`).
- Real events are mentioned as potential validation cases; details (dates, extent) are
  **to be verified**.

> **Review note (2026-10-12, author decision):** water flow / flooding is treated as
> **one model with scenarios**. Items HYD-01, HYD-02, HYD-03, URB-02, HYD-04 and LND-03
> are evaluated together as `WAT` (`water-flow-flooding`) in
> `docs/review/evaluation-matrix.md`. The items stay listed below as scenario ideas.

## Overview

| Category | Code | Items |
|---|---|---|
| Hydrology and geomorphology | `HYD` | 7 |
| Natural hazards | `HAZ` | 5 |
| Ecology and forestry | `ECO` | 8 |
| Landscape and land use | `LND` | 3 |
| City and infrastructure | `URB` | 4 |
| Atmosphere and pollution | `ATM` | 4 |
| Spread of diseases and populations | `EPI` | 3 |
| Movement of people and traffic | `MOV` | 3 |
| **Total** | | **37** |

## HYD — Hydrology and geomorphology

**HYD-01 · Surface runoff and ponding** (`surface-runoff`) ★
Rain falling on terrain flows downslope between cells, fills depressions and accumulates
into concentrated flow paths. *Data:* DEM, land cover / imperviousness, soil
infiltration class, rainfall (scalar or radar raster). *Why:* the basic "water finds its
way" demo; most other water models are built on it.

**HYD-02 · River flood inundation** (`river-flood-inundation`) ★ `CZ`
Water overtopping river banks spreads over the floodplain; the simulated extent can be
compared with official flood zones. *Data:* high-resolution DTM, river network,
inflow hydrograph or water level, (to be verified) official flood-zone maps. *Why:*
directly relatable (large floods in CZ are part of collective memory); strong
"what if the dike were here" interaction.

**HYD-03 · Flash flood on a small catchment** (`flash-flood`) ★ `CZ`
A short, intense convective storm over a small catchment produces a rapid flood wave in
a narrow valley. *Data:* DEM, land cover, soil, rainfall intensity (radar-like raster).
*Why:* flash floods are a frequent, hard-to-forecast hazard in CZ; shows how terrain
concentrates water within minutes.

**HYD-04 · Fishpond cascade breach** (`pond-cascade-breach`) `CZ`
Failure of one pond dam releases water that overtops and breaches the next pond
downstream, creating a domino effect. *Data:* DEM, water bodies with dam positions
(pond register — to be verified), dam heights (likely not open — to be verified).
*Why:* very Czech landscape feature (historic pond systems); dramatic, easy-to-grasp
chain reaction.

**HYD-05 · Soil erosion, sediment transport and muddy floods** (`soil-erosion`) `CZ`
Runoff detaches soil on fields, carries sediment downslope and deposits it in villages,
roads or ponds. *Data:* DEM, land use / crop type, soil erodibility, rainfall, field
boundaries (LPIS — to be verified); (to be verified) erosion-event monitoring records.
*Why:* a recurring problem of Czech agricultural landscape (large fields on slopes);
shows the effect of field layout and land-use measures.

**HYD-06 · Snow accumulation and snowmelt** (`snowmelt`)
Snow cover builds up and melts depending on elevation, aspect and temperature, releasing
water into runoff. *Data:* DEM (elevation, aspect), temperature series, land cover,
(to be verified) satellite snow-cover products. *Why:* links weather to spring floods;
nice seasonal animation; mostly vertical (cell-local) process, laterally coupled only
through runoff.

**HYD-07 · River channel morphodynamics** (`river-morphodynamics`)
Erosion and deposition reshape a braided or meandering channel over many floods.
Landscape-evolution CA exist as leads (e.g. CAESAR-type models — to be verified).
*Data:* DEM / river bathymetry, sediment properties, discharge series. *Why:* unusual,
long time scale "landscape is alive" demo; scientifically demanding.

## HAZ — Natural hazards

**HAZ-01 · Wildfire spread** (`wildfire-spread`) ★ `CZ`
Fire spreads from burning cells to neighbours depending on fuel, moisture, slope and
wind. Fire-behaviour models such as Rothermel-type spread rates are leads (to be
verified). *Data:* land cover / fuel type, forest stand data (to be verified), DEM,
wind, fuel moisture. *Why:* classic and visually striking CA; topical after recent large
fires in CZ (e.g. the České Švýcarsko fire — details to be verified).

**HAZ-02 · Landslides and debris flows** (`landslide-runout`) `CZ`
Cells become unstable when slope and saturation exceed a threshold; the released mass
travels downslope and stops in flatter terrain. *Data:* DEM, geology / soil,
soil moisture or rainfall, (to be verified) national slope-instability register.
*Why:* a real hazard in the Carpathian part of CZ (flysch); combines trigger and runout.

**HAZ-03 · Snow avalanche runout** (`avalanche-runout`) `CZ`
Snow released in steep starting zones flows down the slope; the model shows the reach of
the avalanche. *Data:* DEM, forest cover (protective forest), snow depth (scenario),
(to be verified) avalanche records from mountain rescue services. *Why:* relevant for
Czech mountains (Krkonoše, Jeseníky); reuses gravity-flow mechanics.

**HAZ-04 · Windthrow in forests** (`windthrow`) `CZ`
A storm topples trees; damage propagates from stand edges and gaps into the stand,
because opened edges are more exposed. *Data:* forest stands (species, age, height —
to be verified), DEM (exposure), wind direction and strength scenario. *Why:*
windthrow is a major disturbance of Czech spruce forests and a trigger of bark-beetle
outbreaks (see links).

**HAZ-05 · Lava flow** (`lava-flow`)
Lava spreads downslope, cools and solidifies, changing the terrain for later flows.
CA lava models are a known lead (to be verified). *Data:* DEM of a volcano, vent
position, effusion rate. *Why:* textbook CA demo, but no relevance for CZ (EU: Italy,
Iceland, Canary Islands) — included for completeness and as a didactic counterpoint.

## ECO — Ecology and forestry

**ECO-01 · Bark-beetle outbreak** (`bark-beetle-outbreak`) `CZ`
Beetles spread from infested spruce trees to nearby susceptible stands; drought and
windthrow increase susceptibility. *Data:* forest stands (spruce share, age),
drought index, (to be verified) satellite-derived forest dieback maps. *Why:* the
defining forest disaster in CZ in recent years; strong validation potential from
satellite imagery.

**ECO-02 · Forest succession and recovery after disturbance** (`forest-succession`)
After fire, windthrow or beetle outbreak, cells move through successional stages
(bare → grass/shrub → pioneer trees → mature forest), seeded from neighbouring stands.
*Data:* land cover, disturbance map, distance to seed sources, site conditions.
*Why:* closes the loop of disturbance chains; illustrates slow ecological time.

**ECO-03 · Invasive species spread** (`invasive-species-spread`) `CZ`
An invasive plant or animal spreads mainly along corridors (rivers, roads, railways) and
by occasional long-distance jumps. Examples relevant for CZ: Japanese knotweed,
giant hogweed, golden jackal (all to be verified). *Data:* river and road network,
land cover, (to be verified) occurrence records from nature conservation databases.
*Why:* corridor-driven spread is a visually clear CA pattern; relevant for nature
conservation.

**ECO-04 · Habitat connectivity and animal movement** (`habitat-connectivity`) `CZ`
Animals disperse through a landscape whose cells have different "resistance"; highways,
fences and towns act as barriers. *Data:* land cover, road and rail network, fences,
(to be verified) wildlife-crossing locations. *Why:* shows the effect of infrastructure
on large mammals returning to CZ (e.g. lynx, wolf — to be verified); closely related to
cost-distance spreading.

**ECO-05 · Beaver dams and wetland formation** (`beaver-wetlands`) `CZ`
Beavers build dams on small streams; water backs up and wetlands form, changing local
hydrology. *Data:* DEM, stream network, land cover, (to be verified) beaver occurrence
data. *Why:* unusual combination of ecology and hydrology; topical as nature-based water
retention.

**ECO-06 · Spatial predator–prey dynamics** (`predator-prey`)
Prey and predator populations per cell grow, die and migrate, producing travelling waves
and patches (Lotka–Volterra-type dynamics as a lead — to be verified). *Data:* habitat
suitability from land cover; otherwise mostly synthetic. *Why:* classic emergent
behaviour; weak link to real geodata.

**ECO-07 · Climate-driven shift of species ranges / tree line** (`species-range-shift`)
Suitable habitat moves upslope or northward with warming, and species follow with
limited dispersal speed. *Data:* DEM, climate scenarios, current species or forest-type
distribution. *Why:* visualises climate change impact on Czech mountains and forest
composition (e.g. spruce at lower elevations — to be verified).

**ECO-08 · Self-organised vegetation patterns** (`vegetation-patterns`)
Local facilitation and competition for water create spots, stripes or labyrinths of
vegetation (Turing-type patterns as a lead — to be verified). *Data:* DEM (slope),
rainfall; essentially synthetic for Europe. *Why:* beautiful emergent patterns;
didactically strong, but little relevance to CZ landscapes.

## LND — Landscape and land use

**LND-01 · Urban growth and suburbanisation** (`urban-growth`) `CZ`
Built-up area grows from existing settlements, attracted by roads and limited by slope
and protected areas. Classic CA application (SLEUTH-type models as a lead — to be
verified). *Data:* historical land cover (CORINE, Urban Atlas — to be verified), roads,
DEM, protected areas. *Why:* very relevant around Prague and other cities; validation by
comparing historical land-cover snapshots.

**LND-02 · Farmland abandonment and overgrowth** (`farmland-abandonment`) `CZ`
Abandoned meadows and fields gradually overgrow with shrubs and forest, faster near
existing forest. *Data:* land cover time series, DEM (remoteness, slope), historical
maps. *Why:* tells the story of Czech border regions after 1945; links to wildfire fuel
and habitat connectivity.

**LND-03 · Filling of post-mining lakes** (`post-mining-lake`) `CZ`
A mining pit fills with water from rivers and groundwater, gradually flooding its
terrain until the target level. *Data:* DEM of the pit (to be verified whether open),
inflow scenarios. *Why:* specific to North Bohemian lignite region (e.g. lake Most —
to be verified); simple, reuses water-filling mechanics.

## URB — City and infrastructure

**URB-01 · Urban heat island** (`urban-heat-island`)
Surface temperature per cell depends on surface type and is smoothed by exchange with
neighbours; green and blue areas cool their surroundings. *Data:* land cover / imperviousness,
building footprints, greenery, (to be verified) satellite land-surface temperature for
comparison. *Why:* topical for city planning; "plant a park and see" interaction.
Physically an energy-balance problem — CA only as an approximation.

**URB-02 · Pluvial flooding in cities** (`pluvial-urban-flood`) ★
Intense rain on streets and roofs flows over a surface model with buildings and collects
in underpasses and low spots (sewer capacity simplified). *Data:* DSM/DTM with
buildings, imperviousness, rainfall. *Why:* very relatable (flooded streets and
underpasses); variant of surface runoff in urban setting.

**URB-03 · Fire spread in a historic town** (`urban-fire`) `CZ`
Fire jumps between buildings depending on distance, building material and wind.
*Data:* building footprints, (to be verified) building materials / roof types, wind.
*Why:* unusual historical angle (historic town fires); reuses wildfire mechanics on a
different "fuel" layer.

**URB-04 · Cascading infrastructure failures** (`infrastructure-cascade`)
Failure of a power substation propagates to dependent water, telecom and transport
services. *Data:* infrastructure networks (mostly not open — to be verified). *Why:*
important topic, but mainly a network problem rather than a raster CA — included as a
boundary case.

## ATM — Atmosphere and pollution

**ATM-01 · Air pollutant and smoke dispersion** (`pollutant-dispersion`) `CZ`
Pollutant concentration is transported by wind and spreads to neighbouring cells
(simplified advection–diffusion); includes smoke from a wildfire as a scenario.
*Data:* emission sources, wind field, DEM, (to be verified) air-quality monitoring
stations for comparison. *Why:* relevant for inversion smog in basins (e.g. Ostrava
region — to be verified) and for wildfire smoke; only an approximation of physics.

**ATM-02 · Cold-air pooling and frost hollows** (`cold-air-pooling`) `CZ`
On clear calm nights, cold dense air drains downslope and accumulates in valleys and
basins, creating frost hollows. *Data:* DEM, land cover (forest vs. open land),
(to be verified) temperature station data. *Why:* unusual but intuitive; reuses
water-like flow routing for air; known Czech frost hollows could serve as cases (to be
verified).

**ATM-03 · Heavy-gas release** (`heavy-gas-release`)
A gas heavier than air leaks from an industrial source and flows along terrain into low
places, diluting over time. *Data:* DEM, building footprints, source location, wind.
*Why:* civil protection scenario; combines gravity flow with dispersion; sensitive topic
to be handled as a purely illustrative demo.

**ATM-04 · Agricultural drought propagation** (`agricultural-drought`) `CZ`
Soil moisture decreases with lack of rain and high temperature, depending on soil and
land cover; dry areas expand. *Data:* soil type, land cover, precipitation and
temperature series, (to be verified) soil-moisture monitoring products for CZ. *Why:*
highly topical in CZ; but mostly a cell-local water balance with weak neighbour
interaction.

## EPI — Spread of diseases and populations

**EPI-01 · Spatial epidemic (SIR on a population grid)** (`spatial-epidemic`)
Each cell holds susceptible / infected / recovered population; infection spreads locally
and through commuting. SIR-type compartment models as a lead (to be verified). *Data:*
population grid (to be verified), commuting or transport data. *Why:* widely understood
after COVID-19; but human mobility is strongly non-local.

**EPI-02 · African swine fever in wild boar** (`wild-boar-asf`) `CZ`
Infection spreads among wild boar groups through the forest landscape; fences and
culling zones slow it down. *Data:* forest cover, habitat suitability, roads, fences,
(to be verified) reported outbreak locations. *Why:* CZ dealt with an ASF outbreak
(details to be verified); demo of containment measures; links to habitat connectivity.

**EPI-03 · Tick-borne disease risk** (`tick-borne-risk`) `CZ`
Tick habitat suitability and activity change with vegetation, moisture and temperature;
risk spreads with hosts and shifts with climate. *Data:* land cover, DEM, climate
series, (to be verified) disease incidence statistics. *Why:* CZ is known for
tick-borne encephalitis (to be verified); mostly suitability mapping rather than
spread — CA fit questionable.

## MOV — Movement of people and traffic

**MOV-01 · Pedestrian evacuation** (`pedestrian-evacuation`)
Pedestrians move cell by cell towards exits or safe areas, avoiding obstacles and
congestion (floor-field-type models as a lead — to be verified). *Data:* building
footprints, street network, open spaces, population or scenario crowd. *Why:* natural
follow-up to flood and fire scenarios; visible congestion emerges.

**MOV-02 · Road traffic flow** (`traffic-flow`)
Vehicles move along road cells with simple acceleration and braking rules, producing
spontaneous traffic jams (Nagel–Schreckenberg-type model as a lead — to be verified).
*Data:* road network (OpenStreetMap — to be verified), traffic intensity counts.
*Why:* classic CA; but it lives on a 1D network, not on a 2D geographic raster.

**MOV-03 · Accessibility front / travel-time spreading** (`accessibility-front`)
A front spreads from a source over a cost surface (terrain, roads, land cover), showing
how far one can get in a given time — e.g. emergency service reach or walking access.
*Data:* road network, land cover, DEM, locations of services. *Why:* cheap, intuitive;
shares the "front propagation over a cost raster" mechanism with fire and animal
dispersal.

## Links and chains of phenomena

Linked scenarios — the output of one model becomes the input of another — could be a
distinctive strength of the demo ("the landscape is a system"). Proposed chains:

| # | Chain | Items | What the user would see |
|---|---|---|---|
| L1 | Wildfire → loss of vegetation → higher runoff → erosion / muddy flood | HAZ-01 → HYD-01 → HYD-05 | the same storm causes much more damage on a burnt slope |
| L2 | Drought → bark-beetle outbreak → dead spruce stands → higher wildfire hazard | ATM-04 → ECO-01 → HAZ-01 | how a forest crisis becomes a fire risk (relevant to recent CZ events — to be verified) |
| L3 | Windthrow → breeding material → bark-beetle outbreak | HAZ-04 → ECO-01 | one storm starts a multi-year outbreak |
| L4 | Disturbance (fire / beetle / windthrow) → succession → recovered forest | HAZ-01, ECO-01, HAZ-04 → ECO-02 | closing the loop on long time scales |
| L5 | Intense rain → runoff → flash flood → fishpond cascade breach → downstream flood | HYD-01 → HYD-03 → HYD-04 → HYD-02 | domino effect in a typical Czech landscape |
| L6 | Snowmelt + rain → river flood | HYD-06 → HYD-02 | spring flood genesis |
| L7 | Saturation → landslide → river blockage → natural dam breach | HAZ-02 → HYD-04 / HYD-02 | a hazard creating another hazard |
| L8 | Urban growth → more impervious surface → pluvial flooding, stronger heat island | LND-01 → URB-02, URB-01 | consequences of planning decisions |
| L9 | Farmland abandonment → continuous vegetation → fuel for fire; better habitat connectivity | LND-02 → HAZ-01, ECO-04 | land-use history shapes present hazards |
| L10 | Beaver dams → water retention → lower flood peak downstream | ECO-05 → HYD-02 | nature-based flood mitigation |
| L11 | Wildfire → smoke dispersion → air quality in nearby towns | HAZ-01 → ATM-01 | impact beyond the burnt area |
| L12 | Flood / fire / gas release → evacuation and accessibility of emergency services | HYD-02, HAZ-01, ATM-03 → MOV-01, MOV-03 | the human side of a hazard (closed roads, congestion) |
| L13 | Habitat connectivity → spread of disease among wild animals; fences as barriers | ECO-04 → EPI-02 | containment by landscape barriers |
| L14 | Climate warming → drought, species range shift, tick habitat shift | ATM-04, ECO-07, EPI-03 | one driver, many responses |

Observations for the review phase (not decisions):

- **Mechanism families** recur: *gravity-driven flow* (water, mud, debris, avalanche,
  lava, cold air, heavy gas), *contagious spread* (fire, beetle, disease, invasive
  species), *front over a cost surface* (accessibility, animal dispersal, fire arrival
  time), *growth / succession* (urban growth, overgrowth, forest recovery),
  *diffusion / advection* (pollution, smoke, heat). This is relevant for
  `docs/review/shared-components.md`.
- **The confirmed "water flow / flooding" model spans several items** (HYD-01, HYD-02,
  HYD-03, URB-02, partly HYD-04 and LND-03). Whether these are one model with
  scenarios or separate models is an open question for the review.
- Chains require **compatible time scales** (minutes for floods vs. years for succession)
  and **compatible grids**; how to hand over state between models is an open
  architectural question.
- Items with weak CA fit (URB-04, MOV-02, EPI-03, ATM-04) are kept deliberately as
  boundary cases to make the scope explicit.
