"""Local static server for the growth guide page (data/historic/growth/site/) with HTTP Range support,
so the video can be seeked from the chapter buttons (python -m http.server cannot do that).

usage: python serve_site.py [port]        → http://localhost:<port>/site/   (default port 5219)
POST /api/review merges review decisions into site/check/review.json (review.html).
Manual editor (apps/historic-mapper/editor/, http://localhost:<port>/editor/): /editor/, /manual/, /projects/ and
/sources/ are served from the repository (editor, manual edits, project with the veduta cameras, source images);
POST /api/manual/<name>.json|.png saves an edit into apps/historic-mapper/manual/ (PNG as a data URL).
"""
import base64, http.server, json, os, re, sys, threading, urllib.parse
LOCK = threading.Lock()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'historic', 'growth'))
APP = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ALIAS = {'/editor/': os.path.join(APP, 'editor'), '/manual/': os.path.join(APP, 'manual'), '/projects/': os.path.join(APP, 'projects'),
         '/sources/': os.path.abspath(os.path.join(ROOT, '..', 'sources'))}
os.makedirs(ALIAS['/manual/'], exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, path):
        p = path.split('?')[0].split('#')[0]
        for pre, d in ALIAS.items():
            if p.startswith(pre):
                rest = urllib.parse.unquote(p[len(pre):])
                full = os.path.abspath(os.path.join(d, rest))
                return full if full.startswith(d) else d
        return super().translate_path(path)

    def send_head(self):
        rng = self.headers.get('Range')
        path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().send_head()
        m = re.match(r'bytes=(\d*)-(\d*)', rng)
        size = os.path.getsize(path)
        if not m:
            return super().send_head()
        a = int(m[1]) if m[1] else max(0, size - int(m[2] or 0))
        b = min(int(m[2]), size - 1) if m[1] and m[2] else size - 1
        if a >= size:
            self.send_error(416); return None
        f = open(path, 'rb'); f.seek(a)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {a}-{b}/{size}')
        self.send_header('Content-Length', str(b - a + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        self._left = b - a + 1
        return f

    def copyfile(self, source, outputfile):
        left = getattr(self, '_left', None)
        if left is None:
            return super().copyfile(source, outputfile)
        while left > 0:
            chunk = source.read(min(65536, left))
            if not chunk: break
            try: outputfile.write(chunk)
            except (BrokenPipeError, ConnectionResetError): break
            left -= len(chunk)
        self._left = None

    def do_POST(self):
        # review decisions from site/check/review.html → site/check/review.json (merged)
        n = int(self.headers.get('Content-Length') or 0)
        m = re.fullmatch(r'/api/manual/([a-z0-9_.-]+\.(json|png))', self.path.split('?')[0])
        if m:   # manual edits (editor): JSON as it is, PNG as a data URL
            body = self.rfile.read(n)
            f = os.path.join(ALIAS['/manual/'], m[1])
            with LOCK:
                if m[2] == 'json':
                    json.loads(body)   # valid JSON only
                    open(f + '.tmp', 'wb').write(body)
                else:
                    open(f + '.tmp', 'wb').write(base64.b64decode(body.split(b',', 1)[-1]))
                os.replace(f + '.tmp', f)
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', '2'); self.end_headers(); self.wfile.write(b'{}')
            return
        if self.path.split('?')[0] != '/api/review':
            self.send_error(404); return
        try:
            upd = json.loads(self.rfile.read(n) or b'{}')
        except ValueError:
            self.send_error(400); return
        f = os.path.join(ROOT, 'site', 'check', 'review.json')
        with LOCK:
            cur = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
            for k, v in upd.items(): cur[k] = {**cur.get(k, {}), **v}
            json.dump(cur, open(f + '.tmp', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            os.replace(f + '.tmp', f)
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', '2'); self.end_headers(); self.wfile.write(b'{}')

    def end_headers(self):
        if not self.headers.get('Range'): self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5219
    print(f'http://localhost:{port}/site/')
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
