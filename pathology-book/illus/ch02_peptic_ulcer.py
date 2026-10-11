"""Chronic peptic ulcer in cross-section: the four zones of the base. Run: python3 illus/ch02_peptic_ulcer.py"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from diagrams import A, A60, A40, A20, A10, A05, INK, INK2, G20, G40, G05, esc
W, H = 665, 232
X0, X1 = 20, 455
yM0, yMM, yS0, yP0, yP1, ySe = 46, 84, 88, 120, 178, 184   # mucosa top, musc. mucosae, submucosa, propria top/bottom, serosa
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="BookSans, sans-serif">']
# wall layers
o.append(f'<rect x="{X0}" y="{yM0}" width="{X1-X0}" height="{yMM-yM0}" fill="{A05}"/>')
for x in range(X0 + 6, X1 - 4, 13):
    o.append(f'<rect x="{x}" y="{yM0+4}" width="6" height="{yMM-yM0-10}" rx="3" fill="{A20}"/>')
o.append(f'<rect x="{X0}" y="{yMM}" width="{X1-X0}" height="{yS0-yMM}" fill="{A60}"/>')
o.append(f'<rect x="{X0}" y="{yS0}" width="{X1-X0}" height="{yP0-yS0}" fill="#fff"/>')
for cx, cy in ((60, 104), (120, 110), (390, 103), (430, 111)):
    o.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="none" stroke="{G40}" stroke-width="1.2"/>')
o.append(f'<rect x="{X0}" y="{yP0}" width="{X1-X0}" height="{yP1-yP0}" fill="{A20}"/>')
for y in range(yP0 + 7, yP1 - 3, 9):
    for x in range(X0 + 4 + (y % 2) * 8, X1 - 14, 22):
        o.append(f'<line x1="{x}" y1="{y}" x2="{x+12}" y2="{y}" stroke="{A40}" stroke-width="2" stroke-linecap="round"/>')
o.append(f'<rect x="{X0}" y="{yP1}" width="{X1-X0}" height="{ySe-yP1}" fill="{A60}"/>')
# ulcer zones, drawn outside-in
def trap(dl, db, top, base_y, bulge):
    """crater-shaped polygon widened by dl at the top and db at the base"""
    lx0, rx0 = 182 - dl, 312 + dl
    lx1, rx1 = 214 - db, 280 + db
    return f'M{lx0},{top} L{lx1},{base_y} Q247,{base_y+bulge} {rx1},{base_y} L{rx0},{top} Z'
o.append(f'<path d="{trap(44, 26, yMM, 166, 16)}" fill="{G20}"/>')            # fibrous scar
for i, y in enumerate((126, 138, 150, 160)):
    o.append(f'<path d="M{176+i*4},{y} q18,-5 36,0 t36,0 t36,0" fill="none" stroke="{G40}" stroke-width="1.1"/>')
o.append(f'<circle cx="203" cy="165" r="6" fill="#fff" stroke="{INK2}" stroke-width="3.2"/>')   # thick-walled artery
o.append(f'<path d="{trap(20, 16, yM0+2, 148, 15)}" fill="{A10}"/>')            # granulation tissue
pts = [(171, 60), (186, 100), (198, 132), (226, 152), (268, 152), (296, 132), (308, 100), (323, 60)]
for cx, cy in pts:
    o.append(f'<path d="M{cx-4},{cy} a4,3 0 1,0 8,0 a4,3 0 1,0 -8,0" fill="none" stroke="{A}" stroke-width="1.1"/>')
o.append(f'<path d="{trap(8, 7, yM0, 136, 14)}" fill="#fff"/>')                 # inflammatory exudate
import random
random.seed(4)
for t in [i / 46 for i in range(47)]:
    # walk along the crater outline: left wall, base, right wall
    if t < 0.35:
        u = t / 0.35; x, y = 177 + (209 - 177) * u, 48 + (133 - 48) * u
    elif t < 0.65:
        u = (t - 0.35) / 0.30; x, y = 209 + (285 - 209) * u, 133 + 13 * math.sin(math.pi * u)
    else:
        u = (t - 0.65) / 0.35; x, y = 285 + (317 - 285) * u, 133 - (133 - 48) * u
    o.append(f'<circle cx="{x+random.uniform(-1.5,1.5):.1f}" cy="{y+random.uniform(-1.5,1.5):.1f}" r="1.6" fill="{INK}"/>')
# crater (lumen) with necrotic fibrinoid lining
o.append(f'<path d="M182,{yM0} L214,128 Q247,140 280,128 L312,{yM0}" fill="#fff" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
o.append(f'<line x1="{X0}" y1="{yM0}" x2="182" y2="{yM0}" stroke="{A60}" stroke-width="1"/><line x1="312" y1="{yM0}" x2="{X1}" y2="{yM0}" stroke="{A60}" stroke-width="1"/>')
# layer names (left)
def lt(x, y, s, col=INK2, it=True, w="400"):
    o.append(f'<text x="{x}" y="{y}" font-size="8.4" font-weight="{w}" fill="{col}"{" font-style=\"italic\"" if it else ""}>{esc(s)}</text>')
lt(X0 + 3, yM0 + 34, "Mucosa (gastritis)")
lt(X0 + 3, yS0 + 12, "Submucosa")
lt(X0 + 3, yP0 + 32, "Muscularis propria")
lt(X0 + 3, ySe + 11, "Serosa")
lt(232, 74, "Lumen", INK2)
# labelled zones (right) with leader lines
def label(y, title, sub, px, py, n):
    lx = 474
    o.append(f'<line x1="{px}" y1="{py}" x2="{lx-6}" y2="{y-3}" stroke="{INK2}" stroke-width="0.8"/>')
    o.append(f'<circle cx="{px}" cy="{py}" r="2" fill="{INK2}"/>')
    o.append(f'<circle cx="{lx+6}" cy="{y-3}" r="7" fill="{A}"/><text x="{lx+6}" y="{y}" font-size="8.4" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>')
    o.append(f'<text x="{lx+18}" y="{y-1}" font-size="9" font-weight="700" fill="{INK}">{esc(title)}</text>')
    o.append(f'<text x="{lx+18}" y="{y+10}" font-size="8.2" fill="{INK2}">{esc(sub)}</text>')
label(52, "Necrotic fibrinoid debris", "thin layer lining the crater", 302, 82, 1)
label(88, "Inflammatory exudate", "mainly neutrophils", 311, 96, 2)
label(124, "Granulation tissue", "capillaries, mononuclear cells", 318, 112, 3)
label(160, "Fibrous scar", "replaces muscularis propria", 322, 152, 4)
o.append(f'<text x="{474}" y="{196}" font-size="8.2" fill="{INK2}">Thick-walled, thrombosed vessels in the</text>')
o.append(f'<text x="{474}" y="{207}" font-size="8.2" fill="{INK2}">scar may erode and bleed</text>')
o.append(f'<line x1="209" y1="168" x2="468" y2="196" stroke="{INK2}" stroke-width="0.8" stroke-dasharray="2 2"/>')
o.append(f'<text x="{60}" y="{24}" font-size="8.6" font-weight="700" fill="{A}">Punched-out edge, level with the mucosa</text>')
o.append(f'<line x1="150" y1="28" x2="181" y2="{yM0-1}" stroke="{A}" stroke-width="0.9"/>')
o.append(f'<text x="{X0}" y="{H-8}" font-size="8.2" fill="{INK2}" font-style="italic">Scarring of the whole wall puckers the mucosa, so folds radiate from the crater like spokes of a wheel.</text>')
o.append("</svg>")
open(os.path.join(os.path.dirname(__file__), "ch02_peptic_ulcer.svg"), "w", encoding="utf-8").write("\n".join(o))
print("ok")
