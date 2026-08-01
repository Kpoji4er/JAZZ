"""QA for style-B Icon drafts (Anaconda-like soft silhouette).

Exit 0 = all pass. Exit 1 = failures listed (regen those).

Usage:
  python docs/tools/_qa_icon_style_b.py
  python docs/tools/_qa_icon_style_b.py path/to/preview_JAZZ_Foo.png
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "Icons" / "Upgrades" / "_review" / "icon_style_B"
SIZE = 100
MIN_OPAQUE = 900
MAX_OPAQUE = 7800
# soft fringe: some pixels with partial alpha near edge
MIN_SOFT_EDGE = 40
# light rembg-like fringe on outer edge (bad)
MAX_BRIGHT_EDGE_LUM = 120


def qa_one(path: Path) -> list[str]:
    fails: list[str] = []
    im = Image.open(path).convert("RGBA")
    if im.size != (SIZE, SIZE):
        fails.append(f"size {im.size} != {SIZE}x{SIZE}")
    px = list(im.getdata())
    w, h = im.size
    opaque = sum(1 for p in px if p[3] > 200)
    soft = sum(1 for p in px if 12 <= p[3] < 200)
    if opaque < MIN_OPAQUE:
        fails.append(f"too empty opaque={opaque} < {MIN_OPAQUE}")
    if opaque > MAX_OPAQUE:
        fails.append(f"too filled opaque={opaque} > {MAX_OPAQUE} (cropped tight?)")
    if soft < MIN_SOFT_EDGE:
        fails.append(f"no soft AA fringe soft={soft} < {MIN_SOFT_EDGE}")
    # corner must be transparent
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if im.getpixel(xy)[3] > 8:
            fails.append(f"corner {xy} not transparent")
            break
    # bright edge fringe (chewed rembg / light halo)
    bright_edge = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            if a < 40 or a > 250:
                continue
            # near transparent neighbor?
            edge = False
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < w and 0 <= ny < h) or im.getpixel((nx, ny))[3] < 8:
                        edge = True
                        break
                if edge:
                    break
            if edge and (r + g + b) // 3 >= MAX_BRIGHT_EDGE_LUM:
                bright_edge += 1
    if bright_edge > 80:
        fails.append(f"bright edge fringe px={bright_edge} (regen/heal)")
    return fails


def main() -> int:
    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        paths = sorted(REVIEW.glob("preview_*.png"))
    if not paths:
        print("no preview_*.png found")
        return 1
    bad = 0
    for p in paths:
        fails = qa_one(p)
        if fails:
            bad += 1
            print(f"FAIL {p.name}")
            for f in fails:
                print(f"  - {f}")
        else:
            print(f"PASS {p.name}")
    print(f"\n{len(paths) - bad}/{len(paths)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
