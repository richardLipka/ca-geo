// Exports: project JSON, entities as GeoJSON (EPSG:5514 or WGS84), evidence table (CSV),
// control points for GDAL (gdal_translate -gcp + gdalwarp) and QGIS Georeferencer (.points).

import { entityAnchor, type Project, type Source } from './model';
import { toWgs } from './proj';
import { store } from './store';
import type { Vec2 } from './transform';

export function download(name: string, text: string, type = 'application/json') {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type }));
  a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

export function entitiesGeoJson(p: Project, wgs: boolean): string {
  const tr = (c: Vec2): Vec2 => (wgs ? toWgs(c) : c);
  const features = p.entities.filter(e => e.geom).map(e => {
    const g = e.geom!, cs = g.coords.map(tr);
    const geometry = g.type === 'Point' ? { type: 'Point', coordinates: cs[0] } : g.type === 'LineString' ? { type: 'LineString', coordinates: cs } : { type: 'Polygon', coordinates: [[...cs, cs[0]]] };
    const evidence = p.annotations.filter(a => a.entityId === e.id).map(a => ({ source: a.sourceId, img: a.img.map(v => Math.round(v)), label: a.label ?? null, confidence: a.confidence, note: a.note ?? null }));
    return { type: 'Feature', id: e.id, geometry, properties: { name: e.name, type: e.type, cp: e.cp ?? null, valid_from: e.validFrom ?? null, valid_to: e.validTo ?? null, notes: e.notes ?? null, evidence } };
  });
  const fc: Record<string, unknown> = { type: 'FeatureCollection', name: p.name, features };
  if (!wgs) fc.crs = { type: 'name', properties: { name: 'urn:ogc:def:crs:EPSG::5514' } };
  return JSON.stringify(fc, null, 1);
}

export function evidenceCsv(p: Project): string {
  const esc = (v: unknown) => { const s = v === undefined || v === null ? '' : String(v); return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  const rows = [['entity_id', 'entity_name', 'entity_type', 'cp', 'valid_from', 'valid_to', 'map_x', 'map_y', 'source_id', 'source_title', 'img_x', 'img_y', 'label', 'confidence', 'note']];
  for (const a of p.annotations) {
    const e = p.entities.find(x => x.id === a.entityId), s = p.sources.find(x => x.id === a.sourceId), m = e && entityAnchor(e);
    rows.push([e?.id ?? '', e?.name ?? '', e?.type ?? '', e?.cp ?? '', String(e?.validFrom ?? ''), String(e?.validTo ?? ''), m ? m[0].toFixed(2) : '', m ? m[1].toFixed(2) : '', a.sourceId, s?.title ?? '', a.img[0].toFixed(1), a.img[1].toFixed(1), a.label ?? '', String(a.confidence), a.note ?? ''].map(String));
  }
  return rows.map(r => r.map(esc).join(',')).join('\n');
}

/** GDAL commands: attach GCPs, then warp (TPS for tps/poly2, otherwise polynomial order 1). */
export function gdalScript(src: Source): string {
  const ctrl = store.controls(src);
  const file = src.file.split('/').pop() ?? 'source.jpg', base = file.replace(/\.[^.]+$/, '');
  const gcp = ctrl.map(c => `-gcp ${c.img[0].toFixed(2)} ${c.img[1].toFixed(2)} ${c.map[0].toFixed(3)} ${c.map[1].toFixed(3)}`).join(' \\\n  ');
  const warp = src.method === 'tps' ? '-tps' : src.method === 'poly2' ? '-order 2' : '-order 1';
  return `# ${src.title}\n# ${ctrl.length} control points (${src.method}); EPSG:5514\ngdal_translate -of GTiff -a_srs EPSG:5514 \\\n  ${gcp} \\\n  ${file} ${base}_gcp.tif\ngdalwarp -r bilinear ${warp} -t_srs EPSG:5514 -dstalpha ${base}_gcp.tif ${base}_5514.tif\n`;
}

/** QGIS Georeferencer .points file (pixel y is negative in QGIS convention). */
export function qgisPoints(src: Source): string {
  const ctrl = store.controls(src);
  return ['#CRS: EPSG:5514', 'mapX,mapY,sourceX,sourceY,enable,dX,dY,residual', ...ctrl.map(c => `${c.map[0]},${c.map[1]},${c.img[0]},${-c.img[1]},1,0,0,0`)].join('\n');
}
