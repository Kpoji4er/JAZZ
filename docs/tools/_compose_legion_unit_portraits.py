#!/usr/bin/env python3
"""Build polished Legion schematic unit portraits.

The layout is deterministic:

* transparent 300x300 RGBA canvas;
* one distressed red role glyph inside an outline shield;
* family mark inside the shield at the very top;
* 0..4 circular class-tier pips below the shield.

Generated glyph sheets and the original Legion PSD exports are design sources.
This script keys them to the Legion red, normalizes their bounds, and composes
all 38 runtime PNGs from catalog.json.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs/design/_legion-unit-portraits"
CATALOG = DESIGN / "catalog.json"
MASTERS = DESIGN / "masters"
SHEETS = MASTERS / "sheets"
GLYPHS = MASTERS / "glyphs"
DEFAULT_OUT = ROOT.parent / "jazz-units" / "EnemyPortraits" / "Legion"

SIZE = 300
AA = 4
RED = (216, 72, 72, 255)

FRAME_BOX = (28, 24, 234, 240)
GLYPH_BOX = (58, 76, 204, 205)
MARK_BOX = (110, 39, 152, 71)
PIP_CENTER = (131, 269)

SHEET_LAYOUTS: dict[str, tuple[int, int, list[str]]] = {
    "assault.png": (
        3,
        3,
        [
            "assault-v2-roughneck",
            "assault-v2-grenadier",
            "assault-v2-crusher",
            "assault-v2-pillager",
            "assault-v2-shocktrooper",
            "assault-v2-pyro",
            "assault-v2-punisher",
            "assault-v2-skullcrusher",
            "assault-v2-headsman",
        ],
    ),
    "front.png": (
        3,
        3,
        [
            "front-rifle",
            "front-medic",
            "front-battle-rifle",
            "front-ambush-rifle",
            "front-assault-rifle",
            "front-dmr",
            "front-sniper",
            "front-merc-rifle",
            "front-suppressed-sniper",
        ],
    ),
    "flanker-leader.png": (
        3,
        3,
        [
            "flanker-smg",
            "flanker-binoculars",
            "flanker-battle-rifle",
            "flanker-radio",
            "flanker-carbine",
            "flanker-suppressed-carbine",
            "leader-pistol",
            "leader-smg",
            "leader-command-radio",
        ],
    ),
    "gunner.png": (
        3,
        2,
        [
            "gunner-old-lmg",
            "gunner-gpmg",
            "gunner-assault-lmg",
            "gunner-heavy-mg",
            "gunner-merc-lmg",
            "gunner-ammo-belt",
        ],
    ),
    "heavy-recruit.png": (
        2,
        2,
        [
            "heavy-rpg",
            "heavy-grenade-launcher",
            "heavy-mortar",
            "recruit-bust",
        ],
    ),
}


def red_alpha(image: Image.Image) -> Image.Image:
    """Key red artwork from black/transparent source and normalize its color."""
    src = image.convert("RGBA")
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    source = src.load()
    target = out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = source[x, y]
            dominance = r - max(g, b)
            if a < 8 or r < 38 or dominance < 22:
                continue
            keyed = min(a, max(0, min(255, int((r - 28) * 1.45))))
            if keyed < 22:
                continue
            target[x, y] = (RED[0], RED[1], RED[2], keyed)
    return out


def trim(image: Image.Image, margin: int = 6) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("empty red glyph")
    left = max(0, bbox[0] - margin)
    top = max(0, bbox[1] - margin)
    right = min(image.width, bbox[2] + margin)
    bottom = min(image.height, bbox[3] + margin)
    return image.crop((left, top, right, bottom))


def remove_sheet_edge_fragments(
    image: Image.Image,
    *,
    maximum_relative_size: float = 0.35,
) -> Image.Image:
    """Drop small pieces bleeding in from neighboring sprite-sheet cells."""
    alpha = image.getchannel("A")
    components = connected_components(alpha)
    if not components:
        return image
    largest = max(len(component) for component in components)
    cleaned_alpha = alpha.copy()
    pixels = cleaned_alpha.load()
    edge = 3
    for component in components:
        xs = [point[0] for point in component]
        ys = [point[1] for point in component]
        touches_edge = (
            min(xs) <= edge
            or min(ys) <= edge
            or max(xs) >= image.width - 1 - edge
            or max(ys) >= image.height - 1 - edge
        )
        if touches_edge and len(component) < largest * maximum_relative_size:
            # Clear the antialiased fringe too; the component search ignores
            # alpha below 32, which would otherwise survive as tiny red dots.
            left = max(0, min(xs) - 4)
            top = max(0, min(ys) - 4)
            right = min(image.width, max(xs) + 5)
            bottom = min(image.height, max(ys) + 5)
            for y in range(top, bottom):
                for x in range(left, right):
                    pixels[x, y] = 0
    result = image.copy()
    result.putalpha(cleaned_alpha)
    return result


def split_sheet(path: Path, columns: int, rows: int, names: list[str]) -> None:
    sheet = Image.open(path).convert("RGBA")
    if len(names) != columns * rows:
        raise ValueError(f"{path}: layout mismatch")
    for index, name in enumerate(names):
        row, column = divmod(index, columns)
        left = round(column * sheet.width / columns)
        right = round((column + 1) * sheet.width / columns)
        top = round(row * sheet.height / rows)
        bottom = round((row + 1) * sheet.height / rows)
        cell = red_alpha(sheet.crop((left, top, right, bottom)))
        # A small median pass removes isolated antialias sparks while retaining
        # the deliberately distressed cuts in the generated stencil.
        alpha = cell.getchannel("A").filter(ImageFilter.MedianFilter(3))
        cell.putalpha(alpha)
        cell = remove_sheet_edge_fragments(cell)
        glyph = trim(cell, 10)
        # The neighboring long sniper silhouettes bleed a few detached pixels
        # into this middle cell. A second post-trim pass removes only tiny edge
        # pieces while preserving the rifle's stock and muzzle components.
        if name == "front-merc-rifle":
            glyph = remove_sheet_edge_fragments(glyph, maximum_relative_size=0.12)
            glyph.putalpha(glyph.getchannel("A").point(lambda alpha: 0 if alpha < 32 else alpha))
            cleanup = ImageDraw.Draw(glyph)
            cleanup.rectangle((0, 0, 28, 38), fill=(0, 0, 0, 0))
            cleanup.rectangle(
                (glyph.width - 20, glyph.height - 55, glyph.width, glyph.height),
                fill=(0, 0, 0, 0),
            )
            glyph = trim(glyph, 10)
        elif name == "flanker-suppressed-carbine":
            # Two low-alpha dots from the radio cell below survive the first
            # trim and become visible after runtime scaling.
            glyph.putalpha(glyph.getchannel("A").point(lambda alpha: 0 if alpha < 32 else alpha))
            glyph = trim(glyph, 10)
        glyph.save(GLYPHS / f"{name}.png")


def prepare_rank_masters() -> None:
    """Draw large, unambiguous officer rank insignia glyphs."""
    size = 512
    stroke = 30
    for name in (
        "leader-rank-sergeant",
        "leader-rank-lieutenant",
        "leader-rank-captain",
        "leader-rank-merc-captain",
    ):
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if name == "leader-rank-sergeant":
            # Three sleeve chevrons.
            for y in (130, 225, 320):
                draw.line(
                    [(105, y), (256, y + 85), (407, y)],
                    fill=RED,
                    width=stroke,
                    joint="curve",
                )
        elif name == "leader-rank-lieutenant":
            # One officer bar with flared caps.
            draw.rounded_rectangle((218, 105, 294, 407), radius=18, fill=RED)
            draw.rounded_rectangle((175, 82, 337, 137), radius=18, fill=RED)
            draw.rounded_rectangle((175, 375, 337, 430), radius=18, fill=RED)
        elif name == "leader-rank-captain":
            # Paired captain bars.
            for x in (166, 270):
                draw.rounded_rectangle((x, 105, x + 76, 407), radius=18, fill=RED)
            draw.rounded_rectangle((130, 82, 382, 137), radius=18, fill=RED)
            draw.rounded_rectangle((130, 375, 382, 430), radius=18, fill=RED)
        else:
            # Elite/mercenary command: diamond above three short bars.
            draw.polygon([(256, 65), (345, 154), (256, 243), (167, 154)], fill=RED)
            draw.polygon([(256, 108), (302, 154), (256, 200), (210, 154)], fill=(0, 0, 0, 0))
            for y in (285, 350, 415):
                draw.rounded_rectangle((145, y, 367, y + 36), radius=14, fill=RED)
        trim(image, 12).save(GLYPHS / f"{name}.png")


def prepare_glyph_masters() -> None:
    GLYPHS.mkdir(parents=True, exist_ok=True)
    for filename, (columns, rows, names) in SHEET_LAYOUTS.items():
        path = SHEETS / filename
        if not path.exists():
            raise FileNotFoundError(f"missing generated glyph sheet: {path}")
        split_sheet(path, columns, rows, names)

    for path in MASTERS.glob("assault-*.png"):
        cleaned = trim(red_alpha(Image.open(path)), 8)
        cleaned.save(GLYPHS / f"{path.stem}.png")
    prepare_rank_masters()


def connected_components(mask: Image.Image) -> list[list[tuple[int, int]]]:
    pixels = mask.load()
    width, height = mask.size
    seen: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []
    for y in range(height):
        for x in range(width):
            if pixels[x, y] < 32 or (x, y) in seen:
                continue
            component: list[tuple[int, int]] = []
            queue = deque([(x, y)])
            seen.add((x, y))
            while queue:
                px, py = queue.popleft()
                component.append((px, py))
                for ny in range(max(0, py - 1), min(height, py + 2)):
                    for nx in range(max(0, px - 1), min(width, px + 2)):
                        if (nx, ny) in seen or pixels[nx, ny] < 32:
                            continue
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            components.append(component)
    return components


def prepare_frame_master() -> Image.Image:
    source = MASTERS / "tier-Tier1.png"
    keyed = red_alpha(Image.open(source))
    # Tier1 contains the old star connected to the shield by a thin raster
    # artifact. The shield point ends at row 238 in this PSD export.
    ImageDraw.Draw(keyed).rectangle((0, 239, keyed.width, keyed.height), fill=(0, 0, 0, 0))
    alpha = keyed.getchannel("A")
    components = connected_components(alpha)
    if not components:
        raise ValueError(f"no frame component in {source}")
    shield = max(components, key=len)
    keep = Image.new("L", keyed.size, 0)
    keep_pixels = keep.load()
    source_alpha = alpha.load()
    for x, y in shield:
        keep_pixels[x, y] = source_alpha[x, y]
    frame = Image.new("RGBA", keyed.size, (0, 0, 0, 0))
    solid = Image.new("RGBA", keyed.size, RED)
    frame.paste(solid, (0, 0), keep)
    frame = trim(frame, 3)
    frame.save(MASTERS / "frame-shield.png")
    return frame


def fit(image: Image.Image, box: tuple[int, int, int, int], fill: float = 0.92) -> tuple[Image.Image, tuple[int, int]]:
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    scale = min(width * fill / image.width, height * fill / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    x = left + (width - resized.width) // 2
    y = top + (height - resized.height) // 2
    return resized, (x, y)


def star_points(cx: float, cy: float, outer: float, inner: float) -> list[tuple[float, float]]:
    result = []
    for index in range(10):
        angle = math.radians(-90 + index * 36)
        radius = outer if index % 2 == 0 else inner
        result.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    return result


def draw_family_mark(draw: ImageDraw.ImageDraw, kind: str) -> None:
    left, top, right, bottom = (value * AA for value in MARK_BOX)
    cx = (left + right) / 2
    cy = (top + bottom) / 2
    color = RED
    width = 6 * AA

    if kind == "none":
        return
    if kind == "chevron":
        # Double spearhead: aggressive forward pressure.
        for offset in (-6 * AA, 5 * AA):
            draw.line(
                [(left + 4 * AA, bottom - 6 * AA + offset), (cx, top + 6 * AA + offset), (right - 4 * AA, bottom - 6 * AA + offset)],
                fill=color,
                width=width,
                joint="curve",
            )
    elif kind == "bar":
        # A held front line.
        draw.rounded_rectangle((left + 2 * AA, cy - 5 * AA, right - 2 * AA, cy + 5 * AA), radius=3 * AA, fill=color)
    elif kind == "arrow":
        # Flanking motion.
        draw.line([(left + 4 * AA, bottom - 7 * AA), (right - 10 * AA, top + 9 * AA)], fill=color, width=width)
        draw.polygon(
            [
                (right - 17 * AA, top + 5 * AA),
                (right - 2 * AA, top + 2 * AA),
                (right - 5 * AA, top + 17 * AA),
            ],
            fill=color,
        )
    elif kind == "bars":
        # Three cartridges for the gunner family.
        for index, height in enumerate((19, 27, 19)):
            x = left + (7 + index * 12) * AA
            y = cy - height * AA / 2
            draw.rectangle((x, y + 4 * AA, x + 7 * AA, y + height * AA), fill=color)
            draw.polygon([(x, y + 4 * AA), (x + 3.5 * AA, y), (x + 7 * AA, y + 4 * AA)], fill=color)
    elif kind == "star":
        draw.polygon(star_points(cx, cy, 14 * AA, 6 * AA), fill=color)
    elif kind == "diamond":
        draw.polygon([(cx, top + 2 * AA), (right - 2 * AA, cy), (cx, bottom - 2 * AA), (left + 2 * AA, cy)], fill=color)
        draw.polygon([(cx, top + 11 * AA), (right - 11 * AA, cy), (cx, bottom - 11 * AA), (left + 11 * AA, cy)], fill=(0, 0, 0, 0))
    else:
        raise ValueError(f"unknown family mark: {kind}")


def draw_pips(draw: ImageDraw.ImageDraw, tier: int) -> None:
    if tier <= 0:
        return
    center_x, center_y = (value * AA for value in PIP_CENTER)
    spacing = 27 * AA
    radius = 8 * AA
    first = center_x - (tier - 1) * spacing / 2
    for index in range(tier):
        x = first + index * spacing
        draw.ellipse((x - radius, center_y - radius, x + radius, center_y + radius), fill=RED)


def compose_one(frame: Image.Image, glyph_name: str, mark: str, tier: int) -> Image.Image:
    canvas = Image.new("RGBA", (SIZE * AA, SIZE * AA), (0, 0, 0, 0))

    frame_large, frame_pos = fit(frame, tuple(value * AA for value in FRAME_BOX), fill=1.0)
    canvas.alpha_composite(frame_large, frame_pos)

    glyph_path = GLYPHS / f"{glyph_name}.png"
    if not glyph_path.exists():
        raise FileNotFoundError(f"missing glyph master: {glyph_path}")
    glyph = red_alpha(Image.open(glyph_path))
    glyph_large, glyph_pos = fit(glyph, tuple(value * AA for value in GLYPH_BOX), fill=0.82)
    canvas.alpha_composite(glyph_large, glyph_pos)

    draw = ImageDraw.Draw(canvas)
    draw_family_mark(draw, mark)
    draw_pips(draw, tier)

    result = canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    # Normalize every visible edge pixel after resampling. Transparent pixels
    # carry zero RGB; partially transparent pixels remain exactly Legion red.
    pixels = result.load()
    for y in range(SIZE):
        for x in range(SIZE):
            _, _, _, a = pixels[x, y]
            if a == 0:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (RED[0], RED[1], RED[2], a)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--only", nargs="*", help="Optional output filename subset")
    args = parser.parse_args()

    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    families = data["families"]
    only = set(args.only) if args.only else None

    prepare_glyph_masters()
    frame = prepare_frame_master()
    args.out.mkdir(parents=True, exist_ok=True)

    written = 0
    for unit in data["units"]:
        if only and unit["file"] not in only:
            continue
        mark = families[unit["family"]]["mark"]
        portrait = compose_one(frame, unit["glyph"], mark, int(unit["tier"]))
        output = args.out / unit["file"]
        portrait.save(output, "PNG", optimize=True)
        print(f"OK {unit['file']}: {unit['family']} / {unit['glyph']} / T{unit['tier']}")
        written += 1

    print(f"Wrote {written} portraits -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
