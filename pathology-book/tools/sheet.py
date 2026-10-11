#!/usr/bin/env python3
"""Contact sheet: python3 tools/sheet.py build/ch16.pdf [dpi] -> build/sheets/ch16_sN.png (8 pages per sheet)."""
import sys, os, subprocess, glob
from PIL import Image
pdf = sys.argv[1]; dpi = sys.argv[2] if len(sys.argv) > 2 else "45"
name = os.path.splitext(os.path.basename(pdf))[0]
d = os.path.join(os.path.dirname(pdf), "sheets"); os.makedirs(d, exist_ok=True)
tmp = os.path.join(d, "_" + name); os.makedirs(tmp, exist_ok=True)
for f in glob.glob(tmp + "/*.png"): os.remove(f)
subprocess.run(["pdftoppm", "-r", dpi, "-png", pdf, tmp + "/p"], check=True)
pages = sorted(glob.glob(tmp + "/*.png"))
per = 8
for s in range(0, len(pages), per):
    ims = [Image.open(p) for p in pages[s:s + per]]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w * 4 + 30, h * 2 + 10), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 4) * (w + 10), (i // 4) * (h + 10)))
    out = os.path.join(d, f"{name}_s{s // per + 1}.png"); sheet.save(out); print(out)
