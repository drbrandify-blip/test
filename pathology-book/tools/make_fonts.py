"""Static Lora instances + TrueType (quadratic) Inter, so Chromium embeds real TrueType fonts."""
import os
from fontTools.ttLib import TTFont, newTable
from fontTools.varLib import instancer
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")
for src, ital in [("/tmp/Lora[wght].ttf", ""), ("/tmp/Lora-Italic[wght].ttf", "Italic")]:
    for wt, name in [(400, "Regular"), (600, "SemiBold"), (700, "Bold")]:
        instancer.instantiateVariableFont(TTFont(src), {"wght": wt}).save(os.path.join(OUT, f"Lora-{name}{ital}.ttf"))
def otf2ttf(src, dst):
    font = TTFont(src); order = font.getGlyphOrder(); gs = font.getGlyphSet()
    glyf = newTable("glyf"); glyf.glyphOrder = order; glyf.glyphs = {}
    for g in order:
        pen = TTGlyphPen(gs); gs[g].draw(Cu2QuPen(pen, 1.0, reverse_direction=True)); glyf.glyphs[g] = pen.glyph()
    font["glyf"] = glyf; font["loca"] = newTable("loca")
    m = font["maxp"]; m.tableVersion = 0x00010000
    for k in ["maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs", "maxStackElements", "maxSizeOfInstructions", "maxComponentElements"]:
        setattr(m, k, 0)
    m.maxZones = 1
    font["post"].formatType = 2.0; font["post"].extraNames = []; font["post"].mapping = {}
    font["head"].glyphDataFormat = 0
    del font["CFF "]
    if "VORG" in font: del font["VORG"]
    font.sfntVersion = "\x00\x01\x00\x00"; font.save(dst)
for wname in ["Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Italic"]:
    otf2ttf(f"/usr/share/fonts/opentype/inter/Inter-{wname}.otf", os.path.join(OUT, f"Inter-{wname}.ttf"))
print("fonts ready")
