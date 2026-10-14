# Accessibility front / travel-time spreading

| Field | Value |
|---|---|
| ID | `accessibility-front` |
| Longlist ref. | `MOV-03` (scenario `ECO-04` habitat connectivity) |
| Category | movement of people / emergency planning / ecology (connectivity) |
| Group | extension |
| Weighted score | 4.25 (revision 2) |
| Primary reference | `wood2012anisotropic` |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

How long does it take to get from any place to the nearest safe area, hospital or fire
station — or, reversed, how far can one get from a source in a given time? Movement speed
depends on land cover (road, field, forest, swamp), on slope and **its direction** (uphill
is slower than downhill, very steep downhill slows again), and on impassable features
(buildings, water). The answer is a travel-time surface; animated, it looks like a front
spreading from the sources over the landscape. Scales: 1 m–10 m cells for pedestrian
evacuation (`wood2012anisotropic`), ~1 km for national / global access to cities and
healthcare (`nelson2019suite`, `weiss2020global`). Demo questions: *Can people in this
village walk to high ground before the flood wave? Which areas are more than 20 minutes
from an ambulance base? What changes if a bridge is closed?*

## 2. Suitability for CA

Good as a demonstration, though the templates are GIS least-cost-distance (LCD) methods
rather than CA. The rule is local (cost of moving to a neighbour) and the solution can be
computed either with a priority queue (Dijkstra) or with a CA-like synchronous relaxation
(each cell repeatedly takes the minimum over neighbours of "neighbour time + step cost"),
which converges to the same field. Limits: no congestion or capacity (`wood2012anisotropic`
§5.1 says so and recommends agent-based models at chokepoints — `pedestrian-evacuation`);
8-neighbour grids overestimate distances in off-grid directions (metrication); raster roads
lose sinuosity at coarse resolution (`nelson2019suite`, Technical Validation); travel mode
and behaviour (who uses roads) are fixed assumptions.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `dem` | real (m) | elevation | static input |
| `landcover` | categorical | land-cover class → speed conservation value (SCV) via LUT | static input |
| `roads` | categorical / boolean | road class (speed via LUT) | static input |
| `passable` | boolean | false for buildings, water (NoData in the primary) | static input |
| `source` | boolean | safe zone / facility cells (zero time) | static input / intervention |
| `cost.slot` | real ≥ 0, slot (8 or 16) | travel time across the edge to neighbour k | derived |
| `travelTime` | real ≥ 0 (s) or ∞ | least travel time to (or from) the nearest source | output |
| `parent` | slot index | neighbour on the least-cost path (for path tracing) | output |
| `nearest` | id | which source is nearest | output (optional) |

## 4. Neighbourhood and time step

- **Grid:** square; 1 m DEM and land cover in the primary, 10 m and 30 m in its
  sensitivity tests (`wood2012anisotropic` §3.3); 30 arc-seconds (~1 km) for the global
  layers (`nelson2019suite`, `weiss2020global`).
- **Neighbourhood:** 8 neighbours (`nelson2019suite`, Processing steps 2a, also the default
  in ArcGIS / GRASS); 16 with the "knight's move" for fewer metrication errors
  (implementation GRASS r.cost / r.walk, files `raster/r.cost/r.cost.md`,
  `raster/r.walk/r.walk.md`). Diagonal edges use their true length.
- **Time step:** none in the physical sense. With a queue the "time" is the arrival time
  itself (event policy); with synchronous relaxation one iteration propagates information
  by one cell (converge policy).
- **Update scheme:** ordered (Dijkstra, label-setting) or synchronous Bellman–Ford
  relaxation until no cell changes.
- **Boundary conditions:** closed (no paths leave the domain); this can bias times near the
  edge if real sources lie outside — pad the domain (as `nelson2019suite` does with 20°
  zone overlaps).

## 5. Transition rule

### 5.1 Primary: anisotropic path-distance model (`wood2012anisotropic` §3.2.3–3.2.4)

1. **Land-cover speed factor.** Each class gets a speed conservation value SCV_lc ∈ [0,1],
   the fraction of the maximum (road) speed, here the inverse of energy-cost terrain
   coefficients (Table 1). Buildings and water are impassable (NoData).
2. **Slope per move.** For every focal cell and each neighbour, the slope along the move is
   s = Δz / horizontal distance (from the DEM).
3. **Slope speed factor.** Tobler's hiking function gives the walking speed
   W(s) = 6 · exp(−3.5 · |s + 0.05|) km h⁻¹ (Eq. 1); SCV_slope(s) = W(s) / W_max, where
   W_max is the maximum potential walking speed (Q1).
4. **Combined factor.** SCV = SCV_lc × SCV_slope (multiplication assumes independence,
   discussed in §5.3 of the paper). The cost of crossing a unit of (surface) distance is
   1 / SCV.
5. **Accumulation.** Starting from all cells of the safe zone (cost 0), the least
   accumulated cost to every other cell is computed with ArcGIS Path Distance, which uses
   3-D surface distances between cells of different elevation and the slope along each
   move (algorithm details not stated — Q2, Q3).
6. **Direction reversal.** The search runs from safety into the hazard zone, but people
   move the other way, so the slope sign in the lookup table is reversed: what is downhill
   for the search is uphill for the evacuee (§3.2.4). In our terms: when computing time
   **to** the sources, evaluate the edge cost in the direction j → i.
7. **Travel time.** The accumulated cost (a distance) is multiplied by 1 / v_base,
   v_base = 1.1 m s⁻¹ (§3.2); speeds are applied after the accumulation, so other speeds
   just rescale the surface.

Not conserved: nothing — this is a shortest-path field, not a mass model.

### 5.2 Comparison models in the primary (§3.2.1–3.2.3)

- **Distance only:** isotropic cost 1 per metre (flat Euclidean / grid distance).
- **Road-constrained:** distance to the nearest road + network distance along roads.
- **Isotropic:** SCV_slope from the **maximum** slope in the cell (direction ignored).
Results: the distance and isotropic models underestimate travel times (Table 2, §4.2); a
10 m DEM instead of 1 m lowered mean and maximum times by about 60 % (§4.3) — resolution
matters more than the cost model.

### 5.3 Variant: friction surface + accumulated cost (`nelson2019suite`, `weiss2020global`)

- A **friction surface** holds the time to cross one metre of each pixel, built from the
  fastest available mode in the pixel (roads with speed by class and country, rail,
  navigable water, off-road speed from land cover and slope, border crossing times)
  (`weiss2020global`, Methods).
- A walking-only friction caps road travel at 5 km h⁻¹ and water at 1 km h⁻¹
  (`weiss2020global`, Methods).
- Accumulated cost with an 8-neighbour transition graph whose edge value is the mean of the
  two pixels' values (as conductance = 1 / resistance), divided by the great-circle
  distance between pixel centres to correct diagonals and latitude distortion; Dijkstra
  (gdistance `accCost`, Earth Engine `cumulativeCost`) (`nelson2019suite`, Processing
  steps 2a–c; `weiss2020global`, Methods).
- Isotropic: slope penalises walking speed but not direction.

### 5.4 Variant: Langmuir / Naismith anisotropic walking time (GRASS r.walk; reference only)

From the documentation of implementation GRASS r.walk (file `raster/r.walk/r.walk.md`,
GPL — facts only): time of a move T = a·ΔS + b·ΔH_up + c·ΔH_moderate-down +
d·ΔH_steep-down, plus λ · friction · ΔS; moderate vs. steep downhill split at slope
−0.2125 (tan 12°); defaults a, b, c, d = 0.72, 6.0, 1.9998, −1.9998; Dijkstra; optional
knight's move. A second anisotropic cost law for the same `queue` stage.

### 5.5 CA formulation (our own; for the visual demo and the GPU)

Synchronous relaxation: T_i(0) = 0 on sources, ∞ elsewhere;
T_i(n+1) = min(T_i(n), min_k [T_{j(k)}(n) + c(j(k) → i)]) until no change. The result
equals the Dijkstra field; the number of iterations equals the largest number of edges on
a least-cost path. Animation by **arrival time** (show cells with T ≤ t_display) is the
same for both solvers.

### 5.6 ECO-04 habitat connectivity scenario

Speed → **resistance** per land-cover class (motorways and fences high, crossing
structures low); sources = habitat patches; output = cost distance and least-cost
corridors (path tracing via `parent`). Compared with the population colonisation of
`population-dispersal` over the same landscape (§11). `kramerschadt2004fragmented` (lynx,
DE–CZ border) is the CZ-relevant motivation; values not available (paywall). Circuit-theory
connectivity (`mcrae2008using`) is a different method, out of scope.

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Tobler peak speed | — | km h⁻¹ | 6 | `wood2012anisotropic`, Eq. 1 | |
| Tobler decay | — | — | 3.5 | ibid., Eq. 1 | |
| Tobler slope offset | — | — | 0.05 | ibid., Eq. 1 | fastest at s = −0.05 |
| Base travel speed | v_base | m s⁻¹ | 1.1 (15th percentile walking) | ibid., §3.2 | |
| Walking speeds slow / moderate / fast | — | m s⁻¹ | 0.91 / 1.22 / 1.52 | ibid., §3.4 | |
| Running speeds slow / moderate / fast | — | m s⁻¹ | 1.79 / 2.68 / 3.83 | ibid., §3.4 | |
| SCV roads | — | — | 1 | ibid., Table 1 | |
| SCV developed (dirt road) | — | — | 0.9091 | ibid., Table 1 | NLCD 21–24 |
| SCV light brush (forest, grass, crops) | — | — | 0.8333 | ibid., Table 1 | NLCD 41–43, 71, 81, 82 |
| SCV heavy brush | — | — | 0.6667 | ibid., Table 1 | NLCD 52 |
| SCV hard sand / swampy bog | — | — | 0.5556 | ibid., Table 1 | NLCD 31, 90, 95 |
| SCV open water, buildings | — | — | 0 / impassable | ibid., Table 1, §3.2.3 | |
| DEM / land-cover resolution | Δx | m | 1 (sens. 10 m DEM, 30 m NLCD) | ibid., §3.3 | |
| Walking-only road speed | — | km h⁻¹ | 5 | `weiss2020global`, Methods | |
| Walking-only water speed | — | km h⁻¹ | 1 | ibid. | |
| Global grid | — | arc-second | 30 (~1 km) | `nelson2019suite`, Methods; `weiss2020global` | |
| Neighbourhood | K | — | 8 | `nelson2019suite`, step 2a | 4 / 8 / 16 possible |
| Validation vs. Google journey times | — | min, % | median −13.7 min (IQR −35.5 to 2.0); median −16.9 % | `nelson2019suite`, Technical Validation | raster times shorter in 72 % of tiles |
| Langmuir coefficients | a, b, c, d | s m⁻¹ | 0.72, 6.0, 1.9998, −1.9998 | implementation GRASS r.walk, file `raster/r.walk/r.walk.md` | GPL, facts only |
| Steep-downhill threshold | — | — | −0.2125 | ibid. | |
| SCV for CZ land-cover classes | — | — | not given | — | Q5 |

## 6. Deterministic vs. stochastic

Deterministic. Uncertainty enters through inputs (speed assumptions, DEM resolution) — the
primary handles it as a sensitivity analysis over six speeds and three resolutions, not as
randomness. The demo can show the spread between slow-walk and fast-run surfaces. A
stochastic variant (random travel times per edge) exists in the engine's `queue` for fire
(PROPAGATOR-type) and for the rabies front (`population-dispersal` EPI-05), not needed here.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| DEM | raster (continuous) | slope along each move, 3-D distance | required (anisotropic) |
| Land cover | raster (categorical) + LUT | SCV / off-road speed | required |
| Roads / paths | vector lines → raster classes | fast cells | required |
| Buildings, water | polygons → impassable mask | barriers | required for pedestrian scale |
| Sources / destinations | points or polygons (safe zone, hospitals, stations) | zero-cost seeds | required |
| Barriers on edges (rivers without bridges, fences, motorways) | lines → slot weights | edge closure | optional |
| Hazard arrival time (from WAT / HAZ-01) | raster | time-dependent closure | optional (chain) |
| Population | raster / points | exposure counts per travel-time class | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| DEM | DMR 5G / DMR 4G (ČÚZK, LiDAR-based), Copernicus DEM | CZ / EU | to be verified; resolution matters (primary §4.3) |
| Land cover | CORINE Land Cover, Urban Atlas (Copernicus), ZABAGED | EU / CZ | to be verified |
| Roads, paths, buildings | ZABAGED, RÚIAN (buildings), OpenStreetMap | CZ / global | to be verified (ODbL for OSM) |
| Healthcare providers | National Register of Healthcare Providers (NRPZS, ÚZIS) | CZ | to be verified |
| Fire / ambulance stations | HZS ČR, regional ambulance services; OSM | CZ | to be verified |
| Population grid | ČSÚ grid statistics; GHSL | CZ / global | to be verified |
| Reference travel-time rasters | MAP friction / accessibility rasters (`weiss2020global`, `nelson2019suite` via figshare) | global | oracle for coarse demos; to be verified |

## 9. Visualization

Front animation by arrival time (isochrones every N minutes) over hillshade; click to add
or remove a source (hospital, shelter); slider for walking speed (rescales instantly, since
speed is applied after accumulation); toggle distance / isotropic / anisotropic to show the
error of simpler models (primary §4.2); draw a closure (bridge out, flooded road) and
recompute; trace the least-cost path from a clicked cell; exposure histogram (people per
travel-time class) with a "hazard arrives at t" line.

## 10. Validation options

- Verification against GRASS r.cost / r.walk outputs on the same rasters (run as external
  oracle, test suite in `external/grass-raster-sim/raster/r.cost/test_suite`).
- Analytic checks: uniform cost → distances; 8-neighbour octagonal metrication bound;
  Tobler on a constant slope plane.
- Coarse validation: compare with MAP travel-time rasters (`nelson2019suite`,
  `weiss2020global`) and with routing-service journey times as `nelson2019suite` did with
  Google (licence of such services to be checked).
- Local: timed walks (field data not available — qualitative only).

## 11. Links to other models

- **`pedestrian-evacuation` (MOV-01):** provides the static floor field S over real
  geography (travel time converted to a field increasing towards exits).
- **`population-dispersal` (EPI-04, ECO-04):** same resistance raster; the colonisation
  front of the population model vs. the cost front (front speed from demography, see
  `population-dispersal` §5.4); cost-distance field as emigration direction weights
  (`bradshaw2023directionally`).
- **HAZ-01 wildfire:** PROPAGATOR-style variant uses the same `queue` with stochastic times.
- **WAT / HAZ-01 → MOV-03 (chain L12):** flooded or burning cells close edges; the
  "evacuate before the hazard" variant constrains arrival times by the hazard arrival field.
- Shared components: SC-GRID, SC-LUT, SC-RECLASS, SC-SLOPE, SC-RASTERIZE, SC-SLOT,
  SC-COST, SC-QUEUE, SC-DIRWEIGHT (slope direction), SC-ARRIVAL, SC-INTERV, SC-BOUNDARY,
  SC-BENCH, SC-FLOORFIELD (consumer).

## 11a. Engine mapping

- **Init / derived layers:** SC-RECLASS land cover → SCV (SC-LUT); SC-RASTERIZE roads,
  buildings, edge barriers (slot weights); `map` per-slot cost
  c(i→k) = d3D(i,k) / (v_base · SCV_lc(edge) · SCV_slope(s_ik)) stored as a slot layer
  (SC-SLOT) or evaluated inside the relax function.
- **Stage:** `queue` (SC-QUEUE / SC-COST), multi-source Dijkstra, 8 or 16 slots, with a
  **direction flag** (`from` sources vs. `to` sources — the latter evaluates c(j→i), as in
  the primary's slope reversal), outputs `travelTime`, `parent`, `nearest`; optional
  `maxCost` stop.
- **GPU / CA alternative:** `stencil` min-plus relaxation with `converge` policy (same
  output).
- **Time policy:** event (queue) or converge (stencil). Display clock maps arrival time to
  animation frames.
- **Boundaries:** closed; padding recommended.
- **RNG:** none.
- **Observers:** arrival field is the output (SC-ARRIVAL semantics); exposure histogram
  (`reduce` histogram of travel time weighted by population).
- **Interventions:** add/remove source, close edge / cell, change speed (no recompute needed
  if only v_base changes), change land cover.
- **Coupling:** a time-dependent closure (edge usable only if the arrival time is earlier
  than the hazard arrival time in the target cell) needs the relax function to read another
  layer (hazard arrival) — supported if `queue` relax reads arbitrary layers.
- **Model-specific:** Tobler / Langmuir cost laws, SCV LUT, direction reversal.
- **Corrections to `model-mapping.md`:** (1) add the direction flag (time *to* vs. *from*
  sources); (2) add `parent` / `nearest` outputs and path tracing (needed by ECO-04
  corridors); (3) 16-slot knight's-move neighbourhood for `queue`; (4) edge cost
  definition (average of the two cells vs. per-move slope) must be a parameter (Q3);
  (5) the queue must be **re-runnable during a simulation** (controller-triggered) when used
  as a floor field after closures.

## 12. Complexity estimate

- **Implementation:** low–medium — Dijkstra with a binary heap and slot costs; anisotropy
  and the direction flag are the subtle parts.
- **Computation in the browser:** low–medium — 2000 × 2000 cells (4 M) Dijkstra in a worker
  is feasible (estimate); 1 m DEM over a town quickly exceeds this, so tile / limit extent.
- **Data preparation:** medium — speed LUTs for CZ classes, edge barriers, high-resolution
  DEM.

## 13. Risks

- Scientific: SCV values and Tobler are generic (hikers); multiplication of factors is an
  assumption; no congestion — times are lower bounds for crowds.
- Data: coarse DEM strongly underestimates times (primary §4.3, −60 %); missing small
  water bodies / fences change routes (primary §4.3, Fig. 7).
- Technical: metrication error of 8-neighbour grids; large rasters.
- Communication: a travel-time map can be read as a guaranteed evacuation time; label
  speeds and assumptions, show the slow-walk case for vulnerable groups (primary §4.4).

## 14. Open questions

- Q1. W_max for normalising the slope SCV: the theoretical 6 km h⁻¹ at s = −0.05 or the
  maximum over the study surface? (primary §3.2.3 is ambiguous; on flat ground the factor
  is then 0.84, not 1).
- Q2. Exact ArcGIS Path Distance algorithm (horizontal vs. vertical factor tables, surface
  distance) — closed software; document our own choice.
- Q3. Edge cost: SCV_lc of the source cell, the target cell or their mean (gdistance uses
  the mean of conductances; r.cost averages the two cells)?
- Q4. Is slope taken from adjacent cell centres or from a smoothed DEM? (1 m LiDAR noise.)
- Q5. SCV / speed LUT for CORINE / ZABAGED classes in CZ (`TODO(literature)`).
- Q6. Do we need fast marching / ordered-upwind to reduce metrication, or is the 16-slot
  neighbourhood enough for the demo?
- Q7. Scale of the CZ demo: walking to shelters in a flood-prone town (1–5 m) or ambulance
  reach at 25–100 m with road speeds?

## 15. Literature and implementations

- **Primary reference:** `wood2012anisotropic` — explicit anisotropic pedestrian cost
  (Tobler + land-cover SCV table) with sensitivity analysis; read in full.
- **Supporting references:** `nelson2019suite` (accumulated-cost workflow, 8-neighbour
  graph, validation; read for method), `weiss2020global` (friction surfaces, walking-only
  speeds; read for method), `kramerschadt2004fragmented` (ECO-04 motivation; not local),
  `bradshaw2023directionally` (cost field directing dispersal).
- **Benchmarks / reference data:** GRASS r.cost test suite; MAP global friction and
  travel-time rasters (not downloaded).
- **Implementations:**
  - GRASS r.cost / r.walk (`external/grass-raster-sim`) — GPL-2.0+ — reference / oracle
    only.
  - AccessMod 5 — LGPL-3.0 — reference only (weak copyleft; no code copying).
  - malariaAtlas R package — MIT — data access only.
  - `nelson2019suite` R scripts (figshare) — licence not checked — reference only.
  - gdistance (R) — licence to be verified — reference only.
- **Still missing:** `TODO(literature)` CZ pedestrian / ambulance speed values per land
  cover; an open anisotropic test case with expected values.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| accessibility front | čelo dostupnosti | phenomenon |
| travel time | doba cesty (dojezdová / docházková doba) | output |
| isochrone | izochrona | output |
| least-cost distance | nákladová vzdálenost | method |
| cost surface / friction surface | nákladový povrch / povrch tření | input |
| speed conservation value | koeficient zachování rychlosti | parameter |
| hiking function (Tobler) | Toblerova funkce chůze | parameter |
| anisotropic cost | anizotropní náklad | method |
| walking speed | rychlost chůze | parameter |
| safe zone | bezpečná zóna | input |
| least-cost path | cesta s nejmenšími náklady | output |
| add source | přidat zdroj (cíl) | UI action |
| close road / bridge | uzavřít silnici / most | UI action |
