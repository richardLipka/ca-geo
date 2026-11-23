// Download full-resolution source images listed in sources.json into data/historic/sources/
// (repository data/ folder, not versioned). Existing files are skipped.
// usage: npm run fetch-sources [-- <id> ...]
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(here, '../../../data/historic/sources');
const sources = JSON.parse(readFileSync(resolve(here, '../sources.json'), 'utf8'));
const only = process.argv.slice(2);
// Some image servers reject generic script user agents; a browser-like string is accepted.
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) historic-mapper/0.1';
mkdirSync(out, { recursive: true });

async function get(url, tries = 4) {
  for (let i = 0; i < tries; i++) {
    const r = await fetch(url, { headers: { 'User-Agent': UA }, redirect: 'follow' });
    if (r.ok) return Buffer.from(await r.arrayBuffer());
    if (r.status !== 429 && r.status < 500) throw new Error(`HTTP ${r.status}`);
    await new Promise(res => setTimeout(res, 5000 * (i + 1)));
  }
  throw new Error('gave up after retries');
}

/** Kramerius 7 (Charles University): first page of the item through the IIIF image API. */
async function kramerius(pid) {
  const api = 'https://kramerius.cuni.cz/search/api/client/v7.0';
  const r = await fetch(`${api}/search?q=own_parent.pid:"${pid}"&fl=pid&rows=1&sort=rels_ext_index.sort%20asc&wt=json`, { headers: { 'User-Agent': UA } });
  const page = (await r.json()).response.docs[0]?.pid ?? pid;
  return `https://kramerius.cuni.cz/search/iiif/${page}/full/3000,/0/default.jpg`;
}

for (const s of sources) {
  if (only.length && !only.includes(s.id)) continue;
  const file = join(out, s.file);
  if (existsSync(file)) { console.log(`skip  ${s.id} (exists)`); continue; }
  try {
    const url = s.download.startsWith('kramerius-cuni:') ? await kramerius(s.download.slice('kramerius-cuni:'.length)) : s.download;
    const buf = await get(url);
    writeFileSync(file, buf);
    console.log(`ok    ${s.id}  ${(buf.length / 1e6).toFixed(1)} MB`);
  } catch (e) {
    console.log(`FAIL  ${s.id}  ${e.message}`);
  }
  await new Promise(res => setTimeout(res, 1500));
}
