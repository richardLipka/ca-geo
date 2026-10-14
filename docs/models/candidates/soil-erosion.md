# Soil erosion, sediment transport and muddy floods

| Field | Value |
|---|---|
| ID | `soil-erosion` |
| Longlist ref. | `HYD-05` |
| Category | hydrology, geomorphology, agriculture |
| Group | extension |
| Weighted score | 3.70 (revision 2, `docs/review/evaluation-matrix.md`) |
| Primary reference | `landa2019smoderp2d` (SMODERP2D, CZ) |
| Status | draft |
| Last updated | 2026-10-14 |

**Source note.** `landa2019smoderp2d` (local, read in full) describes the **runoff part**
of SMODERP2D (mass balance, sheet and rill flow, Philip infiltration, CFL) but gives **no
sediment detachment / transport equations**. The SMODERP2D code (`external/smoderp2d`,
GPL-3.0 → reference only) was read for facts: it computes erosion **indicators** (maximum
shear stress and velocity vs critical values), not a sediment mass balance. A
transport-capacity sediment rule is available only from the supporting RillGrow paper
(`eltner2025using`, local, read; equations are in its Supplement S1–S14, **not local**).

## 1. Phenomenon

Intense rain on bare or row-crop fields exceeds infiltration; runoff concentrates,
detaches soil, cuts rills and carries sediment downslope, where it deposits on roads, in
villages and ponds ("muddy floods"). Field to small-catchment scale (0.1–10 km²), one storm
event (minutes to hours). User questions: *where does the field erode, where does mud
end up, what does a grass strip, a different crop or a smaller field change?*

## 2. Suitability for CA

Good. Runoff routing and sediment exchange are local (D8 / von Neumann), driven by raster
inputs (DEM, soil, land use). RillGrow is explicitly a CA (`eltner2025using` §1, §2.3);
SMODERP2D is a cell-by-cell mass balance on a raster (`landa2019smoderp2d` §2.1).
Limits: rill geometry is sub-grid at field resolution (SMODERP2D treats rills as a
parameterised channel inside the cell); physically correct rill initiation needs cm cells
and Δt of hundredths of a second (RillGrow, plot scale only); sediment physics depends on
many empirical parameters.

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `dem` z | real (m) | terrain; dynamic if erosion changes it | static or dynamic |
| `soilveg` | categorical + LUT | soil × vegetation class → parameters (k, s, X, Y, b, n_rill, τ_c, v_c, retention, interception) | static |
| `water.depth` h | real ≥ 0 (m) | total surface water (from WAT or own routing) | dynamic |
| `water.hSheet`, `water.hRill` | real ≥ 0 (m) | split of h into sheet and rill parts | dynamic |
| `rill.state` | categorical {0 sheet, 1 rill growing, 2 rill receding} | rill regime | dynamic |
| `rill.hMax` | real (m) | depth when state 1 ended (code: `h_last_state1`) | dynamic |
| `infil.cum` | real (m) | cumulative infiltration (time since ponding for Philip) | dynamic |
| `erosion.tauMax`, `erosion.vMax` | real | max shear stress / velocity (indicator) | output |
| `sediment.c` or `sediment.load` | real ≥ 0 (kg m⁻² or kg) | suspended load per cell (RillGrow-type variant) | dynamic |
| `erosion.dz` | real (m) | cumulative elevation change | output |

## 4. Neighbourhood and time step

- **Grid:** square; 1–10 m for fields / small catchments (SMODERP2D); 1–3 cm for plots
  (RillGrow, `eltner2025using` §2.2: 3 cm field, 1.5 cm lab DEMs).
- **Neighbourhood:** D8 single direction (`landa2019smoderp2d` Eq. 2); the code also has
  MFD for sheet flow with D8 for rills (implementation SMODERP2D, `core/flow.py`).
  RillGrow: D8 steepest (`eltner2025using` §2.3).
- **Time step:** adaptive CFL (`landa2019smoderp2d` Eq. 4); RillGrow Courant from the
  previous step's maximum speed, hundredths of a second (§2.3).
- **Update scheme:** synchronous explicit (SMODERP2D also has an implicit variant —
  implementation SMODERP2D, `time_step.py`; not used here).
- **Boundaries:** open outlet edge (water and sediment leave, recorded); closed elsewhere
  if the domain is a catchment.

## 5. Transition rule

### 5.1 SMODERP2D (primary, `landa2019smoderp2d` §2.1)

1. **Mass balance per cell** (Eq. 1–3): Δh/Δt = inflow − outflow, inflow = effective
   rain e_s + Σ inflows q_j from upslope D8 donors, outflow = infiltration + own outflow +
   surface retention. (The paper writes "Outflow = inf − q − ret"; sign convention in
   Eq. 3 is ambiguous → open question.)
2. **Effective rain** e_s = rain minus interception on vegetation (§2.1; interception
   formula not given; code uses LUT fields `pi`, `ppl` — meaning not documented in the
   paper → open question).
3. **Infiltration** (Philip, Eq. 8): f(t) = ½ S t^(−½) + K_s, with sorptivity S and
   saturated conductivity K_s per soil class. Sheet flow starts when rain exceeds
   infiltration (§2.1). Definition of t (time since start or since ponding) → open.
4. **Surface retention** `ret` per class is filled before runoff (code field `ret`; unit
   not given in the paper → open).
5. **Sheet flow** (Eq. 5): q_sh = X · I^Y · h_sh^b per unit width (I = slope). In the code
   the coefficient is a = I^Y / n_sheet, i.e. X = 1/n_sheet (implementation SMODERP2D,
   `providers/base/data_preparation.py`); outflow volume per step = q_sh · Δt · Δx
   (`core/surface.py`).
6. **Rill flow** (Eq. 6): Manning q_rl = (A/n) R^(2/3) I^(1/2) for the part of h above the
   critical sheet depth h_crit; total q = q_sh + q_rl (Eq. 7, printed as "q_rl + q_rl" —
   typo).
7. **Critical depth** (paper: from critical shear stress, qualitative). Code: h_crit =
   min( τ_c / (γ I), (v_c / a)^(1/(b−1)), (τ_c v_c / (γ I a))^(1/b) ) with γ = 9807 N m⁻³,
   i.e. the sheet depth at which shear stress, velocity or stream power reaches its
   critical value (implementation SMODERP2D, `data_preparation.py`). Zero slope → large
   h_crit (sheet only).
8. **Rill regime** (code `core/surface.py`): state 0 → 1 when h > h_crit; in state 1 the
   sheet part is min(h, h_crit) and the rill part the rest; 1 → 2 when h starts to fall
   (h at that moment stored); 2 → 1 when h exceeds the stored value again. The paper
   only states that rills appear above h_crit.
9. **Time step** (Eq. 4): Courant number q·Δt/Δx < 1. Code: target band [0.85·0.95, 0.95]
   with coefficient 0.5601 on the velocity; if the maximum Courant number leaves the band,
   Δt = Δx_eff · 0.95 · 0.5601 / v_max and **the step is repeated**; Δt is also cut so
   that whole minutes are hit (implementation SMODERP2D, `courant.py`, `runoff.py`).
10. **Erosion indicators** (code `core/cumulative_max.py`): per cell maximum sheet shear
    stress τ = γ · h_sh · I and maximum velocity over the event; comparison with τ_c, v_c
    marks erosion-prone cells. No detachment, transport or deposition is computed.

Conserved: water volume (explicit D8 exchange limited by available sheet / rill water).
Sediment: not modelled in the primary reference.

### 5.2 Variant — RillGrow sediment CA (`eltner2025using` §2.3)

- Rain falls as individual drops at random cells (count per step from mean and SD of
  intensity; drop volume from diameter mean / SD). Optional explicit Green–Ampt
  infiltration.
- Flow moves to the steepest D8 neighbour until it leaves the grid or ponds; ponded depth
  rises until overtopping. Speed by a Manning-type or Darcy–Weisbach law; a maximum flow
  speed caps cell-to-cell runoff.
- Each wet cell carries the sediment load received from upslope. Transport capacity from
  Nearing et al. 1997 (Eq. 5 there; not in references.bib). Load > capacity → deposit a
  linear function of the excess (Lei et al. 1998, Eq. 12; not in bib). Load < capacity →
  **probabilistic** flow detachment (Nearing 1991; not in bib).
- Splash redistribution as diffusion (Planchon et al. 2000; not in bib) with a
  depth-dependent splash efficiency; slumping of saturated cells above a shear-stress
  threshold and toppling above a gradient threshold, both down to an angle of rest.
- Three size fractions, erodible layers over a basement; Δt from the previous maximum
  speed (Courant).
- All equations are in Supplement S1–S14 → `TODO(literature)`; values of the 7 calibrated
  parameters are shown only graphically (Fig. 9) → not given.

### 5.3 Proposed ca-geo composition (assumption, to be decided)

Submodel of WAT in one simulation (R9.2): WAT (or the SMODERP-style sheet/rill routing)
provides h and edge outflows each step; the erosion submodel (a) always computes the
τ / v indicators, and (b) optionally carries sediment along the **same water outflows**
(sediment flux = outflow × concentration) with a capacity-limited detachment / deposition
`map`, updating `dem` and triggering slope recomputation every N steps. Variant (b) needs
the RillGrow / transport-capacity equations first.

## 5a. Parameters

Values below are **test configurations** of the SMODERP2D code, not calibrated
recommendations; units are not documented in the paper (open question).

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Saturated conductivity | K_s (`k`) | m s⁻¹ (assumed) | 1.26e-7 (class CAZP); 1.39e-6 (HXGEO); 3.67e-6 (PXOP) | implementation SMODERP2D, `tests/data/rain_sim/soil_veg_tab.csv`, `tests/data/profile1d/data1D_soil_types.csv` | |
| Sorptivity | S (`s`) | m s⁻¹ᐟ² (assumed) | 1.25e-4; 3.10e-4; 7.75e-5 | same files | |
| Sheet-flow exponent | b | – | 1.5847; 1.5847; 1.7925 | same files | |
| Sheet-flow coefficient | n_sheet (X = 1/n_sheet) | – | 0.0073; 0.12; 0.035 | same files | |
| Slope exponent | Y (`y`) | – | 0.4889; 0.4889; 0.4622 | same files | |
| Rill Manning | n_rill | s m⁻¹ᐟ³ | 0.0035; 0.035; 0.035 | same files | 0.0035 looks implausibly low → check |
| Critical shear stress | τ_c | Pa | 100; 60; 10.66 | same files | |
| Critical velocity | v_c | m s⁻¹ | 0.28; 1.0; 0.245 | same files | |
| Surface retention | ret | mm (assumed) | 0; 8; 5 | same files | |
| Interception fields | pi, ppl | – | 0; 1.0 / 0.4; 0.16 / 0.13 | same files | meaning to be verified |
| Specific weight of water | γ | N m⁻³ | 9807 | implementation SMODERP2D, `data_preparation.py` | |
| Courant target / coefficient | – | – | 0.95 / 0.5601; lower band 0.85 × 0.95 | implementation SMODERP2D, `courant.py` | |
| Philip, sheet, rill equations | – | – | Eqs. 5, 6, 8 | `landa2019smoderp2d` §2.1 | |
| RillGrow calibrated parameters | – | – | base level, splash N, max flow speed, detachment K, shear-stress radius, slump threshold, angle of rest | `eltner2025using` §2.4 | values not given (Fig. 9) |
| Rainfall-simulator plots | – | – | field 2 × 8 m, 9 %, 90 min; lab 1 × 4 m, 40 %, 30 min | `eltner2025using` Table 1 | PDF table extraction garbled → verify; intensities not read reliably |

## 6. Deterministic vs. stochastic

SMODERP2D: deterministic. RillGrow: stochastic raindrop positions and probabilistic
detachment → seeded RNG (SC-RNG), ensembles for rill-pattern variability. The ca-geo
indicator variant is deterministic; a sediment variant with probabilistic detachment
would need per-cell keyed draws.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| DEM | raster, continuous | routing, slope | required |
| Soil type | raster / vector, categorical | K_s, S, τ_c, v_c via LUT | required |
| Land use / crop | raster / vector, categorical | X, Y, b, n, retention, interception via LUT | required |
| Field blocks | vector | field layout, grass strips (interventions) | optional |
| Rainfall | scalar series (event hyetograph) | forcing | required |
| Stream network | vector | outlet / stream routing (SMODERP2D 1D reaches) | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| DEM | ČÚZK DMR 5G | CZ | to be verified |
| Soils | VÚMOP BPEJ, soil maps; ESDAC soil erodibility | CZ / EU | to be verified |
| Field blocks, crops | LPIS (eAGRI) | CZ | to be verified (licence, update) |
| Erosion events | VÚMOP erosion-event monitoring | CZ | to be verified |
| Rain | ČHMÚ gauge / radar | CZ | to be verified |
| Parameter tables | SMODERP2D parameter database (ČVUT) | CZ | to be verified (licence) |

## 9. Visualization

Animated runoff depth with rill cells highlighted; map of maximum shear stress relative to
τ_c (red = erosion-prone); in the sediment variant, erosion (red) / deposition (blue)
dz map and sediment yield chart at the outlet. Interactions: change crop on a field
block, draw a grass buffer strip, split a large field, change storm intensity; compare
scenarios side by side. Chain L1: burnt slope (HAZ-01) → higher runoff and erosion.

## 10. Validation options

SMODERP2D regression outputs (Nučice catchment, rain simulator, 1D profile; implementation
`tests/data/reference`) as an oracle for the runoff part. RillGrow / Eltner plot data
(OPARA 10.25532/OPARA-602, not downloaded): DoDs and sediment yield time series for
plot-scale checks. Qualitative: VÚMOP erosion-event records (to be verified).

## 11. Links to other models

Submodel of WAT (reads depth and outflows, R9.2); consumer of HAZ-01 (chain L1) and
LND-01 (land-use change). Produces sediment input for ponds (HYD-04 siltation, not
modelled). Shares the `flux` machinery (sediment carried by water outflows).

## 11a. Engine mapping

- **Stages per step (indicator variant, SMODERP-style routing):**
  1. `map` effective rain, interception, retention, Philip infiltration (cumulative
     layer for t).
  2. `map` split h into sheet / rill parts and update `rill.state` (state machine).
  3. `flux` (a) D8 (or MFD) outflow pass → slot layer `water.out` (sheet q_sh and rill
     q_rl volumes, limited by available water); (b) gather → `water.depth`.
  4. `map` τ = γ h_sh I, v; max into `erosion.tauMax`, `erosion.vMax` (SC-ENVELOPE).
  5. `reduce` max Courant number → Δt (with retry).
- **Sediment variant:** additional `flux` reusing the water outflow slot layer (sediment
  out = water out × concentration), `map` detachment / deposition (capacity-limited,
  optional RNG), `map` dz update of `dem`, derived-layer recomputation of slope every N
  steps.
- **Time policy:** `adaptive` (shared with WAT). SMODERP2D needs **step rejection and
  retry** when the Courant number leaves the band, and snapping to whole minutes.
- **Boundaries:** `open` at outlet edges (water + sediment recorded), `closed` elsewhere.
- **RNG:** none (indicator); keyed per cell / step for RillGrow-type detachment and drops.
- **Observers:** envelope (τ_max, v_max), outlet hydrograph and sedigraph, mass balance
  of water and sediment, dz map.
- **Interventions:** change LUT class in a field polygon (crop), paint buffer strip,
  rain change.
- **Shared components:** SC-GRID, SC-LUT, SC-RECLASS, SC-SLOPE, SC-D8, SC-SLOT, SC-OUTFLOW,
  SC-ADT, SC-SRC, SC-BOUNDARY, SC-ENVELOPE, SC-MASS, SC-INTERV, SC-RNG (variant), SC-CALIB
  (RillGrow used Latin hypercube, `eltner2025using` §2.4), SC-METRICS.
- **Model-specific:** sheet / rill split with h_crit, rill state machine, Philip
  infiltration, transport-capacity sediment rule.
- **Corrections to `model-mapping.md`:** (1) the primary reference provides no sediment
  transport; "detachment / deposition from transport capacity" comes only from RillGrow
  (Supplement not local). (2) SMODERP2D routing is D8 / MFD (slot layer), unlike WCA2D
  (face) — the erosion submodel must be able to read whichever outflow layer the water
  submodel exposes. (3) Time policy needs retry, not only a pre-step Δt.

## 12. Complexity estimate

- **Implementation:** medium (indicator) / high (sediment variant with fractions, splash,
  slumping).
- **Computation:** medium at field scale (10⁵–10⁶ cells, CFL-limited steps); RillGrow scale
  is high (cm cells, 0.01 s steps), plot-sized only.
- **Data preparation:** medium — soil × land-use LUT, LPIS field blocks.

## 13. Risks

Scientific: erosion rates are highly parameter-dependent and equifinal (`eltner2025using`
§3.1: parameters do not cluster); indicator maps may be read as soil-loss predictions.
Data: CZ parameter database licence unknown. Technical: rill Courant numbers force tiny Δt
for the whole grid (`landa2019smoderp2d` §1). Communication: show as "erosion risk", not
tonnes per hectare.

## 14. Open questions

- Indicator-only (fully supported) or full sediment transport (needs RillGrow Supplement
  S1–S14 or another verified source)?
- Units and meaning of the SMODERP2D LUT fields (`pi`, `ppl`, `ret`, `nsheet`) and the
  sign convention of Eq. 3; Philip t definition.
- Rill geometry (width, cross-section) used in Eq. 6.
- Reuse WAT's WCA2D routing or SMODERP-style D8 sheet/rill routing for this scenario?
- Licence of the SMODERP2D parameter database.

## 15. Literature and implementations

- **Primary reference:** `landa2019smoderp2d` — Czech, open paper and code, runoff and rill
  hydrology with erosion thresholds.
- **Supporting:** `eltner2025using` (RillGrow CA, CTU rainfall-simulator data, LHS
  calibration); `favismortlock1998selforganizing` (RillGrow origin, not local);
  `coulthard2013integrating` (CAESAR-Lisflood, not local); `hobley2017creative`
  (Landlab, local, not read for this card); `heung2013modelling` (USLE + CA, not read).
- **Benchmarks:** SMODERP2D regression data; Eltner OPARA dataset (not downloaded).
- **Implementations:** SMODERP2D (GPL-3.0 → reference / oracle); RillGrow (no licence on
  GitHub, Zenodo says CC BY 4.0 ⚠ → reference until clarified); CAESAR-Lisflood (licence
  unclear ⚠ → reference); GRASS r.sim.sediment (GPL → oracle); Landlab erosion components
  (MIT → reusable after review).
- **Still missing:** `TODO(literature)` transport capacity (Nearing et al. 1997),
  deposition (Lei et al. 1998), detachment (Nearing 1991), splash (Planchon et al. 2000) —
  none in references.bib; SMODERP validation papers; RillGrow Supplement.

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| soil erosion by water | vodní eroze půdy | phenomenon |
| muddy flood | bahnitá povodeň, erozní smyv | phenomenon |
| sheet flow | plošný odtok | state variable |
| rill flow | soustředěný odtok v rýhách | state variable |
| rill | erozní rýha | state variable |
| sediment load | množství unášených splavenin | state variable |
| critical shear stress | kritické tečné napětí | parameter |
| critical velocity | kritická rychlost | parameter |
| sorptivity | sorptivita | parameter |
| saturated hydraulic conductivity | nasycená hydraulická vodivost | parameter |
| surface retention | povrchová retence | parameter |
| transport capacity | transportní kapacita | parameter |
| erosion / deposition map | mapa eroze a akumulace | output |
| buffer (grass) strip | ochranný travní pás | UI action |
