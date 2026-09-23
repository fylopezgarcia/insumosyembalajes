#!/usr/bin/env python3
"""Foto de la página Nosotros: producto en uso real (empacando), no genérica de IA."""
from PIL import Image, ImageDraw, ImageOps, ImageFilter
from pathlib import Path

FR = Path("/private/tmp/claude-501/-Users-fredy-Library-Application-Support-Claude-scratch-workspaces-6577ff4a-29c0-4a96-be98-19a27c4d4389-6496c886-76dd-4a05-a588-6ea977c66960-scratch-2026-09-04-228be1/d76037c5-1fe4-4e85-a5df-344f15b4467f/scratchpad/frames")
OUT = Path(__file__).parent.parent / "assets/img/bodega-nosotros.jpg"
PAPER = (241, 228, 211)
GAP, RAD = 14, 22


def vframe(name, y0=0.0, y1=1.0, x0=0.0, x1=1.0):
    im = Image.open(FR / name).convert("RGB")
    w, h = im.size
    return im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))


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


img = compose(1600, 1200, [
    ((0, 0, .62, 1), vframe("v1_3.jpg", .08, .95), (.55, .5)),
    ((.62, 0, 1, .5), vframe("v6b_6.jpg", .05, 1.0), (.5, .5)),
    ((.62, .5, 1, 1), vframe("v7b_5.jpg", .05, 1.0), (.5, .55)),
])
img.save(OUT, quality=90, optimize=True, progressive=True)
print(OUT, img.size)
