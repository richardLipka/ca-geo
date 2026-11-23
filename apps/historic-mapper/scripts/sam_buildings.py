"""Building footprints from a colour-coded historical plan (stable cadastre) with Segment
Anything (GPU) constrained by the colour classes.

1. colour classes (HSV): stone buildings (red / carmine), wooden buildings (yellow);
2. SAM automatic masks on overlapping tiles (thin parcel lines become mask boundaries,
   which splits the merged blocks of the colour mask into houses);
3. keep masks that are mostly building-coloured, of plausible size; resolve overlaps
   (larger IoU-dominant masks win), polygonise and transform to EPSG:5514.

usage: python sam_buildings.py plan.jpg xmin,ymin,xmax,ymax checkpoint.pth out.geojson [preview.jpg]
"""
import json, sys, time
import cv2
import numpy as np


def imread(p):
    """cv2.imread fails on non-ASCII Windows paths; decode from bytes instead."""
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)

def imwrite(p, img, params=()):
    ok, buf = cv2.imencode('.' + p.rsplit('.', 1)[-1], img, list(params)); buf.tofile(p)
import torch
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

img_path, bbox, ckpt, out = sys.argv[1:5]
preview = sys.argv[5] if len(sys.argv) > 5 else None
xmin, ymin, xmax, ymax = map(float, bbox.split(','))
bgr = imread(img_path); H, W = bgr.shape[:2]
mx = (xmax - xmin) / W; my = (ymax - ymin) / H  # metres per pixel

hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)  # H 0..180
h, s, v = hsv[..., 0].astype(int), hsv[..., 1] / 255, hsv[..., 2] / 255
red = (((h < 10) | (h > 165)) & (s > 0.25) & (v > 0.35))
yellow = ((h >= 17) & (h < 33) & (s > 0.30) & (v > 0.45))
building = red | yellow

dev = 'cuda' if torch.cuda.is_available() else 'cpu'
t0 = time.time()
sam = sam_model_registry['vit_h'](checkpoint=ckpt).to(dev)
gen = SamAutomaticMaskGenerator(sam, points_per_side=int(__import__('os').environ.get('SAM_PPS', 48)), pred_iou_thresh=0.80, stability_score_thresh=0.85,
                                crop_n_layers=0, min_mask_region_area=40)
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
TILE, STEP = int(__import__('os').environ.get('SAM_TILE', 400)), int(__import__('os').environ.get('SAM_STEP', 300))
masks = []
for y0 in range(0, max(H - TILE, 0) + 1, STEP):
    for x0 in range(0, max(W - TILE, 0) + 1, STEP):
        tile = rgb[y0:y0 + TILE, x0:x0 + TILE]
        for m in gen.generate(tile):
            seg = np.zeros((H, W), bool); seg[y0:y0 + tile.shape[0], x0:x0 + tile.shape[1]] = m['segmentation']
            masks.append((seg, m['predicted_iou']))
print(f'device {dev}; {len(masks)} raw masks in {time.time() - t0:.0f} s')

min_px, max_px = 15 / (mx * my), 2500 / (mx * my)  # 15 m² … 2500 m²
cand = []
for seg, iou in masks:
    a = int(seg.sum())
    if a < min_px or a > max_px: continue
    share = building[seg].mean()
    if share < 0.75: continue
    cand.append((seg, iou, a, share))
# smaller masks first (houses), drop masks mostly covered by already accepted ones
cand.sort(key=lambda c: c[2])
taken = np.zeros((H, W), bool); feats = []
for seg, iou, a, share in cand:
    if (seg & taken).sum() > 0.3 * a: continue
    seg = seg & ~taken & building
    if seg.sum() < min_px: continue
    taken |= seg
    cs, _ = cv2.findContours(seg.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    c = cv2.approxPolyDP(c, 1.5, True).reshape(-1, 2)
    if len(c) < 3: continue
    ring = [[round(xmin + (x + 0.5) * mx, 2), round(ymax - (y + 0.5) * my, 2)] for x, y in c]
    ring.append(ring[0])
    material = 'stone' if red[seg].mean() >= yellow[seg].mean() else 'wood'
    feats.append({'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [ring]},
                  'properties': {'area_m2': round(float(seg.sum() * mx * my), 1), 'material': material, 'sam_iou': round(float(iou), 3)}})
cover = taken.sum() / max(building.sum(), 1)
# fallback: building-coloured areas SAM did not split (dense block interiors) → one feature per component
rest = (building & ~taken).astype(np.uint8)
rest = cv2.morphologyEx(rest, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # drop parcel numbers and lines
n, lab, stats, _ = cv2.connectedComponentsWithStats(rest, 4)
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] < 30 / (mx * my): continue
    seg = lab == i
    cs, _ = cv2.findContours(seg.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 1.5, True).reshape(-1, 2)
    if len(c) < 3: continue
    ring = [[round(xmin + (x + 0.5) * mx, 2), round(ymax - (y + 0.5) * my, 2)] for x, y in c]; ring.append(ring[0])
    feats.append({'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [ring]},
                  'properties': {'area_m2': round(float(seg.sum() * mx * my), 1), 'material': 'stone' if red[seg].mean() >= yellow[seg].mean() else 'wood', 'sam_iou': None, 'block_remainder': True}})
    taken |= seg
cover_all = taken.sum() / max(building.sum(), 1)
json.dump({'type': 'FeatureCollection', 'name': 'stable-cadastre buildings (SAM)', 'crs': {'type': 'name', 'properties': {'name': 'urn:ogc:def:crs:EPSG::5514'}},
           'features': feats}, open(out, 'w'), indent=0)
print(f'{len(feats)} features ({sum(1 for f in feats if not f["properties"].get("block_remainder"))} SAM houses); coverage by SAM {cover:.1%}, with block remainders {cover_all:.1%}; total {time.time() - t0:.0f} s')
if preview:
    vis = (bgr * 0.45 + 255 * 0.55).astype(np.uint8)
    rng = np.random.default_rng(1)
    for f in feats:
        ring = np.array([[(X - xmin) / mx, (ymax - Y) / my] for X, Y in f['geometry']['coordinates'][0]], np.int32)
        col = tuple(int(c) for c in rng.integers(40, 220, 3))
        cv2.fillPoly(vis, [ring], col); cv2.polylines(vis, [ring], True, (30, 30, 30), 1)
    imwrite(preview, vis, [cv2.IMWRITE_JPEG_QUALITY, 85])
