"""Render the entity model (extruded footprints, towers) as seen from a viewpoint with a
cylindrical panorama camera and put it under the veduta for comparison.

Column: x = cx + f·wrap(β − θ) (β = map bearing atan2(dY, dX)), row: y = y_h − |f|·atan((z − eye)/d).
The horizon row y_h is set so that the ground under the reference object lands on its row
in the veduta. Painter's algorithm, far to near.

usage: python render_view.py project.json veduta.jpg out.jpg X0 Y0 theta_rad f_px ref_entity_id ref_row [eye_m]
"""
import json, math, sys
import cv2
import numpy as np

def imread(p): return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)
def imwrite(p, img): ok, b = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 88]); b.tofile(p)

proj, ved_path, out = sys.argv[1:4]
X0, Y0, th, f = map(float, sys.argv[4:8]); ref_id = sys.argv[8]; ref_row = float(sys.argv[9])
eye = float(sys.argv[10]) if len(sys.argv) > 10 else 25.0
P = json.load(open(proj, encoding='utf-8')); ved = imread(ved_path); H, W = ved.shape[:2]; cx = W / 2
F = abs(f)
wrap = lambda a: (a + math.pi) % (2 * math.pi) - math.pi
def col(X, Y): return cx + f * wrap(math.atan2(Y - Y0, X - X0) - th)
ents = {e['id']: e for e in P['entities'] if e.get('geom')}
def anchor(e):
    c = e['geom']['coords']; return (sum(p[0] for p in c) / len(c), sum(p[1] for p in c) / len(c))
ref = ents[ref_id]; ra = anchor(ref); dref = math.dist(ra, (X0, Y0))
yh = ref_row + F * math.atan((0 - eye) / dref)  # horizon row
def row(z, d): return yh - F * math.atan((z - eye) / max(d, 1.0))

def inside(p, ring):
    c = False
    for i in range(len(ring)):
        (x1, y1), (x2, y2) = ring[i], ring[i - 1]
        if (y1 > p[1]) != (y2 > p[1]) and p[0] < (x2 - x1) * (p[1] - y1) / (y2 - y1) + x1: c = not c
    return c
# a building that contains a church landmark takes the church height
churches = [e for e in ents.values() if e['type'] == 'church' and e['geom']['type'] == 'Point']
items = []
for e in ents.values():
    g = e['geom']; h = e.get('height') or (8 if e['type'] == 'building' else 0)
    if g['type'] == 'Polygon' and e['type'] == 'building':
        for c in churches:
            if inside(c['geom']['coords'][0], g['coords']): h = max(h, c.get('height', h))
        items.append(('prism', e, g['coords'], h, math.dist(anchor(e), (X0, Y0))))
    elif g['type'] == 'Polygon' and e['type'] == 'wall':
        ring = g['coords']
        for i in range(len(ring)):
            a, b = ring[i], ring[(i + 1) % len(ring)]
            items.append(('wall', e, [a, b], h, math.dist(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), (X0, Y0))))
    elif g['type'] == 'Point' and e['type'] in ('tower', 'gate') and h:
        items.append(('tower', e, g['coords'][0], h, math.dist(g['coords'][0], (X0, Y0))))
items.sort(key=lambda it: -it[4])

img = np.full((H, W, 3), 245, np.uint8)
cv2.rectangle(img, (0, int(yh)), (W, H), (205, 225, 205), -1)
def shade(base, k): return tuple(int(c * k) for c in base)
COL = {'building': (120, 140, 200), 'wall': (150, 160, 170), 'tower': (110, 110, 160), 'gate': (60, 150, 230)}
for kind, e, geo, h, d in items:
    if kind == 'prism':
        ring = geo
        for i in range(len(ring)):  # walls of the prism, far edges first
            a, b = ring[i], ring[(i + 1) % len(ring)]
            da, db = math.dist(a, (X0, Y0)), math.dist(b, (X0, Y0))
            quad = np.array([[col(*a), row(0, da)], [col(*b), row(0, db)], [col(*b), row(h, db)], [col(*a), row(h, da)]], np.int32)
            if abs(quad[0, 0] - quad[1, 0]) > W / 2: continue
            cv2.fillPoly(img, [quad], shade(COL['building'], 0.85)); cv2.polylines(img, [quad], True, (70, 70, 90), 1)
        top = np.array([[col(*p), row(h, math.dist(p, (X0, Y0)))] for p in ring], np.int32)
        cv2.fillPoly(img, [top], COL['building'] if h < 20 else (90, 90, 190)); cv2.polylines(img, [top], True, (60, 60, 80), 1)
    elif kind == 'wall':
        a, b = geo; da, db = math.dist(a, (X0, Y0)), math.dist(b, (X0, Y0))
        quad = np.array([[col(*a), row(0, da)], [col(*b), row(0, db)], [col(*b), row(h, db)], [col(*a), row(h, da)]], np.int32)
        if abs(quad[0, 0] - quad[1, 0]) < W / 2: cv2.fillPoly(img, [quad], COL['wall']); cv2.polylines(img, [quad], True, (90, 90, 90), 1)
    else:
        x = col(*geo); w = max(3, F * 8 / d / 2); yb, yt = row(0, d), row(h, d); ys = row(h * 1.35, d)
        c = COL[e['type']]
        cv2.rectangle(img, (int(x - w), int(yt)), (int(x + w), int(yb)), c, -1)
        cv2.fillPoly(img, [np.array([[x - w, yt], [x + w, yt], [x, ys]], np.int32)], shade(c, 0.7))
        cv2.putText(img, e['name'].split(' (')[0][:26], (int(x - w), int(ys) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (40, 40, 40), 2, cv2.LINE_AA)
# St Bartholomew tower as tall marker if present as a point
for e in ents.values():
    if e['type'] == 'church' and e['geom']['type'] == 'Point' and e.get('height'):
        p = e['geom']['coords'][0]; d = math.dist(p, (X0, Y0)); x = col(*p)
        cv2.line(img, (int(x), int(row(0, d))), (int(x), int(row(e['height'], d))), (40, 40, 160), 3)
        cv2.putText(img, e['name'].split(' (')[0][:26], (int(x) + 6, int(row(e['height'], d))), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (40, 40, 160), 2, cv2.LINE_AA)
y0, y1 = int(max(0, yh - 0.35 * H)), int(min(H, yh + 0.2 * H))
both = np.vstack([ved[y0:y1], img[y0:y1]])
imwrite(out, both)
print(f'horizon row {yh:.0f}; crop rows {y0}-{y1}; {len(items)} items')
