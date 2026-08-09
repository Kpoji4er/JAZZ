# -*- coding: utf-8 -*-
"""Lock ammo drafts from Cursor assets → Ammopics/_gen + soft outline; purge assets."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from _lock_ammo_icon_silhouette import apply_soft_outline, lock_to_silhouette  # noqa: E402

ASSETS = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\assets"
)
OUT = ROOT / "Ammopics" / "_gen"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--silhouette", required=True)
    ap.add_argument("names", nargs="+", help="gen_*.png basenames or paths")
    ap.add_argument("--soft-outline", type=float, default=0.45)
    ap.add_argument("--choke", type=int, default=0)
    ap.add_argument("--rim-plate", type=int, default=0)
    ap.add_argument("--fit", default="contain", choices=("contain", "cover"))
    ap.add_argument("--alpha-from", default="draft", choices=("sil", "draft"))
    ap.add_argument(
        "--hard-alpha",
        action="store_true",
        help="Binary alpha (usually worse on black UI; vanilla uses soft sil alpha).",
    )
    ap.add_argument(
        "--key",
        default="auto",
        choices=("auto", "magenta", "black", "alpha"),
        help="Draft background cut (prefer magenta for new gens).",
    )
    ap.add_argument("--purge-assets", action="store_true")
    args = ap.parse_args()
    sil = Path(args.silhouette)
    if not sil.is_absolute():
        sil = ROOT / sil
    OUT.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        src = Path(name)
        if not src.is_absolute():
            src = ASSETS / src.name
        if not src.exists():
            print(f"MISSING {src}")
            continue
        dst = OUT / src.name
        # Soft sil alpha matches vanilla AA edge; hard binary looks jagged on black UI.
        lock_to_silhouette(
            src,
            dst,
            sil_path=sil,
            fit=args.fit,
            thr=28,
            structure=0.0,
            plate_first=False,
            choke=args.choke,
            rim_plate=args.rim_plate,
            hard_alpha=args.hard_alpha,
            alpha_from=args.alpha_from,
            soft_outline=0.0,
            key=args.key,
        )
        arr = np.array(Image.open(dst).convert("RGBA"))
        arr = apply_soft_outline(arr, strength=args.soft_outline, width=1, outer=False)
        Image.fromarray(arr, "RGBA").save(dst)
        print(
            f"outlined {dst.name} (key={args.key} alpha={args.alpha_from} "
            f"choke={args.choke} rim={args.rim_plate})"
        )
        if args.purge_assets:
            src.unlink(missing_ok=True)
    # do NOT wipe unrelated drafts still waiting for lock


if __name__ == "__main__":
    main()
