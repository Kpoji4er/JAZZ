#!/usr/bin/env python3
"""Recenter + scale dual-strip HUD action icons in Icons/Med/*.png.

Each file is 108x54 (left cool / right sand halves of 54x54). Default pad=9 →
glyph fill ≈36px (not edge-to-edge). Too-small / off-center drafts: raise fill
with lower --pad; too-big: --pad 9..12.

Usage (from jazz/):
  python docs/tools/_recenter_med_action_icons.py
  python docs/tools/_recenter_med_action_icons.py --dry-run
  python docs/tools/_recenter_med_action_icons.py --pad 9 --dir Icons/Med
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

HALF = 54
DEFAULT_PAD = 9
ALPHA_THR = 20


def content_bbox(arr: np.ndarray, thr: int = ALPHA_THR):
    ys, xs = np.where(arr[:, :, 3] > thr)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def process_half(half: np.ndarray, pad: int) -> np.ndarray:
    target = HALF - 2 * pad
    b = content_bbox(half)
    if b is None:
        return half.copy()
    x0, y0, x1, y1 = b
    crop = half[y0:y1, x0:x1]
    ch, cw = crop.shape[:2]
    scale = min(target / cw, target / ch)
    cx = (x0 + x1 - 1) / 2
    cy = (y0 + y1 - 1) / 2
    # Allow shrink or slight grow to target; prefer matching pad size.
    already_ok = (
        abs(scale - 1.0) < 0.05
        and abs(cx - HALF / 2) < 2
        and abs(cy - HALF / 2) < 2
        and max(cw, ch) <= target + 2
        and max(cw, ch) >= target - 4
    )
    if already_ok:
        return half.copy()
    nw = max(1, int(round(cw * scale)))
    nh = max(1, int(round(ch * scale)))
    resized = np.array(
        Image.fromarray(crop, "RGBA").resize((nw, nh), Image.Resampling.LANCZOS)
    )
    out = np.zeros_like(half)
    ox = (HALF - nw) // 2
    oy = (HALF - nh) // 2
    out[oy : oy + nh, ox : ox + nw] = resized
    return out


def process_file(path: Path, pad: int, dry_run: bool) -> str:
    im = Image.open(path).convert("RGBA")
    if im.size != (108, 54):
        return f"SKIP {path.name} size={im.size}"
    arr = np.array(im)
    left = process_half(arr[:, :HALF], pad)
    right = process_half(arr[:, HALF:], pad)
    out = np.concatenate([left, right], axis=1)
    lines = [path.name]
    for label, half in (("L", out[:, :HALF]), ("R", out[:, HALF:])):
        b = content_bbox(half)
        if not b:
            lines.append(f"  {label}: empty")
            continue
        x0, y0, x1, y1 = b
        cx = (x0 + x1 - 1) / 2
        cy = (y0 + y1 - 1) / 2
        lines.append(
            f"  {label}: {x1 - x0}x{y1 - y0} dx={cx - 27:+.1f} dy={cy - 27:+.1f}"
        )
    if not dry_run:
        Image.fromarray(out, "RGBA").save(path)
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dir",
        type=Path,
        default=Path("Icons/Med"),
        help="Folder of 108x54 dual-strip PNGs (default Icons/Med)",
    )
    ap.add_argument("--pad", type=int, default=DEFAULT_PAD, help="Padding per side in each 54x54 half")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]
    folder = args.dir if args.dir.is_absolute() else root / args.dir
    if not folder.is_dir():
        raise SystemExit(f"Not a directory: {folder}")

    paths = sorted(folder.glob("*.png"))
    if not paths:
        raise SystemExit(f"No PNGs in {folder}")

    for p in paths:
        print(process_file(p, args.pad, args.dry_run))
        print("---")
    mode = "dry-run" if args.dry_run else "wrote"
    print(f"{mode}: {len(paths)} file(s) in {folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
