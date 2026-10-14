# Shared components

Building blocks that recur across the selected models — the basis for the general CA
engine (`docs/architecture/`). Each component has a stable ID (`SC-…`) used in the model
cards (`docs/models/candidates/*.md`, section 11a).

**Status:** seed list (2026-10-14), to be completed from the model cards.

## Seed list

| ID | Component | Engine element |
|---|---|---|
| SC-GRID | Georeferenced raster grid with domain mask | GridSpec |
| SC-LUT | Categorical layer + lookup table (class → parameters) | LayerDecl.categories |
| SC-FACE | Edge-centred (face) layers | Placement `face` |
| SC-SLOT | Per-neighbour slot layers | Placement `slot` |
| SC-SLOPE | Slope, aspect, hillshade | geodata derived layer |
| SC-D8 | Flow direction, flow accumulation | geodata derived layer |
| SC-FILL | Depression filling | geodata derived layer |
| SC-COST | Cost-distance, anisotropic (slope-dependent) cost | `queue` + geodata |
| SC-RASTERIZE | Rasterisation of vectors, incl. barriers between cells | geodata |
| SC-RECLASS | Reclassification of land cover to model classes | geodata + LUT |
| SC-OUTFLOW | Conservative outflow distribution (minimisation of differences, weighted, multiple flow direction) | `flux` |
| SC-INERTIAL | Face flux with local inertia and friction | `flux` on face layer |
| SC-ADT | Adaptive time step (CFL / velocity limit, snapping to output times) | TimePolicy `adaptive` + `reduce` |
| SC-SRC | Sources, sinks and time-dependent forcing | `map` + Forcing |
| SC-STOCH-SPREAD | Stochastic neighbour transmission (ignition / infection) | `stencil` + RNG |
| SC-DIRWEIGHT | Direction weights from wind, slope or aspect | Neighbourhood `directional` |
| SC-KERNEL | Dispersal kernels and convolution | `convolve` / weighted `stencil` |
| SC-LDD | Long-distance jumps | `jump` |
| SC-GROWTH | Local population growth (logistic, Ricker, Gompertz) | `map` |
| SC-QUEUE | Priority-queue front propagation | `queue` |
| SC-FRONT | Active list with parent (runout, lava) | `front` |
| SC-ENERGY | Energy line / travel-angle stopping criterion | `front` state |
| SC-AGENTS | Lattice agents with propose–resolve | `agents` |
| SC-FLOORFIELD | Static and dynamic floor fields | `queue` + `stencil` |
| SC-ALLOC | Demand-constrained allocation | `allocate` |
| SC-ROADWALK | Walk along a network raster | `walk` |
| SC-SELFMOD | Controller changing parameters from global statistics | Controller |
| SC-INTERV | User interventions (ignite, barrier, dam, control zone, exit) | Interventions |
| SC-BOUNDARY | Boundary policies | BoundaryPolicy |
| SC-ARRIVAL | First-arrival time observer | Observer |
| SC-ENVELOPE | Maximum envelope observer | Observer |
| SC-MASS | Mass-balance observer | Observer + `reduce` |
| SC-ENSEMBLE | Ensembles and probability maps | Ensemble runner |
| SC-METRICS | Validation metrics (disagreement, figure of merit, Jaccard, fuzzy kappa, RMSE) | analysis |
| SC-BENCH | Benchmark runner with reference data | analysis |
| SC-CALIB | Calibration (sweep, Latin hypercube, genetic algorithm) | analysis |
| SC-RNG | Counter-based RNG and distributions | RNG |
