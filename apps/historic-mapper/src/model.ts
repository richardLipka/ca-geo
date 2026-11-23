// Project data model: sources (images), control points, entities (real-world objects with
// map geometry and lifetime) and annotations (an image location that shows an entity).
// Coordinates on the map are EPSG:5514 (S-JTSK / Krovak East North, metres); image
// coordinates are pixels of the full-resolution source file (origin top-left, y down).

import type { Method, Vec2 } from './transform';

export type SourceKind = 'map' | 'birdseye' | 'panorama';
export type EntityType = 'building' | 'church' | 'tower' | 'gate' | 'bastion' | 'wall' | 'moat' | 'water' | 'bridge' | 'street' | 'other';
export const ENTITY_TYPES: EntityType[] = ['building', 'church', 'tower', 'gate', 'bastion', 'wall', 'moat', 'water', 'bridge', 'street', 'other'];
export type GeomType = 'Point' | 'LineString' | 'Polygon';

export interface Source {
  id: string;
  title: string;
  kind: SourceKind;
  made?: string; // date the source was made, free text
  depicted?: [number, number]; // years depicted
  holder?: string;
  licence?: string;
  page?: string; // landing page URL
  file: string; // URL of the local image, e.g. /data/historic/sources/te-1618.jpg
  method: Method; // transform used for map / bird's-eye sources
  useLinks: boolean; // use identity links (annotation ↔ entity point) as control points
  overlay: boolean; // draw warped image on the map
  opacity: number;
}

export interface Gcp { id: string; img: Vec2; map: Vec2; enabled: boolean }

export interface Entity {
  id: string;
  name: string;
  type: EntityType;
  geom: { type: GeomType; coords: Vec2[] } | null; // Point: 1 coord; Polygon: ring without closing vertex
  cp?: string; // house number (číslo popisné) with part of town, free text
  height?: number; // approximate height above ground in metres (for 3D views)
  validFrom?: number;
  validTo?: number;
  notes?: string;
}

export interface Annotation {
  id: string;
  sourceId: string;
  img: Vec2;
  entityId: string | null;
  label?: string; // legend letter or inscription
  confidence: 1 | 2 | 3; // 1 uncertain, 2 probable, 3 certain
  note?: string;
  useAsControl: boolean; // counts as a control point when the source uses links
  shape?: Vec2[]; // outline of the object in the image (polygon, pixels)
  kind?: AnnotationKind; // what the outlined piece shows
}

export type AnnotationKind = 'house' | 'roof' | 'tower' | 'church' | 'gate' | 'wall' | 'bridge' | 'other';
export const ANNOTATION_KINDS: AnnotationKind[] = ['house', 'roof', 'tower', 'church', 'gate', 'wall', 'bridge', 'other'];

export interface Project {
  format: 'ca-geo/historic-mapper';
  version: 1;
  crs: 'EPSG:5514';
  name: string;
  sources: Source[];
  gcps: Record<string, Gcp[]>;
  entities: Entity[];
  annotations: Annotation[];
}

export function emptyProject(name: string): Project {
  return { format: 'ca-geo/historic-mapper', version: 1, crs: 'EPSG:5514', name, sources: [], gcps: {}, entities: [], annotations: [] };
}

export const uid = (p: string) => `${p}-${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;

export function entityAnchor(e: Entity): Vec2 | null {
  if (!e.geom || !e.geom.coords.length) return null;
  const c = e.geom.coords;
  if (e.geom.type === 'Point') return c[0];
  if (e.geom.type === 'Polygon' && c.length >= 3) { // area centroid
    let a = 0, x = 0, y = 0;
    for (let i = 0; i < c.length; i++) {
      const [x0, y0] = c[i], [x1, y1] = c[(i + 1) % c.length], k = x0 * y1 - x1 * y0;
      a += k; x += (x0 + x1) * k; y += (y0 + y1) * k;
    }
    if (Math.abs(a) > 1e-9) return [x / (3 * a), y / (3 * a)];
  }
  return [c.reduce((s, p) => s + p[0], 0) / c.length, c.reduce((s, p) => s + p[1], 0) / c.length];
}

export function activeIn(e: Entity, year: number | null): boolean {
  if (year === null) return true;
  return (e.validFrom === undefined || e.validFrom <= year) && (e.validTo === undefined || e.validTo >= year);
}

/** Validate an imported object loosely and fill defaults. */
export function normaliseProject(o: unknown): Project {
  const p = o as Partial<Project>;
  if (!p || p.format !== 'ca-geo/historic-mapper') throw new Error('not a historic-mapper project');
  return {
    ...emptyProject(p.name ?? 'project'),
    ...p,
    sources: (p.sources ?? []).map(s => Object.assign({ method: 'affine', useLinks: true, overlay: true, opacity: 0.7 }, s) as Source),
    gcps: p.gcps ?? {},
    entities: p.entities ?? [],
    annotations: (p.annotations ?? []).map(a => Object.assign({ confidence: 2, useAsControl: true }, a) as Annotation),
  };
}
