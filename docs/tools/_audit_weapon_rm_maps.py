"""Compare packed roughness/metallic maps of a new weapon against accepted ones.

    python docs/tools/_audit_weapon_rm_maps.py <dir-with-*_RM.tga> [...]

JAZZ packs roughness in R and metallic in B. A physically sane metallic map is
almost binary: bare metal near 1, polymer and wood near 0. Large mid-range
areas wash the base colour out under the engine's inventory lighting, which is
how the first AK-103 import ended up looking like grey plastic.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HEADER = f"{'file':32} {'rough':>6} {'metal':>6} {'<0.12':>8} {'mid':>7} {'>0.87':>8}"


def row(path):
    data = np.asarray(Image.open(path).convert("RGB")).astype(float)
    rough, metal = data[..., 0], data[..., 2]
    low = (metal < 32).mean() * 100
    high = (metal > 223).mean() * 100
    return (
        f"{path.name:32} {rough.mean() / 255:6.2f} {metal.mean() / 255:6.2f} "
        f"{low:7.1f}% {100 - low - high:6.1f}% {high:7.1f}%"
    )


def main(paths):
    print(HEADER)
    for folder in paths:
        files = sorted(Path(folder).glob("*_RM.tga"))
        if not files:
            print(f"  (no *_RM.tga in {folder})")
            continue
        print(f"-- {folder}")
        for path in files:
            print(row(path))


if __name__ == "__main__":
    main(sys.argv[1:])
