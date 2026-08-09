# -*- coding: utf-8 -*-
"""Normalize ammo icon box footprint to a reference canvas (110x110)."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def content_bbox(im: Image.Image, thr: int = 28) -> tuple[int, int, int, int]:
    px = im.convert("RGB").load()
    w, h = im.size
    min_x, min_y, max_x, max_y = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r + g + b > thr:
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
    if max_x < 0:
        raise SystemExit("empty content")
    return min_x, min_y, max_x + 1, max_y + 1


def normalize(
    src: Path,
    dst: Path,
    *,
    canvas: int = 110,
    fit_w: int = 100,
    fit_h: int = 86,
    thr: int = 28,
) -> None:
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if r + g + b <= thr:
                px[x, y] = (0, 0, 0, 0)
    alpha = im.split()[-1]
    bbox = alpha.getbbox()
    if not bbox:
        raise SystemExit(f"no content: {src}")
    crop = im.crop(bbox)
    # contain into fit_w x fit_h
    scale = min(fit_w / crop.width, fit_h / crop.height)
    tw = max(1, int(round(crop.width * scale)))
    th = max(1, int(round(crop.height * scale)))
    crop = crop.resize((tw, th), Image.Resampling.LANCZOS)
    rgb = Image.new("RGB", (canvas, canvas), (0, 0, 0))
    ox = (canvas - tw) // 2
    oy = (canvas - th) // 2
    rgb.paste(crop.convert("RGB"), (ox, oy), crop.split()[-1])
    rgb.save(dst)
    print(f"{src.name} -> {dst.name} box {tw}x{th} @({ox},{oy})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--fit-w", type=int, default=100)
    ap.add_argument("--fit-h", type=int, default=86)
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for s in args.sources:
        src = Path(s)
        normalize(src, out_dir / src.name, fit_w=args.fit_w, fit_h=args.fit_h)


if __name__ == "__main__":
    main()
