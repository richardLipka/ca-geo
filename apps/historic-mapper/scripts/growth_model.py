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
from growth_rules import BBOX, RES, N, to_px, to_map, imread, rule, coverage, hsv

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

EVENTS = [
    (1295, 'Založení Nové Plzně (Václav II.), pravidelná osnova s náměstím', 'Founding of New Plzeň (Wenceslas II), regular plan with the square'),
    (1320, 'Hradby a stavba kostela sv. Bartoloměje (1. pol. 14. st.)', 'Town wall and St Bartholomew church under construction (early 14th c.)'),
    (1420, 'Parkán (vnější hradba) a příkop před r. 1420', 'Zwinger (outer wall) and moat before 1420'),
    (1433, 'Husitské obléhání 1433–34, předměstí zničena', 'Hussite siege 1433–34, suburbs destroyed'),
    (1532, 'Vodárenská věž', 'Water tower'),
    (1618, 'Obléhání Mansfeldem 19. 9. – 21. 11. 1618, předměstí vypálena (Theatrum Europaeum, leg. D)', 'Siege by Mansfeld 19 Sep – 21 Nov 1618, suburbs burned (Theatrum Europaeum, legend D)'),
    (1645, 'Šance a raveliny před hradbou (de la Corona 1645–58; plán 1658), 1647 vyklizeno předpolí', 'Earthwork bastions and ravelins (de la Corona 1645–58; plan of 1658), glacis cleared 1647'),
    (1703, 'Zizner obnovuje opevnění (březen–prosinec 1703), rozsah nových děl nejistý', 'Zizner repairs the fortification (March–December 1703); extent of new works uncertain'),
    (1760, 'Díla chátrají (plán 1781: „eingegangene Vestungswerker“)', 'The works decay (1781 plan: "eingegangene Vestungswerker")'),
    (1788, 'Schaller: 315 domů ve městě, 142 na předměstích', 'Schaller: 315 houses in the town, 142 in the suburbs'),
    (1795, 'Začíná bourání hradeb, zasypávání příkopů (1795–1822)', 'Wall demolition begins, moats filled (1795–1822)'),
    (1804, 'Zbořena Litická brána', 'Litice gate demolished'), (1822, 'Zbořena Pražská brána', 'Prague gate demolished'),
    (1828, 'Západní hradby a bašta → okružní sady', 'Western walls and bastion → ring park'), (1833, 'Zbořena Říšská brána', 'Imperial gate demolished'),
    (1842, 'Měšťanský pivovar', "Burghers' brewery"), (1849, 'Zbořena Saská brána, poslední brána', 'North (Saxon) gate demolished, the last gate'),
    (1859, 'Valdštejnova strojírna, od 1869 Škoda', 'Waldstein engineering works, Škoda from 1869'),
    (1861, 'Železnice Praha – Plzeň – Furth (1861–62)', 'Railway Prague – Plzeň – Furth (1861–62)'),
    (1869, 'Sčítání: ve městě 988 domů (ČSÚ)', 'Census: 988 houses in the town (ČSÚ)'),
    (1893, 'Poslední úsek hradeb odstraněn pro muzeum (1893–99)', 'Last wall section removed for the museum (1893–99)'),
    (1924, 'Velká Plzeň: připojeny Doubravka, Doudlevce, Lobzy, Skvrňany', 'Greater Plzeň: Doubravka, Doudlevce, Lobzy and Skvrňany joined'),
    (1945, 'Bombardování Škodových závodů a nádraží', 'Bombing of the Škoda works and the railway'),
    (1955, 'Panelová sídliště (Slovany, Bory, Doubravka)', 'Prefab housing estates (Slovany, Bory, Doubravka)'),
    (1975, 'Sídliště Severního Předměstí: Lochotín, Košutka, Vinice (dokončena do 1992)', 'Northern estates: Lochotín, Košutka, Vinice (completed by 1992)'),
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
print('loading epochs')
B, C, D = {}, {}, {}
for name, year, *_ in EPOCHS:
    im, alpha = imread(raw_path(name))
    cov = coverage(name, im, alpha)
    b = rule(name, im, alpha) & cov
    if name == '1840_cadastre':  # add saturated yellow (wooden buildings); field colours are paler
        H, S, V = hsv(im); b |= (H >= 45) & (H < 65) & (S > 0.5) & (V > 0.6) & cov
    B[name], C[name] = b, cov
    area = cv2.blur(b.astype(np.float32), (41, 41)) > 0.08
    D[name] = cv2.distanceTransform((~area).astype(np.uint8), cv2.DIST_L2, 5) * RES  # metres to the built-up area
    print(f'  {name:14s} coverage {cov.sum() * RES * RES / 1e6:5.1f} km²  building pixels {b.sum() * RES * RES / 1e6:5.2f} km²')


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
DECAY = 1760  # the 1781 legend calls the works "eingegangene Vestungswerker" (defunct): lowered from about 1760
for wk in FORT['works']:  # bastions, ravelins, redoubt: the "Schantzen" of the 1658 plan, built 1645-1658
    ring = wk['poly'] + [wk['poly'][0]]; c = Polygon(ring).centroid
    recs.append({'ring': ring, 'x': c.x, 'y': c.y, 'from': rng.uniform(1645, 1658), 'to': float(wk['to']), 'h0': wk['h'], 'h1': wk['h_decayed'],
                 'tR': DECAY + rng.uniform(-10, 10), 'gaps': [], 'cls': 'fort', 'basis': 'plan 1781 + dated demolitions', 'id': 'fort:' + wk['id']})
for bd in FORT['bands']:  # ramparts along the rivers, cut into pieces
    for p0, p1, mid in line_pieces(bd['line'], 25.0):
        poly = LineString([p0, p1]).buffer(bd['half'], cap_style=2)
        recs.append({'ring': list(poly.exterior.coords), 'x': mid[0], 'y': mid[1], 'from': rng.uniform(1645, 1658), 'to': bd['to'] + rng.uniform(-3, 0),
                     'h0': bd['h'], 'h1': bd['h_decayed'], 'tR': DECAY + rng.uniform(-10, 10), 'gaps': [], 'cls': 'fort',
                     'basis': 'plan 1781 + dated demolitions', 'id': 'fort:' + bd['id']})
# moat and ditches as drawn (blue) on the 1781 plan; Zwinger moat before 1420, filled 1795-1822 by section
for wt in FORT['water']:
    for p0, p1, mid in line_pieces(wt['line'], 30.0):
        poly = LineString([p0, p1]).buffer(wt['half'], cap_style=2)
        fill = wt['to'] or min(max(wall_demolition(mid), 1795), 1822)
        start = 1420.0 if wt['id'].startswith('moat') else rng.uniform(1645, 1658)
        recs.append({'ring': list(poly.exterior.coords), 'x': mid[0], 'y': mid[1], 'from': start, 'to': fill + rng.uniform(-2, 0), 'h0': 0.35, 'h1': 0.35,
                     'gaps': [], 'cls': 'moat', 'basis': 'plan 1781 + dated demolitions', 'id': 'fort:' + wt['id']})
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
dxy = tuple(ENT['g1618-dominican']['geom']['coords'][0])
recs.append({'ring': box(dxy, 34, 14), 'x': dxy[0], 'y': dxy[1], 'from': 1300, 'to': 1785, 'h0': 16, 'h1': 16, 'gaps': [], 'cls': 'landmark', 'basis': 'history', 'id': 'g1618-dominican'})

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
CLS = ['inner', 'suburb', 'glacis', 'village', 'rural', 'town', 'fort', 'landmark', 'moat']
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

# ---------- water per epoch and ground textures ----------
S = 2048


def clean(mask, mn=150):
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    nw, lw, sw, _ = cv2.connectedComponentsWithStats(mask, 8); keep = np.zeros(nw, bool); keep[1:] = sw[1:, cv2.CC_STAT_AREA] >= mn
    return cv2.morphologyEx(keep[lw].astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)) > 0


ztm, _ = imread(raw_path('2025_ztm'))
H, Sat, V = hsv(ztm)
water_now = clean((H >= 180) & (H < 235) & (Sat > 0.25) & (V > 0.5))
WATER_RULES = {  # water colour per map; the detected old water is added to the present water (old meanders,
                 # mill races, moats), because the detection along the town reaches is incomplete
    '1840_cadastre': (1840, lambda H, S, V: (H >= 150) & (H < 220) & (S > 0.15) & (V > 0.35) & (V < 0.9)),
    '1908': (1908, lambda H, S, V: (H >= 160) & (H < 205) & (S > 0.18) & (V > 0.6)),
    '1938': (1938, lambda H, S, V: (H >= 165) & (H < 215) & (S > 0.15) & (V > 0.45)),
}
water_ep = []
for name, (year, wr) in WATER_RULES.items():
    im, alpha = imread(raw_path(name)); H, Sat, V = hsv(im); cov = coverage(name, im, alpha)
    w = clean(wr(H, Sat, V) & cov, 300) | water_now
    water_ep.append((year, w))
water_ep.append((1953, water_now))
for year, w in water_ep:
    f = f'water_{year}.png'
    cv2.imencode('.png', (cv2.resize(w.astype(np.uint8) * 255, (1024, 1024), interpolation=cv2.INTER_AREA)))[1].tofile(os.path.join(OUT, f))
    out['water'].append({'year': 1295 if year == 1840 else year, 'file': f})


def base_for(year):
    w = next((m for y, m in reversed(water_ep) if y <= max(year, 1840)), water_ep[0][1])
    b = np.full((N, N, 3), (196, 214, 205), np.uint8); b[w] = (205, 160, 110); return b


bases = {}
b0 = base_for(1840)
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
for f in os.listdir(OUT):  # remove ground files of an earlier run that are no longer listed
    if f.startswith('ground_') and f not in {g['file'] for g in out['grounds']}: os.remove(os.path.join(OUT, f))
json.dump(out, open(os.path.join(OUT, 'model.json'), 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
json.dump({'calibration': calib, 'validation': valid}, open(os.path.join(OUT, 'validation.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', len(recs), 'buildings', round(os.path.getsize(os.path.join(OUT, 'model.json')) / 1e6, 1), 'MB')
