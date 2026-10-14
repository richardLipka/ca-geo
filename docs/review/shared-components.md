# Shared components

Building blocks that recur across the 14 selected models (ADR 0001) — the basis for the
general CA engine (`docs/architecture/`). Compiled from the model cards
(`docs/models/candidates/*.md`, section 11a), which reference these IDs.

**Status:** revision 1, 2026-10-14 (after writing all 14 model cards). The seed list of
2026-10-13 was extended by 22 components found while writing the cards (marked †); SC-ROADWALK was replaced by SC-EVENTS.

## How to read the matrix

● = main mechanism of the model's primary rule, ○ = variant, scenario or optional output.
*n* = number of models using the component, *core* = how many of the 6 core models use it.
Models are grouped by family: water (WAT, HYD-05, HYD-09), gravity flows (ATM-02, HAZ-05,
HAZ-02), stochastic spread (HAZ-01, ECO-01, ECO-09), populations / fronts / agents (EPI-04,
MOV-03, MOV-01), growth and dispersion (LND-01, ATM-01).

## Usage matrix

| ID | Component | WAT | HYD-05 | HYD-09 | ATM-02 | HAZ-05 | HAZ-02 | HAZ-01 | ECO-01 | ECO-09 | EPI-04 | MOV-03 | MOV-01 | LND-01 | ATM-01 | n | core |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Space and data** | | | | | | | | | | | | | | | | | |
| `SC-GRID` | Georeferenced raster grid with domain mask (time-varying mask optional) | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | 14 | 6 |
| `SC-LUT` | Categorical layer + lookup table, recomputable from mutable parameters, swappable by interventions | ● | ● | ● | ● |  | ○ | ● | ● | ● | ● | ● |  | ● |  | 11 | 6 |
| `SC-PAIRLUT` † | Two-key tables: source class × target class; distance ring × class × class |  |  |  |  |  |  | ○ |  |  |  |  |  | ○ |  | 2 | 2 |
| `SC-FACE` | Edge-centred (face) layers, persistent and readable by submodels | ● |  | ● | ● |  |  |  |  |  |  |  |  |  |  | 3 | 2 |
| `SC-SLOT` | Per-neighbour slot layers incl. reverseSlot(k) access and extended (16) slots | ○ | ● |  | ○ | ● | ● | ● |  |  | ● | ● | ○ |  |  | 9 | 4 |
| `SC-SLOTMASK` † | Per-cell bitmask of slots (parents, donors) for direction memory |  |  |  |  | ● | ● |  |  |  |  |  |  |  |  | 2 | 0 |
| **Derived layers** | | | | | | | | | | | | | | | | | |
| `SC-SLOPE` | Slope, aspect, hillshade — static, or of a dynamic surface per step | ● | ● |  | ● |  | ● |  |  |  | ○ |  |  | ● |  | 6 | 4 |
| `SC-DIRSLOPE` † | Per-slot elevation difference / slope towards each neighbour |  |  |  |  |  | ○ | ● |  |  | ○ | ● | ○ |  |  | 5 | 2 |
| `SC-D8` | Flow direction (D8 / MFD), flow accumulation | ○ | ● |  | ○ |  |  |  |  |  |  |  |  |  |  | 3 | 2 |
| `SC-FILL` | Depression filling (priority-flood) | ○ |  |  |  |  |  |  |  |  |  |  |  |  |  | 1 | 1 |
| `SC-EDT` † | Euclidean distance transform, nearest-feature index |  |  |  |  |  |  |  |  |  |  |  |  | ● |  | 1 | 1 |
| `SC-COST` | Cost-distance, anisotropic slope cost, direction to / from sources |  |  |  |  |  |  |  | ○ |  | ○ | ● | ● |  |  | 4 | 2 |
| `SC-RASTERIZE` | Rasterisation of vectors incl. line barriers into slot layers and burn-in of dikes | ● | ● | ● |  |  |  | ● |  | ● | ● | ● | ● | ● | ● | 10 | 4 |
| `SC-RECLASS` | Reclassification of land cover to model classes | ● | ● |  | ● |  |  | ● | ● | ● | ● | ● |  | ● |  | 9 | 6 |
| `SC-EFFSURF` † | Effective surface = terrain + mobile layer(s) (+ virtual head) | ● |  |  | ● | ● | ○ |  |  |  |  |  |  |  |  | 4 | 2 |
| **Dynamics** | | | | | | | | | | | | | | | | | |
| `SC-OUTFLOW` | Conservative flux: donor-limited outflow or antisymmetric face flux; per-donor limiter; retention threshold; integer / multinomial mode; ordered slot loop with RNG | ● | ● | ● | ● | ○ | ○ |  |  |  | ● |  | ○ |  | ○ | 9 | 3 |
| `SC-FLOWWEIGHT` † | Flow-partition weights (∝ drop, drop / length, Holmgren exponent, MoD equalisation) with cutoff redistribution | ○ | ○ |  | ● | ● | ● |  |  |  |  |  |  |  |  | 5 | 2 |
| `SC-INERTIAL` | Face flux with local inertia and friction | ○ |  |  | ○ |  |  |  |  |  |  |  |  |  |  | 2 | 2 |
| `SC-INFIL` † | Infiltration library (constant capacity, Philip, Green–Ampt) with cumulative state | ● | ● | ○ |  |  |  |  |  |  |  |  |  |  |  | 3 | 1 |
| `SC-ADT` | Adaptive Δt: reduction, recompute period, snapping, forcing look-ahead, growth when idle, step retry | ● | ● | ○ | ● |  |  |  |  |  |  |  |  |  | ○ | 5 | 2 |
| `SC-REPEAT` † | Nested iteration of a stage group (count or until a condition) inside one step | ○ |  |  |  |  |  |  |  |  |  |  |  | ○ | ● | 3 | 2 |
| `SC-SRC` | Sources, sinks, forcing (scalar / raster series with interpolation, per-period reset, budgeted pulses) | ● | ● | ● | ● | ● |  |  |  |  | ○ |  |  |  | ● | 7 | 3 |
| `SC-STOCH-SPREAD` | Stochastic neighbour transmission 1 − Π(1 − p), incl. scatter-as-gather pattern |  |  |  |  |  |  | ● | ○ |  | ○ |  |  | ○ |  | 4 | 4 |
| `SC-MARKOV` † | Stochastic categorical transition table (joint class → destination probabilities) |  |  |  |  |  |  |  | ● |  |  |  |  | ○ |  | 2 | 2 |
| `SC-TIMER` † | Per-cell stage timers with deterministic or stochastic exit |  |  |  |  |  |  | ● |  |  | ○ |  |  |  |  | 2 | 2 |
| `SC-DIRWEIGHT` | Per-slot direction values (cos θ, magnitude, distance) passed to the kernel; model chooses multiplier or exponent |  |  |  |  |  |  | ● |  | ○ |  | ● |  |  | ● | 4 | 1 |
| `SC-KERNEL` | Kernels: normalised or not, class-pair weights, centre weight, FFT without wrap-around |  |  |  |  |  |  |  | ○ | ● |  |  |  | ● | ● | 4 | 2 |
| `SC-LDD` | Long-distance jumps: emission, distance, direction, acceptance; conservative mode; discard / redraw |  |  |  |  |  |  | ○ | ○ | ● | ● |  |  |  |  | 4 | 3 |
| `SC-GROWTH` | Local growth (logistic, Ricker, Gompertz) with demographic noise |  |  |  |  |  |  |  |  | ● | ● |  |  |  |  | 2 | 1 |
| `SC-QUEUE` | Priority-queue front: multi-source, direction flag, parent / nearest outputs, stochastic edge times, re-runnable | ○ |  |  |  |  |  | ○ | ○ |  | ○ | ● | ● |  |  | 6 | 4 |
| `SC-FRONT` | Active-list propagation: shared-grid relaxation (lava) or per-source traversal (runout) |  |  |  |  | ● | ● |  |  |  |  |  |  |  |  | 2 | 0 |
| `SC-PERSIST` † | Persistence weights by (incoming slot, outgoing slot) |  |  |  |  | ○ | ● |  |  |  |  |  |  |  |  | 2 | 0 |
| `SC-ENERGY` | Energy line / travel angle as path state or cell layer |  |  |  |  |  | ● |  |  |  |  |  |  |  |  | 1 | 0 |
| `SC-AGENTS` | Lattice agents with propose–resolve, friction, move probability for slow speeds |  |  |  |  |  |  |  |  |  |  |  | ● |  |  | 1 | 0 |
| `SC-FLOORFIELD` | Static field from queue + dynamic stochastic field; also emigration direction weights |  |  |  |  |  |  |  |  |  | ○ |  | ● |  |  | 2 | 1 |
| `SC-ALLOC` | Allocation: top-N, joint greedy multi-class, zone quotas, weighted sampling, patch growth, allowed-transition matrix |  |  |  |  |  |  |  |  |  |  |  |  | ● |  | 1 | 1 |
| `SC-EVENTS` † | Sequential sparse event scripts (random start, spiral search, walk along features, local action with retries) |  |  |  |  |  |  |  |  | ○ |  |  |  | ● |  | 2 | 1 |
| `SC-SELFMOD` | Controllers reading reductions, changing parameters / LUTs, scheduling pulses and breaches | ○ |  |  |  | ● |  |  |  |  |  |  |  | ● |  | 3 | 2 |
| `SC-CLUSTEREVENT` † | Spatially clustered random event masks (cluster point process) |  |  |  |  |  |  |  |  |  | ○ |  |  |  |  | 1 | 1 |
| `SC-TIMEGATE` † | Cells / edges usable only before another model's arrival time |  |  |  |  |  |  |  |  |  |  | ○ | ○ |  |  | 2 | 0 |
| `SC-INTERV` | Interventions (ignite, barrier, dam, breach, zone, exit, paint, LUT swap); DEM edits invalidate derived layers | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | 14 | 6 |
| `SC-BOUNDARY` | Boundary policies incl. interior fixed cells, domain-exit flag, interior-only sources | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | 14 | 6 |
| `SC-RNG` | Counter-based RNG; distributions incl. beta, lognormal, multinomial, discrete 2D Gaussian, categorical |  | ○ |  |  | ● | ○ | ● | ● | ● | ● |  | ● | ● |  | 9 | 4 |
| **Observation and analysis** | | | | | | | | | | | | | | | | | |
| `SC-ARRIVAL` | First-arrival time with threshold predicate; agent-origin variant | ● |  |  | ○ |  | ○ | ● | ● | ● | ● | ● | ○ | ○ |  | 10 | 6 |
| `SC-ENVELOPE` | Maximum envelope | ● | ○ |  | ● | ● | ● |  |  |  |  |  | ○ |  | ○ | 7 | 2 |
| `SC-MASS` | Mass balance (optional per model) | ● | ● | ● | ● | ● |  |  |  |  | ● |  |  |  |  | 6 | 3 |
| `SC-ZONAL` † | Reductions grouped by a zone layer |  |  |  |  |  |  |  | ● | ● |  |  |  |  |  | 2 | 1 |
| `SC-POINTOBS` † | Values at station points over time | ○ |  | ○ |  |  |  |  |  |  |  |  |  |  | ● | 3 | 1 |
| `SC-FRONTSPEED` † | Arrival time vs. distance, front speed |  |  |  |  |  |  |  |  |  | ● | ○ |  |  |  | 2 | 1 |
| `SC-PATHTRACE` † | Back-tracking / least-cost path from parent links |  |  |  |  |  | ○ |  |  |  |  | ○ |  |  |  | 2 | 0 |
| `SC-SOURCEMERGE` † | Merge of independent per-source runs (max / sum / count) |  |  |  |  | ○ | ● |  |  |  |  |  |  |  |  | 2 | 0 |
| `SC-SRCSAMPLE` † | Sampling start cells from a probability raster |  |  |  |  | ● | ○ | ○ |  |  |  |  |  |  |  | 3 | 1 |
| `SC-ENSEMBLE` | Ensembles: probability, mean, per-cell quantiles, paired scenarios, per-run parameter reset | ○ |  |  |  | ● | ○ | ● | ● | ● | ● |  | ● | ● |  | 9 | 5 |
| `SC-METRICS` | Validation metrics (disagreement, FoM, fuzzy kappa, Jaccard / Sørensen, F1, AUC, Boyce, NRMSE, RMSE) | ● | ● |  |  | ● | ● | ● | ● | ● | ● |  |  | ● | ● | 10 | 5 |
| `SC-CCL` † | Connected components and landscape metrics |  |  |  |  |  |  |  |  |  |  |  |  | ● |  | 1 | 1 |
| `SC-NEUTRAL` † | Neutral benchmark models |  |  |  |  |  |  | ○ |  |  |  |  |  | ● |  | 2 | 2 |
| `SC-BENCH` | Benchmark runner incl. analytical oracles and statistical tolerances | ● | ○ | ● |  | ● | ● |  |  |  |  | ○ | ● | ● |  | 8 | 2 |
| `SC-CALIB` | Calibration (sweep, Latin hypercube, GA, coarse-to-fine) |  | ○ |  |  |  |  | ○ |  |  | ○ |  | ○ | ● | ● | 6 | 3 |

Components added in revision 1 (†) and where they came from:

| ID | Origin (proposal in the card work) | Merged with / note |
|---|---|---|
| SC-PAIRLUT † | NEW-PAIRLUT (fire), class-pair kernels (land use) | extension of SC-LUT |
| SC-SLOTMASK † | NEW-SLOTMASK (lava, runout) | parent is a set of slots, not one slot |
| SC-DIRSLOPE † | NEW-DIRSLOPE (fire), per-move slope (fronts) | complements SC-SLOPE |
| SC-EDT † | NEW-EDT (land use) | — |
| SC-EFFSURF † | NEW-EFFSURF (gravity flows) | — |
| SC-FLOWWEIGHT † | NEW-MFDWEIGHT + NEW-CUTOFF (gravity flows) | — |
| SC-INFIL † | NEW-INFIL (water) | — |
| SC-REPEAT † | NEW-INNERLOOP (land use, dispersion) | — |
| SC-MARKOV † | NEW-MARKOV (bark beetle) | — |
| SC-TIMER † | NEW-TIMER (fire) | — |
| SC-PERSIST † | NEW-PERSIST (runout) | — |
| SC-EVENTS † | NEW-EVENTS (land use) | replaces SC-ROADWALK and the `walk` primitive |
| SC-CLUSTEREVENT † | NEW-CLUSTEREVENT (population) | — |
| SC-TIMEGATE † | NEW-TIMEGATE (fronts) | chains L12 |
| SC-ZONAL † | NEW-ZONAL (spread) | — |
| SC-POINTOBS † | NEW-POINTOBS (dispersion) | — |
| SC-FRONTSPEED † | NEW-FRONTSPEED (population) | — |
| SC-PATHTRACE † | NEW-BACKTRACK + NEW-LCPATH | — |
| SC-SOURCEMERGE † | NEW-SOURCE-MERGE (runout) | — |
| SC-SRCSAMPLE † | NEW-SRCSAMPLE (lava, fire, runout) | — |
| SC-CCL †, SC-NEUTRAL † | NEW-CCL, NEW-NEUTRAL (land use) | analysis |
| (folded) | NEW-DTSNAP, NEW-RETRY → SC-ADT; NEW-RETAIN, NEW-STOCHDIFF → SC-OUTFLOW; NEW-LEVELVOL, NEW-BREACH → SC-SELFMOD + `reduce` (scenario-specific); NEW-THEIS → SC-BENCH; NEW-PATCHGROW → SC-ALLOC; NEW-FORCING-RESET → SC-SRC | — |

## Tiers for the engine

Derived from the matrix and the implementation order of ADR 0001
(WAT → HAZ-01 → ATM-02 → EPI-04 → ECO-01 → LND-01).

| Tier | Meaning | Components |
|---|---|---|
| **T0 — engine foundation** | used by (almost) all models; must exist before the first model | SC-GRID, SC-LUT, SC-SLOT, SC-FACE, SC-BOUNDARY, SC-INTERV, SC-SRC, SC-RNG, SC-ARRIVAL, SC-ENVELOPE, SC-MASS, SC-RECLASS, SC-RASTERIZE, SC-SLOPE |
| **T1 — first two models** (WAT, HAZ-01) | flux family and stochastic-spread family | SC-OUTFLOW, SC-EFFSURF, SC-ADT, SC-INFIL, SC-FILL, SC-D8, SC-DIRSLOPE, SC-DIRWEIGHT, SC-STOCH-SPREAD, SC-TIMER, SC-ENSEMBLE, SC-METRICS, SC-BENCH |
| **T2 — remaining core** (ATM-02, EPI-04, ECO-01, LND-01) | reuse T1, add population, Markov and land-use parts | SC-FLOWWEIGHT, SC-GROWTH, SC-LDD, SC-KERNEL, SC-QUEUE, SC-COST, SC-MARKOV, SC-ZONAL, SC-ALLOC, SC-EVENTS, SC-SELFMOD, SC-REPEAT, SC-PAIRLUT, SC-EDT, SC-CCL, SC-NEUTRAL, SC-CALIB, SC-FRONTSPEED, SC-CLUSTEREVENT |
| **T3 — extension only** | needed only by extension models | SC-FRONT, SC-SLOTMASK, SC-PERSIST, SC-ENERGY, SC-SOURCEMERGE, SC-SRCSAMPLE, SC-PATHTRACE, SC-AGENTS, SC-FLOORFIELD, SC-TIMEGATE, SC-INERTIAL, SC-POINTOBS |

## Recurring patterns (what the cards revealed)

1. **One gravity-flow family.** Water (WCA2D, MoD, FlowFill), cold air (Nowatschin, SAGA),
   lava (Connor / MOLASSES, SCIARA), debris (SCIDDICA) and runout (Flow-Py) all read an
   **effective surface** (terrain + mobile layer), keep a **retention** share (residual
   thickness, adherence, tolerance), test **eligibility** (lower surface, not parent,
   energy > 0) and split the mobile part by a **flow weight** function. Synchronous models
   use it in `flux`, sequential ones in `front` — the weight library (SC-FLOWWEIGHT) and
   SC-EFFSURF are shared by both.
2. **Two flux forms.** Donor-limited outflow (WCA2D, MoD, kinematic, emigration) vs.
   antisymmetric face flux (Darcy groundwater, local inertial water, Nowatschin faces).
   Both conserve mass, by limiter or by antisymmetry + Δt bound.
3. **One stochastic-transmission rule.** Fire, rabies, SLEUTH edge growth and the beetle
   variant combine per-neighbour probabilities as 1 − Π(1 − p). Direction factors (wind,
   slope) enter either as multipliers or as exponents — the engine must hand per-slot
   direction values to the kernel and let the model combine them.
4. **Scatter as gather.** Processes where a source picks a target (SLEUTH edge growth,
   short-range spotting, agent proposals, emigration) can be computed exactly by the
   target if draws are keyed by (source, tag). This keeps parallel stages gather-only.
5. **Barriers in three forms** — impassable cells, slot permeability between cells (river
   between two cells), extended reach for corridors. One permeability slot layer + a cell
   LUT covers all of them (population, rabies, connectivity, evacuation, pest corridors).
6. **Fronts everywhere.** Arrival time is the most common observer (10 models). A
   deterministic population model without jumps behaves like a `queue` front with per-cell
   lag — a consistency test between EPI-04 and MOV-03 is proposed for SC-BENCH. The same
   cost field serves accessibility, the pedestrian static floor field and directed
   emigration.
7. **Mass conservation is not universal.** Water, cold air, lava, groundwater and population
   exchange conserve; the empirical dispersion smoothing (ATM-01) and land-use allocation do
   not — SC-MASS must be optional per model.
8. **Statistical, not cell-by-cell, oracles.** Stochastic reference implementations (SLEUTH,
   PyTorchFire, Xylella) use their own sequential RNGs; our counter-based RNG cannot
   reproduce their runs, so benchmarks compare distributions of statistics.
9. **Parameters hide in tolerances.** Numerical cut-offs (Xylella 1e-8, WCA2D tolerances,
   Flow-Py flux cutoff) change model behaviour; they are declared parameters with
   provenance, not engine constants.

## Implications for the architecture

Findings from the cards that change or refine `docs/architecture/engine-architecture.md`.
Applied in architecture revision 1.1 (2026-10-14), proposed as ADR 0007.

| # | Finding | Source cards | Change |
|---|---|---|---|
| I1 | `flux` needs two kernel shapes (donor-limited cell kernel, antisymmetric face kernel), an optional per-donor limiter pass, a declared flux unit, a retention threshold, an integer / multinomial mode and an ordered slot loop with RNG; the flux layer may be persistent state readable by submodels | water, gravity, front | §6 `flux` |
| I2 | `front` has two modes: shared-grid relaxation (lava pulses) and independent per-source traversal with merge (runout) | gravity | §6 `front` |
| I3 | `walk` is too narrow → replaced by `events` (sequential sparse event scripts: start, spiral search, walk, local action with retries) | growth | §6, ADR 0007 |
| I4 | `allocate` modes: top-N, joint greedy multi-class, zone quotas, weighted sampling (random keys + top-N), patch growth, allowed-transition matrix | growth | §6 `allocate` |
| I5 | `jump`: conservative mode, per-target acceptance probability, discard or redraw on masked targets, deterministic multi-cell rays | spread, front | §6 `jump` |
| I6 | `queue`: direction flag, `parent` / `nearest` outputs, 16-slot neighbourhood, stochastic exponential edge times, re-runnable during a run | front | §6 `queue` |
| I7 | `agents`: move probability for speeds below one cell per step, conflict counts | front | §6 `agents` |
| I8 | Directional weights: engine computes per-slot direction values (cos θ, magnitude, distance, ΔE) and passes them to the kernel; kernels get `reverseSlot(k)`; kernel weight tables may be class-pair, normalised, with centre weight | spread, growth | §5.3 |
| I9 | Time: adaptive Δt with recompute period, snapping, forcing look-ahead, growth when idle and retry; nested `repeat` of a stage group; runout has no model time (display = traversal generation) | water, gravity, growth | §7.1 |
| I10 | Boundaries: fixed value on interior cell masks; domain-exit flag / abort; interior-only sources | water, gravity, growth | §9 |
| I11 | Derived layers of dynamic state per step (slope of the air surface; DEM edits by erosion or interventions invalidate slope / D8) | water, gravity | §12 |
| I12 | LUTs recomputable by controllers from mutable parameters and swappable by interventions; ensembles reset mutable parameters per run | growth, spread | §5.2, §7.3, §11 |
| I13 | RNG distributions: add beta, lognormal, multinomial, categorical, discrete 2D Gaussian displacement | front, spread, gravity | §8 |
| I14 | Observers / ensembles: arrival with predicate, point observations, zonal reductions, front speed, per-cell quantiles, means of continuous fields, paired-scenario differences | all | §11, §13 |
| I15 | One-pass state updates: burn-out and ignition must read the same previous state (merge stages or double-buffer across them) | spread | §6 note |
| I16 | `model-mapping.md` corrections (WAT face layer and persistent outflow; HAZ-05 von Neumann primary rule and slot-mask parent; HAZ-02 one-shot traversal; ECO-01 Markov rule; EPI-05 as `queue`; LND-01 `events`; ATM-01 `repeat`) | all | model-mapping.md |
