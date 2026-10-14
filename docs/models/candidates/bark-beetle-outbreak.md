# Bark-beetle outbreak

| Field | Value |
|---|---|
| ID | `bark-beetle-outbreak` |
| Longlist ref. | `ECO-01` |
| Category | ecology (forest disturbance) |
| Group | core |
| Weighted score | 4.05 (revision 2) |
| Primary reference | `pietzsch2023nonparametric` (read in full) |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

The European spruce bark beetle (*Ips typographus*) breeds in weakened Norway spruce; in
warm, dry years and after windthrow its population explodes, mass attacks overcome the
defence of healthy trees and whole stands die within one or two seasons. Spread is mostly
short range (most new attacks within 100–500 m of last year's spots, `dolezal2016fine`
Discussion) with occasional longer flights (max. recorded 1094 m, `dolezal2016fine`
Results). Two or three generations per year depend on temperature. Scale: stands of
1–100 ha, landscapes of 10²–10⁴ km², yearly steps over 5–20 years. Demo questions: how
fast does an outbreak leave a national park, and how much sanitation felling is needed to
stop it? CZ relevance: the 2015–2022 outbreak (Šumava, Bohemian Switzerland, Vysočina).

## 2. Suitability for CA

Good: infestation spreads from cell to adjacent cell, susceptibility is a raster (spruce
share, age, attractiveness, drought), and outcomes are mapped yearly from satellites.
Limits: beetle dispersal has a fat tail that a Moore neighbourhood of 250 m cells cuts off
(`pietzsch2023nonparametric` Discussion); within-cell dynamics (beetle numbers, tree
defence) are hidden in transition tables; management and weather are scenario inputs, not
mechanisms.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `beetle.level` | categorical {0, ≤11, ≤36, ≤286 infested trees} + dead | infestation level per 250 m cell | dynamic |
| `stand.attract` | categorical, 3 classes of mean primary attractiveness | host susceptibility (kairomone-induced attractiveness) | dynamic (changes via table) |
| `stand.spruce` | categorical, 3 classes of spruce proportion (%) | host availability | dynamic |
| `stand.living` | integer ≥ 0 | living spruces in the cell (dieback extension) | dynamic |
| `beetle.class` | categorical, 36 combinations + dead | joint state used as LUT key | derived each step |
| `beetle.year` | integer | first year of infestation | output |
| `zone` | categorical {national park, outside} | reporting / management zone | static input |

## 4. Neighbourhood and time step

- **Grid:** square 250 × 250 m (`pietzsch2023nonparametric`, Data processing);
  the IBM inside each cell uses 5 m patches.
- **Neighbourhood:** Moore, 8 cells (implementation IPS-UPS, file `Upscaling.R`, neighbour
  rule section; the paper only says "direct neighborhood", Discussion).
- **Time step:** one year; the number of beetle generations per year g ∈ {2, 3} is a
  scenario parameter that scales the neighbour rule.
- **Update scheme:** synchronous (neighbour changes are collected in a copy and written
  after the sweep; `Upscaling.R`).
- **Boundary:** closed (no beetles enter from outside). The R code replaces a missing
  neighbour by cell 1, which is a quirk, not a stated policy (open question).

## 5. Transition rule

Restated from `pietzsch2023nonparametric` (Metamodel section, Figs. 4–5, Table 1), with
details from the implementation IPS-UPS (`Upscaling.R`, meta-model section). The
"metamodel" (MM) is a CA whose transition table was learned from an individual-based
model (IBM IPS-SPREADS) run on representative cells.

**Offline (table construction, not part of the demo run):** each cell is classified by
three features — mean primary attractiveness (3 classes), spruce proportion (3 classes)
and number of infested trees (4 levels) — giving 36 combinations. Representative cells of
each combination were simulated with the IBM for every scenario (g = 2 or 3 generations ×
sanitation felling 0–100 % in 10 % steps; 22 scenarios, 10 replicates). The frequency with
which a combination turned into another one gives, per scenario, a table
`T_s(c) = {(c'_k, π_k)}` with at most two destinations (paper, Table 1 caption; the code
supports three) and, for the dieback extension, the number of trees that died.

**Per year, for every cell (MM-N-C variant, the one used for forecasts):**

1. **Neighbour rule (N).** If the cell contains spruce and at least one Moore neighbour is
   at the top infestation level (≤ 286, "fully infested"), its own level rises by g levels,
   capped at the top: for g = 2, 0 → ≤36, ≤11 → top, ≤36 → top; for g = 3, any level →
   top (`Upscaling.R`; the paper says "one level for each beetle generation"). This rule is
   **deterministic** — the number of such neighbours does not matter beyond ≥ 1.
2. **Markov step.** The cell's combination c (after step 1) is looked up in the scenario
   table T_s; one uniform draw u selects destination k with cumulative probability
   (u ≤ π_1 → c'_1, else c'_2 …). All three features are replaced by those of c'_k.
3. **Dieback (C).** Living spruces decrease by the dead count of the chosen destination;
   if ≤ 0, the cell becomes **dead** (absorbing; all features set to a sentinel value 500
   in the code).
4. Repeat for 20 years; record the infestation level per year and the share of dead spruce.

Nothing is conserved (no beetle numbers). Susceptibility enters only through the LUT key
(attractiveness and spruce-share classes). Sanitation felling is **not** a cell operation:
it selects which table T_s is used, uniformly over the whole domain.

**Open questions:** (a) transitions of combinations never simulated (9 of 36 had no prior
infestation, Simulation experiments) — presumably identity; (b) whether the neighbour rule
uses neighbours' state before or after their own update (code: before — synchronous);
(c) boundary handling; (d) the paper's "one level per generation" vs. the code's jumps.

### 5.1 Variant: stochastic density CA on a hex grid (`liu2025multiscale`; not local, domain notes)

Hex cells hold normalised beetle density in [0, 1]. A Bernoulli draw, whose probability
grows with the density gradient and the number of affected neighbours, decides which cells
join a dispersal event; above-mean cells give a fraction γ1 of their excess, a fraction γ2
settles subject to a survival probability (φ, ρ); a microscale birth–death chain runs
within each step; absorbing boundary. Implementation MPB-Infestation (no licence).

### 5.2 Variant: data-driven susceptibility surface (`duraciova2020bark`, Šumava, CZ)

On 30 m cells, two logistic surfaces are fitted per year: spot initiation (NDVI, solar
radiation, age, density, wood volume) and spot spreading (the same plus the cost distance
from last year's spots, restricted to ≤ 228 m = √ of the largest spot area, 52,200 m²).
The attack-susceptibility map is the cell-wise MAX of both. The paper forecasts one year
only; iterating it (threshold or Bernoulli on the surface, then recompute distances) would
make a CA, but the conversion is not specified (open question).

### 5.3 Proposed generalisation for the shared engine (assumption, not from a reference)

To share SC-STOCH-SPREAD with HAZ-01: `P_i = 1 − Π_j (1 − s_i · k(d_ij) · I_j)` over
infested cells j within a radius, with s_i from a stand LUT and k a distance kernel fitted
to `dolezal2016fine` (ED50 ≈ 76–86 m, ED10 ≈ 432–555 m). Marked as an assumption; it would
need its own calibration (e.g. against `duraciova2020bark` AUC).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| cell size | L | m | 250 | `pietzsch2023nonparametric` Data processing | IBM patches 5 m (IBM section) |
| domain | – | cells / ha | 7524 cells, ≈ 14,100 ha forest; 2257 with spruce; 170 infested in 2015 | `pietzsch2023nonparametric` Data processing | Saxon Switzerland NP |
| feature classes | – | – | 3 × 3 × 4 = 36 combinations | `pietzsch2023nonparametric` Data processing, Table S1 | |
| infested-tree level bounds | – | trees | 0; ≤ 11; ≤ 36; ≤ 286 | impl. IPS-UPS, `Upscaling.R` (classification) | top level = 286 |
| attractiveness class bounds | – | abstract | ≤ 3.87; ≤ 4.59; ≤ 5.9 | impl. IPS-UPS, `Upscaling.R` | |
| spruce proportion bounds | – | % | ≤ 46; ≤ 66; ≤ 100 | impl. IPS-UPS, `Upscaling.R` | of 2500 patches per cell |
| generations per year | g | yr⁻¹ | 2 or 3 | `pietzsch2023nonparametric` Simulation experiments | climate scenario |
| sanitation felling intensity | – | % | 0–100, step 10 | `pietzsch2023nonparametric` Simulation experiments | selects table |
| swarming days per generation | – | d | 40 | `pietzsch2023nonparametric` Simulation experiments | IBM setting |
| IBM runs | – | – | 22 scenarios × 27 cells × 10 replicates = 5940 | `pietzsch2023nonparametric` Simulation experiments | |
| max destinations per combination | – | – | 2 (paper), 3 (code) | `pietzsch2023nonparametric` Table 1; impl. IPS-UPS `Upscaling.R` | |
| transition probabilities | π_k | – | per scenario table | impl. IPS-UPS, `data-sites/results-IPS-SPREADS.csv` | no licence → not redistributable |
| forecast horizon | – | yr | 20 | `pietzsch2023nonparametric` Long-term forecast | |
| effective felling threshold | – | % | ≥ 80 | `pietzsch2023nonparametric` Results | result, not input |
| Ips dispersal ED50 / ED10 (spring; summer) | – | m | 86 / 555; 76 / 432 | `dolezal2016fine` Table 1 | Šumava; abstract prints "55 m and 4 m" (typo?) |
| Ips dispersal fit parameters a, b (spring; summer) | a, b | – | 76.185, 0.1548; 85.597, 0.1658 | `dolezal2016fine` Table 1 | kernel form not legible in extracted text |
| max recorded flight | – | m | 1094 | `dolezal2016fine` Results | |
| spreading distance limit | – | m | 228 | `duraciova2020bark` Results | √52,200 m² |
| logistic coefficients | – | – | per year | `duraciova2020bark` Tabs. 3–4 | 30 m cells |
| IBM beetle traits (perceptual range, moving angle, energy, efficiency) | – | m, °, – | 15, ±45, 10, 20 | `kautz2016dispersal` Table 1 | background only |
| hex-CA parameters γ1, γ2, φ, ρ, C, N | – | – | 0.8, 0.8, 1/3, 1/3, 100, 100 | `liu2025multiscale` Table 2 (via `docs/research/domains/ecology.md`) | not read locally |
| generations from temperature | – | – | not given | `berec2013population` (not local) | PHENIPS, TODO(literature) |

## 6. Deterministic vs. stochastic

The Markov step is a categorical random draw per cell and year; the neighbour rule is
deterministic. The randomness summarises IBM variability (10 replicates). Ensembles
(≥ 100 runs) give infestation / dieback probability maps; a fixed seed is needed for
replay and for comparing felling scenarios on the same random stream.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| spruce proportion | raster, continuous → 3 classes | LUT key, living-tree count | required |
| primary attractiveness | raster, continuous → 3 classes (from tree height / age) | LUT key | required (or a proxy, open) |
| initial infestation | raster (count or level) | initial state | required |
| transition tables | table per scenario | rule | required |
| generations per year | scalar or raster | neighbour-rule step size, table choice | required |
| zones (NP / outside) | vector → raster | reporting, possible management map | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| spruce share, age | ÚHÚL forest maps / management plans; Copernicus HRL Forest Type | CZ / EU | to be verified (licence) |
| infestation / dieback | Sentinel-2 / Landsat disturbance maps; NP Šumava and NP České Švýcarsko infestation maps | EU / CZ | to be verified |
| temperature (generations) | ČHMÚ gridded data; E-OBS; ERA5-Land | CZ / EU | to be verified |
| DEM (solar radiation, variant 5.2) | ČÚZK DMR 4G / 5G | CZ | to be verified |
| protected-area zones | AOPK ČR / NP boundaries | CZ | to be verified |

## 9. Visualization

Yearly map of infestation levels and dead spruce over an orthophoto, a dieback-share chart
inside vs. outside the park, a probability map from the ensemble. Interactions: felling
intensity slider (0–100 %), 2 vs. 3 generations (climate), toggle the neighbour rule to
show why spread matters, click to seed an infestation (e.g. after windthrow, chain L3).

## 10. Validation options

Macro-averaged F1 of predicted vs. observed infestation levels per cell for 2017 and 2018
(`pietzsch2023nonparametric` Fig. 6: the neighbour rule raised agreement substantially).
CZ: compare yearly maps with Šumava spots and AUC 0.75–0.82 (`duraciova2020bark` Tab. 5).
Qualitative: dispersal distances from `dolezal2016fine`.

## 11. Links to other models

Inputs from ATM-04 drought / temperature (L2) and HAZ-04 windthrow (L3); output dead spruce
→ HAZ-01 fuel (L2, `kudlackova2024using`) and ECO-02 succession (L4). Shares the
contagion family with HAZ-01 and ECO-09. Shared: SC-GRID, SC-LUT, SC-RECLASS,
SC-STOCH-SPREAD (variant 5.3), SC-KERNEL / SC-LDD (5.3), SC-COST (5.2), SC-INTERV,
SC-BOUNDARY, SC-ARRIVAL, SC-ENSEMBLE, SC-METRICS, SC-RNG.

## 11a. Engine mapping

- **Init:** SC-RECLASS continuous stand layers → classes; encode the 36-class key;
  load the scenario table (SC-MARKOV).
- **Stages per year:**
  1. `stencil` Moore — neighbour rule: count neighbours at top level, bump own level by g
     (double-buffered `beetle.level`).
  2. `map` — Markov step: categorical draw from `T_s(class)` (one uniform per cell),
     write the three features and the dead count (SC-MARKOV).
  3. `map` — dieback: subtract dead trees, set the absorbing dead class.
  4. `reduce` — counts per level and dead share per zone (SC-ZONAL).
- **Time policy:** fixed, 1 year; g as a parameter.
- **Boundaries:** closed.
- **RNG:** one uniform per cell per year (keyed by run, year, cell).
- **Observers:** first-infestation year (SC-ARRIVAL), dead-share map, zonal series,
  ensemble probability (SC-ENSEMBLE).
- **Interventions:** felling intensity (switches table), generations per year, seed
  infestation; a spatial felling map would need a per-cell table index (not in the paper).
- **Model-specific:** the IBM-derived tables and the level-bump rule.
- **Corrections to `model-mapping.md`:** the primary rule is **not** a Bernoulli draw from
  a LUT indexed by the number of infested neighbours. It is a deterministic neighbour
  bump (threshold ≥ 1 top-level neighbour) followed by a **categorical Markov transition**
  over a joint class; felling is baked into the table (not a `map` removing cells); there
  is no `jump` in the primary model (only suggested in its Discussion). The Bernoulli /
  kernel form is our variant 5.3. Variant 5.2 needs `queue` (cost distance) every year.

## 12. Complexity estimate

- **Implementation:** low (one stencil + one table lookup).
- **Computation in the browser:** very low (10⁴–10⁵ cells, 20 steps); ensembles trivial.
- **Data preparation:** high — transition tables require an IBM or their own
  calibration; the published tables have no licence.

## 13. Risks

The tables are specific to Saxon Switzerland and to IPS-SPREADS assumptions; reusing them
elsewhere (Šumava) is a strong assumption. Deterministic one-cell-per-year spread is slow
compared with real outbreaks (authors' own Discussion). Licence of the IPS-UPS data.
Users may read the felling result (≥ 80 %) as management advice.

## 14. Open questions

- Can we use or regenerate the IPS-UPS transition tables (no licence)? Ask the authors or
  build our own table from a simpler model?
- Proxy for "primary attractiveness" from open data (tree age / height?).
- Unsimulated combinations, boundary handling, level-bump semantics (§5).
- `dolezal2016fine` kernel form (exponent not legible) and the abstract's distances.
- Iteration rule for the Duračiová surface (variant 5.2).
- Generations per year from temperature (`berec2013population` not local).

## 15. Literature and implementations

- **Primary reference:** `pietzsch2023nonparametric` — landscape CA with neighbour spread,
  management scenarios and a map-level validation, next to the CZ border.
- **Supporting references:** `liu2025multiscale` (stochastic density hex CA, not local);
  `kautz2016dispersal` (IBM background); `duraciova2020bark` (CZ data-driven model,
  validation target); `dolezal2016fine` (CZ dispersal kernel); `berec2013population`
  (CZ generations, not local); `kudlackova2024using` (fire chain L2).
- **Benchmarks / reference data:** IPS-UPS Kappa / F1 inputs and 20-year outputs
  (`data-plots/`) as an oracle for a reimplementation.
- **Implementations:** IPS-UPS (R + NetLogo, no licence) — reference / oracle only;
  MPB-Infestation (R, no licence) — reference only.
- **Still missing:** `TODO(literature)` PHENIPS equations (`berec2013population`); full
  text of `liu2025multiscale`; Cipriotti et al. 2016 metamodel template (not in
  references.bib).

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| bark-beetle outbreak | kůrovcová kalamita | phenomenon |
| infestation level | stupeň napadení | state variable |
| infested / dead spruce | napadený / odumřelý smrk | state variable |
| spruce proportion | podíl smrku | parameter |
| primary attractiveness | primární atraktivita (stromu) | parameter |
| beetle generations per year | počet generací za rok | parameter |
| sanitation felling | asanační těžba | UI action |
| transition table | tabulka přechodů | parameter |
| infestation spot | kůrovcové ohnisko | UI output |
| dieback share | podíl odumřelých stromů | UI output |
