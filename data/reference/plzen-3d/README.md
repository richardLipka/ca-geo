# Plzeň 3D building heights (not versioned)

- **Source:** City of Plzeň, `https://ags.plzen.eu/arcgis/rest/services/GIS_3D_budovy/GIS_Budovy_Plzen_2024/MapServer/1`
  (3D building model 2024, multipatch). Only attributes are downloaded.
- **Download:** `python apps/historic-mapper/scripts/city_heights.py data/reference/plzen-3d/heights.json`
  (63 153 rows: ISKN building id, parcel id, relative height of the building and of the eaves).
- **Join:** RÚIAN `identifikacniparcela` = `PAR_ID` (31 012 of 32 425 buildings of the growth frame).
- **Meshes:** `python apps/historic-mapper/scripts/city3d_mesh.py` downloads the multipatch geometry of the
  49 961 objects in the growth frame (FeatureServer query with `multipatchOption=stripMaterials`, raw pages in
  `mp/`, 55 MB) and writes `mesh.npz` (1.58 M vertices, 2.24 M triangles). `growth_model.py` assigns each object to
  the RÚIAN building that contains it (37 467 objects → 31 367 buildings) and writes `web/mesh.bin`.
