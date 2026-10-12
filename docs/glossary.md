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
