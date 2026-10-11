#!/usr/bin/env python3
"""Build pipeline: chapter fragments -> HTML -> PDF (Chromium) -> running heads/folios overlay.

usage:
  python3 tools/build.py ch16          # build one chapter preview (build/ch16.pdf)
"""
import sys, os, json, re, io, html as _html
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
import diagrams as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "chapters")
OUT = os.path.join(ROOT, "build")
ILLUS = os.path.join(ROOT, "illus")
FONTS = os.path.join(ROOT, "assets", "fonts")
CSS = open(os.path.join(ROOT, "assets", "book.css")).read()
BOOK = "Pathology: All-in-One"
SUB = "Special Pathology · 4th Year MBBS"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
ACCENT = (0x5b / 255, 0x2a / 255, 0x86 / 255)

PARTS = {
    "A": "Part A · Gastrointestinal Tract",
    "B": "Part B · Liver, Gallbladder & Pancreas",
    "C": "Part C · Lung",
    "D": "Part D · Blood & Lymphoid System",
    "E": "Part E · Kidney & Urinary Tract",
    "F": "Part F · Reproductive System & Breast",
    "G": "Part G · Endocrine System",
    "H": "Part H · Cardiovascular System",
    "I": "Part I · Musculoskeletal System",
    "J": "Part J · Nervous System",
    "K": "Part K · Skin",
}


def stars(n):
    n = int(n)
    return "★" * n + "☆" * (3 - n)


def opener(meta):
    ch = int(meta["ch"])
    part = PARTS.get(meta.get("part", ""), meta.get("part", ""))
    obj = "".join(f"<li>{o}</li>" for o in meta.get("objectives", []))
    rad = meta.get("radar", {})
    names = {"SEQ": "Theory SEQs", "BCQ": "BCQs / MCQs", "Viva": "Viva voce", "OSPE": "OSPE / slides"}
    rows = "".join(f"<tr><td>{names.get(k,k)}</td><td>{stars(v)}</td></tr>" for k, v in rad.items())
    note = meta.get("radar_note", "")
    rob = meta.get("robbins", "")
    rob_html = f'<div class="robbins"><b>Robbins link</b>{rob}</div>' if rob else ""
    return f"""
<section class="opener" data-ch="{ch}">
  <div class="part">{part}</div>
  <div class="chnum">{ch:02d}</div>
  <h1>{meta['title']}</h1>
  <p class="hook">{meta.get('hook','')}</p>
  <div class="opener-grid">
    <div class="objectives"><h4>By the end of this chapter you can</h4><ol>{obj}</ol></div>
    <div class="radar"><h4>Exam Radar</h4><table>{rows}</table><div class="note">{note}</div></div>
  </div>
  {rob_html}
</section>"""


def fig(svg, cap):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f"<figure>{svg}{c}</figure>"


def jload(txt, where):
    try:
        return json.loads(txt)
    except Exception as e:
        raise SystemExit(f"JSON error in {where}: {e}\n---\n{txt[:400]}")


def frag(s):
    return BeautifulSoup(s, "html.parser")


def process(fragment, name="?"):
    soup = BeautifulSoup(fragment, "html.parser")
    meta_el = soup.find("script", attrs={"class": "meta"})
    meta = None
    if meta_el:
        meta = jload(meta_el.string, name + " meta")
        meta_el.replace_with(frag(opener(meta)))
    for el in soup.select("div.mm"):
        spec = jload(el.get_text(), name + " mindmap")
        el.replace_with(frag(f'<div class="mmwrap">{fig(D.mindmap(spec), el.get("data-cap", ""))}</div>'))
    for el in soup.select("div.flow"):
        svg = D.flow(el.get_text(), el.get("data-dir", "TB"), int(el.get("data-w", 26)))
        el.replace_with(frag(fig(svg, el.get("data-cap", ""))))
    for cls, fn in (("cycle", D.cycle), ("bar", D.bar), ("line", D.line), ("stages", D.stages)):
        for el in soup.select(f"div.{cls}"):
            spec = jload(el.get_text(), f"{name} {cls}")
            el.replace_with(frag(fig(fn(spec), el.get("data-cap", ""))))
    for el in soup.select("div.illus"):
        p = os.path.join(ILLUS, el.get("data-src", ""))
        if not os.path.exists(p):
            raise SystemExit(f"{name}: missing illustration {p}")
        svg = open(p, encoding="utf-8").read()
        svg = svg[svg.find("<svg"):]
        w = el.get("data-width")
        style = f' style="width:{w};margin:0 auto;"' if w else ""
        el.replace_with(frag(f'<figure{style}>{svg}' + (f'<figcaption>{el.get("data-cap")}</figcaption>' if el.get("data-cap") else "") + "</figure>"))
    for el in soup.select("div.box"):
        kind = next((c for c in el.get("class", []) if c in D.LABELS), None)
        if not kind or el.find("div", class_="lbl", recursive=False):
            continue
        label = el.get("data-label", D.LABELS[kind])
        el.insert(0, frag(f'<div class="lbl">{D.ICONS[kind]}<span>{label}</span></div>'))
    for el in soup.select("div.morph"):
        for part, lab in (("gross", "Gross"), ("micro", "Microscopy")):
            d = el.find("div", class_=part, recursive=False)
            if d and not d.find("div", class_="mh", recursive=False):
                d.insert(0, frag(f'<div class="mh">{D.MORPH_ICONS[part]}<span>{d.get("data-label", lab)}</span></div>'))
    for el in soup.select("div.mcqset"):
        items = jload(el.get_text(), name + " mcqset")
        qs, ks = [], []
        for it in items:
            opts = "".join(f"<li>{o}</li>" for o in it["o"])
            qs.append(f'<div class="mcq"><div class="stem">{it["q"]}</div><ol class="opt">{opts}</ol></div>')
            ks.append(f'<li><b class="k">{it["a"]}</b>{it.get("e","")}</li>')
        title = el.get("data-keytitle", "Answer key with one-line reasons")
        el.replace_with(frag(f'<div class="mcqs">{"".join(qs)}</div><div class="keys"><h4>{title}</h4><ol>{"".join(ks)}</ol></div>'))
    for el in soup.select("div.vivaset"):
        items = jload(el.get_text(), name + " vivaset")
        rows = "".join(f'<div class="qa"><div>{q}</div><div>{a}</div></div>' for q, a in items)
        el.replace_with(frag(f'<div class="viva">{rows}</div>'))
    return str(soup), meta


def page_html(body, title="Book"):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{_html.escape(title)}</title>
<style>{CSS}</style></head><body>{body}</body></html>"""


def render_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page()
        pg.goto("file://" + html_path, wait_until="load")
        pg.wait_for_timeout(300)
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        b.close()


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, r in vals:
        while n >= v:
            out += r; n -= v
    return out


def overlay(pdf_in, pdf_out, start_page, head_left, head_right, skip_first=True, skip_all=False, folio="arabic"):
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for n, f in (("PopB", "Poppins-Bold.ttf"), ("PopR", "Poppins-Regular.ttf"), ("PopM", "Poppins-Medium.ttf")):
        try:
            pdfmetrics.registerFont(TTFont(n, os.path.join(FONTS, f)))
        except Exception:
            pass
    r = PdfReader(pdf_in)
    w = PdfWriter()
    if skip_all:
        for page in r.pages:
            w.add_page(page)
        with open(pdf_out, "wb") as f:
            w.write(f)
        return len(r.pages)
    W0, H0 = float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(W0, H0), initialFontName="PopR", initialFontSize=7)
    for i, page in enumerate(r.pages):
        pno = start_page + i
        W, H = float(page.mediabox.width), float(page.mediabox.height)
        c.setPageSize((W, H))
        odd = pno % 2 == 1
        if not (skip_first and i == 0):
            c.setStrokeColorRGB(*ACCENT); c.setLineWidth(0.6)
            c.line(17 * mm, H - 14.2 * mm, W - 17 * mm, H - 14.2 * mm)
            c.setFillColorRGB(*ACCENT); c.setFont("PopB", 7)
            c.drawString(17 * mm, H - 12.4 * mm, head_left[0])
            lw = c.stringWidth(head_left[0], "PopB", 7)
            c.setFillColorRGB(0.08, 0.08, 0.08); c.setFont("PopM", 7.2)
            c.drawString(17 * mm + lw + 2.2 * mm, H - 12.4 * mm, head_left[1])
            c.setFillColorRGB(0.42, 0.42, 0.42); c.setFont("PopR", 6.8)
            c.drawRightString(W - 17 * mm, H - 12.4 * mm, head_right)
        c.setFont("PopB", 8)
        label = roman(pno) if folio == "roman" else str(pno)
        bw = max(8 * mm, c.stringWidth(label, "PopB", 8) + 4 * mm)
        y = 8.5 * mm
        x = W - 17 * mm - bw if odd else 17 * mm
        c.setFillColorRGB(*ACCENT); c.roundRect(x, y, bw, 5.2 * mm, 1.2 * mm, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1); c.drawCentredString(x + bw / 2, y + 1.6 * mm, label)
        c.setFillColorRGB(0.42, 0.42, 0.42); c.setFont("PopR", 6.6)
        txt = f"{BOOK}  ·  {SUB}"
        if odd:
            c.drawRightString(x - 3 * mm, y + 1.7 * mm, txt)
        else:
            c.drawString(x + bw + 3 * mm, y + 1.7 * mm, txt)
        c.showPage()
    c.save()
    buf.seek(0)
    ovr = PdfReader(buf)
    for i, page in enumerate(r.pages):
        page.merge_page(ovr.pages[i])
        w.add_page(page)
    for page in w.pages:
        try:
            page.compress_content_streams()
        except Exception:
            pass
    with open(pdf_out, "wb") as f:
        w.write(f)
    return len(r.pages)


def build_chapter(cid, start_page=1, folio="arabic"):
    if "/" in cid:
        src = os.path.join(ROOT, cid + ".html")
        cid = cid.replace("/", "_")
    else:
        src = os.path.join(CH, cid + ".html")
    body, meta = process(open(src, encoding="utf-8").read(), cid)
    hp = os.path.join(OUT, cid + ".html")
    open(hp, "w", encoding="utf-8").write(page_html(body, cid))
    raw = os.path.join(OUT, cid + ".raw.pdf")
    render_pdf(hp, raw)
    if meta:
        hl = (f"CHAPTER {int(meta['ch']):02d}", _html.unescape(re.sub(r"<[^>]+>", "", meta.get("short", meta["title"]))))
        hr = _html.unescape(PARTS.get(meta.get("part", ""), ""))
    else:
        m = re.search(r'data-head="([^"]*)"', body)
        hl, hr = ((m.group(1).upper(), "") if m else ("", "")), ""
    n = overlay(raw, os.path.join(OUT, cid + ".pdf"), start_page, hl, hr, folio=folio)
    return n, meta


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    arg = sys.argv[1] if len(sys.argv) > 1 else "ch16"
    n, meta = build_chapter(arg, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    print(f"{arg}: {n} pages")
