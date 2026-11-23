"""Render map pages of the Historický atlas měst ČR 21 – Plzeň (HIÚ AV ČR 2009, free PDF) as source images
for the historic mapper (sources with download "hiu-atlas:<page>"). The atlas is copyrighted: the images
stay in data/ (not versioned) and are used for research only.

usage: python atlas_pages.py   (expects data/reference/hiu-atlas/atlas.pdf)
"""
import json, os
import pymupdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PDF = os.path.join(ROOT, 'data', 'reference', 'hiu-atlas', 'atlas.pdf')
OUT = os.path.join(ROOT, 'data', 'historic', 'sources')
doc = pymupdf.open(PDF)
for s in json.load(open(os.path.join(os.path.dirname(__file__), '..', 'sources.json'), encoding='utf-8')):
    if not s.get('download', '').startswith('hiu-atlas:'): continue
    pg = int(s['download'].split(':')[1])
    pix = doc[pg - 1].get_pixmap(dpi=250)
    pix.save(os.path.join(OUT, s['file']), jpg_quality=90)
    print(s['id'], pix.width, pix.height)
