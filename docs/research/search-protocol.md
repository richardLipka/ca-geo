# Search protocol — broad literature survey

## Goal

Broad (breadth-first) survey of **cellular-automata simulations tied to geography**,
across as many application domains as possible. The result is a catalogue from which
models for implementation can be selected; the decisive criterion is
**reimplementability** (`reimplementability-criteria.md`).

Breadth before depth: the first round aims at coverage of domains and model families,
not at an exhaustive list per domain.

## Domains (search units)

| Code | Domain | Typical topics | Output file |
|---|---|---|---|
| `hyd` | Hydrology and floods | surface runoff, flood inundation, urban pluvial flooding, dam breach, ponding | `domains/hydrology.md` |
| `fire` | Fire | wildfire spread, fire behaviour coupling, urban / building fire spread | `domains/fire.md` |
| `lu` | Land use and urban growth | urban growth, land-use change, CA–Markov, calibration of LUCC CA | `domains/land-use.md` |
| `geo` | Geomorphology and mass movements | erosion, landscape evolution, landslides, debris flows, lava, avalanches, rockfall, dunes | `domains/geomorphology.md` |
| `eco` | Ecology and forestry | insect outbreaks, forest dynamics, succession, invasive species, vegetation patterns, predator–prey, dispersal, windthrow | `domains/ecology.md` |
| `epi` | Epidemics and populations | spatial epidemics, vector-borne diseases, animal and plant diseases | `domains/epidemics.md` |
| `mov` | Movement of people and vehicles | pedestrian evacuation, crowd dynamics, traffic flow, accessibility | `domains/movement.md` |
| `atm` | Atmosphere, climate, water bodies and other | air pollution dispersion, heat island, cold air, snow, drought, groundwater, oil spills, coastal processes | `domains/atmosphere-other.md` |
| `gen` | Cross-cutting | reviews of geographic CA, CA–GIS frameworks and software, GPU / web CA, calibration and validation methods | `domains/general.md` |

## Sources

- **OpenAlex API** (`api.openalex.org`) — primary search and metadata verification
  (title, authors, year, venue, DOI, open-access link, citation count).
- **Crossref API** (`api.crossref.org`) — DOI verification.
- **Web search** — finding code repositories, project pages and preprints.
- **Code hosting** (GitHub, GitLab, Zenodo) — checking that code links exist.

## Selection

Inclusion:

- A cellular automaton (or a clearly CA-like grid model with local rules) applied to a
  geographic phenomenon, or a methodological paper about such models.
- Peer-reviewed article, conference paper, thesis or documented software.

Exclusion:

- Purely abstract CA without a geographic interpretation (unless foundational for a domain).
- Agent-based or PDE models without a cellular rule — may be mentioned as context only.
- Publications that cannot be verified in OpenAlex / Crossref.

Prioritisation within a domain (breadth-first round, roughly 15–30 items per domain):

1. foundational / most cited models of each model family,
2. publications with open code or full rule specification (high reimplementability),
3. recent developments (roughly the last ten years),
4. review papers as entry points,
5. studies from the Czech Republic / EU.

## Per-domain output

Each domain file contains: search log (queries, date, hit counts), overview of model
families, a catalogue table, one entry per publication (citation, access, phenomenon,
model summary, inputs, parameters, code, validation, reimplementability scores,
relevance to longlist items) and a list of unverified leads and gaps.

BibTeX entries are collected in `/references.bib` (key `firstauthorYYYYword`).
