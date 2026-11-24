"""Synthetic views of the town from the direction of every veduta, and the mapping of the model's buildings onto
the elements of the drawing (best effort, automatic).

For each veduta (projects/plzen.json sources of kind birdseye / panorama) a pinhole camera is estimated from
points of model objects in the drawing:
  * Theatrum Europaeum 1618 and Ottheinrich 1536: the links of the project (annotations; as veduta_fit.py);
  * the other plates: scripts/veduta_points.json (copies of the 1618 plate: links transferred by SIFT + local
    homographies; Keller, Hogenberg: identified by eye);
  * panoramas (Willenberg, Hollar): the direction is searched (every 3°, three distances and heights): the St
    Bartholomew tower is matched to its drawn tower and the other prominent drawn towers to the nearest projected
    landmarks (chamfer distance in image columns after fitting the field of view); the best direction is refined
    with the matched points.
Robust least squares (soft-L1) from several starting directions; the fit error is reported, poor fits are kept
and labelled (the draughtsmen distorted the towns; the cameras are approximate by nature).

Writes scripts/veduta_views.json (cameras: three.js pos, quaternion, vertical fov, aspect; error; year) and
data/historic/growth/shots/vedmap_<id>.jpg: the veduta with the model projected into it (outlines of the
buildings standing in the veduta's year, landmarks with their names, the clicked points and their residuals).
The synthetic renderings are made by the viewer (growth3d __g3d.snap with the camera of veduta_views.json) and
joined under the mapping by --compose:

usage: python veduta_views.py                  fit the cameras, write the mapping images
       python veduta_views.py --compose RUN    join data/historic/growth/video/RUN/f_<k>.jpg (k = order in the json)
                                               under the mapping → shots/vedview_<id>.jpg
"""
import json, math, os, sys
import cv2
import numpy as np
from PIL import Image
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P = json.load(open(os.path.join(ROOT, 'apps', 'historic-mapper', 'projects', 'plzen.json'), encoding='utf-8'))
M = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'web', 'model.json'), encoding='utf-8'))
IDX = {k: i for i, k in enumerate(M['ids'])}
ENT = {e['id']: e for e in P['entities']}
SHOTS = os.path.join(ROOT, 'data', 'historic', 'growth', 'shots'); os.makedirs(SHOTS, exist_ok=True)
OUTJ = os.path.join(HERE, 'veduta_views.json')
PTS = json.load(open(os.path.join(HERE, 'veduta_points.json'), encoding='utf-8'))['sources']
NAMES = {'g1618-bartholomew': 'sv. Bartoloměj', 'g1618-franciscan': 'františkáni', 'g1618-dominican': 'dominikáni',
         'g1618-water_tower': 'vodárenská věž', 'g1618-gate_prague': 'Pražská brána', 'g1618-gate_reich': 'Říšská brána',
         'g1618-gate_litice': 'Litická brána', 'g1618-gate_north': 'Saská brána', 'g1618-st_nicholas': 'sv. Mikuláš',
         'g1618-all_saints': 'Všech svatých'}


def centre(b):
    r = M['rings'][b]; return sum(r[0::2]) / (len(r) / 2) / 10, sum(r[1::2]) / (len(r) / 2) / 10


def W3(b, frac):           # world point of model object b at a fraction of its height (three.js axes)
    x, y = centre(b); return np.array([x, M['z'][b] + frac * M['h1'][b], -y])


def visible(b, y):
    if M['from'][b] > y or M['to'][b] <= y: return False
    g = M['gaps'][b] or []
    return not any(g[k] <= y < g[k + 1] for k in range(0, len(g) - 1, 2))


def project(par, X, W, H):
    C, R, f = par[:3], Rotation.from_rotvec(par[3:6]).as_matrix(), math.exp(par[6])
    fx = f * math.exp(par[7]) if len(par) > 7 else f      # panoramas: the town drawn wider than a camera sees it
    pc = (np.atleast_2d(X) - C) @ R
    z = np.minimum(pc[:, 2], -1.0)
    return np.c_[W / 2 + fx * pc[:, 0] / -z, H / 2 - f * pc[:, 1] / -z], pc[:, 2] < -1.0


def look(C, T):
    fwd = (T - C) / np.linalg.norm(T - C); zc = -fwd; xc = np.cross([0, 1, 0], zc); xc /= np.linalg.norm(xc); yc = np.cross(zc, xc)
    return Rotation.from_matrix(np.c_[xc, yc, zc]).as_rotvec()


Z0 = float(np.median([M['z'][b] for b in range(M['n']) if math.hypot(*centre(b)) < 400]))
CTR = np.array([0.0, Z0 + 15, 0.0])


def fit(X, obs, W, H, kind, az_list=None, starts=(), wt=None):
    wt = np.ones(len(obs)) if wt is None else np.asarray(wt, float)
    """robust pinhole fit from several starting directions; returns params, rms px"""
    best = None
    dists, hgts = ((900, 1600, 3000), (300, 900, 1800)) if kind == 'birdseye' else ((800, 1500, 2800), (15, 60, 150))
    inits = list(starts)
    for az in (az_list if az_list is not None else range(0, 360, 30)):
        for d in dists:
            for hg in hgts:
                a = math.radians(az); C0 = np.array([math.sin(a) * d, Z0 + hg, -math.cos(a) * d])
                inits.append(np.r_[C0, look(C0, CTR), math.log(H / 2 / math.tan(math.radians(40) / 2))] if kind == 'birdseye'
                             else np.r_[C0, look(C0, CTR), math.log(H / 2 / math.tan(math.radians(40) / 2)), math.log(1.5)])
    for p0 in inits:
                lo = np.r_[[-8000, Z0 - 20, -8000], [-np.pi] * 3, math.log(H / 2 / math.tan(math.radians(70) / 2)), [math.log(0.7)] * (len(p0) - 7)]
                hi = np.r_[[8000, Z0 + 4000, 8000], [np.pi] * 3, math.log(H / 2 / math.tan(math.radians(3) / 2)), [math.log(6.0)] * (len(p0) - 7)]
                def res(p):
                    q, front = project(p, X, W, H)
                    return np.r_[(((q - obs) / (0.01 * H)) * wt[:, None]).ravel(), (~front) * 50.0]
                try:
                    s = least_squares(res, np.clip(p0, lo + 1e-6, hi - 1e-6), bounds=(lo, hi), loss='soft_l1', f_scale=2.0, max_nfev=600)
                except Exception:
                    continue
                q, front = project(s.x, X, W, H)
                rms = float(np.sqrt(((q - obs) ** 2).sum(1).mean())) if front.all() else 1e9
                if best is None or rms < best[1]: best = (s.x, rms)
    return best


LMK = [k for k in ('g1618-bartholomew', 'g1618-franciscan', 'g1618-dominican', 'g1618-water_tower', 'g1618-gate_prague', 'g1618-gate_reich',
                   'g1618-gate_litice', 'g1618-gate_north', 'g1618-st_nicholas', 'g1618-all_saints') if k in IDX]


def panorama(spec, W, H, year):
    """direction search: Bartholomew on its tower, other drawn towers on the nearest projected landmarks"""
    b0 = IDX['g1618-bartholomew']; cand = [IDX[k] for k in LMK if k != 'g1618-bartholomew' and visible(IDX[k], year)]
    tw = np.array(spec['towers'], float); bu = np.array(spec['bart'], float)
    best = None
    for az in range(0, 360, 3):
        for d in (900, 1600, 2800):
            for hg in (20, 60):
                a = math.radians(az); C = np.array([math.sin(a) * d, Z0 + hg, -math.cos(a) * d])
                rv = look(C, CTR)
                p = np.r_[C, rv, 0.0]
                Xc = np.array([W3(b, 1.0) for b in cand]); Xb = W3(b0, 1.0)
                R = Rotation.from_rotvec(rv).as_matrix()
                pc = (np.vstack([Xb, Xc]) - C) @ R
                if (pc[:, 2] > -1).any(): continue
                xs = pc[:, 0] / -pc[:, 2]                      # normalised image columns (f = 1)
                # scale: the drawn towers' spread over the projected spread; offset: Bartholomew on its tower
                for fsc in np.linspace(0.3, 3.0, 28) * W:
                    u = W / 2 + fsc * (xs - xs[0]) + (bu[0] - W / 2)
                    dd = np.abs(tw[:, 0][:, None] - u[None, 1:])
                    cost = float(np.minimum(dd.min(1), 0.06 * W).mean()) / W
                    if best is None or cost < best[0]:
                        best = (cost, az, d, hg, fsc, [cand[j] for j in dd.argmin(1)], dd.min(1))
    cost, az, d, hg, fsc, match, dmin = best
    X = [W3(b0, 1.0), W3(b0, 0.0)]; obs = [bu, [bu[0], spec['ground_row']]]; used = [('g1618-bartholomew', 'top'), ('g1618-bartholomew', 'ground')]
    for t, b, dm in zip(tw, match, dmin):
        if dm < 0.06 * W: X.append(W3(b, 1.0)); obs.append(t); used.append((M['ids'][b], 'top'))
    par, rms = fit(np.array(X), np.array(obs, float), W, H, 'panorama', az_list=[az])
    return par, rms, used, np.array(obs, float), az


def view_of(par, W, H):
    C, R, f = par[:3], Rotation.from_rotvec(par[3:6]), math.exp(par[6])
    st = math.exp(par[7]) if len(par) > 7 else 1.0           # render W / stretch wide, then stretch to the sheet
    return {'pos': [round(float(v), 2) for v in C], 'quat': [round(float(v), 6) for v in R.as_quat()],
            'fov': round(2 * math.degrees(math.atan(H / 2 / f)), 3), 'aspect': round(W / H, 4), 'size': [W, H], 'stretch': round(st, 3)}


def mapping_image(sid, par, W, H, year, pts, used, title):
    im = cv2.cvtColor(np.array(Image.open(os.path.join(ROOT, 'data', 'historic', 'sources', f'{sid}.jpg')).convert('RGB')), cv2.COLOR_RGB2BGR)
    ov = im.copy(); OX, OY = M['origin']
    C = par[:3]
    order = sorted([b for b in range(M['n']) if visible(b, year + 0.01) and M['classes'][M['cls'][b]] not in ('moat', 'ditch') and math.hypot(*centre(b)) < 1600],
                   key=lambda b: -np.linalg.norm(W3(b, 0) - C))
    th = max(1, round(H / 900))
    for b in order:                         # outlines of the model buildings (ground and top rings), far to near
        r = M['rings'][b]; ring = [(r[k] / 10, r[k + 1] / 10) for k in range(0, len(r), 2)]
        if len(ring) > 60: ring = ring[::max(1, len(ring) // 60)]
        g = np.array([[x, M['z'][b], -y] for x, y in ring]); t = g + [0, M['h1'][b], 0]
        q0, f0 = project(par, g, W, H); q1, f1 = project(par, t, W, H)
        if not (f0.all() and f1.all()): continue
        if q1[:, 0].max() < 0 or q1[:, 0].min() > W or q1[:, 1].max() < 0 or q1[:, 1].min() > H: continue
        if np.ptp(q1[:, 0]) > W / 4 and M['classes'][M['cls'][b]] != 'fort': continue      # next to the camera
        cls = M['classes'][M['cls'][b]]
        col = (40, 120, 220) if cls in ('fort',) else (60, 60, 200) if cls == 'landmark' else (200, 90, 40)
        cv2.fillPoly(ov, [np.int32(np.vstack([q0, q1[::-1]]))], col) if cls == 'landmark' else None
        cv2.polylines(im, [np.int32(q1)], True, col, th, cv2.LINE_AA)
    im = cv2.addWeighted(ov, 0.25, im, 0.75, 0)
    labels = []
    for k in LMK:                            # landmarks: foot – tip and name
        b = IDX[k]
        if not visible(b, year + 0.01) or math.hypot(*centre(b)) > 1600: continue
        (u0, v0), (u1, v1) = project(par, np.array([W3(b, 0), W3(b, 1)]), W, H)[0]
        if not (0 <= u1 < W and 0 <= v1 < H): continue
        cv2.line(im, (int(u0), int(v0)), (int(u1), int(v1)), (30, 30, 200), 2 * th, cv2.LINE_AA)
        labels.append((int(u1) + 6, int(v1) - 18 * th, NAMES.get(k, k)))
    for (e, at), o in zip(used, pts):        # clicked points and residuals
        b = IDX.get(e)
        if b is None: continue
        q = project(par, W3(b, {'top': 1.0, 'mid': 0.5, 'ground': 0.0}[at]), W, H)[0][0]
        cv2.circle(im, (int(o[0]), int(o[1])), 5 * th, (0, 170, 0), th, cv2.LINE_AA); cv2.line(im, (int(o[0]), int(o[1])), (int(q[0]), int(q[1])), (0, 170, 0), th, cv2.LINE_AA)
    cv2.rectangle(im, (0, 0), (W, int(34 * th)), (255, 255, 255), -1)
    from PIL import ImageDraw, ImageFont
    pi = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)); dr = ImageDraw.Draw(pi)
    try: fn = ImageFont.truetype('segoeui.ttf', 16 * th); fb = ImageFont.truetype('segoeuib.ttf', 15 * th)
    except OSError: fn = fb = ImageFont.load_default()
    dr.text((10, 6 * th), title, fill=(20, 20, 20), font=fn)
    for x, y, t in labels: dr.text((x, y), t, fill=(200, 30, 30), font=fb, stroke_width=2 * th, stroke_fill=(255, 255, 255))
    return cv2.cvtColor(np.array(pi), cv2.COLOR_RGB2BGR)


TE_PAR = []


def main():
    res = {}
    for s in P['sources']:
        if s.get('kind') not in ('birdseye', 'panorama'): continue
        sid = s['id']; W, H = Image.open(os.path.join(ROOT, 'data', 'historic', 'sources', f'{sid}.jpg')).size
        year = float((s.get('depicted') or [1618])[0])
        if sid in ('te-1618', 'ottheinrich-1536'):
            # the wall entity's centre is the town centre (not a drawn point); church centres at half height on the panorama
            links = [a for a in P['annotations'] if a['sourceId'] == sid and a.get('entityId') in IDX and a['entityId'] != 'g1618-wall']
            used = [(a['entityId'], 'mid' if (s['kind'] == 'panorama' and a['entityId'] in ('g1618-bartholomew', 'g1618-franciscan')) else 'top') for a in links]
            obs = np.array([a['img'] for a in links], float)
            X = np.array([W3(IDX[e], {'top': 1.0, 'mid': 0.5}[at]) for e, at in used])
            # Ottheinrich: drawn from the south-south-west (veduta_fit.py, Ottheinrich's route from Nuremberg)
            wt = [3.0 if e == 'g1618-bartholomew' else 1.0 for e, _ in used]    # the dominant tower first
            par, rms = fit(X, obs, W, H, 'birdseye' if s['kind'] == 'birdseye' else 'panorama', az_list=[195, 205, 215] if sid == 'ottheinrich-1536' else None, wt=wt)
            how = f'{len(links)} links of the project'
            if sid == 'te-1618': TE_PAR[:] = [par, W, H]
        elif PTS.get(sid, {}).get('kind') == 'panorama':
            par, rms, used, obs, az = panorama(PTS[sid], W, H, year)
            how = f'direction search ({az}°), {len(used)} matched points'
        elif sid in PTS:
            pts = PTS[sid]['points']; used = [(p['e'], p['at']) for p in pts if p['e'] in IDX]
            obs = np.array([p['img'] for p in pts if p['e'] in IDX], float)
            X = np.array([W3(IDX[e], {'top': 1.0, 'mid': 0.5, 'ground': 0.0}[at]) for e, at in used])
            st = []
            if TE_PAR:   # copies of the 1618 plate: also start from its camera (focal length scaled to the sheet)
                p0 = TE_PAR[0].copy(); p0[6] += math.log(H / TE_PAR[2]); st = [p0]
            par, rms = fit(X, obs, W, H, 'birdseye', starts=st)
            how = f'{len(used)} points'
        else:
            continue
        v = view_of(par, W, H); v.update({'year': year, 'rms': round(rms, 1), 'rms_pct': round(100 * rms / H, 1), 'how': how})
        res[sid] = v
        title = f"{sid}: model {int(year)} promítnutý do veduty / model projected into the veduta (odchylka / error {100 * rms / H:.1f} % výšky / of the height)"
        im = mapping_image(sid, par, W, H, year, obs, used, title)
        cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 85])[1].tofile(os.path.join(SHOTS, f'vedmap_{sid}.jpg'))
        print(f'{sid:18s} {how:40s} error {rms:7.1f} px ({100 * rms / H:4.1f} %)  camera {np.round(par[:3]).astype(int)}  fov {v["fov"]:.1f}°')
    json.dump({'note': 'cameras of the vedute estimated by veduta_views.py (three.js axes: x east, y up, z south; quaternion x y z w)', 'views': res},
              open(OUTJ, 'w', encoding='utf-8'), indent=1)


def compose(run):
    V = json.load(open(OUTJ, encoding='utf-8'))['views']
    for k, (sid, v) in enumerate(V.items()):
        f = os.path.join(ROOT, 'data', 'historic', 'growth', 'video', run, f'f_{k:06d}.jpg')
        mp = os.path.join(SHOTS, f'vedmap_{sid}.jpg')
        if not (os.path.exists(f) and os.path.exists(mp)): continue
        a = cv2.imdecode(np.fromfile(mp, np.uint8), 1); b = cv2.imdecode(np.fromfile(f, np.uint8), 1)
        w = 1400; a = cv2.resize(a, (w, int(a.shape[0] * w / a.shape[1])), interpolation=cv2.INTER_AREA)
        b = cv2.resize(b, (w, a.shape[0]), interpolation=cv2.INTER_AREA)     # also undoes the panorama stretch
        pass
        cv2.imencode('.jpg', np.vstack([a, np.full((8, w, 3), 255, np.uint8), b]), [cv2.IMWRITE_JPEG_QUALITY, 84])[1].tofile(os.path.join(SHOTS, f'vedview_{sid}.jpg'))
        print('composed', sid)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--compose': compose(sys.argv[2])
    else: main()
