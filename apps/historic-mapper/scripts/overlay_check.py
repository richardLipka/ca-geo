"""Visual check of a georeference: warp a source image onto a map raster with a homography
(or other OpenCV-supported model) and write a blended comparison with control points.

usage: python overlay_check.py source.jpg map.jpg map_bbox(xmin,ymin,xmax,ymax) points.json out.jpg [crop_px]
points.json: [{"id":..,"img":[x,y],"map":[X,Y]}, ...]  (map in the CRS of map_bbox)
"""
import json, sys
import cv2
import numpy as np


def imread(p):
    """cv2.imread fails on non-ASCII Windows paths; decode from bytes instead."""
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)

def imwrite(p, img, params=()):
    ok, buf = cv2.imencode('.' + p.rsplit('.', 1)[-1], img, list(params)); buf.tofile(p)

src_path, map_path, bbox, pts_path, out = sys.argv[1:6]
xmin, ymin, xmax, ymax = map(float, bbox.split(','))
src = imread(src_path); base = imread(map_path)
H_, W_ = base.shape[:2]
to_px = lambda X, Y: ((X - xmin) / (xmax - xmin) * W_, (ymax - Y) / (ymax - ymin) * H_)
pts = json.load(open(pts_path, encoding='utf-8'))
s = np.array([p['img'] for p in pts], np.float64)
d = np.array([to_px(*p['map']) for p in pts], np.float64)
H, _ = cv2.findHomography(s, d, 0)
warp = cv2.warpPerspective(src, H, (W_, H_), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
mask = cv2.warpPerspective(np.full(src.shape[:2], 255, np.uint8), H, (W_, H_)) > 0
gray = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
ink = (gray < 120) & mask  # engraving lines
outimg = base.copy()
outimg[ink] = (0.25 * outimg[ink] + 0.75 * np.array([90, 30, 20])).astype(np.uint8)  # dark blue strokes
proj = cv2.perspectiveTransform(s.reshape(-1, 1, 2), H).reshape(-1, 2)
for p, q, r in zip(pts, d, proj):
    cv2.circle(outimg, (int(q[0]), int(q[1])), 7, (0, 200, 0), 2)           # map position
    cv2.line(outimg, (int(q[0]), int(q[1])), (int(r[0]), int(r[1])), (0, 0, 255), 2)  # residual
    cv2.putText(outimg, p['id'], (int(q[0]) + 8, int(q[1]) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 120, 0), 1, cv2.LINE_AA)
if len(sys.argv) > 6:
    x0, y0, x1, y1 = map(int, sys.argv[6].split(','))
    outimg = outimg[y0:y1, x0:x1]
imwrite(out, outimg, [cv2.IMWRITE_JPEG_QUALITY, 85])
res = np.hypot(*(proj - d).T) * (xmax - xmin) / W_
print(json.dumps({p['id']: round(float(v), 1) for p, v in zip(pts, res)}))
