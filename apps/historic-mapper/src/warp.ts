// WebGL renderer that draws georeferenced source images on the map by warping a mesh:
// a regular grid over the image is pushed through the fitted image→map transform and the
// image is texture-mapped onto the resulting triangles (works for any transform, incl. TPS).

import type { Fit } from './transform';

const VS = `#version 300 es
in vec2 aMap; in vec2 aUv; uniform vec2 uC; uniform float uRes; uniform vec2 uSize; out vec2 vUv;
void main() {
  vec2 s = (aMap - uC) / uRes;               // metres → screen px relative to centre (y up)
  gl_Position = vec4(2.0 * s.x / uSize.x, 2.0 * s.y / uSize.y, 0.0, 1.0);
  vUv = aUv;
}`;
const FS = `#version 300 es
precision mediump float; in vec2 vUv; uniform sampler2D uTex; uniform float uAlpha; out vec4 o;
void main() { vec4 c = texture(uTex, vUv); o = vec4(c.rgb, c.a * uAlpha); }`;

interface Mesh { key: string; vao: WebGLVertexArrayObject; count: number }

export class WarpLayer {
  private gl: WebGL2RenderingContext | null;
  private prog: WebGLProgram | null = null;
  private tex = new Map<string, WebGLTexture>();
  private meshes = new Map<string, Mesh>();

  constructor(private canvas: HTMLCanvasElement) {
    this.gl = canvas.getContext('webgl2', { premultipliedAlpha: false, alpha: true });
    if (this.gl) this.prog = this.program();
  }
  get ok() { return !!this.gl; }

  private program() {
    const gl = this.gl!;
    const sh = (type: number, src: string) => { const s = gl.createShader(type)!; gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) ?? 'shader'); return s; };
    const p = gl.createProgram()!; gl.attachShader(p, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p) ?? 'link');
    return p;
  }

  private texture(url: string, img: HTMLImageElement): WebGLTexture | null {
    const gl = this.gl!; let t = this.tex.get(url);
    if (t) return t;
    const max = gl.getParameter(gl.MAX_TEXTURE_SIZE) as number;
    let srcEl: TexImageSource = img;
    if (img.naturalWidth > max || img.naturalHeight > max) { // downscale oversized images
      const k = max / Math.max(img.naturalWidth, img.naturalHeight), cv = document.createElement('canvas');
      cv.width = Math.floor(img.naturalWidth * k); cv.height = Math.floor(img.naturalHeight * k);
      cv.getContext('2d')!.drawImage(img, 0, 0, cv.width, cv.height); srcEl = cv;
    }
    t = gl.createTexture()!;
    gl.bindTexture(gl.TEXTURE_2D, t);
    try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, srcEl); } catch { gl.deleteTexture(t); return null; } // cross-origin without CORS
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    this.tex.set(url, t);
    return t;
  }

  private mesh(id: string, key: string, f: Fit, w: number, h: number): Mesh {
    const old = this.meshes.get(id);
    if (old && old.key === key) return old;
    const gl = this.gl!, N = 40, data: number[] = [];
    const v = (i: number, j: number) => { const u = i / N, vv = j / N, m = f.forward([u * w, vv * h]); return [m[0], m[1], u, vv]; };
    // positions are large (≈ −10⁶ m): keep them relative to the first vertex to preserve float precision
    const grid: number[][][] = [];
    for (let i = 0; i <= N; i++) { grid.push([]); for (let j = 0; j <= N; j++) grid[i].push(v(i, j)); }
    for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
      const a = grid[i][j], b = grid[i + 1][j], c = grid[i][j + 1], d = grid[i + 1][j + 1];
      data.push(...a, ...b, ...c, ...b, ...d, ...c);
    }
    const vao = old?.vao ?? gl.createVertexArray()!;
    gl.bindVertexArray(vao);
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data.map((x, k) => (k % 4 === 0 ? x - REF[0] : k % 4 === 1 ? x - REF[1] : x))), gl.STATIC_DRAW);
    const la = gl.getAttribLocation(this.prog!, 'aMap'), lu = gl.getAttribLocation(this.prog!, 'aUv');
    gl.enableVertexAttribArray(la); gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 16, 0);
    gl.enableVertexAttribArray(lu); gl.vertexAttribPointer(lu, 2, gl.FLOAT, false, 16, 8);
    const m = { key, vao, count: data.length / 4 };
    this.meshes.set(id, m);
    return m;
  }

  /** Draw all layers; centre in EPSG:5514, resolution in metres per CSS pixel. */
  draw(layers: { id: string; url: string; img: HTMLImageElement; fit: Fit; key: string; opacity: number }[], c: [number, number], res: number) {
    const gl = this.gl; if (!gl) return;
    const dpr = Math.min(devicePixelRatio || 1, 2), w = this.canvas.clientWidth, h = this.canvas.clientHeight;
    if (this.canvas.width !== Math.round(w * dpr) || this.canvas.height !== Math.round(h * dpr)) { this.canvas.width = Math.round(w * dpr); this.canvas.height = Math.round(h * dpr); }
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.useProgram(this.prog);
    gl.uniform2f(gl.getUniformLocation(this.prog!, 'uC'), c[0] - REF[0], c[1] - REF[1]);
    gl.uniform1f(gl.getUniformLocation(this.prog!, 'uRes'), res);
    gl.uniform2f(gl.getUniformLocation(this.prog!, 'uSize'), w, h);
    for (const L of layers) {
      const tex = this.texture(L.url, L.img); if (!tex) continue;
      const m = this.mesh(L.id, L.key, L.fit, L.img.naturalWidth, L.img.naturalHeight);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.uniform1i(gl.getUniformLocation(this.prog!, 'uTex'), 0);
      gl.uniform1f(gl.getUniformLocation(this.prog!, 'uAlpha'), L.opacity);
      gl.bindVertexArray(m.vao); gl.drawArrays(gl.TRIANGLES, 0, m.count);
    }
  }
}

/** Local origin near Plzeň used to keep vertex coordinates small (float32 precision). */
const REF: [number, number] = [-822400, -1069700];
