"""Self-contained, publishable bilingual (cs / en) web for people: the video guide, the video and the interactive 3D
model with its timeline and ground maps; no authoring or review tools (check/, editor/ stay out).

data/historic/growth/publish/ (not versioned: the maps include quoted third-party works):
  index.html, flip/, img/, logos/       the guide (site/ of sources_site.py)
  video/plzen-growth-1295-2020.mp4      the animation
  model/index.html, model/assets/…      the viewer (vite, public3d.html in public mode)
  model/data/model.json, mesh.bin.0…n (parts < 14 MB for hosts with a file-size limit), ground_*.jpg, water_*.png, …
The folder can be served by any static web server (e.g. scripts/serve_site.py → http://localhost:5219/publish/).

usage: python publish_site.py        (after growth_model.py, the video and sources_site.py; needs node / npm)
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(APP, '..', '..'))
WEB = os.path.join(ROOT, 'data', 'historic', 'growth', 'web')
PUB = os.path.join(ROOT, 'data', 'historic', 'growth', 'publish')
SITE = os.path.join(ROOT, 'data', 'historic', 'growth', 'site')
VIDEO = os.path.join(ROOT, 'data', 'historic', 'growth', 'video', 'plzen-growth-1295-2020.mp4')
OUT = os.path.join(PUB, 'model')
PART = 14 * 1024 * 1024

npx = 'npx.cmd' if sys.platform == 'win32' else 'npx'
subprocess.run([npx, 'vite', 'build', '--outDir', os.path.join(APP, 'dist')], cwd=APP, check=True)
if os.path.isdir(PUB): shutil.rmtree(PUB)
shutil.copytree(SITE, PUB, ignore=shutil.ignore_patterns('check'))
page = open(os.path.join(PUB, 'index.html'), encoding='utf-8').read().replace('"../video/', '"video/')
open(os.path.join(PUB, 'index.html'), 'w', encoding='utf-8').write(page)
os.makedirs(os.path.join(PUB, 'video')); shutil.copy(VIDEO, os.path.join(PUB, 'video'))
os.makedirs(os.path.join(OUT, 'data'))
if os.path.isdir(os.path.join(APP, 'public', 'logos')): shutil.copytree(os.path.join(APP, 'public', 'logos'), os.path.join(OUT, 'logos'))
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
size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(PUB) for f in fs)
print('published to', PUB, f'{size / 1e6:.1f} MB,', len(os.listdir(os.path.join(OUT, 'data'))), 'data files')
