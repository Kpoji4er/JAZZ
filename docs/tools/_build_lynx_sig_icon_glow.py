# -*- coding: utf-8 -*-
"""Passive hotbar Jazz_Perk_Lynx: 54x54 cool blue, keep glowing eyes.

Standard _build_passive_signature_icon_54.py recolors the whole glyph to solid
COOL and would wipe the eye bloom. This keeps high-luma pixels as cyan-white
glow (+ 1px bloom) and paints the rest of the lynx head in Hud LEFT blue.

  python docs/tools/_build_lynx_sig_icon_glow.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Perks" / "Personal" / "Lynx.png"
OUT = ROOT / "Perks" / "SignatureAbilities" / "Jazz_Perk_Lynx.png"

COOL = np.array([0x60, 0x9B, 0xB8], dtype=np.float32)
GLOW = np.array([0xD8, 0xF6, 0xFF], dtype=np.float32)
CORE = np.array([0xFF, 0xFF, 0xFF], dtype=np.float32)
OUT_S = 54
GLYPH_MAX = 42
GLOW_LUMA = 170.0
CORE_LUMA = 230.0


def key_black(rgba: np.ndarray, thr: int = 28) -> np.ndarray:
    out = rgba.copy()
    lum = out[:, :, :3].max(axis=2)
    mask = (lum <= thr) & (out[:, :, 3] > 0)
    out[mask, 3] = 0
    return out


def extract(rgba: np.ndarray) -> np.ndarray:
    a = rgba[:, :, 3] > 20
    if not a.any():
        return rgba
    ys, xs = np.where(a)
    return rgba[int(ys.min()) : int(ys.max()) + 1, int(xs.min()) : int(xs.max()) + 1]


def luma(rgb: np.ndarray) -> np.ndarray:
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def dilate(mask: np.ndarray) -> np.ndarray:
    h, w = mask.shape
    out = mask.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            y0, y1 = max(0, dy), h + min(0, dy)
            x0, x1 = max(0, dx), w + min(0, dx)
            out[y0:y1, x0:x1] |= mask[y0 - dy : y1 - dy, x0 - dx : x1 - dx]
    return out


def build() -> Image.Image:
    keyed = key_black(np.array(Image.open(SRC).convert("RGBA")))
    glyph = extract(keyed)
    g = Image.fromarray(glyph, "RGBA")
    gw, gh = g.size
    scale = min(GLYPH_MAX / max(gw, 1), GLYPH_MAX / max(gh, 1), 1.0)
    nw, nh = max(1, int(round(gw * scale))), max(1, int(round(gh * scale)))
    arr = np.array(g.resize((nw, nh), Image.Resampling.LANCZOS), dtype=np.float32)
    a = arr[:, :, 3] / 255.0
    L = luma(arr[:, :, :3])
    glow = (a > 0.2) & (L >= GLOW_LUMA)
    core = (a > 0.2) & (L >= CORE_LUMA)
    halo = dilate(dilate(glow))

    canvas = np.zeros((OUT_S, OUT_S, 4), dtype=np.float32)
    x0 = (OUT_S - nw) // 2
    y0 = (OUT_S - nh) // 2
    sl = canvas[y0 : y0 + nh, x0 : x0 + nw]
    body = (a > 0.05) & ~glow
    sl[body, :3] = COOL
    sl[body, 3] = a[body] * 255.0
    # Halo even over near-empty neighbors so eyes read at 54px.
    sl[halo, :3] = GLOW
    sl[halo, 3] = np.maximum(sl[halo, 3], 110.0)
    sl[glow, :3] = GLOW
    sl[glow, 3] = np.maximum(a[glow] * 255.0, 220.0)
    sl[core, :3] = CORE
    sl[core, 3] = 255.0
    return Image.fromarray(canvas.astype(np.uint8), "RGBA")


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = build()
    img.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)} {img.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
