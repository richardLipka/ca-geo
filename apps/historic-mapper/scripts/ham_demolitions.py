"""Demolished historic buildings of central Plzeň from the Historický atlas měst ČR 21 – Plzeň (HIÚ AV ČR,
2009), map 65 "Rozsah demolic historické zástavby centrální oblasti Plzně od roku 1942" (P. Domanický):
orange = demolitions of historic buildings 1945–2008, black dots = buildings destroyed or heavily damaged
by the air raids 1942–45.

The atlas page is rendered at 300 dpi, registered to the RÚIAN building footprints (initial similarity
from the square and the scale bar, refined by ECC affine alignment of the building masks), and the
orange polygons and black dots are converted to EPSG:5514.

usage: python ham_demolitions.py            (paths relative to the repository)
writes data/historic/growth/ham65_demolitions.json and _ham65_check.jpg
"""
import json, math, os
import cv2
import numpy as np
import pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PDF = os.path.join(ROOT, 'data', 'reference', 'hiu-atlas', 'atlas.pdf')
OUT = os.path.join(ROOT, 'data', 'historic', 'growth')
DPI = 300
SQUARE = (-822396.8, -1069689.4)

page = pymupdf.open(PDF)[95]  # page 96 = map 65
pix = page.get_pixmap(dpi=DPI)
im = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3][..., ::-1].copy()
H, W = im.shape[:2]
k = 0.45 * 200 / DPI  # preview (45 % of a 200-dpi render) pixels per 300-dpi pixel
# map frame (inside the neat line) and legend box, in 300-dpi pixels
x0, y0, x1, y1 = int(48 / k), int(108 / k), int(1000 / k), int(1375 / k)
legend = (int(543 / k), int(1113 / k), int(1000 / k), int(1375 / k))
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
Hh, S, V = hsv[..., 0].astype(int) * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
valid = np.zeros((H, W), bool); valid[y0:y1, x0:x1] = True
valid[legend[1]:legend[3], legend[0]:legend[2]] = False
orange = valid & (Hh >= 4) & (Hh < 30) & (S > 0.55) & (V > 0.7)
grey = valid & (S < 0.08) & (V > 0.68) & (V < 0.86)
dark = valid & (V < 0.25)

# ---- initial similarity: square ("náměstí") and scale bar (1 km) ----
sq_px = (560 / k, 735 / k)
m_per_px = 1000 / ((940 - 590) / k)


def px2map(px, py, A):
    return A[0, 0] * px + A[0, 1] * py + A[0, 2], A[1, 0] * px + A[1, 1] * py + A[1, 2]


A0 = np.array([[m_per_px, 0, SQUARE[0] - m_per_px * sq_px[0]], [0, -m_per_px, SQUARE[1] + m_per_px * sq_px[1]]])

# ---- RÚIAN mask in the page pixel frame (via the initial transform) ----
F = json.load(open(os.path.join(ROOT, 'data', 'reference', 'plzen-ruian', 'buildings.geojson'), encoding='utf-8'))['features']
inv = cv2.invertAffineTransform(A0)
ru = np.zeros((H, W), np.uint8)
for f in F:
    ring = np.array(f['geometry']['coordinates'][0], np.float64)
    p = np.c_[ring, np.ones(len(ring))] @ inv.T
    if p[:, 0].max() < 0 or p[:, 1].max() < 0 or p[:, 0].min() > W or p[:, 1].min() > H: continue
    cv2.fillPoly(ru, [np.round(p).astype(np.int32)], 255)
mp = ((grey | orange) * 255).astype(np.uint8)
# coarse-to-fine ECC: translation on a 1/4 image, then affine on 1/2 and full resolution
mask = np.zeros((H, W), np.uint8); mask[int(H * 0.30):int(H * 0.68), int(W * 0.12):int(W * 0.88)] = 255  # town centre, no legend / title
warp = np.eye(2, 3, dtype=np.float32); cc = 0
for scale, motion, sig in ((0.25, cv2.MOTION_TRANSLATION, 6), (0.5, cv2.MOTION_AFFINE, 4), (1.0, cv2.MOTION_AFFINE, 3)):
    r = lambda m: cv2.resize(m, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    t = lambda m: cv2.GaussianBlur(r(m).astype(np.float32) / 255, (0, 0), sig)
    wsc = warp.copy(); wsc[:, 2] *= scale
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 400, 1e-7)
    cc, wsc = cv2.findTransformECC(t(ru), t(mp), wsc, motion, crit, r(mask), 5)
    warp = wsc.copy(); warp[:, 2] /= scale
    print(' ECC', scale, round(cc, 3), warp.round(4).tolist())
print('ECC correlation', round(cc, 3))
# warp maps RÚIAN-frame pixels → page pixels; page → map = A0 ∘ inverse(warp)
Wi = cv2.invertAffineTransform(warp)
A = np.r_[A0, [[0, 0, 1]]] @ np.r_[Wi, [[0, 0, 1]]]
A = A[:2]

# ---- check image ----
chk = im.copy()
ru2 = cv2.warpAffine(ru, warp, (W, H), flags=cv2.INTER_NEAREST)
cnts, _ = cv2.findContours(ru2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(chk, cnts, -1, (255, 0, 0), 2)
cv2.imencode('.jpg', cv2.resize(chk[y0:y1, x0:x1], None, fx=0.4, fy=0.4))[1].tofile(os.path.join(OUT, '_ham65_check.jpg'))

# ---- orange polygons → map coordinates ----
feats = []
om = cv2.morphologyEx(orange.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(om, 8)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] * (m_per_px ** 2) < 25: continue
    xs, ys, w, h = st[i, :4]
    sub = (lab[ys:ys + h, xs:xs + w] == i).astype(np.uint8)
    cs, _ = cv2.findContours(sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    ap = cv2.approxPolyDP(c, 1.5, True).reshape(-1, 2)
    if len(ap) < 3: continue
    ring = [list(map(lambda v: round(v, 2), px2map(xs + px, ys + py, A))) for px, py in ap]
    ring.append(ring[0])
    feats.append({'type': 'Feature', 'properties': {'kind': 'demolished_1945_2008'}, 'geometry': {'type': 'Polygon', 'coordinates': [ring]}})
# ---- black dots (air raids 1942-45): filled circles, small = one building, large = group ----
dm = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
n, lab, st, cen = cv2.connectedComponentsWithStats(dm, 8)
for i in range(1, n):
    w, h, a = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT], st[i, cv2.CC_STAT_AREA]
    if not (0.75 < w / max(h, 1) < 1.33) or a < 0.6 * math.pi * (w / 2) ** 2 or w < 18: continue
    X, Y = px2map(*cen[i], A)
    feats.append({'type': 'Feature', 'properties': {'kind': 'bombed_group' if w > 34 else 'bombed', 'radius_m': round(w / 2 * m_per_px, 1)},
                  'geometry': {'type': 'Point', 'coordinates': [round(X, 2), round(Y, 2)]}})
json.dump({'type': 'FeatureCollection', 'crs': 'EPSG:5514', 'source': 'HAM ČR 21 Plzeň (2009), map 65 (P. Domanický); registered to RÚIAN, ECC ' + str(round(cc, 3)),
           'features': feats}, open(os.path.join(OUT, 'ham65_demolitions.json'), 'w', encoding='utf-8'))
print('demolished polygons', sum(1 for f in feats if f['properties']['kind'].startswith('demol')), 'bomb dots', sum(1 for f in feats if f['properties']['kind'].startswith('bomb')))
