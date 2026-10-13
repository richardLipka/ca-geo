# 0004 — Randomness and reproducibility: counter-based RNG

| Field | Value |
|---|---|
| Status | accepted (2026-10-13) |
| Date | 2026-10-13 |
| Deciders | Richard Lipka (author) |
| Related | `docs/architecture/engine-architecture.md` §8 |

## Context

Most selected models are stochastic (fire, beetle, land use, population, pest spread,
evacuation, lava ensembles). Demos, tests and validation need reproducible runs; the same
run should give the same result regardless of worker count, evaluation order or (within
float tolerance) backend; any member of an ensemble should be replayable alone.

## Options considered

### Option A — Sequential PRNG stream per simulation (e.g. one xorshift / PCG state)

Pros: simple. Cons: results depend on evaluation order; impossible to match on the GPU;
parallel workers need stream splitting.

### Option B — Per-cell PRNG states stored in a layer

Pros: GPU-friendly. Cons: memory per cell; state must be carried through every stage and
across backends; still order-dependent for sequential primitives.

### Option C — Counter-based generator: `random = hash(seed, run, step, stage, cell, draw)`

Pros: stateless, order-independent, identical integer output on CPU and GPU, trivial
ensemble seeding and replay. Cons: needs a hash of good statistical quality that is cheap
in WGSL (32-bit integer operations only).

## Decision

Option C. Candidate generators (Philox-style 32-bit, or a strong 32-bit integer hash) will
be compared for statistical quality and WGSL cost before the choice is fixed in this ADR.
Distributions are derived from uniform draws in one shared specification (CPU and WGSL).
Sequential primitives key draws by entity / event id instead of container position.

## Consequences

- **Positive:** reproducible runs, replayable ensembles, cross-backend comparison of
  stochastic models.
- **Negative:** slightly more arithmetic per draw than a stream PRNG; the key layout must
  stay stable across versions (changing it changes all results — version it).
- **Follow-up:** statistical test of the chosen hash; document the key layout.
