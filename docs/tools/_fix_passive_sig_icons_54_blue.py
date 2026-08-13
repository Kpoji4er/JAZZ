# -*- coding: utf-8 -*-
"""Fix Passive signature icons that are still 108x54 dual (SetColumns=1 artifact).

Rebuilds Jazz_Perk_Spider (+ siblings if dual) as 54x54 cool blue.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SIG = ROOT / "Perks" / "SignatureAbilities"
META = ROOT / "metadata.lua"
BUILD = ROOT / "docs" / "tools" / "_build_passive_signature_icon_54.py"

PASSIVES = [
    "Jazz_Perk_Spider",
    "Jazz_Perk_Lynx",
    "Jazz_Perk_Buzz",
    "Jazz_Perk_Colby",
]

COOL = np.array([0x60, 0x9B, 0xB8], dtype=np.float32)
OUT = 54
GLYPH_MAX = 42


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


def fit_cool(glyph: np.ndarray) -> Image.Image:
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
    out[y0 : y0 + nh, x0 : x0 + nw, :3] = COOL
    out[y0 : y0 + nh, x0 : x0 + nw, 3:4] = alpha * 255.0
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def rebuild_from_sig_dual(stem: str) -> bool:
    path = SIG / f"{stem}.png"
    if not path.exists():
        return False
    src = np.array(Image.open(path).convert("RGBA"))
    h, w = src.shape[0], src.shape[1]
    if w < 100 or h > 60:
        # already single or weird — still force cool 54 if not 54x54
        if (w, h) == (OUT, OUT):
            # recolor existing to cool
            keyed = key_black(src)
            img = fit_cool(extract(keyed))
            img.save(path)
            print(f"recolored {stem} 54x54 cool")
            return True
        return False
    half = src[:, : w // 2]
    keyed = key_black(half)
    img = fit_cool(extract(keyed))
    img.save(path)
    print(f"wrote {stem} from LEFT dual -> 54x54 cool")
    return True


def bump_meta() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    ver = int(m.group(1)) + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    bullet = (
        "- UNITS-006: Spider Jazz_Perk_Spider Passive icon 54x54 cool blue "
        "(was 108 dual → SetColumns=1 artifact) [no new game]\\n"
    )
    m2 = re.search(r"'last_changes',\s*\"", text)
    i = m2.end()
    if "Jazz_Perk_Spider Passive icon 54x54" not in text[i : i + 220]:
        text = text[:i] + bullet + text[i:]
    META.write_text(text, encoding="utf-8")
    print(f"metadata version -> {ver}")


def main() -> None:
    for stem in PASSIVES:
        p = SIG / f"{stem}.png"
        if not p.exists():
            print(f"skip missing {stem}")
            continue
        im = Image.open(p)
        print(f"before {stem} {im.size}")
        rebuild_from_sig_dual(stem)
        print(f"after  {stem} {Image.open(p).size}")

    bump_meta()
    readme = ROOT / "docs/tools/README.md"
    entry = (
        "| `_fix_passive_sig_icons_54_blue.py` | Rebuild Passive `Jazz_Perk_*` Signature "
        "icons to 54×54 cool blue (fix 108 dual SetColumns=1 squash). |\n"
    )
    rt = readme.read_text(encoding="utf-8")
    if "_fix_passive_sig_icons_54_blue.py" not in rt:
        if "| `_build_passive_signature_icon_54.py`" in rt:
            rt = rt.replace(
                "| `_build_passive_signature_icon_54.py`",
                entry + "| `_build_passive_signature_icon_54.py`",
            )
        else:
            rt += "\n" + entry
        readme.write_text(rt, encoding="utf-8")


if __name__ == "__main__":
    main()
