# Historical source images (not versioned)

Full-resolution images of historical maps, views and engravings of Plzeň used by the
historic mapper tool (`apps/historic-mapper`). The list of sources, with holders, licences
and download URLs, is `apps/historic-mapper/sources.json`; download with

```
npm --prefix apps/historic-mapper run fetch-sources
```

- `sources/<id>.jpg` — one file per source id. Files are ignored by git (large data, third-party
  rights); licences differ per source (public domain, CC0, CC BY-SA, CC BY-NC-ND …) and are
  shown in the tool next to each source.
- Wikimedia Commons rate-limits automated downloads (HTTP 429) and serves only standard
  thumbnail widths (e.g. 1920, 3840) to scripts; if a download fails, fetch it later or
  through another network.

Derived data (also not versioned, regenerate with the scripts in `apps/historic-mapper/scripts/`):

- `cutouts/<source>/` — house-by-house cut-outs of vedute (PNG with transparency) and a contact sheet.
- `facets/te-1618/` — facet textures (walls, roofs) from the 1618 siege plate + `facets.json`.
- `growth/raw/` — all map epochs in the common 9 x 9 km frame; `growth/builtup.geojson`,
  `growth/villages.json`, `growth/mask_*.png` — classified settlement areas per epoch.
- `growth/web/` — growth model for `growth3d.html` (`model.json`, `mesh.bin` with the city 3D models, ground textures `ground_*.jpg`).
- `growth/video/` — exported animation frames (`<run>/f_*.jpg`) and encoded MP4.
- `growth/site/` — guide to the growth video with previews of all sources (`scripts/sources_site.py`); open with
  `python apps/historic-mapper/scripts/serve_site.py` → `http://localhost:5219/site/` (the server supports HTTP Range,
  needed for the chapter jumps in the video). Contains reproductions of works under copyright shown as quotations
  (§ 31 AZ), so it stays local.
- `growth/site/check/` — footprint check per map (`check_epochs.py`) and the yes / no review page (`review_items.py`, `review.html`; decisions in `review.json`).
- `growth/publish/` — publishable page with the 3D model, timeline and maps (`scripts/publish_site.py`); serve the folder statically.
- `growth/raw_hi/` — detailed map exports for local analysis (e.g. the 1902 plan around the barracks at 0.5 m).
- `growth/shots/` — stills from the 3D viewer used by the guide (3D models, veduta projection).
- `../reference/plzen-ruian/buildings.geojson` — RÚIAN building footprints of the 9 × 9 km frame.
