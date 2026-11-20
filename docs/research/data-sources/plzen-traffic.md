# Plzeň traffic data — can a realistic traffic simulation be reconstructed?

Analysis of the City of Plzeň's open traffic and road GIS data (portal
https://opendata.plzen.eu, see `plzen-opendata.md`) for building a lane-level traffic
model (cellular-automaton traffic in the Nagel–Schreckenberg family: `nagel1992cellular`,
`rickert1996two`, `chowdhury1999selforganization`, CZ-calibrated `korcek2012evolutionary`).
Done 2026-11-20 by downloading the GeoJSON distributions to a temporary folder and
analysing them with scripts (geometry, attributes, topology); nothing stored in the
repository.

> **Update 2026-11-20:** the city GIS services (not the open-data portal) contain a routable
> traffic-model network with capacities and assigned volumes, live and historical FCD speeds,
> DTM road surfaces and a 0.5 m terrain model — see `plzen-gis-services.md`, which revises the
> feasibility conclusion below (subject to the city's GIS data licence).

## Datasets and what they contain

| Dataset (ID) | Content (measured) | Attributes | Use for a traffic model |
|---|---|---|---|
| Street graph (56) | 7 899 centreline segments, ≈ 1 023 km, 10 road categories (incl. 2 042 pedestrian segments, 31 motorway) | road category, segment ID, road number, street code — **no direction, lanes, speed or turn rules** | network skeleton |
| Road outlines (81) | 1 635 lines — carriageway edges | none | carriageway width (distance between edges) |
| Horizontal markings (92) | 30 221 features, 40 marking codes | marking code (e.g. V2b), text for symbols | **lane structure**: lane dividers V2b (2 831 dashed) and V1a (1 393 solid), edge lines V4 (4 690), stop lines V5 (568), direction arrows V9a (1 315, drawn as polygons), pedestrian crossings V7a (1 143), parking bays V10a–g, hatched areas V13a, texts V15 |
| Vertical signs (6) | 28 506 features, 233 sign codes | sign code, text (e.g. `ZÓNA {B20a "30"}`) | **rules**: priority P2 (1 482) / P4 (1 804) / P6 (87) / P1 (38) / P3 (108); one-way IP4b (682), B2 (788), B1 (410); mandatory direction C2a–c, C4a (580); turn bans B24a (336) / B24b (307); speed limits B20a (188: 5–110 km/h), zones IZ8a (30 km/h: 188, 20 km/h: 45), residential zones IZ5a (490) |
| Traffic detectors (162) | 1 171 loops / wireless detectors at **100 junctions** (K…), named per approach and lane (e.g. `DVC`, `DVC'`) | junction, detector ID, label | lane-level measurement points |
| Detector data (160, 161) | CSV: per detector **occupancy and intensity in 90-s intervals**; some junctions also speed (`V_VALUE`, junction K117); rolling window (samples seen from 8–17 Nov 2026) | detector, UTC time, occupancy, intensity, (speed) | demand and calibration per lane; fundamental diagrams |
| Sensor profiles (133) + profile segments (132) | 364 profiles at junctions; 364 segments with **capacity** (500–3 600 veh/h) | junction, profile number, capacity | saturation flows / link capacities |
| Public transport | MHD segments (58: 1 384, flags bus / tram / trolleybus / night / ZOO), stops (9: 712, with PMDP GPS IDs), tram tracks (80: 662), GTFS timetables (187, CC BY 4.0) | modes, stop IDs | buses and trams in the simulation (dwell, priority) |
| Parking | car parks (55: 120 polygons, type), parking houses occupancy (166, weekly CSV) | type, capacity, occupancy | destinations / parking search |
| Counts at Náměstí Republiky (218), school surroundings (219) | vehicle / pedestrian / cyclist counts | — | local validation |

## Data quality findings

- **Both sign layers are invalid GeoJSON**: unescaped double quotes inside texts
  (`"TEXT": "ZÓNA {B20a "30"}"`) — 550 lines in vertical signs, 73 in horizontal
  markings; easy to repair line by line (done for the analysis).
- **Signs in GeoJSON are drawings, not points**: each sign is a `GeometryCollection` of the
  cartographic symbol (sign plate polygons, pole / arrow lines). The **SHP version** splits
  them into points (28 470), lines (630) and polygons (71) with the same four attributes —
  sign positions are therefore available as points, in S-JTSK coordinates (EPSG:5514, read
  from the file extent; the ZIP has **no .prj** file). Neither version has a **facing
  direction or link to a road segment**. Position = centroid; which approach a sign governs must be
  inferred (nearest segment, side of road, symbol orientation) — the main source of
  ambiguity.
- **Direction arrows (V9a) carry no arrow type** (straight / left / right); the type would
  have to be recognised from the polygon shape.
- **Street graph is a cartographic centreline network, not a routable graph**: with exact
  endpoint matching it falls apart into 2 224 components (largest 4 162 of 8 922 nodes,
  5 605 dead ends); with a 1e-4° (~10 m) tolerance still 1 849 components; 181 dead ends lie
  on interior vertices of other segments (T-junctions not split). Pedestrian paths are mixed
  in. Topology cleaning (snapping, splitting, filtering by category) is required.
- Street lights (130) are lamps, **not traffic signals**; no traffic-signal locations or
  **signal timing plans** are published (signalised junctions are only implied by the
  detector junction IDs K…).

## Feasibility

**Short answer: yes for a realistic CA traffic model of a selected central sub-network
(tens of junctions with detectors), with semi-automatic reconstruction and manual
curation; no for a fully automatic city-wide lane-level model.**

| Model element | Source | Automation | Effort / risk |
|---|---|---|---|
| Road network topology (links, junction nodes) | street graph (56) filtered to vehicle categories + snapping / splitting | automatic + checks | medium — cleaning rules, small manual fixes |
| Carriageway width | road outlines (81) | automatic (cross-section distance) | low |
| **Number of lanes per link** | lane dividers V2b / V1a between edge lines V4 (92), counted along cross-sections | semi-automatic | medium — only where markings exist (main roads); residential streets default to 1 + 1 |
| **Turn lanes at junctions** | arrows V9a near stop lines V5 (92) | shape recognition + manual check | high — arrow type not in attributes |
| One-way streets | IP4b / B2 / C2 signs (6) | sign-to-segment association | high — no sign orientation; cross-check needed |
| Speed limits | B20a values + IZ8a / IZ5a zones (6); defaults by category | semi-automatic (zones as polygons need reconstruction from entry / exit signs) | medium |
| Priority at unsignalised junctions | P1–P6 signs (6) | association to approaches | high (same orientation problem) |
| Turn bans | B24a / B24b (6) | association | high |
| **Signal timing** | not published | — | **gap** — estimate fixed-time plans or request from the city; 90-s detector intervals are about one signal cycle, too coarse to infer phases |
| Demand (inflows, turning ratios) | detector intensities per lane at 100 junctions (160) + profile capacities (132) | automatic aggregation | medium — no OD matrix; turning ratios only partly derivable from lane-level loops |
| Calibration / validation | detector occupancy and intensity (90 s), speed at some junctions | automatic | low–medium |
| Public transport | GTFS (187) + MHD segments (58) + stops (9) + tram tracks (80) | automatic | medium — map stops to links |

**Complementary source (to be verified):** OpenStreetMap carries `oneway`, `lanes`,
`turn:lanes`, `maxspeed` tags and traffic-signal nodes; its coverage for Plzeň could not
be measured (Overpass API overloaded during the check). A practical pipeline would likely
start from OSM topology and lane tags and use the city's markings, signs and detectors to
correct and calibrate them.

## Fit with ca-geo

- Traffic flow (MOV-02) is **out of scope** in ADR 0001 (class-A literature, but a network
  model, not a raster CA). Adding it would be a **scope decision** for the author.
- Engine impact: a traffic CA runs on **1D lane cells connected at junctions** — a new
  topology ("lane network") beyond the planned square / hex / graph topologies
  (requirement R1.7 graph topology is deferred). Primitives that fit: `stencil` on 1D lanes
  (NaSch rules), `agents` (vehicles with propose–resolve at merges), `queue`
  (routing), controllers (signal plans), observers (detector emulation for calibration).
- Validation story is strong: per-lane 90-s detector data at 100 junctions is rarely
  available openly and allows fundamental-diagram and queue-length comparisons.

## Open questions

- Will the city provide signal timing plans (fixed-time programmes per junction)?
- Archive depth of detector data (the portal shows a rolling recent window; is history
  available, e.g. via the ČHMÚ-tailored dataset 161?).
- Meaning of detector labels (`DVC` vs `DVC'`) — lane vs. upstream / downstream loop.
- OSM coverage of lanes / turn lanes / signals in Plzeň.
- Does the DGN version keep the symbol rotation (cell angle) of the signs? It would give the
  facing direction (SHP and GeoJSON do not; to be verified).
