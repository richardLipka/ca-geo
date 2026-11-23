// Side panels: source list (left) and the tabbed inspector (right). Rendered from state as
// HTML strings; a panel is not re-rendered while one of its form fields has focus.

import { download, entitiesGeoJson, evidenceCsv, gdalScript, qgisPoints } from './exporters';
import { getImage, imageFailed } from './images';
import { t } from './i18n';
import { ANNOTATION_KINDS, ENTITY_TYPES, activeIn, entityAnchor, normaliseProject, type AnnotationKind, type EntityType, type Source, type SourceKind } from './model';
import { store } from './store';
import type { Method, Vec2 } from './transform';

const esc = (s: unknown) => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const fmt = (v: number, d = 1) => (Number.isFinite(v) ? v.toFixed(d) : '—');
const METHODS: Method[] = ['helmert', 'affine', 'projective', 'poly2', 'tps'];
const KINDS: SourceKind[] = ['map', 'birdseye', 'panorama'];

export interface PanelHooks { centreImage: (p: Vec2) => void; centreMap: (p: Vec2) => void }

function guarded(el: HTMLElement, render: () => void) {
  let pending = false;
  el.addEventListener('focusout', () => { if (pending) { pending = false; setTimeout(render, 0); } });
  return () => {
    const a = document.activeElement;
    if (a && el.contains(a) && /^(INPUT|SELECT|TEXTAREA)$/.test(a.tagName)) { pending = true; return; }
    render();
  };
}

export function mountSources(el: HTMLElement) {
  const render = () => {
    const ui = store.ui;
    el.innerHTML = `<h2>${t('sources.title')}</h2><ul class="srclist">${store.project.sources.map(s => {
      const n = store.controls(s).length, miss = imageFailed(s.file);
      getImage(s.file);
      return `<li><button type="button" class="src${s.id === ui.sourceId ? ' on' : ''}" data-id="${esc(s.id)}">
        <span class="k k-${s.kind}">${t('kind.' + s.kind)}</span>
        <b>${esc(s.title)}</b>
        <small>${esc(s.made ?? '')}${n ? ' · ' + t('sources.ctrl', { n }) : ''}</small>
        ${miss ? `<small class="warn">${t('sources.missing')}</small>` : ''}</button></li>`;
    }).join('')}</ul>
    <label class="drop" for="addfile">${t('sources.add')}<input type="file" id="addfile" accept="image/*" hidden></label>
    <p class="muted small">${t('sources.dropHint')}</p>`;
    el.querySelectorAll<HTMLButtonElement>('button.src').forEach(b => b.onclick = () => store.setUi({ sourceId: b.dataset.id!, pendingImg: null, pendingMap: null, selAnnotation: null }));
    (el.querySelector('#addfile') as HTMLInputElement).onchange = e => { const f = (e.target as HTMLInputElement).files?.[0]; if (f) addLocalFile(f); };
  };
  store.on(guarded(el, render)); render();
  el.addEventListener('dragover', e => e.preventDefault());
  el.addEventListener('drop', e => { e.preventDefault(); const f = e.dataTransfer?.files?.[0]; if (f && f.type.startsWith('image/')) addLocalFile(f); });
}

/** Ad-hoc local image (object URL, not persisted across reloads unless placed in data/historic/sources). */
function addLocalFile(f: File) {
  const id = 'local-' + f.name.replace(/\W+/g, '-').toLowerCase();
  const src: Source = { id, title: f.name, kind: 'birdseye', file: URL.createObjectURL(f), method: 'projective', useLinks: true, overlay: true, opacity: 0.7, licence: '?' };
  store.change(p => { p.sources.push(src); });
  store.setUi({ sourceId: id });
}

export function mountInspector(el: HTMLElement, hooks: PanelHooks) {
  const render = () => {
    const ui = store.ui;
    const tabs = (['points', 'identity', 'entities', 'export'] as const).map(k => `<button type="button" role="tab" class="tab${ui.tab === k ? ' on' : ''}" data-tab="${k}" aria-selected="${ui.tab === k}">${t('tab.' + k)}</button>`).join('');
    const body = ui.tab === 'points' ? pointsTab() : ui.tab === 'identity' ? identityTab() : ui.tab === 'entities' ? entitiesTab() : exportTab();
    el.innerHTML = `<div class="tabs" role="tablist">${tabs}</div><div class="tabbody">${body}</div>`;
    el.querySelectorAll<HTMLButtonElement>('button.tab').forEach(b => b.onclick = () => store.setUi({ tab: b.dataset.tab as typeof ui.tab }));
    wire(el, hooks);
  };
  store.on(guarded(el, render)); render();
}

function sourceHeader(s: Source) {
  return `<div class="srchead"><b>${esc(s.title)}</b><small>${t('src.made')}: ${esc(s.made ?? '—')} · ${t('src.licence')}: ${esc(s.licence ?? '—')}${s.page ? ` · <a href="${esc(s.page)}" target="_blank" rel="noopener">${t('src.page')}</a>` : ''}</small></div>`;
}

function pointsTab(): string {
  const s = store.source; if (!s) return `<p class="muted">${t('img.noSource')}</p>`;
  const r = store.fitOf(s), ctrl = store.controls(s), gcps = store.project.gcps[s.id] ?? [];
  const methodSel = s.kind === 'panorama' ? '' : `<label>${t('pts.method')}<select data-act="method">${METHODS.map(m => `<option value="${m}"${m === s.method ? ' selected' : ''}>${t('method.' + m)}</option>`).join('')}</select></label>`;
  let summary = '';
  if (r.pano) summary = `<p class="stat">${t('pts.panoRmse', { v: fmt(r.pano.rmsePx) })}<br>${t('pts.panoView', { x: fmt(r.pano.X0, 0), y: fmt(r.pano.Y0, 0) })}</p>`;
  else if (r.fit) summary = `<p class="stat">${t('pts.rmse', { v: fmt(r.fit.rmse, 2) })} · <b>${t('pts.loo', { v: fmt(r.fit.looRmse, 1) })}</b></p>`;
  else if (r.error?.startsWith('min:')) summary = `<p class="muted">${t('pts.need', { n: r.error.slice(4) })}</p>`;
  else if (r.error) summary = `<p class="warn">${esc(r.error)}</p>`;
  const idx = new Map(ctrl.map((c, i) => [c.id, i]));
  const rows = [
    ...gcps.map((g, i) => ({ id: g.id, name: `G${i + 1}`, on: g.enabled, link: false, i: idx.get(g.id) })),
    ...ctrl.filter(c => c.origin === 'link').map(c => ({ id: c.id, name: c.label, on: true, link: true, i: idx.get(c.id) })),
  ];
  const resid = (i: number | undefined, which: 'residuals' | 'loo') => (i === undefined ? '—' : r.fit ? fmt(r.fit[which][i]) : r.pano && which === 'residuals' ? fmt(r.pano.residualsPx[i]) + ' px' : '—');
  const table = rows.length ? `<table class="pts"><thead><tr><th>${t('pts.th.id')}</th><th>${t('pts.th.res')}</th><th>${t('pts.th.loo')}</th><th>${t('pts.th.on')}</th><th></th></tr></thead><tbody>${rows.map(rw => {
    const loo = rw.i !== undefined && r.fit ? r.fit.loo[rw.i] : NaN, bad = Number.isFinite(loo) && r.fit && loo > 3 * (r.fit.looRmse || 1);
    return `<tr class="${rw.id === store.ui.selGcp ? 'sel' : ''}${bad ? ' bad' : ''}"><td><button type="button" class="lnk" data-act="${rw.link ? 'selann' : 'selgcp'}" data-id="${rw.id}">${esc(rw.name)}</button>${rw.link ? ` <small class="muted">${t('pts.link')}</small>` : ''}</td>
      <td class="num">${resid(rw.i, 'residuals')}</td><td class="num">${resid(rw.i, 'loo')}</td>
      <td>${rw.link ? '' : `<input type="checkbox" data-act="gcpon" data-id="${rw.id}"${rw.on ? ' checked' : ''} aria-label="${t('pts.th.on')}">`}</td>
      <td>${rw.link ? '' : `<button type="button" class="x" data-act="gcpdel" data-id="${rw.id}" aria-label="${t('pts.delete')}">×</button>`}</td></tr>`;
  }).join('')}</tbody></table>` : `<p class="muted">${t('pts.none')}</p>`;
  return `${sourceHeader(s)}
    <label>${t('pts.kind')}<select data-act="kind">${KINDS.map(k => `<option value="${k}"${k === s.kind ? ' selected' : ''}>${t('kind.' + k)}</option>`).join('')}</select></label>
    ${methodSel}
    ${s.kind === 'map' ? `<label class="chk"><input type="checkbox" data-act="uselinks"${s.useLinks ? ' checked' : ''}> ${t('pts.useLinks')}</label>` : ''}
    ${s.kind !== 'panorama' ? `<label class="chk"><input type="checkbox" data-act="overlay"${s.overlay ? ' checked' : ''}> ${t('pts.overlay')}</label>
    <label>${t('pts.opacity')}<input type="range" min="0" max="1" step="0.05" value="${s.opacity}" data-act="opacity"></label>` : ''}
    ${summary}${table}`;
}

function identityTab(): string {
  const s = store.source; if (!s) return `<p class="muted">${t('img.noSource')}</p>`;
  const anns = store.annotationsOf(s.id);
  if (!anns.length) return `${sourceHeader(s)}<p class="muted">${t('ann.none')}</p>`;
  const ents = [...store.project.entities].sort((a, b) => a.name.localeCompare(b.name));
  return `${sourceHeader(s)}<h3>${t('ann.title')}</h3><div class="anns">${anns.map(a => {
    const sel = a.id === store.ui.selAnnotation;
    if (!sel) { const e = store.entity(a.entityId); return `<button type="button" class="annrow" data-act="selann" data-id="${a.id}"><span>${esc(a.label || (a.shape ? '▱' : '·'))}</span> ${esc(e?.name ?? (a.kind ? t('kind.ann.' + a.kind) : t('ann.unlinked')))} <small>${t('conf.' + a.confidence)}</small></button>`; }
    return `<div class="anned" data-id="${a.id}">
      <label>${t('ann.label')}<input type="text" id="ann-label" data-act="annlabel" value="${esc(a.label ?? '')}"></label>
      <label>${t('ann.kind')}<select id="ann-kind" data-act="annkind"><option value="">—</option>${ANNOTATION_KINDS.map(k => `<option value="${k}"${k === a.kind ? ' selected' : ''}>${t('kind.ann.' + k)}</option>`).join('')}</select></label>
      <label>${t('ann.entity')}<select id="ann-entity" data-act="annentity"><option value="">${t('ann.noEntity')}</option>${ents.map(e => `<option value="${e.id}"${e.id === a.entityId ? ' selected' : ''}>${esc(e.name)} (${t('type.' + e.type)})</option>`).join('')}</select></label>
      <label>${t('ann.confidence')}<select id="ann-conf" data-act="annconf">${[1, 2, 3].map(c => `<option value="${c}"${c === a.confidence ? ' selected' : ''}>${t('conf.' + c)}</option>`).join('')}</select></label>
      <label class="chk"><input type="checkbox" data-act="annctrl"${a.useAsControl ? ' checked' : ''}> ${t('ann.control')}</label>
      <label>${t('ann.note')}<textarea id="ann-note" data-act="annnote" rows="2">${esc(a.note ?? '')}</textarea></label>
      <button type="button" class="danger" data-act="anndel" data-id="${a.id}">${t('ann.delete')}</button></div>`;
  }).join('')}</div>`;
}

function entitiesTab(): string {
  const ui = store.ui, e = store.entity(ui.selEntity);
  const list = [...store.project.entities].filter(x => activeIn(x, ui.year)).sort((a, b) => a.name.localeCompare(b.name));
  const listHtml = list.length ? `<div class="entlist">${list.map(x => `<button type="button" class="entrow${x.id === ui.selEntity ? ' on' : ''}" data-act="selent" data-id="${x.id}"><i class="sw t-${x.type}"></i>${esc(x.name)} <small>${t('type.' + x.type)}${x.validFrom !== undefined || x.validTo !== undefined ? ` · ${x.validFrom ?? '…'}–${x.validTo ?? '…'}` : ''}</small></button>`).join('')}</div>` : `<p class="muted">${t('ent.none')}</p>`;
  if (!e) return `<h3>${t('ent.title')}</h3>${listHtml}`;
  const ev = store.project.annotations.filter(a => a.entityId === e.id);
  const evHtml = ev.length ? `<ul class="ev">${ev.map(a => { const s = store.project.sources.find(x => x.id === a.sourceId); return `<li><button type="button" class="lnk" data-act="goann" data-id="${a.id}">${esc(s?.title ?? a.sourceId)}</button>${a.label ? ` · ${esc(a.label)}` : ''} · ${t('conf.' + a.confidence)}</li>`; }).join('')}</ul>` : `<p class="muted">${t('ent.noEvidence')}</p>`;
  return `<div class="ented">
    <label>${t('ent.name')}<input type="text" id="ent-name" data-act="entname" value="${esc(e.name)}"></label>
    <label>${t('ent.type')}<select id="ent-type" data-act="enttype">${ENTITY_TYPES.map(k => `<option value="${k}"${k === e.type ? ' selected' : ''}>${t('type.' + k)}</option>`).join('')}</select></label>
    <div class="row2"><label>${t('ent.from')}<input type="number" id="ent-from" data-act="entfrom" value="${e.validFrom ?? ''}"></label>
    <label>${t('ent.to')}<input type="number" id="ent-to" data-act="entto" value="${e.validTo ?? ''}"></label></div>
    <div class="row2"><label>${t('ent.cp')}<input type="text" id="ent-cp" data-act="entcp" value="${esc(e.cp ?? '')}"></label>
    <label>${t('ent.height')}<input type="number" id="ent-height" data-act="entheight" min="0" step="0.5" value="${e.height ?? ''}"></label></div>
    <label>${t('ent.notes')}<textarea id="ent-notes" data-act="entnotes" rows="3">${esc(e.notes ?? '')}</textarea></label>
    <div class="btns"><button type="button" data-act="entzoom">${t('ent.zoom')}</button>
      <button type="button" data-act="entredraw">${t('ent.redraw')}</button>
      <button type="button" class="danger" data-act="entdel">${t('ent.delete')}</button></div>
    <h3>${t('ent.evidence')}</h3>${evHtml}</div><h3>${t('ent.title')}</h3>${listHtml}`;
}

function exportTab(): string {
  const s = store.source;
  return `<div class="btncol">
    <button type="button" data-act="exp-project">${t('exp.project')}</button>
    <button type="button" data-act="exp-geo5514">${t('exp.geo5514')}</button>
    <button type="button" data-act="exp-geo4326">${t('exp.geo4326')}</button>
    <button type="button" data-act="exp-csv">${t('exp.csv')}</button>
    ${s && s.kind !== 'panorama' ? `<button type="button" data-act="exp-gdal">${t('exp.gdal')}</button><button type="button" data-act="exp-qgis">${t('exp.qgis')}</button>` : ''}
    <label class="drop" for="impfile">${t('exp.import')}<input type="file" id="impfile" accept="application/json,.json" hidden></label>
  </div><p class="muted small">${t('exp.note', { name: esc(store.project.name) })}</p>`;
}

function wire(el: HTMLElement, hooks: PanelHooks) {
  const s = store.source;
  const on = (act: string, ev: string, fn: (t: HTMLInputElement & HTMLSelectElement) => void) =>
    el.querySelectorAll<HTMLInputElement & HTMLSelectElement>(`[data-act="${act}"]`).forEach(x => x.addEventListener(ev, () => fn(x)));
  const selAnn = () => store.project.annotations.find(a => a.id === store.ui.selAnnotation);
  const selEnt = () => store.entity(store.ui.selEntity);
  if (s) {
    on('kind', 'change', x => store.change(() => { s.kind = x.value as SourceKind; if (s.kind === 'birdseye' && s.method === 'affine') s.method = 'projective'; }));
    on('method', 'change', x => store.change(() => { s.method = x.value as Method; }));
    on('uselinks', 'change', x => store.change(() => { s.useLinks = x.checked; }));
    on('overlay', 'change', x => store.change(() => { s.overlay = x.checked; }));
    on('opacity', 'input', x => { s.opacity = +x.value; store.emit(); });
    on('opacity', 'change', x => store.change(() => { s.opacity = +x.value; }));
    on('gcpon', 'change', x => store.change(p => { const g = p.gcps[s.id]?.find(q => q.id === x.dataset.id); if (g) g.enabled = x.checked; }));
    on('gcpdel', 'click', x => store.change(p => { p.gcps[s.id] = (p.gcps[s.id] ?? []).filter(q => q.id !== x.dataset.id); }));
    on('selgcp', 'click', x => { const g = store.project.gcps[s.id]?.find(q => q.id === x.dataset.id); store.setUi({ selGcp: x.dataset.id! }); if (g) { hooks.centreImage(g.img); hooks.centreMap(g.map); } });
  }
  on('selann', 'click', x => { const a = store.project.annotations.find(q => q.id === x.dataset.id); store.setUi({ selAnnotation: x.dataset.id!, selEntity: a?.entityId ?? null, tab: 'identity' }); if (a) hooks.centreImage(a.img); });
  on('annlabel', 'change', x => { const a = selAnn(); if (a) store.change(() => { a.label = x.value || undefined; }); });
  on('annentity', 'change', x => { const a = selAnn(); if (a) store.change(() => { a.entityId = x.value || null; }); store.setUi({ selEntity: x.value || null }); });
  on('annkind', 'change', x => { const a = selAnn(); if (a) store.change(() => { a.kind = (x.value || undefined) as AnnotationKind | undefined; }); });
  on('annconf', 'change', x => { const a = selAnn(); if (a) store.change(() => { a.confidence = +x.value as 1 | 2 | 3; }); });
  on('annctrl', 'change', x => { const a = selAnn(); if (a) store.change(() => { a.useAsControl = x.checked; }); });
  on('annnote', 'change', x => { const a = selAnn(); if (a) store.change(() => { a.note = x.value || undefined; }); });
  on('anndel', 'click', x => { store.change(p => { p.annotations = p.annotations.filter(a => a.id !== x.dataset.id); }); store.setUi({ selAnnotation: null }); });
  on('selent', 'click', x => { store.setUi({ selEntity: x.dataset.id! }); const e = store.entity(x.dataset.id!), m = e && entityAnchor(e); if (m) hooks.centreMap(m); });
  on('entname', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.name = x.value; }); });
  on('enttype', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.type = x.value as EntityType; }); });
  on('entfrom', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.validFrom = x.value === '' ? undefined : +x.value; }); });
  on('entto', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.validTo = x.value === '' ? undefined : +x.value; }); });
  on('entcp', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.cp = x.value || undefined; }); });
  on('entheight', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.height = x.value === '' ? undefined : +x.value; }); });
  on('entnotes', 'change', x => { const e = selEnt(); if (e) store.change(() => { e.notes = x.value || undefined; }); });
  on('entzoom', 'click', () => { const e = selEnt(), m = e && entityAnchor(e); if (m) hooks.centreMap(m); });
  on('entredraw', 'click', () => { const e = selEnt(); if (!e) return; const tool = e.geom?.type === 'LineString' ? 'draw-line' : e.geom?.type === 'Polygon' ? 'draw-polygon' : 'draw-point'; store.setUi({ tool, redraw: true, drawing: [] }); });
  on('entdel', 'click', () => { const id = store.ui.selEntity; store.change(p => { p.entities = p.entities.filter(e => e.id !== id); p.annotations.forEach(a => { if (a.entityId === id) a.entityId = null; }); }); store.setUi({ selEntity: null }); });
  on('goann', 'click', x => { const a = store.project.annotations.find(q => q.id === x.dataset.id); if (!a) return; store.setUi({ sourceId: a.sourceId, selAnnotation: a.id, tab: 'identity' }); setTimeout(() => hooks.centreImage(a.img), 50); });
  const name = store.project.name;
  on('exp-project', 'click', () => download(`${name}.json`, JSON.stringify(store.project, null, 1)));
  on('exp-geo5514', 'click', () => download(`${name}-entities-5514.geojson`, entitiesGeoJson(store.project, false), 'application/geo+json'));
  on('exp-geo4326', 'click', () => download(`${name}-entities-4326.geojson`, entitiesGeoJson(store.project, true), 'application/geo+json'));
  on('exp-csv', 'click', () => download(`${name}-evidence.csv`, evidenceCsv(store.project), 'text/csv'));
  if (s) {
    on('exp-gdal', 'click', () => download(`${s.id}-gdal.sh`, gdalScript(s), 'text/x-shellscript'));
    on('exp-qgis', 'click', () => download(`${s.id}.points`, qgisPoints(s), 'text/plain'));
  }
  const imp = el.querySelector('#impfile') as HTMLInputElement | null;
  if (imp) imp.onchange = async () => {
    const f = imp.files?.[0]; if (!f) return;
    try { store.replace(normaliseProject(JSON.parse(await f.text()))); } catch { el.querySelector('.tabbody')!.insertAdjacentHTML('beforeend', `<p class="warn">${t('exp.importFail')}</p>`); }
  };
}
