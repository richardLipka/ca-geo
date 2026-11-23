// Application state: the project (persisted), UI state (not persisted), undo history,
// derived fits per source, and persistence (dev-server file + localStorage fallback).

import { type Annotation, type Entity, type Project, type Source, emptyProject, entityAnchor, normaliseProject } from './model';
import { fit, fitPanorama, MIN_POINTS, type Fit, type PanoFit, type Vec2 } from './transform';

export type Tool = 'navigate' | 'gcp' | 'identify' | 'outline' | 'draw-point' | 'draw-line' | 'draw-polygon';

export interface Ui {
  sourceId: string | null;
  tool: Tool;
  selEntity: string | null;
  selAnnotation: string | null;
  selGcp: string | null;
  pendingImg: Vec2 | null; // first click of a GCP / identity pair on the image
  pendingMap: Vec2 | null; // first click on the map
  drawing: Vec2[]; // vertices of an entity being drawn
  outline: Vec2[]; // vertices of an image outline being drawn
  redraw: boolean; // drawing replaces the geometry of the selected entity
  year: number | null; // time filter for entities; null = all
  refLayer: string;
  refOpacity: number;
  showAmcr: boolean;
  showGrowth: boolean;
  tab: 'points' | 'identity' | 'entities' | 'export';
  saveState: 'saved' | 'saving' | 'local' | 'error';
}

/** Control pair used for fitting, with its origin for display. */
export interface Ctrl { id: string; img: Vec2; map: Vec2; origin: 'gcp' | 'link'; label: string }

type Listener = () => void;

class Store {
  project: Project = emptyProject('plzen');
  ui: Ui = {
    sourceId: null, tool: 'navigate', selEntity: null, selAnnotation: null, selGcp: null,
    pendingImg: null, pendingMap: null, drawing: [], outline: [], redraw: false, year: null, refLayer: 'city-GIS_HIS_Plzen_1781', refOpacity: 1,
    showAmcr: false, showGrowth: false, tab: 'points', saveState: 'saved',
  };
  private listeners = new Set<Listener>();
  private undoStack: string[] = [];
  private redoStack: string[] = [];
  private fitCache = new Map<string, { key: string; fit: Fit | null; pano: PanoFit | null; error: string | null }>();
  private saveTimer = 0;

  on(l: Listener) { this.listeners.add(l); return () => this.listeners.delete(l); }
  emit() { this.listeners.forEach(l => l()); }

  /** Mutate the project with undo support and autosave. */
  change(fn: (p: Project) => void) {
    this.undoStack.push(JSON.stringify(this.project));
    if (this.undoStack.length > 100) this.undoStack.shift();
    this.redoStack = [];
    fn(this.project);
    this.scheduleSave();
    this.emit();
  }
  setUi(patch: Partial<Ui>) { Object.assign(this.ui, patch); this.emit(); }
  undo() { const s = this.undoStack.pop(); if (!s) return; this.redoStack.push(JSON.stringify(this.project)); this.project = JSON.parse(s); this.scheduleSave(); this.emit(); }
  redo() { const s = this.redoStack.pop(); if (!s) return; this.undoStack.push(JSON.stringify(this.project)); this.project = JSON.parse(s); this.scheduleSave(); this.emit(); }

  get source(): Source | null { return this.project.sources.find(s => s.id === this.ui.sourceId) ?? null; }
  entity(id: string | null): Entity | null { return id ? this.project.entities.find(e => e.id === id) ?? null : null; }
  annotationsOf(sourceId: string): Annotation[] { return this.project.annotations.filter(a => a.sourceId === sourceId); }

  /** Control pairs for a source: enabled GCPs + identity links to entities with geometry. */
  controls(src: Source): Ctrl[] {
    const out: Ctrl[] = (this.project.gcps[src.id] ?? []).filter(g => g.enabled).map((g, i) => ({ id: g.id, img: g.img, map: g.map, origin: 'gcp' as const, label: `G${i + 1}` }));
    if (src.useLinks || src.kind !== 'map') {
      for (const a of this.annotationsOf(src.id)) {
        if (!a.useAsControl || !a.entityId) continue;
        const e = this.entity(a.entityId); const m = e && entityAnchor(e);
        if (m) out.push({ id: a.id, img: a.img, map: m, origin: 'link', label: e!.name || a.label || '?' });
      }
    }
    return out;
  }

  /** Fitted transform for a source (cached by the control set and method). */
  fitOf(src: Source): { fit: Fit | null; pano: PanoFit | null; error: string | null } {
    const ctrl = this.controls(src);
    const key = JSON.stringify([src.kind, src.method, ctrl.map(c => [c.img, c.map])]);
    const hit = this.fitCache.get(src.id);
    if (hit && hit.key === key) return hit;
    let res: { fit: Fit | null; pano: PanoFit | null; error: string | null } = { fit: null, pano: null, error: null };
    try {
      if (src.kind === 'panorama') {
        const w = imageSize.get(src.file)?.[0];
        if (w && ctrl.length >= 4) res.pano = fitPanorama(ctrl.map(c => ({ x: c.img[0], map: c.map })), w / 2);
        else res.error = 'min:4';
      } else if (ctrl.length >= MIN_POINTS[src.method]) res.fit = fit(src.method, ctrl.map(c => ({ img: c.img, map: c.map })));
      else res.error = 'min:' + MIN_POINTS[src.method];
    } catch (e) { res.error = (e as Error).message; }
    this.fitCache.set(src.id, { key, ...res });
    return res;
  }

  // ---------- persistence ----------
  private scheduleSave() {
    try { localStorage.setItem('historic-mapper:project', JSON.stringify(this.project)); } catch { /* storage unavailable */ }
    this.ui.saveState = 'saving';
    clearTimeout(this.saveTimer);
    this.saveTimer = window.setTimeout(() => this.saveToServer(), 800);
  }
  async saveToServer() {
    try {
      const r = await fetch(`/api/project/${encodeURIComponent(this.project.name)}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(this.project, null, 1) });
      this.ui.saveState = r.ok ? 'saved' : 'local';
    } catch { this.ui.saveState = 'local'; }
    this.emit();
  }
  async load(name: string, seed: () => Promise<Project>) {
    try {
      const r = await fetch(`/api/project/${encodeURIComponent(name)}`);
      if (r.ok) { this.project = normaliseProject(await r.json()); this.ui.saveState = 'saved'; return; }
    } catch { /* no dev server API */ }
    try {
      const s = localStorage.getItem('historic-mapper:project');
      if (s) { this.project = normaliseProject(JSON.parse(s)); this.ui.saveState = 'local'; return; }
    } catch { /* ignore */ }
    this.project = await seed();
    this.ui.saveState = 'local';
  }
  replace(p: Project) { this.undoStack.push(JSON.stringify(this.project)); this.project = p; this.scheduleSave(); this.emit(); }
}

/** Natural sizes of loaded source images (by file URL). */
export const imageSize = new Map<string, [number, number]>();

export const store = new Store();
