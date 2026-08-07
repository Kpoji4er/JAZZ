# -*- coding: utf-8 -*-
"""Cut and resize JA12 face-fix portrait candidates.

Reads generated opaque PNGs from Cursor assets, preserves them under `_raw/`,
and writes review-ready 2000x2000 Big plus 300x300 bust RGBA candidates.
Runtime art is replaced only with explicit `--apply`.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

ASSETS = Path(
    r"C:\Users\SsAnd\.cursor\projects"
    r"\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\assets"
)
JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
OUT = UNITS / "MercPortraits" / "_wip" / "ja12-facefix"
RAW = OUT / "_raw"
REMBG = Path(sys.executable).with_name("Scripts") / "rembg.exe"
FACE_REFS = JAZZ / "docs" / "design" / "mercs-ja12"

JOBS = {
    "Spider": "ja12-facefix-Spider-raw.png",
    "Highball": "ja12-facefix-Highball-raw.png",
    "Flo": "ja12-facefix-Flo-raw.png",
    "Grace": "ja12-facefix-Grace-raw.png",
    "Rothman": "ja12-facefix-Rothman-raw.png",
    "Vilde": "ja12-facefix-Vilde-v2-raw.png",
    "Horg": "ja12-facefix-Horg-v2-raw.png",
    "Blade": "ja12-facefix-Blade-raw.png",
}


def rembg_cut(src: Path, dest: Path) -> None:
    result = subprocess.run(
        [str(REMBG), "i", "-m", "birefnet-general", str(src), str(dest)],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(f"rembg failed for {src.name}: {(result.stderr or '')[-500:]}")


def resize_square(image: Image.Image, size: int) -> Image.Image:
    return image.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)


def bust_crop(big: Image.Image, size: int = 300, head_frac: float = 0.28) -> Image.Image:
    image = big.convert("RGBA")
    width, height = image.size
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        return image.resize((size, size), Image.Resampling.LANCZOS)
    x0, y0, x1, y1 = bbox
    body_width, body_height = x1 - x0, y1 - y0
    side = max(round(body_height * head_frac), round(body_width * 0.45))
    side = min(side, width, height)
    center_x = (x0 + x1) // 2
    left = max(0, min(width - side, center_x - side // 2))
    top = max(0, y0 - round(side * 0.04))
    return image.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.Resampling.LANCZOS
    )


def corner_alpha(image: Image.Image) -> int:
    rgba = image.convert("RGBA")
    corners = (
        rgba.getpixel((0, 0)),
        rgba.getpixel((rgba.width - 1, 0)),
        rgba.getpixel((0, rgba.height - 1)),
        rgba.getpixel((rgba.width - 1, rgba.height - 1)),
    )
    return max(pixel[3] for pixel in corners)


def make_contact_sheet() -> None:
    cell = 300
    label_width = 120
    header_height = 34
    gap = 10
    row_height = cell + gap
    sheet = Image.new(
        "RGB",
        (label_width + 3 * (cell + gap), header_height + len(JOBS) * row_height),
        (35, 33, 29),
    )
    draw = ImageDraw.Draw(sheet)
    for index, title in enumerate(("JA2", "Current", "Candidate")):
        draw.text((label_width + index * (cell + gap) + 8, 9), title, fill="white")

    for row, merc in enumerate(JOBS):
        y = header_height + row * row_height
        draw.text((8, y + 8), merc, fill="white")
        ref_candidates = list(FACE_REFS.glob(f"{merc.lower()}.ja2-face.*"))
        paths = [
            ref_candidates[0] if ref_candidates else None,
            UNITS / "MercPortraits" / f"{merc}.png",
            OUT / f"{merc}.png",
        ]
        for column, path in enumerate(paths):
            tile = Image.new("RGBA", (cell, cell), (80, 70, 51, 255))
            if path and path.exists():
                image = Image.open(path).convert("RGBA")
                image.thumbnail((cell, cell), Image.Resampling.NEAREST if column == 0 else Image.Resampling.LANCZOS)
                tile.alpha_composite(image, ((cell - image.width) // 2, (cell - image.height) // 2))
            sheet.paste(tile.convert("RGB"), (label_width + column * (cell + gap), y))
    sheet.save(OUT / "contact-sheet.png")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--crop-only",
        action="store_true",
        help="Reframe existing Big candidates without rerunning BiRefNet",
    )
    parser.add_argument("--apply", action="store_true", help="Copy candidates into runtime art")
    args = parser.parse_args()

    if not args.crop_only and not REMBG.exists():
        raise SystemExit(f"Missing rembg: {REMBG}")
    RAW.mkdir(parents=True, exist_ok=True)

    missing = (
        [name for name in JOBS.values() if not (ASSETS / name).exists()]
        if not args.crop_only
        else [f"{merc}_Big.png" for merc in JOBS if not (OUT / f"{merc}_Big.png").exists()]
    )
    if missing:
        raise SystemExit("Missing portrait inputs: " + ", ".join(missing))

    for merc, source_name in JOBS.items():
        big_path = OUT / f"{merc}_Big.png"
        if args.crop_only:
            big = Image.open(big_path).convert("RGBA")
            print("crop", merc)
        else:
            raw = RAW / f"{merc}_Big_raw.png"
            shutil.copy2(ASSETS / source_name, raw)
            cut = RAW / f"{merc}_Big_cut.png"
            print("cut", merc)
            rembg_cut(raw, cut)
            big = resize_square(Image.open(cut), 2000)
            big.save(big_path)
        portrait = bust_crop(big)
        portrait_path = OUT / f"{merc}.png"
        portrait.save(portrait_path)
        print(
            f"  Big={big.size} cornerA={corner_alpha(big)} "
            f"Portrait={portrait.size} cornerA={corner_alpha(portrait)}"
        )
    make_contact_sheet()
    print("contact-sheet.png")
    if args.apply:
        runtime = UNITS / "MercPortraits"
        for merc in JOBS:
            shutil.copy2(OUT / f"{merc}.png", runtime / f"{merc}.png")
            shutil.copy2(OUT / f"{merc}_Big.png", runtime / f"{merc}_Big.png")
        print(f"applied={len(JOBS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
