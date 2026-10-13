# EA benchmark Test 4 — LISFLOOD-FP 8.0 configuration and results

- **Source:** Zenodo record 10.5281/zenodo.4661888 ("LISFLOOD-FP 8.0 simulation results"),
  file `ea4.zip`, https://zenodo.org/records/4661888/files/ea4.zip
- **Licence:** CC BY 4.0 (Zenodo metadata).
- **Downloaded:** 2026-10-13. SHA-256 `ea6d2cd7599beafbfcec1db37ff3129e71850f61e724e5b148c8bc153da18bf2`.
- **Size:** 16.8 MB zipped, about 0.99 GB unpacked (201 files). Kept zipped.
- **Related model:** WAT (water flow / flooding). Related keys: `neelz2010benchmarking`
  (test definitions), `shaw2021lisflood` (solver), `bates2010simple` (ACC solver).
- **Contents:** Environment Agency Test 4 (flood wave over a flat floodplain): LISFLOOD-FP
  parameter file `ea4.par`, boundary files `ea4.bci` / `ea4.bdy`, stage-point file
  `ea4.stage`, DEMs at 0.5, 1, 2, 5 and 10 m (`ea4-*.dem.gz`), and outputs for the `acc`
  (local inertial) and `dg2` (discontinuous Galerkin) solvers: water depth and velocity
  snapshots (`*.wd`, `*.Vx`, `*.Vy`), stage / velocity time series at gauge points
  (`*.stage`, `*.velocity`), mass balance (`*.mass`), max fields, sample-line extracts.
  Shell scripts in the archive are the authors' post-processing helpers — not run.
- **Use in ca-geo:** input DEM + boundary hydrograph to set up Test 4; the `acc` stage time
  series at the gauge points are the expected outputs to compare against.

Not downloaded (record only), same Zenodo record:

| File | Size | Note |
|---|---|---|
| `ea5.zip` | 72 MB zipped, ~7.9 GB unpacked | Test 5 (valley dam-break) results only; no input DEM in the archive (checked, then deleted). |
| `ea5-first-hour*.zip`, `ea5-20m.zip`, `ea5-50m-dg2.zip` | 0.3–20 MB | Test 5 results at other resolutions / periods. |
| `eden.zip` | 3.4 GB | Storm Desmond (Eden catchment) case. |

The Test 5 input DEM and inflow hydrograph are defined in the EA report (`neelz2010benchmarking`);
a downloadable source of the inputs was not found in this run.
