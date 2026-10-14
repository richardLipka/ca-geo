# Terminology glossary (EN–CS)

Working glossary of key terms used in the documentation. It is the basis for the future
`cs` / `en` translation catalogues of the web demos, so the Czech term should be the one
we want to show in the UI.

Rules:

- Add a term whenever it first appears in a document that may end up in the UI or in an article.
- Keep entries alphabetical within each section.
- Use the *Note* column for alternative translations, terms to avoid, or open doubts
  (mark with `?` when the Czech term is not settled).

## Cellular automata — core concepts

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| asynchronous update | asynchronní aktualizace | Cells are updated one by one (in some order or randomly); updated values are immediately visible to the others. | |
| boundary condition | okrajová podmínka | Rule defining how cells at the edge of the grid see their missing neighbours. | |
| absorbing boundary | pohlcující okraj | Boundary where anything leaving the grid is lost (e.g. water flows out). | also "otevřený okraj" |
| fixed (constant) boundary | pevný (konstantní) okraj | Cells outside the grid have a fixed prescribed state. | |
| periodic (toroidal) boundary | periodický (toroidální) okraj | Opposite edges of the grid are connected. | rarely meaningful for geodata |
| reflective boundary | odrazný okraj | Boundary that mirrors the state of edge cells; nothing leaves the grid. | |
| cell | buňka | Elementary spatial unit of the automaton; here usually one raster pixel. | |
| cell size | velikost buňky | Ground length of a cell side (spatial resolution). | cf. *resolution* |
| cell state | stav buňky | Value(s) held by a cell at a given time step. | |
| cellular automaton (CA) | celulární automat (CA) | Discrete model: grid of cells, each updated by a local rule from its own state and its neighbours' states. | plural: celulární automaty |
| deterministic model | deterministický model | Same initial state always produces the same evolution. | |
| grid / lattice | mřížka | Regular arrangement of cells (here typically square). | "síť" possible, but "mřížka" preferred |
| hexagonal grid | hexagonální mřížka | Grid of hexagonal cells; all neighbours equidistant. | |
| initial condition | počáteční podmínka | Cell states at time step 0. | |
| iteration | iterace | One application of the transition rule to the whole grid. | often = time step |
| Moore neighbourhood | Moorovo okolí | The 8 cells surrounding a cell (including diagonals). | |
| neighbour | soused | Cell belonging to another cell's neighbourhood. | |
| neighbourhood | okolí | Set of cells whose states influence a cell's next state. | "sousedství" also used; prefer "okolí" |
| random seed | semínko náhodného generátoru | Initial value of the pseudo-random generator; makes stochastic runs reproducible. | ? alternative: "počáteční hodnota generátoru" |
| state variable | stavová proměnná | One quantity stored per cell (e.g. water depth, fuel load). | |
| stochastic model | stochastický model | Evolution depends on random events; runs differ unless the seed is fixed. | |
| synchronous update | synchronní aktualizace | All cells compute their next state from the same previous state, then switch at once. | |
| time step | časový krok | Discrete advance of model time; may correspond to a real duration. | |
| transition rule | přechodové pravidlo | Function that computes a cell's next state from its neighbourhood. | also "pravidlo přechodu" |
| von Neumann neighbourhood | von Neumannovo okolí | The 4 orthogonally adjacent cells (N, E, S, W). | |

## Geodata — core concepts

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| digital elevation model (DEM) | digitální výškový model | Raster of terrain elevations; umbrella term for DTM and DSM. | Czech practice distinguishes DMR/DMP, see below |
| digital surface model (DSM) | digitální model povrchu (DMP) | Elevation including buildings and vegetation. | |
| digital terrain model (DTM) | digitální model reliéfu (DMR) | Elevation of bare ground. | |
| land cover | krajinný pokryv | Physical cover of the surface (forest, water, built-up…). | vs. *land use* |
| land use | využití území | How people use the land (agriculture, housing…). | |
| layer | vrstva | One thematic raster or vector dataset. | |
| open data | otevřená data | Data published under a licence permitting free reuse. | |
| raster | rastr | Grid of values covering an area; natural input for CA. | |
| resolution (spatial) | prostorové rozlišení | Ground size of one raster cell. | |

## Modelling and evaluation

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| calibration | kalibrace | Tuning model parameters so that results match observations. | |
| ensemble (of runs) | soubor simulací | Repeated runs of a stochastic model with different seeds; summarised e.g. as probability maps. | ? "ansámbl" is used in meteorology; prefer "soubor simulací" in UI |
| mass conservation | zachování hmoty | Property that a quantity (e.g. water volume) is neither created nor lost by the rule. | |
| parameter | parametr | Constant controlling the rule (not a per-cell state). | |
| scenario | scénář | Specific combination of inputs and parameters to be simulated and compared. | |
| update scheme | schéma aktualizace | Order in which cells are updated (synchronous / asynchronous). | |
| validation | validace | Comparison of model results with independent observations. | vs. *verification* (ověření správnosti implementace) |
| weighted score | vážené skóre | Weighted average of criterion scores used to rank candidates. | used in docs/review |

## Phenomena (from the longlist)

Czech names proposed for the UI; to be reviewed together with the model cards.

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| accessibility | dostupnost | How far / how fast a place can be reached from a source. | |
| African swine fever (ASF) | africký mor prasat (AMP) | Viral disease of pigs and wild boar. | |
| air pollutant dispersion | rozptyl znečišťujících látek | Spreading of pollutants in the air by wind and mixing. | |
| avalanche | lavina | Rapid flow of snow down a slope. | |
| bark beetle | kůrovec (lýkožrout smrkový) | Insect attacking spruce; cause of large-scale forest dieback. | "kůrovec" in UI, species name in docs |
| bark-beetle outbreak | kůrovcová kalamita | Mass outbreak of bark beetles killing forest stands. | |
| beaver dam | bobří hráz | Dam built by beavers on a stream. | |
| cold-air pooling | stékání a hromadění studeného vzduchu | Night-time drainage of cold air into valleys. | ? shorter UI label needed; "jezero studeného vzduchu" for the pool itself |
| dam breach | protržení hráze | Failure of a dam releasing stored water. | |
| debris flow | mura (bahnokamenný proud) | Fast flow of water-saturated debris in a channel. | ? check usage |
| erosion | eroze | Removal of soil by water or wind. | |
| evacuation | evakuace | Moving people out of a threatened area. | |
| fishpond | rybník | Artificial pond for fish farming, typical of Czech landscape. | |
| flash flood | přívalová povodeň | Rapid flood caused by short intense rainfall. | |
| flood | povodeň | Temporary rise of water flooding normally dry land. | |
| floodplain | údolní niva | Flat land along a river regularly flooded. | |
| flood zone | záplavové území | Officially designated area flooded by a given flood. | |
| frost hollow | mrazová kotlina | Depression where cold air collects, causing frequent frost. | |
| habitat connectivity | konektivita (propojenost) krajiny | Ability of animals to move between habitats. | |
| heavy gas | těžký plyn | Gas denser than air, flowing along the ground. | |
| inundation | zaplavení, rozliv | Area or process of water spreading over land. | |
| invasive species | invazní druh | Non-native species spreading and causing harm. | |
| landslide | sesuv (svahový sesuv) | Downslope movement of soil or rock mass. | |
| lava flow | lávový proud | Flow of molten rock from a vent. | |
| muddy flood | bahnitá povodeň, erozní smyv | Runoff carrying large amounts of eroded soil from fields. | ? settle term |
| pluvial flooding | přívalové zaplavení z dešťů (pluviální povodeň) | Flooding caused directly by rainfall, not by a river. | ? settle term |
| runoff (surface) | povrchový odtok | Water flowing over the ground surface. | |
| snowmelt | tání sněhu | Melting of snow cover releasing water. | |
| succession | sukcese | Natural sequence of vegetation stages on a site. | |
| suburbanisation | suburbanizace | Growth of residential areas around cities. | |
| tick-borne encephalitis | klíšťová encefalitida | Viral disease transmitted by ticks. | |
| urban heat island | městský tepelný ostrov | Higher temperatures in cities compared to surroundings. | |
| wildfire | požár v přírodě (lesní požár) | Uncontrolled fire in vegetation. | "lesní požár" common, but not all are in forests |
| windthrow | polom (větrná kalamita) | Trees uprooted or broken by wind. | |

## Additions from literature review round 1

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| aquifer | zvodeň (kolektor) | Rock or soil layer holding and transmitting groundwater. | "zvodeň" for the water body, "kolektor" for the layer |
| carrying capacity | nosná kapacita (prostředí) | Maximum population a cell's habitat can sustain. | |
| colonisation front | čelo kolonizace (šíření) | Moving boundary of the area occupied by a spreading population. | |
| containment zone | pásmo omezení (ochranné pásmo) | Area with control measures to stop a spread. | ? term varies by domain (veterinary: "uzavřené pásmo") |
| fetch | délka rozběhu větru (fetch) | Distance of open water over which wind blows and builds waves. | ? check hydrology usage |
| groundwater | podzemní voda | Water in saturated soil and rock below the surface. | |
| hydraulic head | piezometrická výška | Height to which groundwater would rise; drives groundwater flow. | ? "hydraulická výška" also used |
| long-distance dispersal | šíření na velké vzdálenosti | Rare jumps far beyond the local neighbourhood. | |
| oil spill | únik ropných látek, ropná skvrna | Release of oil onto water; "skvrna" for the floating slick. | |
| pathogen | patogen (původce choroby) | Organism causing disease in plants or animals. | |
| reimplementability | reimplementovatelnost | How well a model can be re-implemented from its publication. | used in docs/research |
| shoreline erosion | abraze (eroze) břehů | Wave-driven erosion of lake, reservoir or sea shores. | "abraze" is the technical term for reservoirs |
| snow drift | sněhová závěj, sněhový jazyk | Accumulation of wind-blown snow. | "jazyk" for elongated drift |
| water table | hladina podzemní vody | Upper surface of the saturated zone. | |

## Additions from literature review round 2

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| commuting | dojížďka | Regular travel between home and work municipality. | |
| language shift | jazykový posun | Change of a population's dominant language over time. | |
| oral vaccination (of wildlife) | orální vakcinace | Vaccine baits distributed in the landscape. | |
| rabies | vzteklina | Viral disease of mammals spread by bites. | |
| rockfall | skalní řícení, opad kamenů | Free fall, bouncing and rolling of rock fragments. | |
| sinkhole | závrt (krasový), propad | Surface depression from collapse of an underground cavity. | "závrt" for karst, "propad" generic |
| snow redistribution (gravitational) | gravitační přemisťování sněhu | Sliding or sloughing of snow from steep slopes. | |
| ventilation corridor | ventilační (provětrávací) koridor | Path of cold or fresh air flowing into a town. | |
| voter model | voličský model | Opinion model where agents copy a neighbour's opinion. | ? term rarely used in Czech |

## Engine and simulation (architecture)

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| arrival time | čas příchodu (čela) | Time when a front (fire, water, population) first reaches a cell. | UI output |
| backend | výpočetní backend | Implementation executing the engine (CPU or GPU). | technical, not for UI |
| boundary flux | tok přes okraj | Amount leaving or entering the domain across its edge. | |
| engine | výpočetní jádro (engine) | Software running the cellular automaton. | |
| flux | tok | Amount exchanged between two cells per time step. | |
| front | čelo | Moving boundary of a spreading process. | |
| intervention | zásah | User action changing the simulation (ignite, dam, barrier). | UI |
| mass balance | bilance hmoty | Check that inputs − outputs = change of storage. | UI (water) |
| maximum envelope | obálka maxim | Per-cell maximum over the run (e.g. max water depth). | |
| probability map | mapa pravděpodobnosti | Share of ensemble runs in which a cell was affected. | UI |
| replay | přehrání (běhu) | Exact re-run from stored seed, inputs and interventions. | |
| scenario | scénář | (see above) | |
| stage | fáze kroku | One processing step within a simulation time step. | technical |

## Additions from the model cards (2026-10-14)

Terms collected from section 16 ("Terminology (cs)") and the text of the 14 model cards.
Definitions are short working definitions; to be reviewed before they are used in the UI.

| English term | Czech term | Short definition | Note |
|---|---|---|---|
| active list | seznam aktivních buněk | Cells that still have material or energy to distribute. | front primitive |
| adaptive time step | adaptivní časový krok | Δt recomputed from current velocities / stability | SC-ADT |
| adherence | adheze (nepohyblivá vrstva) | Thickness of material that cannot leave a cell. | SCIDDICA p_adh |
| advection | advekce | Transport of a substance by the moving air or water. |  |
| allocation | alokace | Assigning demanded change to the highest-ranked cells. | engine `allocate` |
| allocation disagreement | nesoulad v umístění | Difference due to the different placement of classes. | Pontius |
| anisotropic cost | anizotropní náklad | cost depending on direction of movement |  |
| ash dieback | nekróza jasanu | Fungal disease of ash (*Hymenoscyphus fraxineus*). |  |
| back-tracking | zpětné dohledání | Finding source cells whose paths reach a given target. | UI action |
| background concentration | pozaďová koncentrace | Concentration not caused by the modelled local source. |  |
| barrier permeability | propustnost bariéry | fraction of movement allowed across an edge | slot weight |
| beetle generations per year | počet generací za rok | Number of beetle generations completed in a season. |  |
| boom / bust | konjunktura / útlum | Years with growth rate above / below thresholds that trigger self-modification. |  |
| Boyce index | Boyceův index | Agreement of a suitability / risk map with presence points. | metric |
| breed coefficient | koeficient zakládání | Controls the chance of new spreading centres and the number of road trips. |  |
| buffer strip | ochranný (travní) pás | grass strip that slows runoff and traps sediment | HYD-05 intervention |
| buffer zone | nárazníková zóna | Zone where hosts are surveyed and removed. | cf. *containment zone* |
| burn-probability map | mapa pravděpodobnosti vyhoření | Share of ensemble runs in which a cell burnt. | specialisation of *probability map* |
| burnt / burning / unburnt (cell) | vyhořelá / hořící / nezasažená (buňka) | Fire states of a cell. |  |
| catastrophic mortality event | katastrofická úmrtnost (katastrofa) | rare event killing a large share of a cell's population |  |
| clogging | ucpání | jam at a bottleneck |  |
| cold-air drainage | stékání studeného vzduchu | Downslope flow of cold, dense air on calm clear nights. |  |
| cold-air layer height | výška (mocnost) vrstvy studeného vzduchu | Thickness of the cold-air layer above the ground. | state variable |
| cold-air pool | jezero studeného vzduchu | Body of cold air collected in a valley or depression. | glossary note already mentions it under cold-air pooling |
| cold-air production | produkce studeného vzduchu | Rate at which a land-cover class generates cold air (m h⁻¹). | parameter |
| concentration | koncentrace | Amount of pollutant per volume of air. |  |
| conflict | konflikt | two or more agents choosing the same target cell |  |
| connected-component labelling | značkování souvislých oblastí | Assigning one id to each contiguous cluster of cells. |  |
| constrained cellular automaton | omezený (poptávkou řízený) celulární automat | CA whose total change per class is fixed by exogenous demand. | White–Engelen family |
| corridor | koridor | feature that speeds up / extends movement |  |
| corridor (linear feature) | koridor (liniový prvek) | Road, railway or river guiding spread. | ECO-03 |
| cost surface / friction surface | nákladový povrch / povrch tření | raster of the cost (time) to cross each cell | "friction" here ≠ pedestrian friction |
| Courant number | Courantovo číslo | ratio of distance travelled in Δt to cell size | CFL |
| critical shear stress | kritické tečné napětí | shear stress above which soil is detached | HYD-05 |
| critical slope | kritický sklon | Slope above which urbanisation is impossible. |  |
| crowd density | hustota davu | persons per area |  |
| demic diffusion | démická difuze | spread of a culture by migration of people (not ideas) | archaeology term |
| deposition | depozice | Removal of a pollutant to the ground surface. |  |
| depression filling | vyplňování bezodtokých depresí | raising pits to their spill level | SC-FILL |
| development pressure | rozvojový tlak | Distance-weighted amount of nearby development. | FUTURES |
| disease incidence | incidence choroby | Fraction of hosts infected. | ECO-09 |
| dispersal kernel | disperzní jádro | Weight of dispersal as a function of distance. |  |
| dispersion coefficient (SLEUTH) | koeficient rozptylu | Controls the number of spontaneous trials and the road-walk length. | not the same as atmospheric dispersion |
| distance transform | vzdálenostní transformace | Raster of distance from each cell to the nearest feature cell. |  |
| distance-decay weight | váha klesající se vzdáleností | Weight that decreases with distance from the cell. |  |
| divergence exponent | exponent rozbíhavosti | Exponent controlling lateral spreading in multiple-flow-direction routing. |  |
| diversion barrier | odkloňovací val | Built obstacle meant to deflect a flow. | UI action |
| drawdown cone | depresní kužel | lowered water table around a pumping well | HYD-09 |
| dynamic floor field | dynamické podlahové pole | decaying trace left by moving pedestrians |  |
| edge (organic) growth | okrajový růst | Urbanisation of cells next to existing urban clusters. | SLEUTH phase |
| effective surface (effective elevation) | efektivní povrch (efektivní výška) | Terrain elevation plus the thickness of the flowing layer (water, cold air, lava, debris). | shared concept of gravity-flow models |
| effusion rate | rychlost výlevu (efuze) | Volume of lava erupted per unit time. |  |
| emigration | emigrace (odchod) | individuals leaving a cell for neighbours |  |
| emigration threshold | práh emigrace | fraction of carrying capacity above which emigration starts | φ |
| energy line | energetická čára | Line falling at the runout angle from the release; height above terrain ~ kinetic energy. |  |
| energy-line height | výška energetické čáry | Height of the energy line above terrain (kinetic-energy height). | Flow-Py Z^δ |
| eradication zone | zóna eradikace | Zone where all hosts are removed. |  |
| evacuation time | doba evakuace | time until the last person leaves |  |
| exclusion layer | vrstva vyloučených ploch | Raster of resistance to development; full exclusion for water, protected areas. |  |
| exit | východ |  |  |
| exposure | expozice | Concentration and duration experienced at a place. |  |
| figure of merit | míra shody změn (figure of merit) | Correctly predicted change divided by the union of observed and predicted change. |  |
| fire spotting | přeskok požáru (vznik sekundárních ohnisek) | New ignitions ahead of the front started by embers. | ? check fire-service usage |
| firebrand (ember) | letící žhavá částice | Burning fragment carried by the plume. |  |
| firebreak | protipožární průsek | Strip without fuel that stops spread. | UI |
| first-arrival time | čas prvního příchodu | first time a cell becomes occupied / reached | extends "arrival time" |
| flow resistance | odpor proudění | Land-cover-dependent factor slowing the cold-air flow. | parameter |
| flux cutoff | práh toku | Minimum flux below which routing to a neighbour stops. |  |
| friction (pedestrian conflict) | tření (konflikt chodců) | probability that no one moves in a conflict | μ |
| front speed | rychlost čela | distance advanced by the front per unit time |  |
| fuel (type) | palivo (typ paliva) | Burnable material classified for the fire model. |  |
| fuel moisture | vlhkost paliva | Water content of dead fuel; reduces spread. |  |
| Fuzzy Kappa | fuzzy kappa | Map agreement statistic giving partial credit to nearby matches. |  |
| giant hogweed | bolševník velkolepý | Invasive plant (*Heracleum mantegazzianum*). |  |
| Gompertz growth | Gompertzův růst | Sigmoid growth curve used for local infection build-up. |  |
| gravitational mass flow | gravitační svahový proud | Common term for debris flows, avalanches, rockfall, landslides. |  |
| growth rate | míra růstu | per-step relative increase of a population |  |
| heat-loss rate | míra tepelné ztráty | Local radiative heat loss of the cold layer (W m⁻²). | KLAM variant |
| herding | stádní chování | tendency to follow others |  |
| hiking function (Tobler) | Toblerova funkce chůze | walking speed as a function of slope |  |
| host cover | pokryvnost hostitelských rostlin | Share of a cell covered by host plants. |  |
| ignition | zapálení | Transition of a cell to burning. | UI: "zapálit" |
| incentive power | exponent pobídky | Exponent applied to development probability to favour infill or sprawl. | FUTURES |
| infestation level | stupeň napadení | Class of the number of infested trees in a cell. | ECO-01 |
| infestation spot | kůrovcové ohnisko | Patch of trees killed by bark beetles in one year. |  |
| infill / sprawl | zahušťování / rozrůstání (sprawl) | Compact growth inside / scattered growth outside existing settlements. |  |
| inflow hydrograph | přítokový hydrogram | time series of discharge entering the domain |  |
| inundation probability | pravděpodobnost zaplavení | Share of ensemble runs in which a cell is covered by the flow. | lava output |
| isochrone | izochrona | line of equal travel / arrival time |  |
| katabatic flow | katabatické proudění | Gravity-driven downslope wind of cooled air. | technical synonym |
| kernel density estimation | jádrový odhad hustoty | Smoothing of point events with a kernel to obtain a density surface. |  |
| land demand | poptávka po ploše | Number of cells that must change to a class in a step. |  |
| land-use regression | regresní model využití území (LUR) | Statistical model predicting concentration from land-use predictors. |  |
| least-cost distance | nákladová vzdálenost | minimal accumulated cost to a source |  |
| least-cost path | cesta s nejmenšími náklady | route realising the least-cost distance |  |
| Lee–Sallee index | Lee–Salleeho index | Intersection over union of simulated and observed urban areas. | SLEUTH |
| level–volume curve | čára objemů (vztah hladina–objem) | lake / reservoir volume as a function of water level | LND-03 |
| local inertial model | model s lokální setrvačností | shallow-water simplification without convective acceleration | bates2010simple |
| logistic growth | logistický růst | growth slowing to zero at carrying capacity |  |
| Manning roughness coefficient | Manningův součinitel drsnosti | friction parameter in Manning's velocity formula |  |
| mass-to-drag ratio | poměr hmotnosti a odporu | PCM friction parameter M/D controlling velocity. | GPP, Flow-R |
| maximum depth map | mapa maximálních hloubek | envelope of depth over the run | observer |
| metamodel | metamodel | Simplified model trained on the output of a detailed model. | technical |
| metrication error | metrikační chyba | distance error from restricting moves to grid directions | ? |
| minimisation of differences | minimalizace rozdílů | Outflow rule that equalises heights among the cell and its neighbours. | SCIDDICA, SCIARA |
| minimum viable population | minimální životaschopná populace | size below which extra mortality applies |  |
| mobilisation (erosion) of soil cover | mobilizace (eroze) půdního pokryvu | Entrainment of erodible soil by the flow. | SCIDDICA |
| monitoring station | monitorovací stanice | Fixed site measuring air quality. |  |
| neighbourhood effect | vliv okolí | Distance-weighted attraction or repulsion of land uses around a cell. |  |
| neutral model | neutrální model | Simple benchmark model with the same amount of change. |  |
| new spreading centre | nové centrum šíření | Spontaneously urbanised cell that immediately urbanises some neighbours and can grow into a cluster. | SLEUTH phase |
| non-burnable | nehořlavý | Cell that cannot burn (water, rock, road). |  |
| obstacle | překážka |  |  |
| outflow (cell) | odtok z buňky | volume a cell sends to a neighbour in one step | flux layer |
| outflow (of people) | průtok osob (východem) | persons leaving per unit time |  |
| parent cell | rodičovská buňka | Neighbour from which a cell received material; excluded as a receiver. | front primitive |
| patch growth | růst ploch (záplat) | Growing a contiguous group of new cells from a seed. | FUTURES, PLUS |
| pedestrian | chodec |  |  |
| persistence | setrvačnost směru (perzistence) | Preference for keeping the previous flow direction. |  |
| population dispersal | šíření populace | spread of a population over a landscape by growth and emigration | phenomenon EPI-04 |
| primary attractiveness | primární atraktivita (stromu) | Host-tree attraction to beetles before pheromones. |  |
| priority queue | prioritní fronta | data structure popping the smallest key first | engine |
| process intensity | intenzita procesu | Measure of the strength of the flow at a cell (e.g. max energy-line height). |  |
| propose–resolve | návrh–rozhodnutí (konfliktu) | two-phase parallel agent update | engine; ? |
| protective forest | ochranný les | Forest that reduces or stops mass flows. |  |
| pulse (volume) | pulz (objem pulzu) | Portion of the total volume added at the source in one iteration. | lava |
| pumping well | čerpaný vrt | well extracting groundwater | HYD-09 |
| quantity disagreement | nesoulad v množství | Difference between two maps due to different class totals. | Pontius |
| random walk (path) | náhodná procházka (dráha) | Stochastic choice of the next cell along a mass-flow path. | GPP |
| rate of spread (ROS) | rychlost šíření požáru | Front speed in m/min. |  |
| recharge | dotace podzemní vody | water entering the aquifer from above | HYD-09 |
| relative risk | relativní riziko | Risk under control relative to no control. |  |
| relaxation (shortest path) | relaxace (nejkratší cesty) | updating a cell's value from a neighbour + edge cost | engine |
| relaxation rate | relaxační koeficient | Fraction of the equilibrium outflow applied in one step. |  |
| release zone (starting zone) | odtrhová (zdrojová) oblast | Area where a mass flow starts. |  |
| residual thickness | zbytková mocnost | Thickness a cell retains before passing material on. | lava; cf. adherence |
| Ricker model | Rickerův model | discrete growth N·exp(r(1 − N/K)) |  |
| rill | erozní rýha | small channel cut by runoff | HYD-05 |
| rill flow | soustředěný odtok v rýhách | concentrated flow in small erosion channels | HYD-05 |
| risk map | mapa rizika | Mean incidence over ensemble runs. |  |
| road gravity | přitažlivost silnic | Controls how far from new growth a road is searched for. |  |
| road-influenced growth | růst podél silnic | Urbanisation reached by searching for and travelling along roads from new growth. | SLEUTH phase |
| roughness length | délka drsnosti | Aerodynamic roughness parameter z₀ of the surface. | KLAM variant |
| roulette-wheel selection | výběr ruletou | Random choice with probability proportional to weight. |  |
| routing flux | směrovaný tok | Share of the unit start flux routed through a cell. | Flow-Py R |
| run-up | výběh (výška výběhu) | Height reachable by the flow: thickness plus kinetic head. | SCIDDICA |
| runout | dosah (dojezd) | Distance or area reached by a mass flow until it stops. |  |
| runout angle (travel angle) | úhel dosahu | Angle of the line from the release top to the farthest point reached. | Heim's Fahrböschung |
| runout zone | oblast dojezdu (akumulace) | Area where the flow decelerates and stops. |  |
| safe zone | bezpečná zóna | area considered safe in an evacuation |  |
| sanitation felling | asanační těžba | Removal or debarking of infested trees. | UI |
| saturated hydraulic conductivity | nasycená hydraulická vodivost | infiltration / Darcy rate at saturation | HYD-05, HYD-09 |
| sediment load | množství unášených splavenin | sediment carried by flow | HYD-05 |
| self-modification | samomodifikace | Automatic change of model coefficients from global growth statistics. |  |
| sheet flow | plošný odtok | thin overland flow over the whole cell | HYD-05 |
| sliding friction coefficient | součinitel smykového tření | Coulomb-type friction μ of a mass flow. | GPP, Flow-R |
| slope resistance | odpor svahu | Controls how strongly steep slopes reduce urbanisation. |  |
| smoke plume | kouřová vlečka | Elongated cloud of smoke carried downwind. |  |
| sorptivity | sorptivita | soil parameter of the Philip infiltration equation | HYD-05 |
| spatial density (of vents) | prostorová hustota (průduchů) | Probability density of future source locations from past events. | kernel density estimate |
| specific yield | specifická vydatnost (gravitační pórovitost) ? | water released per unit drop of the water table | HYD-09; ? settle term |
| speed conservation value | koeficient zachování rychlosti | fraction of maximum speed kept on a surface | ? term not settled |
| spontaneous growth | spontánní růst | Urbanisation of randomly chosen cells anywhere in the domain. | SLEUTH phase |
| spread coefficient | koeficient šíření | Controls the chance of edge growth from urban cells. |  |
| static floor field | statické podlahové pole | field increasing towards exits |  |
| step rejection | zamítnutí (opakování) kroku | recomputing a step with smaller Δt | engine, NEW-RETRY |
| storm drain inlet | uliční vpusť | sink cell draining water to the sewer | URB-02 |
| stratified dispersal | stratifikované šíření | Local spread combined with rare long jumps. |  |
| streambed conductance | vodivost dna toku | coefficient of river–aquifer exchange | HYD-09 |
| suitability | vhodnost | Static fitness of a cell for a land use (e.g. from slope). |  |
| surface retention | povrchová retence | water held on the surface before runoff starts | HYD-05 |
| surveillance efficiency | účinnost dozoru | Probability that an infected cell is detected. |  |
| swarming | rojení | Dispersal flight of adult beetles. |  |
| transit zone | tranzitní oblast | Part of the path between release and runout zone. |  |
| transition potential | potenciál přechodu | Score of how likely a cell converts to a class; product of neighbourhood, suitability, accessibility, zoning and noise. |  |
| transition table (Markov) | tabulka přechodů (markovská) | Class → possible next classes with probabilities. |  |
| transmissivity | transmisivita | conductivity × saturated thickness | HYD-09 |
| transport capacity | transportní kapacita | maximum sediment load flow can carry | HYD-05 |
| travel time | doba cesty (dojezdová / docházková doba) | time to reach the nearest source |  |
| unit discharge | měrný průtok | discharge per unit width of a cell face (m² s⁻¹) | local inertial |
| urban fire | požár v zástavbě | Fire spreading between buildings. | URB-03 |
| urban growth | růst zástavby (urbanizace) | Expansion of built-up land into undeveloped land. | LND-01 |
| urbanisation probability | pravděpodobnost urbanizace | Share of ensemble runs in which a cell becomes urban. |  |
| vaccination zone | vakcinační pásmo | area where hosts are made non-susceptible | EPI-05 |
| vent | (erupční) průduch | Opening where lava reaches the surface. |  |
| volume-flow density | hustota objemového toku | Cold-air volume passing a unit width per second (m³ m⁻¹ s⁻¹). | urban ventilation output |
| walking speed | rychlost chůze |  |  |
| water depth | hloubka vody | height of water above the ground in a cell | WAT state |
| water surface elevation | výška (kóta) hladiny | ground elevation + water depth | WAT |
| weight matrix | váhová matice | Table of weights applied to the neighbourhood window. |  |
| windward / leeward | návětrný / závětrný | On the side facing / turned away from the wind. |  |
| zoning | územní regulace | Planning status allowing or forbidding a land use. | CZ: územní plán |
