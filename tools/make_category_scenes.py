#!/usr/bin/env python3
"""
Portadas de categoría: productos reales recortados, flotando con ligero ángulo
sobre un fondo verde pino oscuro con brillo cálido — el mismo ambiente dramático
de estudio que la foto de Herramientas, pero con nuestras propias fotos.
"""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

HERE = Path(__file__).parent
CUT = HERE / "cutouts"
OUT = HERE.parent / "assets/img"
W, H = 1200, 900

PINE_DARK = (12, 24, 18)
PINE_MID = (26, 46, 34)
GLOW = (150, 130, 70)


def scene_bg():
    bg = Image.new("RGB", (W, H), PINE_DARK)
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(PINE_DARK[i] + (PINE_MID[i] - PINE_DARK[i]) * (1 - abs(t - .35) / .8)) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    vign = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vign)
    vd.ellipse((-260, -320, W * .85, H * .55), fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(160))
    glow_layer = Image.new("RGB", (W, H), GLOW)
    bg = Image.composite(Image.blend(bg, glow_layer, 0.35), bg, vign.point(lambda p: int(p * 0.9)))
    edge = Image.new("L", (W, H), 0)
    ed = ImageDraw.Draw(edge)
    ed.rectangle((0, 0, W, H), fill=90)
    ed.rounded_rectangle((70, 70, W - 70, H - 70), 40, fill=0)
    edge = edge.filter(ImageFilter.GaussianBlur(90))
    bg = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), bg, edge)
    return bg.convert("RGBA")


def place(canvas, name, cx, cy, h, ang=0, flip=False, shadow_h_ratio=0.14):
    im = Image.open(CUT / f"{name}.png").convert("RGBA")
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    if ang:
        im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    w2, h2 = im.size

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sy = cy + int(h * 0.5 * 0.86)
    ImageDraw.Draw(sh).ellipse(
        (cx - int(w * .42), sy - int(h * shadow_h_ratio * .5), cx + int(w * .42), sy + int(h * shadow_h_ratio * .5)),
        fill=(5, 12, 8, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    canvas.alpha_composite(sh)

    rim = Image.new("RGBA", im.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rd.ellipse((-w2 * .3, -h2 * .35, w2 * .55, h2 * .45), fill=(255, 235, 190, 70))
    rim = rim.filter(ImageFilter.GaussianBlur(30))
    lit = Image.alpha_composite(im, Image.composite(rim, Image.new("RGBA", im.size, (0, 0, 0, 0)), im.split()[3]))

    canvas.alpha_composite(lit, (cx - w2 // 2, cy - h2 // 2))


def save(canvas, name):
    canvas.convert("RGB").save(OUT / f"{name}.jpg", quality=90, optimize=True, progressive=True)
    print(name, canvas.size)


# ---- Cintas y adhesivos ----
c = scene_bg()
place(c, "cinta-pesada", 190, 470, 360, ang=8)
place(c, "cinta-ducto", 430, 430, 330, ang=-10)
place(c, "cinta-cera-x-300", 660, 420, 470, ang=6)
place(c, "cinta-aluminio", 890, 460, 280, ang=-14)
place(c, "cinta-100micras", 1030, 560, 260, ang=12)
place(c, "pantera", 1140, 610, 380, ang=-6)
save(c, "cat-cintas")

# ---- Zunchado ----
c = scene_bg()
place(c, "zuncho", 430, 480, 560, ang=-8)
place(c, "grapas", 830, 500, 400, ang=10)
save(c, "cat-zunchado")

# ---- Plástico stretch ----
c = scene_bg()
place(c, "strech-45", 340, 490, 480, ang=-12)
place(c, "strech-12.5negro", 760, 460, 430, ang=9)
save(c, "cat-stretch")

# Nota: cat-papeleria.jpg y cat-etiquetas.jpg YA NO se generan aquí — son
# fotos/banners reales (ver papeleria-banner.png, etiquetas-y-recibos.png en
# IMAGENES.md). No volver a correr esos bloques.

# ---- Cartón y protección ----
c = scene_bg()
place(c, "carton-corrugado-cut", 300, 500, 640, ang=-6)
place(c, "plastico-burbuja-cut", 700, 470, 460, ang=10)
place(c, "yumbolon-cut", 980, 480, 510, ang=-10)
save(c, "cat-carton")
