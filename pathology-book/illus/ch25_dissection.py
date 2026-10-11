"""Aortic dissection: DeBakey I-III and Stanford A/B. Run: python3 illus/ch25_dissection.py"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from diagrams import A, A60, A40, A20, A10, INK, INK2, G20, G40, esc

W, H = 665, 300
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="BookSans, sans-serif">']
PW = W / 3                     # panel width
R = 42                         # arch radius
TW = 20                        # aortic tube width


def pt(cx, cy, deg):
    return cx + R * math.cos(math.radians(deg)), cy - R * math.sin(math.radians(deg))


def panel(i, title, sub, segs, tear):
    x0 = i * PW
    ax = x0 + PW / 2 - R       # ascending aorta x
    dx = x0 + PW / 2 + R       # descending aorta x
    cy = 112                   # arch centre y
    cx = x0 + PW / 2
    ybase, yend = 236, 268
    o.append(f'<text x="{cx:.1f}" y="20" font-size="11" font-weight="700" fill="{INK}" text-anchor="middle">{esc(title)}</text>')
    o.append(f'<text x="{cx:.1f}" y="34" font-size="8.6" fill="{INK2}" text-anchor="middle">{esc(sub)}</text>')
    # heart / aortic valve hint
    o.append(f'<ellipse cx="{ax:.1f}" cy="{ybase+12}" rx="26" ry="13" fill="{G20}"/>')
    o.append(f'<text x="{ax:.1f}" y="{ybase+15}" font-size="7.4" fill="{INK2}" text-anchor="middle">heart</text>')
    # branches: brachiocephalic, L carotid, L subclavian
    for deg in (138, 100, 64):
        bx, by = pt(cx, cy, deg)
        o.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx:.1f}" y2="{by-30:.1f}" stroke="{G40}" stroke-width="7" stroke-linecap="round"/>')
    full = f'M{ax:.1f},{ybase} L{ax:.1f},{cy} A{R},{R} 0 0 1 {dx:.1f},{cy} L{dx:.1f},{yend}'
    o.append(f'<path d="{full}" fill="none" stroke="{G20}" stroke-width="{TW}" stroke-linejoin="round"/>')
    for d in segs:
        o.append(f'<path d="{d}" fill="none" stroke="{A60}" stroke-width="{TW}" stroke-linecap="butt"/>')
        o.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 3"/>')
    tx, ty = tear
    o.append(f'<path d="M{tx-6:.1f},{ty-6:.1f} L{tx+6:.1f},{ty+6:.1f} M{tx+6:.1f},{ty-6:.1f} L{tx-6:.1f},{ty+6:.1f}" stroke="{INK}" stroke-width="2.6"/>')
    return ax, dx, cy, ybase, yend


# geometry helpers per panel
def geo(i):
    x0 = i * PW
    cx = x0 + PW / 2
    return cx - R, cx + R, 112, 236, 268, cx

# DeBakey I: ascending + arch + descending
ax, dx, cy, yb, ye, cx = geo(0)
panel(0, "DeBakey I", "ascending + arch + descending",
      [f'M{ax:.1f},{yb-8} L{ax:.1f},{cy} A{R},{R} 0 0 1 {dx:.1f},{cy} L{dx:.1f},{ye}'], (ax, yb - 40))
# DeBakey II: ascending only (stops before brachiocephalic)
ax, dx, cy, yb, ye, cx = geo(1)
bx, by = pt(cx, cy, 160)
panel(1, "DeBakey II", "ascending aorta only",
      [f'M{ax:.1f},{yb-8} L{ax:.1f},{cy} A{R},{R} 0 0 1 {bx:.1f},{by:.1f}'], (ax, yb - 40))
# DeBakey III: descending only, distal to left subclavian
ax, dx, cy, yb, ye, cx = geo(2)
sx, sy = pt(cx, cy, 40)
panel(2, "DeBakey III", "descending aorta only",
      [f'M{sx:.1f},{sy:.1f} A{R},{R} 0 0 1 {dx:.1f},{cy} L{dx:.1f},{ye}'], (dx, cy + 18))

# Stanford brackets
yb2 = 284
o.append(f'<path d="M{12},{yb2-8} L12,{yb2} L{2*PW-12:.1f},{yb2} L{2*PW-12:.1f},{yb2-8}" fill="none" stroke="{A}" stroke-width="1.6"/>')
o.append(f'<text x="{PW:.1f}" y="{yb2+12}" font-size="9.6" font-weight="700" fill="{A}" text-anchor="middle">STANFORD A (proximal): involves ascending aorta → surgery</text>')
o.append(f'<path d="M{2*PW+12:.1f},{yb2-8} L{2*PW+12:.1f},{yb2} L{W-12:.1f},{yb2} L{W-12:.1f},{yb2-8}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
o.append(f'<text x="{2.5*PW:.1f}" y="{yb2+12}" font-size="9.6" font-weight="700" fill="{INK}" text-anchor="middle">STANFORD B (distal) → medical</text>')
# legend
LY = 316
o.append(f'<rect x="{W/2-150}" y="{LY-8}" width="18" height="9" fill="{A60}"/><text x="{W/2-127}" y="{LY}" font-size="8.4" fill="{INK2}">dissected segment (false lumen)</text>')
o.append(f'<path d="M{W/2+40},{LY-9} l10,10 m0,-10 l-10,10" stroke="{INK}" stroke-width="2.2"/><text x="{W/2+58}" y="{LY}" font-size="8.4" fill="{INK2}">intimal tear (usual entry site)</text>')
o.append('</svg>')

H2 = 322
svg = "".join(o).replace(f'viewBox="0 0 {W} {H}"', f'viewBox="0 0 {W} {H2+4}"').replace(f'height="{H}"', f'height="{H2+4}"')
open(os.path.join(os.path.dirname(__file__), "ch25_dissection.svg"), "w").write(svg)
print("ok")
