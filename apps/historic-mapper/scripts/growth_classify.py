"""Built-up growth of Plzeň from maps of many epochs in one frame (9 x 9 km, 2.5 m/px).

Per epoch: classify building pixels with rules tuned to the cartographic style, mask the
area actually covered by the map, turn building pixels into settlement areas (closing +
filling small holes + removing specks), find the connected settlement that contains the old
town, and test which villages (Wikidata points) are part of it.

usage: python growth_classify.py raw_dir villages_wgs.json out_dir
writes out_dir/builtup.geojson (one MultiPolygon per epoch), out_dir/villages.json,
out_dir/mask_<epoch>.png, out_dir/_growth.jpg (contact sheet)
"""
import json, math, os, sys
import cv2
import numpy as np

raw, vil_path, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
BBOX = (-826900, -1074200, -817900, -1065200); RES = 2.5; N = 3600
CORE = (-822400, -1069700)

def imread(p):
    im = cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_UNCHANGED)
    alpha = None
    if im.ndim == 3 and im.shape[2] == 4: alpha = im[..., 3]; im = im[..., :3]
    return im, alpha

def to_px(X, Y): return int((X - BBOX[0]) / RES), int((BBOX[3] - Y) / RES)
def to_map(c, r): return BBOX[0] + (c + 0.5) * RES, BBOX[3] - (r + 0.5) * RES

def hsv(im):
    h = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); return h[..., 0].astype(int) * 2, h[..., 1] / 255, h[..., 2] / 255  # hue in degrees

def dense(mask, k, thr):
    """fraction of mask pixels in a k x k window above thr (for hatched / line drawings)."""
    d = cv2.blur(mask.astype(np.float32), (k, k)); return d > thr

ALPHA = None

def rule(name, im):
    H, S, V = hsv(im)
    red = ((H < 22) | (H > 335)) & (S > 0.22) & (V > 0.35)
    if name == '1840_cadastre':  # carmine buildings only (at 2.5 m/px the yellow wooden-building class collides with field colours)
        return ((H < 15) | (H > 335)) & (S > 0.35) & (V > 0.4)
    if name == '1840_vm2':      # settlements drawn red / carmine on a pale base, 1:28 800
        return dense(((H < 20) | (H > 330)) & (S > 0.18) & (V > 0.3), 5, 0.35)
    if name in ('1880_vm3', '1891', '1912'):  # black / dark brown block hatching
        dark = V < (0.42 if name == '1880_vm3' else 0.45)
        return dense(dark, 9, 0.5 if name == '1880_vm3' else 0.38)
    if name == '1895':
        return dense(red | (V < 0.40), 7, 0.4)
    if name in ('1926', '1931', '1938'):
        return red
    if name == '1947':  # red / orange blocks in the west, grey-violet blocks in the east
        return red | ((H >= 15) & (H < 40) & (S > 0.35) & (V > 0.55)) | ((H >= 250) & (H < 335) & (S > 0.10) & (V > 0.45) & (V < 0.85))
    if name == '1953_orto':     # bright roofs + strong local texture (rough heuristic)
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
        mu = cv2.blur(g, (9, 9)); sd = np.sqrt(np.maximum(cv2.blur(g * g, (9, 9)) - mu * mu, 0))
        return dense((sd > 28) & (mu > 90), 15, 0.5)
    if name == '2025_ruian':    # RÚIAN building polygons (ČÚZK map service, transparent background)
        return ALPHA is not None and ALPHA > 0
    if name == '2025_ztm':      # buildings dark grey, built-up area tint pink-grey
        bld = (S < 0.12) & (V > 0.45) & (V < 0.78)
        tint = ((H < 30) | (H > 320)) & (S > 0.06) & (S < 0.35) & (V > 0.75)
        return dense(bld, 5, 0.25) | dense(tint, 9, 0.6)
    return red

def coverage(name, im, alpha):
    if alpha is not None: m = alpha > 0
    else: m = ~((im > 245).all(2))
    return cv2.erode(m.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0

# 2nd military survey (1840_vm2): the CENIA rendering has no separable settlement colour at this
# scale — kept as a visual layer only, not classified
# density thresholds per epoch (share of building pixels in the 150 m window)
DENS_T = {'1840_cadastre': 0.10, '1880_vm3': 0.30, '1891': 0.25, '1895': 0.25, '1912': 0.2, '1953_orto': 0.25, '2025_ruian': 0.15}
YEAR = {'1840_cadastre': 1840, '1880_vm3': 1880, '1891': 1891, '1895': 1895, '1912': 1912, '1926': 1926,
        '1931': 1931, '1938': 1938, '1947': 1947, '1953_orto': 1953, '2025_ruian': 2025}

villages = json.load(open(vil_path, encoding='utf-8'))
# S-JTSK via proj4-free Krovak is heavy: reuse the WGS84 → 5514 transform from GDAL if present, else pyproj
try:
    from osgeo import osr
    src = osr.SpatialReference(); src.ImportFromEPSG(4326); src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    dst = osr.SpatialReference(); dst.ImportFromProj4('+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56 +units=m +no_defs')
    tr = osr.CoordinateTransformation(src, dst); conv = lambda lon, lat: tr.TransformPoint(lon, lat)[:2]
except Exception:
    from pyproj import Transformer
    t = Transformer.from_crs('EPSG:4326', '+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56 +units=m +no_defs', always_xy=True)
    conv = lambda lon, lat: t.transform(lon, lat)
V = {}
for k, (lon, lat) in villages.items():
    X, Y = conv(lon, lat)
    if BBOX[0] < X < BBOX[2] and BBOX[1] < Y < BBOX[3]: V[k] = (X, Y)

feats, vres, tiles = [], {k: {'xy': [round(v[0], 1), round(v[1], 1)], 'epochs': {}} for k, v in V.items()}, []
cr, cc = to_px(*CORE)[::-1]
for name in sorted(YEAR, key=YEAR.get):
    f = next((x for x in os.listdir(raw) if x.split('.')[0] == name), None)
    if not f: continue
    im, alpha = imread(os.path.join(raw, f)); ALPHA = alpha
    cov = coverage(name, im, alpha) if name != '2025_ruian' else np.ones((N, N), bool)
    globals()['ALPHA'] = alpha
    b = rule(name, im) & cov
    # settlement areas by building density: share of building pixels within ~150 m above a threshold
    # (merges blocks separated by streets and courtyards into continuous urban fabric)
    dens = cv2.blur(b.astype(np.float32), (61, 61))
    area = (dens > DENS_T.get(name, 0.12)) & cov
    area = cv2.morphologyEx(area.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(area, 8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 20000 / (RES * RES)  # ≥ 2 ha
    area = keep[lab]
    lab2 = cv2.connectedComponents(area.astype(np.uint8), connectivity=8)[1]
    # the town = settlement components touching a 250 m disc around the old town
    disc = np.zeros((N, N), np.uint8); cv2.circle(disc, (cc, cr), int(250 / RES), 1, -1)
    ids = np.unique(lab2[(disc > 0) & (lab2 > 0)])
    town = np.isin(lab2, ids) if len(ids) else np.zeros_like(area)
    cv2.imencode('.png', (area.astype(np.uint8) * 120 + town.astype(np.uint8) * 135))[1].tofile(os.path.join(out, f'mask_{name}.png'))
    # polygons (simplified, 5 m)
    cs, hier = cv2.findContours(area.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    polys = []
    if hier is not None:
        for i, c in enumerate(cs):
            if hier[0][i][3] != -1 or cv2.contourArea(c) < 64: continue
            ring = [list(map(lambda v: round(v, 1), to_map(int(x), int(y)))) for x, y in cv2.approxPolyDP(c, 2, True).reshape(-1, 2)]
            if len(ring) < 3: continue
            ring.append(ring[0]); holes = []
            ch = hier[0][i][2]
            while ch != -1:
                h = [list(map(lambda v: round(v, 1), to_map(int(x), int(y)))) for x, y in cv2.approxPolyDP(cs[ch], 2, True).reshape(-1, 2)]
                if len(h) >= 3 and cv2.contourArea(cs[ch]) > 64: h.append(h[0]); holes.append(h)
                ch = hier[0][ch][0]
            mid = c.reshape(-1, 2).mean(0).astype(int)
            polys.append(([ring] + holes, bool(town[min(mid[1], N - 1), min(mid[0], N - 1)]) or bool(town[c[0][0][1], c[0][0][0]])))
    town_m2 = float(town.sum() * RES * RES); all_m2 = float(area.sum() * RES * RES); cov_km2 = float(cov.sum() * RES * RES / 1e6)
    feats.append({'type': 'Feature', 'properties': {'epoch': name, 'year': YEAR[name], 'town_km2': round(town_m2 / 1e6, 2), 'builtup_km2': round(all_m2 / 1e6, 2), 'coverage_km2': round(cov_km2, 1)},
                  'geometry': {'type': 'MultiPolygon', 'coordinates': [p for p, _ in polys]}, 'town_parts': [i for i, (_, t) in enumerate(polys) if t]})
    for kname, (X, Y) in V.items():
        c, r = to_px(X, Y)
        if not (0 <= r < N and 0 <= c < N) or not cov[r, c]: vres[kname]['epochs'][name] = None; continue
        win = (slice(max(0, r - 120), r + 121), slice(max(0, c - 120), c + 121))  # 300 m around the village point
        has = bool(area[win].any()); joined = bool(town[win].any())
        vres[kname]['epochs'][name] = 'joined' if joined else 'separate' if has else 'none'
    vis = cv2.resize(im, (450, 450), interpolation=cv2.INTER_AREA)
    m = cv2.resize(area.astype(np.uint8), (450, 450), interpolation=cv2.INTER_NEAREST) > 0
    t2 = cv2.resize(town.astype(np.uint8), (450, 450), interpolation=cv2.INTER_NEAREST) > 0
    vis[m] = (0.4 * vis[m] + 0.6 * np.array([60, 160, 255])).astype(np.uint8); vis[t2] = (0.4 * vis[t2] + 0.6 * np.array([40, 40, 200])).astype(np.uint8)
    cv2.putText(vis, f'{YEAR[name]} {name.split("_")[-1] if "_" in name else ""}  town {town_m2 / 1e6:.1f} km2', (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    tiles.append(vis)
    print(f'{name:14s} coverage {cov_km2:5.1f} km²  built-up {all_m2 / 1e6:5.2f} km²  town {town_m2 / 1e6:5.2f} km²')
json.dump({'type': 'FeatureCollection', 'name': 'Plzeň built-up by epoch', 'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::5514'}}, 'features': feats},
          open(os.path.join(out, 'builtup.geojson'), 'w'), separators=(',', ':'))
# year each village first appears joined to the town (with following epochs consistent)
for k, v in vres.items():
    seq = [(YEAR[e], s) for e, s in v['epochs'].items() if s]
    v['first_joined'] = next((y for y, s in sorted(seq) if s == 'joined'), None)
json.dump(vres, open(os.path.join(out, 'villages.json'), 'w'), indent=1, ensure_ascii=False)
while len(tiles) % 4: tiles.append(np.full((450, 450, 3), 255, np.uint8))
sheet = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)])
cv2.imencode('.jpg', sheet, [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(out, '_growth.jpg'))
for k, v in sorted(vres.items(), key=lambda kv: kv[1]['first_joined'] or 9999):
    print(f'  {k:15s} joined {v["first_joined"]}  ' + ' '.join(f'{YEAR[e]}:{(s or "-")[0]}' for e, s in sorted(v["epochs"].items(), key=lambda kv: YEAR[kv[0]])))
