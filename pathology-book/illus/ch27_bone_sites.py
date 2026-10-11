"""Long bone: zones and the classic sites of bone tumours. Run: python3 illus/ch27_bone_sites.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from diagrams import A, A60, A40, A20, A10, A05, INK, INK2, G20, G40, G05, esc

W, H = 665, 366
C = 178                      # long axis of the bone
mx = lambda x: 664 - x       # mirror for the right end
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="BookSans, sans-serif">']


def outline(sh, mh, eh, xend, xphys, xmeta):
    """Closed outline: shaft half-height sh, metaphysis max mh, epiphysis max eh, bone ends at xend/mx(xend)."""
    L = (f"M{mx(xmeta)},{C-sh} L{xmeta},{C-sh} C{xmeta-40},{C-sh} {xphys+30},{C-mh+6} {xphys+2},{C-mh} "
         f"L{xphys-2},{C-mh-1} C{xphys-35},{C-eh} {xend},{C-eh+26} {xend},{C} "
         f"C{xend},{C+eh-26} {xphys-35},{C+eh} {xphys-2},{C+mh+1} L{xphys+2},{C+mh} "
         f"C{xphys+30},{C+mh-6} {xmeta-40},{C+sh} {xmeta},{C+sh} L{mx(xmeta)},{C+sh} ")
    R = (f"C{mx(xmeta-40)},{C+sh} {mx(xphys+30)},{C+mh-6} {mx(xphys+2)},{C+mh} "
         f"L{mx(xphys-2)},{C+mh+1} C{mx(xphys-35)},{C+eh} {mx(xend)},{C+eh-26} {mx(xend)},{C} "
         f"C{mx(xend)},{C-eh+26} {mx(xphys-35)},{C-eh} {mx(xphys-2)},{C-mh-1} L{mx(xphys+2)},{C-mh} "
         f"C{mx(xphys+30)},{C-mh+6} {mx(xmeta-40)},{C-sh} {mx(xmeta)},{C-sh} Z")
    return L + R


outer = outline(31, 64, 74, 56, 130, 230)
inner = outline(20, 60, 70, 60, 130, 230)
o.append(f'<defs><clipPath id="bs_in"><path d="{inner}"/></clipPath></defs>')
# cortex (compact bone) = outer silhouette; cancellous interior
o.append(f'<path d="{outer}" fill="{A40}" stroke="{INK2}" stroke-width="1.1"/>')
o.append(f'<path d="{inner}" fill="{A10}"/>')
# trabeculae (cancellous bone) in both ends
tr = []
for k in range(-6, 7):
    y0 = C + k * 10
    tr.append(f"M40,{y0} q40,{-k*3} 90,{-k*2} q50,{k*1.5} 110,{k*4}")
    tr.append(f"M{mx(40)},{y0} q-40,{-k*3} -90,{-k*2} q-50,{k*1.5} -110,{k*4}")
for x in range(64, 236, 16):
    tr.append(f"M{x},{C-80} l6,160")
    tr.append(f"M{mx(x)},{C-80} l-6,160")
o.append(f'<g clip-path="url(#bs_in)"><path d="{" ".join(tr)}" fill="none" stroke="{A40}" stroke-width=".8"/></g>')
# medullary (marrow) cavity of the shaft
med = (f"M196,{C} C210,{C-13} 222,{C-20} 244,{C-20} L{mx(244)},{C-20} C{mx(222)},{C-20} {mx(210)},{C-13} {mx(196)},{C} "
       f"C{mx(210)},{C+13} {mx(222)},{C+20} {mx(244)},{C+20} L244,{C+20} C222,{C+20} 210,{C+13} 196,{C} Z")
o.append(f'<path d="{med}" fill="#fff"/>')
o.append(f'<text x="236" y="{C+3}" font-size="7.8" font-style="italic" fill="{INK2}">medullary cavity</text>')
o.append(f'<text x="250" y="{C+28.5}" font-size="7.4" font-weight="700" fill="{INK}">cortex</text>')
# articular cartilage caps (follow the outer contour of each end)
for sx in (1, -1):
    X = (lambda x: x) if sx == 1 else mx
    o.append(f'<path d="M{X(97.9)},{C-64} C{X(75.1)},{C-56.4} {X(56)},{C-33.6} {X(56)},{C} C{X(56)},{C+33.6} {X(75.1)},{C+56.4} {X(97.9)},{C+64}" '
             f'fill="none" stroke="{G40}" stroke-width="4.5" stroke-linecap="round"/>')
# physes: left open growth plate (child), right closed (epiphyseal line, adult)
o.append(f'<path d="M130,{C-62} q5,10 0,20 q-5,10 0,20 q5,10 0,20 q-5,10 0,20 q5,10 0,20 q-5,10 0,22" fill="none" stroke="{A}" stroke-width="4"/>')
o.append(f'<path d="M{mx(130)},{C-62} q-5,10 0,20 q5,10 0,20 q-5,10 0,20 q5,10 0,20 q-5,10 0,20 q5,10 0,22" fill="none" stroke="{A60}" stroke-width="1.2" stroke-dasharray="3 2.5"/>')

MAL, BEN = A, G40   # malignant = purple, benign = grey
# 1 chondroblastoma: left epiphysis (open plate)
o.append(f'<ellipse cx="94" cy="{C-24}" rx="15" ry="11" fill="{BEN}" stroke="{INK}" stroke-width="1"/>')
for (dx, dy) in ((-6, -3), (2, 2), (6, -4), (-2, 5)):
    o.append(f'<circle cx="{94+dx}" cy="{C-24+dy}" r="1.1" fill="{INK}"/>')
# 2 osteosarcoma: left metaphysis, breaking the lower cortex: sunburst + Codman triangle
o.append(f'<path d="M150,{C-10} C162,{C-34} 205,{C-30} 214,{C-8} C222,{C+8} 214,{C+30} 200,{C+40} C185,{C+50} 160,{C+46} 152,{C+30} C146,{C+18} 144,{C+4} 150,{C-10} Z" fill="{MAL}"/>')
for i, ang in enumerate(range(-70, 75, 14)):
    import math
    a = math.radians(ang)
    x1, y1 = 182 + 22 * math.sin(a), C + 46 + 4 * math.cos(a)
    x2, y2 = 182 + 40 * math.sin(a), C + 46 + 22 * math.cos(a)
    o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{MAL}" stroke-width="1.3"/>')
o.append(f'<path d="M222,{C+31} L240,{C+31} L222,{C+42} Z" fill="{A60}" stroke="{INK}" stroke-width=".8"/>')
# 3 osteoid osteoma: upper cortex of the shaft: fusiform sclerosis + nidus
o.append(f'<path d="M286,{C-31} C298,{C-41} 322,{C-41} 334,{C-31} Z" fill="{A60}" stroke="{INK2}" stroke-width=".8"/>')
o.append(f'<circle cx="310" cy="{C-30}" r="5" fill="#fff" stroke="{INK}" stroke-width="1.3"/><circle cx="310" cy="{C-30}" r="1.6" fill="{INK}"/>')
# 4 Ewing sarcoma: medulla of the shaft + onion-skin periosteal layers
o.append(f'<ellipse cx="392" cy="{C+2}" rx="34" ry="17" fill="{MAL}"/>')
o.append(f'<rect x="372" y="{C+16}" width="34" height="13" fill="{MAL}" opacity=".55"/>')
for j in range(3):
    yy = C + 35 + j * 4.2
    o.append(f'<path d="M{350-j*4},{yy} C370,{yy+2} 414,{yy+2} {436+j*4},{yy}" fill="none" stroke="{A60}" stroke-width="1.3"/>')
# 5 enchondroma: medulla near the right metaphysis: cartilage lobules with stippled calcification
for (cx, cy, r) in ((452, C - 4, 9), (466, C + 6, 8), (450, C + 10, 7)):
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BEN}" stroke="{INK}" stroke-width=".9"/>')
for (dx, dy) in ((450, C - 6), (456, C - 1), (466, C + 5), (448, C + 11), (470, C + 9)):
    o.append(f'<circle cx="{dx}" cy="{dy}" r="1" fill="{INK}"/>')
# 6 osteochondroma: right metaphysis surface, stalk pointing away from the joint, cartilage cap
o.append(f'<path d="M462,{C-31} Q454,{C-56} 440,{C-74} L458,{C-82} Q468,{C-60} 492,{C-42} Z" fill="{A10}" stroke="{A40}" stroke-width="3"/>')
o.append(f'<ellipse cx="447" cy="{C-80}" rx="14" ry="8" transform="rotate(-28 447 {C-80})" fill="{G20}" stroke="{INK}" stroke-width="1"/>')
# 7 giant cell tumour: right epiphysis (closed plate), eccentric, up to subchondral bone, soap-bubble
o.append(f'<path d="M548,{C-10} C548,{C-38} 582,{C-46} 598,{C-28} C606,{C-12} 606,{C+24} 594,{C+34} C578,{C+44} 550,{C+30} 548,{C-10} Z" fill="{BEN}" stroke="{INK}" stroke-width="1.1"/>')
o.append(f'<path d="M556,{C-12} Q574,{C-4} 596,{C-16} M560,{C+14} Q578,{C+6} 600,{C+16} M574,{C-38} Q570,{C} 578,{C+38}" fill="none" stroke="{INK}" stroke-width=".8"/>')


def label(cx, y, title, sub, tx, ty, anchor="middle"):
    """Label block at (cx, y) with leader line to target (tx, ty)."""
    up = ty > y          # label above target
    ly = y + 11.5 * len(sub) + 5 if up else y - 13
    lx = cx if anchor == "middle" else (cx - 30 if anchor == "end" else cx + 30)
    o.append(f'<line x1="{lx}" y1="{ly}" x2="{tx}" y2="{ty}" stroke="{INK}" stroke-width=".8"/>')
    o.append(f'<circle cx="{tx}" cy="{ty}" r="2" fill="{INK}"/>')
    o.append(f'<text x="{cx}" y="{y}" font-size="9.4" font-weight="700" fill="{INK}" text-anchor="{anchor}">{esc(title)}</text>')
    for j, s in enumerate(sub):
        o.append(f'<text x="{cx}" y="{y+11.5*(j+1)}" font-size="8.3" fill="{INK2}" text-anchor="{anchor}">{esc(s)}</text>')


label(66, 16, "Chondroblastoma", ["Epiphysis, growth", "plate still open", "(10–20 years)"], 92, C - 34)
label(190, 16, "Osteosarcoma", ["Metaphysis (knee);", "Codman triangle,", "sunburst spicules"], 182, C - 30)
label(316, 16, "Osteoid osteoma", ["Cortex: nidus < 2 cm", "in dense sclerosis;", "night pain, NSAIDs"], 310, C - 40)
label(445, 16, "Osteochondroma", ["Metaphysis; cartilage", "cap, stalk grows away", "from the joint"], 443, C - 88)
label(586, 16, "Giant cell tumour", ["Epiphysis after plate", "closes (20–40 y), up to", "subchondral bone"], 580, C - 40)
label(372, 262, "Ewing sarcoma", ["Diaphysis, medullary;", "onion-skin periosteum"], 392, C + 50)
label(522, 262, "Enchondroma", ["Medullary cavity; mostly", "small bones of hands/feet"], 462, C + 15)

# zone brackets (bottom row)
by = 316
def bracket(x0, x1, text, sub=None):
    o.append(f'<path d="M{x0},{by-6} L{x0},{by} L{x1},{by} L{x1},{by-6}" fill="none" stroke="{A}" stroke-width="1.1"/>')
    o.append(f'<text x="{(x0+x1)/2}" y="{by+13}" font-size="9" font-weight="700" fill="{A}" text-anchor="middle">{esc(text)}</text>')
    if sub:
        o.append(f'<text x="{(x0+x1)/2}" y="{by+24}" font-size="8" fill="{INK2}" text-anchor="middle">{esc(sub)}</text>')

bracket(56, 126, "Epiphysis", "beyond the plate")
bracket(134, 228, "Metaphysis", "flared end of shaft")
bracket(232, 432, "Diaphysis", "shaft: cortex + medulla")
o.append(f'<line x1="130" y1="{C+64}" x2="130" y2="{by+30}" stroke="{A}" stroke-width=".8" stroke-dasharray="2 2"/>')
o.append(f'<text x="130" y="{by+40}" font-size="8.6" font-weight="700" fill="{A}" text-anchor="middle">Physis (growth plate)</text>')
# legend
lx = 470
o.append(f'<rect x="{lx}" y="{by-4}" width="11" height="9" fill="{MAL}"/><text x="{lx+16}" y="{by+4}" font-size="8.4" fill="{INK}">Malignant</text>')
o.append(f'<rect x="{lx}" y="{by+10}" width="11" height="9" fill="{BEN}" stroke="{INK}" stroke-width=".6"/><text x="{lx+16}" y="{by+18}" font-size="8.4" fill="{INK}">Benign (GCT locally aggressive)</text>')
o.append(f'<text x="{lx}" y="{by+33}" font-size="8" font-style="italic" fill="{INK2}">Left end: child (open plate) · right end: adult</text>')
o.append("</svg>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch27_bone_sites.svg"), "w").write("".join(o))
print("ok")
