// Reference raster layers for the map view, all served in EPSG:5514 and loaded as plain
// <img> elements (no CORS needed). Historic plans come from the City of Plzeň ArcGIS
// server (GIS_Historicke); present-day layers from ČÚZK WMS.

export interface RefLayer { id: string; labelKey?: string; label?: string; url: (bbox: number[], w: number, h: number) => string }

const city = (svc: string, label: string): RefLayer => ({
  id: 'city-' + svc, label,
  url: (b, w, h) => `https://ags.plzen.eu/arcgis/rest/services/GIS_Historicke/${encodeURIComponent(svc)}/MapServer/export?bbox=${b.join(',')}&bboxSR=5514&imageSR=5514&size=${w},${h}&format=jpg&f=image`,
});
const wms = (id: string, labelKey: string, base: string, layers: string, fmt = 'image/jpeg'): RefLayer => ({
  id, labelKey,
  url: (b, w, h) => `${base}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=${layers}&STYLES=&SRS=EPSG:5514&BBOX=${b.join(',')}&WIDTH=${w}&HEIGHT=${h}&FORMAT=${encodeURIComponent(fmt)}`,
});

export const REF_LAYERS: RefLayer[] = [
  { id: 'none', labelKey: 'ref.none', url: () => '' },
  wms('cuzk-orto', 'ref.orto', 'https://ags.cuzk.gov.cz/arcgis1/services/ORTOFOTO/MapServer/WMSServer', '0'),
  wms('cuzk-ztm', 'ref.ztm', 'https://ags.cuzk.gov.cz/arcgis1/services/ZTM/ZTM10/MapServer/WMSServer', '0', 'image/png'),
  city('GIS_HIS_Plzen_1781', '1781 – situační plán / situation plan'),
  city('GIS_HIS_Plzen_1821', '1821 – J. z Tošenovic'),
  city('GIS_HIS_Cisarske_otisky', '1839–41 – stabilní katastr / stable cadastre (© ČÚZK)'),
  city('GIS_HIS_Plzen_1840', '1840'),
  city('GIS_HIS_Plzen_1864', '1864'),
  city('GIS_HIS_Plzen_1877_mesto', '1877'),
  city('GIS_HIS_Plzen_1881', '1881'),
  city('GIS_HIS_Plzen_1891', '1891'),
  city('GIS_HIS_Plzen_1893', '1893'),
  city('GIS_HIS_Plzen_1908', '1908'),
  city('GIS_HIS_Plzen_1938', '1938'),
  city('GIS_HIS_Plzen_1947', '1947'),
  city('GIS_HIS_Plzen_1971', '1971'),
];
