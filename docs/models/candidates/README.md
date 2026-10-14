# Model cards

One card per selected model (ADR 0001), named after the longlist slug. Cards follow
`docs/templates/model-candidate.md` (version 2): rule and parameters of the primary
reference with provenance, engine mapping (section 11a, authoritative for
`docs/architecture/model-mapping.md`), data, validation, literature and implementations,
Czech terminology.

Status of all cards: **draft** (2026-10-14).

| Card | ID | Group | Primary reference | Primary read in full | Note |
|---|---|---|---|---|---|
| [water-flow-flooding](water-flow-flooding.md) | WAT | core ★ | `guidolin2016weighted` | no — rule from the authors' caflood kernels (GPL, facts only) | 6 scenarios; EA benchmarks |
| [wildfire-spread](wildfire-spread.md) | HAZ-01 | core ★ | `alexandridis2008cellular` | restated in full texts of `xia2025pytorchfire`, `freire2019using` | original not local |
| [population-dispersal](population-dispersal.md) | EPI-04 | core | `bradshaw2021stochastic` | yes | + EPI-05, ECO-04 |
| [cold-air-pooling](cold-air-pooling.md) | ATM-02 | core | `nowatschin2006gpubased` | no — second-hand description | needs full text |
| [bark-beetle-outbreak](bark-beetle-outbreak.md) | ECO-01 | core | `pietzsch2023nonparametric` | yes | Markov CA |
| [urban-growth](urban-growth.md) | LND-01 | core | `clarke1997selfmodifying` / `roodposhti2020towards` | no — SLEUTH documentation and source; supporting papers read | two variants |
| [accessibility-front](accessibility-front.md) | MOV-03 | extension | `wood2012anisotropic` | yes | |
| [lava-flow](lava-flow.md) | HAZ-05 | extension | `connor2012probabilistic` | yes | |
| [plant-pest-spread](plant-pest-spread.md) | ECO-09 | extension | `white2017modelling` | yes | + ECO-03 |
| [landslide-runout](landslide-runout.md) | HAZ-02 | extension | `damboise2022flowpy` | yes | + avalanche, rockfall |
| [pedestrian-evacuation](pedestrian-evacuation.md) | MOV-01 | extension | `kirchner2002simulation` | yes | |
| [soil-erosion](soil-erosion.md) | HYD-05 | extension | `landa2019smoderp2d` | yes (no transport rule in it) | transport rule in RillGrow supplement, not local |
| [pollutant-dispersion](pollutant-dispersion.md) | ATM-01 | extension | `sonnenschein2025hybrid` | no — rule from CellAutDisp code (GPL, facts only) | traffic NO₂ vs. smoke open |
| [groundwater-flow](groundwater-flow.md) | HYD-09 | extension | `ravazzani2011macroscopic` | no — domain notes | Theis benchmark |

Papers to obtain manually (university access) to complete the cards:
`guidolin2016weighted`, `alexandridis2008cellular`, `nowatschin2006gpubased`,
`clarke1997selfmodifying`, `roodposhti2020towards`, `sonnenschein2025hybrid`,
`ravazzani2011macroscopic`, `bates2010simple`, `ghisu2015optimal`, `ghisu2015improved`
(see `literature/manifest.md`).

Shared building blocks across the cards: `docs/review/shared-components.md`.
