# -*- coding: utf-8 -*-
"""Meltdown VengefulTemperament: Active hotbar needs 108x54 dual, not Personal 68x68.

Vanilla CA was Passive (`UI/Icons/Hud/perk_vengeful_temperament`, SetColumns=1).
JAZZ CA is ActionType=Other (Hurricane Norma) so CombatActionBarButton SetColumns=2.
Build dual strip from the vanilla HUD glyph; wire jazz-units CombatAction.Icon.
CE Icon stays UI/Icons/Perks/VengefulTemperament (character sheet).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
HUD = JAZZ / "Icons" / "Hud" / "references" / "perk_vengeful_temperament.png"
OUT = JAZZ / "Perks" / "SignatureAbilities" / "VengefulTemperament.png"
ITEMS = UNITS / "items.lua"
ICON = "Mod/e6L4ECj/Perks/SignatureAbilities/VengefulTemperament.png"

GREY = np.array([0xB5, 0xAD, 0xA5], dtype=np.float32)
CREAM = np.array([0xF7, 0xF7, 0xD6], dtype=np.float32)
HALF = 54
GLYPH_MAX = 38


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
    g = Image.fromarray(glyph, "RGBA")
    gw, gh = g.size
    scale = min(GLYPH_MAX / max(gw, 1), GLYPH_MAX / max(gh, 1), 1.0)
    nw, nh = max(1, int(round(gw * scale))), max(1, int(round(gh * scale)))
    g = g.resize((nw, nh), Image.Resampling.LANCZOS)
    arr = np.array(g, dtype=np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    rgb = np.broadcast_to(fill, arr[:, :, :3].shape)
    out = np.zeros((HALF, HALF, 4), dtype=np.float32)
    x0 = (HALF - nw) // 2
    y0 = (HALF - nh) // 2
    out[y0 : y0 + nh, x0 : x0 + nw, :3] = rgb
    out[y0 : y0 + nh, x0 : x0 + nw, 3:4] = alpha * 255.0
    return out.astype(np.uint8)


def build_dual(src: Path) -> Image.Image:
    keyed = key_black_to_alpha(np.array(Image.open(src).convert("RGBA")))
    # If already a 108x54 dual, take LEFT half as the glyph source.
    h, w = keyed.shape[:2]
    if w >= 100 and h <= 60:
        keyed = keyed[:, : w // 2]
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
    if not HUD.exists():
        raise SystemExit(f"missing HUD ref {HUD}")
    src = Image.open(HUD)
    print(f"HUD ref {HUD.name}: {src.size}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = build_dual(HUD)
    img.save(OUT)
    print(f"wrote {OUT.relative_to(JAZZ)} {img.size}")
    wire_units_items()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
