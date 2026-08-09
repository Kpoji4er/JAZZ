# -*- coding: utf-8 -*-
"""Paint ammo-type variants onto ONE blank carton plate (identical mesh).

Ensures per-caliber form lock: body tint + mid wrap band + ink/text only.
Does not regenerate box geometry.

Example (9x18):
  python docs/tools/_paint_ammo_carton_family.py \\
    --plate Ammopics/_gen/_plate_9x18_blank.png \\
    --family 9x18 \\
    --out-dir Ammopics/_gen
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def load_rgba(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGBA"))


def luminance(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    return 0.299 * r + 0.587 * g + 0.114 * b


def tint_body(plate_rgb: np.ndarray, mask: np.ndarray, color: tuple[int, int, int], mix: float) -> np.ndarray:
    out = plate_rgb.astype(np.float32).copy()
    p_lum = luminance(out)
    mean_l = float(p_lum[mask].mean()) + 1e-3
    target = np.array(color, dtype=np.float32)
    shaded = np.clip(target[None, None, :] * (p_lum[:, :, None] / mean_l), 0, 255)
    out[mask] = (1.0 - mix) * out[mask] + mix * shaded[mask]
    return out


def paint_mid_band(
    rgb: np.ndarray,
    mask: np.ndarray,
    *,
    y0: int,
    y1: int,
    color: tuple[int, int, int],
) -> np.ndarray:
    out = rgb.astype(np.float32)
    p_lum = luminance(out)
    band = mask.copy()
    band[:y0, :] = False
    band[y1:, :] = False
    if not band.any():
        return out.astype(np.uint8)
    mean_l = float(p_lum[band].mean()) + 1e-3
    target = np.array(color, dtype=np.float32)
    shaded = np.clip(target[None, None, :] * (p_lum[:, :, None] / mean_l), 0, 255)
    out[band] = shaded[band]
    return out.astype(np.uint8)


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, fill) -> None:
    pts = []
    for i in range(10):
        ang = np.deg2rad(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rad * np.cos(ang), cy + rad * np.sin(ang)))
    draw.polygon(pts, fill=fill)


def stamp_text(
    rgb: np.ndarray,
    alpha: np.ndarray,
    *,
    lines: list[tuple[str, tuple[int, int], int, tuple[int, int, int]]],
    side_pm: bool = True,
) -> np.ndarray:
    """lines: (text, (x,y), font_size, color) top-left anchors."""
    im = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), "RGBA")
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    ink = (28, 30, 36, 230)

    if side_pm:
        # left side panel of ¾ carton (matches Ammopics/9x18.png layout)
        f = find_font(10)
        draw.text((14, 14), "ПМ", font=f, fill=ink)
        draw_star(draw, 22, 36, 5.5, ink)

    for text, (x, y), size, color in lines:
        f = find_font(size)
        draw.text((x, y), text, font=f, fill=(*color, 230))

    composed = Image.alpha_composite(im, overlay)
    arr = np.array(composed)
    arr[:, :, 3] = alpha
    arr[alpha <= 8] = (0, 0, 0, 0)
    return arr[:, :, :3]


# family presets: body, optional band, front lines
FAMILIES: dict[str, dict[str, dict]] = {
    "9x18": {
        "band_y": (48, 64),
        "variants": {
            "substandart": {
                "out": "gen_9x18substandart.png",
                "body": (98, 118, 72),
                "body_mix": 0.78,
                "band": None,
                "lines": [
                    ("9x18", (52, 16), 11, (28, 30, 36)),
                    ("57-Н-181С", (44, 68), 8, (28, 30, 36)),
                    ("Substandard", (42, 82), 7, (40, 44, 36)),
                ],
            },
            "fmj": {
                "out": "gen_9x18.png",
                "body": (148, 146, 142),
                "body_mix": 0.35,
                "band": (120, 122, 128),
                "lines": [
                    ("9x18", (52, 16), 11, (28, 30, 36)),
                    ("ПСО", (56, 68), 11, (28, 30, 36)),
                ],
            },
            "crafted": {
                "out": "gen_9x18Crafted.png",
                "body": (148, 112, 72),
                "body_mix": 0.78,
                "band": None,
                "lines": [
                    ("9x18", (52, 16), 11, (36, 28, 20)),
                    ("кустарный", (46, 68), 9, (36, 28, 20)),
                ],
            },
            "jhp": {
                "out": "gen_9x18JHP.png",
                "body": (150, 148, 146),
                "body_mix": 0.25,
                "band": (55, 105, 200),
                "lines": [
                    ("9x18", (52, 16), 11, (28, 30, 36)),
                    ("СП-7", (56, 68), 11, (40, 80, 170)),
                ],
            },
            "ap": {
                "out": "gen_9x18AP.png",
                "body": (150, 148, 146),
                "body_mix": 0.25,
                "band": (200, 45, 40),
                "lines": [
                    ("9x18", (52, 16), 11, (28, 30, 36)),
                    ("ПСТ", (58, 68), 11, (180, 35, 30)),
                ],
            },
            "app": {
                "out": "gen_9x18APP.png",
                "body": (150, 148, 146),
                "body_mix": 0.25,
                "band": (120, 35, 55),
                "lines": [
                    ("9x18", (52, 16), 11, (28, 30, 36)),
                    ("7н25", (54, 68), 11, (110, 30, 50)),
                ],
            },
        },
    }
}


def paint_variant(plate: np.ndarray, spec: dict, band_y: tuple[int, int]) -> Image.Image:
    rgb = plate[:, :, :3].astype(np.float32)
    a = plate[:, :, 3]
    mask = a > 8
    rgb = tint_body(rgb, mask, tuple(spec["body"]), float(spec["body_mix"]))
    if spec.get("band"):
        rgb = paint_mid_band(rgb, mask, y0=band_y[0], y1=band_y[1], color=tuple(spec["band"]))
    else:
        rgb = rgb.astype(np.uint8)
    rgb = stamp_text(rgb, a, lines=spec["lines"], side_pm=True)
    out = np.dstack([rgb, a])
    return Image.fromarray(out, "RGBA")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plate", type=Path, required=True)
    ap.add_argument("--family", required=True, choices=sorted(FAMILIES))
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--only", nargs="*", help="optional variant keys")
    args = ap.parse_args()

    fam = FAMILIES[args.family]
    plate = load_rgba(args.plate)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    keys = args.only or list(fam["variants"])
    for key in keys:
        spec = fam["variants"][key]
        im = paint_variant(plate, spec, fam["band_y"])
        dst = args.out_dir / spec["out"]
        im.save(dst)
        print(f"{key} -> {dst.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
