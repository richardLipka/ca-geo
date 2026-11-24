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
and exports the animation as video frames. It stands on the DMR 5G terrain with per-epoch water,
shows the epoch maps as ground by their validity and has a **view mode**: the model seen from the
viewpoint of a veduta or bird's-eye plate next to the drawing; click a building in 3D and then the
object in the drawing to store a link (annotation, with the clicked 3D surface point) in the project.
*Fit camera* solves the draughtsman's camera (position, rotation, focal length) from ≥ 5 links by
robust least squares; *Project drawing* then paints the drawing from that camera onto façades, roofs
and terrain, with a depth test so surfaces hidden from the draughtsman stay unpainted. Present
buildings use their real shape from the City of Plzeň 3D model (`mesh.bin`), kept for their whole
life in the model.

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
| `growth_model.py` | dates every building 1295–2020 from RÚIAN, 16 map epochs, census house counts (ČSÚ), the 1618 model, the 1781 fortification and written sources; validation against the maps; terrain and water → `data/historic/growth/web/` |
| `fort_1781.json` | Zwinger and bastioned works digitised from the 1781 plan, with demolition years |
| `city_heights.py` | building heights of the City of Plzeň 3D model 2024 (attributes, joined by parcel) |
| `check_epochs.py` | footprint check of the model against every ground / epoch map at its first year (support by the map, buildings standing on one place at once) → `data/historic/growth/site/check/` |
| `publish_site.py` | builds the publishable bilingual web for people → `data/historic/growth/publish/`: the video guide (`index.html`), the video and the interactive model (`model/`, viewer in public mode: model, timeline, maps under the model); no review or editing tools |
| `map_buildings.py` | building footprints of the town plans 1891, 1895, 1902, 1908, 1912 at 0.5 m (city GIS, 3 × 3 km), one colour rule per plan; tiles registered to the 1912 plan / RÚIAN (tile shift + 4 × 4 local cells) → `data/historic/growth/hi_buildings.json`; `growth_model.py` chains them across the plans into dated buildings |
| `check_hi.py` | overlay of the model (buildings standing in the plan's year) on the 0.5 m plans → `raw_hi/_model_<year>_<i>_<j>.jpg` |
| `notable_buildings.json` | completion years and coordinates of 52 significant buildings (Czech Wikipedia); the RÚIAN building at the point (a `complex` with all joined buildings, e.g. the Bory prison 1878) stands from then on |
| `manual_maps.py` | index of the map set for the manual editor (all frame maps, early grounds, 0.5 m plans with their registration, vedute with cameras) → `manual/maps.json` |
| `veduta_recon.py` | gable houses from the points clicked on a veduta (footprint corners, eaves, ridge) and its fitted camera → `manual/veduta_buildings.json` |
| `review_items.py` | yes / no review page for the footprint tiles of every map and the veduta links (`site/check/review.html`; decisions saved by `serve_site.py` to `site/check/review.json`) |
| `veduta_fit.py` | fits the camera of the vedute to the model and estimates tower / gate heights → `veduta_heights.json`, saves the fitted views to the project |
| `ham57.py` | registers HAM map 57 (medieval topography c. 1410) and vectorises its blocks, suburbs, suburb walls, moat, churches and rivers → `ham57_map.json` |
| `fabric.py` | generated houses (gabled, perimeter blocks, scattered suburbs) and watertight earth bodies / ditches for `growth_model.py` |
| `fort_plans.py` | registers the 1658 and 1703 fortification plans (HAM maps 5, 6) by their wall ring and converts the works traced on them (`fort_plans.json`) to `fort_plans_map.json` |
| `city3d_mesh.py` | the City of Plzeň 3D model 2024 as triangle meshes (multipatch `binaryPatches` decoded and triangulated) → `data/reference/plzen-3d/mesh.npz` |
| `fetch_terrain.py` | ČÚZK DMR 5G terrain for the growth frame |
| `encode_video.py` | H.264 MP4 from the frames exported by `growth3d.html` (ffmpeg from `imageio-ffmpeg` in `.venv`) |
| `sources_site.py` | guide to the growth video: chapters with short texts, video jumps, stills, overview and fortification timelines, previews of every source with licence labels; catalogue and chapters in `sources_site.json`; writes `data/historic/growth/site/` (not versioned: quoted third-party maps) |
| `serve_site.py` | local server for the guide page with HTTP Range (video seeking): `http://localhost:5219/site/`; also the manual editor `http://localhost:5219/editor/` (saves into `manual/`) |

## Licence

Code: MIT (repository licence). Source images keep their own licences (shown per source);
they are never committed. Base layers are fetched live from their providers.

### Manual editor (`editor/index.html`)

Working tool, not part of the public web: `python scripts/serve_site.py` → `http://localhost:5219/editor/`.
*Maps*: every map of the model (and the 0.5 m plans, drawn registered) with the model buildings of the map's year;
a water brush / eraser and a footprint tool (click corners, Enter); optional from / to / height per footprint.
*Vedute*: per building click the footprint corners, eave points and ridge ends on the drawing.
Edits are saved in `manual/` (versioned): `map_<id>.json`, `water_<id>.png` (frame raster), `veduta_<id>.json`.
`veduta_recon.py` turns the veduta points into 3D (needs the fitted camera of `veduta_fit.py`); `growth_model.py`
adds the footprints (priority over generated and map-dated buildings), the reconstructed houses and the painted
water (into the map's water epoch). Logos for the video and the web are copied locally to `public/logos/` (not versioned).
