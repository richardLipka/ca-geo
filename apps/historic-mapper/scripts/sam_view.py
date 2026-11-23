"""Automatic Segment Anything masks on a region of a veduta (test of automatic house cutting).

usage: python sam_view.py veduta.jpg x0,y0,x1,y1 checkpoint.pth out_prefix
writes <out_prefix>_masks.json (polygons in full-image pixels) and <out_prefix>_preview.jpg
"""
import json, sys
import cv2
import numpy as np
import torch
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

def imread(p): return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)
def imwrite(p, img): ok, b = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 88]); b.tofile(p)

path, box, ckpt, out = sys.argv[1:5]
x0, y0, x1, y1 = map(int, box.split(','))
img = imread(path); crop = img[y0:y1, x0:x1]
sam = sam_model_registry['vit_h'](checkpoint=ckpt).to('cuda' if torch.cuda.is_available() else 'cpu')
gen = SamAutomaticMaskGenerator(sam, points_per_side=64, pred_iou_thresh=0.84, stability_score_thresh=0.88, min_mask_region_area=60)
masks = gen.generate(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
A = crop.shape[0] * crop.shape[1]
keep = [m for m in masks if 150 < m['area'] < 0.05 * A]
keep.sort(key=lambda m: -m['area'])
vis = crop.copy(); polys = []
rng = np.random.default_rng(3)
for m in keep:
    cs, _ = cv2.findContours(m['segmentation'].astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 1.5, True).reshape(-1, 2)
    if len(c) < 3: continue
    col = tuple(int(v) for v in rng.integers(40, 230, 3))
    ov = vis.copy(); cv2.fillPoly(ov, [c], col); vis = cv2.addWeighted(ov, 0.45, vis, 0.55, 0)
    cv2.polylines(vis, [c], True, col, 2)
    polys.append({'area': int(m['area']), 'iou': round(float(m['predicted_iou']), 3), 'poly': (c + [x0, y0]).tolist()})
json.dump({'image': path, 'box': [x0, y0, x1, y1], 'masks': polys}, open(out + '_masks.json', 'w'))
imwrite(out + '_preview.jpg', vis)
print(f'{len(masks)} masks, kept {len(polys)}')
