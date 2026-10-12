# ca-geo

A demonstration toolkit for **cellular automata (CA) simulations over geographic data**.

The goal is to show — interactively, in a web browser — how simple local rules applied
on a raster grid can reproduce spatial phenomena such as water flow, flooding or wildfire
spread, driven by real open geodata.

## Current phase: literature review

The exploratory phase produced a longlist, criteria and an evaluation (scope grouping
pending approval). The project is now in a **broad literature review** of geographic CA
models, focused on how well published models can be re-implemented
(see `docs/research/`).

The exploratory phase produced documentation only:

- a brainstormed longlist of phenomena suitable for CA simulation,
- evaluation criteria and an evaluation of the candidates,
- candidate model cards for the selected models,
- an overview of shared components and data needs,
- open questions for the later literature review,
- a scope decision (ADR) and a roadmap.

No model implementation, no dependencies and no downloaded data exist yet. Literature and
concrete published models will be added in the next phase (see `docs/research/`).

Models confirmed so far:

1. **Water flow / flooding**
2. **Wildfire spread**

Further models are being selected in this phase.

## Planned direction

- **JavaScript** implementation running **in the browser** (planned stack: npm workspaces,
  Vite, Vitest).
- **Open geodata** with a focus on the **Czech Republic and the EU**.
- **Bilingual demos (cs/en)** — all UI texts via translation catalogues; see
  `docs/glossary.md` for the EN–CS terminology.

## Repository structure

```
docs/
  brainstorm/          free-form ideas, longlist
  models/candidates/   candidate model cards
  review/              criteria, evaluation, shared components, data needs, open questions
  decisions/           architecture / scope decisions (ADR)
  templates/           document templates
  research/            literature review (later phase)
  glossary.md          EN–CS terminology glossary
data/                  local data (not versioned, except README files)
packages/              future shared libraries (CA core, geodata, visualization)
apps/                  future web demos
references.bib         bibliography (filled in during the literature phase)
```

## Contributing conventions

- Documentation, file names, identifiers and commit messages are in English.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
- See `CLAUDE.md` for the working rules of the current phase.

## Remote

Planned remote: GitLab at `https://gitlab.kiv.zcu.cz/lipka/` (not configured yet).
