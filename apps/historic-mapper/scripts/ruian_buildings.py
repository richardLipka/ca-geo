"""Download present building footprints (RÚIAN stavební objekty, ČÚZK ArcGIS REST) for the
9 x 9 km growth frame, with completion date, number of floors and use.

usage: python ruian_buildings.py out.geojson
"""
import json, sys, time, urllib.parse, urllib.request

BBOX = (-826900, -1074200, -817900, -1065200)
URL = 'https://ags.cuzk.gov.cz/arcgis/rest/services/RUIAN/MapServer/3/query'
FIELDS = 'kod,dokonceni,pocetpodlazi,zpusobvyuzitikod,typstavebnihoobjektukod,zastavenaplocha,cisladomovni,druhkonstrukcekod,castobce,isknbudovaid,identifikacniparcela'


def get(params):
    q = URL + '?' + urllib.parse.urlencode(params)
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(q, headers={'User-Agent': 'Mozilla/5.0'}), timeout=180).read())
        except Exception as e:
            print('retry', e); time.sleep(5)
    raise RuntimeError('query failed')


feats, off, page = [], 0, 2000
while True:
    r = get({'where': '1=1', 'geometry': ','.join(map(str, BBOX)), 'geometryType': 'esriGeometryEnvelope', 'inSR': 5514,
             'outSR': 5514, 'spatialRel': 'esriSpatialRelIntersects', 'outFields': FIELDS, 'returnGeometry': 'true',
             'orderByFields': 'objectid', 'resultOffset': off, 'resultRecordCount': page, 'f': 'json'})
    fs = r.get('features', [])
    for f in fs:
        g = f.get('geometry')
        if not g or not g.get('rings'): continue
        feats.append({'type': 'Feature', 'properties': f['attributes'],
                      'geometry': {'type': 'Polygon', 'coordinates': [[[round(x, 2), round(y, 2)] for x, y in ring] for ring in g['rings']]}})
    print(off, len(fs)); off += len(fs)
    if len(fs) < page: break
json.dump({'type': 'FeatureCollection', 'crs': 'EPSG:5514', 'features': feats}, open(sys.argv[1], 'w', encoding='utf-8'))
print('buildings', len(feats))
