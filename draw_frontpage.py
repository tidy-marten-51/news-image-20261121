"""Drawing helpers for the 21 November 2026 front page.

All artwork is original flat vector-style art drawn with PIL shapes:
a skyline under attack, a Danish flag scene, three summit flags,
a courtroom, a hospital cross, a globe and a protest crowd.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (26, 26, 22)
RED = (176, 32, 32)
DARKRED = (128, 20, 20)
BLUE = (30, 58, 95)
NAVY = (22, 30, 46)
GREY = (112, 110, 100)
LINE = (70, 66, 58)
LIGHT = (233, 227, 210)
GOLD = (214, 164, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, weight=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=weight)


def double_rule(d, x0, x1, y, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=3)
    d.line([(x0, y + 5), (x1, y + 5)], fill=fill, width=1)


def starburst(d, cx, cy, r, spikes=12, colour=(255, 140, 26)):
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)
    d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
              fill=(255, 210, 63))


def draw_lead_illustration(img, x, y, w, h):
    """City skyline at dusk under attack: gradient sky, silhouettes,
    explosions, smoke and a hit bridge."""
    d = ImageDraw.Draw(img)
    top = (24, 34, 66)
    mid = (120, 62, 66)
    bot = (224, 122, 58)
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.55:
            u = t / 0.55
            c = tuple(int(top[k] + (mid[k] - top[k]) * u) for k in range(3))
        else:
            u = (t - 0.55) / 0.45
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * u) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    # stars in the upper sky
    rng = random.Random(11)
    for _ in range(26):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.3))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(235, 235, 220))
    # far skyline
    rng = random.Random(21)
    bx = x
    horizon = y + h - 46
    while bx < x + w - 30:
        bw = rng.randint(28, 58)
        bh = rng.randint(38, 92)
        d.rectangle([bx, horizon - bh, bx + bw, horizon + 6],
                    fill=(52, 48, 66))
        bx += bw + rng.randint(2, 10)
    # near buildings with lit windows
    rng = random.Random(31)
    bx = x + 6
    while bx < x + w - 40:
        bw = rng.randint(44, 78)
        bh = rng.randint(70, 150)
        base = y + h
        d.rectangle([bx, base - bh, bx + bw, base], fill=(28, 26, 34))
        for _ in range(int(bw * bh / 260)):
            wx = bx + rng.randint(5, bw - 9)
            wy = base - bh + rng.randint(6, bh - 12)
            d.rectangle([wx, wy, wx + 4, wy + 6],
                        fill=(255, 196, 66) if rng.random() < 0.7
                        else (150, 170, 200))
        bx += bw + rng.randint(4, 14)
    # bridge on the right, hit and burning
    bx0, bx1 = x + w - 190, x + w - 8
    by = y + h - 18
    d.arc([bx0, by - 74, bx1, by + 10], start=180, end=360,
          fill=(18, 18, 24), width=7)
    d.line([(bx0, by), (bx1, by)], fill=(18, 18, 24), width=6)
    for k in range(6):
        cx = bx0 + 14 + k * 30
        d.line([(cx, by - 26), (cx, by)], fill=(18, 18, 24), width=3)
    # explosions
    starburst(d, x + 120, y + 62, 30, colour=(255, 140, 26))
    starburst(d, x + 300, y + 44, 22, colour=(255, 110, 30))
    starburst(d, x + w - 96, y + 78, 26, colour=(255, 150, 40))
    # smoke puffs
    for cx, cy, r in [(x + 132, y + 40, 26), (x + 108, y + 52, 18),
                      (x + 306, y + 26, 18), (x + w - 90, y + 56, 22)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 70, 78))
        d.ellipse([cx - r + 10, cy - r + 6, cx + r + 8, cy + r + 4],
                  fill=(90, 86, 94))
    # missile streak
    d.line([(x + 430, y + 18), (x + 486, y + 66)], fill=(255, 240, 200),
           width=3)
    for k in range(4):
        px = x + 430 + k * 14
        py = y + 18 + k * 12
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 140))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_denmark(img, x, y, w, h):
    """Danish flag on a pole over rooftops at night, with a shadowy
    figure and a warning marker."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(36, 52, 92))
    rng = random.Random(41)
    for _ in range(14):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.4))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 220, 200))
    # rooftops
    base = y + h
    for i, (bw, bh) in enumerate([(70, 34), (64, 48), (76, 30), (60, 42)]):
        bx = x + 6 + i * 76
        d.polygon([(bx, base), (bx, base - bh), (bx + bw // 2, base - bh - 16),
                   (bx + bw, base - bh), (bx + bw, base)], fill=(24, 30, 54))
        d.rectangle([bx + 8, base - bh + 8, bx + 14, base - bh + 16],
                    fill=(255, 200, 90))
    # flag pole and Danish flag
    px = x + 210
    d.line([(px, y + 14), (px, base)], fill=(210, 210, 200), width=4)
    fx, fy, fw, fh = px + 4, y + 16, 74, 46
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(198, 12, 48))
    d.rectangle([fx + 20, fy, fx + 30, fy + fh], fill=(255, 255, 255))
    d.rectangle([fx, fy + 18, fx + fw, fy + 28], fill=(255, 255, 255))
    # shadowy figure
    d.ellipse([x + 52, y + 58, x + 66, y + 72], fill=(12, 12, 16))
    d.polygon([(x + 50, y + 74), (x + 68, y + 74), (x + 74, base - 6),
               (x + 44, base - 6)], fill=(12, 12, 16))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def _mini_flag(d, x, y, w, h, kind):
    if kind == "us":
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=col)
        d.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.57)],
                    fill=(30, 48, 96))
        for r in range(3):
            for c in range(4):
                sx = x + 6 + c * 12
                sy = y + 5 + r * 9
                d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1],
                          fill=(255, 255, 255))
    elif kind == "cn":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        starburst(d, x + 12, y + 11, 7, spikes=5, colour=(255, 222, 0))
        starburst(d, x + 30, y + 7, 3, spikes=5, colour=(255, 222, 0))
        starburst(d, x + 34, y + 16, 3, spikes=5, colour=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3],
                    fill=(0, 57, 166))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def draw_summit(img, x, y, w, h):
    """Three flags — US, China, Russia — above a summit table."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(42, 52, 78))
    d.rectangle([x, y + h - 28, x + w, y + h], fill=(96, 68, 44))
    d.rectangle([x, y + h - 34, x + w, y + h - 28], fill=(150, 112, 70))
    fw, fh = 74, 44
    gap = (w - 3 * fw) // 4
    for i, kind in enumerate(("us", "cn", "ru")):
        fx = x + gap + i * (fw + gap)
        fy = y + 8
        d.line([(fx + fw // 2, fy), (fx + fw // 2, y + h - 34)],
               fill=(200, 200, 190), width=3)
        _mini_flag(d, fx, fy + 4, fw, fh, kind)
        d.rectangle([fx, fy + 4, fx + fw, fy + 4 + fh], outline=INK, width=1)
    # three microphones on the table, below the flags
    for cx in (x + 70, x + w // 2, x + w - 70):
        d.line([(cx, y + h - 28), (cx, y + h - 40)], fill=(30, 30, 30),
               width=3)
        d.ellipse([cx - 6, y + h - 52, cx + 6, y + h - 40],
                  fill=(30, 30, 30))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_courtroom(img, x, y, w, h):
    """A courtroom bench, gavel and scales of justice."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w, y + h], fill=(58, 48, 74))
    # back wall panels
    for i in range(4):
        px = x + 10 + i * 76
        d.rectangle([px, y + 8, px + 66, y + 46], outline=(120, 104, 140),
                    width=2)
    # bench
    d.rectangle([x + 16, y + 62, x + w - 16, y + h - 8], fill=(96, 64, 38))
    d.rectangle([x + 16, y + 62, x + w - 16, y + 70], fill=(128, 88, 52))
    # scales of justice
    cx, cy = x + w // 2, y + 30
    d.line([(cx, cy - 14), (cx, cy + 26)], fill=(214, 164, 32), width=3)
    d.line([(cx - 30, cy - 8), (cx + 30, cy - 8)], fill=(214, 164, 32),
           width=3)
    for sx in (cx - 30, cx + 30):
        d.line([(sx, cy - 8), (sx, cy + 14)], fill=(214, 164, 32), width=2)
        d.pieslice([sx - 12, cy + 12, sx + 12, cy + 30], start=0, end=180,
                   fill=(214, 164, 32))
    # gavel on the bench
    d.line([(x + 52, y + 84), (x + 96, y + 78)], fill=(96, 64, 38), width=5)
    d.rectangle([x + 96, y + 70, x + 116, y + 86], fill=(150, 110, 66))
    d.ellipse([x + 48, y + 88, x + 78, y + 96], fill=(170, 130, 80))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def draw_hospital_icon(img, x, y, s):
    """Small hospital building with a red cross."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + s, y + s], fill=(226, 236, 244))
    d.rectangle([x + s * 0.18, y + s * 0.34, x + s * 0.82, y + s],
                fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x + s * 0.42, y + s * 0.08, x + s * 0.58, y + s * 0.34],
                fill=(176, 32, 32))
    d.rectangle([x + s * 0.33, y + s * 0.16, x + s * 0.67, y + s * 0.26],
                fill=(176, 32, 32))
    for i in range(3):
        wx = x + s * (0.26 + i * 0.24)
        d.rectangle([wx, y + s * 0.52, wx + s * 0.1, y + s * 0.66],
                    fill=(120, 160, 200))
    d.rectangle([x + s * 0.42, y + s * 0.78, x + s * 0.58, y + s],
                fill=(96, 64, 38))
    d.rectangle([x, y, x + s - 1, y + s - 1], outline=INK, width=2)


def draw_globe_icon(img, x, y, s):
    """A blue globe with green land and a small sun."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 244))
    cx, cy, r = x + s // 2, y + s // 2 + 2, s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 196),
              outline=INK, width=2)
    d.ellipse([cx - r + 8, cy - r + 10, cx - r + 30, cy - r + 26],
              fill=(86, 168, 92))
    d.polygon([(cx + 2, cy - r + 14), (cx + 22, cy - r + 8),
               (cx + 26, cy - r + 22), (cx + 8, cy - r + 26)],
              fill=(86, 168, 92))
    d.ellipse([cx - 6, cy + 6, cx + 16, cy + 24], fill=(86, 168, 92))
    for k in range(-2, 3):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=90 + k * 36,
              end=90 + k * 36 + 18, fill=(30, 80, 150), width=1)
    d.ellipse([x + s - 16, y + 2, x + s - 4, y + 14], fill=(255, 196, 66))
    d.rectangle([x, y, x + s - 1, y + s - 1], outline=INK, width=2)


def draw_crowd_icon(img, x, y, s):
    """A protest crowd: heads, shoulders and placards."""
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + s, y + s], fill=(244, 226, 200))
    cols = [(176, 32, 32), (30, 58, 95), (214, 164, 32), (86, 120, 80),
            (120, 60, 120)]
    for i, col in enumerate(cols):
        hx = x + 8 + i * 12
        d.ellipse([hx, y + s * 0.42, hx + 12, y + s * 0.42 + 12], fill=col)
        d.pieslice([hx - 3, y + s * 0.58, hx + 15, y + s], start=180, end=360,
                   fill=col)
    # two placards
    d.rectangle([x + 10, y + 8, x + 34, y + 26], fill=(255, 255, 255),
                outline=INK, width=2)
    d.line([(x + 22, y + 26), (x + 22, y + 40)], fill=INK, width=2)
    d.rectangle([x + s - 34, y + 12, x + s - 10, y + 30],
                fill=(176, 32, 32), outline=INK, width=2)
    d.line([(x + s - 22, y + 30), (x + s - 22, y + 44)], fill=INK, width=2)
    d.rectangle([x, y, x + s - 1, y + s - 1], outline=INK, width=2)
