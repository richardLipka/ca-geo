"""Seed the historic-mapper project with the first model of Plzeň (c. 1536–1618):
landmarks, the inner town wall, wall towers projected from the 1618 siege plate, building
footprints from the stable cadastre (SAM) and identity links in the 1618 plate and in the
oldest veduta (Ottheinrich album 1536–37). Idempotent: replaces items with ids 'g1618-…'.

usage: python build_1618_project.py project.json analysis.json buildings.geojson
  analysis.json  — output of plzen_1618.py
  buildings.geojson — output of sam_buildings.py
"""
import json, math, sys

proj_path, ana_path, bld_path = sys.argv[1:4]
P = json.load(open(proj_path, encoding='utf-8'))
A = json.load(open(ana_path, encoding='utf-8'))
B = json.load(open(bld_path, encoding='utf-8'))
G = 'g1618-'
P['entities'] = [e for e in P['entities'] if not e['id'].startswith(G)]
P['annotations'] = [a for a in P['annotations'] if not a['id'].startswith(G)]

# heights (m, approximate, for 3D views) and lifetimes; values marked "to be verified" in notes
META = {
    'bartholomew':  dict(height=30, notes='Nave/chancel; the tower is a separate entity.'),
    'barth_tower':  dict(height=100, notes='West tower, c. 100 m with spire (present height 102 m; earlier spire to be verified).'),
    'barth_east':   dict(height=30),
    'dominican':    dict(height=30, validTo=1785, notes='Black (Dominican) monastery; abolished 1785 (to be verified); position = later Militair Spital.'),
    'franciscan':   dict(height=35),
    'all_saints':   dict(height=25),
    'st_nicholas':  dict(height=25),
    'gate_prague':  dict(height=25, validTo=1822, notes='Demolished 1822 (Deník 2008, cs.wiki).'),
    'gate_reich':   dict(height=25, validTo=1833, notes='Demolished 1833.'),
    'gate_litice':  dict(height=25, validTo=1804, notes='Demolished 1804; side tower kept in the gymnasium; position approximate.'),
    'gate_north':   dict(height=22, validTo=1849, notes='Saxon / mill gate; demolished 1849; identification with TE "Klein thor" (G) to be verified.'),
    'water_tower':  dict(height=30, validFrom=1532),
}
ents = {}
for k, v in A['landmarks'].items():
    e = {'id': G + k, 'name': v['name'], 'type': v['type'], 'geom': {'type': 'Point', 'coords': [v['xy']]}}
    m = META.get(k, {})
    e.update({kk: vv for kk, vv in m.items() if kk != 'notes'})
    e['notes'] = ' '.join(filter(None, [m.get('notes'), 'Position: ' + v['provenance'] + '.']))
    ents[k] = e

wall = A['wall']
ents['wall'] = {'id': G + 'wall', 'name': 'Inner town wall (line from the stable cadastre)', 'type': 'wall', 'height': 8, 'validTo': 1849,
                'geom': {'type': 'Polygon', 'coords': wall},
                'notes': 'Backs of the perimeter houses on the stable cadastre 1839–41; walls demolished 1795–1849. The outer (Zwinger) wall and the 1645–49 bastions are not modelled yet.'}

def snap(p, ring):
    best = (1e18, None)
    for i in range(len(ring)):
        a, b = ring[i], ring[(i + 1) % len(ring)]
        vx, vy = b[0] - a[0], b[1] - a[1]; L = vx * vx + vy * vy or 1e-9
        t = max(0, min(1, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L))
        q = (a[0] + t * vx, a[1] + t * vy); d = math.dist(p, q)
        if d < best[0]: best = (d, q)
    return best

towers = []
for i, t in enumerate(A['te1618_towers']):
    d, q = snap(t['map'], wall)
    k = f'te_tower_{i + 1}'
    ents[k] = {'id': G + k, 'name': f'Wall tower {i + 1} (from the 1618 plate)', 'type': 'tower', 'height': 15, 'validTo': 1849,
               'geom': {'type': 'Point', 'coords': [[round(q[0], 1), round(q[1], 1)]]},
               'notes': f'Projected from the Theatrum Europaeum plate (homography, LOO RMSE {A["te1618"]["loo_rmse_m"]} m) and snapped {d:.0f} m onto the wall line.'}
    towers.append((k, t['img']))

for f in B['features']:
    pr = f['properties']; ring = f['geometry']['coordinates'][0][:-1]
    n = sum(1 for e in ents if e.startswith('bld')) + 1
    k = f'bld{n:04d}'
    rem = pr.get('block_remainder')
    ents[k] = {'id': G + k, 'name': f'{"Block remainder" if rem else "Building"} {n} ({pr["material"]})', 'type': 'building',
               'height': 9 if pr['material'] == 'stone' else 6,
               'geom': {'type': 'Polygon', 'coords': ring},
               'notes': f'Stable cadastre 1839–41 footprint ({"colour mask, not split into houses" if rem else "Segment Anything vit_h"}), {pr["area_m2"]} m², {pr["material"]}. Presence in 1618 not verified.'}

P['entities'].extend(ents.values())

def ann(src, key, img, label='', conf=2, ctrl=True, note=None):
    a = {'id': f'{G}{src}-{key}', 'sourceId': src, 'img': [float(img[0]), float(img[1])], 'entityId': G + key,
         'label': label or None, 'confidence': conf, 'useAsControl': ctrl}
    if note: a['note'] = note
    P['annotations'].append({k: v for k, v in a.items() if v is not None})

for p in A['te1618']['points']:
    conf = 1 if p['id'] == 'gate_prague' else 3 if p['id'] in ('bartholomew', 'franciscan', 'dominican') else 2
    ann('te-1618', p['id'], p['img'], p['label'], conf, True, f'residual {p["res_m"]} m, leave-one-out {p["loo_m"]} m')
for k, img in towers:
    ann('te-1618', k, img, '', 2, False, 'tower drawn on the plate; projected onto the map')

# oldest veduta — identification by the ordinal analysis (see docs/research/plzen-first-model.md)
OTT = [('barth_tower', (1017, 1300), 3, 'west tower of St Bartholomew'),
       ('barth_east', (1217, 1340), 3, 'east end of the chancel'),
       ('gate_reich', (642, 1420), 1, 'left gate with passage — hypothesis'),
       ('gate_litice', (779, 1400), 1, 'round tower — hypothesis'),
       ('water_tower', (1536, 1300), 2, 'tall tower with corner turrets — hypothesis (water tower 1532 or Prague gate)'),
       ('franciscan', (1801, 1380), 1, 'church with spire — hypothesis'),
       ('gate_prague', (2020, 1440), 1, 'right corner tower — hypothesis')]
for k, img, conf, note in OTT:
    ann('ottheinrich-1536', k, img, '', conf, True, note)

for s in P['sources']:
    if s['id'] == 'te-1618': s.update(method='projective', overlay=True, opacity=0.6, useLinks=True)
    elif s['id'] == 'ottheinrich-1536': s.update(kind='panorama')
    else: s['overlay'] = False

json.dump(P, open(proj_path, 'w', encoding='utf-8', newline='\n'), indent=1, ensure_ascii=False)
print(f'entities {len(P["entities"])} (buildings {sum(1 for e in ents if e.startswith("bld"))}), annotations {len(P["annotations"])}')
