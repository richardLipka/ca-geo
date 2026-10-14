# Urban growth and suburbanisation

| Field | Value |
|---|---|
| ID | `urban-growth` |
| Longlist ref. | `LND-01` |
| Category | land use / settlement dynamics |
| Group | core |
| Weighted score | 3.95 (revision 2) |
| Primary reference | `clarke1997selfmodifying` (variant A, SLEUTH); `roodposhti2020towards` with `hewitt2019cellular` (variant B, constrained CA) |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

Built-up land expands from existing settlements into agricultural and natural land. Growth
concentrates at the edges of existing towns, along roads and in flat, accessible places; it is
blocked by water, protected areas and steep slopes, and it is steered by planning (zoning) and
by how much new land is demanded (population, economy). Time scale: years to decades; spatial
scale: a municipality to a metropolitan region (cells 30–300 m). Demo questions: *where will
Prague's suburbs grow if the trend continues? what changes if a protected zone or a new
motorway exit is added? how much farmland is lost?* (CZ context: suburbanisation south-east of
Prague along the D1 motorway, `indrova2015land`; historical Vienna, `koenig2011cellularautomatabased`).

## 2. Suitability for CA

Good fit: conversion of a cell depends strongly on urban cells nearby (edge growth,
neighbourhood attraction), inputs are rasters (land cover, slope, roads, exclusion) and the
classic models are CA. Limits: the *amount* of growth is driven by non-local socio-economic
demand (handled by an exogenous quota or by self-modifying growth coefficients, not by local
rules); real development comes in parcels and projects (patch models, §5.C); road-network
attraction is a long-range effect (SLEUTH emulates it with searches and walks along the road
raster); results are scenarios, not forecasts (`pontius2007comparing`: error often exceeds
correctly predicted change at native resolution).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `urban` | u8 {0, 1} (A); or class id (B) | urban / non-urban (A); land-use class (B) | evolves |
| `growthYear` | i32 | year of conversion (output, also growth-type code in A) | evolves |
| `delta` | u8 {0, phase code} | cells urbanised in the current year (A, scratch) | per step |
| `slope` | u8 (percent, 0–255 index) | slope class used by the slope LUT (A) | static input |
| `excluded` | u8 0–100 | resistance to urbanisation, ≥ 100 = never (A) | static input |
| `roads` | u8 0–100 | road presence and weight (A); several dated layers | input, switched by year |
| `N_k` | f32 | neighbourhood effect for class k (B) | evolves |
| `S_k`, `A`, `Z_k` | f32 / u8 | suitability, accessibility, zoning (B) | static input |
| `P_k` | f32 | transition potential (B) | per step |
| `urbanProb` | f32 [0, 1] | Monte Carlo urbanisation probability (ensemble output) | output |

## 4. Neighbourhood and time step

- **Grid:** square. A: SLEUTH demo grids of a few hundred cells per side (demo50/100/200 in the
  distribution, implementation SLEUTH 3.0beta_p01, `Input/`); B: 300 m cells in
  `roodposhti2020towards` (7 920 cells, per domain notes); 30 m in `liang2021understanding` and
  `petrasova2016open`; 50 m in `koenig2011cellularautomatabased`.
- **Neighbourhood:** A: Moore (edge growth, spreading centres, road walk) plus non-local
  searches (spiral road search, random spontaneous trials). B: square distance-decay window up
  to 11 × 11 (`roodposhti2020towards`); White–Engelen type models use circular neighbourhoods
  (radius ≤ 8 cells in the software used by `hagenzanker2008neutral`, §3.3); PLUS uses 3 × 3
  (`liang2021understanding`, §4.1).
- **Time step:** one year (A: yearly loop; B: one allocation per year; FUTURES 1 year,
  `petrasova2016open` §4.1.5); Koenig uses one month.
- **Update scheme:** A is *sequential within a year*: phases run in a fixed order and each new
  cell is written to `delta` immediately, so later trials see earlier ones; the urban map `z`
  itself is updated only at the end of the year. B is synchronous potential computation
  followed by a global allocation.
- **Boundary conditions:** A: spontaneous and edge growth only consider interior cells (the
  outermost row / column is never a source); neighbour targets must lie inside the image
  (implementation SLEUTH, `ugm_macros.h` INTERIOR_PT / IMAGE_PT). B: not stated in the
  available sources → open question (treat outside as non-urban, `closed`).

## 5. Transition rule

### 5.A SLEUTH (primary `clarke1997selfmodifying`)

The paper is paywalled and not local (`literature/manifest.md`: manual). The rule below is
restated from the official Gigalopolis documentation as summarised in
`docs/research/domains/land-use.md` and checked against the reference implementation
SLEUTH 3.0beta_p01 (`external/`, no licence → reference / oracle only; facts only, files
`spread.c`, `coeff_obj.c`, `growth.c`, `stats_obj.c`). Five coefficients, each in [0, 100]:
dispersion `c_d`, breed `c_b`, spread `c_s`, slope resistance `c_sl`, road gravity `c_r`.

**Urbanisation test** `try(x)` used by every phase: cell x succeeds iff (1) it is not urban,
(2) it was not urbanised earlier this year, (3) it passes the slope test, (4) it passes the
exclusion test; on success it is written to `delta` with the phase code.
- Slope test: with critical slope `s_c` and exponent `e = c_sl / 50`, the pass probability is
  `p_slope(s) = ((s_c − s) / s_c)^e` for `s < s_c` and 0 otherwise (implementation SLEUTH,
  `spread.c` spr_get_slp_weights; the code stores `1 − p_slope` and passes if a uniform draw
  exceeds it). Higher `c_sl` → steeper slopes resisted more.
- Exclusion test: passes iff `excluded(x) < r`, r a uniform integer in {0 … 99} (`spread.c`
  spr_urbanize). Value 0 still fails with probability 0.01; ≥ 99 never passes (open question
  whether this off-by-one is intended).

**Per year** (`spread.c` spr_spread):
1. *Spontaneous growth.* Number of trials `n_sp = 1 + ⌊c_d · 0.005 · √(rows² + cols²)⌋`
   (at most 5 % of the image diagonal). Each trial picks a uniformly random cell (with
   replacement); if interior, apply `try`.
2. *New spreading centres.* After each successful spontaneous cell, with probability
   ≈ `c_b / 101` (integer draw in {0 … 100} compared with `c_b`), make up to 8 attempts to
   `try` a random Moore neighbour (a random start index, then the next inside-image
   neighbour in a fixed cyclic order); stop after 2 successes (`MIN_NGHBR_TO_SPREAD = 2`).
3. *Edge (organic) growth.* For every interior cell that was urban at the start of the year
   (`z`, not `delta`), with probability ≈ `c_s / 101`: count urban Moore neighbours in `z`; if
   `2 ≤ count < 8`, pick one of the 8 neighbours uniformly and `try` it.
4. *Road-influenced growth.* Collect all cells urbanised this year (phases 1–3). Repeat
   `1 + ⌊c_b⌋` times: (a) pick one of them uniformly; (b) search for the nearest road pixel
   along a square spiral (rings of growing radius, fixed visiting order) up to
   `L = max(4·g·(1 + g), rows, cols)` positions, where `g = ⌊(c_r / 100) · (rows + cols) / 16⌋`;
   (c) if found, walk along the road: at each step take the first road neighbour in cyclic
   order from a random start (backtracking allowed), count steps; stop with success when
   `steps > ⌊roads(x)/100 · c_d⌋` (road value of the current pixel times the *dispersion
   coefficient*, not its scaled value); stop without success at a dead end; (d) on success
   `try` a random neighbour of the end cell and, if it succeeds, make 3 more attempts to `try`
   random neighbours of that new cell.
5. *Commit.* Clear `delta` where `excluded ≥ 100`; every non-urban cell with `delta > 0`
   becomes urban (`z ← 1`); the seed (first control year) stays urban.

**Statistics and self-modification** (`growth.c`, `stats_obj.c`, `coeff_obj.c`):
- growth rate `G = 100 · newCells / urbanCells`; percent urban
  `U = 100 · (urbanCells + roadCells) / (allCells − roadCells − excludedCells)`.
- *Boom* (`G > CRITICAL_HIGH`): `c_sl −= U · SLOPE_SENSITIVITY` (reset to 1 if ≤ 0.01),
  `c_r += U · ROAD_GRAV_SENSITIVITY` (capped at 100); if `c_d < 100`, multiply `c_d`, `c_b`,
  `c_s` by `BOOM` (each capped at 100).
- *Bust* (`G < CRITICAL_LOW`): the opposite changes to `c_sl` and `c_r`; multiply `c_d`, `c_s`,
  `c_b` by `BUST` (each reset to 1 if it falls to ≤ 0.01).
- Coefficients are re-initialised at the start of every Monte Carlo run.

**Land-use extension (Deltatron).** Out of scope for the first demo (open question).

**Conserved:** nothing; urban area only grows (no de-urbanisation). **Not local:** spontaneous
trials, road search radius, self-modification.

### 5.B Constrained CA, SIMLANDER (primary `roodposhti2020towards`, `hewitt2019cellular`)

`roodposhti2020towards` is not local (manual; ScienceDirect bot protection) and
`hewitt2019cellular` is local but its text cannot be extracted (font encoding; no PDF
renderer available). The rule is restated from the domain notes (full-text reading recorded in
`docs/research/domains/land-use.md`) and from the White–Engelen formulation read in full in
`hagenzanker2008neutral` §3.1. Each year:
1. *Neighbourhood effect* (`hagenzanker2008neutral` eq. 6): `N_k(a) = Σ_b w(d(a,b), k, L(b))`
   over all cells b within the window; in SIMLANDER (binary urban case) the weight decays with
   distance as `w(d) = x0 · β^(d / cellSize)` in a square window up to 11 × 11.
2. *Accessibility* `A(a)`: 1 within 300 m of a major road, decreasing along a cosine-sigmoid to
   0 at 1 500 m (`roodposhti2020towards`, per domain notes).
3. *Suitability* `S(a)`: slope classes scored 1.0 / 0.7 / 0.5 / 0.3 / 0.1 / 0.0 (class limits
   not recorded → open question).
4. *Stochastic term* `v(a) = 1 + (−ln(1 − u))^α`, u uniform (Weibull-type).
5. *Potential* `P(a) = N(a) · A(a) · S(a) · v(a)` (zoning `Z` multiplies in the general
   White–Engelen form; `hagenzanker2008neutral` §3.1 lists random term, neighbourhood,
   suitability, accessibility, zoning).
6. *Allocation:* the yearly demand `D` (observed new urban cells ÷ number of years) is given to
   the `D` non-urban cells with the highest `P`. In the multi-class White–Engelen form the
   allocator repeatedly takes the unassigned cell with the highest potential *over all
   classes whose demand is still unmet* (`hagenzanker2008neutral` §3.1) — a joint greedy, not
   independent per-class rankings.

**Conserved:** total area per class equals demand (exactly, by construction).

### 5.C Supporting variants

- **PLUS** (`liang2021understanding` §2.2, read in full; equations partly garbled in text
  extraction → exact forms to be checked): overall probability per class k
  `OP_k = P_k · Ω_k · D_k`, where `P_k` is a random-forest growth probability (offline),
  `Ω_k` the weighted share of class k in an n × n window (`n·n − 1` neighbours, class weight
  `w_k`), and `D_k` an adaptive inertia coefficient updated each iteration from the gap
  between current area and demand (unchanged if the gap shrinks; scaled by the ratio of the
  last two gaps otherwise). If `Ω_k = 0` a patch seed may appear when `P_k` exceeds a random
  value (`OP_k = P_k · r · μ_k · D_k`). A roulette wheel over classes picks the candidate;
  it is accepted if `OP_k > τ = δ^l · r1` and the conversion matrix allows it; `l` (decay step)
  increases when total demand gap shrinks by less than `Step` per iteration. Iterate until
  demand is met.
- **FUTURES** (`petrasova2016open` §2–4, read in full; `meentemeyer2013futures` not read):
  per subregion demand from population (`r.futures.demand`), multilevel logistic potential
  including a dynamic *development pressure* predictor, patch-growing algorithm: draw a seed,
  accept it with its probability, grow a contiguous patch (4/8 neighbours) whose size is drawn
  from a calibrated patch library and whose shape follows a compactness parameter; repeat
  until demand is met; then update development pressure. Development pressure kernels
  (GRASS manual of `r.futures.devpressure`, implementation `external/grass-addons-futures`,
  GPL-2.0+): count, gravity `s / d^γ`, or kernel `s · exp(−2d/γ)` in a `(2·size+1)²` window.
  Scenario lever: incentive power `p → p^x` (x > 1 infill, x < 1 sprawl).
- **Settler roulette (Vienna)** (`koenig2011cellularautomatabased` §4.5, read): monthly
  population moves; cells chosen by roulette wheel proportional to an attractiveness built from
  beta-distribution assessment of density plus a supply potential; von Neumann averaging of a
  population potential.

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Dispersion, breed, spread, slope resistance, road gravity | `c_d, c_b, c_s, c_sl, c_r` | – | 0–100 each | implementation SLEUTH, file `ugm_defines.h` (MIN/MAX values 0.01 / 100) | SF Bay calibrated values in `clarke1997selfmodifying` not read |
| demo200 calibration ranges | – | – | c_d 1–5, c_b 1–5, c_s 7–12, c_sl 75–93 (step 3), c_r 0–50 (step 10) | implementation SLEUTH, file `Scenarios/scenario.demo200_calibrate` | demo only |
| demo200 prediction "best fit" | – | – | c_d 2, c_b 5, c_s 20, c_sl 51, c_r 5 | implementation SLEUTH, file `Scenarios/scenario.demo200_predict` | demo values, not a real calibration |
| Critical slope | `s_c` | % (to be verified) | 15 (calibrate / predict) or 21 (test files) | implementation SLEUTH, `Scenarios/*` | |
| Boom / bust factors | `BOOM`, `BUST` | – | 1.01 / 0.09 (calibrate, predict, derive) vs 0.9 (test files) | implementation SLEUTH, `Scenarios/*` | 0.09 vs 0.9 inconsistency → open question |
| Critical high / low growth | – | % yr⁻¹ | 1.3 / 0.97 | implementation SLEUTH, `Scenarios/*` | |
| Slope / road-gravity sensitivity | – | – | 0.1 / 0.01 | implementation SLEUTH, `Scenarios/*` | |
| Monte Carlo runs | – | – | 4–8 (calibrate / test), 100 (predict) | implementation SLEUTH, `Scenarios/*` | |
| Spreading-centre successes | – | cells | 2 of max 8 tries | implementation SLEUTH, `ugm_defines.h`, `spread.c` | |
| Max spontaneous trials share | – | – | 0.005 · c_d of the diagonal | implementation SLEUTH, `spread.c` | |
| Neighbourhood weight | `x0, β` | – | x0 ∈ [5, 50], β ∈ (0, 1) (search ranges) | `roodposhti2020towards` (domain notes; table not recorded) | best values not recorded |
| Window size | – | cells | up to 11 × 11 | `roodposhti2020towards` (domain notes) | |
| Accessibility limits | – | m | 1 below 300, 0 beyond 1 500 | `roodposhti2020towards` (domain notes) | cosine-sigmoid shape → open question |
| Slope suitability scores | – | – | 1.0 / 0.7 / 0.5 / 0.3 / 0.1 / 0.0 | `roodposhti2020towards` (domain notes) | class limits not given here |
| Weibull exponent | `α` | – | 0.5 | `roodposhti2020towards` (domain notes) | |
| PLUS neighbourhood / seed threshold / decay / step | n, μ, δ, Step | – | 3 × 3, 0.1, 0.9, 500 | `liang2021understanding` §4.1 | trial and error |
| PLUS RF | – | – | 50 trees, 5 % sample | `liang2021understanding` §4.1 | offline |
| FUTURES potential coefficients (Asheville) | – | – | intercept −2.593 (by county), dev. pressure 0.058, road density 0.118, forest −0.013, dist. protected −0.140, dist. water −0.148 | `petrasova2016open` Table 1 | case-specific |
| FUTURES incentive power | x | – | 0.25, 0.5, 1, 2, 4; 50 runs each | `petrasova2016open` §4.1.5 | |
| Vienna GA | – | – | 32 individuals, 28-bit chromosome, crossover 80 %, mutation 1 %, parameter cap 12.7 | `koenig2011cellularautomatabased` §5.1, §6.1 | |

## 6. Deterministic vs. stochastic

A is fully stochastic (cell picks, Bernoulli trials, neighbour choice, road walk); B uses one
noise draw per cell and class (Weibull term), PLUS uses roulette and random seeds, FUTURES
random seeds and patch sizes. Randomness stands for unmodelled decisions of developers and
planners. Ensembles are required: SLEUTH reports means over Monte Carlo runs and a per-cell
urbanisation probability. Fixed seeds are needed for replay; SLEUTH is seeded by `RANDOM_SEED`
but uses a single sequential generator, so our counter-based RNG cannot reproduce its runs
bit-exactly — the oracle comparison must be statistical.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| Urban extent at ≥ 2 dates (A: ≥ 4 control years) | raster, binary | seed + calibration / validation | required |
| Land cover / land use (B, multi-class) | raster, categorical | state + LUT | required for B |
| Roads (by year, weighted 0–100) | vector → raster | road growth (A), accessibility (B) | required |
| DEM → slope | raster, continuous | slope test / suitability | required |
| Exclusion / protected areas, water | vector → raster 0–100 | blocks growth | required |
| Zoning (municipal land-use plans) | vector → raster | Z factor / exclusion | optional |
| Demand per year (and subregion) | time series | quota for B | required for B |
| Hillshade | raster | background only | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| Urban extent, land cover | Copernicus CORINE Land Cover 1990–2018; Urban Atlas; HRL Imperviousness | EU | to be verified (100 m CLC vs 10–20 m HRL) |
| Built-up history | JRC Global Human Settlement Layer (GHSL) built-up epochs | global | to be verified |
| Roads | OpenStreetMap; ČÚZK ZABAGED | CZ / global | to be verified; historical road dates are hard |
| DEM | ČÚZK DMR 5G / DMR 4G; Copernicus DEM | CZ / EU | to be verified (licence) |
| Protected areas | AOPK ČR (NP, CHKO, Natura 2000) | CZ | to be verified |
| Soil protection classes | BPEJ classes (VÚMOP), as used in `indrova2015land` | CZ | to be verified |
| Zoning | municipal land-use plans (územní plány), national planning geoportal | CZ | to be verified; heterogeneous |
| Demand | ČSÚ population projections; dwelling completions | CZ | to be verified |
| Reference probability | `zhou2019highresolution` global SLEUTH projection | global | to be verified |

## 9. Visualization

Animated yearly growth over a basemap, coloured by growth type (spontaneous, spreading centre,
edge, road — SLEUTH phase codes) or by year of conversion; urbanisation-probability map from
the ensemble; time charts of urban area, growth rate and the five coefficients (self-
modification visible as boom / bust); side-by-side SLEUTH vs constrained CA vs neutral model;
interactive edits: paint an exclusion zone, add a road, change demand, change incentive power
(sprawl vs infill), redraw the neighbourhood-weight curve.

## 10. Validation options

- Three-map comparison (initial, observed later, simulated later) with quantity / allocation
  disagreement (`pontius2011death`; not local, metric definitions from domain notes and the
  diffeR package description) and figure of merit (`pontius2007comparing`; not local).
- Fuzzy Kappa with spatial-autocorrelation correction (`hagenzanker2009improved`, read): needs
  nearest-distance per category (Euclidean distance transform), a category-similarity matrix
  and a distance-decay function.
- Neutral benchmarks with the same amount of change (`hagenzanker2008neutral`, read): random
  constraint match and growing clusters.
- SLEUTH-specific fit statistics (implementation SLEUTH, `stats_obj.c`): Lee–Sallee (overlap /
  union of simulated and actual urban), compare ratio of final urban counts, and r² over the
  control years of edges, clusters, population, mean x / y, radius, average slope, mean
  cluster size, percent urban; their product ranks calibrations. Needs connected-component
  labelling.
- Ring-based population difference around the centre of mass (`koenig2011cellularautomatabased` §5).
- Oracle: SLEUTH demo50/100/200 with expected outputs (`control_stats.log`, `avg.log`, yearly
  GIFs) — statistical comparison of averaged statistics, not cell-by-cell.
- CZ case: Průhonice–Čestlice–Modletice area 1994 → 2007 (`indrova2015land`; its input data
  are not open → reconstruct from CORINE / Urban Atlas, to be verified).

## 11. Links to other models

- Chain L8: urban growth → more impervious surface → pluvial flooding (URB-02 / WAT) and heat
  island (URB-01): `urban` output reclassified to imperviousness / Manning n / surface class.
- Accessibility front (MOV-03) can provide travel-time accessibility for variant B.
- LND-02 (farmland abandonment) reuses variant B with other classes.
- Shared components: see §11a.

## 11a. Engine mapping

**Variant A (SLEUTH), per year:**
1. `map` (init year) clear `delta`; switch `roads` layer by year (Forcing, raster series).
2. Spontaneous + spreading centres — sequential sparse trials: K uniform random cells, each with
   a local follow-up (up to 8 neighbour tries). Not a `map`: SLEUTH draws an exact count with
   replacement and checks `delta` between trials. Proposed: `walk` generalised to an *event
   script* stage (§components file, SC-EVENTS) or `custom` (CPU) for the oracle-faithful mode;
   a GPU-friendly approximation is a `map` with per-cell probability `n_sp / cells`.
3. Edge growth — scatter (source picks one random neighbour). Exactly expressible as `stencil`
   (gather) because the keyed RNG lets a target recompute each neighbour's draw
   (`rng(source, 'spread')`, `rng(source, 'dir')`) and its own test draws keyed by
   (source, target); "first success wins" becomes "any success" — same distribution.
4. Road growth — `walk`: seeds = this year's `delta` cells (random with replacement,
   `1 + ⌊c_b⌋` walkers), spiral nearest-feature search with radius from `c_r`, walk along
   `roads` with value-dependent step limit, end-of-walk local action with 1 + 3 tries.
   Sequential; walkers see earlier walkers' results.
5. `map` commit `delta` → `urban`, `growthYear`.
6. `reduce` new cells, urban cells, road cells, excluded cells; **controller** SC-SELFMOD
   (boom / bust with clamping and reset-to-1 rules).
- Time policy: fixed, 1 year. Boundaries: interior-only sources, `closed` for neighbours.
- RNG: yes, everything. Observers: growth type per cell, arrival (year of conversion),
  per-year statistics at control years, ensemble probability. Interventions: paint exclusion,
  add road, change coefficients.

**Variant B (constrained CA), per year:**
1. `stencil` (≤ 11 × 11) or `convolve` (larger, multi-class) — distance-decay neighbourhood
   effect per class with a class-pair weight table `w(d, k, l)`.
2. `map` potential `P = N · A · S · Z · v` (v Weibull from keyed RNG).
3. `allocate` demand: top-D cells (binary) or joint greedy over (cell, class) with per-class
   quotas (multi-class), optionally per subregion.
4. `map` commit; `reduce` areas.
- Init: `A` from distance to roads (Euclidean distance transform, geodata), `S` by LUT.
- Time policy: fixed, 1 year; demand as Forcing series. RNG: noise only (allocation ties).
- PLUS variant needs an *inner loop* (iterate stencil + roulette + acceptance until demand met,
  inertia coefficient updated by a controller between iterations); FUTURES needs patch growing
  (seed sampling + priority growth to a drawn size) and per-step `convolve` of development
  pressure.

**Shared components:** SC-GRID, SC-LUT, SC-SLOPE, SC-RASTERIZE, SC-RECLASS, SC-KERNEL,
SC-ALLOC, SC-EVENTS, SC-SELFMOD, SC-INTERV, SC-BOUNDARY, SC-ARRIVAL, SC-ENSEMBLE,
SC-METRICS, SC-BENCH, SC-CALIB, SC-RNG; proposed new: SC-EVENTS, SC-EDT, SC-CCL /
landscape metrics, SC-NEUTRAL, SC-ALLOC (patch growth), SC-REPEAT (see components file).

**Model-specific:** SLEUTH spiral search order, road-walk neighbour order, slope LUT, fit
statistic product; White–Engelen class-pair weights; PLUS adaptive inertia and descending
threshold.

**Corrections to `model-mapping.md` (LND-01):** (1) spontaneous growth is not a cell-local
`map` but a fixed number of random trials with sequential conflict checks; (2) edge growth is a
scatter that becomes a `stencil` only via keyed RNG — note this as an engine pattern; (3) road
growth needs a nearest-feature *spiral search* before the walk, starts from this year's new
cells, and its step limit uses the road pixel value; (4) `allocate` as "top N per class" is
insufficient for multi-class competition (joint greedy), subregion quotas, roulette sampling
and patch growth; (5) fit statistics need connected-component labelling and an EDT.

## 12. Complexity estimate

- **Implementation:** medium — A has many small sequential details to match the oracle; B is
  simple; PLUS / FUTURES medium–high.
- **Computation in the browser:** low per run (A: ≤ 10⁶ cells × 30–50 years; B: one kernel sum
  per year); high for brute-force calibration (5-D grid × Monte Carlo) → offline in Node.
- **Data preparation:** medium — urban extents at several dates, dated roads, exclusion layers.

## 13. Risks

Users may read projections as forecasts (show probability and neutral models). Historical CZ
data are short (CORINE since 1990) and class definitions change between years. SLEUTH
self-modification and its quirks (exclusion off-by-one, `max(…, rows, cols)` search length,
BUST 0.09) make results sensitive to implementation details. Constrained CA quality depends on
demand, which is exogenous. Licence: SLEUTH has no licence (no code reuse), PLUS binary only,
FUTURES GPL.

## 14. Open questions

- Is `max(4g(1 + g), rows, cols)` for the road-search length intended (a minimum of `rows`
  spiral positions regardless of `c_r`)? Does it match the paper / documentation?
- Is the exclusion test off-by-one (value 0 fails 1 %) intended? Same for `RANDOM_INT(101) < c`.
- BUST = 0.09 (calibrate / predict files) vs 0.9 (test files): typo or deliberate?
- Slope layer units (percent vs degrees) and `s_c` units in SLEUTH.
- How are `excludedCells` counted for percent urban (value ≥ 100 only?).
- SIMLANDER: slope class limits, exact accessibility cosine-sigmoid, whether zoning is used,
  boundary handling, tie handling in allocation, best `x0, β` for Ahvaz — needs a manual read
  of `roodposhti2020towards` and a working text of `hewitt2019cellular` (or the SIMLANDER R
  script, licence unstated).
- PLUS equations 4–7: exact forms (text extraction garbled).
- Which variant leads the demo: SLEUTH (oracle, self-modification) or SIMLANDER (simpler,
  demand-driven, interactive kernel)? (Ask the user — scope decision.)
- Deltatron land-use change: include or not?

## 15. Literature and implementations

- **Primary references:** `clarke1997selfmodifying` (SLEUTH; not local, rule from the official
  documentation and code); `roodposhti2020towards` (SIMLANDER rule with all values; not local);
  `hewitt2019cellular` (SIMLANDER documentation; local but unreadable).
- **Supporting:** `hagenzanker2008neutral` (White–Engelen potential and allocation, neutral
  models; read); `liang2021understanding` (PLUS; read); `petrasova2016open` (FUTURES; read);
  `meentemeyer2013futures` (FUTURES origin; not read); `white1997use`, `white1993cellular`
  (constrained CA origin; not read); `koenig2011cellularautomatabased` (Vienna; read);
  `indrova2015land` (Prague suburbs, LCM / Dyna-CLUE; read); `clarke1998loose`,
  `silva2002calibration`, `dietzel2007toward` (SLEUTH calibration; not read);
  `hewitt2017stable`, `straatman2004towards`, `newland2018multiobjective` (calibration /
  sensitivity; not read); `zhou2019highresolution` (global SLEUTH layer).
- **Validation:** `pontius2011death`, `pontius2007comparing` (not local), `hagenzanker2009improved`
  (read), `hagenzanker2008neutral` (read).
- **Benchmarks:** SLEUTH demo50 / demo100 / demo200 inputs, scenarios and expected outputs in
  `external/SLEUTH3.0beta_p01`; PLUS Wuhan data in mcPLUS (not downloaded); FUTURES GRASS
  testsuites in `external/grass-addons-futures`.
- **Implementations:** SLEUTH 3.0beta_p01 (C, no licence → reference / oracle only);
  FUTURES `r.futures` (GPL-2.0+ → reference only); PLUS / mcPLUS (binaries, no licence → oracle
  only); SIMLANDER (R, licence unstated → reference only until clarified); sleuth_automation
  (GPL-3.0 wrapper, not used).
- **Still missing:** `TODO(literature)` full text of `clarke1997selfmodifying` and
  `roodposhti2020towards`; a peer-reviewed CA for a Czech city (none found); keywords:
  "SLEUTH Czech", "constrained cellular automata Prague", "CORINE urban growth CA Central Europe".

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| urban growth | růst zástavby (urbanizace) | phenomenon |
| built-up / urban cell | zastavěná buňka | state variable |
| spontaneous growth | spontánní růst | rule phase |
| new spreading centre | nové centrum šíření | rule phase |
| edge (organic) growth | okrajový růst | rule phase |
| road-influenced growth | růst podél silnic | rule phase |
| dispersion / breed / spread coefficient | koeficient rozptylu / zakládání / šíření | parameter |
| slope resistance | odpor svahu | parameter |
| road gravity | přitažlivost silnic | parameter |
| self-modification (boom / bust) | samomodifikace (konjunktura / útlum) | controller |
| exclusion layer | vrstva vyloučených ploch | input |
| transition potential | potenciál přechodu | derived |
| neighbourhood effect | vliv okolí | derived |
| suitability | vhodnost | input |
| zoning | územní regulace (územní plán) | input |
| land demand | poptávka po ploše | parameter |
| allocation | alokace | UI output / stage |
| development pressure | rozvojový tlak | derived |
| urbanisation probability | pravděpodobnost urbanizace | UI output |
| figure of merit | míra shody změn (figure of merit) | validation |
| quantity / allocation disagreement | nesoulad v množství / v umístění | validation |
| neutral model | neutrální model | validation |
