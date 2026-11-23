# ČSÚ Historický lexikon obcí (not versioned)

- `13n106cd1.pdf` — *Historický lexikon obcí České republiky 1869–2005*, I. díl (ČSÚ 2006),
  `https://csu.gov.cz/docs/107508/8bc22eb2-b0bd-8ff2-1256-dd9373457cd4/13n106cd1.pdf` (21 MB; the
  server cuts long transfers, download with HTTP range requests). Population and houses per part of
  a municipality 1869–2001 and the year of the first written mention.
- The PDF text uses a font shifted by 29 code points: decode extracted text with `chr(ord(c) + 29)`
  (pages 301–302: okres Plzeň-město).
- `13008415okr.xlsx` — 1869–2011 edition, district totals only.
- The Plzeň house counts used by the growth model are copied into
  `apps/historic-mapper/scripts/growth_model.py` (`CENSUS`).
