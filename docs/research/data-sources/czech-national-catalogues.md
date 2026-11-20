# National open-data catalogues of the Czech Republic — usability for ca-geo

Overview of country-wide open-data catalogues and sources for configuring the selected CA
models anywhere in Czechia. Checked 2026-11-20 by querying the catalogues' machine
interfaces (NKOD SPARQL, ČÚZK Atom search, ČHMÚ directory listings). Items not checked
are marked "to be verified". Complements `plzen-opendata.md` (a city catalogue).

## Catalogues

| Catalogue | URL / interface | What it is | Verified |
|---|---|---|---|
| **NKOD** — National Open Data Catalogue | https://data.gov.cz, SPARQL endpoint `https://data.gov.cz/sparql`, DCAT-AP-CZ | Central catalogue harvesting local catalogues of ministries, agencies, regions and cities; **30 373 datasets** on 2026-11-20. Plzeň's catalogue is harvested (150 of its 153 datasets) | yes |
| **ČÚZK open data** (Atom download services) | https://atom.cuzk.gov.cz, search API `get.ashx?format=json&searchTerms=…`, files on `openzu.cuzk.gov.cz` and `services.cuzk.gov.cz` | National geodata of the surveying office; **not in NKOD** (searched titles for DMR / ZABAGED: 0 hits). Rights stated as "no conditions apply" | yes |
| **ČHMÚ open data** | https://opendata.chmi.cz (directory listing) | Meteorology, hydrology, air quality; also listed in NKOD | yes |
| **National INSPIRE geoportal** (CENIA) | https://geoportal.gov.cz, CSW catalogue | Metadata of spatial data of all public bodies (INSPIRE themes) | reachable; content to be verified |
| Sectoral portals | DIBAVOD (https://www.dibavod.cz), AOPK (https://data.aopk.gov.cz), ÚHÚL forestry geoportal | Water bodies / catchments, nature protection, forest management data | DIBAVOD and AOPK reachable; ÚHÚL not reachable during the check; licences to be verified |
| EU level | data.europa.eu (harvests NKOD), Copernicus Land Monitoring Service | European datasets (CORINE, Urban Atlas, HRL, EU-DEM / Copernicus DEM) | to be verified (Copernicus portal did not respond during the check) |

Largest NKOD publishers (by dataset count) are statistical, municipal-register and
regional catalogues; for ca-geo the relevant ones are ČSÚ, ČHMÚ, CENIA, the Ministry of
the Environment, the Ministry of Agriculture, regions and the City of Prague.

## Key national data for the selected models

| Need | Source | Format / size | Terms | Models |
|---|---|---|---|---|
| **Terrain (DTM)** | ČÚZK **DMR 5G** and **DMR 4G** (Atom, per SM5 map sheet, S-JTSK) | LAZ point clouds (ground) — must be gridded offline (e.g. to 1–5 m) | "no conditions apply" | WAT, ATM-02, HAZ-01, HAZ-02, HYD-05, MOV-03 |
| **Surface model (DSM)** | ČÚZK **DMP 1G** (per map sheet, S-JTSK) | LAZ | as above | pluvial flooding with buildings, cold air in towns, evacuation |
| **Topographic database** | ČÚZK **ZABAGED** (whole country; also contours per map sheet) | GeoPackage ≈ 12.5 GB, FGDB ≈ 8 GB (S-JTSK and ETRS89-TM33); contours SHP per sheet | as above | land cover / roads / water network / buildings for all models (SC-RECLASS, SC-RASTERIZE) |
| Orthophoto | ČÚZK orthophoto (per map sheet, 2025) | JPEG tiles | as above | visual base layer, digitising |
| Buildings, parcels, addresses | ČÚZK INSPIRE buildings / cadastral parcels (per municipality / cadastre), cadastral maps (SHP / DXF / DGN / VFK), RÚIAN | GML, SHP, CSV | as above | MOV-01, URB-03, LND-01 |
| **Land cover** | CENIA (in NKOD): **CORINE Land Cover** CZ 1990, 2000, 2006, 2012, 2018 + change layers; **Urban Atlas**; Copernicus High Resolution Layers (e.g. small woody features) | vector / raster | CC BY 4.0 / CC0 (per dataset) | LND-01 (history for calibration), HAZ-01 fuels, ATM-02, EPI-04 habitat |
| **Flood zones** | NKOD: flood zones of major rivers, Q5 / Q100 for regions and Prague (32 title hits) | vector | per publisher | WAT validation beyond Plzeň |
| Ecological network | NKOD: ÚSES of regions (ZÚR) and municipalities (10 hits) | vector | per publisher | EPI-04, ECO-04 |
| **Meteorology** | ČHMÚ: station climate data (historical / recent), **radar**, NWP ALADIN, gridded climate products for CZ (`products/grids_CZ`), radiosoundings, wind profiles | CSV / grids / images | mostly **CC BY 4.0**; some datasets CC BY-NC-ND 4.0 (check per dataset) | WAT rainfall forcing, HAZ-01 wind / moisture, ATM-02 night temperatures, ATM-01 meteorology |
| **Hydrology** | ČHMÚ: hourly and daily discharge and water levels (historical / recent / now), **groundwater** levels | CSV | as above | WAT hydrographs and validation, HYD-09 groundwater validation |
| Air quality and emissions | ČHMÚ: air-quality measurements (ISKO archive 1969–2025), emissions, smog situations; NKOD: REZZO 1–4 emissions (ČSÚ), stationary sources REZZO 1 / 2 (Prague) | CSV / vector | as above / per publisher | ATM-01 sources and validation |
| Statistics | ČSÚ (in NKOD), census grids (to be verified) | CSV | per dataset | MOV-03 population weighting, EPI-04 context |
| Water network, catchments | DIBAVOD (VÚV TGM) | vector | to be verified | WAT, HYD-05, ECO-03 corridors |
| Forest stands | ÚHÚL forestry data (species, age) | to be verified | to be verified | ECO-01 (spruce share), HAZ-01 fuels |
| Nature protection, species occurrence | AOPK | to be verified | to be verified | EPI-04 (species returning), ECO-03 invasive plants |

Not found in NKOD titles: bark-beetle (kůrovec) data, wildfire (požár) data, traffic-
intensity datasets (dopravní intenzity), GTFS — these exist elsewhere (e.g. forestry and
fire-service portals, national road administration, city transit operators) and remain
to be verified.

## Practical notes for the engine and geodata pipeline

- **The national DTM is open but comes as point clouds** (LAZ per map sheet). The
  geodata pipeline needs an offline gridding step (Node or a GIS tool) producing a raster
  in the model CRS; browser demos should load precomputed rasters (Cloud-Optimised
  GeoTIFF).
- **Two CRSs dominate**: S-JTSK (EPSG:5514) for ČÚZK and most Czech data, ETRS89 / TM33
  (EPSG:3045) as an alternative; city GeoJSON often in WGS 84. The pipeline must reproject
  to one model CRS (open question Q7 in `engine-architecture.md`).
- **Licences differ by dataset** even within one provider (ČHMÚ: CC BY 4.0 vs. CC BY-NC-ND
  4.0); each input layer in `data/` must record its licence (`data/README.md` convention).
- **Discovery is scriptable**: NKOD SPARQL for anything harvested, ČÚZK Atom search for
  national geodata, ČHMÚ directory listings for time series.

## Open questions

- Is there an official gridded DTM product (raster) besides the LAZ point clouds, to avoid
  our own gridding? (to be verified)
- Licences and download interfaces of DIBAVOD, AOPK and ÚHÚL data.
- Copernicus Land products and EU-DEM / Copernicus DEM access for EU-wide demos.
- Census population grid availability (ČSÚ).
