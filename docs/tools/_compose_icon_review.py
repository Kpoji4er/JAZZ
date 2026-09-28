"""Contact sheet for reviewing a new weapon icon against accepted ones.

    python docs/tools/_compose_icon_review.py --icon <new.png> \
        --reference WeaponIcons/AK74.png --reference WeaponIcons/AKM.png \
        --out <review.png>

Produces one PNG: the raw icon on a checkerboard (so the alpha contour is
visible), the same icon on the #2a2a2a inventory background, and each
reference on that identical background for a like-for-like comparison.

The recurring failure this catches is a weapon rendered without a dark outline:
it looks fine on white, then disappears into the inventory slot.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

SLOT = (0x2A, 0x2A, 0x2A, 255)
PAD = 16
LABEL_H = 18


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--icon", required=True, type=Path)
    p.add_argument("--reference", action="append", default=[], type=Path)
    p.add_argument("--out", required=True, type=Path)
    return p.parse_args()


def checkerboard(size, step=8):
    img = Image.new("RGBA", size, (210, 210, 210, 255))
    draw = ImageDraw.Draw(img)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle([x, y, x + step - 1, y + step - 1], fill=(170, 170, 170, 255))
    return img


def on_background(icon, background):
    plate = Image.new("RGBA", icon.size, background)
    plate.alpha_composite(icon)
    return plate


def main():
    args = parse_args()
    icon = Image.open(args.icon).convert("RGBA")

    tiles = [
        (
            f"{args.icon.name}  {icon.width}x{icon.height}",
            Image.alpha_composite(checkerboard(icon.size), icon),
        ),
        (f"{args.icon.stem} on #2a2a2a", on_background(icon, SLOT)),
    ]
    for ref in args.reference:
        image = Image.open(ref).convert("RGBA")
        tiles.append((f"{ref.name}  {image.width}x{image.height}", on_background(image, SLOT)))

    width = max(t.width for _, t in tiles) + PAD * 2
    height = sum(t.height + LABEL_H + PAD for _, t in tiles) + PAD
    sheet = Image.new("RGBA", (width, height), (24, 24, 24, 255))
    draw = ImageDraw.Draw(sheet)

    y = PAD
    for label, tile in tiles:
        draw.text((PAD, y), label, fill=(225, 225, 225, 255))
        y += LABEL_H
        sheet.alpha_composite(tile, (PAD, y))
        y += tile.height + PAD

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out)
    print(f"{args.out}  {sheet.width}x{sheet.height}  tiles={len(tiles)}")


if __name__ == "__main__":
    main()
