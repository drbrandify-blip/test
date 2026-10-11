"""SVG diagram generators for the book (2-colour: ink + haematoxylin purple)."""
import json, math, re, subprocess, html
from PIL import ImageFont

A = "#5b2a86"; A60 = "#9d7fb6"; A40 = "#bdaacf"; A20 = "#ded4e7"; A10 = "#efeaf3"; A05 = "#f7f4f9"
INK = "#141414"; INK2 = "#3a3a3a"; G20 = "#d9d9d9"; G05 = "#f6f6f6"; G40 = "#a8a8a8"
FONT_R = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FONT_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
_fc = {}


def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]


def tw(text, size=10, bold=False):
    f = font(FONT_B if bold else FONT_R, int(round(size * 4)))
    return f.getlength(text) / 4.0


def wrap(text, width, size=10, bold=False):
    words = str(text).split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, size, bold) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def esc(s):
    return html.escape(str(s), quote=False)


def rich(s):
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r'<tspan font-weight="700">\1</tspan>', s)


def svg_open(w, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'font-family="BookSans, sans-serif" {extra}>')


# ------------------------------------------------------------------ MIND MAP
def mindmap(spec, W=665):
    W = spec.get("W", W)
    center = spec.get("center", "")
    br = spec.get("branches", [])
    n = len(br)
    nl = math.ceil(n / 2)
    left, right = br[:nl], br[nl:]
    colw = 214
    fs, hfs, lh, pad, gap = 10.3, 10.8, 13.4, 7, 9

    def box(b):
        title_lines = wrap(b.get("t", ""), colw - 2 * pad, hfs, True)
        items = []
        for it in b.get("items", []):
            ls = wrap(it.replace("**", ""), colw - 2 * pad - 9, fs)
            items.append((it, ls))
        hh = len(title_lines) * 12.5 + 7
        ih = sum(len(ls) * lh for _, ls in items) + (len(items) * 1.5) + 6
        return title_lines, items, hh, hh + ih

    lb = [box(b) for b in left]
    rb = [box(b) for b in right]
    Hl = sum(b[3] for b in lb) + gap * (len(lb) - 1) if lb else 0
    Hr = sum(b[3] for b in rb) + gap * (len(rb) - 1) if rb else 0
    H = max(Hl, Hr, 90) + 8
    out = [svg_open(W, H)]
    cx, cy = W / 2, H / 2
    clines = wrap(center, 120, 13, True)
    ch = len(clines) * 16 + 18
    cw = max(max(tw(l, 13, True) for l in clines) + 30, 110)

    def draw_col(boxes, x0, side):
        H0 = sum(b[3] for b in boxes) + gap * (len(boxes) - 1)
        y = (H - H0) / 2
        parts = []
        for (tl, items, hh, bh) in boxes:
            if side == "L":
                x1, y1 = cx - cw / 2, cy
                x2, y2 = x0 + colw, y + hh / 2
            else:
                x1, y1 = cx + cw / 2, cy
                x2, y2 = x0, y + hh / 2
            mx = (x1 + x2) / 2
            parts.append(f'<path d="M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{A60}" stroke-width="1.6"/>')
            parts.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2.6" fill="{A}"/>')
            parts.append(f'<rect x="{x0}" y="{y:.1f}" width="{colw}" height="{bh:.1f}" rx="6" fill="#fff" stroke="{A40}" stroke-width="1"/>')
            parts.append(f'<path d="M{x0},{y+6:.1f} a6,6 0 0 1 6,-6 h{colw-12} a6,6 0 0 1 6,6 v{hh-6:.1f} h-{colw} z" fill="{A}"/>')
            ty = y + 12.5
            for l in tl:
                parts.append(f'<text x="{x0+pad}" y="{ty:.1f}" font-size="{hfs}" font-weight="700" fill="#fff">{esc(l)}</text>')
                ty += 12.5
            iy = y + hh + 4 + fs
            for it, ls in items:
                parts.append(f'<circle cx="{x0+pad+2.5}" cy="{iy-3.4:.1f}" r="1.7" fill="{A}"/>')
                for l in ls:
                    parts.append(f'<text x="{x0+pad+9}" y="{iy:.1f}" font-size="{fs}" fill="{INK}">{rich(l)}</text>')
                    iy += lh
                iy += 1.5
            y += bh + gap
        return parts

    out += draw_col(lb, 0, "L")
    out += draw_col(rb, W - colw, "R")
    out.append(f'<rect x="{cx-cw/2:.1f}" y="{cy-ch/2:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="{min(ch/2,22):.1f}" fill="{INK}"/>')
    ty = cy - ch / 2 + 9 + 13
    for l in clines:
        out.append(f'<text x="{cx:.1f}" y="{ty:.1f}" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">{esc(l)}</text>')
        ty += 16
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ FLOWCHART (graphviz)
def _lab(s, width=26):
    s = s.strip()
    if "\\n" in s:
        return s.replace("\\n", "\n")
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return "\n".join(lines)


def flow(text, direction="TB", width=26):
    nodes, edges, order, ranks = {}, [], [], []

    def node(raw):
        raw = raw.strip()
        kind = "n"
        if raw.startswith("*"): kind, raw = "e", raw[1:].strip()
        elif raw.startswith("?"): kind, raw = "d", raw[1:].strip()
        elif raw.startswith("!"): kind, raw = "k", raw[1:].strip()
        elif raw.startswith("~"): kind, raw = "g", raw[1:].strip()
        key = raw
        if key not in nodes:
            nodes[key] = (f"n{len(nodes)}", kind)
            order.append(key)
        elif kind != "n":
            nodes[key] = (nodes[key][0], kind)
        return nodes[key][0]

    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        if line.lower().startswith("rank:"):
            ranks.append([p.strip().lstrip("*?!~").strip() for p in line[5:].split("|")]); continue
        parts = re.split(r"\s*(-\[[^\]]*\]->|->|<->|--)\s*", line)
        prev = node(parts[0])
        i = 1
        while i < len(parts) - 1:
            op, nxt = parts[i], node(parts[i + 1])
            lab = ""
            m = re.match(r"-\[([^\]]*)\]->", op)
            if m: lab = m.group(1)
            edges.append((prev, nxt, lab, op))
            prev = nxt; i += 2
    g = [f'digraph G {{ rankdir={direction}; bgcolor="transparent"; nodesep=0.22; ranksep=0.32; pad=0.05;',
         f'node [fontname="Inter" fontsize=10 shape=box style="rounded,filled" fillcolor="white" color="{A}" penwidth=1.1 margin="0.13,0.06" fontcolor="{INK}"];',
         f'edge [color="{A}" penwidth=1.1 arrowsize=0.65 fontname="Inter" fontsize=8.5 fontcolor="{INK2}"];']
    for key in order:
        nid, kind = nodes[key]
        lab = _lab(key, width).replace('"', '\\"').replace("\n", "\\n")
        if kind == "e":
            g.append(f'{nid} [label="{lab}" fillcolor="{A}" fontcolor="white" fontname="Inter Bold" color="{A}"];')
        elif kind == "k":
            g.append(f'{nid} [label="{lab}" fillcolor="{INK}" fontcolor="white" fontname="Inter Bold" color="{INK}"];')
        elif kind == "d":
            g.append(f'{nid} [label="{lab}" shape=diamond style="filled" fillcolor="{A10}" margin="0.04,0.02"];')
        elif kind == "g":
            g.append(f'{nid} [label="{lab}" fillcolor="{G05}" color="{G40}" style="rounded,filled,dashed"];')
        else:
            g.append(f'{nid} [label="{lab}"];')
    for a, b, lab, op in edges:
        attrs = []
        if lab: attrs.append(f'label=" {lab} "')
        if op == "--": attrs.append('arrowhead=none style=dashed')
        if op == "<->": attrs.append('dir=both')
        g.append(f'{a} -> {b} [{" ".join(attrs)}];')
    for r in ranks:
        ids = [nodes[x][0] for x in r if x in nodes]
        g.append("{rank=same; " + "; ".join(ids) + ";}")
    g.append("}")
    res = subprocess.run(["dot", "-Tsvg"], input="\n".join(g).encode(), capture_output=True)
    svg = res.stdout.decode()
    if "<svg" not in svg:
        raise SystemExit("graphviz error: " + res.stderr.decode()[:400])
    svg = svg[svg.find("<svg"):]
    m = re.search(r'width="([\d.]+)pt" height="([\d.]+)pt"', svg)
    if m:
        w, h = float(m.group(1)) * 1.333, float(m.group(2)) * 1.333
        scale = min(1.0, 665 / w)
        svg = svg.replace(m.group(0), f'width="{w*scale:.0f}" height="{h*scale:.0f}"', 1)
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = svg.replace('font-family="Inter Bold"', 'font-family="BookSans" font-weight="700"').replace('font-family="Inter"', 'font-family="BookSans"')
    svg = svg.replace('<title>G</title>', '')
    svg = re.sub(r'<title>[^<]*</title>', '', svg)
    svg = re.sub(r'<polygon fill="transparent"[^>]*/>', '', svg)
    return svg


# ------------------------------------------------------------------ CYCLE
def cycle(spec, W=665, H=None):
    W = spec.get("W", W)
    steps = spec["steps"]
    center = spec.get("center", "")
    n = len(steps)
    R = spec.get("r", 120)
    bw = spec.get("bw", 150)
    H = H or (2 * R + 110)
    cx, cy = W / 2, H / 2
    out = [svg_open(W, H)]
    out.append(f'<defs><marker id="arw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{A}"/></marker></defs>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{A20}" stroke-width="9"/>')
    pos = []
    for i in range(n):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + R * math.cos(ang), cy + R * math.sin(ang), ang))
    for i in range(n):
        a1 = pos[i][2] + (2 * math.pi / n) * 0.30
        a2 = pos[i][2] + (2 * math.pi / n) * 0.70
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        x2, y2 = cx + R * math.cos(a2), cy + R * math.sin(a2)
        out.append(f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{A}" stroke-width="2" marker-end="url(#arw)"/>')
    for i, (x, y, ang) in enumerate(pos):
        st = steps[i]
        title = st["t"] if isinstance(st, dict) else st
        sub = st.get("s", "") if isinstance(st, dict) else ""
        tl = wrap(title, bw - 14, 10.5, True)
        sl = wrap(sub, bw - 14, 8.6) if sub else []
        h = len(tl) * 13 + len(sl) * 11 + 12
        out.append(f'<rect x="{x-bw/2:.1f}" y="{y-h/2:.1f}" width="{bw}" height="{h:.1f}" rx="8" fill="{"#fff" if i%2 else A10}" stroke="{A}" stroke-width="1.2"/>')
        ty = y - h / 2 + 6 + 10.5
        out.append(f'<circle cx="{x-bw/2+1:.1f}" cy="{y-h/2+1:.1f}" r="8" fill="{A}"/><text x="{x-bw/2+1:.1f}" y="{y-h/2+4.3:.1f}" font-size="9" font-weight="700" fill="#fff" text-anchor="middle">{i+1}</text>')
        for l in tl:
            out.append(f'<text x="{x:.1f}" y="{ty:.1f}" font-size="10.5" font-weight="700" fill="{INK}" text-anchor="middle">{esc(l)}</text>')
            ty += 13
        for l in sl:
            out.append(f'<text x="{x:.1f}" y="{ty-1:.1f}" font-size="8.6" fill="{INK2}" text-anchor="middle">{esc(l)}</text>')
            ty += 11
    if center:
        cl = wrap(center, R * 1.1, 12, True)
        ty = cy - (len(cl) - 1) * 7.5 + 4
        for l in cl:
            out.append(f'<text x="{cx:.1f}" y="{ty:.1f}" font-size="12" font-weight="700" fill="{A}" text-anchor="middle">{esc(l)}</text>')
            ty += 15
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ BAR CHART (horizontal)
def bar(spec, W=665):
    W = spec.get("W", W)
    labels, values = spec["labels"], spec["values"]
    unit = spec.get("unit", "")
    hl = set(spec.get("highlight", []))
    n = len(labels)
    rowh = spec.get("rowh", 20)
    lw = max(tw(l, 9.4) for l in labels) + 12
    H = n * rowh + 16
    mx = spec.get("max") or max(values) * 1.12
    out = [svg_open(W, H)]
    bx = lw + 4
    bw = W - bx - 60
    for i, (l, v) in enumerate(zip(labels, values)):
        y = 6 + i * rowh
        col = A if (i in hl or l in hl or not hl) else A40
        out.append(f'<text x="{lw}" y="{y+rowh/2+3.4:.1f}" font-size="9.4" fill="{INK}" text-anchor="end">{esc(l)}</text>')
        out.append(f'<rect x="{bx}" y="{y+3:.1f}" width="{max(1, v/mx*bw):.1f}" height="{rowh-6}" rx="2" fill="{col}"/>')
        out.append(f'<text x="{bx + v/mx*bw + 5:.1f}" y="{y+rowh/2+3.4:.1f}" font-size="9" font-weight="700" fill="{INK}">{v:g}{esc(unit)}</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ LINE CHART
def line(spec, W=665, H=230):
    W = spec.get("W", W); H = spec.get("H", H)
    xs = spec["x"]; series = spec["series"]
    x0, x1, y0, y1 = 44, W - 90, 14, H - 30
    allv = [v for s in series for v in s["y"] if v is not None]
    lo = spec.get("min", 0); hi = spec.get("max", max(allv) * 1.1)
    out = [svg_open(W, H)]
    for k in range(5):
        yv = lo + (hi - lo) * k / 4
        y = y1 - (yv - lo) / (hi - lo) * (y1 - y0)
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{G20}" stroke-width=".7"/>')
        if spec.get("yticks", True):
            out.append(f'<text x="{x0-6}" y="{y+3:.1f}" font-size="8.4" fill="{INK2}" text-anchor="end">{yv:g}</text>')
    if spec.get("ylabel"):
        out.append(f'<text transform="translate(12,{(y0+y1)/2:.0f}) rotate(-90)" font-size="8.6" fill="{INK2}" text-anchor="middle">{esc(spec["ylabel"])}</text>')
    step = (x1 - x0) / max(1, len(xs) - 1)
    for i, xv in enumerate(xs):
        out.append(f'<text x="{x0+i*step:.1f}" y="{y1+14}" font-size="8.4" fill="{INK2}" text-anchor="middle">{esc(xv)}</text>')
    cols = [A, INK, A60, G40]
    dashes = ["", "", "5 3", "2 2"]
    for si, s in enumerate(series):
        pts = [(x0 + i * step, y1 - (v - lo) / (hi - lo) * (y1 - y0)) for i, v in enumerate(s["y"]) if v is not None]
        c = cols[si % 4]
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.2" stroke-dasharray="%s" points="%s"/>' % (c, dashes[si % 4], " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
        for x, y in pts:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="{c}"/>')
        if spec.get("labels", False):
            for (x, y), v in zip(pts, [v for v in s["y"] if v is not None]):
                out.append(f'<text x="{x:.1f}" y="{y-6:.1f}" font-size="8" font-weight="700" fill="{c}" text-anchor="middle">{v:g}</text>')
        lx, ly = pts[-1]
        out.append(f'<text x="{lx+8:.1f}" y="{ly+3:.1f}" font-size="9" font-weight="700" fill="{c}">{esc(s["name"])}</text>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ STAGES (horizontal chevrons)
def stages(spec, W=665):
    W = spec.get("W", W)
    items = spec["items"]
    n = len(items)
    gapx = 6
    w = (W - gapx * (n - 1)) / n
    lines = [(wrap(it["t"], w - 18, 10, True), wrap(it.get("s", ""), w - 16, 8.8) if it.get("s") else []) for it in items]
    H = max(len(a) * 13 + len(b) * 11.5 for a, b in lines) + 22
    out = [svg_open(W, H)]
    for i, (tl, sl) in enumerate(lines):
        x = i * (w + gapx)
        tip = 9 if i < n - 1 else 0
        notch = 9 if i > 0 else 0
        fill = A if i % 2 == 0 else A10
        tc = "#fff" if i % 2 == 0 else INK
        sc = A10 if i % 2 == 0 else INK2
        out.append(f'<path d="M{x},{0} h{w-tip} l{tip},{H/2} l-{tip},{H/2} h-{w-tip} l{notch},-{H/2} z" fill="{fill}" stroke="{A}" stroke-width="1"/>')
        ty = 14 + 8
        for l in tl:
            out.append(f'<text x="{x+w/2+notch/2-tip/2:.1f}" y="{ty:.1f}" font-size="10" font-weight="700" fill="{tc}" text-anchor="middle">{esc(l)}</text>')
            ty += 13
        for l in sl:
            out.append(f'<text x="{x+w/2+notch/2-tip/2:.1f}" y="{ty:.1f}" font-size="8.8" fill="{sc}" text-anchor="middle">{esc(l)}</text>')
            ty += 11.5
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ ICONS
_S = 'fill="none" stroke="currentColor" stroke-width="2"'
ICONS = {
    "def": f'<svg viewBox="0 0 24 24"><path d="M4 4h12l4 4v12H4z" {_S}/><path d="M8 11h8M8 15h6" {_S}/></svg>',
    "concept": f'<svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.7.5 1.5 1.5 1.5 2.6h4c0-1.1.8-2.1 1.5-2.6A6 6 0 0 0 12 3z" {_S}/></svg>',
    "pk": f'<svg viewBox="0 0 24 24"><path d="M5 21V4M5 4h12l-2 4 2 4H5" {_S}/></svg>',
    "hook": f'<svg viewBox="0 0 24 24"><path d="M12 4a5 5 0 0 0-5 5c0 1 .3 2 .9 2.8L6 20h12l-1.9-8.2c.6-.8.9-1.8.9-2.8a5 5 0 0 0-5-5z" {_S}/><circle cx="12" cy="9" r="1.6" fill="currentColor"/></svg>',
    "trap": f'<svg viewBox="0 0 24 24"><path d="M12 3l10 18H2z" {_S}/><path d="M12 10v5M12 17.5v.5" {_S}/></svg>',
    "formula": f'<svg viewBox="0 0 24 24"><path d="M9 3v6L4 19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2L15 9V3M8 3h8M7 15h10" {_S}/></svg>',
    "worked": f'<svg viewBox="0 0 24 24"><rect x="5" y="4" width="14" height="17" rx="2" {_S}/><path d="M9 4V2h6v2M9 10h6M9 14h6M9 18h3" {_S}/></svg>',
    "practice": f'<svg viewBox="0 0 24 24"><path d="M6 3v6a4 4 0 0 0 8 0V3M10 13v3a5 5 0 0 0 10 0v-2" {_S}/><circle cx="20" cy="12" r="2" {_S}/></svg>',
    "molec": f'<svg viewBox="0 0 24 24"><path d="M7 3c0 6 10 6 10 12s-10 6-10 6M17 3c0 6-10 6-10 12M17 21c0-2-1-3.4-2.5-4.5" {_S}/><path d="M8.5 7h7M8.5 17h7M10 12h4" {_S}/></svg>',
    "spot": f'<svg viewBox="0 0 24 24"><path d="M6 21h13M9 21v-3h6M12 18v-3M8 4l4-1 3 9-4 1.3z" {_S}/><circle cx="12" cy="15" r="0.5" {_S}/><path d="M15.5 9.5a5 5 0 0 1 1 6.5" {_S}/></svg>',
}
MORPH_ICONS = {
    "gross": f'<svg viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z" {_S}/><circle cx="12" cy="12" r="3" {_S}/></svg>',
    "micro": ICONS["spot"],
}
LABELS = {"def": "Definition", "concept": "Concept Clear", "pk": "Pakistan Focus", "hook": "Memory Hook",
          "trap": "Exam Trap", "formula": "Lab Values", "worked": "Clinical Case", "practice": "Clinical Correlation",
          "molec": "Molecular Key", "spot": "Lab Spotter"}
