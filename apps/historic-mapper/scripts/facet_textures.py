"""Facet textures for the 3D building model from a georeferenced oblique view (bird's-eye
plate) — each visible wall of an extruded footprint becomes a rectified texture.

Camera model of the plate (approximate, per Janata et al. 2013 the plate is a high oblique
view from the south):
  * ground: homography H (map → image) fitted on control points;
  * vertical: an object of height h is drawn displaced upwards by h·k(x, y) image pixels,
    k = k0 · (local ground scale / ground scale at the reference object) — k0 is estimated from
    an object of known height (St Bartholomew's tower).
A wall (edge of a footprint, height h) maps to the quad
  B1 = H(a), B2 = H(b), T2 = B2 − (0, h·k), T1 = B1 − (0, h·k);
it is visible when its outward normal points towards the viewer (the map direction that the
plate draws as "down"). Visible walls are rectified to width = length·ppm, height = h·ppm.
Roofs: the top face (footprint lifted by h) is warped from the plate onto the footprint
shape (orthographic roof texture).

usage: python facet_textures.py project.json plate.jpg points.json out_dir [k0] [ppm]
points.json: [{"img": [x, y], "map": [X, Y]}, ...] (control points of the plate)
writes out_dir/<entity>_<edge>.png, out_dir/<entity>_roof.png and out_dir/facets.json
"""
import json, math, os, sys
import cv2
import numpy as np

def imread(p): return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)
def imwrite(p, img): ok, b = cv2.imencode('.png', img); b.tofile(p)

proj, plate_path, pts_path, out = sys.argv[1:5]
k0 = float(sys.argv[5]) if len(sys.argv) > 5 else 2.8
ppm = float(sys.argv[6]) if len(sys.argv) > 6 else 4.0
os.makedirs(out, exist_ok=True)
P = json.load(open(proj, encoding='utf-8')); plate = imread(plate_path); IH, IW = plate.shape[:2]
pts = json.load(open(pts_path, encoding='utf-8'))
Hm2i, _ = cv2.findHomography(np.array([p['map'] for p in pts], float), np.array([p['img'] for p in pts], float), 0)

def to_img(X, Y):
    q = Hm2i @ np.array([X, Y, 1.0]); return np.array([q[0] / q[2], q[1] / q[2]])
def ground_scale(X, Y):  # image px per metre (geometric mean of the local Jacobian)
    e = 1.0; a = to_img(X, Y); bx = to_img(X + e, Y); by = to_img(X, Y + e)
    u, v = bx - a, by - a; return math.sqrt(abs(u[0] * v[1] - u[1] * v[0]))
# reference: St Bartholomew
ref = next(e for e in P['entities'] if e['id'] == 'g1618-bartholomew')['geom']['coords'][0]
s_ref = ground_scale(*ref)
def k_at(X, Y): return k0 * ground_scale(X, Y) / s_ref
def view_dir(X, Y):  # map direction drawn as image "down" (towards the viewer)
    a = to_img(X, Y); J = np.stack([to_img(X + 1, Y) - a, to_img(X, Y + 1) - a], 1)
    d = np.linalg.solve(J, np.array([0.0, 1.0])); return d / np.linalg.norm(d)

# the plate is reliable inside the town: keep buildings inside the wall line (+ 25 m)
wall = next((e['geom']['coords'] for e in P['entities'] if e['id'] == 'g1618-wall'), None)
def near_town(X, Y):
    if not wall: return True
    inside = False
    for i in range(len(wall)):
        (x1, y1), (x2, y2) = wall[i], wall[i - 1]
        if (y1 > Y) != (y2 > Y) and X < (x2 - x1) * (Y - y1) / (y2 - y1) + x1: inside = not inside
    if inside: return True
    for i in range(len(wall)):
        a, b = wall[i], wall[(i + 1) % len(wall)]; vx, vy = b[0] - a[0], b[1] - a[1]; L = vx * vx + vy * vy or 1e-9
        t = max(0, min(1, ((X - a[0]) * vx + (Y - a[1]) * vy) / L))
        if math.dist((X, Y), (a[0] + t * vx, a[1] + t * vy)) < 25: return True
    return False

facets = []; n_vis = 0
for e in P['entities']:
    g = e.get('geom')
    if not g or g['type'] != 'Polygon' or e['type'] != 'building': continue
    if not near_town(sum(p[0] for p in g['coords']) / len(g['coords']), sum(p[1] for p in g['coords']) / len(g['coords'])): continue
    ring = g['coords']; h = float(e.get('height') or 8)
    # orientation: make ring counter-clockwise in map coordinates so that outward normal = right of edge
    area = sum(ring[i][0] * ring[(i + 1) % len(ring)][1] - ring[(i + 1) % len(ring)][0] * ring[i][1] for i in range(len(ring))) / 2
    if area < 0: ring = ring[::-1]
    cxm = sum(p[0] for p in ring) / len(ring); cym = sum(p[1] for p in ring) / len(ring)
    vd = view_dir(cxm, cym); k = k_at(cxm, cym)
    ent = {'entity': e['id'], 'walls': [], 'roof': None}
    for i in range(len(ring)):
        a, b = ring[i], ring[(i + 1) % len(ring)]
        L = math.dist(a, b)
        if L < 2.0: continue
        n = np.array([b[1] - a[1], -(b[0] - a[0])]) / L  # outward normal of a CCW ring
        if float(n @ vd) < 0.15: continue  # wall faces away from the viewer
        B1, B2 = to_img(*a), to_img(*b); T1, T2 = B1 - [0, h * k], B2 - [0, h * k]
        quad = np.float32([T1, T2, B2, B1])
        if (quad[:, 0].min() < 0) or (quad[:, 1].min() < 0) or (quad[:, 0].max() >= IW) or (quad[:, 1].max() >= IH): continue
        w, hh = max(2, int(L * ppm)), max(2, int(h * ppm))
        M = cv2.getPerspectiveTransform(quad, np.float32([[0, 0], [w, 0], [w, hh], [0, hh]]))
        tex = cv2.warpPerspective(plate, M, (w, hh), flags=cv2.INTER_LINEAR)
        img_w = float(np.linalg.norm(B2 - B1))  # drawn width in plate pixels (texture quality)
        fn = f'{e["id"]}_{i}.png'; imwrite(os.path.join(out, fn), tex)
        ent['walls'].append({'edge': i, 'a': a, 'b': b, 'height': h, 'texture': fn, 'facing': round(float(n @ vd), 2), 'plate_px': round(img_w, 1)})
        n_vis += 1
    # roof: top face lifted by h, warped onto the footprint (orthographic)
    top = np.float32([to_img(*p) - [0, h * k] for p in ring])
    if top[:, 0].min() >= 0 and top[:, 1].min() >= 0 and top[:, 0].max() < IW and top[:, 1].max() < IH and len(ring) >= 4:
        xs = [p[0] for p in ring]; ys = [p[1] for p in ring]; x0, y1 = min(xs), max(ys)
        dst = np.float32([[(p[0] - x0) * ppm, (y1 - p[1]) * ppm] for p in ring])
        Hr, _ = cv2.findHomography(top, dst, 0)
        if Hr is not None:
            W_ = max(2, int((max(xs) - x0) * ppm)); H_ = max(2, int((y1 - min(ys)) * ppm))
            roof = cv2.warpPerspective(plate, Hr, (W_, H_))
            mask = np.zeros((H_, W_), np.uint8); cv2.fillPoly(mask, [dst.astype(np.int32)], 255)
            rgba = cv2.cvtColor(roof, cv2.COLOR_BGR2BGRA); rgba[..., 3] = mask
            fn = f'{e["id"]}_roof.png'; imwrite(os.path.join(out, fn), rgba)
            ent['roof'] = {'texture': fn, 'origin': [x0, y1], 'ppm': ppm}
    if ent['walls'] or ent['roof']: facets.append(ent)
json.dump({'plate': os.path.basename(plate_path), 'k0': k0, 'ppm': ppm, 'buildings': facets}, open(os.path.join(out, 'facets.json'), 'w'), indent=0)
print(f'{len(facets)} buildings with facets, {n_vis} visible walls')
