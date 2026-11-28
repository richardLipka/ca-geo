import { defineConfig, type Plugin } from 'vite';
import { createReadStream, existsSync, mkdirSync, readFileSync, statSync, writeFileSync, renameSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const dataRoot = resolve(here, '../../data'); // repository data/ (not versioned)
const projectsDir = resolve(here, 'projects'); // saved annotation projects (versioned)
const manualDir = resolve(here, 'manual');     // manual corrections and reconstructions (versioned)
const repoRoot = resolve(here, '../..');
const PY = existsSync(join(repoRoot, '.venv', 'Scripts', 'python.exe')) ? join(repoRoot, '.venv', 'Scripts', 'python.exe') : join(repoRoot, '.venv', 'bin', 'python');
// pipeline steps of the workbench (workbench.html): scripts run one after another, output kept for the log panel
const STEPS: Record<string, string[][]> = {
  detect: [['map_buildings.py'], ['detect_footprints.py'], ['manual_maps.py']],
  model: [['growth_model.py'], ['check_epochs.py']],
  vedute: [['veduta_recon.py'], ['growth_model.py']],
};
const run = { step: '', running: false, code: null as number | null, log: [] as string[], started: 0 };
const APPDATA = new Set(['veduta_views.json', 'veduta_points.json']);

const MIME: Record<string, string> = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif', '.tif': 'image/tiff', '.webp': 'image/webp', '.json': 'application/json' };

/** Dev-only middleware: serve /data/* from the repository data folder and read/write projects. */
function localData(): Plugin {
  return {
    name: 'historic-mapper-local-data',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = decodeURIComponent((req.url ?? '').split('?')[0]);
        if (url.startsWith('/data/')) {
          const file = normalize(join(dataRoot, url.slice('/data/'.length)));
          if (!file.startsWith(dataRoot + sep) || !existsSync(file) || !statSync(file).isFile()) { res.statusCode = 404; return res.end(); }
          res.setHeader('Content-Type', MIME[extname(file).toLowerCase()] ?? 'application/octet-stream');
          return createReadStream(file).pipe(res);
        }
        if (url.startsWith('/manual/') || url.startsWith('/appdata/')) {   // manual edits (versioned) and small script outputs
          const name = url.split('/').pop() ?? '';
          const file = url.startsWith('/manual/') ? normalize(join(manualDir, name)) : (APPDATA.has(name) ? join(here, 'scripts', name) : '');
          if (!file || !existsSync(file)) { res.statusCode = 404; return res.end(); }
          res.setHeader('Content-Type', MIME[extname(file).toLowerCase()] ?? 'application/octet-stream'); res.setHeader('Cache-Control', 'no-store');
          return createReadStream(file).pipe(res);
        }
        const mm = url.match(/^\/api\/manual\/([a-z0-9_.-]+\.(json|png))$/);
        if (mm && req.method === 'POST') {   // JSON as it is, PNG as a data URL
          const parts: Buffer[] = [];
          req.on('data', (c: Buffer) => parts.push(c));
          req.on('end', () => {
            try {
              const body = Buffer.concat(parts); mkdirSync(manualDir, { recursive: true });
              const file = join(manualDir, mm[1]);
              const data = mm[2] === 'json' ? (JSON.parse(body.toString('utf8')), body) : Buffer.from(body.toString('utf8').split(',').pop() ?? '', 'base64');
              writeFileSync(file + '.tmp', data); renameSync(file + '.tmp', file);
              res.statusCode = 204; res.end();
            } catch { res.statusCode = 400; res.end(); }
          });
          return;
        }
        const fa = url.match(/^\/api\/facade\/(src|tex)\/([a-z0-9_.-]+\.(jpg|jpeg|png|webp))$/i);
        if (fa && req.method === 'POST') {   // facade images (data URL): sources and rectified textures → data/historic/growth/facades/ (not versioned)
          const parts: Buffer[] = []; let size = 0;
          req.on('data', (c: Buffer) => { parts.push(c); size += c.length; if (size > 120e6) req.destroy(); });
          req.on('end', () => {
            try {
              const dir = join(dataRoot, 'historic', 'growth', 'facades', fa[1]); mkdirSync(dir, { recursive: true });
              writeFileSync(join(dir, fa[2]), Buffer.from(Buffer.concat(parts).toString('utf8').split(',').pop() ?? '', 'base64'));
              res.statusCode = 204; res.end();
            } catch { res.statusCode = 400; res.end(); }
          });
          return;
        }
        const rm = url.match(/^\/api\/run(?:\/(\w+))?$/);
        if (rm) {   // pipeline: POST /api/run/<step> starts it, GET /api/run reports the state and the last lines
          if (req.method === 'POST' && rm[1]) {
            if (run.running || !STEPS[rm[1]]) { res.statusCode = 409; return res.end(); }
            Object.assign(run, { step: rm[1], running: true, code: null, log: [], started: Date.now() });
            const queue = [...STEPS[rm[1]]];
            const next_ = () => {
              const cmd = queue.shift();
              if (!cmd) { run.running = false; run.code = 0; run.log.push('— hotovo / done —'); return; }
              run.log.push(`$ python ${cmd.join(' ')}`);
              const p = spawn(PY, [join(here, 'scripts', cmd[0]), ...cmd.slice(1)], { cwd: repoRoot, env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONUNBUFFERED: '1' } });
              const add = (b: Buffer) => { for (const l of b.toString('utf8').split(/\r?\n/)) if (l.trim()) run.log.push(l); if (run.log.length > 2000) run.log.splice(0, run.log.length - 2000); };
              p.stdout.on('data', add); p.stderr.on('data', add);
              p.on('close', code => { if (code) { run.running = false; run.code = code; run.log.push(`— chyba / error ${code} —`); } else next_(); });
            };
            next_(); res.statusCode = 202; return res.end();
          }
          res.setHeader('Content-Type', 'application/json'); res.setHeader('Cache-Control', 'no-store');
          return res.end(JSON.stringify({ ...run, log: run.log.slice(-400) }));
        }
        const fm = url.match(/^\/api\/frame\/([\w-]+)\/(\d+)$/);
        if (fm && req.method === 'PUT') { // exported animation frame (JPEG) → data/historic/growth/video/<run>/
          const dir = join(dataRoot, 'historic', 'growth', 'video', fm[1]); mkdirSync(dir, { recursive: true });
          const parts: Buffer[] = []; let size = 0;
          req.on('data', (c: Buffer) => { parts.push(c); size += c.length; if (size > 50e6) req.destroy(); });
          req.on('end', () => { writeFileSync(join(dir, `f_${fm[2].padStart(6, '0')}.jpg`), Buffer.concat(parts)); res.statusCode = 204; res.end(); });
          return;
        }
        const m = url.match(/^\/api\/project\/([\w-]+)$/);
        if (m) {
          const file = join(projectsDir, `${m[1]}.json`);
          if (req.method === 'GET') {
            if (!existsSync(file)) { res.statusCode = 404; return res.end(); }
            res.setHeader('Content-Type', 'application/json');
            return res.end(readFileSync(file));
          }
          if (req.method === 'PUT') {
            let body = '';
            req.on('data', c => { body += c; if (body.length > 50e6) req.destroy(); });
            req.on('end', () => {
              try {
                const o = JSON.parse(body);
                if (o.format !== 'ca-geo/historic-mapper') throw new Error('format');
                mkdirSync(projectsDir, { recursive: true });
                writeFileSync(file, JSON.stringify(o, null, 1) + '\n');
                res.statusCode = 204; res.end();
              } catch { res.statusCode = 400; res.end(); }
            });
            return;
          }
        }
        next();
      });
    },
  };
}

export default defineConfig({
  base: './',
  plugins: [localData()],
  build: { rollupOptions: { input: { main: resolve(here, 'index.html'), viewer3d: resolve(here, 'viewer3d.html'), growth3d: resolve(here, 'growth3d.html'), public3d: resolve(here, 'public3d.html'), workbench: resolve(here, 'workbench.html'), iso: resolve(here, 'iso.html'), facade: resolve(here, 'facade.html') } } },
  server: { port: 5218, strictPort: true },
});
