# 0001 — Model scope for the first implementation stages

| Field | Value |
|---|---|
| Status | proposed |
| Date | 2026-10-13 |
| Deciders | Richard Lipka (author) |
| Related | `docs/review/evaluation-matrix.md` (revision 2), `docs/review/criteria.md`, `docs/research/catalogue.md`, `docs/architecture/` |

## Context

The exploratory phase produced a longlist (now 47 items) and an evaluation matrix. Two
literature rounds (418 verified references) showed how well each phenomenon is supported
by reimplementable CA models. The engine architecture needs a defined set of models whose
mechanisms it must cover. Water flow / flooding and wildfire spread were confirmed by the
author from the start; water is one model with scenarios (author decision).

## Options considered

### Option A — Revision-1 grouping (5 core + 6 extension)

Selection before the literature review. Pros: smaller. Cons: did not use the literature
evidence; ATM-02 had no literature support at the time.

### Option B — Revision-2 grouping (6 core + 8 extension)

Selection with criterion C9 (literature support / reimplementability). Pros: every
selected model has a class A or B template; covers all mechanism families (gravity flow,
contagious spread, population dynamics, growth / allocation, fronts, particles,
dispersion). Cons: larger extension set.

### Option C — Pure ranking by score

Top N by weighted score. Cons: ignores diversity of mechanisms and Czech relevance
(would include e.g. lava without the portfolio argument made explicit).

## Decision (proposed)

Option B.

- **Core (first stage):** HAZ-01 wildfire ★, WAT water / flooding ★, EPI-04 population
  dispersal (+EPI-05, ECO-04), ATM-02 cold-air pooling, ECO-01 bark beetle, LND-01 urban
  growth.
- **Extension:** MOV-03 accessibility front, HAZ-05 lava, ECO-09 plant pest / pathogen
  (+ECO-03), HAZ-02 runout (+HAZ-03, rockfall), MOV-01 pedestrian evacuation, HYD-05
  erosion, ATM-01 pollutant dispersion, HYD-09 groundwater.
- Proposed implementation order of the core: WAT → HAZ-01 → ATM-02 (reuses the flux
  kernel of WAT) → EPI-04 → ECO-01 (reuses stochastic spread of HAZ-01) → LND-01
  (adds allocation, walk and controllers). Rationale: start with the two confirmed models,
  then reuse their primitives before adding new ones.

## Consequences

- **Positive:** the engine requirements (`docs/architecture/requirements.md`) are derived
  from a fixed, literature-backed set; each model has a primary reference for its card.
- **Negative / costs:** the extension set is large; hex and graph topologies and
  multi-clock coupling are deferred.
- **Follow-up:** author approval (status → accepted); write model cards for the selected
  models from `docs/templates/model-candidate.md`; revisit when round-3 full-text reading
  changes a template's class.
