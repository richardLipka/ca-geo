# Lava flow

| Field | Value |
|---|---|
| ID | `lava-flow` |
| Longlist ref. | `HAZ-05` |
| Category | natural hazards (volcanic) |
| Group | extension |
| Weighted score | 4.15 (revision 2) |
| Primary reference | `connor2012probabilistic` |
| Status | draft |
| Last updated | 2026-10-14 |

> Primary reference read in full (`literature/open/connor2012probabilistic.pdf`). Facts
> from its GPL successor MOLASSES are cited as "implementation MOLASSES, file
> `external/MOLASSES/src/<file>`" (reference / oracle only, ADR 0006).

## 1. Phenomenon

Molten rock erupted from a vent spreads downslope as a viscous, cooling gravity current,
fills depressions, splits around obstacles and stops when the supply ends or the lava
solidifies. The area inundated depends on erupted volume, effusion rate, rheology
(viscosity, yield strength, crust) and topography. Scales: grid 10–100 m, flows of
1–30 km, hours to months. Questions: *Which areas could a flow from this vent reach? How
likely is a given site to be inundated if a new vent opens somewhere in the field? Would
a barrier divert it?* No CZ relevance (EU cases: Etna, Iceland, Canary Islands); a
didactic counterpart to water and debris models.

## 2. Suitability for CA

Very good, a textbook CA application. The `connor2012probabilistic` algorithm is purely
geometric and local: a cell keeps a residual thickness and passes the excess to lower
neighbours. It deliberately ignores flow rate, rheology and cooling and reproduces only
the final inundated area for a given volume and modal thickness. It is extremely fast:
`dietterich2017benchmarking` reports MOLASSES 2–3 orders of magnitude faster than 2D CFD
codes. That speed makes Monte Carlo hazard maps possible.

Not captured: flow advance in time (iterations are only loosely related to time), cooling
and crust formation, dynamic thickening against obstacles, channel and tube formation,
effusion-rate changes; thickness is imposed by the residual parameter rather than
emerging from physics (`dietterich2017benchmarking`, Discussion).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `dem` | real (m) | pre-eruption ground elevation | static input |
| `lava.thickness` | real ≥ 0 (m) | lava thickness; effective elevation = dem + thickness | dynamic |
| `lava.residual` | real > 0 (m) | thickness a cell retains before passing lava on | per run (drawn) or raster |
| `lava.parent` | slot bitmask (u8) | neighbour(s) the cell received lava from; excluded as receivers | dynamic |
| `lava.active` | boolean / list membership | cell has thickness > residual and is in the active list | dynamic (front) |
| `lava.hit` | count | number of runs in which the cell was inundated | output (ensemble) |
| `vent.density` | real ≥ 0 | spatial density of future vents | static input (ensemble) |

## 4. Neighbourhood and time step

- **Grid:** square; 100 m in the primary (SRTM resampled, §"A grid-based flow regime");
  10–30 m DEMs are better for low effusion rates (`connor2012probabilistic`, §Numerical
  simulation).
- **Neighbourhood:** **von Neumann (4)** in the primary: "adjacent cells are … north,
  south, east and west", an active cell has one parent and up to 3 receivers.
  MOLASSES uses **Moore (8)** with diagonal drops divided by √2
  (implementation MOLASSES, `neighbor_8.c`; also `dietterich2017benchmarking`,
  §MOLASSES).
- **Time step:** one *iteration* = one pulse of volume added at the vent and distributed.
  Not a physical time step; the paper estimates 10³–10⁴ s per 10⁵ m³ pulse for effusion
  rates of 10–100 m³ s⁻¹ (§"A grid-based flow regime").
- **Update scheme:** sequential / asynchronous over an active list (cells updated in
  place, order matters). MOLASSES shuffles the receiver order with `rand()` and re-sweeps
  the active list (implementation MOLASSES, `distribute_proportional2slope4_LJC2.c`).
- **Boundary conditions:** the domain must contain the whole flow; MOLASSES aborts the
  run when the flow reaches the grid edge (implementation MOLASSES, `neighbor_8.c`).

## 5. Transition rule

### 5.1 Primary rule (`connor2012probabilistic`, §"Numerical Simulation of Lava flows" and §"A grid-based flow regime")

Notation: z_i ground elevation, t_i lava thickness, E_i = z_i + t_i effective elevation,
r residual thickness (one value per run), V total volume, ΔV pulse volume, A cell area.

1. **Run set-up** (per Monte Carlo run): sample vent cell from the spatial-density grid
   (§5.3); draw r and V (§5a). Active list = {vent}.
2. **Pulse:** add ΔV / A to t_vent (10⁵ m³ on a 100 m grid = 10 m per iteration); reduce
   the remaining budget V by ΔV.
3. **Distribution** for an active cell a with excess X_a = t_a − r > 0:
   - Receivers N_a = von Neumann neighbours n that are **not the parent** of a and have
     E_n < E_a. (The paper words it as "less than its parent's effective elevation",
     where "parent" refers to the giving cell a; Q1.)
   - Drops D_n = E_a − E_n, T = Σ_{n∈N_a} D_n.
   - Each receiver gets L_n = X_a · D_n / T (eq. 3); t_a ← r; t_n ← t_n + L_n; a becomes
     the parent of each n; receivers are added to the active list.
   - If N_a is empty, a keeps its excess (pooling: "lava may accumulate … greater than
     this residual value if the topography allows pooling").
4. **Iterate** pulses and distributions "until the total flow volume is depleted".
5. **Run outputs:** inundated cells and thicknesses; site hit (1 if the flow intersects
   the area of interest).

Conserved: lava volume exactly (all excess is handed out; MOLASSES checks erupted volume
against volume on the grid). Not conserved / not modelled: momentum, heat.

**Ambiguities (paper):** order in which active cells are processed and whether one pulse
is distributed by a single sweep or until no cell has excess ("Lava is distributed to
adjacent cells only at each iteration" vs. "iterations continue until the total flow
volume is depleted") — Q2; whether a cell can have several parents (paper: "one parent
cell") — Q3; what happens when a cell with excess has no lower non-parent neighbour
after later pulses raise its neighbours — Q4. The text says "100 m² grid cell" but
10⁵ m³ → 10 m thickness implies 100 m × 100 m (10⁴ m²) — typo.

### 5.2 Variant: MOLASSES (facts from the implementation, reference only)

- Moore neighbourhood; drop to a diagonal neighbour divided by √2 (`neighbor_8.c`).
- Parent stored as a 4-bit code (S, E, N, W bits); a diagonal parent sets two bits
  (e.g. SE = S|E) (`distribute_proportional2slope4_LJC2.c`). A diagonal neighbour is
  excluded when either of its two cardinal bits is set (`neighbor_8.c`, masks 3, 6, 9,
  12). Consequence: a cardinal parent S blocks S, SE and SW; a diagonal parent SE blocks
  S, E, SE, SW and NE — a "backward cone", close to Flow-Py's zero-persistence directions.
- The active cell gives *all* lava above its residual to the receivers, in a randomly
  shuffled order; a receiver whose thickness now exceeds its residual is appended to the
  active list; the list is swept again (up to 3 extra passes) before the pulse ends;
  active flags are then reset (same file).
- Residual, total volume and pulse volume are drawn per run from uniform or log-normal
  ranges; residual can also be a raster; optional DEM elevation uncertainty
  (`external/MOLASSES/inputs/molasses.conf`).
- Several vents and several flows per run are supported (`PARENTS = Y` required for
  multi-vent runs, same file).

### 5.3 Vent sampling (`connor2012probabilistic`, eq. 1–2, §Spatial density estimation)

Spatial density of new vents from a Gaussian kernel over N past vents: radially
symmetric (eq. 1, bandwidth h) or elliptical with a 2 × 2 bandwidth matrix H (eq. 2),
H chosen by the SAMSE pilot selector (R package `ks`). Density is evaluated on a grid and
vent cells are sampled from it for each run. In ca-geo the density raster would be a
precomputed input (or computed once by a `map` over vents); sampling is a source draw
(SC-SRCSAMPLE).

### 5.4 Variant: SCIARA family (`barca1994cellular`, `crisci2004simulation`, `spataro2010latest`; notes only)

Synchronous macroscopic CA: substates altitude, thickness, temperature, solidified lava
and 8 outflows; outflows by the *minimisation of differences* with a critical thickness
(Bingham-like) and a relaxation rate, both depending on temperature between vent and
solidus values; cooling and solidification raise the altitude. Same `flux` primitive as
WAT / SCIDDICA (`docs/research/domains/geomorphology.md`). Parameter values not found in
the sources read (Q8).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Grid spacing | Δx | m | 100 | `connor2012probabilistic`, Table 4 (`DEM_SPACING = 0.1` km) | SRTM resampled |
| Residual (modal thickness), Shamiram | r | m | truncated normal, mean 7.0, SD 3.0, truncated to 4–15 | `connor2012probabilistic`, Table 3 and Fig. 5 | |
| Residual in the configuration file | r | m | mean 8.0, SD 1.0 | `connor2012probabilistic`, Table 4 | differs from Table 3 (Q6) |
| Total volume | V | m³ | log₁₀ V truncated normal, mean 7.2, SD 0.5, truncated to 6–9 | `connor2012probabilistic`, Table 3 | config file Table 4: `TOTAL_LAVA_AV = 1e7`, `SD2 = 0.5` |
| Pulse volume | ΔV | m³ | 10⁵ | `connor2012probabilistic`, Tables 3–4 | 10 m per pulse on 100 m grid |
| Runs | – | – | 10 000 | `connor2012probabilistic`, Table 3 | 24.9 % hit the site |
| Flows per run | – | – | 1 | `connor2012probabilistic`, Table 4 | up to 10 tested, broaden but do not lengthen |
| Flank flows: residual | r | m | 6–9 (mapped from codes 1–4) | `connor2012probabilistic`, Table 6 | Fig. 9 caption says 3 m (Q6) |
| Flank flows: total volume | V | m³ | 5 × 10⁸, 5.3 × 10⁸, 8.7 × 10⁸ | `connor2012probabilistic`, Table 6 | |
| Flank flows: pulse volume | ΔV | m³ | 10⁶ | `connor2012probabilistic`, Table 6 | ~1000 runs |
| Vent bandwidth matrix (18 vents) | H | km² | [[0.844, −0.013], [−0.013, 2.113]] | `connor2012probabilistic`, eq. 4 and Methods | case-specific |
| Residual / volume / pulse (example config) | – | m, m³ | residual 3.0; total 3 × 10⁵; pulse 100 | implementation MOLASSES, `inputs/molasses.conf` | Fagradalsfjall example |
| Critical thickness in benchmarks | r | – | set to the observed steady thickness 24.5 cm from vent (BM-A, B, D); mean thickness at 1800 s (BM-C) | `dietterich2017benchmarking`, §MOLASSES | |
| Benchmark slope | – | ° | 15 (BM-A, B); 13.25 (BM-D) | `dietterich2017benchmarking`, Table 1 | |

## 6. Deterministic vs. stochastic

A single run is deterministic in the primary (given vent, r, V); MOLASSES adds a random
receiver order. Stochasticity is in the inputs: vent location (spatial density), residual
and volume (truncated distributions), optionally DEM uncertainty. The randomness
represents uncertainty about future eruptions. Ensembles (10³–10⁴ runs) with a fixed
master seed are essential for the hazard-map demo; individual runs must be replayable
(SC-RNG keyed by run). The receiver order should use a fixed slot order or a keyed draw
so results do not depend on container order (engine-architecture §8).

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| DEM | raster, continuous | ground elevation | required |
| Vent location(s) | point(s) or density raster | source cells | required |
| Past vents | points | to build the vent density (eq. 1–2) | optional |
| Residual, volume, pulse | scalars or distributions | flow size and thickness | required |
| Area of interest | polygon → mask | hit counting | optional |
| Barrier | vector → raised DEM | intervention | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| DEM | Copernicus DEM GLO-30 | global | to be verified |
| DEM | national lidar DEMs (Iceland, Italy, Spain — Canary Islands) | national | to be verified |
| Vents, past flows | geological maps / volcano observatories (e.g. INGV, Icelandic Met Office) | national | to be verified |
| Test case | Fagradalsfjall DEM + vents bundled with MOLASSES (`external/MOLASSES/inputs`) | local | licence of data to be verified |
| Benchmark | `dietterich2017benchmarking` additional file (XLSX) | – | to be verified (not downloaded) |

## 9. Visualization

Animated growth of one flow pulse by pulse over hillshade (thickness colour ramp), vent
marker, "volume erupted" gauge. Ensemble view: inundation probability map and map of
vents whose flows hit the site (like `connor2012probabilistic` Fig. 6). Interactive:
click to place a vent, sliders for volume and residual (thin fluid lava vs thick viscous
lava), draw a diversion barrier, run 100 / 1000 flows. Learning goal: volume and modal
thickness control length; topography steers the flow; probabilistic hazard maps come
from many plausible flows.

## 10. Validation options

- **Benchmarks** `dietterich2017benchmarking`: BM-A (point source on a 15° plane,
  final X, Y, H), BM-B (90° V-obstacle and 180° wall, thickness upslope of obstacle),
  BM-C (axisymmetric spreading on a horizontal plane, final radius). Reported MOLASSES
  NRMSE: BM-A X 8.30 %, Y 3.99 %, H 8.56 %; BM-A&B H 11.60 %; BM-C R 0.56 %; BM-D X
  21.02 %, Y 38.48 %, H 6.15 % (Table 2). Only final states are comparable.
- **Oracle:** MOLASSES runs on the same DEM / parameters (GPL, CLI only), with the
  randomness disabled or compared statistically.
- **Natural flows:** length / area / thickness envelopes vs mapped flows (as in
  `connor2012probabilistic` Fig. 7); Fagradalsfjall example data.

## 11. Links to other models

- **WAT / HAZ-02 SCIDDICA / ATM-02** share effective surface and proportional-to-drop
  distribution; lava adds the residual (retention) threshold and parent exclusion.
- **HAZ-02 runout** shares the `front` primitive (active list + parent) but not its mode
  (lava: shared grid relaxation; runout: per-source traversal).
- **Mud / tailings spreading** could reuse the residual rule (notes in geomorphology.md).
- Lava changes the DEM → a later flow can run on the post-flow surface (chain).

## 11a. Engine mapping

- **Stages per pulse:**
  1. **Controller** (pulse source): if budget remains, add min(ΔV, remaining) / A to the
     vent cell(s) and enqueue them as active (SC-SRC + `budget` time policy).
  2. `front` in **relaxation mode**: pop active cell, compute receivers (not in parent
     mask, lower effective elevation), share excess ∝ drop (÷√2 on diagonals for the Moore
     variant), set parent bits of receivers, push receivers whose thickness exceeds r;
     repeat until the list is empty or a sweep limit is reached.
  3. `reduce`: volume on grid vs erupted (SC-MASS), extent, hit of area of interest.
- **Time policy:** `budget` (pulses until V is used); display clock = pulse index.
- **Boundaries:** domain-exit flag (abort or mark run as "left domain") — a policy the
  engine does not yet list; `open` sink is an alternative.
- **RNG:** per run — vent (from density raster), r, V (truncated normal / log-normal),
  optional DEM noise; receiver order keyed (or fixed).
- **Observers:** final thickness, SC-ENVELOPE, hit / inundation counts (SC-ENSEMBLE),
  SC-MASS. **Interventions:** place vent, barrier (raise DEM), set volume / residual.
- **Shared components:** SC-GRID, SC-FRONT, SC-SRC, SC-MASS, SC-ENSEMBLE, SC-RNG,
  SC-INTERV, SC-BENCH, SC-METRICS; SC-EFFSURF, SC-SLOTMASK (parent bits),
  SC-SRCSAMPLE (vent sampling), SC-SOURCEMERGE (hit maps over runs).
- **Variant (SCIARA-type):** synchronous `flux` with minimisation of differences +
  temperature `map`; same machinery as WAT / SCIDDICA (SC-OUTFLOW).
- **Possible GPU variant:** a synchronous `flux` with residual + parent mask (all active
  cells give excess in parallel) — not identical to the sequential rule; must be
  validated against the `front` version.
- **Model-specific:** residual rule, vent-density sampling, area-of-interest hit test.
- **Corrections to `model-mapping.md`:** (1) the primary uses von Neumann 4, MOLASSES
  Moore 8 with √2 — the mapping should name both; (2) `lava.parent` should be a slot
  **bitmask**, not a single slot index (diagonal parents set two bits in MOLASSES; the
  parent can change across pulses); (3) `front` needs an inner "until no excess" loop per
  pulse and a defined processing order; (4) a domain-exit boundary policy is missing.

## 12. Complexity estimate

- **Implementation:** low–medium (sequential front, controller, ensemble runner).
- **Computation in the browser:** low per run (sparse active list); 10³–10⁴ runs in
  workers are feasible on 10⁵–10⁶-cell DEMs (to be verified by profiling).
- **Data preparation:** low (DEM + vents); vent density needs a KDE step.

## 13. Risks

- Scientific: thickness imposed, not emergent; no time; poor fit for cooling-limited or
  long-lived flows (BM-D NRMSE 21–38 % for extent).
- Data: no CZ case — demo uses foreign DEMs (licences to be verified).
- Technical: order dependence of the sequential rule; GPU variant differs.
- Communication: "probability given a new vent opens" is conditional, not an annual
  probability; must be labelled.

## 14. Open questions

- Q1: Receiver criterion — lower than the active cell (E_n < E_a) or than the active
  cell's parent? Code (MOLASSES) compares with the active cell.
- Q2: Within one pulse — single sweep or relax until no excess? MOLASSES: list re-swept
  up to 3 extra times; the PERL script (Additional file 2) is not local.
- Q3: Can a cell have several parents (MOLASSES overwrites the code with the last giver)?
- Q4: What happens to excess in a cell with no eligible receiver once it is no longer
  active (pooling semantics across pulses)?
- Q5: Is the MOLASSES backward-cone exclusion (cardinal parent blocks 3 cells, diagonal
  parent 5 cells) intended, and should ca-geo copy it or use the paper's "parent only"
  exclusion? Decide by comparing ensemble outputs.
- Q6: Residual parameters: Table 3 (7 ± 3 m) vs Table 4 (8 ± 1 m); flank flows Table 6
  (6–9 m) vs Fig. 9 caption (3 m).
- Q7: Effect of the random receiver order on ensemble statistics (compare fixed vs
  shuffled).
- Q8: SCIARA parameter values — `TODO(literature)` (spataro2010latest full text not
  accessible).

## 15. Literature and implementations

- **Primary reference:** `connor2012probabilistic` — simplest complete lava CA with a
  probabilistic workflow and parameter distributions; open access.
- **Supporting references:** `dietterich2017benchmarking` (benchmarks, MOLASSES
  accuracy and speed); `barca1994cellular`, `crisci2004simulation`, `spataro2010latest`
  (SCIARA variant, notes only); `digregorio1999empirical` (minimisation of differences).
- **Benchmarks / reference data:** `dietterich2017benchmarking` BM-A–D; MOLASSES
  Fagradalsfjall inputs (`external/MOLASSES/inputs`).
- **Implementations:** MOLASSES (C, GPL-3.0) — reference / oracle only; USF molasses
  (CC BY-NC 3.0) — reference only; SCIARA CUDA port (GPL-2.0, unofficial) — reference
  only; MrLavaLoba (custom licence) — not used.
- **Still missing:** `TODO(literature)` — Richardson (2016) MOLASSES validation (thesis;
  not in references.bib); flat / dipping-plane test DEMs (not found in the clone).

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| lava flow | lávový proud | phenomenon |
| vent | (erupční) průduch | phenomenon / input |
| effusion rate | rychlost výlevu (efuze) | parameter |
| lava thickness | mocnost lávy | state variable |
| effective elevation | efektivní výška (terén + láva) | state variable |
| residual thickness | zbytková mocnost | parameter |
| parent cell | rodičovská buňka | state variable |
| pulse volume | objem pulzu | parameter |
| erupted volume | celkový vyvržený objem | parameter |
| vent spatial density | prostorová hustota průduchů | input |
| inundation probability | pravděpodobnost zaplavení lávou | UI output |
| diversion barrier | odkloňovací val | UI action |
| place vent | umístit průduch | UI action |
