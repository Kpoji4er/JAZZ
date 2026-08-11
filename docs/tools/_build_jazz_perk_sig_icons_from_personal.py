# -*- coding: utf-8 -*-
"""Build Passive SignatureAbilities HUD icons (108x54 dual-strip) from Personal 68x68 tiles.

Personal tiles often have a solid black draft background; HUD expects transparent
dual-strip (left grey / right cream). Wire CombatAction.Icon to SignatureAbilities
while CharacterEffect.Icon stays on Perks/Personal.

Run from jazz root:
  python docs/tools/_build_jazz_perk_sig_icons_from_personal.py
  python docs/tools/_validate_items_quick.py
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PERSONAL = ROOT / "Perks" / "Personal"
SIG = ROOT / "Perks" / "SignatureAbilities"
ITEMS = ROOT / "items.lua"

# Passive named perks that still point CombatAction.Icon at Personal tiles.
TARGETS = (
    "Jazz_Perk_Lynx",
    "Jazz_Perk_Buzz",
    "Jazz_Perk_Spider",
    "Jazz_Perk_Colby",
)

GREY = np.array([0xB5, 0xAD, 0xA5], dtype=np.float32)
CREAM = np.array([0xF7, 0xF7, 0xD6], dtype=np.float32)
HALF = 54
OUT_W, OUT_H = 108, 54
# Visible glyph fill inside each 54x54 half (pad ~8).
GLYPH_MAX = 38


def personal_stem(perk_id: str) -> str:
    return perk_id.replace("Jazz_Perk_", "")


def key_black_to_alpha(rgba: np.ndarray, thr: int = 28) -> np.ndarray:
    """Treat near-black draft background as transparent."""
    out = rgba.copy()
    rgb = out[:, :, :3].astype(np.int16)
    lum = rgb.max(axis=2)
    mask = (lum <= thr) & (out[:, :, 3] > 0)
    out[mask, 3] = 0
    return out


def extract_glyph(rgba: np.ndarray) -> np.ndarray:
    """Crop to opaque bbox, return RGBA glyph."""
    a = rgba[:, :, 3] > 20
    if not a.any():
        return rgba
    ys, xs = np.where(a)
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    return rgba[y0:y1, x0:x1]


def fit_to_half(glyph: np.ndarray, fill: np.ndarray) -> np.ndarray:
    """Scale glyph into 54x54, recolor solid fill, keep AA alpha."""
    g = Image.fromarray(glyph, "RGBA")
    gw, gh = g.size
    scale = min(GLYPH_MAX / max(gw, 1), GLYPH_MAX / max(gh, 1), 1.0)
    nw, nh = max(1, int(round(gw * scale))), max(1, int(round(gh * scale)))
    g = g.resize((nw, nh), Image.Resampling.LANCZOS)
    arr = np.array(g, dtype=np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    # Recolor RGB by alpha; ignore source chroma (Personal tiles vary).
    rgb = np.broadcast_to(fill, arr[:, :, :3].shape)
    out = np.zeros((HALF, HALF, 4), dtype=np.float32)
    x0 = (HALF - nw) // 2
    y0 = (HALF - nh) // 2
    out[y0 : y0 + nh, x0 : x0 + nw, :3] = rgb
    out[y0 : y0 + nh, x0 : x0 + nw, 3:4] = alpha * 255.0
    return out.astype(np.uint8)


def build_dual(personal_path: Path) -> Image.Image:
    src = np.array(Image.open(personal_path).convert("RGBA"))
    keyed = key_black_to_alpha(src)
    glyph = extract_glyph(keyed)
    left = fit_to_half(glyph, GREY)
    right = fit_to_half(glyph, CREAM)
    strip = np.concatenate([left, right], axis=1)
    return Image.fromarray(strip, "RGBA")


def wire_items(perk_ids: list[str]) -> int:
    text = ITEMS.read_text(encoding="utf-8")
    changed = 0
    for pid in perk_ids:
        icon_path = f"Mod/e6L4ECj/Perks/SignatureAbilities/{pid}.png"

        def repl(m: re.Match[str], icon=icon_path, perk=pid) -> str:
            nonlocal changed
            block = m.group(0)
            if f'id = "{perk}"' not in block:
                return block
            new_block, n = re.subn(
                r'Icon = "[^"]+"',
                f'Icon = "{icon}"',
                block,
                count=1,
            )
            if n:
                changed += 1
            return new_block

        pattern = re.compile(
            rf"PlaceObj\('ModItemCombatAction',\s*\{{(?:(?!PlaceObj\('ModItemCombatAction').)*?id = \"{re.escape(pid)}\"\s*,?\s*\}}\),",
            re.S,
        )
        text, _ = pattern.subn(repl, text, count=1)
    if changed:
        tmp = ITEMS.with_suffix(".lua.tmp_wire")
        tmp.write_text(text, encoding="utf-8", newline="\n")
        tmp.replace(ITEMS)
    return changed


def main() -> int:
    SIG.mkdir(parents=True, exist_ok=True)
    built: list[str] = []
    for pid in TARGETS:
        src = PERSONAL / f"{personal_stem(pid)}.png"
        if not src.exists():
            print(f"MISSING personal {src}")
            continue
        out = SIG / f"{pid}.png"
        build_dual(src).save(out)
        print(f"wrote {out.relative_to(ROOT)} from {src.name}")
        built.append(pid)
    n = wire_items(built)
    print(f"wired CombatAction.Icon for {n} ModItems")
    return 0 if built else 1


if __name__ == "__main__":
    raise SystemExit(main())
