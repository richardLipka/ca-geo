# Machine processing of historical images of Plzeň — options and tool

How far the collected historical maps, plans, views, drawings and engravings of Plzeň
(`docs/research/data-sources/plzen-historical.md`) can be processed automatically to extract
building footprints, fortification lines and the identity of depicted buildings, and which
steps need a human. Written 2026-11-23 together with the tool `apps/historic-mapper`.
Tool and method names below are mentioned as leads; their literature is
`TODO(literature)` (not yet verified in OpenAlex / Crossref).

## 1. What geometry each source class carries

| Class | Examples | Geometry | Usable as |
|---|---|---|---|
| Measured georeferenced plans | city `GIS_Historicke` 1781–1972, stable cadastre 1839–41, 1950s orthophoto | planimetric, metres-level (cadastre) to tens of metres (1781, 1821) | primary geometry: footprints, moat and wall lines |
| Unreferenced measured / semi-measured plans | 1712 Vogt, ZČM M97 1781, Schabat 1864, Kramerius UK plans 1882–1943 | planimetric, unknown distortion | geometry after georeferencing (affine → TPS) |
| Siege plans and bird's-eye views | 1618 Isselburg, Theatrum Europaeum, Keller, Hogenberg; Merian 1650; Bodenehr c. 1700; Starck c. 1680 | oblique, perspective not consistent; ground plane roughly projective inside the walls (TE: 29 GCPs, RMSE 18 m inside the town, 107–227 m for the whole sheet, per Janata et al. 2013) | identity and topology (which gates, towers, bastions; order around the ring), approximate positions, roofs and heights |
| Panoramas / profiles | Ottheinrich 1536–37, Willenberg 1602, Hollar, profile 1820–40 | one viewpoint, horizontal directions meaningful, vertical exaggerated | viewpoint, left–right order and bearings of landmarks, relative heights |
| Pictorial details and photos | Willenberg details, UK glass slides 1900–45, AMP photographs | none | facades, roofs, storeys; identity only by description |
| Texts | Listář, Plachý, Schaller, Encyklopedie, address books | addresses, house numbers, dates | building events and lifetimes (LLM extraction, see the overview page schemas) |

Consequence: geometry comes from the measured plans; views supply identity, height,
appearance and presence at a date; texts supply dates. The tool links all three through
**entities** (one record per real object) with **evidence** (annotations in sources).

## 2. Processing tasks and how far automation goes

### 2.1 Georeferencing

- **Already done** for the 23 city services (S-JTSK); export works without login.
- **Manual control points** remain the reliable method for the other plans: stable objects
  (church of St Bartholomew, corners of the square, block corners, gates, river bends) are
  easy for a person and hard for feature matchers because style, generalisation and paper
  distortion differ between epochs.
- **Automatic matching** (keypoint matchers of the SIFT / LoFTR family, `TODO(literature)`)
  can help only between near-identical renditions (e.g. ZČM M97 vs. the city's georeferenced
  1781 plan — same drawing, different scan). Not tested yet: OpenCV is not installed on the
  experiment server (ask before installing).
- **Transform choice:** affine or Helmert first; projective for bird's-eye views; TPS only with
  many evenly spread points. Judge by **leave-one-out RMSE**, which the tool reports per
  point, not by fitted residuals.

### 2.2 Footprints and fortification lines from colour-coded plans

Experiment (`apps/historic-mapper/scripts/segment_colours.py`, numpy + GDAL, run on the
experiment server): HSV thresholds on a 1600 × 1600 px export (0.5 m/px, 800 × 800 m around
the old town) of the stable-cadastre layer and of the 1840 plan.

| Layer | Stone buildings (red) | Wooden buildings (yellow) | Water (blue) |
|---|---|---|---|
| Stable cadastre 1839–41 | 24.5 % of pixels; 276 components ≥ 40 px | 1.2 %; 54 components | 0.5 % (outlines only) |
| Plan 1840 | 0.1 % (plan is not colour-coded for material) | 1.5 % | 4.8 % |

Findings:
- On the cadastre, stone buildings segment almost cleanly; the regular block structure, the
  church, the barracks, the theatre and suburban houses come out without training.
- **Blocks merge**: party walls between houses are thin dark parcel lines, so one block becomes
  one component. Splitting needs line detection (thin dark strokes) or the parcel numbers.
- Red **parcel numbers** and public buildings in darker carmine end up in the same class;
  morphological opening and a size filter remove most numbers.
- Water is drawn as a pale fill with a blue outline: only outlines are detected; moats and
  the millrace need the outline closed and filled.
- The method transfers only to plans with a colour code; the black-and-white lithographs
  (1864–1947) need learned segmentation (point-prompted segmentation models of the SAM
  family, or patch classifiers such as MapReader, `TODO(literature)`), which needs a GPU —
  not available on the experiment server.

Vectorisation path: class raster → `gdal_polygonize` → simplify → snap to the 1840 plan /
present cadastre → entities with `validFrom ≤ 1840`.

### 2.3 Legends, labels and texts

- **Printed legends** on siege plans and views (TE: A–K, Isselburg: A–Z + 1–12, Hogenberg:
  A–Y, Keller: A–M) are short; a multimodal LLM can transcribe them and propose the matching
  object type (gate, church, monastery, camp, breach). The tool stores the letter as the
  annotation label, so a transcribed legend can be joined later.
- **Street names and house numbers** on plans (1840 with house numbers, 1932 house-number
  plans): OCR of small rotated labels is unreliable; LLM-assisted reading of crops, confirmed
  in the tool, is more realistic.
- **Fraktur and manuscripts** (1618 pamphlets, Schaller, town books): specialised handwritten /
  Fraktur recognition (Transkribus-type, `TODO(literature)`) before LLM extraction.

### 2.4 Identity of buildings in views

- A multimodal LLM can propose candidates ("tall tower right of the church = waterworks?")
  but cannot place them on the map; positions come from the plans. **Human confirmation is
  required**; the tool makes it a two-click operation (image → map) and records confidence.
- **Bird's-eye views:** after 4–6 confident links the projective fit predicts where every
  other entity should appear in the image (green markers) and where a clicked image object
  lies on the map. Prediction is good on the ground plane inside the walls and degrades at the
  sheet edges and for tall objects (towers lean in the drawing).
- **Panoramas:** the 1D resection recovers viewpoint, heading and focal length from the image
  columns of ≥ 4 identified landmarks; it then draws guide lines where each known entity
  should appear. Synthetic tests recover the viewpoint within 25 m; on real panoramas the
  artist's composition (several viewpoints stitched, widened skylines) will show up as large
  column residuals — useful in itself to judge the reliability of a veduta.
- **Copy lineage:** Bodenehr (c. 1700) and the 1850–71 lithograph copy Merian / the 1618 plates;
  copies are not independent evidence. Record lineage in the entity notes and count evidence
  per independent original.

### 2.5 Change over time

With entities carrying `validFrom` / `validTo` and evidence per source, presence / absence per
epoch can be tabulated: built by year A (first evidence), gone by year B (absent from a later
measured plan or a dated demolition text). The year slider in the tool already filters by
these fields; deriving them from evidence is the next step.

## 3. Recommended pipeline

1. Base geometry per epoch from the georeferenced plans (city services, cadastre 1839–41,
   orthophoto 1950s): colour segmentation where colour-coded, manual tracing otherwise —
   start with the fortification ring (moat, walls, bastions, gates) on 1781 and 1821, and
   block outlines on 1840.
2. Georeference the remaining measured plans (Vogt 1712, ZČM M97, Schabat 1864, Kramerius UK
   plans) in the tool; keep only sources with acceptable LOO RMSE.
3. Identify landmarks in the views (TE, Isselburg, Keller, Hogenberg, Merian, Bodenehr,
   Willenberg, Ottheinrich, Hollar): start with the church, the four gates, the square and the
   bastion with the bath house; then use predictions to find the rest.
4. Extract dates from texts (LLM, schemas on the overview page) and attach them to entities.
5. Export entities (GeoJSON with evidence) → 3D / time model.

## 4. What the tool provides (apps/historic-mapper)

- Image and map side by side; map in EPSG:5514 with historical plans of the city, ČÚZK
  orthophoto / ZTM 10 and AMČR fieldwork points as base layers.
- Control points with five transforms, per-point residuals and LOO residuals, residual vectors
  on the map, and a WebGL mesh warp that overlays any number of georeferenced sources with
  adjustable opacity.
- Identity links (annotation ↔ entity) with legend label, confidence and note; links can act as
  control points; projective and panorama models predict positions in both directions.
- Entities (building, church, tower, gate, bastion, wall, moat, water, bridge, street) with
  point / line / polygon geometry, house number and lifetime; year filter.
- Exports: project JSON, GeoJSON (S-JTSK / WGS84) with evidence, evidence CSV, GDAL commands
  and QGIS `.points`.
- Bilingual UI (cs / en), autosave to `apps/historic-mapper/projects/`.

Not yet included: image-side polygons (only points), automatic control-point suggestion,
colour segmentation inside the tool, LLM-assisted legend reading, height estimation.

## 5. Open questions

- Install OpenCV / a segmentation model in a separate environment on the experiment server
  (needs the author's approval; no GPU there)?
- Licences: the cadastre mosaic (© ČÚZK) and some sources (CC BY-NC-ND) restrict publishing
  derived geometry — keep provenance per entity.
- Which epoch should the first 3D / time model target (1618, c. 1700, 1781)?
