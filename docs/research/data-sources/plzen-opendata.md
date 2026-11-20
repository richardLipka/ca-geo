# Open data of the City of Plzeň — usability for ca-geo

Analysis of the open-data portal of the Statutory City of Plzeň
(https://opendata.plzen.eu/) for configuring, driving and validating the selected CA
models (ADR 0001). Done 2026-11-20 from the portal's machine-readable catalogue; sample
files were downloaded only to a temporary folder for inspection (nothing stored in the
repository or in `data/`).

## Portal facts

| Item | Finding |
|---|---|
| Catalogue | 153 datasets; DCAT-AP-CZ catalogue in JSON-LD at `https://opendata.plzen.eu/public/opendata/catalog`, one record per dataset at `/public/opendata/dataset/<id>` (Czech open-data catalogue standard, harvestable by NKOD) |
| Downloads | `/public/opendata/download-file/<n>`; no `Content-Length`, no range requests (size unknown before download) |
| Vector formats | Each GIS dataset as five ZIPs: DGN, DXF, **GeoJSON**, KML, **SHP** (same order in every record) |
| CRS | GeoJSON in WGS 84 (lon / lat, no `crs` member); detector CSVs carry both S-JTSK (EPSG:5514, negative x / y) and WGS 84; point clouds in S-JTSK tiles |
| Terms of use | GIS datasets declare "no copyrighted works, no protected database, no special database right, no personal data" (Czech NKOD terms of use) — free reuse; the PMDP timetables (GTFS) are CC BY 4.0 |
| Update frequency | Most GIS layers `NEVER` / `IRREGULAR`; city structure layers `CONTINUOUS`; sensors continuous / weekly |
| Spatial extent | City of Plzeň, some layers also the surrounding ORP / river reach |

**Data quality notes (found while inspecting samples):**

- `zaplavovauzemi_GEOJSON` (dataset 26) is **invalid JSON** (`"features": [, {…`); the fix
  is trivial (remove the leading comma) — the SHP version is presumably fine (to be
  verified).
- Tree passport GeoJSON (163): 3 of 48 683 features have coordinates far outside Plzeň
  (bad transformation); the GeoJSON carries only IDs — attributes are in the TXT version.
- Contours (22) as GeoJSON are **2.1 GB unzipped** (345 MB ZIP) — unsuitable for the browser.
- Point clouds (149, 150) are LAS tiles of ~250 m; the ZOO surface model alone exceeds 1 GB.
- REZZO emission sources (46, 47, 123) date from **2005**; the REZZO1 layer also covers
  the wider region.
- Some sensor endpoints (`onlinedata.plzen.eu`) reject automated requests.

## What is missing for CA configuration

| Need | Status in the Plzeň portal | Fallback (to be verified) |
|---|---|---|
| DEM raster (terrain) | Only contours from DMT 2020 (22) and local point clouds (149, 150) | National DTM from ČÚZK (DMR 5G / 4G) |
| Land-cover raster | Vector layers only (forests, meadows, buildings, land-use plan with 4 coarse categories) | Copernicus Urban Atlas / CORINE, ZABAGED |
| Soil / infiltration | none | national soil maps |
| Flood depths | only flood **extents** (no depth rasters) | — (extents suffice for Jaccard / F1 validation) |
| Hydrographs / rainfall | none (only pond level at Bolevák) | ČHMÚ gauges and radar |

## Relevant datasets by model

IDs are portal dataset IDs (`/public/opendata/detail/<id>`). Role: **in** = model input,
**par** = parameter source, **val** = validation, **scn** = scenario / intervention,
**ctx** = context / zones.

### Core models

| Model | Dataset (ID) | Role | Notes |
|---|---|---|---|
| **WAT water / flooding** | Flood extents Q5 (40), Q20 (95), Q100 (53), active / passive zones (26) | val | Compare simulated extents of a design flood with the official zones (Jaccard / F1, SC-METRICS); Q100 also without bridges |
| | Flood of August 2002 (87), floods of the 19th century (54) | val | Historical event extents — a strong demo ("would the model reproduce 2002?") |
| | Buildings (85), 3D buildings of the centre 2024 (37), road outlines (81) | in | Obstacles / roughness for pluvial urban flooding; DSM in the centre |
| | Contours from DMT 2020 (22) | in (fallback) | Only if the national DTM is not used; heavy |
| | Bolevák pond — water level, temperature, treatment plant (180–182) | val / scn | 10-min level series from 2022 — pond scenario (HYD-04) or level–volume demo |
| **HAZ-01 wildfire** | Forests (111), meadows (112), parks (52), recreation areas (88) | in | Fuel classes via SC-RECLASS (forests from cadastre — no species) |
| | Satellite NDMI 2017–2025 (179, external S3) | par | Sentinel-2 moisture index (~10 m) as a fuel-moisture proxy per date |
| | Buildings (85), 3D buildings (37) | in | URB-03 urban-fire scenario (building fuel, distances) |
| | Road network (81), rail (93), tram tracks (80) | scn | Firebreaks |
| **ATM-02 cold air** | Land-use plan localities (84), built-up areas (128), forests (111), meadows (112), buildings (85) | in | Production / resistance classes; buildings as resistance |
| | Satellite land-surface temperature 2017–2024 (179, Landsat ~60 m) | val (limited) | Daytime scenes only (file timestamps around 09:57) — shows surface heating, not night cold-air pools |
| | Air-quality sensors Envitech / AGDATA (188, 197) | val (to be verified) | If they include air temperature, night cooling at points could be compared |
| **ECO-01 bark beetle** | Forests (111) | in | Forest mask; no species or age → spruce share from national forest data |
| | Satellite NDVI / NDMI time series 2017–2025 (179) | val | Vegetation decline detection in city forests (validation of dieback at ~10 m) |
| | Tree passport (163, TXT): 2 757 *Picea* trees | in (urban variant) | Urban-scale host map with species, planting year, height, crown diameter |
| **LND-01 urban growth** | Historical town plans 1877, 1879, 1891, 1902, 1924 (71–74, 104; ECW raster) and plan from the cadastral map 2007 (115; TIF) | val / in | Historical urban extents for calibration — needs digitising of built-up areas (manual / semi-automatic) |
| | Built-up areas (128), developable and transformation areas (127) | in / scn | Initial urban mask; land-use-plan constraints and demand scenarios ("what if the plan is filled?") |
| | Land-use plan localities (84) | ctx | 334 localities, categories urban / landscape / river landscape / park |
| | Protected areas (51), VKP (33, 35), ÚSES (77), flood zones (26) | in | Exclusion layer |
| | Street graph (56), road outlines (81), tram (80), rail (93), motorway (27) | in | Road gravity / accessibility |
| | Urban districts — ZSJ (109, 113), city parts (106, 108), cadastres (107) | ctx | Zonal statistics, demand per zone |
| **EPI-04 population (ECO-04 connectivity)** | ÚSES — biocentres and biocorridors with functional state (77) | in / val | Directly a habitat network (RBC / LBC / RBK / LBK / NRBK, functional / non-functional) |
| | VKP (33, 35), protected areas (51), forests (111), meadows (112) | in | Habitat suitability (K) |
| | Motorway (27), roads (81), rail (93) | in | Barriers as slot weights (SC-RASTERIZE) |
| | Hunting grounds (96) | ctx | Management zones (culling / vaccination scenarios) |

### Extension models

| Model | Dataset (ID) | Role | Notes |
|---|---|---|---|
| **MOV-03 accessibility** | Street graph (56), road outlines (81), PMDP timetables GTFS (187, CC BY 4.0), stops (9, 78), MHD segments (58) | in | Walking + public-transport travel time; GTFS adds time-dependent transit |
| | Libraries (31), offices (91), polling stations (120), WC (134), waste yards (30) | in | Service locations as sources |
| | Population — urban districts (109) | ctx | Weighting accessibility by population (population counts from ČSÚ — to be verified) |
| **MOV-01 evacuation** | Buildings (85), 3D buildings (37), road outlines (81), 3D ZOO (39, 150) | in | Real geometry for exits / obstacles |
| | Pedestrian and cyclist counts at Náměstí Republiky (217), schools (219) | val (limited) | Flow counts, not evacuation data |
| **ECO-09 plant pest / pathogen** | Tree passport (163, TXT: taxon, planting year, height, crown) | in | **3 376 *Fraxinus*** (ash dieback host), 1 184 *Aesculus*, 901 *Platanus*, 9 177 *Acer*, 7 727 *Tilia* — a real urban host map for a street-tree epidemic demo |
| | Memorable trees (28) | ctx | — |
| **ATM-01 dispersion** | REZZO1 / REZZO2 / domestic heating sources (46, 47, 123; 2005) | in | Point sources with stack height; outdated |
| | Traffic detectors — locations (162), hourly profiles (133, 132), detector data (160, 161) | in | Traffic intensity → road emissions (template `sonnenschein2025hybrid` uses traffic emissions) |
| | Air-quality sensors (188, 197); air-quality time series on the S3 bucket of dataset 179 | val | NO₂, CO, O₃, PM10, PM2.5 aggregates (origin of the S3 series to be verified) |
| | Noise detectors (199–237) | — | Sound propagation is out of scope (ATM-06) |
| **HAZ-05, HAZ-02, HYD-09** | — | — | No relevant data (Plzeň has no lava / avalanche terrain; no hydrogeology) |
| **HYD-05 erosion** | Contours (22) only | — | Soil and crop data missing |

### Not relevant for CA

Electronic notice boards (168–178), counter load (165), parking (55, 125, 131, 166),
waste containers (82, 99, 100), traffic signs (6, 92), house numbers (8), street names (10),
map sheets (48, 50), PlzniTo reports (159), cyclist counters (189–198; possible only as
validation of a bicycle-flow model, which is not selected), URBREATH KPIs (220–222).

## Recommended uses (ranked)

1. **Flood validation for WAT** — Q5 / Q20 / Q100 zones and the 2002 event over the
   national DTM: the most convincing local demo; directly measurable (Jaccard / F1).
2. **Urban growth of Plzeň since 1877** — historical plans + current built-up area +
   land-use-plan development areas: a long time series for LND-01 calibration and a
   "plan scenario" demo (requires digitising the historical built-up areas).
3. **Street-tree epidemic** — the tree passport with species is a rare, high-quality
   host layer for ECO-09 (ash dieback on 3 376 ashes) at street scale.
4. **Habitat connectivity / population spread on ÚSES** — the city's ecological network
   with functional state as corridors and barriers (EPI-04, ECO-04).
5. **Accessibility with GTFS** — walking + transit travel times to services (MOV-03).
6. **Vegetation and moisture time series (Sentinel-2, 2017–2025)** — validation layer for
   ECO-01 / fuel moisture for HAZ-01; land-surface temperature only as daytime context for
   ATM-02.

## Open questions

- Is the national DTM (ČÚZK) openly downloadable at the needed resolution for the Plzeň
  area? (to be verified — decisive for WAT, ATM-02, HAZ-01)
- Licence of the satellite products on the external S3 bucket (worldfromspace) — not
  stated in the bucket; the portal record carries the city's free terms of use (to be
  verified with the provider).
- Do the Envitech / AGDATA sensors include air temperature and humidity (needed for
  cold-air validation)?
- Georeferencing quality of the historical town plans (ECW) — needed before digitising.
- Native CRS of the SHP / DGN distributions (presumably S-JTSK, EPSG:5514 — to be verified).
