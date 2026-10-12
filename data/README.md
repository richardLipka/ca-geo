# Data

Local working directory for geodata. **Its contents are not versioned** — only `README.md`
and `.gitkeep` files are tracked (see `.gitignore`).

During the exploratory phase no data are downloaded. Data needs are described in
`docs/review/data-needs.md`.

Planned conventions (to be confirmed in the architecture phase):

- one subdirectory per source or area of interest,
- each subdirectory has a `README.md` with the source, licence, download date, coordinate
  reference system and processing steps, so that the data can be re-created.
