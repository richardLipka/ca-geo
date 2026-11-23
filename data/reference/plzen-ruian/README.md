# RÚIAN building footprints of Plzeň (not versioned)

- **Source:** ČÚZK, RÚIAN map service, layer 3 *StavebniObjekt*,
  `https://ags.cuzk.gov.cz/arcgis/rest/services/RUIAN/MapServer/3/query` — open data (RÚIAN).
- **Download:** `python apps/historic-mapper/scripts/ruian_buildings.py data/reference/plzen-ruian/buildings.geojson`
  (all objects intersecting the 9 x 9 km growth frame -826900, -1074200, -817900, -1065200, EPSG:5514;
  32 425 footprints, ≈ 17 MB, retrieved Nov 2026).
- **Fields:** `kod`, `dokonceni` (completion date; 31 Dec 1919 / 1945 / 1960 / 1970 / 1980 / 1990 /
  2000 are age-class placeholders), `pocetpodlazi` (floors incl. underground), `zpusobvyuzitikod`
  (use), `typstavebnihoobjektukod`, `zastavenaplocha`, `cisladomovni`, `druhkonstrukcekod`.
- **Used by:** `apps/historic-mapper/scripts/growth_model.py` (growth model 1295–2020).
