#!/usr/bin/env python3
"""Genera portadas (hero y categorías) como composiciones de fotos reales."""
from PIL import Image, ImageDraw, ImageOps, ImageFilter
from pathlib import Path

REAL = Path("/Users/fredy/Documents/Info Fredy/01 INSUMOS/CONTENIDO ORIGINAL INSUMOS")
ROOT = Path("/Users/fredy/Documents/Info Fredy/01 INSUMOS")
FR = Path("/private/tmp/claude-501/-Users-fredy-Library-Application-Support-Claude-scratch-workspaces-6577ff4a-29c0-4a96-be98-19a27c4d4389-6496c886-76dd-4a05-a588-6ea977c66960-scratch-2026-09-04-228be1/d76037c5-1fe4-4e85-a5df-344f15b4467f/scratchpad/frames")
OUT = Path(__file__).parent.parent / "assets/img"
PAPER = (241, 228, 211)
GAP, RAD = 14, 22


def load(p):
    return Image.open(p).convert("RGB")


def warm(im, amt=0.10):
    return Image.blend(im, Image.eval(im, lambda v: v), 0).point(lambda v: v) if amt == 0 else         Image.blend(im, Image.merge("RGB", [Image.new("L", im.size, c) for c in PAPER]).convert("RGB") if False else im, 0)


def tile(im, size, focus=(0.5, 0.5)):
    return ImageOps.fit(im, size, Image.LANCZOS, centering=focus)


def compose(W, H, tiles):
    canvas = Image.new("RGB", (W, H), PAPER)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    placed = []
    for (x0, y0, x1, y1), im, focus in tiles:
        box = (int(x0 * W) + GAP // 2, int(y0 * H) + GAP // 2, int(x1 * W) - GAP // 2, int(y1 * H) - GAP // 2)
        sd.rounded_rectangle((box[0], box[1] + 6, box[2], box[3] + 6), RAD, fill=(60, 45, 20, 70))
        placed.append((box, im, focus))
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    canvas.paste(shadow, (0, 0), shadow)
    for box, im, focus in placed:
        w, h = box[2] - box[0], box[3] - box[1]
        t = tile(im, (w, h), focus)
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), RAD, fill=255)
        canvas.paste(t, box[:2], m)
    return canvas


def save(im, name):
    im.save(OUT / name, quality=88, optimize=True, progressive=True)
    print(name, im.size)


def vframe(name, y0=0.0, y1=1.0):
    im = load(FR / name)
    w, h = im.size
    return im.crop((0, int(h * y0), w, int(h * y1)))


L = lambda n: load(REAL / n)

# Portada del inicio (4:3)
save(compose(1600, 1200, [
    ((0, 0, .40, 1), vframe("v2_1.jpg", .12, .95), (.5, .5)),
    ((.40, 0, .70, .5), L("cinta-pesada.jpg"), (.5, .5)),
    ((.70, 0, 1, .5), L("pantera.jpg"), (.5, .55)),
    ((.40, .5, .70, 1), L("strech-45.jpg"), (.5, .5)),
    ((.70, .5, 1, 1), L("etiqueta-rollo1.jpg"), (.5, .5)),
]), "hero-inicio.jpg")

def cat(name, big, a, b, fa=(.5, .5), fb=(.5, .5), fbig=(.5, .5)):
    save(compose(1200, 900, [
        ((0, 0, .58, 1), big, fbig),
        ((.58, 0, 1, .5), a, fa),
        ((.58, .5, 1, 1), b, fb),
    ]), name)

cat("cat-cintas.jpg", L("cinta-100micras.jpg"), L("cinta-18mm.jpg"), L("cinta-pesada.jpg"))
cat("cat-zunchado.jpg", vframe("v2_0.jpg", .10, .90), vframe("v1_5.jpg", .05, .55), L("grapas.jpg"))
cat("cat-stretch.jpg", L("strech-45.jpg"), L("strech-15.jpg"), L("vinipel.jpg"))
cat("cat-carton.jpg", load(ROOT / "CORRUGADO-01"), load(ROOT / "papel-de-bolitas-de-aire.jpg"), load(ROOT / "yumbolon.jpeg"), fb=(.5, .5))
cat("cat-papeleria.jpg", L("etiqueta-rollo1.jpg"), L("etiqueta-nailon.jpg"), L("rollo-continuo.jpg"))

save(compose(1200, 900, [((0, 0, 1, 1), load(ROOT / "ChatGPT Image 10 abr 2025, 05_22_41 p.m..png"), (.5, .4))]), "cat-herramientas.jpg")


def banner(name, ims, W=1800, H=600):
    n = len(ims)
    save(compose(W, H, [((i / n, 0, (i + 1) / n, 1), im, f) for i, (im, f) in enumerate(ims)]), name)

banner("banner-cintas.jpg", [(L("cinta-100micras.jpg"), (.5, .5)), (L("cinta-18mm.jpg"), (.5, .5)), (L("cinta-pesada.jpg"), (.5, .5)), (L("cinta-aluminio.jpg"), (.5, .5))])
banner("banner-zunchado.jpg", [(vframe("v2_0.jpg", .10, .90), (.5, .5)), (vframe("v1_5.jpg", .05, .55), (.5, .5)), (L("grapas.jpg"), (.5, .5))])
banner("banner-stretch.jpg", [(L("strech-45.jpg"), (.5, .5)), (L("strech-30.jpg"), (.5, .5)), (L("strech-15.jpg"), (.5, .5)), (L("vinipel.jpg"), (.5, .5))])
banner("banner-carton.jpg", [(load(ROOT / "CORRUGADO-01"), (.5, .5)), (load(ROOT / "papel-de-bolitas-de-aire.jpg"), (.5, .5)), (load(ROOT / "yumbolon.jpeg"), (.5, .5))])
