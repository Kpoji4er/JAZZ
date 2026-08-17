#!/usr/bin/env python3
"""Generate Trauma*Stabilized / Trauma*Healing 40x40 status icons from base Trauma{Zone}{Tier}.png.

For each existing Icons/StatusEffects/Trauma{Zone}{Tier}.png (Arms/Legs/Ribs/Head/Burn x
Light/Medium/Heavy) writes two variants with a small top-right corner badge:
  - Trauma{Zone}{Tier}Stabilized.png -- sand/buff badge (cross / bandage mark)
  - Trauma{Zone}{Tier}Healing.png -- cyan medical badge (clock / plus)

Requires Pillow. Idempotent overwrite of outputs only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("ERROR: Pillow required (pip install Pillow)", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
ICON_DIR = ROOT / "Icons" / "StatusEffects"

BASE_RE = re.compile(
    r"^Trauma(Arms|Legs|Ribs|Head|Burn)(Light|Medium|Heavy)\.png$"
)

SAND_FILL = (198, 178, 118, 255)
SAND_EDGE = (92, 72, 40, 230)
SAND_MARK = (72, 52, 28, 255)

CYAN_FILL = (72, 196, 210, 255)
CYAN_EDGE = (24, 72, 88, 230)
CYAN_MARK = (18, 48, 58, 255)

BADGE_SIZE = 12
BADGE_MARGIN = 1


def _draw_badge_disk(draw, ox, oy, fill, edge):
    x1, y1 = ox + BADGE_SIZE - 1, oy + BADGE_SIZE - 1
    draw.ellipse([ox, oy, x1, y1], fill=fill, outline=edge)


def _draw_cross(draw, ox, oy, color, thickness=2):
    cx = ox + BADGE_SIZE // 2
    cy = oy + BADGE_SIZE // 2
    arm = 3
    draw.rectangle(
        [cx - arm, cy - thickness // 2, cx + arm, cy + (thickness - 1) // 2],
        fill=color,
    )
    draw.rectangle(
        [cx - thickness // 2, cy - arm, cx + (thickness - 1) // 2, cy + arm],
        fill=color,
    )


def _draw_bandage(draw, ox, oy, color):
    _draw_cross(draw, ox, oy, color, thickness=2)
    x0, y0 = ox + 3, oy + 3
    draw.line([(x0, y0 + 5), (x0 + 5, y0)], fill=color, width=1)


def _draw_clock(draw, ox, oy, color):
    cx = ox + BADGE_SIZE // 2
    cy = oy + BADGE_SIZE // 2
    draw.line([(cx, cy), (cx, cy - 3)], fill=color, width=1)
    draw.line([(cx, cy), (cx + 3, cy)], fill=color, width=1)
    draw.point((cx, cy), fill=color)


def make_variant(base, kind):
    out = base.convert("RGBA").copy()
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    ox = out.size[0] - BADGE_SIZE - BADGE_MARGIN
    oy = BADGE_MARGIN
    if kind == "Stabilized":
        _draw_badge_disk(draw, ox, oy, SAND_FILL, SAND_EDGE)
        _draw_bandage(draw, ox, oy, SAND_MARK)
    elif kind == "Healing":
        _draw_badge_disk(draw, ox, oy, CYAN_FILL, CYAN_EDGE)
        _draw_clock(draw, ox, oy, CYAN_MARK)
    else:
        raise ValueError(kind)
    return Image.alpha_composite(out, overlay)


def main():
    if not ICON_DIR.is_dir():
        print(f"ERROR: missing {ICON_DIR}", file=sys.stderr)
        return 1
    bases = sorted(p for p in ICON_DIR.glob("Trauma*.png") if BASE_RE.match(p.name))
    if not bases:
        print(f"ERROR: no Trauma Zone Tier png under {ICON_DIR}", file=sys.stderr)
        return 1
    created = []
    errors = []
    for src in bases:
        try:
            base = Image.open(src)
        except OSError as exc:
            errors.append(f"{src.name}: open failed: {exc}")
            continue
        stem = src.stem
        for kind in ("Stabilized", "Healing"):
            dest = ICON_DIR / f"{stem}{kind}.png"
            try:
                variant = make_variant(base, kind)
                variant.save(dest, format="PNG")
                created.append(str(dest.relative_to(ROOT)).replace("\\", "/"))
            except Exception as exc:
                errors.append(f"{dest.name}: {exc}")
    print(f"bases={len(bases)} created={len(created)} errors={len(errors)}")
    for path in created:
        print(f"  OK {path}")
    for err in errors:
        print(f"  ERR {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
