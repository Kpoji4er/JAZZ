# -*- coding: utf-8 -*-
"""UI bust crop from full-body Big — match vanilla JA3 framing (Ice/Blood).

Target: full head in frame + upper shoulders/chest. Face large but NOT clipped.
Too wide (0.42) = waist-up / tiny face.
Too tight (0.15 + face-trim) = chin/forehead cut off.

Usage:
  python bust_crop_tight.py <Big.png> [out.png] [--frac 0.28] [--size 300]
  python bust_crop_tight.py --batch <newrules2_dir>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def bust_crop_tight(
    src: Path,
    dst: Path,
    size: int = 300,
    head_frac: float = 0.28,
    top_pad_frac: float = 0.04,
) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    alpha = im.split()[-1]
    bbox = alpha.getbbox()
    if not bbox:
        im.resize((size, size), Image.Resampling.LANCZOS).save(dst)
        return
    x0, y0, x1, y1 = bbox
    bw, bh = x1 - x0, y1 - y0
    # Head + neck + upper chest (Ice/Omryn style), not waist, not face-only
    side = int(bh * head_frac)
    side = max(side, int(bw * 0.45))
    side = min(side, w, h)
    top = max(0, y0 - int(side * top_pad_frac))
    cx = (x0 + x1) // 2
    left = max(0, min(w - side, cx - side // 2))
    if top + side > h:
        top = max(0, h - side)
    crop = im.crop((left, top, left + side, top + side))
    crop.resize((size, size), Image.Resampling.LANCZOS).save(dst)


def batch_newrules2(root: Path, head_frac: float, size: int) -> int:
    n = 0
    for big in sorted(root.rglob("*_Big.png")):
        if any(p in big.parts for p in ("_raw", "_neural", "_faces", "_quality_bar")):
            continue
        out = big.with_name(big.name.replace("_Big.png", ".png"))
        bust_crop_tight(big, out, size=size, head_frac=head_frac)
        n += 1
        if n % 40 == 0:
            print(f"  {n}…", flush=True)
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?")
    ap.add_argument("output", nargs="?")
    ap.add_argument("--batch", type=Path)
    ap.add_argument(
        "--frac",
        type=float,
        default=0.28,
        help="crop side as fraction of body height (0.28≈Ice/Blood; 0.15 too tight)",
    )
    ap.add_argument("--size", type=int, default=300)
    args = ap.parse_args()

    if args.batch:
        n = batch_newrules2(args.batch, args.frac, args.size)
        print(f"OK recropped {n} busts frac={args.frac}", flush=True)
        return 0

    if not args.input:
        ap.print_help()
        return 2
    inp = Path(args.input)
    out = Path(args.output) if args.output else inp.with_name(inp.name.replace("_Big.png", ".png"))
    bust_crop_tight(inp, out, size=args.size, head_frac=args.frac)
    print(f"OK {out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
