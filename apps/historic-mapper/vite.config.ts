import { defineConfig, type Plugin } from 'vite';
import { createReadStream, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const dataRoot = resolve(here, '../../data'); // repository data/ (not versioned)
const projectsDir = resolve(here, 'projects'); // saved annotation projects (versioned)

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
  plugins: [localData()],
  server: { port: 5218, strictPort: true },
});
