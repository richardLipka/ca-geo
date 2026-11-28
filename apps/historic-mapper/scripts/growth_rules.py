"""Shared classification rules for the built-up growth maps (9 x 9 km frame, 2.5 m/px):
per-epoch building-pixel rules tuned to the cartographic style, map coverage, frame helpers."""
import cv2
import numpy as np

BBOX = (-826900, -1074200, -817900, -1065200); RES = 2.5; N = 3600
CORE = (-822400, -1069700)

def to_px(X, Y): return int((X - BBOX[0]) / RES), int((BBOX[3] - Y) / RES)
def to_map(c, r): return BBOX[0] + (c + 0.5) * RES, BBOX[3] - (r + 0.5) * RES

def imread(p):
    im = cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_UNCHANGED)
    alpha = None
    if im.ndim == 3 and im.shape[2] == 4: alpha = im[..., 3]; im = im[..., :3]
    return im, alpha

def hsv(im):
    h = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); return h[..., 0].astype(int) * 2, h[..., 1] / 255, h[..., 2] / 255  # hue in degrees

def dense(mask, k, thr):
    """fraction of mask pixels in a k x k window above thr (for hatched / line drawings)."""
    d = cv2.blur(mask.astype(np.float32), (k, k)); return d > thr

def rule(name, im, alpha=None):
    H, S, V = hsv(im)
    red = ((H < 22) | (H > 335)) & (S > 0.22) & (V > 0.35)
    if name == '1840_cadastre':  # carmine buildings only (at 2.5 m/px the yellow wooden-building class collides with field colours)
        return ((H < 15) | (H > 335)) & (S > 0.35) & (V > 0.4)
    if name == '1840_vm2':      # settlements drawn red / carmine on a pale base, 1:28 800
        return dense(((H < 20) | (H > 330)) & (S > 0.18) & (V > 0.3), 5, 0.35)
    if name in ('1880_vm3', '1891', '1912'):  # black / dark brown block hatching
        dark = V < (0.42 if name == '1880_vm3' else 0.45)
        return dense(dark, 9, 0.5 if name == '1880_vm3' else 0.38)
    if name == '1895':
        return dense(red | (V < 0.40), 7, 0.4)
    if name in ('1926', '1931', '1938'):
        return red
    if name == '1947':  # red / orange blocks in the west, grey-violet blocks in the east
        return red | ((H >= 15) & (H < 40) & (S > 0.35) & (V > 0.55)) | ((H >= 250) & (H < 335) & (S > 0.10) & (V > 0.45) & (V < 0.85))
    if name == '1821':          # carmine / dark pink buildings (fields are paler salmon)
        return ((H < 6) | (H > 335)) & (S > 0.25) & (V > 0.55)
    if name == '1877_mesto':    # buildings filled dark grey
        return dense((S < 0.22) & (V < 0.5), 3, 0.6)
    if name == '1881':          # maroon (stone) and magenta / pink (other) buildings
        return ((H > 295) | (H < 12)) & (S > 0.28) & (V < 0.85)
    if name == '1902':          # salmon-red houses, black industrial buildings
        return (((H < 22) | (H > 345)) & (S > 0.33) & (V > 0.55)) | dense(V < 0.22, 3, 0.7)
    if name == '1908':          # pink old town, orange / yellow newer buildings
        return (((H < 12) | (H > 340)) & (S > 0.25) & (V > 0.6)) | ((H >= 22) & (H < 58) & (S > 0.55) & (V > 0.7))
    if name == '2001_orto':     # same texture heuristic as the 1953 orthophoto
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
        mu = cv2.blur(g, (9, 9)); sd = np.sqrt(np.maximum(cv2.blur(g * g, (9, 9)) - mu * mu, 0))
        return dense((sd > 18) & (mu > 115), 11, 0.45)
    if name == '1953_orto':     # bright roofs + strong local texture (rough heuristic)
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
        mu = cv2.blur(g, (9, 9)); sd = np.sqrt(np.maximum(cv2.blur(g * g, (9, 9)) - mu * mu, 0))
        return dense((sd > 28) & (mu > 90), 15, 0.5)
    if name == '2025_ruian':    # RÚIAN building polygons (ČÚZK map service, transparent background)
        return alpha > 0 if alpha is not None else np.zeros(im.shape[:2], bool)
    if name == '2025_ztm':      # buildings dark grey, built-up area tint pink-grey
        bld = (S < 0.12) & (V > 0.45) & (V < 0.78)
        tint = ((H < 30) | (H > 320)) & (S > 0.06) & (S < 0.35) & (V > 0.75)
        return dense(bld, 5, 0.25) | dense(tint, 9, 0.6)
    return red

def coverage(name, im, alpha):
    if alpha is not None: m = alpha > 0
    else: m = ~((im > 245).all(2))
    return cv2.erode(m.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0

def building_mask(name, im, alpha):
    """building pixels and map coverage of an epoch raster (as growth_model.py uses them before the manual corrections)"""
    cov = coverage(name, im, alpha)
    b = rule(name, im, alpha) & cov
    if name == '1840_cadastre':  # add saturated yellow (wooden buildings); field colours are paler
        H, S, V = hsv(im); b |= (H >= 45) & (H < 65) & (S > 0.5) & (V > 0.6) & cov
    return b, cov

# 2nd military survey (1840_vm2): the CENIA rendering has no separable settlement colour at this
# scale — kept as a visual layer only, not classified
# density thresholds per epoch (share of building pixels in the 150 m window)
DENS_T = {'1840_cadastre': 0.10, '1880_vm3': 0.30, '1891': 0.25, '1895': 0.25, '1912': 0.2, '1953_orto': 0.25, '2025_ruian': 0.15}
YEAR = {'1840_cadastre': 1840, '1880_vm3': 1880, '1891': 1891, '1895': 1895, '1912': 1912, '1926': 1926,
        '1931': 1931, '1938': 1938, '1947': 1947, '1953_orto': 1953, '2025_ruian': 2025}  # epochs of the settlement-area classification
