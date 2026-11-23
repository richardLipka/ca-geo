import { describe, expect, it } from 'vitest';
import { fit, fitPanorama, type Pair, type Vec2, type Method } from '../src/transform';

// Synthetic image → S-JTSK mapping: rotation 12°, scale 0.8 m/px, y flipped, offset
const ang = (12 * Math.PI) / 180, s = 0.8;
const truth = ([x, y]: Vec2): Vec2 => [
  -822800 + s * (Math.cos(ang) * x + Math.sin(ang) * y),
  -1069300 + s * (Math.sin(ang) * x - Math.cos(ang) * y),
];
const grid: Vec2[] = [];
for (let i = 0; i < 4; i++) for (let j = 0; j < 3; j++) grid.push([100 + i * 400, 80 + j * 450]);
const pairs: Pair[] = grid.map(img => ({ img, map: truth(img) }));

describe('fit', () => {
  for (const m of ['helmert', 'affine', 'projective', 'poly2', 'tps'] as Method[]) {
    it(`${m} recovers a similarity transform`, () => {
      const f = fit(m, pairs);
      expect(f.rmse).toBeLessThan(1e-3);
      const p: Vec2 = [777, 333];
      const q = f.forward(p), t = truth(p);
      expect(Math.hypot(q[0] - t[0], q[1] - t[1])).toBeLessThan(0.05);
      const back = f.inverse(q);
      expect(Math.hypot(back[0] - p[0], back[1] - p[1])).toBeLessThan(0.1);
    });
  }

  it('projective recovers a homography exactly', () => {
    const H = (p: Vec2): Vec2 => { const w = 1 + 2e-4 * p[0] - 1e-4 * p[1]; return [(-822000 + 0.9 * p[0] + 0.1 * p[1]) / w, (-1069000 + 0.05 * p[0] - 0.7 * p[1]) / w]; };
    const pp = grid.map(img => ({ img, map: H(img) }));
    const f = fit('projective', pp);
    const q = f.forward([500, 500]), t = H([500, 500]);
    expect(Math.hypot(q[0] - t[0], q[1] - t[1])).toBeLessThan(0.01);
  });

  it('leave-one-out detects an outlier', () => {
    const bad = pairs.map((p, i) => (i === 5 ? { ...p, map: [p.map[0] + 60, p.map[1]] as Vec2 } : p));
    const f = fit('affine', bad);
    const worst = f.loo.indexOf(Math.max(...f.loo));
    expect(worst).toBe(5);
    expect(f.looRmse).toBeGreaterThan(f.rmse);
  });

  it('rejects too few points', () => {
    expect(() => fit('projective', pairs.slice(0, 3))).toThrow();
  });
});

describe('fitPanorama', () => {
  it('recovers viewpoint and heading of a synthetic panorama', () => {
    const X0 = -822500, Y0 = -1066800, th = -Math.PI / 2 + 0.1, f = 1500, cx = 1200;
    const marks: Vec2[] = [[-823300, -1069500], [-822700, -1069300], [-822300, -1069700], [-821900, -1069400], [-821500, -1069900], [-822900, -1070100]];
    const obs = marks.map(map => ({ map, x: cx + f * Math.tan(Math.atan2(map[1] - Y0, map[0] - X0) - th) }));
    const r = fitPanorama(obs, cx);
    expect(r.rmsePx).toBeLessThan(0.5);
    expect(Math.hypot(r.X0 - X0, r.Y0 - Y0)).toBeLessThan(25);
    expect(r.project(marks[0])!).toBeCloseTo(obs[0].x, 0);
  });
});
