# Plzeň historical sources — maps, views, fortification, building histories

Inventory of online sources for reconstructing the development of Plzeň (fortification
outline, street network, building footprints and building lifetimes) as a time series /
animation, c. 1300–1990. Web research done 2026-11-23 (three parallel surveys: cartography,
fortification and iconography, building-level records). Items marked **TBV** were not
confirmed by opening the source. Nothing was stored in the repository; preview images were
used only for the private overview page (see below).

Interactive overview (private artifact, owner's account): a single page with a preview,
link, metadata (date made, period depicted, holder, licence, access, georeferencing), what
can be extracted and the extraction schema for each source, all reachable from a timeline;
plus a same-frame "flip-book" of the old town 1781–1971.

## 1. Cartography

### City GIS — `GIS_Historicke` (ArcGIS REST, `https://ags.plzen.eu/arcgis/rest/services/GIS_Historicke`)

23 MapServer services, S-JTSK (EPSG:5514), tile cache to level 13 (≈ 0.25 m/px),
`exportTilesAllowed: false`, dynamic `/export` works without login (max 4096 × 4096 px,
PNG / JPG / TIFF), no WMS, no licence text in the services.

| Service | Content | Notes |
|---|---|---|
| `GIS_HIS_Plzen_1781` | military surveyors' situation plan (Capt. Kitteli), ZČM MP 57 | complete bastion ring, glacis, gardens |
| `GIS_HIS_Cisarske_otisky` | stable cadastre Imperial imprints c. 1839–41, 43 cadastral areas | © ČÚZK — portal use "for navigation and overview" only |
| `…_1821` | plan by Josef z Tošenovic | blocks inside the walls |
| `…_1840` | plan alongside the stable cadastre, **house numbers**, ZČM MP 137 | čp. concordance |
| `…_1864` | after the 1861–62 railway, ZČM MP 615 | |
| `…_1873`, `…_1951` | regulation plans (partly proposals) | not "as built" |
| `…_1877_mesto`, `…_1877_Lochotin` | town plan, AMP M 1922 | |
| `…_1881` | F. Auer for the building office, AMP M 956 | single buildings |
| `…_1891`, `…_1895`, `…_1902`, `…_1912_50cm`, `…_1926` (name contains `ň`), `…_1931`, `…_1950` | town plans | |
| `…_1893`, `…_1947` | colour lithographs 1 : 7 500 / 1 : 15 000 (ZČM MP 879, 935) | colour segmentation |
| `…_1908` | building-office plan, ZČM | single buildings |
| `…_1938` | A. Heidelberg, 33 notable buildings, AMP M 291 | |
| `…_1971`, `…_1972` | historic core during the "regeneration" demolitions | |

The city viewer **Staré mapy** (`https://gis.plzen.eu/staremapy/`) has further epochs not in
REST (1703, 1848, 1903, 1929, 1932 house-number plans in 66 sheets ≈ 1 : 700, 1939–45, 1955,
1958, 1981) and orthophotos 1938, 9 Apr 1945, 1956, 1967, 1972, 1982, 1988 — viewer only,
rasters on request (owners VGHMÚř, ČÚZK, Georeal, Geodis; 1945 © Škoda Archive).

### Other cartographic sources

| Source | Epoch | Access / licence | Use |
|---|---|---|---|
| Plzeň open data, plans 1877, 1879, 1891, 1902, 1924 (IDs 71–74, 104), ECW | 1877–1924 | free download; catalogue: no copyright / database right | best automated input (georeferenced) |
| ČÚZK Archive (`https://ags.cuzk.gov.cz/archiv/`): Imperial imprints, indication sketches, original maps, aerial survey photos | 1830s–1960s | viewing free, scans 100 CZK/product (TBV price list) | building parcels c. 1840, owners in indication sketches |
| CENIA historical orthophoto 1950s (Plzeň flown 1952–56), WMTS/WMS layer `orto` | 1950s | **CC BY 4.0** | footprints c. 1953 — legally cleanest aerial |
| 2nd / 3rd Military Survey (CENIA WMS), Geolab UJEP (1st–3rd) | 1764–1880 | WMS / viewer | built-up extent only (1 : 28 800, 1 : 75 000) |
| Charles University map collection (Kramerius UK, 41 public Plzeň items, IIIF) | 1619–1943 | public; licence key `cuni_map_collection_prf_uk` | Keller 1619 siege plan, 1618 siege lithograph, 1820–40 profile, Schabat 1864, Kohut & Líčka 1882/83 (de/cs), Faustus 1895, Pivovar 1892, KČT 1912, Protectorate 1943, War Office 1943 |
| MZK Kramerius (Moll collection) | 1650, c. 1720, 1939–45 | viewer | Merian, Bodenehr views |
| Historický atlas měst ČR 21: Plzeň (HIÚ AV ČR 2009) | medieval–20th c. | e-book, copyright | best published reconstruction of medieval walls and plots (reference only) |
| Kriegsarchiv Vienna, Archiv města Plzně map collection, SOA Plzeň, Porta fontium | 17th–19th c. | catalogues / on request | **TBV** — likely fortification engineering plans |

## 2. Fortification and iconography

| Item | Date | Holder / licence | Use |
|---|---|---|---|
| Ottheinrich travel album, sheet 23 | 1536–37 | UB Würzburg; Commons, PD | earliest view, medieval walls |
| Jan Willenberg panorama | 1602 | Strahov Library; Commons, PD | roofs, towers, bastion with bath house |
| Isselburg / Hondius siege map (Nürnberg) | 1618 | HAB Graph. A1: 1107–1110, CC BY-SA 3.0 DE | legend A–Z, 1–12 |
| Theatrum Europaeum siege plate (Merian) | 1618 event | HAB Graph. C 945/946, CC BY-SA 3.0 | georeferenced by Janata et al. 2013 (inside walls ≈ 1 : 4 500) |
| Georg Keller siege etching | 1619 | Kramerius UK, Commons | legend A–M |
| J. Hauer siege view; M. Seeblummer view | c. 1620; 1672 | ZČM G 141, G 182 — not online | |
| Oldest fortification plan | 1620 | WLB Stuttgart; fold-out in *Dějiny města Plzně I* (2014) | TBV digitisation |
| Merian view + Zeiller text | 1650 | Commons (UB Düsseldorf scan), PD; text on de.wikisource | text names gates, Zwinger, moat, 1647 works |
| J. G. Starck (attr.) bird's-eye view | c. 1680 | SLUB Geogr.A.230-2, CC BY-SA 4.0 | bastioned town with roofs |
| J. G. (Mauritius) Vogt plan | 1712 | Commons, CC BY-SA 3.0 | |
| Military plan, ZČM M97 | 1781 | Commons, PDM | possibly related to GIS 1781 (MP 57) — TBV |
| Eckarth views; Venuto after Döbler | 1794/1802; 1816 | SLUB; ÖNB — PD | demolition era |
| Saská brána engraving (in Hruška & Koráb 1883) | c. 1840 | NK ČR Kramerius, public | last gate (demolished 1849) |
| A. Haun lithograph | 1847/52 (SNG: 1864) | SNG G 12278, CC0 | |
| UK glass slides: vanished buildings, town hall, mill, portals | 1900–45 | Kramerius UK, public | |

Fortification timeline (from the sources above; dates from Plzeňský deník 2008, cs.wiki,
Zeiller 1650, Encyklopedie dějin města Plzně — cross-check): founding c. 1295; Zwinger
before 1420; Hussite sieges 1421–34; Mansfeld siege 19 Sep – 21 Nov 1618 (breach at Pražská
brána); bastioned outer works by J. Lacron 1645–49 (suburb cleared 1647); wall demolition
from 1795, moats filled 1795–1822; Litická brána 1804, Pražská 1822, western walls / ring
park 1828, Říšská 1833, Saská 1849; last wall section removed for the museum 1893–99;
eastern parks on the filled Mlýnská strouha 1921–22.

Literature with measurable facts: Janata, Matoušek & Zimová 2013 (*Kartografické listy* 21,
open PDF); Orna et al. 2023 (*Archaeologia historica* 48/2, doi:10.5817/AH2023-2-2,
CC BY-NC-ND 4.0); Široký et al. 2008 moat excavation at Pražská brána (*Forum urbes medii
aevi* V, TBV online); Kodera 2004 (17th-c. fortification in written sources, record only).
AMČR (`https://api.aiscr.cz/`, CC BY-NC 4.0) for excavation events.

## 3. Building-level records

| Source | Content | Access / licence | Extraction |
|---|---|---|---|
| Encyklopedie dějin města Plzně (`encyklopedie.plzen.eu`) | 362 buildings ("vznik", building history: owners, fires, rebuilds, demolitions, architects); 1 376 streets with renamings | crawlable HTML; no terms stated → ask the archive before republishing | richest LLM input; street gazetteer |
| RÚIAN StavebniObjekt (`ags.cuzk.gov.cz/…/RUIAN/MapServer/3`) | current buildings; `dokonceni` present for 21 408 of 40 603 objects near the core, but old stock carries placeholder years (1946, 1920, 1981, …) = age classes | open data | geocoding target; age class as upper bound |
| NPÚ Památkový katalog open data | ≈ 390 monuments in Plzeň; CSV without coordinates or dating; undocumented JSON API with dating / defunct objects (TBV) | CC BY 4.0 | seed list |
| Address books 1906, 1909 (1948 TBV) | SVK PK Kramerius, public, OCR | API | cross-sections (street, čp., owner) |
| Hruška & Koráb 1883, *Kniha pamětní* | dated chronicle 775–1870 | NK Kramerius, public, OCR | events |
| Newspapers *Plzeňské listy* 1875–1911, *Plzeňské noviny* 1864–76 | building notices | CDK API, OCR | noisy events |
| Wikidata | 3 569 items in Plzeň; 474 with P571, 17 with P576, 391 with ÚSKP ID | CC0 | dated points |
| Archiv města Plzně Digitální badatelna | 237 k records, 3.65 M attachments (views, plans, photos, files) | publication needs consent | photos, building plans |
| Police registrations 1898–1921, census sheets 1869–1921, land registers | AMP / Porta fontium / SOA eBadatelna | scans, handwritten | existence evidence (low priority) |

House numbering: conscription numbers from 1770–71; suburbs (Pražské, Říšské, Saské
předměstí → Východní, Jižní, Severní Předměstí) had separate series; renumbering years
**TBV**. Always key on (part of town, čp.); parcel numbers are the most stable key.

## 4. Extraction schemas and pipeline

Common output structures (full versions in the overview page): map features
(`kind`, geometry in EPSG:5514, material stone/wood, label, house number, confidence),
views (viewpoint, landmarks matched to modern objects, fortification counts, legend),
siege plans (legend letters → objects, events), building events from text (address as
written → (part, čp.), event type built/rebuilt/extended/demolished/burned/renumbered/owner,
year range, certainty, ≤ 25-word evidence quote, source URL), address-book rows, street and
house-number gazetteer.

Pipeline: RÚIAN spine → street gazetteer from the Encyklopedie → vectorise georeferenced
epochs (1781, 1821, 1840, cadastre, 1864–1950, 1950s orthophoto) by colour segmentation and a
vision model → fit pre-1781 siege plans and views to the cadastre moat line (shape
validation only) → LLM event extraction from texts → merge into building / fortification
features with `valid_from` / `valid_to` ranges and provenance → animate layer by layer
(not raster cross-fades).

## 5. Fit with ca-geo

- LND-01 urban growth: a two-century calibration series for Plzeň (built-up extent per
  epoch) instead of only the five open-data plans noted in `plzen-opendata.md`.
- URB-03 (fire in a historic town, merged into HAZ-01): real pre-1800 block structure and
  building materials (stone / wood from the stable cadastre).
- A reconstruction archive itself is outside the engine scope; it would be a data product
  feeding demos. Licensing (ČÚZK cadastre mosaic, city aerials, archive content) is the main
  constraint, not technology.

## Open questions

- Licence for reuse of the city's `GIS_Historicke` rasters (rules point 4 says CC BY-SA 4.0
  for map services; services state nothing) and of the ČÚZK cadastre mosaic.
- Kriegsarchiv / AMP / SOA holdings of fortification plans; WLB 1620 plan digitisation.
- Plzeň house renumbering years and a concordance source.
- NPÚ JSON API (dating, defunct objects) or a bulk export on request.
