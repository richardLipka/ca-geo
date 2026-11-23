import './style.css';
import seedJson from '../sources.json';
import { getLang, setLang, t } from './i18n';
import { ImageView } from './imageview';
import { REF_LAYERS } from './layers';
import { MapView } from './mapview';
import { emptyProject, type Source } from './model';
import { mountInspector, mountSources } from './panels';
import { store, type Tool } from './store';

interface SeedSource { id: string; title: string; kind: Source['kind']; made?: string; depicted?: [number, number]; holder?: string; licence?: string; page?: string; file: string; method?: Source['method'] }

const seedSources = seedJson as unknown as SeedSource[];

function toSource(s: SeedSource): Source {
  return { method: s.kind === 'map' ? 'affine' : 'projective', useLinks: true, overlay: true, opacity: 0.7, ...s, file: `/data/historic/sources/${s.file}` };
}

const TOOLS: { id: Tool; key: string }[] = [
  { id: 'navigate', key: 'v' }, { id: 'gcp', key: 'g' }, { id: 'identify', key: 'i' }, { id: 'outline', key: 'u' },
  { id: 'draw-point', key: 'p' }, { id: 'draw-line', key: 'l' }, { id: 'draw-polygon', key: 'o' },
];

function shell() {
  document.title = t('app.title');
  document.documentElement.lang = getLang();
  document.body.innerHTML = `
  <header class="top">
    <div class="brand"><h1>${t('app.title')}</h1><span>${t('app.subtitle')}</span></div>
    <div class="tools" role="toolbar">${TOOLS.map(x => `<button type="button" class="tool" data-tool="${x.id}" title="${t('tool.' + x.id)} (${x.key.toUpperCase()})">${t('tool.' + x.id)}<kbd>${x.key.toUpperCase()}</kbd></button>`).join('')}</div>
    <div class="right">
      <span class="save" id="save"></span>
      <button type="button" id="undo">${t('btn.undo')}</button><button type="button" id="redo">${t('btn.redo')}</button>
      <a class="btnlink" href="/viewer3d.html">${t('v3d.open')}</a>
      <button type="button" id="lang">${t('btn.lang')}</button>
    </div>
  </header>
  <aside class="left" id="sources"></aside>
  <main class="panes">
    <section class="pane imgpane"><canvas id="imgc"></canvas><div class="hint" id="imghint"></div></section>
    <section class="pane mappane" id="maproot">
      <img class="ref" alt="">
      <canvas id="glc" class="gl"></canvas><canvas id="vecc"></canvas>
      <div class="hint" id="maphint"></div>
      <div class="mapctl">
        <label>${t('ref.label')}<select id="ref">${REF_LAYERS.map(l => `<option value="${l.id}">${l.labelKey ? t(l.labelKey) : l.label}</option>`).join('')}</select></label>
        <label>${t('ref.opacity')}<input type="range" id="refop" min="0" max="1" step="0.05"></label>
        <label class="chk"><input type="checkbox" id="amcr"> ${t('map.amcr')}</label>
        <label class="chk"><input type="checkbox" id="growth"> ${t('map.growth')}</label>
        <label>${t('map.year')} <output id="yearout"></output><input type="range" id="year" min="1290" max="2030" step="1"></label>
        <label class="chk"><input type="checkbox" id="allyears"> ${t('map.allYears')}</label>
      </div>
      <div class="coords" id="coords"></div>
    </section>
  </main>
  <aside class="inspector" id="inspector"></aside>`;
}

async function start() {
  await store.load('plzen', async () => {
    const p = emptyProject('plzen');
    p.sources = seedSources.map(toSource);
    return p;
  });
  // add sources newly listed in sources.json to an existing project
  const known = new Set(store.project.sources.map(s => s.id));
  for (const s of seedSources as SeedSource[]) if (!known.has(s.id)) store.project.sources.push(toSource(s));
  if (!store.ui.sourceId && store.project.sources.length) store.ui.sourceId = store.project.sources[0].id;
  build();
}

let views: { img: ImageView; map: MapView } | null = null;

function build() {
  shell();
  const img = new ImageView(document.getElementById('imgc') as HTMLCanvasElement, document.getElementById('imghint')!);
  const map = new MapView(document.getElementById('maproot')!, document.getElementById('vecc') as HTMLCanvasElement, document.getElementById('glc') as HTMLCanvasElement, document.getElementById('maphint')!, document.getElementById('coords')!);
  views = { img, map };
  mountSources(document.getElementById('sources')!);
  mountInspector(document.getElementById('inspector')!, { centreImage: p => img.centreOn(p), centreMap: p => map.centreOn(p) });

  document.querySelectorAll<HTMLButtonElement>('button.tool').forEach(b => b.onclick = () => store.setUi({ tool: b.dataset.tool as Tool, pendingImg: null, pendingMap: null, drawing: [], outline: [], redraw: false }));
  (document.getElementById('undo') as HTMLButtonElement).onclick = () => store.undo();
  (document.getElementById('redo') as HTMLButtonElement).onclick = () => store.redo();
  (document.getElementById('lang') as HTMLButtonElement).onclick = () => { setLang(getLang() === 'cs' ? 'en' : 'cs'); build(); };
  const ref = document.getElementById('ref') as HTMLSelectElement, refop = document.getElementById('refop') as HTMLInputElement;
  ref.value = store.ui.refLayer; refop.value = String(store.ui.refOpacity);
  ref.onchange = () => { store.setUi({ refLayer: ref.value }); map.requestRef(); };
  refop.oninput = () => store.setUi({ refOpacity: +refop.value });
  const amcr = document.getElementById('amcr') as HTMLInputElement;
  amcr.checked = store.ui.showAmcr;
  amcr.onchange = () => { store.setUi({ showAmcr: amcr.checked }); map.toggleAmcr(amcr.checked); };
  const growth = document.getElementById('growth') as HTMLInputElement;
  growth.checked = store.ui.showGrowth;
  growth.onchange = () => { store.setUi({ showGrowth: growth.checked }); map.toggleGrowth(growth.checked); };
  const year = document.getElementById('year') as HTMLInputElement, all = document.getElementById('allyears') as HTMLInputElement, out = document.getElementById('yearout')!;
  const syncYear = () => { all.checked = store.ui.year === null; year.disabled = all.checked; year.value = String(store.ui.year ?? 1700); out.textContent = store.ui.year === null ? '' : String(store.ui.year); };
  syncYear();
  year.oninput = () => { store.setUi({ year: +year.value }); syncYear(); };
  all.onchange = () => { store.setUi({ year: all.checked ? null : +year.value }); syncYear(); };
  map.requestRef();
  render();
}

function render() {
  if (!views) return;
  document.querySelectorAll<HTMLButtonElement>('button.tool').forEach(b => b.classList.toggle('on', b.dataset.tool === store.ui.tool));
  const ref = document.getElementById('ref') as HTMLSelectElement | null; if (ref && ref.value !== store.ui.refLayer) ref.value = store.ui.refLayer;
  const sv = document.getElementById('save'); if (sv) { sv.textContent = t('save.' + store.ui.saveState); sv.className = 'save ' + store.ui.saveState; }
  views.img.render(); views.map.render();
}
store.on(render);
if (import.meta.env.DEV) (window as unknown as { __hm: unknown }).__hm = { store, views: () => views };

window.addEventListener('keydown', e => {
  const tag = (e.target as HTMLElement).tagName;
  if (/^(INPUT|SELECT|TEXTAREA)$/.test(tag)) return;
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') { e.preventDefault(); e.shiftKey ? store.redo() : store.undo(); return; }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'y') { e.preventDefault(); store.redo(); return; }
  if (e.key === 'Escape') { store.setUi({ pendingImg: null, pendingMap: null, drawing: [], outline: [], redraw: false }); return; }
  if (e.key === 'Enter') { if (store.ui.tool === 'outline') views?.img.finishOutline(); else views?.map.finishDrawing(); return; }
  const tool = TOOLS.find(x => x.key === e.key.toLowerCase());
  if (tool && !e.ctrlKey && !e.metaKey && !e.altKey) store.setUi({ tool: tool.id, pendingImg: null, pendingMap: null, drawing: [], outline: [], redraw: false });
});

start();
