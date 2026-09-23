#!/usr/bin/env python3
"""
Recreación ilustrada (NO foto real) de un tablero de herramientas de taller.
Usa una marca inventada de aspecto similar a marcas profesionales de
herramientas (no reproduce ningún logo real) — solo para representar la
categoría mientras no haya foto propia del inventario real.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math

W, H = 1200, 900
PINE_TOP = (46, 92, 66)
PINE_BOT = (18, 42, 30)
BOARD_HOLE = (12, 28, 20)
ACCENT = (196, 62, 46)
BRASS = (196, 158, 84)
BRASS_DK = (120, 92, 42)
STEEL_HI = (245, 247, 249)
STEEL_MID = (188, 194, 200)
STEEL_LO = (95, 101, 108)
HANDLE = (82, 56, 34)
HANDLE_HI = (120, 86, 54)

canvas = Image.new("RGB", (W, H), (14, 18, 16))
d = ImageDraw.Draw(canvas, "RGBA")

# --- pegboard panel: pine-green vertical gradient + subtle wood-grain noise ---
pad = 40
board = Image.new("RGB", (W - 2 * pad, H - 2 * pad))
bd = ImageDraw.Draw(board)
bh = board.height
for y in range(bh):
    t = y / (bh - 1)
    bd.line([(0, y), (board.width, y)], fill=tuple(int(PINE_TOP[i] + (PINE_BOT[i] - PINE_TOP[i]) * t) for i in range(3)))
# soft top-left sheen
sheen = Image.new("L", board.size, 0)
ImageDraw.Draw(sheen).ellipse((-200, -250, board.width * .7, board.height * .55), fill=45)
sheen = sheen.filter(ImageFilter.GaussianBlur(140))
board = ImageChops.add(board, Image.merge("RGB", (sheen, sheen, sheen)))
bdraw = ImageDraw.Draw(board)
for gy in range(30, board.height - 10, 46):
    for gx in range(30, board.width - 10, 46):
        bdraw.ellipse((gx - 4, gy - 4, gx + 4, gy + 4), fill=BOARD_HOLE)
        bdraw.ellipse((gx - 4, gy - 4, gx, gy), fill=(0, 0, 0, 40))

mask = Image.new("L", board.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, board.width - 1, board.height - 1), 18, fill=255)
canvas.paste(board, (pad, pad), mask)
d.rounded_rectangle((pad, pad, W - pad, H - pad), 18, outline=(8, 16, 11), width=3)


def metal_strip(w, h, base_hi=STEEL_HI, base_mid=STEEL_MID, base_lo=STEEL_LO, vertical=False):
    im = Image.new("RGB", (w, h))
    dd = ImageDraw.Draw(im)
    n = h if vertical else w
    for i in range(n):
        t = i / max(1, n - 1)
        # two-band brushed-metal highlight curve
        v = abs(math.sin(t * math.pi * 1.6 + 0.4))
        c = tuple(int(base_lo[k] + (base_hi[k] - base_lo[k]) * (0.25 + 0.75 * v)) for k in range(3))
        if t > 0.55:
            c = tuple(int(c[k] * (0.55 + 0.45 * (1 - (t - 0.55) / 0.45))) for k in range(3))
        if vertical:
            dd.line([(0, i), (w, i)], fill=c)
        else:
            dd.line([(i, 0), (i, h)], fill=c)
    return im


def drop_shadow(canvas_img, mask_im, pos, blur=16, opacity=140, offset=(6, 10)):
    sh = Image.new("RGBA", canvas_img.size, (0, 0, 0, 0))
    black = Image.new("RGBA", mask_im.size, (5, 15, 9, opacity))
    sh.paste(black, (pos[0] + offset[0], pos[1] + offset[1]), mask_im)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas_img.alpha_composite(sh) if canvas_img.mode == "RGBA" else canvas_img.paste(
        Image.alpha_composite(canvas_img.convert("RGBA"), sh).convert("RGB"), (0, 0))


base = canvas.convert("RGBA")


def stamp(piece, pos, shadow_blur=14, shadow_opacity=130, shadow_offset=(5, 9)):
    alpha = piece.split()[3]
    drop_shadow(base, alpha, pos, blur=shadow_blur, opacity=shadow_opacity, offset=shadow_offset)
    base.alpha_composite(piece, pos)


def peg(cx, top):
    p = Image.new("RGBA", (26, 40), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p)
    strip = metal_strip(10, 26, BRASS, (232, 205, 150), BRASS_DK)
    p.paste(strip, (8, 12))
    pd.ellipse((3, 0, 23, 16), fill=BRASS)
    pd.ellipse((6, 2, 20, 12), fill=(232, 205, 150))
    stamp(p, (cx - 13, top - 6), shadow_blur=6, shadow_opacity=110, shadow_offset=(3, 5))


try:
    fnt = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    fnt_b = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 30)
except Exception:
    fnt = ImageFont.load_default()
    fnt_b = fnt


def label(cx, y, text):
    ld = ImageDraw.Draw(base)
    tw = ld.textlength(text, font=fnt)
    ld.rounded_rectangle((cx - tw / 2 - 10, y, cx + tw / 2 + 10, y + 26), 5, fill=(10, 20, 14, 215))
    ld.text((cx - tw / 2, y + 4), text, font=fnt, fill=(230, 233, 230))


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    return m


# ---------------- Wrench (chrome, realistic gradient) ----------------
def wrench(cx, cy, ang=-16, L=210):
    w, h = int(L * 1.55), int(L * 0.62)
    piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    metal = metal_strip(w, h, vertical=False)
    y = h // 2
    bar_mask = Image.new("L", (w, h), 0)
    bmd = ImageDraw.Draw(bar_mask)
    bmd.rounded_rectangle((28, y - 11, w - 28, y + 11), 9, fill=255)
    for x0 in (0, w - 66):
        bmd.ellipse((x0, y - 30, x0 + 66, y + 30), fill=255)
        bmd.ellipse((x0 + 17, y - 15, x0 + 49, y + 15), fill=0)
    piece.paste(metal, (0, 0), bar_mask)
    pd = ImageDraw.Draw(piece)
    for x0 in (0, w - 66):
        pd.ellipse((x0, y - 30, x0 + 66, y + 30), outline=(30, 34, 38, 160), width=2)
    piece = piece.rotate(ang, expand=True, resample=Image.BICUBIC)
    stamp(piece, (cx - piece.width // 2, cy - piece.height // 2))


# ---------------- Pliers ----------------
def pliers(cx, cy, ang=-6):
    w, h = 170, 270
    piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(piece)
    pivot = (85, 122)

    def jaw_arm(tip, handle_end, jaw_w):
        jaw_mask = Image.new("L", (w, h), 0)
        jd = ImageDraw.Draw(jaw_mask)
        jd.line([tip, pivot], fill=255, width=jaw_w, joint="curve")
        jaw_metal = metal_strip(w, h, vertical=True)
        piece.paste(jaw_metal, (0, 0), jaw_mask)
        hgrad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hgrad)
        hd.line([pivot, handle_end], fill=HANDLE + (255,), width=24, joint="curve")
        hd.line([pivot, ((pivot[0] + handle_end[0]) // 2, (pivot[1] + handle_end[1]) // 2)],
                fill=HANDLE_HI + (255,), width=10, joint="curve")
        piece.alpha_composite(hgrad)
        pd.ellipse((handle_end[0] - 12, handle_end[1] - 12, handle_end[0] + 12, handle_end[1] + 12), fill=HANDLE)

    jaw_arm((62, 4), (38, 258), 17)
    jaw_arm((108, 4), (132, 258), 17)
    pd.ellipse((pivot[0] - 15, pivot[1] - 15, pivot[0] + 15, pivot[1] + 15), fill=STEEL_MID, outline=(35, 38, 42), width=2)
    pd.ellipse((pivot[0] - 6, pivot[1] - 9, pivot[0] + 2, pivot[1] - 1), fill=STEEL_HI)
    piece = piece.rotate(ang, expand=True, resample=Image.BICUBIC)
    stamp(piece, (cx - piece.width // 2, cy - piece.height // 2))


# ---------------- Screwdriver ----------------
def screwdriver(cx, cy, hcolor, ang=0, L=220):
    w = 60
    piece = Image.new("RGBA", (w, L), (0, 0, 0, 0))
    shaft_mask = Image.new("L", (w, L), 0)
    ImageDraw.Draw(shaft_mask).rectangle((23, 0, 37, L - 66), fill=255)
    metal = metal_strip(w, L, vertical=True)
    piece.paste(metal, (0, 0), shaft_mask)
    pd = ImageDraw.Draw(piece)
    hy0 = L - 72
    for i in range(hy0, L):
        t = (i - hy0) / (L - hy0)
        shade = tuple(int(hcolor[k] * (0.65 + 0.5 * math.sin(t * math.pi))) for k in range(3))
        pd.line([(12, i), (48, i)], fill=min(shade, (255, 255, 255)))
    hmask = Image.new("L", (w, L), 0)
    ImageDraw.Draw(hmask).rounded_rectangle((10, hy0, 50, L - 4), 14, fill=255)
    grip = Image.new("RGBA", (w, L), (0, 0, 0, 0))
    grip.paste(piece, (0, 0))
    out = Image.new("RGBA", (w, L), (0, 0, 0, 0))
    out.paste(piece, (0, 0), shaft_mask)
    hbody = Image.new("RGBA", (w, L), (0, 0, 0, 0))
    hbody.paste(Image.new("RGB", (w, L), hcolor), (0, 0), hmask)
    hi = Image.new("L", (w, L), 0)
    ImageDraw.Draw(hi).rounded_rectangle((14, hy0 + 4, 24, L - 8), 6, fill=90)
    hbody.paste(Image.new("RGB", (w, L), (255, 255, 255)), (0, 0), hi)
    out.alpha_composite(hbody)
    ImageDraw.Draw(out).rounded_rectangle((10, hy0, 50, L - 4), 14, outline=(20, 20, 20, 150), width=2)
    out = out.rotate(ang, expand=True, resample=Image.BICUBIC)
    stamp(out, (cx - out.width // 2, cy - out.height // 2), shadow_blur=10)


# ---------------- Tape measure ----------------
def tape(cx, cy, r=76):
    w = h = r * 2 + 10
    piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(piece)
    cx0 = cy0 = w // 2
    pd.ellipse((cx0 - r, cy0 - r, cx0 + r, cy0 + r), fill=ACCENT)
    hi = Image.new("L", (w, h), 0)
    ImageDraw.Draw(hi).ellipse((cx0 - r + 8, cy0 - r + 6, cx0 + r * .3, cy0 + r * .1), fill=70)
    hi = hi.filter(ImageFilter.GaussianBlur(18))
    piece.paste(Image.new("RGB", (w, h), (255, 210, 200)), (0, 0), hi)
    pd = ImageDraw.Draw(piece)
    pd.ellipse((cx0 - r, cy0 - r, cx0 + r, cy0 + r), outline=(60, 20, 14), width=4)
    inner = r - 17
    pd.ellipse((cx0 - inner, cy0 - inner, cx0 + inner, cy0 + inner), fill=(238, 236, 228))
    shade = Image.new("L", (w, h), 0)
    ImageDraw.Draw(shade).ellipse((cx0 - inner, cy0 - inner + inner, cx0 + inner, cy0 + inner), fill=40)
    piece.paste(Image.new("RGB", (w, h), (170, 168, 160)), (0, 0), shade)
    pd = ImageDraw.Draw(piece)
    pd.rectangle((cx0 + r - 34, cy0 - 15, cx0 + r + 28, cy0 + 15), fill=(238, 236, 228), outline=(120, 118, 112), width=2)
    for i in range(6):
        x = cx0 + r - 26 + i * 8
        pd.line((x, cy0 - 11, x, cy0 + 11), fill=(70, 68, 64), width=2)
    pd.text((cx0 - 20, cy0 - 12), "25ft", font=fnt, fill=(50, 48, 44))
    stamp(piece, (cx - w // 2, cy - h // 2))


# ---------------- Hammer ----------------
def hammer(cx, cy, ang=-25):
    w, h = 270, 130
    piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(piece)
    head_mask = Image.new("L", (w, h), 0)
    hd = ImageDraw.Draw(head_mask)
    hd.rounded_rectangle((0, 34, 78, 78), 10, fill=255)
    hd.polygon([(0, 40), (-20, 56), (0, 72)], fill=255)
    metal = metal_strip(w, h, vertical=False)
    piece.paste(metal, (0, 0), head_mask)
    pd.rounded_rectangle((0, 34, 78, 78), 10, outline=(25, 28, 30, 150), width=2)
    handle_grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hgd = ImageDraw.Draw(handle_grad)
    hgd.rounded_rectangle((66, 48, 260, 64), 8, fill=HANDLE + (255,))
    hgd.rounded_rectangle((66, 50, 260, 55), 4, fill=HANDLE_HI + (255,))
    piece.alpha_composite(handle_grad)
    piece = piece.rotate(ang, expand=True, resample=Image.BICUBIC)
    stamp(piece, (cx - piece.width // 2, cy - piece.height // 2))


# ---------------- Utility knife ----------------
def knife(cx, cy, ang=20):
    w, h = 230, 70
    piece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(piece)
    bgrad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd2 = ImageDraw.Draw(bgrad)
    for i in range(160):
        t = i / 160
        c = tuple(int(ACCENT[k] * (0.7 + 0.5 * math.sin(t * math.pi))) for k in range(3))
        bd2.line([(i, 15), (i, 45)], fill=min(c, (255, 255, 255)) + (255,))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 15, 160, 45), 10, fill=255)
    piece.paste(bgrad, (0, 0), mask)
    pd.rounded_rectangle((0, 15, 160, 45), 10, outline=(70, 20, 14, 180), width=2)
    blade = metal_strip(70, 30, STEEL_HI, STEEL_MID, STEEL_LO, vertical=False)
    bmask = Image.new("L", (70, 30), 0)
    ImageDraw.Draw(bmask).polygon([(0, 3), (66, 12), (0, 27)], fill=255)
    bpiece = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bpiece.paste(blade, (155, 15), bmask)
    piece.alpha_composite(bpiece)
    piece = piece.rotate(ang, expand=True, resample=Image.BICUBIC)
    stamp(piece, (cx - piece.width // 2, cy - piece.height // 2), shadow_blur=8)


# layout on pegboard
peg(230, 150); wrench(240, 245)
peg(470, 145); pliers(470, 265)
peg(660, 150); screwdriver(650, 260, (198, 60, 40), ang=-6, L=220)
peg(720, 150); screwdriver(720, 250, (222, 178, 60), ang=4, L=190)
peg(960, 160); tape(960, 250)
peg(300, 470); hammer(340, 540)
peg(870, 470); knife(870, 530)

label(240, 400, "LLAVES")
label(470, 420, "PINZAS")
label(685, 400, "DESTORNILLADORES")
label(960, 350, "METRO")
label(340, 610, "MARTILLO")
label(870, 590, "CORTADOR")

# lower shelf with hardware texture (brass screws)
shelf = Image.new("RGBA", (W - pad * 2 - 340, 60), (0, 0, 0, 0))
sd = ImageDraw.Draw(shelf)
sd.rounded_rectangle((0, 0, shelf.width - 1, 59), 10, fill=(14, 30, 20, 235))
for i in range(24):
    x = 30 + (i % 12) * 55
    y = 8 + (i // 12) * 30
    sd.ellipse((x, y, x + 18, y + 18), outline=BRASS_DK, width=2, fill=(180, 148, 82))
    sd.ellipse((x + 5, y + 4, x + 10, y + 9), fill=(232, 205, 150))
    sd.line((x + 4, y + 9, x + 14, y + 9), fill=BRASS_DK, width=2)
stamp(shelf.convert("RGBA"), (pad + 40, H - 160), shadow_blur=10)

# brand plate
plate_w, plate_h = 260, 70
plate = Image.new("RGBA", (plate_w, plate_h), (0, 0, 0, 0))
pd = ImageDraw.Draw(plate)
pd.rounded_rectangle((0, 0, plate_w - 1, plate_h - 1), 10, fill=(12, 16, 14, 240), outline=(70, 74, 80, 255), width=2)
pd.rectangle((0, 0, 9, plate_h), fill=BRASS)
pd.text((28, 10), "FORZA", font=fnt_b, fill=(240, 241, 242))
pd.text((28, 44), "PROFESSIONAL TOOLS", font=fnt, fill=(190, 180, 150))
stamp(plate, (W - pad - 40 - plate_w, H - pad - 40 - plate_h), shadow_blur=10)

final = base.convert("RGB").filter(ImageFilter.SMOOTH_MORE)
final.save("assets/img/cat-herramientas.jpg", quality=92, optimize=True, progressive=True)
print("saved", final.size)
