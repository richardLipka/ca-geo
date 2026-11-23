# Plzeň growth model 1295–2020 (schematic 3D animation)

Status: first version, November 2026. Tool: `apps/historic-mapper/growth3d.html` (dev server
http://localhost:5218/growth3d.html). Data: `scripts/growth_model.py` → `data/historic/growth/web/`
(not versioned). Video: `growth3d.html` → *Export video* (frames) + `scripts/encode_video.py` → `data/historic/growth/video/plzen-growth-1295-2020.mp4` (1600 × 900, 62 s).

**Schematic** means that every building of the model is a real footprint (present RÚIAN building
or a building of the stable cadastre 1840 that no longer exists). Its year of origin is
**interpolated** within the bounds that the evidence allows. Before 1840 the positions are
those of 1840 shown earlier: the medieval town did not have exactly these houses. The animation
shows the order and the pace of growth. It is not a reconstruction of individual houses.

## 1. Evidence

| Evidence | Coverage | Used as |
|---|---|---|
| RÚIAN stavební objekty (ČÚZK ArcGIS REST, layer 3), 32 425 footprints in the 9 × 9 km frame | present stock | geometry; `dokonceni` (completion) exact for 4 132 + 2 005 rebuilt; the placeholder dates 31 Dec 1919 / 1945 / 1960 / 1970 / 1980 / 1990 / 2000 are age classes (≤ 1919, 1920–45, …) → interval; `pocetpodlazi` → height |
| Map epochs in the common frame (`growth_rules.py`): stable cadastre 1840, 3rd military survey 1880, city plans 1891, 1895, 1912, 1926, 1931, 1938, 1947, orthophoto 1953 | partly (city plans cover the town only) | building pixels at each footprint → first epoch in which the place is built |
| Stable cadastre 1840 buildings that do not overlap a present building | 760 footprints | historic-only buildings; demolition = first later epoch where the place is empty |
| Model c. 1536–1618 (`projects/plzen.json`) | old town | wall ring, towers, gates (with demolition years), churches, Dominican monastery (–1785) |
| Written sources (inventory `data-sources/plzen-historical.md`) | town | founding 1295; sieges 1433–34 and 1618 (TE 1618, legend D: burned suburbs); bastions 1645–49, glacis cleared 1647; wall demolition 1795–1849 (Litická 1804, Pražská 1822, western walls 1828, Říšská 1833, Saská 1849), last section 1893–99 |
| First written mentions of villages (cs.wikipedia, Nov 2026) | 11 villages | Doudlevce 1227, Skvrňany 1239, Malice/Roudná (older than the town), Božkov 1338, Doubravka 1338, Valcha c. 1352, Koterov 1369, Lobzy 1379, Bolevec 1382, Radčice 1420, Hradiště (hammer works 1686). Vinice, Lochotín and Košutka are modern estates |

## 2. Dating rules

1. **Map split.** For each footprint the state in every epoch is *built* (≥ 20 % building pixels),
   *empty* or *unknown* (outside the map). A weighted monotone split gives the first built
   epoch. The weights (1840 1.0, 1880 0.4, 1891/1895 0.5, 1912 0.7, 1926–38 0.8, 1947 0.9,
   1953 0.4) make it tolerant of a badly classified epoch.
2. **Combination with RÚIAN.**
   - An exact RÚIAN date is the origin. If the maps show the place built more than 10 years
     earlier, the place is dated by the maps and the RÚIAN date becomes a rebuild (height
     changes).
   - An age class is intersected with the map interval. If the maps are earlier, the
     building counts as rebuilt within the class. If the maps are later, the class wins.
3. **Growth front.** Within an interval, buildings are ordered by their distance to the
   built-up area of the previous epoch (plus 0–25 m noise). The nearest get the earliest years.
4. **Places built by 1840**, dated by zone:
   - *inner town* (inside the wall): 1295–1335, from the square outwards;
   - *glacis* (≤ 110 m outside the wall): 1796–1840, after the walls fell;
   - *gate suburbs* (≤ 1.25 km of the square; the 45 % nearest to a gate):
     - from 1330–1430;
     - destroyed 1433.6 and rebuilt 1436–1481;
     - destroyed 1618.75, rebuilt 1650–1770, or after 1796 within 260 m of the wall (glacis of the bastioned fortress);
   - *later suburbs*: 1650–1840;
   - *villages*: the core (nearest 40 %) from the first mention, the rest up to 1840;
   - *isolated buildings*: 1650–1838.
   - Inner-town houses are 2–3 storeys (≤ 9 m) until a 19th-century rebuild (1850–1919) to
     their RÚIAN height.
5. **Fortification.**
   - The wall ring is cut into 30 m pieces, built c. 1310–1330.
   - Each piece is demolished with the year of the nearest gate.
   - The western side goes in 1828 (ring park), the piece at the museum in 1896.
   - Wall towers fall with their wall piece. Gates use their documented year.
6. **Landmarks.**
   - St Bartholomew from 1320, with a 102 m tower.
   - Franciscans 1300, water tower 1532, St Nicholas 1400, All Saints (older than the town), Dominican monastery 1300–1785.

## 3. Results

Buildings visible in the model:

| Year | 1300 | 1400 | 1500 | 1618 | 1700 | 1800 | 1840 | 1880 | 1912 | 1938 | 1953 | 1980 | 2020 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| buildings | 51 | 503 | 573 | 593 | 728 | 1 206 | 1 480 | 2 030 | 4 324 | 10 789 | 15 668 | 21 335 | 31 476 |

Calibration check: the model has 313 buildings inside the wall and 103 in the suburbs in 1788.
Schaller (1788) counts 315 houses in the town and 142 in the suburbs. Model buildings are not
houses, so the agreement in the town is partly coincidental. The suburb deficit (≈ 30 %) is
consistent with the 1840 cadastre showing wooden suburban houses in yellow, which the
footprint test catches only partly.

Basis of dating:

| Basis | Buildings |
|---|---|
| maps only | 16 233 |
| maps + RÚIAN age class | 5 373 |
| RÚIAN exact date | 4 132 |
| maps, rebuilt per RÚIAN | 4 322 |
| RÚIAN class, maps later | 1 565 |
| 1840 cadastre + zone rules | 700 |
| 1840 cadastre, demolished | 760 |
| fortification / landmarks | 69 |

The viewer can colour buildings by this basis.

## 4. Viewer and video

- **Display.** Merged mesh with a vertex shader. Buildings rise over 3 years, sink at
  demolition, vanish during the siege gaps and change height when rebuilt. New buildings
  flash yellow.
- **Colour.** By period of origin or by dating evidence.
- **Ground.** The epoch map as terrain (base, 1840, 1880, 1912, 1938, 1953, ZTM). Rivers and
  ponds come from the present ZTM for all years, so the Bolevecký pond (1460) and the České
  údolí reservoir (1970s) appear too early.
- **Overlays.** Village labels with the year of first mention; event captions; growth chart
  under the timeline.
- **Speed.** Adaptive: 28 years/s before 1780, 12 to 1840, 4.5 to 1960, 6 to 2020. That is about 60 s.
- **Video export.** Fixed 30 fps steps, independent of browser speed. Frames carry the year,
  caption, legend, labels and credits. The dev server saves them to
  `data/historic/growth/video/<run>/` and `encode_video.py` makes the MP4.

## 5. Caveats and next steps

- **Pre-1840 positions are schematic.**
  - The 1618 plate and the Ottheinrich veduta are not yet used house by house.
  - Next: per-block presence from the georeferenced TE 1618 plate. Its legend D marks the
    burned suburbs.
- **Missing structures.**
  - Bastions 1645–49 and the Zwinger have no geometry (no plan before 1781 is georeferenced).
  - Buildings built and demolished between two epochs after 1840 are missing, e.g. war damage
    of 1945 and the clearance of old Skvrňany / Doubravka cores for estates.
  - Vectorising the 1912 / 1947 plans the way the 1840 cadastre was done would add them.
- **Uneven map quality.**
  - The 1880 and 1953 epochs are noisy, hence their low weights.
  - City plans cover only the town, so villages are dated mostly by RÚIAN classes and the
    1880 / 1953 epochs.
- **Ancillary buildings.** Garages and sheds without dates follow the maps, so they often
  appear late.
- **Further date sources.** Building dates from the Encyklopedie dějin města Plzně (362
  buildings) and from Wikidata (474 with an inception date) would replace interpolation where
  available (requires permission for the Encyklopedie).
