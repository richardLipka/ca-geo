# Evaluation criteria

Criteria for evaluating the longlist items (`docs/brainstorm/longlist.md`) and selecting
models for the project. Each item is scored **1–5** on every criterion.

**All criteria are oriented so that 5 = best for the project.** For complexity and
computational cost this means 5 = simple / cheap.

Scores in the exploratory phase are expert estimates without literature support; they
express our current understanding and should be revisited after the literature and data
review.

## Summary

| Code | Criterion | Weight | Question |
|---|---|---|---|
| `C1` | Suitability for CA | 20 | Is a local-rule raster automaton a natural model of the phenomenon? |
| `C2` | Open data for CZ/EU | 15 | Can the inputs be obtained as open data for the Czech Republic / EU? |
| `C3` | Demonstration and didactic value | 15 | Does the demo explain something interesting and understandable? |
| `C4` | Implementation complexity | 10 | How hard is it to implement (5 = easy)? |
| `C5` | Computational cost in the browser | 10 | Can it run interactively in a browser (5 = cheap)? |
| `C6` | Validation against reality | 10 | Can results be compared with observed data or events? |
| `C7` | Reuse of shared components | 10 | How much does it share with other models / build the common core? |
| `C8` | Visual attractiveness | 10 | Is the animation / output visually engaging? |
| | **Total** | **100** | |

## Weighted score

```
weighted score = Σ (weight_i × score_i) / 100        → range 1.00 – 5.00
```

Additional rules (proposed):

- **Knock-out flag:** a score of **1 in `C1` or `C2`** marks the item as a likely
  *out of scope* regardless of its total — a phenomenon that is not really a CA, or for
  which we cannot get data, cannot become a good demo. The flag is a prompt for discussion,
  not an automatic exclusion.
- **Tie-break:** with equal weighted scores, prefer the item with the higher `C7`
  (it strengthens the common core), then higher `C3`.
- **Portfolio view:** the final selection is not a pure ranking. It should also cover
  different categories and mechanisms (flow vs. spread vs. growth), so that the shared
  core is tested on diverse models. Deviations from the ranking are justified in the ADR.

## Revision 2 — literature support (2026-10-13)

After literature rounds 1–2 a ninth criterion was added and the weights were revised
(proposal; the author may adjust). Revision-1 weights are kept above for traceability;
`evaluation-matrix.md` shows both scores.

| Code | Criterion | Weight rev. 1 | Weight rev. 2 | Change |
|---|---|---|---|---|
| `C1` | Suitability for CA | 20 | 20 | — |
| `C2` | Open data for CZ/EU | 15 | 15 | — |
| `C3` | Demonstration and didactic value | 15 | 15 | — |
| `C4` | Implementation complexity | 10 | **5** | partly captured by C9 (complete rule, open code) |
| `C5` | Computational cost in the browser | 10 | 10 | — |
| `C6` | Validation against reality | 10 | **5** | partly captured by C9 (reference results, benchmarks) |
| `C7` | Reuse of shared components | 10 | 10 | — |
| `C8` | Visual attractiveness | 10 | 10 | — |
| `C9` | **Literature support / reimplementability** | — | **10** | new |
| | **Total** | 100 | 100 | |

`C9` is derived from the best reimplementability class of a reference that can serve as
the template for the model (`docs/research/catalogue.md`):

| Score | Description |
|---|---|
| 1 | No CA (or CA-like grid) model found in the literature. |
| 2 | Best template is class D, or only non-CA physics models exist. |
| 3 | Best template is class C, or a class B model that is not a CA (e.g. individual-based). |
| 4 | Best template is class B, or class A that is not strictly a CA (e.g. cost-distance). |
| 5 | Best template is class A: complete rule, parameters, open code and reference results. |

Rationale: the project now has evidence on how much of each model can be taken over
from published, checkable work; this lowers implementation risk and gives validation
targets, so it gets its own weight, taken from the two criteria it overlaps with.

## Rationale for the weights

- **`C1` Suitability for CA (20)** — the project is about cellular automata; a phenomenon
  that only fits a CA with heavy distortion undermines the whole message. Highest weight.
- **`C2` Open data (15)** — "over geographic data" is the other half of the project's
  identity; without real open data for CZ/EU the demo loses its point. Slightly below `C1`,
  because synthetic or simplified inputs are an acceptable fallback for some demos.
- **`C3` Demonstration and didactic value (15)** — the product is a demonstration tool;
  the model has to teach something (a mechanism, a "what if" effect). Equal to `C2`.
- **`C4` Complexity (10)** and **`C5` Computation (10)** — practical feasibility.
  Important, but they rarely decide alone: a complex model can be simplified, and grid
  size can be reduced. Medium weight.
- **`C6` Validation (10)** — valuable for credibility and for possible articles, but
  for a demonstration tool qualitative plausibility is often enough. Medium weight.
- **`C7` Reuse (10)** — models that share building blocks make the core architecture
  better and lower the marginal cost of each new model. Medium weight; also tie-breaker.
- **`C8` Visual attractiveness (10)** — matters for a demo, but partly overlaps with `C3`
  (a good explanation is usually also visual), so it is not weighted higher.

The weights are a proposal and can be changed by the author; changing them only requires
recomputing the weighted scores in `evaluation-matrix.md`.

## Scale descriptions

### `C1` Suitability for CA

| Score | Description |
|---|---|
| 1 | Not a local process; essentially global, network-based or continuous physics where a CA would be misleading. |
| 2 | A CA can only mimic the outcome; the key mechanism is non-local or needs heavy workarounds. |
| 3 | Reasonable CA formulation exists, but important parts (e.g. long-range transport) need extensions beyond a plain neighbourhood rule. |
| 4 | Natural CA fit with minor extensions (e.g. extended neighbourhood, global parameters such as wind). |
| 5 | Textbook CA fit: purely local interactions on a raster, discrete states or local fluxes. |

### `C2` Open data for CZ/EU

| Score | Description |
|---|---|
| 1 | Key inputs are not openly available; only synthetic data would be possible. |
| 2 | Key inputs exist but are restricted, expensive, or only available for tiny areas. |
| 3 | Inputs available openly, but at coarse resolution, partial coverage, or needing substantial derivation. |
| 4 | Most inputs available openly for CZ or EU at usable resolution; some derivation needed. |
| 5 | All inputs available openly for CZ and EU at suitable resolution, with clear licences. |

In the exploratory phase this is an *expectation*; all sources are "to be verified".

### `C3` Demonstration and didactic value

| Score | Description |
|---|---|
| 1 | Hard to explain or of little interest to the target audience; the result says nothing new. |
| 2 | Interesting only to specialists; the mechanism is not visible in the simulation. |
| 3 | Understandable, shows a basic mechanism, limited "what if" interaction. |
| 4 | Clearly explains a mechanism; meaningful user interaction (change inputs, compare scenarios). |
| 5 | Strong "aha" effect: visible emergence or a counter-intuitive result; topical, relatable (e.g. local events), rich interaction. |

### `C4` Implementation complexity (5 = easiest)

| Score | Description |
|---|---|
| 1 | Research-level effort: many coupled processes, unclear rules, heavy calibration. |
| 2 | Several coupled state variables and processes; non-trivial numerical issues (stability, conservation). |
| 3 | Moderate: a few state variables, one main process, some care needed (e.g. mass conservation). |
| 4 | Simple rule with a few parameters; mostly reuses shared components. |
| 5 | Very simple rule (a few lines of logic once the core exists). |

### `C5` Computational cost in the browser (5 = cheapest)

| Score | Description |
|---|---|
| 1 | Infeasible interactively even on small grids; would need a server or offline precomputation. |
| 2 | Needs many small steps or large ensembles; interactive only on very small grids or with GPU. |
| 3 | Interactive on moderate grids with care (typed arrays, workers, possibly GPU). |
| 4 | Comfortably interactive on moderate grids on a typical laptop. |
| 5 | Trivial cost; runs in real time even on large grids or on mobile devices. |

### `C6` Validation against reality

| Score | Description |
|---|---|
| 1 | No meaningful comparison possible; results are purely illustrative. |
| 2 | Only qualitative plausibility check by an expert. |
| 3 | Comparison with reference maps or typical patterns possible, but not with specific events. |
| 4 | Specific historical events or observations exist and could be compared, with some effort to obtain data. |
| 5 | Well-documented events with open observed data (extent, timing) allowing quantitative comparison. |

### `C7` Reuse of shared components

| Score | Description |
|---|---|
| 1 | Stand-alone: almost nothing shared with other models. |
| 2 | Shares only generic infrastructure (grid, rendering). |
| 3 | Shares one substantive building block (e.g. DEM derivatives, stochastic spread). |
| 4 | Shares several building blocks and/or provides inputs to other models. |
| 5 | Core-forming: built mostly from shared blocks and a hub in model chains. |

### `C8` Visual attractiveness

| Score | Description |
|---|---|
| 1 | Little visible change; output is mainly numbers. |
| 2 | Slow or subtle change; static-looking maps. |
| 3 | Clear change over time, but visually plain. |
| 4 | Dynamic, readable animation on a map; obvious patterns. |
| 5 | Striking, intuitive animation (fronts, flows, growth) that invites playing with it. |
