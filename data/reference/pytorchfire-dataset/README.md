# PyTorchFire paper dataset

- **Source:** Mendeley Data, "Data for: 'PyTorchFire: A GPU-Accelerated Wildfire Simulator with
  Differentiable Cellular Automata'", DOI 10.17632/nx2wsksp9k.1 (version 1),
  https://data.mendeley.com/datasets/nx2wsksp9k/1 (files fetched via the public API).
- **Licence:** CC BY 4.0 (dataset metadata).
- **Downloaded:** 2026-10-13.
- **Files:**
  - `dataset.hdf5` — 94.6 MB, SHA-256 `9873c486ca86c366965c548559a1f87b65c2641695c25c564f237933f1f92900`
  - `prediction_time.csv` — 4 KB (run name, prediction time), SHA-256 `f284568d4214b6d3dd743cd1bc6dfb23a17da221557b2ee88730f404af46fbe8`
- **Related model:** HAZ-01 wildfire. Key: `xia2025pytorchfire`. Code: `external/PyTorchFire`.
- **Contents:** HDF5 file with the simulated and real-fire targets used in the paper
  (the example scripts read `simulated_fig_targets.hdf5`, `real_targets.hdf5`). The exact
  group layout was **not inspected** (no HDF5 reader installed; to be verified).
- **Related data inside the clone:** `external/PyTorchFire/examples/Bear_2020/*.npz`
  (vegetation, density, slope, wind, ignition, target burn map of the 2020 Bear fire).
