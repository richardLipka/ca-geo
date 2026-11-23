"""Plzeň around 1536–1618: landmark model, georeference of the 1618 siege plate and
reverse analysis (viewpoint resection) of the oldest veduta (Ottheinrich album, 1536–37).

Inputs are hand-identified positions:
  * map positions of landmarks in the stable-cadastre export frame (0.5 m/px, bbox
    -822810,-1070100,-822010,-1069300 in EPSG:5514) or from Wikidata coordinates;
  * pixel positions of the same objects in the Theatrum Europaeum plate (te-1618.jpg,
    2000 x 1823 px) and image columns in the Ottheinrich view (ottheinrich-1536.jpg,
    3061 x 2282 px).
Outputs: JSON with fits and residuals (stdout + file) used to seed the historic-mapper
project. numpy only.
usage: python plzen_1618.py out.json
"""
import json, math, sys
import numpy as np

def cad(px, py):
    """stable-cadastre export pixel → EPSG:5514"""
    return (-822810 + 0.5 * px, -1069300 - 0.5 * py)

# ---------------------------------------------------------------- landmarks (map)
# id: (name, type, map position, provenance)
L = {
    'bartholomew':   ('St Bartholomew (church centre)', 'church', (-822396.8, -1069689.4), 'Wikidata Q1124051'),
    'barth_tower':   ('St Bartholomew – west tower', 'tower', cad(750, 800), 'stable cadastre, west front'),
    'barth_east':    ('St Bartholomew – east end of chancel', 'church', cad(874, 795), 'stable cadastre'),
    'dominican':     ('Dominican monastery (Black monastery)', 'church', cad(775, 330), 'stable cadastre: Militair Spital block 69 (site)'),
    'franciscan':    ('Franciscan church (Assumption)', 'church', cad(938, 1235), 'stable cadastre'),
    'all_saints':    ('All Saints church (Roudná)', 'church', (-822079.7, -1068508.4), 'Wikidata Q12030559'),
    'gate_prague':   ('Prague gate (Pražská brána)', 'gate', cad(1230, 800), 'east end of Prager Gasse, cadastre + 1821 plan'),
    'gate_reich':    ('Imperial / Nuremberg gate (Říšská brána)', 'gate', cad(270, 905), 'west end of Reichs Gasse, cadastre'),
    'gate_litice':   ('Litice gate (Litická brána)', 'gate', cad(470, 1285), 'south side near the Lyceum (tower kept in the gymnasium), approx.'),
    'gate_north':    ('North gate (Saská / Mill gate)', 'gate', cad(1090, 415), 'north end of Sachsen Gasse, cadastre, approx.'),
    'water_tower':   ('Water tower (Vodárenská věž, 1532)', 'tower', cad(1185, 805), 'next to the meat stalls, cadastre, approx.'),
    'st_nicholas':   ('St Nicholas church (suburb)', 'church', (-821983.1, -1070684.7), 'Wikidata Q15124089'),
    'sq_nw': ('Square – NW corner', 'street', cad(743, 650), 'stable cadastre block corners'),
    'sq_ne': ('Square – NE corner', 'street', cad(1000, 717), 'stable cadastre block corners'),
    'sq_se': ('Square – SE corner', 'street', cad(887, 1052), 'stable cadastre block corners'),
    'sq_sw': ('Square – SW corner', 'street', cad(627, 992), 'stable cadastre block corners'),
    'sq_w':  ('Square – west street mouth', 'street', cad(668, 823), 'stable cadastre block corners'),
    'sq_e':  ('Square – east street mouth', 'street', cad(943, 893), 'stable cadastre block corners'),
}

# inner town wall (backs of the perimeter houses on the stable cadastre), cadastre px
WALL = [(509, 280), (791, 225), (1086, 405), (1381, 534), (1345, 600), (1345, 746), (1215, 792), (1178, 866),
        (1045, 912), (1035, 1088), (1008, 1115), (994, 1217), (994, 1346), (883, 1355), (791, 1337), (615, 1300),
        (495, 1291), (302, 1217), (269, 1115), (255, 1005), (278, 885), (302, 783), (398, 691), (431, 562), (477, 405)]

# ---------------------------------------------------------------- 1618 plate (Theatrum Europaeum)
# legend: A St Bartholomew, B Black (Dominican) monastery, C Franciscan monastery (first breach),
# E Prague gate, F Nuremberg gate, G Small gate, H Litice gate, K All Saints
TE = {  # ground positions (footprint centres / street junctions), refined by back-projection checks
    'bartholomew': ((1010, 830), 'A'), 'dominican': ((1036, 600), 'B'), 'franciscan': ((1029, 1110), 'C'),
    'gate_prague': ((1403, 896), 'E'), 'gate_north': ((1285, 708), 'G'), 'gate_litice': ((740, 960), 'H'),
    'sq_nw': ((970, 720), ''), 'sq_ne': ((1157, 849), ''), 'sq_se': ((1021, 989), ''),
    'sq_sw': ((880, 880), ''), 'sq_w': ((930, 800), ''), 'sq_e': ((1082, 931), ''),
}
# wall towers drawn on the plate (pixel), to be projected onto the map
TE_TOWERS = [(932, 539), (659, 785), (761, 960), (1357, 874), (1286, 689), (779, 660), (718, 581), (1420, 819)]

def homography(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    h, *_ = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)
    H = np.append(h, 1).reshape(3, 3)
    return H

def apply(H, p):
    q = H @ np.array([p[0], p[1], 1.0]); return (q[0] / q[2], q[1] / q[2])

def norm_pts(pts):
    a = np.array(pts, float); c = a.mean(0); s = math.sqrt(2) / np.sqrt(((a - c) ** 2).sum(1).mean())
    T = np.array([[s, 0, -s * c[0]], [0, s, -s * c[1]], [0, 0, 1]]); return T

def fit_h(src, dst):
    Ts, Td = norm_pts(src), norm_pts(dst)
    s = [tuple((Ts @ [x, y, 1])[:2]) for x, y in src]; d = [tuple((Td @ [x, y, 1])[:2]) for x, y in dst]
    Hn = homography(s, d)
    return np.linalg.inv(Td) @ Hn @ Ts

def residuals(src, dst, fitter):
    H = fitter(src, dst)
    res = [math.dist(apply(H, p), q) for p, q in zip(src, dst)]
    loo = []
    for i in range(len(src)):
        s = src[:i] + src[i + 1:]; d = dst[:i] + dst[i + 1:]
        Hi = fitter(s, d); loo.append(math.dist(apply(Hi, src[i]), dst[i]))
    return H, res, loo

# ---------------------------------------------------------------- oldest veduta (Ottheinrich 1536–37)
OTT_W = 3061
OTT = {  # image column x of the vertical axis of each object, plus a row for the annotation marker
    'barth_tower': (1017, 1300), 'barth_east': (1217, 1340),
}
OTT_CANDIDATES = {  # unidentified objects in the view and their hypotheses
    'left_gate_642': ((642, 1420), ['gate_reich', 'gate_litice']),
    'tall_tower_1536': ((1536, 1300), ['water_tower', 'gate_prague']),
    'spire_church_1801': ((1801, 1380), ['franciscan', 'dominican', 'st_nicholas']),
    'right_tower_2020': ((2020, 1440), ['gate_prague', 'gate_litice', 'water_tower']),
    'round_tower_779': ((779, 1400), ['gate_litice', 'gate_reich', None]),
}

def pano_fit(obs, cx, box=None, proj='tan'):
    """x = cx + f·tan(β − θ) (perspective) or cx + f·(β − θ) (cylindrical); grid search + LM."""
    P = np.array([o[1] for o in obs], float); X = np.array([o[0] for o in obs], float)
    def model(q):
        b = np.arctan2(P[:, 1] - q[1], P[:, 0] - q[0]) - q[2]; b = (b + np.pi) % (2 * np.pi) - np.pi
        return cx + q[3] * (np.tan(b) if proj == 'tan' else b)
    def cost(q):
        r = model(q) - X; r = np.where(np.isfinite(r), r, 1e6); return float((r ** 2).sum())
    best = (1e30, None)
    xs, ys = P[:, 0], P[:, 1]
    bx = box or (xs.min() - 5000, ys.min() - 5000, xs.max() + 5000, ys.max() + 5000)
    for X0 in np.linspace(bx[0], bx[2], 81):
        for Y0 in np.linspace(bx[1], bx[3], 81):
            if np.min(np.hypot(xs - X0, ys - Y0)) < 150: continue
            bear = np.arctan2(ys - Y0, xs - X0); m = math.atan2(np.sin(bear).sum(), np.cos(bear).sum())
            for th in (m, m + math.pi):
                t = (np.tan(bear - th) if proj == 'tan' else ((bear - th + np.pi) % (2 * np.pi) - np.pi)); f = float((t * (X - cx)).sum() / max((t * t).sum(), 1e-9))
                c = cost([X0, Y0, th, f])
                if c < best[0]: best = (c, [X0, Y0, th, f])
    q = np.array(best[1]); lam = 1e-2; c = best[0]; steps = np.array([1, 1, 1e-4, 1])
    for _ in range(300):
        r = model(q) - X
        J = np.stack([(model(q + np.eye(4)[j] * steps[j]) - X - r) / steps[j] for j in range(4)], 1)
        A = J.T @ J; g = J.T @ r; ok = False
        for _ in range(8):
            try: d = np.linalg.solve(A + lam * np.diag(np.diag(A) + 1e-9), -g)
            except np.linalg.LinAlgError: lam *= 10; continue
            qn = q + d
            qn[0] = min(max(qn[0], bx[0]), bx[2]); qn[1] = min(max(qn[1], bx[1]), bx[3])
            cn = cost(qn)
            if cn < c: q, c, lam, ok = qn, cn, lam / 3, True; break
            lam *= 10
        if not ok: break
    r = model(q) - X
    return {'proj': proj, 'X0': float(q[0]), 'Y0': float(q[1]), 'theta_deg': math.degrees(q[2]), 'f_px': float(q[3]),
            'residuals_px': [float(v) for v in r], 'rmse_px': float(np.sqrt((r ** 2).mean())), 'n': len(obs)}

def order_map(obs, box, n=121):
    """Share of object pairs whose left-to-right order in the image matches the order of
    their bearings seen from each candidate viewpoint (robust to the artist's distortions)."""
    X = np.array([o[0] for o in obs], float); P = np.array([o[1] for o in obs], float)
    xs = np.linspace(box[0], box[2], n); ys = np.linspace(box[1], box[3], n)
    best = (-1, None); grid = np.zeros((n, n))
    pairs = [(i, j) for i in range(len(obs)) for j in range(i + 1, len(obs)) if abs(X[i] - X[j]) > 20]
    for a, Y0 in enumerate(ys):
        for b, X0 in enumerate(xs):
            bear = np.arctan2(P[:, 1] - Y0, P[:, 0] - X0)
            # looking towards the town (north): image x grows with decreasing bearing (clockwise)
            ref = math.atan2(np.sin(bear).mean(), np.cos(bear).mean())
            rel = (bear - ref + np.pi) % (2 * np.pi) - np.pi
            ok = sum((X[i] - X[j]) * (rel[j] - rel[i]) > 0 for i, j in pairs)
            grid[a, b] = ok / max(len(pairs), 1)
            if grid[a, b] > best[0]: best = (grid[a, b], (float(X0), float(Y0)))
    good = np.argwhere(grid >= grid.max() - 1e-9)
    region = [(float(xs[j]), float(ys[i])) for i, j in good]
    return {'best_share': float(best[0]), 'n_pairs': len(pairs), 'region_size': len(region),
            'region_bbox': [min(r[0] for r in region), min(r[1] for r in region), max(r[0] for r in region), max(r[1] for r in region)]}

def main(out):
    res = {'landmarks': {k: {'name': v[0], 'type': v[1], 'xy': v[2], 'provenance': v[3]} for k, v in L.items()},
           'wall': [cad(*p) for p in WALL]}
    # 1618 plate
    keys = list(TE)
    src = [TE[k][0] for k in keys]; dst = [L[k][2] for k in keys]
    H, r, loo = residuals(src, dst, fit_h)
    res['te1618'] = {'points': [{'id': k, 'label': TE[k][1], 'img': TE[k][0], 'map': L[k][2], 'res_m': round(a, 1), 'loo_m': round(b, 1)} for k, a, b in zip(keys, r, loo)],
                     'rmse_m': round(float(np.sqrt(np.mean(np.square(r)))), 1), 'loo_rmse_m': round(float(np.sqrt(np.mean(np.square(loo)))), 1)}
    # inner-town only (without the far All Saints point)
    k2 = keys  # all TE points are inside / at the town
    H2, r2, loo2 = residuals([TE[k][0] for k in k2], [L[k][2] for k in k2], fit_h)
    res['te1618_town'] = {'rmse_m': round(float(np.sqrt(np.mean(np.square(r2)))), 1), 'loo_rmse_m': round(float(np.sqrt(np.mean(np.square(loo2)))), 1),
                          'loo_m': {k: round(v, 1) for k, v in zip(k2, loo2)}}
    res['te1618_towers'] = [{'img': p, 'map': [round(c, 1) for c in apply(H2, p)]} for p in TE_TOWERS]
    # oldest veduta: base identification + hypotheses for the unidentified objects
    base = [(OTT[k][0], L[k][2]) for k in OTT]
    hyps = []
    import itertools
    cand = list(OTT_CANDIDATES.items())
    for combo in itertools.product(*[c[1][1] for c in cand]):
        used = [k for k in combo if k]
        if len(set(used)) < len(used) or set(used) & set(OTT): continue  # one object per landmark
        obs = base + [(c[1][0][0], L[k][2]) for c, k in zip(cand, combo) if k]
        for proj in ('tan', 'lin'):
            # Ježek (1997): the drawer stood south of the town → search viewpoints south of the walls
            f = pano_fit(obs, OTT_W / 2, box=(-825000, -1073500, -819500, -1070050), proj=proj)
            f['assignment'] = {c[0]: k for c, k in zip(cand, combo)}
            hyps.append(f)
    for h in hyps:
        obs = base + [(OTT_CANDIDATES[c][0][0], L[k][2]) for c, k in h['assignment'].items() if k]
        h['order'] = order_map(obs, (-825000, -1073500, -819500, -1070050), n=61)
    hyps = [h for h in hyps if abs(h['f_px']) < 50000]
    hyps.sort(key=lambda h: h['rmse_px'] * (1 + 2.0 / max(h['n'] - 4, 1)))  # penalise fits with few points
    res['ottheinrich_hypotheses'] = hyps
    json.dump(res, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('TE 1618 all points: RMSE %.1f m, LOO %.1f m' % (res['te1618']['rmse_m'], res['te1618']['loo_rmse_m']))
    for p in res['te1618']['points']: print('  %-3s %-12s res %6.1f  loo %6.1f' % (p['label'], p['id'], p['res_m'], p['loo_m']))
    print('TE 1618 town only: RMSE %.1f m, LOO %.1f m' % (res['te1618_town']['rmse_m'], res['te1618_town']['loo_rmse_m']))
    print('Ottheinrich hypotheses (best 6):')
    for h in hyps[:6]:
        print('  %s rmse %6.1f px (n=%d) view (%.0f, %.0f) f %.0f order %.2f  %s' % (h['proj'], h['rmse_px'], h['n'], h['X0'], h['Y0'], h['f_px'], h['order']['best_share'], h['assignment']))
    print('Best by ordinal consistency:')
    for h in sorted([h for h in hyps if h['proj'] == 'lin'], key=lambda h: (-h['order']['best_share'], -h['n']))[:6]:
        o = h['order']; print('  order %.2f of %d pairs, region %s  %s' % (o['best_share'], o['n_pairs'], [round(v) for v in o['region_bbox']], h['assignment']))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'plzen_1618.json')
