# Landslide, debris-flow, avalanche and rockfall runout

| Field | Value |
|---|---|
| ID | `landslide-runout` |
| Longlist ref. | `HAZ-02` (scenarios: avalanche `HAZ-03`, rockfall) |
| Category | natural hazards (gravitational mass flows) |
| Group | extension |
| Weighted score | 3.85 (revision 2) |
| Primary reference | `damboise2022flowpy` |
| Status | draft |
| Last updated | 2026-10-14 |

> Primary reference read in full (`literature/open/damboise2022flowpy.pdf`); supporting
> `wichmann2017gpp`, `horton2013flowr`, `dambrosio2003simulating` read. Facts from the
> GPL Flow-Py v1.0 clone are cited as "implementation Flow-Py, file
> `external/FlowPy/<file>`" (reference / oracle only, ADR 0006).

## 1. Phenomenon

Gravitational mass flows (GMF) — debris flows, shallow landslides turning into flows,
snow avalanches, rockfall — start in steep release (starting) zones, travel through
transit zones and stop in runout zones on flatter ground. Runout length is classically
described by the travel (runout) angle α: the line from the top of the release to the
farthest deposit (Heim's energy line). Lateral spreading depends on the material (block
movement vs fluid-like spreading). Scales: 5–10 m grids, slopes of 0.1–5 km, seconds to
minutes, regional maps of 10–1000 km². Questions: *Which areas can a flow from these
release zones reach? With what intensity? Which release zones threaten this road or
house? What changes if the forest disappears?* CZ relevance: flysch landslides and debris
flows (Beskydy, Hrubý Jeseník after Storm Boris 2024, `tichavsky2026hydrogeomorphic`),
avalanches in Krkonoše and Jeseníky, rockfall in sandstone areas.

## 2. Suitability for CA

Good. Flow-Py is a cell-by-cell local rule: a 3 × 3 window around a "base cell" routes
flux to neighbours depending on local terrain and on the direction it came from; a
stopping rule along the path ends the process. It is not called a CA, and it is not a
synchronous CA: paths are traversed per release cell (breadth-first). SCIDDICA
(`dambrosio2003simulating`) is a true synchronous macroscopic CA for the same phenomenon.

Not captured by the data-based models: mass, volume, momentum, entrainment and
deposition (Flow-Py "does not account for mass"; persistence is only an analogy of
momentum, `damboise2022flowpy` §2.4.3), time evolution (no time-dependent equations),
release (trigger) mechanics — release zones are an input.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `dem` | real (m) | elevation | static input |
| `release` | boolean / ID | starting cells (release zones) | static input |
| `landcover` | categorical | friction / runout-angle class (forest extension, GPP friction) | optional input |
| `runout.R` | real ∈ [0, 1] | routing flux at a cell for the current path | per-path (front) |
| `runout.Zdelta` | real ≥ 0 (m) | energy-line height above terrain (process intensity, kinetic-energy height) | per-path (front) |
| `runout.S` | real ≥ 0 (m) | projected travel distance from the start cell | per-path |
| `runout.parents` | slot bitmask | neighbours that passed flux to the cell | per-path |
| `out.Zmax`, `out.Rmax` | real | maximum Z^δ and R over all paths | output |
| `out.Zsum`, `out.CC` | real, count | sum of Z^δ, number of paths through the cell | output |
| `out.gammaMax` | real (°) | maximum travel angle | output |
| `out.backtrack` | boolean / ID | cells whose paths reach infrastructure | output (extension) |
| SCIDDICA variant: `qth`, `qe`, `qd`, `qo` | real; slot | debris thickness, energy, erodible soil depth, 6 outflows | dynamic |

## 4. Neighbourhood and time step

- **Grid:** square; 5 and 10 m tested (`damboise2022flowpy` §2.3); 10 m recommended for
  regional debris-flow mapping (`horton2013flowr` §4.1.1). SCIDDICA: hexagonal (square
  for quick tests).
- **Neighbourhood:** Moore (3 × 3 around the base cell) for Flow-Py, Flow-R, GPP;
  hexagonal 6 for SCIDDICA S3-hex.
- **Time step:** none in Flow-Py — "spatial iterations" only. The display clock can use
  the breadth-first generation (distance in steps from the release). SCIDDICA: fixed CA
  step with a time correspondence pt (value not given).
- **Update scheme:** Flow-Py / Flow-R — sequential traversal of an active (calculation)
  queue per release cell, independent between release cells (parallel tiles in Flow-Py,
  §2.3). GPP — one particle at a time, Monte Carlo repetitions. SCIDDICA — synchronous.
- **Boundary conditions:** cells whose 3 × 3 window touches NoData or the grid edge are
  not expanded (implementation Flow-Py, `flow_core.py`); GPP deletes the particle at the
  DTM border (`wichmann2017gpp` §2).

## 5. Transition rule

### 5.1 Primary rule (`damboise2022flowpy`, §2.4, eq. 1–17)

Notation: b base cell, p its parent(s), n / i neighbours, z elevation, Δx cell size,
S_bn horizontal distance b→n (Δx or √2 Δx), α runout angle, exp divergence exponent,
R_stop flux cutoff, Z_lim intensity limit.

1. **Release.** Each starting cell starts its own path with R_start = 1 and Z^δ = 0
   (§2.4.1; implementation Flow-Py: start cells sorted by altitude, highest first).
2. **Energy line** (eq. 10–13, 15): for each neighbour n of base b:
   Z^γ_bn = z_b − z_n (elevation drop), Z^α_bn = S_bn · tan α (friction loss),
   Z^δ_n = min(Z^δ_b + Z^γ_bn − Z^α_bn, Z_lim). Z^δ is the kinetic-energy height above
   the terrain (Fig. 1, eq. 5).
3. **Terrain weight** (eq. 7): local slope θ_n from b to n (positive downhill),
   distribution angle φ_n = (θ_n + 90°)/2, T_n = tan(φ_n)^exp / Σ tan(φ_m)^exp. Because
   φ ∈ (0°, 90°), uphill and flat neighbours get small but non-zero weight — the flow can
   cross flat ground and climb (exp ≥ 1; exp → ∞ single flow direction, exp → 1 wide
   spreading).
4. **Persistence weight** (eq. 8–9): for each parent p, direction weight
   D_n = max(0, cos δ), δ = deviation between the incoming direction p→b and the outgoing
   direction b→n; this gives 1 straight ahead, 0.707 at ±45°, 0 elsewhere (also the
   parent). P_n = Σ_p Z^δ_p · D_n(p) — parents with higher energy steer more.
5. **Routing** (eq. 6): R_n = T_n P_n / Σ_m T_m P_m · R_b. Flux is conserved
   (Σ R_n = R_b) unless a stopping rule applies.
6. **Stopping:** a neighbour does not become a child if Z^δ_n < 0 (runout-angle stop,
   eq. 16) or R_n < R_stop (flux stop, eq. 17). Children are appended to the calculation
   queue.
7. **Restrictions** (§2.4.3): a cell that has been a base cell cannot become a child
   again (prevents ping-pong in bowls); Z^δ capped at Z_lim (eq. 15).
8. **Multiple parents:** a child reached from several parents keeps the maximum Z^δ of
   the incoming routes and accumulates their flux (§2.4.3).
9. **Path end:** when the queue is empty, per-cell results are merged into raster
   outputs: Z_max = max, R_max = max, Z_sum = Σ, CC = count, γ_max = max (§2.5).

Conserved: routing flux R per path (up to cutoffs). Not conserved: mass, volume,
momentum (not modelled). Geometric check: along a centreline, z + Z_max matches the
α-line from the release top (RMSE 4 × 10⁻⁵, §3.4, Fig. 6) — an exact unit test.

### 5.1a Implementation details (implementation Flow-Py, `flow_class.py`, `flow_core.py`)

- Z^δ_n is clipped at 0 and Z_lim before use; T is zeroed where Z^δ_n ≤ 0 or the
  persistence is 0, and for the base cell itself.
- Start cells and their direct children use persistence 1 in all directions.
- Shares below R_stop are not lost: their sum is redistributed equally to the shares
  above the threshold, and any remaining deficit is also spread equally — flux stays
  exactly R_b (deviation from the paper's "stop" wording, Q2).
- Children are processed in FIFO order (breadth-first); new children of a base are
  sorted by Z^δ before insertion. Flux arriving at a location is merged only into
  entries not yet processed; otherwise a new entry for the same location is appended
  (as read; to be verified by running the oracle, Q3).
- After each release cell, all release cells already reached by its path (Z^δ > 0) are
  removed from the list of release cells — also in the default calculation, not only in
  the back-tracking extension the paper describes (§5.1) (Q4).
- Travel-angle outputs: γ from the start cell along the shortest parent path and along
  the straight line.

### 5.2 Variant: Flow-R (`horton2013flowr`, §2.2)

- **Spreading:** Holmgren multiple-flow-direction p_i = (tan β_i)^x / Σ (tan β_j)^x over
  lower neighbours (eq. 3), modified by raising the central cell by dh to smooth DEM
  roughness (§2.2.1).
- **Persistence:** weights by direction change (eq. 4, Table 1): proportional
  (0°: 1, 45°: 0.8, 90°: 0.4, 135°: 0, 180°: 0), cosines (1, 0.707, 0, 0, 0), Gamma
  (1.5, 1, 1, 1, 0); backward direction always 0.
- **Combination** (eq. 5): p_i = p_i^fd · p_i^p / Σ (p_j^fd · p_j^p) · p_0.
- **Energy:** unit kinetic-energy balance per step (eq. 6); friction by Perla (PCM)
  or SFLM: E_f = g · Δx · tan φ (eq. 9), velocity V_i = min(√(V_0² + 2gΔh − 2gΔx tan φ),
  V_max) (eq. 10); cells without energy are not reached.
- **Precision:** susceptibility below a threshold is nulled and redistributed locally to
  active cells to conserve the total (§2.2.3) — same idea as Flow-Py's redistribution.
- **Processing:** active-cell list per source area; overlapping propagations merged by
  sum of susceptibility and max of energy; results by sum or max (§2.3).

### 5.3 Variant: GPP (`wichmann2017gpp`, §2–3)

- A particle walks from a start cell; Monte Carlo repetitions (default 1000) per cell;
  outputs transition frequencies, max velocity, stop positions.
- **Path:** steepest descent (eq. 1) or random walk: neighbours admitted by a slope
  threshold and divergence exponent a (eq. 2–4), chosen with probability
  ∝ f_i · tan β_i where f = persistence factor p for the previous direction, else 1
  (eq. 5). Flat areas: random choice among untraversed equal-height cells.
- **Runout:** geometric gradient, Fahrböschung, shadow angle (energy line, eq. 6–7),
  one-parameter friction (rockfall: free fall, energy loss on impact, sliding / rolling,
  eq. 8–12), PCM two-parameter (μ, M/D; eq. 13–19).
- **Deposition:** sink filling and deposition on stop / along path alter the DTM between
  iterations (order of release areas matters, §2).

### 5.4 Variant: SCIDDICA S3-hex (`dambrosio2003simulating`, §2.3, §3.2)

Synchronous hexagonal CA. Substates: altitude q_a, debris thickness q_th, energy q_e,
erodible soil depth q_d, 6 outflows q_o. Per step, in order:

1. **T1 mobilisation:** if q_e > p_mt, eroded depth d = min((q_e − p_mt) · p_er, q_d);
   altitude and soil depth decrease, thickness and energy increase (eq. 16–17).
2. **I1 outflows by minimisation of differences:** central height uses the run-up
   r = k · q_e / q_th instead of the thickness (k = 2/(ρgA)); q(0) = q_a(0) + p_adh,
   p = r − p_adh, q(i) = q_a(i) + q_th(i). Neighbours whose "angle" to the centre is below
   p_f are removed; then iteratively: average = (p + Σ_{i∈A} q(i)) / #A, remove cells with
   q(i) ≥ average; outflow f(i) = average − q(i) for i ∈ A; normalised by
   v_nf = q_th / r and relaxed by p_r (eq. 9 and steps 1–4).
3. **I2 update:** new thickness = q_th + Σ (inflows − outflows); energy updated with
   inflowing / outflowing energy referred to the central altitude.
4. **T2 energy loss:** run-up reduced by p_rl (not below the thickness).

Ambiguities: p_f is called a height threshold but step 1 compares an angle (Q6); the
time correspondence p_t is not given (Q7). Full minimisation algorithm is in
`digregorio1999empirical` (not read; paywall).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Runout angle (avalanche, examples) | α | ° | 25 (30 stops on the dam) | `damboise2022flowpy` §3.1–3.3, §4.1 | large to very large avalanches |
| Divergence exponent | exp | – | 8 (high spreading), 100 (low) | `damboise2022flowpy` §3.1, Fig. 3 | 8 on 10 m DEM for avalanches (§4.1) |
| Flux cutoff | R_stop | – | 3 × 10⁻⁴ (default) | `damboise2022flowpy` §2.4.6 | same value recommended by `horton2013flowr` §4.1.2 for 10 m |
| Intensity limit | Z_lim | m | 8849 (= no limit) | `damboise2022flowpy` §3.1 | |
| Start flux | R_start | – | 1 | `damboise2022flowpy` §2.4.1 | |
| Release criterion (performance test only) | – | m, ° | altitude > 1800, slope 31–34 | `damboise2022flowpy` §4.1 | "overly simple", not for hazard use |
| Persistence weights | D | – | 1 / 0.707 / 0 | `damboise2022flowpy` eq. 9 | |
| Holmgren exponent (debris flows) | x | – | 4 (Claessens); 4–6 common | `horton2013flowr` §2.2.1, §4.1.3 | |
| Central-cell raise | dh | m | 2 (fine DEMs); negligible ≥ 25 m | `horton2013flowr` §4.1.1 | |
| Susceptibility threshold | – | – | 10⁻⁴ (2 m DEM), 3 × 10⁻⁴ (10 m) | `horton2013flowr` §4.1.2 | |
| Travel angle, debris flows | φ | ° | 11 (coarse / medium), 7 (fine-grained) | `horton2013flowr` §2.2.2 (citing Zimmermann et al.) | |
| Velocity limit | V_max | m s⁻¹ | 15 | `horton2013flowr` §2.2.2 | |
| Persistence tables | w0…w180 | – | see §5.2 | `horton2013flowr` Table 1 | |
| GPP rockfall | – | °, %, – | slope threshold 55–65; exponent 1.5–2.0; persistence 1.0–1.6; free-fall threshold 55–65; energy reduction 70–75 %; μ 0.35–2.5 (sliding) | `wichmann2017gpp` Table 1 | |
| GPP debris flow | – | °, –, m | slope threshold 20–40; exponent 1.3–3.0; persistence 1.5–2.0; μ 0.04–0.8; M/D 20–150 | `wichmann2017gpp` Table 3 | |
| GPP avalanche | – | °, –, m | slope threshold 45–60; exponent 1.3–5.0; persistence 1.5–3.0; μ 0.1–0.5; M/D 20–1000 | `wichmann2017gpp` Table 4 | |
| GPP friction by land cover | μ | – | meadow 0.5–0.6; alpine shrubs 0.6–0.9; bushes 0.6–0.7; open forest 1.0–2.0; dense forest > 2.0; bare rock 0.4–0.9; scree (flysch) 0.6–0.7 | `wichmann2017gpp` Table 2 | rockfall sliding model |
| GPP iterations | – | – | 1000 (default) | `wichmann2017gpp` §2 | |
| SCIDDICA cell apothem | p_a | m | 1.25 | `dambrosio2003simulating` §4.2 | |
| SCIDDICA adherence | p_adh | m | 0.001 | same | |
| SCIDDICA height threshold | p_f | m | 0.1 | same | Q6 |
| SCIDDICA relaxation rate | p_r | – | 1 | same | |
| SCIDDICA run-up loss | p_rl | m | 0.6 | same | |
| SCIDDICA mobilisation threshold | p_mt | printed as "m2" | 3.5 | same | compared with energy q_e — unit unclear |
| SCIDDICA erosion parameter | p_er | – | 0.015 | same | |
| SCIDDICA time per step | p_t | s | not given | `dambrosio2003simulating` Table 2 | Q7 |
| SCIDDICA fit thresholds | e1, e2 | – | 0.7, 0.85 | `dambrosio2003simulating` §4.2 | |

## 6. Deterministic vs. stochastic

Flow-Py, Flow-R and SCIDDICA are deterministic. GPP is stochastic (random walk, Monte
Carlo, seed fixable). Uncertainty in Flow-Py can be explored by parameter ensembles
(α, exp) rather than RNG. For the demo: deterministic Flow-Py default; GPP-style random
walk as an optional stochastic variant with a keyed RNG (SC-RNG).

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| DEM | raster, continuous | routing and energy line | required |
| Release zones | raster / polygons → mask | start cells | required (or derived) |
| Land cover / forest | raster, categorical | α or μ per class (forest extension, GPP friction) | optional |
| Infrastructure | raster / vector → mask | back-tracking target | optional |
| Slope, curvature, lithology, flow accumulation | derived / categorical | release-zone derivation (Flow-R source criteria) | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| DEM | ČÚZK DMR 5G / DMR 4G | CZ | to be verified |
| DEM | Copernicus DEM GLO-30, EU-DEM | EU | to be verified |
| Landslide inventory | ČGS slope-instability register | CZ | to be verified |
| Avalanche paths / events | Horská služba ČR; Krkonoše NP records | CZ | to be verified |
| Forest / land cover | Copernicus HRL Tree Cover Density, CORINE, ZABAGED | EU / CZ | to be verified |
| Generic test terrains | AvaFrame generated topographies (parabolic slope, channel, dam) | – | EUPL code; data licence to be verified |

## 9. Visualization

Release zones drawn or derived; animated front growing generation by generation from the
release, coloured by Z^δ (intensity) or flux; final maps Z_max, CC, travel angle.
Side-by-side parameter comparison (α, exp) on the same slope; energy-line profile along
a clicked path (terrain, α-line, Z^δ). Interactive: paint release zones, remove or plant
forest (α or μ class), click a building to back-track the threatening release zones.
Scenarios: debris flow, avalanche (HAZ-03), rockfall (GPP-style parameters).

## 10. Validation options

- **Analytical:** α-line on generic slopes — z + Z_max equals the straight line from the
  release top (`damboise2022flowpy` §3.4); exact unit test for the engine.
- **Oracle:** Flow-Py v1.0 (GPL) on the same DEM / parameters; AvaFrame test
  topographies (not cloned).
- **Events:** mapped debris-flow outlines (SCIDDICA indicators e1, e2 —
  `dambrosio2003simulating`; SC-METRICS Jaccard-like), CZ inventories (Storm Boris 2024,
  to be verified).
- Mostly qualitative for avalanches without CZ event data.

## 11. Links to other models

- **HAZ-05 lava** shares `front` (active list, parents) but not its mode.
- **WAT / ATM-02 / SCIDDICA** share the effective-surface + outflow family; SCIDDICA's
  run-up is the synchronous counterpart of Flow-Py's Z^δ.
- **HYD triggers:** rainfall / saturation (WAT) → release zones (L7 chain:
  landslide → river blockage → dam breach); **ECO / forest** cover changes α (protective
  forest); **ATM-05** snow redistribution → avalanche release (HAZ-03).

## 11a. Engine mapping

- **Stages:**
  1. `init`: derive release cells (input mask or `map` with slope / altitude criteria);
     sort by altitude (implementation order).
  2. `front` in **per-source mode**, for each release cell independently: queue of
     (cell, R, Z^δ, S, parent mask); expand by the 3 × 3 rule of §5.1 (energy line →
     terrain weight → persistence → routing → stop tests → cutoff redistribution);
     merge duplicate children (sum R, max Z^δ, OR parent mask).
  3. **Merge** per-path results into global outputs (max / sum / count) —
     SC-SOURCEMERGE; independent sources run in parallel workers.
- **Time policy:** none / `event` — a one-shot traversal; display clock = BFS generation
  of the active path (the mapping's "budget / converge" does not fit Flow-Py).
- **Boundaries:** skip expansion near NoData / edge (closed); record "reached edge".
- **RNG:** none (Flow-Py); keyed per particle and iteration for the GPP variant.
- **Observers:** Z_max, R_max, Z_sum, CC, γ_max, back-tracking. **Interventions:**
  release zones, forest removal / planting (α or μ class change), dam (raise DEM),
  infrastructure target.
- **Shared components:** SC-GRID, SC-SLOPE, SC-FRONT, SC-ENERGY, SC-ENVELOPE,
  SC-METRICS, SC-BENCH, SC-INTERV, SC-LUT (forest α / μ), SC-RNG (GPP); SC-FLOWWEIGHT,
  SC-PERSIST, SC-SLOTMASK, SC-FLOWWEIGHT (cutoff), SC-SOURCEMERGE, SC-PATHTRACE.
- **Variant (SCIDDICA):** synchronous `flux` with minimisation of differences on hex or
  square + `map` stages for mobilisation and energy loss; energy (run-up) is a cell
  layer, so SC-ENERGY is not only a `front` state.
- **Model-specific:** runout-angle bookkeeping, Flow-Py half-angle terrain weight,
  back-tracking extension, GPP friction models.
- **Corrections to `model-mapping.md`:** (1) Flow-Py routing is T × P where persistence
  is weighted by the parents' Z^δ, uphill routing is allowed, parents are excluded and
  multi-parent merges take max Z^δ — the mapping's "slope weight × persistence" is
  incomplete; (2) sub-threshold flux is redistributed, not dropped; (3) time policy is a
  one-shot traversal, not budget / converge; (4) the outputs are reductions over many
  independent per-source fronts, which `front` must support as a mode; (5) SC-ENERGY is
  also a cell layer in the SCIDDICA variant.

## 12. Complexity estimate

- **Implementation:** medium (per-source front with per-path sparse state, merge,
  redistribution rules).
- **Computation in the browser:** medium — runtime grows with spreading (low exp) and
  the number of release cells (1–16 s per scenario on 8 cores in the paper, §3.1; 3 h 45
  min for 57 000 start cells on 16 cores, §4.2); demos must limit release areas or
  prune overrun release cells.
- **Data preparation:** medium — release zones need a susceptibility rule or mapping.

## 13. Risks

- Scientific: data-based model, no physics of mass; parameters process- and
  resolution-dependent (exp and R_stop depend on DEM resolution, §3.4).
- Data: release zones and event inventories for CZ to be verified.
- Technical: path-wise traversal is CPU-bound; many release cells are slow.
- Communication: hazard maps from a demo are not official hazard zoning.

## 14. Open questions

- Q1: Eq. 8 sums over parents p and neighbours n; is P_i = Σ_p Z^δ_p · D_i(p) (one term
  per parent for direction i)? Implementation suggests yes.
- Q2: Flux cutoff — stop (paper) or redistribute (implementation)? Decide and document;
  conservation tests depend on it.
- Q3: Duplicate entries for already-processed cells in the implementation vs the paper's
  "a base cell cannot be a child" rule — which defines the reference behaviour?
- Q4: Pruning of release cells reached by earlier paths changes Z_sum and CC — keep
  (speed) or drop (exact counts)?
- Q5: Forest extension (`D'Amboise et al. 2021b`, not in references.bib): how α depends
  on forest structure and Z_max — `TODO(literature)`.
- Q6: SCIDDICA p_f is a height threshold, but the elimination step compares an angle.
- Q7: SCIDDICA time per step p_t not given; `digregorio1999empirical` (paywall) holds the
  full minimisation algorithm; `avolio2013sciddica` (SCIDDICA-SS3) not yet read.
- Q8: Release-zone (trigger) model for CZ debris flows / shallow landslides — threshold
  rules (Flow-R source criteria) or input only?

## 15. Literature and implementations

- **Primary reference:** `damboise2022flowpy` — complete, open, minimal-parameter runout
  model with geometric validation; A-class.
- **Supporting references:** `horton2013flowr` (Flow-R persistence tables, dh, Vmax,
  travel angles); `wichmann2017gpp` (random walk, friction models, rockfall / debris /
  avalanche parameter tables); `dambrosio2003simulating` (SCIDDICA, synchronous MoD
  variant, fitness indices); `digregorio1999empirical` (MoD theory, not read);
  `avolio2013sciddica` (later SCIDDICA, not read); `kronholm2005integrating` (avalanche
  release-zone CA, HAZ-03 idea); `tichavsky2026hydrogeomorphic` (CZ event context).
- **Benchmarks / reference data:** α-line on generic slopes (`damboise2022flowpy` §3);
  AvaFrame test topographies; SCIDDICA Sarno cases (no data locally).
- **Implementations:** Flow-Py v1.0 (Python, GPL-3.0, archived) — reference / oracle
  only; AvaFrame `com4FlowPy` (EUPL-1.2) — reference only; SAGA GPP (GPL) — reference /
  oracle only; Flow-R (free binary, closed) — oracle only; OpenCAL SCIDDICA-T (licence to
  be verified) — reference only.
- **Still missing:** `TODO(literature)` — D'Amboise et al. 2021 (forest extension,
  parameter sets); CZ event inventories; Gamma (2000) random walk (cited by GPP and
  Flow-R).

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| gravitational mass flow | gravitační svahový pohyb (proud) | phenomenon |
| runout | dosah (dojezd) | phenomenon / output |
| release (starting) zone | odtrhová (zdrojová) oblast | input |
| transit zone | tranzitní oblast | output |
| runout zone | oblast dojezdu (akumulace) | output |
| runout (travel) angle | úhel dosahu | parameter |
| energy line | energetická čára | concept |
| energy-line height | výška energetické čáry (nad terénem) | state variable |
| routing flux | směrovaný tok | state variable |
| divergence exponent | exponent rozbíhavosti | parameter |
| persistence | setrvačnost (perzistence) směru | parameter |
| flux cutoff | práh toku | parameter |
| process intensity | intenzita procesu | output |
| back-tracking | zpětné dohledání zdrojových oblastí | UI action |
| protective forest | ochranný les | UI action / class |
