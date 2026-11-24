"""Fit the draughtsman's camera of the vedute to the growth model and estimate tower / gate heights.

For each view with links to model objects (project annotations: drawing point → entity id) a pinhole camera
(position, rotation, focal length) and the unknown heights of the linked towers and gates are estimated
together by robust least squares (scipy, soft-L1): image residuals of the linked tops plus a prior that keeps
each height near its present value (σ = 35 %). Heights of the church towers taken from the city 3D model
(St Bartholomew, Franciscan church, Dominican copy, water tower) are fixed and anchor the scale.
The estimates of all views are combined (weighted by their image fit) and written to veduta_heights.json,
which growth_model.py applies to the towers and gates of the model c. 1320–1850; the fitted cameras are
saved as the views of the sources in projects/plzen.json (for the projection of the drawing in growth3d).

usage: python veduta_fit.py        (after growth_model.py; paths relative to the repository)
"""
import json, math, os
import numpy as np
from PIL import Image
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PROJ = os.path.join(ROOT, 'apps', 'historic-mapper', 'projects', 'plzen.json')
P = json.load(open(PROJ, encoding='utf-8'))
M = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'web', 'model.json'), encoding='utf-8'))
IDX = {k: i for i, k in enumerate(M['ids'])}
ENT = {e['id']: e for e in P['entities']}
FIXED = {'g1618-bartholomew', 'g1618-franciscan', 'g1618-dominican', 'g1618-water_tower'}
# initial viewpoints (as VIEW_DEFAULTS in growth3d.ts): direction from the town to the viewer (deg from north), distance, height, fov
INIT = {'te-1618': (180, 900, 750, 45), 'ottheinrich-1536': (205, 1600, 40, 38)}


def centre(b):
    r = M['rings'][b]
    return sum(r[0::2]) / (len(r) / 2) / 10, sum(r[1::2]) / (len(r) / 2) / 10


def project(par, X, W, H):
    C, rv, lf = par[:3], par[3:6], par[6]
    R = Rotation.from_rotvec(rv).as_matrix()          # camera → world
    pc = (X - C) @ R                                    # world → camera (three.js: looks along −Z, up +Y)
    f = math.exp(lf)
    z = np.minimum(pc[:, 2], -1.0)
    return np.c_[W / 2 + f * pc[:, 0] / -z, H / 2 - f * pc[:, 1] / -z]


def look_rotvec(C, T):
    fwd = (T - C) / np.linalg.norm(T - C)
    zc = -fwd; xc = np.cross([0, 1, 0], zc); xc /= np.linalg.norm(xc); yc = np.cross(zc, xc)
    return Rotation.from_matrix(np.c_[xc, yc, zc]).as_rotvec()


est = {}
views = {}
bad = set()
for sid, (az, dist, hgt, fov) in INIT.items():
    src = next(s for s in P['sources'] if s['id'] == sid)
    W, H = Image.open(os.path.join(ROOT, 'data', 'historic', 'sources', os.path.basename(src['file']))).size
    links = [a for a in P['annotations'] if a['sourceId'] == sid and a.get('entityId') in IDX]
    if len(links) < 5: continue
    ents = sorted({a['entityId'] for a in links})
    free = [e for e in ents if e not in FIXED]
    base = {}
    for e in ents:
        b = IDX[e]; x, y = centre(b)
        h_prior = float(ENT.get(e, {}).get('height') or M['h1'][b]) if e not in FIXED else M['h1'][b]   # prior: the 1618 model, not an earlier estimate
        base[e] = (x, M['z'][b], -y, h_prior)
    a = math.radians(az)
    C0 = np.array([math.sin(a) * dist, base[ents[0]][1] + hgt, -math.cos(a) * dist])
    T0 = np.array([0.0, 30.0, 0.0])
    p0 = np.r_[C0, look_rotvec(C0, T0), math.log(H / 2 / math.tan(math.radians(fov) / 2)), [base[e][3] for e in free]]

    def resid(p):
        hs = dict(zip(free, p[7:]))
        X = np.array([[base[a['entityId']][0], base[a['entityId']][1] + hs.get(a['entityId'], base[a['entityId']][3]), base[a['entityId']][2]] for a in links])
        obs = np.array([a['img'] for a in links], float)
        r = (project(p, X, W, H) - obs).ravel() / (0.01 * H)       # in % of the image height
        prior = [(hs[e] - base[e][3]) / (0.35 * base[e][3]) for e in free]
        return np.r_[r, prior]
    # bounds: the viewer within 6 km and 3 km up, field of view at least 8° (a plate seen from infinity
    # would make the camera degenerate); heights 0.5–2 × their present value
    lfmax = math.log(H / 2 / math.tan(math.radians(4)))
    lo = np.r_[[-6000, 0, -6000], [-np.pi] * 3, 0, [0.5 * base[e][3] for e in free]]
    hi = np.r_[[6000, 3000, 6000], [np.pi] * 3, lfmax, [2.0 * base[e][3] for e in free]]
    p0 = np.clip(p0, lo + 1e-6, hi - 1e-6)
    sol = least_squares(resid, p0, loss='soft_l1', f_scale=2.0, max_nfev=4000, bounds=(lo, hi))
    res = resid(sol.x)[:2 * len(links)].reshape(-1, 2) * 0.01 * H
    rms = float(np.sqrt((res ** 2).sum(1).mean()))
    hs = dict(zip(free, sol.x[7:]))
    print(f'{sid}: {len(links)} links, image RMS {rms:.1f} px ({100 * rms / H:.1f} % of height)')
    good = rms / H < 0.05   # views the camera model cannot explain (e.g. the widened Ottheinrich town) give no heights
    for e in free:
        print(f'   {e:22s} {base[e][3]:6.1f} → {hs[e]:6.1f} m' + ('' if good else '   (not used: poor fit)'))
        if good and e != 'g1618-wall': est.setdefault(e, []).append((float(hs[e]), 1.0 / max(rms / H, 0.005)))
    if not good:
        bad.add(sid); continue
    C = sol.x[:3]; R = Rotation.from_rotvec(sol.x[3:6])
    q = R.as_quat()                                       # x, y, z, w (three.js order)
    fwd = R.apply([0, 0, -1])
    views[sid] = {'pos': [round(float(v), 2) for v in C], 'target': [round(float(v), 2) for v in C + 300 * fwd],
                  'fov': round(2 * math.degrees(math.atan(H / 2 / math.exp(sol.x[6]))), 2), 'year': src.get('depicted', [1618])[0],
                  'quat': [round(float(v), 6) for v in q], 'aspect': round(W / H, 4), 'fit': {'rms': round(rms, 1), 'n': len(links), 'by': 'veduta_fit.py'}}
heights = {}
for e, lst in est.items():
    h0 = float(ENT.get(e, {}).get('height') or M['h1'][IDX[e]])
    h = sum(v * w for v, w in lst) / sum(w for _, w in lst)
    heights[e] = round(float(min(max(h, 0.7 * h0), 1.5 * h0)), 1)
json.dump({'note': 'tower / gate heights estimated from the vedute (veduta_fit.py); clamped to 0.7–1.5 × the previous height',
           'heights': heights, 'views': {k: v['fit'] for k, v in views.items()}}, open(os.path.join(HERE, 'veduta_heights.json'), 'w', encoding='utf-8'), indent=1)
for s in P['sources']:
    if s['id'] in views: s['view'] = views[s['id']]
    elif s['id'] in bad and s.get('view', {}).get('fit', {}).get('by') == 'veduta_fit.py': s.pop('view')
json.dump(P, open(PROJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('heights', heights)
