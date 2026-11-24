"""3D building models of the City of Plzeň (GIS_3D_budovy / GIS_Budovy_Plzen_2024, multipatch) for the
9 x 9 km growth frame → triangle meshes.

The ArcGIS query with multipatchOption=stripMaterials returns each multipatch as 'binaryPatches':
base64 of [uint32 type, uint32 raw size, uint32 compressed size, zlib(ESRI extended shape buffer)].
The shape buffer is the shapefile MultiPatch layout: bbox, part / point counts, part starts, part
types (0 strip, 1 fan, 2 outer ring, 3 inner ring, 4 first ring, 5 ring), XY, Z range, Z.
Rings are planar faces; they are triangulated in their own plane (fan for convex faces, constrained
Delaunay from shapely otherwise, holes kept).

usage: python city3d_mesh.py        (paths relative to the repository)
writes data/reference/plzen-3d/mp/page_*.json (raw responses, cached) and data/reference/plzen-3d/mesh.npz:
  oid, par, bud (per object), vstart (offsets into verts), verts (float32 x, y, z in EPSG:5514 metres,
  relative to ORIGIN for x / y), tris (int32, indices local to the object)
"""
import base64, json, os, struct, sys, time, urllib.parse, urllib.request, zlib
import numpy as np
import shapely
from shapely.geometry import Polygon

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'data', 'reference', 'plzen-3d')
MP = os.path.join(OUT, 'mp'); os.makedirs(MP, exist_ok=True)
URL = 'https://ags.plzen.eu/arcgis/rest/services/GIS_3D_budovy/GIS_Budovy_Plzen_2024/FeatureServer/1/query'
BBOX = (-826900, -1074200, -817900, -1065200)
ORIGIN = (-822396.8, -1069689.4)
BATCH = 150


def get(params):
    data = urllib.parse.urlencode(params).encode()
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(URL, data=data, headers={'User-Agent': 'historic-mapper/0.1'}), timeout=300).read())
        except Exception as e:
            print(' retry', i, e); time.sleep(5 * (i + 1))
    raise RuntimeError('query failed')


# ---- fetch (cached pages) ----
ids = get({'where': '1=1', 'geometry': ','.join(map(str, BBOX)), 'geometryType': 'esriGeometryEnvelope', 'inSR': 5514,
           'spatialRel': 'esriSpatialRelIntersects', 'returnIdsOnly': 'true', 'f': 'json'})['objectIds']
ids.sort(); print('objects', len(ids))
pages = [ids[i:i + BATCH] for i in range(0, len(ids), BATCH)]
for k, pg in enumerate(pages):
    p = os.path.join(MP, f'page_{k:04d}.json')
    if os.path.exists(p): continue
    r = get({'objectIds': ','.join(map(str, pg)), 'outFields': 'OBJECTID,PAR_ID,BUDID_VYH,RELVYS_BUD', 'returnGeometry': 'true', 'returnZ': 'true',
             'multipatchOption': 'stripMaterials', 'outSR': 5514, 'f': 'json'})
    json.dump(r, open(p, 'w'))
    if k % 20 == 0: print('page', k, '/', len(pages)); sys.stdout.flush()


# ---- decode + triangulate ----
def decode(b64):
    b = base64.b64decode(b64)
    _, usz, csz = struct.unpack('<III', b[:12])
    raw = zlib.decompress(b[12:12 + csz])
    o = 36
    nparts, npts = struct.unpack('<II', raw[o:o + 8]); o += 8
    starts = list(struct.unpack(f'<{nparts}I', raw[o:o + 4 * nparts])); o += 4 * nparts
    types = [t & 0xF for t in struct.unpack(f'<{nparts}I', raw[o:o + 4 * nparts])]; o += 4 * nparts
    xy = np.frombuffer(raw, '<f8', 2 * npts, o).reshape(-1, 2); o += 16 * npts + 16
    z = np.frombuffer(raw, '<f8', npts, o)
    return np.c_[xy, z], starts + [npts], types


def plane_tris(rings):
    """rings: [outer, hole, ...] arrays (k, 3) → triangles as arrays of 3D points"""
    P = rings[0]
    if len(P) > 1 and np.allclose(P[0], P[-1]): rings = [r[:-1] if np.allclose(r[0], r[-1]) else r for r in rings]; P = rings[0]
    if len(P) < 3: return []
    n = np.zeros(3)
    for i in range(len(P)):  # Newell normal
        a, b = P[i], P[(i + 1) % len(P)]
        n += [(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])]
    if np.linalg.norm(n) < 1e-9: return []
    ax = int(np.argmax(np.abs(n)))
    keep = [i for i in range(3) if i != ax]
    if len(rings) == 1:
        q = P[:, keep]
        if len(P) == 3: return [P]
        d = np.roll(q, -1, 0) - q
        cr = d[:, 0] * np.roll(d, -1, 0)[:, 1] - d[:, 1] * np.roll(d, -1, 0)[:, 0]
        if (cr >= -1e-9).all() or (cr <= 1e-9).all():
            return [np.array([P[0], P[i], P[i + 1]]) for i in range(1, len(P) - 1)]
    pts = np.vstack(rings)
    lookup = {tuple(np.round(p[keep], 4)): p for p in pts}
    try:
        poly = Polygon(rings[0][:, keep], [r[:, keep] for r in rings[1:] if len(r) >= 3])
        if not poly.is_valid: poly = poly.buffer(0)
        out = []
        for t in shapely.get_parts(shapely.constrained_delaunay_triangles(poly)):
            c = np.asarray(t.exterior.coords)[:3]
            tri = [lookup.get(tuple(np.round(p, 4))) for p in c]
            if any(v is None for v in tri):  # new vertex from buffer(0): interpolate the plane coordinate
                tri = [lookup.get(tuple(np.round(p, 4)), None) for p in c]
                if any(v is None for v in tri): continue
            out.append(np.array(tri))
        return out
    except Exception:
        return [np.array([P[0], P[i], P[i + 1]]) for i in range(1, len(P) - 1)]


def triangulate(pts, bounds, types):
    tris = []
    group = None
    for k, t in enumerate(types):
        part = pts[bounds[k]:bounds[k + 1]]
        if t == 0:
            tris += [part[i:i + 3] for i in range(len(part) - 2)]
        elif t == 1:
            tris += [np.array([part[0], part[i], part[i + 1]]) for i in range(1, len(part) - 1)]
        elif t in (2, 4):
            if group: tris += plane_tris(group)
            group = [part]
        elif t in (3, 5):
            if group: group.append(part)
            else: group = [part]
    if group: tris += plane_tris(group)
    return tris


oid, par, bud, vstart, V, T = [], [], [], [0], [], []
nv = 0
files = sorted(f for f in os.listdir(MP) if f.startswith('page_'))
for k, f in enumerate(files):
    for ft in json.load(open(os.path.join(MP, f)))['features']:
        g = ft.get('geometry') or {}
        if 'binaryPatches' not in g: continue
        pts, bounds, types = decode(g['binaryPatches'])
        tris = triangulate(pts, bounds, types)
        if not tris: continue
        tv = np.vstack(tris)  # (3m, 3)
        uv, inv = np.unique(np.round(tv, 3), axis=0, return_inverse=True)
        a = ft['attributes']
        oid.append(a['OBJECTID']); par.append(int(a['PAR_ID']) if str(a['PAR_ID'] or '').strip().isdigit() else 0); bud.append(a['BUDID_VYH'] or '')
        V.append(np.c_[uv[:, 0] - ORIGIN[0], uv[:, 1] - ORIGIN[1], uv[:, 2]].astype(np.float32))
        T.append(inv.reshape(-1, 3).astype(np.int32))
        nv += len(uv); vstart.append(nv)
    if k % 50 == 0: print('decoded', k, '/', len(files), 'objects', len(oid), 'verts', nv); sys.stdout.flush()
tstart = np.cumsum([0] + [len(t) for t in T])
np.savez_compressed(os.path.join(OUT, 'mesh.npz'), oid=np.array(oid), par=np.array(par, np.int64), bud=np.array(bud),
                    vstart=np.array(vstart, np.int64), tstart=tstart, verts=np.vstack(V), tris=np.vstack(T), origin=np.array(ORIGIN))
print('objects', len(oid), 'vertices', nv, 'triangles', int(tstart[-1]))
