// Facades from photos and drawings: textures for the walls and roofs of a block of houses of the growth model.
// A block is one building or several neighbouring ones (a street front, a whole block of an isometric town view);
// its outer walls (party walls excluded) and its roofs are textured together from one source image (a layer).
// Each wall seen in the image gets a quad of four image points (the corners of a control rectangle on the wall), from
// which a homography rectifies the wall's texture. The quads come
//  - by hand: four clicks per wall, or four clicks for a whole front of several walls (shift-select the walls),
//  - from a camera fitted to clicked points of the block (corners at the ground and at the eaves, gable tops):
//    veduta camera + local correction (1–3 points), affine camera for isometric drawings (≥ 4 points at two heights)
//    or perspective DLT for photographs (≥ 6 points); all walls facing the camera at once,
//  - from the camera of a veduta (scripts/veduta_views.json) without any click.
// With a camera the roofs of the block become one plan-view texture, and a depth map of the houses around hides
// what is behind other houses (transparent); roof slopes turned away are mirrored from the opposite slope.
// Walls not seen in the image take a copy of the opposite wall or a texture uploaded straight onto the wall.
// Saved: manual/facades.json (versioned, per block) and the images in data/historic/growth/facades/.
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { applyH, dlt, faceMesh, heightAt, homography, maxHeight, profAt, statePeriod, wallsOf, type BFac, type Face, type Layer, type ModelLike, type Wall, type XY } from './facades3d';
import { blockOf, bodyTris, camFromMatrix, depthMap, fitAffine, fitCorr, footIndex, near, openParts, outlineCorners, ridgeOf, roofMesh, seen, type Cam, type DepthMap, type Index, type Roof, type V3 } from './blocks3d';

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const inp = (id: string) => $<HTMLInputElement>(id);
let lang: 'cs' | 'en' = 'cs';
const EN: Record<string, string> = {
  title: 'Facades from photos and drawings', load: 'Load building', back: '← 3D model', sources: 'Image sources', addFile: '+ photo / drawing', addVed: '+ veduta with a camera…',
  kind: 'kind', photo: 'photograph', drawing: 'drawing / engraving', veduta: 'veduta', year: 'year', valid: 'valid',
  validHint: 'The year of the image sets the height of the houses; validity (from–to) is the period in which the textures show in the model – prefilled from the changes of the houses in the register.',
  mode: 'Method', mQuad: '4 wall corners', mCam: 'camera from points of the block', snap: 'snap clicks to a corner in the image', camFit: 'Fit camera', camApply: 'Project onto walls',
  camKind: 'camera', cAuto: 'automatic', cCorr: 'veduta + local correction', cAff: 'affine (isometric drawing)', cDlt: 'perspective (photo)',
  roofOn: 'roofs of the block from the image', ovl: 'block outline by the camera', fillHidden: 'Fill hidden walls with copies', blkAll: 'whole block', blkOne: 'this house only',
  walls: 'Walls', ctrl: 'points: left / right (m)', ctrlz: 'points: bottom / top (m)', faceDel: 'remove wall from image', copyOpp: 'copy of the opposite wall', fileTex: 'texture from a file…',
  save: 'Rectify textures and save', capImg: 'Image', cap3d: 'Block with textures (preview)',
};
const CS: Record<string, string> = {}; document.querySelectorAll<HTMLElement>('[data-t]').forEach(e => CS[e.dataset.t!] = e.textContent ?? '');
const T2 = (c: string, e: string) => (lang === 'cs' ? c : e);
const pl = (n: number, one: string, few: string, many: string) => `${n} ${n === 1 ? one : n >= 2 && n <= 4 ? few : many}`;   // Czech plural
$('lang').onclick = () => { lang = lang === 'cs' ? 'en' : 'cs'; document.querySelectorAll<HTMLElement>('[data-t]').forEach(e => e.textContent = (lang === 'en' ? EN[e.dataset.t!] : CS[e.dataset.t!]) ?? e.textContent); $('lang').textContent = lang === 'cs' ? 'EN' : 'CS'; refresh(); drawImg(); };
const status = (t: string) => { $('status').textContent = t; };
async function getJSON<T>(u: string): Promise<T | null> { try { const r = await fetch(u, { cache: 'no-store' }); return r.ok ? await r.json() as T : null; } catch { return null; } }

// ---------- data ----------
type M_ = ModelLike & { n: number; ids: string[]; origin: XY; z: number[]; classes: string[]; cls: number[]; mesh?: { file: string; files?: string[] } };
interface View { pos: [number, number, number]; quat: [number, number, number, number]; fov: number; size: [number, number]; stretch: number; year: number; how: string }
type FacFile = { note?: string; format?: number; blocks?: Record<string, BFac>; buildings?: Record<string, BFac> };
let M: M_, IX: Index, VIEWS: { origin: XY; ground: number; views: Record<string, View> } | null = null;
let VED: { id: string; label: string; url: string; year: number | null }[] = [];
const meshOf = new Map<number, { v: Float32Array; t: Uint16Array }>(), idIdx = new Map<string, number>();
type BW = Wall & { b: number; bid: string; letter: string; open: [number, number][]; openL: number };
let B = -1, BID = '', KEY = '', mem: number[] = [], walls: BW[] = [], fac: BFac = { layers: [] }, lay: Layer | null = null;
let selW = -1, selWs: number[] = [], runPts: XY[] = [], mode: 'quad' | 'cam' = 'quad', selC = 0, dirty = false;
let img: HTMLImageElement | null = null;
const hid = new Set<string>();   // walls the camera does not see (facing away or hidden behind other houses)
const yearOf = () => lay?.year ?? (+new URLSearchParams(location.search).get('year')! || 2020);
const standing = (b: number) => { const y = yearOf(), g = M.gaps[b]; return y >= M.from[b] && y < M.to[b] && !(y >= g[0] && y < g[1]) && !(y >= g[2] && y < g[3]); };
const letter = (i: number) => (i < 26 ? '' : String.fromCharCode(64 + Math.floor(i / 26))) + String.fromCharCode(65 + i % 26);
const wkey = (w: BW) => `${w.bid}#${w.k}`;
const fb = (f: Face) => f.b ?? KEY;
const isF = (f: Face, w: BW) => fb(f) === w.bid && f.wall === w.k;
const faceOf = (w: BW | undefined) => (w && lay ? lay.faces.find(f => isF(f, w)) : undefined);
const bOf = (f: Face) => idIdx.get(fb(f)) ?? B;
const zmaxOf = (w: { prof: XY[] }) => Math.max(...w.prof.map(q => q[1]));
const lenOf = (f: { p0: XY; p1: XY }) => Math.hypot(f.p1[0] - f.p0[0], f.p1[1] - f.p0[1]) || 1;
const wallPt = (w: { p0: XY; p1: XY }, t: number, z: number, base: number): V3 => {
  const L = lenOf(w); return [w.p0[0] + (w.p1[0] - w.p0[0]) * t / L, w.p0[1] + (w.p1[1] - w.p0[1]) * t / L, base + z];
};
const inOpen = (open: [number, number][] | undefined, t: number) => !open || open.some(([a, b]) => t >= a - 0.05 && t <= b + 0.05);

// ---------- points of the block for the camera: outline corners at the ground and at the eaves, gable tops ----------
interface Corner { c: string; X: V3 }
let cornerCache: Corner[] | null = null;
function corners(): Corner[] {
  if (cornerCache) return cornerCache;
  const out: Corner[] = []; if (!mem.length) return out;
  const oc = outlineCorners(mem.map(b => IX.ring(b))), y = yearOf();
  const cx = oc.reduce((s, o) => s + o.p[0], 0) / (oc.length || 1), cy = oc.reduce((s, o) => s + o.p[1], 0) / (oc.length || 1);
  oc.sort((a, b) => Math.atan2(a.p[1] - cy, a.p[0] - cx) - Math.atan2(b.p[1] - cy, b.p[0] - cx));   // anticlockwise from the west
  oc.forEach((o, i) => {
    let top = Infinity, base = NaN;
    for (const w of walls) for (const [p, t] of [[w.p0, 0], [w.p1, w.L]] as [XY, number][]) if (Math.hypot(p[0] - o.p[0], p[1] - o.p[1]) < 1.6) { top = Math.min(top, profAt(w.prof, t)); base = M.z[w.b]; }
    if (!isFinite(top)) { const b = mem.reduce((a, c) => (Math.hypot(IX.box[4 * c] - o.p[0], IX.box[4 * c + 1] - o.p[1]) < Math.hypot(IX.box[4 * a] - o.p[0], IX.box[4 * a + 1] - o.p[1]) ? c : a)); base = M.z[b]; top = heightAt(M, b, y) * 0.6; }
    out.push({ c: `R${i + 1}↓`, X: [o.p[0], o.p[1], base] }, { c: `R${i + 1}↑`, X: [o.p[0], o.p[1], base + top] });
  });
  for (const w of walls) {   // gable tops
    const e = Math.max(profAt(w.prof, 0), profAt(w.prof, w.L)), apex = w.prof.reduce((a, q) => (q[1] > a[1] ? q : a), [0, 0] as XY);
    if (apex[1] > e + 1 && apex[0] > 0.5 && apex[0] < w.L - 0.5 && inOpen(w.open, apex[0])) out.push({ c: `${w.letter}${w.k + 1}S`, X: wallPt(w, apex[0], apex[1], M.z[w.b]) });
  }
  return cornerCache = out;
}

// ---------- cameras ----------
let camRms: number | null = null, resid = new Map<string, number>(), dmCache: DepthMap | null = null;
function vedOf(l: Layer | null): View | undefined { return l && l.kind === 'veduta' && l.src.startsWith('veduta:') && VIEWS ? VIEWS.views[l.src.slice(7)] : undefined; }
function vedCam(V: View): Cam {   // veduta camera (three.js world: x, y up = absolute height, z = −north)
  const q = new THREE.Quaternion(...V.quat).invert(), C = new THREE.Vector3(...V.pos), [W, H] = V.size;
  const sx = img ? img.width / W : 1, sy = img ? img.height / H : 1;
  const f = H / 2 / Math.tan(V.fov * Math.PI / 360), fx = f * (V.stretch || 1), Cm: V3 = [V.pos[0], -V.pos[2], V.pos[1]], p = new THREE.Vector3();
  return {
    P: ([x, y, Z]) => { p.set(x, Z, -y).sub(C).applyQuaternion(q); return p.z > -1 ? null : [(W / 2 + fx * p.x / -p.z) * sx, (H / 2 - f * p.y / -p.z) * sy]; },
    toViewer: X => [Cm[0] - X[0], Cm[1] - X[1], Cm[2] - X[2]], depth: X => Math.hypot(Cm[0] - X[0], Cm[1] - X[1], Cm[2] - X[2]),
  };
}
function camOf(l: Layer | null = lay): Cam | null {
  if (!l) return null;
  if ((l.camFit === 'affine' || l.camFit === 'dlt') && l.cam) return camFromMatrix(l.cam);
  const V = vedOf(l);
  if (V) {
    const c = vedCam(V); if (l.camFit !== 'corr' || !l.corr) return c;
    // local correction (see fitCamera): P'(X) = A·q(Xg) + h·w, or without w the heights as the veduta camera has them
    const A = l.corr.slice(0, 9), [wx, wy, Zr, hasW] = l.corr.slice(9);
    return { ...c, P: X => { const g = c.P([X[0], X[1], Zr]); if (!g) return null; const a = applyH(A, ...g);
      if (hasW) return [a[0] + (X[2] - Zr) * wx, a[1] + (X[2] - Zr) * wy];
      const q = c.P(X); return q ? applyH(A, ...q) : null; } };
  }
  return l.cam ? camFromMatrix(l.cam) : null;
}
const CAMNAME = () => ({ corr: T2('veduta + místní oprava', 'veduta + local correction'), affine: T2('afinní (izometrie)', 'affine (isometric)'), dlt: T2('perspektivní', 'perspective') });
function fitCamera(quiet = false) {
  if (!lay) return false;
  const cs = corners(), pairs = (lay.pts ?? []).map(p => ({ p, c: cs.find(c => c.c === p.c)! })).filter(o => o.c);
  const X = pairs.map(o => o.c.X), uv = pairs.map(o => o.p.uv), V = vedOf(lay), want = lay.camKind ?? 'auto';
  type R = { fit: 'corr' | 'affine' | 'dlt'; cam?: number[]; corr?: number[] };
  const errs = (r: R) => { const c = camOf({ ...lay!, camFit: r.fit, cam: r.cam, corr: r.corr }); return pairs.map(o => { const q = c?.P(o.c.X); return q ? Math.hypot(q[0] - o.p.uv[0], q[1] - o.p.uv[1]) : 1e9; }); };
  const rms = (r: R | null) => { if (!r) return Infinity; const e = errs(r); return Math.sqrt(e.reduce((s, v) => s + v * v, 0) / (e.length || 1)); };
  const tryCorr = (): R | null => {
    // local correction of the veduta camera: P'(X) = A·q(Xg) + h·w – an image affine A of the ground plane (Xg = the
    // point at the ground height Zr, the mean base of the houses) and an image vector w per metre of height (the
    // draughtsman's verticals and his exaggeration of the heights); points at the ground are the corners marked ↓
    if (!V || !pairs.length) return null;
    const g = vedCam(V), Zr = mem.reduce((a, b) => a + M.z[b], 0) / (mem.length || 1), low = pairs.map(o => o.c.c.endsWith('↓'));
    const qg = X.map(x => g.P([x[0], x[1], Zr])), q = X.map(x => g.P(x)); if (qg.some(v => !v) || q.some(v => !v)) return null;
    const h = X.map(x => x[2] - Zr), gi = pairs.map((_, i) => i).filter(i => low[i]), hi = pairs.map((_, i) => i).filter(i => !low[i]);
    // w (image vector per metre of height) from the corners clicked both at the ground and at the top: robust, it
    // does not depend on the plan; then every point is brought down to the ground (uv − h·w) and the plan affine A is
    // fitted to all of them (1 point shift, 2 similarity, ≥ 3 affine) – so eave points far in the block fix its depth
    const lab = pairs.map(o => o.c.c), vpairs = hi.map(i => [i, lab.indexOf(lab[i].replace('↑', '↓'))]).filter(([i, j]) => j >= 0 && lab[i].endsWith('↑'));
    let w: XY | null = null;
    if (vpairs.length) { let wx = 0, wy = 0, hh = 0; for (const [i, j] of vpairs) { const dh = X[i][2] - X[j][2]; wx += (uv[i][0] - uv[j][0]) * dh; wy += (uv[i][1] - uv[j][1]) * dh; hh += dh * dh; } if (hh > 1) w = [wx / hh, wy / hh]; }
    if (w) {
      const all = pairs.map((_, i) => i), down = all.map(i => [uv[i][0] - h[i] * w![0], uv[i][1] - h[i] * w![1]] as XY);
      return { fit: 'corr', corr: [...planFit(all.map(i => qg[i]!), down), w[0], w[1], Zr, 1] };
    }
    const I = gi.length ? gi : pairs.map((_, i) => i), A = planFit(I.map(i => qg[i]!), I.map(i => uv[i]));
    if (!hi.length || !gi.length) return { fit: 'corr', corr: [...A, 0, 0, Zr, 0] };
    let wx = 0, wy = 0, hh = 0;   // w from the points above the ground (least squares, A fixed)
    for (const i of hi) { const a = applyH(A, ...qg[i]!); wx += (uv[i][0] - a[0]) * h[i]; wy += (uv[i][1] - a[1]) * h[i]; hh += h[i] * h[i]; }
    return { fit: 'corr', corr: [...A, wx / hh, wy / hh, Zr, 1] };
  };
  const tryAff = (): R | null => { const P = fitAffine(X, uv); return P ? { fit: 'affine', cam: P } : null; };
  const tryDlt = (): R | null => (pairs.length >= 6 ? { fit: 'dlt', cam: dlt(X, uv) } : null);
  let r: R | null = null;
  if (want === 'corr') r = tryCorr(); else if (want === 'affine') r = tryAff(); else if (want === 'dlt') r = tryDlt();
  else if (V) { const c = tryCorr(), a = pairs.length >= 6 ? tryAff() : null; r = a && rms(a) < 0.6 * rms(c) ? a : c; }
  else if (lay.kind === 'drawing') r = tryAff() ?? tryDlt(); else r = tryDlt() ?? tryAff();
  if (!r) {
    lay.camFit = undefined; lay.corr = undefined; if (!V) lay.cam = undefined; camRms = null; resid.clear(); dmCache = null;
    if (!quiet) status(want === 'corr' || (want === 'auto' && V) ? T2('Klikněte aspoň 1 bod bloku (lépe 3 rohy u země).', 'Click at least 1 point of the block (better 3 corners at the ground).')
      : want === 'dlt' || lay.kind === 'photo' ? T2('Perspektivní kamera potřebuje aspoň 6 bodů (rohy dole i nahoře, aspoň dvě stěny).', 'The perspective camera needs at least 6 points (corners at the ground and at the top, at least two walls).')
        : T2('Afinní kamera potřebuje aspoň 4 body ve dvou výškách (rohy u země i u okapu).', 'The affine camera needs at least 4 points at two heights (corners at the ground and at the eaves).'));
    return false;
  }
  lay.camFit = r.fit; lay.cam = r.cam ?? (V ? undefined : lay.cam); lay.corr = r.corr; dirty = true; dmCache = null;
  const e = errs(r); resid = new Map(pairs.map((o, i) => [o.p.c, e[i]])); camRms = Math.sqrt(e.reduce((s, v) => s + v * v, 0) / (e.length || 1));
  if (!quiet) status(T2(`Kamera ${CAMNAME()[r.fit]}: ${pl(pairs.length, 'bod', 'body', 'bodů')}, odchylka ${camRms.toFixed(1)} px (max ${Math.max(...e).toFixed(1)})${heightScale()}.`, `Camera ${CAMNAME()[r.fit]}: ${pairs.length} points, error ${camRms.toFixed(1)} px (max ${Math.max(...e).toFixed(1)})${heightScale()}.`));
  return true;
}
const heightScale = () => {   // exaggeration of the heights in the drawing against the camera of the veduta (at the same plan scale)
  if (lay?.camFit !== 'corr' || !lay.corr?.[12] || !mem.length) return '';
  const V = vedOf(lay); if (!V) return ''; const c = vedCam(V), [x0, y0, x1, y1] = blockBox(0), Zr = lay.corr[11], X: V3 = [(x0 + x1) / 2, (y0 + y1) / 2, Zr];
  const A = lay.corr.slice(0, 9), a = c.P(X), e = c.P([X[0] + 10, X[1], Zr]), n = c.P([X[0], X[1] + 10, Zr]), up = c.P([X[0], X[1], Zr + 10]); if (!a || !e || !n || !up) return '';
  // plan scale of the correction (image area of 10 × 10 m, drawing / camera) and the heights (drawing / camera)
  const ar = (p: XY, q: XY, r: XY) => Math.abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]));
  const sPlan = Math.sqrt(ar(applyH(A, ...a), applyH(A, ...e), applyH(A, ...n)) / (ar(a, e, n) || 1)), sH = Math.hypot(lay.corr[9], lay.corr[10]) * 10 / (Math.hypot(up[0] - a[0], up[1] - a[1]) || 1);
  return T2(`, kresba: půdorys × ${sPlan.toFixed(2)}, výšky × ${sH.toFixed(2)}`, `, drawing: plan × ${sPlan.toFixed(2)}, heights × ${sH.toFixed(2)}`);
};
/** Plan correction: affine (≤ 3 points: shift, similarity, affine) or a homography from 4 points on. */
function planFit(q0: XY[], uv0: XY[]): number[] {
  const q: XY[] = [], uv: XY[] = [], n: number[] = [];   // one point per place (a corner clicked at the ground and at the top)
  q0.forEach((p, i) => { const j = q.findIndex(o => Math.hypot(o[0] - p[0], o[1] - p[1]) < 0.5); if (j < 0) { q.push(p); uv.push([...uv0[i]] as XY); n.push(1); } else { uv[j] = [(uv[j][0] * n[j] + uv0[i][0]) / (n[j] + 1), (uv[j][1] * n[j] + uv0[i][1]) / (n[j] + 1)]; n[j]++; } });
  const tri = (a: XY, b: XY, c: XY) => Math.abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2;
  let minT = Infinity, maxT = 0;
  for (let i = 0; i < q.length; i++) for (let j = i + 1; j < q.length; j++) for (let k = j + 1; k < q.length; k++) { const t = tri(q[i], q[j], q[k]); minT = Math.min(minT, t); maxT = Math.max(maxT, t); }
  if (q.length >= 4 && minT > 20) { const H = homography(q, uv); if (H.every(isFinite)) return H; }
  const A = q.length >= 3 && maxT > 20 ? fitCorr(q, uv) : fitCorr(q.slice(0, 2), uv.slice(0, 2)); return [...A, 0, 0, 1];
}
/** Depth map of the houses around the block as the layer's camera sees them (cached until the camera changes). */
function depth(): DepthMap | null {
  const cam = camOf(); if (!cam || !img || !mem.length) return null;
  if (dmCache) return dmCache;
  const y = yearOf(), skip = new Set(['moat', 'ditch'].map(c => M.classes.indexOf(c)));
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const b of mem) { x0 = Math.min(x0, IX.box[4 * b]); y0 = Math.min(y0, IX.box[4 * b + 1]); x1 = Math.max(x1, IX.box[4 * b + 2]); y1 = Math.max(y1, IX.box[4 * b + 3]); }
  const R = lay?.kind === 'photo' ? 250 : 120;
  const bs = near(IX, M.n, x0 - R, y0 - R, x1 + R, y1 + R, b => (standing(b) || mem.includes(b)) && !skip.has(M.cls[b]));
  const tris = bs.map(b => { const t = bodyTris(M, b, y, meshOf.get(b)), z = M.z[b]; for (let i = 2; i < t.length; i += 3) t[i] += z; return t; });
  const k = Math.max(1, Math.max(img.width, img.height) / 2000);
  return dmCache = depthMap(cam, tris, Math.ceil(img.width / k), Math.ceil(img.height / k), k);
}
/** Share of the open part of a wall that the camera sees. */
function seenShare(w: BW, cam: Cam, dm: DepthMap): number {
  let s = 0, n = 0;
  for (const [a, b] of w.open) for (let t = a + 0.25; t < b; t += Math.max(0.5, (b - a) / 10)) {
    const top = profAt(w.prof, t);
    for (let z = 0.4; z < top; z += Math.max(0.6, top / 6)) { const X = wallPt(w, t, z, M.z[w.b]), uv = cam.P(X); n++; if (uv && seen(dm, cam, X, uv)) s++; }
  }
  return n ? s / n : 0;
}
function applyCamera(quiet = false) {
  const cam = camOf(); if (!cam || !lay || !img) { if (!quiet) status(T2('Nejdřív spočítejte kameru.', 'Fit the camera first.')); return; }
  const dm = depth()!; let n = 0; hid.clear();
  for (const w of walls) {
    const f0 = faceOf(w); if (f0 && (f0.how === 'manual' || f0.how === 'file' || f0.how === 'copy')) continue;   // kept
    const mid = wallPt(w, w.L / 2, 1, M.z[w.b]), tv = cam.toViewer(mid);
    const drop = () => { hid.add(wkey(w)); if (f0) lay!.faces = lay!.faces.filter(f => f !== f0); };
    if (tv[0] * w.out[0] + tv[1] * w.out[1] <= 0) { drop(); continue; }   // facing away
    const ctrl: [number, number, number, number] = [0, 0, w.L, zmaxOf(w)];
    const quad = ctrlCorners(ctrl).map(([t, z]) => cam.P(wallPt(w, t, z, M.z[w.b])));
    if (quad.some(q => !q) || !quad.some(q => q![0] >= 0 && q![1] >= 0 && q![0] <= img!.width && q![1] <= img!.height)) { drop(); continue; }
    const share = seenShare(w, cam, dm);
    if (share < 0.15) { drop(); continue; }   // hidden behind other houses
    setFace(w, { ctrl, quad: quad as XY[], how: vedOf(lay) && lay.camFit !== 'affine' && lay.camFit !== 'dlt' ? 'veduta' : 'camera' }); faceOf(w)!.seen = Math.round(share * 100) / 100; n++;
  }
  if (!quiet) status(T2(`Promítnuto na ${pl(n, 'stěnu', 'stěny', 'stěn')}, ${pl(hid.size, 'stěnu', 'stěny', 'stěn')} kamera nevidí (lze je doplnit kopiemi nebo texturou ze souboru).`, `Projected onto ${n} walls; ${hid.size} walls are not seen by the camera (fill them with copies or a texture from a file).`));
  changed();
}
const ctrlCorners = (c: number[]): XY[] => [[c[0], c[1]], [c[2], c[1]], [c[2], c[3]], [c[0], c[3]]];
function setFace(w: BW, o: { ctrl: [number, number, number, number]; quad: XY[]; how: Face['how'] }): Face | undefined {
  if (!lay) return;
  const f: Face = { wall: w.k, b: w.bid, p0: w.p0, p1: w.p1, out: w.out, prof: w.prof, rect: [0, 0, w.L, zmaxOf(w)], ctrl: o.ctrl, quad: o.quad, tex: '', how: o.how };
  if (w.openL < w.L - 0.3) f.open = w.open.map(([a, b]) => [Math.round(a * 100) / 100, Math.round(b * 100) / 100]);
  lay.faces = [...lay.faces.filter(x => !isF(x, w)), f]; dirty = true; return f;
}
/** Face providing the pixels of f (the wall itself, or the source of a copy). */
const sourceOf = (f: Face) => (f.copy ? lay?.faces.find(g => fb(g) === f.copy!.b && g.wall === f.copy!.wall && !g.copy) : f);

// ---------- source pixels ----------
const pixCache = new Map<string, { img: HTMLImageElement; pix: ImageData; k: number }>();
const srcURL = (src: string) => src.startsWith('veduta:') ? VED.find(v => v.id === src.slice(7))?.url ?? '' : '/data/historic/growth/facades/' + src;
async function loadPix(src: string) {
  if (pixCache.has(src)) return pixCache.get(src)!;
  const im = await new Promise<HTMLImageElement | null>(res => { const i = new Image(); i.onload = () => res(i); i.onerror = () => res(null); i.src = srcURL(src); });
  if (!im) return null;
  const k = Math.max(1, Math.max(im.width, im.height) / 6000), cv = document.createElement('canvas'); cv.width = Math.round(im.width / k); cv.height = Math.round(im.height / k);
  const g = cv.getContext('2d', { willReadFrequently: true })!; g.drawImage(im, 0, 0, cv.width, cv.height);
  const e = { img: im, pix: g.getImageData(0, 0, cv.width, cv.height), k }; pixCache.set(src, e); return e;
}
function sample(P: { pix: ImageData; k: number }, u0: number, v0: number, o: Uint8ClampedArray, q: number): boolean {
  const u = u0 / P.k - 0.5, v = v0 / P.k - 0.5, sw = P.pix.width, s = P.pix.data;
  if (u < 0 || v < 0 || u >= sw - 1 || v >= P.pix.height - 1) return false;
  const x0 = u | 0, y0 = v | 0, fx = u - x0, fy = v - y0, k = (y0 * sw + x0) * 4;
  for (let c = 0; c < 3; c++) o[q + c] = (s[k + c] * (1 - fx) + s[k + 4 + c] * fx) * (1 - fy) + (s[k + sw * 4 + c] * (1 - fx) + s[k + sw * 4 + 4 + c] * fx) * fy;
  o[q + 3] = 255; return true;
}

// ---------- rectification of a wall ----------
function rectify(f: Face, ppmMax: number): HTMLCanvasElement | null {
  const s0 = sourceOf(f); if (!s0 || s0.quad.length < 4 || !lay) return null;
  const P = pixCache.get(s0.src ?? lay.src); if (!P) return null;
  const sc = f.copy ? lenOf(s0) / lenOf(f) : 1;
  const H = homography(ctrlCorners(s0.ctrl), s0.quad);
  const [t0, z0, t1, z1] = f.rect;
  const est = Math.max(Math.hypot(s0.quad[1][0] - s0.quad[0][0], s0.quad[1][1] - s0.quad[0][1]) / (s0.ctrl[2] - s0.ctrl[0] || 1), Math.hypot(s0.quad[3][0] - s0.quad[0][0], s0.quad[3][1] - s0.quad[0][1]) / (s0.ctrl[3] - s0.ctrl[1] || 1));
  let ppm = Math.min(ppmMax, Math.max(8, Math.round(est * 1.2)));
  ppm = Math.min(ppm, 2048 / Math.max(t1 - t0, z1 - z0));
  // visibility of the source wall (camera faces): a 0.25 m grid checked against the depth map
  let vis: Uint8Array | null = null, nT = 0, nZ = 0;
  const cam = !s0.src && (s0.how === 'camera' || s0.how === 'veduta') ? camOf() : null, dm = cam ? depth() : null;
  if (cam && dm) {
    const Ls = lenOf(s0), zs = zmaxOf(s0), base = M.z[bOf(s0)]; nT = Math.ceil(Ls / 0.25); nZ = Math.ceil(zs / 0.25); vis = new Uint8Array(nT * nZ);
    for (let j = 0; j < nZ; j++) for (let i = 0; i < nT; i++) { const X = wallPt(s0, (i + 0.5) * 0.25, (j + 0.5) * 0.25, base), uv = cam.P(X); vis[j * nT + i] = uv && seen(dm, cam, X, uv) ? 1 : 0; }
  }
  const W = Math.max(2, Math.round((t1 - t0) * ppm)), Ht = Math.max(2, Math.round((z1 - z0) * ppm));
  const cv = document.createElement('canvas'); cv.width = W; cv.height = Ht; const g = cv.getContext('2d')!, out = g.createImageData(W, Ht), o = out.data;
  for (let j = 0; j < Ht; j++) {
    const z = z1 - (j + 0.5) / Ht * (z1 - z0);
    for (let i = 0; i < W; i++) {
      const t = t0 + (i + 0.5) / W * (t1 - t0);
      if (z > profAt(f.prof, t) + 0.05 || !inOpen(f.open, t)) continue;   // above the wall (sky beside a gable), party wall
      const ts = t * sc;
      if (vis) { const ii = Math.min(nT - 1, Math.floor(ts / 0.25)), jj = Math.min(nZ - 1, Math.floor(z / 0.25)); if (ii < 0 || jj < 0 || !vis[jj * nT + ii]) continue; }
      const w_ = H[6] * ts + H[7] * z + H[8]; if (w_ <= 0) continue;
      sample(P, (H[0] * ts + H[1] * z + H[2]) / w_, (H[3] * ts + H[4] * z + H[5]) / w_, o, (j * W + i) * 4);
    }
  }
  g.putImageData(out, 0, 0); return cv;
}

// ---------- roofs of the block: one plan-view texture, hidden slopes mirrored from the opposite slope ----------
function blockBox(m = 1): [number, number, number, number] {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const b of mem) { x0 = Math.min(x0, IX.box[4 * b]); y0 = Math.min(y0, IX.box[4 * b + 1]); x1 = Math.max(x1, IX.box[4 * b + 2]); y1 = Math.max(y1, IX.box[4 * b + 3]); }
  return [x0 - m, y0 - m, x1 + m, y1 + m];
}
function rectifyRoof(ppmMax: number): { cv: HTMLCanvasElement; roof: Roof } | null {
  const cam = camOf(), P = lay && pixCache.get(lay.src), dm = depth(); if (!cam || !P || !lay || !dm) return null;
  const y = yearOf(), box = blockBox(1), [x0, y0, x1, y1] = box;
  const c3: V3 = [(x0 + x1) / 2, (y0 + y1) / 2, M.z[mem[0]] + 8], a = cam.P(c3), bq = cam.P([c3[0] + 1, c3[1], c3[2]]), cq = cam.P([c3[0], c3[1] + 1, c3[2]]);
  const est = a && bq && cq ? (Math.hypot(bq[0] - a[0], bq[1] - a[1]) + Math.hypot(cq[0] - a[0], cq[1] - a[1])) / 2 : 2;
  let ppm = Math.min(ppmMax, Math.max(4, Math.round(est * 1.5))); ppm = Math.min(ppm, 2048 / Math.max(x1 - x0, y1 - y0));
  const W = Math.ceil((x1 - x0) * ppm), Hh = Math.ceil((y1 - y0) * ppm), N = W * Hh;
  const zb = new Float32Array(N).fill(-Infinity), bi = new Int32Array(N).fill(-1), nrm = new Float32Array(N * 3);
  const ridges: ([XY, XY] | null)[] = [];
  mem.forEach((b, mi) => {
    const T = bodyTris(M, b, y, meshOf.get(b), true), base = M.z[b]; ridges.push(ridgeOf(T));
    for (let i = 0; i < T.length; i += 9) {
      const p = [0, 1, 2].map(j => [(T[i + 3 * j] - x0) * ppm, (y1 - T[i + 3 * j + 1]) * ppm, base + T[i + 3 * j + 2]]);
      const ux = T[i + 3] - T[i], uy = T[i + 4] - T[i + 1], uz = T[i + 5] - T[i + 2], vx = T[i + 6] - T[i], vy = T[i + 7] - T[i + 1], vz = T[i + 8] - T[i + 2];
      let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; if (nz < 0) { nx = -nx; ny = -ny; nz = -nz; }
      const den = (p[1][1] - p[2][1]) * (p[0][0] - p[2][0]) + (p[2][0] - p[1][0]) * (p[0][1] - p[2][1]); if (Math.abs(den) < 1e-9) continue;
      const ia = Math.max(0, Math.floor(Math.min(p[0][0], p[1][0], p[2][0]))), ib = Math.min(W - 1, Math.ceil(Math.max(p[0][0], p[1][0], p[2][0])));
      const ja = Math.max(0, Math.floor(Math.min(p[0][1], p[1][1], p[2][1]))), jb = Math.min(Hh - 1, Math.ceil(Math.max(p[0][1], p[1][1], p[2][1])));
      for (let j = ja; j <= jb; j++) for (let ii = ia; ii <= ib; ii++) {
        const px = ii + 0.5, py = j + 0.5;
        const l0 = ((p[1][1] - p[2][1]) * (px - p[2][0]) + (p[2][0] - p[1][0]) * (py - p[2][1])) / den, l1 = ((p[2][1] - p[0][1]) * (px - p[2][0]) + (p[0][0] - p[2][0]) * (py - p[2][1])) / den, l2 = 1 - l0 - l1;
        if (l0 < -0.01 || l1 < -0.01 || l2 < -0.01) continue;
        const z = l0 * p[0][2] + l1 * p[1][2] + l2 * p[2][2], o = j * W + ii;
        if (z > zb[o]) { zb[o] = z; bi[o] = mi; nrm[3 * o] = nx / l; nrm[3 * o + 1] = ny / l; nrm[3 * o + 2] = nz / l; }
      }
    }
  });
  const cv = document.createElement('canvas'); cv.width = W; cv.height = Hh; const g = cv.getContext('2d')!, out = g.createImageData(W, Hh), od = out.data;
  const vis = new Uint8Array(N); let nRoof = 0, nSeen = 0, nMir = 0;
  for (let j = 0; j < Hh; j++) for (let i = 0; i < W; i++) {
    const o = j * W + i; if (bi[o] < 0) continue; nRoof++;
    const X: V3 = [x0 + (i + 0.5) / ppm, y1 - (j + 0.5) / ppm, zb[o]], tv = cam.toViewer(X);
    if (nrm[3 * o] * tv[0] + nrm[3 * o + 1] * tv[1] + nrm[3 * o + 2] * tv[2] <= 0) continue;   // slope turned away
    const uv = cam.P(X); if (!uv || !seen(dm, cam, X, uv, 1.0)) continue;
    if (sample(P, uv[0], uv[1], od, o * 4)) { vis[o] = 1; nSeen++; }
  }
  for (let j = 0; j < Hh; j++) for (let i = 0; i < W; i++) {   // hidden slopes: mirror image across the ridge of the same house
    const o = j * W + i; if (bi[o] < 0 || vis[o]) continue; const r = ridges[bi[o]]; if (!r) continue;
    const x = x0 + (i + 0.5) / ppm, yy = y1 - (j + 0.5) / ppm, dx = r[1][0] - r[0][0], dy = r[1][1] - r[0][1], l2 = dx * dx + dy * dy || 1;
    const t = ((x - r[0][0]) * dx + (yy - r[0][1]) * dy) / l2, fx = r[0][0] + t * dx, fy = r[0][1] + t * dy, xm = 2 * fx - x, ym = 2 * fy - yy;
    const im = Math.floor((xm - x0) * ppm), jm = Math.floor((y1 - ym) * ppm); if (im < 0 || jm < 0 || im >= W || jm >= Hh) continue;
    const om = jm * W + im; if (!vis[om] || bi[om] !== bi[o]) continue;
    od.set(od.subarray(om * 4, om * 4 + 4), o * 4); nMir++;
  }
  // the rest (slopes hidden on both sides): the nearest textured pixel of the same house along its ridge, else the
  // nearest textured roof pixel of the block – the roofs keep the tone and hatching of the drawing
  const done = new Uint8Array(N); for (let o = 0; o < N; o++) done[o] = od[o * 4 + 3] ? 1 : 0;
  let nFill = 0; const filled = new Uint8Array(N);
  for (let j = 0; j < Hh; j++) for (let i = 0; i < W; i++) {
    const o = j * W + i; if (bi[o] < 0 || done[o]) continue;
    let src = -1; const r = ridges[bi[o]];
    if (r) { const L = Math.hypot(r[1][0] - r[0][0], r[1][1] - r[0][1]) || 1, ux = (r[1][0] - r[0][0]) / L, uy = -(r[1][1] - r[0][1]) / L;
      for (let k = 1; k < 60 && src < 0; k++) for (const sg of [1, -1]) { const ii = Math.round(i + sg * k * ux), jj = Math.round(j + sg * k * uy); if (ii < 0 || jj < 0 || ii >= W || jj >= Hh) continue; const q = jj * W + ii; if (done[q] && bi[q] === bi[o]) { src = q; break; } } }
    for (let rad = 1; rad <= 30 && src < 0; rad++) for (let dj = -rad; dj <= rad && src < 0; dj++) for (const di of Math.abs(dj) === rad ? Array.from({ length: 2 * rad + 1 }, (_, k) => k - rad) : [-rad, rad]) {
      const ii = i + di, jj = j + dj; if (ii < 0 || jj < 0 || ii >= W || jj >= Hh) continue; const q = jj * W + ii; if (done[q]) { src = q; break; } }
    if (src >= 0) { od.set(od.subarray(src * 4, src * 4 + 4), o * 4); filled[o] = 1; nFill++; }
  }
  g.putImageData(out, 0, 0);
  const sh = (n: number) => Math.round(n / (nRoof || 1) * 100) / 100;
  return { cv, roof: { tex: '', box: box.map(v => Math.round(v * 100) / 100) as Roof['box'], px: [W, Hh], seen: sh(nSeen), mirrored: sh(nMir), filled: sh(nFill) } };
}

// ---------- assisted clicking: snap to the strongest corner (Harris) near the click ----------
function snap(x: number, y: number, r: number): XY {
  const P = lay && pixCache.get(lay.src); if (!P || !inp('snap').checked) return [x, y];
  const pix = P.pix, pixK = P.k, W = pix.width, Hh = pix.height, d = pix.data, cx = Math.round(x / pixK), cy = Math.round(y / pixK), R = Math.max(4, Math.min(40, Math.round(r / pixK))), Q = R + 3;
  if (cx - Q < 1 || cy - Q < 1 || cx + Q >= W - 1 || cy + Q >= Hh - 1) return [x, y];
  const n = 2 * Q + 1, gray = new Float32Array(n * n), ix = new Float32Array(n * n), iy = new Float32Array(n * n);
  for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) { const k = ((cy - Q + j) * W + cx - Q + i) * 4; gray[j * n + i] = 0.3 * d[k] + 0.59 * d[k + 1] + 0.11 * d[k + 2]; }
  for (let j = 1; j < n - 1; j++) for (let i = 1; i < n - 1; i++) { const k = j * n + i; ix[k] = gray[k + 1] - gray[k - 1]; iy[k] = gray[k + n] - gray[k - n]; }
  // Harris response in the circle, then the best compromise of strength (relative to the strongest corner there) and
  // closeness to the click: the user clicks near the corner they mean, the snap only removes the last pixels of error
  const Rs: [number, number, number][] = []; let rmax = 0;
  for (let j = 3; j < n - 3; j++) for (let i = 3; i < n - 3; i++) {
    if ((i - Q) ** 2 + (j - Q) ** 2 > R * R) continue;
    let a = 0, b = 0, c = 0;
    for (let v = -2; v <= 2; v++) for (let u = -2; u <= 2; u++) { const k = (j + v) * n + i + u; a += ix[k] * ix[k]; b += ix[k] * iy[k]; c += iy[k] * iy[k]; }
    const h = (a * c - b * b) - 0.05 * (a + c) ** 2; if (h > 0) { Rs.push([i, j, h]); rmax = Math.max(rmax, h); }
  }
  let best = -1e9, bx = cx, by = cy;
  for (const [i, j, h] of Rs) { const sc = Math.sqrt(h / rmax) - 2.0 * ((i - Q) ** 2 + (j - Q) ** 2) / (R * R); if (sc > best) { best = sc; bx = cx - Q + i; by = cy - Q + j; } }
  return rmax > 5e5 && best > 0 ? [(bx + 0.5) * pixK, (by + 0.5) * pixK] : [x, y];
}

// ---------- 3D preview ----------
const gl = $<HTMLCanvasElement>('gl'), p3 = $('p3'), labels = $('labels');
const renderer = new THREE.WebGLRenderer({ canvas: gl, antialias: true, preserveDrawingBuffer: true });
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xdfe4e2);
const cam3 = new THREE.PerspectiveCamera(40, 1, 0.5, 5000), ctl = new OrbitControls(cam3, gl);
scene.add(new THREE.HemisphereLight(0xffffff, 0x9a9a8a, 1.7)); const sun = new THREE.DirectionalLight(0xffffff, 1.3); sun.position.set(-60, 120, 40); scene.add(sun);
const bGroup = new THREE.Group(), fGroup = new THREE.Group(); scene.add(bGroup, fGroup);
const matMem = new THREE.MeshLambertMaterial({ color: 0xd9cfc0, side: THREE.DoubleSide, flatShading: true }), matCtx = new THREE.MeshLambertMaterial({ color: 0xb4bab6, side: THREE.DoubleSide, flatShading: true, transparent: true, opacity: 0.55 });
function bodyMesh(b: number, mat: THREE.Material) {
  const T = bodyTris(M, b, yearOf(), meshOf.get(b)), z = M.z[b], pos = new Float32Array(T.length);
  for (let i = 0; i < T.length; i += 3) { pos[i] = T[i]; pos[i + 1] = z + T[i + 2]; pos[i + 2] = -T[i + 1]; }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, mat); m.userData.b = b; return m;
}
function building3d() {
  bGroup.clear(); if (!mem.length) return;
  for (const b of mem) bGroup.add(bodyMesh(b, matMem));
  const [x0, y0, x1, y1] = blockBox(35);
  for (const b of near(IX, M.n, x0, y0, x1, y1, c => standing(c) && !mem.includes(c))) bGroup.add(bodyMesh(b, matCtx));
  const c = centre(), gr = new THREE.Mesh(new THREE.CircleGeometry(Math.max(80, (x1 - x0) * 0.8), 48), new THREE.MeshLambertMaterial({ color: 0xc3cfc3 })); gr.rotation.x = -Math.PI / 2; gr.position.set(c[0], c[1] - 0.05, c[2]); bGroup.add(gr);
  for (const i of selWs.length ? selWs : selW >= 0 ? [selW] : []) {   // outline of the selected walls
    const w = walls[i]; if (!w) continue;
    const pts = [[0, 0], [w.L, 0], ...[...w.prof].reverse()].map(([t, z]) => { const p = wallPt(w, t, z, M.z[w.b]); return new THREE.Vector3(p[0] + w.out[0] * 0.2, p[2], -(p[1] + w.out[1] * 0.2)); });
    bGroup.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xe0a020 })));
  }
}
const centre = (): [number, number, number] => { const [x0, y0, x1, y1] = blockBox(0); return [(x0 + x1) / 2, M.z[B], -(y0 + y1) / 2]; };
let previewTimer = 0;
function faces3d() {
  clearTimeout(previewTimer);
  previewTimer = window.setTimeout(async () => {
    fGroup.clear(); if (!lay || !mem.length) return;
    await Promise.all(lay.faces.filter(f => f.src).map(f => loadPix(f.src!)));
    for (const f of lay.faces) { const cv = rectify(f, 25); if (!cv) continue; const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; fGroup.add(faceMesh(f, M.z[bOf(f)], tx)); }
    if (!lay.noRoof && camOf()) {
      const r = rectifyRoof(30);
      if (r) { const tx = new THREE.CanvasTexture(r.cv); tx.colorSpace = THREE.SRGBColorSpace; for (const b of mem) fGroup.add(roofMesh(bodyTris(M, b, yearOf(), meshOf.get(b), true), r.roof.box, M.z[b], tx)); roofInfo = r.roof; }
    } else roofInfo = null;
    refresh();
  }, 150);
}
let roofInfo: Roof | null = null;
function focus3d() {
  if (!mem.length) return; const c = new THREE.Vector3(...centre()), [x0, y0, x1, y1] = blockBox(0), ext = Math.max(10, Math.hypot(x1 - x0, y1 - y0) / 2), h = Math.max(...mem.map(b => maxHeight(M, b)));
  ctl.target.set(c.x, c.y + h / 2, c.z); cam3.position.set(c.x + ext * 0.6, c.y + h + ext * 1.3, c.z + ext * 1.6);
}
function size3d() { const r = p3.getBoundingClientRect(); renderer.setPixelRatio(devicePixelRatio); renderer.setSize(r.width, r.height, false); cam3.aspect = r.width / Math.max(r.height, 1); cam3.updateProjectionMatrix(); }
renderer.setAnimationLoop(() => {
  ctl.update(); renderer.render(scene, cam3);
  if (mode !== 'cam' || !mem.length || !lay) { labels.innerHTML = ''; return; }   // point labels (camera mode)
  const r = p3.getBoundingClientRect(), done = new Set((lay.pts ?? []).map(p => p.c)); let html = '';
  corners().forEach((c, i) => { const v = new THREE.Vector3(c.X[0], c.X[2], -c.X[1]).project(cam3); if (v.z > 1 || Math.abs(v.x) > 1.05 || Math.abs(v.y) > 1.05) return;
    html += `<span class="${i === selC ? 'on' : done.has(c.c) ? 'done' : ''}" style="left:${(v.x + 1) / 2 * r.width}px;top:${(1 - v.y) / 2 * r.height}px">${c.c}</span>`; });
  labels.innerHTML = html;
});
addEventListener('resize', () => { size3d(); sizeImg(); });

// ---------- image canvas ----------
const ic = $<HTMLCanvasElement>('img'), ix = ic.getContext('2d')!;
let iv = { cx: 0, cy: 0, s: 1 };
const DPR = () => devicePixelRatio;
const S2I = (u: number, v: number): XY => [(u - ic.width / 2) / DPR() * iv.s + iv.cx, (v - ic.height / 2) / DPR() * iv.s + iv.cy];
function sizeImg() { const r = ic.parentElement!.getBoundingClientRect(); ic.width = r.width * DPR(); ic.height = r.height * DPR(); drawImg(); }
const QC = ['#2d9a4e', '#2f5fd0', '#d0402a', '#e0a020'];
function drawImg() {
  ix.setTransform(1, 0, 0, 1, 0, 0); ix.fillStyle = '#e9e7e0'; ix.fillRect(0, 0, ic.width, ic.height);
  nextHint();
  if (!img || !lay) return;
  const k = DPR() / iv.s; ix.setTransform(k, 0, 0, k, ic.width / 2 - iv.cx * k, ic.height / 2 - iv.cy * k); ix.imageSmoothingEnabled = iv.s > 1; ix.drawImage(img, 0, 0);
  const cam = camOf();
  if (cam && inp('ovl').checked) {   // the block projected by the camera (check): walls and ridges
    const line = (c1: string, w1: number) => { ix.strokeStyle = 'rgba(255,255,255,.85)'; ix.lineWidth = (w1 + 1.5) / k; ix.stroke(); ix.strokeStyle = c1; ix.lineWidth = w1 / k; ix.stroke(); };
    for (const w of walls) {
      const pts = [[0, 0], [w.L, 0], ...[...w.prof].reverse()].map(([t, z]) => cam.P(wallPt(w, t, z, M.z[w.b])));
      if (pts.some(p => !p)) continue; ix.beginPath(); pts.forEach((p, i) => (i ? ix.lineTo(...p!) : ix.moveTo(...p!))); ix.closePath(); line(hid.has(wkey(w)) ? 'rgba(120,120,120,.6)' : 'rgba(30,30,30,.9)', 1);
    }
    for (const b of mem) { const r = ridgeOf(bodyTris(M, b, yearOf(), meshOf.get(b), true)); if (!r) continue; const zt = M.z[b] + heightAt(M, b, yearOf()); const a = cam.P([r[0][0], r[0][1], zt]), c = cam.P([r[1][0], r[1][1], zt]); if (a && c) { ix.beginPath(); ix.moveTo(...a); ix.lineTo(...c); line('rgba(140,59,46,.9)', 1); } }
  }
  for (const f of lay.faces) {   // quads
    if (f.copy || f.src) continue;
    const on = selWs.some(i => walls[i] && isF(f, walls[i])) || isF(f, walls[selW] ?? ({} as BW));
    ix.beginPath(); f.quad.forEach((q, i) => (i ? ix.lineTo(...q) : ix.moveTo(...q))); if (f.quad.length === 4) ix.closePath();
    ix.strokeStyle = on ? '#e0a020' : 'rgba(208,64,42,.85)'; ix.lineWidth = (on ? 2.5 : 1.2) / k; ix.stroke();
    if (on || f.quad.length < 4) f.quad.forEach((q, i) => { ix.beginPath(); ix.arc(q[0], q[1], 5 / k, 0, 7); ix.fillStyle = QC[i]; ix.fill(); ix.strokeStyle = '#fff'; ix.lineWidth = 1.2 / k; ix.stroke(); });
    if (on) { const c = f.quad.reduce((s, q) => [s[0] + q[0] / f.quad.length, s[1] + q[1] / f.quad.length], [0, 0]); const w = walls.find(w => isF(f, w)); const lb = w ? w.letter + (w.k + 1) : ''; ix.font = `600 ${12 / k}px system-ui`; ix.fillStyle = '#fff'; ix.strokeStyle = '#000'; ix.lineWidth = 3 / k; ix.strokeText(lb, c[0], c[1]); ix.fillText(lb, c[0], c[1]); }
  }
  runPts.forEach((q, i) => { ix.beginPath(); ix.arc(q[0], q[1], 5 / k, 0, 7); ix.fillStyle = QC[i]; ix.fill(); ix.strokeStyle = '#fff'; ix.lineWidth = 1.2 / k; ix.stroke(); });
  if (mode === 'cam') for (const p of lay.pts ?? []) {
    ix.beginPath(); ix.arc(p.uv[0], p.uv[1], 4 / k, 0, 7); ix.fillStyle = '#7a2e8c'; ix.fill(); ix.strokeStyle = '#fff'; ix.lineWidth = 1.2 / k; ix.stroke();
    ix.font = `600 ${11 / k}px system-ui`; ix.fillStyle = '#7a2e8c'; ix.fillText(p.c, p.uv[0] + 5 / k, p.uv[1] - 5 / k);
    if (cam) { const c = corners().find(c => c.c === p.c); const q = c ? cam.P(c.X) : null; if (q) { ix.beginPath(); ix.moveTo(...p.uv); ix.lineTo(...q); ix.strokeStyle = '#e03131'; ix.lineWidth = 1.5 / k; ix.stroke(); } }
  }
}
const QN = () => [T2('levý dolní', 'bottom left'), T2('pravý dolní', 'bottom right'), T2('pravý horní', 'top right'), T2('levý horní', 'top left')];
function nextHint() {
  const el = $('next'); let t = '';
  if (B < 0) t = T2('Zadejte id budovy (nebo otevřete stránku z panelu domu ve 3D modelu).', 'Enter a building id (or open this page from the house panel of the 3D model).');
  else if (!lay) t = T2('Přidejte fotku nebo kresbu, nebo vyberte vedutu s kamerou.', 'Add a photo or drawing, or choose a veduta with a camera.');
  else if (mode === 'quad') {
    if (selWs.length > 1) t = runAxis() ? T2(`Fronta ${selWs.length} stěn: klikněte ${QN()[runPts.length]} roh celé fronty (nahoře = nejnižší okap).`, `Front of ${selWs.length} walls: click the ${QN()[runPts.length]} corner of the whole front (top = the lowest eave).`)
      : T2('Vybrané stěny neleží v jedné řadě (odchylka směru > 25°).', 'The selected walls are not in one row (direction differs by > 25°).');
    else {
      const w = walls[selW], f = faceOf(w);
      t = selW < 0 ? T2('Vyberte stěnu (seznam vlevo nebo klik ve 3D; Shift přidá další stěnu fronty).', 'Select a wall (list on the left or click in 3D; Shift adds another wall of a front).')
        : f?.copy ? T2(`Stěna ${w.letter}${w.k + 1}: kopie stěny ${f.copy.b === w.bid ? '' : f.copy.b + ' '}${f.copy.wall + 1}.`, `Wall ${w.letter}${w.k + 1}: copy of wall ${f.copy.wall + 1}.`)
          : f?.src ? T2(`Stěna ${w.letter}${w.k + 1}: textura ze souboru (rozsah upravte čísly vlevo).`, `Wall ${w.letter}${w.k + 1}: texture from a file (adjust the extent with the numbers on the left).`)
            : !f || f.quad.length < 4 ? T2(`Stěna ${w.letter}${w.k + 1}: klikněte ${QN()[f?.quad.length ?? 0]} roh stěny (při pohledu zvenku; nahoře = okap).`, `Wall ${w.letter}${w.k + 1}: click the ${QN()[f?.quad.length ?? 0]} corner of the wall (seen from outside; top = eave).`)
              : T2(`Stěna ${w.letter}${w.k + 1}: hotovo – rohy lze táhnout, Delete stěnu odebere.`, `Wall ${w.letter}${w.k + 1}: done – drag the corners, Delete removes the wall.`);
    }
  } else {
    const cs = corners(); t = T2(`Klikněte v obrázku bod ${cs[selC]?.c ?? ''} (popisky ve 3D: R↓ roh bloku u země, R↑ u okapu, S vrchol štítu). Bodů: ${lay.pts?.length ?? 0}.`, `Click point ${cs[selC]?.c ?? ''} in the image (labels in 3D: R↓ block corner at the ground, R↑ at the eave, S gable top). Points: ${lay.pts?.length ?? 0}.`)
      + (camRms != null && lay.camFit ? T2(` Kamera ${CAMNAME()[lay.camFit]}: odchylka ${camRms.toFixed(1)} px.`, ` Camera ${CAMNAME()[lay.camFit]}: error ${camRms.toFixed(1)} px.`) : '');
  }
  el.textContent = t; el.style.display = t ? '' : 'none';
}
/** Axis of a front of several selected walls (nearly parallel, same outward side): origin and direction; T = position along it. */
function runAxis(): { o: XY; u: XY; Lt: number; T: (p: XY) => number } | null {
  const ws = selWs.map(i => walls[i]).filter(Boolean); if (ws.length < 2) return null;
  let ux = 0, uy = 0; for (const w of ws) { ux += (w.p1[0] - w.p0[0]) / w.L * w.L; uy += (w.p1[1] - w.p0[1]) / w.L * w.L; }
  const l = Math.hypot(ux, uy) || 1, u: XY = [ux / l, uy / l];
  if (ws.some(w => ((w.p1[0] - w.p0[0]) * u[0] + (w.p1[1] - w.p0[1]) * u[1]) / w.L < Math.cos(25 * Math.PI / 180))) return null;
  const pr = (p: XY) => p[0] * u[0] + p[1] * u[1], all = ws.flatMap(w => [pr(w.p0), pr(w.p1)]), m0 = Math.min(...all), m1 = Math.max(...all);
  return { o: [u[0] * m0, u[1] * m0], u, Lt: m1 - m0, T: p => pr(p) - m0 };
}
function distributeRun() {
  const ax = runAxis(); if (!ax || runPts.length < 4) return;
  const ws = selWs.map(i => walls[i]), zc = Math.min(...ws.map(w => Math.min(profAt(w.prof, 0), profAt(w.prof, w.L))));
  const H = homography([[0, 0], [ax.Lt, 0], [ax.Lt, zc], [0, zc]], runPts);
  for (const w of ws) { const a = ax.T(w.p0), b = ax.T(w.p1); setFace(w, { ctrl: [0, 0, w.L, zc], quad: ([[a, 0], [b, 0], [b, zc], [a, zc]] as XY[]).map(([T, z]) => applyH(H, T, z)), how: 'manual' }); }
  runPts = []; status(T2(`Fronta rozdělena na ${pl(ws.length, 'stěnu', 'stěny', 'stěn')}; rohy každé lze doladit.`, `Front split into ${ws.length} walls; the corners of each can be refined.`));
}
let drag: number[] | null = null, dragQ: { f: Face; i: number } | null = null, space = false;
const evI = (e: MouseEvent): XY => { const r = ic.getBoundingClientRect(); return [(e.clientX - r.left) * DPR(), (e.clientY - r.top) * DPR()]; };
ic.addEventListener('wheel', e => { e.preventDefault(); const [u, v] = evI(e), [x, y] = S2I(u, v); iv.s = Math.min(Math.max(iv.s * Math.exp(e.deltaY * 0.0015), 0.02), 30); const [x2, y2] = S2I(u, v); iv.cx += x - x2; iv.cy += y - y2; drawImg(); }, { passive: false });
ic.addEventListener('contextmenu', e => e.preventDefault());
function clickImage(x: number, y: number, button = 0) {
  if (!lay || !img) return;
  const tol = 9 * iv.s;
  if (button === 2) {   // right click: remove the nearest camera point / last quad corner
    if (mode === 'cam' && lay.pts) { const j = lay.pts.findIndex(p => Math.hypot(p.uv[0] - x, p.uv[1] - y) < tol * 1.5); if (j >= 0) { lay.pts.splice(j, 1); camAfterPoints(); } }
    else if (runPts.length) runPts.pop();
    else { const f = faceOf(walls[selW]); if (f && !f.copy && !f.src) { f.quad.pop(); if (!f.quad.length) lay.faces = lay.faces.filter(q => q !== f); } }
    dirty = true; changed(); return;
  }
  const [sx, sy] = snap(x, y, 7 * iv.s), pt: XY = [Math.round(sx * 10) / 10, Math.round(sy * 10) / 10];
  if (mode === 'cam') {
    const cs = corners(); if (!cs[selC]) return;
    lay.pts = [...(lay.pts ?? []).filter(p => p.c !== cs[selC].c), { c: cs[selC].c, uv: pt }];
    const done = new Set(lay.pts.map(p => p.c)); const nx = cs.findIndex((c, i) => i > selC && !done.has(c.c)); selC = nx >= 0 ? nx : Math.min(selC + 1, cs.length - 1);
    dirty = true; camAfterPoints(); return;
  }
  if (selWs.length > 1) { if (!runAxis()) return; runPts.push(pt); if (runPts.length === 4) distributeRun(); dirty = true; changed(); return; }
  if (selW < 0) { status(T2('Nejdřív vyberte stěnu.', 'Select a wall first.')); return; }
  const w = walls[selW]; let f = faceOf(w);
  if (!f || f.copy || f.src) { const eave = Math.min(profAt(w.prof, 0), profAt(w.prof, w.L)); f = setFace(w, { ctrl: [0, 0, w.L, eave], quad: [], how: 'manual' })!; }
  if (f.quad.length < 4) { f.quad.push(pt); f.how = 'manual'; dirty = true; changed(); }
}
/** After a change of the camera points: refit and reproject (camera faces only; faces set by hand stay). */
function camAfterPoints() {
  const ok = fitCamera((lay?.pts?.length ?? 0) === 0);
  if (ok || vedOf(lay)) applyCamera(true); else changed();
  if (ok) { const e = [...resid.values()]; status(T2(`Kamera ${CAMNAME()[lay!.camFit!]}: ${pl(e.length, 'bod', 'body', 'bodů')}, odchylka ${camRms!.toFixed(1)} px (max ${Math.max(...e).toFixed(1)})${heightScale()}; promítnuto na ${pl(lay!.faces.filter(f => f.how === 'camera' || f.how === 'veduta').length, 'stěnu', 'stěny', 'stěn')}.`, `Camera ${CAMNAME()[lay!.camFit!]}: ${e.length} points, error ${camRms!.toFixed(1)} px (max ${Math.max(...e).toFixed(1)})${heightScale()}; projected onto ${lay!.faces.filter(f => f.how === 'camera' || f.how === 'veduta').length} walls.`)); }
}
ic.addEventListener('mousedown', e => {
  const [u, v] = evI(e);
  if (e.button === 1 || space || !lay || !img) { drag = [u, v, iv.cx, iv.cy]; return; }
  const [x, y] = S2I(u, v), tol = 9 * iv.s;
  if (e.button === 0) for (const f of lay.faces) if (!f.copy && !f.src) f.quad.forEach((q, i) => { if (!dragQ && Math.hypot(q[0] - x, q[1] - y) < tol && f.quad.length === 4) dragQ = { f, i }; });
  if (dragQ) { selW = walls.findIndex(w => isF(dragQ!.f, w)); selWs = []; refresh(); return; }
  clickImage(x, y, e.button);
});
addEventListener('mousemove', e => {
  if (dragQ) { const [u, v] = evI(e); const [x, y] = S2I(u, v); dragQ.f.quad[dragQ.i] = [Math.round(x * 10) / 10, Math.round(y * 10) / 10]; dirty = true; drawImg(); return; }
  if (!drag) return; const [u, v] = evI(e), k = iv.s / DPR(); iv.cx = drag[2] - (u - drag[0]) * k; iv.cy = drag[3] - (v - drag[1]) * k; drawImg();
});
addEventListener('mouseup', () => {
  if (dragQ) { const q = dragQ.f.quad[dragQ.i]; const s_ = snap(q[0], q[1], 6 * iv.s); dragQ.f.quad[dragQ.i] = [Math.round(s_[0] * 10) / 10, Math.round(s_[1] * 10) / 10]; dragQ.f.how = 'manual'; dragQ = null; changed(); }
  drag = null;
});
addEventListener('keydown', e => {
  const tg = e.target as HTMLElement; if (tg.tagName === 'INPUT' || tg.tagName === 'SELECT') return;
  if (e.code === 'Space') { space = true; e.preventDefault(); }
  if ((e.key === 'Delete' || e.key === 'Backspace') && lay) { const ks = (selWs.length ? selWs : [selW]).map(i => walls[i]).filter(Boolean); lay.faces = lay.faces.filter(f => !ks.some(w => isF(f, w))); dirty = true; changed(); }
  if (e.key === 'Escape') { selWs = []; runPts = []; refresh(); drawImg(); building3d(); }
  if (e.key === 's' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); void save(); }
});
addEventListener('keyup', e => { if (e.code === 'Space') space = false; });
// click in 3D: selects a wall (Shift adds it to a front); Ctrl adds a neighbouring house to the block or removes one
const ray = new THREE.Raycaster(); let down3: XY | null = null;
gl.addEventListener('pointerdown', e => { down3 = [e.clientX, e.clientY]; });
gl.addEventListener('pointerup', e => {
  if (!down3 || Math.hypot(e.clientX - down3[0], e.clientY - down3[1]) > 4 || B < 0) return;
  const r = gl.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1), cam3);
  const hit = ray.intersectObjects([...fGroup.children, ...bGroup.children.filter(o => o.userData.b !== undefined)], false)[0]; if (!hit) return;
  const px = hit.point.x, py = -hit.point.z, hb = hit.object.userData.b as number | undefined;
  if ((e.ctrlKey || e.metaKey) && hb !== undefined) { setMembers(mem.includes(hb) ? mem.filter(b => b !== hb) : [...mem, hb]); return; }
  let best = -1, bd = 1e9;
  walls.forEach((w, i) => { if (hb !== undefined && w.b !== hb) return; const d: XY = [(w.p1[0] - w.p0[0]) / w.L, (w.p1[1] - w.p0[1]) / w.L], t = (px - w.p0[0]) * d[0] + (py - w.p0[1]) * d[1];
    const dist = t < -0.3 || t > w.L + 0.3 ? 1e9 : Math.abs((px - w.p0[0]) * w.out[0] + (py - w.p0[1]) * w.out[1]); if (dist < bd) { bd = dist; best = i; } });
  if (mode === 'cam') { const cs = corners(); let bc = -1, bdc = 1e9; cs.forEach((c, i) => { const d = Math.hypot(c.X[0] - px, c.X[1] - py, c.X[2] - hit.point.y); if (d < bdc) { bdc = d; bc = i; } }); if (bc >= 0 && bdc < 4) selC = bc; }
  if (best >= 0 && bd < 2) {
    if (e.shiftKey) { if (!selWs.length && selW >= 0) selWs = [selW]; selWs = selWs.includes(best) ? selWs.filter(i => i !== best) : [...selWs, best]; runPts = []; }
    else selWs = [];
    selW = best;
  }
  refresh(); drawImg(); building3d();
});

// ---------- panel ----------
function refresh() {
  const ul = $('layers'); ul.innerHTML = '';
  fac.layers.forEach(l => { const li = document.createElement('li'); li.className = l === lay ? 'on' : '';
    li.innerHTML = `<span>${l.label || l.src.split('/').pop()}</span><span>${l.year ?? ''} · ${l.faces.length} ${T2('st.', 'w.')}${l.roof || (l === lay && roofInfo) ? T2(' + střechy', ' + roofs') : ''}</span>`;
    li.onclick = () => void openLayer(l); ul.appendChild(li); });
  $('blk').textContent = mem.length ? T2(`blok: ${mem.length} ${mem.length === 1 ? 'dům' : mem.length < 5 ? 'domy' : 'domů'}, ${walls.length} vnějších stěn`, `block: ${mem.length} house${mem.length === 1 ? '' : 's'}, ${walls.length} outer walls`) : '';
  $('layEdit').hidden = !lay;
  if (lay) {
    inp('lLabel').value = lay.label ?? ''; ($('lKind') as HTMLSelectElement).value = lay.kind; inp('lYear').value = lay.year?.toString() ?? '';
    inp('lV0').value = String(lay.valid[0]); inp('lV1').value = lay.valid[1] >= 9999 ? '' : String(lay.valid[1]); inp('lV1').placeholder = T2('dodnes', 'today');
    ($('camKind') as HTMLSelectElement).value = lay.camKind ?? 'auto'; inp('roofOn').checked = !lay.noRoof;
  }
  document.querySelectorAll<HTMLButtonElement>('[data-mode]').forEach(b => b.classList.toggle('on', b.dataset.mode === mode));
  $('camBox').hidden = mode !== 'cam';
  $('modeHint').textContent = !lay ? '' : vedOf(lay) && mode === 'quad' ? T2('Veduta má kameru: v režimu „kamera“ ji 1–3 kliky na rohy bloku místně doladí; projekce na stěny i střechy je pak automatická.', 'The veduta has a camera: in the "camera" mode 1–3 clicks on corners of the block refine it locally; walls and roofs are then projected automatically.')
    : mode === 'quad' ? T2('Pro každou viditelnou stěnu klikněte 4 rohy (zleva dole, proti směru hodinek při pohledu zvenku). Shift + klik ve 3D vybere víc stěn jedné fronty – pak stačí 4 rohy celé fronty. Pravý klik vrátí poslední bod.', 'For each visible wall click its 4 corners (from the bottom left, anticlockwise seen from outside). Shift + click in 3D selects several walls of one front – then 4 corners of the whole front are enough. Right click undoes the last point.')
      : vedOf(lay) ? T2('Klikejte rohy bloku podle popisků ve 3D: body u země (↓) opraví půdorys – 1 posun, 2 i měřítko a otočení, 3 a víc afinně; body nahoře (↑, S) měřítko výšek (kreslíři je přehánějí). Od 6 bodů ve dvou výškách se zkusí i afinní kamera.', 'Click corners of the block as labelled in 3D: points at the ground (↓) correct the plan – 1 shift, 2 also scale and rotation, 3 and more affine; points at the top (↑, S) the scale of the heights (draughtsmen exaggerate them). From 6 points at two heights an affine camera is tried as well.')
        : T2('Klikejte rohy bloku podle popisků ve 3D (klik ve 3D vybere bod). Kresba: aspoň 4 body ve dvou výškách (afinní kamera); fotka: aspoň 6 (perspektivní).', 'Click corners of the block as labelled in 3D (click in 3D selects a point). Drawing: at least 4 points at two heights (affine camera); photo: at least 6 (perspective).');
  const cl = $('corners'); cl.innerHTML = '';
  if (mode === 'cam' && lay) { const done = new Set((lay.pts ?? []).map(p => p.c)); corners().forEach((c, i) => { const li = document.createElement('li'); li.className = i === selC ? 'on' : ''; const e = resid.get(c.c);
    li.innerHTML = `<span>${c.c}</span><span class="${done.has(c.c) ? 'ok' : ''}">${done.has(c.c) ? '✓' + (e != null ? ' ' + e.toFixed(1) + ' px' : '') : ''} ${(c.X[2] - M.z[B]).toFixed(1)} m</span>`; li.onclick = () => { selC = i; refresh(); drawImg(); }; cl.appendChild(li); }); }
  const wl = $('walls'); wl.innerHTML = '';
  walls.forEach((w, i) => { const f = faceOf(w); const li = document.createElement('li'); li.className = i === selW || selWs.includes(i) ? 'on' : '';
    const st = !f ? (hid.has(wkey(w)) ? `<span class="hint">${T2('nevidí', 'unseen')}</span>` : '') : f.copy ? `<span class="ok">${T2('kopie', 'copy')} ${walls.find(x => x.bid === f.copy!.b && x.k === f.copy!.wall)?.letter ?? ''}${f.copy.wall + 1}</span>` : f.src ? `<span class="ok">${T2('soubor', 'file')}</span>` : `<span class="ok">${f.quad.length === 4 ? '✓' + (f.seen != null && f.seen < 0.95 ? ` ${Math.round(f.seen * 100)} %` : '') : f.quad.length + '/4'}</span>`;
    li.innerHTML = `<span>${w.letter}${w.k + 1}</span><span>${w.openL.toFixed(1)} m ${st}</span>`;
    li.onclick = ev => { if (ev.shiftKey) { if (!selWs.length && selW >= 0) selWs = [selW]; selWs = selWs.includes(i) ? selWs.filter(x => x !== i) : [...selWs, i]; runPts = []; } else selWs = []; selW = i; refresh(); drawImg(); building3d(); };
    wl.appendChild(li); });
  const f = lay && selW >= 0 ? faceOf(walls[selW]) : undefined;
  $('wallEdit').hidden = !(lay && selW >= 0);
  $('ctrlBox').hidden = !f;
  if (f) { inp('c0').value = String(+f.ctrl[0].toFixed(2)); inp('c1').value = String(+f.ctrl[2].toFixed(2)); inp('z0').value = String(+f.ctrl[1].toFixed(2)); inp('z1').value = String(+f.ctrl[3].toFixed(2)); }
  const pc = (v?: number) => Math.round((v ?? 0) * 100);
  $('roofStat').textContent = roofInfo ? T2(`střechy: z obrázku ${pc(roofInfo.seen)} %, zrcadleno ${pc(roofInfo.mirrored)} %, doplněno ${pc(roofInfo.filled)} %, ${roofInfo.px?.join(' × ')} px`, `roofs: from the image ${pc(roofInfo.seen)} %, mirrored ${pc(roofInfo.mirrored)} %, filled ${pc(roofInfo.filled)} %, ${roofInfo.px?.join(' × ')} px`) : '';
}
for (const [id, i] of [['c0', 0], ['z0', 1], ['c1', 2], ['z1', 3]] as const) inp(id).onchange = () => { const f = faceOf(walls[selW]); if (!f) return; f.ctrl[i] = +inp(id).value; dirty = true; changed(); };
document.querySelectorAll<HTMLButtonElement>('[data-mode]').forEach(b => b.onclick = () => { mode = b.dataset.mode as 'quad' | 'cam'; runPts = []; refresh(); drawImg(); });
inp('lLabel').oninput = () => { if (lay) { lay.label = inp('lLabel').value || undefined; dirty = true; } };
$('lKind').onchange = () => { if (lay) { lay.kind = ($('lKind') as HTMLSelectElement).value as Layer['kind']; dirty = true; refresh(); } };
inp('lYear').onchange = () => { if (!lay) return; lay.year = inp('lYear').value === '' ? undefined : +inp('lYear').value; lay.valid = blockPeriod(yearOf()); dirty = true; loadWalls(); changed(); };
inp('lV0').onchange = inp('lV1').onchange = () => { if (!lay) return; lay.valid = [+inp('lV0').value || M.from[B], inp('lV1').value === '' ? 9999 : +inp('lV1').value]; dirty = true; };
($('camKind') as HTMLSelectElement).onchange = () => { if (!lay) return; const v = ($('camKind') as HTMLSelectElement).value as Layer['camKind']; lay.camKind = v === 'auto' ? undefined : v; camAfterPoints(); };
inp('roofOn').onchange = () => { if (lay) { lay.noRoof = !inp('roofOn').checked || undefined; dirty = true; faces3d(); } };
inp('ovl').onchange = () => drawImg();
$('camFit').onclick = () => camAfterPoints(); $('camApply').onclick = () => applyCamera();
$('faceDel').onclick = () => { if (lay && selW >= 0) { lay.faces = lay.faces.filter(f => !isF(f, walls[selW])); dirty = true; changed(); } };
/** Best source for a wall not seen in the image: the opposite wall of the same house, else of the block, of similar length. */
function oppositeOf(w: BW): Face | undefined {
  if (!lay) return;
  let best: Face | undefined, bs = 1e9;
  for (const g of lay.faces) {
    if (g.copy || (g.quad.length < 4 && !g.src) || isF(g, w)) continue;
    const dot = g.out[0] * w.out[0] + g.out[1] * w.out[1], dl = Math.abs(lenOf(g) - w.L) / w.L;
    const s = (fb(g) === w.bid ? 0 : 2) + (dot < -0.7 ? 0 : dot < 0.3 ? 1 : 1.5) + dl + (1 - (g.seen ?? 1));
    if (s < bs) { bs = s; best = g; }
  }
  return best;
}
function copyInto(w: BW, g: Face) { const f = setFace(w, { ctrl: [0, 0, w.L, zmaxOf(w)], quad: [], how: 'copy' }); if (f) f.copy = { b: fb(g), wall: g.wall }; }
$('copyOpp').onclick = () => { const w = walls[selW]; if (!w || !lay) return; const g = oppositeOf(w); if (!g) { status(T2('Ve vrstvě zatím není žádná stěna s texturou.', 'The layer has no textured wall yet.')); return; } copyInto(w, g); changed(); };
$('fillHidden').onclick = () => {
  if (!lay) return; let n = 0;
  for (const w of walls) { if (faceOf(w)) continue; const g = oppositeOf(w); if (g) { copyInto(w, g); n++; } }
  status(T2(`Doplněno: ${pl(n, 'kopie stěny', 'kopie stěn', 'kopií stěn')} (označeny „kopie“; zdroj lze změnit tlačítkem u stěny).`, `Filled ${n} walls with copies (marked "copy").`)); changed();
};
$('fileTex').onclick = () => { if (selW < 0 || !lay) return; inp('wfile').click(); };
inp('wfile').onchange = async () => {
  const file = inp('wfile').files?.[0], w = walls[selW]; if (!file || !w || !lay) return;
  const src = await upload(file); inp('wfile').value = ''; if (!src) return;
  const P = await loadPix(src); if (!P) return;
  const W = P.img.width, H = P.img.height, f = setFace(w, { ctrl: [0, 0, w.L, zmaxOf(w)], quad: [[0, H], [W, H], [W, 0], [0, 0]], how: 'file' });
  if (f) f.src = src;
  status(T2('Textura ze souboru pokrývá celou stěnu (od země po vrchol); rozsah obrázku na stěně upravte čísly „body“.', 'The texture from the file covers the whole wall (ground to top); adjust its extent on the wall with the "points" numbers.')); changed();
};
function changed() { refresh(); drawImg(); faces3d(); }
function loadWalls() {
  walls = []; cornerCache = null; dmCache = null; hid.clear();
  if (mem.length) {
    const y = yearOf(), [x0, y0, x1, y1] = blockBox(3), nb = near(IX, M.n, x0, y0, x1, y1, b => standing(b) || mem.includes(b));
    mem.forEach((b, i) => {
      const others = nb.filter(c => c !== b).map(c => IX.ring(c));
      for (const w of wallsOf(M, b, y, meshOf.get(b))) {
        const open = openParts(w, others), openL = open.reduce((s, q) => s + q[1] - q[0], 0);
        if (openL >= 1) walls.push({ ...w, b, bid: M.ids[b], letter: letter(i), open, openL });
      }
    });
  }
  if (selW >= walls.length) selW = -1; selWs = selWs.filter(i => i < walls.length);
  building3d();
}
/** Period in which every house of the block keeps its state (intersection of their periods around year y). */
function blockPeriod(y: number): [number, number] {
  let a = -1e9, e = 1e9; for (const b of mem) { const [p, q] = statePeriod(M, b, y); a = Math.max(a, p); e = Math.min(e, q); }
  return [Math.round(a * 10) / 10, e >= 9999 ? 9999 : Math.round(e * 10) / 10];
}
function setMembers(m: number[]) {
  if (!m.length) return;
  mem = [...new Set(m)]; if (!mem.includes(B)) { B = mem[0]; BID = M.ids[B]; }
  dirty = true; selW = -1; selWs = []; runPts = [];
  loadWalls(); focus3d();
  if (lay) { if (lay.pts?.length) fitCamera(true); if (camOf()) applyCamera(true); }
  changed();
}
/** Houses that join a block automatically: not the walls, towers, earthworks, water or the churches. */
const NOJOIN = () => new Set(['fort', 'moat', 'ditch', 'landmark', 'water'].map(c => M.classes.indexOf(c)).filter(i => i >= 0));
const autoBlock = (b: number) => { const nj = NOJOIN(); return blockOf(M, IX, b, c => standing(c) && (c === b || !nj.has(M.cls[c])), 3.0); };   // 3 m: across vacant gaps of a block, not across a street
$('blkAll').onclick = () => { if (B >= 0) setMembers(autoBlock(B)); };
$('blkOne').onclick = () => { if (B >= 0) setMembers([B]); };

// ---------- sources ----------
async function openLayer(l: Layer) {
  lay = l; camRms = null; resid.clear(); dmCache = null; roofInfo = null;
  const P = await loadPix(l.src); img = P?.img ?? null;
  if (img) iv = { cx: img.width / 2, cy: img.height / 2, s: Math.max(img.width / ic.clientWidth, img.height / ic.clientHeight) * 1.02 };
  else status(T2('Obrázek se nepodařilo načíst: ', 'Could not load the image: ') + srcURL(l.src));
  if (l.kind === 'veduta' || l.pts?.length) mode = 'cam';
  loadWalls();
  if (l.pts?.length) fitCamera(true);
  if (camOf()) {   // walls the camera does not see (for the list)
    const cam = camOf()!, dm = depth();
    for (const w of walls) if (!faceOf(w)) { const tv = cam.toViewer(wallPt(w, w.L / 2, 1, M.z[w.b])); if (tv[0] * w.out[0] + tv[1] * w.out[1] <= 0 || (dm && seenShare(w, cam, dm) < 0.15)) hid.add(wkey(w)); }
    zoomToBlock();
  }
  changed();
}
function zoomToBlock() {   // image view on the projected block
  const cam = camOf(); if (!cam || !img || !mem.length) return;
  const [x0, y0, x1, y1] = blockBox(4), z = M.z[B], pts = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]].flatMap(([x, y]) => [cam.P([x, y, z]), cam.P([x, y, z + 15])]).filter(Boolean) as XY[];
  if (pts.length < 2) return;
  const u0 = Math.min(...pts.map(p => p[0])), u1 = Math.max(...pts.map(p => p[0])), v0 = Math.min(...pts.map(p => p[1])), v1 = Math.max(...pts.map(p => p[1]));
  iv = { cx: (u0 + u1) / 2, cy: (v0 + v1) / 2, s: Math.max((u1 - u0) / ic.clientWidth, (v1 - v0) / ic.clientHeight) * 1.6 };
}
async function upload(file: File): Promise<string | null> {
  const buf = await file.arrayBuffer(), hash = [...new Uint8Array(await crypto.subtle.digest('SHA-1', buf))].slice(0, 6).map(b => b.toString(16).padStart(2, '0')).join('');
  const ext = (file.name.split('.').pop() ?? 'jpg').toLowerCase().replace('jpeg', 'jpg'), name = `src_${hash}.${['jpg', 'png', 'webp'].includes(ext) ? ext : 'jpg'}`;
  const url = await new Promise<string>(res => { const r = new FileReader(); r.onload = () => res(r.result as string); r.readAsDataURL(file); });
  const r = await fetch(`/api/facade/src/${name}`, { method: 'POST', body: url }).catch(() => null);
  if (!r?.ok) { status(T2('Nahrání obrázku selhalo.', 'Uploading the image failed.')); return null; }
  return 'src/' + name;
}
inp('file').onchange = async () => {
  const f = inp('file').files?.[0]; if (!f || B < 0) return;
  const src = await upload(f); inp('file').value = ''; if (!src) return;
  const l: Layer = { id: 'L' + Date.now().toString(36), src, kind: 'photo', label: f.name.replace(/\.[^.]+$/, ''), year: undefined, valid: blockPeriod(yearOf()), faces: [] };
  fac.layers.push(l); dirty = true; mode = 'quad'; await openLayer(l);
  status(T2('Doplňte rok snímku (určí výšku domů a platnost textur) a druh (kresba → afinní kamera).', 'Fill in the year of the image (sets the height of the houses and the validity of the textures) and the kind (drawing → affine camera).'));
};
$('addFile').onclick = () => { if (B < 0) { status(T2('Nejdřív načtěte budovu.', 'Load a building first.')); return; } inp('file').click(); };
async function addVeduta(id: string) {
  const v = VED.find(q => q.id === id); if (!v || B < 0) return;
  const y = v.year ?? yearOf();
  let l = fac.layers.find(q => q.src === 'veduta:' + id);
  if (!l) { l = { id: 'L' + Date.now().toString(36), src: 'veduta:' + id, kind: 'veduta', label: v.label.slice(0, 60), year: y, valid: [0, 0], faces: [] }; fac.layers.push(l); dirty = true; }
  lay = l; loadWalls(); if (!l.faces.length) l.valid = blockPeriod(y);
  await openLayer(l); applyCamera();
}
($('vedSel') as HTMLSelectElement).onchange = async () => { const s = $('vedSel') as HTMLSelectElement, id = s.value; s.value = ''; if (id) await addVeduta(id); };

// ---------- saving ----------
async function save() {
  if (B < 0) return;
  status(T2('Narovnávám textury…', 'Rectifying the textures…'));
  try {
    const safe = KEY.replace(/[^a-z0-9]+/gi, '-'), ids = new Set(mem.map(b => M.ids[b])), cur = lay;
    for (const l of fac.layers) {
      if (l !== lay) await openLayer(l);   // the source pixels and the camera of each layer
      await Promise.all(l.faces.filter(f => f.src).map(f => loadPix(f.src!)));
      l.faces = l.faces.filter(f => ids.has(fb(f)) && (f.quad.length === 4 || f.copy));
      l.faces = l.faces.filter(f => !f.copy || sourceOf(f));
      for (const f of l.faces) {
        f.b = fb(f);
        const cv = rectify(f, 80); if (!cv) continue;
        f.tex = `${safe}_${l.id}_${f.b.replace(/[^a-z0-9]+/gi, '-')}_w${f.wall}.webp`; f.px = [cv.width, cv.height];
        const r = await fetch(`/api/facade/tex/${f.tex}`, { method: 'POST', body: cv.toDataURL('image/webp', 0.9) }); if (!r.ok) throw new Error('tex ' + r.status);
      }
      l.roof = undefined;
      if (!l.noRoof && camOf()) {
        const rr = rectifyRoof(60);
        if (rr) { rr.roof.tex = `${safe}_${l.id}_roof.webp`; const r = await fetch(`/api/facade/tex/${rr.roof.tex}`, { method: 'POST', body: rr.cv.toDataURL('image/webp', 0.9) }); if (!r.ok) throw new Error('roof ' + r.status); l.roof = rr.roof; }
      }
    }
    if (cur && cur !== lay) await openLayer(cur);
    const all: FacFile = (await getJSON<FacFile>('/manual/facades.json')) ?? {};
    all.blocks = all.blocks ?? {};
    const layers = fac.layers.filter(l => l.faces.length || l.pts?.length || l.roof);
    if (layers.length) all.blocks[KEY] = { members: mem.map(b => M.ids[b]), layers, edited: new Date().toISOString().slice(0, 10) }; else delete all.blocks[KEY];
    all.format = 2;
    all.note = 'facade textures of the growth model (facade.html): per block (key = its first house; members = building ids) layers of source images with the rectified wall textures (faces, b = building) and the roof texture of the block (images in data/historic/growth/facades/, not versioned)';
    const r = await fetch('/api/manual/facades.json', { method: 'POST', body: JSON.stringify(all, null, 1) }); if (!r.ok) throw new Error(String(r.status));
    dirty = false; const n = layers.reduce((s, l) => s + l.faces.length, 0), nr = layers.filter(l => l.roof).length;
    status(T2(`Uloženo: ${pl(n, 'textura stěny', 'textury stěn', 'textur stěn')}, ${pl(nr, 'textura střech', 'textury střech', 'textur střech')}. Ve 3D modelu (vývojový režim) se ukážou po obnovení stránky, do publikovaného modelu po generování.`, `Saved: ${n} wall textures, ${nr} roof textures. They show in the 3D model (dev) after a reload, in the published model after the next generation.`));
    faces3d();
  } catch (e) { status('ERROR ' + (e as Error).message); }
}
$('save').onclick = () => void save();
addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });

// ---------- loading ----------
async function loadBuilding(id: string, opts: { block?: boolean; ved?: string } = {}) {
  if (dirty && !confirm(T2('Neuložené změny se zahodí. Pokračovat?', 'Unsaved changes will be lost. Continue?'))) return;
  const b = idIdx.get(id.trim());
  if (b === undefined) { status(T2('Budova s tímto id v modelu není.', 'No building with this id in the model.')); return; }
  B = b; BID = M.ids[b]; inp('bid').value = BID; dirty = false; lay = null; img = null; selW = -1; selWs = []; runPts = []; selC = 0; roofInfo = null;
  const all = await getJSON<FacFile>('/manual/facades.json'), blocks = all?.blocks ?? {};
  for (const [k, v] of Object.entries(all?.buildings ?? {})) if (!blocks[k]) blocks[k] = { members: [k], ...v };   // first format: one building
  KEY = blocks[BID] ? BID : Object.keys(blocks).find(k => blocks[k].members?.includes(BID)) ?? BID;
  fac = JSON.parse(JSON.stringify(blocks[KEY] ?? { members: [BID], layers: [] }));
  mem = (fac.members ?? [KEY]).map(i => idIdx.get(i)).filter((v): v is number => v !== undefined); if (!mem.length) mem = [B];
  if (opts.block && !blocks[KEY]) mem = autoBlock(B);
  const y = yearOf();
  $('binfo').textContent = `${M.classes[M.cls[b]]} · ${Math.round(M.from[b])}${M.to[b] < 9999 ? '–' + Math.round(M.to[b]) : ''} · ${T2('výška', 'height')} ${heightAt(M, b, y).toFixed(1)} m (${Math.round(y)})`;
  history.replaceState(null, '', `?id=${encodeURIComponent(BID)}&year=${Math.round(y)}`);
  loadWalls(); focus3d(); fGroup.clear();
  if (opts.ved) await addVeduta(opts.ved);
  else if (fac.layers.length) await openLayer(fac.layers[0]); else changed();
}
$('load').onclick = () => void loadBuilding(inp('bid').value);
inp('bid').onkeydown = e => { if (e.key === 'Enter') void loadBuilding(inp('bid').value); };

(async () => {
  sizeImg(); size3d();
  status(T2('Načítám model…', 'Loading the model…'));
  const DATA = '/data/historic/growth/web/';
  M = (await getJSON<M_>(DATA + 'model.json'))!;
  M.ids.forEach((id, b) => idIdx.set(id, b)); IX = footIndex(M);
  if (M.mesh) {
    const parts = await Promise.all((M.mesh.files ?? [M.mesh.file]).map(async f => new Uint8Array(await (await fetch(DATA + f)).arrayBuffer())));
    const all = new Uint8Array(parts.reduce((s, q) => s + q.length, 0)); { let o = 0; for (const q of parts) { all.set(q, o); o += q.length; } }
    const buf = all.buffer, [nb, nvm, ntm] = new Int32Array(buf, 0, 4);
    const bl = new Int32Array(buf, 16, nb), vc = new Int32Array(buf, 16 + 4 * nb, nb), tc = new Int32Array(buf, 16 + 8 * nb, nb);
    const V = new Float32Array(buf, 16 + 12 * nb, nvm * 3), T = new Uint16Array(buf, 16 + 12 * nb + 12 * nvm, ntm * 3);
    let vo = 0, to = 0; for (let i = 0; i < nb; i++) { meshOf.set(bl[i], { v: V.subarray(3 * vo, 3 * (vo + vc[i])), t: T.subarray(3 * to, 3 * (to + tc[i])) }); vo += vc[i]; to += tc[i]; }
  }
  VIEWS = await getJSON('/appdata/veduta_views.json');
  const idx = await getJSON<{ vedute: { id: string; label: string; url: string; year: number | null }[] }>('/manual/maps.json');
  VED = (idx?.vedute ?? []).filter(v => VIEWS?.views[v.id]).map(v => ({ ...v, url: '/data/historic' + v.url }));
  for (const v of VED) ($('vedSel') as HTMLSelectElement).add(new Option(`${v.year ?? ''} · ${v.label.slice(0, 50)}`, v.id));
  status('');
  const q = new URLSearchParams(location.search), id = q.get('id');
  if (id) await loadBuilding(id, { block: q.get('block') === '1', ved: q.get('ved') ?? undefined }); else drawImg();
})();

// debug handle (dev)
(window as any).__fac = {
  get lay() { return lay; }, get walls() { return walls; }, get mem() { return mem.map(b => M.ids[b]); }, corners, rectify, rectifyRoof, save, loadBuilding, setMembers: (ids: string[]) => setMembers(ids.map(i => idIdx.get(i)!).filter(v => v !== undefined)),
  get B() { return B; }, fitCamera, applyCamera, clickImage, camOf, depth, get resid() { return Object.fromEntries(resid); }, get camRms() { return camRms; }, get hid() { return [...hid]; },
  addLayer: async (src: string, year: number, kind: Layer['kind'] = 'photo') => { const l: Layer = { id: 'L' + Date.now().toString(36), src, kind, label: src.split('/').pop(), year, valid: blockPeriod(year), faces: [] }; fac.layers.push(l); dirty = true; await openLayer(l); return l; },
  selC: (i: number) => { selC = i; refresh(); }, setMode: (m: 'quad' | 'cam') => { mode = m; refresh(); drawImg(); }, view: (x: number, y: number, sc: number) => { iv = { cx: x, cy: y, s: sc }; drawImg(); },
  select: (is: number[]) => { selWs = is.length > 1 ? is : []; selW = is[is.length - 1] ?? -1; runPts = []; refresh(); drawImg(); building3d(); }, fill: () => $('fillHidden').click(),
  shot: () => [ic.toDataURL('image/jpeg', 0.9), (renderer.render(scene, cam3), gl.toDataURL('image/jpeg', 0.9))],
  cam3: (x: number, y: number, z: number, tx: number, ty: number, tz: number) => { cam3.position.set(x, y, z); ctl.target.set(tx, ty, tz); },
};
