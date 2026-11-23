import proj4 from 'proj4';
import type { Vec2 } from './transform';

// EPSG:5514 (S-JTSK / Krovak East North). proj4js returns East-North (negative) values for
// this definition. The 7-parameter towgs84 set is the commonly used one for the Czech
// Republic (accuracy ~1 m, sufficient for historical sources).
const KROVAK = '+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56 +units=m +no_defs';

export const toWgs = (p: Vec2): Vec2 => proj4(KROVAK, 'EPSG:4326', p) as Vec2;
export const fromWgs = (p: Vec2): Vec2 => proj4('EPSG:4326', KROVAK, p) as Vec2;
