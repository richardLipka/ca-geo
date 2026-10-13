# 0006 — Licence: MIT with a clean-room rule for copyleft references

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-10-13 |
| Deciders | Richard Lipka (author) |
| Related | `docs/research/implementations.md` (licence facts), `/LICENSE` |

## Context

ca-geo is a research and teaching project. The author prefers a permissive licence (MIT)
and accepts GPL only if it is the only way to use existing code. Several reference
implementations of the selected models are copyleft (GPL: Cell2Fire, LISFLOOD-FP,
SMODERP2D, PoPS, MOLASSES, SahulHumanSpread, CellAutDisp, Flow-Py, FUTURES, SAGA, GRASS;
EUPL: PROPAGATOR, AvaFrame), some have no licence (SLEUTH, MPB-Infestation, IPS-UPS),
and some are permissive (MIT: PyTorchFire, dispeRse, Xylella model, WebFlood).

Key fact: **a project under MIT cannot incorporate GPL / EUPL code** (copying or
translating it creates a derivative work that must be distributed under the copyleft
licence). Algorithms and mathematical rules themselves are not protected by copyright;
the selected models are re-implemented in TypeScript from their publications anyway.

## Options considered

### Option A — MIT, copyleft code used only as reference and test oracle

Re-implement from papers (clean room); copyleft programs may be read to understand an
algorithm and run as external oracles to compare results, but their source is not
copied or translated. Permissive code may be reused with attribution.

### Option B — GPL-3.0 for the whole project

Allows porting GPL code directly. EUPL is compatible with GPL via its compatibility list
(to be verified per case). Restricts reuse of ca-geo by others in permissive projects.

### Option C — MIT core, GPL only for individual packages that need ported code

Possible in the monorepo if ever needed; an app bundling such a package would then be
distributed under GPL.

## Decision

**Option A — MIT**, because the planned work is re-implementation from publications, which
does not require copying copyleft code. Option C is the fallback if a specific model
turns out to require ported GPL code; it would be decided in a separate ADR for that
package. Code without any licence (SLEUTH etc.) is treated as "all rights reserved":
reference and oracle only.

## Rules (clean-room policy)

1. Model kernels are written from the paper (and our model card), not from copyleft
   source.
2. Copyleft source may be **read** for understanding; notes must be paraphrases (as in
   `implementations.md`), never code fragments.
3. Running copyleft programs to produce reference outputs for tests is allowed; the
   outputs (data) are stored under `data/reference/` with their licence noted.
4. Code from MIT / BSD / Apache-2.0 projects may be reused with the original copyright
   notice kept (third-party notice file).
5. Each model card states which sources were used (paper, permissive code, oracle).

## Consequences

- **Positive:** permissive licence for a research / teaching toolkit; maximal reuse by
  others.
- **Negative:** more effort than porting; careful documentation of sources is needed.
- **Follow-up:** add a third-party notice file when the first permissive code is reused;
  confirm the copyright holder (author vs. university) — `LICENSE` currently names the
  author.
