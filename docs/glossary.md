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
