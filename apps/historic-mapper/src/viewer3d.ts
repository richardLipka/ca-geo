// 3D view of the entity model: extruded footprints (buildings, wall), towers and gates as
// boxes with spires, and facet textures (walls / roofs) cut from a georeferenced plate.
// Scene units: metres, local origin near the old town; x = east, y = up, z = south.
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { getLang, setLang, t } from './i18n';
import type { Entity, Project } from './model';
import { activeIn } from './model';

const ORIGIN = [-822400, -1069700];
const P = (x: number, y: number) => new THREE.Vector3(x - ORIGIN[0], 0, -(y - ORIGIN[1]));
const TYPE_COL: Record<string, number> = { building: 0xd8c7b0, church: 0xc9b9a6, tower: 0xb9a99a, gate: 0xc29a6b, wall: 0xa59b8f };

interface Facets { ppm: number; buildings: { entity: string; walls: { edge: number; a: number[]; b: number[]; height: number; texture: string }[]; roof: { texture: string; origin: number[]; ppm: number } | null }[] }

async function main() {
  document.title = t('v3d.title');
  document.body.innerHTML = `<div id="v3d"></div><div class="v3dbar">
    <b>${t('v3d.title')}</b>
    <label><input type="checkbox" id="tex" checked> ${t('v3d.textures')}</label>
    <label>${t('map.year')} <output id="yo"></output><input type="range" id="yr" min="1290" max="2030" value="1618"></label>
    <label><input type="checkbox" id="all"> ${t('map.allYears')}</label>
    <a href="./">${t('v3d.back')}</a> <button type="button" id="lang">${t('btn.lang')}</button>
    <span class="muted" id="stat"></span></div>`;
  (document.getElementById('lang') as HTMLButtonElement).onclick = () => { setLang(getLang() === 'cs' ? 'en' : 'cs'); location.reload(); };
  const proj = (await (await fetch('/api/project/plzen')).json()) as Project;
  let facets: Facets | null = null;
  try { facets = await (await fetch('/data/historic/facets/te-1618/facets.json')).json(); } catch { /* no facets */ }
  const facetBy = new Map((facets?.buildings ?? []).map(b => [b.entity, b]));

  const host = document.getElementById('v3d')!;
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  host.appendChild(renderer.domElement);
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0xdfe6ea);
  const cam = new THREE.PerspectiveCamera(45, 1, 1, 20000); cam.position.set(-150, 380, 620);
  const ctl = new OrbitControls(cam, renderer.domElement); ctl.target.set(0, 0, 0); ctl.maxPolarAngle = Math.PI * 0.49;
  scene.add(new THREE.HemisphereLight(0xffffff, 0x88806f, 1.6));
  const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(-400, 600, 300); scene.add(sun);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(4000, 4000), new THREE.MeshLambertMaterial({ color: 0xc9d6b8 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -0.05; scene.add(ground);

  const loader = new THREE.TextureLoader(); const texCache = new Map<string, THREE.Texture>();
  const tex = (f: string) => { let x = texCache.get(f); if (!x) { x = loader.load('/data/historic/facets/te-1618/' + f); x.colorSpace = THREE.SRGBColorSpace; texCache.set(f, x); } return x; };
  const groups = new Map<string, THREE.Group>();
  const plainMat = (type: string) => new THREE.MeshLambertMaterial({ color: TYPE_COL[type] ?? 0xcccccc });

  function prism(e: Entity, h: number): THREE.Group {
    const g = new THREE.Group(); const ring = e.geom!.coords;
    const shape = new THREE.Shape(ring.map(([x, y]) => new THREE.Vector2(x - ORIGIN[0], y - ORIGIN[1])));
    const geo = new THREE.ExtrudeGeometry(shape, { depth: h, bevelEnabled: false });
    geo.rotateX(-Math.PI / 2); // shape plane XY → ground XZ, extrusion along +Y
    const m = new THREE.Mesh(geo, plainMat(e.type)); m.userData.base = true; g.add(m);
    const f = facetBy.get(e.id);
    if (f) {
      for (const w of f.walls) { // textured quad slightly in front of the wall
        const a = P(w.a[0], w.a[1]), b = P(w.b[0], w.b[1]); const len = a.distanceTo(b);
        const q = new THREE.Mesh(new THREE.PlaneGeometry(len, w.height), new THREE.MeshLambertMaterial({ map: tex(w.texture), side: THREE.DoubleSide }));
        const mid = a.clone().add(b).multiplyScalar(0.5); const dir = b.clone().sub(a).normalize();
        q.position.set(mid.x, w.height / 2, mid.z); q.rotation.y = -Math.atan2(dir.z, dir.x);
        const n = new THREE.Vector3(dir.z, 0, -dir.x); q.position.addScaledVector(n, -0.06);
        q.userData.facet = true; g.add(q);
      }
      if (f.roof) { // roof texture is an orthographic image of the footprint: UV = (X − x0, y1 − Y)·ppm / size
        const r = f.roof;
        const roofGeo = new THREE.ShapeGeometry(shape); roofGeo.rotateX(-Math.PI / 2);
        const pos = roofGeo.attributes.position; const px = new Float32Array(pos.count * 2);
        for (let i = 0; i < pos.count; i++) {
          const X = pos.getX(i) + ORIGIN[0], Y = -pos.getZ(i) + ORIGIN[1];
          px[2 * i] = (X - r.origin[0]) * r.ppm; px[2 * i + 1] = (r.origin[1] - Y) * r.ppm;
        }
        roofGeo.setAttribute('uv', new THREE.BufferAttribute(px.slice(), 2));
        const mat = new THREE.MeshLambertMaterial({ transparent: true, color: 0xffffff });
        const roof = new THREE.Mesh(roofGeo, mat);
        roof.position.y = h + 0.05; roof.userData.facet = true; g.add(roof);
        loader.load('/data/historic/facets/te-1618/' + r.texture, tx => {
          tx.colorSpace = THREE.SRGBColorSpace;
          const im = tx.image as HTMLImageElement, uv = roofGeo.attributes.uv as THREE.BufferAttribute;
          for (let i = 0; i < uv.count; i++) uv.setXY(i, px[2 * i] / im.width, 1 - px[2 * i + 1] / im.height);
          uv.needsUpdate = true; mat.map = tx; mat.needsUpdate = true;
        });
      }
    }
    return g;
  }
  function towerMesh(e: Entity, h: number): THREE.Group {
    const g = new THREE.Group(); const p = P(...(e.geom!.coords[0] as [number, number]));
    const s = e.type === 'gate' ? 12 : e.type === 'church' ? 0 : 8;
    if (s) { const b = new THREE.Mesh(new THREE.BoxGeometry(s, h, s), plainMat(e.type)); b.position.set(p.x, h / 2, p.z); g.add(b);
      const c = new THREE.Mesh(new THREE.ConeGeometry(s * 0.75, h * 0.35, 4), new THREE.MeshLambertMaterial({ color: 0x8a5a44 })); c.position.set(p.x, h + h * 0.175, p.z); c.rotation.y = Math.PI / 4; g.add(c); }
    return g;
  }
  let n = 0;
  for (const e of proj.entities) {
    if (!e.geom) continue; const h = e.height ?? (e.type === 'building' ? 8 : 0);
    let g: THREE.Group | null = null;
    if (e.geom.type === 'Polygon' && e.type === 'building') g = prism(e, h);
    else if (e.geom.type === 'Polygon' && e.type === 'wall') { // wall as a band along the ring
      g = new THREE.Group(); const r = e.geom.coords;
      for (let i = 0; i < r.length; i++) { const a = P(...(r[i] as [number, number])), b = P(...(r[(i + 1) % r.length] as [number, number])); const len = a.distanceTo(b);
        const m = new THREE.Mesh(new THREE.BoxGeometry(len, h || 8, 1.6), plainMat('wall')); const mid = a.clone().add(b).multiplyScalar(0.5);
        m.position.set(mid.x, (h || 8) / 2, mid.z); m.rotation.y = -Math.atan2(b.z - a.z, b.x - a.x); g.add(m); }
    } else if (e.geom.type === 'Point' && (e.type === 'tower' || e.type === 'gate') && h) g = towerMesh(e, h);
    else if (e.geom.type === 'Point' && e.id.endsWith('barth_tower')) g = towerMesh({ ...e, type: 'tower' }, h);
    if (g) { g.userData.entity = e; scene.add(g); groups.set(e.id, g); n++; }
  }
  const yr = document.getElementById('yr') as HTMLInputElement, all = document.getElementById('all') as HTMLInputElement, yo = document.getElementById('yo')!, texBox = document.getElementById('tex') as HTMLInputElement;
  const apply = () => {
    const year = all.checked ? null : +yr.value; yo.textContent = all.checked ? '' : yr.value;
    let vis = 0;
    groups.forEach(g => { const on = activeIn(g.userData.entity as Entity, year); g.visible = on; if (on) vis++;
      g.children.forEach(c => { if (c.userData.facet) c.visible = texBox.checked; }); });
    document.getElementById('stat')!.textContent = t('v3d.stat', { n: vis, f: facets?.buildings.length ?? 0 });
  };
  [yr, all, texBox].forEach(x => x.addEventListener('input', apply)); apply();
  const resize = () => { const w = host.clientWidth, h = host.clientHeight; renderer.setSize(w, h); cam.aspect = w / h; cam.updateProjectionMatrix(); };
  new ResizeObserver(resize).observe(host); resize();
  renderer.setAnimationLoop(() => { ctl.update(); renderer.render(scene, cam); });
  void n;
}
main();
