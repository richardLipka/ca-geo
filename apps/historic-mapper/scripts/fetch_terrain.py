"""Download the ČÚZK DMR 5G terrain model (ImageServer exportImage, float32 TIFF) for the 9 x 9 km
growth frame.

usage: python fetch_terrain.py out.tif [m_per_px]
"""
import sys, time, urllib.parse, urllib.request

BBOX = (-826900, -1074200, -817900, -1065200)
out = sys.argv[1]; res = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
n = int((BBOX[2] - BBOX[0]) / res)
q = 'https://ags.cuzk.gov.cz/arcgis2/rest/services/dmr5g/ImageServer/exportImage?' + urllib.parse.urlencode({
    'bbox': ','.join(map(str, BBOX)), 'bboxSR': 5514, 'imageSR': 5514, 'size': f'{n},{n}', 'format': 'tiff',
    'pixelType': 'F32', 'interpolation': 'RSP_BilinearInterpolation', 'f': 'image'})
for i in range(4):
    try:
        data = urllib.request.urlopen(urllib.request.Request(q, headers={'User-Agent': 'Mozilla/5.0'}), timeout=300).read(); break
    except Exception as e:
        print('retry', e); time.sleep(5)
open(out, 'wb').write(data)
print(out, len(data), 'bytes', n, 'px', res, 'm/px')
