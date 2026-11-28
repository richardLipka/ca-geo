// Register of the buildings in the growth viewer (growth3d.html, dev mode): the history of the selected building
// (since when it stands, its changes of height, periods destroyed, end) with the evidence behind each date, and
// manual values for any of them where there are no better data. Manual entries are saved to manual/buildings.json
// (read by growth_model.py, they win over every automatic rule), previewed in the model at once.
// Also the facade textures (facade.html) drawn on the walls in the viewer.
import * as THREE from 'three';
import { faceMesh, type BFac } from './facades3d';
import { bodyTris, roofMesh } from './blocks3d';
import { getLang } from './i18n';

interface Ovr { from?: number; to?: number | null; h0?: number; changes?: { year: number; h: number }[]; gaps?: [number, number][]; name?: string; note?: string; src?: string; xy?: [number, number]; edited?: string }
interface Reg { lo: (number | null)[]; hi: (number | null)[]; names: Record<string, string>; manual: Record<string, Ovr>; auto: Record<string, any>; orphans: string[] }
type Fac = Awaited<ReturnType<typeof initFacades>>;
interface Ctx {
  M: any; IDS: string[]; ZS: number[]; bd: Float32Array; btex: THREE.DataTexture; TW: number; TEXELS: number; data: string;
  getYear(): number; setYear(y: number): void; select(b: number): void; facades: Fac;
}
const cs = () => getLang() === 'cs';
const L = (c: string, e: string) => (cs() ? c : e);
const fmt = (v: number | null | undefined) => v == null || v >= 9999 || v <= 0 ? '' : String(Math.round(v * 10) / 10);
const esc = (s: string) => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
const BASIS_CS: [RegExp, string][] = [[/^history/, 'písemné prameny'], [/^manual \(register\)/, 'ručně v registru'], [/^manual/, 'ručně doplněno'], [/^RÚIAN date/, 'RÚIAN – datum dokončení'],
  [/RÚIAN/, 'RÚIAN + mapy'], [/^map 1840/, 'stabilní katastr 1840'], [/^plans? /, 'plány města'], [/^model 1618/, 'model 1618 + datované bourání'], [/permanence/, 'plány města (permanence)']];

export async function initRegister(c: Ctx) {
  const { M, IDS } = c;
  const css = document.createElement('style');
  css.textContent = `#rpanel { position: fixed; right: 10px; top: 52px; width: 330px; max-height: calc(100% - 140px); overflow: auto; background: rgba(251,251,250,.96); border: 1px solid #d3d8d6; border-radius: 6px; padding: 8px 10px; z-index: 3; font-size: 12.5px }
  #rpanel h3 { margin: 0 0 4px; font-size: 14px } #rpanel h4 { margin: 10px 0 3px; font-size: 11.5px; text-transform: uppercase; letter-spacing: .04em; color: #8c3b2e }
  #rpanel .g { display: grid; grid-template-columns: 92px 1fr 1fr 18px; gap: 3px 5px; align-items: center }
  #rpanel input[type=number], #rpanel input[type=text] { width: 100%; box-sizing: border-box; padding: 2px 4px; border: 1px solid #c9cfcc; border-radius: 3px; font: inherit }
  #rpanel input.man { background: #fbe3dc; border-color: #d0402a } #rpanel .x { cursor: pointer; color: #d0402a; text-align: center; visibility: hidden } #rpanel .x.on { visibility: visible }
  #rpanel .tl { display: flex; height: 16px; margin: 6px 0 2px; border-radius: 3px; overflow: hidden; background: #e7e9e8; position: relative }
  #rpanel .tl i { position: absolute; top: 0; bottom: 0 } #rpanel .ev { margin: 2px 0; padding-left: 4px } #rpanel .ev b { display: inline-block; min-width: 44px }
  #rpanel .btns { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px } #rpanel button, #rpanel a.b { padding: 3px 9px; border: 1px solid #c9cfcc; background: #fff; border-radius: 4px; cursor: pointer; font: inherit; color: inherit; text-decoration: none }
  #rpanel button.save { background: #2d6a3e; color: #fff; border-color: #2d6a3e } #rpanel .muted { color: #67706f } #rpanel .close { float: right; cursor: pointer; border: 0; background: none; font-size: 16px; padding: 0 }`;
  document.head.appendChild(css);
  const panel = document.createElement('div'); panel.id = 'rpanel'; panel.hidden = true; document.body.appendChild(panel);
  const getJSON = async <T,>(u: string): Promise<T | null> => { try { const r = await fetch(u, { cache: 'no-store' }); return r.ok ? await r.json() as T : null; } catch { return null; } };
  const reg = (await getJSON<Reg>(c.data + 'register.json')) ?? { lo: [], hi: [], names: {}, manual: {}, auto: {}, orphans: [] };
  let file = (await getJSON<{ note?: string; buildings: Record<string, Ovr> }>('/manual/buildings.json')) ?? { buildings: {} };
  // automatic values of every building (before the manual entries of the last build)
  const autoOf = (b: number) => {
    const a = reg.auto[String(b)], g = M.gaps[b] as number[];
    if (a) return { from: a.from, to: a.to ?? 9999, h0: a.h0 ?? a.h1, h1: a.h1, tR: a.tR ?? 9999, ch2: undefined as [number, number] | undefined, gaps: (a.gaps ?? []) as [number, number][], basis: a.basis, lo: a.lo, hi: a.hi };
    return { from: M.from[b], to: M.to[b], h0: M.h0[b], h1: M.h1[b], tR: M.tR[b], ch2: M.ch2?.[String(b)], gaps: [[g[0], g[1]], [g[2], g[3]]].filter(q => q[1] > 0) as [number, number][], basis: M.basis[M.basisIdx[b]], lo: reg.lo[b], hi: reg.hi[b] };
  };
  // effective state = automatic + manual entry → model arrays and the shader texture (preview without a rebuild)
  const apply = (b: number) => {
    const a = autoOf(b), o = complete(file.buildings[IDS[b]] ?? {});
    let from = o.from ?? a.from, to = o.to === undefined ? a.to : (o.to ?? 9999), h0 = o.h0 ?? a.h0, h1 = a.h1, tR = a.tR, ch2 = a.ch2, gaps = o.gaps ?? a.gaps;
    if (o.changes) { const ch = [...o.changes].sort((x, y) => x.year - y.year); tR = ch[0]?.year ?? 9999; h1 = ch[0]?.h ?? h0; ch2 = ch[1] ? [ch[1].year, ch[1].h] : undefined; }
    else if (o.h0 != null && a.tR >= 9999) h1 = h0;
    if (to <= from) to = from + 0.1;
    M.from[b] = from; M.to[b] = to; M.h0[b] = h0; M.h1[b] = h1; M.tR[b] = tR;
    const g = [...gaps, [0, 0], [0, 0]].slice(0, 2) as [number, number][]; M.gaps[b] = [g[0][0], g[0][1], g[1][0], g[1][1]];
    M.ch2 = M.ch2 ?? {}; if (ch2) M.ch2[String(b)] = ch2; else delete M.ch2[String(b)];
    const off = (Math.floor(b / c.TW) * c.TW * c.TEXELS + (b % c.TW) * c.TEXELS) * 4;
    c.bd.set([from, to, tR, M.cls[b]], off); c.bd.set([h0, h1, c.ZS[b], ch2?.[0] ?? 0], off + 4); c.bd.set(M.gaps[b], off + 8); c.bd[off + 15] = ch2?.[1] ?? 0;
    c.btex.needsUpdate = true; c.facades.update(c.getYear());
  };
  let sel = -1, cur: Ovr = {};
  // only complete rows count: a change needs year and height, a destruction start < end
  const complete = (o: Ovr): Ovr => ({ ...o, ...(o.changes ? { changes: o.changes.filter(q => q.year != null && q.h != null) } : {}), ...(o.gaps ? { gaps: o.gaps.filter(q => q[0] != null && q[1] != null && q[1] > q[0]) } : {}) });
  const centroid = (b: number): [number, number] => { const r = M.rings[b]; let x = 0, y = 0; for (let i = 0; i < r.length; i += 2) { x += r[i]; y += r[i + 1]; } const n = r.length / 2; return [x / n / 10 + M.origin[0], y / n / 10 + M.origin[1]]; };
  const basisName = (b: string) => cs() ? (BASIS_CS.find(([re]) => re.test(b))?.[1] ?? b) : b;
  function render() {
    if (sel < 0) { panel.hidden = true; return; }
    panel.hidden = false; const b = sel, a = autoOf(b), o = cur, id = IDS[b] || '#' + b;
    const name = o.name ?? reg.names[String(b)] ?? '';
    const ch = o.changes ?? [...(a.tR < 9999 ? [{ year: a.tR, h: a.h1 }] : []), ...(a.ch2 ? [{ year: a.ch2[0], h: a.ch2[1] }] : [])];
    const gaps = o.gaps ?? a.gaps, okCh = complete({ changes: ch }).changes!, okG = complete({ gaps }).gaps!;
    const row = (key: string, label: string, v1: string, v2: string | null, man: boolean, ph1 = '', ph2 = '') =>
      `<span>${label}</span><input type="number" step="0.1" data-k="${key}" data-i="0" value="${v1}" placeholder="${ph1}" class="${man ? 'man' : ''}">` +
      (v2 === null ? '<span></span>' : `<input type="number" step="0.1" data-k="${key}" data-i="1" value="${v2}" placeholder="${ph2}" class="${man ? 'man' : ''}">`) + `<span class="x ${man ? 'on' : ''}" data-x="${key}" title="${L('vrátit automatickou hodnotu', 'back to the automatic value')}">×</span>`;
    // timeline 1295–2020: standing (period colour), gaps (white), changes (ticks)
    const X = (y: number) => `${Math.max(0, Math.min(100, (y - 1295) / (2020 - 1295) * 100))}%`;
    const from = M.from[b], to = Math.min(M.to[b], 2020);
    let tl = `<i style="left:${X(from)};right:calc(100% - ${X(to)});background:#b9905a"></i>`;
    if (a.lo != null && a.hi != null && a.hi > a.lo) tl += `<i style="left:${X(a.lo)};right:calc(100% - ${X(a.hi)});background:repeating-linear-gradient(45deg,#d9b86a 0 3px,transparent 3px 6px)"></i>`;
    for (const [s, e] of okG) tl += `<i style="left:${X(s)};right:calc(100% - ${X(e)});background:#fff"></i>`;
    for (const q of okCh) tl += `<i style="left:${X(q.year)};width:2px;background:#8c3b2e"></i>`;
    const yr = c.getYear(); tl += `<i style="left:${X(yr)};width:1px;background:#000"></i>`;
    const ev: string[] = [];
    ev.push(`<div class="ev"><b>${fmt(from)}</b>${L('stojí od', 'stands from')}${a.lo != null && a.hi != null && a.hi - a.lo > 0.5 && o.from == null ? ` <span class="muted">(${L('mezi', 'between')} ${fmt(a.lo)}–${fmt(a.hi)})</span>` : ''}</div>`);
    for (const q of okCh) ev.push(`<div class="ev"><b>${fmt(q.year)}</b>${L('změna výšky na', 'height changed to')} ${fmt(q.h)} m</div>`);
    for (const [s, e] of okG) ev.push(`<div class="ev"><b>${fmt(s)}</b>${L('zničen / chybí do', 'destroyed / missing until')} ${fmt(e)}</div>`);
    ev.push(`<div class="ev"><b>${M.to[b] < 9999 ? fmt(M.to[b]) : '—'}</b>${M.to[b] < 9999 ? L('zbořen / zanikl', 'demolished') : L('stojí dodnes', 'still standing')}</div>`);
    panel.innerHTML = `<button class="close" title="×">×</button><h3>${esc(name || id)}</h3>
      <div class="muted">${esc(id)} · ${M.classes[M.cls[b]]} · ${L('datace', 'dated by')}: ${esc(basisName(M.basis[M.basisIdx[b]] ?? ''))}${file.buildings[IDS[b]] ? ' · <b style="color:#d0402a">' + L('ručně upraveno', 'set by hand') + '</b>' : ''}</div>
      <div class="tl">${tl}</div><div class="muted" style="display:flex;justify-content:space-between"><span>1295</span><span>2020</span></div>
      <h4>${L('Historie', 'History')}</h4>${ev.join('')}
      <div class="muted">${L('automaticky', 'automatic')}: ${esc(basisName(a.basis ?? ''))}</div>
      <h4>${L('Ruční hodnoty', 'Manual values')}</h4>
      <div class="g">
        ${row('from', L('stojí od', 'stands from'), fmt(o.from ?? from), null, o.from != null)}
        ${row('to', L('zbořen', 'demolished'), o.to === undefined ? fmt(M.to[b]) : fmt(o.to ?? 9999), null, o.to !== undefined, L('stojí', 'standing'))}
        ${row('h0', L('výška na počátku', 'first height'), fmt(o.h0 ?? M.h0[b]), null, o.h0 != null)}
        ${row('ch0', L('1. změna: rok / m', '1st change: year / m'), fmt(ch[0]?.year), fmt(ch[0]?.h), !!o.changes, L('rok', 'year'), 'm')}
        ${row('ch1', L('2. změna: rok / m', '2nd change: year / m'), fmt(ch[1]?.year), fmt(ch[1]?.h), !!o.changes, L('rok', 'year'), 'm')}
        ${row('g0', L('zničen: od / do', 'destroyed: from / to'), fmt(gaps[0]?.[0]), fmt(gaps[0]?.[1]), !!o.gaps)}
        ${row('g1', L('2. zničení', '2nd destruction'), fmt(gaps[1]?.[0]), fmt(gaps[1]?.[1]), !!o.gaps)}
      </div>
      <div class="g" style="grid-template-columns:92px 1fr 18px;margin-top:4px">
        <span>${L('název', 'name')}</span><input type="text" data-t="name" value="${esc(o.name ?? '')}" placeholder="${esc(reg.names[String(b)] ?? '')}"><span></span>
        <span>${L('pramen', 'source')}</span><input type="text" data-t="src" value="${esc(o.src ?? '')}" placeholder="${L('kniha, archiv, foto…', 'book, archive, photo…')}"><span></span>
        <span>${L('poznámka', 'note')}</span><input type="text" data-t="note" value="${esc(o.note ?? '')}"><span></span>
      </div>
      <div class="btns"><button class="save">${L('Uložit do registru', 'Save to the register')}</button><button data-a="revert">${L('Zrušit ruční úpravy', 'Remove manual values')}</button>
        <button data-a="go">${L('Na rok vzniku', 'Go to its start')}</button><a class="b" href="facade.html?id=${encodeURIComponent(IDS[b])}&year=${Math.round(yr)}" target="_blank">${L('Fasády z fotek / kreseb →', 'Facades from photos / drawings →')}</a></div>
      <div class="muted" id="rmsg" style="margin-top:6px">${L('Změny se hned ukážou v modelu; uložením se zapíší do manual/buildings.json a model je převezme při dalším generování.', 'Changes show in the model at once; saving writes manual/buildings.json, the model takes them at the next generation.')}
        ${Object.keys(file.buildings).length} ${L('ručně upravených budov', 'buildings set by hand')} · <a href="${c.data}register.csv" target="_blank">register.csv</a>${reg.orphans.length ? ` · ${reg.orphans.length} ${L('záznamů bez budovy', 'entries without a building')}` : ''}</div>`;
    panel.querySelector<HTMLButtonElement>('.close')!.onclick = () => { sel = -1; c.select(-1); render(); };
    panel.querySelectorAll<HTMLInputElement>('input[data-k]').forEach(inp => inp.onchange = () => edit(inp.dataset.k!));
    panel.querySelectorAll<HTMLInputElement>('input[data-t]').forEach(inp => inp.oninput = () => { const k = inp.dataset.t as 'name' | 'src' | 'note'; if (inp.value) cur[k] = inp.value; else delete cur[k]; });
    panel.querySelectorAll<HTMLElement>('[data-x]').forEach(x => x.onclick = () => { const k = x.dataset.x!; const key = k === 'from' || k === 'to' || k === 'h0' ? k : k.startsWith('ch') ? 'changes' : 'gaps'; delete (cur as any)[key]; preview(); });
    panel.querySelector<HTMLButtonElement>('.save')!.onclick = () => void save();
    panel.querySelector<HTMLButtonElement>('[data-a=revert]')!.onclick = () => { cur = {}; preview(); };
    panel.querySelector<HTMLButtonElement>('[data-a=go]')!.onclick = () => c.setYear(M.from[b] + 0.5);
  }
  const val = (k: string, i: number) => { const e = panel.querySelector<HTMLInputElement>(`input[data-k="${k}"][data-i="${i}"]`); return e && e.value !== '' ? +e.value : null; };
  function edit(k: string) {
    if (k === 'from') { const v = val('from', 0); if (v == null) delete cur.from; else cur.from = v; }
    if (k === 'to') { const v = val('to', 0); cur.to = v == null || v >= 9999 ? null : v; }
    if (k === 'h0') { const v = val('h0', 0); if (v == null) delete cur.h0; else cur.h0 = v; }
    if (k.startsWith('ch')) cur.changes = [0, 1].map(i => ({ year: val('ch' + i, 0), h: val('ch' + i, 1) })) as { year: number; h: number }[];   // rows may be incomplete while typing
    if (k.startsWith('g')) cur.gaps = [0, 1].map(i => [val('g' + i, 0), val('g' + i, 1)]) as [number, number][];
    preview();
  }
  function preview() { const id = IDS[sel]; const keep = file.buildings[id]; file.buildings[id] = cur; apply(sel); if (keep) file.buildings[id] = keep; else delete file.buildings[id]; render2(); }
  // render with the edited (unsaved) entry
  function render2() { const id = IDS[sel], keep = file.buildings[id]; file.buildings[id] = cur; render(); if (keep) file.buildings[id] = keep; else delete file.buildings[id]; }
  async function save() {
    const id = IDS[sel]; if (!id) return;
    const fresh = (await getJSON<typeof file>('/manual/buildings.json')) ?? { buildings: {} };
    const data = Object.fromEntries(Object.entries(complete(cur)).filter(([k]) => !['xy', 'edited'].includes(k)));
    if (Object.keys(data).length) fresh.buildings[id] = { ...data, xy: centroid(sel).map(v => Math.round(v * 10) / 10) as [number, number], edited: new Date().toISOString().slice(0, 10) };
    else delete fresh.buildings[id];
    fresh.note = 'manual history of the buildings (growth3d.html register): from, to (null = stands), h0, changes [{year, h}], gaps [[from, to]], name, src, note; read by growth_model.py';
    const r = await fetch('/api/manual/buildings.json', { method: 'POST', body: JSON.stringify(fresh, null, 1) }).catch(() => null);
    file = fresh; apply(sel); render();
    const m = panel.querySelector('#rmsg'); if (m) m.textContent = r?.ok ? L('Uloženo do registru (manual/buildings.json).', 'Saved to the register (manual/buildings.json).') : L('Uložení selhalo.', 'Saving failed.');
  }
  // the manual entries saved after the last build are applied at once
  IDS.forEach((id, b) => { if (file.buildings[id] || reg.manual[String(b)]) apply(b); });
  return {
    select(b: number) { sel = b; cur = b >= 0 ? JSON.parse(JSON.stringify(file.buildings[IDS[b]] ?? {})) : {}; render(); },
  };
}

/** Facade textures on the walls: one mesh per textured face, shown while its building stands and its layer is valid. */
export async function initFacades(o: { scene: THREE.Scene; M: any; ZS: number[]; IDS: string[]; visibleAt: (b: number, y: number) => boolean; dev: boolean; data: string; meshOf: Map<number, { v: Float32Array; t: Uint16Array }> }) {
  const group = new THREE.Group(); o.scene.add(group);
  const items: { b: number; valid: [number, number]; mesh: THREE.Mesh }[] = [];
  const loader = new THREE.TextureLoader();
  const load = async () => {
    group.clear(); items.length = 0;
    const url = o.dev ? '/manual/facades.json' : (o.M.facades ? o.data + o.M.facades : '');
    const texBase = o.dev ? '/data/historic/growth/facades/tex/' : o.data + 'facades/';
    if (!url) return;
    let f: { blocks?: Record<string, BFac>; buildings?: Record<string, BFac> } | null = null;
    try { const r = await fetch(url, { cache: 'no-store' }); f = r.ok ? await r.json() : null; } catch { f = null; }
    if (!f) return;
    const idx = new Map(o.IDS.map((id, b) => [id, b]));
    const blocks: Record<string, BFac> = { ...(f.blocks ?? {}) };
    for (const [k, v] of Object.entries(f.buildings ?? {})) if (!blocks[k]) blocks[k] = { members: [k], ...v };   // first format: one building
    let li0 = 0;
    for (const [key, bf] of Object.entries(blocks)) {
      bf.layers.forEach(lay => {
        const lift = 0.02 * (li0++ % 4);
        for (const fc of lay.faces) {   // walls
          const b = idx.get(fc.b ?? key); if (b === undefined || !fc.tex) continue;
          const tex = loader.load(texBase + fc.tex); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
          const m = faceMesh(fc, o.ZS[b], tex, lift); m.visible = false; group.add(m); items.push({ b, valid: lay.valid, mesh: m });
        }
        if (lay.roof?.tex) {   // roofs of the block: one plan-view texture over the roofs of all its houses, at the image's heights
          const tex = loader.load(texBase + lay.roof.tex); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
          const y = lay.year ?? lay.valid[0];
          for (const id of bf.members ?? [key]) {
            const b = idx.get(id); if (b === undefined) continue;
            const m = roofMesh(bodyTris(o.M, b, y, o.meshOf.get(b), true), lay.roof.box, o.ZS[b] + lift, tex); m.visible = false; group.add(m); items.push({ b, valid: lay.valid, mesh: m });
          }
        }
      });
    }
  };
  await load();
  let last = 1295;
  const update = (y: number) => { last = y; for (const it of items) it.mesh.visible = o.visibleAt(it.b, y) && y >= it.valid[0] && y < it.valid[1]; };
  return { update, reload: async () => { await load(); update(last); }, get count() { return items.length; } };
}
