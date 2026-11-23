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
