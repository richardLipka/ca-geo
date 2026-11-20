# Czech data gems for CA demos

A survey of Czech national open data that is **unusual, specific to Czechia and good for
visualisation** in ca-geo demos: inputs, drivers (time series), validation targets and
striking scenario material. It goes beyond `czech-national-catalogues.md`, which covers the
basic layers (DTM, ZABAGED, CORINE, flood zones, ČHMÚ station data), and
`plzen-opendata.md`, which covers one city. Model IDs refer to `docs/brainstorm/longlist.md`
and ADR 0001.

Done on 2026-11-20 with the machine interfaces of the catalogues. **Only metadata,
directory listings, HEAD requests and two byte-limited peeks** were used. No dataset was
downloaded or stored. Anything not seen directly is marked *to be verified*.

## 1. Method

### Interfaces used

| Interface | How it was used |
|---|---|
| NKOD SPARQL `https://data.gov.cz/sparql` | Case-insensitive substring search for ~200 Czech word stems over `dct:title`, `dcat:keyword` and `dct:description` (union). For the most promising datasets: publisher (`foaf:name`), `dct:accrualPeriodicity`, `dct:temporal`, `dct:spatial`, distributions (`dcat:downloadURL` / `accessURL`, `dct:format`, `dcat:mediaType`) and the terms of use (`podmínky-užití:specifikace`: copyrighted work, database as work, special database right, personal data) |
| ČÚZK Atom search `atom.cuzk.gov.cz/get.ashx?format=json&searchTerms=…` | 24 terms (historick, ortofoto, 3D, budovy, geografick, Geonames, Data250, DMR, digitální model, reliéf, ZABAGED, vrstevnice, císařsk, katastr, LOD, …). **The API returns at most 100 entries per query**, so it shows which products exist but cannot count map sheets |
| ČHMÚ `https://opendata.chmi.cz` | Directory listings (file names, counts, first and last file). One HEAD request for a file size |
| Other portals | Reachability (HTTP status) and landing pages: AOPK `data.aopk.gov.cz` (dataset pages with licence text), DIBAVOD, ŘSD traffic census, ÚHÚL, ČGS, HZS, agrigis.gov.cz |
| HEAD requests | `Content-Length` / `Last-Modified` of ~20 distributions (sizes in the tables below) |

### NKOD hit counts per keyword (distinct datasets matching title, keyword or description)

Short stems also match unrelated words (e.g. `sad` ⊂ "sada", `les ` ⊂ "… les …", `emis` ⊂
"komise", `sníh` ⊂ other words, `srážk` ⊂ "exekuční srážka"). Counts marked † are mostly
noise and were only skimmed.

| Group | Keyword: hits |
|---|---|
| Water | povodeň 21, povodn 32, záplav 39, srážk 61†, sníh 57†, sněh 16, rybník 10, mokřad 6, bobr 8 (no beaver data, only place names), vodní hladin 2, vodočet 0, podzemní vod 25, studán 6, pramen 25, průtok 39, hydrolog 43, sucho 10, povodí 88, nádrž 59, povodňov 28 |
| Hazards | lavin 1 (irrelevant), lavinov 0, sesuv 5, požár 1 (irrelevant), kalamit 2, hasič 5, zásah 5, evakuac 0, poddolov 3, eroz 34, vichřic 0, krupobit 0, tornád 0, blesk 0, bourk 0 |
| Ecology | kůrov 0, lesní 36, lesy 15, zvěř 17, srážky se zvěří 0, invazn 2, bolševník 1, pyl 0, včel 14, strom 35, zeleň 12, biotop 20, natura 2000 7, úses 13, honitb 17, škůdc 2, fenolog 1, porost 17, africk (mor) 0, vzteklin 0, ptačí chřip 0 |
| Land use and history | lpis 132, osev 4, plodin 28, chmel 6, vinic 81, bpej 15, půd 190†, důl 97†, dobývac 11, halda 1, výsypk 0, rekultivac 0, brownfield 2, zastavěn 21, územní plán 54, historick 174, stabilní katastr 0, císařsk 5, zanikl 7, letecké snímk 5, ortofoto 12, lidar 0, 3d 20, digitální model 10, sčítání lidu 5, 1869 1 |
| City and mobility | doprava 250†, dopravní 154†, intenzit 46, sčítání dopravy 2, nehod 37, cyklo 22, chodc 14, gtfs 3, jízdní řád 15, sdílen 9 (none on shared mobility), kolob 0, parkov 38, mobilit 19, detektor 30, dešťov 3, kanaliz 29 |
| Atmosphere and climate | vlhkost 22, teplot 74, hluk 40, ovzduší 199, imis 22, smog 3, inverz 0, meteorolog 236, klima 186, teplotní ostrov 0, oázy 7, satelit 4, sentinel 0, ndvi 0, copernicus 22, radar 24, fotovolt 1, větrn 9, ozon 18, radon 10 |
| Society | obyvatel 346†, hustot 23, migrac 34, stěhov 23, epidemi 19, nákaz 25, klíště 3, covid 71, sčítání 169, dojížď 15, mobilní data 0, telefon 118†, turist 66, návštěvnost 23, lyž 3, horská služba 1, izs 1, památ 81, hřbitov 12 |

8 798 distinct datasets matched at least one stem (inflated by the noisy stems). Among the
relevant matches (noisy stems removed), the most frequent publishers are ČHMÚ (173), ČSÚ
(150), Ministry of Agriculture (74), City of Brno (68), IPR Praha (64), City of Plzeň (62),
CENIA (54), Hradec Králové Region (51), Ministry of Health (50), Ministry of the Environment
(48), State Land Office (43), Ministry of Transport (38), VÚV TGM (32), City of Most (24),
AOPK (17) and ČGS (10).

### Licence notation used below

NKOD records terms of use per distribution. **CC BY 4.0** = copyrighted work or database
under CC BY 4.0 (attribution required). **"no rights"** = the record declares no
copyrighted work, no protected database, no special database right (free reuse without
conditions). Personal data are declared absent unless noted.

## 2. Top picks

Ranked by uniqueness × visual appeal × CA fit (author's judgement). Sizes come from HEAD
requests on 2026-11-20.

### 1. September 2024 flood extent (national)

| Field | Value |
|---|---|
| Publisher | VÚV TGM (data authored by ČHMÚ); a derived version with population and housing counts by ČSÚ ("Rozlivy povodní 2024") |
| URL | VÚV record `https://data.gov.cz/zdroj/datové-sady/00020711/645c19635fce959059d27a8f6c784bce`, SHP `https://heis.vuv.cz/data/webmap/datovesady/db/RozlivPovodne2024/vymezeni_rozlivu_povodne_09_24_SJTSK.zip` (2.3 MB). ČSÚ record `…/00025593/0e8668552e05bff1045273e948519b1c` (GPKG zip 3.5 MB; also SHP, GeoJSON, FGDB) |
| Format, extent | Polygons, S-JTSK; affected parts of Czechia (mainly the north-east and east) |
| Time | Event of September 2024; frequency OTHER / NEVER |
| Licence | VÚV: CC BY 4.0; ČSÚ: no rights |
| Enables | **WAT / HYD-02 validation** on a real, recent, nationwide event; ČSÚ attributes give exposed population for MOV-01 / evacuation demos |
| Visualisation | Replay a river reach (e.g. Opava, Bělá) with the observed hydrograph (pick 2) and overlay the mapped extent; Jaccard score live |
| Caveats | The record says the delineation is uncertain and prioritised the worst-hit places; only river overflow, not ponding |

### 2. ČHMÚ daily discharge archive back to 1887

| Field | Value |
|---|---|
| Publisher | ČHMÚ |
| URL | Record `https://data.gov.cz/zdroj/datové-sady/00020699/7dedcbb58e2edbea533b0b4cca445e43`; files `https://opendata.chmi.cz/hydrology/historical/data/daily/` (39 291 JSON files, one per station and year; 803 station IDs), hourly `…/data/hourly/` (12 358 files, earliest years 1905+), schemas in `…/historical/metadata/` |
| Format, extent | JSON, gauging stations in Czechia |
| Time | Earliest file `H_0-203-1-240000_DQ_1887.json` (1887) to 2025; updated annually |
| Licence | CC BY 4.0 |
| Enables | **WAT drivers** (inflow hydrographs) and validation of peak timing; long series for return-period scenarios |
| Visualisation | A "hydrograph scrubber": drag a timeline over 1890–2025 floods and watch the CA inundate the valley; side panel with the real gauge curve |
| Caveats | Which stations have hourly data for which events is to be verified; station coordinates come from the metadata files |

### 3. Radar precipitation composites (MERGE 1 h every 10 min, MAX_Z, PseudoCAPPI, ECHO_TOP)

| Field | Value |
|---|---|
| Publisher | ČHMÚ |
| URL | MERGE record `…/00020699/548562b969d1492e6371043b37b31aee`; files `https://opendata.chmi.cz/meteorology/weather/radar/composite/merge1h/hdf5/` (also `png/`), `…/composite/{maxz,pseudocappi2km,echotop,fct_maxz,fct_pseudocappi2km}/`; radar volumes per site (Brdy-Praha, Skalky) also in NKOD |
| Format, extent | HDF5 (ODIM), 1 × 1 km grid in EPSG:3857, whole of Czechia |
| Time | 10-minute step. **The directory is a rolling window**: 1 096 files from 2026-11-12 22:30 to 2026-11-20 13:00 on the day of the check |
| Licence | CC BY 4.0 |
| Enables | **WAT rainfall forcing** (pluvial and flash flood); new demo "rain-cell advection / nowcasting" (section 4) |
| Visualisation | Rain field sweeping across the map, feeding runoff in the CA underneath |
| Caveats | No historical archive in the open directory → keep our own copies of interesting events or find an archive (to be verified) |

### 4. Register of slope deformations (landslides, flows, rockfalls)

| Field | Value |
|---|---|
| Publisher | Czech Geological Survey (ČGS) |
| URL | Record `…/00025798/d5b5b634ca6f7480c971ed82d6696b48`; GeoJSON zip `https://od.geology.cz/svahove_deformace.zip` (22 MB); WFS; INSPIRE version `…/93fe704de97b37be797cdf531f602ed2` |
| Format, extent | GeoJSON polygons, mapped at 1 : 10 000, whole of Czechia |
| Time | Since 1976 (temporal start in the record); updated monthly |
| Licence | CC BY 4.0 |
| Enables | **HAZ-02 runout** source areas and validation (active / dormant / stabilised classes); rockfall variant |
| Visualisation | Release a mapped landslide body on the DTM and compare the runout with the mapped extent; national map of thousands of scars as an intro screen |
| Caveats | Number of records not counted (zip not opened) |

### 5. Undermined areas, mine openings and mining-waste dumps

| Field | Value |
|---|---|
| Publisher | ČGS |
| URL | Undermined areas `…/00025798/b75cdc8b648f5c99a7e1a8dfa239e21b` → `https://od.geology.cz/poddolovane_uzemi.zip` (1.1 MB); mine works and recorded collapses `…/2498e3343ea928eb374d534397f4d92a` → `dulni_dila.zip` (3.7 MB); abandoned mining-waste sites `…/d9976f5a790ff1883ed0b4c052824743` → `ium.zip` (1.1 MB) |
| Format, extent | GeoJSON, whole of Czechia |
| Time | Records since 1985 / 1998; updated weekly / monthly |
| Licence | CC BY 4.0 |
| Enables | HAZ-06 collapse sinkholes (mine openings with recorded collapses), LND-03 post-mining landscapes, HYD-09 (mine water), new "mining landscape" demo (section 4) |
| Visualisation | Kladno, Ostrava or Kutná Hora: shafts as points, undermined polygons as hatched hazard, a collapse CA spreading from weak cells |
| Caveats | The record says polygons may contain non-undermined parts |

### 6. Historical orthophoto of the 1950s (whole country)

| Field | Value |
|---|---|
| Publisher | CENIA (imagery from the military geographic office, processed by GEODIS) |
| URL | Record `…/45249130/68f8d82bd7337b69bd097ed41a8cefbf`; JPEG 2000 tiles `https://gis.cenia.cz/data/ortofotomap_historie/50.leta/`; WMTS / WMS; sheet index and "years of imaging" layers as separate datasets |
| Format, extent | JP2 raster, whole of Czechia |
| Time | Mostly 1952–1954, gaps filled with 1937–1970 and 1996 imagery |
| Licence | CC BY 4.0 |
| Enables | **LND-01 urban growth calibration** (1950s → today), LND-02 overgrowth, ECO-02 succession, river regulation (HYD-07) |
| Visualisation | Swipe slider 1953 ↔ today under a CA growth run starting from the 1950s built-up mask |
| Caveats | Built-up / forest masks must be digitised or classified; tile sizes not checked |

### 7. Population and houses in every municipality, censuses 1869–2011

| Field | Value |
|---|---|
| Publisher | ČSÚ |
| URL | Record `…/00025593/f9a50772981c2bb3237277fff76bd969`; CSV in zip `https://csu.gov.cz/docs/107516/0c242a34-ca97-0209-581f-dde18a20a25f/170240-17data.zip` (3.3 MB) |
| Format, extent | CSV, all municipalities, recalculated to the 2015 municipal structure |
| Time | Census years 1869–2011 (decennial) |
| Licence | no rights |
| Enables | LND-01 demand curves per municipality; new "settlement shrinkage" demo (borderland depopulation after 1945, section 4); EPI-01 historical populations |
| Visualisation | 140-year animated choropleth / dot map; CA allocating growth or loss to cells around each village |
| Caveats | Which census years are included in detail (e.g. 1930, 1950) is to be verified in the file |

### 8. 1 km population grid and commuting grid (Census 2021) + municipal commuting matrix

| Field | Value |
|---|---|
| Publisher | ČSÚ |
| URL | Population grid `…/00025593/33a742e51c1ac89c1a17008084e2412e` (GPKG zip 7.3 MB, also GeoJSON / FGDB); commuting grid `…/f49fa184c6e04736b22b7c66952833ba`; municipality-to-municipality commuting `…/1fde1d5e15b699c2618af512e4826dc7` (CSV `dojizdka_obce.csv`) |
| Format, extent | 1 km grid polygons, whole of Czechia |
| Time | 26 March 2021; NEVER updated |
| Licence | no rights |
| Enables | **MOV-03** population weighting, EPI-01 SIR on a real grid, ATM-01 exposure; commuting links as long-range contacts |
| Visualisation | SIR epidemic on the 1 km grid with commuting "jumps" drawn as arcs |
| Caveats | Census grid suppresses small counts (to be verified) |

### 9. Present population from mobile-operator data (Brno and South Moravia)

| Field | Value |
|---|---|
| Publisher | City of Brno (Vodafone data) |
| URL | Record `https://data.gov.cz/zdroj/datové-sady/44992785/a50ba0116b8f39e1412ec27d70357aee` |
| Format, extent | CSV daily matrices of present population per basic settlement unit (ZSJ) and municipality of the South Moravian Region |
| Time | Two weeks: 20–26 Sept 2021 and 4–10 Oct 2021; time intervals within the day |
| Licence | CC BY 4.0 (work); database: no rights |
| Enables | New "diurnal population tide" demo (section 4); MOV-01 / MOV-03 time-of-day exposure |
| Visualisation | A 24-hour loop: the city "breathes" — people flow into the centre in the morning and out in the evening |
| Caveats | Download URL in the catalogue is an ArcGIS item with an embedded token (not reproduced here; may expire); unique in NKOD — no other mobile-data set found |

### 10. Wolf: areas of repeated occurrence (two time snapshots) and large-carnivore habitat

| Field | Value |
|---|---|
| Publisher | AOPK ČR |
| URL | `https://data.aopk.gov.cz/ds/107` (valid from 1 Feb 2026) and `https://data.aopk.gov.cz/ds/109` (valid until 31 Jan 2026, with sub-periods to 9 Jul 2024 / from 10 Jul 2024); habitat of wolf, lynx, bear, elk: NKOD `…/62933591/5ced61eb2287d75d67412f84de45df29` = `data.aopk.gov.cz/ds/53` |
| Format, extent | ESRI shapefile (S-JTSK); CSV / GeoJSON / KML for the habitat layer; whole of Czechia |
| Time | Snapshots 2024 → 2026; habitat layer 2021 |
| Licence | CC BY 4.0, attribution "(c) AOPK ČR" |
| Enables | **EPI-04 population dispersal** — the wolf's return to Czechia as a real colonisation front; habitat layer = carrying capacity and corridor barriers |
| Visualisation | Wolf packs spreading from the borders over the habitat map; compare simulated occupancy with the two official snapshots |
| Caveats | The layer is a compensation zone derived from NDOP records, not raw occurrences; raw finds (NDOP, `ds/19`) are under separate licence terms (CC BY-SA noted) and access was not tested |

### 11. American foulbrood outbreaks in apiaries

| Field | Value |
|---|---|
| Publisher | State Veterinary Administration (SVS) |
| URL | Record `https://data.gov.cz/zdroj/datové-sady/00018562/1107913523`; XML feed `https://www.svscr.cz/public/opendata/mvp.php` |
| Format, extent | XML: case ID, outbreak start / end dates, point geometry (WKT, WGS 84), measures, zones; whole of Czechia |
| Time | Since 2022-01-01; updated daily |
| Licence | no rights |
| Enables | New "apiary disease spread" demo (section 4); template for EPI-02 / EPI-05 style containment zones |
| Visualisation | Outbreak points lighting up month by month, with protection zones as rings; a contact CA over apiary density |
| Caveats | **The feed contains beekeepers' names in free-text fields despite the "no personal data" declaration** — use only dates and geometry |

### 12. Crop declarations on every LPIS field block 2015–2026

| Field | Value |
|---|---|
| Publisher | Ministry of Agriculture |
| URL | Record `…/00020478/bd5c35af2e35309af0eae546715aa2f7`; `https://agrigis.gov.cz/download/lpis/plodiny/Plodiny_tabulkova_data_2015-2026.zip` (511 MB) |
| Format, extent | XLSX tables per year keyed to LPIS field-block parts (geometry from LPIS, also in NKOD); whole of Czechia |
| Time | 2015–2026, state at 1 August; annual |
| Licence | no rights |
| Enables | **HYD-05 erosion** (crop cover factor per field and year), ECO-09 crop pest spread over a rotating mosaic, ATM-04 drought |
| Visualisation | The field mosaic changing colour year by year; muddy-flood run on the same slope with maize vs. wheat |
| Caveats | Large; tables must be joined to LPIS geometry |

### 13. Phenological observations (forest trees and herbs)

| Field | Value |
|---|---|
| Publisher | ČHMÚ |
| URL | Record `…/00020699/6da5ae4c739245bc9364d2f3443a1feb`; `https://opendata.chmi.cz/meteorology/phenology/wood_species/data/` (19 CSV files, one per species, e.g. `Buk_lesni.csv`, `Borovice_lesni.csv`, `Trnovnik_akat.csv`) and `…/herbs/` |
| Format, extent | CSV per species, phenological stations in Czechia |
| Time | Not read (to be verified) |
| Licence | CC BY 4.0 |
| Enables | New "spring green-up wave" demo (section 4); ECO-07 range shift; ECO-01 beetle swarming timing |
| Visualisation | Leaf-out front climbing from lowlands to mountains, driven by degree-days from station temperatures |
| Caveats | Station coordinates and series lengths to be verified |

### 14. Weekly snow water equivalent and snow depth grids

| Field | Value |
|---|---|
| Publisher | ČHMÚ |
| URL | Record `…/00020699/e60b78ccf3f1078a7679f464f4531f93`; `https://opendata.chmi.cz/hydrology/product/data/snow/` (71 files: `SNOW_SWE_YYYYMMDD.zip`, `SNOW_SD_…zip`, `SNOW_AREA_…csv`) |
| Format, extent | GeoTIFF (zipped), whole of Czechia |
| Time | Weekly (Mondays), November–April; listing covered Feb 2025 – Apr 2026 |
| Licence | CC BY 4.0 |
| Enables | **HYD-06 snowmelt** initial state; L6 chain (snowmelt + rain → flood) |
| Visualisation | Snowpack shrinking week by week in the Krkonoše; melt water routed by the WAT kernel |
| Caveats | Only recent seasons in the directory |

### 15. Flash-flood risk product + critical points of torrential runoff

| Field | Value |
|---|---|
| Publisher | ČHMÚ (risk product); VÚV TGM (critical points) |
| URL | ČHMÚ record `…/00020699/9b596d03dd10af94988212afbb552efc` → `https://opendata.chmi.cz/hydrology/product/data/flash_flood/` (`risk_FF_web.json`, `rsraz_exp_web.json`, `un_exp_web.json`: risk, dangerous precipitation, saturation); VÚV record `…/00020711/f64a6ec9431cee484660d4492a3673aa` → `KritBody.zip` (11.6 MB) |
| Format, extent | GeoJSON (ČHMÚ, continuously updated); SHP (VÚV) — whole of Czechia |
| Time | ČHMÚ continuous; VÚV temporal 2009–2026 |
| Licence | CC BY 4.0 (both) |
| Enables | **HYD-03 flash flood**: critical points = outlets of small catchments threatening villages; saturation as initial soil state |
| Visualisation | Click a village's critical point → its contributing area lights up and a cloudburst runs down to the village edge |
| Caveats | ČHMÚ files are current state only (no archive seen) |

### 16. Prague climate suitability maps (ventilation, calm, airflow speed)

| Field | Value |
|---|---|
| Publisher | IPR Praha |
| URL | e.g. ventilation `…/70883858/10c73ad7125ba20cdef0f937de10dfe9`, calm `…/70883858/29a17dae925b4491f23409312fd7841d`; sibling layers for sunshine, built-up share, air pollution and an overall "Bonita klimatu" |
| Format, extent | Vector (converted from a 25 m raster), FGDB / GeoJSON / KML / CSV / ArcGIS service; Prague |
| Time | Update 2008 |
| Licence | CC BY 4.0 (work); database: no rights |
| Enables | **ATM-02 cold-air pooling** qualitative validation (calm and poorly ventilated valleys), URB-01 heat island context |
| Visualisation | Night-time cold-air CA over Prague's DTM, with the expert ventilation map as a toggle |
| Caveats | Expert / modelled map from 2008, not measurements |

### 17. Buildings of old Most (1938), the town demolished for coal

| Field | Value |
|---|---|
| Publisher | City of Most |
| URL | Record `…/00266094/56c172296efd2ae5389a6a3d82dc0f4b`; SHP / GeoJSON / CSV / KML via `opendata.mesto-most.cz` |
| Format, extent | Building polygons vectorised from the 1938 town plan; Most |
| Time | 1938 |
| Licence | no rights |
| Enables | URB-03 fire in a historic town on a real vanished street pattern; new "open-pit mine advance" demo (section 4) together with picks 5 and 6 |
| Visualisation | The old town appearing on today's lake / mine landscape, then consumed cell by cell by the advancing pit |
| Caveats | Unique local story; scale is one town |

### 18. Lost paths from the Imperial cadastre and the Second Military Survey

| Field | Value |
|---|---|
| Publisher | IPR Praha |
| URL | Prague `…/70883858/42870d3461a3435fa4bb847787490bbb`; metropolitan area in Central Bohemia `…/70883858/5959e74f2bfb7d8308e8ae2793548dff` |
| Format, extent | Lines (GeoJSON, SHP, FGDB, CSV); Prague and surroundings |
| Time | State of the 19th century vs. today |
| Licence | CC BY 4.0 (work) |
| Enables | New "trail formation / desire paths" demo (section 4); LND history |
| Visualisation | Walkers wear paths into a field; compare with 19th-century paths that disappeared |
| Caveats | Positions approximate (the record says the Second Military Survey is imprecise) |

### 19. Brno hydrogeology: rivers before regulation, groundwater flow direction, contamination

| Field | Value |
|---|---|
| Publisher | City of Brno ("Georizika" series, ~15 layers) |
| URL | Rivers before regulation `…/44992785/b89d42482ba98cf6838eba08c4159fe6`; groundwater flow direction `…/44992785/d72a24d0ceeb13cb7c015c6b9eb5d05f`; further: soil contamination, transit groundwater contamination, unsuitable infiltration, landfills, flood risk |
| Format, extent | GeoPackage / SHP / GeoJSON / DXF; Brno |
| Time | Updated annually |
| Licence | CC BY 4.0 (work) |
| Enables | HYD-07 channel history (Svratka, Svitava, Ponávka), **HYD-09 groundwater** with a contaminant-plume variant, URB-02 infiltration constraints |
| Visualisation | Old meanders under the modern straightened river; a contaminant plume drifting along the mapped flow arrows |
| Caveats | Old channel courses are approximate (record) |

### 20. Ecoducts with effectiveness ratings and river migration barriers

| Field | Value |
|---|---|
| Publisher | AOPK ČR |
| URL | Ecoducts `https://data.aopk.gov.cz/ds/146` (updated 2025-12-01); migration barriers on rivers `https://data.aopk.gov.cz/sds/8` (dams, weirs, passable objects, small hydro, 2017) |
| Format, extent | ESRI shapefile, whole of Czechia |
| Time | 2017 / 2025 |
| Licence | CC BY 4.0 |
| Enables | **ECO-04 connectivity** (road crossings rated per animal category A–G), EPI-04 barriers; new "fish passage on the river network" demo |
| Visualisation | Animal dispersal blocked by motorways; toggle ecoducts on/off and see the population reconnect |
| Caveats | Rating categories need a mapping to permeability values |

### 21. Land-cover time series: CORINE 1990–2024 and Copernicus imperviousness

| Field | Value |
|---|---|
| Publisher | CENIA |
| URL | CLC 2024 `…/45249130/f4aab2b16f677692a583291a738ec6f0` → `https://geoportal.gov.cz/atom/corine_land_cover/CLC_CZ_2024_epsg5514.gpkg` (144 MB); change layer 2018–2024 and older years also in NKOD; HRL imperviousness `…/45249130/6f7456e2bc49cc4ec35fa7d7b033ceee` → e.g. `IMD_2009_020m_CR.tif` (493 MB), 2006 / 2009 / 2012 layers and change layers |
| Format, extent | GeoPackage (25 ha MMU); GeoTIFF 20 m / 100 m; whole of Czechia |
| Time | CLC 1990, 2000, 2006, 2012, 2018, **2024**; imperviousness from 2006 (record temporal 2018) |
| Licence | CC BY 4.0 |
| Enables | **LND-01** calibration over 34 years; URB-02 imperviousness as infiltration input |
| Visualisation | Suburban rings around Prague growing between CLC snapshots vs. the CA |
| Caveats | CLC MMU 25 ha is coarse for towns |

### 22. Smog situation history and the ISKO air-quality archive 1969–2025

| Field | Value |
|---|---|
| Publisher | ČHMÚ |
| URL | Smog record `…/00020699/f3eff063797d9a36137b74658e890e37` → `https://opendata.chmi.cz/air_quality/historical/smog/`; archive `https://opendata.chmi.cz/air_quality/historical/OpenISKO_1969_2025.zip` (895 MB); precipitation chemistry `…/historical/precipitation/Data_precipitation_1976_2025.zip`; emissions `…/historical/emissions/year_2022–2024.zip` |
| Format, extent | CSV; stations in Czechia |
| Time | Smog declarations since 2009-11-19 (continuous); measurements from 1969 |
| Licence | CC BY 4.0 |
| Enables | **ATM-01** validation of winter episodes (Ostrava basin), ATM-02 + ATM-01 coupling (inversion traps emissions) |
| Visualisation | Calendar of smog episodes; pick one and run dispersion under a cold-air lid |
| Caveats | ISKO zip is large — fetch station subsets instead (structure to be verified) |

### 23. Historical flood extents: Prague 2013 (and Plzeň 2002 / 19th century)

| Field | Value |
|---|---|
| Publisher | IPR Praha (2013); City of Plzeň (see `plzen-opendata.md`) |
| URL | `…/70883858/9352b87581e1979fa15a949ba3523599` (GeoJSON, SHP, FGDB, CSV, KML, ArcGIS service) |
| Format, extent | Polygons; Prague |
| Time | June 2013 event |
| Licence | CC BY 4.0 (work) |
| Enables | WAT validation for the Vltava in Prague; with Prague's mobile flood barriers (`Protipovodňová ochrana`, incl. sandbag lines) as scenario |
| Visualisation | 2013 flood replay with and without the mobile barriers |
| Caveats | Discharge forcing from pick 2 (Vltava gauges) |

### 24. Giant hogweed occurrences (Liberec Region)

| Field | Value |
|---|---|
| Publisher | Liberec Region |
| URL | Record `…/70891508/e518bef1e2670dd378bc95eb1dddba3b` (FGDB, GeoPackage, KML and 8 other formats via datalk.cz) |
| Format, extent | Points of stands and individual plants; Liberec Region |
| Time | Points since 2023 (mapping since 2021); annual |
| Licence | no rights |
| Enables | **ECO-03 invasive spread** along streams with real occurrence points (only invasive-plant occurrence set found in NKOD) |
| Visualisation | Hogweed creeping down a valley from mapped seed stands; eradication scenario |
| Caveats | Regional only |

## 3. Further notable datasets by theme

Shorter rows; all records are in NKOD unless stated. "Rec." = NKOD dataset IRI suffix
(`https://data.gov.cz/zdroj/datové-sady/<suffix>`).

### Water

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| Dams (Hráze), weirs, in-channel objects, reservoirs | Ministry of Agriculture (ISVS VODA) | SHP `https://voda.gov.cz/data/ISVSVoda_Hraze.zip` (1.7 MB), `…_Vodninadrze.zip` (0.1 MB) | continuous / annual | no rights | HYD-04 pond cascade breach (real dam positions) |
| Historical drainage (meliorace) | Ministry of Agriculture | SHP (digitised analogue maps) | never updated | no rights | HYD-01 / HYD-09 hidden drainage, ATM-04 |
| Drainage structures by region (points / lines) | State Land Office | per region | — | to be verified | as above |
| Flood hazard / risk maps (FD) | VÚV TGM | vector | — | to be verified | WAT validation (depth classes per return period) |
| Groundwater levels and spring yields | ČHMÚ | `hydrology/groundwater/historical/data/` (JSON per object and year, e.g. from 1959) | annual | CC BY 4.0 | HYD-09 validation |
| Watershed divides 1st–4th order, sub-basins | ČHMÚ | vector | — | CC BY 4.0 (to be verified) | catchment masks for WAT / HYD-05 |
| Drought state (HAMR) | ČHMÚ | — | — | to be verified | ATM-04 driver |
| Wetlands of national / international importance | AOPK | SHP `https://data.nature.cz/ds/97/download` | 1999–2016 | CC BY 4.0 | ECO-05 beaver / wetland targets |
| Framework floodplain delineation | AOPK | `data.aopk.gov.cz/sds/18` | — | CC BY 4.0 (to be verified per item) | HYD-02 natural floodplain vs. regulated |
| Prague "cold oases": springs, fountains, misting points, bathing sites | IPR Praha | GeoJSON etc. | — | CC BY 4.0 | heat-refuge accessibility (section 4) |
| Flood gauges, rain gauges (Jihlava; Ústí Region flood sensors) | cities / region | live | — | per record | local WAT validation |

### Hazards

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| Radon index map 1 : 50 000 | ČGS | GML via Atom | — | CC BY 4.0 | context only (not CA) |
| Protected deposit areas, mining leases | ČGS / Czech Mining Office | vector | — | to be verified | mining scenarios |
| Contaminated sites (SEKM) | Ministry of the Environment | CSV `https://data.mzp.cz/datasets/dataset/sekm/mzp_kontaminovana_mista.csv` (2.0 MB) | weekly | no rights | HYD-09 plume sources |
| Damage to transport infrastructure from climate events | CENIA (indicator) | CSV | annual | no rights | storyline numbers only |
| Salvage felling by cause (wind, insects, snow, ice, drought) | CENIA (indicator) | CSV | annual | no rights | ECO-01 / HAZ-04 national context (no maps) |
| Alarm sirens (Most) | City of Most | vector | — | to be verified | MOV-01 warning coverage |
| Brno geohazards (complex foundation, neogene waters, landfills) | City of Brno | vector | annual | CC BY 4.0 | urban hazard overlays |

### Ecology

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| Grid mapping cells (KFME ~11 × 12 km and subdivisions) | AOPK | SHP `https://data.nature.cz/ds/30/download` (65 KB) | — | CC BY 4.0 | common grid for atlas-style species data (ECO-07) |
| Consolidated ecosystem layer | AOPK | `data.aopk.gov.cz/sds/17` | 2013– | CC BY 4.0 (to be verified) | habitat suitability for EPI-04 / HAZ-01 fuels |
| Habitat mapping (biotopes) | AOPK | `sds/7` | — | to be verified | habitat classes |
| Biogeographic division (366 biochores) | AOPK | `ds/29` | — | to be verified | climate / vegetation zoning |
| Game counts and culls by species | ČSÚ | CSV / JSON `https://data.csu.gov.cz/opendata/sady/LES020215/distribuce/csv` | 2015–2025, annual | no rights | EPI-02 wild boar densities (national / regional only) |
| Game damage by hunting ground (LČR) | Lesy ČR | — | — | to be verified | browsing pressure |
| Forest species composition, dead wood, clear-cut structure | CENIA (indicators) | CSV | annual | no rights | national context for ECO-01 (no maps) |
| HRL forest, grassland, small woody features, riparian zones | CENIA | raster | — | CC BY 4.0 (to be verified) | fuels, hedgerow corridors (ECO-04) |
| Memorable trees + buffer zones | AOPK; cities | vector | — | CC BY 4.0 (AOPK, to be verified) | ECO-09 urban hosts |
| Brno green passport (trees and shrubs) | City of Brno | vector | — | to be verified | ECO-09 urban host map (cf. Plzeň tree passport) |
| Bee colonies (Prague forest apiaries) | IPR Praha | vector | — | to be verified | with pick 11 |

### Land use and history

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| Data50 / Data250 digital geographic models | ČÚZK (Atom) | zip `openzu.cuzk.gov.cz/opendata/Data50/epsg-3045/data50.zip` (757 MB), Data250 (320 MB) | — | no conditions (ČÚZK) | coarse national demos without ZABAGED |
| Geographic names (GEONAMES) | ČÚZK (Atom) | GPKG zip 37 MB, FGDB 26 MB (2026-10-30) | — | as above | labelling in demos |
| ZABAGED national file | ČÚZK (Atom) | FGDB 4.1 GB, GPKG 6.7 GB (2026-10-04, ETRS89-TM33) | — | as above | these are zip sizes from the Atom feed; `czech-national-catalogues.md` gives larger figures (possibly unpacked) — to be reconciled |
| RÚIAN historical change data | ČÚZK (Atom) | XML zip per municipality | — | as above | boundary changes for long time series |
| BPEJ soil-ecological units by region | State Land Office | per region | — | to be verified | HYD-05 erodibility / infiltration |
| Soil map 1 : 50 000 (INSPIRE) | ČGS | GML / WMS | — | no rights | HYD-05, HYD-01 infiltration |
| Geological map 1 : 500 000 | ČGS | INSPIRE | — | to be verified | HYD-09 permeability classes |
| Brownfields (Liberec Region, Moravian-Silesian Region) | regions | vector | — | to be verified | LND-01 redevelopment scenario |
| Prague 3D photorealistic mesh; Ostrava 3D buildings LOD 2.3; Brno DSM and box model | IPR Praha; Ostrava; Brno | mesh service; SHP / DGN zip; raster | — | CC BY 4.0 (Prague work, Ostrava) | MOV-01, URB-02, URB-03 3D context |
| Valuable post-war housing estates (Prague) | IPR Praha | vector | — | to be verified | LND-01 era layers |

### City and mobility

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| National timetables (bus lines, rail) — CIS JŘ | Ministry of Transport | JDF (CSV-like) zip `https://portal.cisjr.cz/pub/JDF/JDF.zip` (106 MB) | 3× weekly | no rights | MOV-03 national accessibility (needs JDF → GTFS conversion) |
| GTFS: PID Prague, PMDP Plzeň; IDS JMK routes | ROPID; Plzeň; Brno | GTFS | continuous | per record | MOV-03 urban |
| Prague bike counters (Golemio API) | Operátor ICT | API `https://api.golemio.cz` | 2018–, continuous | no rights | validation of flows (API key needed — to be verified) |
| "Bike to work" counts per street segment 2018–2022 | City of Brno | ArcGIS service, XLS | annual campaign | CC BY 4.0 | cyclist flow maps |
| Traffic intensity pentlograms 2016– (vehicles, cyclists, trams, buses) | City of Brno | GPKG / DXF | annual | CC BY-SA 4.0 | ATM-01 road emissions, MOV-02 |
| Pedestrian accidents since 2010; all accidents | City of Brno | GPKG | annual | CC BY 4.0 | MOV-01 risk context |
| Speed cameras, bike counters, accidents (Most) | City of Most | vector + CSV | — | to be verified | local MOV-02 |
| PID operational disruptions | ROPID | RSS | live | CC BY | live "network disruption" scenario for MOV-03 |
| Prague noise maps (day / night, road traffic, 2010) | IPR Praha | GeoJSON | 2010 | CC BY 4.0 | ATM-06 context (out of scope) |
| Green roofs subsidised since 2018; rain-water retention projects | City of Brno | GeoJSON | annual | CC BY 4.0 | URB-02 / URB-01 intervention scenarios |

### Atmosphere and climate

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| 10-minute station data (temperature, humidity, wind, precipitation, radiation, pressure, sunshine) | ČHMÚ | JSON `meteorology/climate/historical/data/10min/`, CSV `historical_csv/data/10min/` | yearly folders from 2018 (CSV temperature) | CC BY 4.0 | ATM-02 night cooling, HAZ-01 wind |
| Daily station data incl. snow, soil temperature, evaporation | ČHMÚ | CSV `historical_csv/data/daily/` | long series | CC BY 4.0 | HYD-06, ATM-04 |
| Climate normal grids 1991–2020 (temperature, precipitation, sunshine; monthly and annual) | ČHMÚ | GeoTIFF 1 km, EPSG:32633 | — | CC BY 4.0 | ECO-07 climate envelope, EPI-03 |
| ALADIN NWP 1 km and 2.3 km | ČHMÚ | GRIB2 bz2, runs 00/06/12/18 | rolling | CC BY 4.0 (to be verified per dataset) | HAZ-01 wind / humidity forcing |
| Precipitation forecast maps from the September 2024 flood onward | ČHMÚ | `meteorology/floods/` — 28 440 PNG (`floods_prec24h_YYYYMMDDHH+NN.png`) from 2024-09-11 to 2026-11-20 | 6-hourly runs | CC BY 4.0 (to be verified) | storytelling for the 2024 flood (images, not data) |
| Satellite images (geostationary channels, polar) | ČHMÚ | JPG per 15 min, rolling (2 402 files in `geo/ir108/`) | rolling | to be verified | backdrops |
| Radiosoundings Praha-Libuš, Prostějov; ozone profiles | ČHMÚ | — | recent | CC BY 4.0 (to be verified) | inversion height for ATM-02 / ATM-01 |
| Tick activity forecast map (days 1–3) | ČHMÚ with SZÚ | PNG (`forecast_maps_bio/now_/kliste_1.png`) | daily | CC BY 4.0 | EPI-03 comparison (image only) |
| Wind direction frequency per station (annual) | ČHMÚ | CSV | — | to be verified | ATM-01 wind roses |
| City sensor networks (Olomouc meteo, Brno mobile air-quality stations, Bohumín) | cities | various | — | per record | local ATM validation |

### Society

| Dataset | Publisher | Access / format | Time | Licence | Use |
|---|---|---|---|---|---|
| Population movement (births, deaths, migration) per municipality | ČSÚ | CSV per year (2014–2018 seen) | annual | no rights | LND-01 / settlement shrinkage drivers |
| Census 2021 by municipality, ZSJ; DEGURBA classification | ČSÚ | GPKG / CSV | 2021 | no rights | context layers |
| Infectious diseases by region, month, age, ICD-10 | Ministry of Health / ÚZIS | CSV (30 MB) | 2018–2025 | CC BY 4.0 | EPI-01 regional curves (too coarse for cells) |
| COVID-19 epidemiological characteristics of municipalities | Ministry of Health | CSV | 2020– | to be verified | EPI-01 validation on municipal level |
| Accommodation occupancy by tourist region | ČSÚ | CSV | monthly / quarterly | no rights | seasonal population for MOV / EPI |
| Cultural monuments; UNESCO buffer zones | NPÚ | vector | — | to be verified | URB-03 historic-town selection |

## 4. New phenomena and demo ideas not in the longlist

| Idea | Mechanism (CA family) | Data | What the user would see |
|---|---|---|---|
| **Diurnal population tide** | Mass-conserving redistribution between home and work cells driven by an hourly schedule | Brno mobile data (pick 9), commuting grid (pick 8) | The city "breathing" over 24 h; flood or evacuation risk changing with the hour |
| **Apiary disease spread (American foulbrood)** | Stochastic contact spread on apiary density with zone controls (like EPI-05) | SVS outbreaks (pick 11) | Outbreaks igniting along flight ranges; 3 km protection rings stopping or failing |
| **Spring green-up wave** | Degree-day accumulator per cell (local rule + temperature field from elevation) | Phenology (pick 13), climate normal grids, DTM | A green front sweeping uphill in April–May, earlier in warm basins |
| **Rain-cell advection nowcast** | Advection of a scalar field by an estimated motion vector (semi-Lagrangian CA) | Radar MERGE / MAX_Z (pick 3) | A storm cell moving and decaying; compare with the next real radar frame |
| **Settlement shrinkage (borderland depopulation)** | Inverse urban growth: abandonment probability from neighbourhood decline | Census 1869–2011 (pick 7), 1950s orthophoto (pick 6) | Villages emptying and fields overgrowing after 1945 (link to LND-02) |
| **Open-pit mine advance and town relocation** | Front propagation along a lease boundary + land-use replacement + post-mining lake filling | Old Most (pick 17), mining leases, undermined areas (pick 5), 1950s orthophoto | A town disappearing into the pit, later a lake (link to LND-03) |
| **Trail formation (desire paths)** | Active-walker model: walkers deposit "trampling", paths attract walkers | Lost paths (pick 18), parks and road graph | Paths emerging in a park; historical paths as reference |
| **Groundwater contaminant plume** | Advection–dispersion on the HYD-09 head field | Brno flow directions and contamination (pick 19), SEKM sites | A plume drifting from an old landfill towards wells |
| **Fish passage on the river network** | Dispersal on a river graph with barrier permeabilities | AOPK river barriers (pick 20), ISVS dams and weirs | Upstream colonisation stopping at weirs; removing a weir reopens the river |
| **Heat-refuge accessibility** | MOV-03 front from cold oases on the street graph, weighted by heat | Prague cold oases, population grid | Walking minutes to the nearest fountain / spring on a hot day |

## 5. Gaps (searched, not found)

| Searched for | Result |
|---|---|
| Bark-beetle (kůrovec) maps | 0 NKOD hits; only national salvage-felling indicators (CENIA). Forestry portals: ÚHÚL not reachable during the check; other bark-beetle portals not reachable or redirecting — to be verified |
| Wildfire / fire-service records (požár, HZS, zásah, IZS) | No fire event data in NKOD (1 irrelevant hit for požár); only fire-station locations (Hradec Králové Region). HZS website reachable; statistics not checked |
| Avalanches, mountain rescue | 0 avalanche hits; only mountain-rescue station locations (Jeseníky) |
| Evacuation, extreme weather events (hail, tornado, lightning, storms) | 0 hits |
| Animal diseases besides foulbrood (African swine fever, rabies, avian influenza) | 0 hits; SVS publishes only foulbrood and trichinella sampling points in NKOD |
| Wildlife–vehicle collisions (srážky se zvěří) | 0 hits |
| Pollen, ticks as data | No pollen data; ticks only as forecast images |
| Beaver occurrences | 0 (hits are place names); possibly inside NDOP raw finds (access not tested) |
| Satellite products (Sentinel, NDVI) | 0 national hits; only Plzeň's satellite set |
| National road traffic census (ŘSD) | Not in NKOD; `scitani.rsd.cz` is reachable (JavaScript application) — download format and licence to be verified |
| National GTFS | Not available; national timetables only in JDF format (Ministry of Transport) |
| Shared mobility, scooters (sdílen, kolob) | 0 relevant |
| Mobile-phone data at national scale | Only the Brno / South Moravia two-week set |
| POVIS (flood information system) data | Only a "request to open data" record (`…/podněty-na-data-k-otevření/R59`, promised for 2026-01-01), not a dataset |
| Imperial cadastre (Císařské otisky) as raster | Not in NKOD or ČÚZK Atom search; only derived "lost paths" layers (IPR Praha) |
| LiDAR keyword, 3D in ČÚZK Atom | 0 hits for "lidar", "3D", "3D budov", "LOD" (as a product); DMR 4G / 5G and DMP exist (per map sheet) |
| DMR 4G format | A DMR 4G sheet (`DMR4G/epsg-5514/AS01.zip`) is only 186 KB, which suggests a gridded product rather than a point cloud — **to be verified** (archive not opened) |
| Urban heat island measurements | 0 for "teplotní ostrov"; only Plzeň satellite LST and Prague expert climate maps |
| Long radar archive | Open directory keeps ~8 days only |
