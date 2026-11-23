"""Tiled WMS export for services that refuse large GetMap requests (CENIA mapcache):
fetch the common growth frame in tiles and mosaic them with OpenCV.

usage: python growth_tiles.py out_dir [m_per_px] [tile_px]
"""
import os, sys, time, urllib.request
import cv2
import numpy as np

out = sys.argv[1]; res = float(sys.argv[2]) if len(sys.argv) > 2 else 2.5; T = int(sys.argv[3]) if len(sys.argv) > 3 else 900
BBOX = (-826900, -1074200, -817900, -1065200)
N = int((BBOX[2] - BBOX[0]) / res); step = T * res
SERV = {
    '1840_vm2': ('https://gis.cenia.cz/mapcache/II_vojenske_mapovani/wms', 'II_vojenske_mapovani'),
    '1880_vm3': ('https://gis.cenia.cz/mapcache/III_vojenske_mapovani/wms', 'III_vojenske_mapovani'),
    '1953_orto': ('https://gis.cenia.cz/mapcache/ortofotomapa_historicka/wms', 'orto'),
    '2001_orto': ('https://geoportal.cuzk.gov.cz/WMS_ORTOFOTO_ARCHIV/WMService.aspx', '2001'),  # ČÚZK archive orthophoto (Plzeň flown 2001)
}
for name, (base, layer) in SERV.items():
    p = os.path.join(out, name + '.jpg')
    if os.path.exists(p): print('skip', name); continue
    mos = np.full((N, N, 3), 255, np.uint8); ok = 0
    for j in range(0, N, T):
        for i in range(0, N, T):
            w, h = min(T, N - i), min(T, N - j)
            x0 = BBOX[0] + i * res; y1 = BBOX[3] - j * res
            b = f'{x0},{y1 - h * res},{x0 + w * res},{y1}'
            url = f'{base}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS={layer}&STYLES=&SRS=EPSG:5514&BBOX={b}&WIDTH={w}&HEIGHT={h}&FORMAT=image/jpeg'
            for k in range(3):
                try:
                    data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'historic-mapper/0.1'}), timeout=120).read()
                    tile = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
                    if tile is not None: mos[j:j + h, i:i + w] = tile[:h, :w]; ok += 1
                    break
                except Exception as e:
                    print(name, 'retry', e); time.sleep(3)
    okb, buf = cv2.imencode('.jpg', mos, [cv2.IMWRITE_JPEG_QUALITY, 90]); buf.tofile(p)
    print(name, 'tiles', ok)
