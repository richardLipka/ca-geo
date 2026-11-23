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
from growth_rules import BBOX, RES, N, CORE, to_px, to_map, imread, rule, coverage, DENS_T, YEAR


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
    im, alpha = imread(os.path.join(raw, f))
    cov = coverage(name, im, alpha) if name != '2025_ruian' else np.ones((N, N), bool)
    b = rule(name, im, alpha) & cov
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
json.dump(vres, open(os.path.join(out, 'villages.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
while len(tiles) % 4: tiles.append(np.full((450, 450, 3), 255, np.uint8))
sheet = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)])
cv2.imencode('.jpg', sheet, [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(out, '_growth.jpg'))
for k, v in sorted(vres.items(), key=lambda kv: kv[1]['first_joined'] or 9999):
    print(f'  {k:15s} joined {v["first_joined"]}  ' + ' '.join(f'{YEAR[e]}:{(s or "-")[0]}' for e, s in sorted(v["epochs"].items(), key=lambda kv: YEAR[kv[0]])))
