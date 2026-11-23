// Animated schematic 3D growth model of Plzeň 1295–2020 (data from scripts/growth_model.py).
// All buildings are one merged mesh; a vertex shader shows / raises / lowers / removes each
// building from per-vertex attributes (origin, demolition, rebuild, gaps) and the uniform year.
// Scene units: metres from the square; x = east, y = up, z = south.
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { getLang, setLang, t } from './i18n';

interface Model {
  origin: [number, number]; frame: [number, number, number, number]; years: [number, number];
  classes: string[]; basis: string[]; events: { year: number; cs: string; en: string }[];
  villages: { name: string; xy: [number, number]; mention: number }[];
  grounds: { year: number; file: string; label?: string }[]; water?: { year: number; file: string }[]; n: number;
  terrain?: { file: string; size: number; zmin: number; scale: number };
  rings: number[][]; from: number[]; to: number[]; h0: number[]; h1: number[]; tR: number[]; gaps: number[][]; cls: number[]; basisIdx: number[];
  z?: number[]; ids?: string[];
}
interface ProjSource { id: string; title: string; kind: string; file: string; depicted?: [number, number]; made?: string; view?: View }
interface View { pos: number[]; target: number[]; fov: number; year: number }
interface Ann { id: string; sourceId: string; img: [number, number]; entityId: string | null; label?: string; confidence: 1 | 2 | 3; note?: string; useAsControl: boolean; kind?: string }

// default viewpoints for the views (direction from the town to the viewer in degrees from north,
// distance and height in metres); adjust in the page and save to the project
const VIEW_DEFAULTS: Record<string, { az: number; dist: number; h: number; fov: number; year: number }> = {
  'ottheinrich-1536': { az: 205, dist: 1600, h: 40, fov: 38, year: 1536 },
  'willenberg-1602': { az: 45, dist: 1500, h: 60, fov: 40, year: 1602 },
  'hollar-p812': { az: 200, dist: 1500, h: 50, fov: 40, year: 1650 },
  'te-1618': { az: 180, dist: 900, h: 750, fov: 45, year: 1618 },
  'isselburg-1618': { az: 180, dist: 900, h: 750, fov: 45, year: 1618 },
  'keller-1619': { az: 180, dist: 900, h: 750, fov: 45, year: 1619 },
  'hogenberg-1619': { az: 180, dist: 900, h: 750, fov: 45, year: 1619 },
  'merian-1650': { az: 180, dist: 900, h: 750, fov: 45, year: 1650 },
  'bodenehr-1700': { az: 180, dist: 900, h: 750, fov: 45, year: 1700 },
};
const CLS_KIND: Record<string, string> = { landmark: 'church', fort: 'wall', inner: 'house', suburb: 'house', glacis: 'house', village: 'house', rural: 'house', town: 'house', moat: 'other' };

const DATA = '/data/historic/growth/web/';
// colour by period of origin (place first built)
const PERIODS: [number, number, string][] = [
  [1295, 0xa9533f, 'g3d.p.medieval'], [1500, 0xb0603a, 'g3d.p.early'], [1650, 0xc98f4a, 'g3d.p.baroque'], [1840, 0xd9b86a, 'g3d.p.c19a'],
  [1880, 0xb8c46e, 'g3d.p.c19b'], [1919, 0x7fb08a, 'g3d.p.inter'], [1946, 0x5b95b0, 'g3d.p.social'], [1990, 0x6f6fb8, 'g3d.p.recent'],
];
const periodCol = (y: number) => { let c = PERIODS[0][1]; for (const [s, col] of PERIODS) if (y >= s) c = col; return c; };
// colour by kind of evidence (how the date was obtained)
const BASIS_COL = (b: string) => b === 'history' || b.startsWith('model 1618') ? 0x7a2e8c
  : b.startsWith('RÚIAN date') ? 0x1f7a4d : b.includes('RÚIAN') ? 0x4f9a6a : b.startsWith('map 1840') ? 0xc77d2a : 0x9aa3ab;
const BASIS_KEYS: [number, string][] = [[0x7a2e8c, 'g3d.b.history'], [0x1f7a4d, 'g3d.b.ruian'], [0x4f9a6a, 'g3d.b.ruianmap'], [0xc77d2a, 'g3d.b.pre1840'], [0x9aa3ab, 'g3d.b.map']];

async function main() {
  document.title = t('g3d.title');
  document.body.innerHTML = `<div id="g3d"></div><div id="labels"></div>
  <div class="bar top"><b>${t('g3d.title')}</b>
    <label>${t('g3d.colour')} <select id="mode"><option value="0">${t('g3d.byPeriod')}</option><option value="1">${t('g3d.byBasis')}</option></select></label>
    <label><input type="checkbox" id="mapg"> ${t('g3d.mapGround')}</label>
    <label><input type="checkbox" id="auto" checked> ${t('g3d.autoCam')}</label>
    <label>${t('g3d.view')} <select id="vsel"><option value="">–</option></select></label>
    <a href="./">${t('v3d.back')}</a> <button type="button" id="lang">${t('btn.lang')}</button></div>
  <div id="vpanel"><div class="vhead"><b id="vtitle"></b>
      <label>${t('g3d.opacity')} <input type="range" id="vop" min="0" max="1" step="0.05" value="1"></label>
      <label><input type="checkbox" id="vsil"> ${t('g3d.silhouette')}</label>
      <button type="button" id="vsave">${t('g3d.saveView')}</button></div>
    <div class="vimg"><img id="vimg" alt=""><canvas id="vcan"></canvas></div>
    <div class="vhelp muted" id="vhelp">${t('g3d.vhelp')}</div></div>
  <div id="legend" class="bar"></div>
  <div id="caption"></div>
  <div class="bar bottom">
    <button type="button" id="play">▶</button>
    <output id="yo" class="year"></output>
    <div class="tl"><canvas id="chart"></canvas><input type="range" id="yr" min="1295" max="2020" step="0.1" value="1295"></div>
    <label>${t('g3d.speed')} <select id="speed"><option value="a" selected>${t('g3d.adaptive')}</option><option value="5">5</option><option value="15">15</option><option value="40">40</option></select></label>
    <button type="button" id="rec">● ${t('g3d.record')}</button>
    <span id="stat" class="muted"></span></div>`;
  (document.getElementById('lang') as HTMLButtonElement).onclick = () => { setLang(getLang() === 'cs' ? 'en' : 'cs'); location.reload(); };
  const M = (await (await fetch(DATA + 'model.json')).json()) as Model;
  const ZS = M.z ?? new Array(M.n).fill(0), IDS = M.ids ?? new Array(M.n).fill('');
  const lang = getLang();

  // ---------- scene ----------
  const host = document.getElementById('g3d')!;
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0xdfe6ea); scene.fog = new THREE.Fog(0xdfe6ea, 6000, 16000);
  const cam = new THREE.PerspectiveCamera(40, 1, 2, 40000); cam.position.set(-260, 420, 620);
  const ctl = new OrbitControls(cam, renderer.domElement); ctl.maxPolarAngle = Math.PI * 0.47; ctl.enableDamping = true;
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8270, 1.5));
  const sun = new THREE.DirectionalLight(0xffffff, 1.7); sun.position.set(-500, 800, 350); scene.add(sun);

  const [fx0, fy0, fx1, fy1] = M.frame; const [OX, OY] = M.origin;
  const loader = new THREE.TextureLoader(); const gtex = new Map<string, THREE.Texture>();
  const groundTex = (f: string) => { let x = gtex.get(f); if (!x) { x = loader.load(DATA + f); x.colorSpace = THREE.SRGBColorSpace; x.anisotropy = 8; gtex.set(f, x); } return x; };
  const groundMat = new THREE.MeshLambertMaterial({ map: groundTex(M.grounds[0].file) });
  // terrain: ČÚZK DMR 5G heights encoded in an RGB PNG (R high byte, G low byte, 0.1 m), relative to zmin
  const TSEG = 450;
  const tgeo = new THREE.PlaneGeometry(fx1 - fx0, fy1 - fy0, TSEG, TSEG); tgeo.rotateX(-Math.PI / 2);
  let heights: Float32Array | null = null, hsize = 0;
  if (M.terrain) {
    const img = await new Promise<HTMLImageElement>((res, rej) => { const im = new Image(); im.onload = () => res(im); im.onerror = rej; im.src = DATA + M.terrain!.file; });
    const cv = document.createElement('canvas'); cv.width = img.width; cv.height = img.height;
    const g2 = cv.getContext('2d', { willReadFrequently: true })!; g2.drawImage(img, 0, 0);
    const px = g2.getImageData(0, 0, img.width, img.height).data; hsize = img.width;
    heights = new Float32Array(hsize * hsize);
    for (let i = 0; i < hsize * hsize; i++) heights[i] = (px[4 * i] * 256 + px[4 * i + 1]) * M.terrain.scale;
    const tp = tgeo.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i < tp.count; i++) {
      const u = (tp.getX(i) + (fx1 - fx0) / 2) / (fx1 - fx0), w = (tp.getZ(i) + (fy1 - fy0) / 2) / (fy1 - fy0); // w: 0 = north edge
      const c = Math.min(hsize - 1, Math.max(0, Math.round(u * (hsize - 1)))), r = Math.min(hsize - 1, Math.max(0, Math.round(w * (hsize - 1))));
      tp.setY(i, heights[r * hsize + c]);
    }
    tgeo.computeVertexNormals();
  }
  const terrainAt0 = (x: number, z: number) => {
    if (!heights) return 0;
    const u = (x + OX - fx0) / (fx1 - fx0), w = (fy1 - (OY - z)) / (fy1 - fy0);
    const c = Math.min(hsize - 1, Math.max(0, Math.round(u * (hsize - 1)))), r = Math.min(hsize - 1, Math.max(0, Math.round(w * (hsize - 1))));
    return heights[r * hsize + c];
  };
  const groundUni = { uWater: { value: null as THREE.Texture | null }, uDepth: { value: 2.0 } };
  groundMat.onBeforeCompile = sh => {
    Object.assign(sh.uniforms, groundUni);
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nuniform sampler2D uWater; uniform float uDepth;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\ntransformed.y -= uDepth * texture2D(uWater, uv).r;');
  };
  const wtex = new Map<string, THREE.Texture>();
  const waterTex = (f: string) => { let x = wtex.get(f); if (!x) { x = loader.load(DATA + f); x.colorSpace = THREE.NoColorSpace; wtex.set(f, x); } return x; };
  if (M.water?.length) groundUni.uWater.value = waterTex(M.water[0].file);
  else { const d = new THREE.DataTexture(new Uint8Array([0, 0, 0, 255]), 1, 1); d.needsUpdate = true; groundUni.uWater.value = d; }
  const ground = new THREE.Mesh<THREE.BufferGeometry, THREE.Material>(tgeo, groundMat);
  ground.position.set((fx0 + fx1) / 2 - OX, -0.05, -((fy0 + fy1) / 2 - OY)); scene.add(ground);

  // ---------- merged building mesh ----------
  let nv = 0, ni = 0;
  const tris: number[][] = [];
  for (let b = 0; b < M.n; b++) {
    const r = M.rings[b]; const k = r.length / 2;
    const contour = Array.from({ length: k }, (_, i) => new THREE.Vector2(r[2 * i] / 10, r[2 * i + 1] / 10));
    const tr = THREE.ShapeUtils.triangulateShape(contour, []);
    tris.push(tr.flat()); nv += 4 * k + k; ni += 6 * k + tr.length * 3;
  }
  const pos = new Float32Array(nv * 3), nor = new Float32Array(nv * 3), col = new Float32Array(nv * 3), col2 = new Float32Array(nv * 3);
  const aT = new Float32Array(nv * 4), aH = new Float32Array(nv * 2), aG = new Float32Array(nv * 4), aZ = new Float32Array(nv);
  const idx = new Uint32Array(ni), faceB = new Int32Array(ni / 3);
  const MOAT = M.classes.indexOf('moat');
  let v = 0, ii = 0;
  const c1 = new THREE.Color(), c2 = new THREE.Color();
  for (let b = 0; b < M.n; b++) {
    const r = M.rings[b]; const k = r.length / 2;
    c1.setHex(periodCol(M.from[b])); c2.setHex(BASIS_COL(M.basis[M.basisIdx[b]]));
    if (M.cls[b] === MOAT) { c1.setHex(0x6f9fc4); c2.setHex(0x6f9fc4); }
    const v0 = v, i0 = ii;
    const put = (x: number, y: number, u: number, nx: number, ny: number, nz: number) => {
      pos[3 * v] = x; pos[3 * v + 1] = u; pos[3 * v + 2] = -y; nor[3 * v] = nx; nor[3 * v + 1] = ny; nor[3 * v + 2] = nz;
      col[3 * v] = c1.r; col[3 * v + 1] = c1.g; col[3 * v + 2] = c1.b; col2[3 * v] = c2.r; col2[3 * v + 1] = c2.g; col2[3 * v + 2] = c2.b;
      aT[4 * v] = M.from[b]; aT[4 * v + 1] = M.to[b]; aT[4 * v + 2] = M.tR[b]; aT[4 * v + 3] = M.cls[b];
      aH[2 * v] = M.h0[b]; aH[2 * v + 1] = M.h1[b];
      const g = M.gaps[b]; aG[4 * v] = g[0]; aG[4 * v + 1] = g[1]; aG[4 * v + 2] = g[2]; aG[4 * v + 3] = g[3];
      aZ[v] = ZS[b];
      v++;
    };
    // orientation: walls face outwards for counter-clockwise rings (in map coordinates)
    let area = 0; for (let i = 0; i < k; i++) { const j = (i + 1) % k; area += r[2 * i] * r[2 * j + 1] - r[2 * j] * r[2 * i + 1]; }
    const s = area >= 0 ? 1 : -1;
    for (let i = 0; i < k; i++) {
      const j = (i + 1) % k;
      const x1 = r[2 * i] / 10, y1 = r[2 * i + 1] / 10, x2 = r[2 * j] / 10, y2 = r[2 * j + 1] / 10;
      const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1;
      const nx = s * dy / L, nz = s * dx / L; // outward normal in scene coords (z = −y)
      const w = v;
      put(x1, y1, 0, nx, 0, nz); put(x2, y2, 0, nx, 0, nz); put(x2, y2, 1, nx, 0, nz); put(x1, y1, 1, nx, 0, nz);
      if (s > 0) idx.set([w, w + 1, w + 2, w, w + 2, w + 3], ii); else idx.set([w, w + 2, w + 1, w, w + 3, w + 2], ii);
      ii += 6;
    }
    const rv = v;
    for (let i = 0; i < k; i++) put(r[2 * i] / 10, r[2 * i + 1] / 10, 1, 0, 1, 0);
    const tr = tris[b];
    for (let q = 0; q < tr.length; q += 3) {
      if (s > 0) { idx[ii++] = rv + tr[q]; idx[ii++] = rv + tr[q + 1]; idx[ii++] = rv + tr[q + 2]; }
      else { idx[ii++] = rv + tr[q]; idx[ii++] = rv + tr[q + 2]; idx[ii++] = rv + tr[q + 1]; }
    }
    void v0; faceB.fill(b, i0 / 3, ii / 3);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3)); geo.setAttribute('color2', new THREE.BufferAttribute(col2, 3));
  geo.setAttribute('aT', new THREE.BufferAttribute(aT, 4)); geo.setAttribute('aH', new THREE.BufferAttribute(aH, 2)); geo.setAttribute('aG', new THREE.BufferAttribute(aG, 4)); geo.setAttribute('aZ', new THREE.BufferAttribute(aZ, 1));
  geo.setIndex(new THREE.BufferAttribute(idx, 1));
  const uni = { uYear: { value: 1295 }, uMode: { value: 0 }, uRise: { value: 3 }, uSel: { value: -1 }, uSil: { value: 0 } };
  const aB = new Float32Array(nv); for (let f = 0; f < faceB.length; f++) { aB[idx[3 * f]] = faceB[f]; aB[idx[3 * f + 1]] = faceB[f]; aB[idx[3 * f + 2]] = faceB[f]; }
  geo.setAttribute('aB', new THREE.BufferAttribute(aB, 1));
  const mat = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide });
  mat.onBeforeCompile = sh => {
    Object.assign(sh.uniforms, uni);
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', `#include <common>
        uniform float uYear; uniform float uMode; uniform float uRise;
        attribute vec4 aT; attribute vec2 aH; attribute vec4 aG; attribute vec3 color2; attribute float aZ; attribute float aB;
        uniform float uSel; uniform float uSil;
        varying float vFresh; varying float vSel;`)
      .replace('#include <begin_vertex>', `
        float yr = uYear;
        float start = aT.x;
        if (aG.y > 0.0 && yr >= aG.y) start = max(start, aG.y);   // rebuilt after the first destruction
        if (aG.w > 0.0 && yr >= aG.w) start = max(start, aG.w);   // rebuilt after the second destruction
        bool vis = yr >= aT.x && yr < aT.y && !(yr >= aG.x && yr < aG.y) && !(yr >= aG.z && yr < aG.w);
        float rise = clamp((yr - start) / uRise, 0.0, 1.0);
        float fall = clamp((aT.y - yr) / 1.5, 0.0, 1.0);
        float h = (yr < aT.z ? aH.x : aH.y) * min(rise, fall);
        if (yr >= aT.z) h *= clamp((yr - aT.z) / uRise, 0.35, 1.0);
        vec3 transformed = vec3(position);
        transformed.y = vis ? aZ + position.y * max(h, 0.2) : aZ - 3.0;
        vSel = abs(aB - uSel) < 0.5 ? 1.0 : 0.0;
        vFresh = vis ? 1.0 - clamp((yr - max(start, aT.z < yr ? aT.z : start)) / 4.0, 0.0, 1.0) : 0.0;`)
      .replace('#include <color_vertex>', `#include <color_vertex>
        vColor.rgb = mix(color, color2, uMode);
        if (uSil > 0.5) vColor.rgb = vec3(0.25, 0.22, 0.2);`);
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\nvarying float vFresh; varying float vSel;')
      .replace('#include <color_fragment>', `#include <color_fragment>
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(1.0, 0.93, 0.55), 0.75 * vFresh);
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.9, 0.1, 0.5), vSel);`);
  };
  const mesh = new THREE.Mesh<THREE.BufferGeometry, THREE.Material>(geo, mat); mesh.frustumCulled = false; scene.add(mesh);

  // ---------- statistics for the chart and the automatic camera ----------
  const Y0 = M.years[0], Y1 = M.years[1];
  const visibleAt = (b: number, y: number) => y >= M.from[b] && y < M.to[b] && !(y >= M.gaps[b][0] && y < M.gaps[b][1]) && !(y >= M.gaps[b][2] && y < M.gaps[b][3]);
  const cx = M.rings.map(r => { let s = 0; for (let i = 0; i < r.length; i += 2) s += r[i]; return s / (r.length / 2) / 10; });
  const cy = M.rings.map(r => { let s = 0; for (let i = 1; i < r.length; i += 2) s += r[i]; return s / (r.length / 2) / 10; });
  const counts: number[] = [], radius: number[] = [];
  for (let y = Y0; y <= Y1; y += 5) {
    const ds: number[] = []; let n = 0;
    for (let b = 0; b < M.n; b++) if (visibleAt(b, y)) { n++; ds.push(Math.hypot(cx[b], cy[b])); }
    ds.sort((a, b) => a - b); counts.push(n); radius.push(ds.length ? ds[Math.floor(ds.length * 0.6)] : 300);
  }
  const atStep = (arr: number[], y: number) => { const f = (y - Y0) / 5, i = Math.min(arr.length - 2, Math.max(0, Math.floor(f))); const u = Math.min(1, f - i); return arr[i] * (1 - u) + arr[i + 1] * u; };

  // ---------- UI ----------
  const yr = document.getElementById('yr') as HTMLInputElement, yo = document.getElementById('yo') as HTMLOutputElement;
  const stat = document.getElementById('stat')!, caption = document.getElementById('caption')!, labels = document.getElementById('labels')!;
  const mode = document.getElementById('mode') as HTMLSelectElement, mapg = document.getElementById('mapg') as HTMLInputElement;
  const auto = document.getElementById('auto') as HTMLInputElement, speed = document.getElementById('speed') as HTMLSelectElement;
  const playBtn = document.getElementById('play') as HTMLButtonElement, recBtn = document.getElementById('rec') as HTMLButtonElement;
  const legend = document.getElementById('legend')!;
  const hex = (c: number) => '#' + c.toString(16).padStart(6, '0');
  const drawLegend = () => {
    const items = mode.value === '0' ? PERIODS.map(([s, c, k]) => [c, `${t(k)} (${s}–)`] as [number, string]) : BASIS_KEYS.map(([c, k]) => [c, t(k)] as [number, string]);
    legend.innerHTML = items.map(([c, l]) => `<span><i style="background:${hex(c)}"></i>${l}</span>`).join('') + `<span><i style="background:#fff08c"></i>${t('g3d.fresh')}</span>`;
  };
  mode.onchange = () => { uni.uMode.value = +mode.value; drawLegend(); }; drawLegend();
  const vlabels = M.villages.map(vl => { const d = document.createElement('div'); d.className = 'vlabel'; labels.appendChild(d); return { ...vl, el: d }; });

  const chart = document.getElementById('chart') as HTMLCanvasElement;
  const drawChart = () => {
    const w = chart.clientWidth, h = chart.clientHeight; chart.width = w * devicePixelRatio; chart.height = h * devicePixelRatio;
    const g = chart.getContext('2d')!; g.scale(devicePixelRatio, devicePixelRatio); g.clearRect(0, 0, w, h);
    const mx = Math.max(...counts), X = (y: number) => (y - Y0) / (Y1 - Y0) * w;
    g.fillStyle = 'rgba(140,59,46,.25)'; g.strokeStyle = '#8c3b2e'; g.beginPath(); g.moveTo(0, h);
    counts.forEach((c, i) => g.lineTo(X(Y0 + 5 * i), h - Math.sqrt(c / mx) * (h - 4))); g.lineTo(w, h); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = '#1f2427'; for (const e of M.events) g.fillRect(X(e.year), 0, 1, 5);
    g.fillStyle = '#1f7a4d'; for (const gr of M.grounds.slice(1)) g.fillRect(X(gr.year) - 1, h - 5, 3, 5);
  };
  drawChart();

  let year = 1295, playing = false;
  const setYear = (y: number) => {
    year = Math.max(Y0, Math.min(Y1, y)); uni.uYear.value = year; yr.value = String(year); yo.textContent = String(Math.floor(year));
    const ev = [...M.events].reverse().find(e => e.year <= year);
    if (ev && year - ev.year < 14) { caption.textContent = `${ev.year} — ${lang === 'cs' ? ev.cs : ev.en}`; caption.style.opacity = String(Math.min(1, (14 - (year - ev.year)) / 4)); }
    else caption.style.opacity = '0';
    const gr = mapg.checked ? [...M.grounds].reverse().find(g => g.year <= year + 0.01) ?? M.grounds[0] : M.grounds[0];
    const tx = groundTex(gr.file); if (groundMat.map !== tx) { groundMat.map = tx; groundMat.needsUpdate = true; }
    if (M.water?.length) { const wf = ([...M.water].reverse().find(w => w.year <= year + 0.01) ?? M.water[0]).file; groundUni.uWater.value = waterTex(wf); }
    stat.textContent = t('g3d.stat', { n: Math.round(atStep(counts, year)), g: gr.year > Y0 ? gr.year : '–' });
  };
  yr.oninput = () => { if (!exporting) setYear(+yr.value); };
  mapg.onchange = () => setYear(year);
  const startPlay = () => { if (year >= Y1 - 0.01) setYear(Y0); playing = true; playBtn.textContent = '❚❚'; };
  const stopPlay = () => { playing = false; playBtn.textContent = '▶'; };
  playBtn.onclick = () => (playing ? stopPlay() : startPlay());
  ctl.addEventListener('start', () => { auto.checked = false; });
  const rate = (y: number) => {
    if (speed.value !== 'a') return +speed.value;
    return y < 1780 ? 28 : y < 1840 ? 12 : y < 1960 ? 4.5 : 6; // years per second: slower when the town grows fast
  };

  // ---------- one animation step (shared by the live loop and the frame export) ----------
  let exporting = false;
  const resize = () => { if (exporting) return; const w = host.clientWidth, h = host.clientHeight; renderer.setSize(w, h); cam.aspect = w / h; cam.updateProjectionMatrix(); drawChart(); };
  addEventListener('resize', resize); resize();
  let az = -2.4;
  setYear(1295);
  const tmp = new THREE.Vector3();
  const labelPos = () => vlabels.map(l => {
    tmp.set(l.xy[0], terrainAt0(l.xy[0], -l.xy[1]) + 30, -l.xy[1]).project(cam);
    const show = year >= Math.max(l.mention, Y0) - 0.01 && tmp.z < 1 && Math.abs(tmp.x) < 1.05 && Math.abs(tmp.y) < 1.05;
    return { l, show, x: (tmp.x + 1) / 2, y: (1 - tmp.y) / 2 };
  });
  const step = (dt: number) => {
    if (playing) { setYear(year + rate(year) * dt); if (year >= Y1) stopPlay(); }
    if (auto.checked) { // slow orbit; distance follows the extent of the town
      az += dt * 0.05;
      const R = Math.max(380, atStep(radius, year)) * 2.1;
      const want = new THREE.Vector3(Math.cos(az) * R, terrainAt0(0, 0) + R * 0.62, Math.sin(az) * R);
      cam.position.lerp(want, Math.min(1, dt * 1.5)); ctl.target.lerp(new THREE.Vector3(0, terrainAt0(0, 0), 0), Math.min(1, dt * 1.5));
    }
    ctl.update();
    renderer.render(scene, cam);
  };

  // ---------- video export: deterministic frames (fixed 30 fps time step) with overlays drawn in ----------
  // frames are saved by the dev server to data/historic/growth/video/<run>/ and encoded by scripts/encode_video.py
  const comp = document.createElement('canvas');
  const composite = () => {
    const src = renderer.domElement, W = src.width, H = src.height, k = W / (exporting ? EXP_W : host.clientWidth);
    comp.width = W; comp.height = H; const g = comp.getContext('2d')!;
    g.drawImage(src, 0, 0);
    g.textBaseline = 'top';
    for (const p of labelPos()) if (p.show) {
      g.font = `600 ${12 * k}px system-ui`; g.lineWidth = 3 * k; g.strokeStyle = 'rgba(255,255,255,.9)'; g.fillStyle = '#1f2427';
      const s = `${p.l.name} (${p.l.mention})`; g.strokeText(s, p.x * W - 20 * k, p.y * H - 8 * k); g.fillText(s, p.x * W - 20 * k, p.y * H - 8 * k);
    }
    const box = (x: number, y: number, w: number, h: number, a: number) => { g.fillStyle = `rgba(31,36,39,${a})`; g.beginPath(); g.roundRect(x, y, w, h, 6 * k); g.fill(); };
    // year and building count
    box(16 * k, H - 86 * k, 270 * k, 70 * k, 0.78);
    g.fillStyle = '#fff'; g.font = `700 ${46 * k}px "Segoe UI", system-ui`; g.fillText(String(Math.floor(year)), 28 * k, H - 80 * k);
    { const gy = mapg.checked ? ([...M.grounds].reverse().find(q => q.year <= year + 0.01)?.year ?? Y0) : Y0;
      g.font = `${15 * k}px system-ui`;
      g.fillText(`${t('g3d.nBuildings')}: ${Math.round(atStep(counts, year))}`, 140 * k, H - 74 * k);
      g.fillText(`${t('g3d.mapShort')}: ${gy > Y0 ? gy : '–'}`, 140 * k, H - 50 * k); }
    // event caption
    const op = +caption.style.opacity || 0;
    if (op > 0.02 && caption.textContent) {
      g.font = `600 ${18 * k}px "Segoe UI", system-ui`; const tw = Math.min(g.measureText(caption.textContent).width, W * 0.8);
      g.globalAlpha = op; box((W - tw) / 2 - 14 * k, 18 * k, tw + 28 * k, 38 * k, 0.8);
      g.fillStyle = '#fff'; g.textAlign = 'center'; g.fillText(caption.textContent, W / 2, 28 * k, W * 0.8); g.textAlign = 'left'; g.globalAlpha = 1;
    }
    // title, legend, credits
    g.font = `700 ${15 * k}px system-ui`; g.fillStyle = '#1f2427'; g.fillText(t('g3d.title'), 16 * k, 14 * k);
    const items = mode.value === '0' ? PERIODS.map(([s, c, kk]) => [c, `${t(kk)} (${s}–)`] as [number, string]) : BASIS_KEYS.map(([c, kk]) => [c, t(kk)] as [number, string]);
    g.font = `${12 * k}px system-ui`;
    items.forEach(([c, l], i) => { g.fillStyle = hex(c); g.fillRect(16 * k, (40 + 17 * i) * k, 12 * k, 12 * k); g.fillStyle = '#1f2427'; g.fillText(l, 34 * k, (39 + 17 * i) * k); });
    g.font = `${11 * k}px system-ui`; g.fillStyle = 'rgba(31,36,39,.8)'; g.textAlign = 'right';
    g.fillText(t('g3d.credits'), W - 14 * k, H - 22 * k); g.textAlign = 'left';
    return comp;
  };
  const EXP_W = 1600, EXP_H = 900;
  const exportVideo = async (fps = 30) => {
    if (exporting) { exporting = false; return; }
    exporting = true; renderer.setAnimationLoop(null);
    // fixed output size, independent of the window; no user input while exporting
    const prevRatio = renderer.getPixelRatio();
    renderer.setPixelRatio(1); renderer.setSize(EXP_W, EXP_H, false); cam.aspect = EXP_W / EXP_H; cam.updateProjectionMatrix();
    ctl.enabled = false; playBtn.disabled = true; yr.disabled = true;
    const run = `plzen-growth-${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}`;
    recBtn.textContent = `■ ${t('g3d.stop')}`;
    setYear(Y0); auto.checked = true; playing = true; az = -2.4;
    const R0 = Math.max(380, atStep(radius, Y0)) * 2.1; cam.position.set(Math.cos(az) * R0, R0 * 0.62, Math.sin(az) * R0);
    let n = 0, tail = 3 * fps;
    while (exporting && (playing || tail-- > 0)) {
      step(1 / fps);
      const blob = await new Promise<Blob | null>(res => composite().toBlob(res, 'image/jpeg', 0.92));
      if (!blob) break;
      const r = await fetch(`/api/frame/${run}/${n}`, { method: 'PUT', body: blob }).catch(() => null);
      if (!r?.ok) { stat.textContent = t('g3d.saveFail'); break; }
      n++; if (n % 30 === 0) stat.textContent = `${t('g3d.export')}: ${n} · ${Math.floor(year)}`;
    }
    exporting = false; recBtn.textContent = `● ${t('g3d.record')}`;
    ctl.enabled = true; playBtn.disabled = false; yr.disabled = false; renderer.setPixelRatio(prevRatio); resize();
    stat.textContent = t('g3d.saved', { f: `data/historic/growth/video/${run}/ (${n})` });
    (window as unknown as Record<string, unknown>).__g3dExport = { run, frames: n };
    startLoop();
  };
  recBtn.onclick = () => { void exportVideo(); };

  // ---------- views (vedute, bird's-eye plates): the model seen from the view's direction ----------
  // Select a view → camera at its viewpoint and year, the drawing in the left panel. Click a building in
  // the 3D view (GPU picking) and then the same object in the drawing → annotation linking the drawing
  // to the building id (ruian:…, h1840:…, g1618-…, fort:…), saved to the project.
  const vsel = document.getElementById('vsel') as HTMLSelectElement, vimg = document.getElementById('vimg') as HTMLImageElement;
  const vcan = document.getElementById('vcan') as HTMLCanvasElement, vop = document.getElementById('vop') as HTMLInputElement;
  const vsil = document.getElementById('vsil') as HTMLInputElement, vsave = document.getElementById('vsave') as HTMLButtonElement;
  const vtitle = document.getElementById('vtitle')!, vhelp = document.getElementById('vhelp')!;
  type Proj = { sources: ProjSource[]; annotations: Ann[]; entities?: { id: string; name: string }[] } & Record<string, unknown>;
  let project: Proj | null = null;
  try { project = await (await fetch('/api/project/plzen')).json(); } catch { project = null; }
  const entName = new Map((project?.entities ?? []).map(e => [e.id, e.name]));
  const views = (project?.sources ?? []).filter(s => VIEW_DEFAULTS[s.id] || s.kind === 'panorama' || s.kind === 'birdseye');
  for (const s of views) vsel.add(new Option(`${s.title.slice(0, 48)}`, s.id));
  let vs: ProjSource | null = null, selB = -1;
  const terrainAt = (x: number, z: number) => { // scene coords → terrain height
    if (!heights) return 0;
    const u = (x + OX - fx0) / (fx1 - fx0), w = (fy1 - (OY - z)) / (fy1 - fy0);
    const c = Math.min(hsize - 1, Math.max(0, Math.round(u * (hsize - 1)))), r = Math.min(hsize - 1, Math.max(0, Math.round(w * (hsize - 1))));
    return heights[r * hsize + c];
  };
  const viewOf = (s: ProjSource): View => {
    if (s.view) return s.view;
    const d = VIEW_DEFAULTS[s.id] ?? { az: 180, dist: 1500, h: 60, fov: 40, year: s.depicted?.[0] ?? 1600 };
    const a = d.az * Math.PI / 180, x = Math.sin(a) * d.dist, z = -Math.cos(a) * d.dist;
    return { pos: [x, terrainAt(x, z) + d.h, z], target: [0, terrainAt(0, 0) + 15, 0], fov: d.fov, year: d.year };
  };
  const saveProject = async () => {
    if (!project) return false;
    const r = await fetch('/api/project/plzen', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(project) }).catch(() => null);
    return !!r?.ok;
  };
  const describe = (b: number) => b < 0 ? '' : `${IDS[b] || '#' + b} · ${entName.get(IDS[b]) ?? M.classes[M.cls[b]]} · ${Math.round(M.from[b])}${M.to[b] < 9999 ? '–' + Math.round(M.to[b]) : ''}`;
  const drawAnns = () => {
    const w = vimg.clientWidth, h = vimg.clientHeight; vcan.width = w; vcan.height = h;
    const g = vcan.getContext('2d')!; g.clearRect(0, 0, w, h);
    if (!vs || !project || !vimg.naturalWidth) return;
    const k = w / vimg.naturalWidth;
    g.font = '600 11px system-ui';
    for (const a of project.annotations.filter(a => a.sourceId === vs!.id)) {
      const b = a.entityId ? IDS.indexOf(a.entityId) : -1;
      g.beginPath(); g.arc(a.img[0] * k, a.img[1] * k, b === selB && b >= 0 ? 6 : 4, 0, 7);
      g.fillStyle = b >= 0 ? '#d6336c' : '#1c7ed6'; g.fill(); g.strokeStyle = '#fff'; g.lineWidth = 1.5; g.stroke();
      const lab = a.label || (a.entityId ? (entName.get(a.entityId) ?? a.entityId) : '');
      const showLab = b === selB && b >= 0 || (!!a.entityId && a.entityId.startsWith('g1618-') && !a.entityId.startsWith('g1618-bld') && !a.entityId.startsWith('g1618-cut'));
      if (lab && showLab) { g.lineWidth = 3; g.strokeStyle = 'rgba(255,255,255,.85)'; g.strokeText(lab.slice(0, 28), a.img[0] * k + 7, a.img[1] * k + 4); g.fillStyle = '#1f2427'; g.fillText(lab.slice(0, 28), a.img[0] * k + 7, a.img[1] * k + 4); }
    }
  };
  vimg.onload = () => drawAnns();
  vsel.onchange = () => {
    vs = views.find(s => s.id === vsel.value) ?? null;
    document.body.classList.toggle('vmode', !!vs); resize();
    if (!vs) { uni.uSel.value = -1; return; }
    vimg.src = vs.file; vtitle.textContent = vs.title;
    const v = viewOf(vs); auto.checked = false; stopPlay();
    cam.position.fromArray(v.pos); ctl.target.fromArray(v.target); cam.fov = v.fov; cam.updateProjectionMatrix(); setYear(v.year);
    vhelp.textContent = t('g3d.vhelp');
  };
  vop.oninput = () => { vimg.style.opacity = vop.value; };
  vsil.onchange = () => { uni.uSil.value = vsil.checked ? 1 : 0; ground.visible = !vsil.checked; scene.background = new THREE.Color(vsil.checked ? 0xffffff : 0xdfe6ea); };
  vsave.onclick = async () => {
    if (!vs) return;
    vs.view = { pos: cam.position.toArray(), target: ctl.target.toArray(), fov: cam.fov, year: Math.round(year) };
    vhelp.textContent = (await saveProject()) ? t('g3d.viewSaved') : t('g3d.saveFail');
  };
  // GPU picking: the buildings drawn with their index as colour into a 1 × 1 target at the mouse position
  const pickMat = new THREE.ShaderMaterial({
    uniforms: uni,
    vertexShader: `uniform float uYear; uniform float uRise;
      attribute vec4 aT; attribute vec2 aH; attribute vec4 aG; attribute float aZ; attribute float aB; varying float vB;
      void main() {
        float yr = uYear; float start = aT.x;
        if (aG.y > 0.0 && yr >= aG.y) start = max(start, aG.y);
        if (aG.w > 0.0 && yr >= aG.w) start = max(start, aG.w);
        bool vis = yr >= aT.x && yr < aT.y && !(yr >= aG.x && yr < aG.y) && !(yr >= aG.z && yr < aG.w);
        float h = (yr < aT.z ? aH.x : aH.y) * min(clamp((yr - start) / uRise, 0.0, 1.0), clamp((aT.y - yr) / 1.5, 0.0, 1.0));
        vec3 p = position; p.y = vis ? aZ + position.y * max(h, 0.2) : aZ - 3.0; vB = vis ? aB : -1.0;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
      }`,
    fragmentShader: `varying float vB;
      void main() { float id = floor(vB + 1.5); gl_FragColor = vec4(mod(id, 256.0), mod(floor(id / 256.0), 256.0), floor(id / 65536.0), 255.0) / 255.0; }`,
    side: THREE.DoubleSide,
  });
  const pickRT = new THREE.WebGLRenderTarget(1, 1), black = new THREE.MeshBasicMaterial({ color: 0x000000 });
  const pick = (ev: MouseEvent) => {
    const rect = renderer.domElement.getBoundingClientRect(), dpr = renderer.getPixelRatio();
    const W = rect.width * dpr, H = rect.height * dpr;
    cam.setViewOffset(W, H, (ev.clientX - rect.left) * dpr, (ev.clientY - rect.top) * dpr, 1, 1);
    const gm = ground.material, mm = mesh.material;
    ground.material = black; mesh.material = pickMat;
    renderer.setRenderTarget(pickRT); renderer.render(scene, cam); renderer.setRenderTarget(null);
    ground.material = gm; mesh.material = mm; cam.clearViewOffset();
    const px = new Uint8Array(4); renderer.readRenderTargetPixels(pickRT, 0, 0, 1, 1, px);
    return px[0] + px[1] * 256 + px[2] * 65536 - 1;
  };
  let down: [number, number] | null = null;
  renderer.domElement.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
  renderer.domElement.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4) return; // a drag, not a click
    const b = pick(e); selB = b; uni.uSel.value = b;
    vhelp.textContent = b >= 0 ? `${t('g3d.selected')}: ${describe(b)}` : t('g3d.vhelp');
    drawAnns();
  });
  vcan.addEventListener('click', async e => {
    if (!vs || !project || !vimg.naturalWidth) return;
    const rect = vcan.getBoundingClientRect(), k = vimg.naturalWidth / rect.width;
    const x = (e.clientX - rect.left) * k, y = (e.clientY - rect.top) * k;
    const near = project.annotations.find(a => a.sourceId === vs!.id && Math.hypot(a.img[0] - x, a.img[1] - y) < 8 * k);
    if (e.shiftKey && near) { project.annotations = project.annotations.filter(a => a !== near); await saveProject(); drawAnns(); return; }
    if (near && !e.altKey) { const b = near.entityId ? IDS.indexOf(near.entityId) : -1; selB = b; uni.uSel.value = b; vhelp.textContent = describe(b) || near.entityId || ''; drawAnns(); return; }
    if (selB < 0) { vhelp.textContent = t('g3d.pickFirst'); return; }
    project.annotations.push({ id: 'g3d-' + Date.now().toString(36), sourceId: vs.id, img: [Math.round(x), Math.round(y)], entityId: IDS[selB] || null,
      confidence: 2, useAsControl: false, kind: CLS_KIND[M.classes[M.cls[selB]]] ?? 'other', note: `growth model: ${describe(selB)}` });
    vhelp.textContent = (await saveProject()) ? `${t('g3d.linked')}: ${describe(selB)}` : t('g3d.saveFail');
    drawAnns();
  });
  addEventListener('resize', () => drawAnns());
  // labels of landmarks (churches, gates, towers, monasteries) in the view mode
  const lmarks: { b: number; el: HTMLDivElement }[] = [];
  const seen = new Set<string>();
  for (let b = 0; b < M.n; b++) {
    const id = IDS[b];
    if (!id.startsWith('g1618-') || id === 'g1618-wall' || seen.has(id)) continue;
    seen.add(id); const el = document.createElement('div'); el.className = 'vlabel lm'; el.textContent = (entName.get(id) ?? id).replace(/\s*\(.*\)\s*/g, ' ').replace(/ – .*/, '').trim(); labels.appendChild(el); lmarks.push({ b, el });
  }
  const tmp2 = new THREE.Vector3();
  const drawLandmarks = () => {
    const rect = host.getBoundingClientRect();
    for (const { b, el } of lmarks) {
      const on = !!vs && visibleAt(b, year);
      if (on) { tmp2.set(cx[b], ZS[b] + M.h1[b] + 4, -cy[b]).project(cam); }
      const show = on && tmp2.z < 1 && Math.abs(tmp2.x) < 1 && Math.abs(tmp2.y) < 1;
      el.style.display = show ? 'block' : 'none';
      if (show) el.style.transform = `translate(${rect.left + (tmp2.x + 1) / 2 * rect.width}px, ${rect.top + (1 - tmp2.y) / 2 * rect.height}px)`;
    }
  };

  // ---------- live loop ----------
  let last = performance.now();
  const startLoop = () => {
    last = performance.now();
    renderer.setAnimationLoop(now => {
      const dt = Math.min(0.1, (now - last) / 1000); last = now;
      step(dt);
      const hr = host.getBoundingClientRect();
      for (const p of labelPos()) {
        p.l.el.style.display = p.show ? 'block' : 'none';
        if (p.show) { p.l.el.style.transform = `translate(${hr.left + p.x * hr.width}px, ${hr.top + p.y * hr.height}px)`; p.l.el.textContent = `${p.l.name} (${p.l.mention})`; }
      }
      drawLandmarks();
    });
  };
  startLoop();
  Object.assign(window as unknown as Record<string, unknown>, { __g3d: { setYear, uni, cam, ctl, M, exportVideo, pick } });
}

main();
