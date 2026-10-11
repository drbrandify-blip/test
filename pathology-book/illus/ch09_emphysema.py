"""Acinar distribution of emphysema: normal vs centriacinar vs panacinar vs distal acinar.
Run: python3 illus/ch09_emphysema.py  -> illus/ch09_emphysema.svg"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from diagrams import A, A60, A40, A20, A10, A05, INK, INK2, G20, G40, G05, esc

W, H, PW, GAP = 665, 268, 158, 11
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="BookSans, sans-serif">']


def tube(x1, y1, x2, y2, w=7):
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{G40}" stroke-width="{w}" stroke-linecap="round"/>')
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="{w-3.2}" stroke-linecap="round"/>')


def alv(x, y, r=6.5, hot=False):
    fill, stroke = (A20, A) if hot else ("#fff", G40)
    o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')


def blob(x, y, rx, ry):
    o.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{A20}" stroke="{A}" stroke-width="1.1"/>')


def acinus(cx, kind):
    # terminal bronchiole and two respiratory bronchioles
    tube(cx, 42, cx, 72, 8)
    rb_ends = [(cx - 38, 106), (cx + 38, 106)]
    for ex, ey in rb_ends:
        tube(cx, 72, ex, ey)
    ad_ends = []
    for ex, ey in rb_ends:
        for dx in (-19, 19):
            ad_ends.append((ex + dx, ey + 34))
            tube(ex, ey, ex + dx, ey + 34, 6)
    # respiratory-bronchiole buds (alveoli opening off the wall)
    for sx in (-1, 1):
        mx, my = cx + sx * 19, 89
        if kind in ("centri", "pan"):
            blob(mx, my, 17 if kind == "centri" else 14, 13 if kind == "centri" else 11)
            if kind == "centri":
                for px, py in ((-8, -4), (5, 5), (9, -6), (-3, 7)):
                    o.append(f'<circle cx="{mx+px}" cy="{my+py}" r="1.5" fill="{INK}"/>')
        else:
            alv(mx - 9 * sx, my + 4, 4)
            alv(mx + 9 * sx, my - 6, 4)
    # alveolar sacs at the ends of the alveolar ducts
    for ex, ey in ad_ends:
        if kind == "pan" or kind == "distal":
            blob(ex, ey + 15, 16, 14)
            o.append(f'<line x1="{ex-6}" y1="{ey+5}" x2="{ex+3}" y2="{ey+20}" stroke="{A60}" stroke-width=".8"/>')
        else:
            for dx, dy in ((-8, 7), (8, 7), (-8, 22), (8, 22)):
                alv(ex + dx, ey + dy)


panels = [
    ("Normal acinus", "normal", ["TB → RB → alveolar ducts", "→ alveolar sacs"]),
    ("Centriacinar", "centri", ["Respiratory bronchioles enlarged,", "distal alveoli spared. Smokers;", "upper lobes; often pigmented"]),
    ("Panacinar", "pan", ["Whole acinus enlarged uniformly.", "α1-antitrypsin deficiency;", "lower lobes, bases"]),
    ("Distal acinar (paraseptal)", "distal", ["Distal acinus enlarged next to", "pleura and septa. Bullae →", "pneumothorax in young adults"]),
]
for i, (title, kind, sub) in enumerate(panels):
    x0 = i * (PW + GAP)
    cx = x0 + PW / 2
    o.append(f'<rect x="{x0}" y="0" width="{PW}" height="{H-22}" rx="6" fill="{A05 if kind != "normal" else G05}" stroke="{G20}"/>')
    o.append(f'<text x="{cx}" y="20" font-size="10.4" font-weight="700" fill="{A if kind != "normal" else INK}" text-anchor="middle">{esc(title)}</text>')
    if kind == "distal":
        o.append(f'<line x1="{x0+8}" y1="174" x2="{x0+PW-8}" y2="174" stroke="{INK2}" stroke-width="2.2"/>')
        o.append(f'<text x="{x0+PW-10}" y="186" font-size="7.6" font-style="italic" fill="{INK2}" text-anchor="end">pleura / septum</text>')
    acinus(cx, kind)
    if kind == "normal":
        for lab, lx, ly, tx, ty in (("TB", cx + 4, 52, cx + 30, 46), ("RB", cx + 22, 86, cx + 54, 76), ("AD", cx + 30, 126, cx + 66, 118)):
            o.append(f'<line x1="{lx}" y1="{ly}" x2="{tx-9}" y2="{ty-3}" stroke="{INK2}" stroke-width=".6"/>')
            o.append(f'<text x="{tx}" y="{ty}" font-size="8" font-weight="700" fill="{INK2}" text-anchor="middle">{lab}</text>')
    for k, line in enumerate(sub):
        o.append(f'<text x="{cx}" y="{204 + k*11.5}" font-size="8.4" fill="{INK2}" text-anchor="middle">{esc(line)}</text>')
# legend
o.append(f'<rect x="4" y="{H-15}" width="14" height="10" rx="2" fill="{A20}" stroke="{A}"/>')
o.append(f'<text x="24" y="{H-6.5}" font-size="8.6" fill="{INK2}">Enlarged airspaces with destroyed walls</text>')
o.append(f'<circle cx="232" cy="{H-10}" r="2" fill="{INK}"/>')
o.append(f'<text x="240" y="{H-6.5}" font-size="8.6" fill="{INK2}">Anthracotic (carbon) pigment</text>')
o.append(f'<text x="{W-4}" y="{H-6.5}" font-size="8.6" fill="{INK2}" text-anchor="end">TB terminal bronchiole · RB respiratory bronchiole · AD alveolar duct</text>')
o.append("</svg>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch09_emphysema.svg"), "w", encoding="utf-8").write("".join(o))
print("ok")
