export {};
// Workbench: automatic recognition → manual review of the vector footprints on every map → model generation → 3D.
// Corrections are saved per map in manual/map_<id>.json ("removed": detected footprints rejected, "buildings":
// drawn or edited footprints) and water in manual/water_<id>.png; growth_model.py applies them to the recognition
// before dating. Runs on the vite dev server (API: /api/manual/*, /api/run/*, /manual/*, /data/*).

type XY = [number, number];
interface Layer { url: string; bbox: number[]; cells?: number[][][] | null }
interface MapInfo { id: string; year: number; label: string; layers: Layer[] }
interface Det { id: string; ring: XY[] }
interface Bld { ring: XY[]; from?: number; to?: number; h?: number; src?: string }
interface Edits { map: string; year: number; buildings: Bld[]; removed: Det[]; waterEdited?: boolean; saved?: string }

const G = '/data/historic/growth';
const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const cv = $<HTMLCanvasElement>('cv'), ctx = cv.getContext('2d')!;

// ---------- language ----------
const EN: Record<string, string> = {
  title: 'Growth of Plzeň: recognition → review → model', s1: 'Recognition', s2: 'Footprint review', s3: 'Model generation', s4: '3D preview', iso: 'Houses from vedute →',
  p1h: 'Finds buildings on all maps automatically (town plans 1891–1912 at 0.5 m, registered; epochs 1821–2001 at 2.5 m) and stores them as vector footprints for review.',
  runDetect: 'Run recognition', map: 'Map', layers: 'Layers', lDet: 'recognised footprints', lMan: 'added / edited by hand', lModel: 'model buildings in the map year', lWater: 'water painted by hand',
  opacity: 'Map', tool: 'Tool', tSel: 'Select / edit', tPoly: 'Polygon', tRect: 'Rectangle', tWater: 'Water', tErase: 'Eraser', brush: 'Brush (m)',
  keys: 'Select: click a footprint, Delete rejects a recognised one (Delete again restores it), drag a vertex to edit, Alt+click a vertex removes it, double click an edge adds a vertex. Polygon: corners, Enter. Rectangle: two corners of one side and the depth. Pan: middle button or space, wheel = zoom. Ctrl+S saves.',
  selected: 'Selected footprint', from: 'from', to: 'to', height: 'height (m)', save: 'Save corrections of this map',
  p3h: 'The corrections of all maps are applied to the recognition (epoch rasters, plan footprints) and the model is rebuilt: building dating, permanence of objects (a house stands until a map clearly shows it gone; on the place of a present building it is the same building with its model from the city catalogue), generated fabric, fortification. Takes a few minutes.',
  runModel: 'Generate the model', runVed: 'Reconstruct houses from the vedute and generate', p4h: 'The model opens in the city growth viewer (timeline, period maps under the model).', open3d: 'Open the 3D model',
};
let lang: 'cs' | 'en' = 'cs';
const CS: Record<string, string> = {}; document.querySelectorAll<HTMLElement>('[data-t]').forEach(e => CS[e.dataset.t!] = e.textContent ?? '');
const tr = (k: string) => (lang === 'en' ? EN[k] : CS[k]) ?? k;
const T2 = (cs: string, en: string) => (lang === 'cs' ? cs : en);
$('lang').onclick = () => { lang = lang === 'cs' ? 'en' : 'cs'; document.querySelectorAll<HTMLElement>('[data-t]').forEach(e => e.textContent = tr(e.dataset.t!)); $('lang').textContent = lang === 'cs' ? 'EN' : 'CS'; refresh(); };

// ---------- state ----------
let IDX: { frame: number[]; res: number; maps: MapInfo[] };
let cur: MapInfo | null = null, imgs: { L: Layer; im: HTMLImageElement }[] = [];
let dets: Det[] = [], detPath: Path2D | null = null, grid = new Map<string, number[]>();
let edits: Edits | null = null, removedIds = new Set<string>();
let MODEL: any = null, modelPath: Path2D | null = null;
let waterCv: HTMLCanvasElement | null = null, waterCtx: CanvasRenderingContext2D | null = null;
let view = { cx: -822500, cy: -1069700, s: 1.0 };
let tool = 'select', draft: XY[] = [], hover: XY | null = null, dirty = false;
let sel: { kind: 'det' | 'man'; i: number } | null = null;
const status = (t: string) => { $('status').textContent = t; };

async function getJSON<T>(u: string): Promise<T | null> { try { const r = await fetch(u, { cache: 'no-store' }); return r.ok ? await r.json() as T : null; } catch { return null; } }
const loadImg = (u: string) => new Promise<HTMLImageElement | null>(res => { const i = new Image(); i.onload = () => res(i); i.onerror = () => res(null); i.src = u; });
const dataUrl = (u: string) => u.startsWith('/manual/') ? u : G + u;

// ---------- transforms ----------
const DPR = () => devicePixelRatio;
const S2W = (u: number, v: number): XY => [(u - cv.width / 2) / DPR() * view.s + view.cx, -(v - cv.height / 2) / DPR() * view.s + view.cy];
const evPos = (e: MouseEvent): XY => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) * DPR(), (e.clientY - r.top) * DPR()]; };
function worldT() { const k = DPR() / view.s; ctx.setTransform(k, 0, 0, -k, cv.width / 2 - view.cx * k, cv.height / 2 + view.cy * k); return k; }
function resize() { const r = cv.parentElement!.getBoundingClientRect(); cv.width = r.width * DPR(); cv.height = r.height * DPR(); draw(); }
addEventListener('resize', resize);

// ---------- geometry ----------
function inRing(x: number, y: number, r: XY[]) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, yi] = r[i], [xj, yj] = r[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; }
const area = (r: XY[]) => Math.abs(r.reduce((s, p, i) => { const q = r[(i + 1) % r.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0) / 2);
function segDist(p: XY, a: XY, b: XY) { const dx = b[0] - a[0], dy = b[1] - a[1], L = dx * dx + dy * dy || 1; const t = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L)); return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy); }
const r1 = (r: XY[]): XY[] => r.map(([x, y]) => [Math.round(x * 10) / 10, Math.round(y * 10) / 10]);
const GS = 100;
function buildGrid() {
  grid = new Map(); detPath = new Path2D();
  dets.forEach((d, i) => {
    const xs = d.ring.map(p => p[0]), ys = d.ring.map(p => p[1]);
    for (let gx = Math.floor(Math.min(...xs) / GS); gx <= Math.floor(Math.max(...xs) / GS); gx++)
      for (let gy = Math.floor(Math.min(...ys) / GS); gy <= Math.floor(Math.max(...ys) / GS); gy++) { const k = gx + ',' + gy; if (!grid.has(k)) grid.set(k, []); grid.get(k)!.push(i); }
    detPath!.moveTo(...d.ring[0]); d.ring.slice(1).forEach(p => detPath!.lineTo(...p)); detPath!.closePath();
  });
}
function hitDet(x: number, y: number) { const c = grid.get(Math.floor(x / GS) + ',' + Math.floor(y / GS)) ?? []; let best = -1, ba = 1e12; for (const i of c) if (inRing(x, y, dets[i].ring)) { const a = area(dets[i].ring); if (a < ba) { ba = a; best = i; } } return best; }

// ---------- map ----------
async function openMap(id: string) {
  if (dirty && !confirm(T2('Neuložené opravy se zahodí. Pokračovat?', 'Unsaved corrections will be lost. Continue?'))) { ($('mapSel') as HTMLSelectElement).value = cur!.id; return; }
  cur = IDX.maps.find(m => m.id === id)!; dirty = false; sel = null; draft = [];
  status('…');
  imgs = (await Promise.all(cur.layers.map(async L => ({ L, im: await loadImg(dataUrl(L.url)) })))).filter(o => o.im) as { L: Layer; im: HTMLImageElement }[];
  dets = (await getJSON<{ polygons: Det[] }>(`${G}/detected/${id}.json`))?.polygons ?? []; buildGrid();
  const e = await getJSON<Edits>(`/manual/map_${id}.json`);
  edits = { map: id, year: cur.year, buildings: e?.buildings ?? [], removed: e?.removed ?? [] };
  removedIds = new Set(edits.removed.map(r => r.id));
  const F = IDX.frame, n = Math.round((F[2] - F[0]) / IDX.res);
  waterCv = document.createElement('canvas'); waterCv.width = waterCv.height = n; waterCtx = waterCv.getContext('2d')!;
  const wi = await loadImg(`/manual/water_${id}.png?${Date.now()}`);
  if (wi) { const t = document.createElement('canvas'); t.width = t.height = n; const tc = t.getContext('2d')!; tc.drawImage(wi, 0, 0, n, n);
    const d = tc.getImageData(0, 0, n, n), o = waterCtx.createImageData(n, n);
    for (let k = 0; k < d.data.length; k += 4) if (d.data[k] > 127) { o.data[k] = 47; o.data[k + 1] = 127; o.data[k + 2] = 208; o.data[k + 3] = 255; }
    waterCtx.putImageData(o, 0, 0); }
  buildModelPath();
  if (id.endsWith('_hi')) { view.cx = -822500; view.cy = -1069700; view.s = 0.7; }
  refresh(); draw();
  status(`${cur.label}: ${dets.length ? T2(dets.length + ' rozpoznaných půdorysů (modře)', dets.length + ' recognised footprints (blue)') : T2('bez automatického rozpoznání', 'no automatic recognition')}`);
}
function visible(b: number, y: number) { if (MODEL.from[b] > y || MODEL.to[b] <= y) return false; const g = MODEL.gaps[b] || []; for (let k = 0; k + 1 < g.length; k += 2) if (g[k] <= y && y < g[k + 1]) return false; return true; }
function buildModelPath() {
  modelPath = null; if (!MODEL || !cur) return;
  const y = cur.year + 0.01, [OX, OY] = MODEL.origin, skip = new Set(['moat', 'ditch'].map((c: string) => MODEL.classes.indexOf(c)));
  const p = new Path2D();
  for (let b = 0; b < MODEL.n; b++) { if (skip.has(MODEL.cls[b]) || !visible(b, y)) continue; const r = MODEL.rings[b];
    p.moveTo(r[0] / 10 + OX, r[1] / 10 + OY); for (let k = 2; k < r.length; k += 2) p.lineTo(r[k] / 10 + OX, r[k + 1] / 10 + OY); p.closePath(); }
  modelPath = p;
}

// ---------- drawing ----------
function draw() {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#e9e7e0'; ctx.fillRect(0, 0, cv.width, cv.height);
  if (!cur || !edits) return;
  const k = worldT();
  ctx.globalAlpha = +($('mapOp') as HTMLInputElement).value; ctx.imageSmoothingEnabled = view.s > 1.2;
  for (const { L, im } of imgs) {
    const sx = (L.bbox[2] - L.bbox[0]) / im.width, sy = (L.bbox[3] - L.bbox[1]) / im.height;
    if (L.cells) { const cw = im.width / 4, ch = im.height / 4;
      for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) { const [dx, dy] = L.cells[r][c]; ctx.save(); ctx.translate(L.bbox[0] + dx, L.bbox[3] + dy); ctx.scale(sx, -sy); ctx.drawImage(im, c * cw, r * ch, cw, ch, c * cw, r * ch, cw, ch); ctx.restore(); }
    } else { ctx.save(); ctx.translate(L.bbox[0], L.bbox[3]); ctx.scale(sx, -sy); ctx.drawImage(im, 0, 0); ctx.restore(); }
  }
  ctx.globalAlpha = 1;
  if (($('lWater') as HTMLInputElement).checked && waterCv) { const F = IDX.frame; ctx.save(); ctx.globalAlpha = 0.55; ctx.translate(F[0], F[3]); ctx.scale(IDX.res, -IDX.res); ctx.drawImage(waterCv, 0, 0); ctx.restore(); }
  if (($('lModel') as HTMLInputElement).checked && modelPath) { ctx.lineWidth = 1 / k; ctx.strokeStyle = 'rgba(90,90,90,.8)'; ctx.stroke(modelPath); }
  if (($('lDet') as HTMLInputElement).checked && detPath) {
    ctx.fillStyle = 'rgba(47,111,208,.22)'; ctx.fill(detPath); ctx.lineWidth = 2 / k; ctx.strokeStyle = 'rgba(25,80,200,1)'; ctx.stroke(detPath);
    ctx.setLineDash([5 / k, 4 / k]); ctx.strokeStyle = '#c02020'; ctx.lineWidth = 1.6 / k;
    for (const r of edits.removed) { ctx.beginPath(); r.ring.forEach((p, j) => j ? ctx.lineTo(...p) : ctx.moveTo(...p)); ctx.closePath(); ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.fill(); ctx.stroke(); }
    ctx.setLineDash([]);
  }
  if (($('lMan') as HTMLInputElement).checked) edits.buildings.forEach(b => { ctx.beginPath(); b.ring.forEach((p, j) => j ? ctx.lineTo(...p) : ctx.moveTo(...p)); ctx.closePath(); ctx.fillStyle = 'rgba(208,64,42,.28)'; ctx.fill(); ctx.lineWidth = 1.8 / k; ctx.strokeStyle = '#d0402a'; ctx.stroke(); });
  const sr = selRing();
  if (sr) { ctx.beginPath(); sr.forEach((p, j) => j ? ctx.lineTo(...p) : ctx.moveTo(...p)); ctx.closePath(); ctx.lineWidth = 3 / k; ctx.strokeStyle = '#e0a020'; ctx.stroke();
    for (const p of sr) { ctx.fillStyle = '#fff'; ctx.fillRect(p[0] - 3 / k, p[1] - 3 / k, 6 / k, 6 / k); ctx.strokeStyle = '#e0a020'; ctx.lineWidth = 1.5 / k; ctx.strokeRect(p[0] - 3 / k, p[1] - 3 / k, 6 / k, 6 / k); } }
  const dr = draftRing();
  if (dr.length) { ctx.beginPath(); dr.forEach((p, j) => j ? ctx.lineTo(...p) : ctx.moveTo(...p)); if (tool === 'rect' && dr.length === 4) ctx.closePath();
    ctx.lineWidth = 2 / k; ctx.strokeStyle = '#d0402a'; ctx.setLineDash([6 / k, 4 / k]); ctx.stroke(); ctx.setLineDash([]); }
  if ((tool === 'water' || tool === 'erase') && hover) { ctx.beginPath(); ctx.arc(hover[0], hover[1], +($('brush') as HTMLInputElement).value / 2, 0, 7); ctx.lineWidth = 1.5 / k; ctx.strokeStyle = '#2f7fd0'; ctx.stroke(); }
}
function selRing(): XY[] | null { if (!sel || !edits) return null; return sel.kind === 'det' ? dets[sel.i]?.ring ?? null : edits.buildings[sel.i]?.ring ?? null; }
function draftRing(): XY[] {
  if (tool === 'poly') return hover && draft.length ? [...draft, hover] : draft;
  if (tool === 'rect') { const pts = hover && draft.length < 3 ? [...draft, hover] : draft; if (pts.length < 3) return pts; return rectFrom(pts[0], pts[1], pts[2]); }
  return [];
}
function rectFrom(a: XY, b: XY, c: XY): XY[] { const ux = b[0] - a[0], uy = b[1] - a[1], L = Math.hypot(ux, uy) || 1; const nx = -uy / L, ny = ux / L; const d = (c[0] - a[0]) * nx + (c[1] - a[1]) * ny;
  return [a, b, [b[0] + nx * d, b[1] + ny * d], [a[0] + nx * d, a[1] + ny * d]]; }

// ---------- panel ----------
function refresh() {
  if (!edits) return;
  const nd = dets.length, nr = edits.removed.length, nb = edits.buildings.length;
  $('stats').innerHTML = `<span>${T2('rozpoznáno', 'recognised')}</span><b>${nd}</b><span>${T2('odebráno', 'rejected')}</span><b>${nr}</b><span>${T2('doplněno / upraveno', 'added / edited')}</span><b>${nb}</b>`;
  const b = sel?.kind === 'man' ? edits.buildings[sel.i] : null;
  $('selBox').hidden = !b;
  if (b) { ($('bFrom') as HTMLInputElement).value = b.from?.toString() ?? ''; ($('bTo') as HTMLInputElement).value = b.to?.toString() ?? ''; ($('bH') as HTMLInputElement).value = b.h?.toString() ?? ''; }
}
for (const [id, key] of [['bFrom', 'from'], ['bTo', 'to'], ['bH', 'h']] as const)
  $(id).oninput = () => { if (sel?.kind !== 'man' || !edits) return; const v = ($(id) as HTMLInputElement).value; (edits.buildings[sel.i] as any)[key] = v === '' ? undefined : +v; dirty = true; };
['lDet', 'lMan', 'lModel', 'lWater', 'mapOp'].forEach(id => $(id).addEventListener('input', draw));
document.querySelectorAll<HTMLButtonElement>('[data-tool]').forEach(b => b.onclick = () => { tool = b.dataset.tool!; draft = []; document.querySelectorAll('[data-tool]').forEach(x => x.classList.toggle('on', x === b)); draw(); });
($('mapSel') as HTMLSelectElement).onchange = () => openMap(($('mapSel') as HTMLSelectElement).value);

// ---------- editing actions ----------
function toManual(i: number) {   // an edited recognised footprint: rejected original + editable copy
  if (!edits) return -1;
  const d = dets[i]; if (!removedIds.has(d.id)) { edits.removed.push({ id: d.id, ring: d.ring }); removedIds.add(d.id); }
  edits.buildings.push({ ring: d.ring.map(p => [p[0], p[1]] as XY), src: d.id }); dirty = true; return edits.buildings.length - 1;
}
function finishDraft() {
  const r = tool === 'rect' ? (draft.length === 3 ? rectFrom(draft[0], draft[1], draft[2]) : []) : draft;
  if (r.length >= 3 && edits && area(r) > 4) { edits.buildings.push({ ring: r1(r) }); sel = { kind: 'man', i: edits.buildings.length - 1 }; dirty = true; }
  draft = []; refresh(); draw();
}
function deleteSel() {
  if (!sel || !edits) return;
  if (sel.kind === 'det') { const d = dets[sel.i];
    if (removedIds.has(d.id)) { edits.removed = edits.removed.filter(r => r.id !== d.id); removedIds.delete(d.id); edits.buildings = edits.buildings.filter(b => b.src !== d.id); }
    else { edits.removed.push({ id: d.id, ring: d.ring }); removedIds.add(d.id); }
  } else edits.buildings.splice(sel.i, 1), sel = null;
  dirty = true; refresh(); draw();
}
let lastPaint: XY | null = null;
function paint(x: number, y: number) {
  if (!waterCtx || !edits) return; const F = IDX.frame, r = Math.max(+($('brush') as HTMLInputElement).value / 2 / IDX.res, 0.7);
  const u = (x - F[0]) / IDX.res, v = (F[3] - y) / IDX.res;
  waterCtx.globalCompositeOperation = tool === 'erase' ? 'destination-out' : 'source-over';
  waterCtx.fillStyle = waterCtx.strokeStyle = '#2f7fd0'; waterCtx.lineCap = 'round'; waterCtx.lineWidth = 2 * r;
  if (lastPaint) { waterCtx.beginPath(); waterCtx.moveTo(...lastPaint); waterCtx.lineTo(u, v); waterCtx.stroke(); }
  waterCtx.beginPath(); waterCtx.arc(u, v, r, 0, 7); waterCtx.fill(); lastPaint = [u, v];
  waterCtx.globalCompositeOperation = 'source-over'; edits.waterEdited = true; dirty = true;
}
async function save() {
  if (!cur || !edits) return;
  try {
    const body = { ...edits, buildings: edits.buildings.map(b => ({ ...b, ring: r1(b.ring) })), saved: new Date().toISOString() };
    let r = await fetch(`/api/manual/map_${cur.id}.json`, { method: 'POST', body: JSON.stringify(body, null, 1) }); if (!r.ok) throw new Error(String(r.status));
    if (edits.waterEdited && waterCv && waterCtx) { const n = waterCv.width, t = document.createElement('canvas'); t.width = t.height = n; const tc = t.getContext('2d')!;
      tc.fillStyle = '#000'; tc.fillRect(0, 0, n, n); const d = waterCtx.getImageData(0, 0, n, n), o = tc.getImageData(0, 0, n, n);
      for (let k = 0; k < d.data.length; k += 4) if (d.data[k + 3] > 100) o.data[k] = o.data[k + 1] = o.data[k + 2] = 255;
      tc.putImageData(o, 0, 0); r = await fetch(`/api/manual/water_${cur.id}.png`, { method: 'POST', body: t.toDataURL('image/png') }); if (!r.ok) throw new Error(String(r.status)); }
    dirty = false; status(T2('uloženo ', 'saved ') + new Date().toLocaleTimeString());
  } catch (e) { status('ERROR ' + (e as Error).message); }
}
$('save').onclick = save;
addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });

// ---------- mouse ----------
let drag: number[] | null = null, vdrag: number | null = null, space = false, painting = false;
const near = (a: XY, b: XY) => Math.hypot(a[0] - b[0], a[1] - b[1]) < 7 * view.s;
cv.addEventListener('wheel', e => { e.preventDefault(); const [u, v] = evPos(e), [x, y] = S2W(u, v); view.s = Math.min(Math.max(view.s * Math.exp(e.deltaY * 0.0015), 0.05), 12); const [x2, y2] = S2W(u, v); view.cx += x - x2; view.cy += y - y2; draw(); }, { passive: false });
cv.addEventListener('contextmenu', e => e.preventDefault());
cv.addEventListener('mousedown', e => {
  const [u, v] = evPos(e); const p = S2W(u, v);
  if (e.button === 1 || space) { drag = [u, v, view.cx, view.cy]; return; }
  if (!edits || e.button !== 0) return;
  if (tool === 'water' || tool === 'erase') { painting = true; paint(...p); draw(); return; }
  if (tool === 'poly') { draft.push(p); draw(); return; }
  if (tool === 'rect') { draft.push(p); if (draft.length === 3) finishDraft(); else draw(); return; }
  // select / edit: vertex of the selected footprint first
  const sr = selRing();
  if (sr) { const vi = sr.findIndex(q => near(q, p));
    if (vi >= 0) {
      if (sel!.kind === 'det') { const ni = toManual(sel!.i); sel = { kind: 'man', i: ni }; }
      const ring = edits.buildings[sel!.i].ring;
      if (e.altKey) { if (ring.length > 3) ring.splice(vi, 1); dirty = true; refresh(); draw(); return; }
      vdrag = vi; return;
    } }
  const mi = edits.buildings.findIndex(b => inRing(p[0], p[1], b.ring));
  if (mi >= 0) { sel = { kind: 'man', i: mi }; refresh(); draw(); return; }
  const di = ($('lDet') as HTMLInputElement).checked ? hitDet(...p) : -1;
  sel = di >= 0 ? { kind: 'det', i: di } : null;
  if (!sel) drag = [u, v, view.cx, view.cy];   // empty place: pan
  refresh(); draw();
});
addEventListener('mousemove', e => {
  const [u, v] = evPos(e);
  if (drag) { const k = view.s / DPR(); view.cx = drag[2] - (u - drag[0]) * k; view.cy = drag[3] + (v - drag[1]) * k; draw(); return; }
  const p = S2W(u, v); hover = p;
  $('coord').textContent = `S-JTSK ${p[0].toFixed(1)}, ${p[1].toFixed(1)} · ${view.s.toFixed(2)} m/px`;
  if (vdrag !== null && sel?.kind === 'man' && edits) { edits.buildings[sel.i].ring[vdrag] = p; dirty = true; draw(); return; }
  if (painting) paint(...p);
  if (draft.length || painting || tool === 'water' || tool === 'erase') draw();
});
addEventListener('mouseup', () => { if (vdrag !== null && sel?.kind === 'man' && edits) edits.buildings[sel.i].ring = r1(edits.buildings[sel.i].ring); drag = null; vdrag = null; painting = false; lastPaint = null; });
cv.addEventListener('dblclick', e => {
  if (tool === 'poly') { draft.pop(); finishDraft(); return; }
  const p = S2W(...evPos(e)); const sr = selRing(); if (!sr || !edits) return;
  let best = -1, bd = 1e9; sr.forEach((a, i) => { const d = segDist(p, a, sr[(i + 1) % sr.length]); if (d < bd) { bd = d; best = i; } });
  if (bd > 8 * view.s) return;
  if (sel!.kind === 'det') sel = { kind: 'man', i: toManual(sel!.i) };
  edits.buildings[sel!.i].ring.splice(best + 1, 0, p); dirty = true; refresh(); draw();
});
addEventListener('keydown', e => {
  const tg = e.target as HTMLElement; if (tg.tagName === 'INPUT' && (tg as HTMLInputElement).type !== 'range' && (tg as HTMLInputElement).type !== 'checkbox') return;
  if (e.code === 'Space') { space = true; e.preventDefault(); }
  if (e.key === 'Enter' && tool === 'poly') finishDraft();
  if (e.key === 'Escape') { draft = []; sel = null; refresh(); draw(); }
  if (e.key === 'Delete' || e.key === 'Backspace') deleteSel();
  if (e.key === 's' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); void save(); }
});
addEventListener('keyup', e => { if (e.code === 'Space') space = false; });

// ---------- steps and pipeline ----------
function showStep(n: number) { document.querySelectorAll<HTMLElement>('.step').forEach(s => s.classList.toggle('on', s.dataset.step === String(n))); for (let k = 1; k <= 4; k++) $('p' + k).hidden = k !== n; }
document.querySelectorAll<HTMLElement>('.step').forEach(s => s.onclick = () => showStep(+s.dataset.step!));
const logEl = $('log');
async function runStep(step: string, mark: number) {
  if (dirty) await save();
  const r = await fetch(`/api/run/${step}`, { method: 'POST' });
  if (!r.ok) { status(T2('úloha už běží nebo není dostupná (spuštěno přes npm run dev?)', 'a task is already running or not available (started with npm run dev?)')); return; }
  logEl.classList.add('open'); status(T2('běží…', 'running…'));
  const poll = async () => {
    const s = await getJSON<{ running: boolean; code: number | null; log: string[] }>('/api/run'); if (!s) return;
    logEl.textContent = s.log.join('\n'); logEl.scrollTop = logEl.scrollHeight;
    if (s.running) { setTimeout(poll, 1000); return; }
    if (s.code === 0) { status(T2('hotovo', 'done')); document.querySelector(`.step[data-step="${mark}"]`)?.classList.add('done');
      if (step === 'detect') { await init(false); } else { MODEL = await getJSON(`${G}/web/model.json`); buildModelPath(); draw(); } }
    else status(T2('chyba – viz log', 'error – see the log'));
  };
  setTimeout(poll, 800);
}
$('runDetect').onclick = () => runStep('detect', 1);
$('runModel').onclick = () => runStep('model', 3);
$('runVed').onclick = () => runStep('vedute', 3);

async function init(first = true) {
  IDX = (await getJSON<typeof IDX>('/manual/maps.json'))!;
  const det = new Set(((await getJSON<{ map: string }[]>(`${G}/detected/index.json`)) ?? []).map(d => d.map));
  const sel_ = $('mapSel') as HTMLSelectElement; const keep = sel_.value; sel_.innerHTML = '';
  for (const m of IDX.maps) sel_.add(new Option(`${m.year} · ${m.label}${det.has(m.id) ? '' : T2(' (bez rozpoznání)', ' (no recognition)')}`, m.id));
  if (first) { resize(); MODEL = await getJSON(`${G}/web/model.json`); }
  const start = keep || (IDX.maps.find(m => m.id === '1902_hi') ?? IDX.maps[0]).id;
  sel_.value = start; dirty = false; await openMap(start);
}
void init();

// debug handle (dev)
(window as any).__wb = { get edits() { return edits; }, get draft() { return draft; }, get tool() { return tool; }, get sel() { return sel; }, get view() { return view; }, get dets() { return dets; } };
