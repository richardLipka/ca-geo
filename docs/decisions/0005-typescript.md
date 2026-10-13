# 0005 — Implementation language: TypeScript

| Field | Value |
|---|---|
| Status | accepted |
| Date | 2026-10-13 |
| Deciders | Richard Lipka (author) |
| Related | `docs/architecture/engine-architecture.md` §17 (Q5), ADR 0002 |

## Context

The engine has a rich declarative API (layer, parameter and stage declarations, time
policies, worker protocol) and two backends that must stay consistent. The planned stack
was JavaScript with npm workspaces, Vite and Vitest.

## Options considered

- **Plain JavaScript + JSDoc types** — no build step for types, but weaker checking of
  the declarative model API and of cross-package contracts.
- **TypeScript** — static checking of model definitions, stage reads / writes and worker
  messages; first-class support in Vite and Vitest; output is plain JavaScript for the
  browser and Node.

## Decision

TypeScript for all packages and apps (author decision). WGSL kernels stay WGSL (as
strings or separate files imported by the build).

## Consequences

- **Positive:** model definitions and engine contracts are type-checked; better editor
  support; easier refactoring across packages.
- **Negative:** a compile step and `tsconfig` setup per workspace.
- **Follow-up:** strict mode (`strict: true`); shared base `tsconfig`; typed i18n keys so
  that missing translations fail type checking where practical.
