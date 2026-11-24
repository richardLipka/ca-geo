"""Check the growth model against every ground / epoch map before a video is rendered.

For each map at the first year of its validity:
1. Map support: every model building standing in that year (real and generated) gets the share of its footprint
   that the map draws as built (building pixels of growth_rules, 2.5 m tolerance). Classes: supported (≥ 30 %),
   weak (10–30 %), extra (< 10 %: the map shows no building there). Maps without a building detector (plans of
   1658 / 1703, map 57, the 1781 plan) are checked only for overlaps.
2. Overlaps: pairs of buildings standing at the same time whose footprints overlap by more than 25 % of the smaller
   one (e.g. a 19th-century building over a monastery that is still standing).

usage: python check_epochs.py        (after growth_model.py)
writes data/historic/growth/site/check/index.html, check_<year>.jpg (footprints over the map, core 2 × 2 km),
       check.json (counts and the worst cases per map)
"""
import html, json, os
import cv2
import numpy as np
from shapely.geometry import Polygon
from shapely.strtree import STRtree
from growth_rules import imread, rule, coverage, hsv, BBOX, RES, N

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
G = os.path.join(ROOT, 'data', 'historic', 'growth')
OUT = os.path.join(G, 'site', 'check'); os.makedirs(OUT, exist_ok=True)
M = json.load(open(os.path.join(G, 'web', 'model.json'), encoding='utf-8'))
OX, OY = M['origin']; CLS = M['classes']; BAS = M['basis']
SKIP = {'fort', 'ditch', 'moat'}
RAW = os.path.join(G, 'raw')
raw_path = lambda n: os.path.join(RAW, next(x for x in os.listdir(RAW) if x.split('.')[0] == n))
DETECT = [('1821', 1821), ('1840_cadastre', 1840), ('1877_mesto', 1877), ('1880_vm3', 1880), ('1881', 1881), ('1891', 1891), ('1895', 1895),
          ('1902', 1902), ('1908', 1908), ('1912', 1912), ('1926', 1926), ('1931', 1931), ('1938', 1938), ('1947', 1947), ('1953_orto', 1953),
          ('2001_orto', 2001)]
NODETECT = [(1300, 'ground_1300.jpg', 'mapa 57 (cca 1410)'), (1618, 'ground_1618.jpg', 'Theatrum Europaeum 1618'), (1658, 'ground_1658.jpg', 'plán 1658'),
            (1703, 'ground_1703.jpg', 'plán 1703'), (1781, 'ground_1781.jpg', 'plán 1781')]
CORE = (-823400, -1070700, -821400, -1068700)   # 2 × 2 km around the old town
CR = 1.25; CN = int((CORE[2] - CORE[0]) / CR)


def ring(b):
    r = M['rings'][b]
    return [(OX + r[i] / 10, OY + r[i + 1] / 10) for i in range(0, len(r), 2)]


def visible(b, y):
    g = M['gaps'][b]
    return M['from'][b] <= y - 0.05 < M['to'][b] and not (g[0] <= y < g[1]) and not (g[2] <= y < g[3])


def px(pts):   # frame pixels (2.5 m)
    return np.array([[(x - BBOX[0]) / RES, (BBOX[3] - y) / RES] for x, y in pts], np.float32)


def cpx(pts):  # core crop pixels
    return np.round(np.array([[(x - CORE[0]) / CR, (CORE[3] - y) / CR] for x, y in pts])).astype(np.int32)


def core_image(img_frame):
    """frame-sized image (N×N) → core crop at 1.25 m"""
    x0 = int((CORE[0] - BBOX[0]) / RES); y0 = int((BBOX[3] - CORE[3]) / RES); w = int((CORE[2] - CORE[0]) / RES)
    return cv2.resize(img_frame[y0:y0 + w, x0:x0 + w], (CN, CN), interpolation=cv2.INTER_CUBIC)


def overlaps(vis):
    polys = []
    for b in vis:
        p = Polygon(ring(b)).buffer(0)
        if p.area > 8: polys.append((b, p))
    tree = STRtree([p for _, p in polys]); out = []
    for i, (b, p) in enumerate(polys):
        for j in tree.query(p):
            if j <= i: continue
            b2, p2 = polys[j]
            a = p.intersection(p2).area
            if a > 0.25 * min(p.area, p2.area) and a > 15: out.append((b, b2, a))
    return out


report = []
TILES = []


def draw(base, vis, status, ovl, year, title):
    im = core_image(base) if base.shape[0] == N else cv2.resize(base, (CN, CN))
    im = (im * 0.75 + 255 * 0.25).astype(np.uint8)
    col = {'ok': (40, 160, 40), 'weak': (0, 165, 255), 'extra': (0, 0, 230), 'na': (150, 90, 30)}
    for b in vis:
        cv2.polylines(im, [cpx(ring(b))], True, col[status.get(b, 'na')], 2)
    for b1, b2, a in ovl:
        for b in (b1, b2): cv2.fillPoly(im, [cpx(ring(b))], (200, 0, 200))
    cv2.putText(im, f'{year}  {title}', (12, 40), 0, 1.1, (0, 0, 0), 3)
    cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 82])[1].tofile(os.path.join(OUT, f'check_{year}.jpg'))
    # tiles 3 × 3 for the review page (only tiles with buildings), with counts per status
    os.makedirs(os.path.join(OUT, 'tiles'), exist_ok=True)
    ts = CN // 3; tiles = []
    for r in range(3):
        for c in range(3):
            x0, y0 = CORE[0] + c * ts * CR, CORE[3] - (r + 1) * ts * CR
            inb = []
            for b in vis:
                rr = ring(b); cx = sum(p[0] for p in rr) / len(rr); cy = sum(p[1] for p in rr) / len(rr)
                if x0 <= cx < x0 + ts * CR and y0 <= cy < y0 + ts * CR: inb.append(b)
            if not inb: continue
            ov = sum(1 for b1, b2, _ in ovl if b1 in inb or b2 in inb)
            cnt = {k: sum(1 for b in inb if status.get(b) == k) for k in ('ok', 'weak', 'extra')}
            f = f'tiles/t_{year}_{r}{c}.jpg'
            cv2.imencode('.jpg', im[r * ts:(r + 1) * ts, c * ts:(c + 1) * ts], [cv2.IMWRITE_JPEG_QUALITY, 85])[1].tofile(os.path.join(OUT, f))
            tiles.append({'id': f'plan:{year}:{r}{c}', 'year': year, 'map': title, 'img': f, 'n': len(inb), 'overlaps': ov, **cnt})
    TILES.extend(tiles)


def describe(b):
    return {'id': M['ids'][b], 'from': M['from'][b], 'to': M['to'][b], 'basis': BAS[M['basisIdx'][b]], 'class': CLS[M['cls'][b]]}


for year, gfile, title in NODETECT:
    vis = [b for b in range(M['n']) if visible(b, year + 0.01) and CLS[M['cls'][b]] not in SKIP]
    ovl = overlaps(vis)
    base = cv2.imdecode(np.fromfile(os.path.join(G, 'web', gfile), np.uint8), 1)
    base = cv2.resize(base, (N, N))
    draw(base, vis, {}, ovl, year, title)
    report.append({'year': year, 'map': title, 'buildings': len(vis), 'overlaps': len(ovl),
                   'overlap_cases': [{'a': describe(a), 'b': describe(c), 'm2': round(ar)} for a, c, ar in sorted(ovl, key=lambda t: -t[2])[:25]]})
    print(year, title, len(vis), 'buildings,', len(ovl), 'overlaps')
for name, year in DETECT:
    im, alpha = imread(raw_path(name)); cov = coverage(name, im, alpha); B = rule(name, im, alpha) & cov
    if name == '1840_cadastre':
        H, S, V = hsv(im); B |= (H >= 45) & (H < 65) & (S > 0.5) & (V > 0.6) & cov
    Bd = cv2.dilate(B.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    vis = [b for b in range(M['n']) if visible(b, year + 0.01) and CLS[M['cls'][b]] not in SKIP]
    status, extra = {}, []
    for b in vis:
        p = px(ring(b)); x0, y0 = np.floor(p.min(0)).astype(int) - 1; x1, y1 = np.ceil(p.max(0)).astype(int) + 1
        if x0 < 0 or y0 < 0 or x1 >= N or y1 >= N: continue
        m = np.zeros((y1 - y0 + 1, x1 - x0 + 1), np.uint8); cv2.fillPoly(m, [np.round(p - [x0, y0]).astype(np.int32)], 1)
        m = m > 0
        if not m.any() or cov[y0:y1 + 1, x0:x1 + 1][m].mean() < 0.5: continue
        share = Bd[y0:y1 + 1, x0:x1 + 1][m].mean()
        status[b] = 'ok' if share >= 0.3 else 'weak' if share >= 0.1 else 'extra'
        if status[b] == 'extra': extra.append((b, Polygon(ring(b)).area))
    ovl = overlaps(vis)
    draw(im, vis, status, ovl, year, name)
    cnt = {k: sum(1 for v in status.values() if v == k) for k in ('ok', 'weak', 'extra')}
    gen_extra = sum(1 for b, _ in extra if M['ids'][b].startswith('gen:'))
    report.append({'year': year, 'map': name, 'buildings': len(status), **cnt, 'extra_generated': gen_extra, 'overlaps': len(ovl),
                   'extra_cases': [describe(b) | {'m2': round(a)} for b, a in sorted(extra, key=lambda t: -t[1])[:25]],
                   'overlap_cases': [{'a': describe(a), 'b': describe(c), 'm2': round(ar)} for a, c, ar in sorted(ovl, key=lambda t: -t[2])[:25]]})
    print(year, name, cnt, 'generated extra', gen_extra, 'overlaps', len(ovl))
json.dump(report, open(os.path.join(OUT, 'check.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(TILES, open(os.path.join(OUT, 'tiles.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# index page
rows, figs = [], []
for r in sorted(report, key=lambda r: r['year']):
    ex = r.get('extra', '–'); tot = r['buildings']
    rows.append(f'<tr><td>{r["year"]}</td><td>{html.escape(r["map"])}</td><td>{tot}</td><td>{r.get("ok", "–")}</td><td>{r.get("weak", "–")}</td>'
                f'<td class="{"bad" if isinstance(ex, int) and ex > 0.05 * tot else ""}">{ex}</td><td>{r.get("extra_generated", "–")}</td>'
                f'<td class="{"bad" if r["overlaps"] else ""}">{r["overlaps"]}</td></tr>')
    cases = ''.join(f'<li>{html.escape(c["a"]["id"])} ({c["a"]["from"]:.0f}–{c["a"]["to"]:.0f}, {html.escape(c["a"]["basis"])}) × {html.escape(c["b"]["id"])} ({c["b"]["from"]:.0f}–{c["b"]["to"]:.0f}, {html.escape(c["b"]["basis"])}): {c["m2"]} m²</li>' for c in r['overlap_cases'][:8])
    excs = ''.join(f'<li>{html.escape(c["id"])} {c["from"]:.0f}–{c["to"]:.0f}, {html.escape(c["basis"])}, {c["m2"]} m²</li>' for c in r.get('extra_cases', [])[:8])
    figs.append(f'<section><h2>{r["year"]} – {html.escape(r["map"])}</h2><a href="check_{r["year"]}.jpg"><img src="check_{r["year"]}.jpg" loading="lazy"></a>'
                f'<div class="cs"><h3>Souběžné budovy</h3><ul>{cases or "<li>žádné</li>"}</ul>' + (f'<h3>Navíc proti mapě (největší)</h3><ul>{excs or "<li>žádné</li>"}</ul>' if 'extra' in r else '') + '</div></section>')
page = f"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kontrola půdorysů</title>
<style>body{{font:14px/1.5 system-ui;margin:0;padding:16px;background:#f6f5f1;color:#1f2427}}table{{border-collapse:collapse;background:#fff}}td,th{{border:1px solid #ddd;padding:4px 8px;text-align:right}}
td:nth-child(2){{text-align:left}}.bad{{background:#fde2e2;font-weight:600}}section{{display:grid;grid-template-columns:minmax(0,700px) minmax(0,1fr);gap:16px;margin:24px 0;border-top:1px solid #ccc;padding-top:12px}}
section h2{{grid-column:1/-1;margin:0}}img{{width:100%;border:1px solid #ccc}}.lg span{{display:inline-block;padding:0 8px;margin-right:6px;border-radius:3px;color:#fff}}
@media(max-width:900px){{section{{display:block}}}}</style></head><body>
<h1>Kontrola půdorysů proti podkladovým mapám</h1>
<p class="lg">Půdorysy budov modelu stojících v roce, kdy mapa začíná platit: <span style="background:#28a028">mapa je ukazuje</span><span style="background:#ffa500">slabě</span>
<span style="background:#e60000">navíc (mapa tam nic nemá)</span><span style="background:#c800c8">dvě budovy na stejném místě</span><span style="background:#1e5a96">mapa bez detekce budov</span></p>
<table><tr><th>rok</th><th>mapa</th><th>budov</th><th>ok</th><th>slabě</th><th>navíc</th><th>z toho generované</th><th>souběh</th></tr>{''.join(rows)}</table>
{''.join(figs)}</body></html>"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
print('written', os.path.join(OUT, 'index.html'))
