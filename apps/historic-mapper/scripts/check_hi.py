"""Overlay of the model (buildings visible in the plan's year) on the 0.5 m town plans 1891–1912.

usage: python check_hi.py [i j]    → data/historic/growth/raw_hi/_model_<year>_<i>_<j>.jpg
  model buildings outlined: blue = real (RÚIAN / maps), magenta = from the town plans (hmap), orange = generated, green = history
"""
import json, os, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RAW = os.path.join(ROOT, 'data', 'historic', 'growth', 'raw_hi')
M = json.load(open(os.path.join(ROOT, 'data', 'historic', 'growth', 'web', 'model.json'), encoding='utf-8'))
OX, OY = M['origin']
X0, Y1, TILE, RES = -823900.0, -1068200.0, 1000.0, 0.5
i, j = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 1)
x0, y1 = X0 + i * TILE, Y1 - j * TILE


def vis(b, y):
    if M['from'][b] > y or M['to'][b] <= y: return False
    return not any(s <= y < e for s, e in zip(*[iter(M['gaps'][b] or [])] * 2))


for year in (1891, 1895, 1902, 1908, 1912):
    from PIL import Image
    im = cv2.cvtColor(np.array(Image.open(os.path.join(RAW, f'{year}_{i}_{j}.png')).convert('RGB')), cv2.COLOR_RGB2BGR)
    im = (im * 0.75 + 255 * 0.25).astype(np.uint8)
    for b in range(M['n']):
        if not vis(b, year + 0.01) or M['classes'][M['cls'][b]] in ('moat', 'ditch'): continue
        r = M['rings'][b]
        pts = np.array([[(r[k] / 10 + OX - x0) / RES, (y1 - (r[k + 1] / 10 + OY)) / RES] for k in range(0, len(r), 2)], np.int32)
        if pts[:, 0].max() < 0 or pts[:, 1].max() < 0 or pts[:, 0].min() > 2000 or pts[:, 1].min() > 2000: continue
        idv = M['ids'][b]; bs = M['basis'][M['basisIdx'][b]]
        col = (200, 0, 200) if idv.startswith('hmap:') else (0, 140, 255) if idv.startswith('gen:') else (0, 160, 0) if bs == 'history' else (200, 80, 0)
        cv2.polylines(im, [pts], True, col, 2)
    cv2.putText(im, str(year), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
    cv2.imencode('.jpg', cv2.resize(im, (1200, 1200), interpolation=cv2.INTER_AREA))[1].tofile(os.path.join(RAW, f'_model_{year}_{i}_{j}.jpg'))
print('ok')
