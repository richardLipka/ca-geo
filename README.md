# ca-geo

A demonstration toolkit for **cellular automata (CA) simulations over geographic data**.

The goal is to show — interactively, in a web browser — how simple local rules applied
on a raster grid can reproduce spatial phenomena such as water flow, flooding or wildfire
spread, driven by real open geodata.

## Current phase: architecture design

Done so far (documentation only, no implementation code yet):

- exploration — longlist of 47 phenomena, criteria, evaluation (`docs/brainstorm/`,
  `docs/review/`),
- literature review — two rounds, 418 verified references scored by reimplementability
  (`docs/research/`, `references.bib`), inventory of reference implementations,
- **accepted model scope** (`docs/decisions/0001-model-scope.md`),
- **accepted engine architecture** (`docs/architecture/`, ADRs 0002–0006).

Selected models:

| Core | Extension |
|---|---|
| Water flow / flooding ★ | Accessibility front |
| Wildfire spread ★ | Lava flow |
| Population dispersal | Plant pest / pathogen spread |
| Cold-air pooling | Landslide / avalanche / rockfall runout |
| Bark-beetle outbreak | Pedestrian evacuation |
| Urban growth | Soil erosion |
| | Pollutant dispersion |
| | Groundwater flow |

## Planned direction

- **TypeScript** implementation running **in the browser** and in Node (planned stack:
  npm workspaces, Vite, Vitest; WebGPU acceleration with a CPU reference backend).
- **Open geodata** with a focus on the **Czech Republic and the EU**.
- **Bilingual demos (cs/en)** — all UI texts via translation catalogues; see
  `docs/glossary.md` for the EN–CS terminology.

## Repository structure

```
docs/
  brainstorm/          longlist of phenomena
  models/candidates/   model cards
  review/              criteria, evaluation matrix
  research/            literature survey, catalogue, implementations
  architecture/        engine requirements, architecture, model mapping
  decisions/           ADRs
  templates/           document templates
  glossary.md          EN–CS terminology glossary
literature/            downloaded papers (PDFs local only, never in git) + manifest
data/                  local data (not versioned, except README files)
external/              local clones of reference implementations (not versioned)
packages/              future TypeScript libraries (core, backends, geodata, models, …)
apps/                  future web demos (cs/en)
references.bib         bibliography
```

## Contributing conventions

- Documentation, file names, identifiers and commit messages are in English.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
- See `CLAUDE.md` for the working rules of the current phase.

## Remote

Repository: https://github.com/richardLipka/ca-geo (public). A mirror on GitLab KIV (`https://gitlab.kiv.zcu.cz/lipka/`) may follow.

## Licence

MIT — see `LICENSE`. Models are re-implemented from their publications; copyleft
reference implementations are used only as algorithm references and test oracles
(`docs/decisions/0006-licence.md`).
