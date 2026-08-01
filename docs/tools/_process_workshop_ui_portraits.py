# -*- coding: utf-8 -*-
"""Workshop UI Portrait 300 processing.

Only Annie needed a wider Big→bust crop (over-zoom fix vs Grom/Blood).
Other workshop IDs keep their dedicated UI cutouts (letterbox full-bleed).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

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
# Annie only: UI raw was extreme face-fill; reframe from Big.
WIDER_FROM_BIG = {"Annie"}
ANNIE_HEAD_FRAC = 0.32


def letterbox_ui(im: Image.Image, size: int = 300) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
    return canvas.resize((size, size), Image.Resampling.LANCZOS)


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    for mid in IDS:
        out = OUT / f"{mid}.png"
        if mid in WIDER_FROM_BIG:
            big = OUT / f"{mid}_Big.png"
            if not big.exists():
                print("MISSING Big for wider crop", mid)
                continue
            bust_crop_tight(big, out, size=300, head_frac=ANNIE_HEAD_FRAC)
            print("OK", out.name, f"from Big frac={ANNIE_HEAD_FRAC}")
            continue

        src = ASSETS / f"{mid}_UI_raw.png"
        if not src.exists():
            print("MISSING", src)
            continue
        raw = RAW / f"{mid}_UI.png"
        shutil.copy2(src, raw)
        cut = RAW.parent / f"{mid}_UI_cut.png"
        r = subprocess.run(
            [str(REMBG), "i", "-m", "birefnet-general", str(raw), str(cut)],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print("FAIL", mid, r.stderr[-300:])
            continue
        letterbox_ui(Image.open(cut), 300).save(out)
        print("OK", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
