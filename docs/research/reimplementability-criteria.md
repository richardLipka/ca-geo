# Reimplementability criteria

The key question of the literature review is: **can we re-implement the model from the
publication alone (plus openly available material)?** Each publication in the survey is
scored on five sub-criteria (0–2 each), giving a total of 0–10 and a class A–D.

## Sub-criteria

| Code | Sub-criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| `S1` | **Rule specification** | Rule described only verbally / vaguely; key steps missing. | Main equations or logic given, but some parts (update order, neighbourhood weights, boundary handling, special cases) are missing or ambiguous. | Complete specification: states, neighbourhood, transition rule (equations or pseudocode), update scheme, time step, boundary handling. |
| `S2` | **Parameters** | Parameter values not given and no calibration procedure. | Some values given, or values only for the case study without explaining how to obtain them elsewhere. | All parameter values given (table) or a reproducible calibration procedure. |
| `S3` | **Code** | No code found. | Code exists but is not openly available (on request, closed tool, dead link, binary only). | Open-source code in a public repository (verified link). |
| `S4` | **Input data** | Inputs proprietary or not described. | Inputs described (type, resolution) but not available. | Inputs openly available, or the model can be run on generic layers (DEM, land cover) with documented preprocessing. |
| `S5` | **Reference results** | No results usable as a check. | Qualitative results (maps, figures) only. | Quantitative results with metrics or test cases that a reimplementation can be compared against. |

## Classes

| Total | Class | Meaning for ca-geo |
|---|---|---|
| 9–10 | **A** | Direct reimplementation; results can be checked. |
| 7–8 | **B** | Reimplementation with minor assumptions. |
| 4–6 | **C** | Substantial assumptions needed; usable as a template for our own variant. |
| 0–3 | **D** | Inspiration only (concept, overview). |

Review papers and frameworks without a single specific model are not scored (`n/a`);
they are listed as entry points.

## Additional flags (not part of the score)

- **Access:** `OA` (open access), `preprint` (author version available), `paywall`.
- **Assessed from:** `full text` or `abstract` — scores from the abstract only are
  provisional and must be marked as such. `S1`–`S2` assessed from an abstract are at
  most 1 unless the abstract explicitly states otherwise.
- **Browser fit:** rough note whether the model looks feasible in a browser
  (grid size, number of steps, ensembles).
- **CZ/EU:** study area in the Czech Republic or the EU.

## Integrity rules

- Every listed publication must be verified in a bibliographic database (OpenAlex or
  Crossref) — title, authors, year, venue and DOI are taken from the metadata, never
  from memory.
- Code links are listed only if the URL was checked to exist.
- Summaries are written in our own words; no long quotations.
- When unsure about a score, choose the lower value and say why.
