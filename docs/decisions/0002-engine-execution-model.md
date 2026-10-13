# 0002 — Engine execution model: declarative models over stage primitives

| Field | Value |
|---|---|
| Status | accepted (2026-10-13) |
| Date | 2026-10-13 |
| Deciders | Richard Lipka (author) |
| Related | `docs/architecture/engine-architecture.md` §5–§7, `docs/architecture/model-mapping.md` |

## Context

The selected models use very different update schemes: synchronous stochastic stencils
(fire, beetle), conservative flux exchange with adaptive time steps (water, cold air,
groundwater), priority-queue fronts (accessibility, event-driven fire), active lists with
parents (lava, runout), agents with conflict resolution (evacuation) and global
demand-constrained allocation (land use). The engine must run all of them, in the
browser, with an accelerated path for the heavy ones.

## Options considered

### Option A — Generic per-cell callback

One `update(cell, neighbours)` function per model, engine loops over cells.
Pros: simple, familiar. Cons: cannot express queue / allocation / agents cleanly; hides
read / write patterns, so neither GPU translation nor conservation checks are possible;
scatter writes cause order dependence.

### Option B — Declarative model with a fixed set of stage primitives

Models declare layers, parameters and an ordered list of typed stages (`map`, `stencil`,
`flux`, `reduce`, `convolve`, `jump`, `queue`, `front`, `agents`, `allocate`, `walk`,
`custom`). Pros: each primitive has clear semantics (gather-only, conservative flux,
sequential queue) that the engine can buffer, check and accelerate; models stay short.
Cons: needs up-front design of primitives; unusual models may need new primitives.

### Option C — Adopt an existing framework (e.g. port of OpenCAL / PCRaster concepts)

Pros: proven abstractions. Cons: no JavaScript / browser implementations found
(`docs/research/implementations.md`); still needs Option B-like primitives for queue and
agent processes.

## Decision

Option B, with a `custom` stage as a CPU-only escape hatch for prototyping. Parallel
stages are **gather-only**; scatter-like processes are written as two-pass `flux` stages
(outflow slots → inflow gather).

## Consequences

- **Positive:** conservation by construction; order-independent parallel stages; clear
  mapping to GPU; coverage of all selected models shown in `model-mapping.md`.
- **Negative:** primitives `front`, `agents`, `walk`, `queue` are CPU-only initially;
  mixed CPU / GPU pipelines need transfers.
- **Follow-up:** implement primitives in the order required by ADR 0001; review the set
  after the first three models.
