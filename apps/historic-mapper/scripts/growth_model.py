"""Schematic 3D growth model of Plzeň 1295-2020: every building gets an (interpolated) year of
origin, optional rebuild and demolition, consistent with the available evidence.

Evidence, in order of trust:
1. RÚIAN building footprints (present stock) with completion date `dokonceni`; dates that are
   age-class placeholders (31 Dec 1919 / 1945 / 1960 / 1970 / 1980 / 1990 / 2000) are intervals.
   Heights from the City of Plzeň 3D building model 2024 (joined by parcel), else from floors.
2. Building pixels of 16 georeferenced map epochs (city plans 1821-1947, stable cadastre 1840,
   3rd military survey 1880, orthophotos 1953 and 2001) at each footprint → first epoch in which
   the place is built (monotone split with separate weights for "built" and "empty" evidence, so
   that detectors with low recall cannot push a building later).
3. House counts per part of the town (ČSÚ Historický lexikon obcí ČR 1869-2005, censuses 1869-2001): the
   origin years of houses (buildings with a house number) are re-mapped per part so that the
   model reproduces the census counts, within the bounds of items 1-2.
4. Before 1840 (place already built on the stable cadastre): dated by zone and written history —
   inner town settled after the founding (1295-1335, from the square outwards); medieval gate
   suburbs (burned 1433-34 and 1618, glacis cleared 1647, rebuilt after 1795); villages from their
   first written mention (ČSÚ lexicon); later suburbs and isolated buildings 1650-1840.
5. Buildings of the stable cadastre that no longer exist → historic-only footprints; their
   demolition is the first later epoch where the place is empty.
6. Fortification: medieval wall ring, towers and gates (model c. 1536-1618); Zwinger and the
   works of 1645-1658 (the "Schantzen" of the 1658 plan) digitised from the 1781 plan (fort_1781.json), defunct by 1781, demolition dates
   from the 1821 / 1840 plans and written sources; moat.
Within an interval the year follows the growth front: places closer to the built-up area of the
previous epoch are dated earlier. Terrain: ČÚZK DMR 5G; water per epoch from the maps.

usage: python growth_model.py   (paths relative to the repository)
writes data/historic/growth/web/model.json, terrain.png, ground_*.jpg, water_*.png, validation.json
"""
import datetime, json, math, os, random
import cv2
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from growth_rules import BBOX, RES, N, to_px, to_map, imread, rule, coverage, hsv, building_mask

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, 'data', 'historic', 'growth', 'raw')
OUT = os.path.join(ROOT, 'data', 'historic', 'growth', 'web')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(1295)

# map epochs: (raster, year, weight of "built" evidence, weight of "empty" evidence, pixel share threshold)
EPOCHS = [('1821', 1821, 0.5, 0.1, 0.12), ('1840_cadastre', 1840, 1.0, 1.0, 0.2), ('1877_mesto', 1877, 0.6, 0.2, 0.15),
          ('1880_vm3', 1880, 0.4, 0.4, 0.2), ('1881', 1881, 0.7, 0.4, 0.15), ('1891', 1891, 0.5, 0.5, 0.2),
          ('1895', 1895, 0.5, 0.5, 0.2), ('1902', 1902, 0.7, 0.3, 0.12), ('1908', 1908, 0.8, 0.6, 0.15),
          ('1912', 1912, 0.7, 0.7, 0.2), ('1926', 1926, 0.8, 0.8, 0.2), ('1931', 1931, 0.8, 0.8, 0.2),
          ('1938', 1938, 0.8, 0.8, 0.2), ('1947', 1947, 0.9, 0.9, 0.2), ('1953_orto', 1953, 0.4, 0.4, 0.2),
          ('2001_orto', 2001, 0.6, 0.15, 0.1)]
YEARS = [e[1] for e in EPOCHS]
K40 = next(i for i, e in enumerate(EPOCHS) if e[0] == '1840_cadastre')
CLASS_END = {1919: None, 1945: 1919, 1960: 1945, 1970: 1960, 1980: 1970, 1990: 1980, 2000: 1990}  # RÚIAN age classes
SQUARE = (-822396.8, -1069689.4)  # St Bartholomew, centre of the square

# villages: first written mention (ČSÚ Historický lexikon obcí 1869-2005; Valcha from cs.wikipedia); Malice = Roudná
VILLAGES = {
    'Skvrňany': ((-826599.1, -1071139.1), 1239), 'Doudlevce': ((-822166.5, -1073163.7), 1227),
    'Malice (Roudná)': (None, 1250), 'Božkov': ((-818286.0, -1071613.8), 1338), 'Doubravka': ((-819089.0, -1069692.9), 1383),
    'Valcha': ((-825336.9, -1072906.6), 1352), 'Koterov': ((-818903.4, -1073770.1), 1369), 'Lobzy': ((-819992.2, -1070748.4), 1379),
    'Bolevec': ((-821245.7, -1065654.0), 1382), 'Radčice': ((-826001.3, -1067270.2), 1420), 'Hradiště': ((-821662.9, -1074027.4), 1414),
}

# houses per part of the town at the censuses (ČSÚ, Historický lexikon obcí ČR 1869-2005, I. díl, okres Plzeň-město).
# Parts are RÚIAN části obce; 1869-1950 "Vnitřní Město" includes all suburbs (Jižní, Severní, Východní
# Předměstí); 1970 values are dropped where the lexicon notes boundary changes (1961-70).
CENSUS_YEARS = [1869, 1880, 1890, 1900, 1910, 1921, 1930, 1950, 1970, 1980, 1991, 2001]
CENSUS = {
    'town': ({406392, 406368, 406317, 490318}, [988, 1681, 1995, 2410, 2757, 3284, 4162, 5182, None, 5374, 5221, 5007]),
    'Bolevec': ({122122}, [69, 96, 116, 191, 214, 255, 523, 846, 855, 1105, 1471, 1674]),
    'Božkov': ({122297}, [73, 94, 107, 134, 178, 200, 407, 516, None, 533, 552, 573]),
    'Doudlevce': ({490288}, [46, 62, 86, 149, 177, 230, 362, 446, None, 480, 493, 479]),
    'Hradiště': ({122343}, [11, 11, 12, 15, 15, 19, 57, 163, None, 271, 299, 357]),
    'Koterov': ({71056}, [57, 71, 75, 79, 91, 98, 158, 308, None, 445, 493, 519]),
    'Lobzy': ({490300}, [27, 35, 57, 128, 186, 261, 594, 691, None, 930, 955, 960]),
    'Skvrňany': ({406376}, [89, 122, 149, 214, 257, 296, 529, 598, 526, 688, 708, 682]),
    'Doubravka': ({122670}, [57, 75, 90, 164, 226, 427, 804, 930, 1157, 1069, 1106, 1167]),
    'Újezd': ({406422}, [43, 51, 62, 69, 91, 99, 187, 319, 375, 427, 467, 578]),
    'Radčice': ({137413}, [41, 49, 50, 56, 62, 73, 107, 214, 249, 248, 280, 280]),
    'Valcha': ({122505}, [None, None, None, None, None, None, None, None, 160, 119, 126, 129]),
}
PART_GROUP = {code: g for g, (codes, _) in CENSUS.items() for code in codes}

EVENTS = [  # captions of the video; sources in docs/research/plzen-growth-model.md §1 and the guide page
    (1295, 'Založení Nové Plzně (Václav II.), pravidelná osnova s náměstím', 'Founding of New Plzeň (Wenceslas II), regular plan with the square'),
    (1320, 'Stavba hradeb a kostela sv. Bartoloměje (1. pol. 14. st.)', 'Town wall and St Bartholomew church built (early 14th c.)'),
    (1420, 'Parkán (vnější hradba) a příkop', 'Zwinger (outer wall) and moat'),
    (1433, 'Husitské obléhání 1433–34 (Prokop Holý): město nedobyto, předměstí zničena', 'Hussite siege 1433–34 (Prokop Holý): the town holds, suburbs destroyed'),
    (1532, 'Vodárenská věž', 'Water tower'),
    (1618, 'Mansfeldovo obléhání 19. 9. – 21. 11. 1618: město dobyto útokem, předměstí vypálena', 'Mansfeld\'s siege 19 Sep – 21 Nov 1618: the town taken by storm, suburbs burned'),
    (1619, 'Mansfeldova posádka staví zemní bastiony kolem města (1618–1620)', 'Mansfeld\'s garrison builds earthwork bastions around the town (1618–1620)'),
    (1621, 'Mansfeldova posádka vydává město císařským (březen 1621)', 'Mansfeld\'s garrison hands the town over to the Imperial army (March 1621)'),
    (1634, 'Valdštejn v Plzni, plzeňské reversy (leden 1634)', 'Wallenstein in Plzeň, the Plzeň reverses (January 1634)'),
    (1639, 'Další etapa opevňování (1639–1649)', 'Next stage of fortification (1639–1649)'),
    (1645, 'La Corona: bastiony a raveliny, nová Říšská brána; 1647 vyklizeno předpolí', 'La Corona: bastions and ravelins, the new Imperial gate; glacis cleared 1647'),
    (1658, 'Vnější šance 1658–59 podle plánu z 23. 2. 1658 (díla a–h), Turecká šance', 'Outer works 1658–59 after the plan of 23 Feb 1658 (works a–h), the Turkish redoubt'),
    (1703, 'Zizner opravuje opevnění (březen–prosinec 1703); nová díla na jihu, rozsah nejistý', 'Zizner repairs the fortification (March–December 1703); new works in the south, extent uncertain'),
    (1760, 'Opevnění chátrá (plán 1781: „eingegangene Vestungswerker“)', 'The fortification decays (1781 plan: "eingegangene Vestungswerker")'),
    (1784, 'Krajský úřad povoluje zbourání opevnění', 'The district office permits demolition of the fortification'),
    (1795, 'Začíná bourání hradeb a zasypávání příkopů (1795–1822)', 'Demolition of the walls and filling of the moats begins (1795–1822)'),
    (1804, 'Zbořena Litická brána', 'Litice gate demolished'),
    (1822, 'Turecká šance srovnána, zbořena Pražská brána', 'Turkish redoubt levelled, Prague gate demolished'),
    (1823, 'Kasárna 35. pěšího pluku na místě Turecké šance (rozhodnuto 1820)', 'Barracks of the 35th Infantry Regiment on the site of the Turkish redoubt (decided 1820)'),
    (1828, 'Západní hradby → okružní sady', 'Western walls → ring park'),
    (1833, 'Zbořena Říšská brána', 'Imperial gate demolished'),
    (1842, 'Měšťanský pivovar', 'Burghers\' brewery'),
    (1849, 'Zbořena Saská brána, poslední brána', 'Saxon gate demolished, the last gate'),
    (1859, 'Valdštejnova strojírna, od 1869 Škodovy závody', 'Waldstein engineering works, the Škoda works from 1869'),
    (1862, 'Železnice Praha – Plzeň – Furth (1861–62), první nádraží', 'Railway Prague – Plzeň – Furth (1861–62), the first station'),
    (1893, 'Poslední úsek hradeb ustupuje muzeu (1893–99)', 'The last wall section gives way to the museum (1893–99)'),
    (1899, 'Elektrická tramvaj', 'Electric tram'),
    (1907, 'Nová budova hlavního nádraží (R. Štech, otevřena 17. 7. 1907)', 'New main station building (R. Štech, opened 17 July 1907)'),
    (1924, 'Velká Plzeň: připojeny Doubravka, Doudlevce, Lobzy, Skvrňany', 'Greater Plzeň: Doubravka, Doudlevce, Lobzy and Skvrňany join'),
    (1942, 'Nálety na Škodovy závody a nádraží (1942–45)', 'Air raids on the Škoda works and the station (1942–45)'),
    (1945, 'Osvobození americkou armádou 6. 5. 1945', 'Liberation by the US Army, 6 May 1945'),
    (1954, 'Sídliště Slovany (1954–63)', 'Slovany housing estate (1954–63)'),
    (1960, 'Sídliště Doubravka (1960–67)', 'Doubravka housing estate (1960–67)'),
    (1965, 'Sídliště Bory (1965–72)', 'Bory housing estate (1965–72)'),
    (1968, 'Sídliště Skvrňany (1968–76)', 'Skvrňany housing estate (1968–76)'),
    (1969, 'Kasárna 35. pluku odstřelena (24. 1. 1969) kvůli průtahu na Roudnou a Lochotín', 'Barracks of the 35th Regiment blown up (24 Jan 1969) for the through-road to Roudná and Lochotín'),
    (1975, 'Sídliště Lochotín (1975–80)', 'Lochotín housing estate (1975–80)'),
    (1978, 'Sídliště Bolevec (1978–81)', 'Bolevec housing estate (1978–81)'),
    (1983, 'Sídliště Košutka a Vinice (dokončena do 1992)', 'Košutka and Vinice housing estates (completed by 1992)'),
]


def dyear(ms):
    """RÚIAN completion → ('exact', y, y) or ('class', lo, hi) age-class interval, or None."""
    if ms is None: return None
    d = (datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=ms + 7200000)).date()
    if d.month == 12 and d.day == 31 and d.year in CLASS_END: return ('class', CLASS_END[d.year], d.year)
    return ('exact', d.year, d.year)


def poly_px(ring):
    return np.array([[(x - BBOX[0]) / RES, (BBOX[3] - y) / RES] for x, y in ring], np.float32)


def footprint(ring, dil=1):
    """pixel mask of a footprint (with dilation) as (slice, mask) or None outside the frame."""
    p = poly_px(ring); x0, y0 = np.floor(p.min(0)).astype(int) - dil - 1; x1, y1 = np.ceil(p.max(0)).astype(int) + dil + 1
    if x0 < 0 or y0 < 0 or x1 >= N or y1 >= N: return None
    m = np.zeros((y1 - y0 + 1, x1 - x0 + 1), np.uint8)
    cv2.fillPoly(m, [np.round(p - [x0, y0]).astype(np.int32)], 1)
    if dil: m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    return (slice(y0, y1 + 1), slice(x0, x1 + 1)), m > 0


def raw_path(name):
    return os.path.join(RAW, next(x for x in os.listdir(RAW) if x.split('.')[0] == name))


# ---------- evidence rasters ----------
# manual corrections of the recognition (workbench.html → manual/map_<id>.json): "removed" rings erase detected
# buildings, "buildings" rings add missing ones; applied to the evidence before anything is dated
MAN = os.path.join(HERE, '..', 'manual')
def manual_map(mid):
    f = os.path.join(MAN, f'map_{mid}.json')
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None
print('loading epochs')
B, C, D = {}, {}, {}
ncorr = 0
for name, year, *_ in EPOCHS:
    im, alpha = imread(raw_path(name))
    b, cov = building_mask(name, im, alpha)
    E_ = manual_map(name)
    if E_:
        for r_ in E_.get('removed', []):
            m_ = np.zeros((N, N), np.uint8); cv2.fillPoly(m_, [np.round(poly_px(r_['ring'])).astype(np.int32)], 1); b[m_ > 0] = False; ncorr += 1
        for r_ in E_.get('buildings', []):
            m_ = np.zeros((N, N), np.uint8); cv2.fillPoly(m_, [np.round(poly_px(r_['ring'])).astype(np.int32)], 1); b[m_ > 0] = True; cov[m_ > 0] = True; ncorr += 1
    B[name], C[name] = b, cov
    area = cv2.blur(b.astype(np.float32), (41, 41)) > 0.08
    D[name] = cv2.distanceTransform((~area).astype(np.uint8), cv2.DIST_L2, 5) * RES  # metres to the built-up area
    print(f'  {name:14s} coverage {cov.sum() * RES * RES / 1e6:5.1f} km²  building pixels {b.sum() * RES * RES / 1e6:5.2f} km²')
print('manual corrections of the recognition rasters:', ncorr)


def states(sl, m):
    out = []
    for name, _, _, _, thr in EPOCHS:
        if C[name][sl][m].mean() < 0.5: out.append(None); continue
        out.append(B[name][sl][m].mean() >= thr)
    return out


def split_built(st):
    """first epoch index k from which the place is built (len = after the last epoch)."""
    best, bk = 1e9, 0
    for k in range(len(EPOCHS) + 1):
        c = sum((wb if i < k else we) for i, (_, _, wb, we, _) in enumerate(EPOCHS)
                if st[i] is not None and ((i < k and st[i]) or (i >= k and not st[i])))
        if c < best - 1e-9: best, bk = c, k
    return bk


def split_gone(st):
    """first epoch index k from which a historic building is gone (2025 counts as gone)."""
    best, bk = 1e9, len(EPOCHS)
    for k in range(1, len(EPOCHS) + 1):
        c = sum((we if i < k else wb) for i, (_, _, wb, we, _) in enumerate(EPOCHS)
                if st[i] is not None and ((i < k and not st[i]) or (i >= k and st[i])))
        if c < best - 1e-9: best, bk = c, k
    return bk


def interval(k):
    lo = YEARS[k - 1] if k > 0 else None
    hi = YEARS[k] if k < len(YEARS) else 2020
    return lo, hi


# ---------- model input ----------
P = json.load(open(os.path.join(ROOT, 'apps', 'historic-mapper', 'projects', 'plzen.json'), encoding='utf-8'))
ENT = {e['id']: e for e in P['entities']}
WALL = Polygon(ENT['g1618-wall']['geom']['coords'])
VILLAGES['Malice (Roudná)'] = (tuple(ENT['g1618-all_saints']['geom']['coords'][0]), 1250)
GATES = [(tuple(ENT[g]['geom']['coords'][0]), ENT[g]['validTo']) for g in ('g1618-gate_prague', 'g1618-gate_reich', 'g1618-gate_litice', 'g1618-gate_north')]
F = json.load(open(os.path.join(ROOT, 'data', 'reference', 'plzen-ruian', 'buildings.geojson'), encoding='utf-8'))['features']
HROWS = json.load(open(os.path.join(ROOT, 'data', 'reference', 'plzen-3d', 'heights.json')))['rows']
H3D = {}
for _, par, hr, he in HROWS:
    if par and hr: H3D[int(par)] = max(H3D.get(int(par), 0), hr)
FORT = json.load(open(os.path.join(HERE, 'fort_1781.json'), encoding='utf-8'))

recs = []  # dicts: ring, from, to, h0, h1, tR, gaps, cls, basis, lo, hi, part, house, id


def height(p, area):
    par = p.get('identifikacniparcela')
    if par and int(par) in H3D and H3D[int(par)] > 1.5: return float(min(H3D[int(par)], 120))
    f, use = p.get('pocetpodlazi'), p.get('zpusobvyuzitikod')
    if f: return max(3.0, 3.1 * f - (3.0 if f >= 4 else 0.0))
    if use == 18: return 2.8                       # garage
    if use in (12, 1, 13): return 7.0 if area > 150 else 4.0  # production / storage / farm
    if use == 6: return 12.0
    if use == 8: return 4.0
    if use == 19: return 3.0 if area < 50 else 5.0
    return 6.5


def zone(x, y):
    pt = Point(x, y)
    if WALL.contains(pt): return 'inner', None
    dw = WALL.exterior.distance(pt)
    vname, vd = None, 1e9
    for k, (xy, _) in VILLAGES.items():
        d = math.hypot(x - xy[0], y - xy[1])
        if d < vd: vname, vd = k, d
    if vd < 550 and math.hypot(x - SQUARE[0], y - SQUARE[1]) > 1000: return 'village', vname
    if dw < 110: return 'glacis', None
    if math.hypot(x - SQUARE[0], y - SQUARE[1]) < 1250: return 'suburb', None
    return 'rural', None


def pre1840(items):
    """date places already built in 1840 (items: dicts with x, y); sets from, gaps, cls."""
    groups = {}
    for it in items:
        z, v = zone(it['x'], it['y']); it['cls'] = z; it['village'] = v
        groups.setdefault((z, v), []).append(it)
    for (z, v), its in groups.items():
        if z == 'inner':
            its.sort(key=lambda it: math.hypot(it['x'] - SQUARE[0], it['y'] - SQUARE[1]))
            for i, it in enumerate(its):
                it['from'] = max(1295.0, 1295 + 40 * i / len(its) + rng.uniform(-3, 3))
        elif z == 'glacis':  # built on the filled moat / glacis after the walls fell
            for it in its: it['from'] = rng.uniform(1796, 1840)
        elif z == 'suburb':
            for it in its: it['dg'] = min(math.hypot(it['x'] - g[0][0], it['y'] - g[0][1]) for g in GATES)
            its.sort(key=lambda it: it['dg'])
            for i, it in enumerate(its):
                r = i / len(its)
                if r < 0.45 and it['dg'] < 500:  # medieval gate suburbs
                    it['from'] = 1330 + 100 * r / 0.45 + rng.uniform(-5, 5)
                    g1 = (1433.6, 1436 + rng.uniform(0, 45))
                    near = WALL.exterior.distance(Point(it['x'], it['y'])) < 260
                    g2 = (1618.75, (1796 + rng.uniform(0, 44)) if near else (1650 + rng.uniform(0, 120)))
                    it['gaps'] = [g1, g2] if it['from'] < g1[0] else [g2]
                else:
                    it['from'] = 1650 + 190 * (r - 0.45) / 0.55 + rng.uniform(-8, 8)
        elif z == 'village':
            m = VILLAGES[v][1]; xy = VILLAGES[v][0]
            its.sort(key=lambda it: math.hypot(it['x'] - xy[0], it['y'] - xy[1]))
            for i, it in enumerate(its):
                r = i / len(its)
                it['from'] = m + rng.uniform(0, 10) if r < 0.4 else m + (1840 - m) * ((r - 0.4) / 0.6) ** 1.5 + rng.uniform(-5, 5)
        else:
            for it in its: it['from'] = rng.uniform(1650, 1838)
        for it in its:
            it['from'] = min(it['from'], it.get('hi', 1840) - 0.5, 1839.5)


def front_rank(items, epoch_lo):
    """order items inside one interval by distance to the built-up area of the previous epoch."""
    if not items: return
    if epoch_lo is None:
        for it in items: it['rank'] = rng.random()
        return
    name = next(e[0] for e in EPOCHS if e[1] == epoch_lo)
    for it in items:
        c, r = to_px(it['x'], it['y'])
        it['d'] = float(D[name][min(max(r, 0), N - 1), min(max(c, 0), N - 1)]) + rng.uniform(0, 25)
    items.sort(key=lambda it: it['d'])
    for i, it in enumerate(items): it['rank'] = (i + 0.5) / len(items)


# ---------- present buildings ----------
print('dating', len(F), 'RÚIAN buildings')
ruian_mask = np.zeros((N, N), np.uint8)
pending, pre = [], []
LANDMARK_PTS = {k: Point(*ENT[k]['geom']['coords'][0]) for k in ('g1618-bartholomew', 'g1618-franciscan', 'g1618-water_tower', 'g1618-st_nicholas', 'g1618-all_saints')}
LANDMARK_KOD = {24142204: 1300.0,   # Franciscan monastery with the Gothic cloister (čp. 121; RÚIAN date 2010 = reconstruction)
                24144177: 1897.0, 24143821: 1897.5,   # museum complex on Kopeckého sady (Západočeské muzeum, 1896–98)
                }
# significant buildings dated by history (Czech Wikipedia, scripts/notable_buildings.json): the RÚIAN building at the
# article coordinates (containing it, or the nearest within 15 m) stands from its completion year; a 'complex' (the
# star-shaped Bory prison, 1874–78) takes all buildings joined to it, finished at once
NOTABLE_KOD = {}
try:
    from pyproj import Transformer as _Tr
    from shapely.strtree import STRtree
    _tr = _Tr.from_crs('EPSG:4326', 'EPSG:5514', always_xy=True)
    _NB = json.load(open(os.path.join(HERE, 'notable_buildings.json'), encoding='utf-8'))['buildings']
    _polys = []
    for f in F:
        if len(f['geometry']['coordinates'][0]) < 4: continue
        pg_ = Polygon(f['geometry']['coordinates'][0]); _polys.append((pg_ if pg_.is_valid else pg_.buffer(0), f['properties']['kod']))
    _ntree = STRtree([q for q, _ in _polys])
    for b in _NB:
        x_, y_ = _tr.transform(b['lon'], b['lat']); pt_ = Point(x_, y_)
        hit = [i for i in _ntree.query(pt_, predicate='intersects')]
        if not hit: hit = list(_ntree.query_nearest(pt_, max_distance=40.0 if b.get('complex') else 15.0))
        if not hit: print('  notable building not found:', b['name']); continue
        seed = min(hit, key=lambda i: _polys[i][0].distance(pt_))
        group = {seed}
        if b.get('complex'):   # flood over buildings that touch (≤ 1.5 m) within 250 m of the seed
            todo = [seed]
            while todo:
                i = todo.pop()
                for j in _ntree.query(_polys[i][0].buffer(1.5)):
                    if j not in group and _polys[j][0].distance(pt_) < 250 and _polys[j][0].distance(_polys[i][0]) <= 1.5:
                        group.add(j); todo.append(j)
        for i in group: NOTABLE_KOD.setdefault(_polys[i][1], (float(b['done']) + 0.3, b['name']))
    print('notable buildings (Wikipedia):', len(_NB), 'entries →', len(NOTABLE_KOD), 'RÚIAN buildings dated')
except Exception as e:
    print('notable buildings skipped:', e)
LANDMARK_FROM = {'g1618-bartholomew': (1320, 30), 'g1618-franciscan': (1300, 20), 'g1618-water_tower': (1532, 30), 'g1618-st_nicholas': (1400, 18), 'g1618-all_saints': (1250, 14)}
for f in F:
    ring = f['geometry']['coordinates'][0]
    if len(ring) < 4: continue
    fp = footprint(ring)
    if fp is None: continue
    sl, m = fp
    ruian_mask[sl][m] = 1
    poly = Polygon(ring)
    if not poly.is_valid: poly = poly.buffer(0)
    c = poly.representative_point()
    p = f['properties']; area = p.get('zastavenaplocha') or poly.area
    it = {'ring': ring, 'x': c.x, 'y': c.y, 'h1': height(p, area), 'ruian': dyear(p.get('dokonceni')), 'area': area, 'gaps': [],
          'part': p.get('castobce'), 'house': p.get('typstavebnihoobjektukod') in (1, 2), 'id': f'ruian:{p["kod"]}'}
    lm = next((k for k, q in LANDMARK_PTS.items() if poly.buffer(2).contains(q)), None)
    if p['kod'] in LANDMARK_KOD:   # buildings dated by history, not by the maps
        it['from'], it['cls'], it['basis'] = LANDMARK_KOD[p['kod']], 'landmark', 'history'; it['h0'] = it['h1']; it['lo'] = it['hi'] = it['from']
        it['id'] = f'ruian:{p["kod"]}'; recs.append(it); continue
    if p['kod'] in NOTABLE_KOD and not lm:
        it['from'] = NOTABLE_KOD[p['kod']][0]; it['cls'] = 'town'; it['basis'] = 'history'; it['h0'] = it['h1']; it['lo'] = it['hi'] = it['from']
        it['notable'] = NOTABLE_KOD[p['kod']][1]; recs.append(it); continue
    if lm:
        it['from'], h = LANDMARK_FROM[lm]; it['h1'] = max(it['h1'], h) if lm != 'g1618-bartholomew' else it['h1']
        it['h0'] = it['h1']; it['cls'] = 'landmark'; it['basis'] = 'history'; it['lo'] = it['hi'] = it['from']; it['id'] = lm
        recs.append(it); continue
    st = states(sl, m)
    it['k'] = split_built(st)
    pending.append(it)

# housing estates of the Northern Suburb (Lochotín, Košutka, Vinice) were completed in the early 1990s
# (Vinice 1992): tall residential blocks there get 1992 as the latest year
ESTATES = [((-822744.8, -1067175.9), 700), ((-823269.7, -1066797.6), 600), ((-824099.5, -1067847.8), 600)]
ESTATE_DONE = 1992.5


def in_estate(it):
    return it['h1'] >= 12 and any(math.hypot(it['x'] - c[0], it['y'] - c[1]) < r for c, r in ESTATES)


groups = {}
for it in pending:
    k, rd = it['k'], it['ruian']
    mlo, mhi = interval(k)
    if in_estate(it) and not (rd and rd[0] == 'exact'):
        if rd and rd[0] == 'class' and rd[2] > ESTATE_DONE: rd = it['ruian'] = ('class', rd[1], ESTATE_DONE)
        mhi = min(mhi, ESTATE_DONE) if mhi > (mlo or 0) + 1 else mhi
    built40 = k <= K40
    if rd and rd[0] == 'exact':
        ye = rd[1]
        if built40 and ye > 1860: it['tR'] = ye + 0.5; it['basis'] = 'map 1840 + rebuilt (RÚIAN date)'; it['hi'] = mhi; pre.append(it)
        elif not built40 and mhi < ye - 10: it['tR'] = ye + 0.5; it['basis'] = 'map + rebuilt (RÚIAN date)'; it['lo'], it['hi'] = mlo, mhi; groups.setdefault((mlo, mhi), []).append(it)
        elif built40: it['from'] = float(min(ye, 1839)); it['basis'] = 'RÚIAN date'; it['cls'] = zone(it['x'], it['y'])[0]; it['lo'] = it['hi'] = it['from']
        else: it['from'] = ye + rng.random() * 0.9; it['basis'] = 'RÚIAN date'; it['lo'] = it['hi'] = it['from']
        continue
    if rd and rd[0] == 'class':
        clo, chi = rd[1], rd[2]
        lo = max(clo if clo is not None else -1e9, mlo if mlo is not None else -1e9); hi = min(chi, mhi)
        if built40 and clo is None:  # built in 1840 and old class: pre-1840 place, 19th-c. rebuild possible
            it['basis'] = 'map 1840 + RÚIAN class'; it['hi'] = mhi; pre.append(it); continue
        if built40: it['tR'] = rng.uniform(clo, chi) + 0.5; it['basis'] = 'map 1840 + rebuilt (RÚIAN class)'; it['hi'] = mhi; pre.append(it); continue
        if lo < hi:
            it['basis'] = 'map + RÚIAN class'; it['lo'], it['hi'] = (None if lo < -1e8 else lo), hi
            groups.setdefault((it['lo'], hi), []).append(it); continue
        if mhi <= (clo or -1e9):
            it['tR'] = rng.uniform(clo, chi) + 0.5; it['basis'] = 'map + rebuilt (RÚIAN class)'; it['lo'], it['hi'] = mlo, mhi
            groups.setdefault((mlo, mhi), []).append(it); continue
        it['basis'] = 'RÚIAN class (map later)'; it['lo'], it['hi'] = clo, chi; groups.setdefault((clo, chi), []).append(it); continue
    if built40: it['basis'] = 'map 1840'; it['hi'] = mhi; pre.append(it); continue
    it['basis'] = 'map'; it['lo'], it['hi'] = mlo, mhi; groups.setdefault((mlo, mhi), []).append(it)

for (lo, hi), its in groups.items():
    front_rank(its, lo if lo in YEARS else None)
    lo2 = lo if lo is not None else 1840
    for it in its: it['from'] = lo2 + (hi - lo2) * (0.05 + 0.9 * it['rank'])

# ---------- historic-only buildings of the stable cadastre ----------
print('historic-only footprints from the stable cadastre')
b40 = B['1840_cadastre'].astype(np.uint8) & (cv2.dilate(ruian_mask, np.ones((3, 3), np.uint8)) == 0).astype(np.uint8)
b40 = cv2.morphologyEx(b40, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
n, lab, stt, cen = cv2.connectedComponentsWithStats(b40, 8)
hist = []
wall_line = WALL.exterior
for i in range(1, n):
    a = stt[i, cv2.CC_STAT_AREA] * RES * RES
    if a < 15: continue
    x0, y0, w, h = stt[i, :4]
    sub = (lab[y0:y0 + h, x0:x0 + w] == i).astype(np.uint8)
    cs, _ = cv2.findContours(sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cs, key=cv2.contourArea)
    ap = cv2.approxPolyDP(cnt, 0.8, True).reshape(-1, 2)
    if len(ap) < 3: continue
    ring = [to_map(x0 + px, y0 + py) for px, py in ap]
    ring.append(ring[0])
    X, Y = to_map(*cen[i][:2].tolist())
    if wall_line.distance(Point(X, Y)) < 9: continue  # the town wall itself is drawn in carmine
    fp = footprint(ring)
    if fp is None: continue
    st = states(*fp)
    kg = max(split_gone(st), K40 + 1)
    lo, hi = interval(kg)
    it = {'ring': ring, 'x': X, 'y': Y, 'h1': 9.0 if WALL.contains(Point(X, Y)) else 5.5, 'gaps': [], 'basis': 'map 1840, demolished (maps)',
          'to': (lo or 1840) + ((hi - (lo or 1840)) * rng.uniform(0.15, 0.85)), 'hi': 1840, 'house': a >= 60, 'id': f'h1840:{len(hist)}'}
    hist.append(it)
# ---------- demolitions 1942-2008 in the centre (HAM Plzeň map 65, ham_demolitions.py) ----------
HAM = os.path.join(ROOT, 'data', 'historic', 'growth', 'ham65_demolitions.json')
bombs = []
if os.path.exists(HAM):
    hf = json.load(open(HAM, encoding='utf-8'))['features']
    bombs = [(f['geometry']['coordinates'], f['properties']['radius_m']) for f in hf if f['geometry']['type'] == 'Point']
    nh = 0
    for f in hf:
        if f['geometry']['type'] != 'Polygon': continue
        ring = f['geometry']['coordinates'][0]
        fp = footprint(ring, dil=0)
        if fp is None: continue
        sl, m = fp
        if ruian_mask[sl][m].mean() > 0.3: continue  # replaced on the same footprint: the RÚIAN building carries it
        poly = Polygon(ring); c = poly.representative_point()
        st = states(*footprint(ring))
        k = split_built(st)
        bombed = any(math.hypot(c.x - b[0][0], c.y - b[0][1]) < b[1] + 15 for b in bombs)
        # demolition year: last map showing the place built (1947, 1953, 2001), within 1945-2008
        kg = split_gone(st); glo, ghi = interval(kg)
        lo_d, hi_d = max(1945.5, glo or 1945.5), min(2008.0, ghi if ghi > (glo or 0) else 2008.0)
        to = 1945.3 if bombed else (rng.uniform(lo_d, hi_d) if hi_d > lo_d else rng.uniform(1950, 1990))
        it = {'ring': ring, 'x': c.x, 'y': c.y, 'h1': 10.0, 'gaps': [], 'to': to, 'house': poly.area >= 40, 'id': f'ham65:{nh}',
              'basis': 'HAM map 65 demolition' + (' (air raid 1945)' if bombed else '')}
        if k <= K40: it['hi'] = interval(k)[1]; hist.append(it)
        else:
            lo, hi = interval(k); hi = min(hi, to - 1)
            it['from'] = rng.uniform(lo or 1840, max((lo or 1840) + 0.5, hi)); it['lo'], it['hi'] = lo, hi; it['h0'] = it['h1']; recs.append(it)
        nh += 1
    print('HAM map 65:', nh, 'demolished buildings added,', len(bombs), 'air-raid sites')
pre1840(pre + hist)
for it in pre + hist:
    if 'h0' not in it:
        it['h0'] = min(it['h1'], 9.0 if it['cls'] == 'inner' else 6.0)
        if it['h1'] > it['h0'] + 1 and 'tR' not in it: it['tR'] = rng.uniform(1850, 1919)
recs += pending + hist

for it in recs:  # present buildings inside an air-raid circle of map 65: damaged 1945, rebuilt 1946-50
    if it.get('id', '').startswith('ruian:') and it['from'] < 1945 and any(math.hypot(it['x'] - bb[0][0], it['y'] - bb[0][1]) < bb[1] for bb in bombs):
        it['tR'] = min(it.get('tR', 9999), rng.uniform(1946, 1950)); it.setdefault('h0', it['h1'])
# ---------- parts of the town for buildings without a house number (nearest numbered building) ----------
G = 50.0
grid = {}
for it in recs:
    if it.get('part'): grid.setdefault((int(it['x'] // G), int(it['y'] // G)), []).append(it)
for it in recs:
    if it.get('part'): continue
    gx, gy = int(it['x'] // G), int(it['y'] // G); best = None
    for rad in range(0, 8):
        cand = [q for dx in range(-rad, rad + 1) for dy in range(-rad, rad + 1) if max(abs(dx), abs(dy)) == rad for q in grid.get((gx + dx, gy + dy), [])]
        if cand: best = min(cand, key=lambda q: (q['x'] - it['x']) ** 2 + (q['y'] - it['y']) ** 2); break
    it['part'] = best['part'] if best else None


# ---------- calibration to the census house counts ----------
def visible(it, y):
    if it['from'] > y or it.get('to', 9999) <= y: return False
    return not any(s <= y < e for s, e in it.get('gaps', []))


def counts(hs, years):
    return [sum(1 for it in hs if visible(it, y)) for y in years]


calib = {}
for gname, (codes, series) in CENSUS.items():
    hs = [it for it in recs if it.get('house') and it.get('part') in codes and it.get('cls') not in ('landmark', 'fort')]
    yrs = [y for y, v in zip(CENSUS_YEARS, series) if v is not None]
    tv = [v for v in series if v is not None]
    if not hs or not tv: continue
    before = counts(hs, yrs)
    r = before[-1] / tv[-1] if tv[-1] else 1.0           # in-frame share and house-definition ratio, from 2001
    target = [v * r for v in tv]
    dem = [sum(1 for it in hs if it.get('to', 9999) <= y) for y in yrs]
    cum = list(np.maximum.accumulate([t + d for t, d in zip(target, dem)]))
    hs.sort(key=lambda it: it['from'])
    n0 = sum(1 for it in hs if it['from'] < yrs[0] - 0.01)   # already standing at the first census

    def inv(k):  # year at which the k-th house appears according to the census curve
        if k < cum[0]: return None
        for j in range(1, len(yrs)):
            if k < cum[j]: return yrs[j - 1] + (yrs[j] - yrs[j - 1]) * (k - cum[j - 1]) / max(cum[j] - cum[j - 1], 1e-9)
        return None
    moved = 0
    for k, it in enumerate(hs):
        lo, hi = it.get('lo'), it.get('hi')
        if lo is not None and hi is not None and hi - lo < 0.95: continue  # exact date
        y = inv(k)
        if y is None:
            if k < cum[0] and it['from'] >= yrs[0]: y = rng.uniform(max(lo or 1841, 1841), yrs[0])  # needed before the first census
            else: continue
        y += rng.uniform(-0.5, 0.5)
        if lo is not None: y = max(y, lo + 0.05)
        if hi is not None: y = min(y, hi - 0.05)
        if it['from'] < 1840 and y >= 1840 and (hi or 1840) <= 1840: continue  # pre-1840 places stay
        if abs(y - it['from']) > 0.5: moved += 1
        if it.get('tR', 9999) < 9999 and it['tR'] <= y: it['tR'] = min(9999, y + 1)
        it['from'] = y
    after = counts(hs, yrs)
    calib[gname] = {'years': yrs, 'census': tv, 'ratio_2001': round(r, 3), 'before': before, 'after': after, 'target': [round(t) for t in target], 'moved': moved, 'houses': len(hs)}
    print(f'  calib {gname:10s} r={r:4.2f} moved {moved:5d}/{len(hs):5d} ' + ' '.join(f'{y}:{round(t)}/{b}->{a}' for y, t, b, a in zip(yrs, target, before, after)))


# ---------- fortification and landmarks without a present footprint ----------
def box(xy, w, d, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(xy[0] + ca * u - sa * v, xy[1] + sa * u + ca * v) for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]
    return pts + [pts[0]]  # closed ring like the other footprints


MUSEUM = (-822180.0, -1069800.0)  # east / south-east of the old town (Kopeckého sady)


def wall_demolition(mid):
    g = min(GATES, key=lambda g: math.hypot(mid[0] - g[0][0], mid[1] - g[0][1]))
    dem = g[1]
    if mid[0] < SQUARE[0] - 90: dem = 1828  # western walls → ring park
    if math.hypot(mid[0] - MUSEUM[0], mid[1] - MUSEUM[1]) < 45: dem = 1896
    return dem


def line_pieces(coords, step=30.0):
    for i in range(len(coords) - 1):
        a, b = coords[i], coords[i + 1]; L = math.hypot(b[0] - a[0], b[1] - a[1]); nseg = max(1, int(L // step))
        for j in range(nseg):
            p0 = (a[0] + (b[0] - a[0]) * j / nseg, a[1] + (b[1] - a[1]) * j / nseg)
            p1 = (a[0] + (b[0] - a[0]) * (j + 1) / nseg, a[1] + (b[1] - a[1]) * (j + 1) / nseg)
            yield p0, p1, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)


pieces = []
for p0, p1, mid in line_pieces(list(WALL.exterior.coords)):
    dem = wall_demolition(mid)
    poly = LineString([p0, p1]).buffer(1.4, cap_style=2)
    recs.append({'ring': list(poly.exterior.coords), 'x': mid[0], 'y': mid[1], 'from': 1320 + rng.uniform(-10, 10), 'to': dem + rng.uniform(-3, 0),
                 'h0': 8.0, 'h1': 8.0, 'gaps': [], 'cls': 'fort', 'basis': 'model 1618 + dated demolitions', 'id': 'g1618-wall'})
    pieces.append((mid, dem))
for ln in FORT['lines']:  # Zwinger and outer walls (1781 plan)
    for p0, p1, mid in line_pieces(ln['line']):
        dem = ln['to'] or wall_demolition(mid)
        poly = LineString([p0, p1]).buffer(1.1, cap_style=2)
        recs.append({'ring': list(poly.exterior.coords), 'x': mid[0], 'y': mid[1], 'from': ln['from'] + rng.uniform(-8, 8), 'to': dem + rng.uniform(-3, 0),
                     'h0': ln['h'], 'h1': ln['h'], 'gaps': [], 'cls': 'fort', 'basis': 'plan 1781 + dated demolitions', 'id': 'fort:' + ln['id']})
import shapely
import shapely.ops
from shapely.ops import unary_union
from shapely.strtree import STRtree
import fabric
DECAY = 1760  # the 1781 legend calls the works "eingegangene Vestungswerker" (defunct): lowered from about 1760
FPLANS = json.load(open(os.path.join(HERE, 'fort_plans_map.json'), encoding='utf-8'))
H57 = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'ham57_map.json'), encoding='utf-8'))
W1703 = {w['id']: Polygon(w['poly']).buffer(0) for w in FPLANS['plans']['1703']['works']}
# Baroque star after the plans of 1658 (HAM map 5, phases: cores existing in 1658 → 1645–49, proposals →
# 1658–59) and 1703 (HAM map 6, geometry of all works; Vogt 1712 is a simplified copy). Bastions are joined
# to a continuous main rampart around the Zwinger (Mansfeld 1618–20); one ditch follows the whole outline;
# ravelins and lunettes stand detached in front with their own ditch. Removal years from the 1821 / 1840 plans.
WORKS = [  # id, attached, (from lo, hi), to, height
    ('z1703_sw_bastion', True, (1645, 1649), 1805, 7.0), ('z1703_s_bastion', True, (1645, 1649), 1800, 7.0),
    ('z1703_s_bastion2', True, (1645, 1649), 1833, 7.0), ('z1703_ne_work', True, (1645, 1649), 9999, 7.0),
    ('z1703_w_redoubt', True, (1658, 1659.9), 1822.3, 7.5), ('z1703_nw_bastion', True, (1658, 1659.9), 1810, 7.0),
    ('z1703_s_redan', False, (1703.2, 1703.9), 1775, 5.0), ('z1703_sw_lunette', False, (1703.2, 1703.9), 1772, 5.0),
    ('z1703_w_block', False, (1703.2, 1703.9), 1772, 5.0)]
ZW = WALL.buffer(13, join_style=2)
RING_OUT = WALL.buffer(36, join_style=2)
ATT = {wid: fabric.connect(W1703[wid], RING_OUT).difference(ZW) for wid, att, *_ in WORKS if att}
NSEC = 28
TC = (WALL.centroid.x, WALL.centroid.y)


def sector_of(x, y):
    return int(((math.atan2(y - TC[1], x - TC[0]) + math.pi) / (2 * math.pi)) * NSEC) % NSEC


def split_mesh(m):
    """triangles of a mesh grouped by angular sector around the town (shared vertices → no seams)."""
    out = {}
    for t in m['t']:
        cx = sum(m['v'][i][0] for i in t) / 3; cy = sum(m['v'][i][1] for i in t) / 3
        out.setdefault(sector_of(cx, cy), []).append(t)
    res = []
    for k, ts in out.items():
        used = sorted({i for t in ts for i in t}); remap = {o: n for n, o in enumerate(used)}
        res.append((k, {'v': [m['v'][i] for i in used], 't': [[remap[i] for i in t] for t in ts]}))
    return res


def mesh_ring(m):
    pts = [(v[0], v[1]) for v in m['v']]
    hull = Polygon(pts).convex_hull if len(pts) > 2 else Point(pts[0]).buffer(1)
    return list(hull.exterior.coords)


def sector_demolition(k):
    ang = (k + 0.5) / NSEC * 2 * math.pi - math.pi
    pt = WALL.exterior.interpolate(WALL.exterior.project(Point(TC[0] + 400 * math.cos(ang), TC[1] + 400 * math.sin(ang))))
    return min(max(wall_demolition((pt.x, pt.y)), 1796), 1830)


def add_split(m, base, label):
    for k, sub in split_mesh(m):
        r = mesh_ring(sub); c = Polygon(r).centroid
        recs.append(base | {'ring': r, 'x': c.x, 'y': c.y, 'id': label, 'imesh': sub,
                            'to': base['to'] if base['to'] != 'sector' else sector_demolition(k) + rng.uniform(-2, 2)})


EARTH = lambda h: [(0, 0.0), (1.8, h * 0.86), (3.8, h), (7.0, h * 0.82)]
# main rampart (Mansfeld 1618–20), split by sector: removed with the nearest walls
ring_body = RING_OUT.difference(ZW)
add_split(fabric.band_mesh(ring_body, EARTH(6.0), mode_all=1),
          {'from': rng.uniform(1619.0, 1620.0), 'to': 'sector', 'h0': 6.0, 'h1': 3.6, 'tR': DECAY + rng.uniform(-8, 8), 'gaps': [], 'cls': 'fort',
           'basis': 'plans 1658 / 1703 (star), dated demolitions'}, 'fort:rampart')
for wid, att, (lo, hi), to, h in WORKS:
    body = ATT[wid] if att else W1703[wid]
    body = max(fabric._parts(body), key=lambda g: g.area)
    c = body.centroid
    recs.append({'ring': list(body.exterior.coords), 'x': c.x, 'y': c.y, 'from': rng.uniform(lo, hi), 'to': float(to) + (rng.uniform(-2, 2) if to < 9999 else 0),
                 'h0': h, 'h1': h * 0.6, 'tR': (DECAY if att else rng.uniform(1725, 1745)) + rng.uniform(-8, 8), 'gaps': [], 'cls': 'fort',
                 'basis': 'plan 1703 (Zizner), phase 1658' if att else 'plan 1703 (Zizner), realisation uncertain', 'id': 'fort:' + wid,
                 'imesh': fabric.band_mesh(body, EARTH(h), mode_all=1)})
# ditches: one per phase, following the outline of the star at that time; the medieval moat (map 57) before
E1 = RING_OUT
E2 = unary_union([RING_OUT] + [ATT[w] for w, att, (lo, _), *_ in WORKS if att and lo < 1650])
E3 = unary_union([E2] + [ATT[w] for w, att, (lo, _), *_ in WORKS if att and lo >= 1650])
DW = 15.0
ditch = lambda E: E.buffer(DW, join_style=2).difference(E).difference(ZW)
outw = unary_union([W1703[w].buffer(10, join_style=2).difference(W1703[w]) for w, att, *_ in WORKS if not att]).difference(E3)
FILL = 1810.0
DITCHES = [(ditch(E1), 1619.6, 1647.0), (ditch(E2), 1647.0, 1659.9), (ditch(E3), 1659.9, 1703.6),
           (unary_union([ditch(E3), outw]), 1703.6, 1772.0), (ditch(E3), 1772.0, FILL)]
med = [Polygon(f['poly']).buffer(0) for f in H57['features'] if f['kind'] == 'moat']
MED = unary_union([g for g in med if WALL.exterior.distance(g) < 60]).difference(ZW.buffer(-2))
CUTS = []   # (geometry, from, to): terrain cut out while the ditch exists (bit i of cuts.png)
for gi, (g, f0, t0) in enumerate([(MED, 1420.0, 1619.6)] + DITCHES):
    if g.is_empty: continue
    for part in fabric._parts(g):
        if part.area < 50: continue
        base = {'from': f0, 'to': t0, 'h0': 4.5, 'h1': 4.5, 'gaps': [], 'basis': 'plans 1658 / 1703 (star)' if gi else 'map 57 (moat c. 1410)'}
        add_split(fabric.trough(part, 4.5), base | {'cls': 'ditch'}, 'fort:ditch')
        add_split(fabric.trough(part, 4.5, water=-3.3), base | {'cls': 'moat'}, 'fort:ditch:water')
    CUTS.append((g, f0, t0))
# suburb walls of c. 1410 (map 57): low masonry, until the 1618 siege
for f in H57['features']:
    if f['kind'] != 'suburb_wall': continue
    for p0, p1, mid in line_pieces(f['line'], 30.0):
        poly = LineString([p0, p1]).buffer(0.9, cap_style=2)
        recs.append({'ring': list(poly.exterior.coords), 'x': mid[0], 'y': mid[1], 'from': rng.uniform(1395, 1415), 'to': 1618.85, 'h0': 4.5, 'h1': 4.5,
                     'gaps': [(1433.6, rng.uniform(1436, 1450))], 'cls': 'fort', 'basis': 'map 57 (suburb walls c. 1410)', 'id': 'fort:suburb_wall'})
for k, e in ENT.items():
    if e['type'] not in ('gate', 'tower') or not e.get('geom') or e['geom']['type'] != 'Point': continue
    xy = tuple(e['geom']['coords'][0])
    if k == 'g1618-barth_tower': recs.append({'ring': box(xy, 11, 11), 'x': xy[0], 'y': xy[1], 'from': 1320, 'h0': 102.3, 'h1': 102.3, 'gaps': [], 'cls': 'landmark', 'basis': 'history', 'id': k}); continue
    if k == 'g1618-water_tower': continue
    dem = e.get('validTo') or 1849
    if k.startswith('g1618-te_tower'): dem = min(pieces, key=lambda p: math.hypot(p[0][0] - xy[0], p[0][1] - xy[1]))[1]
    w = 10 if e['type'] == 'gate' else 7
    recs.append({'ring': box(xy, w, w), 'x': xy[0], 'y': xy[1], 'from': 1325 + rng.uniform(-5, 5), 'to': float(dem), 'h0': e.get('height', 15), 'h1': e.get('height', 15),
                 'gaps': [], 'cls': 'fort', 'basis': 'model 1618 + dated demolitions', 'id': k})
VH = os.path.join(HERE, 'veduta_heights.json')
if os.path.exists(VH):   # heights of towers and gates from the fitted vedute (veduta_fit.py)
    VHH = json.load(open(VH, encoding='utf-8'))['heights']
    for it in recs:
        if it.get('id') in VHH and it.get('cls') == 'fort': it['h0'] = it['h1'] = VHH[it['id']]
CUT = os.path.join(ROOT, 'data', 'historic', 'cutouts', 'ottheinrich-1536')
if os.path.isdir(CUT):   # wall towers and gates shaped after the cut-outs of the 1536 veduta (corner tower, gate)
    PROF = {k: fabric.silhouette_profile(os.path.join(CUT, f'{k}.png')) for k in ('corner-tower', 'gate-left', 'tall-tower', 'church-facade-left')}
    for it in recs:
        iid = str(it.get('id', ''))
        if it.get('cls') != 'fort' or not (iid.startswith('g1618-gate_') or iid.startswith('g1618-te_tower')): continue
        pt = Point(it['x'], it['y']); s_ = WALL.exterior.project(pt)
        q1, q2 = WALL.exterior.interpolate(s_ - 3), WALL.exterior.interpolate(s_ + 3)
        ang = math.atan2(q2.y - q1.y, q2.x - q1.x)
        gate = iid.startswith('g1618-gate_')
        it['imesh'] = fabric.loft(PROF['gate-left' if gate else 'corner-tower'], (it['x'], it['y']), ang, 10.0 if gate else 7.0, it['h1'])
        it['basis'] = 'model 1618, shape after the 1536 veduta'

# ---------- dated single buildings ----------
TURK = W1703['z1703_w_redoubt'].buffer(30).union(Polygon(next(w for w in FORT['works'] if w['id'] == 'bastion_w')['poly']).buffer(45))
nk = 0
for it in recs:
    if str(it.get('id', '')).startswith('h1840:') and TURK.contains(Point(it['x'], it['y'])) and it.get('to', 9999) > 1900:
        it['from'] = 1823.0 + rng.uniform(0, 1.5); it['lo'] = it['hi'] = it['from']; it['to'] = 1969.07; it['basis'] = 'history'; nk += 1
        pg = Polygon(it['ring']).buffer(0)
        it['imesh'] = fabric.courtyard_block(pg, 14.0); it['h0'] = it['h1'] = 14.0; it['cls'] = 'town'; it.pop('tR', None); it['gaps'] = []
print('barracks of the 35th regiment (1823–1969):', nk, 'footprints')

# ---------- generated historic fabric (inner town before 1750, suburbs and villages before the 1840 houses) ----------
# Inside the walls: narrow gabled burgher houses around the blocks of map 57 (gable to the street, rear
# courtyard); the square is complete from the founding. Present buildings replace them only after
# 1750–1800 (per block), or later if their own date (RÚIAN / rebuild) is later: the epoch evidence wins.
# Outside the walls: small houses grow organically in the medieval suburbs of map 57 (from the gates,
# burned 1433 and 1618, glacis cleared 1647); the houses of the historic database (1840 cadastre, present
# buildings dated before 1840) appear only when the baroque walls fall (by sector, 1796–1835), villages
# about 1825–1845; before that, small generated houses stand at their places.
GEN = []
gid = [0]


def gen(q, eave, roof, cls, basis, ridge_depth=True, **kw):
    gid[0] += 1
    pg = Polygon(q); c = pg.centroid
    r = {'ring': list(q) + [q[0]], 'x': c.x, 'y': c.y, 'h0': eave + roof, 'h1': eave + roof, 'gaps': [], 'cls': cls, 'basis': basis,
         'id': f'gen:{gid[0]}', 'imesh': fabric.gable_house(q, eave, roof, ridge_depth)}
    r.update(kw); GEN.append(r); return r


# Dominican monastery (Black monastery, founded c. 1300; abolished 1785, military hospital from 1786 – HAM map 8;
# replaced c. 1800): church outline of map 57 next to point B of the Theatrum Europaeum plate (1618)
TE_B = Point(-822422.5, -1069465.0)
dch = [Polygon(f['poly']).buffer(0) for f in H57['features'] if f['kind'] == 'church']
DOM_CHURCH = min(dch, key=lambda g: g.distance(TE_B))
_mrr = list(DOM_CHURCH.minimum_rotated_rectangle.exterior.coords)[:4]
_e = sorted([(math.dist(_mrr[i], _mrr[(i + 1) % 4]), i) for i in range(4)])
DOM_LEN = _e[-1][0]; _i = _e[-1][1]
DOM_ANG = math.atan2(_mrr[(_i + 1) % 4][1] - _mrr[_i][1], _mrr[(_i + 1) % 4][0] - _mrr[_i][0])
_blk = min((Polygon(f['poly']).buffer(0) for f in H57['features'] if f['kind'] == 'inner_block'), key=lambda g: g.distance(DOM_CHURCH.centroid))
_n = (-math.sin(DOM_ANG), math.cos(DOM_ANG)); _c = DOM_CHURCH.centroid
if (_blk.centroid.x - _c.x) * _n[0] + (_blk.centroid.y - _c.y) * _n[1] < 0: _n = (-_n[0], -_n[1])
CLOISTER_C = (_c.x + _n[0] * 27, _c.y + _n[1] * 27)
CLOISTER = Polygon(fabric.rect((CLOISTER_C[0] - _n[0] * 20, CLOISTER_C[1] - _n[1] * 20), (math.cos(DOM_ANG), math.sin(DOM_ANG)), 40, 40))
DOM_AREA = unary_union([DOM_CHURCH.buffer(3), CLOISTER.buffer(2)])
DOM_TO = 1802.0
uq = (math.cos(DOM_ANG), math.sin(DOM_ANG))
for k in range(4):  # cloister wings
    ang = DOM_ANG + k * math.pi / 2; u = (math.cos(ang), math.sin(ang)); nn = (-u[1], u[0])
    fc = (CLOISTER_C[0] - nn[0] * 20, CLOISTER_C[1] - nn[1] * 20)
    gen(fabric.rect(fc, u, 40, 10), 9.0, 5.0, 'landmark', 'history', ridge_depth=False, **{'from': 1300 + rng.uniform(0, 20), 'to': DOM_TO})

LMK = unary_union([Polygon(it['ring']).buffer(2) for it in recs if it.get('cls') == 'landmark'] + [DOM_AREA])
blocks = [Polygon(f['poly']).buffer(0).intersection(WALL.buffer(-1)) for f in H57['features'] if f['kind'] == 'inner_block']
blocks = [max(fabric._parts(bk), key=lambda g: g.area) for bk in blocks if not bk.is_empty and bk.area > 300]
inner_gen = []
BLOCK_T = []
for bk in blocks:
    T = rng.uniform(1750, 1800); BLOCK_T.append((bk, T))
    for q, c, nrm in fabric.perimeter_houses(bk, rng, depth=13.5, width=(8.5, 12.5), skip=LMK):
        d = math.hypot(c[0] - SQUARE[0], c[1] - SQUARE[1])
        sq = d < 130 and ((SQUARE[0] - c[0]) * nrm[0] + (SQUARE[1] - c[1]) * nrm[1]) / max(d, 1) > 0.5
        r = gen(q, rng.uniform(6.5, 8.5) if sq else rng.uniform(5.0, 7.0), rng.uniform(4.0, 5.2), 'inner', 'generated: blocks of map 57', ridge_depth=True,
                **{'to': T + rng.uniform(-3, 3), 'sq': sq, 'd': d, 'blk': bk})
        inner_gen.append(r)
for r in inner_gen:   # houses on the square: three to four storeys
    if r['sq']:
        q = [tuple(v[:2]) for v in r['imesh']['v'][:4]]; ev, rf = rng.uniform(8.5, 11.0), rng.uniform(5.0, 6.2)
        r['imesh'] = fabric.gable_house(q, ev, rf, True); r['h0'] = r['h1'] = ev + rf
for r in inner_gen: r['from'] = 1295.0 + rng.uniform(0, 4.0)   # the whole plan at the founding (heights grow later, see below)


def block_T(x, y):
    p = Point(x, y)
    return min(BLOCK_T, key=lambda bt: bt[0].distance(p))[1]


REAL = lambda it: str(it.get('id', '')).split(':')[0] in ('ruian', 'h1840', 'ham65', 'hmap') and it.get('cls') != 'landmark'
# the square: open area around the church between the blocks; its frontage is Renaissance (town hall 1554–59),
# so the present models of the houses on the square (and the town hall) stand from then on
_sq = Point(*SQUARE).buffer(170).difference(unary_union(blocks).buffer(1.0))
SQ = min(fabric._parts(_sq), key=lambda g: g.distance(Point(*SQUARE)))
SQ = max(fabric._parts(SQ.buffer(-14, join_style=2).buffer(14, join_style=2)), key=lambda g: g.area)   # without the streets
TOWNHALL = {f['properties']['kod'] for f in F if str(f['properties'].get('cisladomovni')) == '1' and f['properties'].get('castobce') == 406392}
inside = []
for it in recs:
    if not REAL(it) or not WALL.contains(Point(it['x'], it['y'])): continue
    t_new = max(block_T(it['x'], it['y']) + rng.uniform(0, 4), it['from'])
    if it.get('tR', 9999) < 9999: t_new = max(t_new, it['tR']); it.pop('tR', None); it['h0'] = it['h1']   # epoch evidence: the old house stays until the rebuild
    if str(it.get('id', '')).startswith('ruian:') and Polygon(it['ring']).buffer(0).intersects(SQ.buffer(3)):
        t_new = 1558.0 if int(it['id'].split(':')[1]) in TOWNHALL else rng.uniform(1555, 1575); it.pop('tR', None); it['h0'] = it['h1']; it['basis'] = 'history'
    if DOM_AREA.intersects(Polygon(it['ring']).buffer(0)): t_new = max(t_new, DOM_TO + rng.uniform(0, 3))
    if t_new < it.get('to', 9999):
        it['from'] = t_new; it['gaps'] = []; inside.append(it)
# generated houses stay until the present building on their plot appears
if inside:
    tr_in = STRtree([Polygon(it['ring']).buffer(0) for it in inside])
    for r in inner_gen:
        pg = Polygon(r['ring'])
        hits = [inside[i] for i in tr_in.query(pg) if Polygon(inside[i]['ring']).buffer(0).intersection(pg).area > 0.2 * pg.area]
        if hits: r['to'] = max(h['from'] for h in hits) + rng.uniform(-0.5, 0.5)   # until the present building on the plot appears
# growth in height on the same plots, after the isometric views of 1618 / 1650: low timber houses 1295–1390 →
# taller Gothic stone houses with rear tracts → Renaissance (1530–1620, on most plots and all of the square): taller,
# double roofs on wide plots, wings and back houses glued together; the present model replaces the last stage
staged = []
for r in inner_gen:
    q = [tuple(v[:2]) for v in r['imesh']['v'][:4]]
    sq = r['sq']; end = r['to']; bk = r.get('blk')
    t2 = rng.uniform(1375, 1405)
    t3 = rng.uniform(1530, 1620) if (sq or rng.random() < 0.75) else 9999
    stages = [(r['from'], t2, 1, rng.uniform(3.0, 4.0), rng.uniform(3.2, 3.8)),
              (t2, t3, 2, rng.uniform(8.0, 9.5) if sq else rng.uniform(6.0, 7.5), rng.uniform(5.0, 6.0)),
              (t3, 9999, 3, rng.uniform(9.5, 11.0) if sq else rng.uniform(7.5, 9.0), rng.uniform(5.5, 6.5))]
    first = True
    for f0, t0, st, ev, rf in stages:
        if f0 >= end: break
        mesh = fabric.burgher_complex(q, ev, rf, st, rng, bk)
        if first:
            r['imesh'] = mesh; r['h0'] = r['h1'] = ev + rf; r['to'] = min(t0, end); first = False
        else:
            g2 = gen(q, ev, rf, 'inner', 'generated: blocks of map 57, ' + ('Gothic' if st == 2 else 'Renaissance'), ridge_depth=True,
                     **{'from': f0, 'to': min(t0, end), 'sq': sq, 'd': r['d']})
            g2['imesh'] = mesh; staged.append(g2)
inner_gen += staged

# medieval suburbs of map 57: small houses from the gates outwards
GATE_PTS = [g[0] for g in GATES]
sub_gen = []
for f in H57['features']:
    if f['kind'] != 'suburb_block': continue
    area = Polygon(f['poly']).buffer(0)
    if area.distance(Point(*SQUARE)) > 1600: continue
    # frontage along the roads that bound the block (with gaps), then the inside of the block
    plots = [(q, c, True) for q, c, n in fabric.perimeter_houses(area, rng, depth=9.0, width=(8.0, 12.0)) if rng.random() < 0.8]
    inner_area = area.buffer(-11)
    plots += [(q, xy, False) for q, xy, de in fabric.scatter_houses(inner_area, rng, spacing=20.0, size=((6, 8), (7.5, 10)))] if not inner_area.is_empty else []
    for q, (x, y), front in plots:
        dg = min(math.hypot(x - g[0], y - g[1]) for g in GATE_PTS)
        r = gen(q, rng.uniform(3.3, 4.5), rng.uniform(2.8, 3.6), 'suburb', 'generated: suburbs of map 57', ridge_depth=not front,
                **{'dg': dg + (0 if front else 180) + rng.uniform(0, 70), 'dw': WALL.exterior.distance(Point(x, y))})
        sub_gen.append(r)
sub_gen.sort(key=lambda r: r['dg'])   # from the gates along the roads first, the insides of the blocks later
for i, r in enumerate(sub_gen):
    r['from'] = 1330 + 95 * i / max(len(sub_gen), 1) + rng.uniform(-4, 4)
    if r['from'] < 1433.6: r['gaps'] = [(1433.6, rng.uniform(1436, 1480))]
    if rng.random() < 0.55:          # rebuilt after the siege of 1618, cleared for the glacis in 1647 or replaced later
        r['gaps'].append((1618.85, rng.uniform(1622, 1640)))
        r['to'] = 1647.3 if r['dw'] < 260 else rng.uniform(1650, 1665)
    else:
        r['to'] = 1618.85

# historic database outside the walls only after the baroque walls fall; small houses before
nph = 0
for it in recs:
    if not REAL(it) or WALL.contains(Point(it['x'], it['y'])): continue
    z = it.get('cls')
    dw = WALL.exterior.distance(Point(it['x'], it['y']))
    if z in ('suburb', 'glacis') or dw < 1200:
        pt = WALL.exterior.interpolate(WALL.exterior.project(Point(it['x'], it['y'])))
        T = min(max(wall_demolition((pt.x, pt.y)), 1796), 1835) + rng.uniform(-3, 6)
        ph0 = None if dw < 260 else max(it['from'], 1650.0)
    elif z in ('village', 'rural'):
        T = rng.uniform(1825, 1845); ph0 = it['from']
    else:
        T = None; ph0 = None
    t_old = it['from']
    t_new = it['from']
    if T is not None and t_old < T: t_new = T
    if it.get('tR', 9999) < 9999 and it['tR'] > t_new + 5:   # epoch evidence: older house on the plot until the rebuild
        t_new = it['tR']; ph0 = t_old if ph0 is None and dw >= 260 else ph0
    it.pop('tR', None); it['h0'] = it['h1']
    if t_new <= t_old + 0.01 or t_new >= it.get('to', 9999): continue
    it['from'] = t_new; it['gaps'] = []
    if ph0 is not None and ph0 < t_new - 2:
        pg = Polygon(it['ring']).buffer(0)
        mrr = list(pg.minimum_rotated_rectangle.exterior.coords)[:4]
        e = sorted([(math.dist(mrr[i], mrr[(i + 1) % 4]), i) for i in range(4)]); L, i0 = e[-1]
        u = ((mrr[(i0 + 1) % 4][0] - mrr[i0][0]) / L, (mrr[(i0 + 1) % 4][1] - mrr[i0][1]) / L)
        w, d = min(L, rng.uniform(9, 13)), min(e[0][0], rng.uniform(6.5, 9))
        c = pg.centroid; nn = (-u[1], u[0])
        q = fabric.rect((c.x - nn[0] * d / 2, c.y - nn[1] * d / 2), u, w, d)
        village = z in ('village', 'rural')
        gen(q, rng.uniform(3.2, 4.2), rng.uniform(3.5, 4.5) if village else rng.uniform(2.8, 3.6), 'village' if village else 'suburb',
            'generated: before the historic database', ridge_depth=False, **{'from': ph0, 'to': t_new + rng.uniform(-1, 0.5)})
        nph += 1
for r in GEN:
    for k in ('sq', 'd', 'dg', 'dw', 'blk'): r.pop(k, None)
    r.setdefault('from', 1300.0); r.setdefault('to', 9999.0)
    r['to'] = max(r['to'], r['from'] + 1)
recs += GEN
print('generated fabric:', len(inner_gen), 'inner houses,', len(sub_gen), 'medieval suburb houses,', nph, 'houses before the historic database')

# ---------- city 3D models: the real shape of present buildings, held back in time ----------
# GIS_Budovy_Plzen_2024 multipatches (scripts/city3d_mesh.py) replace the extruded footprint of the RÚIAN
# building that contains them. The shape is kept for the whole life of the building in the model (no
# lower pre-rebuild height), so e.g. St Bartholomew has its present form from 1320 on: schematic, not historic.
MESH_NPZ = os.path.join(ROOT, 'data', 'reference', 'plzen-3d', 'mesh.npz')
if os.path.exists(MESH_NPZ):
    from shapely.strtree import STRtree
    MZ = np.load(MESH_NPZ)
    m_vs, m_ts, m_V, m_T, m_O = MZ['vstart'], MZ['tstart'], MZ['verts'], MZ['tris'], MZ['origin']
    cand = [it for it in recs if 'ruian' in it]
    cpoly = []
    for it in cand:
        pg = Polygon(it['ring'])
        cpoly.append(pg if pg.is_valid else pg.buffer(0))
    tree = STRtree(cpoly)
    hits = {}
    for j in range(len(m_vs) - 1):
        xy = m_V[m_vs[j]:m_vs[j + 1], :2]
        c = Point(float(xy[:, 0].min() + xy[:, 0].max()) / 2 + m_O[0], float(xy[:, 1].min() + xy[:, 1].max()) / 2 + m_O[1])
        # the footprint that holds most of the object's vertices (not just its bbox centre: the museum next to the
        # Franciscan monastery has its centre inside the monastery outline and stood there from 1300 otherwise)
        q = tree.query(shapely.box(float(xy[:, 0].min()) + m_O[0], float(xy[:, 1].min()) + m_O[1], float(xy[:, 0].max()) + m_O[0], float(xy[:, 1].max()) + m_O[1]))
        if not len(q):
            q = tree.query_nearest(c, max_distance=2.0)
        if not len(q): continue
        vx, vy = xy[:, 0] + m_O[0], xy[:, 1] + m_O[1]
        share = {i: float(shapely.contains_xy(cpoly[i].buffer(1.0), vx, vy).mean()) for i in q}
        k = max(q, key=lambda i: (share[i], -cpoly[i].area))
        if share[k] < 0.5 and not cpoly[k].buffer(2.0).contains(c): continue
        hits.setdefault(k, []).append(j)
    nm = 0
    for k, objs in hits.items():
        it = cand[k]
        z0 = min(float(m_V[m_vs[j]:m_vs[j + 1], 2].min()) for j in objs)
        z1 = max(float(m_V[m_vs[j]:m_vs[j + 1], 2].max()) for j in objs)
        if z1 - z0 < 1.0: continue
        it['mesh'] = objs; it['mesh_z0'] = z0
        it['h0'] = it['h1'] = round(z1 - z0, 1); it.pop('tR', None); nm += 1
    if any(it.get('id') == 'g1618-bartholomew' and 'mesh' in it for it in recs):
        recs = [it for it in recs if it.get('id') != 'g1618-barth_tower']  # the tower is part of the church model
    print('city 3D models:', len(m_vs) - 1, 'objects,', sum(len(v) for v in hits.values()), 'matched to', nm, 'model buildings')
    # Dominican church (nave, choir, tower) shaped after the 1536 veduta: the steep gable of the church facades as the
    # cross-section of nave and choir, the slender tower with its spire; plan after the church outline of map 57
    # (next to point B of the 1618 plate)
    if os.path.isdir(CUT):
        from PIL import Image as _Im
        _m = list(DOM_CHURCH.minimum_rotated_rectangle.exterior.coords)[:4]
        _e = sorted([(math.dist(_m[i], _m[(i + 1) % 4]), i) for i in range(4)])
        DW_ = min(_e[0][0], 16.0); c0 = DOM_CHURCH.centroid
        ax = (math.cos(DOM_ANG), math.sin(DOM_ANG))
        if ax[0] < 0: ax = (-ax[0], -ax[1])                                   # towards the east (choir)
        w_end = (c0.x - ax[0] * DOM_LEN / 2, c0.y - ax[1] * DOM_LEN / 2); e_end = (c0.x + ax[0] * DOM_LEN / 2, c0.y + ax[1] * DOM_LEN / 2)
        split = (w_end[0] + ax[0] * DOM_LEN * 0.62, w_end[1] + ax[1] * DOM_LEN * 0.62)
        fa = _Im.open(os.path.join(CUT, 'church-facade-left.png')); fa_ratio = fa.size[1] / max(fa.size[0], 1)
        nave_h = min(max(DW_ * fa_ratio * 0.9, 18.0), 32.0)
        ta = np.array(_Im.open(os.path.join(CUT, 'tall-tower.png')).convert('RGBA'))[..., 3] > 128
        rows = np.where(ta.any(1))[0]; cols = np.where(ta.any(0))[0]
        tw_ = 7.5; tower_h = min(max(tw_ * (rows.max() - rows.min()) / max(np.median([np.ptp(np.where(ta[r])[0]) for r in rows[len(rows) // 3: 2 * len(rows) // 3] if ta[r].any()]), 1), 34.0), 45.0)
        tower_c = (w_end[0] + ax[0] * tw_ / 2, w_end[1] + ax[1] * tw_ / 2)
        mm = fabric.merge([fabric.extrude_profile(PROF['church-facade-left'], w_end, split, DW_, nave_h),
                           fabric.extrude_profile(PROF['church-facade-left'], split, e_end, DW_ * 0.8, nave_h * 0.88),
                           fabric.loft(PROF['tall-tower'], tower_c, DOM_ANG, tw_, tower_h)])
        recs.append({'ring': list(DOM_CHURCH.exterior.coords), 'x': c0.x, 'y': c0.y, 'from': 1300.0, 'to': DOM_TO, 'h0': tower_h, 'h1': tower_h, 'gaps': [],
                     'cls': 'landmark', 'basis': 'history', 'id': 'g1618-dominican', 'imesh': mm})
        print(f'Dominican church after the 1536 veduta: nave {nave_h:.0f} m, tower {tower_h:.0f} m')

# permanence helper: the present (RÚIAN) building on the same place (overlap > 50 % of the smaller footprint)
_PERM = [it for it in recs if str(it.get('id', '')).startswith('ruian:') and it.get('cls') != 'landmark' and it.get('basis') != 'history']
_PERM_PG = [Polygon(it['ring']).buffer(0) for it in _PERM]
_PERM_TREE = STRtree(_PERM_PG)
def permanent_match(pg):
    best = None
    for k in _PERM_TREE.query(pg):
        a_ = _PERM_PG[k].intersection(pg).area
        if a_ > 0.5 * min(_PERM_PG[k].area, pg.area) and (best is None or a_ > best[0]): best = (a_, _PERM[k])
    return best[1] if best else None


# ---------- buildings of the town plans 1891–1912 at 0.5 m (scripts/map_buildings.py → hi_buildings.json) ----------
# a footprint of a plan that no model building covers at the plan's year (< 30 %) is missing; detections of the five
# plans that overlap are chained into one building: from between the last plan without it and the first with it,
# until between the last plan with it and the next without it (after 1912: the epoch maps 1926–1953 decide)
HIJ = os.path.join(ROOT, 'data', 'historic', 'growth', 'hi_buildings.json')
if os.path.exists(HIJ):
    HB = json.load(open(HIJ))
    HYS = sorted(int(y) for y in HB['plans'])
    hx0, hy0, hx1, hy1 = HB['area']; hres = 1.0; hw = int((hx1 - hx0) / hres); hh_ = int((hy1 - hy0) / hres)
    def hpx(ring): return np.array([[(x - hx0) / hres, (hy1 - y) / hres] for x, y in ring], np.int32)
    det = []   # (year, polygon, covered share)
    for Y in HYS:
        cv_ = np.zeros((hh_, hw), np.uint8)
        for it in recs:
            if it.get('cls') in ('ditch', 'moat') or not visible(it, Y + 0.01): continue
            cv2.fillPoly(cv_, [hpx(it['ring'])], 1)
        cv_ = cv2.dilate(cv_, np.ones((3, 3), np.uint8))
        E_ = manual_map(f'{Y}_hi') or {}
        rem_ = [Polygon(r_['ring']).buffer(0) for r_ in E_.get('removed', [])]
        rings_ = [r_ for r_ in HB['plans'][str(Y)] if not any(q_.intersection(Polygon(r_).buffer(0)).area > 0.5 * max(Polygon(r_).buffer(0).area, 1e-6) for q_ in rem_)]
        rings_ += [r_['ring'] for r_ in E_.get('buildings', [])]
        for ring in rings_:
            pg = Polygon(ring).buffer(0)
            if pg.is_empty or pg.area < 40: continue
            if pg.geom_type != 'Polygon': pg = max(pg.geoms, key=lambda g: g.area)
            _mr = list(pg.minimum_rotated_rectangle.exterior.coords); _L = max(math.dist(_mr[0], _mr[1]), math.dist(_mr[1], _mr[2]))
            if pg.area / max(_L, 1e-6) < 4.5: continue   # mean width: plot boundaries, hatching along streets
            m_ = np.zeros((hh_, hw), np.uint8); pts = hpx(pg.exterior.coords); cv2.fillPoly(m_, [pts], 1)
            x0_, y0_ = max(pts[:, 0].min(), 0), max(pts[:, 1].min(), 0); x1_, y1_ = pts[:, 0].max() + 1, pts[:, 1].max() + 1
            mm_ = m_[y0_:y1_, x0_:x1_] > 0
            share = float(cv_[y0_:y1_, x0_:x1_][mm_].mean()) if mm_.any() else 1.0
            det.append((Y, pg, share))
    dtree = STRtree([d[1] for d in det])
    def ovl(p_, q_):   # tolerant: the plans are locally misaligned by up to ~20 m even after registration
        a_ = p_.buffer(6).intersection(q_).area
        return a_ / max(min(p_.area, q_.area), 1e-6)
    def onmap(Y, pg):
        nm = str(Y); c_, r_ = to_px(pg.centroid.x, pg.centroid.y)
        return 0 <= r_ < N and 0 <= c_ < N and C[nm][r_, c_]
    used = set(); nhi = 0; nskip = 0; nperm = 0
    order = sorted(range(len(det)), key=lambda i: (det[i][2], -det[i][1].area))
    for i in order:
        Y, pg, share = det[i]
        if i in used or share >= 0.3: continue
        chain = {Y: pg}; used.add(i)
        for j in dtree.query(pg):            # the same building on the other plans
            Yj, pj, sj = det[j]
            if Yj == Y or ovl(pg, pj) < 0.5 or not (0.33 < pj.area / pg.area < 3.0): continue
            if Yj not in chain or ovl(pg, pj) > ovl(pg, chain[Yj]): chain[Yj] = pj
            if sj < 0.3: used.add(j)
        pres = sorted(chain)
        # permanence of objects: a plan counts as "the building is gone" only where it covers the place and shows
        # (almost) no building there (< 10 % of the footprint under any detection of that plan); otherwise it stands
        absent = [y_ for y_ in HYS if y_ not in chain and onmap(y_, pg) and
                  sum(det[k][1].intersection(pg).area for k in dtree.query(pg) if det[k][0] == y_) < 0.1 * pg.area]
        if len(pres) < 2 and pg.area < 150: nskip += 1; continue    # one plan only and small: lettering, symbols
        Yf, Yl = pres[0], pres[-1]
        before = [y_ for y_ in absent if y_ < Yf]; after = [y_ for y_ in absent if y_ > Yl]
        ring = list(chain[min(pres, key=lambda y_: [1912, 1908, 1891, 1895, 1902].index(y_))].exterior.coords)   # footprint of the best registered plan
        fp = footprint(ring)
        if fp is None: continue
        st_ = states(*fp)
        if before: fr = rng.uniform(before[-1] + 0.3, Yf - 0.2)
        else:
            kb = split_built(st_); lo_, hi_ = interval(kb)
            fr = Yf - rng.uniform(1, 6) if (hi_ is None or hi_ >= Yf or lo_ is None) else rng.uniform(max(lo_, 1840.5), min(hi_, Yf - 0.5))
        if after: to = rng.uniform(Yl + 0.3, after[0] - 0.2)
        else:
            kg = max(split_gone(st_), YEARS.index(Yl) + 1); lo_, hi_ = interval(kg)
            to = lo_ + (hi_ - lo_) * rng.uniform(0.2, 0.8) if hi_ > lo_ else hi_
        pgc = Polygon(ring).buffer(0)
        if TURK.buffer(120).intersects(pgc) and not after: to = max(to, 1969.07) if to < 1969.07 else to
        if to <= fr + 1: continue
        # the same place as a present building (and no evidence of a demolition after the last plan): one building
        # through time – the present building (with its 3D model from the city catalogue) stands from the plan dating on
        pm = None if after else permanent_match(pgc)
        if pm is not None:
            if fr < pm['from']: pm['from'] = fr; pm['gaps'] = []; pm.pop('tR', None); pm['basis'] = 'map + plans (permanence)'; nperm += 1
            continue
        A_ = pgc.area; hgt = 6.0 if A_ < 100 else 9.0 if A_ > 1500 else rng.uniform(11.0, 14.0)
        c = pgc.representative_point()
        recs.append({'ring': ring, 'x': c.x, 'y': c.y, 'from': fr, 'to': to, 'h0': hgt, 'h1': hgt, 'gaps': [], 'cls': 'town',
                     'basis': 'plans ' + ', '.join(str(y_) for y_ in pres), 'id': f'hmap:{nhi}', 'house': False})
        nhi += 1
    print(f'town plans 1891–1912: {len(det)} footprints, {nhi} missing buildings added, {nperm} present buildings dated earlier (permanence), {nskip} single small detections skipped')

# ---------- manual edits (editor/index.html → apps/historic-mapper/manual/) ----------
# footprints added on a map exist in the map's year: from / to as entered, else from the epoch maps around it
# (as the town-plan buildings above); buildings reconstructed from the vedute (veduta_recon.py) are gable houses
MIDX = json.load(open(os.path.join(MAN, 'maps.json'), encoding='utf-8')) if os.path.exists(os.path.join(MAN, 'maps.json')) else {'maps': []}
MYEAR = {m['id']: m['year'] for m in MIDX['maps']}
nman = 0
for f in sorted(os.listdir(MAN)) if os.path.isdir(MAN) else []:
    if not (f.startswith('map_') and f.endswith('.json')): continue
    E = json.load(open(os.path.join(MAN, f), encoding='utf-8')); Y = MYEAR.get(E['map'], E.get('year', 1900))
    if str(E['map']).endswith('_hi'): continue   # footprints of the 0.5 m plans enter as plan detections (chains above)
    for k, b in enumerate(E.get('buildings', [])):
        ring = [tuple(p) for p in b['ring']]; pg = Polygon(ring).buffer(0)
        if pg.is_empty or pg.area < 4: continue
        fp = footprint(ring + [ring[0]])
        fr, to = b.get('from'), b.get('to')
        if fp is not None and Y >= 1821:
            st_ = states(*fp)
            if fr is None:
                kb = split_built(st_); lo_, hi_ = interval(kb)
                fr = Y - rng.uniform(1, 8) if (hi_ is None or hi_ >= Y or lo_ is None) else rng.uniform(lo_, min(hi_, Y - 0.5))
            if to is None:
                ky = next((i for i, yy in enumerate(YEARS) if yy > Y), len(YEARS))
                kg = max(split_gone(st_), ky); lo_, hi_ = interval(kg)
                to = lo_ + (hi_ - lo_) * rng.uniform(0.2, 0.8) if hi_ > lo_ else hi_
        fr = float(fr if fr is not None else Y - 30); to = float(to if to is not None else Y + 30)
        if to <= fr + 0.5: continue
        h = float(b.get('h') or (7.5 if Y < 1850 else 11.0)); c = pg.representative_point()
        q = list(pg.minimum_rotated_rectangle.exterior.coords)[:4]
        it = {'ring': ring + [ring[0]], 'x': c.x, 'y': c.y, 'from': fr, 'to': to, 'h0': h, 'h1': h, 'gaps': [],
              'cls': 'inner' if WALL.contains(c) else 'town', 'basis': f"manual (map {E['map']})", 'id': f"man:{E['map']}:{k}", 'house': False}
        pm = permanent_match(pg) if b.get('to') is None else None
        if pm is not None:   # a present building drawn on an older map: the same building, standing from then on
            if fr < pm['from']: pm['from'] = fr; pm['gaps'] = []; pm.pop('tR', None); pm['basis'] = f"manual (map {E['map']}, permanence)"
            nman += 1; continue
        if Y < 1850 and len(ring) == 4: it['imesh'] = fabric.gable_house(ring, h * 0.6, h * 0.4, True)
        recs.append(it); nman += 1
VB = os.path.join(MAN, 'veduta_buildings.json')
if os.path.exists(VB):
    for k, b in enumerate(json.load(open(VB, encoding='utf-8'))['buildings']):
        q = [tuple(p) for p in b['ring']]; pg = Polygon(q); c = pg.centroid
        recs.append({'ring': q + [q[0]], 'x': c.x, 'y': c.y, 'from': float(b['from']), 'to': float(b['to']), 'h0': b['ridge'], 'h1': b['ridge'], 'gaps': [],
                     'cls': 'inner' if WALL.contains(c) else 'suburb', 'basis': f"manual (veduta {b['source']})", 'id': f"man:ved:{b['source']}:{k}",
                     'imesh': fabric.roof_house(q, b['eave'], b['ridge'] - b['eave'], b.get('roof', 'gable'))})
        nman += 1
print('manual edits:', nman, 'buildings')

# ---------- consistency with the maps and between buildings (check_epochs.py reports the result) ----------
# 1. duplicates: a demolished house from the 1840 cadastre and the same house from map 65 → one record
# 2. reliable maps (building detection with good recall) are binding at their year: a generated house the map does
#    not show ends before it; a real building without an exact date that the map does not show starts after it
# 3. no two buildings on the same place at the same time (> 25 % of the smaller footprint): priority history /
#    landmarks > RÚIAN exact date > other real buildings > generated houses; the lower one gives way
PRI = lambda it: 4 if it.get('cls') == 'landmark' or it.get('basis') == 'history' or str(it.get('basis', '')).startswith('manual') else 3 if it.get('basis') == 'RÚIAN date' else \
    1 if str(it.get('id', '')).startswith('gen:') else 2
SKIPC = {'fort', 'ditch', 'moat'}
cons = [it for it in recs if it.get('cls') not in SKIPC]
for it in cons:
    pg = Polygon(it['ring']); it['_pg'] = pg if pg.is_valid else pg.buffer(0)
tree_c = STRtree([it['_pg'] for it in cons])
drop = set()
nd = 0
for i, it in enumerate(cons):   # 1. duplicates h1840 × ham65
    if not str(it['id']).startswith('ham65:'): continue
    for j in tree_c.query(it['_pg']):
        o = cons[j]
        if not str(o['id']).startswith('h1840:') or id(o) in drop: continue
        a_ = it['_pg'].intersection(o['_pg']).area
        if a_ > 0.25 * min(it['_pg'].area, o['_pg'].area):
            if o.get('basis') == 'history': drop.add(id(it))                    # the barracks stay as modelled
            else: it['from'] = min(it['from'], o['from']); it['gaps'] = []; drop.add(id(o))
            nd += 1
RELIABLE = [('1840_cadastre', 1840), ('1891', 1891), ('1912', 1912), ('1926', 1926), ('1931', 1931), ('1938', 1938)]
NEXT = {y: (RELIABLE[k + 1][1] if k + 1 < len(RELIABLE) else 1953) for k, (_, y) in enumerate(RELIABLE)}
ngen = nreal = 0
for name, Y in RELIABLE:   # 2. binding maps
    Bd = cv2.dilate(B[name].astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    for it in cons:
        if id(it) in drop or it.get('cls') == 'landmark' or it.get('basis') == 'history' or str(it['id']).startswith(('hmap:', 'man:')) or 'permanence' in str(it.get('basis', '')): continue
        if not (it['from'] <= Y + 0.01 < it.get('to', 9999)) or any(a <= Y < b for a, b in it.get('gaps', [])): continue
        fp = footprint(it['ring'], dil=0)
        if fp is None: continue
        sl, m = fp
        if not m.any() or C[name][sl][m].mean() < 0.5: continue
        if Bd[sl][m].mean() >= 0.1: continue
        if str(it['id']).startswith('gen:'):
            it['to'] = min(it.get('to', 9999), Y - rng.uniform(0.3, 3.0)); ngen += 1
            if it['to'] <= it['from'] + 0.5: drop.add(id(it))
        elif it.get('basis') != 'RÚIAN date':
            it['from'] = Y + rng.uniform(0.3, min(10.0, NEXT[Y] - Y - 0.3)); it['gaps'] = []; nreal += 1
            if it.get('to', 9999) <= it['from'] + 0.5: drop.add(id(it))
nov = 0
for i, it in enumerate(cons):   # 3. overlaps in space and time
    if id(it) in drop: continue
    for j in tree_c.query(it['_pg']):
        if j <= i: continue
        o = cons[j]
        if id(o) in drop: continue
        a_ = it['_pg'].intersection(o['_pg']).area
        if a_ <= 0.25 * min(it['_pg'].area, o['_pg'].area) or a_ < 15: continue
        if it['from'] >= o.get('to', 9999) or o['from'] >= it.get('to', 9999): continue
        hi_, lo_ = (it, o) if (PRI(it), -it['from']) >= (PRI(o), -o['from']) else (o, it)
        if PRI(hi_) == PRI(lo_) == 1:
            drop.add(id(min((it, o), key=lambda q: q['_pg'].area))); nov += 1; continue
        if PRI(hi_) == PRI(lo_):   # two real buildings
            hist_ = [q for q in (it, o) if not str(q['id']).startswith('ruian:')]
            pres_ = [q for q in (it, o) if str(q['id']).startswith('ruian:')]
            if len(hist_) != 1: continue   # both present today (data overlap) or both historic: leave
            h_, p_ = hist_[0], pres_[0]
            p_['from'] = max(p_['from'], h_.get('to', 9999)) if h_.get('to', 9999) < 9999 else p_['from']
            if h_.get('to', 9999) >= 9999 or p_['from'] >= p_.get('to', 9999): h_['to'] = min(h_.get('to', 9999), p_['from'])
            if h_.get('to', 9999) <= h_['from'] + 0.5: drop.add(id(h_))
            nov += 1; continue
        if lo_['from'] < hi_['from']: lo_['to'] = min(lo_.get('to', 9999), hi_['from'])
        elif hi_.get('to', 9999) < 9999: lo_['from'] = max(lo_['from'], hi_['to']); lo_['gaps'] = []
        else: drop.add(id(lo_))
        if lo_.get('to', 9999) <= lo_['from'] + 0.5: drop.add(id(lo_))
        nov += 1
for it in cons: it.pop('_pg', None)
recs = [it for it in recs if id(it) not in drop]
print(f'consistency: {nd} duplicates merged, {ngen} generated houses ended before a map, {nreal} buildings moved after a map, {nov} overlaps resolved, {len(drop)} records dropped')

# ---------- building register: stable ids and the manual history of each building ----------
# Present buildings keep their RÚIAN code, landmarks and fortification their names. The other records (1840 cadastre,
# map 65, town plans, generated houses) are numbered by the run, so they get an id from their place instead
# (prefix:dx/dy = centroid in metres from the square, '.2', '.3' … for several records on one place in time order):
# a manual entry then survives a rebuild of the model.
_seen = {}
for it in sorted(recs, key=lambda q: (round(q.get('from', 0), 1), str(q.get('id', '')))):
    pre_, _, suf_ = str(it.get('id', '')).partition(':')
    if pre_ in ('h1840', 'ham65', 'hmap', 'gen') and suf_.isdigit():
        k_ = f"{pre_}:{round(it['x'] - SQUARE[0])}/{round(it['y'] - SQUARE[1])}"
        _seen[k_] = _seen.get(k_, 0) + 1
        it['id'] = k_ if _seen[k_] == 1 else f'{k_}.{_seen[k_]}'
_cnt = {}   # pieces of one work (wall, ditch, rampart split by sector): '#2', '#3' … from west to east
for it in recs: _cnt[str(it.get('id', ''))] = _cnt.get(str(it.get('id', '')), 0) + 1
_seen = {}
for it in sorted(recs, key=lambda q: (round(q['x'], 1), round(q['y'], 1), round(q.get('from', 0), 1))):
    k_ = str(it.get('id', ''))
    if _cnt[k_] > 1:
        _seen[k_] = _seen.get(k_, 0) + 1
        if _seen[k_] > 1: it['id'] = f'{k_}#{_seen[k_]}'
# manual/buildings.json (the register in growth3d.html): per id any of from, to (null = stands), h0 (first height),
# changes [{year, h}] (up to two changes of height), gaps [[from, to]] (up to two periods destroyed / missing),
# name, note, src. Entered values replace the automatic ones and win over every rule above.
REG_F = os.path.join(MAN, 'buildings.json')
OVR = json.load(open(REG_F, encoding='utf-8')).get('buildings', {}) if os.path.exists(REG_F) else {}
_byid = {str(it.get('id', '')): it for it in recs}
orphans, nman = [], 0
for k_, o in OVR.items():
    it = _byid.get(k_)
    if it is None and o.get('xy'):   # a place-based id that moved (footprint edited): same kind of record within 3 m
        pre_ = k_.split(':')[0]; ox_, oy_ = o['xy']
        cand = [q for q in recs if str(q.get('id', '')).split(':')[0] == pre_ and math.hypot(q['x'] - ox_, q['y'] - oy_) < 3]
        it = min(cand, key=lambda q: math.hypot(q['x'] - ox_, q['y'] - oy_)) if cand else None
    if it is None: orphans.append(k_); continue
    it['auto'] = {f: it.get(f) for f in ('from', 'to', 'h0', 'h1', 'tR', 'gaps', 'basis', 'lo', 'hi')}
    dated = False
    if o.get('from') is not None: it['from'] = float(o['from']); it['lo'] = it['hi'] = it['from']; dated = True
    if 'to' in o: it['to'] = 9999 if o['to'] is None else float(o['to']); dated = True
    if o.get('h0') is not None: it['h0'] = float(o['h0']); dated = True
    if 'changes' in o:
        ch = sorted([c for c in o['changes'] if c.get('year') is not None and c.get('h') is not None], key=lambda c: c['year'])[:2]
        it.setdefault('h0', it['h1'])
        it['tR'], it['h1'] = (float(ch[0]['year']), float(ch[0]['h'])) if ch else (9999, it['h0'])
        if len(ch) > 1: it['tR2'], it['h2'] = float(ch[1]['year']), float(ch[1]['h'])
        else: it.pop('tR2', None); it.pop('h2', None)
        dated = True
    if 'gaps' in o: it['gaps'] = [(float(a), float(b)) for a, b in o['gaps']][:2]; dated = True
    if o.get('name'): it['notable'] = o['name']
    if dated: it['basis'] = 'manual (register)'
    it['manual'] = o; nman += 1
print(f'register: {nman} buildings set by hand' + (f', {len(orphans)} entries without a building: {orphans[:8]}' if orphans else ''))

# ---------- checks ----------
cnt = {c: sum(1 for it in recs if it.get('cls') == c and visible(it, 1788)) for c in ('inner', 'suburb', 'glacis')}
print('visible in 1788 (buildings, not houses):', cnt, '| Schaller 1788: 315 houses in town, 142 in suburbs')
for y in (1300, 1400, 1500, 1618, 1700, 1800, 1840, 1880, 1912, 1938, 1953, 1980, 2001, 2020):
    print(f'  {y}: {sum(1 for it in recs if visible(it, y))} buildings')

# consistency with every map epoch at its own year: recall = share of the map's building pixels covered
# by visible model buildings; precision = share of visible model footprint pixels that are built on the map
print('validation against the map epochs')
valid = {}
for name, year, *_ in EPOCHS + [('2025_ruian', 2020, 1, 1, 0)]:
    if name == '2025_ruian': continue
    mm = np.zeros((N, N), np.uint8)
    for it in recs:
        if it.get('cls') == 'moat' or not visible(it, year + 0.01): continue
        p = poly_px(it['ring'])
        cv2.fillPoly(mm, [np.round(p).astype(np.int32)], 1)
    cov = C[name]; mb = B[name]
    mmd = cv2.dilate(mm, np.ones((5, 5), np.uint8)) > 0; mbd = cv2.dilate(mb.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    rec_ = float((mb & cov & mmd).sum() / max((mb & cov).sum(), 1)); prec = float(((mm > 0) & cov & mbd).sum() / max(((mm > 0) & cov).sum(), 1))
    valid[name] = {'year': year, 'recall': round(rec_, 3), 'precision': round(prec, 3)}
    print(f'  {name:14s} {year}  recall {rec_:5.2f}  precision {prec:5.2f}')

# ---------- terrain ----------
dmr = cv2.imdecode(np.fromfile(os.path.join(ROOT, 'data', 'reference', 'dmr5g', 'plzen_5m.tif'), np.uint8), cv2.IMREAD_UNCHANGED).astype(np.float32)
TN = dmr.shape[0]; TRES = (BBOX[2] - BBOX[0]) / TN
ZMIN = float(np.floor(np.nanmin(dmr)))


def z_at(x, y):
    c = min(max((x - BBOX[0]) / TRES - 0.5, 0), TN - 1.001); r = min(max((BBOX[3] - y) / TRES - 0.5, 0), TN - 1.001)
    c0, r0 = int(c), int(r); fc, fr = c - c0, r - r0
    return float(dmr[r0, c0] * (1 - fc) * (1 - fr) + dmr[r0, c0 + 1] * fc * (1 - fr) + dmr[r0 + 1, c0] * (1 - fc) * fr + dmr[r0 + 1, c0 + 1] * fc * fr)


for it in recs:
    it['z'] = min(z_at(x, y) for x, y in it['ring'][:-1]) - ZMIN
TS = 900
tz = cv2.resize(dmr, (TS, TS), interpolation=cv2.INTER_AREA) - ZMIN
v = np.clip(np.round(tz * 10), 0, 65535).astype(np.uint16)
tex = np.zeros((TS, TS, 3), np.uint8); tex[..., 2] = (v >> 8).astype(np.uint8); tex[..., 1] = (v & 255).astype(np.uint8)  # BGR: R = high byte, G = low byte
cv2.imencode('.png', tex)[1].tofile(os.path.join(OUT, 'terrain.png'))

# ---------- write ----------
OX, OY = SQUARE
CLS = ['inner', 'suburb', 'glacis', 'village', 'rural', 'town', 'fort', 'landmark', 'moat', 'ditch']
BASIS = sorted({it['basis'] for it in recs})
out = {'format': 'ca-geo/growth-model', 'crs': 'EPSG:5514', 'origin': [OX, OY], 'frame': BBOX, 'years': [1295, 2020],
       'terrain': {'file': 'terrain.png', 'size': TS, 'zmin': ZMIN, 'scale': 0.1, 'source': 'ČÚZK DMR 5G'},
       'classes': CLS, 'basis': BASIS, 'events': [{'year': y, 'cs': c, 'en': e} for y, c, e in EVENTS],
       'villages': [{'name': k, 'xy': [round(v[0][0] - OX, 1), round(v[0][1] - OY, 1)], 'mention': v[1]} for k, v in VILLAGES.items()],
       'calibration': calib, 'validation': valid, 'grounds': [], 'water': [],
       'n': len(recs), 'rings': [], 'from': [], 'to': [], 'h0': [], 'h1': [], 'tR': [], 'gaps': [], 'cls': [], 'basisIdx': [], 'z': [], 'ids': []}
for it in recs:
    out['rings'].append([v for x, y in it['ring'][:-1] for v in (round((x - OX) * 10), round((y - OY) * 10))])
    out['from'].append(round(it['from'], 1)); out['to'].append(round(it.get('to', 9999), 1))
    out['h0'].append(round(it.get('h0', it['h1']), 1)); out['h1'].append(round(it['h1'], 1)); out['tR'].append(round(it.get('tR', 9999), 1))
    g = it.get('gaps', []) + [(0, 0)] * (2 - len(it.get('gaps', [])))
    out['gaps'].append([round(v, 1) for s, e in g[:2] for v in (s, e)])
    out['cls'].append(CLS.index(it.get('cls', 'town')))
    out['basisIdx'].append(BASIS.index(it['basis']))
    out['z'].append(round(it['z'], 1)); out['ids'].append(it.get('id', ''))
# second change of height (manual register only): index → [year, height]
out['ch2'] = {str(b): [round(it['tR2'], 1), round(it['h2'], 1)] for b, it in enumerate(recs) if 'tR2' in it}
# register.json: the evidence behind every building, aligned with model.json (date ranges, the automatic values of
# buildings set by hand, names, manual entries without a building); register.csv the same as a table
r6 = lambda v: round(v, 1) if isinstance(v, float) else v
reg = {'format': 'ca-geo/growth-register', 'n': len(recs), 'lo': [r6(it.get('lo')) for it in recs], 'hi': [r6(it.get('hi')) for it in recs],
       'names': {str(b): it['notable'] for b, it in enumerate(recs) if it.get('notable')},
       'manual': {str(b): it['manual'] for b, it in enumerate(recs) if 'manual' in it},
       'auto': {str(b): {k: ([[r6(x) for x in g] for g in v] if isinstance(v, list) else r6(v)) for k, v in it['auto'].items()} for b, it in enumerate(recs) if 'auto' in it},
       'orphans': orphans}
json.dump(reg, open(os.path.join(OUT, 'register.json'), 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
import csv
with open(os.path.join(OUT, 'register.csv'), 'w', encoding='utf-8-sig', newline='') as fh:
    w_ = csv.writer(fh, delimiter=';')
    w_.writerow(['id', 'name', 'class', 'from', 'from_lo', 'from_hi', 'to', 'h0', 'change1', 'h1', 'change2', 'h2', 'gap1', 'gap2', 'basis', 'manual', 'x', 'y'])
    for it in recs:
        g = it.get('gaps', []); yr = lambda v: '' if v is None or v >= 9999 else r6(v)
        w_.writerow([it.get('id', ''), it.get('notable', ''), it.get('cls', ''), r6(it['from']), r6(it.get('lo')), r6(it.get('hi')), yr(it.get('to')),
                     r6(it.get('h0', it['h1'])), yr(it.get('tR')), r6(it['h1']), yr(it.get('tR2')), r6(it.get('h2', '')),
                     '–'.join(str(r6(v)) for v in g[0]) if len(g) > 0 else '', '–'.join(str(r6(v)) for v in g[1]) if len(g) > 1 else '',
                     it['basis'], 'yes' if 'manual' in it else '', round(it['x'], 1), round(it['y'], 1)])
# facade textures (facade.html → manual/facades.json, rectified images in data/historic/growth/facades/tex): copied next
# to the model for the viewer, only for buildings that are in the model
import shutil
FAC_F, FAC_TEX = os.path.join(MAN, 'facades.json'), os.path.join(ROOT, 'data', 'historic', 'growth', 'facades', 'tex')
fac_out = os.path.join(OUT, 'facades')
if os.path.isdir(fac_out): shutil.rmtree(fac_out)
if os.path.exists(FAC_F):
    _ff = json.load(open(FAC_F, encoding='utf-8'))
    blocks = dict(_ff.get('blocks', {}))   # per block (members = building ids); first format: per building
    for k, v in _ff.get('buildings', {}).items(): blocks.setdefault(k, {'members': [k], **v})
    blocks = {k: v for k, v in blocks.items() if any(m in _byid for m in v.get('members', [k]))}
    os.makedirs(fac_out, exist_ok=True); nfac = nroof = 0
    for k, v in blocks.items():
        for lay in v.get('layers', []):
            lay['faces'] = [fc for fc in lay.get('faces', []) if fc.get('b', k) in _byid and fc.get('tex')]
            for fc in lay['faces']:
                src_ = os.path.join(FAC_TEX, fc['tex'])
                if os.path.exists(src_): shutil.copy2(src_, os.path.join(fac_out, fc['tex'])); nfac += 1
            if lay.get('roof', {}).get('tex'):
                src_ = os.path.join(FAC_TEX, lay['roof']['tex'])
                if os.path.exists(src_): shutil.copy2(src_, os.path.join(fac_out, lay['roof']['tex'])); nroof += 1
                else: lay.pop('roof')
    json.dump({'format': 2, 'blocks': blocks}, open(os.path.join(fac_out, 'facades.json'), 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
    out['facades'] = 'facades/facades.json'
    print('facades:', len(blocks), 'blocks,', nfac, 'wall textures,', nroof, 'roof textures')

# ---------- water per epoch and ground textures ----------
S = 2048


def clean(mask, mn=150):
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    nw, lw, sw, _ = cv2.connectedComponentsWithStats(mask, 8); keep = np.zeros(nw, bool); keep[1:] = sw[1:, cv2.CC_STAT_AREA] >= mn
    return cv2.morphologyEx(keep[lw].astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)) > 0


ztm, _ = imread(raw_path('2025_ztm'))
H, Sat, V = hsv(ztm)
water_now = clean((H >= 180) & (H < 235) & (Sat > 0.25) & (V > 0.5))
# River courses per epoch. In every map that shows water well, the detected water is taken as it is; the present
# water is accepted only right next to it (so a channel that moved, an old meander or a mill race keep their old
# course); outside the map the previous epoch continues. Before 1840 only the connected river network is kept
# (no Bolevec ponds, no sewage works).
def largest_network(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 1: return m
    return lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))


def nearby(m, px):
    return cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * px + 1, 2 * px + 1))) > 0


def rivers_only(m):
    """river-like water: components bridged over bridges, long and thin (compactness 4πA/P² < 0.12); ponds,
    reservoirs and sewage tanks are compact and drop out"""
    mc = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mc, 8)
    keep = np.zeros(n, bool)
    for i in range(1, n):
        a_ = st[i, cv2.CC_STAT_AREA]
        if a_ < 300: continue
        x, y, w, h = st[i, :4]
        cs, _ = cv2.findContours((lab[y:y + h, x:x + w] == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        per = sum(cv2.arcLength(c, True) for c in cs)
        if 4 * math.pi * a_ / max(per * per, 1) < 0.12: keep[i] = True
    return keep[lab] & (m > 0) | (keep[lab] & (mc > 0))


rivers_now = rivers_only(water_now)
RBAND = nearby(rivers_now, 120)   # old courses lie within 300 m of the present rivers


def epoch_water(det, cov, base):
    return base | clean(det & cov & RBAND, 300)
FRAME_PX = lambda pts: np.array([[(x - BBOX[0]) / RES, (BBOX[3] - y) / RES] for x, y in pts], np.int32)
r57 = np.zeros((N, N), np.uint8); f57 = np.zeros((N, N), np.uint8)
for f in H57['features']:
    if f['kind'] == 'river': cv2.fillPoly(r57, [FRAME_PX(f['poly'])], 1)
cv2.fillPoly(f57, [FRAME_PX(H57['field'])], 1)
w1410 = np.where(f57 > 0, r57 > 0, rivers_now)
water_ep = [(1410, w1410)]
# the fortification plan of 1658 (map 5): pale blue rivers, warped into the frame
FMW = np.array([[1 / RES, 0, -BBOX[0] / RES], [0, -1 / RES, BBOX[3] / RES], [0, 0, 1]])
_pj = json.load(open(os.path.join(HERE, 'fort_plans.json'), encoding='utf-8'))['plans']['1658']
_A = np.r_[np.array(FPLANS['plans']['1658']['affine']), [[0, 0, 1]]] @ np.array([[0.5, 0, -_pj['origin'][0] / 2], [0, 0.5, -_pj['origin'][1] / 2], [0, 0, 1]])
_pg = os.path.join(ROOT, 'data', 'reference', 'hiu-atlas', 'pages', 'p043_300.png')
if os.path.exists(_pg):
    pim = cv2.imdecode(np.fromfile(_pg, np.uint8), 1)
    pf = np.zeros(pim.shape[:2], np.uint8); cv2.fillPoly(pf, [np.array([(160, 883), (1270, 883), (1270, 160), (2967, 160), (2967, 3815), (160, 3815)], np.int32)], 255)
    Hf = FMW @ _A
    wim = cv2.warpPerspective(pim, Hf, (N, N), flags=cv2.INTER_AREA); cov58 = cv2.warpPerspective(pf, Hf, (N, N), flags=cv2.INTER_NEAREST) > 0
    H, Sat, V = hsv(wim)
    w = epoch_water((H >= 160) & (H < 230) & (Sat > 0.10) & (V > 0.45), cov58, w1410)
    water_ep.append((1658, w))
WATER_RULES = [  # (raster, year, rule)
    ('1840_cadastre', 1840, lambda H, S, V: (H >= 150) & (H < 220) & (S > 0.15) & (V > 0.35) & (V < 0.9)),
    ('1908', 1908, lambda H, S, V: (H >= 160) & (H < 205) & (S > 0.18) & (V > 0.6)),
]   # from 1920 on (modern Plzeň) the present rivers (owner's decision 2026-11-24; to be refined by hand in the editor)
for name, year, wr in WATER_RULES:
    im, alpha = imread(raw_path(name)); H, Sat, V = hsv(im); cov = coverage(name, im, alpha)
    water_ep.append((year, epoch_water(wr(H, Sat, V), cov, rivers_now)))   # present rivers + the water of this map (meanders, races, ponds)
water_ep.append((1920, rivers_now))
water_ep.append((1953, water_now))
# water painted by hand in the editor (manual/water_<map>.png, frame raster): added to the epoch of the map, or a new
# epoch at the map's year (the water of the previous epoch plus the painted water)
for f in sorted(os.listdir(MAN)) if os.path.isdir(MAN) else []:
    if not (f.startswith('water_') and f.endswith('.png')): continue
    Y = MYEAR.get(f[6:-4]);  wm = cv2.imdecode(np.fromfile(os.path.join(MAN, f), np.uint8), 0)
    if Y is None or wm is None: continue
    wm = cv2.resize(wm, (N, N), interpolation=cv2.INTER_NEAREST) > 127
    water_ep.sort(key=lambda e: e[0])
    k = max([i for i, (yy, _) in enumerate(water_ep) if yy <= Y] or [0])
    if water_ep[k][0] == Y: water_ep[k] = (Y, water_ep[k][1] | wm)
    else: water_ep.insert(k + 1, (Y, water_ep[k][1] | wm))
    print('  manual water', f, '→ epoch', Y, f'{wm.sum() * RES * RES / 1e4:.1f} ha')
water_ep.sort(key=lambda e: e[0])
for year, w in water_ep:
    f = f'water_{year}.png'
    cv2.imencode('.png', (cv2.resize(w.astype(np.uint8) * 255, (1024, 1024), interpolation=cv2.INTER_AREA)))[1].tofile(os.path.join(OUT, f))
    out['water'].append({'year': 1295 if year == 1410 else year, 'file': f})
print('water epochs:', [y for y, _ in water_ep])


def base_for(year):
    w = next((m for y, m in reversed(water_ep) if (1295 if y == 1410 else y) <= year), water_ep[0][1])
    b = np.full((N, N, 3), (196, 214, 205), np.uint8); b[w] = (205, 160, 110); return b


bases = {}
b0 = base_for(1295)   # the opening map: rivers only
cv2.imencode('.jpg', cv2.resize(b0, (S, S), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 85])[1].tofile(os.path.join(OUT, 'ground_base.jpg'))
out['grounds'].append({'year': 1295, 'file': 'ground_base.jpg', 'label': 'base'})
# ground maps: each is shown from its year until the next one
GROUNDS = [('1781', 1781), ('1821', 1821), ('1840_cadastre', 1840), ('1877_mesto', 1877), ('1881', 1881), ('1893', 1893), ('1902', 1902), ('1908', 1908),
           ('1926', 1926), ('1938', 1938), ('1947', 1947), ('1953_orto', 1953), ('2001_orto', 2001), ('2025_ztm', 2015)]
for name, year in GROUNDS:
    im, alpha = imread(raw_path(name))
    cov = coverage(name, im, alpha) if name != '2025_ztm' else np.ones(im.shape[:2], bool)
    if name == '2001_orto': cov &= im.max(2) > 8  # the archive orthophoto has a black gap in the north-west
    im = cv2.resize(im, (N, N)) if im.shape[0] != N else im
    comp = base_for(year).copy(); comp[cov] = im[cov]
    cv2.imencode('.jpg', cv2.resize(comp, (S, S), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(OUT, f'ground_{year}.jpg'))
    out['grounds'].append({'year': year, 'file': f'ground_{year}.jpg', 'label': name})
# early ground maps registered to the model: map 57 (c. 1410), the Theatrum Europaeum plate (1618, homography of
# its 12 control points), the fortification plans of 1658 and 1703 (affines of fort_plans.py)
FM = np.array([[1 / RES, 0, -BBOX[0] / RES], [0, -1 / RES, BBOX[3] / RES], [0, 0, 1]])
M3 = lambda a: np.r_[np.asarray(a, float), [[0, 0, 1]]] if np.asarray(a).shape == (2, 3) else np.asarray(a, float)


def early_ground(img, H_page2map, field, year, name, content_only=False):
    Hf = FM @ M3(H_page2map)
    warped = cv2.warpPerspective(img, Hf, (N, N), flags=cv2.INTER_AREA)
    fm = np.zeros(img.shape[:2], np.uint8); cv2.fillPoly(fm, [np.array(field, np.int32)], 255)
    m = cv2.warpPerspective(fm, Hf, (N, N), flags=cv2.INTER_NEAREST) > 0
    if content_only:   # the drawn map only (colour fills, rivers, lines): the white paper and the grey watermark of the
        hh, ss, vv = hsv(warped)   # atlas page become the terrain base
        m &= cv2.dilate(((ss > 0.12) | (vv < 0.5)).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    comp = base_for(year).copy(); comp[m] = warped[m]
    cv2.imencode('.jpg', cv2.resize(comp, (S, S), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(OUT, f'ground_{year}.jpg'))
    out['grounds'].append({'year': year, 'file': f'ground_{year}.jpg', 'label': name})


PAGES = os.path.join(ROOT, 'data', 'reference', 'hiu-atlas', 'pages')
rd = lambda f: cv2.imdecode(np.fromfile(f, np.uint8), 1)
if os.path.exists(os.path.join(PAGES, 'p090_300.png')):
    early_ground(rd(os.path.join(PAGES, 'p090_300.png')), H57['affine'], [(160, 1000), (3350, 1000), (3350, 4650), (160, 4650)], 1300, 'map 57 (c. 1410)', content_only=True)
te_pts = json.load(open(os.path.join(HERE, 'te1618_points.json'), encoding='utf-8'))
Hte, _ = cv2.findHomography(np.array([q['img'] for q in te_pts], np.float32), np.array([q['map'] for q in te_pts], np.float64))
tc = np.mean([q['img'] for q in te_pts], 0)
te_field = [(tc[0] + 1.7 * (x - tc[0]), tc[1] + 1.7 * (y - tc[1])) for x, y in cv2.convexHull(np.array([q['img'] for q in te_pts], np.float32)).reshape(-1, 2)]
early_ground(rd(os.path.join(ROOT, 'data', 'historic', 'sources', 'te-1618.jpg')), Hte, te_field, 1618, 'Theatrum Europaeum 1618')
for pid, year, field in (('1658', 1658, [(160, 883), (1270, 883), (1270, 160), (2967, 160), (2967, 3815), (160, 3815)]),
                         ('1703', 1703, [(177, 406), (3196, 406), (3196, 4521), (1166, 4521), (1166, 3037), (212, 3037), (177, 3037)])):
    pl = FPLANS['plans'][pid]; ox, oy = next(v['origin'] for k, v in json.load(open(os.path.join(HERE, 'fort_plans.json'), encoding='utf-8'))['plans'].items() if k == pid)
    A = M3(pl['affine']) @ np.array([[0.5, 0, -ox / 2], [0, 0.5, -oy / 2], [0, 0, 1]])
    early_ground(rd(os.path.join(PAGES, f'p04{3 if pid == "1658" else 4}_300.png')), A, field, year, f'plan {pid}')
out['grounds'].sort(key=lambda g: g['year'])
for f in os.listdir(OUT):  # remove ground files of an earlier run that are no longer listed
    if f.startswith('ground_') and f not in {g['file'] for g in out['grounds']}: os.remove(os.path.join(OUT, f))
# mesh.bin: int32 [nb, nv, nt, 0], int32 bld[nb], vcount[nb], tcount[nb], float32 verts[nv, 3]
# (x, y relative to the origin in metres, z above the model base), uint16 tris[nt, 3] (local per building)
mb_b, mb_vc, mb_tc, mb_V, mb_T = [], [], [], [], []
for b, it in enumerate(recs):
    if 'imesh' in it:   # generated shapes (fortification): mode 0 = z above the base, mode 1 = z above the local terrain
        v = np.array(it['imesh']['v'], float)
        zz = v[:, 2] + np.where(v[:, 3] > 0.5, [z_at(x, y) - ZMIN - it['z'] for x, y in v[:, :2]], 0.0)
        mb_b.append(b); mb_vc.append(len(v)); mb_tc.append(len(it['imesh']['t']))
        mb_V.append(np.c_[v[:, 0] - OX, v[:, 1] - OY, zz]); mb_T.append(np.array(it['imesh']['t'], np.int64)); continue
    if 'mesh' not in it: continue
    vv, tt, off = [], [], 0
    for j in it['mesh']:
        v = m_V[m_vs[j]:m_vs[j + 1]].astype(np.float64)
        vv.append(np.c_[v[:, 0] + m_O[0] - OX, v[:, 1] + m_O[1] - OY, v[:, 2] - it['mesh_z0']]); tt.append(m_T[m_ts[j]:m_ts[j + 1]] + off); off += len(v)
    if off > 65535: continue
    mb_b.append(b); mb_vc.append(off); mb_tc.append(sum(len(t) for t in tt)); mb_V.append(np.vstack(vv)); mb_T.append(np.vstack(tt))
if mb_b:
    with open(os.path.join(OUT, 'mesh.bin'), 'wb') as fh:
        nv_, nt_ = sum(mb_vc), sum(mb_tc)
        fh.write(np.array([len(mb_b), nv_, nt_, 0], np.int32).tobytes())
        for a in (mb_b, mb_vc, mb_tc): fh.write(np.array(a, np.int32).tobytes())
        fh.write(np.vstack(mb_V).astype(np.float32).tobytes()); fh.write(np.vstack(mb_T).astype(np.uint16).tobytes())
    # terrain cut-outs over the moats: R = index into out['cuts']['periods'] (1-based), 1 m pixels
    if CUTS:
        u = shapely.ops.unary_union([c[0] for c in CUTS]).bounds
        cx0, cy0, cx1, cy1 = u[0] - 5, u[1] - 5, u[2] + 5, u[3] + 5
        CW, CH = int(cx1 - cx0) + 1, int(cy1 - cy0) + 1
        cm = np.zeros((CH, CW), np.uint8)
        for i, (pg, f0, t0) in enumerate(CUTS[:8]):   # bit i = region i
            lay = np.zeros((CH, CW), np.uint8)
            for part in fabric._parts(pg):
                cv2.fillPoly(lay, [np.array([[(x - cx0), (cy1 - y)] for x, y in part.exterior.coords], np.int32)], 1)
                for hole in part.interiors: cv2.fillPoly(lay, [np.array([[(x - cx0), (cy1 - y)] for x, y in hole.coords], np.int32)], 0)
            cm |= (lay << i).astype(np.uint8)
        cv2.imencode('.png', cm)[1].tofile(os.path.join(OUT, 'cuts.png'))
        out['cuts'] = {'bits': True, 'file': 'cuts.png', 'box': [round(cx0 - OX, 1), round(cy0 - OY, 1), round(cx1 - OX, 1), round(cy1 - OY, 1)],
                       'periods': [[round(f0, 2), round(t0, 2)] for _, f0, t0 in CUTS]}
    out['mesh'] = {'file': 'mesh.bin', 'buildings': len(mb_b), 'source': 'Statutární město Plzeň, 3D model budov 2024 (GIS_Budovy_Plzen_2024)'}
    print('mesh.bin', len(mb_b), 'buildings', round(os.path.getsize(os.path.join(OUT, 'mesh.bin')) / 1e6, 1), 'MB')
json.dump(out, open(os.path.join(OUT, 'model.json'), 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
json.dump({'calibration': calib, 'validation': valid}, open(os.path.join(OUT, 'validation.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', len(recs), 'buildings', round(os.path.getsize(os.path.join(OUT, 'model.json')) / 1e6, 1), 'MB')
