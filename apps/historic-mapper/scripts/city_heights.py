"""Download building heights of the City of Plzeň 3D building model 2024 (ArcGIS REST, attributes
only: ISKN building id, parcel id, relative height of the building and of the eaves) for joining to
the RÚIAN footprints (isknbudovaid / identifikacniparcela).

usage: python city_heights.py out.json
"""
import json, sys, time, urllib.parse, urllib.request

URL = 'https://ags.plzen.eu/arcgis/rest/services/GIS_3D_budovy/GIS_Budovy_Plzen_2024/MapServer/1/query'
out, off, page = [], 0, 2000
while True:
    q = URL + '?' + urllib.parse.urlencode({'where': '1=1', 'outFields': 'BUDID_VYH,PAR_ID,RELVYS_BUD,RELVYS_OKA', 'returnGeometry': 'false',
                                             'orderByFields': 'OBJECTID', 'resultOffset': off, 'resultRecordCount': page, 'f': 'json'})
    for i in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(q, headers={'User-Agent': 'Mozilla/5.0'}), timeout=180).read()); break
        except Exception as e:
            print('retry', e); time.sleep(5)
    fs = r.get('features', [])
    for f in fs:
        a = f['attributes']
        out.append([(a['BUDID_VYH'] or '').strip(), (a['PAR_ID'] or '').strip(), a['RELVYS_BUD'], a['RELVYS_OKA']])
    off += len(fs); print(off)
    if len(fs) < page: break
json.dump({'fields': ['budid', 'parid', 'h_roof', 'h_eaves'], 'rows': out}, open(sys.argv[1], 'w'))
print('rows', len(out))
