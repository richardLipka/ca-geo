# Air pollutant and smoke dispersion

| Field | Value |
|---|---|
| ID | `pollutant-dispersion` |
| Longlist ref. | `ATM-01` |
| Category | atmosphere / air quality |
| Group | extension |
| Weighted score | 3.60 (revision 2) |
| Primary reference | `sonnenschein2025hybrid` |
| Status | draft |
| Last updated | 2026-10-14 |

## 1. Phenomenon

Pollutants emitted by traffic, chimneys or a fire are carried by wind and mixed by
turbulence, so concentration is highest next to the source and decays with distance, more
slowly downwind. Buildings and vegetation modify local ventilation. Scales: street to city
(10–100 m cells, hours) for traffic NO₂; landscape to region (100 m–1 km cells, hours to days)
for wildfire smoke. Demo questions: *how far does traffic NO₂ reach into a neighbourhood and
how does it change with wind? what happens if a street is closed? which towns does the smoke of
a forest fire reach?* (chain L11: wildfire → smoke → air quality).

## 2. Suitability for CA

Partly suitable. Transport and mixing are local exchanges between neighbouring cells, the
inputs are rasters (emissions, land cover, building morphology) and a CA runs fast enough for
interactive scenarios — the stated aim of the primary reference (domain notes: 0.48 s
runtime). Limits: real dispersion is 3-D advection–diffusion with a boundary layer,
stability classes and chemistry; the primary template is not a physical transport model but a
calibrated iterated smoothing (an empirical "hybrid" with land-use regression), so it gives
plausible patterns, not a conserved mass budget; long-range plume transport over hours needs a
transport scheme with memory (§5.B).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `conc` | f32 ≥ 0 | dispersed source-related concentration (traffic NO₂) | evolves within the hour |
| `emission` | f32 ≥ 0 | on-road (source) concentration for the hour | forcing (per hour) |
| `isSource` | u8 {0, 1} | cell is an on-road / source cell | static input |
| `baseline` | f32 ≥ 0 | background concentration from land-use regression | static input |
| `adjuster` | f32 | morphology factor (green, open space, trees, building height, height difference) | static derived |
| `out` | f32 ≥ 0 | final estimate = scaled dispersed part + scaled baseline | output |
| `smoke` (variant B) | f32 ≥ 0 | smoke mass per cell | evolves |

## 4. Neighbourhood and time step

- **Grid:** square, 50 m in the example workflow (implementation CellAutDisp, file
  `ExampleApplications/01DataPreparationExample.py`, `cellsize = "50m"`, 25 m also prepared).
- **Neighbourhood:** n × n window, n odd; 3 × 3 in the example calibration (implementation
  CellAutDisp, `ExampleApplications/02CalibrationExample.py`); matrix size is one of the tested
  settings ("meteomatrixsizerepeats" calibration step, README). Weights depend on distance and
  on the angle between the neighbour offset and the wind direction.
- **Time step:** the forcing step is one hour (hourly traffic emissions); meteorology enters as
  monthly values (one weight matrix per month). Inside an hour the filter is iterated
  `k` times; `k` has no physical duration — it acts as a calibrated range parameter.
- **Update scheme:** synchronous (whole-raster focal operation each iteration).
- **Boundary conditions:** whatever the focal library (`xrspatial.focal.apply`) does at the
  raster edge — not checked → open question; for the demo use `closed` (renormalise over
  in-domain neighbours, which the weighted average does naturally).

## 5. Transition rule

### 5.A Hybrid CA (primary `sonnenschein2025hybrid`)

The paper is not local (`literature/manifest.md`: failed, ScienceDirect bot check); the rule is
taken from the authors' code (implementation CellAutDisp, GPL-3.0 → reference only; facts
only, files `create_weighted_matrix.py`, `cellautom_dispersion.py`, `meteorepeats.py`,
`provide_adjuster.py`, `calibration.py`) and the domain notes. Whether the paper's final model
uses exactly these code paths is an open question.

**Weight matrix** (per month, from monthly meteorology: temperature T, rain R, wind speed u,
wind direction φ; parameters p₀…p₈):
1. Base weight `W = max(0, p₀ + p₁·T + p₂·R + p₃·u)` (optionally with log of T, R, u).
2. Disparity factor `F = p₄ + p₅·u`.
3. For each offset (i, j) in the window: Euclidean distance `d` in cells and direction angle
   `ψ` (0° = towards the top row, clockwise); angular difference `θ = min(|ψ − φ|, 360° − |ψ − φ|)`.
4. `w(i, j) = W · (p₆ / (d + 0.01) + p₇ / (θ + 1))`, then multiplied by `F` if `θ ≤ 90°`
   ("windward") or divided by `F` otherwise ("leeward").
5. Centre weight ("inertia") `w(0, 0) = p₈ / F` — more wind, less inertia.
A "flexible" variant uses `W = p₀ + p₁·u + Σ pₖ·xₖ` with any extra meteorological factors xₖ.

**Per hour:**
1. Initialise `conc` from the hour's traffic layer (source cells carry emission values, others 0).
   The field does **not** carry over from the previous hour.
2. Repeat `k` times: (a) reset source cells to their emission values; (b) replace every cell
   by the weighted average `Σ w·conc / Σ w` over its window (rounded to 10⁻¹⁰);
   (c) optional "iter" mode: multiply by `(1 + adjuster)` each iteration.
3. Optional "end" mode: apply `(1 + adjuster)` once after the loop.
4. Optional scaling: multiply source cells by `s_on`, other cells by `s_off`.
5. Output `out = conc + s_b · baseline`.

**Repeats:** either a calibrated integer or `k = ⌊a + b·u⌋` (`meteorepeats.py`).
**Morphology adjuster:** `adj = m₀ + Σ mᵢ·featureᵢ`, clipped to `[min, max]`
(`provide_adjuster.py`; features: green cover, open-space fraction, number of trees, building
height, height difference to neighbours).

**Conserved:** nothing. The weighted average is a normalised smoothing with Dirichlet-like
source cells; total mass changes with `k`, the adjuster and the scaling. Its fixed point (large
`k`) is a weighted-harmonic field between sources.

**Ambiguities:** wind-direction convention (meteorological "from" vs "to") — with "from",
upwind neighbours receive the windward weight, which transports pollution downwind; the angle
origin (`arctan2(col offset, −row offset)`) assumes north-up rasters; whether the distance term
`1 / (d + 0.01)` makes the centre-excluded kernel strongly dominated by the nearest ring.

### 5.B Smoke-transport variant (for chain L11) — no verified template yet

The hourly reset of 5.A cannot move a plume over several hours. For wildfire smoke a
conservative scheme is proposed: each step, every cell sends mass downwind with a donor-cell
(upwind) advection fraction `u·Δt/Δx` split over the two downwind faces, plus a diffusive
exchange `D·Δt/Δx²` with all four neighbours, minus first-order decay / deposition; sources add
emission from burning cells of HAZ-01. Candidate templates in `references.bib`, not read:
`wang2023novel` (CA advection–diffusion–decay of solutes), `milasinovic2019coupled` (CA
advection–dispersion in groundwater), `guariso1992air` (early CA air quality, paywalled).
All coefficients → `TODO(literature)`.

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Repeats (fixed) | k | – | 2–36 (GA bounds) | implementation CellAutDisp, `calibration.py` generateparambounds | calibrated value not seen |
| Base-weight intercept | p₀ | – | 0–1 | same | |
| Temperature / rain / wind-speed coefficients | p₁, p₂, p₃ | – | −1 … 2 each | same | |
| Disparity intercept / wind-speed coefficient | p₄, p₅ | – | 0–3 / 0–2 | same | |
| Distance / alignment coefficients | p₆, p₇ | – | 0–2 each | same | |
| Inertia | p₈ | – | 0–9 | same | |
| Repeats from wind | a, b | –, s m⁻¹ | 1–12, 0–1 | same ("meteonrrepeat") | |
| Morphology adjuster coefficients | m₀…m₅ | – | m₀ −2…2, green −1…1, open space −5…2, trees −1…1, building height −1…1, neighbour height diff. −1…1 | same ("morph") | |
| Adjuster limits | max, min | – | 3–20, −1–0 | same | |
| Scaling (baseline, on-road, off-road) | s_b, s_on, s_off | – | 0.1–2 each | same ("scaling") | |
| Window size | n | cells | 3 in the example | implementation CellAutDisp, `02CalibrationExample.py` | other sizes tested in the paper (not seen) |
| Cell size | Δx | m | 50 (25 prepared) | implementation CellAutDisp, `01DataPreparationExample.py` | |
| GA settings (example) | – | – | population 30, stop after 5 non-improving iterations, seed 42 | `02CalibrationExample.py` | marked "set low for initial testing" |
| Fitted parameter values | – | – | not given | `sonnenschein2025hybrid` (full text not read) | open question |
| Smoke variant coefficients | u, D, λ, emission factor | – | not given | – | `TODO(literature)` |

## 6. Deterministic vs. stochastic

5.A and 5.B are deterministic. Randomness appears only in calibration (genetic algorithm) and,
for smoke, through the stochastic fire model upstream; a smoke ensemble would follow from a
HAZ-01 ensemble (exposure probability). Fixed seeds only for the GA.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| Source emissions (traffic NO₂ per road cell and hour) | raster / vector → raster, time series | fixed source values | required |
| Background (land-use regression) concentration | raster, continuous | added baseline | required for 5.A |
| Meteorology (T, rain, wind speed, direction) | scalar time series | weight matrix, repeats | required |
| Morphology (green, open space, trees, building heights) | rasters | adjuster | optional |
| Monitoring observations | points, time series | calibration / validation | required for calibration |
| Burning cells / fire intensity (HAZ-01) | raster time series | smoke sources (5.B) | required for L11 |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| Air-quality observations | ČHMÚ ISKO station data; EEA Air Quality e-reporting | CZ / EU | to be verified |
| Meteorology | ČHMÚ station data; ERA5 reanalysis (wind, T, precipitation) | CZ / global | to be verified (licence of ČHMÚ data) |
| Traffic intensity | ŘSD national traffic census (Celostátní sčítání dopravy); city traffic models | CZ | to be verified |
| Emission inventory | ČHMÚ REZZO; CAMS emission inventories | CZ / EU | to be verified |
| Background concentration | CAMS regional air-quality reanalysis; ČHMÚ annual maps | EU / CZ | to be verified |
| Building heights, green | Urban Atlas Building Height; Copernicus HRL Tree Cover; city open data (Praha IPR) | EU / city | to be verified |
| Smoke reference | CAMS / Sentinel-5P aerosol products for a known fire (e.g. Bohemian Switzerland 2022) | EU | to be verified |

## 9. Visualization

Concentration heat map over the city basemap with a wind arrow; animation of the iterations
(dispersion "spreading" from roads) and of hourly maps over a day; the kernel weight matrix as
a small glyph that rotates with wind; scenario comparison (difference map) for traffic changes
(street closure, −30 % traffic) and wind; for smoke: plume animation downwind of the fire with
exposure time per town. Explicit "illustrative, not a forecast" label.

## 10. Validation options

- Correlation and errors against monitoring stations and mobile measurements: R², MSE, MAE,
  ME, RMSE (implementation CellAutDisp, `performance_metrics.py`); paper reports external R²
  0.60 and 0.57 for a lockdown scenario (domain notes; full text not read).
- Analytical check for 5.B: Gaussian puff (advection + isotropic diffusion) and mass balance.
- Smoke: qualitative comparison with satellite aerosol maps — only qualitative is realistic.

## 11. Links to other models

- L11: HAZ-01 wildfire → smoke sources (burning cells, intensity) → 5.B.
- ATM-03 heavy gas: WAT gravity flow + this model's dilution step.
- LND-01 / traffic scenarios could change emission rasters (long chain, optional).

## 11a. Engine mapping

**Variant A (CellAutDisp-like), per forcing hour:**
1. Controller (start of hour / month): rebuild the weight table when meteorology changes;
   compute `k` from wind speed.
2. `map` initialise `conc` from the hour's emission layer.
3. Inner loop ×k: `map` reset source cells (better: BoundaryPolicy `fixed(layer)` on marked
   cells); `stencil` n × n normalised weighted average with direction weights (SC-DIRWEIGHT,
   SC-KERNEL); optional `map` adjuster.
4. `map` scaling + baseline → `out`.
- Time policy: fixed 1 h with an inner fixed-count loop whose count comes from forcing — the
  current TimePolicy has no nested iteration (finding). RNG: none. Observers: hourly `out`,
  daily mean, values at station points. Interventions: change traffic on a road segment, change
  wind, add green (adjuster).

**Variant B (smoke):** `map` add emission from HAZ-01 burning cells; `flux` upwind advection +
diffusion (exact mass conservation, SC-OUTFLOW machinery, boundary `open` with outflow
recorded); `map` decay; `reduce` total mass (SC-MASS) and max velocity for an adaptive Δt
(SC-ADT, CFL `u·Δt/Δx ≤ 1`). Wind as global vector or raster Forcing.

**Shared components:** SC-GRID, SC-KERNEL, SC-DIRWEIGHT, SC-SRC, SC-BOUNDARY, SC-OUTFLOW (B),
SC-ADT (B), SC-MASS (B), SC-ENVELOPE (max concentration), SC-ARRIVAL (smoke arrival), SC-METRICS
(R², RMSE), SC-CALIB (GA), SC-ENSEMBLE (exposure probability from fire ensembles), SC-INTERV;
proposed new: SC-REPEAT, SC-POINTOBS (station sampling).

**Model-specific:** the CellAutDisp weight formula, windward / leeward disparity, morphology
adjuster, hourly reset.

**Corrections to `model-mapping.md` (ATM-01):** (1) the iteration count per hour is not fixed —
it may depend on wind speed; (2) the field is reset each hour (no memory), so the mapping should
say so and the smoke chain L11 needs the conservative `flux` variant B, not the focal average;
(3) direction weights depend on distance *and* angle jointly and include a centre (inertia)
weight — the `directional.weight(cosAngle, magnitude)` signature lacks distance and centre
handling; (4) the stencil is a normalised weighted average (division by Σw over valid
neighbours), which should be a stencil option.

## 12. Complexity estimate

- **Implementation:** low for 5.A (one stencil + maps); medium for 5.B (flux, CFL).
- **Computation in the browser:** low — 3 × 3 to ~11 × 11 kernel, ≤ 36 iterations per hour on
  ≤ 10⁶ cells; a day = 24 hours. Calibration (GA over months × hours) offline.
- **Data preparation:** high for traffic NO₂ (hourly emissions, LUR baseline, morphology) — the
  inputs are case-specific; low for an illustrative smoke demo.

## 13. Risks

Health-related topic: results can be mistaken for official air-quality information (strong
disclaimer, no named-street "exposure" claims). The model is empirical and calibrated to
Amsterdam; transfer to CZ needs re-calibration with station data. No mass conservation in 5.A.
Licence: CellAutDisp is GPL-3.0 — clean-room reimplementation from this card only. Smoke
variant has no verified template yet.

## 14. Open questions

- Fitted parameter values, chosen window size and repeats in `sonnenschein2025hybrid` (full
  text needed; manual download).
- Wind-direction convention and raster orientation assumed by the weight matrix.
- Edge handling of the focal operation (NaN padding vs shrinking window).
- Which code path (dummy / adjust / adjust_iter / scaled) is the paper's final model?
- Is the hourly reset intended for all uses, or only because traffic emissions dominate locally?
- Smoke variant: which verified CA template (read `wang2023novel`), emission factors for fire
  smoke, vertical mixing — or keep it explicitly illustrative?
- Is ATM-01 demo the traffic NO₂ case (needs case-specific data) or the smoke case (needs a
  different rule)? (Ask the user — scope decision.)

## 15. Literature and implementations

- **Primary reference:** `sonnenschein2025hybrid` — only modern CA dispersion model with open
  code and validation (not local; rule from code).
- **Supporting references:** `wang2023novel`, `milasinovic2019coupled` (conservative CA
  transport, candidates for 5.B; not read); `guariso1992air` (early air-quality CA; paywalled);
  `lauret2016atmospheric` (ANN-based CA, context for ATM-03).
- **Benchmarks / reference data:** CellAutDisp `tests/` (4 files, data not included);
  analytical Gaussian puff for 5.B (to be added).
- **Implementations:** CellAutDisp (`external/CellAutDisp`, Python, GPL-3.0 → reference only,
  may be run as an oracle on our own inputs).
- **Still missing:** `TODO(literature)` full text of `sonnenschein2025hybrid`; a verified CA
  for smoke / plume transport at landscape scale; keywords: "cellular automata smoke
  dispersion wildfire", "cellular automata advection diffusion atmosphere".

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| air pollutant dispersion | rozptyl znečišťujících látek | phenomenon |
| smoke plume | kouřová vlečka | phenomenon |
| concentration | koncentrace | state variable |
| emission source | zdroj emisí | input |
| background (baseline) concentration | pozaďová koncentrace | input |
| land-use regression | regresní model využití území (LUR) | method |
| weight matrix (kernel) | váhová matice (jádro) | parameter |
| windward / leeward | návětrný / závětrný | parameter |
| disparity factor | faktor nerovnoměrnosti | parameter |
| inertia weight | váha setrvačnosti | parameter |
| number of iterations | počet iterací | parameter |
| morphology adjuster | morfologická korekce | parameter |
| advection | advekce | process |
| deposition / decay | depozice / rozpad | process |
| monitoring station | monitorovací stanice | validation |
| exposure | expozice | UI output |
