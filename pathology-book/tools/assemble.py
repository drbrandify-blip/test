#!/usr/bin/env python3
"""Assemble the complete book: covers + prelims (roman) + chapters + back matter (arabic) with a generated TOC."""
import os, re, sys, json, html as _html
sys.path.insert(0, os.path.dirname(__file__))
import build as B
from bs4 import BeautifulSoup
import pdfplumber
from pypdf import PdfReader, PdfWriter

ROOT = B.ROOT
OUT = B.OUT
CHAPTERS = [f"ch{i:02d}" for i in range(1, 32)]
FRONT = ["front/fm02_howto", "front/fm03_syllabus", "front/fm04_examcraft", "front/fm05_plan"]
BACK = ["back/bm01_tables", "back/bm02_buzzwords", "back/bm03_atlas", "back/bm04_top_seqs", "back/bm05_mock", "back/bm06_checklist"]
TITLE = "Pathology: All-in-One — Special Pathology for 4th Year MBBS"


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def sections_of(cid):
    soup = BeautifulSoup(open(os.path.join(ROOT, "chapters", cid + ".html"), encoding="utf-8").read(), "html.parser")
    meta = json.loads(soup.find("script", attrs={"class": "meta"}).string)
    secs = []
    for h2 in soup.find_all("h2"):
        sn = h2.find("span", class_="sn")
        num = sn.get_text(strip=True) if sn else ""
        title = h2.get_text(" ", strip=True)
        if num and title.startswith(num):
            title = title[len(num):].strip()
        secs.append((num, title))
    return meta, secs


def locate(pdf_path, needles):
    found = {}
    with pdfplumber.open(pdf_path) as pdf:
        texts = [norm(p.extract_text() or "") for p in pdf.pages]
    for key, needle in needles:
        n = norm(needle)[:40]
        for i, t in enumerate(texts):
            if n and n in t:
                found[key] = i
                break
    return found


def fm_title(path):
    s = open(os.path.join(ROOT, path + ".html"), encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else path


def toc_html(front_entries, chapter_entries, back_entries):
    rows = ['<div class="fm-head" data-head="CONTENTS"><div class="kicker">Pathology: All-in-One · Special Pathology</div><h1>Contents</h1>'
            '<p>Page numbers for every chapter, section, exam zone and night-before page.</p></div>', '<div class="toc">',
            '<div class="toc-part">Before you begin</div>']
    for title, pg in front_entries:
        rows.append(f'<div class="toc-row fm"><span class="t">{title}</span><span class="dots"></span><span class="p">{pg}</span></div>')
    cur = None
    for e in chapter_entries:
        if e["part"] != cur:
            cur = e["part"]
            rows.append(f'<div class="toc-part">{B.PARTS[cur]}</div>')
        rows.append(f'<div class="toc-ch keep"><div class="toc-row ch"><span class="n">{e["ch"]:02d}</span><span class="t">{e["title"]}</span><span class="dots"></span><span class="p">{e["page"]}</span></div>')
        subs = [f'<span class="s"><b>{num}</b> {t} <i>{pg}</i></span>' for num, t, pg in e["secs"]]
        subs.append(f'<span class="s ex"><b>Exam Zone</b> <i>{e["exam"]}</i></span>')
        subs.append(f'<span class="s ex"><b>Night-before page</b> <i>{e["rev"]}</i></span>')
        rows.append('<div class="toc-subs">' + " ".join(subs) + "</div></div>")
    rows.append('<div class="toc-part">Rapid revision &amp; practice</div>')
    for title, pg in back_entries:
        rows.append(f'<div class="toc-row fm"><span class="t">{title}</span><span class="dots"></span><span class="p">{pg}</span></div>')
    rows.append("</div>")
    return "\n".join(rows)


def render_fragment(name, body_html, start, folio, skip_all=False):
    path = os.path.join(OUT, name + ".html")
    open(path, "w", encoding="utf-8").write(B.page_html(body_html, name))
    raw = os.path.join(OUT, name + ".raw.pdf")
    B.render_pdf(path, raw)
    m = re.search(r'data-head="([^"]*)"', body_html)
    hl = (_html.unescape(m.group(1)).upper(), "") if m else ("", "")
    return B.overlay(raw, os.path.join(OUT, name + ".pdf"), start, hl, "", folio=folio, skip_all=skip_all)


CACHE = os.path.join(OUT, "_starts.json")


def cached_build(cid, start, folio="arabic"):
    try:
        cache = json.load(open(CACHE))
    except Exception:
        cache = {}
    src = os.path.join(ROOT, cid + ".html") if "/" in cid else os.path.join(ROOT, "chapters", cid + ".html")
    pdf = os.path.join(OUT, cid.replace("/", "_") + ".pdf")
    deps = [src, os.path.join(ROOT, "assets", "book.css"), os.path.join(ROOT, "tools", "build.py"), os.path.join(ROOT, "tools", "diagrams.py")]
    if os.path.exists(pdf) and cache.get(cid) == [start, folio] and all(os.path.getmtime(pdf) > os.path.getmtime(d) for d in deps):
        return len(PdfReader(pdf).pages), (sections_of(cid)[0] if "/" not in cid else None)
    n, meta = B.build_chapter(cid, start, folio=folio)
    cache[cid] = [start, folio]
    json.dump(cache, open(CACHE, "w"))
    return n, meta


def main():
    os.makedirs(OUT, exist_ok=True)
    page, ch_entries = 1, []
    for cid in CHAPTERS:
        n, meta = cached_build(cid, page)
        meta2, secs = sections_of(cid)
        pdfp = os.path.join(OUT, cid + ".pdf")
        needles = [(f"s{i}", (num + " " + t) if num else t) for i, (num, t) in enumerate(secs)]
        needles += [("exam", "Past-Paper Pattern SEQs"), ("rev", "The Night-Before Page")]
        loc = locate(pdfp, needles)
        ch_entries.append({"ch": int(meta2["ch"]), "part": meta2["part"], "title": meta2["title"], "page": page,
                           "secs": [(num, t, page + loc.get(f"s{i}", 0)) for i, (num, t) in enumerate(secs)],
                           "exam": page + loc.get("exam", 0), "rev": page + loc.get("rev", n - 1), "n": n})
        print(f"{cid}: pages {page}-{page+n-1}", flush=True)
        page += n
    back_entries = []
    for bm in BACK:
        n, _ = cached_build(bm, page)
        back_entries.append((fm_title(bm), page))
        print(f"{bm}: pages {page}-{page+n-1}", flush=True)
        page += n
    last_arabic = page - 1
    # prelims
    B.build_chapter("front/fm01_title", 1, folio="roman")
    n_title = B.overlay(os.path.join(OUT, "front_fm01_title.raw.pdf"), os.path.join(OUT, "front_fm01_title.pdf"), 1, ("", ""), "", skip_all=True)
    fake_front = [(fm_title(f), "x") for f in FRONT]
    n_toc = render_fragment("contents", toc_html(fake_front, ch_entries, back_entries), n_title + 1, "roman")
    rp = n_title + n_toc + 1
    front_entries = []
    for f in FRONT:
        n, _ = cached_build(f, rp, folio="roman")
        front_entries.append((fm_title(f), B.roman(rp)))
        rp += n
    n_toc2 = render_fragment("contents", toc_html(front_entries, ch_entries, back_entries), n_title + 1, "roman")
    assert n_toc2 == n_toc, "contents length changed"
    prelim_total = rp - 1
    blank_needed = prelim_total % 2 == 1
    for c in ["front/cover", "back/cover_back"]:
        name = c.replace("/", "_")
        body, _ = B.process(open(os.path.join(ROOT, c + ".html"), encoding="utf-8").read(), name)
        hp = os.path.join(OUT, name + ".html")
        open(hp, "w", encoding="utf-8").write(B.page_html(body, name))
        B.render_pdf(hp, os.path.join(OUT, name + ".pdf"))
    if blank_needed:
        hp = os.path.join(OUT, "blank.html")
        open(hp, "w").write(B.page_html('<p class="muted small" style="text-align:center;margin-top:120mm">Notes</p>', "blank"))
        B.render_pdf(hp, os.path.join(OUT, "blank.raw.pdf"))
        B.overlay(os.path.join(OUT, "blank.raw.pdf"), os.path.join(OUT, "blank.pdf"), rp, ("", ""), "", skip_all=True)
    order = ["front_fm01_title", "contents"] + [f.replace("/", "_") for f in FRONT] + (["blank"] if blank_needed else []) \
        + CHAPTERS + [b.replace("/", "_") for b in BACK]
    titles = {"front_fm01_title": "Title page", "contents": "Contents"}
    for f in FRONT:
        titles[f.replace("/", "_")] = fm_title(f)
    for e, cid in zip(ch_entries, CHAPTERS):
        titles[cid] = f"{e['ch']:02d}  " + _html.unescape(re.sub(r"<[^>]+>", "", e["title"]))
    for b in BACK:
        titles[b.replace("/", "_")] = fm_title(b)
    w = PdfWriter()
    def add(name):
        s = len(w.pages)
        for p in PdfReader(os.path.join(OUT, name + ".pdf")).pages:
            w.add_page(p)
        return s
    add("front_cover")
    marks = [(name, add(name)) for name in order]
    add("back_cover_back")
    w.add_outline_item("Cover", 0)
    parent = None
    cur_part = None
    part_of = {cid: e["part"] for e, cid in zip(ch_entries, CHAPTERS)}
    for name, s in marks:
        if name == "blank":
            continue
        if name in part_of:
            if part_of[name] != cur_part:
                cur_part = part_of[name]
                parent = w.add_outline_item(_html.unescape(B.PARTS[cur_part]), s)
            w.add_outline_item(_html.unescape(titles.get(name, name)), s, parent=parent)
        else:
            parent = None if name not in part_of else parent
            w.add_outline_item(_html.unescape(titles.get(name, name)), s)
    w.add_metadata({"/Title": TITLE, "/Subject": "4th-year MBBS Special Pathology, Modules 10–12",
                    "/Author": "Pathology: All-in-One", "/Keywords": "Pathology, Special Pathology, MBBS, Robbins, Pakistan"})
    w.page_mode = "/UseOutlines"
    with open(os.path.join(OUT, "BOOK_full.pdf"), "wb") as fh:
        w.write(fh)
    wi = PdfWriter()
    for name in order:
        for p in PdfReader(os.path.join(OUT, name + ".pdf")).pages:
            wi.add_page(p)
    with open(os.path.join(OUT, "BOOK_interior_print.pdf"), "wb") as fh:
        wi.write(fh)
    wc = PdfWriter()
    for name in ["front_cover", "back_cover_back"]:
        for p in PdfReader(os.path.join(OUT, name + ".pdf")).pages:
            wc.add_page(p)
    with open(os.path.join(OUT, "BOOK_cover.pdf"), "wb") as fh:
        wc.write(fh)
    print("prelims:", prelim_total, "+blank" if blank_needed else "", "| arabic pages:", last_arabic, "| total incl. covers:", len(w.pages))


if __name__ == "__main__":
    main()
