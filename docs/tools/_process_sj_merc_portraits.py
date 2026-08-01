# -*- coding: utf-8 -*-
"""Cut+resize Shady Job Khalif merc portraits (Benny/Simon).

Expects raw PNGs in Cursor assets/ (or copies under MercPortraits/_wip/_raw/sj/).
Writes MercPortraits/<Id>.png (300) + <Id>_Big.png (2000).

Usage (jazz/):
  python docs/tools/_process_sj_merc_portraits.py
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image
except ImportError as e:
    raise SystemExit("Pillow required") from e

ASSETS = Path(
    r"C:\Users\SsAnd\.cursor\projects"
    r"\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\assets"
)
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
RAW = JU / "MercPortraits" / "_wip" / "_raw" / "sj"
OUT = JU / "MercPortraits"
REMBG = Path(
    r"C:\Users\SsAnd\AppData\Local\Programs\Python\Python312\Scripts\rembg.exe"
)

# portrait_id → (big_raw_name, bust_raw_name or None → crop from Big)
JOBS = {
    "Benny": ("Benny_Big_raw.png", "Benny_bust_raw.png"),
    "Simon": ("Simon_Big_raw_v2.png", "Simon_bust_raw.png"),
}


def rembg_cut(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(REMBG), "i", "-m", "birefnet-general", str(src), str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("rembg FAIL", src.name, (r.stderr or "")[-400:])
        raise SystemExit(1)


def fit_square(im: Image.Image, size: int) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    scale = size / max(w, h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(im, ((size - nw) // 2, (size - nh) // 2), im)
    return canvas


def tight_bust(big: Image.Image, size: int = 300, frac: float = 0.28) -> Image.Image:
    big = big.convert("RGBA")
    w, h = big.size
    side = int(h * frac * 2.2)
    side = min(side, w, h)
    left = (w - side) // 2
    top = int(h * 0.02)
    if top + side > h:
        top = h - side
    crop = big.crop((left, top, left + side, top + side))
    return crop.resize((size, size), Image.Resampling.LANCZOS)


def corner_alpha(im: Image.Image) -> int:
    px = im.convert("RGBA").load()
    w, h = im.size
    return max(px[0, 0][3], px[w - 1, 0][3], px[0, h - 1][3], px[w - 1, h - 1][3])


def main() -> int:
    if not REMBG.exists():
        print("MISSING rembg", REMBG)
        return 1
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    for mid, (big_name, bust_name) in JOBS.items():
        src_big = ASSETS / big_name
        if not src_big.exists():
            alt = RAW / big_name
            if alt.exists():
                src_big = alt
            else:
                print("MISSING", src_big)
                continue
        raw_copy = RAW / f"{mid}_Big.png"
        shutil.copy2(src_big, raw_copy)
        cut_big = RAW.parent / f"{mid}_Big_cut.png"
        print("rembg Big", mid)
        rembg_cut(raw_copy, cut_big)
        big = fit_square(Image.open(cut_big), 2000)
        big_path = OUT / f"{mid}_Big.png"
        big.save(big_path)
        print("  Big", big_path.name, big.size, "cornerA", corner_alpha(big))

        bust_src = ASSETS / bust_name if bust_name else None
        if bust_src and bust_src.exists():
            raw_bust = RAW / f"{mid}_bust.png"
            shutil.copy2(bust_src, raw_bust)
            cut_bust = RAW.parent / f"{mid}_bust_cut.png"
            print("rembg bust", mid)
            rembg_cut(raw_bust, cut_bust)
            portrait = fit_square(Image.open(cut_bust), 300)
        else:
            print("bust crop from Big", mid)
            portrait = tight_bust(big, 300, 0.28)
        por_path = OUT / f"{mid}.png"
        portrait.save(por_path)
        print("  Portrait", por_path.name, portrait.size, "cornerA", corner_alpha(portrait))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
