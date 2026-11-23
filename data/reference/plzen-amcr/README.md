# AMČR fieldwork events in the historic core of Plzeň

- **Source:** Archaeological Map of the Czech Republic (AMČR), Digital Archive of the
  Archaeological Information System of the Czech Republic (AIS CR),
  `https://digiarchiv.aiscr.cz/api/search/query?entity=akce&loc_rpt=49.743,13.370,49.752,13.384&rows=100&page=N`.
- **Downloaded:** 2026-11-23.
- **Licence:** metadata CC BY-NC 4.0 (AIS CR). Only public records (access level A).
- **Contents:**
  - `akce-raw.json`: 195 fieldwork events (`akce`) as returned by the API.
  - `akce-compact.json`: one record per event with identifier, start year, leader, centroid
    of all locations (WGS84), component periods, location text, the first 220 characters of
    the summary, and a `fort` flag (keyword match on walls / gates / moat / fortification;
    25 events).
- **Use:** positions of medieval / early-modern walls, moat, gates and house plots for the
  Plzeň reconstruction (see `docs/research/data-sources/plzen-historical.md`, section 6).
- **Caveat:** centroids of linear trenches can fall away from the actual find spot.
