# Plzeň growth model 1295–2020 (schematic 3D animation)

Status: version 2, November 2026. Tool: `apps/historic-mapper/growth3d.html` (dev server
http://localhost:5218/growth3d.html). Data: `scripts/growth_model.py` → `data/historic/growth/web/`
(not versioned). Video: `growth3d.html` → *Export video* (frames) + `scripts/encode_video.py` →
`data/historic/growth/video/plzen-growth-1295-2020.mp4` (1600 × 900, 62 s).

**Schematic** means that every building of the model is a real footprint. It is either a present
RÚIAN building or a building of the stable cadastre 1840 that no longer exists. Its year of origin
is **interpolated** within the bounds that the evidence allows. Before 1840 the positions are those
of 1840 shown earlier: the medieval town did not have exactly these houses. The animation shows the
order and the pace of growth. It is not a reconstruction of individual houses.

Changes in version 2:
- fortification from the 1781 plan (0.5 m), phased by the 1658 and 1703 plans of the Historický atlas;
- demolitions 1942–2008 and air-raid damage in the centre (Historický atlas, map 65);
- calibration to census house counts;
- six more map epochs, including the 2001 orthophoto;
- validation of the model against every map at its own year;
- heights from the city 3D model;
- terrain and per-epoch water;
- view mode for mapping vedute onto buildings.

Changes in version 3:
- real building shapes from the City of Plzeň 3D model 2024 (31 367 buildings), held back in time;
- camera fit and projective texturing of vedute onto the 3D model (view mode);
- guide page to the video (`sources_site.py`).

Changes in version 5:
- generated historic fabric (`fabric.py`): gabled burgher houses around the blocks of HAM map 57 inside the walls
  until 1750–1800 (square complete from 1295; present buildings replace them per block, or later when their own date
  is later); organic suburbs of small houses in the suburb blocks of map 57 (from the gates, burned 1433 and 1618,
  glacis cleared 1647); outside the walls the houses of the historic database appear only when the baroque walls fall
  (by sector 1796–1835), villages 1825–1845, with small generated houses at their places before;
- two growth modes: inside the walls the whole plan stands from the founding (low timber houses on all plots of map 57)
  and the houses grow in height on their plots, after the isometric views of 1618 / 1650 (Theatrum Europaeum, Merian:
  gable to the street, rear tracts and courtyard wings glued to the front houses, double roofs on wide plots):
  low timber houses 1295–1390 → Gothic stone houses (eaves 6–7.5 m, steep roofs, half with a rear tract) →
  Renaissance 1530–1620 on 75 % of the plots and the whole square (eaves 7.5–11 m, double roofs, side wings,
  back houses) until the present model replaces them (`fabric.burgher_complex`); the suburbs grow organically from the gates
  along the roads (frontage of the suburb blocks first, the insides later) until they fill the blocks of map 57;
- epoch evidence first: a present building with a later rebuild date (RÚIAN date / class) appears only then, an older
  generated house stands on its plot before;
- the baroque fortification as one star (plans of 1703 and 1658, Vogt 1712 as a check): main rampart around the
  Zwinger (1618–20), bastions joined to it (1645–49, 1658–59), detached ravelins and lunettes (1703), one ditch per
  phase following the outline, the medieval moat of map 57 before 1620; rampart and ditches split by sector (shared
  vertices, local terrain base, staggered demolition);
- Dominican monastery: church outline of map 57 next to point B of the 1618 plate, church = the 3D model of the
  Franciscan church turned and scaled, cloister of four wings; 1300 to c. 1800 (hospital from 1786, HAM map 8);
- barracks of the 35th regiment with a courtyard;
- river courses per epoch: the base is the present river network only (ZTM water bridged over bridges, long thin
  components with compactness 4πA/P² < 0.12, so ponds, reservoirs and sewage tanks drop out); until 1840 the courses
  of map 57 inside its field (wide confluence), plus the water drawn on the 1658 plan; 1840, 1908, 1926, 1938 and
  1947 add the water detected on their maps within 300 m of the rivers (old meanders, mill races, ponds when drawn);
  the full present water (Bolevec ponds, České údolí reservoir, sewage works) only from 1953; the opening map shows
  rivers only;
- ground maps: map 57 (from 1300), the Theatrum Europaeum plate (homography, 1618), plans 1658 and 1703;
- guide page: map flipbook of 30 registered maps with the dated model on top; the four 1618 siege plates as one source.
- the square: generated houses there are taller (8.5–11 m eaves); from the town hall (1554–59) the present models of
  the houses on the square and of the town hall (čp. 1) stand; the Franciscan monastery with its Gothic cloister
  (RÚIAN 24142204, date 2010 = reconstruction) stands from 1300;
- vedute: `veduta_fit.py` fits the draughtsman's camera and the heights of linked towers and gates together (robust
  least squares, prior σ 35 % around the 1618 model, camera within 6 km, field of view ≥ 8°). Theatrum Europaeum
  1618: 14 links, 63 px RMS (3.4 % of the sheet) → wall towers 14–17.5 m, gates 21–28 m, applied to the model; the
  fitted camera is saved as the view of the plate. Ottheinrich 1536 cannot be fitted (11 % RMS; the town is drawn
  widened), so it gives no heights.
- consistency pass before writing (growth_model.py) and a check per map (`check_epochs.py` → site/check/):
  duplicates of the 1840 cadastre and map 65 merged; the maps with reliable building detection (1840, 1891, 1912,
  1926, 1931, 1938) are binding at their year (generated houses they do not show end before them, real buildings
  without an exact date start after them); no two buildings on one place at one time (priority history > RÚIAN
  exact date > other real > generated). Result: extra buildings on the reliable maps 0–20 of 1 000–7 000, no
  overlaps. On the maps with weak detectors (1821, 1877, 1881, 1895–1908, 1947, orthophotos) "extra" mostly
  means a missed detection and is reviewed visually.
- dated individual buildings: town hall (čp. 1) and the houses on the square (the open square without its streets)
  from 1554–75 (history, not moved by the maps); museum complex on Kopeckého sady 1896–98; the court (Veleslavínova)
  only after the Dominican monastery is gone; present × present buildings never displace each other;
- buildings of the 1902 plan around the barracks (city GIS export at 0.5 m; black = military / public, solid red =
  others) that the model lacked: 191 footprints from 1899–1902, the barracks group removed in 1969, others when the
  later maps no longer show them;
- shapes from the 1536 veduta (Ottheinrich cut-outs, `fabric.silhouette_profile` / `loft` / `extrude_profile`): wall
  towers after the corner tower, gates after the gate tower, the Dominican church (nave and choir with the steep
  facade gable as cross-section, tower 45 m after the tall tower) on the outline of map 57;
- publishable page (`publish_site.py` → data/historic/growth/publish/): the viewer in public mode (`public3d.html`)
  with the timeline of events, the map under the model (by year, none, or any of the 18 maps) with dimming, cs / en;
  mesh split into parts < 14 MB;
- Not done: villages from the 1st military survey (HAM map 9) – automatic registration to the 2nd survey failed
  (ECC correlation < 0.2); needs manual control points.

Changes in version 4:
- the 1658 and 1703 plans registered to the model (`fort_plans.py`) and used for the phases and for the 1703-only works;
- fortification in 3D: earthwork bodies with scarp, parapet and terreplein, sunk moats with water and terrain cut-outs;
- barracks of the 35th regiment (1823–1969); 39 dated captions; maps dimmed in the video; slower pace 1600–1720 and 1780–1840.

## 1. Evidence

### Present buildings

| Evidence | Coverage | Used as |
|---|---|---|
| RÚIAN stavební objekty (ČÚZK ArcGIS REST, layer 3; `ruian_buildings.py`) | 32 425 footprints in the 9 × 9 km frame | geometry; `castobce` (part of the town); `dokonceni` exact or as age class (31 Dec 1919 / 1945 / 1960 / 1970 / 1980 / 1990 / 2000 = class upper bounds) |
| City of Plzeň 3D building model 2024 (`GIS_3D_budovy/GIS_Budovy_Plzen_2024`, attributes only; `city_heights.py`) | 63 153 objects; 31 012 RÚIAN buildings joined by ISKN parcel id | building height (ridge, `RELVYS_BUD`); floors only where no join |

### Map epochs

`growth_rules.py` holds the building-pixel rule per cartographic style. Each epoch has separate
weights for "built" and "empty" evidence:

| Epoch | Source | Weight built / empty | Coverage km² |
|---|---|---|---|
| 1821 | city plan | 0.5 / 0.1 | 4 |
| 1840 | stable cadastre (císařské otisky) | 1.0 / 1.0 | 77 |
| 1877 | city plan | 0.6 / 0.2 | 6 |
| 1880 | 3rd military survey (CENIA) | 0.4 / 0.4 | 81 |
| 1881 | city plan | 0.7 / 0.4 | 7 |
| 1891, 1895 | city plans | 0.5 / 0.5 | 25–30 |
| 1902 | city plan | 0.7 / 0.3 | 26 |
| 1908 | city plan | 0.8 / 0.6 | 9 |
| 1912 | city plan | 0.7 / 0.7 | 42 |
| 1926–1938 | city plans | 0.8 / 0.8 | 23–79 |
| 1947 | city plan | 0.9 / 0.9 | 76 |
| 1953 | orthophoto (CENIA) | 0.4 / 0.4 | 80 |
| 2001 | **ČÚZK archive orthophoto**, flown 2001 | 0.6 / 0.15 | 80 |

- The low "empty" weights of 1821, 1877 and 2001 stop a detector with low recall from pushing
  buildings later.
- Visual only: the 1781, 1864, 1893, 1950 and 1951 plans (line drawings, no fill) and the 1971 /
  1972 sheets (1972 is a *planning* drawing for Petrohrad, not a survey).

### Census and history

**Census house counts per part of the town.** Source: ČSÚ, *Historický lexikon obcí ČR
1869–2005*, I. díl (2006; censuses to 2001), okres Plzeň-město; `data/reference/csu-hlo/`.
- The PDF uses a font shifted by 29 code points. Decode with `chr(ord(c) + 29)`.
- The house counts for 1869–2001 are copied into `growth_model.py` (`CENSUS`).
- 1869–1950 "Vnitřní Město" includes all suburbs, so the town is one group:
  - Vnitřní Město 988 / 1 681 / 1 995 / 2 410 / 2 757 / 3 284 / 4 162 / 5 182 houses for
    1869–1950;
  - from 1980 it is the sum of Vnitřní, Jižní, Severní and Východní Předměstí.
- 1961 and part of 1970 are dropped because of reorganisations noted in the lexicon.

**First written mentions.** Taken from the same lexicon: Doudlevce 1227, Skvrňany 1239, Božkov
1338, Koterov 1369, Lobzy 1379, Bolevec 1382, Doubravka 1383, Hradiště 1414, Radčice 1420.
Valcha c. 1352 is from cs.wikipedia.

**Other evidence:**

| Evidence | Used as |
|---|---|
| Stable cadastre 1840 buildings without a present building | 760 historic-only footprints; demolition = first later epoch where the place is empty |
| Model c. 1536–1618 (`projects/plzen.json`) | wall ring, towers, gates (demolition years), churches, Dominican monastery (–1785) |
| **1781 plan** (city GIS = Kitelli / Strassoldo, ZČM MP 57) checked against the 1821 and 1840 plans; `scripts/fort_1781.json` | Zwinger, outer works, ramparts and moat, see §2.6 |
| Historický atlas měst ČR 21 – Plzeň (HIÚ AV ČR 2009): maps 5 (1658), 6 (Zizner 1703), 65 (demolitions since 1942) | phases of the fortification; demolished buildings in the centre |
| Written sources (`data-sources/plzen-historical.md`) | founding 1295; sieges 1433–34 and 1618; bastions 1645–49, completed 1659; glacis cleared 1647; walls demolished 1795–1849, last section 1893–99 |
| ČÚZK DMR 5G (`fetch_terrain.py`, 5 m) | terrain, building base heights |

## 2. Dating rules

1. **Map split.** For each footprint, every epoch gives *built* (share of building pixels above
   the epoch threshold), *empty* or *unknown* (outside the map). A monotone split with the
   built / empty weights gives the first built epoch.
2. **Combination with RÚIAN.**
   - An exact date is the origin. If the maps show the place built more than 10 years earlier,
     the place is dated by the maps and the RÚIAN date becomes a rebuild.
   - An age class is intersected with the map interval. If the maps are earlier, the building
     counts as rebuilt within the class. If the maps are later, the class wins.
   - Every building keeps its admissible interval (`lo`, `hi`) for the calibration.
3. **Growth front.** Within an interval, the places nearest to the built-up area of the previous
   epoch come first.
4. **Housing estates.** Tall residential blocks of Lochotín, Košutka and Vinice must be complete
   by 1992 (`ESTATE_DONE`). Their interval and RÚIAN class end there.
5. **Places built by 1840**, dated by zone:
   - inner town 1295–1335, from the square outwards;
   - glacis 1796–1840;
   - gate suburbs from 1330–1430, destroyed 1433.6 and 1618.75, rebuilt; within 260 m of the
     wall only after 1796;
   - later suburbs 1650–1840;
   - villages from their first mention, the core first;
   - isolated buildings 1650–1838.
6. **Fortification.** Positions come from the 1781 plan, which is surveyed. It was digitised by
   eye at 0.5 m/px, so expect an error of about 3–8 m. The phases come from the 1658 and 1703
   plans (§9 of the source inventory).
   - **Registration of the 1658 and 1703 plans** (`fort_plans.py`, traces in `fort_plans.json`): the
     medieval wall ring traced on each plan (west at the top) is aligned to the wall ring of the
     model by ECC on blurred masks, from a similarity start. Ring IoU 0.95 (1658) and 0.92 (1703);
     St Bartholomew and the Prague / Saxon gates of the 1703 plan land 19–32 m from the model.
     Check images: `data/historic/growth/fort/_reg_1658.jpg`, `_reg_1703.jpg`.
   - **Phases from the 1658 plan.** Around the SW, S and SE works and the NE bastion the 1658 plan
     draws small olive cores (existing) inside larger pale outlines (the proposals of 1658). Cores →
     built 1645–1649 (La Corona); the west bastion (Turkish redoubt) and the NW ravelin exist only as
     proposals → built 1658–59, the third stage named in the atlas commentary. Ramparts 1639–1649.
   - **Works of the 1703 plan.** Its south bastion and its bastion by the Mže road coincide with
     the 1781 S work and SE redoubt. The redan between them and two outer lunettes at the SW
     corner are not on the 1781 plan: modelled 1703 (March–December) to 1765–1780, lowered from
     1725–1745, basis "plan 1703 (Zizner), realisation uncertain".
   - **3D shapes.** Works and ramparts are earth bodies (`profile_mesh`): scarp to 86 % of the
     height at 1.6 m inset, parapet crest at 3.6 m, terreplein at 82 % (works 7 m, 1703 works 5 m,
     ramparts 5–6 m). The moat (16 m wide, 5 m deep) and the ditch of the W bastion (12 m, 3.5 m)
     are troughs in ~120 m sections with a water surface; while a section exists the terrain above
     it is cut out (`cuts.png`, `model.json` → `cuts`). Walls, Zwinger and gates stay extruded
     masonry. Colours in the viewer: earthworks olive, masonry grey, water blue.

   | Work | Built | 1781 | Removed |
   |---|---|---|---|
   | Medieval wall (30 m pieces) | c. 1320 | standing | year of the nearest gate; west 1828, museum piece 1896 |
   | Zwinger N / W / S | c. 1420 | standing | W 1828; others by the nearest gate |
   | West bastion, Turkish redoubt (1658: proposal) | 1658–59 | defunct (13) | levelled c. 1822 for the barracks of the 35th regiment (1823–1969) |
   | NW ravelin (1658: proposal) | 1658–59 | defunct | 1810 (gone by 1821) |
   | SW hexagonal work (1658: core) | 1645–49 | defunct | 1805 (gone by 1821) |
   | S pentagonal work (1658: core) | 1645–49 | defunct | 1800 (gone by 1821) |
   | SE redoubt (1658: core) | 1645–49 | defunct | 1833 |
   | N, NE and E ramparts along the rivers | 1639–49 | defunct | 1822 |
   | NE bastion by the arsenal (1658: core) | 1645–49 | defunct | survives (sady 5. května) |
   | 1703 redan (south front), two outer lunettes (SW) | 1703 | absent | 1765–1780 |
   | Moat and the ditch of the W bastion (as drawn in blue in 1781) | 1420 / 1658–59 | water | filled 1795–1822 by section; ditch 1822 |

   - The 1781 legend calls all outer works *"Eingegangene Vestungswerker"*. The model lowers
     them by about a third from c. 1760 (rebuild attribute `tR`).
   - The Mansfeld earthworks of 1618–1620 are named in a caption only; their shape is unknown.
7. **Demolitions 1942–2008 in the centre** (HAM map 65, `ham_demolitions.py`).
   - 184 demolished historic buildings are registered to RÚIAN (ECC 0.55). 105 of them do not
     overlap a present building and become historic-only footprints.
   - Their origin is dated by the maps. Their demolition is the last map that shows them, clamped
     to 1945–2008.
   - Inside the 30 air-raid circles of 1942–45, demolished buildings end in 1945. Present
     buildings there are rebuilt in 1946–50.
8. **Calibration to the censuses** (12 groups: the town and 11 villages).
   - Houses are buildings with a house number (RÚIAN `typstavebnihoobjektukod` 1–2) and
     historic-only footprints of at least 60 m².
   - Buildings without a number get the part of the nearest numbered building.
   - The target per census is the census count × r, where r = model houses in 2001 / census
     2001. This absorbs the frame cut and the definition of a house.
   - Houses are sorted by their current year and re-mapped by the inverse of the cumulative
     census curve (births = target + demolitions so far).
   - Each year is clamped to the building's admissible interval. Exact dates and pre-1840 places
     are not moved.
9. **Landmarks.** St Bartholomew from 1320 (tower 102 m), Franciscans 1300, water tower 1532,
   St Nicholas 1400, All Saints (older than the town), Dominican monastery 1300–1785.

## 3. Results

Buildings visible in the model:

| Year | 1300 | 1400 | 1500 | 1618 | 1700 | 1800 | 1840 | 1880 | 1912 | 1938 | 1953 | 1980 | 2001 | 2020 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| buildings | 46 | 478 | 626 | 647 | 792 | 1 261 | 1 436 | 1 936 | 4 422 | 11 084 | 15 592 | 20 355 | 23 640 | 31 715 |

### Calibration (houses: target → model after calibration)

| Group | 1869 | 1900 | 1921 | 1950 | 1980 | 2001 | Comment |
|---|---|---|---|---|---|---|---|
| Town (r = 1.14) | 1 128 → 634 | 2 750 → 1 350 | 3 748 → 3 221 | 5 914 → 4 954 | 6 133 → 5 525 | 5 714 | see below |
| Bolevec | 69 → 69 | 190 → 190 | 254 → 259 | 842 → 840 | 1 100 → 1 308 | 1 667 | |
| Doubravka | 56 → 57 | 160 → 92 | 418 → 418 | 910 → 913 | 1 046 → 1 063 | 1 142 | |
| Lobzy | 26 → 27 | 123 → 41 | 250 → 255 | 662 → 620 | 891 → 852 | 920 | |
| Skvrňany | 94 → 93 | 225 → 80 | 312 → 302 | 630 → 495 | 724 → 663 | 718 | |
| Koterov, Hradiště, Újezd, Radčice, Božkov | within ± 5 % from 1921 | | | | | | |

**Town shortfall.** The town before 1910 stays at about 55 % of the census. So does Skvrňany /
Lobzy around 1900. The houses of that period that were later demolished and replaced by fewer,
larger buildings are missing from the model. Examples are the 1960s–70s clearance of Jižní and
Východní Předměstí; the census drop from 6 783 to 5 374 houses between 1970 and 1980 points to
it. The maps do not let present buildings move earlier.

Full tables are in `data/historic/growth/web/validation.json`.

### Validation against the maps

For each epoch at its own year: *recall* is the share of the map's building pixels covered by
visible model buildings (5 px tolerance). *Precision* is the share of visible model footprints
that are built on the map.

| Epoch | 1821 | 1840 | 1877 | 1880 | 1881 | 1891 | 1902 | 1908 | 1912 | 1926 | 1931 | 1938 | 1947 | 1953 | 2001 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| recall | 0.54 | 0.70 | 0.19 | 0.07 | 0.63 | 0.61 | 0.37 | 0.53 | 0.43 | 0.51 | 0.62 | 0.64 | 0.62 | 0.43 | 0.45 |
| precision | 0.13 | 0.96 | 0.28 | 0.65 | 0.26 | 0.83 | 0.56 | 0.61 | 0.71 | 0.88 | 0.59 | 0.86 | 0.67 | 0.51 | 0.49 |

**How to read it.**
- The plans with solid fills agree with the model with precision 0.83–0.96: the stable cadastre
  1840, 1891, 1926 and 1938.
- Low values mostly measure the detector, not the model:
  - 1821, 1877 and 1881 colour only part of the buildings;
  - in 1880 the hatched blocks swallow streets;
  - in the orthophotos, roofs are found by texture.
- Missing demolished buildings lower the recall for 1902–1947.

### Basis of dating

| Basis | Buildings |
|---|---|
| maps only | 16 248 |
| maps + RÚIAN age class | 4 440 |
| RÚIAN exact date | 3 690 |
| maps, rebuilt per RÚIAN (date or class) | 4 747 |
| RÚIAN class, maps later | 2 552 |
| 1840 cadastre + zone rules | 648 |
| 1840 cadastre, demolished | 760 |
| fortification / landmarks | 154 |

## 4. Viewer, terrain and water

- **Display.** Merged mesh with a vertex shader. Per vertex only the position (relative height
  0–1) and the building index; dates, heights, base, gaps and colours come from a per-building float
  texture. Buildings stand on the terrain (base = lowest terrain point under the footprint). They rise over 3 years, sink at demolition, vanish during
  the siege gaps and change height when rebuilt. New buildings flash yellow. The moat is blue.
- **City 3D models.** Present buildings with a multipatch in the City of Plzeň 3D model 2024
  (`city3d_mesh.py`; 37 467 objects matched by containment to 31 367 RÚIAN buildings) are drawn with
  their real triangles instead of an extruded footprint. The shape is kept for the whole life of the
  building in the model (no lower pre-rebuild height, `tR` dropped), so St Bartholomew has its present
  form from 1320 on and its separate tower block is removed. This is schematic: older states of the
  buildings are not reconstructed.
- **Terrain.** DMR 5G at 10 m: a 450 × 450 mesh, heights in `terrain.png` (16 bit in R / G,
  0.1 m).
- **Water per epoch.**
  - Water masks for 1840 (cadastre), 1908 and 1938, each united with the present water, plus the
    present water from 1953.
  - The ground is lowered by 2 m in the water of the current epoch, so old meanders and mill
    races appear as channels.
  - Present water bodies stay in every epoch: the Bolevecký pond (1460) and the České údolí
    reservoir (1970s) appear too early.
- **Ground maps by validity.** Each map is shown from its year until the next one:
  - base, then 1781, 1821, 1840, 1877, 1881, 1893, 1902, 1908, 1926, 1938, 1947;
  - orthophoto 1953, orthophoto 2001, ZTM 10 from 2015.
- **View mode** (select a view in the header). It prepares the material for mapping vedute onto
  the model:
  - The camera goes to the view's default viewpoint and year (`VIEW_DEFAULTS`), e.g.
    Ottheinrich from the south-south-west, 1536. Willenberg is from the north-east, 1602.
    Bird's-eye plates are seen from above in the south.
  - The drawing is shown in the left panel with an opacity slider. A *silhouette* switch shows
    the town shape against white.
  - Churches, gates, towers and monasteries are labelled in 3D.
  - Click a building in 3D (GPU picking), then the same object in the drawing. This creates an
    annotation (`entityId` = `ruian:<kód>`, `h1840:<n>`, `g1618-…`, `fort:…`) in
    `projects/plzen.json`, so the mapper and the exports see it.
  - The link stores the 3D surface point under the click (`xyz`, second picking pass into a float
    target).
  - *Fit camera* solves position, rotation and focal length of the draughtsman's camera from ≥ 5
    links: Levenberg–Marquardt on the image residuals, Huber-like weights, start from the current
    3D camera. Older links without `xyz` use the top (towers, churches, gates) or 70 % of the height
    (houses) of the linked building with a lower weight. Residuals are drawn on the drawing (green
    < 15 px, orange < 40 px, red). First result: Theatrum Europaeum 1618, 14 usable links, 65 px RMS
    on a 3 000 px plate.
  - *Project drawing* paints the drawing from the fitted camera onto buildings and terrain
    (projective texturing; a depth map rendered from the fitted camera hides surfaces the
    draughtsman could not see).
  - *Save view* stores the camera in the source (`view`, with `quat`, `aspect` and the fit).
- **Video export.** Fixed 30 fps steps. Frames carry the year, caption, legend, labels and
  credits. Encode them with `encode_video.py` (ffmpeg from `imageio-ffmpeg`).

## 5. Caveats and next steps

- **Missing demolished buildings.** Houses demolished between epochs after 1840 are missing. They
  cause the town's census shortfall. Vectorising the 1891 / 1926 / 1938 / 1947 plans the way the
  1840 cadastre was done would add them as historic-only footprints.
- **Pre-1840 positions are schematic.** Next: per-block presence from the TE 1618 plate (legend D
  = burned suburbs). Also use the view links created in the view mode as evidence.
- **Fortification.**
  - The bastions are from the 1781 plan; the 1703 plan (AMP inv. 2727/1-4) is still to be
    requested.
  - Glacis and outer ditch are not modelled.
- **Detectors.**
  - The 1821, 1877 and 1881 plans and both orthophotos need better building detection.
  - A segmentation model (SAM, as for the cadastre) would raise recall.
- **Ancillary buildings.** Garages and sheds follow the maps and appear late.
- **Further date sources.** See `data-sources/plzen-historical.md` §7–8: Profous, Schaller,
  Sommer, Berní rula, NPÚ, Encyklopedie, postcards and photographs.
