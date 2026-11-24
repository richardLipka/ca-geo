"""Static web page: a guide to the Plzeň growth video (chapters with short texts, video jumps, stills,
an overview timeline) with previews of every source the model uses.

The page is written to data/historic/growth/site/ (not versioned: it contains reproductions of
third-party maps). Each picture is labelled with its licence; works under copyright are shown as
quotations (citace, § 31 odst. 1 písm. a) zákona č. 121/2000 Sb.) with author, work and source.

Inputs: scripts/sources_site.json (catalogue and chapters, bilingual), ../sources.json (vedute),
data/historic/growth/web/model.json, scripts/fort_1781.json, the source images under data/,
the HAM atlas and ČSÚ lexicon PDFs, and the encoded video (stills are cut from it).

usage: python sources_site.py        (run from anywhere; paths are relative to the repository)
needs: pillow, numpy, pymupdf, imageio-ffmpeg
"""
import html, json, math, os, subprocess
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'data', 'historic', 'growth', 'site')
IMG = os.path.join(OUT, 'img')
VIDEO = os.path.join(ROOT, 'data', 'historic', 'growth', 'video', 'plzen-growth-1295-2020.mp4')
os.makedirs(IMG, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None

CAT = json.load(open(os.path.join(HERE, 'sources_site.json'), encoding='utf-8'))
SRC = json.load(open(os.path.join(HERE, '..', 'sources.json'), encoding='utf-8'))
M = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'web', 'model.json'), encoding='utf-8'))
esc = html.escape


def L(cs, en):
    return f'<span class="cs">{cs}</span><span class="en">{en}</span>'


def LS(cs, en):  # inside SVG: an HTML <span> would end the SVG element in the HTML parser
    return f'<tspan class="cs">{cs}</tspan><tspan class="en">{en}</tspan>'


LIC = {  # class → (badge cs, badge en, css class)
    'pd': ('Volné dílo', 'Public domain', 'open'),
    'cc0': ('CC0', 'CC0', 'open'),
    'ccbysa': ('CC BY-SA', 'CC BY-SA', 'open'),
    'ccby': ('CC BY 4.0', 'CC BY 4.0', 'open'),
    'ccbyncnd': ('Citace · CC BY-NC-ND', 'Quotation · CC BY-NC-ND', 'cite'),
    'cite': ('Citace (§ 31 AZ)', 'Quotation (§ 31 Czech Copyright Act)', 'cite'),
    'own': ('Vlastní výstup', 'Own output', 'own'),
}


def lic_of(s):
    s = s.lower()
    if 'nc-nd' in s: return 'ccbyncnd'
    if 'by-sa' in s: return 'ccbysa'
    if 'cc0' in s: return 'cc0'
    if '©' in s or 'research' in s: return 'cite'
    return 'pd'


# ---------------------------------------------------------------- catalogue
SHORT = {'te-1618': 'Theatrum Eur. 1618', 'zcm-1781': 'Plán ZČM 1781', 'hollar-p812': 'Hollar 1602–40', 'bodenehr-1700': 'Bodenehr 1650–1700',
         'ottheinrich-1536': 'Ottheinrich 1536', 'schabat-1864': 'Schabat 1864'}
items = []
for s in SRC:
    if s['id'] not in CAT['vedute']: continue
    u = CAT['vedute'][s['id']]
    d = s['depicted']
    items.append({'id': s['id'], 'group': 'vedute', 'lic': lic_of(s['licence']), 'year': d, 'made': s['made'],
                  'short': SHORT.get(s['id'], f"{s['id'].split('-')[0].capitalize()} {d[0]}"), 'title': s['title'], 'holder': s['holder'],
                  'licence': s['licence'], 'url': s['page'], 'img': {'src': f"data/historic/sources/{s['file']}"},
                  'cs': u['cs'], 'en': u['en']})
SIEGE = ['te-1618', 'isselburg-1618', 'keller-1619', 'hogenberg-1619']
mem = [i for i in items if i['id'] in SIEGE]
if mem:
    items = [i for i in items if i['id'] not in SIEGE]
    items.append({'id': 'siege-1618', 'group': 'vedute', 'lic': 'ccbysa', 'year': [1618, 1618], 'made': '1618–1635', 'short': 'Obléhání 1618 (4×)',
                  'title': 'Obléhání Plzně Mansfeldem 1618: čtyři vyobrazení (Theatrum Europaeum, Isselburg, Keller, Hogenberg)',
                  'members': mem, 'img': {'grid': [m['img']['src'] for m in mem]}, 'url': mem[0]['url'],
                  'cs': CAT['siege']['cs'], 'en': CAT['siege']['en']})
items.sort(key=lambda i: i['year'][0])
for it in CAT['items']:
    it = dict(it)
    if it['group'] == 'plans':
        it.setdefault('holder', f"Statutární město Plzeň, GIS_Historicke / {it['layer']}")
        it.setdefault('url', f"https://ags.plzen.eu/arcgis/rest/services/GIS_Historicke/{it['layer']}/MapServer")
    items.append(it)
byid = {i['id']: i for i in items}
# reference numbers for every third-party source, in page order
# reference numbers in the order of the chapters
refs = []
for ch in CAT['chapters']:
    for i in ch['items']:
        if i in byid and byid[i]['lic'] != 'own' and byid[i] not in refs: refs.append(byid[i])
for n, i in enumerate(refs, 1): i['ref'] = n


def ref_html(text):
    """[id] in catalogue text → link to the reference number"""
    import re
    return re.sub(r'\[([a-z0-9-]+)\]', lambda m: f'<a class="rf" href="#ref-{m[1]}">[{byid[m[1]]["ref"]}]</a>' if m[1] in byid and 'ref' in byid[m[1]] else m[0], text)


# ---------------------------------------------------------------- images
def save(im, name, big=1800, small=560):
    im = im.convert('RGB')
    a = im.copy(); a.thumbnail((big, big), Image.LANCZOS); a.save(os.path.join(IMG, name + '.jpg'), quality=86)
    b = im.copy(); b.thumbnail((small, small), Image.LANCZOS); b.save(os.path.join(IMG, name + '_t.jpg'), quality=82)
    return a.size


def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); return bg
    return im


def autocrop(im):
    a = np.asarray(im.convert('RGBA'))
    m = a[..., 3] > 0
    m &= ~((a[..., 0] > 245) & (a[..., 1] > 245) & (a[..., 2] > 245))
    ys, xs = np.nonzero(m)
    if not len(xs): return im
    p = int(0.02 * max(im.size))
    return im.crop((max(0, xs.min() - p), max(0, ys.min() - p), min(im.width, xs.max() + p), min(im.height, ys.max() + p)))


def terrain(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    h = (a[..., 0] * 256 + a[..., 1]) * 0.1
    gy, gx = np.gradient(h, 10.0)
    shade = np.clip(0.55 + (-gx * 0.6 + gy * 0.6) / np.sqrt(1 + gx ** 2 + gy ** 2), 0, 1)
    t = (h - h.min()) / max(1e-6, np.ptp(h))
    stops = np.array([[61, 122, 87], [151, 179, 103], [214, 196, 132], [166, 120, 82], [240, 236, 230]], float)
    pos = t * (len(stops) - 1); i = np.clip(pos.astype(int), 0, len(stops) - 2); f = (pos - i)[..., None]
    rgb = (stops[i] * (1 - f) + stops[i + 1] * f) * (0.45 + 0.55 * shade[..., None])
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


_pdfs = {}


def pdf_page(path, page, dpi=130):
    import pymupdf
    d = _pdfs.setdefault(path, pymupdf.open(os.path.join(ROOT, path)))
    pix = d[page - 1].get_pixmap(dpi=dpi)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples if pix.n == 3 else pix.samples)  # rgb, no alpha


for it in items:
    spec = it.get('img')
    if not spec: continue
    try:
        if 'pdf' in spec:
            im = pdf_page(spec['pdf'], spec['page'])
        elif 'grid' in spec:
            ims = [flat(Image.open(os.path.join(ROOT, q))).convert('RGB') for q in spec['grid']]
            cw = 900; tiles = []
            for i in ims: i = i.copy(); i.thumbnail((cw, cw)); tiles.append(i)
            ch = max(t.height for t in tiles)
            im = Image.new('RGB', (2 * cw + 10, 2 * ch + 10), 'white')
            for k, t in enumerate(tiles): im.paste(t, ((k % 2) * (cw + 10) + (cw - t.width) // 2, (k // 2) * (ch + 10) + (ch - t.height) // 2))
        elif 'strip' in spec:
            ims = [flat(Image.open(os.path.join(ROOT, p))) for p in spec['strip']]
            hh = min(i.height for i in ims); ims = [i.resize((round(i.width * hh / i.height), hh)) for i in ims]
            im = Image.new('RGB', (sum(i.width for i in ims) + 20 * (len(ims) - 1), hh), 'white')
            x = 0
            for i in ims: im.paste(i.convert('RGB'), (x, 0)); x += i.width + 20
        elif spec.get('terrain'):
            im = terrain(os.path.join(ROOT, spec['src']))
        else:
            im = Image.open(os.path.join(ROOT, spec['src']))
            if spec.get('crop') == 'auto': im = autocrop(im)
            im = flat(im)
        it['size'] = save(im, it['id'])
        print('img', it['id'], it['size'])
    except Exception as e:  # missing local file → card without picture
        print('MISSING', it['id'], e); it['img'] = None

# ---------------------------------------------------------------- video stills
SEG = [(1295, 1600, 16), (1600, 1720, 8), (1720, 1780, 16), (1780, 1840, 8), (1840, 1960, 4.5), (1960, 2020, 5)]  # growth3d.ts PACE: years per second


def t_of(y):
    t = 0
    for a, b, r in SEG:
        if y <= a: break
        t += (min(y, b) - a) / r
    return max(0, t - 1 / 30)


stills = []
if os.path.exists(VIDEO):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    for y in sorted({y for ch in CAT['chapters'] for y in ch['stills']}):
        p = os.path.join(IMG, f'still_{y}.png')
        if not os.path.exists(p):
            subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', f'{t_of(y):.3f}', '-i', VIDEO, '-frames:v', '1', p], check=True)
        save(Image.open(p), f'still_{y}', big=1600, small=640); os.remove(p); stills.append(y)
    print('stills', stills)

# ---------------------------------------------------------------- flipbook of map overlays
# Every map registered to the model is cut to the same 1.6 × 1.6 km frame around the old town; a transparent
# layer shows the model buildings standing in that year (generated houses lighter, fortification olive / blue).
import cv2
FLIP = os.path.join(OUT, 'flip'); os.makedirs(FLIP, exist_ok=True)
GROWTH = os.path.join(ROOT, 'data', 'historic', 'growth')
BB = (-826900, -1074200, -817900, -1065200)
FC = (-822380.0, -1069700.0); FS = 1600.0; FR = 1.25; FN = int(FS / FR)
crop_M = np.array([[1 / FR, 0, -(FC[0] - FS / 2) / FR], [0, -1 / FR, (FC[1] + FS / 2) / FR], [0, 0, 1]])
rdcv = lambda f: cv2.imdecode(np.fromfile(f, np.uint8), cv2.IMREAD_UNCHANGED)


def warp_to_crop(img, H_img2map, field=None):
    Hc = crop_M @ (np.r_[np.asarray(H_img2map, float), [[0, 0, 1]]] if np.asarray(H_img2map).shape == (2, 3) else np.asarray(H_img2map, float))
    if img.ndim == 3 and img.shape[2] == 4:
        alpha = img[..., 3]; img = img[..., :3]
    else:
        alpha = np.full(img.shape[:2], 255, np.uint8)
    if field is not None:
        fm = np.zeros(img.shape[:2], np.uint8); cv2.fillPoly(fm, [np.array(field, np.int32)], 255); alpha = np.minimum(alpha, fm)
    w = cv2.warpPerspective(img, Hc, (FN, FN), flags=cv2.INTER_AREA, borderValue=(235, 235, 232))
    a = cv2.warpPerspective(alpha, Hc, (FN, FN), flags=cv2.INTER_NEAREST)
    bg = np.full_like(w, 236); w[a < 128] = bg[a < 128]
    return w


frames = []
H57 = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'ham57_map.json'), encoding='utf-8'))
FPM = json.load(open(os.path.join(HERE, 'fort_plans_map.json'), encoding='utf-8'))
FPJ = json.load(open(os.path.join(HERE, 'fort_plans.json'), encoding='utf-8'))
pages = os.path.join(ROOT, 'data', 'reference', 'hiu-atlas', 'pages')
early = [(1410, 'mapa 57 (rekonstrukce cca 1410)', 'map 57 (reconstruction c. 1410)', os.path.join(pages, 'p090_300.png'), H57['affine'], None, 'ham-57')]
te = json.load(open(os.path.join(HERE, 'te1618_points.json'), encoding='utf-8'))
Hte, _ = cv2.findHomography(np.array([q['img'] for q in te], np.float32), np.array([q['map'] for q in te], np.float64))
early.append((1618, 'Theatrum Europaeum 1618', 'Theatrum Europaeum 1618', os.path.join(ROOT, 'data', 'historic', 'sources', 'te-1618.jpg'), Hte, None, 'siege-1618'))
for pid, ref in (('1658', 'ham-5'), ('1703', 'ham-6')):
    ox, oy = FPJ['plans'][pid]['origin']
    A = np.r_[np.array(FPM['plans'][pid]['affine']), [[0, 0, 1]]] @ np.array([[0.5, 0, -ox / 2], [0, 0.5, -oy / 2], [0, 0, 1]])
    early.append((int(pid), f'plán opevnění {pid}', f'fortification plan {pid}', os.path.join(pages, f'p04{3 if pid == "1658" else 4}_300.png'), A, None, ref))
RAWNAMES = [('1781', 1781, 'plan-1781'), ('1821', 1821, 'plan-1821'), ('1840_cadastre', 1840, 'plan-1840'), ('1840_vm2', 1841, 'vm2'), ('1864', 1864, 'plan-1864'),
            ('1873', 1873, 'plan-1873'), ('1877_mesto', 1877, 'plan-1877'), ('1880_vm3', 1880, 'vm3'), ('1881', 1881, 'plan-1881'), ('1891', 1891, 'plan-1891'),
            ('1893', 1893, 'plan-1893'), ('1895', 1895, 'plan-1895'), ('1902', 1902, 'plan-1902'), ('1908', 1908, 'plan-1908'), ('1912', 1912, 'plan-1912'),
            ('1926', 1926, 'plan-1926'), ('1931', 1931, 'plan-1931'), ('1938', 1938, 'plan-1938'), ('1947', 1947, 'plan-1947'), ('1950', 1950, 'plan-1950'),
            ('1951', 1951, 'plan-1951'), ('1953_orto', 1953, 'orto-1953'), ('1971', 1971, 'plan-1971'), ('1972', 1972, 'plan-1972'), ('2001_orto', 2001, 'orto-2001'),
            ('2025_ztm', 2020, 'ztm')]
RAWM = np.array([[2.5, 0, BB[0]], [0, -2.5, BB[3]]])
MODEL = json.load(open(os.path.join(GROWTH, 'web', 'model.json'), encoding='utf-8'))
OXY = MODEL['origin']; CLS = MODEL['classes']


def overlay(year):
    im = np.zeros((FN, FN, 4), np.uint8)
    col = {'fort': (69, 143, 125, 210), 'ditch': (88, 122, 138, 200), 'moat': (196, 134, 63, 220), 'landmark': (140, 46, 122, 235)}
    for b in range(MODEL['n']):
        fr, to = MODEL['from'][b], MODEL['to'][b]; g = MODEL['gaps'][b]
        if not (fr <= year < to) or (g[0] <= year < g[1]) or (g[2] <= year < g[3]): continue
        r = MODEL['rings'][b]
        pts = np.array([[(OXY[0] + r[i] / 10 - (FC[0] - FS / 2)) / FR, ((FC[1] + FS / 2) - (OXY[1] + r[i + 1] / 10)) / FR] for i in range(0, len(r), 2)], np.int32)
        if pts[:, 0].max() < 0 or pts[:, 1].max() < 0 or pts[:, 0].min() > FN or pts[:, 1].min() > FN: continue
        c = CLS[MODEL['cls'][b]]
        gen = MODEL['ids'][b].startswith('gen:')
        cv2.fillPoly(im, [pts], col.get(c, (60, 60, 200, 150) if gen else (40, 40, 190, 205)))
    cv2.imencode('.png', im)[1].tofile(os.path.join(FLIP, f'o_{year}.png'))


for year, cs, en, path, H, field, ref in early:
    if not os.path.exists(path): continue
    cv2.imencode('.jpg', warp_to_crop(rdcv(path)[..., :3], H, field), [cv2.IMWRITE_JPEG_QUALITY, 84])[1].tofile(os.path.join(FLIP, f'f_{year}.jpg'))
    overlay(year); frames.append((year, cs, en, ref))
for name, year, ref in RAWNAMES:
    f = next((x for x in os.listdir(os.path.join(GROWTH, 'raw')) if x.split('.')[0] == name), None)
    if not f: continue
    cv2.imencode('.jpg', warp_to_crop(rdcv(os.path.join(GROWTH, 'raw', f)), RAWM), [cv2.IMWRITE_JPEG_QUALITY, 84])[1].tofile(os.path.join(FLIP, f'f_{year}.jpg'))
    overlay(year); frames.append((year, byid[ref]['short'] if ref in byid else name, byid[ref]['short'] if ref in byid else name, ref))
frames.sort()
print('flipbook frames', len(frames))

# ---------------------------------------------------------------- scale and SVG helpers
Y0, YB, Y1 = 1280, 1780, 2030
W, PADL, PADR = 1100, 150, 20


def X(y):  # piecewise linear: 1280–1780 on 36 % of the width, 1780–2030 on 64 %
    span = W - PADL - PADR
    if y <= YB: return PADL + (y - Y0) / (YB - Y0) * span * 0.36
    return PADL + span * 0.36 + (min(y, Y1) - YB) / (Y1 - YB) * span * 0.64


def axis(y_top, y_bot):
    ticks = [1300, 1400, 1500, 1600, 1700, 1780, 1800, 1850, 1900, 1950, 2000]
    s = [f'<line x1="{X(Y0):.1f}" x2="{X(Y1):.1f}" y1="{y_bot}" y2="{y_bot}" class="ax"/>']
    for t in ticks:
        s.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{y_top}" y2="{y_bot}" class="grid{" brk" if t == YB else ""}"/>'
                 f'<text x="{X(t):.1f}" y="{y_bot + 14}" class="tick" text-anchor="middle">{t}</text>')
    return ''.join(s)


def lanes(objs, gap=6):
    """objs: dicts with x0, x1 (px, incl. label) → adds 'lane'"""
    ends = []
    for o in sorted(objs, key=lambda o: o['x0']):
        for k, e in enumerate(ends):
            if e + gap < o['x0']: o['lane'] = k; ends[k] = o['x1']; break
        else: o['lane'] = len(ends); ends.append(o['x1'])
    return len(ends)


def tw(s, px=6.2):
    return len(s) * px


# ---- 3. fortification ----
FORT = [  # label cs, label en, built, decayed-from, removed, note-ref
    ('Hradba (středověká)', 'Medieval wall', 1320, None, 1828, 'odstraňována 1795–1849, poslední úsek 1893–99'),
    ('Parkán S / J', 'Zwinger N / S', 1420, None, 1849, 'podle nejbližší brány'),
    ('Parkán Z', 'Zwinger W', 1420, None, 1828, 'okružní sady 1828'),
    ('Příkop', 'Moat', 1320, None, 1822, 'zasypáván 1795–1822'),
    ('Litická brána', 'Litice gate', 1320, None, 1804, ''),
    ('Pražská brána', 'Prague gate', 1320, None, 1822, ''),
    ('Říšská brána', 'Imperial gate', 1320, None, 1833, ''),
    ('Saská brána', 'Saxon gate', 1320, None, 1849, ''),
    ('Bastion Z (dílo b)', 'W bastion (work b)', 1645, 1760, 1828, 'plán 1658 b; 1821 ano, 1840 ne'),
    ('Ravelin SZ (d)', 'NW ravelin (d)', 1645, 1760, 1810, 'na plánu 1821 chybí'),
    ('Dílo JZ (c)', 'SW work (c)', 1645, 1760, 1805, ''),
    ('Dílo J (a)', 'S work (a)', 1645, 1760, 1800, ''),
    ('Reduta JV (h)', 'SE redoubt (h)', 1645, 1760, 1833, 'u Říšské brány'),
    ('Valy S / V / SV', 'Ramparts N / E / NE', 1645, 1760, 1822, ''),
    ('Bastion SV', 'NE bastion', 1645, 1760, 2025, 'dochován, sady 5. května'),
    ('Díla Ziznera 1703', 'Zizner works 1703', 1703, None, 1760, 'nejisté, nemodelováno'),
]


def svg_fort():
    s, y = [], 10
    for cs, en, a, dec, b, note in FORT:
        unc = 'Zizner' in en
        s.append(f'<text x="8" y="{y + 11}" class="rowlab s">{LS(cs, en)}</text>')
        if a == 1645:  # building phase 1645–1658 (plan 1658)
            s.append(f'<rect x="{X(1645):.1f}" y="{y + 2}" width="{X(1658) - X(1645):.1f}" height="12" class="f build"/>')
            a = 1658
        end1 = dec or b
        s.append(f'<rect x="{X(a):.1f}" y="{y + 2}" width="{X(end1) - X(a):.1f}" height="12" class="f {"unc" if unc else "stand"}"/>')
        if dec: s.append(f'<rect x="{X(dec):.1f}" y="{y + 2}" width="{X(b) - X(dec):.1f}" height="12" class="f decay"/>')
        if b < 2025: s.append(f'<text x="{X(b) + 4:.1f}" y="{y + 12}" class="lab">{b}{" · " + esc(note) if note else ""}</text>')
        elif note: s.append(f'<text x="{X(b) - 4:.1f}" y="{y + 12}" class="lab" text-anchor="end">{esc(note)}</text>')
        y += 18
    for k, (yy, cs, en) in enumerate(((1645, 'šance 1645–58 (plán 1658)', 'earthworks 1645–58 (1658 plan)'), (1760, 'chátrání od 1760 (plán 1781, leg. 13)', 'decay from 1760 (1781 plan, key 13)'), (1795, 'bourání 1795–1849', 'demolition 1795–1849'))):
        s.append(f'<line x1="{X(yy):.1f}" x2="{X(yy):.1f}" y1="6" y2="{y + 24 + 14 * k}" class="mark"/><text x="{X(yy) + 3:.1f}" y="{y + 28 + 14 * k}" class="lab i">{LS(cs, en)}</text>')
    return f'<svg viewBox="0 0 {W} {y + 72}" class="tl">{axis(6, y + 4)}{"".join(s)}</svg>'


# ---- overview timeline: chapters, events, building count ----
GROUND = {1781: 'plan-1781', 1821: 'plan-1821', 1840: 'plan-1840', 1877: 'plan-1877', 1881: 'plan-1881', 1893: 'plan-1893', 1902: 'plan-1902',
          1908: 'plan-1908', 1926: 'plan-1926', 1938: 'plan-1938', 1947: 'plan-1947', 1953: 'orto-1953', 2001: 'orto-2001', 2015: 'ztm'}


def ground_of(y):
    g = [q for q in M['grounds'] if q['year'] <= y + 0.01][-1]
    return byid.get(GROUND.get(g['year'], ''))


def counts():
    fr, to, cl = np.array(M['from'], float), np.array(M['to'], float), np.array(M['cls'])
    keep = ~np.isin(cl, [M['classes'].index(c) for c in ('fort', 'landmark', 'moat') if c in M['classes']])
    ys = np.arange(1295, 2021, 5)
    return ys, [int(((fr <= y) & (to > y) & keep).sum()) for y in ys]


def svg_overview():
    ys, cs_ = counts(); mx = max(cs_)
    s = []
    top, bot = 64, 150
    Yp = lambda c: bot - c / mx * (bot - top)
    for k, ch in enumerate(CAT['chapters']):
        a, b = ch['years']; x0, x1 = X(a), X(b + 1)
        s.append(f'<a href="#{ch["id"]}" class="chap" data-t="{t_of(a):.2f}"><rect x="{x0:.1f}" y="6" width="{x1 - x0 - 1:.1f}" height="{bot - 6}" class="cb{k % 2}"/>'
                 f'<text x="{(x0 + x1) / 2:.1f}" y="22" class="ct" text-anchor="middle">{k + 1}</text><title>{a}–{b}: {esc(ch["cs"])}</title></a>')
    pts = ' '.join(f'{X(y):.1f},{Yp(c):.1f}' for y, c in zip(ys, cs_))
    s.append(f'<polygon points="{X(ys[0]):.1f},{bot} {pts} {X(ys[-1]):.1f},{bot}" class="area"/><polyline points="{pts}" class="line"/>')
    objs = [{'e': e, 'x0': X(e['year']) - 3, 'x1': X(e['year']) + 6 + tw(str(e['year']), 6.5)} for e in M['events']]
    n = lanes(objs, 2)
    for o in objs:
        x, yy = X(o['e']['year']), 34 + 13 * o['lane']
        s.append(f'<circle cx="{x:.1f}" cy="{yy - 3}" r="2.6" class="evd"/><text x="{x + 4:.1f}" y="{yy}" class="lab sm">{o["e"]["year"]}</text>'
                 f'<title>{o["e"]["year"]} – {esc(o["e"]["cs"])}</title>')
    s.append(f'<text x="8" y="{bot - 4}" class="rowlab s">{LS("Počet budov", "Buildings")}</text>')
    s.append(f'<text x="8" y="22" class="rowlab s">{LS("Kapitoly", "Chapters")}</text><text x="8" y="40" class="rowlab s">{LS("Události", "Events")}</text>')
    return f'<svg viewBox="0 0 {W} {bot + 22}" class="tl">{axis(6, bot)}{"".join(s)}</svg>'


# ---------------------------------------------------------------- page parts
def card(it):
    lc = LIC[it['lic']]
    yrs = f"{it['year'][0]}" + (f"–{it['year'][1]}" if it['year'][1] != it['year'][0] else '')
    ref = f'<span class="refno">[{it["ref"]}]</span> ' if 'ref' in it else ''
    pic = (f'<button class="pic" data-full="img/{it["id"]}.jpg" aria-label="{esc(it["title"])}"><img loading="lazy" src="img/{it["id"]}_t.jpg" alt=""></button>'
           if it.get('img') else '')
    if it.get('members'):
        cap = '<br>'.join(f'{esc(m["title"])}. {esc(m["holder"])}. {esc(m["licence"])}. <a href="{esc(m["url"])}" target="_blank" rel="noopener">{L("zdroj", "source")} ↗</a>' for m in it['members'])
    elif it['lic'] == 'own':
        cap = L('Vlastní výstup', 'Own output')
    elif lc[2] == 'cite':
        cap = L(f'Citace: {esc(it["title"])}. {esc(it.get("holder", ""))}.', f'Quotation: {esc(it["title"])}. {esc(it.get("holder", ""))}.')
    else:
        cap = f'{esc(it["title"])}. {esc(it.get("holder", ""))}. {esc(it.get("licence", lc[1]))}.'
    link = f' <a href="{esc(it["url"])}" target="_blank" rel="noopener">{L("zdroj", "source")} ↗</a>' if it.get('url') and not it.get('members') else ''
    return (f'<article class="card" id="{it["id"]}">{pic}<div class="body">'
            f'<div class="meta"><span class="badge {lc[2]}">{L(lc[0], lc[1])}</span><span class="yr">{yrs}</span></div>'
            f'<h4>{ref}{esc(it["title"])}</h4><p class="use">{L(ref_html(esc(it["cs"])), ref_html(esc(it["en"])))}</p>'
            f'<p class="cap">{cap}{link}</p></div></article>')


def still_cap(y):
    g = ground_of(y)
    if not g: return f'<b>{y}</b>'
    return f'<b>{y}</b> · {L("podklad", "ground")}: {esc(g["short"])} <a class="rf" href="#ref-{g["id"]}">[{g["ref"]}]</a>'


def mmss(t):
    return f'{int(t // 60)}:{int(t % 60):02d}'


def chapter(k, ch):
    a, b = ch['years']
    evs = [e for e in M['events'] if a <= e['year'] <= b]
    ev = ''.join(f'<li><b>{e["year"]}</b> {L(esc(e["cs"]), esc(e["en"]))}</li>' for e in evs)
    st = ''.join(f'<figure class="still"><button class="pic" data-full="img/still_{y}.jpg" data-t="{t_of(y):.2f}"><img loading="lazy" src="img/still_{y}_t.jpg" alt="{y}"></button>'
                 f'<figcaption>{still_cap(y)}</figcaption></figure>' for y in ch['stills'] if y in stills)
    cards = ''.join(card(byid[i]) for i in ch['items'] if i in byid)
    fort = f'<h3>{L("Opevnění: stavba, chátrání a zánik", "Fortification: building, decay and removal")}</h3><div class="box">{svg_fort()}</div>' if ch.get('fort') else ''
    return (f'<section class="ch" id="{ch["id"]}" data-a="{a}" data-b="{b}">'
            f'<div class="chh"><span class="num">{k + 1}</span><div><div class="yrs">{a}–{b}</div><h2>{L(esc(ch["cs"]), esc(ch["en"]))}</h2></div>'
            f'<button class="seek" data-t="{t_of(a):.2f}">▶ {mmss(t_of(a))}</button></div>'
            f'<p class="txt">{L(esc(ch["text_cs"]), esc(ch["text_en"]))}</p>'
            + (f'<div class="stills">{st}</div>' if st else '')
            + (f'<ul class="evs">{ev}</ul>' if ev else '')
            + fort
            + f'<h3>{L("Podklady", "Sources")}</h3><div class="cards">{cards}</div></section>')


def reflist():
    s = []
    for it in refs:
        lc = LIC[it['lic']]
        yrs = it.get('made') or (f"{it['year'][0]}" + (f"–{it['year'][1]}" if it['year'][1] != it['year'][0] else ''))
        if it.get('members'):
            s.append(f'<li id="ref-{it["id"]}"><a href="#{it["id"]}">{esc(it["title"])}</a>:<ul>' + ''.join(
                f'<li>{esc(m["title"])}. {esc(m["made"])}. {esc(m["holder"])}. {esc(m["licence"])}. <a href="{esc(m["url"])}" target="_blank" rel="noopener">{L("zdroj", "source")} ↗</a></li>' for m in it['members']) + '</ul></li>')
            continue
        s.append(f'<li id="ref-{it["id"]}"><a href="#{it["id"]}">{esc(it["title"])}</a>. {esc(str(yrs))}. {esc(it.get("holder", ""))}. '
                 f'<span class="badge {lc[2]} sm">{L(lc[0], lc[1])}</span>'
                 + (f' <a href="{esc(it["url"])}" target="_blank" rel="noopener">{L("zdroj", "source")} ↗</a>' if it.get('url') else '') + '</li>')
    return '<ol class="refs">' + ''.join(s) + '</ol>'


chapters_html = ''.join(chapter(k, ch) for k, ch in enumerate(CAT['chapters']))
FLIPDATA = json.dumps([{'y': y, 'cs': cs, 'en': en, 'ref': byid[r]['ref'] if r in byid and 'ref' in byid[r] else None, 'id': r} for y, cs, en, r in frames], ensure_ascii=False)
flip_html = (f'<section id="flip" class="ch"><div class="chh"><div><div class="yrs">{len(frames)} {L("map", "maps")}</div>'
             f'<h2>{L("Překryvy map v jednom výřezu", "Map overlays in one frame")}</h2></div></div>'
             f'<p class="txt">{L("Stejný výřez 1,6 × 1,6 km kolem jádra ve všech mapách zarovnaných na model, od rekonstrukce kolem roku 1410 po dnešní mapu. Vrstva navrchu ukazuje budovy modelu stojící v roce mapy (sytě skutečné půdorysy, světle generované domy, olivově opevnění, modře příkop).", "The same 1.6 × 1.6 km frame around the core in every map registered to the model, from the reconstruction of c. 1410 to the present map. The layer on top shows the model buildings standing in the map\'s year (strong: real footprints, light: generated houses, olive: fortification, blue: moat).")}</p>'
             f'<div class="flip"><div class="flip-frame"><img id="fimg" alt=""><img id="fov" alt=""><div class="flip-year" id="fyear"></div></div>'
             f'<div class="tools"><button id="fplay">▶</button><input type="range" id="frange" min="0" max="{len(frames) - 1}" value="0" style="flex:1">'
             f'<label><input type="checkbox" id="fshow" checked> {L("model", "model")}</label><input type="range" id="fop" min="0" max="1" step="0.05" value="0.6" style="width:90px"></div>'
             f'<div class="fstrip" id="fstrip"></div><p class="cap" id="fcap"></p></div></section>')
toc = ''.join(f'<li><a href="#{ch["id"]}" data-t="{t_of(ch["years"][0]):.2f}"><span>{ch["years"][0]}</span> {L(esc(ch["cs"]), esc(ch["en"]))}</a></li>' for ch in CAT['chapters'])
n_cite = sum(1 for i in items if LIC[i['lic']][2] == 'cite'); n_open = sum(1 for i in items if LIC[i['lic']][2] == 'open')

CSS = """
:root{--bg:#f7f6f2;--fg:#1f2427;--mut:#5d676f;--card:#fff;--line:#d9dcd6;--band:#eeede7;--acc:#8c3b2e;
--cite:#b5651d;--citebg:#fbecd9;--open:#2f7a4d;--openbg:#e1f1e6;--own:#2d5f8f;--ownbg:#e0ebf6;--decay:#c9a27a;--grid:#e4e3dc;--b0:#efe9dc;--b1:#e6eee6}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17191b;--fg:#e8e6e1;--mut:#a0a7ad;--card:#212427;--line:#383c40;--band:#1d2023;
--acc:#e08a74;--cite:#f0a35e;--citebg:#3d2b17;--open:#6cc28f;--openbg:#18301f;--own:#7fb1e3;--ownbg:#172839;--decay:#8a6a4a;--grid:#2b2f33;--b0:#26231d;--b1:#1d2620}}
:root[data-theme=dark]{--bg:#17191b;--fg:#e8e6e1;--mut:#a0a7ad;--card:#212427;--line:#383c40;--band:#1d2023;
--acc:#e08a74;--cite:#f0a35e;--citebg:#3d2b17;--open:#6cc28f;--openbg:#18301f;--own:#7fb1e3;--ownbg:#172839;--decay:#8a6a4a;--grid:#2b2f33;--b0:#26231d;--b1:#1d2620}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 "Segoe UI",system-ui,sans-serif}
html[data-lang=cs] .en,html[data-lang=en] .cs{display:none}
.wrap{max-width:1480px;margin:auto;padding:0 16px;display:grid;grid-template-columns:minmax(0,560px) minmax(0,1fr);gap:28px}
aside{position:sticky;top:0;align-self:start;height:100vh;padding:18px 0;display:flex;flex-direction:column;gap:10px;overflow:auto}
main{padding:18px 0 60px;min-width:0}
h1{font:600 28px/1.2 Georgia,"Times New Roman",serif;margin:0}h2{font:600 22px/1.25 Georgia,serif;margin:0}
h3{font:600 15px/1.3 "Segoe UI",system-ui;margin:18px 0 8px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
h4{font-size:14px;margin:6px 0 3px;line-height:1.35}
.lead{color:var(--mut);margin:6px 0 0}
video{width:100%;border-radius:8px;background:#000;display:block;aspect-ratio:16/9}
.now{display:flex;align-items:baseline;gap:12px}.now .y{font:700 34px/1 Georgia,serif;font-variant-numeric:tabular-nums}.now .c{color:var(--mut)}
.toc{list-style:none;margin:0;padding:0;font-size:14px}.toc li a{display:flex;gap:10px;padding:4px 8px;border-radius:5px;color:var(--fg);text-decoration:none}
.toc li a span{color:var(--mut);font-variant-numeric:tabular-nums;min-width:38px}.toc li a:hover{background:var(--band)}.toc li a.on{background:var(--citebg);color:var(--acc)}
.tools{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-size:13px;color:var(--mut)}
button{font:inherit;cursor:pointer}.tools button{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:5px;padding:2px 9px}
.note{background:var(--citebg);border-left:4px solid var(--cite);padding:9px 12px;border-radius:4px;font-size:13px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px;overflow-x:auto}
svg.tl{display:block;width:100%;min-width:640px;height:auto;font:11px "Segoe UI",system-ui,sans-serif}
svg .ax{stroke:var(--mut)}svg .grid{stroke:var(--grid)}svg .brk{stroke:var(--mut);stroke-dasharray:3 3}
svg .tick{fill:var(--mut);font-size:10.5px}svg .lab{fill:var(--fg)}svg .lab.sm{font-size:9.5px}svg .lab.i{font-style:italic;fill:var(--mut)}
svg .rowlab{fill:var(--fg);font-weight:600;font-size:11.5px}svg .rowlab.s{font-weight:500}
svg .cb0{fill:var(--b0)}svg .cb1{fill:var(--b1)}svg .chap:hover rect{fill:var(--citebg)}svg .ct{fill:var(--mut);font-weight:700}
svg .evd{fill:var(--acc)}svg .area{fill:var(--acc);opacity:.18}svg .line{fill:none;stroke:var(--acc);stroke-width:1.8}
svg .f.build{fill:var(--decay);opacity:.55}svg .f.stand{fill:var(--acc)}svg .f.decay{fill:var(--decay)}
svg .f.unc{fill:none;stroke:var(--acc);stroke-dasharray:4 3}svg .mark{stroke:var(--mut);stroke-dasharray:2 3}
.ch{border-top:1px solid var(--line);padding-top:22px;margin-top:26px;scroll-margin-top:8px}
.chh{display:flex;align-items:center;gap:14px}.num{font:700 30px/1 Georgia,serif;color:var(--acc);min-width:30px}
.yrs{color:var(--mut);font-variant-numeric:tabular-nums;font-size:14px}.seek{margin-left:auto;border:1px solid var(--acc);background:none;color:var(--acc);border-radius:16px;padding:3px 12px;white-space:nowrap}
.seek:hover{background:var(--acc);color:var(--bg)}
.txt{font-size:16px;max-width:760px}
.evs{list-style:none;padding:0;margin:8px 0;font-size:13.5px;columns:2 300px;column-gap:24px}.evs li{break-inside:avoid;margin-bottom:3px}.evs b{color:var(--acc);font-variant-numeric:tabular-nums}
.stills{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:10px 0}
.still{margin:0}.still .pic{height:140px;border-radius:6px}.still figcaption{font-size:12.5px;color:var(--mut);text-align:center}.still b{color:var(--fg)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;scroll-margin-top:12px}
.card:target{outline:3px solid var(--acc)}
.pic{display:block;width:100%;height:160px;border:0;padding:0;background:#e9e7e0;cursor:zoom-in;overflow:hidden}
.pic img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s}.pic:hover img{transform:scale(1.04)}
.body{padding:8px 10px 10px}.meta{display:flex;justify-content:space-between;align-items:center;gap:8px}
.yr{font-variant-numeric:tabular-nums;color:var(--mut);font-size:12.5px}
.badge{font-size:11px;font-weight:600;padding:2px 7px;border-radius:10px;white-space:nowrap}
.badge.cite{background:var(--citebg);color:var(--cite)}.badge.open{background:var(--openbg);color:var(--open)}.badge.own{background:var(--ownbg);color:var(--own)}
.badge.sm{font-size:10.5px;padding:1px 6px}
.refno{color:var(--acc)}.use{margin:3px 0;font-size:13px}.cap{margin:5px 0 0;font-size:11.5px;color:var(--mut)}
.cap a,.refs a,.rf,.note a{color:var(--acc)}
.flip-frame{position:relative;width:100%;max-width:820px;aspect-ratio:1;background:#ddd;border-radius:8px;overflow:hidden}
.flip-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.flip-year{position:absolute;left:12px;top:8px;font:700 34px/1 Georgia,serif;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.8)}
.flip .tools{margin:8px 0;max-width:820px}.fstrip{display:flex;flex-wrap:wrap;gap:4px;max-width:820px}
.fstrip button{font:12px system-ui;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:4px;padding:2px 6px}
.fstrip button.on{background:var(--acc);color:var(--bg);border-color:var(--acc)}
.refs ul{margin:4px 0 0;padding-left:18px}
.refs{font-size:13px;padding-left:28px}.refs li{margin-bottom:5px;scroll-margin-top:12px}.refs li:target{background:var(--citebg)}
#lb{position:fixed;inset:0;background:rgba(10,12,14,.92);display:none;align-items:center;justify-content:center;z-index:10;cursor:zoom-out;padding:16px}
#lb.on{display:flex}#lb img{max-width:100%;max-height:100%;box-shadow:0 4px 30px #000}
footer{color:var(--mut);font-size:12.5px;border-top:1px solid var(--line);margin-top:30px;padding-top:12px}
.org{display:flex;flex-wrap:wrap;align-items:center;gap:18px;background:#1f2427;border-radius:8px;padding:12px 16px;margin-top:10px}
.org a{display:block}.org img{height:34px;display:block}.org .who{color:#e8e6e1;font-size:13px;margin-left:auto}.org .who a{color:#f0b9a8;display:inline}
.links{font-size:13px;color:var(--mut)}.links a{color:var(--acc)}
.cta{display:inline-block;background:var(--acc);color:var(--bg);border-radius:6px;padding:6px 14px;text-decoration:none;font-weight:600}
.state{background:var(--ownbg);border-left:4px solid var(--own);padding:9px 12px;border-radius:4px;font-size:14px;margin-top:12px}.state ul{margin:4px 0 0;padding-left:20px}
@media (max-width:980px){.wrap{display:block}aside{position:static;height:auto;padding-bottom:0}.toc{columns:2}}
@media (max-width:600px){h1{font-size:23px}.toc{columns:1}.pic{height:150px}}
"""

JS = """
const FL=%%FLIP%%, fimg=document.getElementById('fimg'), fov=document.getElementById('fov'), fr=document.getElementById('frange'), fy=document.getElementById('fyear'), fcap=document.getElementById('fcap'), fst=document.getElementById('fstrip');
let fi=0, ft=null;
const fset=i=>{fi=(i+FL.length)%%FL.length; const f=FL[fi]; fimg.src='flip/f_'+f.y+'.jpg'; fov.src='flip/o_'+f.y+'.png'; fr.value=fi; fy.textContent=f.y;
  const ln=document.documentElement.dataset.lang; fcap.innerHTML=(ln==='en'?f.en:f.cs)+(f.ref?' <a class="rf" href="#ref-'+f.id+'">['+f.ref+']</a>':'');
  [...fst.children].forEach((b,k)=>b.classList.toggle('on',k===fi));};
FL.forEach((f,k)=>{const b=document.createElement('button'); b.textContent=f.y; b.onclick=()=>fset(k); fst.appendChild(b);});
fr.oninput=()=>fset(+fr.value);
document.getElementById('fshow').onchange=e=>{fov.style.display=e.target.checked?'block':'none'};
document.getElementById('fop').oninput=e=>{fov.style.opacity=e.target.value}; fov.style.opacity=0.6;
document.getElementById('fplay').onclick=e=>{ if(ft){clearInterval(ft);ft=null;e.target.textContent='▶';} else {ft=setInterval(()=>fset(fi+1),1400);e.target.textContent='❚❚';}};
fset(0);
const h=document.documentElement,lb=document.getElementById('lb'),li=lb.querySelector('img'),v=document.getElementById('vid');
const SEG=%s, CH=[...document.querySelectorAll('section.ch')];
const yearAt=t=>{let y=SEG[0][0];for(const [a,b,r] of SEG){const d=(b-a)/r;if(t<=d)return a+t*r;t-=d;y=b}return y};
const setLang=l=>{h.dataset.lang=l;h.lang=l;try{localStorage.setItem('lang',l)}catch(e){}};
try{const l=localStorage.getItem('lang');if(l)setLang(l)}catch(e){}
document.getElementById('lang').onclick=()=>setLang(h.dataset.lang==='cs'?'en':'cs');
const seek=t=>{v.currentTime=+t;v.play().catch(()=>{})};
document.querySelectorAll('[data-t]').forEach(b=>{if(b.classList.contains('pic'))return;b.addEventListener('click',e=>{seek(b.dataset.t)})});
document.querySelectorAll('button.pic').forEach(b=>b.onclick=()=>{li.src=b.dataset.full;lb.classList.add('on')});
lb.onclick=()=>{lb.classList.remove('on');li.src=''};
addEventListener('keydown',e=>{if(e.key==='Escape')lb.click()});
const yo=document.getElementById('nowy'),co=document.getElementById('nowc'),toc=[...document.querySelectorAll('.toc a')];
let follow=document.getElementById('follow');
v.addEventListener('timeupdate',()=>{const y=Math.min(2020,Math.floor(yearAt(v.currentTime)));yo.textContent=y;
  const k=CH.findIndex(c=>y>=+c.dataset.a&&y<=+c.dataset.b);toc.forEach((a,i)=>a.classList.toggle('on',i===k));
  if(k>=0){co.innerHTML=CH[k].querySelector('h2').innerHTML;if(follow.checked&&!v.paused&&CH[k].dataset.shown!=='1'){CH.forEach(c=>c.dataset.shown='');CH[k].dataset.shown='1';CH[k].scrollIntoView({behavior:'smooth'})}}});
"""

legend = (f'<div class="tools"><span class="badge cite">{L("Citace", "Quotation")}</span>{L("dílo chráněné autorským právem", "work under copyright")}'
          f'<span class="badge open">{L("Volné dílo", "Public domain")}</span>{L("nebo otevřená licence", "or open licence")}'
          f'<span class="badge own">{L("Vlastní výstup", "Own output")}</span></div>')

STATE = [
    ("Budovy: polohy z RÚIAN, tvary z 3D modelu města 2024, datace z historických map a plánů 1410–2025; středověké a raně novověké domy jsou generované podle map a vedut.",
     "Buildings: positions from RÚIAN, shapes from the city 3D model 2024, dating from historical maps and plans 1410–2025; medieval and early modern houses are generated after the maps and vedute."),
    ("Nově: budovy z plánů města 1891, 1895, 1902, 1908 a 1912 (0,5 m) navzájem sesouhlasené – např. blok domů proti kasárnám a areál Škodových závodů.",
     "New: buildings from the town plans of 1891, 1895, 1902, 1908 and 1912 (0.5 m) registered to each other, e.g. the block opposite the barracks and the Škoda works."),
    ("Nově: data dokončení 52 významných staveb podle Wikipedie (divadla, nádraží, synagogy, školy); hvězdicová věznice na Borech stojí celá od roku 1878.",
     "New: completion years of 52 significant buildings after Wikipedia (theatres, stations, synagogues, schools); the star-shaped Bory prison stands complete from 1878."),
    ("Řeky: středověká koryta podle atlasu (mapa 57) a plánu 1658, toky z map 1840 a 1908, od roku 1920 dnešní stav.",
     "Rivers: medieval channels after the atlas (map 57) and the 1658 plan, courses of the 1840 and 1908 maps, the present state from 1920."),
    ("Rozpracováno: ruční doplnění vodních ploch a půdorysů na všech mapách a 3D rekonstrukce budov z vedut podle bodů zadaných uživatelem.",
     "In progress: manual completion of water and footprints on all maps and 3D reconstruction of buildings from the vedute from points entered by the user."),
]
_LOGO = os.path.join(HERE, '..', 'public', 'logos')
if os.path.isdir(_LOGO):
    import shutil
    shutil.copytree(_LOGO, os.path.join(OUT, 'logos'), dirs_exist_ok=True)

page = f"""<!doctype html>
<html lang="cs" data-lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Plzeň 1295–2020: průvodce</title>
<meta name="description" content="Růst Plzně 1295–2020: animace a interaktivní 3D model podle historických map, plánů a vedut / Growth of Plzeň 1295–2020: animation and interactive 3D model after historical maps, plans and vedute.">
<meta property="og:title" content="Růst Plzně 1295–2020 / Growth of Plzeň 1295–2020"><meta property="og:type" content="website"><meta property="og:image" content="img/still_1900_t.jpg"><style>{CSS}</style></head><body>
<div class="wrap">
<aside>
<div class="links"><a class="cs" href="https://home.zcu.cz/~lipka/">← home.zcu.cz/~lipka</a><a class="en" href="https://home.zcu.cz/~lipka/en/">← home.zcu.cz/~lipka</a></div>
<h1>{L("Růst Plzně 1295–2020", "Growth of Plzeň 1295–2020")}</h1>
<p class="lead">{L("Průvodce animací: co video ukazuje a z jakých podkladů vzniklo.", "A guide to the animation: what the video shows and what it is made from.")}</p>
<video id="vid" controls preload="metadata" src="../video/plzen-growth-1295-2020.mp4"></video>
<div class="now"><span class="y" id="nowy">1295</span><span class="c" id="nowc"></span></div>
<ol class="toc">{toc}</ol>
<p><a class="cta" href="model/">{L("Interaktivní 3D model s mapami →", "Interactive 3D model with the maps →")}</a></p>
<div class="links">{L("Katedra informatiky a výpočetní techniky, Fakulta aplikovaných věd, Západočeská univerzita v Plzni", "Department of Computer Science and Engineering, Faculty of Applied Sciences, University of West Bohemia")}</div>
<div class="tools"><label><input type="checkbox" id="follow" checked> {L("posouvat text s videem", "scroll text with the video")}</label><button id="lang">CS / EN</button></div>
</aside>
<main>
<p class="txt">{L("Animace ukazuje, jak se Plzeň během 725 let rozrůstala od založeného města s náměstím po dnešní aglomeraci. Každá budova v ní je skutečný půdorys a dnešní budovy mají svůj skutečný tvar z 3D modelu města. Rok vzniku je odhadnutý z historických map, plánů, rytin a sčítání, takže animace ukazuje pořadí a tempo růstu, ne přesnou podobu jednotlivých domů.",
"The animation shows how Plzeň grew over 725 years, from a founded town around a square to the present city. Every building in it is a real footprint, and present buildings have their real shape from the city 3D model. The year of origin is estimated from historical maps, plans, engravings and censuses, so the animation shows the order and pace of growth, not the exact look of each house.")}</p>
<div class="state"><b>{L("Stav projektu (listopad 2026)", "State of the project (November 2026)")}</b><ul>{''.join('<li>' + L(c, e) + '</li>' for c, e in STATE)}</ul></div>
<div class="box" style="margin-top:12px">{svg_overview()}</div>
{legend}
<div class="note" style="margin-top:10px">{L(f"Ukázky z děl chráněných autorským právem ({n_cite}, štítek „Citace“) jsou užity jako citace podle § 31 odst. 1 písm. a) autorského zákona (č. 121/2000 Sb.) pro účel rozboru a výzkumu, s uvedením autora či držitele, názvu a zdroje. Čísla v závorkách odkazují na <a href='#refs'>seznam zdrojů</a>. Obrázky nejsou určeny k dalšímu šíření.",
f"Excerpts of works under copyright ({n_cite}, label \"Quotation\") are used as quotations under § 31(1)(a) of the Czech Copyright Act (No. 121/2000 Coll.) for analysis and research, with the author or holder, title and source. Numbers in brackets point to the <a href='#refs'>list of sources</a>. The images are not for redistribution.")}</div>
{flip_html}
{chapters_html}
<section id="refs" class="ch"><h2>{L("Zdroje", "Sources")}</h2>{reflist()}</section>
<footer>{L("Projekt ca-geo. Model, animace i tato stránka jsou schematickou rekonstrukcí; datace budov je interpolovaná.", "Project ca-geo. The model, the animation and this page are a schematic reconstruction; building dates are interpolated.")}
<div class="org"><a href="https://www.kiv.zcu.cz/" target="_blank" rel="noopener" title="KIV"><img src="logos/kiv.svg" alt="KIV"></a>
<a href="https://www.fav.zcu.cz/" target="_blank" rel="noopener" title="FAV"><img src="logos/fav.svg" alt="FAV"></a>
<a href="https://www.zcu.cz/" target="_blank" rel="noopener" title="ZČU"><img class="cs" src="logos/zcu.png" alt="ZČU"><img class="en" src="logos/zcu-en.png" alt="UWB"></a>
<span class="who">Richard Lipka · <a href="https://home.zcu.cz/~lipka/" target="_blank" rel="noopener">home.zcu.cz/~lipka</a></span></div></footer>
</main></div>
<div id="lb"><img alt=""></div><script>{(JS % json.dumps(SEG)).replace('%FLIP%', FLIPDATA)}</script></body></html>"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
print('written', os.path.join(OUT, 'index.html'), len(items), 'items', len(refs), 'references')
