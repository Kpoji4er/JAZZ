#!/usr/bin/env python3
"""Audit dual-strip 108x54 action-icon centering."""
from pathlib import Path
import numpy as np
from PIL import Image

HALF = 54
ROOT = Path(__file__).resolve().parents[2]


def bbox(a, thr=20):
    ys, xs = np.where(a[:, :, 3] > thr)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def audit_folder(folder: Path):
    print(f"=== {folder.relative_to(ROOT)} ===")
    warn = []
    ok = []
    for p in sorted(folder.glob("*.png")):
        im = np.array(Image.open(p).convert("RGBA"))
        if im.shape[0] != 54 or im.shape[1] != 108:
            print(f"BADSIZE {p.name}: {im.shape[1]}x{im.shape[0]}")
            warn.append(p.name)
            continue
        flags = []
        brief = []
        for label, half in (("L", im[:, :HALF]), ("R", im[:, HALF:])):
            b = bbox(half)
            if not b:
                flags.append(f"{label}=empty")
                continue
            x0, y0, x1, y1 = b
            bw, bh = x1 - x0 + 1, y1 - y0 + 1
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            dx, dy = cx - 27, cy - 27
            fill = bw * bh / (54 * 54)
            brief.append(f"{label}:{bw}x{bh} dx={dx:+.1f} dy={dy:+.1f}")
            if abs(dx) > 2.5 or abs(dy) > 2.5 or (fill < 0.28 and max(bw, bh) < 40):
                flags.append(
                    f"{label} {bw}x{bh} fill={fill:.2f} dx={dx:+.1f} dy={dy:+.1f}"
                )
        if flags:
            print(f"WARN {p.name}: {' | '.join(flags)}")
            warn.append(p.name)
        else:
            print(f"OK   {p.name:28} {'  '.join(brief)}")
            ok.append(p.name)
    print(f"-> OK={len(ok)} WARN={len(warn)}\n")
    return ok, warn


def main():
    folders = [
        ROOT / "Perks" / "SignatureAbilities",
        ROOT / "Icons" / "Med",
        ROOT / "Icons",  # FoldStock / flashlight CombatAction dual-strips at root
    ]
    # other 108x54 outside those folders
    extras = []
    scanned = {f.resolve() for f in folders if f.is_dir()}
    for base in (ROOT / "Perks", ROOT / "Icons", ROOT / "Images"):
        if not base.exists():
            continue
        for p in base.rglob("*.png"):
            parent = p.parent.resolve()
            if parent in scanned:
                continue
            if "references" in p.parts:
                continue
            try:
                if Image.open(p).size == (108, 54):
                    extras.append(p)
            except OSError:
                pass
    if extras:
        print("EXTRA 108x54 (not in audited folders):")
        for p in extras:
            print(" ", p.relative_to(ROOT))
        print()

    all_warn = []
    seen = set()
    for f in folders:
        if not f.is_dir():
            print(f"MISSING {f}")
            continue
        key = f.resolve()
        if key in seen:
            continue
        seen.add(key)
        # Icons root: only *.png directly in folder (not Med/)
        if f.name == "Icons" and f == ROOT / "Icons":
            print(f"=== {f.relative_to(ROOT)} (root dual-strips only) ===")
            warn = []
            ok = []
            for p in sorted(f.glob("*.png")):
                im = np.array(Image.open(p).convert("RGBA"))
                if im.shape[0] != 54 or im.shape[1] != 108:
                    continue
                flags = []
                brief = []
                for label, half in (("L", im[:, :HALF]), ("R", im[:, HALF:])):
                    b = bbox(half)
                    if not b:
                        flags.append(f"{label}=empty")
                        continue
                    x0, y0, x1, y1 = b
                    bw, bh = x1 - x0 + 1, y1 - y0 + 1
                    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                    dx, dy = cx - 27, cy - 27
                    fill = bw * bh / (54 * 54)
                    brief.append(f"{label}:{bw}x{bh} dx={dx:+.1f} dy={dy:+.1f}")
                    if abs(dx) > 2.5 or abs(dy) > 2.5 or (fill < 0.28 and max(bw, bh) < 40):
                        flags.append(
                            f"{label} {bw}x{bh} fill={fill:.2f} dx={dx:+.1f} dy={dy:+.1f}"
                        )
                if flags:
                    print(f"WARN {p.name}: {' | '.join(flags)}")
                    warn.append(p.name)
                else:
                    print(f"OK   {p.name:28} {'  '.join(brief)}")
                    ok.append(p.name)
            print(f"-> OK={len(ok)} WARN={len(warn)}\n")
            all_warn.extend(warn)
            continue
        _, w = audit_folder(f)
        all_warn.extend(w)
    print("TOTAL WARN:", len(all_warn), all_warn)


if __name__ == "__main__":
    main()
