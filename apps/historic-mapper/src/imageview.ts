// Image pane: pan/zoom a source image, place control points and identity annotations,
// and show where the current transform expects known entities (ghost markers / guide lines).

import { getImage, imageFailed } from './images';
import { entityAnchor, uid, type Annotation } from './model';
import { store } from './store';
import { t } from './i18n';
import type { Vec2 } from './transform';

const COL = { gcp: '#d9480f', link: '#1971c2', ann: '#1971c2', annFree: '#868e96', ghost: '#2f9e44', sel: '#e8590c', pending: '#e03131' };

export class ImageView {
  private ctx: CanvasRenderingContext2D;
  private scale = 1; private ox = 0; private oy = 0; // screen = img * scale + o
  private fittedFor = ''; private fittedSize = ''; private userMoved = false;
  private drag: { x: number; y: number; ox: number; oy: number; moved: boolean } | null = null;

  constructor(private canvas: HTMLCanvasElement, private hint: HTMLElement) {
    this.ctx = canvas.getContext('2d')!;
    new ResizeObserver(() => this.render()).observe(canvas);
    canvas.addEventListener('wheel', e => this.onWheel(e), { passive: false });
    canvas.addEventListener('pointerdown', e => { canvas.setPointerCapture(e.pointerId); this.drag = { x: e.clientX, y: e.clientY, ox: this.ox, oy: this.oy, moved: false }; });
    canvas.addEventListener('pointermove', e => {
      if (!this.drag) return;
      const dx = e.clientX - this.drag.x, dy = e.clientY - this.drag.y;
      if (Math.abs(dx) + Math.abs(dy) > 4) this.drag.moved = true;
      if (this.drag.moved) { this.ox = this.drag.ox + dx; this.oy = this.drag.oy + dy; this.userMoved = true; this.render(); }
    });
    canvas.addEventListener('pointerup', e => { const d = this.drag; this.drag = null; if (d && !d.moved) this.onClick(e); });
    canvas.addEventListener('dblclick', e => { e.preventDefault(); this.finishOutline(); });
  }

  toImg(e: MouseEvent): Vec2 { const r = this.canvas.getBoundingClientRect(); return [(e.clientX - r.left - this.ox) / this.scale, (e.clientY - r.top - this.oy) / this.scale]; }
  toScr(p: Vec2): Vec2 { return [p[0] * this.scale + this.ox, p[1] * this.scale + this.oy]; }

  private onWheel(e: WheelEvent) {
    e.preventDefault();
    const r = this.canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    const k = Math.exp(-e.deltaY * 0.0015);
    this.ox = mx - (mx - this.ox) * k; this.oy = my - (my - this.oy) * k; this.scale *= k; this.userMoved = true;
    this.render();
  }

  /** Centre the view on an image point. */
  centreOn(p: Vec2) { this.userMoved = true; const w = this.canvas.clientWidth, h = this.canvas.clientHeight; this.ox = w / 2 - p[0] * this.scale; this.oy = h / 2 - p[1] * this.scale; this.render(); }

  private hitAnnotation(p: Vec2): Annotation | null {
    const src = store.source; if (!src) return null;
    let best: Annotation | null = null, bd = 12 / this.scale;
    for (const a of store.annotationsOf(src.id)) { const d = Math.hypot(a.img[0] - p[0], a.img[1] - p[1]); if (d < bd) { bd = d; best = a; } }
    return best;
  }

  private onClick(e: PointerEvent) {
    const src = store.source; if (!src) return;
    const p = this.toImg(e), ui = store.ui;
    if (ui.tool === 'gcp') {
      if (ui.pendingMap) {
        const map = ui.pendingMap;
        store.change(pr => { (pr.gcps[src.id] ??= []).push({ id: uid('g'), img: p, map, enabled: true }); });
        store.setUi({ pendingMap: null, pendingImg: null });
      } else store.setUi({ pendingImg: p });
      return;
    }
    if (ui.tool === 'outline') { store.ui.outline.push(p); this.render(); return; }
    if (ui.tool === 'identify') {
      const hit = this.hitAnnotation(p);
      if (hit) { store.setUi({ selAnnotation: hit.id, selEntity: hit.entityId, tab: 'identity', pendingImg: null }); return; }
      const id = uid('a');
      store.change(pr => pr.annotations.push({ id, sourceId: src.id, img: p, entityId: null, confidence: 2, useAsControl: true }));
      store.setUi({ selAnnotation: id, tab: 'identity' });
      return;
    }
    const hit = this.hitAnnotation(p);
    store.setUi({ selAnnotation: hit?.id ?? null, selEntity: hit?.entityId ?? store.ui.selEntity });
  }

  /** Close the outline being drawn into a new annotation (centroid = marker position). */
  finishOutline() {
    const src = store.source, pts = store.ui.outline;
    if (!src || store.ui.tool !== 'outline') return;
    if (pts.length < 3) { store.setUi({ outline: [] }); return; }
    const c: Vec2 = [pts.reduce((s, q) => s + q[0], 0) / pts.length, pts.reduce((s, q) => s + q[1], 0) / pts.length];
    const id = uid('a');
    store.change(pr => pr.annotations.push({ id, sourceId: src.id, img: c, shape: pts.slice(), kind: 'house', entityId: null, confidence: 2, useAsControl: false }));
    store.setUi({ outline: [], selAnnotation: id, tab: 'identity' });
  }

  render() {
    const c = this.canvas, dpr = Math.min(devicePixelRatio || 1, 2);
    const w = c.clientWidth, h = c.clientHeight;
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) { c.width = Math.round(w * dpr); c.height = Math.round(h * dpr); }
    const g = this.ctx; g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    const src = store.source;
    if (!src) { this.hint.textContent = t('img.noSource'); return; }
    const img = getImage(src.file);
    if (!img) { this.hint.textContent = imageFailed(src.file) ? t('img.failed', { file: src.file }) : t('img.loading'); return; }
    this.hint.textContent = t('hint.' + store.ui.tool);
    const size = `${w}x${h}`;
    if (this.fittedFor !== src.id || (!this.userMoved && this.fittedSize !== size)) { // fit image to pane on first show / resize
      this.scale = Math.min(w / img.naturalWidth, h / img.naturalHeight) * 0.95;
      this.ox = (w - img.naturalWidth * this.scale) / 2; this.oy = (h - img.naturalHeight * this.scale) / 2;
      if (this.fittedFor !== src.id) this.userMoved = false;
      this.fittedFor = src.id; this.fittedSize = size;
    }
    g.imageSmoothingQuality = 'high';
    g.drawImage(img, this.ox, this.oy, img.naturalWidth * this.scale, img.naturalHeight * this.scale);

    const res = store.fitOf(src);
    // predicted positions of entities (inverse transform) — help to find what is where
    if (res.fit) {
      const linked = new Set(store.annotationsOf(src.id).map(a => a.entityId));
      for (const e of store.project.entities) {
        if (e.type === 'building' && e.id !== store.ui.selEntity) continue; // too many to show as hints
        const m = entityAnchor(e); if (!m || linked.has(e.id)) continue;
        const q = this.toScr(res.fit.inverse(m));
        if (q[0] < -20 || q[1] < -20 || q[0] > w + 20 || q[1] > h + 20) continue;
        this.cross(q, COL.ghost, 5); this.label(q, e.name, COL.ghost, true);
      }
    }
    if (res.pano) { // vertical guide lines at predicted columns
      g.save(); g.setLineDash([4, 4]); g.lineWidth = 1;
      for (const e of store.project.entities) {
        if (e.type === 'building' && e.id !== store.ui.selEntity) continue;
        const m = entityAnchor(e); if (!m) continue;
        const x = res.pano.project(m); if (x === null) continue;
        const sx = x * this.scale + this.ox; if (sx < 0 || sx > w) continue;
        g.strokeStyle = e.id === store.ui.selEntity ? COL.sel : COL.ghost;
        g.beginPath(); g.moveTo(sx, 0); g.lineTo(sx, h); g.stroke();
        g.fillStyle = g.strokeStyle; g.font = '11px system-ui'; g.fillText(e.name, sx + 3, 14);
      }
      g.restore();
    }
    // control points
    const gcps = store.project.gcps[src.id] ?? [];
    const ctrl = store.controls(src), resid = new Map<string, number>();
    if (res.fit) ctrl.forEach((cc, i) => resid.set(cc.id, res.fit!.loo[i]));
    gcps.forEach((gp, i) => {
      const q = this.toScr(gp.img);
      this.dot(q, gp.enabled ? COL.gcp : '#adb5bd', gp.id === store.ui.selGcp ? 7 : 5);
      const r = resid.get(gp.id);
      this.label(q, `G${i + 1}${r !== undefined && Number.isFinite(r) ? ` · ${r.toFixed(1)} m` : ''}`, COL.gcp);
    });
    // annotations (outlines first, then markers)
    for (const a of store.annotationsOf(src.id)) {
      if (!a.shape) continue;
      const sel = a.id === store.ui.selAnnotation, pts = a.shape.map(p => this.toScr(p));
      g.beginPath(); pts.forEach((q, i) => (i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1]))); g.closePath();
      g.fillStyle = sel ? 'rgba(232,89,12,.22)' : a.entityId ? 'rgba(25,113,194,.14)' : 'rgba(134,142,150,.12)'; g.fill();
      g.lineWidth = sel ? 2.5 : 1.5; g.strokeStyle = sel ? COL.sel : a.entityId ? COL.ann : '#495057'; g.stroke();
    }
    if (store.ui.outline.length) {
      const pts = store.ui.outline.map(p => this.toScr(p));
      g.setLineDash([5, 4]); g.strokeStyle = COL.sel; g.lineWidth = 2; g.beginPath(); pts.forEach((q, i) => (i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1]))); g.stroke(); g.setLineDash([]);
      pts.forEach(q => this.dot(q, COL.sel, 3));
    }
    for (const a of store.annotationsOf(src.id)) {
      const q = this.toScr(a.img), e = store.entity(a.entityId), sel = a.id === store.ui.selAnnotation || (e && e.id === store.ui.selEntity);
      this.ring(q, sel ? COL.sel : e ? COL.ann : COL.annFree, sel ? 9 : 7);
      const txt = [a.label, e?.name ?? (a.kind ? t('kind.ann.' + a.kind) : '')].filter(Boolean).join(' · ') || t('ann.unlinked');
      this.label(q, txt, sel ? COL.sel : e ? COL.ann : COL.annFree);
    }
    if (store.ui.pendingImg) this.cross(this.toScr(store.ui.pendingImg), COL.pending, 9);
  }

  private dot(p: Vec2, col: string, r: number) { const g = this.ctx; g.beginPath(); g.arc(p[0], p[1], r, 0, 7); g.fillStyle = col; g.fill(); g.lineWidth = 1.5; g.strokeStyle = '#fff'; g.stroke(); }
  private ring(p: Vec2, col: string, r: number) { const g = this.ctx; g.beginPath(); g.arc(p[0], p[1], r, 0, 7); g.lineWidth = 3; g.strokeStyle = '#fff'; g.stroke(); g.lineWidth = 2; g.strokeStyle = col; g.stroke(); }
  private cross(p: Vec2, col: string, r: number) { const g = this.ctx; g.strokeStyle = col; g.lineWidth = 2; g.beginPath(); g.moveTo(p[0] - r, p[1]); g.lineTo(p[0] + r, p[1]); g.moveTo(p[0], p[1] - r); g.lineTo(p[0], p[1] + r); g.stroke(); }
  private label(p: Vec2, s: string, col: string, faint = false) {
    if (!s) return; const g = this.ctx; g.font = `${faint ? '' : '600 '}12px system-ui`;
    g.lineWidth = 3; g.strokeStyle = 'rgba(255,255,255,.85)'; g.strokeText(s, p[0] + 9, p[1] - 7); g.fillStyle = col; g.fillText(s, p[0] + 9, p[1] - 7);
  }
}
