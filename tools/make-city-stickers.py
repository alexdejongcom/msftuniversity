#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the Microsoft University city stickers.

Five circular die-cut stickers, each with a city skyline silhouette, the
MicrosoftUniversity wordmark and the city name. Transparent PNG, 1200x1200.

Run:  python3 tools/make-city-stickers.py
Needs: Pillow, and Segoe UI at FONT_DIR (falls back to any sans font).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = "/tmp/segoe/package/"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "swag", "stickers")

SIZE = 1200
SS = 2                      # supersample factor for smooth edges
CX = CY = SIZE * SS // 2
R_OUTER = int(578 * SS)     # die-cut edge
R_RING = int(548 * SS)      # inner art circle
MS_COLORS = ["#f25022", "#7fba00", "#00a4ef", "#ffb900"]


def font(name, size):
    for f in (name, "segoeui.ttf"):
        p = FONT_DIR + f
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def sky(draw, top, bottom, y0, y1):
    """Vertical gradient band."""
    t_, b_ = rgb(top), rgb(bottom)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line([(0, y), (SIZE * SS, y)], fill=lerp(t_, b_, t))


# --------------------------------------------------------------------------
# Skyline builders. Each draws dark silhouettes into `d`, sitting on `ground`.
# Coordinates are in supersampled space; `u` is a convenient unit (~1% width).
# --------------------------------------------------------------------------

def tower(d, x, w, h, ground, col, roof=None):
    d.rectangle([x, ground - h, x + w, ground], fill=col)
    if roof == "spire":
        d.polygon([(x + w / 2, ground - h - w * 1.4), (x, ground - h), (x + w, ground - h)], fill=col)
    elif roof == "point":
        d.polygon([(x + w / 2, ground - h - w * 0.8), (x, ground - h), (x + w, ground - h)], fill=col)
    elif roof == "dome":
        d.pieslice([x, ground - h - w / 2, x + w, ground - h + w / 2], 180, 360, fill=col)


def windows(d, x, w, h, ground, col, cols=3, rows=6):
    """Faint window grid on a tower."""
    pad = w * 0.16
    cw = (w - pad * 2) / (cols * 2 - 1)
    ch = h * 0.055
    gap = h * 0.045
    for r in range(rows):
        yy = ground - h + h * 0.10 + r * (ch + gap)
        if yy + ch > ground - h * 0.05:
            break
        for c in range(cols):
            xx = x + pad + c * cw * 2
            d.rectangle([xx, yy, xx + cw, yy + ch], fill=col)


def skyline_oslo(d, ground, u, dark, mid, light):
    # Holmenkollen ski jump — slender tower with a curved in-run
    d.polygon([(4 * u, ground), (9 * u, ground), (11 * u, ground - 40 * u),
               (7 * u, ground - 40 * u)], fill=mid)
    d.polygon([(11 * u, ground - 40 * u), (7 * u, ground - 40 * u),
               (14 * u, ground - 16 * u), (20 * u, ground - 11 * u),
               (20 * u, ground - 15 * u), (14 * u, ground - 20 * u)], fill=mid)
    # Opera house — low white wedge rising out of the fjord
    d.polygon([(16 * u, ground), (42 * u, ground), (42 * u, ground - 13 * u),
               (16 * u, ground)], fill=light)
    d.polygon([(30 * u, ground - 7 * u), (42 * u, ground - 13 * u),
               (42 * u, ground - 19 * u), (34 * u, ground - 13 * u)], fill=mid)
    # Barcode buildings — signature row of narrow towers
    xs = [44, 51, 58, 65, 72, 79]
    hs = [34, 44, 28, 50, 38, 46]
    for x, h in zip(xs, hs):
        tower(d, x * u, 5.2 * u, h * u, ground, dark)
        windows(d, x * u, 5.2 * u, h * u, ground, light, cols=2, rows=7)
    # Oslo Plaza (tall, rounded top)
    tower(d, 86 * u, 8 * u, 58 * u, ground, dark, roof="dome")
    windows(d, 86 * u, 8 * u, 58 * u, ground, light, cols=3, rows=8)


def skyline_newyork(d, ground, u, dark, mid, light):
    # Statue of Liberty (left, small)
    bx = 8 * u
    d.rectangle([bx, ground - 8 * u, bx + 9 * u, ground], fill=mid)
    d.polygon([(bx + 3 * u, ground - 8 * u), (bx + 6 * u, ground - 8 * u),
               (bx + 5.6 * u, ground - 22 * u), (bx + 3.4 * u, ground - 22 * u)], fill=mid)
    d.ellipse([bx + 3.4 * u, ground - 25 * u, bx + 5.8 * u, ground - 21.5 * u], fill=mid)
    for i in range(7):  # crown
        a = math.pi * (0.15 + 0.7 * i / 6)
        d.line([(bx + 4.6 * u, ground - 23.5 * u),
                (bx + 4.6 * u - math.cos(a) * 4 * u, ground - 23.5 * u - math.sin(a) * 4 * u)],
               fill=mid, width=int(u * 0.5))
    d.line([(bx + 5.5 * u, ground - 21 * u), (bx + 9 * u, ground - 30 * u)],
           fill=mid, width=int(u * 0.9))  # torch arm
    d.ellipse([bx + 8 * u, ground - 33 * u, bx + 11 * u, ground - 29 * u], fill=light)
    # Midtown blocks
    for x, h, w in [(22, 26, 7), (30, 34, 6), (37, 22, 8)]:
        tower(d, x * u, w * u, h * u, ground, dark)
        windows(d, x * u, w * u, h * u, ground, light, cols=3, rows=5)
    # Chrysler — stepped arches + spire
    cx0 = 46 * u
    tower(d, cx0, 9 * u, 40 * u, ground, dark)
    windows(d, cx0, 9 * u, 40 * u, ground, light, cols=3, rows=5)
    for i, wfrac in enumerate([1.0, 0.78, 0.56, 0.34]):
        w = 9 * u * wfrac
        y = ground - 40 * u - i * 3.4 * u
        d.pieslice([cx0 + (9 * u - w) / 2, y - 3.4 * u, cx0 + (9 * u + w) / 2, y + 3.4 * u],
                   180, 360, fill=dark)
    d.line([(cx0 + 4.5 * u, ground - 54 * u), (cx0 + 4.5 * u, ground - 68 * u)],
           fill=dark, width=int(u * 0.9))
    # Empire State — setbacks + mast
    ex = 60 * u
    tower(d, ex, 13 * u, 30 * u, ground, dark)
    tower(d, ex + 2.5 * u, 8 * u, 46 * u, ground, dark)
    tower(d, ex + 4.5 * u, 4 * u, 56 * u, ground, dark)
    windows(d, ex, 13 * u, 30 * u, ground, light, cols=4, rows=4)
    d.line([(ex + 6.5 * u, ground - 56 * u), (ex + 6.5 * u, ground - 66 * u)],
           fill=dark, width=int(u * 0.8))
    # One WTC — tapering
    wx = 78 * u
    d.polygon([(wx, ground), (wx + 11 * u, ground), (wx + 9 * u, ground - 62 * u),
               (wx + 2 * u, ground - 62 * u)], fill=dark)
    windows(d, wx + 1.5 * u, 8 * u, 58 * u, ground, light, cols=3, rows=8)
    d.line([(wx + 5.5 * u, ground - 62 * u), (wx + 5.5 * u, ground - 76 * u)],
           fill=dark, width=int(u * 0.7))
    tower(d, 92 * u, 7 * u, 30 * u, ground, dark)
    windows(d, 92 * u, 7 * u, 30 * u, ground, light, cols=2, rows=5)


def skyline_athens(d, ground, u, dark, mid, light):
    # Lycabettus hill (right, behind)
    d.polygon([(66 * u, ground), (84 * u, ground - 40 * u), (100 * u, ground)], fill=mid)
    d.rectangle([82.5 * u, ground - 43 * u, 85.5 * u, ground - 39 * u], fill=light)
    d.pieslice([82.5 * u, ground - 45 * u, 85.5 * u, ground - 41 * u], 180, 360, fill=light)
    # Acropolis rock
    d.polygon([(10 * u, ground), (16 * u, ground - 16 * u), (30 * u, ground - 22 * u),
               (58 * u, ground - 21 * u), (66 * u, ground - 13 * u), (72 * u, ground)], fill=mid)
    # Parthenon on top
    px0, px1 = 26 * u, 60 * u
    base = ground - 22 * u
    d.rectangle([px0 - 2 * u, base - 2 * u, px1 + 2 * u, base], fill=dark)
    ncol = 8
    cw = 2.6 * u
    gap = (px1 - px0 - ncol * cw) / (ncol - 1)
    for i in range(ncol):
        x = px0 + i * (cw + gap)
        d.rectangle([x, base - 22 * u, x + cw, base - 2 * u], fill=dark)
    d.rectangle([px0 - 3 * u, base - 26 * u, px1 + 3 * u, base - 22 * u], fill=dark)
    d.polygon([(px0 - 3 * u, base - 26 * u), (px1 + 3 * u, base - 26 * u),
               ((px0 + px1) / 2, base - 34 * u)], fill=dark)
    # low city blocks
    for x, h, w in [(2, 9, 8), (74, 11, 7), (84, 8, 6), (92, 12, 7)]:
        tower(d, x * u, w * u, h * u, ground, dark)


def skyline_zurich(d, ground, u, dark, mid, light):
    # Alps behind
    d.polygon([(0, ground), (14 * u, ground - 34 * u), (26 * u, ground - 14 * u),
               (38 * u, ground - 40 * u), (52 * u, ground - 12 * u), (64 * u, ground - 30 * u),
               (78 * u, ground), (0, ground)], fill=mid)
    for peak, h in [(14, 34), (38, 40), (64, 30)]:  # snow caps
        d.polygon([(peak * u, ground - h * u),
                   (peak * u - 4 * u, ground - (h - 8) * u),
                   (peak * u + 4 * u, ground - (h - 8) * u)], fill=light)
    # Grossmünster — twin towers
    for gx in (24 * u, 34 * u):
        tower(d, gx, 8 * u, 34 * u, ground, dark)
        d.polygon([(gx - 1 * u, ground - 34 * u), (gx + 9 * u, ground - 34 * u),
                   (gx + 4 * u, ground - 44 * u)], fill=dark)
        d.rectangle([gx + 2.5 * u, ground - 26 * u, gx + 5.5 * u, ground - 21 * u], fill=light)
    d.rectangle([24 * u, ground - 16 * u, 42 * u, ground], fill=dark)
    # Fraumünster — slim spire
    fx = 52 * u
    tower(d, fx, 6 * u, 30 * u, ground, dark)
    d.polygon([(fx - 0.5 * u, ground - 30 * u), (fx + 6.5 * u, ground - 30 * u),
               (fx + 3 * u, ground - 52 * u)], fill=dark)
    d.rectangle([fx + 1.5 * u, ground - 24 * u, fx + 4.5 * u, ground - 19 * u], fill=light)
    # St. Peter clock tower
    sx = 66 * u
    tower(d, sx, 7 * u, 26 * u, ground, dark)
    d.ellipse([sx + 0.6 * u, ground - 24 * u, sx + 6.4 * u, ground - 18 * u], fill=light)
    d.polygon([(sx - 0.5 * u, ground - 26 * u), (sx + 7.5 * u, ground - 26 * u),
               (sx + 3.5 * u, ground - 38 * u)], fill=dark)
    # old town roofline + lake boat
    for x, h, w in [(76, 14, 8), (85, 18, 7), (93, 12, 7)]:
        tower(d, x * u, w * u, h * u, ground, dark, roof="point")
    d.polygon([(6 * u, ground - 3 * u), (20 * u, ground - 3 * u), (17 * u, ground),
               (9 * u, ground)], fill=dark)
    d.line([(13 * u, ground - 3 * u), (13 * u, ground - 12 * u)], fill=dark, width=int(u * 0.6))
    d.polygon([(13.5 * u, ground - 12 * u), (13.5 * u, ground - 4 * u), (19 * u, ground - 4 * u)],
              fill=light)


def skyline_orlando(d, ground, u, dark, mid, light):
    # palms (left)
    for px, ph in [(6, 26), (15, 20)]:
        d.line([(px * u, ground), (px * u + 1.5 * u, ground - ph * u)],
               fill=dark, width=int(u * 1.2))
        for a in (-1.0, -0.5, 0.0, 0.5, 1.0):
            d.line([(px * u + 1.5 * u, ground - ph * u),
                    (px * u + 1.5 * u + math.sin(a) * 9 * u,
                     ground - ph * u - math.cos(a) * 5 * u + 3 * u)],
                   fill=dark, width=int(u * 0.9))
    # castle with spires (generic fairytale silhouette)
    bx = 26 * u
    d.rectangle([bx, ground - 22 * u, bx + 30 * u, ground], fill=dark)
    for sx, sh, sw in [(0, 34, 7), (11.5, 44, 7), (23, 34, 7)]:
        x = bx + sx * u
        d.rectangle([x, ground - sh * u, x + sw * u, ground], fill=dark)
        d.polygon([(x - 1.4 * u, ground - sh * u), (x + sw * u + 1.4 * u, ground - sh * u),
                   (x + sw * u / 2, ground - (sh + 13) * u)], fill=dark)
        d.line([(x + sw * u / 2, ground - (sh + 13) * u), (x + sw * u / 2, ground - (sh + 17) * u)],
               fill=dark, width=int(u * 0.5))
        d.polygon([(x + sw * u / 2, ground - (sh + 17) * u),
                   (x + sw * u / 2 + 4 * u, ground - (sh + 15.6) * u),
                   (x + sw * u / 2, ground - (sh + 14.2) * u)], fill=light)
    d.polygon([(bx + 12 * u, ground), (bx + 12 * u, ground - 12 * u),
               (bx + 18 * u, ground - 12 * u), (bx + 18 * u, ground)], fill=mid)
    # Ferris wheel (ICON-style)
    wx, wy, wr = 66 * u, ground - 33 * u, 18 * u
    d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], outline=dark, width=int(u * 1.4))
    d.ellipse([wx - wr * 0.16, wy - wr * 0.16, wx + wr * 0.16, wy + wr * 0.16], fill=dark)
    for i in range(12):
        a = math.pi * 2 * i / 12
        ex, ey = wx + math.cos(a) * wr, wy + math.sin(a) * wr
        d.line([(wx, wy), (ex, ey)], fill=dark, width=int(u * 0.5))
        d.ellipse([ex - 1.9 * u, ey - 1.9 * u, ex + 1.9 * u, ey + 1.9 * u], fill=light)
    d.line([(wx, wy), (wx - 9 * u, ground)], fill=dark, width=int(u * 1.4))
    d.line([(wx, wy), (wx + 9 * u, ground)], fill=dark, width=int(u * 1.4))
    # rocket launch (right) — Space Coast nod
    rx = 80 * u
    d.polygon([(rx, ground - 46 * u), (rx + 3 * u, ground - 56 * u), (rx + 6 * u, ground - 46 * u)],
              fill=light)
    d.rectangle([rx + 0.8 * u, ground - 47 * u, rx + 5.2 * u, ground - 32 * u], fill=light)
    d.polygon([(rx + 0.8 * u, ground - 34 * u), (rx - 1.6 * u, ground - 29 * u),
               (rx + 0.8 * u, ground - 29 * u)], fill=light)
    d.polygon([(rx + 5.2 * u, ground - 34 * u), (rx + 7.6 * u, ground - 29 * u),
               (rx + 5.2 * u, ground - 29 * u)], fill=light)
    for k in range(3):
        rr = (3.4 - k) * u
        d.ellipse([rx + 3 * u - rr, ground - 30 * u + k * 4 * u - rr,
                   rx + 3 * u + rr, ground - 30 * u + k * 4 * u + rr], fill=mid)


CITIES = [
    dict(key="oslo", name="OSLO", sub="NORWAY",
         top="#08203f", bot="#2b6f9e", dark="#071726", mid="#123a5c", light="#eaf4ff",
         glow="#7fdbff", draw=skyline_oslo),
    dict(key="new-york", name="NEW YORK", sub="USA",
         top="#241a4a", bot="#f2662a", dark="#160f28", mid="#3a2a5c", light="#fff3e0",
         glow="#ffb900", draw=skyline_newyork),
    dict(key="athens", name="ATHENS", sub="GREECE",
         top="#0d3b63", bot="#f2a63b", dark="#10263c", mid="#1d4a6e", light="#fff6e3",
         glow="#ffd166", draw=skyline_athens),
    dict(key="zurich", name="ZURICH", sub="SWITZERLAND",
         top="#0a3350", bot="#7fc0e8", dark="#0b2033", mid="#2d5f85", light="#f3fbff",
         glow="#bfe6ff", draw=skyline_zurich),
    dict(key="orlando", name="ORLANDO", sub="FLORIDA",
         top="#2a1747", bot="#ff7a4d", dark="#1a0f2e", mid="#4a2a63", light="#fff1e6",
         glow="#ffd48a", draw=skyline_orlando),
]


def arc_text(base, text, radius, font_, fill, span_deg=150, center_deg=270):
    """Draw text along the top arc of the circle, reading left to right."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    widths = [tmp.textlength(c, font=font_) for c in text]
    total = sum(widths)
    if total == 0:
        return
    start = math.radians(center_deg - span_deg / 2)
    span = math.radians(span_deg)
    acc = 0.0
    for c, w in zip(text, widths):
        frac = (acc + w / 2) / total
        acc += w
        if c == " ":
            continue
        theta = start + span * frac
        # glyph image
        bbox = font_.getbbox(c)
        gw, gh = max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])
        pad = int(max(gw, gh) * 0.6) + 4
        g = Image.new("RGBA", (gw + pad * 2, gh + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((pad - bbox[0], pad - bbox[1]), c, font=font_, fill=fill)
        g = g.rotate(-(math.degrees(theta) + 90), resample=Image.BICUBIC, expand=True)
        x = CX + math.cos(theta) * radius
        y = CY + math.sin(theta) * radius
        base.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))


def make(city):
    W = SIZE * SS
    art = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    canvas = Image.new("RGB", (W, W), rgb(city["top"]))
    d = ImageDraw.Draw(canvas)

    ground = int(W * 0.66)
    sky(d, city["top"], city["bot"], 0, ground)
    u = W / 100.0 * 0.86
    off = W * 0.07  # centre the 100u-wide skyline

    # sun / glow
    d.ellipse([W * 0.60, W * 0.30, W * 0.60 + W * 0.17, W * 0.30 + W * 0.17], fill=rgb(city["glow"]))

    # stars
    import random
    random.seed(len(city["key"]))
    for _ in range(70):
        sx, sy = random.uniform(0, W), random.uniform(0, ground * 0.55)
        r = random.uniform(1.2, 3.0) * SS
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))

    # skyline on its own layer so we can offset it
    sky_layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sky_layer)
    city["draw"](sd, ground, u, rgb(city["dark"]), rgb(city["mid"]), rgb(city["light"]))
    canvas.paste(sky_layer, (int(off), 0), sky_layer)

    # ground band
    d.rectangle([0, ground, W, W], fill=rgb(city["dark"]))

    # clip to circle
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).ellipse([CX - R_RING, CY - R_RING, CX + R_RING, CY + R_RING], fill=255)
    art.paste(canvas, (0, 0), mask)

    # white die-cut ring
    ring = ImageDraw.Draw(art)
    ring.ellipse([CX - R_OUTER, CY - R_OUTER, CX + R_OUTER, CY + R_OUTER],
                 outline=(255, 255, 255, 255), width=int(R_OUTER - R_RING))
    ring.ellipse([CX - R_RING - SS, CY - R_RING - SS, CX + R_RING + SS, CY + R_RING + SS],
                 outline=(255, 255, 255, 90), width=int(3 * SS))

    # four-square mark, top centre
    sq, gap = int(30 * SS), int(5 * SS)
    mx = CX - (sq * 2 + gap) // 2
    my = int(CY - R_RING * 0.60)
    for col, (dx, dy) in zip(MS_COLORS, [(0, 0), (sq + gap, 0), (0, sq + gap), (sq + gap, sq + gap)]):
        ring.rectangle([mx + dx, my + dy, mx + dx + sq, my + dy + sq], fill=rgb(col))

    # wordmark band
    f_word = font("segoeuib.ttf", int(74 * SS))
    f_city = font("segoeui.ttf", int(50 * SS))
    word = "MicrosoftUniversity"
    tw = ring.textlength(word, font=f_word)
    wy = int(CY + R_RING * 0.36)
    ring.text((CX - tw / 2, wy), word, font=f_word, fill=(255, 255, 255, 255))

    # city name, letterspaced under the wordmark
    name = city["name"]
    track = int(10 * SS)
    cw = sum(ring.textlength(c, font=f_city) for c in name) + track * (len(name) - 1)
    x = CX - cw / 2
    cy_ = wy + int(96 * SS)
    for c in name:
        ring.text((x, cy_), c, font=f_city, fill=rgb(city["glow"]) + (255,))
        x += ring.textlength(c, font=f_city) + track

    # country on the top arc
    arc_text(art, city["sub"], R_RING * 0.885, font("segoeui.ttf", int(34 * SS)),
             (255, 255, 255, 215), span_deg=72, center_deg=270)

    art = art.resize((SIZE, SIZE), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    p = os.path.join(OUT_DIR, "sticker-%s.png" % city["key"])
    art.save(p)
    return p


if __name__ == "__main__":
    for c in CITIES:
        print("wrote", make(c))
