# Mapping of selected models onto the engine

Coverage check of `engine-architecture.md`: every selected model (ADR 0001) expressed with
the engine primitives.

**Revision 1.1, 2026-10-14.** The authoritative, detailed mapping of each model is section
11a of its card in `docs/models/candidates/`; this file is the summary. Revision 1.0
(2026-10-13) was written before the cards; the corrections found while writing them are
listed at the end.

## Coverage matrix

● = main mechanism of the primary rule, ○ = variant / scenario / optional.

| Model | map | stencil | flux | reduce | convolve | jump | queue | front | agents | allocate | events | repeat | Time policy | RNG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WAT water / flooding | ● | | ● | ● | | | ○ | | | | | ○ | adaptive (period, snapping, look-ahead); converge (FlowFill) | no |
| HYD-05 soil erosion | ● | | ● | ● | | | | | | | | | adaptive (shares WAT; retry) | optional |
| HYD-09 groundwater | ● | | ● | ○ | | | | | | | | | fixed (stability-checked) | no |
| ATM-02 cold air | ● | ○ | ● | ○ | | | | | | | | | fixed (Nowatschin) / adaptive with growth when idle (SAGA) | no |
| HAZ-05 lava | ○ | | ○ | ○ | | | | ● | | | | | budget (pulses) | yes (ensembles) |
| HAZ-02 runout | | | ○ | | | | | ● | | | | | oneShot (per-source traversal) | optional |
| HAZ-01 wildfire | ○ | ● | | ○ | | ○ | ○ | | | | | | fixed; event (PROPAGATOR variant) | yes |
| ECO-01 bark beetle | ● | ● | | ● | | ○ | ○ | | | | | | fixed (year) | yes |
| ECO-09 pest / pathogen | ● | ○ | | ○ | ● | ● | | | | | ○ | | fixed (year) | yes |
| EPI-04 population | ● | ○ | ● | ● | | ● | ○ | | | | | | fixed (generation); event (EPI-05 variant) | yes |
| MOV-03 accessibility | ○ | ○ | | | | | ● | | | | | | event (or converge for the CA-like animation) | optional |
| MOV-01 evacuation | ● | ○ | ○ | ● | | | ● | | ● | | | | fixed (~0.3 s per step) | yes |
| LND-01 urban growth | ● | ● | | ● | ○ | | | | | ● | ● | ○ | fixed (year) | yes |
| ATM-01 dispersion | ● | ● | ○ | | | | | | | | | ● | fixed (hour) with repeat (iterations per hour) | no |

Every primitive is used by at least one core model except `front` and `agents` (extension
only).

## Per-model summary

Stages per step in order; *init* = once before the first step. Component IDs refer to
`docs/review/shared-components.md`.

| Model | Card | Stages per step (primary rule) | Notable engine needs |
|---|---|---|---|
| WAT (WCA2D) | `water-flow-flooding.md` | `map` sources / sinks / infiltration → `flux` (donor kernel on a **persistent face layer**) → every update period: `map` velocity + `reduce` Δt → `reduce` mass balance | adaptive Δt with recompute period, snapping and forcing look-ahead; previous Δt available to kernels; boundaries on edge segments; LND-03 scenario = histogram `reduce` + controller, not flux |
| WAT variants | same | local inertial: `flux` face kernel on persistent discharge; FlowFill: `flux` D8 slots with `converge` or CPU `queue` sweeps | antisymmetric face kernel |
| HYD-05 | `soil-erosion.md` | submodel of WAT: `map` detachment / deposition → `flux` sediment along water outflows → DEM update → derived slope / D8 recomputed | reads WAT flux layer; derived-layer invalidation; step retry (Courant band) |
| HYD-09 | `groundwater-flow.md` | `map` recharge, wells, river exchange → `flux` face kernel (harmonic-mean transmissivity × head difference) → gather | fixed head on interior cell masks; analytical oracle (Theis) |
| ATM-02 | `cold-air-pooling.md` | `map` production by land-use LUT → `flux` face kernel with **per-donor limiter** → gather; SAGA variant: slot outflows ∝ drop / length, adaptive Δt | effective surface (SC-EFFSURF); scatter of SAGA rewritten as gather |
| HAZ-05 | `lava-flow.md` | controller adds a pulse at the vent → `front` shared-grid relaxation until no excess (residual retention, lower non-parent neighbours, share ∝ drop) | parent = **slot bitmask**; primary rule uses von Neumann (MOLASSES uses Moore); keyed order |
| HAZ-02 | `landslide-runout.md` | `front` per-source traversal from each release cell (flow weights × persistence, energy line stop, cutoff with redistribution) → merge by max / sum / count | `oneShot` time; per-source workers; SCIDDICA variant = `flux` with energy as a cell layer |
| HAZ-01 | `wildfire-spread.md` | *init* per-slot elevation difference → one `stencil` (ignition 1 − Π(1 − p) **and** burn-out from the previous state) → optional `jump` spotting → `reduce` burning count | direction values per slot, combined by the kernel; deterministic N2 ray; `reverseSlot` for the Cell2Fire variant |
| ECO-01 | `bark-beetle-outbreak.md` | `stencil` neighbour bump of the level → `map` **categorical Markov** transition from a scenario table → `map` dieback → `reduce` by zone | SC-MARKOV, LUT swap by intervention; Bernoulli / kernel form is a variant |
| ECO-09 | `plant-pest-spread.md` | `map` Gompertz growth → `convolve` exponential kernel (no wrap) → `jump` threshold-triggered jumps (redraw on sea) → `map` control-zone removal | unnormalised kernel; numerical cut-off as a parameter; ensemble mean and paired scenarios |
| EPI-04 | `population-dispersal.md` | `map` K slice + resampling → `map` Ricker growth → `map` clustered catastrophes → `flux` emigration (ordered slot loop with RNG, barrier slot weights) → `jump` **conservative** LDD with acceptance probability | arrival with threshold predicate; per-cell arrival quantiles; EPI-05 as `queue` with exponential edge times |
| MOV-03 | `accessibility-front.md` | `queue` multi-source with anisotropic Tobler cost per slot (direction to / from sources) | `parent` / `nearest` outputs, path tracing, 16 slots; time gates from hazard arrival |
| MOV-01 | `pedestrian-evacuation.md` | *init* `queue` static field → `agents` propose / resolve (friction) / move → `flux` or `stencil` dynamic field (stochastic decay / diffusion) → `reduce` agents left | move probability for slow speeds; `queue` re-run when exits change |
| LND-01 SLEUTH | `urban-growth.md` | `events` spontaneous growth and spreading centres → `stencil` edge growth (scatter as gather) → `events` road growth (spiral search + walk) → `map` commit → `reduce` + controller self-modification | LUT rebuild from mutable coefficients; per-run parameter reset; statistical oracle |
| LND-01 constrained | same | `stencil` / `convolve` neighbourhood effect (class-pair weights) → `map` potential + Weibull noise → `allocate` (joint greedy / quotas / patches) → `map` commit | `allocate` modes; EDT for accessibility; CCL and neutral models for validation |
| ATM-01 | `pollutant-dispersion.md` | per hour: reset from emissions → `repeat` k(u) × (`stencil` wind-weighted normalised focal average with centre weight → `map` reset source cells) | normalised kernel with distance and direction; repeat block; point observations; not mass-conserving |

## Corrections against revision 1.0

| Model | Revision 1.0 said | Corrected (source: card section 11a) |
|---|---|---|
| WAT | outflows in a slot layer; Δt from a `reduce` every step | face layer suffices for WCA2D; outflow layer is persistent state; Δt recomputed every update period |
| WAT / LND-03 | flux scenario | histogram `reduce` + connected basin mask + controller |
| HAZ-01 | `map` burning → burnt after the stencil; spotting by `jump` | burn-out inside the same stencil (previous state); N2 rule is a deterministic ray; per-slot elevation difference needed |
| ECO-01 | Bernoulli draw from LUT by infested-neighbour count; optional jump | neighbour bump + categorical Markov table; felling inside the table; no jump in the primary model |
| EPI-04 | `jump` accumulates arrivals | `jump` is conservative with acceptance probabilities; clustered catastrophes; EPI-05 better as `queue` |
| HAZ-05 | `lava.parent` slot index | slot bitmask; von Neumann in the primary rule |
| HAZ-02 | time policy budget / converge | `oneShot` per-source traversal + merge |
| ATM-02 | plain face flux | per-donor limiter sub-pass; description second-hand (primary not local) |
| LND-01 | `map` spontaneous growth, `walk` road growth, top-N `allocate` | `events` (sequential trials, spiral search + walk), scatter-as-gather stencil, extended `allocate` modes |
| ATM-01 | fixed iterations per hour | `repeat` block, forcing reset each hour, normalised kernel with centre weight |
| MOV-01 | `stencil` for the dynamic field | stochastic integer decay / diffusion (`flux` integer mode); `queue` re-run on exit changes |
