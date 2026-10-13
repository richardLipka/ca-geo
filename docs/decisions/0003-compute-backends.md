# 0003 — Compute backends: CPU reference + WebGPU acceleration

| Field | Value |
|---|---|
| Status | accepted (2026-10-13) |
| Date | 2026-10-13 |
| Deciders | Richard Lipka (author) |
| Related | `docs/architecture/engine-architecture.md` §10 |

## Context

Flux and stencil models (water with adaptive Δt, cold air, groundwater, fire ensembles)
need thousands of steps on grids up to millions of cells; queue- and agent-based
primitives are inherently sequential. Simulations must also run headless in Node for
tests, benchmarks and calibration.

## Options considered

### Option A — CPU only (JS typed arrays in Web Workers)

Pros: one code path, runs everywhere. Cons: large flood scenarios and ensembles become
slow.

### Option B — CPU reference + WebGPU compute, kernels written twice (JS + WGSL)

Pros: full speed where needed, CPU remains the specification; equivalence tests catch
divergence. Cons: duplicated kernel bodies for GPU stages.

### Option C — CPU reference + WebGL2 fragment-shader compute

Pros: wider legacy support (the cold-air template is itself a fragment-shader model).
Cons: awkward for reductions, integer atomics and multi-output stages; WebGPU supersedes it.

### Option D — Single kernel DSL compiled to JS and WGSL

Pros: no duplication. Cons: design effort before knowing the real kernel shapes; risk of a
leaky abstraction.

## Decision

Option B. The CPU backend implements every primitive and is the reference; the WebGPU
backend implements `map`, `stencil`, `flux`, `reduce`, `convolve` (and later `jump`,
`allocate`). Engine generates WGSL boilerplate; models provide kernel bodies.
Option D is re-evaluated after 3–4 models are implemented. WebGL2 compute is not
pursued (rendering may still use WebGL2).

## Consequences

- **Positive:** demos work without WebGPU (smaller presets); heavy models scale on GPU.
- **Negative:** two bodies per GPU stage; cross-backend results equal only within
  tolerance for floats.
- **Follow-up:** verify WebGPU support in target browsers at the start of implementation
  (to be verified); define per-layer tolerances in equivalence tests.
