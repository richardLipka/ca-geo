"""Colour segmentation experiment on a georeferenced plan export (numpy + GDAL only).

Classifies pixels into stone buildings (carmine/red), wooden buildings (yellow/ochre),
water (blue) and other, using HSV thresholds; writes a classified PNG preview and
per-class statistics, then counts connected components (4-neighbourhood) per class.
usage: python3 segment.py input.jpg out_prefix
"""
import sys, json
import numpy as np
from osgeo import gdal

src, out = sys.argv[1], sys.argv[2]
ds = gdal.Open(src)
rgb = np.stack([ds.GetRasterBand(i + 1).ReadAsArray().astype(np.float32) / 255 for i in range(3)], -1)
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mx, mn = rgb.max(-1), rgb.min(-1)
v = mx
s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
d = np.maximum(mx - mn, 1e-6)
h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60

cls = np.zeros(r.shape, np.uint8)  # 0 other
red = ((h < 20) | (h > 330)) & (s > 0.25) & (v > 0.35)
yellow = (h >= 35) & (h < 65) & (s > 0.30) & (v > 0.45)
blue = (h >= 170) & (h < 250) & (s > 0.15) & (v > 0.25)
cls[red] = 1; cls[yellow] = 2; cls[blue] = 3

def components(mask):
    """Count 4-connected components with a simple union-find over runs (no SciPy)."""
    lab = np.zeros(mask.shape, np.int32); parent = [0]
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    nxt = 1
    H, W = mask.shape
    for y in range(H):
        row = mask[y]; up = lab[y - 1] if y else None
        for x in np.flatnonzero(row):
            l = lab[y, x - 1] if x and row[x - 1] else 0
            u = up[x] if up is not None and mask[y - 1, x] else 0
            if l and u:
                a, c = find(l), find(u)
                lab[y, x] = min(a, c); parent[max(a, c)] = min(a, c)
            elif l or u:
                lab[y, x] = l or u
            else:
                parent.append(nxt); lab[y, x] = nxt; nxt += 1
    roots = {find(i) for i in range(1, nxt)}
    flat = lab[lab > 0]
    if flat.size == 0:
        return 0, []
    rootmap = np.array([find(i) for i in range(nxt)])
    flat = rootmap[flat]
    _, counts = np.unique(flat, return_counts=True)
    return len(roots), counts

stats = {}
for k, name in [(1, 'stone_red'), (2, 'wood_yellow'), (3, 'water_blue')]:
    m = cls == k
    n, counts = components(m)
    big = int((np.asarray(counts) >= 40).sum()) if n else 0
    stats[name] = {'pixel_share': round(float(m.mean()), 4), 'components': int(n), 'components_ge_40px': big}

pal = np.array([[245, 245, 240], [200, 30, 30], [230, 190, 0], [40, 110, 200]], np.uint8)
img = pal[cls]
drv = gdal.GetDriverByName('MEM').Create('', img.shape[1], img.shape[0], 3, gdal.GDT_Byte)
for i in range(3):
    drv.GetRasterBand(i + 1).WriteArray(img[..., i])
gdal.GetDriverByName('PNG').CreateCopy(out + '_classes.png', drv)
json.dump({'input': src, 'size': [int(r.shape[1]), int(r.shape[0])], 'classes': stats}, open(out + '_stats.json', 'w'), indent=1)
print(json.dumps(stats))
