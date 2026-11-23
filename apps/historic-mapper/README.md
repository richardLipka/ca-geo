# Historic mapper

Browser tool for preparing data about the historical town of Plzeň: georeference
historical maps and plans, overlay them on each other and on present-day layers, and link
objects depicted in views, drawings and engravings (towers, gates, churches, houses,
bastions) to positions on the map. The output — entities with geometry, lifetime and
evidence — is the input for a later 3D / time model of the town.

Analysis of the source material and of automation options:
`docs/research/historic-image-processing.md`. Source inventory:
`docs/research/data-sources/plzen-historical.md`.

## Run

```
npm install
npm run fetch-sources   # downloads source images into ../../data/historic/sources (not versioned)
npm run dev             # http://localhost:5218
npm test                # transform and i18n tests
```

The dev server also serves `../../data/` under `/data/` (source images, AMČR points) and
saves the project to `projects/<name>.json` on every change (with a browser copy as
fallback). Add sources by editing `sources.json` (id, title, kind, licence, download URL);
new entries are merged into an existing project on the next start.

## Workflow

Image pane (left) and map pane (right, EPSG:5514). Tools (keyboard shortcut):

| Tool | Use |
|---|---|
| Pan (V) | pan / zoom both panes, select markers |
| Control point (G) | click in the image, then the same place on the map (or the reverse) → control point |
| Identity (I) | click an object in the image → annotation; then click its entity on the map, or an empty place to create a new point entity |
| Outline (U) | outline an object in the image (house, roof, tower, church, gate, wall…) — stored as an annotation with a polygon; double-click or Enter finishes |
| Point / Line / Polygon (P, L, O) | draw entity geometry on the map; double-click or Enter finishes |

Map layers also include the **growth layer** (settlement areas per map epoch, see
`docs/research/plzen-first-model.md` §8) and AMČR fieldwork points. The **3D model**
(`/viewer3d.html`, link in the header) shows the entities as prisms with heights and the facet
textures cut from the 1618 plate, with a year filter. The **growth model**
(`/growth3d.html`, link in the header) animates all buildings of the town from 1295 to 2020
(schematic positions, interpolated dates; method in `docs/research/plzen-growth-model.md`)
and exports the animation as video frames.

Source types and transforms:

- **Map / plan** — Helmert (similarity, with or without reflection), affine, projective,
  2nd-order polynomial or thin-plate spline from control points; identity links to entities
  can also act as control points. The warped image is drawn on the map (WebGL mesh warp)
  with adjustable opacity, so several epochs can be overlaid.
- **Bird's-eye view** — projective transform (homography) from identity links: valid for
  the ground plane only, so tall objects are displaced; use it to predict where remaining
  objects lie, not as exact geometry.
- **Panorama / veduta** — 1D camera resection: from ≥ 4 identified objects the tool
  estimates the viewpoint, heading and focal length from their image columns, draws the
  viewpoint and sight lines on the map and shows vertical guide lines where every known
  entity should appear in the image.

Accuracy: the inspector reports fitted residuals and **leave-one-out residuals** per point
(the transform refitted without that point). Use the LOO RMSE as the accuracy of a source;
fitted residuals of flexible transforms (TPS) are always near zero. Points with LOO residuals
above three times the RMSE are highlighted.

Base layers: historical plans of the City of Plzeň (1781–1971, ArcGIS REST export), ČÚZK
orthophoto and ZTM 10 (WMS); optional AMČR fieldwork events
(`data/reference/plzen-amcr/akce-compact.json`). A year slider filters entities by
`validFrom` / `validTo`.

## Data model and exports

`projects/<name>.json` (`format: ca-geo/historic-mapper`, `crs: EPSG:5514`):
`sources`, `gcps` (per source), `entities` (name, type, geometry, house number,
validFrom / validTo, notes) and `annotations` (source, image position, entity, legend label,
confidence 1–3, note, use as control point).

Exports: project JSON; entities GeoJSON in EPSG:5514 or WGS84 with an `evidence` list per
feature; evidence table (CSV); GDAL commands (`gdal_translate -gcp …` + `gdalwarp`) and a
QGIS Georeferencer `.points` file for the current source.

## Scripts

- `scripts/fetch-sources.mjs` — download source images listed in `sources.json`.
- `scripts/segment_colours.py` — colour segmentation experiment for colour-coded plans
  (stable cadastre: stone buildings red, wooden yellow, water blue); numpy + GDAL only.

Image-processing scripts use the repository's local Python environment `.venv` (not
versioned; Python 3.13, PyTorch with CUDA 12.8, OpenCV, Segment Anything; SAM ViT-H weights in
`data/models/`):

| Script | Purpose |
|---|---|
| `plzen_1618.py` | landmark table, 1618 plate homography with LOO residuals, veduta viewpoint tests (metric + ordinal) |
| `overlay_check.py` | warp a source onto a map raster and draw residuals (visual georeference check) |
| `sam_buildings.py` | building footprints from a colour-coded plan with Segment Anything (GPU) |
| `build_1618_project.py` | seed the project with the c. 1536–1618 model (ids `g1618-…`) |
| `sam_view.py` | automatic SAM masks on a veduta region |
| `ottheinrich_cuts.json`, `cut_pieces.py` | house-by-house outlines of the oldest veduta → cut-outs + annotations |
| `facet_textures.py` | facet (wall / roof) textures from a georeferenced oblique view |
| `render_view.py` | render the model from a panorama viewpoint under the veduta |
| `growth_export.py`, `growth_tiles.py`, `growth_classify.py`, `growth_rules.py` | multi-epoch built-up growth in a 9 × 9 km frame (shared classification rules) |
| `ruian_buildings.py` | present building footprints with completion date and floors (RÚIAN, ČÚZK) |
| `growth_model.py` | dates every building 1295–2020 from RÚIAN, the map epochs, the 1618 model and written sources → `data/historic/growth/web/` |
| `encode_video.py` | H.264 MP4 from the frames exported by `growth3d.html` (ffmpeg from `imageio-ffmpeg` in `.venv`) |

## Licence

Code: MIT (repository licence). Source images keep their own licences (shown per source);
they are never committed. Base layers are fetched live from their providers.
