# Pedestrian evacuation

| Field | Value |
|---|---|
| ID | `pedestrian-evacuation` |
| Longlist ref. | `MOV-01` |
| Category | movement of people / civil protection |
| Group | extension |
| Weighted score | 3.80 (revision 2) |
| Primary reference | `kirchner2002simulation` |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

People leave a room, a building or a street area towards exits or safe places. Each person
moves step by step towards the exit they know about, avoids walls and occupied places and
partly follows others. At narrow exits a dense, arch-shaped jam forms and the outflow is
limited; in a panic, hesitation and pushing can make the evacuation slower ("faster is
slower"). Scales: cells of about 40 × 40 cm and steps of about 0.3 s
(`burstedde2001simulation`, §2); rooms to neighbourhoods. Demo questions: *How long does
it take to empty this school / square? Where do jams form? Does a second exit help, and
where should it be? How does the evacuation over real terrain differ from a flat
floor plan?*

## 2. Suitability for CA

Very good at building / street scale: the floor-field CA is a classic, simple local rule
(exclusion, nearest-neighbour moves, parallel update) and reproduces jamming, arching and
lane formation (`kirchner2002simulation` §2.4). Long-range knowledge (where the exit is) is
precomputed into a static field; following others becomes a local dynamic field
(§1, chemotaxis analogy). Limits: one fixed cell size means one maximum speed (1 cell per
step, `burstedde2001simulation` §2); no body shape or physical forces; behaviour
parameters (k_S, k_D, μ) need calibration (`kirchner2002simulation` §4); town-scale
evacuations need millions of 0.4 m cells — for that scale use the travel-time field of
`accessibility-front` and run the CA only at chokepoints, as `wood2012anisotropic` §5.3
recommends.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `obstacle` ξ | boolean | 0 = wall / building / forbidden, 1 = walkable | static input (dynamic with hazard masks) |
| `exit` | id or 0 | exit (door) cells | static input / intervention |
| `S` | real ≥ 0 | static floor field, increases towards the exits | derived (queue) |
| `D` | integer ≥ 0 | dynamic floor field (number of "bosons" left by moving people) | dynamic |
| `occupancy` n | {0,1} | cell occupied by one pedestrian | dynamic |
| agents | list (id, cell, optional speed / group) | pedestrians | dynamic |
| `evac.time` | real (s) | evacuation time of the person who started in the cell | output |
| `density.max` | real | maximum local density | output |

## 4. Neighbourhood and time step

- **Grid:** square, ~0.4 m cells (`burstedde2001simulation` §2). Kirchner's rooms: 63 × 63
  sites with a one-cell exit; 102 × 102 with two doors (`kirchner2002simulation` §3.1,
  §3.3).
- **Neighbourhood:** von Neumann moves plus staying (5 target cells,
  `kirchner2002simulation` Fig. 1; `kirchner2003friction` Fig. 1); Moore (9 target cells)
  in `burstedde2001simulation` §2. Q1 which one we use.
- **Time step:** ~0.3 s, from a free walking speed of about 1.3 m s⁻¹ and one 40 cm cell per
  step (`burstedde2001simulation` §2; `kirchner2002simulation` §3.1). Fixed.
- **Update scheme:** **parallel** (synchronous) with conflict resolution; random sequential
  updates would hide conflicts, which matter for clogging (`kirchner2003friction` §III.B).
- **Boundary conditions:** closed (walls), exits are sinks; agents leave the system at
  exits.

## 5. Transition rule

### 5.1 Primary: floor-field CA (`kirchner2002simulation` §2.3; friction from `kirchner2003friction` §III)

Each step, in this order:

1. **Dynamic field update.** Every boson of D decays with probability α and, if it
   survives, moves with probability δ to a random neighbouring cell (§2.2; order of decay
   and diffusion within a step is not stated — Q2).
2. **Transition probabilities.** For each pedestrian and each target cell (i,j) of its
   neighbourhood: p_ij = N · exp(k_D · D_ij) · exp(k_S · S_ij) · (1 − n_ij) · ξ_ij
   (Eq. 1), where n_ij is occupancy, ξ_ij = 0 for walls, and N normalises the sum to 1
   (the pedestrian's own cell counts as available — Q3).
3. **Choice.** Each pedestrian draws a target from p_ij.
4. **Conflicts.** If m ≥ 2 pedestrians chose the same target: with probability μ none of
   them moves (friction, `kirchner2003friction` §III.B); otherwise one moves, chosen with
   probability 1/m or in proportion to its p (both variants, §III.A). Others stay.
5. **Move and trace.** Winners move; each moving pedestrian adds one boson to D at its
   **origin** cell (D_ij ← D_ij + 1).
6. **Exit.** A pedestrian on an exit cell leaves in the next step (`kirchner2003friction`
   §IV.D: "with probability 1").

Static field for simple rooms (`kirchner2002simulation` Appendix A, Eq. A.1): S at a cell is
the largest distance of any cell to the exit minus the cell's own (Euclidean) distance to
the exit, i.e. zero at the farthest cell and largest at the door; with several doors the
nearest-door value is used (the min / max order in Eq. A.1 is hard to read — Q4). Other
constructions (e.g. Manhattan) give the same qualitative results as long as S grows towards
the exit (Appendix A).

Conserved: number of pedestrians (until they leave); D is not conserved (decay).

### 5.2 Model behaviour used for verification

- Three regimes (`kirchner2002simulation` §3.1; `kirchner2003friction` §IV): **ordered**
  (strong k_S, about k_S > 3, weak k_D — near-deterministic shortest paths), **disordered**
  (strong k_D, weak k_S — panic, herding, maximal times), **cooperative / optimal**
  (intermediate couplings — minimal times).
- Evacuation time is non-monotonic in k_D for fixed k_S (minimum at small k_D > 0,
  strongest around k_S ≈ 0.4) (`kirchner2002simulation` §3.1, Fig. 5b).
- Friction μ barely matters at low density but strongly increases times in the ordered
  regime at high density; T diverges as μ → 1 (`kirchner2003friction` §IV.A).
- Analytic outflow for a one-cell door in the ordered regime: evacuated persons
  N(t) ≈ (1 − μ)/(2 − μ) · t for large t (`kirchner2003friction` Eq. 9) — a ready-made
  verification test.
- Low density: evacuation time ~ largest initial distance to the exit; above ρ ≈ 0.005 a
  queue forms and time grows about linearly with density (`kirchner2002simulation` §3.1).

### 5.3 Variant: matrix of preference (`burstedde2001simulation` §2)

Moore neighbourhood; each pedestrian has a 3 × 3 matrix of move probabilities from its
preferred direction; the floor-field terms multiply it. Not used in evacuation from rest
(`kirchner2002simulation` §2.3 drops it).

### 5.4 Extension: static field from the accessibility front (real geography)

For outdoor or terrain evacuation, S comes from the `accessibility-front` queue:
travel time T to the nearest exit / safe zone with Tobler slope and land-cover factors
(`wood2012anisotropic`), converted to S = (T_max − T) · v_ref / Δx (cell units, so that k_S
keeps its meaning; our assumption — Q5). Obstacles = buildings, water. Effects of slope on
speed cannot come only from S; they need per-cell move probabilities (Q6).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Cell size | Δx | m | ~0.4 | `burstedde2001simulation`, §2 | 40 × 40 cm² |
| Time step | Δt | s | ~0.3 | `burstedde2001simulation`, §2; `kirchner2002simulation` §3.1 | from 1.3 m s⁻¹ |
| Free walking speed | v | m s⁻¹ | ~1.3 | `burstedde2001simulation`, §2 | = Δx / Δt |
| Static coupling | k_S | — | studied 0–10; ordered regime about > 3 | `kirchner2002simulation` Fig. 5; `kirchner2003friction` §IV.B | calibration open |
| Dynamic coupling | k_D | — | studied 0–10 (−10 to 10 for variants) | `kirchner2002simulation` Fig. 5, Fig. 10 | |
| Decay | α | — | [0,1]; 0, 0.1, 0.3 studied | `kirchner2002simulation` §2.2, Figs. 5–7 | |
| Diffusion | δ | — | [0,1]; 0.1–0.4 studied | ibid., Figs. 5–8 | |
| Friction | μ | — | [0,1]; 0–0.9 studied | `kirchner2003friction` §III.B, Figs. 5–9 | |
| Initial density | ρ | — | 0.003–0.9; typical 0.3 | `kirchner2002simulation` §3.1, Fig. 9 | |
| Room / exit | — | cells | 63 × 63, 1-cell exit; 102 × 102, two 1-cell doors | ibid., §3.1, §3.3 | test geometries |
| Samples | — | runs | 500 | ibid., §3.1 | ensemble size |
| NIST corridor test | — | — | 2 m × 40 m, 1 m s⁻¹ → 40 s | `ronchi2013process`, Verif.2.1 | needs speed control (Q6) |
| NIST door-flow test | — | — | 8 m × 5 m room, 1 m exit, 100 occupants | `ronchi2013process`, Verif.5.2 | |
| Max. specific flow (IMO) | — | p m⁻¹ s⁻¹ | 1.33 | `ronchi2013process`, Verif.5.2 (citing IMO MSC/Circ.1238) | external threshold |
| Tobler / walking speeds for S | — | — | see `accessibility-front` §5a | `wood2012anisotropic` | extension only |

## 6. Deterministic vs. stochastic

Stochastic: target choice, conflict winner, friction refusals, D decay / diffusion per
boson, random initial positions. Randomness represents individual variation and imperfect
knowledge; k_S acts like an inverse temperature (`kirchner2002simulation` §3.1). Results
must be ensembles: relative variance of evacuation time is large when k_S is small (§3.1,
Fig. 6); `ronchi2013process` gives convergence criteria for the number of runs (Section 4 /
Appendix). Seeds per run (keyed by agent id) for replay.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| Building footprints / walls | vector polygons → obstacle raster | non-walkable cells | required |
| Exits / safe zones | points / polygons | sinks and S sources | required |
| Walkable area (streets, squares, open land) | vector / land cover | domain | required |
| DEM, land cover | raster | anisotropic S (extension) | optional |
| Initial crowd | count per area or points | agents | required (scenario) |
| Hazard arrival (flood, fire) | raster from WAT / HAZ-01 | dynamic obstacles / closures | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| Buildings | RÚIAN, ZABAGED (ČÚZK); OpenStreetMap | CZ / global | to be verified |
| Streets, squares, footpaths | ZABAGED; OSM | CZ / global | to be verified |
| DEM | DMR 5G (ČÚZK) | CZ | to be verified |
| Floor plans (indoor) | synthetic / user-drawn | — | public plans rarely open |
| Population / crowd | ČSÚ grid, event capacity (scenario) | CZ | to be verified; scenario values are assumptions |
| Flood / fire hazard | WAT / HAZ-01 model outputs; flood zones (DIBAVOD / Povodí) | CZ | to be verified |

## 9. Visualization

Agents as dots over the floor plan or orthophoto; heat map of D (where people follow each
other); density and maximum-density map (jams); cumulative evacuated persons vs. time and
outflow per exit; per-start-cell evacuation-time map; sliders for k_S ("knowledge of the
exit"), k_D ("herding"), μ ("pushing / hesitation"); add / block an exit, move an obstacle,
draw a crowd; scenario comparison (one vs. two doors, `kirchner2002simulation` §3.3); for
the terrain extension the S field from the accessibility front as an overlay.

## 10. Validation options

- Verification: `kirchner2003friction` Eq. 9 outflow; regime behaviour of §5.2;
  NIST / IMO verification tests (`ronchi2013process`, Table 1: Verif.2.1 corridor speed,
  Verif.2.3 corner, Verif.2.8 counter-flow, Verif.5.2 maximum door flow) — the tests are
  textual (no data package; `docs/research/implementations.md`).
- Oracle: chraibi/cellular_automata (GPL-2.0) may be run as an external oracle for
  identical room geometries; JuPedSim (LGPL) concepts of test cases.
- Validation with real drills is out of scope; qualitative only.

## 11. Links to other models

- **`accessibility-front` (MOV-03):** static floor field over real geography; at town scale
  the front model replaces the CA; the CA refines chokepoints (`wood2012anisotropic` §5.3).
- **WAT flood, HAZ-01 wildfire (chain L12):** hazard arrival times as dynamic obstacles and
  deadlines (people "lost" if the hazard reaches their cell first).
- **`population-dispersal`:** shares the idea of a cost-field gradient steering movement
  (directed emigration ≈ static floor field).
- Shared components: SC-GRID, SC-RASTERIZE, SC-COST, SC-QUEUE, SC-FLOORFIELD, SC-AGENTS,
  SC-INTERV, SC-BOUNDARY, SC-ARRIVAL (per-agent evacuation time), SC-ENVELOPE (max
  density), SC-ENSEMBLE, SC-BENCH, SC-RNG, SC-SLOPE (extension).

## 11a. Engine mapping

- **Init:** SC-RASTERIZE obstacles and exits; `queue` (SC-COST) from exit cells → distance
  or anisotropic travel time → `map` to S (SC-FLOORFIELD); place agents (intervention
  `crowd`).
- **Stages per step:**
  1. D update: faithful version = `map` binomial decay (per-cell draw Binomial(D, α)) +
     **stochastic integer `flux`** (Binomial(D, δ) bosons split multinomially over
     neighbours); cheap version = deterministic `stencil` diffusion + decay (approximation,
     changes behaviour at low D — Q2).
  2. `agents` propose: per agent, probabilities over its slots from S, D, occupancy, ξ
     (RNG key agent id, step).
  3. `agents` resolve: per target cell, conflict set; friction μ (refuse all) else winner
     by 1/m or by p.
  4. `agents` move + update occupancy; deposit D at origins (write to D as part of the move,
     or a `map` from a "moved-from" scratch layer); remove agents on exits, record their
     time.
  5. `reduce`: agents left, outflow per exit, number of conflicts (stop when zero agents).
- **Time policy:** fixed Δt ≈ 0.3 s.
- **Boundaries:** closed; exits as sinks.
- **RNG:** keyed by (agent id, step, draw) and (cell, step) for the D field.
- **Observers:** evacuated-vs-time curve, per-exit flow, per-start-cell evacuation time
  (SC-ARRIVAL variant keyed by agent origin), max density (SC-ENVELOPE), conflicts count;
  ensembles → distribution of total evacuation time (SC-ENSEMBLE).
- **Interventions:** add / block exit (→ **re-run the `queue` for S** mid-run), add
  obstacle, add crowd, change k_S, k_D, μ; hazard mask update from a chained model.
- **Model-specific:** Eq. 1 probability form, friction rule, boson D field.
- **Corrections to `model-mapping.md`:** (1) D dynamics in the original are stochastic per
  boson, so "stencil diffusion + decay" is only an approximation — a stochastic integer
  `flux` is needed for the faithful version; (2) the `agents` primitive needs a per-agent
  (or per-cell) move probability to represent speeds below Δx/Δt (NIST Verif.2.1 with
  1 m s⁻¹, slope effects, slower groups) — not in the templates (Q6); (3) the `queue` for S
  must be re-runnable when exits or obstacles change; (4) `agents` must expose a conflicts
  count to `reduce`.

## 12. Complexity estimate

- **Implementation:** medium — parallel propose–resolve with friction and the boson field.
- **Computation in the browser:** low for rooms (63 × 63, ~1000 agents, thousands of steps,
  hundreds of runs); high for districts at 0.4 m (e.g. 500 m × 500 m = 1.56 M cells,
  10⁴ agents) — feasible for single runs in a worker (estimate), ensembles limited.
- **Data preparation:** low for synthetic plans; medium for real buildings (footprint
  cleaning, door locations are usually missing in open data).

## 13. Risks

- Scientific: parameters are not calibrated in the primary (k_S, k_D are behavioural
  dials); a single speed; no stairs model; results for real buildings would be misleading.
- Communication: evacuation times can be mistaken for safety certification — label as an
  illustration; avoid real named schools / venues as "unsafe".
- Data: door locations and indoor plans are rarely open.
- Technical: parallel conflict resolution on GPU is non-trivial; keep CPU reference.

## 14. Open questions

- Q1. von Neumann (Kirchner) or Moore (Burstedde) neighbourhood? Moore on 0.4 m cells
  makes diagonal moves √2 longer per step.
- Q2. Order of decay and diffusion within one step; per-boson stochastic vs. deterministic
  approximation in the demo.
- Q3. Is staying in place a choice with weight exp(k_D D + k_S S) of the own cell (Fig. 1
  shows a probability for the centre)? Its occupancy term must be treated as free.
- Q4. Exact reading of Eq. A.1 with several doors (min / max order) — check the typeset
  paper.
- Q5. Scaling of S from travel time (seconds) to cell units so that k_S keeps its meaning.
- Q6. How to model speeds below one cell per step (slope, mobility-impaired people):
  per-agent move probability v/v_max, or finer cells? No source in our references
  (`TODO(literature)`).
- Q7. Calibration of k_S, k_D, μ to empirical flows (e.g. 1.33 p m⁻¹ s⁻¹ door-flow
  threshold, `ronchi2013process`).
- Q8. Demo scale: indoor (school, stadium) vs. outdoor (flood evacuation of a street block)
  — needs the author's decision.

## 15. Literature and implementations

- **Primary reference:** `kirchner2002simulation` — complete floor-field evacuation rule
  with parameter study (read in full, arXiv preprint).
- **Supporting references:** `kirchner2003friction` (friction μ, analytic outflow; read),
  `burstedde2001simulation` (base model, cell size and time step; read for these facts),
  `ronchi2013process` (NIST verification / validation test suite; test definitions read),
  `wood2012anisotropic` (terrain-based travel times for S).
- **Benchmarks / reference data:** `ronchi2013process` test definitions (textual).
- **Implementations:**
  - chraibi/cellular_automata (`external/cellular_automata_pedestrians`) — GPL-2.0 —
    reference / oracle only.
  - JuPedSim — LGPL-3.0 — not CA; test concepts only.
  - Student FFCA repositories (mixed licences, e.g. aleksejalex/floor_field_model MIT) —
    not reviewed; low value.
- **Still missing:** `TODO(literature)` calibrated k_S / k_D / μ values; terrain-coupled
  floor-field evacuation (no open implementation found, `docs/research/implementations.md`
  Gaps); speed heterogeneity in floor-field CA.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| pedestrian evacuation | evakuace chodců | phenomenon |
| pedestrian | chodec | state |
| static floor field | statické podlahové pole | state variable |
| dynamic floor field | dynamické podlahové pole | state variable |
| coupling to the static field | citlivost na statické pole | parameter |
| coupling to the dynamic field (herding) | citlivost na dynamické pole (stádní chování) | parameter |
| friction (conflict) | tření (konflikt) | parameter |
| decay / diffusion of the trace | rozpad / difuze stopy | parameter |
| exit | východ | input / UI action |
| obstacle | překážka | input / UI action |
| clogging | ucpání | output |
| evacuation time | doba evakuace | output |
| outflow | odtok osob (průtok východem) | output |
| crowd density | hustota davu | output |
