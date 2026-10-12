# CLAUDE.md — ca-geo

## Purpose

ca-geo is a demonstration toolkit for cellular automata (CA) simulations over geographic
(raster) data, running in the browser. Confirmed models: water flow / flooding and wildfire
spread. Other models are being selected.

## Current phase: LITERATURE REVIEW (documentation only)

Exploration (longlist, criteria, evaluation matrix) is done up to the proposed grouping
in `docs/review/evaluation-matrix.md`, which is **paused, pending author approval**;
the literature review may change it. Current work: broad survey of geographic CA,
see `docs/research/search-protocol.md` and `docs/research/reimplementability-criteria.md`.

Rules — follow strictly:

- No model implementation code, no dependencies (no `package.json`, no `npm install`),
  no data downloads, no PDFs stored in the repository.
- Cite only publications verified in OpenAlex / Crossref; take metadata from the
  database, never from memory. Never invent citations, authors, years, DOIs, code links
  or parameter values. Unverified leads are listed as such.
- Summaries in our own words; no long quotations.
- Unsupported claims stay marked `TODO(literature)` / "to be verified".
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
docs/research/            literature review: protocol, criteria, domains/*.md, catalogue
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
