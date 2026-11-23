import { imageSize, store } from './store';

const cache = new Map<string, HTMLImageElement>();
const failed = new Set<string>();

/** Load a source image once; re-render when it arrives. Same-origin files can be WebGL textures. */
export function getImage(url: string): HTMLImageElement | null {
  if (failed.has(url)) return null;
  let img = cache.get(url);
  if (!img) {
    img = new Image();
    img.decoding = 'async';
    if (!url.startsWith('/') && !url.startsWith('blob:')) img.crossOrigin = 'anonymous';
    img.onload = () => { imageSize.set(url, [img!.naturalWidth, img!.naturalHeight]); store.emit(); };
    img.onerror = () => { failed.add(url); store.emit(); };
    img.src = url;
    cache.set(url, img);
  }
  return img.complete && img.naturalWidth ? img : null;
}

export const imageFailed = (url: string) => failed.has(url);
