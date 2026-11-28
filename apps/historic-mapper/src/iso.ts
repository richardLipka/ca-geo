// Houses from the vedute: click footprint corners, wall tops (eaves) and roof ridge points of a house on a bird's-eye
// view or panorama; with the camera of the veduta (scripts/veduta_views.json, estimated by veduta_views.py) the house
// is reconstructed as a right-angled building (footprint back-projected onto the ground, heights from the clicks on
// vertical lines) and shown in 3D with the drawing projected onto its walls and roof.
// Saved: manual/veduta_<id>.json (the clicks, as the editor) and manual/veduta_buildings.json (the reconstruction,
// read by growth_model.py).
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

type XY = [number, number];
type V3 = [number, number, number];
interface Pts { foot: XY[]; eave: XY[]; ridge: XY[] }
interface House { name?: string; from?: number; to?: number; roof?: string; pts: Pts }
interface View { pos: V3; quat: [number, number, number, number]; fov: number; aspect: number; size: [number, number]; stretch: number; year: number; rms_pct: number; how: string }
interface Recon { q: XY[]; eave: number; ridge: number; width: number; len: number; rmsEave: number }

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const EN: Record<string, string> = {
  title: 'Houses from the vedute', back: '← footprint review', houses: 'Houses', new: '+ new house', del: 'delete', roof: 'roof', gable: 'gable', hip: 'hipped', shed: 'shed', flat: 'flat',
  from: 'from', to: 'to', points: 'Points', foot: '1 footprint', eave: '2 wall / eave', ridge: '3 roof / ridge',
  help: '1 – corners where the walls stand on the ground (3 corners are enough, the house is completed to a right angle). 2 – top edge of the wall above a corner. 3 – ends of the ridge (shed roof: its high edge; tower: the apex). Right click removes the nearest point. Wheel = zoom, middle button / space = pan.',
  view3d: '3D', ctx: 'model buildings around', drafts: "draughtsman's view with the veduta", ovop: 'veduta opacity', save: 'Save (points and reconstruction)', capImg: 'Veduta: click the points', cap3d: 'Reconstruction textured from the veduta',
};
let lang: 'cs' | 'en' = 'cs';
const CS: Record<string, string> = {}; document.querySelectorAll<HTMLElement>('[data-t]').forEach(e => CS[e.dataset.t!] = e.textContent ?? '');
const T2 = (cs: string, en: string) => (lang === 'cs' ? cs : en);
$('lang').onclick = () => { lang = lang === 'cs' ? 'en' : 'cs'; document.querySelectorAll<HTMLElement>('[data-t]').forEach(e => e.textContent = (lang === 'en' ? EN[e.dataset.t!] : CS[e.dataset.t!]) ?? e.textContent); $('lang').textContent = lang === 'cs' ? 'EN' : 'CS'; refresh(); };

async function getJSON<T>(u: string): Promise<T | null> { try { const r = await fetch(u, { cache: 'no-store' }); return r.ok ? await r.json() as T : null; } catch { return null; } }
const status = (t: string) => { $('status').textContent = t; };

// ---------- data ----------
let VIEWS: { origin: XY; ground: number; views: Record<string, View> };
let VED: { id: string; label: string; url: string; year: number | null }[] = [];
let MODEL: any = null;
let sid = '', V: View | null = null, img: HTMLImageElement | null = null, tex: THREE.Texture | null = null;
let houses: House[] = [], selH = -1, ptType: keyof Pts = 'foot', dirty = false;

// ---------- camera of the veduta ----------
const camQ = () => new THREE.Quaternion(...V!.quat);
function project(X: THREE.Vector3): XY | null {
  const [W, H] = V!.size, f = H / 2 / Math.tan(V!.fov * Math.PI / 360), fx = f * (V!.stretch || 1);
  const pc = X.clone().sub(new THREE.Vector3(...V!.pos)).applyQuaternion(camQ().invert());
  if (pc.z > -1) return null;
  return [W / 2 + fx * pc.x / -pc.z, H / 2 - f * pc.y / -pc.z];
}
function ground(u: number, v: number): THREE.Vector3 | null {
  const [W, H] = V!.size, f = H / 2 / Math.tan(V!.fov * Math.PI / 360), fx = f * (V!.stretch || 1);
  const d = new THREE.Vector3((u - W / 2) / fx, -(v - H / 2) / f, -1).applyQuaternion(camQ());
  const C = new THREE.Vector3(...V!.pos); if (Math.abs(d.y) < 1e-9) return null;
  const t = (VIEWS.ground - C.y) / d.y; return t > 0 ? C.add(d.multiplyScalar(t)) : null;
}
// three.js world (x east, y up, z south, relative to the model origin) ↔ S-JTSK
const toW = (x: number, y: number, h = 0) => new THREE.Vector3(x - VIEWS.origin[0], VIEWS.ground + h, -(y - VIEWS.origin[1]));
const fromW = (p: THREE.Vector3): XY => [p.x + VIEWS.origin[0], -p.z + VIEWS.origin[1]];
const dist = (a: XY, b: XY) => Math.hypot(a[0] - b[0], a[1] - b[1]);

// ---------- reconstruction ----------
function minRect(pts: XY[]): XY[] {   // minimum-area rectangle of the convex hull
  const P = [...pts].sort((a, b) => a[0] - b[0] || a[1] - b[1]); const cr = (o: XY, a: XY, b: XY) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo: XY[] = [], up: XY[] = [];
  for (const p of P) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
  for (const p of [...P].reverse()) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
  const hull = lo.slice(0, -1).concat(up.slice(0, -1)); let best: XY[] = [], ba = 1e18;
  for (let i = 0; i < hull.length; i++) {
    const a = hull[i], b = hull[(i + 1) % hull.length], L = dist(a, b) || 1, ux = (b[0] - a[0]) / L, uy = (b[1] - a[1]) / L;
    let mn = 1e18, mx = -1e18, mn2 = 1e18, mx2 = -1e18;
    for (const p of hull) { const s = p[0] * ux + p[1] * uy, t = -p[0] * uy + p[1] * ux; mn = Math.min(mn, s); mx = Math.max(mx, s); mn2 = Math.min(mn2, t); mx2 = Math.max(mx2, t); }
    const A = (mx - mn) * (mx2 - mn2);
    if (A < ba) { ba = A; best = [[mn, mn2], [mx, mn2], [mx, mx2], [mn, mx2]].map(([s, t]) => [s * ux - t * uy, s * uy + t * ux] as XY); }
  }
  return best;
}
function recon(h: House): Recon | null {
  if (!V || h.pts.foot.length < 3) return null;
  const g = h.pts.foot.map(([u, v]) => ground(u, v)); if (g.some(p => !p)) return null;
  const xy = g.map(p => fromW(p!));
  let rect: XY[];
  if (xy.length === 3) { const [a, b, c] = xy; rect = [a, b, c, [a[0] + c[0] - b[0], a[1] + c[1] - b[1]]]; rect = minRect(rect); }   // three corners: b is the shared one
  else rect = minRect(xy);
  const e = [0, 1, 2, 3].map(i => ({ i, L: dist(rect[i], rect[(i + 1) % 4]) })).sort((a, b) => a.L - b.L);
  const i0 = e[0].i, q = [0, 1, 2, 3].map(k => rect[(i0 + k) % 4]);   // q0–q1 a short side
  const width = e[0].L, len = e[3].L; if (width * len < 6) return null;
  // eave: the vertical line through the best corner (≥ 2 m)
  const pix = (x: number, y: number, hh: number) => project(toW(x, y, hh));
  const fitLine = (c: XY, click: XY, lo: number, hi: number) => {
    let bh = lo, bd = 1e18;
    for (let hh = lo; hh <= hi; hh += 0.25) { const p = pix(c[0], c[1], hh); if (!p) continue; const d = dist(p, click); if (d < bd) { bd = d; bh = hh; } }
    for (let hh = bh - 0.25; hh <= bh + 0.25; hh += 0.01) { const p = pix(c[0], c[1], hh); if (!p) continue; const d = dist(p, click); if (d < bd) { bd = d; bh = hh; } }
    return { h: bh, d: bd };
  };
  const hs: number[] = [], ds: number[] = [];
  for (const c of h.pts.eave) { const best = q.map(k => fitLine(k, c, 2, 90)).sort((a, b) => a.d - b.d)[0]; hs.push(best.h); ds.push(best.d); }
  const med = (a: number[]) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
  const eave = hs.length ? med(hs) : 7;
  // ridge: position along the long axis and height
  const a0: XY = [(q[0][0] + q[1][0]) / 2, (q[0][1] + q[1][1]) / 2], a1: XY = [(q[2][0] + q[3][0]) / 2, (q[2][1] + q[3][1]) / 2];
  const rs: number[] = [];
  for (const c of h.pts.ridge) {
    let bt = 0.5, bh = eave + 3, bd = 1e18;
    for (let t = -0.1; t <= 1.1; t += 0.02) for (let hh = eave; hh <= eave + 80; hh += 0.25) {
      const p = pix(a0[0] + t * (a1[0] - a0[0]), a0[1] + t * (a1[1] - a0[1]), hh); if (!p) continue; const d = dist(p, c); if (d < bd) { bd = d; bt = t; bh = hh; } }
    for (let hh = bh - 0.25; hh <= bh + 0.25; hh += 0.02) { const p = pix(a0[0] + bt * (a1[0] - a0[0]), a0[1] + bt * (a1[1] - a0[1]), hh); if (!p) continue; const d = dist(p, c); if (d < bd) { bd = d; bh = hh; } }
    rs.push(bh);
  }
  const kind = h.roof ?? 'gable';
  let ridge = rs.length ? med(rs) : (kind === 'flat' ? eave : eave + 0.6 * width);
  if (kind === 'flat') ridge = eave; else ridge = Math.max(ridge, eave + 0.5);
  return { q, eave, ridge, width, len, rmsEave: ds.length ? Math.sqrt(ds.reduce((s, d) => s + d * d, 0) / ds.length) : 0 };
}
// the house mesh as in scripts/fabric.py roof_house: vertices (x, y, z above the ground) and triangles
function houseMesh(r: Recon, kind: string): { v: V3[]; t: number[][] } {
  const p = r.q, e = r.eave, rf = r.ridge - r.eave;
  const v: V3[] = [...p.map(([x, y]) => [x, y, 0] as V3), ...p.map(([x, y]) => [x, y, e] as V3)];
  const t: number[][] = []; for (let i = 0; i < 4; i++) { const j = (i + 1) % 4; t.push([i, j, 4 + j], [i, 4 + j, 4 + i]); }
  const m0: XY = [(p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2], m1: XY = [(p[2][0] + p[3][0]) / 2, (p[2][1] + p[3][1]) / 2];
  if (kind === 'flat' || rf <= 0.05) { t.push([4, 5, 6], [4, 6, 7]); return { v, t }; }
  if (kind === 'shed') { v.push([p[1][0], p[1][1], e + rf], [p[2][0], p[2][1], e + rf]); t.push([4, 8, 9], [4, 9, 7], [5, 8, 4], [6, 7, 9], [5, 6, 9], [5, 9, 8]); return { v, t }; }
  if (kind === 'hip') { const k = Math.min(0.5 * r.width / Math.max(r.len, 1e-6), 0.5);
    v.push([m0[0] + (m1[0] - m0[0]) * k, m0[1] + (m1[1] - m0[1]) * k, e + rf], [m1[0] + (m0[0] - m1[0]) * k, m1[1] + (m0[1] - m1[1]) * k, e + rf]);
    t.push([4, 5, 8], [5, 6, 9], [5, 9, 8], [6, 7, 9], [7, 4, 8], [7, 8, 9]); return { v, t }; }
  v.push([m0[0], m0[1], e + rf], [m1[0], m1[1], e + rf]); t.push([4, 8, 9], [4, 9, 7], [8, 5, 6], [8, 6, 9], [4, 5, 8], [6, 7, 9]);
  return { v, t };
}

// ---------- 3D ----------
const gl = $<HTMLCanvasElement>('gl'), p3 = $('p3'), ov = $<HTMLImageElement>('ov');
const renderer = new THREE.WebGLRenderer({ canvas: gl, antialias: true, preserveDrawingBuffer: true });
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xdfe4e2);
const cam = new THREE.PerspectiveCamera(40, 1, 1, 30000);
const ctl = new OrbitControls(cam, gl);
scene.add(new THREE.HemisphereLight(0xffffff, 0x9a9a8a, 1.6)); const sun = new THREE.DirectionalLight(0xffffff, 1.4); sun.position.set(-300, 600, 200); scene.add(sun);
const groundMesh = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000), new THREE.MeshLambertMaterial({ color: 0xc8d3c8 })); groundMesh.rotation.x = -Math.PI / 2; scene.add(groundMesh);
const housesGroup = new THREE.Group(), ctxGroup = new THREE.Group(); scene.add(housesGroup, ctxGroup);
const plain = new THREE.MeshLambertMaterial({ color: 0xd9cfc0, side: THREE.DoubleSide });
function texMat() { return new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide }); }
function rebuild3d() {
  housesGroup.clear(); if (!V) return;
  const C = new THREE.Vector3(...V.pos); const [W, H] = V.size; const tm = texMat();
  houses.forEach((h, hi) => {
    const r = recon(h); if (!r) return;
    const m = houseMesh(r, h.roof ?? 'gable');
    const P = m.v.map(([x, y, z]) => toW(x, y, z));
    const pos: number[] = [], uv: number[] = [], texd: number[] = [], plainT: number[] = [];
    m.t.forEach((tri, k) => {
      const a = P[tri[0]], b = P[tri[1]], c = P[tri[2]];
      const n = new THREE.Vector3().subVectors(b, a).cross(new THREE.Vector3().subVectors(c, a)).normalize();
      const ctr = a.clone().add(b).add(c).multiplyScalar(1 / 3);
      if (n.dot(new THREE.Vector3().subVectors(ctr, C)) > 0) n.negate();   // the triangles are not consistently wound
      const uvs = [a, b, c].map(p => project(p));
      const seen = n.dot(new THREE.Vector3().subVectors(C, ctr)) > 0 && uvs.every(u => u && u[0] >= 0 && u[0] <= W && u[1] >= 0 && u[1] <= H);
      (seen ? texd : plainT).push(k);
      for (let j = 0; j < 3; j++) { const p = [a, b, c][j]; pos.push(p.x, p.y, p.z); const u = uvs[j]; uv.push(u ? u[0] / W : 0, u ? 1 - u[1] / H : 0); }
    });
    // order triangles: textured first, plain after (two material groups)
    const order = [...texd, ...plainT], P2: number[] = [], U2: number[] = [];
    for (const k of order) { P2.push(...pos.slice(k * 9, k * 9 + 9)); U2.push(...uv.slice(k * 6, k * 6 + 6)); }
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(P2, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(U2, 2));
    geo.computeVertexNormals(); geo.addGroup(0, texd.length * 3, 0); geo.addGroup(texd.length * 3, plainT.length * 3, 1);
    const mesh = new THREE.Mesh(geo, [tm, plain]); mesh.userData.h = hi; housesGroup.add(mesh);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({ color: hi === selH ? 0xe0a020 : 0x3b3b3b })); housesGroup.add(edges);
  });
  if (!($('drafts') as HTMLInputElement).checked) focus3d();
}
function context3d() {
  ctxGroup.clear(); if (!MODEL || !V || !($('ctx') as HTMLInputElement).checked) return;
  const y = V.year + 0.01, [OX, OY] = MODEL.origin; const pos: number[] = [];
  const vis = (b: number) => { if (MODEL.from[b] > y || MODEL.to[b] <= y) return false; const g = MODEL.gaps[b] || []; for (let k = 0; k + 1 < g.length; k += 2) if (g[k] <= y && y < g[k + 1]) return false; return true; };
  for (let b = 0; b < MODEL.n; b++) {
    if (!vis(b) || ['moat', 'ditch'].includes(MODEL.classes[MODEL.cls[b]])) continue;
    const r = MODEL.rings[b]; const pts: XY[] = []; for (let k = 0; k < r.length; k += 2) pts.push([r[k] / 10 + OX, r[k + 1] / 10 + OY]);
    const c = pts.reduce((s, p) => [s[0] + p[0] / pts.length, s[1] + p[1] / pts.length], [0, 0]);
    if (Math.hypot(c[0] - OX, c[1] - OY) > 1500) continue;
    const h = Math.min(MODEL.h1[b], 40), z0 = MODEL.z[b] - VIEWS.ground;
    const W3 = (p: XY, hh: number) => toW(p[0], p[1], z0 + hh);
    for (let i = 0; i < pts.length; i++) { const a = pts[i], bb = pts[(i + 1) % pts.length]; const A = W3(a, 0), B = W3(bb, 0), Ct = W3(bb, h), D = W3(a, h); pos.push(A.x, A.y, A.z, B.x, B.y, B.z, Ct.x, Ct.y, Ct.z, A.x, A.y, A.z, Ct.x, Ct.y, Ct.z, D.x, D.y, D.z); }
    const tri = THREE.ShapeUtils.triangulateShape(pts.map(p => new THREE.Vector2(p[0], p[1])), []);
    for (const t of tri) for (const k of t) { const P = W3(pts[k], h); pos.push(P.x, P.y, P.z); }
  }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.computeVertexNormals();
  ctxGroup.add(new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: 0xb9b4ab, side: THREE.DoubleSide, transparent: true, opacity: 0.55 })));
}
function focus3d() {
  const box = new THREE.Box3().setFromObject(housesGroup);
  const c = box.isEmpty() ? new THREE.Vector3(0, VIEWS.ground, 0) : box.getCenter(new THREE.Vector3());
  const sz = box.isEmpty() ? 400 : Math.max(60, box.getSize(new THREE.Vector3()).length());
  if (!box.isEmpty() || !ctl.target.lengthSq()) { ctl.target.copy(c); if (cam.position.distanceTo(c) > 6 * sz || cam.position.distanceTo(c) < 0.5 * sz) cam.position.copy(c).add(new THREE.Vector3(sz * 0.9, sz * 0.8, sz * 1.1)); }
}
function size3d() {
  const r = p3.getBoundingClientRect(); let w = r.width, h = r.height, x = 0, y = 0;
  const drafts = ($('drafts') as HTMLInputElement).checked && V;
  if (drafts) { const a = V!.size[0] / V!.size[1]; if (w / h > a) { const w2 = h * a; x = (w - w2) / 2; w = w2; } else { const h2 = w / a; y = (h - h2) / 2; h = h2; } }
  renderer.setPixelRatio(devicePixelRatio); renderer.setSize(w, h, false); gl.style.width = w + 'px'; gl.style.height = h + 'px'; gl.style.marginLeft = x + 'px'; gl.style.marginTop = y + 'px';
  Object.assign(ov.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
  cam.aspect = w / h;
  if (drafts) { cam.position.set(...V!.pos); cam.quaternion.set(...V!.quat); cam.fov = V!.fov; ctl.enabled = false; cam.updateProjectionMatrix(); cam.projectionMatrix.elements[0] *= (V!.stretch || 1); cam.projectionMatrixInverse.copy(cam.projectionMatrix).invert(); ov.style.opacity = ($('ovop') as HTMLInputElement).value; }
  else { cam.fov = 40; ctl.enabled = true; cam.updateProjectionMatrix(); ov.style.opacity = '0'; }
}
$('drafts').onchange = () => { if (!($('drafts') as HTMLInputElement).checked) focus3d(); size3d(); };
$('ovop').oninput = () => { if (($('drafts') as HTMLInputElement).checked) ov.style.opacity = ($('ovop') as HTMLInputElement).value; };
$('ctx').onchange = context3d;
renderer.setAnimationLoop(() => { if (ctl.enabled) ctl.update(); renderer.render(scene, cam); });
addEventListener('resize', () => { size3d(); sizeImg(); });

// ---------- veduta image (2D) ----------
const ic = $<HTMLCanvasElement>('img'), ix = ic.getContext('2d')!;
let iv = { cx: 0, cy: 0, s: 1 };
const DPR = () => devicePixelRatio;
const S2I = (u: number, v: number): XY => [(u - ic.width / 2) / DPR() * iv.s + iv.cx, (v - ic.height / 2) / DPR() * iv.s + iv.cy];
function sizeImg() { const r = ic.parentElement!.getBoundingClientRect(); ic.width = r.width * DPR(); ic.height = r.height * DPR(); drawImg(); }
const PTC: Record<keyof Pts, string> = { foot: '#2d9a4e', eave: '#d0402a', ridge: '#2f5fd0' };
function drawImg() {
  ix.setTransform(1, 0, 0, 1, 0, 0); ix.fillStyle = '#e9e7e0'; ix.fillRect(0, 0, ic.width, ic.height); if (!img) return;
  const k = DPR() / iv.s; ix.setTransform(k, 0, 0, k, ic.width / 2 - iv.cx * k, ic.height / 2 - iv.cy * k); ix.imageSmoothingEnabled = iv.s > 1; ix.drawImage(img, 0, 0);
  houses.forEach((h, hi) => {
    const on = hi === selH, r = recon(h);
    if (r) {   // the reconstruction projected back into the drawing
      const m = houseMesh(r, h.roof ?? 'gable'); const P = m.v.map(([x, y, z]) => project(toW(x, y, z)));
      ix.strokeStyle = on ? 'rgba(224,160,32,.95)' : 'rgba(30,60,160,.8)'; ix.lineWidth = (on ? 2 : 1.2) / k;
      for (const t of m.t) { const a = P[t[0]], b = P[t[1]], c = P[t[2]]; if (!a || !b || !c) continue; ix.beginPath(); ix.moveTo(...a); ix.lineTo(...b); ix.lineTo(...c); ix.closePath(); ix.stroke(); }
    }
    for (const t of ['foot', 'eave', 'ridge'] as (keyof Pts)[]) for (const [x, y] of h.pts[t]) { ix.beginPath(); ix.arc(x, y, (on ? 4.5 : 3) / k, 0, 7); ix.fillStyle = PTC[t]; ix.fill(); ix.lineWidth = 1 / k; ix.strokeStyle = '#fff'; ix.stroke(); }
    const c0 = h.pts.foot[0] ?? h.pts.eave[0]; if (c0) { ix.font = `${12 / k}px system-ui`; ix.fillStyle = on ? '#8c3b2e' : '#222'; ix.fillText(h.name || `#${hi + 1}`, c0[0] + 6 / k, c0[1] + 14 / k); }
  });
}
let drag: number[] | null = null, space = false;
const evI = (e: MouseEvent): XY => { const r = ic.getBoundingClientRect(); return [(e.clientX - r.left) * DPR(), (e.clientY - r.top) * DPR()]; };
ic.addEventListener('wheel', e => { e.preventDefault(); const [u, v] = evI(e), [x, y] = S2I(u, v); iv.s = Math.min(Math.max(iv.s * Math.exp(e.deltaY * 0.0015), 0.03), 30); const [x2, y2] = S2I(u, v); iv.cx += x - x2; iv.cy += y - y2; drawImg(); }, { passive: false });
ic.addEventListener('contextmenu', e => e.preventDefault());
ic.addEventListener('mousedown', e => {
  const [u, v] = evI(e);
  if (e.button === 1 || space || selH < 0) { drag = [u, v, iv.cx, iv.cy]; return; }
  const [x, y] = S2I(u, v), P = houses[selH].pts;
  if (e.button === 2) { let best: [keyof Pts, number] | null = null, bd = 1e9;
    for (const t of ['foot', 'eave', 'ridge'] as (keyof Pts)[]) P[t].forEach((p, j) => { const d = Math.hypot(p[0] - x, p[1] - y); if (d < bd) { bd = d; best = [t, j]; } });
    if (best && bd < 15 * iv.s) P[(best as [keyof Pts, number])[0]].splice((best as [keyof Pts, number])[1], 1); }
  else if (e.button === 0) P[ptType].push([Math.round(x * 10) / 10, Math.round(y * 10) / 10]);
  dirty = true; changed();
});
addEventListener('mousemove', e => { if (!drag) return; const [u, v] = evI(e), k = iv.s / DPR(); iv.cx = drag[2] - (u - drag[0]) * k; iv.cy = drag[3] - (v - drag[1]) * k; drawImg(); });
addEventListener('mouseup', () => { drag = null; });
addEventListener('keydown', e => {
  const tg = e.target as HTMLElement; if (tg.tagName === 'INPUT' && (tg as HTMLInputElement).type === 'text') return;
  if (e.code === 'Space') { space = true; e.preventDefault(); }
  if (e.key === '1' || e.key === '2' || e.key === '3') setPt((['foot', 'eave', 'ridge'] as (keyof Pts)[])[+e.key - 1]);
  if (e.key === 'n') $('new').click();
  if (e.key === 's' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); void save(); }
});
addEventListener('keyup', e => { if (e.code === 'Space') space = false; });

// ---------- panel ----------
function setPt(t: keyof Pts) { ptType = t; document.querySelectorAll<HTMLButtonElement>('[data-pt]').forEach(b => b.classList.toggle('on', b.dataset.pt === t)); }
document.querySelectorAll<HTMLButtonElement>('[data-pt]').forEach(b => b.onclick = () => setPt(b.dataset.pt as keyof Pts));
function refresh() {
  const ul = $('list'); ul.innerHTML = '';
  houses.forEach((h, i) => { const r = recon(h); const li = document.createElement('li'); li.className = i === selH ? 'on' : '';
    li.innerHTML = `<span>${h.name || '#' + (i + 1)}</span><span>${r ? `${r.width.toFixed(1)}×${r.len.toFixed(1)} m, ${r.eave.toFixed(1)}/${r.ridge.toFixed(1)} m` : `${h.pts.foot.length}/${h.pts.eave.length}/${h.pts.ridge.length}`}</span>`;
    li.onclick = () => { selH = i; refresh(); drawImg(); rebuild3d(); }; ul.appendChild(li); });
  $('edit').hidden = selH < 0;
  if (selH >= 0) { const h = houses[selH], r = recon(h);
    ($('name') as HTMLInputElement).value = h.name ?? ''; ($('roof') as HTMLSelectElement).value = h.roof ?? 'gable';
    ($('from') as HTMLInputElement).value = h.from?.toString() ?? ''; ($('to') as HTMLInputElement).value = h.to?.toString() ?? '';
    $('info').innerHTML = r ? T2(`půdorys ${r.width.toFixed(1)} × ${r.len.toFixed(1)} m · okap ${r.eave.toFixed(1)} m · hřeben ${r.ridge.toFixed(1)} m` + (h.pts.eave.length ? ` · odchylka okapů ${r.rmsEave.toFixed(1)} px` : ''),
      `footprint ${r.width.toFixed(1)} × ${r.len.toFixed(1)} m · eave ${r.eave.toFixed(1)} m · ridge ${r.ridge.toFixed(1)} m` + (h.pts.eave.length ? ` · eave error ${r.rmsEave.toFixed(1)} px` : ''))
      : T2('chybí aspoň 3 rohy půdorysu', 'at least 3 footprint corners are missing'); }
}
function changed() { refresh(); drawImg(); rebuild3d(); }
$('name').oninput = () => { if (selH < 0) return; houses[selH].name = ($('name') as HTMLInputElement).value || undefined; dirty = true; refresh(); drawImg(); };
$('roof').onchange = () => { if (selH < 0) return; houses[selH].roof = ($('roof') as HTMLSelectElement).value; dirty = true; changed(); };
for (const k of ['from', 'to'] as const) $(k).oninput = () => { if (selH < 0) return; const v = ($(k) as HTMLInputElement).value; houses[selH][k] = v === '' ? undefined : +v; dirty = true; };
$('new').onclick = () => { houses.push({ roof: 'gable', pts: { foot: [], eave: [], ridge: [] } }); selH = houses.length - 1; setPt('foot'); dirty = true; changed(); };
$('del').onclick = () => { if (selH < 0) return; houses.splice(selH, 1); selH = -1; dirty = true; changed(); };

// ---------- saving ----------
async function save() {
  if (!V) return;
  try {
    const [W, H] = V.size;
    let r = await fetch(`/api/manual/veduta_${sid}.json`, { method: 'POST', body: JSON.stringify({ source: sid, size: [W, H], buildings: houses, saved: new Date().toISOString() }, null, 1) });
    if (!r.ok) throw new Error(String(r.status));
    const all = (await getJSON<{ buildings: any[] }>('/manual/veduta_buildings.json')) ?? { buildings: [] };
    const year = V.year;
    const mine = houses.map((h, i) => ({ h, i, r: recon(h) })).filter(o => o.r).map(({ h, i, r }) => ({
      source: sid, name: h.name || `#${i + 1}`, ring: r!.q.map(([x, y]) => [Math.round(x * 100) / 100, Math.round(y * 100) / 100]), eave: +r!.eave.toFixed(2), ridge: +r!.ridge.toFixed(2),
      roof: h.roof ?? 'gable', tower: h.pts.ridge.length === 1, from: h.from ?? year - 25, to: h.to ?? year + 25, n: { foot: h.pts.foot.length, eave: h.pts.eave.length, ridge: h.pts.ridge.length } }));
    const out = { note: 'buildings reconstructed from the vedute (iso.html / veduta_recon.py); heights above the ground', ground: VIEWS.ground, buildings: [...all.buildings.filter(b => b.source !== sid), ...mine] };
    r = await fetch('/api/manual/veduta_buildings.json', { method: 'POST', body: JSON.stringify(out, null, 1) }); if (!r.ok) throw new Error(String(r.status));
    dirty = false; status(T2(`uloženo: ${mine.length} domů – model je převezme při dalším generování`, `saved: ${mine.length} houses – the model takes them at the next generation`));
  } catch (e) { status('ERROR ' + (e as Error).message); }
}
$('save').onclick = save;
addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });

// ---------- opening a veduta ----------
async function openVed(id: string) {
  if (dirty && !confirm(T2('Neuložené změny se zahodí. Pokračovat?', 'Unsaved changes will be lost. Continue?'))) { ($('vedSel') as HTMLSelectElement).value = sid; return; }
  sid = id; V = VIEWS.views[id] ?? null; dirty = false; selH = -1;
  const ved = VED.find(v => v.id === id)!;
  img = await new Promise<HTMLImageElement | null>(res => { const i = new Image(); i.onload = () => res(i); i.onerror = () => res(null); i.src = ved.url; });
  if (img) { ov.src = img.src; tex = new THREE.Texture(img); tex.colorSpace = THREE.SRGBColorSpace; tex.needsUpdate = true;
    iv = { cx: img.width / 2, cy: img.height / 2, s: Math.max(img.width / ic.clientWidth, img.height / ic.clientHeight) }; }
  const e = await getJSON<{ buildings: House[] }>(`/manual/veduta_${id}.json`);
  houses = (e?.buildings ?? []).map(h => ({ ...h, pts: { foot: h.pts?.foot ?? [], eave: h.pts?.eave ?? [], ridge: h.pts?.ridge ?? [] } }));
  $('cam').textContent = V ? T2(`kamera: ${V.how}, odchylka ${V.rms_pct} % výšky listu`, `camera: ${V.how}, error ${V.rms_pct} % of the sheet height`) : T2('kamera chybí – spusťte veduta_views.py', 'no camera – run veduta_views.py');
  context3d(); changed(); size3d(); focus3d();
}
($('vedSel') as HTMLSelectElement).onchange = () => openVed(($('vedSel') as HTMLSelectElement).value);

(async () => {
  VIEWS = (await getJSON<typeof VIEWS>('/appdata/veduta_views.json'))!;
  const idx = await getJSON<{ vedute: { id: string; label: string; url: string; year: number | null }[] }>('/manual/maps.json');
  VED = (idx?.vedute ?? []).filter(v => VIEWS?.views[v.id]).map(v => ({ ...v, url: '/data/historic' + v.url }));
  for (const v of VED) ($('vedSel') as HTMLSelectElement).add(new Option(`${v.year ?? ''} · ${v.label}`, v.id));
  sizeImg(); size3d();
  MODEL = await getJSON('/data/historic/growth/web/model.json');
  if (VED.length) await openVed(VED.find(v => v.id === 'te-1618')?.id ?? VED[0].id);
})();

// debug handle (dev)
(window as any).__iso = { get houses() { return houses; }, set houses(h: House[]) { houses = h; }, project: (x: number, y: number, h: number) => project(toW(x, y, h)), changed: () => { selH = houses.length - 1; changed(); }, recon };
