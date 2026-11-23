import { describe, expect, it } from 'vitest';
import { CATALOGUES } from '../src/i18n';

describe('i18n catalogues', () => {
  it('cs and en have the same keys', () => {
    const cs = Object.keys(CATALOGUES.cs).sort(), en = Object.keys(CATALOGUES.en).sort();
    expect(cs).toEqual(en);
  });
  it('placeholders match between languages', () => {
    const ph = (s: string) => (s.match(/\{\w+\}/g) ?? []).sort().join();
    for (const k of Object.keys(CATALOGUES.cs) as (keyof typeof CATALOGUES.cs)[]) expect(ph(CATALOGUES.cs[k]), k).toBe(ph(CATALOGUES.en[k]));
  });
});
