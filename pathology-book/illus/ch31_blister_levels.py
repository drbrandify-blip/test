"""Level of the split in blistering diseases (ch31). Run: python3 illus/ch31_blister_levels.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from diagrams import A, A60, A40, A20, A10, A05, INK, INK2, G20, G40, G05, esc

W, H = 665, 250
X0, X1 = 20, 420
yC0, yC1 = 34, 50      # stratum corneum
yG1 = 60               # granulosum bottom
yS1 = 108              # spinosum bottom
yB1 = 122              # basale bottom
yBM = 124              # basement membrane
yD1 = 186              # dermis bottom
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="BookSans, sans-serif">']

def t(x, y, s, size=8.4, w="400", fill=INK2, anchor="start", style=""):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}"{style}>{esc(s)}</text>')

# dermis
o.append(f'<rect x="{X0}" y="{yBM}" width="{X1-X0}" height="{yD1-yBM}" fill="{A05}"/>')
for x in range(X0 + 10, X1, 34):
    o.append(f'<path d="M{x},{yBM+18} q8,-6 16,0 t16,0" fill="none" stroke="{G40}" stroke-width="0.8"/>')
    o.append(f'<path d="M{x+6},{yBM+42} q8,-6 16,0 t16,0" fill="none" stroke="{G40}" stroke-width="0.8"/>')
# corneum (flat lamellae)
o.append(f'<rect x="{X0}" y="{yC0}" width="{X1-X0}" height="{yC1-yC0}" fill="{G05}"/>')
for y in range(yC0 + 3, yC1, 4):
    o.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{G40}" stroke-width="0.7"/>')
# granulosum (flattened cells with dark granules)
o.append(f'<rect x="{X0}" y="{yC1}" width="{X1-X0}" height="{yG1-yC1}" fill="{A10}"/>')
for x in range(X0 + 6, X1 - 6, 16):
    o.append(f'<ellipse cx="{x+6}" cy="{(yC1+yG1)/2}" rx="7" ry="3.4" fill="#fff" stroke="{A40}" stroke-width="0.7"/>')
    o.append(f'<circle cx="{x+4}" cy="{(yC1+yG1)/2}" r="1.1" fill="{INK2}"/><circle cx="{x+9}" cy="{(yC1+yG1)/2+1}" r="1.1" fill="{INK2}"/>')
# spinosum (polygonal cells)
o.append(f'<rect x="{X0}" y="{yG1}" width="{X1-X0}" height="{yS1-yG1}" fill="{A10}"/>')
for row, y in enumerate((70, 85, 100)):
    off = 9 if row % 2 else 0
    for x in range(X0 + 4 + off, X1 - 8, 18):
        o.append(f'<rect x="{x}" y="{y-6}" width="15" height="12" rx="3" fill="#fff" stroke="{A40}" stroke-width="0.8"/>')
        o.append(f'<circle cx="{x+7.5}" cy="{y}" r="2.4" fill="{A60}"/>')
# basale (columnar cells)
o.append(f'<rect x="{X0}" y="{yS1}" width="{X1-X0}" height="{yB1-yS1}" fill="{A20}"/>')
for x in range(X0 + 2, X1 - 6, 9):
    o.append(f'<rect x="{x}" y="{yS1+1}" width="7" height="{yB1-yS1-2}" rx="2" fill="{A40}"/>')
    o.append(f'<ellipse cx="{x+3.5}" cy="{(yS1+yB1)/2}" rx="2" ry="3.4" fill="{A}"/>')
# basement membrane
o.append(f'<rect x="{X0}" y="{yB1}" width="{X1-X0}" height="{yBM-yB1+1}" fill="{INK}"/>')

# --- the three splits ---
# 1 subcorneal (pemphigus foliaceus)
o.append(f'<ellipse cx="90" cy="{yC1+1}" rx="38" ry="6.5" fill="#fff" stroke="{A}" stroke-width="1.2"/>')
o.append(f'<circle cx="80" cy="{yC1+1}" r="2.6" fill="{A20}" stroke="{A60}" stroke-width="0.7"/>')
# 2 suprabasal (pemphigus vulgaris): row of tombstones remains
o.append(f'<ellipse cx="225" cy="{yS1-3}" rx="42" ry="8" fill="#fff" stroke="{A}" stroke-width="1.2"/>')
for cx in (212, 230, 244):
    o.append(f'<circle cx="{cx}" cy="{yS1-4}" r="3.6" fill="{A20}" stroke="{A60}" stroke-width="0.8"/><circle cx="{cx}" cy="{yS1-4}" r="1.3" fill="{A}"/>')
# 3 subepidermal (BP / DH): whole epidermis is the roof
o.append(f'<ellipse cx="360" cy="{yBM+9}" rx="48" ry="9.5" fill="#fff" stroke="{A}" stroke-width="1.2"/>')
for cx, cy in ((340, yBM+8), (352, yBM+12), (366, yBM+7), (380, yBM+11)):
    o.append(f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{A}"/>')

# split pointers and labels under the dermis
cols = [
    (90, yC1 + 1, "Subcorneal", ["Pemphigus foliaceus", "(desmoglein 1)"]),
    (225, yS1 - 3, "Suprabasal", ["Pemphigus vulgaris", "(desmoglein 3 ± 1)", "basal ‘tombstones’ remain"]),
    (360, yBM + 9, "Subepidermal", ["Bullous pemphigoid (BP180/230)", "Dermatitis herpetiformis (IgA)", "roof = whole epidermis"]),
]
for cx, cy, head, lines in cols:
    o.append(f'<line x1="{cx}" y1="{cy+8}" x2="{cx}" y2="{yD1+6}" stroke="{A}" stroke-width="1" stroke-dasharray="3,2"/>')
    t(cx, yD1 + 18, head, 9, "700", A, "middle")
    for k, ln in enumerate(lines):
        t(cx, yD1 + 30 + 11 * k, ln, 8.2, "400", INK2, "middle")

# layer labels on the right
labels = [((yC0 + yC1) / 2, "Stratum corneum"), ((yC1 + yG1) / 2, "Stratum granulosum"),
          ((yG1 + yS1) / 2, "Stratum spinosum (desmosomes)"), ((yS1 + yB1) / 2 - 2, "Stratum basale"),
          (yBM + 6, "Basement membrane (hemidesmosomes)"), ((yBM + yD1) / 2 + 8, "Papillary dermis")]
for y, s in labels:
    o.append(f'<line x1="{X1+2}" y1="{y}" x2="{X1+12}" y2="{y}" stroke="{G40}" stroke-width="0.8"/>')
    t(X1 + 15, y + 3, s, 8.4, "700" if "membrane" in s else "400", INK if "membrane" in s else INK2)

# IF legend
t(X1 + 15, yD1 + 18, "Immunofluorescence", 9, "700", A)
for k, s in enumerate(["Pemphigus: intercellular ‘fishnet’ IgG", "Pemphigoid: linear IgG + C3 along BM", "DH: granular IgA at papillary tips"]):
    t(X1 + 15, yD1 + 30 + 11 * k, s, 8.2)
o.append("</svg>")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch31_blister_levels.svg")
open(out, "w", encoding="utf-8").write("\n".join(o))
print("wrote", out)
