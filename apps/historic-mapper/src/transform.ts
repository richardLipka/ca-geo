// Geometric transforms between image pixels and map coordinates (EPSG:5514, metres).
// All fits are least squares except TPS (exact interpolation with optional smoothing).
// Each fit reports per-point residuals and leave-one-out (LOO) residuals, which are the
// honest accuracy estimate for historical sources (fitted residuals of flexible models
// such as TPS are always ~0).

export type Vec2 = [number, number];
export type Method = 'helmert' | 'affine' | 'projective' | 'poly2' | 'tps';

export interface Pair { img: Vec2; map: Vec2 }

export interface Fit {
  method: Method;
  forward: (p: Vec2) => Vec2; // image → map
  inverse: (p: Vec2) => Vec2; // map → image
  residuals: number[]; // metres, per pair, of the fitted model
  rmse: number;
  loo: number[]; // leave-one-out residuals in metres (NaN if not computable)
  looRmse: number;
}

export const MIN_POINTS: Record<Method, number> = { helmert: 2, affine: 3, projective: 4, poly2: 6, tps: 3 };

// ---------- small linear algebra ----------

/** Solve A x = b (A n×n, row-major arrays) by Gaussian elimination with partial pivoting. */
export function solve(A: number[][], b: number[]): number[] {
  const n = b.length;
  const M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    if (Math.abs(M[p][c]) < 1e-12) throw new Error('singular system');
    [M[c], M[p]] = [M[p], M[c]];
    for (let r = c + 1; r < n; r++) {
      const f = M[r][c] / M[c][c];
      if (f) for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  const x = new Array(n).fill(0);
  for (let r = n - 1; r >= 0; r--) {
    let s = M[r][n];
    for (let k = r + 1; k < n; k++) s -= M[r][k] * x[k];
    x[r] = s / M[r][r];
  }
  return x;
}

/** Least squares min |A x - b| via normal equations (A m×n). Inputs are normalised by callers. */
export function lstsq(A: number[][], b: number[]): number[] {
  const n = A[0].length;
  const N = Array.from({ length: n }, () => new Array(n).fill(0));
  const r = new Array(n).fill(0);
  for (let i = 0; i < A.length; i++) {
    const a = A[i];
    for (let j = 0; j < n; j++) {
      r[j] += a[j] * b[i];
      for (let k = 0; k < n; k++) N[j][k] += a[j] * a[k];
    }
  }
  return solve(N, r);
}

// Normalisation: shift to centroid and scale to unit RMS distance (Hartley) for stability.
interface Norm { cx: number; cy: number; s: number }
function norm(pts: Vec2[]): Norm {
  const cx = pts.reduce((a, p) => a + p[0], 0) / pts.length;
  const cy = pts.reduce((a, p) => a + p[1], 0) / pts.length;
  const d = Math.sqrt(pts.reduce((a, p) => a + (p[0] - cx) ** 2 + (p[1] - cy) ** 2, 0) / pts.length) || 1;
  return { cx, cy, s: Math.SQRT2 / d };
}
const fwdN = (n: Norm, p: Vec2): Vec2 => [(p[0] - n.cx) * n.s, (p[1] - n.cy) * n.s];
const invN = (n: Norm, p: Vec2): Vec2 => [p[0] / n.s + n.cx, p[1] / n.s + n.cy];

// ---------- one-directional mappers (src → dst) ----------

type Mapper = (p: Vec2) => Vec2;

function fitDir(method: Method, src: Vec2[], dst: Vec2[], smoothing = 0): Mapper {
  const ns = norm(src), nd = norm(dst);
  const S = src.map(p => fwdN(ns, p)), D = dst.map(p => fwdN(nd, p));
  let m: Mapper;
  switch (method) {
    case 'helmert': {
      // similarity, with or without reflection (image y points down, map y up):
      //   proper:    x' = a x − b y + c ; y' = b x + a y + d
      //   reflected: x' = a x + b y + c ; y' = b x − a y + d
      const variant = (sgn: 1 | -1): { m: Mapper; e: number } => {
        const A: number[][] = [], rhs: number[] = [];
        S.forEach(([x, y], i) => { A.push([x, -sgn * y, 1, 0]); rhs.push(D[i][0]); A.push([sgn * y, x, 0, 1]); rhs.push(D[i][1]); });
        const [a, b, c, d] = lstsq(A, rhs);
        const mm: Mapper = ([x, y]) => [a * x - sgn * b * y + c, b * x + sgn * a * y + d];
        const e = S.reduce((acc, p, i) => { const q = mm(p); return acc + (q[0] - D[i][0]) ** 2 + (q[1] - D[i][1]) ** 2; }, 0);
        return { m: mm, e };
      };
      const p1 = variant(1), p2 = variant(-1);
      m = p1.e <= p2.e ? p1.m : p2.m;
      break;
    }
    case 'affine': {
      const A = S.map(([x, y]) => [x, y, 1]);
      const px = lstsq(A, D.map(p => p[0])), py = lstsq(A, D.map(p => p[1]));
      m = ([x, y]) => [px[0] * x + px[1] * y + px[2], py[0] * x + py[1] * y + py[2]];
      break;
    }
    case 'projective': { // h33 = 1, linearised DLT in normalised coordinates
      const A: number[][] = [], rhs: number[] = [];
      S.forEach(([x, y], i) => {
        const [u, v] = D[i];
        A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); rhs.push(u);
        A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); rhs.push(v);
      });
      const h = lstsq(A, rhs);
      m = ([x, y]) => { const w = h[6] * x + h[7] * y + 1; return [(h[0] * x + h[1] * y + h[2]) / w, (h[3] * x + h[4] * y + h[5]) / w]; };
      break;
    }
    case 'poly2': {
      const row = ([x, y]: Vec2) => [1, x, y, x * x, x * y, y * y];
      const A = S.map(row);
      const px = lstsq(A, D.map(p => p[0])), py = lstsq(A, D.map(p => p[1]));
      m = p => { const r = row(p); return [r.reduce((a, v, i) => a + v * px[i], 0), r.reduce((a, v, i) => a + v * py[i], 0)]; };
      break;
    }
    case 'tps': { // thin-plate spline U(r) = r² log r², with affine part; smoothing on the diagonal
      const n = S.length;
      const U = (r2: number) => (r2 < 1e-20 ? 0 : r2 * Math.log(r2));
      const K = Array.from({ length: n + 3 }, () => new Array(n + 3).fill(0));
      for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) K[i][j] = U((S[i][0] - S[j][0]) ** 2 + (S[i][1] - S[j][1]) ** 2) + (i === j ? smoothing : 0);
        K[i][n] = K[n][i] = 1; K[i][n + 1] = K[n + 1][i] = S[i][0]; K[i][n + 2] = K[n + 2][i] = S[i][1];
      }
      const wx = solve(K, [...D.map(p => p[0]), 0, 0, 0]), wy = solve(K, [...D.map(p => p[1]), 0, 0, 0]);
      m = ([x, y]) => {
        let u = wx[n] + wx[n + 1] * x + wx[n + 2] * y, v = wy[n] + wy[n + 1] * x + wy[n + 2] * y;
        for (let i = 0; i < n; i++) { const k = U((x - S[i][0]) ** 2 + (y - S[i][1]) ** 2); u += wx[i] * k; v += wy[i] * k; }
        return [u, v];
      };
      break;
    }
  }
  return p => invN(nd, m(fwdN(ns, p)));
}

const dist = (a: Vec2, b: Vec2) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const rms = (v: number[]) => { const f = v.filter(Number.isFinite); return f.length ? Math.sqrt(f.reduce((a, x) => a + x * x, 0) / f.length) : NaN; };

/** Fit image→map (and map→image) for the given pairs. Throws if too few points. */
export function fit(method: Method, pairs: Pair[], smoothing = 0): Fit {
  if (pairs.length < MIN_POINTS[method]) throw new Error(`need ≥ ${MIN_POINTS[method]} points`);
  const img = pairs.map(p => p.img), map = pairs.map(p => p.map);
  const forward = fitDir(method, img, map, smoothing);
  const inverse = fitDir(method, map, img, smoothing);
  const residuals = pairs.map(p => dist(forward(p.img), p.map));
  const loo = pairs.map((p, i) => {
    const rest = pairs.filter((_, j) => j !== i);
    if (rest.length < MIN_POINTS[method] + (method === 'tps' ? 0 : 1)) return NaN;
    try { return dist(fitDir(method, rest.map(q => q.img), rest.map(q => q.map), smoothing)(p.img), p.map); } catch { return NaN; }
  });
  return { method, forward, inverse, residuals, rmse: rms(residuals), loo, looRmse: rms(loo) };
}

// ---------- panorama resection (1D camera) ----------
// A panorama/veduta drawn from one viewpoint maps a ground bearing β to an image column
//   x = cx + f · tan(β − θ)      (perspective, horizontal only)
// Unknowns: viewpoint (X0, Y0), heading θ, focal length f (px); cx fixed at image centre.
// Bearing is measured in the map plane: β = atan2(Y − Y0, X − X0) (S-JTSK axes as given).
// The view direction sign convention is absorbed by the sign of f.

export interface PanoFit { X0: number; Y0: number; theta: number; f: number; cx: number; residualsPx: number[]; rmsePx: number; project: (p: Vec2) => number | null }

export function fitPanorama(obs: { x: number; map: Vec2 }[], cx: number, searchBox?: [number, number, number, number]): PanoFit {
  if (obs.length < 4) throw new Error('need ≥ 4 points');
  const model = (q: number[], p: Vec2) => { const b = Math.atan2(p[1] - q[1], p[0] - q[0]) - q[2]; return Math.abs(Math.cos(b)) < 1e-3 ? NaN : cx + q[3] * Math.tan(b); };
  const cost = (q: number[]) => obs.reduce((a, o) => { const r = model(q, o.map) - o.x; return a + (Number.isFinite(r) ? r * r : 1e12); }, 0);
  // initial grid search over viewpoint; for each viewpoint solve θ, f by 1D search
  const xs = obs.map(o => o.map[0]), ys = obs.map(o => o.map[1]);
  const [x0, y0, x1, y1] = searchBox ?? [Math.min(...xs) - 4000, Math.min(...ys) - 4000, Math.max(...xs) + 4000, Math.max(...ys) + 4000];
  let best = { c: Infinity, q: [0, 0, 0, 0] };
  const G = 40;
  for (let i = 0; i <= G; i++) for (let j = 0; j <= G; j++) {
    const X = x0 + (x1 - x0) * i / G, Y = y0 + (y1 - y0) * j / G;
    if (obs.some(o => dist(o.map, [X, Y]) < 50)) continue;
    const bear = obs.map(o => Math.atan2(o.map[1] - Y, o.map[0] - X));
    const mean = Math.atan2(bear.reduce((a, b) => a + Math.sin(b), 0), bear.reduce((a, b) => a + Math.cos(b), 0));
    for (const th of [mean, mean + Math.PI]) {
      // f by least squares given θ: x - cx = f tan(β-θ)
      const t = bear.map(b => Math.tan(b - th));
      const f = t.reduce((a, v, k) => a + v * (obs[k].x - cx), 0) / (t.reduce((a, v) => a + v * v, 0) || 1);
      const q = [X, Y, th, f], c = cost(q);
      if (c < best.c) best = { c, q };
    }
  }
  // Levenberg–Marquardt refinement with numeric Jacobian
  let q = best.q.slice(), lambda = 1e-2, c = best.c;
  const steps = [1, 1, 1e-4, 1];
  for (let it = 0; it < 200; it++) {
    const r = obs.map(o => model(q, o.map) - o.x);
    const J = obs.map((o, k) => q.map((_, j) => { const qq = q.slice(); qq[j] += steps[j]; return (model(qq, o.map) - o.x - r[k]) / steps[j]; }));
    const JTJ = q.map((_, a) => q.map((_, b) => J.reduce((s, row) => s + row[a] * row[b], 0)));
    const JTr = q.map((_, a) => J.reduce((s, row, k) => s + row[a] * r[k], 0));
    let improved = false;
    for (let tries = 0; tries < 8 && !improved; tries++) {
      const A = JTJ.map((row, a) => row.map((v, b) => v + (a === b ? lambda * (v || 1) : 0)));
      let d: number[];
      try { d = solve(A, JTr.map(v => -v)); } catch { lambda *= 10; continue; }
      const qn = q.map((v, k) => v + d[k]), cn = cost(qn);
      if (cn < c) { q = qn; c = cn; lambda /= 3; improved = true; } else lambda *= 10;
    }
    if (!improved) break;
  }
  const residualsPx = obs.map(o => model(q, o.map) - o.x);
  return {
    X0: q[0], Y0: q[1], theta: q[2], f: q[3], cx, residualsPx, rmsePx: rms(residualsPx),
    project: p => { const v = model(q, p); return Number.isFinite(v) ? v : null; },
  };
}
