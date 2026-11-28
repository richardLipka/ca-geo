// Blocks of houses, roofs and cameras for the facade editor (facade.html) and the viewer (growth3d.html).
// A block = several neighbouring buildings textured together from one image: outer walls (party walls excluded),
// the roofs as one plan-view image draped over all roofs of the block, one camera for all (a veduta camera with a
// local correction, an affine camera for isometric drawings or a perspective DLT camera for photographs), and a
// software depth map so that parts hidden behind other houses stay transparent.
import * as THREE from 'three';
import { cameraCentre, heightAt, maxHeight, projectP, type ModelLike, type Wall, type XY } from './facades3d';

export type V3 = [number, number, number];
export function ringXY(M: ModelLike, b: number): XY[] { const r = M.rings[b], P: XY[] = []; for (let i = 0; i < r.length; i += 2) P.push([r[i] / 10, r[i + 1] / 10]); return P; }
export function pip(P: XY[], x: number, y: number): boolean {
  let c = false;
  for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; }
  return c;
}
const segD = (p: XY, a: XY, b: XY) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], l = dx * dx + dy * dy || 1, t = Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l));
  return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy);
};
/** Smallest distance between two footprints (0 when they overlap). */
export function ringDist(A: XY[], B: XY[]): number {
  if (pip(B, ...A[0]) || pip(A, ...B[0])) return 0;
  let d = 1e9;
  for (let i = 0; i < A.length; i++) for (let j = 0; j < B.length; j++) d = Math.min(d, segD(A[i], B[j], B[(j + 1) % B.length]), segD(B[j], A[i], A[(i + 1) % A.length]));
  return d;
}
export interface Index { box: Float32Array; ring(b: number): XY[] }
/** Bounding boxes of all footprints (for the neighbour queries). */
export function footIndex(M: ModelLike & { n: number }): Index {
  const box = new Float32Array(M.n * 4), cache = new Map<number, XY[]>();
  for (let b = 0; b < M.n; b++) {
    const r = M.rings[b]; let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (let i = 0; i < r.length; i += 2) { x0 = Math.min(x0, r[i]); x1 = Math.max(x1, r[i]); y0 = Math.min(y0, r[i + 1]); y1 = Math.max(y1, r[i + 1]); }
    box.set([x0 / 10, y0 / 10, x1 / 10, y1 / 10], 4 * b);
  }
  return { box, ring: b => { let p = cache.get(b); if (!p) { p = ringXY(M, b); cache.set(b, p); } return p; } };
}
export function near(ix: Index, n: number, x0: number, y0: number, x1: number, y1: number, ok: (b: number) => boolean): number[] {
  const out: number[] = [], B = ix.box;
  for (let b = 0; b < n; b++) if (B[4 * b] <= x1 && B[4 * b + 2] >= x0 && B[4 * b + 1] <= y1 && B[4 * b + 3] >= y0 && ok(b)) out.push(b);
  return out;
}
/** The block of building b: buildings standing (in the year) joined by footprints closer than gap, transitively. */
export function blockOf(M: ModelLike & { n: number }, ix: Index, b: number, standing: (b: number) => boolean, gap = 0.8, max = 120): number[] {
  const mem = [b], seen = new Set(mem), bx = ix.box;
  for (let i = 0; i < mem.length && mem.length < max; i++) {
    const a = mem[i];
    for (const c of near(ix, M.n, bx[4 * a] - gap, bx[4 * a + 1] - gap, bx[4 * a + 2] + gap, bx[4 * a + 3] + gap, c => !seen.has(c) && standing(c)))
      if (ringDist(ix.ring(a), ix.ring(c)) < gap) { seen.add(c); mem.push(c); if (mem.length >= max) break; }
  }
  return mem;
}
/** Parts of a wall not covered by other footprints (party walls): intervals of t, sampled every 0.5 m, 0.45 m outside. */
export function openParts(w: Wall, others: XY[][]): [number, number][] {
  const d: XY = [(w.p1[0] - w.p0[0]) / w.L, (w.p1[1] - w.p0[1]) / w.L], n = Math.max(2, Math.ceil(w.L / 0.5)), h = w.L / n / 2, out: [number, number][] = [];
  let s = -1;
  for (let i = 0; i <= n; i++) {
    const t = w.L * i / n, x = w.p0[0] + d[0] * t + w.out[0] * 0.45, y = w.p0[1] + d[1] * t + w.out[1] * 0.45;
    const open = !others.some(P => pip(P, x, y));
    if (open && s < 0) s = Math.max(0, t - h);
    if (s >= 0 && (!open || i === n)) { const e = open ? w.L : Math.min(w.L, t - h); if (e - s > 0.4) out.push([s, e]); s = -1; }
  }
  return out;
}
/** Points where the outline of the union of the footprints turns (convex or concave corners of the block). */
export function outlineCorners(rings: XY[][]): { p: XY; convex: boolean }[] {
  const out: { p: XY; convex: boolean }[] = [], R = 1.0, K = 24;
  for (const P of rings) for (const p of P) {
    if (out.some(o => Math.hypot(o.p[0] - p[0], o.p[1] - p[1]) < 1.5)) continue;
    let ins = 0;
    for (let k = 0; k < K; k++) {
      const a = (k + 0.5) / K * 2 * Math.PI, x = p[0] + R * Math.cos(a), y = p[1] + R * Math.sin(a);
      if (rings.some(Q => pip(Q, x, y) || Q.some((q, i) => segD([x, y], q, Q[(i + 1) % Q.length]) < 0.25))) ins++;
    }
    const f = ins / K; if (f > 0.92 || Math.abs(f - 0.5) < 0.15) continue;
    out.push({ p, convex: f < 0.5 });
  }
  return out;
}

// ---------- surfaces of a building (its mesh or the extruded footprint) at the height of a year ----------
type MeshV = { v: Float32Array; t: Uint16Array } | null | undefined;
/** Triangles (flat x, y, z: model-local metres, z above the base) of building b in year y; roofOnly: faces turned up. */
export function bodyTris(M: ModelLike, b: number, y: number, mesh: MeshV, roofOnly = false): Float32Array {
  const H = heightAt(M, b, y), Hm = maxHeight(M, b), out: number[] = [];
  const add = (a: V3, c: V3, e: V3) => {
    if (roofOnly) {
      const ux = c[0] - a[0], uy = c[1] - a[1], uz = c[2] - a[2], vx = e[0] - a[0], vy = e[1] - a[1], vz = e[2] - a[2];
      const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx, l = Math.hypot(nx, ny, nz) || 1;
      if (Math.abs(nz / l) < 0.3) return;
    }
    out.push(...a, ...c, ...e);
  };
  if (mesh) {
    const s = H / Hm, V = (k: number): V3 => [mesh.v[3 * k], mesh.v[3 * k + 1], mesh.v[3 * k + 2] * s];
    for (let i = 0; i < mesh.t.length; i += 3) add(V(mesh.t[i]), V(mesh.t[i + 1]), V(mesh.t[i + 2]));
  } else {
    const P = ringXY(M, b);
    if (!roofOnly) P.forEach((a, i) => { const c = P[(i + 1) % P.length]; add([a[0], a[1], 0], [c[0], c[1], 0], [c[0], c[1], H]); add([a[0], a[1], 0], [c[0], c[1], H], [a[0], a[1], H]); });
    for (const t of THREE.ShapeUtils.triangulateShape(P.map(p => new THREE.Vector2(p[0], p[1])), [])) add([P[t[0]][0], P[t[0]][1], H], [P[t[1]][0], P[t[1]][1], H], [P[t[2]][0], P[t[2]][1], H]);
  }
  return new Float32Array(out);
}
/** Ridge of a roof: the segment between the two most distant of its highest vertices (null for a flat roof). */
export function ridgeOf(tris: Float32Array): [XY, XY] | null {
  let zt = -1e9, zb = 1e9; for (let i = 2; i < tris.length; i += 3) { zt = Math.max(zt, tris[i]); zb = Math.min(zb, tris[i]); }
  if (zt - zb < 0.8) return null;
  const top: XY[] = []; for (let i = 0; i < tris.length; i += 3) if (tris[i + 2] > zt - 0.15) top.push([tris[i], tris[i + 1]]);
  let best: [XY, XY] | null = null, bd = 0.5;
  for (const a of top) for (const c of top) { const d = Math.hypot(a[0] - c[0], a[1] - c[1]); if (d > bd) { bd = d; best = [a, c]; } }
  return best;
}
/** Roof texture of a block: one plan-view image over the box [x0, y0, x1, y1] (north up) draped over the roofs. */
export interface Roof { tex: string; box: [number, number, number, number]; px?: [number, number]; seen?: number; mirrored?: number; filled?: number }
export function roofMesh(tris: Float32Array, box: Roof['box'], baseY: number, tex: THREE.Texture): THREE.Mesh {
  const pos = new Float32Array(tris.length), uv = new Float32Array(tris.length / 3 * 2);
  for (let i = 0, k = 0; i < tris.length; i += 3, k += 2) {
    pos[i] = tris[i]; pos[i + 1] = baseY + tris[i + 2] + 0.05; pos[i + 2] = -tris[i + 1];
    uv[k] = (tris[i] - box[0]) / (box[2] - box[0]); uv[k + 1] = (tris[i + 1] - box[1]) / (box[3] - box[1]);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ map: tex, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -3, polygonOffsetUnits: -3 }));
  m.renderOrder = 2; return m;
}

// ---------- cameras ----------
/** A camera: projection of a model point (x, y, Z = absolute height as in the viewer), direction to the viewer, depth. */
export interface Cam { P: (X: V3) => XY | null; toViewer: (X: V3) => V3; depth: (X: V3) => number }
const cross = (a: V3, b: V3): V3 => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
/** Linear least squares (normal equations, Gauss–Jordan with pivoting). */
export function solveLS(A: number[][], y: number[]): number[] | null {
  const n = A[0].length, N = Array.from({ length: n }, () => new Array(n + 1).fill(0));
  A.forEach((r, k) => { for (let i = 0; i < n; i++) { for (let j = 0; j < n; j++) N[i][j] += r[i] * r[j]; N[i][n] += r[i] * y[k]; } });
  for (let c = 0; c < n; c++) {
    let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(N[r][c]) > Math.abs(N[p][c])) p = r;
    if (Math.abs(N[p][c]) < 1e-9) return null;
    [N[c], N[p]] = [N[p], N[c]];
    for (let r = 0; r < n; r++) if (r !== c) { const f = N[r][c] / N[c][c]; for (let j = c; j <= n; j++) N[r][j] -= f * N[c][j]; }
  }
  return N.map((r, i) => r[n] / r[i]);
}
/** Affine (parallel-projection) camera, 3 × 4 with the last row 0 0 0 1, from ≥ 4 points not all at one height. */
export function fitAffine(X: V3[], uv: XY[]): number[] | null {
  if (X.length < 4) return null;
  const zr = Math.max(...X.map(p => p[2])) - Math.min(...X.map(p => p[2])); if (zr < 1) return null;   // vertical scale undetermined
  const c = [0, 1, 2].map(i => X.reduce((s, p) => s + p[i], 0) / X.length) as V3;
  const A = X.map(p => [p[0] - c[0], p[1] - c[1], p[2] - c[2], 1]);
  const ru = solveLS(A, uv.map(q => q[0])), rv = solveLS(A, uv.map(q => q[1])); if (!ru || !rv) return null;
  const row = (r: number[]) => [r[0], r[1], r[2], r[3] - r[0] * c[0] - r[1] * c[1] - r[2] * c[2]];
  return [...row(ru), ...row(rv), 0, 0, 0, 1];
}
/** Image-space correction of a camera (local fit of a veduta): 1 point shift, 2 similarity, ≥ 3 affine (2 × 3, row-major). */
export function fitCorr(q: XY[], uv: XY[]): number[] {
  const n = q.length;
  if (n === 0) return [1, 0, 0, 0, 1, 0];
  if (n === 1) return [1, 0, uv[0][0] - q[0][0], 0, 1, uv[0][1] - q[0][1]];
  const sim = () => {   // u' = a u − b v + c, v' = b u + a v + d
    const s = solveLS(q.flatMap(p => [[p[0], -p[1], 1, 0], [p[1], p[0], 0, 1]]), uv.flatMap(p => [p[0], p[1]]));
    return s ? [s[0], -s[1], s[2], s[1], s[0], s[3]] : fitCorr(q.slice(0, 1), uv.slice(0, 1));
  };
  if (n === 2) return sim();
  const A = q.map(p => [p[0], p[1], 1]), a = solveLS(A, uv.map(p => p[0])), b = solveLS(A, uv.map(p => p[1]));
  return a && b ? [...a, ...b] : sim();
}
export const applyCorr = (A: number[], p: XY): XY => [A[0] * p[0] + A[1] * p[1] + A[2], A[3] * p[0] + A[4] * p[1] + A[5]];
/** Camera of a 3 × 4 matrix: affine (last row 0 0 0 1) or perspective. */
export function camFromMatrix(P: number[]): Cam {
  if (Math.abs(P[8]) + Math.abs(P[9]) + Math.abs(P[10]) < 1e-12) {
    // image axes a (u, right) and b (v, down): the viewing direction into the scene is a × b, to the viewer b × a
    const a: V3 = [P[0], P[1], P[2]], b: V3 = [P[4], P[5], P[6]], d = cross(b, a), l = Math.hypot(...d) || 1, dn: V3 = [d[0] / l, d[1] / l, d[2] / l];
    return { P: X => projectP(P, ...X), toViewer: () => dn, depth: X => -(X[0] * dn[0] + X[1] * dn[1] + X[2] * dn[2]) };
  }
  const C = cameraCentre(P) as V3;
  return { P: X => projectP(P, ...X), toViewer: X => [C[0] - X[0], C[1] - X[1], C[2] - X[2]], depth: X => Math.hypot(C[0] - X[0], C[1] - X[1], C[2] - X[2]) };
}

// ---------- visibility: software depth map of the buildings seen by a camera ----------
export interface DepthMap { W: number; H: number; k: number; d: Float32Array }
/** Depth of the nearest surface per image pixel (image scaled by 1/k); tris: triangles in absolute coordinates. */
export function depthMap(cam: Cam, tris: Float32Array[], W: number, H: number, k: number): DepthMap {
  const d = new Float32Array(W * H).fill(Infinity);
  for (const T of tris) for (let i = 0; i < T.length; i += 9) {
    const P: V3[] = [];
    for (let j = 0; j < 3; j++) { const X: V3 = [T[i + 3 * j], T[i + 3 * j + 1], T[i + 3 * j + 2]], q = cam.P(X); if (!q) break; P.push([q[0] / k, q[1] / k, cam.depth(X)]); }
    if (P.length < 3) continue;
    const x0 = Math.max(0, Math.floor(Math.min(P[0][0], P[1][0], P[2][0]))), x1 = Math.min(W - 1, Math.ceil(Math.max(P[0][0], P[1][0], P[2][0])));
    const y0 = Math.max(0, Math.floor(Math.min(P[0][1], P[1][1], P[2][1]))), y1 = Math.min(H - 1, Math.ceil(Math.max(P[0][1], P[1][1], P[2][1])));
    if (x1 < x0 || y1 < y0 || (x1 - x0) * (y1 - y0) > 4e6) continue;
    const [a, b, c] = P, den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1]); if (Math.abs(den) < 1e-9) continue;
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const px = x + 0.5, py = y + 0.5;
      const l0 = ((b[1] - c[1]) * (px - c[0]) + (c[0] - b[0]) * (py - c[1])) / den, l1 = ((c[1] - a[1]) * (px - c[0]) + (a[0] - c[0]) * (py - c[1])) / den, l2 = 1 - l0 - l1;
      if (l0 < -0.02 || l1 < -0.02 || l2 < -0.02) continue;
      const z = l0 * a[2] + l1 * b[2] + l2 * c[2], o = y * W + x; if (z < d[o]) d[o] = z;
    }
  }
  return { W, H, k, d };
}
/** Is the model point X (absolute) seen by the camera, i.e. not behind another surface of the depth map? */
export function seen(dm: DepthMap, cam: Cam, X: V3, uv: XY, tol = 1.2): boolean {
  const x = Math.floor(uv[0] / dm.k), y = Math.floor(uv[1] / dm.k); if (x < 0 || y < 0 || x >= dm.W || y >= dm.H) return false;
  let m = Infinity;
  for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) { const xx = x + i, yy = y + j; if (xx >= 0 && yy >= 0 && xx < dm.W && yy < dm.H) m = Math.min(m, dm.d[yy * dm.W + xx]); }
  return cam.depth(X) <= m + tol;
}
