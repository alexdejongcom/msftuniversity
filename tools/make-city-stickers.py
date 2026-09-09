#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the Microsoft University city stickers.

Circular die-cut stickers, each with a city skyline silhouette, the
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



def skyline_eindhoven(d, ground, u, dark, mid, light):
    """Evoluon, the Philips Lichttoren and the Strijp-S skyline."""
    # Philips Lichttoren — brick tower with the lamp on top
    lx = 6 * u
    tower(d, lx, 13 * u, 46 * u, ground, dark)
    windows(d, lx, 13 * u, 46 * u, ground, light, cols=4, rows=7)
    d.rectangle([lx + 4 * u, ground - 52 * u, lx + 9 * u, ground - 46 * u], fill=dark)
    d.ellipse([lx + 3 * u, ground - 60 * u, lx + 10 * u, ground - 51 * u], fill=light)
    # Klokgebouw / Strijp-S sheds
    d.rectangle([22 * u, ground - 16 * u, 40 * u, ground], fill=dark)
    for i in range(4):  # saw-tooth factory roof
        x = 22 * u + i * 4.5 * u
        d.polygon([(x, ground - 16 * u), (x + 4.5 * u, ground - 16 * u),
                   (x + 4.5 * u, ground - 21 * u)], fill=dark)
    d.rectangle([29 * u, ground - 26 * u, 33 * u, ground - 16 * u], fill=dark)
    d.ellipse([28.5 * u, ground - 30 * u, 33.5 * u, ground - 25 * u], fill=light)   # clock
    # Evoluon — the flying saucer
    ecx, ecy = 62 * u, ground - 30 * u
    d.polygon([(ecx - 4 * u, ground), (ecx - 2 * u, ecy + 2 * u),
               (ecx + 2 * u, ecy + 2 * u), (ecx + 4 * u, ground)], fill=dark)
    for lx2 in (-13, -6.5, 0, 6.5, 13):   # concrete legs
        d.line([(ecx + lx2 * u, ecy + 3 * u), (ecx + lx2 * u * 1.35, ground)],
               fill=dark, width=int(u * 1.3))
    d.ellipse([ecx - 24 * u, ecy - 4 * u, ecx + 24 * u, ecy + 7 * u], fill=dark)     # rim
    d.pieslice([ecx - 17 * u, ecy - 17 * u, ecx + 17 * u, ecy + 6 * u], 180, 360, fill=dark)
    d.pieslice([ecx - 17 * u, ecy - 17 * u, ecx + 17 * u, ecy + 6 * u], 180, 360,
               outline=light, width=int(u * 0.45))
    for i in range(7):   # lit windows around the rim
        wx2 = ecx - 19 * u + i * 6.3 * u
        d.ellipse([wx2 - 1.5 * u, ecy - 0.6 * u, wx2 + 1.5 * u, ecy + 2.4 * u], fill=light)
    # Admirant / high-rise blocks on the right
    for x, h, w in [(88, 30, 8), (96, 22, 6)]:
        tower(d, x * u, w * u, h * u, ground, dark)
        windows(d, x * u, w * u, h * u, ground, light, cols=3, rows=5)


def skyline_bergen(d, ground, u, dark, mid, light):
    """Bryggen's gabled wharf under the seven mountains."""
    # Floyen and Ulriken behind
    d.polygon([(0, ground), (18 * u, ground - 40 * u), (40 * u, ground - 12 * u),
               (58 * u, ground - 34 * u), (78 * u, ground - 10 * u), (100 * u, ground)],
              fill=mid)
    # funicular line up Floyen
    d.line([(18 * u, ground - 40 * u), (30 * u, ground - 18 * u)], fill=light, width=int(u * 0.4))
    d.rectangle([26 * u, ground - 25 * u, 29 * u, ground - 22 * u], fill=light)
    # Bryggen — the row of colourful gabled Hanseatic houses
    facades = ["#c94f3d", "#d9a441", "#e8e2d0", "#7a9e4f", "#b8563f",
               "#e0c060", "#efe8d8", "#6f8fa8"]
    x = 12 * u
    for i, col in enumerate(facades):
        w = 9.4 * u
        h = (24 + (i % 3) * 3) * u
        d.rectangle([x, ground - h, x + w, ground], fill=rgb(col))
        d.polygon([(x - 0.8 * u, ground - h), (x + w + 0.8 * u, ground - h),
                   (x + w / 2, ground - h - 9 * u)], fill=rgb(col))
        # dark window grid
        for r in range(3):
            top_y = ground - h + 4 * u + r * 6 * u
            bot_y = top_y + 4.5 * u
            if bot_y > ground - 9 * u:
                break
            for c2 in range(2):
                d.rectangle([x + 1.9 * u + c2 * 4.2 * u, top_y,
                             x + 4.4 * u + c2 * 4.2 * u, bot_y], fill=dark)
        d.rectangle([x + 3.4 * u, ground - 7 * u, x + 6 * u, ground], fill=dark)  # door
        x += w + 1.2 * u
    # quay + a sailing ship on the Vagen
    d.rectangle([0, ground - 3 * u, 100 * u, ground], fill=dark)
    sx = 90 * u
    d.polygon([(sx - 9 * u, ground - 3 * u), (sx + 9 * u, ground - 3 * u),
               (sx + 6 * u, ground - 8 * u), (sx - 6 * u, ground - 8 * u)], fill=dark)
    d.line([(sx, ground - 8 * u), (sx, ground - 34 * u)], fill=dark, width=int(u * 0.7))
    d.polygon([(sx + 1 * u, ground - 32 * u), (sx + 1 * u, ground - 10 * u),
               (sx + 11 * u, ground - 10 * u)], fill=light)
    d.polygon([(sx - 1 * u, ground - 28 * u), (sx - 1 * u, ground - 10 * u),
               (sx - 8 * u, ground - 10 * u)], fill=light)



def skyline_online(d, ground, u, dark, mid, light):
    """"The Internet" — a skyline of server racks under a network sky."""
    # network constellation overhead
    nodes = [(6, -44), (19, -53), (32, -41), (46, -55), (60, -43), (74, -51), (88, -40), (97, -47)]
    for (x1, y1), (x2, y2) in zip(nodes, nodes[1:]):
        d.line([(x1 * u, ground + y1 * u), (x2 * u, ground + y2 * u)],
               fill=mid, width=int(u * 0.35))
    d.line([(nodes[0][0] * u, ground + nodes[0][1] * u),
            (nodes[3][0] * u, ground + nodes[3][1] * u)], fill=mid, width=int(u * 0.28))
    d.line([(nodes[4][0] * u, ground + nodes[4][1] * u),
            (nodes[7][0] * u, ground + nodes[7][1] * u)], fill=mid, width=int(u * 0.28))
    for i, (x, y) in enumerate(nodes):
        r = 2.0 * u if i % 3 else 2.8 * u
        d.ellipse([x * u - r, ground + y * u - r, x * u + r, ground + y * u + r], fill=light)

    # the cloud
    ccx, ccy = 32 * u, ground - 36 * u
    for dx, dy, rr in [(-13, 2, 9), (-4, -3, 12), (7, -1, 10), (15, 3, 8)]:
        d.ellipse([ccx + dx * u - rr * u, ccy + dy * u - rr * u,
                   ccx + dx * u + rr * u, ccy + dy * u + rr * u], fill=light)
    d.rectangle([ccx - 21 * u, ccy + 1 * u, ccx + 22 * u, ccy + 10 * u], fill=light)
    d.ellipse([ccx - 24 * u, ccy + 1 * u, ccx - 18 * u, ccy + 11 * u], fill=light)
    d.ellipse([ccx + 19 * u, ccy + 1 * u, ccx + 25 * u, ccy + 11 * u], fill=light)
    # download / upload arrows under the cloud
    d.line([(ccx, ccy + 12 * u), (ccx, ccy + 21 * u)], fill=light, width=int(u * 1.1))
    d.polygon([(ccx - 3 * u, ccy + 19 * u), (ccx + 3 * u, ccy + 19 * u),
               (ccx, ccy + 24 * u)], fill=light)

    # server racks as the "buildings"
    racks = [(6, 30, 12), (20, 44, 12), (34, 26, 12), (48, 38, 12), (62, 48, 12)]
    for i, (x, h, w) in enumerate(racks):
        x, h, w = x * u, h * u, w * u
        d.rectangle([x, ground - h, x + w, ground], fill=dark)
        d.rectangle([x, ground - h, x + w, ground - h + 1.4 * u], fill=mid)
        slots = int(h / (4.6 * u))
        for r in range(slots):
            yy = ground - h + 3.4 * u + r * 4.6 * u
            if yy + 3 * u > ground - 1.5 * u:
                break
            d.rectangle([x + 1.6 * u, yy, x + w - 1.6 * u, yy + 3 * u], fill=mid)
            for k in range(3):   # status LEDs
                col = MS_COLORS[(i + r + k) % 4]
                lx = x + w - 5.2 * u + k * 1.5 * u
                d.ellipse([lx, yy + 0.9 * u, lx + 1.1 * u, yy + 2.0 * u], fill=rgb(col))

    # antenna mast with Wi-Fi arcs
    ax = 78 * u
    d.polygon([(ax - 5 * u, ground), (ax - 1.6 * u, ground - 38 * u),
               (ax + 1.6 * u, ground - 38 * u), (ax + 5 * u, ground)], fill=dark)
    for yy in (10, 22, 34):
        d.line([(ax - 4.2 * u + yy * 0.06 * u, ground - yy * u),
                (ax + 4.2 * u - yy * 0.06 * u, ground - yy * u)], fill=dark, width=int(u * 0.5))
    for k, rr in enumerate((6, 10, 14)):
        d.arc([ax - rr * u, ground - 38 * u - rr * u, ax + rr * u, ground - 38 * u + rr * u],
              205, 335, fill=light, width=int(u * 0.9))
    d.ellipse([ax - 1.8 * u, ground - 40 * u, ax + 1.8 * u, ground - 36.4 * u], fill=light)

    # satellite dish, far right
    sx, sy = 95 * u, ground - 12 * u
    d.polygon([(sx - 2 * u, ground), (sx + 2 * u, ground), (sx + 1 * u, sy), (sx - 1 * u, sy)],
              fill=dark)
    d.pieslice([sx - 9 * u, sy - 12 * u, sx + 7 * u, sy + 4 * u], 200, 20, fill=mid)
    d.line([(sx - 1 * u, sy - 4 * u), (sx + 3 * u, sy - 10 * u)], fill=dark, width=int(u * 0.5))



def fir(d, x, base, h, u, col):
    """A Douglas fir: trunk plus three stacked tiers."""
    d.rectangle([x - 0.9 * u, base - h * 0.16, x + 0.9 * u, base], fill=col)
    for i, (wf, yf, hf) in enumerate([(1.0, 0.14, 0.40), (0.78, 0.42, 0.36), (0.55, 0.68, 0.32)]):
        w = h * 0.34 * wf
        top = base - h * (yf + hf)
        bot = base - h * yf
        d.polygon([(x - w, bot), (x + w, bot), (x, top)], fill=col)


def skyline_redmond(d, ground, u, dark, mid, light):
    """The Microsoft campus in the evergreens, with Rainier on the horizon."""
    # Mount Rainier — broad shoulders, rounded summit
    d.polygon([(38 * u, ground), (56 * u, ground - 30 * u), (66 * u, ground - 48 * u),
               (72 * u, ground - 52 * u), (79 * u, ground - 46 * u), (90 * u, ground - 26 * u),
               (106 * u, ground)], fill=mid)
    d.polygon([(66 * u, ground - 48 * u), (72 * u, ground - 52 * u), (79 * u, ground - 46 * u),
               (76 * u, ground - 41 * u), (73 * u, ground - 44 * u), (70 * u, ground - 40 * u),
               (67 * u, ground - 43 * u)], fill=light)
    # foothills
    d.polygon([(0, ground), (14 * u, ground - 20 * u), (34 * u, ground - 7 * u),
               (48 * u, ground - 15 * u), (60 * u, ground)], fill=mid)

    # evergreens get their own colour so they read against the buildings
    fir_far = rgb("#2f6b63")
    fir_near = rgb("#123f38")

    # a treeline in the middle distance
    for x in range(0, 104, 5):
        fir(d, x * u, ground - 1 * u, 14 * u, u, fir_far)

    # campus buildings — low and wide, glass grids
    for x, w, h in [(9, 18, 17), (31, 14, 23), (48, 18, 15), (73, 11, 25)]:
        tower(d, x * u, w * u, h * u, ground, dark)
        windows(d, x * u, w * u, h * u, ground, light, cols=4, rows=5)
    # angled glass atrium linking the middle blocks
    d.polygon([(45 * u, ground), (46.5 * u, ground - 19 * u), (51 * u, ground - 19 * u),
               (51 * u, ground)], fill=dark)
    d.rectangle([47.6 * u, ground - 17 * u, 50 * u, ground - 7 * u], fill=light)

    # the campus sign out front, clear of everything
    sx = 62 * u
    d.rectangle([sx + 3.4 * u, ground - 4 * u, sx + 5 * u, ground], fill=dark)
    d.rectangle([sx, ground - 14 * u, sx + 8.4 * u, ground - 4 * u], fill=dark)
    q, g = 2.4 * u, 0.5 * u
    ox, oy = sx + (8.4 * u - (2 * q + g)) / 2, ground - 13 * u
    for col, (dx, dy) in zip(MS_COLORS, [(0, 0), (q + g, 0), (0, q + g), (q + g, q + g)]):
        d.rectangle([ox + dx, oy + dy, ox + dx + q, oy + dy + q], fill=rgb(col))

    # big evergreens framing the badge, in front of the campus
    for x, h in [(1, 34), (5.5, 26), (27, 21), (44, 18), (58, 23), (86, 36), (93, 27), (99, 31)]:
        fir(d, x * u, ground, h * u, u, fir_near)



def skyline_johannesburg(d, ground, u, dark, mid, light):
    """Hillbrow Tower, Ponte City, the Carlton Centre and the Mandela Bridge."""
    # gold-mine dumps rolling behind the city
    d.polygon([(0, ground), (10 * u, ground - 15 * u), (24 * u, ground - 11 * u),
               (36 * u, ground - 18 * u), (52 * u, ground - 9 * u), (64 * u, ground)], fill=mid)
    d.polygon([(58 * u, ground), (72 * u, ground - 13 * u), (88 * u, ground - 8 * u),
               (100 * u, ground - 14 * u), (104 * u, ground)], fill=mid)

    # acacia on the left — flat-topped highveld tree
    ax = 8 * u
    d.rectangle([ax - 1.1 * u, ground - 17 * u, ax + 1.1 * u, ground], fill=dark)
    d.line([(ax, ground - 15 * u), (ax - 6 * u, ground - 21 * u)], fill=dark, width=int(u * 0.8))
    d.line([(ax, ground - 15 * u), (ax + 6 * u, ground - 20 * u)], fill=dark, width=int(u * 0.8))
    d.ellipse([ax - 12 * u, ground - 27 * u, ax + 12 * u, ground - 19 * u], fill=dark)
    d.ellipse([ax - 7 * u, ground - 30 * u, ax + 8 * u, ground - 23 * u], fill=dark)

    # Carlton Centre — the big slab
    tower(d, 24 * u, 13 * u, 44 * u, ground, dark)
    windows(d, 24 * u, 13 * u, 44 * u, ground, light, cols=4, rows=7)

    # Ponte City — the cylinder with its rounded crown
    px = 40 * u
    tower(d, px, 11 * u, 38 * u, ground, dark, roof="dome")
    windows(d, px, 11 * u, 38 * u, ground, light, cols=3, rows=6)
    d.rectangle([px + 3 * u, ground - 46 * u, px + 8 * u, ground - 42 * u], fill=mid)

    # Hillbrow Tower — slim shaft, observation collar, mast
    hx = 58 * u
    d.polygon([(hx - 3.6 * u, ground), (hx - 2.0 * u, ground - 44 * u),
               (hx + 2.0 * u, ground - 44 * u), (hx + 3.6 * u, ground)], fill=dark)
    d.rectangle([hx - 6.5 * u, ground - 52 * u, hx + 6.5 * u, ground - 44 * u], fill=dark)
    d.ellipse([hx - 6.5 * u, ground - 55 * u, hx + 6.5 * u, ground - 49 * u], fill=dark)
    for k in range(4):
        wx2 = hx - 4.6 * u + k * 3.0 * u
        d.rectangle([wx2, ground - 50 * u, wx2 + 1.8 * u, ground - 47 * u], fill=light)
    d.rectangle([hx - 1.1 * u, ground - 66 * u, hx + 1.1 * u, ground - 52 * u], fill=dark)
    d.ellipse([hx - 2.2 * u, ground - 69 * u, hx + 2.2 * u, ground - 64.6 * u], fill=light)

    # a couple of Sandton blocks
    for x, h, w in [(68, 26, 8), (78, 20, 7)]:
        tower(d, x * u, w * u, h * u, ground, dark)
        windows(d, x * u, w * u, h * u, ground, light, cols=3, rows=4)

    # Nelson Mandela Bridge, cable-stayed, on the right
    deck = ground - 7 * u
    d.rectangle([70 * u, deck, 104 * u, deck + 2.2 * u], fill=dark)
    for pxx, ph in [(80, 30), (96, 26)]:
        top = ground - ph * u
        d.polygon([(pxx * u - 2.4 * u, deck), (pxx * u - 0.7 * u, top),
                   (pxx * u + 0.7 * u, top), (pxx * u + 2.4 * u, deck)], fill=dark)
        for k in range(4):
            off = (k + 1) * 4.2 * u
            d.line([(pxx * u, top + 1.5 * u), (pxx * u - off, deck)], fill=dark, width=int(u * 0.32))
            d.line([(pxx * u, top + 1.5 * u), (pxx * u + off, deck)], fill=dark, width=int(u * 0.32))



def gable(d, x, w, base, h, col, kind):
    """A canal-house facade with a Dutch/Nordic gable on top."""
    d.rectangle([x, base - h, x + w, base], fill=col)
    t = base - h
    if kind == "step":
        steps = 4
        sw = w / (steps * 2 + 1)
        for i in range(steps):
            d.rectangle([x + sw * i, t - (i + 1) * 2.2 * u_(), x + w - sw * i, t], fill=col)
            t2 = t
    elif kind == "bell":
        d.pieslice([x - 0.4 * (w * 0.5), t - w * 0.55, x + w + 0.4 * (w * 0.5), t + w * 0.55],
                   180, 360, fill=col)
    elif kind == "neck":
        d.rectangle([x + w * 0.28, t - w * 0.5, x + w * 0.72, t], fill=col)
        d.pieslice([x + w * 0.28, t - w * 0.72, x + w * 0.72, t - w * 0.28], 180, 360, fill=col)
    else:  # point
        d.polygon([(x - w * 0.06, t), (x + w * 1.06, t), (x + w * 0.5, t - w * 0.62)], fill=col)


_U = [1.0]


def u_():
    return _U[0]


def skyline_amsterdam(d, ground, u, dark, mid, light):
    """Canal houses, the Westerkerk and a bridge over the gracht."""
    _U[0] = u
    # canal-house row with assorted gables
    specs = [(4, 9, 30, "step"), (14, 8, 26, "bell"), (23, 9, 33, "neck"), (33, 8, 27, "step"),
             (42, 9, 31, "point"), (52, 8, 25, "bell")]
    for x, w, h, kind in specs:
        gable(d, x * u, w * u, ground - 6 * u, h * u, dark, kind)
        windows(d, x * u, w * u, h * u, ground - 6 * u, light, cols=2, rows=4)

    # Westerkerk — tiered tower with its crown
    wx = 66 * u
    d.rectangle([wx, ground - 44 * u, wx + 11 * u, ground - 6 * u], fill=dark)
    d.rectangle([wx + 1.4 * u, ground - 52 * u, wx + 9.6 * u, ground - 44 * u], fill=dark)
    d.polygon([(wx + 0.4 * u, ground - 52 * u), (wx + 10.6 * u, ground - 52 * u),
               (wx + 5.5 * u, ground - 58 * u)], fill=dark)
    d.rectangle([wx + 3.4 * u, ground - 64 * u, wx + 7.6 * u, ground - 58 * u], fill=dark)
    d.polygon([(wx + 2.4 * u, ground - 64 * u), (wx + 8.6 * u, ground - 64 * u),
               (wx + 5.5 * u, ground - 70 * u)], fill=dark)
    d.ellipse([wx + 3.6 * u, ground - 75 * u, wx + 7.4 * u, ground - 70 * u], fill=light)  # crown
    d.ellipse([wx + 2.8 * u, ground - 36 * u, wx + 8.2 * u, ground - 30 * u], fill=light)  # clock

    # a few more houses right of the church
    for x, w, h, kind in [(80, 9, 28, "step"), (90, 8, 24, "bell")]:
        gable(d, x * u, w * u, ground - 6 * u, h * u, dark, kind)
        windows(d, x * u, w * u, h * u, ground - 6 * u, light, cols=2, rows=4)

    # the canal and its bridge
    d.rectangle([0, ground - 8 * u, 104 * u, ground], fill=lerp(mid, dark, 0.55))
    for bx2 in (14, 32, 50):
        d.pieslice([bx2 * u, ground - 13 * u, (bx2 + 14) * u, ground - 3 * u], 180, 360, fill=dark)
    d.rectangle([10 * u, ground - 14 * u, 68 * u, ground - 11 * u], fill=dark)

    # a bicycle leaning on the bridge rail
    bx, by, r = 76 * u, ground - 3 * u, 3.4 * u
    for cx2 in (bx, bx + 8 * u):
        d.ellipse([cx2 - r, by - r, cx2 + r, by + r], outline=dark, width=int(u * 0.55))
    d.line([(bx, by), (bx + 4 * u, by - 5 * u), (bx + 8 * u, by)], fill=dark, width=int(u * 0.5))
    d.line([(bx + 4 * u, by - 5 * u), (bx + 2.5 * u, by - 7 * u)], fill=dark, width=int(u * 0.5))


def skyline_berlin(d, ground, u, dark, mid, light):
    """Brandenburger Tor, the Dom and the Fernsehturm."""
    # Brandenburg Gate
    gx, gw = 6 * u, 30 * u
    d.rectangle([gx, ground - 22 * u, gx + gw, ground], fill=dark)
    for i in range(5):
        cx2 = gx + 2.5 * u + i * 6.4 * u
        d.rectangle([cx2, ground - 20 * u, cx2 + 3.2 * u, ground], fill=lerp(dark, mid, 0.55))
    d.rectangle([gx - 1.5 * u, ground - 28 * u, gx + gw + 1.5 * u, ground - 22 * u], fill=dark)
    # quadriga on top
    qx = gx + gw / 2
    d.rectangle([qx - 6 * u, ground - 31 * u, qx + 6 * u, ground - 28 * u], fill=dark)
    for k in range(4):
        d.rectangle([qx - 5 * u + k * 2.6 * u, ground - 35 * u,
                     qx - 3.6 * u + k * 2.6 * u, ground - 31 * u], fill=dark)
    d.polygon([(qx - 6 * u, ground - 35 * u), (qx - 1 * u, ground - 35 * u),
               (qx - 3 * u, ground - 39 * u)], fill=dark)

    # Berliner Dom
    dx = 40 * u
    d.rectangle([dx, ground - 20 * u, dx + 18 * u, ground], fill=dark)
    d.pieslice([dx + 3 * u, ground - 34 * u, dx + 15 * u, ground - 16 * u], 180, 360, fill=dark)
    d.rectangle([dx + 8 * u, ground - 38 * u, dx + 10 * u, ground - 32 * u], fill=dark)
    d.ellipse([dx + 7.4 * u, ground - 41 * u, dx + 10.6 * u, ground - 37.5 * u], fill=light)
    for k in (0, 1):
        cx2 = dx + 1 * u + k * 14 * u
        d.rectangle([cx2, ground - 26 * u, cx2 + 3 * u, ground - 16 * u], fill=dark)
        d.pieslice([cx2, ground - 30 * u, cx2 + 3 * u, ground - 24 * u], 180, 360, fill=dark)

    # Fernsehturm — shaft, sphere, antenna
    fx = 70 * u
    d.polygon([(fx - 3.4 * u, ground), (fx - 1.4 * u, ground - 44 * u),
               (fx + 1.4 * u, ground - 44 * u), (fx + 3.4 * u, ground)], fill=dark)
    d.ellipse([fx - 9 * u, ground - 55 * u, fx + 9 * u, ground - 37 * u], fill=dark)
    d.arc([fx - 9 * u, ground - 55 * u, fx + 9 * u, ground - 37 * u], 200, 340,
          fill=light, width=int(u * 1.0))
    d.rectangle([fx - 1 * u, ground - 72 * u, fx + 1 * u, ground - 53 * u], fill=dark)
    d.polygon([(fx - 1 * u, ground - 72 * u), (fx + 1 * u, ground - 72 * u),
               (fx, ground - 80 * u)], fill=dark)

    for x, h, w in [(84, 24, 8), (93, 18, 7)]:
        tower(d, x * u, w * u, h * u, ground, dark)
        windows(d, x * u, w * u, h * u, ground, light, cols=3, rows=4)


def skyline_brussels(d, ground, u, dark, mid, light):
    """The Atomium and the Grand-Place spire."""
    # Grand-Place: Town Hall spire and guild gables
    tx = 12 * u
    d.rectangle([tx, ground - 26 * u, tx + 14 * u, ground], fill=dark)
    d.rectangle([tx + 4.5 * u, ground - 44 * u, tx + 9.5 * u, ground - 26 * u], fill=dark)
    d.polygon([(tx + 3 * u, ground - 44 * u), (tx + 11 * u, ground - 44 * u),
               (tx + 7 * u, ground - 62 * u)], fill=dark)
    d.ellipse([tx + 5.6 * u, ground - 65 * u, tx + 8.4 * u, ground - 61.5 * u], fill=light)
    d.ellipse([tx + 5 * u, ground - 38 * u, tx + 9 * u, ground - 34 * u], fill=light)
    for x, w, h in [(1, 8, 20), (28, 8, 23), (37, 7, 19)]:
        gable(d, x * u, w * u, ground, h * u, dark, "step")
        windows(d, x * u, w * u, h * u, ground, light, cols=2, rows=3)

    # Atomium — nine spheres on their rods
    acx, acy, R = 70 * u, ground - 38 * u, 20 * u
    r = 5.4 * u
    pts = [(0, 0)]
    for k in range(8):
        a = math.pi * 2 * k / 8 - math.pi / 2
        pts.append((math.cos(a) * R, math.sin(a) * R))
    for i in range(1, 9):
        d.line([(acx, acy), (acx + pts[i][0], acy + pts[i][1])], fill=mid, width=int(u * 0.8))
    for i in range(1, 9):
        j = i + 1 if i < 8 else 1
        d.line([(acx + pts[i][0], acy + pts[i][1]), (acx + pts[j][0], acy + pts[j][1])],
               fill=mid, width=int(u * 0.5))
    for px, py in pts:
        d.ellipse([acx + px - r, acy + py - r, acx + px + r, acy + py + r], fill=light)
        d.ellipse([acx + px - r * 0.45, acy + py - r * 0.7,
                   acx + px + r * 0.1, acy + py - r * 0.15], fill=lerp(light, mid, 0.35))
    # legs to the ground
    for lx in (-1, 1):
        d.line([(acx + lx * R * 0.7, acy + R * 0.7), (acx + lx * R * 1.05, ground)],
               fill=mid, width=int(u * 1.1))
    d.line([(acx, acy + R), (acx, ground)], fill=mid, width=int(u * 1.2))


def skyline_copenhagen(d, ground, u, dark, mid, light):
    """Nyhavn, Borsen's twisted spire, the Round Tower and Frederik's dome."""
    # Nyhavn facades
    facades = ["#d24b3e", "#e8b64c", "#f2ece0", "#4f7fa8", "#c9603f"]
    x = 2 * u
    for i, col in enumerate(facades):
        w, h = 8.6 * u, (22 + (i % 3) * 3) * u
        d.rectangle([x, ground - h, x + w, ground], fill=rgb(col))
        d.polygon([(x - 0.6 * u, ground - h), (x + w + 0.6 * u, ground - h),
                   (x + w / 2, ground - h - 5 * u)], fill=rgb(col))
        for r in range(3):
            ty = ground - h + 3.5 * u + r * 5.5 * u
            if ty + 3.4 * u > ground - 6 * u:
                break
            for c2 in range(2):
                d.rectangle([x + 1.6 * u + c2 * 3.8 * u, ty,
                             x + 3.8 * u + c2 * 3.8 * u, ty + 3.4 * u], fill=dark)
        x += w + 1 * u

    # Rundetaarn — the round tower
    rx = 50 * u
    d.rectangle([rx, ground - 30 * u, rx + 11 * u, ground], fill=dark)
    d.pieslice([rx, ground - 36 * u, rx + 11 * u, ground - 24 * u], 180, 360, fill=dark)
    d.rectangle([rx + 4.4 * u, ground - 40 * u, rx + 6.6 * u, ground - 34 * u], fill=dark)
    d.rectangle([rx + 2.5 * u, ground - 22 * u, rx + 8.5 * u, ground - 17 * u], fill=light)

    # Borsen — the twisted dragon-tail spire
    bx = 66 * u
    d.rectangle([bx, ground - 18 * u, bx + 16 * u, ground], fill=dark)
    d.polygon([(bx + 4 * u, ground - 18 * u), (bx + 12 * u, ground - 18 * u),
               (bx + 8 * u, ground - 26 * u)], fill=dark)
    cxs = bx + 8 * u
    d.polygon([(cxs - 5 * u, ground - 26 * u), (cxs + 5 * u, ground - 26 * u),
               (cxs + 1.1 * u, ground - 58 * u), (cxs - 1.1 * u, ground - 58 * u)], fill=dark)
    for k in range(6):   # the twist, read as alternating barbs
        yy = ground - 29 * u - k * 5 * u
        wdt = (4.3 - k * 0.62) * u
        sgn = 1 if k % 2 else -1
        d.polygon([(cxs, yy), (cxs + sgn * (wdt + 2.4 * u), yy - 1.6 * u),
                   (cxs, yy - 3.6 * u)], fill=dark)
    d.line([(cxs, ground - 58 * u), (cxs, ground - 65 * u)], fill=dark, width=int(u * 0.55))
    d.ellipse([cxs - 1.6 * u, ground - 68 * u, cxs + 1.6 * u, ground - 64.8 * u], fill=light)

    # Frederik's Church dome
    fx = 88 * u
    d.rectangle([fx, ground - 18 * u, fx + 16 * u, ground], fill=dark)
    d.pieslice([fx + 1 * u, ground - 34 * u, fx + 15 * u, ground - 12 * u], 180, 360, fill=dark)
    d.arc([fx + 1 * u, ground - 34 * u, fx + 15 * u, ground - 12 * u], 200, 340,
          fill=light, width=int(u * 0.7))
    d.rectangle([fx + 7 * u, ground - 38 * u, fx + 9 * u, ground - 32 * u], fill=dark)


def skyline_stockholm(d, ground, u, dark, mid, light):
    """Stadshuset, Riddarholmen's lattice spire and the Gamla Stan waterfront."""
    # Gamla Stan waterfront row
    for i in range(7):
        x = (2 + i * 7.4) * u
        h = (18 + (i % 3) * 4) * u
        d.rectangle([x, ground - h - 6 * u, x + 6.6 * u, ground - 6 * u], fill=dark)
        d.polygon([(x - 0.5 * u, ground - h - 6 * u), (x + 7.1 * u, ground - h - 6 * u),
                   (x + 3.3 * u, ground - h - 10 * u)], fill=dark)
        windows(d, x, 6.6 * u, h, ground - 6 * u, light, cols=2, rows=3)

    # Riddarholmen church — openwork iron spire
    rx = 40 * u
    d.rectangle([rx, ground - 26 * u, rx + 9 * u, ground - 6 * u], fill=dark)
    cxr = rx + 4.5 * u
    d.polygon([(cxr - 5.6 * u, ground - 26 * u), (cxr + 5.6 * u, ground - 26 * u),
               (cxr, ground - 58 * u)], fill=dark)
    for k, off in enumerate((-4.4, 4.4)):   # corner turrets
        d.polygon([(cxr + off * u - 1.4 * u, ground - 26 * u),
                   (cxr + off * u + 1.4 * u, ground - 26 * u),
                   (cxr + off * u, ground - 35 * u)], fill=dark)
    d.line([(cxr, ground - 58 * u), (cxr, ground - 64 * u)], fill=dark, width=int(u * 0.5))
    d.ellipse([cxr - 1.5 * u, ground - 67 * u, cxr + 1.5 * u, ground - 64 * u], fill=light)

    # Stadshuset — the City Hall tower with its lantern and three crowns
    sx = 62 * u
    d.rectangle([sx, ground - 16 * u, sx + 34 * u, ground - 6 * u], fill=dark)
    d.rectangle([sx + 18 * u, ground - 52 * u, sx + 31 * u, ground - 6 * u], fill=dark)
    windows(d, sx + 18 * u, 13 * u, 46 * u, ground - 6 * u, light, cols=3, rows=6)
    d.rectangle([sx + 17 * u, ground - 56 * u, sx + 32 * u, ground - 52 * u], fill=dark)
    for k in range(4):   # corner pinnacles
        px = sx + 17.5 * u + k * 4.6 * u
        d.polygon([(px, ground - 56 * u), (px + 2.4 * u, ground - 56 * u),
                   (px + 1.2 * u, ground - 61 * u)], fill=dark)
    d.rectangle([sx + 22 * u, ground - 64 * u, sx + 27 * u, ground - 56 * u], fill=dark)
    d.polygon([(sx + 21 * u, ground - 64 * u), (sx + 28 * u, ground - 64 * u),
               (sx + 24.5 * u, ground - 70 * u)], fill=dark)
    for off in (-3.4, 0, 3.4):   # the three crowns
        d.ellipse([sx + 24.5 * u + off * u - 1.7 * u, ground - 76 * u,
                   sx + 24.5 * u + off * u + 1.7 * u, ground - 72.4 * u], fill=rgb("#ffb900"))

    # water and a little steamer
    d.rectangle([0, ground - 6 * u, 104 * u, ground], fill=lerp(mid, dark, 0.45))
    d.polygon([(6 * u, ground - 5 * u), (22 * u, ground - 5 * u), (19 * u, ground - 1 * u),
               (9 * u, ground - 1 * u)], fill=dark)
    d.rectangle([12 * u, ground - 10 * u, 16 * u, ground - 5 * u], fill=dark)
    d.rectangle([17 * u, ground - 12 * u, 18.6 * u, ground - 5 * u], fill=dark)


def skyline_london(d, ground, u, dark, mid, light):
    """The Eye, Big Ben, St Paul's, the Gherkin and the Shard."""
    # The London Eye, low and left where the badge is widest
    ex, ey, er = 17 * u, ground - 25 * u, 15 * u
    d.ellipse([ex - er, ey - er, ex + er, ey + er], outline=dark, width=int(u * 1.2))
    for k in range(16):
        a = math.pi * 2 * k / 16
        px, py = ex + math.cos(a) * er, ey + math.sin(a) * er
        d.line([(ex, ey), (px, py)], fill=dark, width=int(u * 0.3))
        d.ellipse([px - 1.4 * u, py - 1.4 * u, px + 1.4 * u, py + 1.4 * u], fill=light)
    d.ellipse([ex - 2.2 * u, ey - 2.2 * u, ex + 2.2 * u, ey + 2.2 * u], fill=dark)
    d.line([(ex, ey), (ex - 6 * u, ground)], fill=dark, width=int(u * 1.3))
    d.line([(ex, ey), (ex + 3 * u, ground)], fill=dark, width=int(u * 1.3))

    # Elizabeth Tower (Big Ben), brought in towards the middle
    bx = 36 * u
    d.rectangle([bx, ground - 44 * u, bx + 9 * u, ground], fill=dark)
    windows(d, bx, 9 * u, 28 * u, ground, light, cols=2, rows=4)
    d.rectangle([bx - 1 * u, ground - 50 * u, bx + 10 * u, ground - 44 * u], fill=dark)
    d.ellipse([bx + 1.4 * u, ground - 49 * u, bx + 7.6 * u, ground - 45 * u], fill=light)
    d.polygon([(bx - 1 * u, ground - 50 * u), (bx + 10 * u, ground - 50 * u),
               (bx + 4.5 * u, ground - 60 * u)], fill=dark)
    d.line([(bx + 4.5 * u, ground - 60 * u), (bx + 4.5 * u, ground - 64 * u)],
           fill=dark, width=int(u * 0.5))

    # The Shard, tallest, so keep it near the centre
    hx = 52 * u
    d.polygon([(hx, ground), (hx + 13 * u, ground), (hx + 8.6 * u, ground - 58 * u),
               (hx + 6.8 * u, ground - 68 * u), (hx + 5.4 * u, ground - 58 * u)], fill=dark)
    for k in range(5):
        yy = ground - 10 * u - k * 10 * u
        d.line([(hx + 1.6 * u + k * 0.8 * u, yy), (hx + 11.4 * u - k * 0.9 * u, yy)],
               fill=light, width=int(u * 0.28))

    # St Paul's
    sx = 68 * u
    d.rectangle([sx, ground - 15 * u, sx + 16 * u, ground], fill=dark)
    d.pieslice([sx + 2 * u, ground - 30 * u, sx + 14 * u, ground - 11 * u], 180, 360, fill=dark)
    d.rectangle([sx + 7.1 * u, ground - 35 * u, sx + 8.9 * u, ground - 28 * u], fill=dark)
    d.ellipse([sx + 6.3 * u, ground - 38 * u, sx + 9.7 * u, ground - 34 * u], fill=light)

    # The Gherkin
    gx = 88 * u
    d.polygon([(gx, ground), (gx, ground - 22 * u), (gx + 2 * u, ground - 31 * u),
               (gx + 5 * u, ground - 35 * u), (gx + 8 * u, ground - 31 * u),
               (gx + 10 * u, ground - 22 * u), (gx + 10 * u, ground)], fill=dark)
    for k in range(4):
        yy = ground - 8 * u - k * 6 * u
        d.line([(gx + 0.6 * u, yy), (gx + 9.4 * u, yy - 3 * u)], fill=light, width=int(u * 0.35))

CITIES = [
    dict(key="amsterdam", name="AMSTERDAM", sub="NETHERLANDS",
         top="#122845", bot="#e8a052", dark="#0d1b2e", mid="#2a4a70", light="#fff3df",
         glow="#ffd08a", draw=skyline_amsterdam),
    dict(key="athens", name="ATHENS", sub="GREECE",
         top="#0d3b63", bot="#f2a63b", dark="#10263c", mid="#1d4a6e", light="#fff6e3",
         glow="#ffd166", draw=skyline_athens),
    dict(key="bergen", name="BERGEN", sub="NORWAY",
         top="#0b2c40", bot="#7fb6cd", dark="#0a1f2e", mid="#265a75", light="#f2fbff",
         glow="#cfeaf7", draw=skyline_bergen),
    dict(key="berlin", name="BERLIN", sub="GERMANY",
         top="#132436", bot="#d8904a", dark="#0e1a28", mid="#2d4a63", light="#fff4e4",
         glow="#ffc98a", draw=skyline_berlin),
    dict(key="brussels", name="BRUSSELS", sub="BELGIUM",
         top="#0e1c33", bot="#dcae5e", dark="#0a1526", mid="#3a5a80", light="#fff6e6",
         glow="#ffd98f", draw=skyline_brussels),
    dict(key="copenhagen", name="COPENHAGEN", sub="DENMARK",
         top="#1b2c4e", bot="#efa088", dark="#12203a", mid="#3d5b85", light="#fff2ea",
         glow="#ffd0bb", draw=skyline_copenhagen),
    dict(key="eindhoven", name="EINDHOVEN", sub="NETHERLANDS",
         top="#101c3d", bot="#e8843c", dark="#0d1526", mid="#26365e", light="#fff4dc",
         glow="#ffc46b", draw=skyline_eindhoven),
    dict(key="johannesburg", name="JOHANNESBURG", sub="SOUTH AFRICA",
         top="#251239", bot="#ef8f3c", dark="#170c23", mid="#4d2c50", light="#fff3e2",
         glow="#ffc978", draw=skyline_johannesburg),
    dict(key="london", name="LONDON", sub="UNITED KINGDOM",
         top="#101d33", bot="#c98a62", dark="#0b1424", mid="#2f4a6b", light="#fff1e2",
         glow="#ffc48f", draw=skyline_london),
    dict(key="new-york", name="NEW YORK", sub="USA",
         top="#241a4a", bot="#f2662a", dark="#160f28", mid="#3a2a5c", light="#fff3e0",
         glow="#ffb900", draw=skyline_newyork),
    dict(key="online", name="ONLINE", sub="THE INTERNET",
         top="#04142b", bot="#0a6fb8", dark="#071a2c", mid="#1f6ea8", light="#eaf7ff",
         glow="#7fdbff", draw=skyline_online),
    dict(key="orlando", name="ORLANDO", sub="FLORIDA",
         top="#2a1747", bot="#ff7a4d", dark="#1a0f2e", mid="#4a2a63", light="#fff1e6",
         glow="#ffd48a", draw=skyline_orlando),
    dict(key="oslo", name="OSLO", sub="NORWAY",
         top="#08203f", bot="#2b6f9e", dark="#071726", mid="#123a5c", light="#eaf4ff",
         glow="#7fdbff", draw=skyline_oslo),
    dict(key="redmond", name="REDMOND", sub="WASHINGTON",
         top="#12314a", bot="#9ec9d8", dark="#0e2233", mid="#2f6b86", light="#f4fbff",
         glow="#d9eef7", draw=skyline_redmond),
    dict(key="stockholm", name="STOCKHOLM", sub="SWEDEN",
         top="#0d2440", bot="#7aa8cd", dark="#0a1a2e", mid="#2c5479", light="#f2f9ff",
         glow="#cfe6f7", draw=skyline_stockholm),
    dict(key="zurich", name="ZURICH", sub="SWITZERLAND",
         top="#0a3350", bot="#7fc0e8", dark="#0b2033", mid="#2d5f85", light="#f3fbff",
         glow="#bfe6ff", draw=skyline_zurich),
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
        ImageDraw.Draw(g).text((pad - bbox[0], pad - bbox[1]), c, font=font_, fill=fill,
                              stroke_width=max(1, int(font_.size * 0.10)),
                              stroke_fill=(0, 0, 0, 120))
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
    span = min(120, max(72, 8.5 * len(city["sub"])))
    arc_text(art, city["sub"], R_RING * 0.885, font("segoeui.ttf", int(34 * SS)),
             (255, 255, 255, 215), span_deg=span, center_deg=270)

    art = art.resize((SIZE, SIZE), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    p = os.path.join(OUT_DIR, "sticker-%s.png" % city["key"])
    art.save(p)
    return p


if __name__ == "__main__":
    for c in CITIES:
        print("wrote", make(c))
