"""Review page: quick yes / no decisions for the footprint plans and the veduta links.

Items
- plan tiles (from check_epochs.py: tiles.json): one 3 × 3 tile of the core per map, footprints of the model in the
  map's first year over the map. Question: do the footprints match the map (nothing extra, nothing missing)?
- veduta links: every annotation that links a point of a drawing to a model object, as a crop of the drawing with
  the drawn point (green) and, where the camera of the view is fitted, the projected model point (red).
  Question: is the link right (this point of the drawing is this object)?
- veduta projections: the drawing projected onto the model from the fitted camera. Question: does it fit?

Decisions are saved by serve_site.py (POST /api/review) to data/historic/growth/site/check/review.json; the page keeps a
copy in the browser and can export it as a file. Keys: A = ano, N = ne, U = nevím, J / K = next / previous.

usage: python review_items.py   (after check_epochs.py)  → data/historic/growth/site/check/review.html, items.json, ved/*.jpg
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial.transform import Rotation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
G = os.path.join(ROOT, 'data', 'historic', 'growth')
OUT = os.path.join(G, 'site', 'check'); os.makedirs(os.path.join(OUT, 'ved'), exist_ok=True)
P = json.load(open(os.path.join(ROOT, 'apps', 'historic-mapper', 'projects', 'plzen.json'), encoding='utf-8'))
M = json.load(open(os.path.join(G, 'web', 'model.json'), encoding='utf-8'))
IDX = {k: i for i, k in enumerate(M['ids'])}
ENT = {e['id']: e for e in P['entities']}
try: FONT = ImageFont.truetype('arial.ttf', 15)
except Exception: FONT = ImageFont.load_default()
items = []
for t in json.load(open(os.path.join(OUT, 'tiles.json'), encoding='utf-8')):
    items.append({'id': t['id'], 'kind': 'plan', 'group': f"{t['year']} – {t['map']}", 'img': t['img'],
                  'title': f"{t['year']} · {t['map']} · dlaždice {t['id'][-2:]}",
                  'info': f"budov {t['n']}" + (f" · ok {t['ok']} · slabě {t['weak']} · navíc {t['extra']}" if t['ok'] + t['weak'] + t['extra'] else '') + (f" · souběh {t['overlaps']}" if t['overlaps'] else ''),
                  'q': 'Odpovídají půdorysy mapě? (nic navíc, nic nechybí)'})


def centre(b):
    r = M['rings'][b]
    return sum(r[0::2]) / (len(r) / 2) / 10, sum(r[1::2]) / (len(r) / 2) / 10


for src in P['sources']:
    anns = [a for a in P['annotations'] if a['sourceId'] == src['id'] and a.get('entityId')]
    if not anns: continue
    im = Image.open(os.path.join(ROOT, 'data', 'historic', 'sources', os.path.basename(src['file']))).convert('RGB')
    W, H = im.size
    v = src.get('view') if src.get('view', {}).get('quat') else None
    if v:
        C = np.array(v['pos']); R = Rotation.from_quat(v['quat']).as_matrix(); f = H / 2 / math.tan(math.radians(v['fov']) / 2)
    for a in anns:
        e = a['entityId']; name = ENT.get(e, {}).get('name', e)
        pr = None
        if v and e in IDX:
            b = IDX[e]; x, y = centre(b); X = np.array([x, M['z'][b] + M['h1'][b], -y])
            pc = (X - C) @ R
            if pc[2] < -1: pr = (W / 2 + f * pc[0] / -pc[2], H / 2 - f * pc[1] / -pc[2])
        cx, cy = a['img']; half = max(120, int(0.09 * max(W, H)))
        if pr:
            cx, cy = (cx + pr[0]) / 2, (cy + pr[1]) / 2; half = max(half, int(abs(pr[0] - a['img'][0]) / 2 + 60), int(abs(pr[1] - a['img'][1]) / 2 + 60))
        box = (int(cx - half), int(cy - half), int(cx + half), int(cy + half))
        crop = im.crop(box).resize((360, 360)); k = 360 / (2 * half)
        d = ImageDraw.Draw(crop)
        ox, oy = (a['img'][0] - box[0]) * k, (a['img'][1] - box[1]) * k
        if pr:
            px_, py_ = (pr[0] - box[0]) * k, (pr[1] - box[1]) * k
            d.line([(ox, oy), (px_, py_)], fill=(220, 0, 0), width=2); d.ellipse([px_ - 6, py_ - 6, px_ + 6, py_ + 6], outline=(220, 0, 0), width=3)
        d.ellipse([ox - 7, oy - 7, ox + 7, oy + 7], outline=(0, 170, 0), width=3)
        d.rectangle([0, 0, 360, 22], fill=(255, 255, 255)); d.text((4, 3), name[:44], fill=(0, 0, 0), font=FONT)
        fn = f"ved/{src['id']}_{a['id']}.jpg".replace(':', '_')
        crop.save(os.path.join(OUT, fn), quality=86)
        err = f" · odchylka {math.hypot(pr[0] - a['img'][0], pr[1] - a['img'][1]):.0f} px" if pr else ' · kamera nenapasována'
        items.append({'id': f"ved:{src['id']}:{a['id']}", 'kind': 'veduta', 'group': src['title'][:60], 'img': fn,
                      'title': f"{name}", 'info': f"{src['id']} · {a.get('label') or ''}{err}".replace(' ·  ·', ' ·'),
                      'q': 'Je vazba správná? (zelený bod v kresbě = tento objekt; červený = kam ho promítá model)'})
for fn, sid, t in (('veduta_te1618_camera.jpg', 'te-1618', 'Rytina 1618 promítnutá z napasované kamery'), ('veduta_te1618_oblique.jpg', 'te-1618', 'Rytina 1618 na fasádách (jiný pohled)')):
    p = os.path.join(G, 'shots', fn)
    if os.path.exists(p):
        Image.open(p).convert('RGB').resize((800, 450)).save(os.path.join(OUT, 'ved', fn), quality=86)
        items.append({'id': f'proj:{fn}', 'kind': 'veduta', 'group': 'Promítnutí', 'img': f'ved/{fn}', 'title': t, 'info': sid,
                      'q': 'Sedí promítnutí kresby na model?'})
json.dump(items, open(os.path.join(OUT, 'items.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('items', len(items), {k: sum(1 for i in items if i['kind'] == k) for k in ('plan', 'veduta')})

PAGE = r"""<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kontrola: ano / ne</title>
<style>
:root{--bg:#f6f5f1;--fg:#1f2427;--mut:#5d676f;--card:#fff;--line:#d9dcd6;--yes:#2f7a4d;--no:#b3311f;--uns:#a06800}
@media (prefers-color-scheme:dark){:root{--bg:#17191b;--fg:#e8e6e1;--mut:#a0a7ad;--card:#212427;--line:#383c40;--yes:#6cc28f;--no:#e8664f;--uns:#e0a53a}}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,sans-serif;background:var(--bg);color:var(--fg)}
header{position:sticky;top:0;z-index:3;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
h1{font-size:18px;margin:0 12px 0 0}button,select,input{font:inherit}header button,header select{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:6px;padding:4px 10px;cursor:pointer}
header button.on{background:var(--fg);color:var(--bg)}.prog{color:var(--mut)}.save{margin-left:auto;color:var(--mut)}
main{padding:12px 16px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}
.card{background:var(--card);border:2px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.card.cur{outline:3px solid #4a7fd0;outline-offset:1px}.card.yes{border-color:var(--yes)}.card.no{border-color:var(--no)}.card.unsure{border-color:var(--uns)}
.card img{width:100%;aspect-ratio:1;object-fit:cover;background:#ddd;cursor:zoom-in;display:block}.card img.wide{aspect-ratio:16/9}
.b{padding:8px 10px;display:grid;gap:6px}.t{font-weight:600}.i{color:var(--mut);font-size:12.5px}.q{font-size:13px}
.btns{display:flex;gap:6px}.btns button{flex:1;border:2px solid var(--line);background:var(--card);color:var(--fg);border-radius:8px;padding:8px 0;font-weight:700;cursor:pointer}
.btns .y.on{background:var(--yes);border-color:var(--yes);color:#fff}.btns .n.on{background:var(--no);border-color:var(--no);color:#fff}.btns .u.on{background:var(--uns);border-color:var(--uns);color:#fff}
.note{width:100%;border:1px solid var(--line);border-radius:6px;padding:5px 8px;background:var(--bg);color:var(--fg)}
.grp{grid-column:1/-1;font-weight:700;margin-top:10px;border-bottom:1px solid var(--line);padding-bottom:4px}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:9;cursor:zoom-out}#lb.on{display:flex}#lb img{max-width:96vw;max-height:94vh}
.help{color:var(--mut);font-size:12.5px;width:100%}
</style></head><body>
<header><h1>Kontrola: ano / ne</h1>
<button data-k="plan" class="on">Plány</button><button data-k="veduta">Veduty</button><button data-k="all">Vše</button>
<label><input type="checkbox" id="open"> jen nerozhodnuté</label>
<span class="prog" id="prog"></span><button id="exp">Stáhnout rozhodnutí</button><span class="save" id="save"></span>
<div class="help">Klávesy: <b>A</b> ano · <b>N</b> ne · <b>U</b> nevím · <b>J/K</b> další / předchozí · klik na obrázek = zvětšit. Plány: barevné obrysy jsou budovy modelu v roce mapy (zelená = mapa je ukazuje, oranžová = slabě, červená = navíc, fialová = dvě budovy na stejném místě, modrá = mapa bez detekce). Do poznámky můžete napsat, co nesedí.</div></header>
<main id="m"></main><div id="lb"><img alt=""></div>
<script>
let ITEMS=[], DEC={}, kind='plan', cur=0, shown=[];
const LS='review-decisions';
const save=async(id)=>{try{localStorage.setItem(LS,JSON.stringify(DEC))}catch(e){}
  try{const r=await fetch('/api/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({[id]:DEC[id]})});document.getElementById('save').textContent=r.ok?'uloženo':'neuloženo na server (jen v prohlížeči)'}catch(e){document.getElementById('save').textContent='neuloženo na server (jen v prohlížeči)'}};
const prog=()=>{const its=ITEMS.filter(i=>kind==='all'||i.kind===kind);const d=its.filter(i=>DEC[i.id]&&DEC[i.id].v).length;
  const y=its.filter(i=>DEC[i.id]&&DEC[i.id].v==='yes').length,n=its.filter(i=>DEC[i.id]&&DEC[i.id].v==='no').length;
  document.getElementById('prog').textContent=`${d} / ${its.length} rozhodnuto · ano ${y} · ne ${n}`;};
const setv=(id,v)=>{DEC[id]=Object.assign(DEC[id]||{},{v,t:new Date().toISOString()});const c=document.getElementById('c-'+CSS.escape(id));
  if(c){c.classList.remove('yes','no','unsure');c.classList.add(v);c.querySelectorAll('.btns button').forEach(b=>b.classList.toggle('on',b.dataset.v===v));}
  save(id);prog();};
const render=()=>{const m=document.getElementById('m');m.innerHTML='';const only=document.getElementById('open').checked;let g='';
  shown=ITEMS.filter(i=>(kind==='all'||i.kind===kind)&&(!only||!(DEC[i.id]&&DEC[i.id].v)));
  shown.forEach((it,k)=>{if(it.group!==g){g=it.group;const h=document.createElement('div');h.className='grp';h.textContent=g;m.appendChild(h);}
    const d=DEC[it.id]||{};const c=document.createElement('div');c.className='card '+(d.v||'');c.id='c-'+it.id;
    c.innerHTML=`<img src="${it.img}" loading="lazy" class="${it.img.includes('proj')||it.id.startsWith('proj:')?'wide':''}"><div class="b"><div class="t"></div><div class="i"></div><div class="q"></div>
      <div class="btns"><button class="y ${d.v==='yes'?'on':''}" data-v="yes">Ano</button><button class="n ${d.v==='no'?'on':''}" data-v="no">Ne</button><button class="u ${d.v==='unsure'?'on':''}" data-v="unsure">?</button></div>
      <input class="note" placeholder="poznámka (nepovinné)"></div>`;
    c.querySelector('.t').textContent=it.title;c.querySelector('.i').textContent=it.info;c.querySelector('.q').textContent=it.q;
    const note=c.querySelector('.note');note.value=d.note||'';note.onchange=()=>{DEC[it.id]=Object.assign(DEC[it.id]||{},{note:note.value,t:new Date().toISOString()});save(it.id);};
    c.querySelectorAll('.btns button').forEach(b=>b.onclick=()=>{cur=k;setv(it.id,b.dataset.v);focus(k+1);});
    c.querySelector('img').onclick=()=>{const lb=document.getElementById('lb');lb.querySelector('img').src=it.img;lb.classList.add('on')};
    c.onclick=e=>{if(e.target.tagName!=='BUTTON'&&e.target.tagName!=='INPUT'&&e.target.tagName!=='IMG'){cur=k;focus(k)}};
    m.appendChild(c);});
  prog();focus(Math.min(cur,shown.length-1));};
const focus=k=>{if(!shown.length)return;cur=Math.max(0,Math.min(k,shown.length-1));document.querySelectorAll('.card.cur').forEach(c=>c.classList.remove('cur'));
  const c=document.getElementById('c-'+CSS.escape(shown[cur].id));if(c){c.classList.add('cur');c.scrollIntoView({block:'nearest',behavior:'smooth'});}};
document.getElementById('lb').onclick=()=>document.getElementById('lb').classList.remove('on');
document.querySelectorAll('header button[data-k]').forEach(b=>b.onclick=()=>{kind=b.dataset.k;cur=0;document.querySelectorAll('header button[data-k]').forEach(x=>x.classList.toggle('on',x===b));render();});
document.getElementById('open').onchange=()=>{cur=0;render()};
document.getElementById('exp').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(DEC,null,1)],{type:'application/json'}));a.download='review.json';a.click();};
addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return;const it=shown[cur];if(!it)return;
  const k=e.key.toLowerCase();if(k==='a'){setv(it.id,'yes');focus(cur+1)}else if(k==='n'){setv(it.id,'no');focus(cur+1)}else if(k==='u'){setv(it.id,'unsure');focus(cur+1)}
  else if(k==='j'||e.key==='ArrowRight'){focus(cur+1)}else if(k==='k'||e.key==='ArrowLeft'){focus(cur-1)}else if(e.key==='Escape'){document.getElementById('lb').classList.remove('on')}});
(async()=>{ITEMS=await (await fetch('items.json')).json();
  try{DEC=JSON.parse(localStorage.getItem(LS)||'{}')}catch(e){DEC={}}
  try{const r=await fetch('review.json',{cache:'no-store'});if(r.ok){Object.assign(DEC,await r.json())}}catch(e){}
  render();})();
</script></body></html>"""
open(os.path.join(OUT, 'review.html'), 'w', encoding='utf-8').write(PAGE)
print('written', os.path.join(OUT, 'review.html'))
