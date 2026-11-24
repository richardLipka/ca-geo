"""3D buildings from points clicked on the vedute (editor/index.html, tab Vedute) and the fitted camera of the view.

Single-view reconstruction with the pinhole camera of veduta_fit.py (projects/plzen.json → manual/maps.json):
  * footprint corners (walls meeting the ground) are back-projected onto the ground plane (median terrain height of
    the old town in the model) → world corners; more than four become their minimum rotated rectangle;
  * each eave point lies on the vertical line through one of the footprint corners: for every corner the height whose
    projection is closest to the click is fitted (1D least squares, ≥ 2 m) and the best corner wins; median = eave;
  * each ridge point lies above the long axis of the footprint: position along the axis and height are fitted
    (2D least squares); the ridge height is the median (default roof: 0.6 × the footprint width);
  * buildings without footprint corners or on a veduta without a camera are reported and skipped.
Output manual/veduta_buildings.json: world rings (EPSG:5514), eave and ridge heights, years (from / to as entered,
else the year of the veduta ± 25); growth_model.py turns them into gable houses (or towers when the ridge is a point).

usage: python veduta_recon.py        (after editing; then growth_model.py)
"""
import glob, json, math, os
import numpy as np
from scipy.optimize import least_squares, minimize_scalar
from scipy.spatial.transform import Rotation
from shapely.geometry import MultiPoint, Point

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(APP, '..', '..'))
MAN = os.path.join(APP, 'manual')
IDX = json.load(open(os.path.join(MAN, 'maps.json'), encoding='utf-8'))
M = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'web', 'model.json'), encoding='utf-8'))
OX, OY = M['origin']
# ground plane: median terrain height of the model buildings within 400 m of the square
zs = [M['z'][b] for b in range(M['n']) if M['rings'][b] and math.hypot(sum(M['rings'][b][0::2]) / len(M['rings'][b][0::2]) / 10,
                                                                      sum(M['rings'][b][1::2]) / len(M['rings'][b][1::2]) / 10) < 400]
Z0 = float(np.median(zs)) if zs else 0.0


class Camera:
    def __init__(self, view, W, H):
        self.C = np.array(view['pos'], float); self.R = Rotation.from_quat(view['quat']).as_matrix()   # camera → world
        self.W, self.H = W, H; self.f = H / 2 / math.tan(math.radians(view['fov']) / 2)

    def project(self, X):                     # world (three.js: x east, y up, z south) → image px
        pc = (np.atleast_2d(X) - self.C) @ self.R
        z = np.minimum(pc[:, 2], -1e-3)
        return np.c_[self.W / 2 + self.f * pc[:, 0] / -z, self.H / 2 - self.f * pc[:, 1] / -z]

    def ground(self, u, v, y0):               # back-projection onto the plane y = y0
        d = self.R @ np.array([(u - self.W / 2) / self.f, -(v - self.H / 2) / self.f, -1.0])
        if abs(d[1]) < 1e-9: return None
        t = (y0 - self.C[1]) / d[1]
        return None if t <= 0 else self.C + t * d


def W3(x, y, h=0.0): return np.array([x - OX, Z0 + h, -(y - OY)])


out, skipped = [], []
for f in sorted(glob.glob(os.path.join(MAN, 'veduta_*.json'))):
    if f.endswith('veduta_buildings.json'): continue
    E = json.load(open(f, encoding='utf-8'))
    src = next((v for v in IDX['vedute'] if v['id'] == E['source']), None)
    if not src or not src.get('view') or not E.get('size'):
        skipped += [f"{E['source']}: no camera"] if E.get('buildings') else []; continue
    cam = Camera(src['view'], *E['size'])
    for k, b in enumerate(E['buildings']):
        P = b['pts']; name = b.get('name') or f"#{k + 1}"
        if len(P['foot']) < 3: skipped.append(f"{E['source']} {name}: fewer than 3 footprint corners"); continue
        g = [cam.ground(u, v, Z0) for u, v in P['foot']]
        if any(p is None for p in g): skipped.append(f"{E['source']} {name}: corner above the horizon"); continue
        xy = [(p[0] + OX, -p[2] + OY) for p in g]
        rect = list(MultiPoint(xy).minimum_rotated_rectangle.exterior.coords)[:4] if len(xy) != 4 else xy
        if MultiPoint(rect).convex_hull.area < 10: skipped.append(f"{E['source']} {name}: footprint < 10 m²"); continue
        # eave: vertical line through the nearest projected corner
        hs = []
        for u, v in P['eave']:   # the corner whose vertical line passes closest to the click (eaves at least 2 m up)
            best = min((minimize_scalar(lambda h, x=x, y=y: float(np.hypot(*(cam.project(W3(x, y, h))[0] - (u, v)))), bounds=(2.0, 90), method='bounded')
                        for x, y in rect), key=lambda r: r.fun)
            hs.append(best.x)
        e = sorted([(math.dist(rect[i], rect[(i + 1) % 4]), i) for i in range(4)])
        i0 = e[0][1]                                                    # a short edge: gable ends on the short sides
        q = [rect[i0], rect[(i0 + 1) % 4], rect[(i0 + 2) % 4], rect[(i0 + 3) % 4]]
        width = e[0][0]
        a0 = ((q[0][0] + q[1][0]) / 2, (q[0][1] + q[1][1]) / 2); a1 = ((q[2][0] + q[3][0]) / 2, (q[2][1] + q[3][1]) / 2)
        eave = float(np.median(hs)) if hs else 7.0
        rs = []
        for u, v in P['ridge']:
            def res(p):
                t, h = p; X = W3(a0[0] + t * (a1[0] - a0[0]), a0[1] + t * (a1[1] - a0[1]), h)
                return cam.project(X)[0] - (u, v)
            s = least_squares(res, [0.5, eave + 0.5 * width], bounds=([-0.1, 0.5], [1.1, 150]))
            rs.append(s.x[1])
        ridge = float(np.median(rs)) if rs else eave + 0.6 * width
        ridge = max(ridge, eave + 0.5)
        year = src.get('year') or 1618
        out.append({'source': E['source'], 'name': name, 'ring': [[round(x, 2), round(y, 2)] for x, y in q], 'eave': round(eave, 2), 'ridge': round(ridge, 2),
                    'tower': len(P['ridge']) == 1, 'from': b.get('from') or year - 25, 'to': b.get('to') or year + 25,
                    'n': {t: len(P[t]) for t in P}})
        print(f"{E['source']:18s} {name:20s} footprint {MultiPoint(q).convex_hull.area:7.1f} m²  eave {eave:5.1f} m  ridge {ridge:5.1f} m")
json.dump({'note': 'buildings reconstructed from the vedute (veduta_recon.py); heights above the ground', 'ground': Z0, 'buildings': out},
          open(os.path.join(MAN, 'veduta_buildings.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for s in skipped: print('  skipped:', s)
print(len(out), 'buildings →', os.path.join(MAN, 'veduta_buildings.json'))
