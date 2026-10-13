# Literature (downloaded papers)

Local copies of papers referenced in `docs/research/`. Every file is listed in
`manifest.md` with its BibTeX key (`/references.bib`), source URL, licence, size and
SHA-256 checksum.

| Folder | Content | Versioned |
|---|---|---|
| `open/` | Papers with a licence that permits redistribution (CC BY, CC BY-SA, CC0, public domain, US government works, OGL) | yes |
| `restricted/` | Other papers that were freely downloadable (author versions, free-to-read, bronze OA) but without a redistribution licence | **no** (local only) |

Rules:

- File name = BibTeX key, e.g. `open/xia2025pytorchfire.pdf`.
- Only papers that are legally accessible without a subscription are downloaded
  automatically. Paywalled papers are listed in `manifest.md` as "manual" — the author
  can add them to `restricted/` using university access.
- Never commit anything from `restricted/`.
