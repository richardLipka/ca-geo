"""Cut outlined pieces out of a source image (PNG with transparency) and build a contact
sheet; optionally load the outlines into the historic-mapper project as annotations.

usage: python cut_pieces.py cuts.json source.jpg out_dir [project.json]
cuts.json: {"source": id, "pieces": [{"id", "kind", "shape": [[x,y],...], "entity"?, "conf"?, "label"?}]}
"""
import json, os, sys
import cv2
import numpy as np

def imread(p): return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)
def imwrite(p, img, ext='.png'): ok, b = cv2.imencode(ext, img); b.tofile(p)

cuts_path, img_path, out = sys.argv[1:4]
proj = sys.argv[4] if len(sys.argv) > 4 else None
C = json.load(open(cuts_path, encoding='utf-8')); img = imread(img_path)
os.makedirs(out, exist_ok=True)
tiles = []
for p in C['pieces']:
    poly = np.array(p['shape'], np.int32)
    x, y, w, h = cv2.boundingRect(poly)
    mask = np.zeros((h, w), np.uint8); cv2.fillPoly(mask, [poly - [x, y]], 255)
    rgba = cv2.cvtColor(img[y:y + h, x:x + w], cv2.COLOR_BGR2BGRA); rgba[..., 3] = mask
    imwrite(os.path.join(out, f'{p["id"]}.png'), rgba)
    tiles.append((p, rgba))
# contact sheet: tiles scaled to a common height, wrapped in rows, with captions
TH, ROW_W, PAD = 150, 1800, 12
rows, cur, cw = [], [], 0
for p, t in tiles:
    s = TH / t.shape[0]; w = min(ROW_W, max(1, int(t.shape[1] * s)))
    if cur and cw + w > ROW_W: rows.append(cur); cur, cw = [], 0
    cur.append((p, cv2.resize(t, (w, TH), interpolation=cv2.INTER_AREA))); cw += w + PAD
if cur: rows.append(cur)
sheet = np.full((len(rows) * (TH + 36) + PAD, ROW_W + 200, 3), 250, np.uint8)
for r, row in enumerate(rows):
    xo = PAD; yo = PAD + r * (TH + 36)
    for p, t in row:
        a = t[..., 3:4] / 255.0; region = sheet[yo:yo + TH, xo:xo + t.shape[1]]
        region[:] = (t[..., :3] * a + region * (1 - a)).astype(np.uint8)
        cap = p['id'] if not p.get('entity') else f'{p["id"]} -> {p["entity"]}'
        cv2.putText(sheet, cap[:30], (xo, yo + TH + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (40, 40, 40), 1, cv2.LINE_AA)
        xo += t.shape[1] + PAD
imwrite(os.path.join(out, '_contact_sheet.jpg'), sheet, '.jpg')
print(f'{len(tiles)} pieces -> {out}')
if proj:
    P = json.load(open(proj, encoding='utf-8')); src = C['source']; pre = f'g1618-cut-{src}-'
    P['annotations'] = [a for a in P['annotations'] if not a['id'].startswith(pre)]
    ids = {e['id'] for e in P['entities']}
    for p in C['pieces']:
        sh = p['shape']; c = [sum(q[0] for q in sh) / len(sh), sum(q[1] for q in sh) / len(sh)]
        eid = 'g1618-' + p['entity'] if p.get('entity') and 'g1618-' + p['entity'] in ids else None
        a = {'id': pre + p['id'], 'sourceId': src, 'img': c, 'shape': sh, 'kind': p['kind'], 'entityId': eid,
             'confidence': p.get('conf', 2), 'useAsControl': False}
        if p.get('label'): a['note'] = p['label']
        P['annotations'].append(a)
    json.dump(P, open(proj, 'w', encoding='utf-8', newline='\n'), indent=1, ensure_ascii=False)
    print('annotations', len(P['annotations']))
