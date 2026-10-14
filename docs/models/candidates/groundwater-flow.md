# Groundwater flow and water table

| Field | Value |
|---|---|
| ID | `groundwater-flow` |
| Longlist ref. | `HYD-09` |
| Category | hydrology (subsurface) |
| Group | extension |
| Weighted score | 3.60 (revision 2, `docs/review/evaluation-matrix.md`) |
| Primary reference | `ravazzani2011macroscopic` (macroscopic CA, FEST) |
| Status | draft |
| Last updated | 2026-10-14 |

**Source note.** `ravazzani2011macroscopic` is **not local** (manifest status *failed*:
ScienceDirect bot check). The rule below is restated from the domain notes
(`docs/research/domains/atmosphere-other.md`, entry `ravazzani2011macroscopic`), which
were taken from the abstract and the open FEST model manual
(https://www.fest.polimi.it/reference/groundwater.html, not re-read here). The FEST code
(chiselapp, GPL per its docs, unverified; HTTP 302 in the last check) was not read. All
equations must be re-checked against the paper.

## 1. Phenomenon

Water in an unconfined aquifer moves from high to low hydraulic head through porous
rock or sediment. Recharge from rain, pumping wells and exchange with rivers raise or
lower the water table. Time scale days to years, space 10–100 m cells over km² to
hundreds of km². User questions: *how far does a pumping well's drawdown cone reach? how
does a drought or a river level change the water table? how fast does a mining pit fill
from groundwater (LND-03)?*

## 2. Suitability for CA

Very good as a verification target: Darcy exchange between face neighbours is purely
local, deterministic and has analytical solutions (Theis drawdown). Same numerical
skeleton as WAT (face flux → gather). Limits: explicit scheme is diffusion-limited
(small Δt on fine grids with high transmissivity); 2D (Dupuit) assumption ignores
vertical flow; confined / multi-layer aquifers and the unsaturated zone need the 3D CA
of `mendicino2006threedimensional` / `furnari2021asynchronous`. The process is invisible —
visualisation must do the work (evaluation C8 = 2).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| `K` | real > 0 (m s⁻¹) | hydraulic conductivity | static |
| `Sy` | real (0, 1) | specific yield | static |
| `bottom` z_b | real (m) | aquifer bottom elevation | static |
| `dem` | real (m) | ground surface (upper limit / seepage) | static |
| `gw.head` h | real (m) | hydraulic head = water-table elevation | dynamic |
| `gw.T` | real (m² s⁻¹) | transmissivity K · (h − z_b) | derived each step |
| `gw.q` | face, real (m³ s⁻¹) | Darcy flux between neighbours | dynamic (scratch) |
| `recharge` | real (m s⁻¹) | areal recharge | forcing |
| `wells` | sparse / raster (m³ s⁻¹) | pumping (−) or injection (+) | input / intervention |
| `river` stage, conductance | raster on river cells | river–aquifer exchange | input |
| `bc.type` | categorical {active, fixed head, fixed flux, inactive} | boundary cells | static |
| `gw.drawdown`, `gw.minHead` | real | observers | output |

## 4. Neighbourhood and time step

- **Grid:** square, uniform Δs (FEST raster; values for tests not in the notes).
- **Neighbourhood:** von Neumann (four faces) — Darcy flux across shared edges.
- **Time step:** fixed; 4000 s in the paper's tests (domain notes); no stability
  criterion stated → see §5 and open questions.
- **Update scheme:** synchronous explicit.
- **Boundaries:** fixed-head (Dirichlet) cells, fixed-flux (Neumann) cells; no-flow
  outside the active domain.

## 5. Transition rule

### 5.1 Macroscopic CA (`ravazzani2011macroscopic`, via domain notes)

Notation: cell i, face neighbour j, Δs cell size, h head, z_b bottom.

1. **Transmissivity** T_i = K_i · (h_i − z_b,i) for the unconfined case (saturated
   thickness). Whether the paper uses a head-dependent T each step or a fixed T is not in
   the notes → open question.
2. **Face transmissivity** T̄_ij = harmonic mean of T_i and T_j = 2 T_i T_j / (T_i + T_j).
3. **Darcy flux** across the face (square cells, face width = distance = Δs):
   Q_ij = T̄_ij · (h_j − h_i) [m³ s⁻¹], positive into cell i.
4. **Sources / sinks** per cell: recharge R_i · Δs²; well rate Q_w; river exchange
   Q_riv = C_riv · (H_riv − h_i) with streambed conductance C_riv (notes: "river–aquifer
   exchange via streambed conductance"; the clamp when h falls below the riverbed bottom is
   not described → open question).
5. **Head update:** h_i(t+Δt) = h_i(t) + Δt · (Σ_j Q_ij + Q_sources) / (S_y,i · Δs²).
6. **Boundaries:** fixed-head cells keep h; fixed-flux cells add a prescribed Q.

Conserved: water volume, because each face flux is antisymmetric (Q_ij = −Q_ji) and the
gather adds exactly the face fluxes plus recorded sources. Not modelled: vertical flow,
storage change from compressibility (confined S_s), unsaturated zone, dry cells
(h ≤ z_b → T = 0; rewetting rule → open question).

**Stability (assumption, not from the paper).** For an explicit 2D scheme with this
structure the usual von Neumann bound is Δt ≤ S_y Δs² / (4 T_max). This is standard
numerical analysis, not taken from a reference in `references.bib` →
`TODO(literature)` and to be checked against the paper's 4000 s choice. ca-geo can use it
as an adaptive or checked fixed Δt (stage `reduce` max T).

### 5.2 Benchmark — Theis drawdown

Domain notes: the model was tested against the Theis solution and MODFLOW-2000. The Theis
solution for a well pumping Q from a homogeneous aquifer of transmissivity T and storage
S: drawdown s(r, t) = Q / (4π T) · W(u), u = r² S / (4 T t), W the exponential integral
(well function). Valid for confined aquifers / small drawdown relative to thickness, so an
unconfined MCA run should use a large saturated thickness or fixed T. `TODO(literature)`:
Theis (1935) is not in references.bib; test settings of the paper not read.

### 5.3 Related CA formulations (supporting, not local)

- `mendicino2006threedimensional`: 3D unsaturated (Richards) macroscopic CA, Darcy fluxes
  between face neighbours, nonlinear capacity / conductivity (abstract only).
- `furnari2021asynchronous`: asynchronous activation by a head-difference threshold
  (abstract only).
- `milasinovic2019coupled`: coupled flow + contaminant transport CA benchmarked against
  MODFLOW / MT3DMS (domain notes).
- `furnari2024hydrocal`: 2D surface CA coupled with 3D subsurface CA (domain notes).

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| Time step (tests) | Δt | s | 4000 | `ravazzani2011macroscopic` via domain notes (`atmosphere-other.md`) | paper not read |
| Hydraulic conductivity | K | m s⁻¹ | not given | – | per test, open question |
| Specific yield | S_y | – | not given | – | open question |
| Aquifer thickness / bottom | z_b | m | not given | – | open question |
| Pumping rate (Theis test) | Q | m³ s⁻¹ | not given | – | open question |
| Streambed conductance | C_riv | m² s⁻¹ | not given | – | open question |
| Grid size of tests | Δs | m | not given | – | open question |
| Stability limit | – | – | Δt ≤ S_y Δs² / (4 T_max) | assumption (standard explicit-diffusion bound) | `TODO(literature)` |

## 6. Deterministic vs. stochastic

Deterministic. Optional ensembles over uncertain K fields (lognormal) for a didactic
"uncertainty" view; not in the primary reference.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| Hydrogeological units | vector / raster, categorical | K, S_y via LUT | required |
| Aquifer bottom / thickness | raster or constant | saturated thickness | required |
| Initial head | raster or interpolated well levels | initial condition | required |
| Recharge | raster or scalar series | source | optional |
| Wells | points + rates | sources / sinks | scenario |
| Rivers / lakes | vector + stage | exchange / fixed head | optional |
| DEM | raster | upper limit, visualisation | optional |

## 8. Likely open data sources

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| Hydrogeology | ČGS hydrogeological maps 1:50 000; hydrogeological zoning (VÚV TGM) | CZ | to be verified |
| Groundwater levels | ČHMÚ groundwater monitoring network | CZ | to be verified (licence, access) |
| Wells / boreholes | ČGS borehole database (Geofond) | CZ | to be verified |
| Rivers | DIBAVOD, ZABAGED | CZ | to be verified |
| Recharge proxy | ČHMÚ climate data; EU drought observatory (EDO) | CZ / EU | to be verified |
| European hydrogeology | IHME 1500 (BGR) | EU | to be verified |

## 9. Visualization

Head as a coloured surface with contour lines and flow arrows; drawdown cone around a
well (animated growth); cross-section profile through the well; head time series at
observation points vs the Theis curve; water-table depth below ground. Interactions:
place / remove a well and set its rate, change river stage, drought (recharge to zero).

## 10. Validation options

Theis analytical drawdown (benchmark runner, SC-BENCH); comparison with MODFLOW 6 /
FloPy or Landlab GroundwaterDupuitPercolator runs on the same grid (oracles); qualitative:
ČHMÚ observation-well hydrographs (to be verified).

## 11. Links to other models

Supports LND-03 (groundwater inflow into the pit lake, coupled with WAT's lake bucket),
ATM-04 / drought scenarios, HYD-01 (infiltration as recharge; seepage when head reaches
the surface — not in the primary reference). Same `flux` machinery as WAT and ATM-02;
contaminant-plume extension via `milasinovic2019coupled`.

## 11a. Engine mapping

- **Stages per step:**
  1. `map` T = K · max(h − z_b, 0) (derived scratch); sources (recharge forcing, wells,
     river exchange) into a source layer, river exchange recorded.
  2. `flux` (a) face pass: harmonic-mean T̄ × head difference → face layer `gw.q`
     (antisymmetric by construction); (b) gather: h += Δt (ΣQ + sources) / (S_y Δs²).
  3. `reduce` max T (stability check / adaptive Δt), total storage and boundary fluxes
     (mass balance).
- **Time policy:** `fixed` with a stability check (`reduce` max T) — or `adaptive` with
  the explicit-diffusion bound; display clock days / years.
- **Boundaries:** `fixed(head layer)` (Dirichlet cells, also inside the domain, e.g.
  lakes), `flux(layer)` (Neumann), `closed` outside the aquifer; exchange recorded.
- **RNG:** none.
- **Observers:** head / drawdown at points (time series), min-head envelope, mass balance
  (storage change vs Σ sources + boundary fluxes).
- **Interventions:** add / remove well (rate), change river stage, recharge scenario.
- **Shared components:** SC-GRID, SC-LUT, SC-FACE, SC-OUTFLOW (face-flux form), SC-ADT
  (stability check), SC-SRC, SC-BOUNDARY, SC-MASS, SC-BENCH, SC-INTERV, SC-ENVELOPE.
- **Model-specific:** harmonic-mean transmissivity, Theis reference implementation
  (well function), dry-cell handling.
- **Corrections to `model-mapping.md`:** (1) Boundary cells with fixed head occur
  **inside** the domain (rivers, lakes), so `fixed` must be a per-cell mask policy, not
  only an edge policy. (2) The flux pass needs no outflow limiter (antisymmetric face
  flux) but needs a **stability** limit instead; the `flux` primitive must allow both.
  (3) A "dry cell" rule (T = 0, no negative saturated thickness) is needed.

## 12. Complexity estimate

- **Implementation:** low — one face stencil, one gather, sources.
- **Computation:** low–medium; explicit Δt may force many steps for fine grids / high K
  (years of model time).
- **Data preparation:** high — hydrogeological parameters and initial heads are the
  bottleneck in CZ (availability to be verified).

## 13. Risks

Scientific: 2D Dupuit and homogeneous K are strong simplifications; heads near wells are
grid-dependent. Data: open hydrogeological parameters may be coarse or missing.
Technical: explicit instability if Δt is too large (must be guarded). Communication:
invisible process; drawdown maps could be misread as well-permit assessments.

## 14. Open questions

- Paper text: exact T definition (head-dependent?), test grid, K, S_y, Q values,
  river-exchange clamp, stability statement.
- Dry-cell and rewetting rule; seepage when h > ground surface.
- Theis test setup in ca-geo: confined-equivalent (fixed T) or unconfined?
- Fixed Δt with check vs adaptive diffusion bound.
- FEST licence and code reachability.

## 15. Literature and implementations

- **Primary reference:** `ravazzani2011macroscopic` — physically based MCA with an analytical
  benchmark (paper not local; manual in FEST docs).
- **Supporting:** `mendicino2006threedimensional`, `furnari2021asynchronous`,
  `furnari2024hydrocal` (CA subsurface family), `milasinovic2019coupled` (contaminant
  transport).
- **Benchmarks:** Theis solution (`TODO(literature)`, not in bib); MODFLOW-2000 comparison
  in the paper.
- **Implementations:** FEST (GPL per docs, unverified → reference only); Landlab
  GroundwaterDupuitPercolator (MIT → reusable after review, oracle); MODFLOW 6 / FloPy
  (USGS public domain → oracle); HydroCAL (code not found).
- **Still missing:** paper full text (manual download), Theis 1935 citation, a CZ case
  (e.g. pit lake inflow — none found).

## 16. Terminology (cs)

| English | Czech | Kind |
|---|---|---|
| groundwater flow | proudění podzemní vody | phenomenon |
| hydraulic head | piezometrická výška | state variable |
| water table | hladina podzemní vody | state variable |
| transmissivity | transmisivita | parameter |
| hydraulic conductivity | hydraulická vodivost | parameter |
| specific yield | specifická vydatnost (gravitační pórovitost) ? | parameter |
| recharge | dotace podzemní vody | input |
| pumping well | čerpaný vrt | input / UI action |
| drawdown (cone) | snížení hladiny (depresní kužel) | output |
| streambed conductance | vodivost dna toku | parameter |
| fixed-head boundary | okrajová podmínka pevné výšky hladiny | engine |
