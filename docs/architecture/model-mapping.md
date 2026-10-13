# Mapping of selected models onto the engine

Coverage check of `engine-architecture.md`: every selected model (revision 2) is expressed
with the engine's primitives. Mechanics come from the template entries in
`docs/research/domains/*.md`; parameter values are not repeated here (they belong in the
model cards, with provenance).

## Coverage matrix

● = main mechanism, ○ = used / optional variant.

| Model | map | stencil | flux | reduce | convolve | jump | queue | front | agents | allocate | walk | Time policy | RNG | Topology |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HAZ-01 wildfire | ○ | ● | | ○ | | ○ | ○ | | | | | fixed (event for PROPAGATOR variant) | yes | square |
| WAT water | ● | | ● | ● | | | ○ | | | | | adaptive / converge | no | square |
| EPI-04 population | ● | | ● | ○ | | ● | | | | | | fixed | yes | square (graph for EPI-05 variant) |
| ATM-02 cold air | ● | | ● | ○ | | | | | | | | fixed (adaptive for KLAM-like) | no | square |
| ECO-01 bark beetle | ○ | ● | | ○ | | ○ | | | | | | fixed (year) | yes | square (hex variant) |
| LND-01 urban growth | ● | ● | | ● | | | | | | ● | ● | fixed (year) | yes | square |
| MOV-03 accessibility | ○ | ○ | | | | | ● | | | | | event (or converge) | no | square |
| HAZ-05 lava | ○ | | ○ | | | | | ● | | | | budget | yes (ensemble) | square |
| ECO-09 pest / pathogen | ● | ○ | | ○ | ● | ● | | | | | | fixed (year) | yes | square |
| HAZ-02 runout | | | ○ | | | | | ● | | | | budget / converge | no | square (hex variant) |
| MOV-01 evacuation | ● | ● | | ○ | | | ● | | ● | | | fixed (~0.3 s) | yes | square |
| HYD-05 erosion | ● | | ● | ● | | | | | | | | adaptive (shares WAT) | optional | square |
| ATM-01 dispersion | ● | ● | | | | | | | | | | fixed (iterations per hour) | no | square |
| HYD-09 groundwater | ● | | ● | ○ | | | | | | | | fixed (stability-checked) | no | square |

Every primitive is used by at least one core model except `front` and `agents` (extension
models only) and `convolve` (ECO-09) — these are the candidates to implement later.

## Per-model mapping

### HAZ-01 Wildfire spread (core ★)

- **Templates:** `alexandridis2008cellular` (rule restated in `xia2025pytorchfire`,
  `freire2019using`), `trucchia2020propagator`, firebrands `hargrove2000simulating`.
- **Layers:** `dem` (in), `fuel` (in, categorical + LUT), `density` (in), `slope`
  (derived), `fire.state` (state u8: non-burnable / unburnt / burning / burnt),
  `fire.arrivalTime` (output), wind (forcing, global or raster).
- **Stages:** `stencil` Moore — burning neighbours ignite an unburnt cell with probability
  from vegetation, density, wind alignment (direction weight per slot) and slope (elevation
  difference per slot), Bernoulli draw; `map` burning → burnt; optional `jump` spotting;
  `reduce` count burning (stop condition).
- **Variant:** PROPAGATOR-style — `queue` with stochastic time-to-ignition per neighbour
  (event time policy) — same layers.
- **Observers:** arrival time, burnt area per step; **ensembles** → burn probability map.
- **Interventions:** ignite, firebreak (set non-burnable), change wind.
- **URB-03 scenario:** buildings as fuel classes; same stages with a different LUT.

### WAT Water flow / flooding (core ★)

- **Templates:** `guidolin2016weighted` (WCA2D), `bates2010simple` / `shaw2021lisflood`
  (local inertial), `callaghan2019computing` (FlowFill), `landa2019smoderp2d`.
- **Layers:** `dem` (in), `roughness` (in or LUT), `infiltration` (in / LUT),
  `water.depth` (state f32), `water.out` (slot f32, WCA2D) or `water.q` (face f32,
  local inertial), `water.maxDepth`, `water.arrivalTime` (outputs).
- **Stages (WCA2D):** `map` sources and sinks (rain forcing, point inflow, infiltration);
  `reduce` → Δt (velocity / CFL limit); `flux` outflow pass computes weighted outflows to
  von Neumann neighbours, limited by available volume and velocity, gather pass updates
  depth; `map` velocity estimate.
- **Stages (local inertial):** `flux` with face layer: (a) update face discharge from
  water-surface gradient, friction and previous discharge; (b) gather to update depth.
- **Variant (FlowFill):** fixed runoff, `converge` policy, Jacobi-style synchronous
  version on the GPU or ordered `queue` sweeps on the CPU.
- **Boundaries:** open by default (boundary flux recorded), closed or fixed level per
  scenario.
- **Checks:** mass balance (`reduce` sum of volume + cumulative boundary / sink fluxes);
  benchmark runner with `neelz2010benchmarking` test cases.
- **Interventions:** dam / dike (raise `dem` cells), rain intensity, breach.

### EPI-04 Population dispersal (core; + EPI-05, ECO-04)

- **Templates:** `bradshaw2021stochastic`, `gregoriodesouza2021reassessing`; barriers
  `smith2002predicting`.
- **Layers:** `K` (carrying capacity, derived from land cover via LUT), `pop.N` (state f32
  or i32), `pop.out` (slot), `barrier` (slot weights from rivers / roads), `pop.arrival`.
- **Stages:** `map` local growth (Ricker / logistic, optional demographic noise from
  Poisson / binomial draws); `flux` emigration: outflow pass sends a share of N to
  neighbours when N/K exceeds a threshold, weighted by neighbour suitability and barrier
  weights; gather pass; `jump` long-distance dispersal; `reduce` occupied area.
- **EPI-05 rabies front:** S/I fractions instead of N (SI rule as `stencil`), vaccination
  zones as an intervention mask; graph topology + discrete-time variant of the township
  model is optional.
- **ECO-04 connectivity:** resistance from land cover; compare with MOV-03 cost front.

### ATM-02 Cold-air pooling (core)

- **Templates:** `nowatschin2006gpubased` (GPU shader model), `sievers2016cold` (KLAM_21,
  momentum + heat deficit).
- **Layers:** `dem`, `landuse` (LUT: production, resistance), `cold.k` (state: cold-air
  height), `cold.v` (face: velocities, simple model) or `cold.E`, `cold.u` (heat deficit,
  face momentum for the KLAM-like variant).
- **Stages (simple):** `map` production per land-use class; `flux` with face velocities
  from the difference of (terrain + cold-air surface) divided by resistance, outflow
  limited so outgoing shares ≤ 1, gather; open boundaries.
- **Variant (KLAM-like):** `flux` on face momentum (gravity of the cold-layer top,
  friction, optional ambient wind) + donor-cell advection; adaptive Δt.
- **Scenario:** urban ventilation corridors (buildings as resistance classes).
- **Interventions:** change land use (e.g. build / remove forest), night duration.

### ECO-01 Bark-beetle outbreak (core)

- **Templates:** `pietzsch2023nonparametric` (Markov CA with neighbour spread),
  `liu2025multiscale` (stochastic density CA), parameters `dolezal2016fine`,
  `berec2013population`, CZ validation case `duraciova2020bark`.
- **Layers:** `stand` (in, categorical: spruce share, age class), `susceptibility`
  (derived; drought forcing), `beetle.state` (state: healthy / infested / dead / cleared)
  or `beetle.density` (f32), `beetle.year` (output: year of attack).
- **Stages:** `stencil` Moore (or hex) — transition probability from a lookup table
  indexed by own state, stand features and the number / density of infested neighbours;
  Bernoulli draw; optional `jump` for long-distance dispersal; `map` sanitation felling
  intervention.
- **Time:** annual (or generations per year); ensembles → infestation probability.

### LND-01 Urban growth (core)

- **Templates:** `clarke1997selfmodifying` (SLEUTH), `roodposhti2020towards` /
  `hewitt2019cellular` (constrained CA, SIMLANDER).
- **SLEUTH variant:** layers `slope`, `excluded`, `roads`, `urban` (state u8). Stages per
  year: `map` spontaneous growth (random cells, slope-weighted); `stencil` new spreading
  centres and edge growth; `walk` road-influenced growth along `roads`; `reduce` growth
  rate; **controller** self-modification of coefficients. Monte Carlo ensembles →
  urbanisation probability.
- **Constrained CA variant:** `stencil` with extended distance-decay kernel (neighbourhood
  effect per class), `map` potential = neighbourhood × suitability × accessibility ×
  zoning + Weibull noise, `allocate` top-N cells per class according to yearly demand.
- **Validation:** `analysis` metrics (quantity / allocation disagreement, figure of
  merit) against historical land cover.

### MOV-03 Accessibility front (extension)

- **Templates:** `wood2012anisotropic` (anisotropic Tobler slope + land-cover speed),
  `nelson2019suite`, `weiss2020global` (reference rasters).
- **Layers:** `dem`, `landcover` (LUT speed), `roads`, `travelTime` (output).
- **Stages:** `queue` from sources (hospitals, fire stations, exits) with direction-dependent
  cost per slot (slope along the move); event time policy; the animation reveals the front
  by arrival time. Alternative CA-like visualisation: `stencil` Bellman-Ford relaxation
  with `converge` policy (GPU friendly).
- Also provides the **static floor field** for MOV-01 and connectivity for ECO-04.

### HAZ-05 Lava flow (extension)

- **Templates:** `connor2012probabilistic` (MOLASSES-type), benchmarks
  `dietterich2017benchmarking`.
- **Layers:** `dem`, `lava.thickness` (state), `lava.parent` (state, slot index),
  `residual` (in or drawn per run).
- **Stages:** `front` from the vent: active cells keep the residual thickness and share
  the excess with lower neighbours (not the parent) in proportion to the effective-elevation
  difference; **controller** adds volume pulses until the budget is used.
- **Ensembles:** thousands of runs with residual / volume drawn from truncated normals →
  inundation probability.
- Alternative (SCIARA-type): `flux` with minimisation of differences + temperature
  solidification (same primitive as WAT).

### ECO-09 Plant pest / pathogen spread (extension; + ECO-03)

- **Templates:** `white2017modelling` (Xylella), `moenickes2013shapes` (giant hogweed,
  corridors), CZ case `nehrbass2007simulation`.
- **Layers:** `host` (cover fraction), `K` (derived), `pest.I` (infected fraction),
  `corridor` (in), `control` (intervention mask), `sea / forbidden` (target mask).
- **Stages:** `map` local growth (discretised Gompertz); `convolve` short-range dispersal
  kernel; `jump` long-distance jumps above a threshold, not into forbidden cells; `map`
  control-zone removal.
- **ECO-03 variant:** kernel weights modulated along corridors (`stencil` with
  corridor-dependent weights instead of a static convolution).

### HAZ-02 Runout: debris flow, avalanche, rockfall (extension)

- **Templates:** `damboise2022flowpy` (energy line + persistence), `wichmann2017gpp`,
  `dambrosio2003simulating` (SCIDDICA MoD on hex).
- **Layers:** `dem`, `release` (in), `runout.flux`, `runout.zDelta` (max energy-line
  height), `runout.travelAngle` (outputs).
- **Stages (Flow-Py):** `front` from release cells; flux split to 8 neighbours by slope
  weight × persistence (direction change vs parent), stop when energy-line height < 0 or
  flux < cutoff; per-cell max / sum aggregation; independent release cells can run in
  parallel workers.
- **Variant (SCIDDICA):** `flux` with minimisation of differences (hex or square).

### MOV-01 Pedestrian evacuation (extension)

- **Templates:** `kirchner2002simulation`, `kirchner2003friction`, test suite
  `ronchi2013process`.
- **Layers:** `walls` / `obstacles` (in, from building footprints), `exits`, `S` (static
  floor field, from `queue`), `D` (dynamic floor field, state), `occupancy` (state), agents
  list.
- **Stages:** `queue` once to build S (distance or anisotropic cost from MOV-03); per step:
  `agents` propose (probabilities from S, D, occupancy), resolve conflicts (friction μ),
  move; `map` deposit bosons into D; `stencil` diffusion + decay of D; `reduce` agents
  left (stop).
- **Ensembles:** hundreds of runs → evacuation-time curves.

### HYD-05 Soil erosion / muddy floods (extension)

- **Templates:** `landa2019smoderp2d` (sheet / rill flow on D8), `eltner2025using`
  (RillGrow, plot scale).
- **Composition:** submodel of WAT in the same simulation (R9.2): reads `water.depth`,
  velocities / outflows; adds `soil.erodible`, `sediment.c` (state), `dem` becomes dynamic.
- **Stages:** `map` detachment / deposition from transport capacity; `flux` sediment
  transport along water outflows; derived-layer recomputation of slope when `dem` changes.

### ATM-01 Pollutant / smoke dispersion (extension)

- **Template:** `sonnenschein2025hybrid` (open code, focal weighted average with wind).
- **Layers:** `baseline` (in), `emission` (in / forcing), `conc` (state), morphology
  layers (in).
- **Stages:** `map` reset source cells to emission values; `stencil` n × n focal average
  with direction weights from wind (windward / leeward factors); repeated k iterations per
  forcing hour.
- **Chain:** smoke source from HAZ-01 burning cells (L11).

### HYD-09 Groundwater flow (extension)

- **Template:** `ravazzani2011macroscopic` (macroscopic CA, Theis benchmark).
- **Layers:** `K` (conductivity), `Sy` (specific yield), `bottom`, `head` (state),
  `recharge` (forcing), `wells` (sources / sinks), river cells.
- **Stages:** `flux` von Neumann with harmonic-mean transmissivity × head difference;
  gather update `h += ΣQ·Δt / (Sy·Δs²)`; `map` recharge, wells, river exchange.
- **Boundaries:** fixed head (Dirichlet) and fixed flux (Neumann) cells.
- **Benchmark:** Theis solution (analytical) in the benchmark runner.

## Requirements traceability (summary)

| Requirement group | Covered by | Notes |
|---|---|---|
| R1 space | GridSpec, layers (cell / face / slot), LUT, agents | hex / graph: slot abstraction ready, implementation deferred |
| R2 neighbourhoods | slot tables, weighted / directional kernels, `convolve`, `jump`, `walk` | |
| R3 update schemes | `map`, `stencil`, `flux`, `queue`, `front`, `agents`, `allocate`, active tiles | Gillespie on graphs deferred (C) |
| R4 time | time policies, forcing, display clock | |
| R5 randomness | counter-based RNG, distributions, ensembles | |
| R6 sources / boundaries / interventions | `map` stages, boundary policies, target masks, interventions, controllers | |
| R7 derived layers | geodata pipeline, derived layers with dependencies | |
| R8 observation | observers, exporters, metrics, benchmark runner | |
| R9 coupling | submodels, chains | concurrent multi-clock coupling deferred (C) |
| R10 parameters | ParamDecl with provenance, scenarios, calibration helpers | |
| R11 non-functional | workers, Node, CPU reference, WebGPU, i18n keys | |
