"""Generated historic fabric and solid shapes for the growth model (growth_model.py).

- gable_house: a small house (box + gable roof) on a quadrilateral plot;
- perimeter_houses: narrow burgher houses around a block (gable to the street, rear courtyard);
- band_mesh: an earth body from a polygon (with holes) as stacked inset levels, triangulated by
  constrained Delaunay per band, so ramparts, bastions and ditches of any shape stay watertight;
- trough: a ditch (rim at the terrain, flat bottom) from a polygon with holes;
- courtyard_block: an extruded building with an inner courtyard.

Mesh dicts: {'v': [[x, y, z, mode]], 't': [[i, j, k]]}; mode 0 = z above the record base,
mode 1 = z above the local terrain (growth_model resolves it when writing mesh.bin).
"""
import math, random
import numpy as np
import shapely
from shapely.geometry import Polygon, MultiPolygon, LineString, Point
from shapely.ops import unary_union


# ---------------------------------------------------------------- houses
def gable_house(q, eave, roof, ridge_depth=True):
    """q: 4 corners (p0, p1 front edge; p2, p3 back), any orientation. Ridge along the depth
    (gable to the street) or along the front."""
    p = [tuple(c) for c in q]
    if not ridge_depth: p = [p[1], p[2], p[3], p[0]]
    V = [[x, y, 0.0, 0] for x, y in p] + [[x, y, eave, 0] for x, y in p]
    r0 = ((p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2); r1 = ((p[2][0] + p[3][0]) / 2, (p[2][1] + p[3][1]) / 2)
    V += [[r0[0], r0[1], eave + roof, 0], [r1[0], r1[1], eave + roof, 0]]
    T = []
    for i in range(4):
        j = (i + 1) % 4; T += [[i, j, 4 + j], [i, 4 + j, 4 + i]]
    T += [[4, 8, 9], [4, 9, 7], [8, 5, 6], [8, 6, 9], [4, 5, 8], [6, 7, 9]]   # roof planes, gables
    return {'v': V, 't': T}


def rect(c, u, w, d):
    """plot rectangle: front centre c, unit front direction u, width w, depth d (inwards = left normal)."""
    n = (-u[1], u[0])
    a = (c[0] - u[0] * w / 2, c[1] - u[1] * w / 2); b = (c[0] + u[0] * w / 2, c[1] + u[1] * w / 2)
    return [a, b, (b[0] + n[0] * d, b[1] + n[1] * d), (a[0] + n[0] * d, a[1] + n[1] * d)]


def ccw(pts):
    pts = [tuple(p) for p in pts]
    if pts[0] == pts[-1]: pts = pts[:-1]
    a2 = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return pts if a2 > 0 else pts[::-1]


def perimeter_houses(block, rng, depth=14.0, width=(6.5, 9.5), skip=None):
    """burgher houses along the edges of a block polygon (CCW: inside = left of each edge).
    Each edge is filled from its start corner to (length - depth): the next edge's first house takes
    the corner. Returns list of (plot quad, front midpoint, outward normal)."""
    P = ccw(list(block.simplify(1.5).exterior.coords))
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 6: continue
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        d = min(depth, L * 0.9)
        t, end = 0.0, max(L - d, 0.6 * L if L < 2 * d else L - d)
        while t < end - 3:
            w = min(rng.uniform(*width), end - t)
            if w < 4: break
            c = (a[0] + u[0] * (t + w / 2), a[1] + u[1] * (t + w / 2))
            q = rect(c, u, w - 0.15, d)
            pg = Polygon(q)
            if skip is not None and pg.intersection(skip).area > 0.3 * pg.area: t += w; continue
            if pg.intersection(block).area > 0.55 * pg.area:
                out.append((q, c, (u[1], -u[0])))
            t += w
    return out


def scatter_houses(area, rng, spacing=17.0, size=((6, 8), (8, 11)), avoid=None, max_n=10_000):
    """small houses scattered in a polygon with a minimum spacing (dart throwing), oriented along the
    nearest boundary edge (houses face the roads that bound the suburb blocks)."""
    if area.is_empty: return []
    minx, miny, maxx, maxy = area.bounds
    pts = []
    tries = int(area.area / (spacing * spacing) * 12) + 20
    edge = area.boundary
    for _ in range(tries):
        x, y = rng.uniform(minx, maxx), rng.uniform(miny, maxy)
        p = Point(x, y)
        if not area.contains(p) or (avoid is not None and avoid.contains(p)): continue
        if any((x - a) ** 2 + (y - b) ** 2 < spacing * spacing for a, b, *_ in pts): continue
        # orientation from the nearest boundary segment
        s = edge.project(p); q1 = edge.interpolate(max(s - 2, 0)); q2 = edge.interpolate(s + 2)
        ang = math.atan2(q2.y - q1.y, q2.x - q1.x)
        pts.append((x, y, ang, edge.distance(p)))
        if len(pts) >= max_n: break
    houses = []
    for x, y, ang, dist in pts:
        w = rng.uniform(*size[0]); d = rng.uniform(*size[1])
        u = (math.cos(ang), math.sin(ang)); n = (-u[1], u[0])
        c = (x - n[0] * d / 2, y - n[1] * d / 2)
        houses.append((rect(c, u, w, d), (x, y), dist))
    return houses


# ---------------------------------------------------------------- solids
def _parts(g):
    if g.is_empty: return []
    if isinstance(g, Polygon): return [g]
    return [p for p in getattr(g, 'geoms', []) if isinstance(p, Polygon) and not p.is_empty]


def _cdt(poly):
    try:
        return [list(t.exterior.coords)[:3] for t in shapely.get_parts(shapely.constrained_delaunay_triangles(poly))]
    except Exception:
        return []


def band_mesh(poly, levels, mode0=0, mode_all=None):
    """levels: [(inset m, z m)] starting with (0, z0); inset levels are mitred buffers. Triangles of each
    band between consecutive levels are a constrained Delaunay triangulation of the band polygon; each
    vertex takes the z of the level boundary it lies on (no new vertices are created)."""
    V, T, idx = [], [], {}

    def vid(x, y, z, mode):
        k = (round(x, 2), round(y, 2), round(z, 2))
        if k not in idx: idx[k] = len(V); V.append([x, y, z, mode])
        return idx[k]
    geoms = [poly]
    for d, _ in levels[1:]:
        g = poly.buffer(-d, join_style=2, mitre_limit=4.0)
        geoms.append(g if not g.is_empty else None)
    for k in range(len(levels) - 1):
        outer, inner = geoms[k], geoms[k + 1]
        if outer is None: break
        z0, z1 = levels[k][1], levels[k + 1][1]
        band = outer if inner is None else outer.difference(inner)
        on_in = None if inner is None else inner.boundary
        for part in _parts(band):
            for tri in _cdt(part):
                ids = []
                for x, y in tri:
                    zi = z1 if (on_in is not None and on_in.distance(Point(x, y)) < 0.05) else z0
                    ids.append(vid(x, y, zi, mode_all if mode_all is not None else (mode0 if zi == levels[0][1] else 0)))
                T.append(ids)
        if inner is None: break
    last = next((g for g in reversed(geoms) if g is not None), None)
    zl = levels[len([g for g in geoms if g is not None]) - 1][1]
    for part in _parts(last):
        for tri in _cdt(part): T.append([vid(x, y, zl, mode_all if mode_all is not None else 0) for x, y in tri])
    return {'v': V, 't': T}


def trough(poly, depth, slope=2.5, water=None):
    """ditch: rim on the terrain (mode 1, z 0), sides to `depth` below the base at `slope` inset, flat
    bottom; with water=z a flat water surface instead (mode 0)."""
    if water is not None:
        g = poly.buffer(-slope * 0.6, join_style=2)
        V, T, idx = [], [], {}
        for part in _parts(g):
            for tri in _cdt(part):
                ids = []
                for x, y in tri:
                    k = (round(x, 2), round(y, 2))
                    if k not in idx: idx[k] = len(V); V.append([x, y, water, 0])
                    ids.append(idx[k])
                T.append(ids)
        return {'v': V, 't': T}
    m = band_mesh(poly, [(0, 0.0), (slope, -depth)], mode0=1)
    return m


def extrude_with_holes(poly, h):
    """flat-roofed building of any polygon (holes = courtyards)."""
    V, T = [], []
    for ring in [poly.exterior] + list(poly.interiors):
        c = list(ring.coords)[:-1]; n = len(c); b = len(V)
        V += [[x, y, 0.0, 0] for x, y in c] + [[x, y, h, 0] for x, y in c]
        for i in range(n):
            j = (i + 1) % n; T += [[b + i, b + j, b + n + j], [b + i, b + n + j, b + n + i]]
    idx = {(round(v[0], 2), round(v[1], 2)): i for i, v in enumerate(V) if v[2] == h}
    for tri in _cdt(poly):
        ids = [idx.get((round(x, 2), round(y, 2))) for x, y in tri]
        if None not in ids: T.append(ids)
    return {'v': V, 't': T}


def courtyard_block(poly, h, wing=14.0):
    """a building around a courtyard: the footprint minus its inset (if the footprint has no courtyard)."""
    if len(poly.interiors) == 0:
        inner = poly.buffer(-wing, join_style=2)
        if not inner.is_empty and inner.area > 0.08 * poly.area:
            poly = poly.difference(inner)
            if isinstance(poly, MultiPolygon): poly = max(poly.geoms, key=lambda g: g.area)
    return extrude_with_holes(poly, h)


def connect(work, ring_outer, extra=6.0):
    """join a bastion to the main rampart: hull of the work and the stretch of the rampart's outer edge
    nearest to it (the gorge)."""
    edge = ring_outer.exterior
    s = edge.project(work.centroid)
    r = math.sqrt(work.area) * 0.55 + extra
    pts = [edge.interpolate((s + t) % edge.length).coords[0] for t in np.linspace(-r, r, 9)]
    return unary_union([work, Polygon(list(work.exterior.coords) + pts).convex_hull])


def transform_mesh(m, ang, src_c, dst_c, scale=1.0):
    ca, sa = math.cos(ang), math.sin(ang)
    V = [[dst_c[0] + scale * (ca * (x - src_c[0]) - sa * (y - src_c[1])), dst_c[1] + scale * (sa * (x - src_c[0]) + ca * (y - src_c[1])), z, mo]
         for x, y, z, mo in m['v']]
    return {'v': V, 't': m['t']}


def merge(meshes):
    V, T = [], []
    for m in meshes:
        b = len(V); V += m['v']; T += [[b + i for i in t] for t in m['t']]
    return {'v': V, 't': T}


def burgher_complex(q, eave, roof, stage, rng, block=None):
    """a burgher house on its plot after the isometric views of 1618 / 1650 (Theatrum Europaeum, Merian):
    front house with its gable to the street; from the Gothic stage on rear tracts and wings glued to it, so the
    inside of the block fills with roofs in both directions; in the Renaissance stage wide plots get a double roof.
    q: plot (p0, p1 street front; p2, p3 back, depth inwards)."""
    p0, p1, p2, p3 = [tuple(c) for c in q]
    w = math.dist(p0, p1); d = math.dist(p1, p2)
    u = ((p1[0] - p0[0]) / w, (p1[1] - p0[1]) / w); n = ((p3[0] - p0[0]) / d, (p3[1] - p0[1]) / d)
    at = lambda s, t: (p0[0] + u[0] * s + n[0] * t, p0[1] + u[1] * s + n[1] * t)
    quad = lambda s0, s1, t0, t1: [at(s0, t0), at(s1, t0), at(s1, t1), at(s0, t1)]
    inside = lambda qq: block is None or Polygon(qq).buffer(0).intersection(block).area > 0.85 * Polygon(qq).area
    parts = []
    if stage == 3 and w >= 10.5:   # double roof (two parallel gables to the street)
        parts += [gable_house(quad(0, w / 2, 0, d), eave, roof * 0.8, True), gable_house(quad(w / 2, w, 0, d), eave, roof * 0.8, True)]
    else:
        parts.append(gable_house(q, eave, roof, True))
    if stage >= 2:
        side = rng.random() < 0.5
        if stage == 3 or rng.random() < 0.5:          # side wing into the courtyard
            ww = min(rng.uniform(4.5, 6.0), w * 0.6); L = rng.uniform(8, 14) if stage == 3 else rng.uniform(6, 10)
            wq = quad(0, ww, d, d + L) if side else quad(w - ww, w, d, d + L)
            if inside(wq): parts.append(gable_house(wq, eave - rng.uniform(1.0, 2.0), roof * 0.7, True))
        if stage == 3 and rng.random() < 0.4:         # back house across the end of the plot
            L0 = d + rng.uniform(10, 14); bq = quad(0, w, L0, L0 + rng.uniform(6, 8))
            if inside(bq): parts.append(gable_house(bq, eave - rng.uniform(1.5, 2.5), roof * 0.75, False))
    return merge(parts)


# ---------------------------------------------------------------- shapes from veduta cut-outs
def silhouette_profile(png, levels=48):
    """width profile of a cut-out (alpha) from the ground (t = 0) to the top (t = 1), normalised by the width of
    the shaft (median width of 30–70 % of the height); returns [(t, w)] with w = 0 at the apex."""
    from PIL import Image
    a = np.array(Image.open(png).convert('RGBA'))[..., 3] > 128
    rows = np.where(a.any(1))[0]
    top, bot = rows.min(), rows.max()
    ws = []
    for r in range(top, bot + 1):
        xs = np.where(a[r])[0]; ws.append((xs.max() - xs.min() + 1) if len(xs) else 0)
    ws = np.array(ws[::-1], float)                 # bottom → top
    n = len(ws); shaft = np.median(ws[int(0.3 * n):int(0.7 * n)]) or ws.max()
    out = []
    for i in range(levels + 1):
        t = i / levels; k = min(n - 1, int(round(t * (n - 1))))
        w = float(np.median(ws[max(0, k - 2):k + 3])) / shaft
        out.append((t, min(w, 1.0 if t < 0.5 else 1.1)))   # lower rows may include neighbouring buildings
    out[-1] = (1.0, 0.0)
    return out


def loft(profile, centre, ang, base_w, height, nseg=4):
    """a tower: cross-sections (square for nseg = 4, round otherwise) scaled by the silhouette profile."""
    ca, sa = math.cos(ang), math.sin(ang)
    V, T = [], []
    for t, w in profile:
        r = base_w / 2 * w * (math.sqrt(2) if nseg == 4 else 1.0)
        for k in range(nseg):
            phi = 2 * math.pi * k / nseg + (math.pi / 4 if nseg == 4 else 0)
            x, y = r * math.cos(phi), r * math.sin(phi)
            V.append([centre[0] + ca * x - sa * y, centre[1] + sa * x + ca * y, t * height, 0])
    L = len(profile)
    for i in range(L - 1):
        for k in range(nseg):
            a0, a1 = i * nseg + k, i * nseg + (k + 1) % nseg
            b0, b1 = a0 + nseg, a1 + nseg
            T += [[a0, a1, b1], [a0, b1, b0]]
    return {'v': V, 't': T}


def extrude_profile(profile, p0, p1, width, height):
    """a nave / choir: the gable silhouette of a facade as the cross-section, extruded from p0 to p1."""
    L = math.dist(p0, p1); u = ((p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L); nrm = (-u[1], u[0])
    V, T = [], []
    sec = [(-w * width / 2, t * height) for t, w in profile] + [(w * width / 2, t * height) for t, w in reversed(profile)]
    m = len(sec)
    for end in (p0, p1):
        for s, z in sec: V.append([end[0] + nrm[0] * s, end[1] + nrm[1] * s, z, 0])
    for k in range(m - 1):
        T += [[k, k + 1, m + k + 1], [k, m + k + 1, m + k]]
    for base in (0, m):   # gable end faces (fan from the bottom centre)
        V.append([(V[base][0] + V[base + m - 1][0]) / 2, (V[base][1] + V[base + m - 1][1]) / 2, 0.0, 0]); c = len(V) - 1
        T += [[c, base + k, base + k + 1] for k in range(m - 1)]
    return {'v': V, 't': T}
