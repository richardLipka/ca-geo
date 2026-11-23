"""Schematic 3D growth model of Plzeň 1295-2020: every building gets an (interpolated) year of
origin, optional rebuild and demolition, consistent with the available evidence.

Evidence, in order of trust:
1. RÚIAN building footprints (present stock) with completion date `dokonceni`; dates that are
   age-class placeholders (31 Dec 1919 / 1945 / 1960 / 1970 / 1980 / 1990 / 2000) are used as
   intervals.
2. Building pixels of the georeferenced map epochs (stable cadastre 1840, 3rd military survey
   1880, city plans 1891-1947, orthophoto 1953) at each footprint → first epoch in which the place
   is built (weighted monotone split, tolerant to misclassified epochs).
3. Before 1840 (place already built on the stable cadastre): dated by zone and written history —
   inner town settled after the founding (1295-1335, from the square outwards); medieval gate
   suburbs (burned 1433-34 and 1618, glacis cleared 1647, rebuilt after 1795); villages from their
   first written mention; later suburbs and isolated buildings 1650-1840.
4. Buildings of the stable cadastre that no longer exist → historic-only footprints; their
   demolition is the first later epoch where the place is empty.
5. Fortification and landmarks from the c. 1536-1618 model (projects/plzen.json): wall ring,
   towers, gates with demolition dates, churches.
Within an interval the year follows the growth front: places closer to the built-up area of the
previous epoch are dated earlier.

usage: python growth_model.py   (paths relative to the repository)
writes data/historic/growth/web/model.json and ground_*.jpg
"""
import datetime, json, math, os, random
import cv2
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from growth_rules import BBOX, RES, N, to_px, to_map, imread, rule, coverage, hsv

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RAW = os.path.join(ROOT, 'data', 'historic', 'growth', 'raw')
OUT = os.path.join(ROOT, 'data', 'historic', 'growth', 'web')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(1295)

# map epochs: (raster, year, weight = trust in the building classification)
EPOCHS = [('1840_cadastre', 1840, 1.0), ('1880_vm3', 1880, 0.4), ('1891', 1891, 0.5), ('1895', 1895, 0.5),
          ('1912', 1912, 0.7), ('1926', 1926, 0.8), ('1931', 1931, 0.8), ('1938', 1938, 0.8),
          ('1947', 1947, 0.9), ('1953_orto', 1953, 0.4)]
YEARS = [y for _, y, _ in EPOCHS]
CLASS_END = {1919: None, 1945: 1919, 1960: 1945, 1970: 1960, 1980: 1970, 1990: 1980, 2000: 1990}  # RÚIAN age classes
SQUARE = (-822396.8, -1069689.4)  # St Bartholomew, centre of the square

# villages: first written mention (cs.wikipedia, retrieved Nov 2026); Malice = Roudná (All Saints, older than the town)
VILLAGES = {
    'Skvrňany': ((-826599.1, -1071139.1), 1239), 'Doudlevce': ((-822166.5, -1073163.7), 1227),
    'Malice (Roudná)': (None, 1250), 'Božkov': ((-818286.0, -1071613.8), 1338), 'Doubravka': ((-819089.0, -1069692.9), 1338),
    'Valcha': ((-825336.9, -1072906.6), 1352), 'Koterov': ((-818903.4, -1073770.1), 1369), 'Lobzy': ((-819992.2, -1070748.4), 1379),
    'Bolevec': ((-821245.7, -1065654.0), 1382), 'Radčice': ((-826001.3, -1067270.2), 1420), 'Hradiště': ((-821662.9, -1074027.4), 1686),
}
EVENTS = [
    (1295, 'Založení Nové Plzně (Václav II.), pravidelná osnova s náměstím', 'Founding of New Plzeň (Wenceslas II), regular plan with the square'),
    (1320, 'Hradby a stavba kostela sv. Bartoloměje (1. pol. 14. st.)', 'Town wall and St Bartholomew church under construction (early 14th c.)'),
    (1433, 'Husitské obléhání 1433–34, předměstí zničena', 'Hussite siege 1433–34, suburbs destroyed'),
    (1532, 'Vodárenská věž', 'Water tower'),
    (1618, 'Obléhání Mansfeldem 19. 9. – 21. 11. 1618, předměstí vypálena (Theatrum Europaeum, leg. D)', 'Siege by Mansfeld 19 Sep – 21 Nov 1618, suburbs burned (Theatrum Europaeum, legend D)'),
    (1645, 'Bastionové opevnění (Lacron 1645–49), 1647 vyklizeno předpolí', 'Bastioned fortification (Lacron 1645–49), glacis cleared 1647'),
    (1788, 'Schaller: 315 domů ve městě, 142 na předměstích', 'Schaller: 315 houses in the town, 142 in the suburbs'),
    (1795, 'Začíná bourání hradeb, zasypávání příkopů (1795–1822)', 'Wall demolition begins, moats filled (1795–1822)'),
    (1804, 'Zbořena Litická brána', 'Litice gate demolished'), (1822, 'Zbořena Pražská brána', 'Prague gate demolished'),
    (1828, 'Západní hradby → okružní sady', 'Western walls → ring park'), (1833, 'Zbořena Říšská brána', 'Imperial gate demolished'),
    (1842, 'Měšťanský pivovar', "Burghers' brewery"), (1849, 'Zbořena Saská brána, poslední brána', 'North (Saxon) gate demolished, the last gate'),
    (1859, 'Valdštejnova strojírna, od 1869 Škoda', 'Waldstein engineering works, Škoda from 1869'),
    (1861, 'Železnice Praha – Plzeň – Furth (1861–62)', 'Railway Prague – Plzeň – Furth (1861–62)'),
    (1893, 'Poslední úsek hradeb odstraněn pro muzeum (1893–99)', 'Last wall section removed for the museum (1893–99)'),
    (1924, 'Velká Plzeň: připojeny Doubravka, Doudlevce, Lobzy, Skvrňany', 'Greater Plzeň: Doubravka, Doudlevce, Lobzy and Skvrňany joined'),
    (1945, 'Bombardování Škodových závodů a nádraží', 'Bombing of the Škoda works and the railway'),
    (1955, 'Panelová sídliště (Slovany, Bory, Doubravka, Lochotín, Košutka, Vinice do 1992)', 'Prefab housing estates (Slovany, Bory, Doubravka, Lochotín, Košutka, Vinice until 1992)'),
]


def dyear(ms):
    """RÚIAN completion → (year, None) exact or (lo, hi) age-class interval, or None."""
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


# ---------- evidence rasters ----------
print('loading epochs')
B, C, D = {}, {}, {}
for name, year, _ in EPOCHS:
    f = next(x for x in os.listdir(RAW) if x.split('.')[0] == name)
    im, alpha = imread(os.path.join(RAW, f))
    cov = coverage(name, im, alpha)
    b = rule(name, im, alpha) & cov
    if name == '1840_cadastre':  # add saturated yellow (wooden buildings); field colours are paler
        H, S, V = hsv(im); b |= (H >= 45) & (H < 65) & (S > 0.5) & (V > 0.6) & cov
    B[name], C[name] = b, cov
    area = cv2.blur(b.astype(np.float32), (41, 41)) > 0.08
    D[name] = cv2.distanceTransform((~area).astype(np.uint8), cv2.DIST_L2, 5) * RES  # metres to the built-up area
    print(' ', name, round(float(b.sum()) * RES * RES / 1e6, 2), 'km² building pixels')


def states(sl, m):
    out = []
    for name, _, _ in EPOCHS:
        if C[name][sl][m].mean() < 0.5: out.append(None); continue
        out.append(B[name][sl][m].mean() >= 0.2)
    return out


def split_built(st):
    """first epoch index k from which the place is built (len = after the last epoch); weighted monotone fit."""
    best, bk = 1e9, 0
    for k in range(len(EPOCHS) + 1):
        c = sum(w for i, (_, _, w) in enumerate(EPOCHS) if st[i] is not None and ((i < k and st[i]) or (i >= k and not st[i])))
        if c < best - 1e-9: best, bk = c, k
    return bk


def split_gone(st):
    """first epoch index k from which a historic building is gone (2025 counts as gone)."""
    best, bk = 1e9, len(EPOCHS)
    for k in range(1, len(EPOCHS) + 1):
        c = sum(w for i, (_, _, w) in enumerate(EPOCHS) if st[i] is not None and ((i < k and not st[i]) or (i >= k and st[i])))
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

recs = []  # dicts: ring, from, to, h0, h1, tR, gaps, cls, basis


def height(p, area):
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
        for it in its: it['from'] = min(it['from'], 1839.5)


def front_rank(items, epoch_lo):
    """order items inside one interval by distance to the built-up area of the previous epoch."""
    if not items: return
    if epoch_lo is None:
        for it in items: it['rank'] = rng.random()
        return
    name = next(n for n, y, _ in EPOCHS if y == epoch_lo)
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
    it = {'ring': ring, 'x': c.x, 'y': c.y, 'h1': height(p, area), 'ruian': dyear(p.get('dokonceni')), 'area': area, 'gaps': []}
    lm = next((k for k, q in LANDMARK_PTS.items() if poly.buffer(2).contains(q)), None)
    if lm:
        it['from'], it['h1'] = LANDMARK_FROM[lm]; it['h0'] = it['h1']; it['cls'] = 'landmark'; it['basis'] = 'history'; recs.append(it); continue
    st = states(sl, m)
    it['k'] = split_built(st)
    pending.append(it)

groups = {}
for it in pending:
    k, rd = it['k'], it['ruian']
    mlo, mhi = interval(k)
    if rd and rd[0] == 'exact':
        ye = rd[1]
        if k == 0 and ye > 1860: it['tR'] = ye + 0.5; it['basis'] = 'map 1840 + rebuilt (RÚIAN date)'; pre.append(it)
        elif k > 0 and mhi < ye - 10: it['tR'] = ye + 0.5; it['basis'] = 'map + rebuilt (RÚIAN date)'; groups.setdefault((mlo, mhi), []).append(it)
        elif k == 0 and ye <= 1860: it['from'] = float(min(ye, 1839)); it['basis'] = 'RÚIAN date'; it['cls'] = zone(it['x'], it['y'])[0]
        else: it['from'] = ye + rng.random() * 0.9; it['basis'] = 'RÚIAN date'
        continue
    if rd and rd[0] == 'class':
        clo, chi = rd[1], rd[2]
        lo = max(clo if clo is not None else -1e9, mlo if mlo is not None else -1e9); hi = min(chi, mhi)
        if k == 0 and (clo is None):  # built in 1840 and old class: pre-1840 place, 19th-c. rebuild possible
            it['basis'] = 'map 1840 + RÚIAN class'; pre.append(it); continue
        if k == 0: it['tR'] = rng.uniform(clo, chi) + 0.5; it['basis'] = 'map 1840 + rebuilt (RÚIAN class)'; pre.append(it); continue
        if lo < hi:
            it['basis'] = 'map + RÚIAN class'; groups.setdefault((None if lo < -1e8 else lo, hi), []).append(it); continue
        if mhi <= (clo or -1e9):
            it['tR'] = rng.uniform(clo, chi) + 0.5; it['basis'] = 'map + rebuilt (RÚIAN class)'; groups.setdefault((mlo, mhi), []).append(it); continue
        it['basis'] = 'RÚIAN class (map later)'; groups.setdefault((clo, chi), []).append(it); continue
    if k == 0: it['basis'] = 'map 1840'; pre.append(it); continue
    it['basis'] = 'map'; groups.setdefault((mlo, mhi), []).append(it)

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
    ring = [to_map(x0 + px - 0.5 + 0.5, y0 + py - 0.5 + 0.5) for px, py in ap]
    X, Y = to_map(*cen[i][:2].tolist())
    if wall_line.distance(Point(X, Y)) < 9: continue  # the town wall itself is drawn in carmine
    fp = footprint(ring)
    if fp is None: continue
    st = states(*fp)
    kg = split_gone(st)
    lo, hi = interval(kg)
    it = {'ring': ring, 'x': X, 'y': Y, 'h1': 9.0 if WALL.contains(Point(X, Y)) else 5.5, 'gaps': [], 'basis': 'map 1840, demolished (maps)',
          'to': (lo or 1840) + ((hi - (lo or 1840)) * rng.uniform(0.15, 0.85))}
    hist.append(it)
pre1840(pre + hist)
for it in pre + hist:
    if 'h0' not in it:
        it['h0'] = min(it['h1'], 9.0 if it['cls'] == 'inner' else 6.0)
        if it['h1'] > it['h0'] + 1 and 'tR' not in it: it['tR'] = rng.uniform(1850, 1919)
recs += pending + hist

# ---------- fortification and landmarks without a present footprint ----------
def box(xy, w, d, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(xy[0] + ca * u - sa * v, xy[1] + sa * u + ca * v) for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2))]
    return pts + [pts[0]]  # closed ring like the other footprints

wall_c = list(WALL.exterior.coords)
ring_len = WALL.exterior.length
MUSEUM = (-822180.0, -1069800.0)  # east / south-east of the old town (Kopeckého sady)
pieces = []
for i in range(len(wall_c) - 1):
    a, b = wall_c[i], wall_c[i + 1]; L = math.hypot(b[0] - a[0], b[1] - a[1]); nseg = max(1, int(L // 30))
    for j in range(nseg):
        p0 = (a[0] + (b[0] - a[0]) * j / nseg, a[1] + (b[1] - a[1]) * j / nseg)
        p1 = (a[0] + (b[0] - a[0]) * (j + 1) / nseg, a[1] + (b[1] - a[1]) * (j + 1) / nseg)
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        g = min(GATES, key=lambda g: math.hypot(mid[0] - g[0][0], mid[1] - g[0][1]))
        dem = g[1]
        if mid[0] < SQUARE[0] - 90: dem = 1828  # western walls → ring park
        if math.hypot(mid[0] - MUSEUM[0], mid[1] - MUSEUM[1]) < 45: dem = 1896
        poly = LineString([p0, p1]).buffer(1.4, cap_style=2)
        recs.append({'ring': list(poly.exterior.coords), 'x': mid[0], 'y': mid[1], 'from': 1320 + rng.uniform(-10, 10), 'to': dem + rng.uniform(-3, 0),
                     'h0': 8.0, 'h1': 8.0, 'gaps': [], 'cls': 'fort', 'basis': 'model 1618 + dated demolitions'})
        pieces.append((mid, dem))
for k, e in ENT.items():
    if e['type'] not in ('gate', 'tower') or not e.get('geom') or e['geom']['type'] != 'Point': continue
    xy = tuple(e['geom']['coords'][0])
    if k == 'g1618-barth_tower': recs.append({'ring': box(xy, 11, 11), 'x': xy[0], 'y': xy[1], 'from': 1320, 'h0': 102.3, 'h1': 102.3, 'gaps': [], 'cls': 'landmark', 'basis': 'history'}); continue
    if k == 'g1618-water_tower': continue
    dem = e.get('validTo') or 1849
    if k.startswith('g1618-te_tower'): dem = min(pieces, key=lambda p: math.hypot(p[0][0] - xy[0], p[0][1] - xy[1]))[1]
    w = 10 if e['type'] == 'gate' else 7
    recs.append({'ring': box(xy, w, w), 'x': xy[0], 'y': xy[1], 'from': 1325 + rng.uniform(-5, 5), 'to': float(dem), 'h0': e.get('height', 15), 'h1': e.get('height', 15),
                 'gaps': [], 'cls': 'fort', 'basis': 'model 1618 + dated demolitions'})
dxy = tuple(ENT['g1618-dominican']['geom']['coords'][0])
recs.append({'ring': box(dxy, 34, 14), 'x': dxy[0], 'y': dxy[1], 'from': 1300, 'to': 1785, 'h0': 16, 'h1': 16, 'gaps': [], 'cls': 'landmark', 'basis': 'history'})

# ---------- calibration check ----------
def visible(it, y):
    if it['from'] > y or it.get('to', 9999) <= y: return False
    return not any(s <= y < e for s, e in it.get('gaps', []))
cnt = {c: sum(1 for it in recs if it.get('cls') == c and visible(it, 1788)) for c in ('inner', 'suburb', 'glacis')}
print('visible in 1788 (buildings, not houses):', cnt, '| Schaller 1788: 315 houses in town, 142 in suburbs')
for y in (1300, 1400, 1500, 1618, 1700, 1800, 1840, 1880, 1912, 1938, 1953, 1980, 2020):
    print(f'  {y}: {sum(1 for it in recs if visible(it, y))} buildings')

# ---------- write ----------
OX, OY = SQUARE
CLS = ['inner', 'suburb', 'glacis', 'village', 'rural', 'town', 'fort', 'landmark']
BASIS = sorted({it['basis'] for it in recs})
out = {'format': 'ca-geo/growth-model', 'crs': 'EPSG:5514', 'origin': [OX, OY], 'frame': BBOX, 'years': [1295, 2020],
       'classes': CLS, 'basis': BASIS, 'events': [{'year': y, 'cs': c, 'en': e} for y, c, e in EVENTS],
       'villages': [{'name': k, 'xy': [round(v[0][0] - OX, 1), round(v[0][1] - OY, 1)], 'mention': v[1]} for k, v in VILLAGES.items()],
       'grounds': [], 'n': len(recs), 'rings': [], 'from': [], 'to': [], 'h0': [], 'h1': [], 'tR': [], 'gaps': [], 'cls': [], 'basisIdx': []}
for it in recs:
    out['rings'].append([v for x, y in it['ring'][:-1] if True for v in (round((x - OX) * 10), round((y - OY) * 10))])
    out['from'].append(round(it['from'], 1)); out['to'].append(round(it.get('to', 9999), 1))
    out['h0'].append(round(it.get('h0', it['h1']), 1)); out['h1'].append(round(it['h1'], 1)); out['tR'].append(round(it.get('tR', 9999), 1))
    g = it.get('gaps', []) + [(0, 0)] * (2 - len(it.get('gaps', [])))
    out['gaps'].append([round(v, 1) for s, e in g[:2] for v in (s, e)])
    out['cls'].append(CLS.index(it.get('cls', 'town')))
    out['basisIdx'].append(BASIS.index(it['basis']))

# ---------- ground textures ----------
S = 2048
# rivers and ponds from the present ZTM 10 (the stable cadastre covers only part of the frame);
# present water bodies are kept for all years (schematic: later reservoirs are not removed)
ztm, _ = imread(os.path.join(RAW, '2025_ztm.png'))
H, Sat, V = hsv(ztm)
water = ((H >= 180) & (H < 235) & (Sat > 0.25) & (V > 0.5)).astype(np.uint8)
water = cv2.morphologyEx(water, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
nw, lw, sw, _ = cv2.connectedComponentsWithStats(water, 8); keep = np.zeros(nw, bool); keep[1:] = sw[1:, cv2.CC_STAT_AREA] >= 150
water = cv2.morphologyEx(keep[lw].astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
base = np.full((N, N, 3), (196, 214, 205), np.uint8); base[water > 0] = (205, 160, 110)
base_s = cv2.resize(base, (S, S), interpolation=cv2.INTER_AREA)
cv2.imencode('.jpg', base_s, [cv2.IMWRITE_JPEG_QUALITY, 85])[1].tofile(os.path.join(OUT, 'ground_base.jpg'))
out['grounds'].append({'year': 1295, 'file': 'ground_base.jpg'})
for name, year in (('1840_cadastre', 1840), ('1880_vm3', 1880), ('1912', 1912), ('1938', 1938), ('1953_orto', 1953), ('2025_ztm', 1995)):  # present map shown from the 1990s
    f = next(x for x in os.listdir(RAW) if x.split('.')[0] == name)
    im, alpha = imread(os.path.join(RAW, f))
    cov = coverage(name, im, alpha) if name != '2025_ztm' else np.ones(im.shape[:2], bool)
    im = cv2.resize(im, (N, N)) if im.shape[0] != N else im
    comp = base.copy(); comp[cov] = im[cov]
    cv2.imencode('.jpg', cv2.resize(comp, (S, S), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(OUT, f'ground_{year}.jpg'))
    out['grounds'].append({'year': year, 'file': f'ground_{year}.jpg'})
json.dump(out, open(os.path.join(OUT, 'model.json'), 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
print('wrote', len(recs), 'buildings', round(os.path.getsize(os.path.join(OUT, 'model.json')) / 1e6, 1), 'MB')
