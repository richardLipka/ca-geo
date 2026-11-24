"""Self-contained, publishable page with the 3D growth model, its timeline and the ground maps (bilingual cs / en).

Builds the viewer (vite, public3d.html in public mode) and copies it with the model data into
data/historic/growth/publish/ (not versioned: the ground maps include quoted third-party maps):
  index.html, assets/…, data/model.json, data/mesh.bin.0…n (parts < 14 MB for hosts with a file-size limit),
  data/ground_*.jpg, water_*.png, terrain.png, cuts.png
The folder can be served by any static web server (e.g. scripts/serve_site.py → http://localhost:5219/publish/).

usage: python publish_site.py        (after growth_model.py; needs node / npm in apps/historic-mapper)
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(APP, '..', '..'))
WEB = os.path.join(ROOT, 'data', 'historic', 'growth', 'web')
OUT = os.path.join(ROOT, 'data', 'historic', 'growth', 'publish')
PART = 14 * 1024 * 1024

npx = 'npx.cmd' if sys.platform == 'win32' else 'npx'
subprocess.run([npx, 'vite', 'build', '--outDir', os.path.join(APP, 'dist')], cwd=APP, check=True)
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'data'))
dist = os.path.join(APP, 'dist')
shutil.copytree(os.path.join(dist, 'assets'), os.path.join(OUT, 'assets'))
shutil.copy(os.path.join(dist, 'public3d.html'), os.path.join(OUT, 'index.html'))
M = json.load(open(os.path.join(WEB, 'model.json'), encoding='utf-8'))
files = set(['terrain.png'] + [g['file'] for g in M['grounds']] + [w['file'] for w in M.get('water', [])] + ([M['cuts']['file']] if M.get('cuts') else []))
for f in sorted(files): shutil.copy(os.path.join(WEB, f), os.path.join(OUT, 'data', f))
if M.get('mesh'):
    data = open(os.path.join(WEB, M['mesh']['file']), 'rb').read()
    parts = []
    for k in range(0, len(data), PART):
        fn = f"{M['mesh']['file']}.{k // PART}"
        open(os.path.join(OUT, 'data', fn), 'wb').write(data[k:k + PART]); parts.append(fn)
    M['mesh']['files'] = parts
json.dump(M, open(os.path.join(OUT, 'data', 'model.json'), 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print('published to', OUT, f'{size / 1e6:.1f} MB,', len(os.listdir(os.path.join(OUT, 'data'))), 'data files')
