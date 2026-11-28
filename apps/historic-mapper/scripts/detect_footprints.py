"""Vector footprints of the automatic building recognition, for review in the workbench (workbench.html) before
the model is generated.

  * every epoch raster of growth_model.py (data/historic/growth/raw/, 2.5 m/px): the building pixels of
    growth_rules.building_mask() as polygons (connected components ≥ 25 m², simplified by 1 px);
  * the town plans 1891–1912 at 0.5 m: the registered footprints of map_buildings.py (hi_buildings.json).
The workbench shows them over the map; the user removes false ones, redraws or adds missing ones; the corrections
(manual/map_<id>.json: "removed" rings, "buildings" rings) are applied by growth_model.py to the recognition
(rasters / plan footprints) before dating, so they steer the whole model.

usage: python detect_footprints.py        → data/historic/growth/detected/<map id>.json, detected/index.json
"""
import json, os, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth_rules import BBOX, RES, imread, building_mask

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
G = os.path.join(ROOT, 'data', 'historic', 'growth')
OUT = os.path.join(G, 'detected'); os.makedirs(OUT, exist_ok=True)
EPOCHS = ['1821', '1840_cadastre', '1877_mesto', '1880_vm3', '1881', '1891', '1895', '1902', '1908', '1912', '1926', '1931', '1938', '1947',
          '1953_orto', '2001_orto']
index = []
for name in EPOCHS:
    f = next((x for x in os.listdir(os.path.join(G, 'raw')) if x.split('.')[0] == name), None)
    if not f: continue
    im, al = imread(os.path.join(G, 'raw', f)); b, cov = building_mask(name, im, al)
    n, lab, st, _ = cv2.connectedComponentsWithStats(b.astype(np.uint8), 8)
    polys = []
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] * RES * RES < 25: continue
        x, y, w, h = st[k, :4]
        cs, _ = cv2.findContours((lab[y:y + h, x:x + w] == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ap = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 1.0, True).reshape(-1, 2)
        if len(ap) < 3: continue
        polys.append({'id': f'd{k}', 'ring': [[round(BBOX[0] + (x + px + 0.5) * RES, 1), round(BBOX[3] - (y + py + 0.5) * RES, 1)] for px, py in ap]})
    json.dump({'map': name, 'res': RES, 'source': 'growth_rules.building_mask', 'polygons': polys}, open(os.path.join(OUT, f'{name}.json'), 'w'))
    index.append({'map': name, 'n': len(polys)}); print(f'{name:14s} {len(polys):6d} footprints')
HB = os.path.join(G, 'hi_buildings.json')
if os.path.exists(HB):
    for y, rings in json.load(open(HB))['plans'].items():
        polys = [{'id': f'h{k}', 'ring': r} for k, r in enumerate(rings)]
        json.dump({'map': f'{y}_hi', 'res': 0.5, 'source': 'map_buildings.py', 'polygons': polys}, open(os.path.join(OUT, f'{y}_hi.json'), 'w'))
        index.append({'map': f'{y}_hi', 'n': len(polys)}); print(f'{y}_hi        {len(polys):6d} footprints')
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w'), indent=1)
