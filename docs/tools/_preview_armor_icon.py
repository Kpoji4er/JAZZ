"""Upscale ArmorIcons PNGs so the silhouette contract can be read before modelling.

Read-only for the repository: results are written to a scratch folder only.

    python docs/tools/_preview_armor_icon.py 6b3 IBAFull --output .tmp/icons
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
ICON_DIR = REPO_ROOT / "ArmorIcons"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="icon stems in ArmorIcons, without .png")
    parser.add_argument("--output", default=".tmp/icons", help="scratch folder for the upscales")
    parser.add_argument("--scale", type=int, default=5)
    parser.add_argument(
        "--flatten",
        metavar="R,G,B",
        help="composite over an opaque colour instead of keeping alpha",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = (REPO_ROOT / args.output) if not Path(args.output).is_absolute() else Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    missing = []
    for name in args.names:
        source = ICON_DIR / f"{name}.png"
        if not source.is_file():
            missing.append(name)
            continue
        image = Image.open(source).convert("RGBA")
        if args.flatten:
            rgb = tuple(int(part) for part in args.flatten.split(","))
            background = Image.new("RGBA", image.size, (*rgb, 255))
            image = Image.alpha_composite(background, image)
        scaled = image.resize(
            (image.width * args.scale, image.height * args.scale), Image.LANCZOS
        )
        target = out_dir / f"{name}_x{args.scale}.png"
        scaled.save(target)
        print(f"{name}: {image.width}x{image.height} -> {target}")

    for name in missing:
        print(f"MISSING {name}: no {ICON_DIR / (name + '.png')}", file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
