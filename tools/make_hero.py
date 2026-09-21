#!/usr/bin/env python3
"""Portada del inicio: productos reales recortados (tools/cutouts) sobre fondo cálido."""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "assets/img/hero-inicio.jpg"
W, H = 1600, 1200

top, bot = (247, 238, 225), (222, 201, 168)
bg = Image.new("RGB", (W, H))
d = ImageDraw.Draw(bg)
for y in range(H):
    t = y / (H - 1)
    d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
glow = Image.new("L", (W, H), 0)
ImageDraw.Draw(glow).ellipse((150, 60, 1450, 900), fill=90)
glow = glow.filter(ImageFilter.GaussianBlur(160))
bg.paste(Image.new("RGB", (W, H), (255, 250, 240)), (0, 0), glow)
canvas = bg.convert("RGBA")


def place(name, cx, base, h, flip=False):
    im = Image.open(HERE / "cutouts" / f"{name}.png").convert("RGBA")
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - int(w * .48), base - int(h * .045), cx + int(w * .48), base + int(h * .05)), fill=(70, 45, 15, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(sh)
    canvas.alpha_composite(im, (cx - w // 2, base - h))


# fila trasera
place("zuncho", 235, 760, 640)
place("cinta-cera-x-300", 520, 745, 470)
place("pantera", 735, 750, 520)
place("pegante-x300", 880, 750, 470)
place("strech-12.5negro", 1105, 750, 430)
place("rollo-cera", 1370, 745, 290)
# fila delantera
place("cinta-100micras", 215, 1080, 300)
place("cinta-18mm", 470, 1080, 330)
place("cinta-pesada", 690, 1075, 260)
place("cinta-ducto", 915, 1080, 260)
place("etiqueta-rollo1", 1170, 1078, 260)
place("grapas", 1420, 1085, 330)

canvas.convert("RGB").save(OUT, quality=90, optimize=True, progressive=True)
print(OUT, canvas.size)
