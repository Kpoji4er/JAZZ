# -*- coding: utf-8 -*-
"""Meltdown VengefulTemperament: Active hotbar 108x54 dual from vanilla Personal perk.

Source is the original perk tile (skull in flame), same pipeline as other
perk-actives (`_build_jazz_perk_sig_icons_from_personal.py`): key near-black,
crop glyph, fit into each 54x54 half, GREY left / CREAM right.

Do NOT use HUD `perk_vengeful_temperament` (scanline skull) — that is the
wrong glyph for this CombatAction.

JAZZ CA is ActionType=Other (Hurricane Norma) so CombatActionBarButton SetColumns=2.
CE Icon stays UI/Icons/Perks/VengefulTemperament (character sheet).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
VANILLA = JAZZ / "Perks" / "references" / "vanilla" / "VengefulTemperament.png"
OUT = JAZZ / "Perks" / "SignatureAbilities" / "VengefulTemperament.png"
ITEMS = UNITS / "items.lua"
ICON = "Mod/e6L4ECj/Perks/SignatureAbilities/VengefulTemperament.png"

GREY = np.array([0xB5, 0xAD, 0xA5], dtype=np.float32)
CREAM = np.array([0xF7, 0xF7, 0xD6], dtype=np.float32)
HALF = 54
# Complex skull+flame: a bit larger than simple stencils so inner holes stay readable.
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


def fit_to_half(glyph: np.ndarray, fill: np.ndarray) -> np.ndarray:
    """Scale glyph into 54x54; recolor to HUD fill, keep source luminance for inner detail."""
    g = Image.fromarray(glyph, "RGBA")
    gw, gh = g.size
    scale = min(GLYPH_MAX / max(gw, 1), GLYPH_MAX / max(gh, 1), 1.0)
    nw, nh = max(1, int(round(gw * scale))), max(1, int(round(gh * scale)))
    g = g.resize((nw, nh), Image.Resampling.LANCZOS)
    arr = np.array(g, dtype=np.float32)
    alpha = arr[:, :, 3] / 255.0
    rgb = arr[:, :, :3]
    lum = (0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]) / 255.0
    vis = alpha > 0.08
    peak = float(lum[vis].max()) if vis.any() else 1.0
    if peak < 1e-6:
        peak = 1.0
    # Keep skull/flame shading; lift floor so HUD grey/cream stays readable.
    shade = np.clip(lum / peak, 0.0, 1.0)
    shade = 0.40 + 0.60 * shade
    tinted = fill * shade[..., None]
    out = np.zeros((HALF, HALF, 4), dtype=np.float32)
    x0 = (HALF - nw) // 2
    y0 = (HALF - nh) // 2
    out[y0 : y0 + nh, x0 : x0 + nw, :3] = tinted
    out[y0 : y0 + nh, x0 : x0 + nw, 3] = alpha * 255.0
    return out.astype(np.uint8)


def build_dual(src: Path) -> Image.Image:
    keyed = key_black_to_alpha(np.array(Image.open(src).convert("RGBA")))
    glyph = extract_glyph(keyed)
    strip = np.concatenate([fit_to_half(glyph, GREY), fit_to_half(glyph, CREAM)], axis=1)
    return Image.fromarray(strip, "RGBA")


def wire_units_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    old = 'Icon = "UI/Icons/Perks/VengefulTemperament",\n\t\t\tIdDefault = "VengefulTemperamentdefault",'
    new = f'Icon = "{ICON}",\n\t\t\tIdDefault = "VengefulTemperamentdefault",'
    if old not in text:
        if ICON in text:
            print("items.lua: CombatAction Icon already wired")
            return
        raise SystemExit("jazz-units items.lua: CombatAction Icon anchor missing")
    ITEMS.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("wired jazz-units CombatAction.Icon")


def main() -> int:
    if not VANILLA.exists():
        raise SystemExit(f"missing vanilla perk {VANILLA}")
    src = Image.open(VANILLA)
    print(f"vanilla perk {VANILLA.name}: {src.size}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = build_dual(VANILLA)
    img.save(OUT)
    print(f"wrote {OUT.relative_to(JAZZ)} {img.size}")
    wire_units_items()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
