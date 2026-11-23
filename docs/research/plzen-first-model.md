# First model of Plzeň (c. 1536–1618): siege plan → building model → oldest veduta

Reverse analysis of the oldest available view of Plzeň (Ottheinrich travel album,
1536–37) against a model of buildings and fortification built from the 1618 siege plate
(Theatrum Europaeum), the stable cadastre (1839–41) and present-day landmarks. Done
2026-11-23 with `apps/historic-mapper` and the scripts in `apps/historic-mapper/scripts/`
(GPU: RTX 5070, PyTorch 2.11 + CUDA 12.8, OpenCV 5.1, Segment Anything ViT-H, all in the
local `.venv`, not versioned). Results are loaded into the historic-mapper project
(`apps/historic-mapper/projects/plzen.json`, ids `g1618-…`).

## 1. Older sources searched

A targeted search for anything older than or contemporary with the 1536 view that shows
the fortification outline found **no new source**:

- every map of Bohemia from Klaudyán (1518) to Criginger (1568, De Jode 1578), Ortelius,
  Mercator and Aretin (1619) uses a generic town sign for Plzeň (checked visually on
  Klaudyán and De Jode); Apian (1568) and Vogel (c. 1600) do not reach Plzeň;
- no Plzeň view in Schedel, Münster, Braun & Hogenberg, Hájek, Meisner or Zeiller's
  *Itinerarium*; the 14th-c. town seal is heraldic (a gate with towers);
- the known early images remain: Dominican cloister mural c. 1500–25 (ZČM, schematic double
  wall), Ottheinrich album 1536–37 (UB Würzburg, Delin. VI, no. 23), Statia mural 1574
  (town hall; shows the Litice gate), Willenberg 1602 (Strahov, view from the north-east),
  the 1618 siege plates, and a 1658 ground plan reported by R. Široký (2010, to be verified).

Literature critique (Ježek, *Průzkumy památek* 1997/2, open PDF): the Ottheinrich drawer
stood south of the town; the outer wall ring with roofed curtains and square towers is
credible, the inner layout of the town is fictitious. To obtain: Mergl 1995 (catalogue of all
Plzeň views), Razím 1995 (reconstruction of the fortification).

## 2. Georeference of the 1618 siege plate

Theatrum Europaeum plate (HAB Graph. C 945, CC BY-SA 3.0), projective transform from 12
control points: legend objects A (St Bartholomew), B (Dominican monastery), C (Franciscan
church), E (Prague gate), G (small / north gate), H (Litice gate) and six corners / street
mouths of the main square, against stable-cadastre block corners and Wikidata coordinates.

| Point | Residual [m] | Leave-one-out [m] |
|---|---|---|
| A St Bartholomew | 14.2 | 16.7 |
| B Dominican monastery | 9.4 | 39.9 |
| C Franciscan church | 5.2 | 12.2 |
| E Prague gate | 37.0 | 81.3 |
| G north gate | 26.5 | 48.7 |
| H Litice gate | 15.1 | 44.4 |
| square corners and mouths (6) | 7.8–24.1 | 9.6–30.9 |
| **all** | **RMSE 19.9** | **LOO RMSE 36.7** |

The fitted RMSE matches the 18 m reported for the inner town by Janata, Matoušek & Zimová
(*Kartografické listy* 21, 2013). Lessons: in an oblique view the ground position of a
building is the centre of its footprint, not the base of the drawn facade (correcting this
for the church removed a 60 m error); back-projecting known map positions into the plate is
the most effective check (it put the Dominican monastery exactly on letter B and exposed a
mis-identified Prague gate). The Prague gate remains the outlier (the breach scene is drawn
confusedly).

Eight wall towers drawn on the plate were projected onto the map and snapped to the wall line.

## 3. Building model

- **Inner town wall**: line along the backs of the perimeter houses on the stable cadastre
  (the 1821 plan is shifted by up to ~70 m in the south-east and was not used for geometry).
- **Landmarks** with heights and lifetimes: St Bartholomew (church and ~100 m tower), Dominican
  and Franciscan monasteries, All Saints, St Nicholas, four gates (demolished 1804–1849), water
  tower (1532).
- **Buildings**: footprints from the stable cadastre with Segment Anything (ViT-H, GPU, 400 px
  tiles, 0.5 m/px), restricted to building-coloured pixels: see section 5 for counts. Heights
  are defaults (stone 9 m, wood 6 m). Presence in 1618 is **not verified** per building; the
  block structure of the 1618 plate matches the cadastre, which supports using it as the base.

## 4. Reverse analysis of the oldest veduta (Ottheinrich 1536–37)

Identified with certainty: the west tower and the east end of St Bartholomew. Candidate
identities for five further objects (left gate with passage, round tower, tall tower with
corner turrets, church with spire, right corner tower) were tested in all combinations:

- **Metric test** (one viewpoint, perspective or cylindrical projection, viewpoint searched
  south of the walls): no combination fits — best RMSE 158–278 px on a 3061 px wide sheet.
  The residuals are systematic: the drawing spreads the objects more widely than any single
  viewpoint would, i.e. the artist **widened the townscape** (and, per Ježek, invented the
  interior).
- **Ordinal test** (does the left-to-right order in the drawing match the order of bearings
  from the viewpoint?): several combinations are fully consistent (21 / 21 pairs). The
  combination that agrees with the architecture and with the "south" viewpoint of the
  literature is: left gate = Imperial (Nuremberg) gate, round tower = Litice gate, tall tower
  = water tower (1532) or Prague gate, church with spire = Franciscan church, right tower =
  Prague gate; consistent viewpoints lie **0.3–3.8 km south-west of the town**.
- These identities are stored as annotations with confidence 1–2 (hypotheses) in the
  project; the two certain ones with confidence 3.

Conclusion: the 1536 view is usable as evidence of **which** landmarks and fortification
elements existed (gates, towers, roofed outer wall) and of their order along the skyline, not
of their positions or of the house layout.

## 5. Results and files

| Product | Numbers | Where |
|---|---|---|
| Building footprints, stable cadastre 1839–41 (800 × 800 m around the core) | Segment Anything ViT-H on the GPU (RTX 5070, 400 px tiles, 215 s): **755 houses**, plus 144 block remainders from the colour mask; 64.2 % of building-coloured pixels covered by SAM houses, 88.8 % with remainders | project entities `g1618-bld…`; `apps/historic-mapper/scripts/sam_buildings.py` |
| 1618 plate georeference | 12 control points, RMSE 19.9 m, LOO 36.7 m | `scripts/te1618_points.json`, project annotations on `te-1618` |
| Wall towers from the plate | 8, snapped onto the wall line | `g1618-te_tower_*` |
| Veduta identities | 2 certain, 5 hypotheses (ordinal analysis) | annotations on `ottheinrich-1536` |
| Veduta cut house by house | 47 outlined pieces (houses, roofs, towers, churches, gates, two curtain-wall sections); 6 linked to model entities | `scripts/ottheinrich_cuts.json`; PNG cut-outs + contact sheet in `data/historic/cutouts/ottheinrich-1536/` (not versioned) |
| Facet textures from the 1618 plate | 645 inner-town buildings, 2 255 visible walls + roofs | `data/historic/facets/te-1618/` (not versioned), `scripts/facet_textures.py`; shown in the 3D view |
| Synthetic view from the veduta viewpoint | model rendered with the fitted cylindrical camera under the veduta | `scripts/render_view.py`, `data/historic/cutouts/_synthetic_view_ottheinrich.jpg` |

## 6. Cutting old views house by house

- **Automatic** (Segment Anything, 64 points per side, on the town strip of the Ottheinrich
  view): 283 masks. Towers, the church nave, many roofs and gables come out, but houses are
  split into roof / wall / gable pieces and trees, sky and hills are mixed in — usable as hints,
  not as the result.
- **Visual recognition** (done here by the assistant on 2.5× zoomed gridded crops, with the SAM
  masks as a guide): one polygon per object, typed (house, roof, tower, church, gate, wall)
  and, where known, linked to a model entity with a confidence. The tool now has an
  **Outline** tool (U) for drawing / correcting such polygons in the image and stores them as
  annotations with `shape` and `kind`; `cut_pieces.py` exports transparent PNG cut-outs and a
  contact sheet. This hybrid (automatic proposals + recognition + confirmation in the tool) is
  the practical workflow for the older views, whose drawing style defeats pure segmentation.

## 7. Mapping images onto the 3D model as facets (method)

Each building of the model is a prism (footprint × height); its facets are the walls (one
per footprint edge) and the roof. Textures come from three kinds of sources:

1. **Georeferenced oblique views (siege plates, bird's-eye views)** — geometric facet mapping.
   Camera = ground homography *H* (map → image) plus a vertical displacement *h·k(x, y)* (pixels
   per metre of height, scaled by the local ground scale; *k₀* from an object of known height,
   here St Bartholomew's tower: *k₀* ≈ 2.3 px/m). A wall *ab* of height *h* projects to the quad
   *H(a), H(b), H(b) − (0, hk), H(a) − (0, hk)*; walls whose outward normal points to the viewer
   are rectified (perspective warp) to textures of *length × height* at 4 px/m; the roof is the
   footprint lifted by *h*, warped orthographically. Implemented in `facet_textures.py`.
   Result on the 1618 plate: many walls show recognisable facades (windows, portals, gables),
   others catch roofs or streets because the georeference error (20–35 m) is comparable to a
   house width. **Improvement:** block-wise refinement — a local homography per block fitted on
   the drawn block corners (or on SAM masks of the drawn blocks) brings the error below a house
   width; then per-house textures become reliable.
2. **Panoramas / vedute** (Ottheinrich, Willenberg) — no consistent camera (section 4), so the
   facet mapping is by **identity, not geometry**: each cut-out piece linked to an entity is
   rectified by a 4-point homography from its drawn facade corners to the facet rectangle
   (front wall + gable/roof). Unlinked house pieces form a **style library** (gable types,
   timber framing, roof colours) applied to model houses of the matching period and material
   without a specific identity — and labelled as such in the model.
3. **Plans and maps** — top facets: a georeferenced map raster (cadastre, plans, 1950s
   orthophoto) draped on the ground / roofs by its georeference (no rectification needed).

Each texture keeps its provenance (source, piece / quad, method, confidence), so a viewer can
show "drawn in 1618" vs "style sample from 1536" vs "generic".

The **3D view** (`apps/historic-mapper/viewer3d.html`, three.js) shows the entity model with
the facet textures and a year filter.

## 8. Growth of the town into its surroundings

All epochs that cover the surroundings were exported into one 9 × 9 km frame (2.5 m/px):
stable cadastre 1839–41, 3rd Military Survey (1880s), city plans 1891, 1895, 1912, 1926, 1931,
1938, 1947, 1950s orthophoto (CENIA) and present-day RÚIAN buildings (ČÚZK); the 2nd Military
Survey (1840s) is kept as a visual layer (its CENIA rendering has no separable settlement
colour). Building pixels are classified per cartographic style, turned into settlement areas
by building density (share of building pixels within ~150 m), and the settlement touching the
old town is taken as the continuous town (`growth_classify.py`).

| Map | Covered [km²] | Continuous town [km²] | Notes |
|---|---|---|---|
| Cadastre 1839–41 | 77.5 | 0.7 | old town + inner suburbs |
| 3rd Military Survey 1880s | 81.0 | 2.6 | roads partly misclassified as built-up |
| Plan 1891 / 1895 / 1912 | 25 / 30 / 42 | 1.0 / 0.4 / 1.9 | sheets cover only the centre |
| Plan 1926 | 79.2 | 5.4 | villages (Doubravka, Lobzy, Košutka, Radčice) still separate |
| Plan 1931 / 1938 / 1947 | 73 / 23 / 76 | 2.7 / 4.8 / 3.2 | different classification per sheet style |
| Orthophoto 1950s | 79.7 | 0.8 | heuristic texture rule — unreliable |
| RÚIAN buildings (present) | 81.0 | 18.8 | |

The tool shows these areas as a **growth layer** (town red, other settlements orange, village
points coloured separate / joined) following the year slider. The year each village joined the
continuous town is computed (`villages.json`) but is **not yet reliable**: classification
quality differs between sheets, and rivers and railways break the density-based continuity
(e.g. Lobzy appears separate even today). Treat the layer as a visual record; the per-village
dates need per-sheet tuning or manual confirmation.

## 9. Next steps

- Willenberg 1602 (view from the north-east, numbered landmarks) as an independent check of
  the identities; Isselburg / Hondius 1618 plate (legend A–Z, 1–12) as a second georeference.
- Outer (Zwinger) wall and towers from the 1618 plate; bastions of 1645–49 from 1703 / 1781.
- Per-building presence in 1618: compare block outlines of the georeferenced plate with the
  cadastre footprints; burned suburbs (legend D) as removed buildings.
- Obtain Mergl 1995, Razím 1995, Ježek 1998 and the 1658 plan.
