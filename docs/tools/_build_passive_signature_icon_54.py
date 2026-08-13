# -*- coding: utf-8 -*-
"""Build Passive SignatureAbilities HUD icons as 54x54 single tiles.

CombatActionBarButton: Passive → SetColumns(1); Active → SetColumns(2).
So Passive must be 54x54 (one glyph). Active/dual-state stay 108x54.

Sources: Hud dual 108x54 — take **LEFT** (cool/blue) half, not cream right —
or Personal 68x68 recolored to cool blue.

  python docs/tools/_build_passive_signature_icon_54.py SteroidPunch
  python docs/tools/_build_passive_signature_icon_54.py --from-hud perk_steroid_punch SteroidPunch
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HUD_REF = ROOT / "Icons" / "Hud" / "references"
PERSONAL = ROOT / "Perks" / "Personal"
SIG = ROOT / "Perks" / "SignatureAbilities"

# Passive hotbar (SetColumns=1) must match vanilla Passive perk_* tone:
# cool blue-grey of the LEFT dual-strip half — NOT sand cream (right half).
# Cream looks white on the bar and mismatches ExplodingPalm / TagTeam style.
COOL = np.array([0x60, 0x9B, 0xB8], dtype=np.float32)  # ≈ Hud left-half mean
CREAM = np.array([0xF7, 0xF7, 0xD6], dtype=np.float32)  # active dual right; do not use for Passive
OUT = 54
GLYPH_MAX = 42


def key_black_to_alpha(rgba: np.ndarray, thr: int = 28) -> np.ndarray:
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.int16)
    lum = rgb.max(axis=2)
    mask = (lum <= thr) & (out[:, :, 3] > 0)
    out[mask, 3] = 0
    return out


def extract_glyph(rgba: np.ndarray) -> np.ndarray:
    a = rgba[:, :, 3] > 20
    if not a.any():
        return rgba
    ys, xs = np.where(a)
    return rgba[int(ys.min()) : int(ys.max()) + 1, int(xs.min()) : int(xs.max()) + 1]


def fit_recolor(glyph: np.ndarray, fill: np.ndarray) -> Image.Image:
    g = Image.fromarray(glyph, "RGBA")
    gw, gh = g.size
    scale = min(GLYPH_MAX / max(gw, 1), GLYPH_MAX / max(gh, 1), 1.0)
    nw, nh = max(1, int(round(gw * scale))), max(1, int(round(gh * scale)))
    g = g.resize((nw, nh), Image.Resampling.LANCZOS)
    arr = np.array(g, dtype=np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    out = np.zeros((OUT, OUT, 4), dtype=np.float32)
    x0 = (OUT - nw) // 2
    y0 = (OUT - nh) // 2
    out[y0 : y0 + nh, x0 : x0 + nw, :3] = fill
    out[y0 : y0 + nh, x0 : x0 + nw, 3:4] = alpha * 255.0
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def from_hud_dual(stem: str, *, keep_colors: bool = True) -> Image.Image:
    """Passive icon from Hud ref.

    Prefer cropping the LEFT 54×54 of a 108×54 dual (cool/blue state) and keeping
    pixels — recoloring to cream was the SteroidPunch white-artifact bug.
    """
    path = HUD_REF / f"{stem}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    src = np.array(Image.open(path).convert("RGBA"))
    w, h = src.shape[1], src.shape[0]
    if w >= 100 and h <= 60:
        # dual strip — LEFT half = Passive cool/blue (right = cream/selected)
        half = src[:, : w // 2]
    else:
        half = src
    if half.shape[0] == OUT and half.shape[1] == OUT and keep_colors:
        # already a perfect Passive tile (or left crop of dual)
        out = half.copy()
        # key near-black scanline bars to alpha for cleaner HUD composite
        return Image.fromarray(key_black_to_alpha(out, thr=18), "RGBA")
    keyed = key_black_to_alpha(half)
    fill = COOL if keep_colors else CREAM
    return fit_recolor(extract_glyph(keyed), fill)


def from_personal(stem: str) -> Image.Image:
    path = PERSONAL / f"{stem}.png"
    if not path.exists():
        # fallback vanilla personal ref
        alt = ROOT / "Perks" / "references" / "vanilla" / f"{stem}.png"
        path = alt if alt.exists() else path
    if not path.exists():
        raise FileNotFoundError(path)
    keyed = key_black_to_alpha(np.array(Image.open(path).convert("RGBA")))
    return fit_recolor(extract_glyph(keyed), COOL)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action_id", help="CombatAction id / output PNG stem, e.g. SteroidPunch")
    ap.add_argument("--from-hud", default="", help="Hud reference stem without .png")
    ap.add_argument("--from-personal", default="", help="Personal tile stem without .png")
    args = ap.parse_args()
    SIG.mkdir(parents=True, exist_ok=True)
    if args.from_hud:
        img = from_hud_dual(args.from_hud)
    elif args.from_personal:
        img = from_personal(args.from_personal)
    else:
        # Steroid default: hud dual → 54
        try:
            img = from_hud_dual("perk_steroid_punch" if args.action_id == "SteroidPunch" else f"perk_{args.action_id.lower()}")
        except FileNotFoundError:
            img = from_personal(args.action_id)
    out = SIG / f"{args.action_id}.png"
    img.save(out)
    print(f"wrote {out.relative_to(ROOT)} size={img.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
