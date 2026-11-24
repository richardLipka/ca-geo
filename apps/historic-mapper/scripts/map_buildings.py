"""Building footprints from the town plans 1891–1912 at 0.5 m (city GIS exports), 3 × 3 km around the old town.

Each plan has its own colour scheme, so each has its own rule:
  1891 black buildings on beige; 1895 orange-red houses and dark grey public / industrial buildings;
  1902 black (public, military) and solid red buildings; 1908 buildings filled by district (saturated green, pink,
  grey, yellow; parks pale green); 1912 olive buildings on pinkish paper.
Thin lines and lettering are removed by a 2.5 m opening; components ≥ 30 m² become polygons (EPSG:5514).

usage: python map_buildings.py        → data/historic/growth/raw_hi/<year>_<i>_<j>.png (tiles, cached),
                                         data/historic/growth/hi_buildings.json, raw_hi/_check_<year>.jpg
"""
import json, os, time, urllib.request
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'data', 'historic', 'growth', 'raw_hi'); os.makedirs(OUT, exist_ok=True)
X0, Y1 = -823900.0, -1068200.0          # north-west corner of the 3 × 3 km area
TILE, RES, NT = 1000.0, 0.5, 3
LAYERS = {1912: 'GIS_HIS_Plzen_1912_50cm', 1891: 'GIS_HIS_Plzen_1891', 1895: 'GIS_HIS_Plzen_1895', 1902: 'GIS_HIS_Plzen_1902', 1908: 'GIS_HIS_Plzen_1908'}
# 1912 (the most accurate plan) is registered to RÚIAN, the older plans to the registered 1912 plan


def fetch(layer, i, j, path):
    if os.path.exists(path): return
    x0, y1 = X0 + i * TILE, Y1 - j * TILE
    url = (f'https://ags.plzen.eu/arcgis/rest/services/GIS_Historicke/{layer}/MapServer/export?bbox={x0},{y1 - TILE},{x0 + TILE},{y1}'
           f'&bboxSR=5514&imageSR=5514&size=2000,2000&format=png&transparent=true&f=image')
    for k in range(3):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'historic-mapper/0.1'}), timeout=180).read()
            open(path, 'wb').write(data); return
        except Exception as e:
            print(' retry', e); time.sleep(5)


def read(path):
    from PIL import Image
    a = np.array(Image.open(path).convert('RGBA'))
    bgr = cv2.cvtColor(a[..., :3], cv2.COLOR_RGB2BGR)
    h = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return bgr, h[..., 0].astype(int) * 2, h[..., 1] / 255, h[..., 2] / 255, a[..., 3] > 0


def rule(year, H, S, V):
    red = ((H < 30) | (H > 340))
    if year == 1891: return (V < 0.40) & (S < 0.6)
    if year == 1895: return (red & (S > 0.42) & (V > 0.5)) | ((V < 0.5) & (S < 0.25) & (V > 0.12))
    if year == 1902:
        r = cv2.morphologyEx((((H < 25) | (H > 340)) & (S > 0.42) & (V > 0.5)).astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
        return ((V < 0.35) & (S < 0.5)) | r
    if year == 1908:
        return (((H >= 55) & (H <= 105) & (S > 0.45) & (V > 0.4) & (V < 0.85)) | (((H < 20) | (H > 330)) & (S > 0.18) & (S < 0.5) & (V > 0.72))
                | ((S < 0.12) & (V > 0.45) & (V < 0.8)) | ((H >= 40) & (H < 60) & (S > 0.55) & (V > 0.75)))
    if year == 1912:   # olive / brown buildings (saturated, darker than the pinkish paper); grey public buildings (solid fills)
        water = (H >= 120) & (H <= 230)
        col = (S > 0.42) & (V < 0.64) & (V > 0.2) & ~water
        grey = cv2.morphologyEx(((V < 0.42) & (S < 0.35) & ~water).astype(np.uint8), cv2.MORPH_OPEN, np.ones((11, 11), np.uint8)) > 0
        return col | grey
    raise ValueError(year)


import sys
sys.path.insert(0, HERE)
from growth_rules import imread as _imread, coverage as _coverage, BBOX as _BB, RES as _RR
_RAW = os.path.join(ROOT, 'data', 'historic', 'growth', 'raw')
_COV = {}


def field(year, i, j):
    """map field of the plan (coverage of the 2.5 m frame raster: no margins, legends or advertisements)"""
    if year not in _COV:
        name = {1912: '1912'}.get(year, str(year))
        f = next(x for x in os.listdir(_RAW) if x.split('.')[0] == name)
        im, al = _imread(os.path.join(_RAW, f)); c = _coverage(name, im, al)
        c = cv2.erode(c.astype(np.uint8), np.ones((9, 9), np.uint8))   # stay away from the edge of the sheet
        _COV[year] = c
    c = _COV[year]
    x0, y1 = X0 + i * TILE, Y1 - j * TILE
    c0, r0 = int((x0 - _BB[0]) / _RR), int((_BB[3] - y1) / _RR); w = int(TILE / _RR)
    return cv2.resize(c[r0:r0 + w, c0:c0 + w], (2000, 2000), interpolation=cv2.INTER_NEAREST) > 0


# registration: the plans of the city GIS are shifted against each other by up to ~40 m; each tile of each plan is
# moved onto the present RÚIAN footprints (phase correlation of the blurred masks, at 1 m; old blocks of the centre
# dominate the match, modern buildings only add noise)
_RU = json.load(open(os.path.join(ROOT, 'data', 'reference', 'plzen-ruian', 'buildings.geojson'), encoding='utf-8'))['features']


def ruian_tile(i, j):
    x0, y1 = X0 + i * TILE, Y1 - j * TILE
    r = np.zeros((1000, 1000), np.uint8)
    for f in _RU:
        ring = f['geometry']['coordinates'][0]
        pts = np.array([[(x - x0), (y1 - y)] for x, y in ring], np.int32)
        if pts[:, 0].max() < 0 or pts[:, 1].max() < 0 or pts[:, 0].min() > 1000 or pts[:, 1].min() > 1000: continue
        cv2.fillPoly(r, [pts], 1)
    return r


def shift(mask, i, j, ref=None):
    """(dx, dy, score) in metres that moves the plan mask onto RÚIAN: normalised correlation of the blurred masks at
    2 m, ±60 m search; no shift when the peak is weak or not distinct"""
    a_ = cv2.GaussianBlur(cv2.resize(mask.astype(np.float32), (500, 500), interpolation=cv2.INTER_AREA), (0, 0), 1.5)
    b_ = cv2.GaussianBlur(cv2.resize((ruian_tile(i, j) if ref is None else ref).astype(np.float32), (500, 500), interpolation=cv2.INTER_AREA), (0, 0), 1.5)
    M_ = 30
    if a_[M_:-M_, M_:-M_].sum() < 200: return 0.0, 0.0, 0.0
    res = cv2.matchTemplate(b_, a_[M_:-M_, M_:-M_], cv2.TM_CCOEFF_NORMED)
    _, mx, _, (px, py) = cv2.minMaxLoc(res)
    z = (res[M_, M_] if res.shape[0] > M_ else 0)
    if mx < 0.25: return 0.0, 0.0, float(mx)
    return (px - M_) * 2.0, -(py - M_) * 2.0, float(mx)


def local_field(mask, ref, base):
    """shifts (dx, dy) in metres of 250 m cells (4 × 4 per tile) onto the reference mask, ±50 m around nothing;
    weak or outlying cells take the tile shift 'base' (the plans are hand-drawn and locally distorted)"""
    A = cv2.resize(mask.astype(np.float32), (500, 500), interpolation=cv2.INTER_AREA)
    B_ = cv2.copyMakeBorder(cv2.resize(ref.astype(np.float32), (500, 500), interpolation=cv2.INTER_AREA), 25, 25, 25, 25, cv2.BORDER_CONSTANT, value=0)
    A = cv2.GaussianBlur(A, (0, 0), 1.2); B_ = cv2.GaussianBlur(B_, (0, 0), 1.2)
    F_ = np.zeros((4, 4, 3))
    for cy in range(4):
        for cx in range(4):
            t = A[cy * 125:(cy + 1) * 125, cx * 125:(cx + 1) * 125]
            F_[cy, cx] = (base[0], base[1], 0)
            if t.sum() < 150 or t.std() < 1e-3: continue
            w = B_[cy * 125:cy * 125 + 175, cx * 125:cx * 125 + 175]
            res = cv2.matchTemplate(w, t, cv2.TM_CCOEFF_NORMED)
            _, mx, _, (px, py) = cv2.minMaxLoc(res)
            dx, dy = (px - 25) * 2.0, -(py - 25) * 2.0
            if mx >= 0.35 and math.hypot(dx - base[0], dy - base[1]) < 40: F_[cy, cx] = (dx, dy, mx)
    return F_


import math
SHIFTS = {}
REF12 = {}
CELLS = {}   # per tile: 4 × 4 cells (rows from the north) of [dx, dy] in metres, used by the manual editor
out = {}
for year, layer in LAYERS.items():
    if len(sys.argv) > 1 and str(year) not in sys.argv[1:]: continue
    polys = []
    for i in range(NT):
        for j in range(NT):
            p = os.path.join(OUT, f'{year}_{i}_{j}.png'); fetch(layer, i, j, p)
            bgr, H, S, V, A = read(p)
            m = rule(year, H, S, V) & A
            m = m.astype(np.uint8)
            if year != 1891: m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))   # hatched / mottled fills
            m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))                       # lines and lettering away
            m = (m > 0) & field(year, i, j)
            if year == 1912: dxm, dym, resp = shift(m, i, j)
            else:
                dxm, dym, resp = shift(m, i, j, REF12.get((i, j)))
                if resp < 0.25: dxm, dym, resp = shift(m, i, j)   # weak match with 1912: RÚIAN
            if year == 1912:
                REF12[(i, j)] = cv2.warpAffine(m.astype(np.uint8), np.float32([[1, 0, dxm / RES], [0, 1, -dym / RES]]), (2000, 2000))
            SHIFTS[f'{year}_{i}_{j}'] = [round(dxm, 1), round(dym, 1), round(resp, 3)]
            LF = local_field(m, ruian_tile(i, j) if year == 1912 else REF12.get((i, j), ruian_tile(i, j)), (dxm, dym))
            SHIFTS[f'{year}_{i}_{j}'].append(int((LF[..., 2] > 0).sum())); CELLS[f'{year}_{i}_{j}'] = [[[round(float(LF[cy, cx, 0]), 1), round(float(LF[cy, cx, 1]), 1)] for cx in range(4)] for cy in range(4)]
            n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
            for k in range(1, n):
                if st[k, cv2.CC_STAT_AREA] * RES * RES < 30: continue
                (cx_, cy_), (rw, rh), _ = cv2.minAreaRect(np.argwhere(lab == k)[:, ::-1].astype(np.float32)) if st[k, cv2.CC_STAT_AREA] < 400000 else ((0, 0), (99, 99), 0)
                if min(rw, rh) * RES < 4.0 or st[k, cv2.CC_STAT_AREA] < 0.3 * rw * rh: continue   # lines of planned streets, lettering
                x, y, w, h = st[k, :4]
                cs, _ = cv2.findContours((lab[y:y + h, x:x + w] == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                ap = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 1.2, True).reshape(-1, 2)
                if len(ap) < 3: continue
                cy_, cx_ = min(int((y + h / 2) / 500), 3), min(int((x + w / 2) / 500), 3); ddx, ddy = LF[cy_, cx_, 0], LF[cy_, cx_, 1]
                polys.append([[round(X0 + i * TILE + (x + px) * RES + ddx, 1), round(Y1 - j * TILE - (y + py) * RES + ddy, 1)] for px, py in ap])
            if (i, j) in ((0, 1), (1, 2)):   # tiles with the barracks and the southern suburb: check images
                vis = bgr.copy(); vis[m > 0] = (vis[m > 0] * 0.4 + np.array([255, 0, 0]) * 0.6).astype(np.uint8)
                cv2.imencode('.jpg', cv2.resize(vis, (800, 800)))[1].tofile(os.path.join(OUT, f'_check_{year}_{i}_{j}.jpg'))
    out[year] = polys
    print(year, len(polys), 'footprints, shifts', {k: v for k, v in SHIFTS.items() if k.startswith(str(year))})
_old = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'hi_buildings.json')))['plans'] if len(sys.argv) > 1 else {}
out = {**{int(k): v for k, v in _old.items()}, **out}
json.dump({'crs': 'EPSG:5514', 'area': [X0, Y1 - NT * TILE, X0 + NT * TILE, Y1], 'res': RES, 'shifts': SHIFTS, 'cells': CELLS, 'plans': out},
          open(os.path.join(ROOT, 'data', 'historic', 'growth', 'hi_buildings.json'), 'w'))
