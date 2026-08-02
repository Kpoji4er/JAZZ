"""Seed Icons/Hud/references/*.png from vanilla ui/Icons/Hud/*.dds (BC7 via imagecodecs).

Usage (from jazz repo root):
  python .agents/skills/create-jazz-action-icons/scripts/seed-hud-references.py
  python .agents/skills/create-jazz-action-icons/scripts/seed-hud-references.py --src "D:/path/to/ui/Icons/Hud"

Requires: pip install imagecodecs pillow numpy
"""
from __future__ import annotations

import argparse
from pathlib import Path

import imagecodecs
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[4]
DEFAULT_DST = REPO / "Icons" / "Hud" / "references"
SKIP = {"placeholder", "placeholder_2", "ammo_infinite"}


def decode_dds(path: Path) -> Image.Image:
    arr = imagecodecs.dds_decode(path.read_bytes())
    if not isinstance(arr, np.ndarray) or arr.ndim != 3:
        raise TypeError(f"unexpected decode for {path}")
    if arr.shape[2] == 3:
        arr = np.dstack([arr, np.full(arr.shape[:2], 255, dtype=np.uint8)])
    return Image.fromarray(arr, mode="RGBA")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--src",
        type=Path,
        default=Path(r"D:\jawiki\hpk-v0.3.12-x86_64-pc-windows-msvc\ui\Icons\Hud"),
        help="Vanilla ui/Icons/Hud directory with .dds",
    )
    ap.add_argument("--dst", type=Path, default=DEFAULT_DST)
    args = ap.parse_args()
    if not args.src.is_dir():
        raise SystemExit(f"src not found: {args.src}")
    args.dst.mkdir(parents=True, exist_ok=True)
    copied = []
    sizes = set()
    for dds in sorted(args.src.glob("*.dds")):
        if dds.stem in SKIP:
            continue
        img = decode_dds(dds)
        sizes.add(img.size)
        # Normalize weird trailing spaces in vanilla names
        name = dds.stem.strip()
        out = args.dst / f"{name}.png"
        img.save(out, format="PNG")
        copied.append(name)
    print(f"copied={len(copied)} sizes={sorted(sizes)} -> {args.dst}")


if __name__ == "__main__":
    main()
