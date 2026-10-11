"""Glomerular capillary wall: where deposits sit -> which disease. Run: python3 illus/glom_deposits.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from diagrams import A, A60, A40, A20, A10, A05, INK, INK2, G20, G40, G05, esc
W, H = 665, 300
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="BookSans, sans-serif">']
X0, X1 = 30, 470
yFP, yG0, yG1, yE1 = 112, 128, 146, 154   # foot-process top, GBM top/bottom, endothelium bottom
# zones
o.append(f'<rect x="{X0}" y="64" width="{X1-X0}" height="{yG0-64}" fill="#fff"/>')
o.append(f'<rect x="{X0}" y="{yE1}" width="{X1-X0}" height="80" fill="{A05}"/>')
o.append(f'<text x="{X0+4}" y="78" font-size="8.6" font-style="italic" fill="{INK2}">Urinary (Bowman) space</text>')
o.append(f'<text x="{X0+4}" y="{yE1+74}" font-size="8.6" font-style="italic" fill="{INK2}">Capillary lumen (blood)</text>')
# RBC
o.append(f'<ellipse cx="400" cy="{yE1+40}" rx="18" ry="9" fill="#fff" stroke="{A60}" stroke-width="1.2"/><ellipse cx="400" cy="{yE1+40}" rx="8" ry="3.5" fill="{A20}"/>')
# GBM
o.append(f'<rect x="{X0}" y="{yG0}" width="{X1-X0}" height="{yG1-yG0}" fill="{G20}"/>')
o.append(f'<text x="{X0+4}" y="{yG0+12}" font-size="8.4" font-weight="700" fill="{INK2}">GBM</text>')
# endothelium with fenestrae (skip the subendothelial zone which is pushed down)
x = X0
while x < X1:
    if 62 <= x <= 138:
        x += 14; continue
    o.append(f'<rect x="{x}" y="{yG1}" width="10" height="{yE1-yG1}" rx="1.5" fill="{A40}"/>')
    x += 14
# foot processes (effaced zone 390-470)
x = X0 + 30
while x < 385:
    o.append(f'<rect x="{x}" y="{yFP}" width="14" height="{yG0-yFP+1}" rx="5" fill="{A60}"/>')
    x += 20
o.append(f'<rect x="388" y="{yFP+4}" width="{X1-388}" height="{yG0-yFP-3}" rx="3" fill="{A60}"/>')
o.append(f'<text x="{X0+4}" y="{yFP-5}" font-size="8" font-weight="700" fill="{A}">Podocyte foot processes</text>')
# podocyte cell bodies
for cx in (150, 330):
    o.append(f'<path d="M{cx-40},{yFP} C{cx-36},{yFP-22} {cx-20},{yFP-30} {cx},{yFP-30} C{cx+20},{yFP-30} {cx+36},{yFP-22} {cx+40},{yFP} z" fill="{A10}" stroke="{A60}" stroke-width="1"/>')
    o.append(f'<ellipse cx="{cx}" cy="{yFP-15}" rx="12" ry="7" fill="{A40}"/>')
# deposits
# 1 PSGN humps (subepithelial, big)
for cx in (70, 98):
    o.append(f'<ellipse cx="{cx}" cy="{yG0-6}" rx="10" ry="9" fill="{INK}"/>')
# 2 membranous: small subepithelial deposits with GBM spikes
for i, cx in enumerate(range(196, 300, 16)):
    o.append(f'<rect x="{cx-4}" y="{yG0-6}" width="8" height="7" rx="1.5" fill="{INK}"/>')
    o.append(f'<path d="M{cx+5},{yG0} l3,-9 l3,9 z" fill="{G40}"/>')
# 3 dense deposit disease: intramembranous ribbon
o.append(f'<rect x="300" y="{yG0+6}" width="70" height="6" rx="3" fill="{INK}"/>')
# 4 subendothelial
for cx in (78, 104, 126):
    o.append(f'<ellipse cx="{cx}" cy="{yG1+5}" rx="11" ry="6" fill="{INK}"/>')
o.append(f'<rect x="64" y="{yG1+11}" width="74" height="5" rx="2" fill="{A40}"/>')
# mesangium
mx0 = 490
o.append(f'<rect x="{mx0}" y="96" width="150" height="120" rx="14" fill="{A10}" stroke="{A}" stroke-width="1.2"/>')
o.append(f'<text x="{mx0+75}" y="112" font-size="9" font-weight="700" fill="{A}" text-anchor="middle">Mesangium</text>')
o.append(f'<ellipse cx="{mx0+45}" cy="150" rx="13" ry="8" fill="{A40}"/><ellipse cx="{mx0+105}" cy="182" rx="13" ry="8" fill="{A40}"/>')
for (dx, dy) in ((80, 140), (95, 152), (40, 182), (62, 194), (118, 140), (75, 170)):
    o.append(f'<circle cx="{mx0+dx}" cy="{dy}" r="5" fill="{INK}"/>')
o.append(f'<path d="M{X1},{yG0} C{X1+8},{yG0} {mx0-6},120 {mx0},120" fill="none" stroke="{G40}" stroke-width="3"/>')

def label(x, y, title, sub, lx, ly, anchor="middle"):
    y2 = y + 11.5 * len(sub) + 4 if y < ly else y - 12
    o.append(f'<line x1="{lx}" y1="{ly}" x2="{lx}" y2="{y2}" stroke="{INK}" stroke-width=".8"/>')
    o.append(f'<circle cx="{lx}" cy="{ly}" r="2" fill="{INK}"/>')
    o.append(f'<text x="{x}" y="{y}" font-size="9.4" font-weight="700" fill="{INK}" text-anchor="{anchor}">{esc(title)}</text>')
    for j, s in enumerate(sub):
        o.append(f'<text x="{x}" y="{y+11.5*(j+1)}" font-size="8.4" fill="{INK2}" text-anchor="{anchor}">{esc(s)}</text>')

label(84, 14, "Subepithelial humps", ["Post-streptococcal GN"], 84, yG0-15)
label(246, 14, "Subepithelial deposits + spikes", ["Membranous nephropathy"], 246, yG0-8)
label(428, 14, "Effaced feet, no deposits", ["Minimal change disease"], 428, yFP+3)
label(100, 268, "Subendothelial deposits", ["MPGN type I · lupus nephritis", "(“wire loops”)"], 100, yG1+12)
label(335, 268, "Intramembranous ribbon", ["Dense deposit disease (C3G)"], 335, yG0+12)
label(565, 268, "Mesangial deposits", ["IgA nephropathy · IgA vasculitis"], 565, 200)
o.append("</svg>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "glom_deposits.svg"), "w").write("".join(o))
print("ok")
