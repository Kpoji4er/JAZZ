#!/usr/bin/env python3
"""Generate simplified AME nationality flag PNG icons for JAZZ-UNITS-005.

Reads nothing; writes 128x80 RGBA PNGs to Icons/Flags/ (f_<country>.png).
Run from jazz/ package root: python docs/tools/_gen_ame_flags.py
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "Icons" / "Flags"
W, H = 128, 80

# Approximate official palette (simplified UI icons).
GREEN = (0, 135, 81)
GREEN_D = (0, 107, 63)
GREEN_K = (0, 122, 61)
GREEN_S = (0, 133, 63)
GREEN_E = (7, 137, 48)
RED = (206, 17, 38)
RED_G = (206, 17, 38)
RED_A = (204, 9, 47)
RED_E = (218, 18, 26)
YELLOW = (252, 209, 22)
YELLOW_G = (252, 209, 22)
YELLOW_S = (253, 239, 66)
YELLOW_E = (252, 221, 9)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_E = (11, 79, 156)


def _save(name: str, img: Image.Image) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    img.save(path, "PNG")
    return path


def _star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, points: int, fill, inner: float = 0.38):
    pts = []
    for i in range(points * 2):
        angle = math.radians(-90 + i * 180 / points)
        rad = r if i % 2 == 0 else r * inner
        pts.append((cx + rad * math.cos(angle), cy + rad * math.sin(angle)))
    draw.polygon(pts, fill=fill)


def flag_nigeria() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    third = W // 3
    d.rectangle((0, 0, third, H), fill=GREEN)
    d.rectangle((third, 0, 2 * third, H), fill=WHITE)
    d.rectangle((2 * third, 0, W, H), fill=GREEN)
    return img


def flag_mali() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    third = W // 3
    d.rectangle((0, 0, third, H), fill=(20, 181, 59))
    d.rectangle((third, 0, 2 * third, H), fill=YELLOW)
    d.rectangle((2 * third, 0, W, H), fill=RED)
    return img


def flag_ghana() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    band = H // 3
    d.rectangle((0, 0, W, band), fill=RED_G)
    d.rectangle((0, band, W, 2 * band), fill=YELLOW_G)
    d.rectangle((0, 2 * band, W, H), fill=GREEN_D)
    _star(d, W / 2, H / 2, min(W, H) * 0.14, 5, BLACK)
    return img


def flag_senegal() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    third = W // 3
    d.rectangle((0, 0, third, H), fill=GREEN_S)
    d.rectangle((third, 0, 2 * third, H), fill=YELLOW_S)
    d.rectangle((2 * third, 0, W, H), fill=(227, 27, 35))
    _star(d, W / 2, H / 2, min(W, H) * 0.13, 5, GREEN_S)
    return img


def flag_ethiopia() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    band = H // 3
    d.rectangle((0, 0, W, band), fill=GREEN_E)
    d.rectangle((0, band, W, 2 * band), fill=YELLOW_E)
    d.rectangle((0, 2 * band, W, H), fill=RED_E)
    r = min(W, H) * 0.22
    cx, cy = W / 2, H / 2
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BLUE_E)
    _star(d, cx, cy, r * 0.55, 5, YELLOW_E, inner=0.45)
    return img


def flag_congo() -> Image.Image:
    """Republic of the Congo: green hoist-top, red fly-bottom, yellow diagonal."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Diagonal lower-left → upper-right; band ~ H/5 thick at center.
    band = max(8, H // 5)
    # Green triangle (upper hoist)
    d.polygon([(0, 0), (W, 0), (0, H)], fill=(0, 150, 57))
    # Red triangle (lower fly)
    d.polygon([(W, H), (W, 0), (0, H)], fill=RED)
    # Yellow band as parallelogram along diagonal
    # Line through (0,H) to (W,0); offset by band/2 each side
    diag_len = math.hypot(W, H)
    nx, ny = H / diag_len, W / diag_len  # unit normal
    ox, oy = nx * band / 2, ny * band / 2
    d.polygon(
        [
            (0 + ox, H - oy),
            (W + ox, 0 - oy),
            (W - ox, 0 + oy),
            (0 - ox, H + oy),
        ],
        fill=YELLOW,
    )
    return img


def flag_angola() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    mid = H // 2
    d.rectangle((0, 0, W, mid), fill=RED_A)
    d.rectangle((0, mid, W, H), fill=BLACK)
    # Simplified emblem: yellow gear ring + star + machete hint
    cx, cy = W / 2, H / 2
    r = min(W, H) * 0.22
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YELLOW, outline=YELLOW)
    d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), fill=RED_A)
    _star(d, cx, cy - r * 0.08, r * 0.28, 5, YELLOW, inner=0.42)
    # Half machete blade (black on yellow ring edge)
    d.polygon(
        [
            (cx + r * 0.15, cy - r * 0.05),
            (cx + r * 0.95, cy - r * 0.35),
            (cx + r * 0.85, cy - r * 0.15),
            (cx + r * 0.35, cy + r * 0.05),
        ],
        fill=BLACK,
    )
    return img


def flag_kenya() -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Black / red / green with white fimbriations (6 stripes)
    stripes = [
        (BLACK, 0.30),
        (WHITE, 0.02),
        (RED, 0.16),
        (WHITE, 0.02),
        (GREEN_K, 0.50),
    ]
    y = 0
    for color, frac in stripes:
        h = max(1, round(H * frac))
        d.rectangle((0, y, W, min(H, y + h)), fill=color)
        y += h
    if y < H:
        d.rectangle((0, y, W, H), fill=GREEN_K)
    # Simplified Maasai shield (center)
    cx, cy = W / 2, H / 2
    sw, sh = W * 0.18, H * 0.38
    shield = [
        (cx, cy - sh / 2),
        (cx + sw / 2, cy - sh * 0.15),
        (cx + sw / 2, cy + sh * 0.35),
        (cx, cy + sh / 2),
        (cx - sw / 2, cy + sh * 0.35),
        (cx - sw / 2, cy - sh * 0.15),
    ]
    d.polygon(shield, fill=WHITE, outline=BLACK)
    d.polygon(
        [
            (cx, cy - sh * 0.38),
            (cx + sw * 0.35, cy),
            (cx, cy + sh * 0.38),
            (cx - sw * 0.35, cy),
        ],
        fill=RED,
    )
    d.line([(cx - sw * 0.55, cy - sh * 0.05), (cx - W * 0.28, cy - H * 0.22)], fill=BLACK, width=2)
    d.line([(cx + sw * 0.55, cy - sh * 0.05), (cx + W * 0.28, cy - H * 0.22)], fill=BLACK, width=2)
    return img


FLAGS = {
    "f_nigeria.png": flag_nigeria,
    "f_kenya.png": flag_kenya,
    "f_angola.png": flag_angola,
    "f_mali.png": flag_mali,
    "f_congo.png": flag_congo,
    "f_ghana.png": flag_ghana,
    "f_senegal.png": flag_senegal,
    "f_ethiopia.png": flag_ethiopia,
}


def main() -> None:
    written: list[tuple[str, tuple[int, int]]] = []
    for filename, builder in FLAGS.items():
        img = builder()
        path = _save(filename, img)
        written.append((str(path.relative_to(ROOT)), img.size))
    print(f"Wrote {len(written)} flags to {OUT_DIR.relative_to(ROOT)}/")
    for rel, size in written:
        print(f"  {rel}  {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
