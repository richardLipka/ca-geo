// Map pane in EPSG:5514: reference raster (<img> from WMS / ArcGIS export), warped source
// overlays (WebGL) and vectors (entities, control points, drawing) on a 2D canvas.

import { getImage } from './images';
import { REF_LAYERS } from './layers';
import { activeIn, entityAnchor, uid, type Entity, type EntityType } from './model';
import { fromWgs } from './proj';
import { store } from './store';
import { t } from './i18n';
import type { Vec2 } from './transform';
import { WarpLayer } from './warp';

export const TYPE_COLOUR: Record<EntityType, string> = {
  building: '#c92a2a', church: '#862e9c', tower: '#5f3dc4', gate: '#e67700', bastion: '#2b8a3e', wall: '#495057',
  moat: '#1864ab', water: '#1c7ed6', bridge: '#a61e4d', street: '#868e96', other: '#343a40',
};

interface Amcr { id: string; y: string; lat: number; lon: number; fort: boolean; loc: string }

export class MapView {
  c: Vec2 = [-822410, -1069700]; // view centre
  res = 1.2; // metres per CSS pixel
  private ctx: CanvasRenderingContext2D;
  private warp: WarpLayer;
  private refImg: HTMLImageElement;
  private refBox: number[] | null = null; private refTimer = 0; private refKey = '';
  private drag: { x: number; y: number; c: Vec2; moved: boolean } | null = null;
  private amcr: (Amcr & { p: Vec2 })[] | null = null;
  private mouse: Vec2 | null = null;

  constructor(private root: HTMLElement, private vec: HTMLCanvasElement, gl: HTMLCanvasElement, private hint: HTMLElement, private coords: HTMLElement) {
    this.ctx = vec.getContext('2d')!;
    this.warp = new WarpLayer(gl);
    this.refImg = root.querySelector('img.ref') as HTMLImageElement;
    this.refImg.addEventListener('load', () => this.render());
    new ResizeObserver(() => { this.render(); this.requestRef(); }).observe(root);
    vec.addEventListener('wheel', e => this.onWheel(e), { passive: false });
    vec.addEventListener('pointerdown', e => { vec.setPointerCapture(e.pointerId); this.drag = { x: e.clientX, y: e.clientY, c: [...this.c] as Vec2, moved: false }; });
    vec.addEventListener('pointermove', e => {
      this.mouse = this.toMap(e);
      this.coords.textContent = `X ${this.mouse[0].toFixed(1)}  Y ${this.mouse[1].toFixed(1)}  (EPSG:5514)`;
      if (this.drag) {
        const dx = e.clientX - this.drag.x, dy = e.clientY - this.drag.y;
        if (Math.abs(dx) + Math.abs(dy) > 4) this.drag.moved = true;
        if (this.drag.moved) { this.c = [this.drag.c[0] - dx * this.res, this.drag.c[1] + dy * this.res]; this.requestRef(); }
      }
      this.render();
    });
    vec.addEventListener('pointerup', e => { const d = this.drag; this.drag = null; if (d && !d.moved) this.onClick(e); });
    vec.addEventListener('dblclick', e => { e.preventDefault(); this.finishDrawing(); });
    vec.addEventListener('pointerleave', () => { this.mouse = null; this.render(); });
  }

  toMap(e: MouseEvent): Vec2 { const r = this.vec.getBoundingClientRect(); return [this.c[0] + (e.clientX - r.left - r.width / 2) * this.res, this.c[1] - (e.clientY - r.top - r.height / 2) * this.res]; }
  toScr(p: Vec2): Vec2 { const w = this.vec.clientWidth, h = this.vec.clientHeight; return [(p[0] - this.c[0]) / this.res + w / 2, h / 2 - (p[1] - this.c[1]) / this.res]; }
  centreOn(p: Vec2) { this.c = [...p] as Vec2; this.requestRef(); this.render(); }

  private onWheel(e: WheelEvent) {
    e.preventDefault();
    const before = this.toMap(e), k = Math.exp(e.deltaY * 0.0015);
    this.res = Math.min(Math.max(this.res * k, 0.05), 50);
    const after = this.toMap(e);
    this.c = [this.c[0] + before[0] - after[0], this.c[1] + before[1] - after[1]];
    this.requestRef(); this.render();
  }

  private hitEntity(p: Vec2): Entity | null {
    let best: Entity | null = null, bd = 10 * this.res;
    for (const e of store.project.entities) {
      if (!activeIn(e, store.ui.year) || !e.geom) continue;
      const cs = e.geom.coords;
      let d = Infinity;
      if (e.geom.type === 'Point') d = Math.hypot(cs[0][0] - p[0], cs[0][1] - p[1]);
      else {
        const ring = e.geom.type === 'Polygon' ? [...cs, cs[0]] : cs;
        for (let i = 1; i < ring.length; i++) d = Math.min(d, segDist(p, ring[i - 1], ring[i]));
        if (e.geom.type === 'Polygon' && inside(p, cs)) d = Math.min(d, bd * 0.9);
      }
      if (d < bd) { bd = d; best = e; }
    }
    return best;
  }

  private onClick(e: PointerEvent) {
    const p = this.toMap(e), ui = store.ui, src = store.source;
    if (ui.tool === 'gcp' && src) {
      if (ui.pendingImg) {
        const img = ui.pendingImg;
        store.change(pr => { (pr.gcps[src.id] ??= []).push({ id: uid('g'), img, map: p, enabled: true }); });
        store.setUi({ pendingImg: null, pendingMap: null });
      } else store.setUi({ pendingMap: p });
      return;
    }
    if (ui.tool.startsWith('draw-')) {
      store.ui.drawing.push(p);
      if (ui.tool === 'draw-point') this.finishDrawing(); else this.render();
      return;
    }
    if (ui.tool === 'identify' && ui.selAnnotation) {
      const a = store.project.annotations.find(x => x.id === ui.selAnnotation);
      if (a && !a.entityId) { // link to an existing entity, or create a new point entity here
        const hit = this.hitEntity(p);
        if (hit) { store.change(() => { a.entityId = hit.id; }); store.setUi({ selEntity: hit.id }); }
        else {
          const id = uid('e'), n = store.project.entities.length + 1;
          store.change(pr => { pr.entities.push({ id, name: a.label ? a.label : t('ent.newName', { n }), type: 'building', geom: { type: 'Point', coords: [p] } }); a.entityId = id; });
          store.setUi({ selEntity: id, tab: 'entities' });
        }
        return;
      }
    }
    const hit = this.hitEntity(p);
    store.setUi({ selEntity: hit?.id ?? null, tab: hit ? 'entities' : store.ui.tab });
  }

  finishDrawing() {
    const ui = store.ui; if (!ui.tool.startsWith('draw-')) return;
    const pts = ui.drawing, type = ui.tool === 'draw-point' ? 'Point' : ui.tool === 'draw-line' ? 'LineString' : 'Polygon';
    const need = type === 'Point' ? 1 : type === 'LineString' ? 2 : 3;
    if (pts.length < need) { store.setUi({ drawing: [] }); return; }
    const geom = { type, coords: type === 'Point' ? [pts[0]] : pts.slice() } as Entity['geom'];
    const target = store.entity(ui.selEntity);
    if (target && ui.redraw) store.change(() => { target.geom = geom; });
    else {
      const id = uid('e'), n = store.project.entities.length + 1;
      store.change(pr => pr.entities.push({ id, name: t('ent.newName', { n }), type: type === 'Polygon' ? 'building' : type === 'LineString' ? 'wall' : 'other', geom }));
      store.setUi({ selEntity: id, tab: 'entities' });
    }
    store.setUi({ drawing: [], redraw: false });
  }

  requestRef() {
    clearTimeout(this.refTimer);
    this.refTimer = window.setTimeout(() => {
      const L = REF_LAYERS.find(l => l.id === store.ui.refLayer);
      const w = this.root.clientWidth, h = this.root.clientHeight;
      if (!L || L.id === 'none' || !w || !h) { this.refImg.removeAttribute('src'); this.refBox = null; this.render(); return; }
      const k = Math.min(Math.min(devicePixelRatio || 1, 2), 4096 / Math.max(w, h));
      const box = [this.c[0] - w / 2 * this.res, this.c[1] - h / 2 * this.res, this.c[0] + w / 2 * this.res, this.c[1] + h / 2 * this.res].map(v => Math.round(v * 10) / 10);
      const url = L.url(box, Math.round(w * k), Math.round(h * k));
      if (url === this.refKey) return;
      this.refKey = url;
      const probe = new Image();
      probe.onload = () => { this.refImg.src = url; this.refBox = box; this.render(); };
      probe.src = url;
    }, 200);
  }

  async toggleAmcr(on: boolean) {
    if (on && !this.amcr) {
      try {
        const r = await fetch('/data/reference/plzen-amcr/akce-compact.json');
        const d = (await r.json()) as Amcr[];
        this.amcr = d.map(o => ({ ...o, p: fromWgs([o.lon, o.lat]) }));
      } catch { this.amcr = []; }
    }
    this.render();
  }

  render() {
    const w = this.vec.clientWidth, h = this.vec.clientHeight, dpr = Math.min(devicePixelRatio || 1, 2);
    if (this.vec.width !== Math.round(w * dpr) || this.vec.height !== Math.round(h * dpr)) { this.vec.width = Math.round(w * dpr); this.vec.height = Math.round(h * dpr); }
    // reference image placement
    if (this.refBox && this.refImg.getAttribute('src')) {
      const a = this.toScr([this.refBox[0], this.refBox[3]]), b = this.toScr([this.refBox[2], this.refBox[1]]);
      Object.assign(this.refImg.style, { left: a[0] + 'px', top: a[1] + 'px', width: b[0] - a[0] + 'px', height: b[1] - a[1] + 'px', opacity: String(store.ui.refOpacity), display: 'block' });
    } else this.refImg.style.display = 'none';
    // warped overlays
    const layers = [];
    for (const s of store.project.sources) {
      if (!s.overlay || s.kind === 'panorama') continue;
      const f = store.fitOf(s).fit; const img = getImage(s.file);
      if (f && img) layers.push({ id: s.id, url: s.file, img, fit: f, key: s.method + JSON.stringify(store.controls(s).map(c => [c.img, c.map])), opacity: s.opacity });
    }
    this.warp.draw(layers, this.c, this.res);

    const g = this.ctx; g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    const ui = store.ui;
    // AMČR archaeology
    if (ui.showAmcr && this.amcr) for (const o of this.amcr) {
      const q = this.toScr(o.p); g.beginPath(); g.arc(q[0], q[1], o.fort ? 5 : 3.5, 0, 7);
      g.fillStyle = o.fort ? 'rgba(224,49,49,.85)' : 'rgba(25,113,194,.55)'; g.fill();
    }
    // entities
    for (const e of store.project.entities) {
      if (!e.geom || !activeIn(e, ui.year)) continue;
      const sel = e.id === ui.selEntity, col = TYPE_COLOUR[e.type] ?? '#333';
      const pts = e.geom.coords.map(p => this.toScr(p));
      g.lineWidth = sel ? 3.5 : 2; g.strokeStyle = sel ? '#e8590c' : col;
      if (e.geom.type === 'Point') { g.beginPath(); g.arc(pts[0][0], pts[0][1], sel ? 7 : 5, 0, 7); g.fillStyle = sel ? '#e8590c' : col; g.fill(); g.lineWidth = 1.5; g.strokeStyle = '#fff'; g.stroke(); }
      else {
        g.beginPath(); pts.forEach((q, i) => (i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])));
        if (e.geom.type === 'Polygon') { g.closePath(); g.fillStyle = hexA(sel ? '#e8590c' : col, 0.18); g.fill(); }
        g.stroke();
      }
      const a = entityAnchor(e); if (a && (sel || this.res < 1.5)) label(g, this.toScr(a), e.name, sel ? '#e8590c' : col);
    }
    // control points of the current source + predicted position of the selected annotation
    const src = store.source;
    if (src) {
      const fitRes = store.fitOf(src);
      (store.project.gcps[src.id] ?? []).forEach((gp, i) => {
        const q = this.toScr(gp.map);
        g.beginPath(); g.rect(q[0] - 5, q[1] - 5, 10, 10); g.fillStyle = gp.enabled ? '#d9480f' : '#adb5bd'; g.fill(); g.strokeStyle = '#fff'; g.lineWidth = 1.5; g.stroke();
        label(g, q, `G${i + 1}`, '#d9480f');
        if (fitRes.fit && gp.enabled) { // residual vector, exaggerated ×5
          const f = fitRes.fit.forward(gp.img), r = this.toScr(f);
          g.beginPath(); g.moveTo(q[0], q[1]); g.lineTo(q[0] + (r[0] - q[0]) * 5, q[1] + (r[1] - q[1]) * 5); g.strokeStyle = '#d9480f'; g.lineWidth = 1.5; g.stroke();
        }
      });
      const selA = store.project.annotations.find(a => a.id === ui.selAnnotation && a.sourceId === src.id);
      if (selA && fitRes.fit) {
        const q = this.toScr(fitRes.fit.forward(selA.img));
        g.strokeStyle = '#2f9e44'; g.lineWidth = 2; g.beginPath(); g.arc(q[0], q[1], 12, 0, 7); g.moveTo(q[0] - 18, q[1]); g.lineTo(q[0] + 18, q[1]); g.moveTo(q[0], q[1] - 18); g.lineTo(q[0], q[1] + 18); g.stroke();
        label(g, q, t('map.predicted'), '#2f9e44');
      }
      if (fitRes.pano) { // viewpoint and sight lines of a panorama
        const v = this.toScr([fitRes.pano.X0, fitRes.pano.Y0]);
        g.fillStyle = '#2f9e44'; g.beginPath(); g.arc(v[0], v[1], 7, 0, 7); g.fill(); label(g, v, t('map.viewpoint'), '#2f9e44');
        g.strokeStyle = 'rgba(47,158,68,.6)'; g.lineWidth = 1;
        for (const c of store.controls(src)) { const q = this.toScr(c.map); g.beginPath(); g.moveTo(v[0], v[1]); g.lineTo(q[0], q[1]); g.stroke(); }
      }
    }
    if (ui.pendingMap) { const q = this.toScr(ui.pendingMap); g.strokeStyle = '#e03131'; g.lineWidth = 2; g.beginPath(); g.moveTo(q[0] - 9, q[1]); g.lineTo(q[0] + 9, q[1]); g.moveTo(q[0], q[1] - 9); g.lineTo(q[0], q[1] + 9); g.stroke(); }
    if (ui.drawing.length) {
      const pts = [...ui.drawing, ...(this.mouse ? [this.mouse] : [])].map(p => this.toScr(p));
      g.strokeStyle = '#e8590c'; g.lineWidth = 2; g.setLineDash([5, 4]); g.beginPath(); pts.forEach((q, i) => (i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1]))); if (ui.tool === 'draw-polygon') g.closePath(); g.stroke(); g.setLineDash([]);
    }
    // scale bar
    const target = 100 * this.res, pow = 10 ** Math.floor(Math.log10(target)), len = [1, 2, 5].map(k => k * pow).reverse().find(v => v <= target) ?? pow;
    const px = len / this.res; g.fillStyle = 'rgba(255,255,255,.85)'; g.fillRect(10, h - 28, px + 16, 20);
    g.fillStyle = '#212529'; g.fillRect(18, h - 14, px, 3); g.font = '11px system-ui'; g.fillText(`${len} m`, 18, h - 17);
    this.hint.textContent = t('hint.map.' + (ui.tool.startsWith('draw-') ? 'draw' : ui.tool));
  }
}

function segDist(p: Vec2, a: Vec2, b: Vec2) { const vx = b[0] - a[0], vy = b[1] - a[1], l = vx * vx + vy * vy || 1e-9; let k = ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / l; k = Math.max(0, Math.min(1, k)); return Math.hypot(a[0] + k * vx - p[0], a[1] + k * vy - p[1]); }
function inside(p: Vec2, ring: Vec2[]) { let c = false; for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) { const [xi, yi] = ring[i], [xj, yj] = ring[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < ((xj - xi) * (p[1] - yi)) / (yj - yi) + xi) c = !c; } return c; }
function hexA(hex: string, a: number) { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }
function label(g: CanvasRenderingContext2D, p: Vec2, s: string, col: string) { if (!s) return; g.font = '600 12px system-ui'; g.lineWidth = 3; g.strokeStyle = 'rgba(255,255,255,.9)'; g.strokeText(s, p[0] + 8, p[1] - 8); g.fillStyle = col; g.fillText(s, p[0] + 8, p[1] - 8); }
