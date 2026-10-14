<!--
Model card template (version 2, 2026-10-14 — adds parameters with provenance, engine
mapping and implementations).
Copy to docs/models/candidates/<id>.md, where <id> is the longlist slug (kebab-case).
Fill in every section. If something is unknown, write it as an open question rather than
guessing. Every numeric value must cite its source (BibTeX key + table / section / page)
or be marked as an assumption. Unverified facts (data sources, licences) are marked
"to be verified". Literature: only references in /references.bib.
-->

# <Model name>

| Field | Value |
|---|---|
| ID | `<id>` |
| Longlist ref. | `<longlist item ID>` |
| Category | <e.g. hydrology, natural hazards, ecology…> |
| Group | core / extension |
| Weighted score | <revision 2 score from docs/review/evaluation-matrix.md> |
| Primary reference | `<bibkey>` |
| Status | draft |
| Last updated | YYYY-MM-DD |

## 1. Phenomenon

What happens in reality, in plain words. Which processes drive it, on what spatial and
temporal scale, and what question would a user of the demo want answered.

## 2. Suitability for CA

Why the phenomenon is (or is not) a good fit for a cellular automaton: locality of
interactions, discrete spread, dependence on neighbouring cells, raster nature of inputs.
Also list what a CA *cannot* capture well here (long-range effects, continuous physics,
network structure…).

## 3. Cell state variables

| Variable | Type / domain | Meaning | Static / dynamic |
|---|---|---|---|
| | e.g. categorical {…}, real ≥ 0, boolean | | static input / evolves in time |

## 4. Neighbourhood and time step

- **Grid:** square / hexagonal; cell size range that makes sense.
- **Neighbourhood:** von Neumann / Moore / extended radius / other; why.
- **Time step:** what one step represents (fixed real duration, adaptive, abstract);
  how it relates to cell size.
- **Update scheme:** synchronous / asynchronous; why.
- **Boundary conditions:** which kind and why.

## 5. Transition rule

The rule of the primary reference, step by step, in our own words; equations may be
restated in our notation with a citation (key + equation / section number). State what a
cell reads, what decides its next state, what is conserved and what is not, and every
place where the paper is ambiguous (mark as an open question). Variants from supporting
references in a separate sub-section.

## 5a. Parameters

| Parameter | Symbol | Unit | Value / range | Source (key, location) | Note |
|---|---|---|---|---|---|
| | | | | `key`, Table N | |

## 6. Deterministic vs. stochastic

Which parts of the rule are random and why; what the randomness represents; whether
repeated runs (ensembles) and a fixed random seed are needed for the demo.

## 7. Input data (layer types)

| Layer | Data type | Role in the model | Required / optional |
|---|---|---|---|
| | raster (continuous / categorical), vector, time series, scalar parameter | | |

## 8. Likely open data sources

All entries "to be verified" (availability, licence, resolution, CZ/EU coverage).

| Layer | Candidate source | Coverage | Note |
|---|---|---|---|
| | | CZ / EU / global | to be verified |

## 9. Visualization

What to show and how: animated state map, overlays on terrain or basemap, time charts,
derived statistics, comparison of scenarios, interactive inputs (e.g. click to ignite,
draw a dam, change wind). What the user should "see" and learn.

## 10. Validation options

How results could be compared with reality: historical events, reference maps, other
models, qualitative plausibility. What data would be needed. Note if only qualitative
validation is realistic.

## 11. Links to other models

Which models can feed this one or consume its output (chaining scenarios), and which
shared components it uses (see `docs/review/shared-components.md`).

## 11a. Engine mapping

- **Stages** (primitives from `docs/architecture/engine-architecture.md` §6), in order per step.
- **Time policy**, **boundaries**, **RNG use**, **observers**, **interventions**.
- **Shared components** used (IDs from `docs/review/shared-components.md`).
- **Model-specific parts** that are not shared.

## 12. Complexity estimate

- **Implementation:** low / medium / high — why.
- **Computation in the browser:** low / medium / high — grid sizes, steps, ensembles.
- **Data preparation:** low / medium / high — why.

## 13. Risks

Scientific (oversimplification, misleading results), data (availability, licence,
resolution), technical (performance), communication (users mistaking a demo for a forecast).

## 14. Open questions

- …

## 15. Literature and implementations

- **Primary reference:** `key` — why this one.
- **Supporting references:** `key` — role (parameters, variant, validation case).
- **Benchmarks / reference data:** `key` or `data/reference/<name>`.
- **Implementations:** name, URL, licence, use under ADR 0006 (reusable code / reference
  only / oracle only).
- **Still missing:** `TODO(literature)` items and keywords for further search.

## 16. Terminology (cs)

Czech names for the UI. New terms must also be added to `docs/glossary.md`.

| English | Czech | Kind |
|---|---|---|
| <phenomenon name> | | phenomenon |
| | | state variable |
| | | parameter |
| | | UI action / output |
