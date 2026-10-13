# Literature (downloaded papers)

Local copies of papers referenced in `docs/research/`. **PDFs are never versioned**
(author decision, 2026-10-13; `*.pdf` is ignored by git). Only this README and
`manifest.md` are in the repository; the PDFs live in the project folder on disk.

`manifest.md` lists every paper with its BibTeX key (`/references.bib`), source URL,
licence, size and SHA-256 checksum, so the local collection can be re-created and checked.

| Folder | Content |
|---|---|
| `open/` | Papers with a licence that permits redistribution (CC BY family, CC0, public domain, US government works, OGL) — could be shared with collaborators |
| `restricted/` | Freely downloadable papers without a redistribution licence (author versions, free-to-read) — personal use only |

Rules:

- File name = BibTeX key, e.g. `open/xia2025pytorchfire.pdf`.
- Only papers legally accessible without a subscription are downloaded automatically.
  Papers listed as "manual" in `manifest.md` can be added by hand (university access);
  subscription copies belong to `restricted/`.
- Never add PDFs to git (also not via `git add -f`).
