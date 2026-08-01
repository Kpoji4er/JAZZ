# -*- coding: utf-8 -*-
"""Cut+resize workshop merc Big raws; crop UI Portrait 300.

Expects raw Big PNGs in assets/ or MercPortraits/_wip/_raw/.
Annie UI: wider bust from Big (head_frac=0.32). Other IDs: skill frac 0.28.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow required")

ASSETS = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\assets"
)
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
RAW = JU / "MercPortraits" / "_wip" / "_raw" / "workshop"
OUT = JU / "MercPortraits"
REMBG = Path(
    r"C:\Users\SsAnd\AppData\Local\Programs\Python\Python312\Scripts\rembg.exe"
)
SCRIPTS = Path(__file__).resolve().parents[2] / (
    ".agents/skills/create-jazz-merc-portraits/scripts"
)
sys.path.insert(0, str(SCRIPTS))
from bust_crop_tight import bust_crop_tight  # noqa: E402

IDS = ["Annie", "Carol", "Hector", "Jerry", "Mildred", "Samuel"]
# Annie only was over-zoomed in dedicated UI gens.
UI_HEAD_FRAC = {
    "Annie": 0.32,
}
DEFAULT_UI_HEAD_FRAC = 0.28


def rembg_cut(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(REMBG), "i", "-m", "birefnet-general", str(src), str(dest)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("rembg FAIL", src.name, r.stderr[-400:])
        raise SystemExit(1)


def fit_square(im: Image.Image, size: int) -> Image.Image:
    # letterbox onto transparent square keeping aspect
    im = im.convert("RGBA")
    w, h = im.size
    scale = size / max(w, h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(im, ((size - nw) // 2, (size - nh) // 2), im)
    return canvas


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for mid in IDS:
        src = ASSETS / f"{mid}_Big_raw.png"
        if not src.exists():
            print("MISSING", src)
            continue
        raw_copy = RAW / f"{mid}_Big.png"
        shutil.copy2(src, raw_copy)
        cut = RAW.parent / f"{mid}_Big_cut.png"
        print("rembg", mid)
        rembg_cut(raw_copy, cut)
        big = fit_square(Image.open(cut), 2000)
        big_path = OUT / f"{mid}_Big.png"
        big.save(big_path)
        frac = UI_HEAD_FRAC.get(mid, DEFAULT_UI_HEAD_FRAC)
        por_path = OUT / f"{mid}.png"
        bust_crop_tight(big_path, por_path, size=300, head_frac=frac)
        print("OK", big_path.name, por_path.name, f"ui_frac={frac}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
