# CLAUDE.md — ca-geo

## Purpose

ca-geo is a demonstration toolkit for cellular automata (CA) simulations over geographic
(raster) data, running in the browser. Confirmed models: water flow / flooding and wildfire
spread. Other models are being selected.

## Current phase: EXPLORATION (documentation only)

Rules of the exploratory phase — follow strictly:

- No model implementation code, no dependencies (no `package.json`, no `npm install`),
  no data downloads.
- No invented citations, authors, years or numeric parameter values. Anything that needs
  support from literature is marked `TODO(literature)`; unverified facts (data sources,
  named models/approaches) are marked "to be verified".
- Named models or approaches may be mentioned only as a lead, marked "to be verified",
  without bibliographic details.
- State uncertainty openly; an open question is better than a confident guess.
- Ask the user before any decision that narrows the project scope.
- Work step by step; commit after each step and summarize briefly.

## Directory structure

```
docs/brainstorm/          free ideas, longlist
docs/models/candidates/   candidate model cards (<id>.md, from docs/templates/model-candidate.md)
docs/review/              criteria, evaluation matrix, shared components, data needs, open questions
docs/decisions/           ADRs (NNNN-short-title.md, from docs/templates/adr.md)
docs/templates/           templates
docs/research/            literature review (later phase)
docs/glossary.md          EN–CS terminology glossary
docs/roadmap.md           project phases
data/                     local data, not versioned (only README.md / .gitkeep)
packages/  apps/          future code (README only for now)
references.bib            BibTeX, filled in during the literature phase
```

## Language conventions

- Communicate with the user in **Czech**.
- Everything in the repository is in **English**: docs, file names, identifiers, commits,
  (future) articles.
- Web demos will be **bilingual (cs/en)**. Whenever a key term appears in docs, add its
  Czech equivalent to `docs/glossary.md`; model cards have a "Terminology (cs)" section.

## Planned stack (do NOT install yet)

- JavaScript (ES modules), browser-first.
- npm workspaces (`packages/*` shared libraries, `apps/*` demos).
- Vite (dev server / build), Vitest (tests).

Future UI rule: **no hard-coded user-facing strings**. All UI texts go through translation
catalogues for `cs` and `en`; both catalogues must stay in sync (same keys).

## Commit conventions

- Conventional Commits: `type(scope): summary`, e.g. `docs(review): add evaluation matrix`.
  Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`.
- English, imperative mood, summary under ~72 characters.
- No AI co-author / attribution trailers.
- Branch `main`; local only for now. Planned remote: `https://gitlab.kiv.zcu.cz/lipka/`.
- Line endings: LF (enforced by `.gitattributes`).

## Markers

- `TODO(literature)` — needs support from literature (later phase).
- "to be verified" — unverified claim (data source availability, licence, named model).
