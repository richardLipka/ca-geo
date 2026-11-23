"""Export all epochs that cover the surroundings of Plzeň into one common frame (EPSG:5514)
for the built-up growth analysis. Sources: city GIS_Historicke plans (ArcGIS export), CENIA
2nd / 3rd military survey and 1950s orthophoto (WMS), ČÚZK ZTM10 (present, WMS).

usage: python growth_export.py out_dir [m_per_px]
"""
import os, sys, time, urllib.request

out = sys.argv[1]; res = float(sys.argv[2]) if len(sys.argv) > 2 else 2.5
os.makedirs(out, exist_ok=True)
# 9 x 9 km around the old town (centre ≈ -822400, -1069700)
BBOX = (-826900, -1074200, -817900, -1065200)
W = H = int((BBOX[2] - BBOX[0]) / res)
b = ','.join(str(v) for v in BBOX)
city = lambda s: f'https://ags.plzen.eu/arcgis/rest/services/GIS_Historicke/{s}/MapServer/export?bbox={b}&bboxSR=5514&imageSR=5514&size={W},{H}&format=png&transparent=true&f=image'
wms = lambda base, layer, fmt='image/png': f'{base}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS={layer}&STYLES=&SRS=EPSG:5514&BBOX={b}&WIDTH={W}&HEIGHT={H}&FORMAT={fmt}&TRANSPARENT=TRUE'
EPOCHS = [
    ('1840_vm2', wms('https://gis.cenia.cz/mapcache/II_vojenske_mapovani/wms', 'II_vojenske_mapovani', 'image/jpeg')),
    ('1840_cadastre', city('GIS_HIS_Cisarske_otisky')),
    ('1880_vm3', wms('https://gis.cenia.cz/mapcache/III_vojenske_mapovani/wms', 'III_vojenske_mapovani', 'image/jpeg')),
    ('1891', city('GIS_HIS_Plzen_1891')), ('1895', city('GIS_HIS_Plzen_1895')), ('1912', city('GIS_HIS_Plzen_1912_50cm')),
    ('1926', city('GIS_HIS_Plze%C5%88_1926')), ('1931', city('GIS_HIS_Plzen_1931')), ('1938', city('GIS_HIS_Plzen_1938')),
    ('1947', city('GIS_HIS_Plzen_1947')),
    ('1953_orto', wms('https://gis.cenia.cz/mapcache/ortofotomapa_historicka/wms', 'orto', 'image/jpeg')),
    ('2025_ztm', wms('https://ags.cuzk.gov.cz/arcgis1/services/ZTM/ZTM10/MapServer/WMSServer', '0')),
]
for name, url in EPOCHS:
    ext = 'jpg' if 'jpeg' in url else 'png'
    p = os.path.join(out, f'{name}.{ext}')
    if os.path.exists(p): print('skip', name); continue
    for i in range(3):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'historic-mapper/0.1'}), timeout=180).read()
            open(p, 'wb').write(data); print(name, len(data)); break
        except Exception as e:
            print(name, 'retry', e); time.sleep(5)
print('frame', BBOX, W, H, res)
