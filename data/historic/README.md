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
