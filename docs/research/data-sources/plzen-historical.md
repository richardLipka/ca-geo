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

## 6. Pre-1800 sources (second round, 2026-11-23)

Focused searches on medieval and early-modern material: iconography and maps, fortification
plans in military / state archives, written and archaeological sources. Automated searches
were blocked at Riksarkivet (CAPTCHA), Gallica (403/503), Heidelberg diglit, digilib.phil.muni.cz
(CAPTCHA) and several Czech portals — "not found" there means "not searched", not "absent".

### Views and siege images (additions)

| Item | Date | Holder / licence | Note |
|---|---|---|---|
| Wall painting, view from NE (Dominican cloister) | c. 1500–25 | fragment in ZČM; Průzkumy památek 1997/2, fig. 15 | oldest view; Commons "Pilsen in 1515" is a modern redrawing |
| G. de Statia, Crucifixion with view from SW (town hall) | 1574 | in situ; ibid., fig. 26 | double wall, turrets on SE outer wall; proportions judged reliable |
| Hogenberg workshop, *Beleg van Pilsen, 1619* (key A–Y) | 1619–21 | Rijksmuseum RP-P-OB-78.785-365, CC0 | longest legend of the 1618 siege images |
| Keller etching, Halle impression | 1619 | Kunstmuseum Moritzburg MOIISt00199; image PDM | better free copy than Kramerius UK |
| *Warhaffter Bericht* with Halbmayr copperplate (Nürnberg) | 1619 | Regensburg 999/Caps.9(12 → BSB bsb11086816, NoC-NC; Ossolineum copy | plate probably not in the scan (TBV) |
| W. Hollar, *Pilsen / Plzen* (P812) | 1640s (TBV) | Fisher Library Toronto; Commons PDM | small profile, likely after Willenberg |
| G. Bodenehr (attr.), *Plan und Ansicht … Pilsen* | c. 1700 | DHM Do 2002/81, CC BY-NC-ND 4.0; copy AMP G18 | copies Merian 1650 |
| J. Lautner, bird's-eye view from SE | 1773 | ZČM (shelfmark TBV); PrP 1997/2, fig. 27 | state just before demolition |
| TE plate, UB Augsburg 600 dpi scan | 1635 / 1618 | urn:nbn:de:bvb:384-uba000237-1 | Janata et al. 2013: 29 GCPs, RMSE 18 m (inner town), 107–227 m (sheet) |

No F. B. Werner view of Plzeň was found (Werner drew Rokycany and Bor; a Plzeň sheet may
exist — check Marsch 1995). Key catalogue for remaining ZČM holdings: Mergl 1995,
*Plzeňské pohledy a veduty čtyř století 1500–1900*.

### Fortification plans

- **Plan of the core with fortification, 1703** — Archiv města Plzně inv. 2727/1-4; viewer
  only (four-part B/W copy, east up), not among the REST services. Likely linked to the
  "extensive reconstruction of the fortification" event of 3/1703 (Encyklopedie). Oldest
  detailed bastion plan found; top request priority.
- **du Portal atlas, French campaign 1741–42** (BnF, shelfmark TBV) — Nechvátal 2016
  (*Archaeologia historica* 41/2, doi:10.5817/AH2016-2-11) says du Portal drew plans of Cheb,
  Bor, Plzeň, Beroun and Prague; whether the Paris atlas holds the Plzeň sheet is TBV.
- Royal Collection RCIN 728063.m (camp "near Alt Bilsen", 1742) — probably Starý Plzenec;
  low value.
- No Pilsen plan web-indexed at Kriegsarchiv (series KPS KS G Städtepläne, KPS GPA Inland C),
  Krigsarkivet, Dresden, Berlin, VHA, Národní archiv.

State of knowledge: bastion work began at the end of 1618 (Památkový katalog) and was
carried out mainly under commander J. de la Corona / Lacron 1645–49 (suburb cleared 1647),
completed by c. 1659 (engineer named "Ziznera" in the Encyklopedie — spelling TBV); deep
moat flooded from the Radbuza, drawbridges, new Říšská gate; one pentagonal bastion (1645)
survives in sady 5. května. No further investment in the 18th c. except 1703. Pražská
bašta demolished 1795. **Bastion count, names, ravelins and moat width are not stated
reliably in any online source**; a blog (Zestínu 2022, citing Anderle) places remains at
about 6–8 locations around the ring (unverified).

### Fortification 1620–1780: third round (2026-11-23)

Targeted search for views, paintings and plans that show the bastioned fortress between the
1618 siege and the start of demolition (1795). "Checked" means opened or inspected; "lead" means
found in a catalogue or literature only.

| Item | Date | Holder / access | What it shows | Status |
|---|---|---|---|---|
| J. G. (Mauritius) Vogt, *Pilsen* plan (in *Das jetzt-lebende Königreich Böhmen*, 1712) | 1712 | Commons, CC BY-SA 3.0; local `data/historic/sources/vogt-1712.jpg` (1920 px) | complete bastioned trace in plan view: 5 bastions with ravelins and a covered way on the south / west, a hornwork-like front on the north, outer works and ravelin along the Radbuza in the east. Legend: Prager, Neue, Nürnberger, Blassen Thor; west is at the top. Schematic copper engraving | **checked**. Best available image of the full trace before 1781. Georeference it in the mapper (square, church, gates) and digitise it as the 1712 state |
| J. Ch. Müller, manuscript map of Bohemia with *Ichnographica duarum … urbium … Budweis et Pilsen* (town plan 1:4 300) | c. 1718 | ÖNB Vienna, AB 55 a 1* Kar. (Čada & Vichrová 2009, *Kartografické listy* 17) | military engineer's ground plan of Plzeň with fortification | **lead, high value**. Not found online. Request a scan from the ÖNB Kartensammlung |
| Müller's draft for the printed map, 25 sheets | 1721 | ÖNB FKB C.51:1-25 Kar. | town outline (small scale) | lead |
| Military plan *Situations Plan der königl. Kreisstad Pilsen*, survey under Count Strassoldo, captain Th. de Kitelli | 1781 | ZČM MP 57 (OldMapsOnline record); = city GIS `GIS_HIS_Plzen_1781` | full fortification before demolition | **used** (`fort_1781.json`) |
| Plan of the core with fortification | 1703 | Archiv města Plzně inv. 2727/1-4 (viewer only) | bastions after the 1703 reconstruction | lead (request; see §6) |
| du Portal, plans from the French campaign | 1741–42 | BnF (shelfmark TBV); Nechvátal 2016 | plan of Plzeň during the French / Bavarian occupation | lead |
| Austrian camp near "Alt Bilsen" | 1742 | Royal Collection RCIN 728063.m | army camp; probably Starý Plzenec | checked; low value |
| Teutschmeister field camp near Pilsen | after 1696 | Landesarchiv BW, Staatsarchiv Sigmaringen (FAS PA plans) | camp layout near the town | lead; low value |
| J. Lautner, bird's-eye view from the SE | 1773 | ZČM (photo in Průzkumy památek 1997/2, fig. 27) | town and works just before demolition | lead (ZČM scan) |
| G. Bodenehr (attr.), *Plan und Ansicht … Pilsen* | c. 1700 | DHM Do 2002/81; local copy | copies Merian 1650 | checked; no independent value |
| M. Merian, *Pilsen* (Topographia Bohemiae) | 1650 | BSB; local copy | the medieval double wall and towers. It does **not** show the bastions of 1645–49, so it follows an older model | checked; use for the walls, not the bastions |
| *Abbildung der Statt Pilsen … durch Gen. von Mansfeld belägert* (re-issue) | c. 1700 | Mapová sbírka UK (Europeana) | 1618 siege plate re-issued | checked (record) |
| Plan der Belagerung Pilsens 1618 | 1618 | MAK Vienna, collection online | siege plan | lead (one more 1618 variant) |
| 1st military survey sheet | 1764–68 | Kriegsarchiv; view on Arcanum Mapire | fortress outline at 1:28 800 | lead (view only; no open WMS) |
| F. B. Werner | c. 1740 | Mollova sbírka MZK holds Werner views (titles not resolvable automatically) | no Plzeň view confirmed | not found |
| Votive / altar paintings with a view of the town (plague column 1681, Marian images) | 17th–18th c. | Muzeum církevního umění plzeňské diecéze, ZČM | none with a town view found online | not found |

Europeana (API, 1600–1800, "Pilsen"/"Plzeň", 126 records) has otherwise only 1618–1634 news
pamphlets, the Merian view, the Homann *Circulus Pilsnensis* (1769, small scale) and Schaller.

**Assessment.** For the shape of the bastioned fortress, three sources are usable:
1. **Vogt 1712** (online, schematic but complete);
2. **Kitelli 1781** (online, surveyed);
3. the **1703 AMP plan** and the **Müller c. 1718 ichnography**, both to be requested.

Together with the 1821 / 1840 plans for the demolition sequence, they would allow a
1659 → 1712 → 1781 → 1821 series. The views of 1650–1700 (Merian, Bodenehr) repeat an older
model and should not be used for the bastions.

### Written sources

| Source | Content | Access |
|---|---|---|
| Strnad (ed.), *Listář král. města Plzně* I, 1300–1450 (1891) | charters, town-book entries: houses, malt-houses, gate suburbs | NK Kramerius `uuid:d7daf450-40fc-11dd-8d2a-000d606f5dc6`, PD, page OCR |
| *Listář* II, 1450–1526 (1905) | incl. 1457 charter on repairing ruined walls, 1453 plot before Litická brána | Internet Archive `listarkralovske01strngoog` (metadata mislabelled), PD, OCR |
| Šimon Plachý z Třebnice, *Paměti plzeňské*, ed. Strnad (1883) | chronicle c. 1560–1609: fires, buildings | MZK `uuid:1456cc10-06fc-11eb-b34d-005056827e51`; IA `mimonaplachhoz00strn`, PD |
| J. Schaller, *Topographie des Königreichs Böhmen* 9, *Pilsner Kreis* (1788) | 315 houses in town + 142 in Prague, Small and New suburbs | BSB `bsb11094711`; IA `11094711bsb`, PD, Fraktur OCR |
| *Fontes rerum Bohemicarum* V (1893) | Hussite sieges 1421–34 | sources.cms.flu.cas.cz bookid 1103 |
| *Sborník Městského historického musea* I–III (1909–14) | topographic studies (Strnad, Macháček) | SVK PK Kramerius, public |
| Strnad, *O založení král. města Plzně* (1894) | founding plan | SVK PK, on-site only |
| Orna & Dudková 2012, *Archaeologia historica* 37/1 | archaeology of the Hussite sieges | open, manual download (CAPTCHA) |
| Kodera 2004; Bělohlávek et al. 1965 *Dějiny Plzně I*; *Minulostí Západočeského kraje* | 17th-c. fortification; synthesis | library / DNNT only — validation, not bulk mining |
| Berní rula 1654, Theresian (1748–57) and Josephine (1785–89) cadastres | house lists | archives; nothing digitised found; Plzeň in Berní rula TBV |

### Archaeology (AMČR)

Querying the AIS CR digital archive for the box 49.743–49.752 N, 13.370–13.384 E returns
**195 public fieldwork events** (leaders: Široký 58, Frýda 32, Postránecká 22, Nováček 17);
25 mention walls, gates, moat or fortification; many give house number and street. Stored
locally (not versioned) in `data/reference/plzen-amcr/` (CC BY-NC 4.0 metadata) and plotted
on the 1781 / 1840 plans in the overview page.

### Archive requests (ranked)

1. Archiv města Plzně — scan of the 1703 plan with scale and author; 1703 reconstruction
   file; other 17th–18th-c. fortification plans.
2. ÖStA Kriegsarchiv — "Pilsen" in KPS GPA Inland C (Böhmen) and KS G Städtepläne (by e-mail).
3. BnF — du Portal atlas shelfmark and Plzeň sheet.
4. Krigsarkivet — manual search "Pilsen" (Sveriges krig; Utländska stads- och fästningsplaner).
5. ZČM — photographs of Hauer (G 141), Seeblummer (G 182), Lautner (1773); Mergl 1995.
6. Library — Kodera 2004, HAMČR 21 (2009), *Dějiny města Plzně I* (2014).

## 7. Origin of villages and buildings in the surroundings (third round, 2026-11-23)

Goal: replace interpolated dates in the growth model (`docs/research/plzen-growth-model.md`)
outside the old town. The checks were run on 2026-11-23. "Checked" means queried or opened. "Lead"
means found in a catalogue or literature but not opened.

### Village origin (first mention, size over time)

| Source | What it gives | Access | Status |
|---|---|---|---|
| cs.wikipedia village articles | first written mention per village (used: 11 villages) | MediaWiki API, CC BY-SA | checked, used |
| Wikidata P1249 (*time of earliest written record*) | 19 items within 6.5 km of the square, e.g. Křimice 1251, Malesice 1239, Bukovec 1379, Červený Hrádek 1384, Radobyčice 1444, Újezd 1115, Nová Hospoda 1720 | SPARQL `wikibase:around`, CC0 | checked. **Conflicts with Wikipedia**: Doubravka 1383 vs 1338, Hradiště 1414 vs hammer works 1686 (court vs hamlet). Needs source-level resolution (Profous) |
| A. Profous, *Místní jména v Čechách* I–V (1947–60) | the standard dated attestations of every place name (year + charter) | print. No digitised copy found online (NDK / Kramerius not checked directly) | lead. **Best authority for first mentions**: 15–20 entries to transcribe by hand |
| ČSÚ, *Historický lexikon obcí ČR 1869–2011* / dataset 170240-17 | **population and number of houses per municipality part** at every census 1869–2011 (Bolevec, Doubravka, Lobzy … are parts) | csu.gov.cz, open data (part-level edition = PDF / XLS TBV) | lead. **Highest value**: house counts per village per decade calibrate the interpolation (target counts per epoch instead of map pixels). Definitions differ by census (houses total vs. occupied 1961–80) |
| Schaller, *Topographie* 9 (1788) | houses per village and suburb | BSB `bsb11094711`, PD, Fraktur OCR | in inventory. To extract: house counts per village for 1788 |
| J. G. Sommer, *Das Königreich Böhmen* 6, *Pilsner Kreis* (1838) | houses and inhabitants per village c. 1837, owners, churches, mills | BSB scan (DDB, URN `urn:nbn:de:bvb:12-bsb10709663-4`), no-copyright / non-commercial | lead. Second calibration point before the 1840 cadastre |
| Berní rula 1654, Kraj Plzeňský (edition vols 23–25) and the 1757 Theresian cadastre | settled / deserted farmsteads per village after the Thirty Years War | print edition; Národní archiv PDFs exist for some regions (`nacr.cz/…/Plzensko_cele_H_zamceno.pdf` — content TBV) | lead. Gives **1654 farmstead counts** (war damage), the only quantitative point between 1618 and 1788 |
| ČÚZK archive (`ags.cuzk.gov.cz/archiv`, Archiv-WEB): indikační skici, císařské otisky per cadastral territory | colour-coded 1838–41 maps for Bolevec, Doubravka, Lobzy … with house numbers; also later reambulations | online viewer, per sheet | lead. The city mosaic used so far covers 77.5 km² of the 81 km² frame. The indication sketches would add **house numbers** (link to Sommer / Schaller) |
| Müller's map of Bohemia (1720) and 1st military survey (1764–68) | presence and rough size of villages, mills, farmsteads before 1788 | geolab.cz (oldmaps moved to `geolab.cz/stare-mapy`), Arcanum Mapire (view only); CENIA has no 1st-survey WMS (HTTP 404) | checked: no open WMS found. Use as visual evidence only |
| OpenHistoricalMap | administrative history of Plzeň (e.g. relation 2853498: Plzeň 1924–42 with Doubravka, Doudlevce, Lobzy) | API, CC0 | checked (search). Join dates of villages to the town as polygons |
| Diploma thesis Hemanová (theses.cz `j0q9dd`), the medieval hinterland of Nová Plzeň | villages subject to the town (Lobzy, Doubravka …), medieval references | theses.cz PDF (download redirected, TBV) | lead |
| Obecní kroniky (Porta fontium, SOA Plzeň; ≈ 5 100 chronicles) | local building events 1920s–1990s | online scans, handwritten | lead; low priority (manual reading) |

### Building origin (individual buildings)

| Source | What it gives | Access | Status |
|---|---|---|---|
| RÚIAN `dokonceni`, `pocetpodlazi` | completion year (or age class) for 15 868 of 32 425 buildings in the frame | open data | checked, used |
| Wikidata P571 / P576 | 383 items with inception within 6.5 km, but mostly statues, plaques, bridges. Only ≈ 30 houses and churches; pre-1800 only 18 (century precision: "1400") | SPARQL, CC0 | checked. Low value for footprints; churches only |
| NPÚ Památkový katalog | ≈ 390 monuments in Plzeň with dating ("datace od–do" fields added 2024) | web + Geoportál NPÚ (`geoportal.npu.cz`), no documented JSON API | lead. Bulk export on request (open question below) |
| Encyklopedie dějin města Plzně | 362 buildings with "vznik" and building history; also entries for villages and their incorporation | crawlable HTML, no terms | in inventory; needs permission before reuse |
| *Soupis památek historických a uměleckých* — Plzeň district volume | dated churches, castles, chapels of the villages (c. 1900) | other district volumes are on archive.org and Kramerius; Plzeň volume not located | lead |
| AMČR (archaeology) | excavation evidence of early-medieval settlement (Doubravka, Košutka) | api.aiscr.cz, CC BY-NC 4.0 | in inventory; settlement presence, not buildings |
| ČÚZK DMR 5G (`ags.cuzk.gov.cz/arcgis2/rest/services/dmr5g/ImageServer`) | terrain (lidar) | open | checked (service listed). Terrain for the 3D model, not dating |

### Recommended order

1. **ČSÚ house counts per municipality part, 1869–2011.** Turn them into target counts per
   village and census. Then rescale the interpolated origin years so the model reproduces the
   counts. This is the largest gain for 1869–1950, where the maps disagree.
2. **Profous** (library) for the ≈ 20 villages and hamlets in the frame. It resolves the
   Wikipedia / Wikidata conflicts.
3. **Schaller 1788, Sommer 1838 and the 1654 Berní rula**: house and farmstead counts per
   village. This gives three calibration points before 1840, including the war loss after
   1618.
4. **Indication sketches** for the village cadastres: house numbers on the 1840 footprints.
5. **NPÚ export, Encyklopedie (with permission) and Wikidata churches**: exact dates for
   landmark buildings.

Used since then:
- ČSÚ *Historický lexikon obcí ČR 1869–2005* I. díl (censuses to 2001) (`13n106cd1.pdf`, 21 MB). It has house counts
  and first mentions per part of Plzeň. The PDF text is shifted by 29 code points, so decode with
  `chr(ord(c) + 29)`. Its house counts calibrate the growth model.
- The 1869–2011 edition on csu.gov.cz offers only district- and ORP-level XLSX. Its part-level
  section III is loaded dynamically and was not reachable.

## 8. Postcards and photographs for façades (19th – early 20th century)

Goal: images of house façades for texturing the model buildings, as façade facets like the TE
1618 facets. A view of a known street has to be matched to RÚIAN buildings. The view mode of
`growth3d.html` links an image point to a building id. A rectified façade texture would follow.

| Source | Content | Access / licence | Status |
|---|---|---|---|
| ZČM — Národopisné muzeum Plzeňska, glass negatives (`negativy.zcm.cz`) | ≈ 800 plates of the Kroužek přátel starožitností (from 1910, "KPS") and Ladislav Lábek (from c. 1912, "L"): historic buildings, streets, interiors 1910–1950 | online database; reuse terms TBV | **checked (description page)**. Best single source of dated façade photographs of the old town; books *Plzeň očima Ladislava Lábka* (2003), *Plzeň na skleněných negativech* (2018) |
| Archiv města Plzně, Digitální archiv (`digiarchiv.plzen.eu`) and Encyklopedie Plzně | photographs, building files and plans; period photos per building in the Encyklopedie | online; publication needs consent | lead (in inventory §3) |
| Bayerisches Hauptstaatsarchiv / Sudetendeutsches Archiv, postcards in the Deutsche Digitale Bibliothek | "Gruß aus Pilsen" cards before 1900 and c. 1900: square, town hall with the Marian column, gymnasium, Smetana park, viaducts, Lochotín; publishers A. H. Bayer, W. Steinhauser, T. Marese | DDB item pages, scans, rights per item | **checked (search)**: [example](https://www.deutsche-digitale-bibliothek.de/item/VRDFMRZUNDCAV6AS7EUSP34KA7A4YAVK?lang=en) |
| Europeana (API, `wskey=api2demo` for tests) | 110 image records "Pilsen OR Plzeň", 1860–1945 | API, per-record rights | **checked (count only)** |
| Univerzita Karlova Kramerius: glass slides of vanished buildings, town hall, mill, portals (1900–45) | already in inventory §2 | Kramerius UK, public | lead |
| Hungaricana (Szerencs postcard collection) | single cards, e.g. "Pozdrav z Plzně" | online, per item | checked (one item) |
| Wikimedia Commons | old postcards / photographs of Plzeň (category names to resolve) | CC / PD | API returned nothing for the guessed category names; search by hand |
| *Velká kniha plzeňských pohlednic* (Starý most, 2008) | printed postcard catalogue | print | reference for dating and locating cards |
| SVK PK, Městská knihovna Plzeň, ZČM sbírky | possible postcard collections | not found online | ask |
| Commercial (akpool, eBay, delcampe) | thousands of cards | view only, not reusable | dating and location aid only |

Recommended workflow:
1. Harvest the DDB / Europeana records (metadata + image URLs) into a list with street or
   building keywords.
2. Pick views with a known standpoint (square, Pražská, Solní, Riegrova; station; brewery).
3. In the view mode, fix the camera and link 4 or more buildings, then rectify each façade:
   homography of the four façade corners, as in `facet_textures.py`.
4. Use the photographs of ZČM (Lábek) and the city archive after their terms of reuse are
   confirmed.

## 9. Historický atlas měst ČR 21 – Plzeň (HIÚ AV ČR 2009) and other sources (2026-11-24)

The atlas is a free PDF of 141 pages, 60 MB:
`obchod.hiu.cas.cz/user_uploads/Knihy ke stažení/historicky_atlas_mesta_plzne.pdf`.
It contains a historical overview (pp. 6–41), 67 maps on map sheets (pp. 42–103) and map
commentaries (pp. 112–124). It is stored locally in `data/reference/hiu-atlas/` and not
versioned, because it is © HIÚ AV ČR and the holders; it is used for research only. Map pages
are rendered with `scripts/atlas_pages.py` (sources `ham-*` in the mapper).

### Maps relevant to the model

| Map | Content | Use |
|---|---|---|
| 5 | *Delineation der Stadt Pilsen, wie die anitzo sich befunden thuet …*, Prague, 23 Feb 1658; plan and profile, ÖStA-KA. The state "as it is now" and the proposal of General de la Corona to add works and ravelins *ad interim*; works lettered a–h | **used** (registered, `fort_plans.py`): olive cores = existing works → 1645–49; pale outlines = proposals → built 1658–59 (west bastion, NW ravelin). The profile gives wall / rampart heights |
| 6 | J. Ch. Zizner, *Grund-Ris … in A. 1703*, ÖStA-KA GPA Inland C IV α Pilsen Nr. 2, 695 × 515 mm, west at the top | **used** (registered, `fort_plans.py`): further bastions and ravelins on the south and west fronts. The legend separates realised from planned works (not read). Two of its south works are the 1781 S work and SE redoubt; the redan between them and two SW lunettes are modelled 1703–1780 as "realisation uncertain". Vogt 1712 is a simplified copy of this plan |
| 9 | 1st military survey, sectio 156 (1780–83), ÖStA-KA | town outline at 1:28 800 (check against 1781) |
| 10 | Kitelli / Strassoldo 1781 (ZČM MP 57) = city GIS `GIS_HIS_Plzen_1781` | **used**. Legend: 7 Blinde Thor, 8 Neuthor, 9 Pragerthor, 10 Kleinthor, 14 Zeughaus, **13 "Eingegangene Vestungswerker"** (defunct works) |
| 12 | Josef z Točenovic, *Situationsplan … 1821* (AMP M 679), c. 1:2 510 | = city GIS 1821. It separates old / new houses, barns and garden houses, so it is the best pre-cadastre source for buildings |
| 46–50 | vertical aerial photographs 1938, **1945 (USAAF, 9 Apr 1945)**, 1972, **1988**, 2008 (VGHMÚř / Škoda archive / GEOREAL) | 1972 / 1988 cover the northern estates; usable for checking dates (not georeferenced; atlas quality) |
| 57 | topography of medieval Nová Plzeň c. 1410 (R. Široký, M. Wasková): walls, gates after the 1658 plan, extent of the suburbs from written sources | **used** (`ham57.py`, ring IoU 0.93): blocks for the generated inner houses, suburb blocks and walls, medieval moat, river courses, Dominican church outline; ground map from 1300 |
| 58 | extent of the 1507 fires (M. Wasková) | event layer (next step) |
| **65** | **demolitions of historic buildings in central Plzeň 1945–2008 and air-raid damage 1942–45** (P. Domanický) | **used**: `scripts/ham_demolitions.py` registers the page to RÚIAN, then extracts 184 demolished-building polygons and 30 air-raid sites. The registration is an initial scale-bar similarity followed by coarse-to-fine ECC, correlation 0.55; the rotation of 8.6° is the meridian convergence of S-JTSK. 105 of the polygons do not overlap a present building and are added to the model |
| 2–4, 21–28, 32–44 | Müller 1720, Kreybich 1830, plans c. 1840–1947, regulation plans, Škoda, brewery, 1988 territorial plan | context; the city GIS has most of the plans georeferenced |

**Map 66.** Map 66 (second cellars in the western part of the core) and the commentaries
(fortification phases, demolitions, suburbs) are worth reading in full for the next round.

### Müller's map (c. 1720), detail "Bolevec"

The Commons file `Müllerovo mapování - Bolevec.png` is 325 × 336 px, public domain. It shows
Pilsen as a walled town with a schematic star-shaped fortification, Malice ("Omn. Sanct."),
Bolevec ponds, Radčice, Skvrňany, the post house and "Kodiken" (Kotíkov).
Small scale (1:132 000), so it confirms existence but not shape. Stored in
`data/reference/mueller/`. The manuscript ichnography 1:4 300 (ÖNB) remains the source to
request.

### ČÚZK archive (`ags.cuzk.gov.cz/archiv/`)

The application shows archival maps (indikační skici, císařské otisky, reambulations) and the
archive of aerial survey photographs. Its image services (`arcgis4/rest/services/Archiv/
archiv_nespojene_{stable,nonstable,skici}/ImageServer`) need a short-lived token that the web
application generates for itself. The scans are offered for viewing; downloads go through the
ČÚZK e-shop. They were **not** harvested by script. Ordering the indication sketches of Plzeň and
the villages from the e-shop, or confirming that the terms allow automated use, is the owner's
decision.

## Open questions

- Licence for reuse of the city's `GIS_Historicke` rasters (rules point 4 says CC BY-SA 4.0
  for map services; services state nothing) and of the ČÚZK cadastre mosaic.
- Kriegsarchiv / AMP / SOA holdings of fortification plans; WLB 1620 plan digitisation.
- Plzeň house renumbering years and a concordance source.
- NPÚ JSON API (dating, defunct objects) or a bulk export on request.
