"""Historický atlas měst ČR 21 – Plzeň, map 57 "Topografie středověké Nové Plzně (cca 1410)" (R. Široký,
M. Wasková): registered to the model and vectorised.

The map is a clean modern drawing (north up, scale bar), so its colours separate the layers:
pink = blocks of the inner town, pale green = blocks of the suburbs, red = town walls and gates,
grey = town and suburb moat, black = suburb walls and gates, magenta = churches, blue = rivers.
Registration: the area inside the red wall ring is aligned to the wall ring of the model by ECC
(translation, then affine) from a similarity start (centroids, area ratio, north up).

usage: python ham57.py        (paths relative to the repository)
reads  data/reference/hiu-atlas/pages/p090_300.png (atlas_pages / pymupdf render of page 90)
writes data/historic/growth/ham57_map.json (not versioned: vectorised from a map under copyright) and data/historic/growth/fort/_reg_57.jpg
"""
import json, os
import cv2
import numpy as np
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = json.load(open(os.path.join(ROOT, 'apps', 'historic-mapper', 'projects', 'plzen.json'), encoding='utf-8'))
ENT = {e['id']: e for e in P['entities']}
WALL = Polygon(ENT['g1618-wall']['geom']['coords'])
im = cv2.imdecode(np.fromfile(os.path.join(ROOT, 'data', 'reference', 'hiu-atlas', 'pages', 'p090_300.png'), np.uint8), 1)
H0, W0 = im.shape[:2]
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
Hh, S, V = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
frame = np.zeros((H0, W0), bool); frame[180:4650, 160:3350] = True       # map field (no title, legend box excluded below)
frame[180:1000, 160:1680] = False
pink = frame & (Hh >= 145) & (Hh <= 178) & (S >= 22) & (S <= 95) & (V > 195)
green = frame & (Hh >= 22) & (Hh <= 48) & (S >= 40) & (S <= 120) & (V > 190)
red = frame & ((Hh < 8) | (Hh > 170)) & (S > 140) & (V > 140)
grey = frame & (S < 18) & (V > 175) & (V < 238)
black = frame & (V < 90)
river = frame & (Hh >= 95) & (Hh <= 125) & (S > 35) & (V > 170)
magenta = frame & (Hh >= 135) & (Hh <= 165) & (S > 80) & (V > 100)
k3 = np.ones((3, 3), np.uint8)


def polys(mask, min_area, eps=2.0):
    m = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, k3)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for i, c in enumerate(cs):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < min_area: continue
        ap = cv2.approxPolyDP(c, eps, True).reshape(-1, 2)
        if len(ap) >= 3: out.append(ap.astype(float))
    return out


# ---- town interior: the blocks of the inner town closed over the streets, grown to the wall line ----
pm = cv2.morphologyEx(pink.astype(np.uint8), cv2.MORPH_OPEN, k3)
pm = cv2.morphologyEx(pm, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81)))
n, lab, st, cen = cv2.connectedComponentsWithStats(pm, 8)
big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
town = cv2.dilate((lab == big).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
cs, _ = cv2.findContours(town, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
ring = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 3.0, True).reshape(-1, 2).astype(float)
rp = Polygon(ring)
print('town interior px²', int(rp.area), 'centroid', rp.centroid)
s = np.sqrt(WALL.area / rp.area)
A0 = np.array([[s, 0, WALL.centroid.x - s * rp.centroid.x], [0, -s, WALL.centroid.y + s * rp.centroid.y]])
print('similarity scale m/px', round(s, 4))
# ECC on a reduced canvas around the town
x0, y0 = int(rp.bounds[0]) - 600, int(rp.bounds[1]) - 600
x1, y1 = int(rp.bounds[2]) + 600, int(rp.bounds[3]) + 600
sc = 0.25
tw, th = int((x1 - x0) * sc), int((y1 - y0) * sc)
T0 = np.array([[sc, 0, -x0 * sc], [0, sc, -y0 * sc]])       # page px → canvas
Ai0 = cv2.invertAffineTransform(A0)
ref = np.zeros((th, tw), np.uint8)
wp = np.c_[np.array(WALL.exterior.coords), np.ones(len(WALL.exterior.coords))] @ Ai0.T
cv2.fillPoly(ref, [np.round(np.c_[wp, np.ones(len(wp))] @ T0.T).astype(np.int32)], 255)
mp = np.zeros((th, tw), np.uint8)
cv2.fillPoly(mp, [np.round(np.c_[ring, np.ones(len(ring))] @ T0.T).astype(np.int32)], 255)
warp = np.eye(2, 3, dtype=np.float32); cc = 0
for motion, sig in ((cv2.MOTION_TRANSLATION, 10), (cv2.MOTION_AFFINE, 6), (cv2.MOTION_AFFINE, 3)):
    t = lambda m: cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), sig)
    cc, warp = cv2.findTransformECC(t(ref), t(mp), warp, motion, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 500, 1e-7), None, 5)
# canvas: ref(x) ≈ mp(warp x); page = T0^-1 canvas; map = A0 page
T0i = cv2.invertAffineTransform(T0)
M3 = lambda a: np.r_[a, [[0, 0, 1]]]
A = (M3(A0) @ M3(T0i) @ M3(cv2.invertAffineTransform(warp)) @ M3(T0))[:2]
tr = lambda pts: np.c_[np.asarray(pts, float), np.ones(len(pts))] @ A.T
iou = Polygon(tr(ring)).intersection(WALL).area / Polygon(tr(ring)).union(WALL).area
print('ECC', round(cc, 3), 'ring IoU', round(iou, 3))


def feat(polylist, kind, minA=0.0):
    out = []
    for p in polylist:
        q = tr(p)
        pg = Polygon(q)
        if not pg.is_valid: pg = pg.buffer(0)
        if pg.area < minA: continue
        out.append({'kind': kind, 'poly': [[round(a, 1), round(b, 1)] for a, b in (pg.exterior.coords if pg.geom_type == 'Polygon' else max(pg.geoms, key=lambda g: g.area).exterior.coords)]})
    return out


feats = []
feats += feat(polys(pink & ~red, 400), 'inner_block', 80)
feats += feat(polys(green, 600), 'suburb_block', 150)
feats += feat(polys(grey, 3000, 3.0), 'moat', 400)
feats += feat(polys(magenta, 150), 'church', 30)
feats += feat(polys(river, 2500, 2.5), 'river', 300)
# suburb walls: long thin black components outside the town
bm = cv2.morphologyEx(black.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(bm, 8)
lines = []
for i in range(1, n):
    x, y, w, h, a = st[i]
    if max(w, h) < 250 or a > 0.12 * w * h: continue          # long and thin (not text, not the frame)
    sub = (lab[y:y + h, x:x + w] == i).astype(np.uint8)
    sk = cv2.ximgproc.thinning(sub * 255) if hasattr(cv2, 'ximgproc') else sub * 255
    cs, _ = cv2.findContours(sk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=len).reshape(-1, 2)
    ap = cv2.approxPolyDP(c.astype(np.int32), 3.0, False).reshape(-1, 2) + [x, y]
    q = tr(ap)
    L = LineString(q)
    if L.length < 80 or WALL.buffer(25).contains(L): continue
    lines.append({'kind': 'suburb_wall', 'line': [[round(a, 1), round(b, 1)] for a, b in q]})
feats += lines
cnt = {}
for f in feats: cnt[f['kind']] = cnt.get(f['kind'], 0) + 1
print(cnt)
field = [[round(a, 1), round(b, 1)] for a, b in tr([(160, 1000), (3350, 1000), (3350, 4650), (160, 4650)])]
json.dump({'crs': 'EPSG:5514', 'field': field, 'source': 'HAM ČR 21 Plzeň (2009), map 57 (R. Široký, M. Wasková), registered by ham57.py',
           'affine': np.round(A, 6).tolist(), 'ecc': round(float(cc), 3), 'iou_ring': round(iou, 3), 'features': feats},
          open(os.path.join(ROOT, 'data', 'historic', 'growth', 'ham57_map.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# check image: page with the model wall (blue) and the vectorised layers
chk = im.copy()
Ai = cv2.invertAffineTransform(A)
to_px = lambda pts: np.round(np.c_[np.asarray(pts, float), np.ones(len(pts))] @ Ai.T).astype(np.int32)
cv2.polylines(chk, [to_px(WALL.exterior.coords)], True, (255, 60, 0), 6)
col = {'river': (200, 120, 0), 'inner_block': (180, 0, 180), 'suburb_block': (0, 140, 0), 'moat': (90, 90, 90), 'church': (200, 0, 120)}
for f in feats:
    if 'poly' in f: cv2.polylines(chk, [to_px(f['poly'])], True, col[f['kind']], 3)
    else: cv2.polylines(chk, [to_px(f['line'])], False, (0, 0, 255), 4)
cv2.imencode('.jpg', cv2.resize(chk[int(rp.bounds[1]) - 1500:int(rp.bounds[3]) + 1200, 160:3350], None, fx=0.32, fy=0.32))[1].tofile(
    os.path.join(ROOT, 'data', 'historic', 'growth', 'fort', '_reg_57.jpg'))
