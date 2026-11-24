"""Index of the map set for the manual editor (editor/index.html): every map of the growth model in the 9 × 9 km
frame (data/historic/growth/raw/, 2.5 m/px), the early ground maps registered to the model (web/ground_*.jpg:
map 57 c. 1410, Theatrum Europaeum 1618, fortification plans 1658 and 1703) and the town plans 1891–1912 at
0.5 m (raw_hi/ tiles of map_buildings.py, 3 × 3 km around the old town), plus the vedute (projects/plzen.json
sources of kind birdseye / panorama) with their fitted cameras.

usage: python manual_maps.py        → apps/historic-mapper/manual/maps.json (versioned; the images stay in data/)
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(APP, '..', '..'))
G = os.path.join(ROOT, 'data', 'historic', 'growth')
from growth_rules import BBOX, RES

maps = []
for f in sorted(os.listdir(os.path.join(G, 'raw'))):
    name, ext = os.path.splitext(f)
    if ext not in ('.png', '.jpg') or name in ('2025_ruian',): continue
    y = int(re.match(r'\d{4}', name)[0])
    maps.append({'id': name, 'year': y, 'label': name.replace('_', ' '), 'layers': [{'url': f'/raw/{f}', 'bbox': BBOX}]})
EARLY = [('ground_1300', 1410, 'map 57 (HAM 21), c. 1410'), ('ground_1618', 1618, 'Theatrum Europaeum 1618'),
         ('ground_1658', 1658, 'fortification plan 1658 (HAM map 5)'), ('ground_1703', 1703, 'fortification plan 1703 (HAM map 6)')]
for name, y, lab in EARLY:
    if os.path.exists(os.path.join(G, 'web', name + '.jpg')):
        maps.append({'id': name, 'year': y, 'label': lab, 'layers': [{'url': f'/web/{name}.jpg', 'bbox': BBOX}]})
HB = os.path.join(G, 'hi_buildings.json')
X0, Y1, TILE = -823900.0, -1068200.0, 1000.0
CELLS = json.load(open(HB)).get('cells', {}) if os.path.exists(HB) else {}   # registration of the plans (map_buildings.py)
for y in (1891, 1895, 1902, 1908, 1912):
    tiles = [{'url': f'/raw_hi/{y}_{i}_{j}.png', 'bbox': [X0 + i * TILE, Y1 - (j + 1) * TILE, X0 + (i + 1) * TILE, Y1 - j * TILE], 'cells': CELLS.get(f'{y}_{i}_{j}')}
             for i in range(3) for j in range(3) if os.path.exists(os.path.join(G, 'raw_hi', f'{y}_{i}_{j}.png'))]
    if tiles: maps.append({'id': f'{y}_hi', 'year': y, 'label': f'town plan {y}, 0.5 m (3 × 3 km)', 'layers': tiles})
maps.sort(key=lambda m: (m['year'], m['id']))
P = json.load(open(os.path.join(APP, 'projects', 'plzen.json'), encoding='utf-8'))
ved = [{'id': s['id'], 'label': s.get('title') or s['id'], 'url': '/sources/' + os.path.basename(s['file']), 'year': (s.get('depicted') or [None])[0],
        'view': s.get('view')} for s in P['sources'] if s.get('kind') in ('birdseye', 'panorama')]
json.dump({'frame': BBOX, 'res': RES, 'maps': maps, 'vedute': ved}, open(os.path.join(APP, 'manual', 'maps.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(maps), 'maps,', len(ved), 'vedute')
