# Plzeň city GIS — map applications and services

Analysis of the City of Plzeň GIS (SITMP) beyond the open-data portal: the transport
section of the map portal (https://mapy.plzen.eu/mapy-a-aplikace/doprava/) and the
ArcGIS services behind it. Done 2026-11-20 via the public ArcGIS REST directory and
portal search (metadata, layer schemas, record counts, a few sample records); nothing
downloaded in bulk, nothing stored in the repository.

## Terms of use — read first

Based on the *Rules for providing data and outputs from the GIS of the City of Plzeň*
(City Council resolution No. 656, 9 June 2016), their annexes (price list valid from
1 Feb 2023, licence conditions, application forms) and the portal's licence page — all read
2026-11-20.

| Tier | What | Access | Licence / conditions |
|---|---|---|---|
| **1. Public, basic regime** (Rules art. 1(3)) | (a) **Open data** at opendata.plzen.eu (153 datasets); (b) **map viewing and download services** "listed at mapy.plzen.eu" | free, no request | Licence conditions point 4: **CC BY-SA 4.0** + attribution "datový podklad © SITMP". **Inconsistent sources:** the portal's open-data page says **ODbL**; the NKOD records of the datasets say "no copyrighted works / no protected database". Third-party data keep their own licences (see below) |
| **2. Technically public, licence unclear** | ArcGIS REST services on ags.plzen.eu queryable **without a token** — traffic-model scenarios, FCD incl. history, detectors, closures, DMT 2020 / 2022 (ImageServer), historical maps, DTM ZPS, orthophotos 2020 / 2022 / 2024, 3D scene layers, cadastre and land-use-plan map services | reachable without login | Whether they count as the "download services" of tier 1 is **not stated**: no explicit list of services (WMS / REST) was found on mapy.plzen.eu. The licence page requires citing the source when "using data from SITMP web services". Clarification requested in `requests/sitmp-article6-request.md`, question 1 |
| **3. On request only** | (a) token-protected services (e.g. folder `GIS_Povodne`); (b) data **files** prepared by SITMP beyond open data (standard / above-standard regime), e.g. the priced items: cadastral parcels, orthophotos 2006 / 2004 / 2002 / 1996 / 1945, simplified base and thematic layers, technical-map networks (public-lighting cables, traffic-signal cables, SITMP optical network, heating, utility tunnels), greenery passport; other data "individually by agreement"; (c) internal applications for city staff | written request (forms 3a–3e) | Article 6 (public research / education): **free**, "reasonable scope (e.g. a data sample) at the supplier's discretion"; use **only for the stated purpose, no provision to third parties in any form** (licence conditions 1.2); contractual penalty 30 000 CZK. Article 8 (others): handling fee 300 CZK + price list |
| **Not available** | traffic-signal timing plans (no service found; loops only linked to controller ids) | — | — |

Third-party data distributed by SITMP keep their supplier's conditions (Rules art. 1(12–13)).
The portal's licence page lists external licences for: 3D models of Plzeň 2024 / 2020 / 2009
(Georeal — the 2024 / 2020 licences allow free sublicensing with the attribution
"© GEOREAL spol. s r.o."), ZABAGED and DMR (ČÚZK), Geonames, orthophotos 1938–2019, the
Mapy.cz plan and the Imperial obligatory imprint 1841. The DMT services are named
"Georeal" (supplier licence to be verified); FCD / CEDA data are not on the list (rights
holder unknown).

## Transport applications on the map portal

| Application | URL | What it shows | Backend found |
|---|---|---|---|
| Traffic intensity and planned closures | https://intenzitadopravy.plzen.eu → `plzen.roadtwin.com` | Visualisation of a **traffic model** with current closures (model id `tm_pilsen_m24_v251105`) | commercial "RoadTwin" platform (third party; not analysed further) |
| Traffic map | https://mapadopravy.plzen.eu | Intensity at the busiest junctions from detectors | detector services below |
| Map project Transport | https://gis.plzen.eu/doprava/ | Closures, parking zones, public transport | services below |
| Public transport plan (IPD) | https://gis.plzen.eu/ipd/ | Lines, stops, timetables, diversions | stops services, GTFS |
| Closures, parking zones, tariff zones, traffic organisation in the centre, access roads, motorway exits | `aplikace.plzen.eu/gis/mapaf.asp?r=…` | predefined maps | closures from JSDI (national traffic information system) |
| Traffic accidents | https://nehodyplzen.innoconnect.net | Visualisation of accidents in Plzeň | third-party application (source to be verified) |

## ArcGIS services (ags.plzen.eu)

Directory `https://ags.plzen.eu/arcgis/rest/services` — 29 folders; services in S-JTSK
(EPSG:5514). Portal (Portal for ArcGIS) at `agp.plzen.eu` with public search. The folder
`GIS_Povodne` (floods) requires a token (not public).

### Transport (`GIS_Doprava` + test services)

| Service / layer | Content (measured) | Key attributes | Value for ca-geo |
|---|---|---|---|
| **Traffic model scenarios** `GIS_Doprava_DM_scenar_01–04` | 4 scenarios: before / after the western bypass, closures July 2024, closures July 2025; ≈ 4 470–4 550 directed edges each | `edge_id`, `source`, `target` (node ids → routable graph), `capacity` (750–4 000), `cost`, `speed`, `type` (0 / 1 / 2), `traffic` (assigned volume, max ≈ 3 088, mean ≈ 312; unit not stated), `traffic_lvl` (volume / capacity) | **A ready macroscopic network with capacities and assigned volumes** — base network for a traffic CA, demand calibration, scenario comparison ("what does the bypass change?") |
| **FCD** `GIS_Doprava_FCD` layer 0 | 5 786 directed segments of the CEDA navigation network with **live** speed, travel time, free-flow speed, traffic level (level1–5), measurement time (minutes old at the time of the check) | CEDA attributes incl. `ONEWAY` (FT: 2 019), functional class `FC`, form of way `FW`, `SL`, `NC`, street names; meaning of codes to be verified in CEDA documentation | live state for validation, one-way information, network hierarchy |
| **FCD history** `GIS_Doprava_FCD` table 3 | **19 024 459** records (`ROAD_ID`, speed, travel time, free-flow time / speed, traffic level, measurement time); range found: **5–27 May 2025** | per-segment time series | calibration / validation of speeds and congestion over three weeks |
| Detector profiles `GIS_AG_AGS_DOPRAVA_Detektory` | 364 profile segments with capacity; table of current flow rates per detector (735 rows) | `c_prof`, `capacity`, `vehicleFlowRate`, calculation time | same as open data, plus a live table |
| Detector loops `GIS_TEST_Smycky_detektoru` | 1 073 loop polygons | junction, detector, **signal controller id** (`id_ssz`), label | links loops to signal controllers (signal plans themselves not found) |
| Closures `GIS_Doprava_Uzavirky` | JSDI closure sections (344), RIA / SUPERDIO works register (679 records with start / end dates), CEDA road network snapshot 2024-12 | dates, streets, investor, state | time-dependent capacity reductions (closure scenarios) |
| Speed radars `GIS_DOPRAVA_Radary_verejne` | 34 radars, 20 section-speed measurements | location | context |
| Parking `GIS_DOPRAVA_Parkovaci_plochy_SHP` | 72 car parks with capacity | `kapacita`, type | destinations |
| Public transport stops | 707 stops | PMDP ids, direction, request stop | transit |
| PoliVisu test service | polylines with capacity and values | — | EU project PoliVisu test data (context) |

### Other folders relevant for the selected models

| Folder / service | Content | Models |
|---|---|---|
| `GIS_DMT_DMR` — **DMT Plzeň 2022** ImageServer | terrain model **0.5 m**, whole city (32 500 × 32 001 px, float32), plus DMT 2020 and contours 2020; export up to 15 000 × 4 100 px per request | WAT, ATM-02, HAZ-01 (closes the DTM gap for Plzeň) |
| `AG_DMT` ImageServer | terrain 1 m, small area (2.5 × 2 km) | — |
| `GIS_Historicke` | **23 historical map epochs 1781–1972** (incl. Imperial obligatory imprints of the stable cadastre, 1821, 1840, 1864 … 1931, 1938, 1947, 1950, 1971) | LND-01 urban growth over almost two centuries |
| `GIS_DTM` | Digital technical map: **road surfaces, pavements, cycle paths, traffic islands (562), dividing strips (245), parking areas, tram tracks, bridges**, walls, kerbs, green areas; carriageway surfaces queryable (6 105 in the cached feature service); road axes and network nodes as display-only layers | lane-level road geometry for traffic, evacuation, pluvial flooding |
| `GIS_3D_budovy`, Hosted scene layers | 3D buildings 2020 / 2024 / 2026, 3D mesh 2024 | evacuation, urban fire, cold air in streets |
| `GIS_OBYV_Heatmapa` | population heat map | MOV-03 weighting, evacuation demand |
| `GIS_Pasporty`, Hosted greenery layers | greenery and street-furniture passports | ECO-09 hosts, heat island context |
| `GIS_UKR` | land-use plan, its changes, development plans | LND-01 scenarios |

## What this changes for the traffic-simulation question

Compared with the open-data-only assessment (`plzen-traffic.md`):

| Gap there | Now available (subject to licence) |
|---|---|
| Street graph not routable; no direction / capacity | **Routable directed graph** with capacities, speeds and assigned volumes (traffic model scenarios); CEDA network with one-way flags |
| Demand only from loops at 100 junctions | **Assigned volumes on every model edge** (a calibrated macroscopic model) + live / historical **FCD speeds** on 5 786 segments |
| No validation of speeds | **19 M FCD records** (three weeks of May 2025) |
| Lane geometry only from markings | **DTM road surfaces, islands, dividing strips** at survey accuracy |
| Terrain for gradients | **0.5 m DTM 2022** |
| Signal plans | still missing — loops are linked to controller ids, plans not published |
| Number of lanes per link | not found as an attribute (CEDA field meanings to be verified) — markings / DTM surfaces needed |

**Conclusion:** with the city's GIS data, a **city-wide mesoscopic or microscopic traffic CA**
becomes realistic: network and capacities from the traffic model, one-way rules from CEDA,
calibration against assigned volumes and detector flows, validation against FCD speeds,
scenarios from the bypass and closure variants. Lane-level detail (turn lanes, signals)
would still need markings, DTM surfaces and estimated or requested signal plans. This is a
scope question (MOV-02 is out of scope in ADR 0001) and a licensing question (article 6
request).

## Open questions

- Conditions of article 6 of the GIS data rules for a public open-source research project
  (redistribution of derived data in a public repository?).
- Units and time basis of `traffic` in the traffic-model scenarios (peak hour? daily?), meaning
  of `type`; who built the model (the RoadTwin model id suggests the same source).
- Meaning of CEDA codes (`FW`, `FC`, `SL`, `NC`, `DS`) and whether a lane-count attribute
  exists in the full CEDA dataset.
- Can signal timing plans be obtained (controller ids are known)?
- Source of the accident visualisation (national police accident data?) — to be verified.
