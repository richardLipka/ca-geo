# 0007 — Revision of the stage primitives after the model cards

| Field | Value |
|---|---|
| Status | proposed (2026-10-14) — awaiting author approval |
| Date | 2026-10-14 |
| Deciders | Richard Lipka (author) |
| Related | ADR 0002 (amended), `docs/review/shared-components.md` ("Implications" I1–I16), `docs/architecture/engine-architecture.md` rev. 1.1, `docs/models/candidates/*.md` |

## Context

ADR 0002 fixed the execution model (declarative models over stage primitives) and planned
to review the primitive set once the models were known in detail. Writing the 14 model
cards from the primary references showed that some primitives were too narrow and that
several engine services were missing.

## Options considered

### Option A — Keep the ADR 0002 set, use `custom` for the gaps

Pros: no change. Cons: SLEUTH, PLUS, lava relaxation and runout traversal would end up in
CPU-only escape hatches without engine guarantees (RNG keying, replay, observers).

### Option B — Revise the set: replace `walk`, widen existing primitives, add `repeat`

Pros: every selected primary rule maps onto declared primitives; the changes are
extensions of existing semantics, not new paradigms. Cons: larger primitive specifications.

## Decision (proposed)

Option B. Amendments to ADR 0002:

1. `walk` is **replaced by `events`** — sequential sparse event scripts (start selection,
   spiral / nearest-feature search, walk along a feature layer, local action with retries).
2. `flux` gains a face kernel (antisymmetric) besides the donor kernel, a per-donor
   limiter, a retention threshold, declared flux units, an integer / multinomial mode and
   persistent flux layers.
3. `front` has two modes: shared-grid relaxation and per-source traversal with merge.
4. `allocate` gains joint greedy multi-class, zone quotas, weighted sampling, patch growth
   and an allowed-transition matrix.
5. `jump` gains a conservative mode, acceptance probabilities, discard / redraw and
   deterministic rays; `queue` gains direction flag, parent / nearest outputs, 16 slots,
   stochastic edge times and re-runs; `agents` gains move probabilities.
6. New **`repeat`** block (nested iteration of a stage group) and new time policy
   **`oneShot`**; adaptive time policy gains recompute period, snapping, look-ahead,
   growth when idle and retry.
7. Engine patterns made explicit: **scatter as gather** with keyed RNG, **one-pass state
   updates** for transitions that read the same previous state, direction values handed
   to kernels (the model combines them).

## Consequences

- **Positive:** all 14 selected models map onto primitives (`model-mapping.md` rev. 1.1);
  the shared-component tiers (T0–T3) give an implementation order for the engine.
- **Negative:** `events`, `front` and `allocate` remain CPU-only at first; the specification
  of `flux` is larger and needs careful tests (conservation, units).
- **Follow-up:** detailed interface specification of the primitives before implementing
  the engine core; review again after the first three models are implemented.
