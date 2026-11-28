// Facade textures of the growth model: shared by the facade editor (facade.html) and the 3D viewer (growth3d.html).
// A building's walls are the edges of its model footprint; a texture covers a rectangle [t0, z0, t1, z1] of a wall
// (t = metres along the wall from p0, z = metres above the building base) and is cut to the wall's top profile (eave,
// gable). Coordinates are model-local metres (x east, y north from the model origin); in three.js x = x, y = base + z,
// z = −y. Records live in manual/facades.json, the rectified images in data/historic/growth/facades/tex/.
import * as THREE from 'three';
import type { Roof } from './blocks3d';

export type XY = [number, number];
export interface Face {
  wall: number; p0: XY; p1: XY; out: XY;   // wall line (model-local metres) and its outward normal
  prof: XY[];                              // top profile of the wall (t, z) from t = 0 to L
  rect: [number, number, number, number];  // texture rectangle t0, z0, t1, z1 (the whole wall by default)
  ctrl: [number, number, number, number];  // control rectangle: wall coordinates of the four image points
  quad: XY[];                              // image points of the control corners (t0,z0) (t1,z0) (t1,z1) (t0,z1)
  tex: string; how: 'manual' | 'camera' | 'veduta' | 'copy' | 'file'; px?: [number, number];
  b?: string;                              // building id (faces of a block)
  open?: [number, number][];               // parts of the wall not covered by a neighbour (t intervals)
  copy?: { b: string; wall: number };      // texture copied from another wall of the layer (walls not seen in the image)
  src?: string;                            // own source image (a texture uploaded straight onto this wall)
  seen?: number;                           // share of the wall seen in the image (the rest hidden behind other houses)
}
export interface Layer {
  id: string; src: string; kind: 'photo' | 'drawing' | 'veduta'; label?: string; year?: number; valid: [number, number]; faces: Face[];
  cam?: number[]; pts?: { c: string; uv: XY }[];   // camera (3 × 4: DLT or affine) and the points clicked for it
  camKind?: 'auto' | 'corr' | 'affine' | 'dlt';    // camera model; corr = veduta camera + local image correction
  camFit?: 'corr' | 'affine' | 'dlt';             // the camera model fitted to the points
  corr?: number[];                                 // local correction of the veduta camera: plan homography (3 × 3), w (2), Zr, has w
  roof?: Roof; noRoof?: boolean;                   // roofs of the block from this image (plan-view texture)
}
/** Facades of a block (one or more neighbouring buildings textured together); faces name their building (b). */
export interface BFac { members?: string[]; layers: Layer[]; edited?: string }
export interface Wall { k: number; p0: XY; p1: XY; L: number; out: XY; prof: XY[] }

// minimal model record access (model.json arrays)
export interface ModelLike { rings: number[][]; from: number[]; to: number[]; h0: number[]; h1: number[]; tR: number[]; gaps: number[][]; z?: number[]; ch2?: Record<string, [number, number]> }

/** Height of building b in year y (as the viewer's shader, without the rising animation). */
export function heightAt(M: ModelLike, b: number, y: number): number {
  const c2 = M.ch2?.[String(b)];
  if (c2 && y >= c2[0]) return c2[1];
  return y < M.tR[b] ? M.h0[b] : M.h1[b];
}
export function maxHeight(M: ModelLike, b: number): number { return Math.max(M.h0[b], M.h1[b], M.ch2?.[String(b)]?.[1] ?? 0, 0.5); }

/** Years in which building b changes (start, changes of height, end of gaps): the periods of one state. */
export function statePeriod(M: ModelLike, b: number, y: number): [number, number] {
  const cuts = [M.from[b], M.tR[b], M.ch2?.[String(b)]?.[0] ?? 9999, M.gaps[b][1] || 9999, M.gaps[b][3] || 9999, M.to[b]].filter(v => v > 0 && v < 9999).sort((a, b2) => a - b2);
  let a = M.from[b], e = M.to[b];
  for (const c of cuts) { if (c <= y) a = Math.max(a, c); else { e = Math.min(e, c); break; } }
  return [Math.round(a * 10) / 10, Math.round(e * 10) / 10];
}

/** Walls of a footprint ring (model-local metres): nearly collinear edges merged, outward normals. */
export function wallsOf(M: ModelLike, b: number, y: number, mesh?: { v: Float32Array } | null): Wall[] {
  const r = M.rings[b]; let P: XY[] = []; for (let i = 0; i < r.length; i += 2) P.push([r[i] / 10, r[i + 1] / 10]);
  const area = P.reduce((s, p, i) => { const q = P[(i + 1) % P.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0) / 2;
  if (area < 0) P.reverse();   // counter-clockwise: seen from outside, t runs from left to right on every wall
  // merge vertices where the direction changes by less than 10° or the edge is shorter than 0.6 m
  for (let pass = 0; pass < 3 && P.length > 3; pass++) {
    const keep: XY[] = [];
    for (let i = 0; i < P.length; i++) {
      const a = P[(i - 1 + P.length) % P.length], p = P[i], c = P[(i + 1) % P.length];
      const d1 = [p[0] - a[0], p[1] - a[1]], d2 = [c[0] - p[0], c[1] - p[1]], l1 = Math.hypot(d1[0], d1[1]), l2 = Math.hypot(d2[0], d2[1]);
      const ang = Math.abs(Math.atan2(d1[0] * d2[1] - d1[1] * d2[0], d1[0] * d2[0] + d1[1] * d2[1]));
      if ((ang < 0.17 || Math.min(l1, l2) < 0.6) && P.length - (i - keep.length) > 3) continue;
      keep.push(p);
    }
    if (keep.length >= 3) P = keep;
  }
  const H = heightAt(M, b, y), Hm = maxHeight(M, b);
  return P.map((p0, k) => {
    const p1 = P[(k + 1) % P.length], L = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]) || 1;
    const d: XY = [(p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L];
    const out: XY = [d[1], -d[0]];   // counter-clockwise ring: outward is to the right of the direction
    let prof: XY[] = [[0, H], [L, H]];
    if (mesh) {   // top profile from the city 3D model: highest vertex near the wall line, per 1 m bin, scaled to the year's height
      const nb = Math.max(2, Math.ceil(L)), top = new Array(nb + 1).fill(-1);
      for (let i = 0; i < mesh.v.length; i += 3) {
        const x = mesh.v[i] - p0[0], yy = mesh.v[i + 1] - p0[1], t = x * d[0] + yy * d[1], s = x * out[0] + yy * out[1];
        if (Math.abs(s) > 0.8 || t < -0.3 || t > L + 0.3) continue;
        const j = Math.min(nb, Math.max(0, Math.round(t / L * nb))); top[j] = Math.max(top[j], mesh.v[i + 2]);
      }
      const known = top.map((z, j) => [j / nb * L, z] as XY).filter(q => q[1] > 0.5);
      if (known.length >= 2) {
        const pts: XY[] = known.map(([t, z]) => [t, z * H / Hm] as XY);
        if (pts[0][0] > 0) pts.unshift([0, pts[0][1]]); if (pts[pts.length - 1][0] < L) pts.push([L, pts[pts.length - 1][1]]);
        prof = simplify(pts, 0.25);
      }
    }
    return { k, p0, p1, L, out, prof };
  });
}
function simplify(p: XY[], tol: number): XY[] {   // Douglas–Peucker
  if (p.length <= 2) return p;
  const a = p[0], b = p[p.length - 1]; let im = 0, dm = 0;
  for (let i = 1; i < p.length - 1; i++) { const d = Math.abs((b[0] - a[0]) * (a[1] - p[i][1]) - (a[0] - p[i][0]) * (b[1] - a[1])) / (Math.hypot(b[0] - a[0], b[1] - a[1]) || 1); if (d > dm) { dm = d; im = i; } }
  return dm < tol ? [a, b] : [...simplify(p.slice(0, im + 1), tol).slice(0, -1), ...simplify(p.slice(im), tol)];
}
export const profAt = (prof: XY[], t: number) => {
  for (let i = 1; i < prof.length; i++) if (t <= prof[i][0]) { const [t0, z0] = prof[i - 1], [t1, z1] = prof[i]; return t1 > t0 ? z0 + (z1 - z0) * (t - t0) / (t1 - t0) : z1; }
  return prof[prof.length - 1][1];
};

/** Mesh of one textured face: the rectangle cut to the wall's top profile, slightly in front of the wall. */
export function faceMesh(f: Face, baseY: number, tex: THREE.Texture, lift = 0): THREE.Mesh {
  const [t0, z0, t1, z1] = f.rect, L = Math.hypot(f.p1[0] - f.p0[0], f.p1[1] - f.p0[1]) || 1;
  const d: XY = [(f.p1[0] - f.p0[0]) / L, (f.p1[1] - f.p0[1]) / L], off = 0.12 + lift;
  // outline in (t, z): bottom edge, then the profile (clipped to the rectangle) backwards
  const top: XY[] = [[t1, Math.min(z1, profAt(f.prof, t1))]];
  for (const [t, z] of [...f.prof].reverse()) if (t > t0 && t < t1) top.push([t, Math.min(z1, z)]);
  top.push([t0, Math.min(z1, profAt(f.prof, t0))]);
  const outline: XY[] = ([[t0, z0], [t1, z0], ...top] as XY[]).filter((q, i, a) => i === 0 || Math.hypot(q[0] - a[i - 1][0], q[1] - a[i - 1][1]) > 1e-3);
  const tris = THREE.ShapeUtils.triangulateShape(outline.map(([t, z]) => new THREE.Vector2(t, z)), []);
  const pos: number[] = [], uv: number[] = [];
  for (const [t, z] of outline) {
    const x = f.p0[0] + d[0] * t + f.out[0] * off, y = f.p0[1] + d[1] * t + f.out[1] * off;
    pos.push(x, baseY + Math.max(z, z0), -y); uv.push((t - t0) / (t1 - t0 || 1), (z - z0) / (z1 - z0 || 1));
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(tris.flat()); g.computeVertexNormals();
  const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ map: tex, transparent: true, alphaTest: 0.05, side: THREE.DoubleSide, depthWrite: true, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }));
  m.renderOrder = 2; return m;
}

// ---------- projective geometry (homography, DLT camera) ----------
/** Symmetric eigen decomposition (Jacobi); returns the eigenvector of the smallest eigenvalue. */
export function smallestEigvec(A: number[][]): number[] {
  const n = A.length, a = A.map(r => [...r]), V: number[][] = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));
  for (let sweep = 0; sweep < 60; sweep++) {
    let off = 0; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) off += a[i][j] * a[i][j];
    if (off < 1e-22) break;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
      if (Math.abs(a[p][q]) < 1e-300) continue;
      const th = (a[q][q] - a[p][p]) / (2 * a[p][q]), t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1)), c = 1 / Math.sqrt(t * t + 1), s = t * c;
      for (let k = 0; k < n; k++) { const akp = a[k][p], akq = a[k][q]; a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq; }
      for (let k = 0; k < n; k++) { const apk = a[p][k], aqk = a[q][k]; a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk; }
      for (let k = 0; k < n; k++) { const vkp = V[k][p], vkq = V[k][q]; V[k][p] = c * vkp - s * vkq; V[k][q] = s * vkp + c * vkq; }
    }
  }
  let im = 0; for (let i = 1; i < n; i++) if (a[i][i] < a[im][im]) im = i;
  return V.map(r => r[im]);
}
const normT = (pts: number[][]) => {   // Hartley normalisation: centroid 0, mean distance √d
  const d = pts[0].length, c = new Array(d).fill(0); for (const p of pts) p.forEach((v, i) => c[i] += v / pts.length);
  const md = pts.reduce((s, p) => s + Math.hypot(...p.map((v, i) => v - c[i])), 0) / pts.length || 1, k = Math.sqrt(d) / md;
  return { c, k, apply: (p: number[]) => p.map((v, i) => (v - c[i]) * k) };
};
/** Homography (3×3, row-major) mapping src[i] → dst[i] (≥ 4 points, least squares). */
export function homography(src: XY[], dst: XY[]): number[] {
  const ns = normT(src), nd = normT(dst), A: number[][] = [];
  src.forEach((s0, i) => {
    const [x, y] = ns.apply(s0), [u, v] = nd.apply(dst[i]);
    A.push([-x, -y, -1, 0, 0, 0, u * x, u * y, u], [0, 0, 0, -x, -y, -1, v * x, v * y, v]);
  });
  const h = smallestEigvec(mtm(A));
  // denormalise: H = Td⁻¹ · Hn · Ts
  const Ts = [ns.k, 0, -ns.k * ns.c[0], 0, ns.k, -ns.k * ns.c[1], 0, 0, 1], Tdi = [1 / nd.k, 0, nd.c[0], 0, 1 / nd.k, nd.c[1], 0, 0, 1];
  const H = mul3(Tdi, mul3(h, Ts)); const s = H[8] || 1; return H.map(v => v / s);
}
export const applyH = (H: number[], x: number, y: number): XY => { const w = H[6] * x + H[7] * y + H[8]; return [(H[0] * x + H[1] * y + H[2]) / w, (H[3] * x + H[4] * y + H[5]) / w]; };
const mul3 = (a: number[], b: number[]) => [0, 1, 2].flatMap(i => [0, 1, 2].map(j => a[3 * i] * b[j] + a[3 * i + 1] * b[3 + j] + a[3 * i + 2] * b[6 + j]));
const mtm = (A: number[][]) => { const n = A[0].length, R = Array.from({ length: n }, () => new Array(n).fill(0)); for (const r of A) for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) R[i][j] += r[i] * r[j]; return R; };
/** Camera matrix P (3×4, row-major) from ≥ 6 correspondences 3D → image (normalised DLT). */
export function dlt(X: number[][], uv: XY[]): number[] {
  const nX = normT(X), nU = normT(uv), A: number[][] = [];
  X.forEach((x0, i) => {
    const [x, y, z] = nX.apply(x0), [u, v] = nU.apply(uv[i]);
    A.push([x, y, z, 1, 0, 0, 0, 0, -u * x, -u * y, -u * z, -u], [0, 0, 0, 0, x, y, z, 1, -v * x, -v * y, -v * z, -v]);
  });
  const p = smallestEigvec(mtm(A));
  // P = Tu⁻¹ · Pn · TX
  const TX = [[nX.k, 0, 0, -nX.k * nX.c[0]], [0, nX.k, 0, -nX.k * nX.c[1]], [0, 0, nX.k, -nX.k * nX.c[2]], [0, 0, 0, 1]];
  const Tui = [[1 / nU.k, 0, nU.c[0]], [0, 1 / nU.k, nU.c[1]], [0, 0, 1]];
  const Pn = [p.slice(0, 4), p.slice(4, 8), p.slice(8, 12)];
  const PX = Pn.map(r => [0, 1, 2, 3].map(j => r.reduce((s, v, k) => s + v * TX[k][j], 0)));
  const P = Tui.map(r => [0, 1, 2, 3].map(j => r.reduce((s, v, k) => s + v * PX[k][j], 0)));
  return P.flat();
}
export const projectP = (P: number[], x: number, y: number, z: number): XY | null => {
  const w = P[8] * x + P[9] * y + P[10] * z + P[11]; if (Math.abs(w) < 1e-12) return null;
  return [(P[0] * x + P[1] * y + P[2] * z + P[3]) / w, (P[4] * x + P[5] * y + P[6] * z + P[7]) / w];
};
/** Camera centre of P (null space): the point with P · [C, 1] = 0. */
export function cameraCentre(P: number[]): number[] {
  const det = (m: number[][]) => m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
  const cols = [0, 1, 2, 3].map(j => [0, 1, 2].map(i => P[4 * i + j]));
  const minor = (skip: number) => det([0, 1, 2].map(i => [0, 1, 2, 3].filter(j => j !== skip).map(j => cols[j][i])));
  const c = [minor(0), -minor(1), minor(2), -minor(3)];
  return [c[0] / c[3], c[1] / c[3], c[2] / c[3]];
}
