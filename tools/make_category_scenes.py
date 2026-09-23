#!/usr/bin/env python3
"""
Portadas de categoría como UNA escena de estudio: productos reales recortados,
conviviendo en un mismo fondo cálido, cada uno apoyado en su línea de base con
su propia sombra, a una escala relativa creíble entre sí. Sin rejilla de tarjetas.
"""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

HERE = Path(__file__).parent
CUT = HERE / "cutouts"
OUT = HERE.parent / "assets/img"
W, H = 1200, 900

TOP, BOT = (247, 238, 225), (219, 197, 162)


def scene_bg():
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((60, 30, W - 60, H * .78), fill=85)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    bg.paste(Image.new("RGB", (W, H), (255, 250, 240)), (0, 0), glow)
    return bg.convert("RGBA")


def place(canvas, name, cx, base, h, flip=False):
    im = Image.open(CUT / f"{name}.png").convert("RGBA")
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((cx - int(w * .46), base - int(h * .05), cx + int(w * .46), base + int(h * .05)), fill=(65, 45, 18, 130))
    sh = sh.filter(ImageFilter.GaussianBlur(13))
    canvas.alpha_composite(sh)
    canvas.alpha_composite(im, (cx - w // 2, base - h))


def save(canvas, name):
    canvas.convert("RGB").save(OUT / f"{name}.jpg", quality=90, optimize=True, progressive=True)
    print(name, canvas.size)


# ---- Cintas y adhesivos ----
c = scene_bg()
place(c, "cinta-pesada", 210, 760, 460)
place(c, "cinta-ducto", 460, 750, 400)
place(c, "cinta-cera-x-300", 700, 745, 560)
place(c, "cinta-aluminio", 930, 735, 330)
place(c, "cinta-100micras", 1000, 780, 300)
place(c, "pantera", 1140, 790, 460)
save(c, "cat-cintas")

# ---- Zunchado ----
c = scene_bg()
place(c, "zuncho", 420, 800, 700)
place(c, "grapas", 830, 790, 470)
save(c, "cat-zunchado")

# ---- Plástico stretch ----
c = scene_bg()
place(c, "strech-45", 310, 795, 560)
place(c, "strech-12.5negro", 730, 775, 520)
save(c, "cat-stretch")

# ---- Papelería ----
c = scene_bg()
place(c, "etiqueta-rollo1", 330, 760, 560)
place(c, "etiqueta-nailon", 700, 780, 620)
place(c, "rollo-cera", 990, 770, 480)
save(c, "cat-papeleria")

# ---- Cartón y protección (imágenes de referencia, no confirmadas como propias) ----
c = scene_bg()
place(c, "carton-corrugado-cut", 300, 810, 780)
place(c, "plastico-burbuja-cut", 720, 780, 560)
place(c, "yumbolon-cut", 1000, 800, 620)
save(c, "cat-carton")
