#!/usr/bin/env python3
"""Static and visual QA for Legion schematic unit portraits."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from _compose_legion_unit_portraits import (
    CATALOG,
    DEFAULT_OUT,
    DESIGN,
    GLYPH_BOX,
    MARK_BOX,
    RED,
    SIZE,
)


PREVIEW = DESIGN / "preview-sheet.png"
STACK_PREVIEW = DESIGN / "preview-stack.png"
REPORT = DESIGN / "qa-report.md"


def alpha_components(image: Image.Image, threshold: int = 72, minimum: int = 16) -> list[list[tuple[int, int]]]:
    alpha = image.getchannel("A")
    pixels = alpha.load()
    width, height = alpha.size
    seen: set[tuple[int, int]] = set()
    result: list[list[tuple[int, int]]] = []
    for y in range(height):
        for x in range(width):
            if pixels[x, y] < threshold or (x, y) in seen:
                continue
            component: list[tuple[int, int]] = []
            queue = deque([(x, y)])
            seen.add((x, y))
            while queue:
                px, py = queue.popleft()
                component.append((px, py))
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height:
                        continue
                    if (nx, ny) in seen or pixels[nx, ny] < threshold:
                        continue
                    seen.add((nx, ny))
                    queue.append((nx, ny))
            if len(component) >= minimum:
                result.append(component)
    return result


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def checker(size: tuple[int, int], cell: int = 8) -> Image.Image:
    image = Image.new("RGBA", size, (42, 46, 55, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            color = (51, 56, 67, 255) if (x // cell + y // cell) % 2 else (67, 72, 84, 255)
            draw.rectangle((x, y, min(x + cell, size[0]), min(y + cell, size[1])), fill=color)
    return image


def pixels(image: Image.Image):
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()


def make_preview(units: list[dict], directory: Path) -> None:
    columns = 8
    cell_w = 150
    cell_h = 148
    header_h = 38
    rows = (len(units) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, header_h + rows * cell_h), (23, 27, 35, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((14, 9), "LEGION UNIT PORTRAITS — 100 px GAME-SCALE QA", font=font(17, True), fill=(225, 225, 220, 255))

    for index, unit in enumerate(units):
        row, column = divmod(index, columns)
        x = column * cell_w
        y = header_h + row * cell_h
        tile = checker((cell_w - 8, 108), 8)
        sheet.alpha_composite(tile, (x + 4, y + 3))
        portrait = Image.open(directory / unit["file"]).convert("RGBA").resize((100, 100), Image.Resampling.LANCZOS)
        sheet.alpha_composite(portrait, (x + 25, y + 7))
        label = Path(unit["file"]).stem
        draw.text((x + 6, y + 115), label[:21], font=font(11, True), fill=(230, 230, 226, 255))
        draw.text(
            (x + 6, y + 131),
            f"{unit['family']}  T{unit['tier']}",
            font=font(10),
            fill=(164, 170, 182, 255),
        )
    sheet.convert("RGB").save(PREVIEW, quality=94)


def make_stack_preview(units: list[dict], directory: Path) -> None:
    # JA3 draws the xN stack counter over the upper-left of a portrait; the
    # family mark at the shield's top-center must remain visible.
    selected_names = [
        "Roughneck.png",
        "Bonemaker.png",
        "Scout.png",
        "GMPG.png",
        "Captain.png",
        "Mortarman.png",
    ]
    selected = [next(unit for unit in units if unit["file"] == name) for name in selected_names]
    tile_w, tile_h = 132, 126
    canvas = Image.new("RGBA", (len(selected) * tile_w + 20, 168), (29, 34, 45, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((10, 8), "xN overlay / family-mark visibility", font=font(15, True), fill=(225, 225, 220, 255))
    for index, unit in enumerate(selected):
        x = 10 + index * tile_w
        y = 35
        draw.rectangle((x, y, x + 116, y + 112), fill=(37, 43, 56, 255))
        portrait = Image.open(directory / unit["file"]).convert("RGBA").resize((108, 108), Image.Resampling.LANCZOS)
        canvas.alpha_composite(portrait, (x + 4, y + 2))
        draw.rectangle((x, y, x + 36, y + 30), fill=(176, 55, 71, 255))
        draw.text((x + 5, y + 5), "x3", font=font(15, True), fill=(240, 225, 218, 255))
        draw.text((x + 2, y + 114), Path(unit["file"]).stem[:16], font=font(10), fill=(190, 194, 204, 255))
    canvas.convert("RGB").save(STACK_PREVIEW, quality=94)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    data = json.loads(args.catalog.read_text(encoding="utf-8"))
    units = data["units"]
    expected = {unit["file"] for unit in units}
    actual = {path.name for path in args.dir.glob("*.png")}
    problems: list[str] = []
    metrics: list[str] = []
    glyph_masks: dict[tuple[str, int], list[tuple[str, bytes]]] = defaultdict(list)
    recruit_unit = next(unit for unit in units if unit["family"] == "recruit")
    recruit_image = Image.open(args.dir / recruit_unit["file"]).convert("RGBA")
    mark_baseline = sum(1 for *_, a in pixels(recruit_image.crop(MARK_BOX)) if a > 64)

    if len(units) != 38:
        problems.append(f"catalog count {len(units)} != 38")
    missing = sorted(expected - actual)
    if missing:
        problems.append(f"missing PNG: {', '.join(missing)}")

    for unit in units:
        path = args.dir / unit["file"]
        if not path.exists():
            continue
        image = Image.open(path).convert("RGBA")
        if image.size != (SIZE, SIZE):
            problems.append(f"{path.name}: size {image.size}, expected 300x300")
            continue
        if Image.open(path).mode != "RGBA":
            problems.append(f"{path.name}: mode {Image.open(path).mode}, expected RGBA")

        corners = [image.getpixel(point)[3] for point in ((0, 0), (299, 0), (0, 299), (299, 299))]
        if any(corners):
            problems.append(f"{path.name}: non-transparent corner alpha {corners}")

        visible = [(r, g, b, a) for r, g, b, a in pixels(image) if a > 8]
        if not visible:
            problems.append(f"{path.name}: empty image")
            continue
        opaque_fraction = len(visible) / (SIZE * SIZE)
        if not 0.035 <= opaque_fraction <= 0.34:
            problems.append(f"{path.name}: visible fraction {opaque_fraction:.3f} out of range")
        off_color = sum(1 for r, g, b, _ in visible if abs(r - RED[0]) > 2 or abs(g - RED[1]) > 2 or abs(b - RED[2]) > 2)
        if off_color:
            problems.append(f"{path.name}: {off_color} visible pixels are not Legion red")

        mark_pixels = sum(1 for *_, a in pixels(image.crop(MARK_BOX)) if a > 64)
        if unit["family"] != "recruit" and mark_pixels - mark_baseline < 80:
            problems.append(
                f"{path.name}: family mark missing/too weak "
                f"({mark_pixels - mark_baseline} px over frame baseline)"
            )

        role_pixels = sum(1 for *_, a in pixels(image.crop(GLYPH_BOX)) if a > 64)
        if role_pixels < 320:
            problems.append(f"{path.name}: role glyph too weak ({role_pixels} px)")

        pip_region = image.crop((48, 251, 214, 291))
        pip_count = len(alpha_components(pip_region, threshold=80, minimum=55))
        if pip_count != int(unit["tier"]):
            problems.append(f"{path.name}: {pip_count} tier pips, expected {unit['tier']}")

        small = image.resize((100, 100), Image.Resampling.LANCZOS)
        small_role = small.crop(tuple(round(value / 3) for value in GLYPH_BOX))
        small_role_pixels = sum(1 for *_, a in pixels(small_role) if a > 60)
        if small_role_pixels < 45:
            problems.append(f"{path.name}: role unreadable at 100px ({small_role_pixels} px)")

        glyph_mask = image.crop(GLYPH_BOX).getchannel("A").resize((48, 48), Image.Resampling.BILINEAR).tobytes()
        glyph_masks[(unit["family"], int(unit["tier"]))].append((path.name, glyph_mask))
        metrics.append(f"{path.name}: visible={opaque_fraction:.3f}, role100={small_role_pixels}")

    # Same-family, same-tier classes must not collapse to the same visual type.
    for key, entries in glyph_masks.items():
        for index, (name_a, mask_a) in enumerate(entries):
            for name_b, mask_b in entries[index + 1 :]:
                mean_difference = sum(abs(a - b) for a, b in zip(mask_a, mask_b)) / len(mask_a)
                if mean_difference < 5.0:
                    problems.append(f"{name_a}/{name_b}: near-duplicate role glyph in {key} ({mean_difference:.1f})")

    make_preview(units, args.dir)
    make_stack_preview(units, args.dir)

    digest = hashlib.sha256()
    for filename in sorted(expected):
        path = args.dir / filename
        if path.exists():
            digest.update(filename.encode("utf-8"))
            digest.update(path.read_bytes())

    lines = [
        "# Legion unit portrait QA",
        "",
        f"- Result: **{'PASS' if not problems else 'FAIL'}**",
        f"- Catalog/runtime PNG: **{len(units)} / {len(expected - set(missing))}**",
        "- Contract: transparent RGBA 300x300; Legion-red-only; family mark inside shield at top; role below it inside shield; exact 0–4 tier pips.",
        "- Visual checks: 100 px game-scale sheet + xN upper-left overlay sheet.",
        f"- Set SHA-256: `{digest.hexdigest()}`",
        "",
    ]
    if problems:
        lines += ["## Failures", ""] + [f"- {problem}" for problem in problems]
    else:
        lines += ["No static QA failures."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if problems:
        print("FAIL")
        for problem in problems:
            print(" -", problem)
        print(f"Preview: {PREVIEW}")
        print(f"Stack preview: {STACK_PREVIEW}")
        return 1
    print(f"PASS: {len(units)} Legion portraits")
    print(f"Preview: {PREVIEW}")
    print(f"Stack preview: {STACK_PREVIEW}")
    print(f"Report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
