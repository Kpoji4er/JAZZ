# -*- coding: utf-8 -*-
"""Build thin 54x54 weapon-chip glyphs from old dual-strip HUD icons."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Icons" / "Hud"

# old dual-strip (108x54) -> single thin chip glyph
MAP = {
    "stock_in.png": "weapon_stock_fold.png",
    "stock_out.png": "weapon_stock_unfold.png",
    "flash_on.png": "weapon_flash_on.png",
    "flash_off.png": "weapon_flash_off.png",
}

CANVAS = 54
# target content size inside chip (leaves padding; reads thinner at 25px button)
CONTENT = 28
ALPHA_KEY = 28  # near-black -> transparent


def key_black(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if r <= ALPHA_KEY and g <= ALPHA_KEY and b <= ALPHA_KEY:
                px[x, y] = (r, g, b, 0)
    return im


def opaque_bbox(im: Image.Image):
    px = im.load()
    w, h = im.size
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 20:
                minx = min(minx, x)
                miny = min(miny, y)
                maxx = max(maxx, x)
                maxy = max(maxy, y)
    if maxx < 0:
        return None
    return (minx, miny, maxx + 1, maxy + 1)


def to_white_alpha(im: Image.Image) -> Image.Image:
    """Keep alpha from luminance; force RGB white so ImageColor tint works like Switch/Reload."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a <= 0:
                px[x, y] = (0, 0, 0, 0)
                continue
            lum = max(r, g, b)
            # thin: use luminance as alpha, slightly soft
            na = min(255, int(a * lum / 255))
            if na < 16:
                px[x, y] = (0, 0, 0, 0)
            else:
                px[x, y] = (255, 255, 255, na)
    return im


def build(src_name: str, dst_name: str):
    src = Image.open(ROOT / "Icons" / src_name).convert("RGBA")
    assert src.size[0] >= 54 and src.size[1] >= 54, src.size
    # left glyph of dual strip
    half = src.crop((0, 0, 54, 54))
    half = key_black(half)
    half = to_white_alpha(half)
    box = opaque_bbox(half)
    if not box:
        raise SystemExit(f"empty glyph: {src_name}")
    glyph = half.crop(box)
    gw, gh = glyph.size
    scale = min(CONTENT / gw, CONTENT / gh)
    nw = max(1, int(round(gw * scale)))
    nh = max(1, int(round(gh * scale)))
    glyph = glyph.resize((nw, nh), Image.Resampling.LANCZOS)
    # light erode via min-filter on alpha to thin strokes one more notch
    gpx = glyph.load()
    thinned = glyph.copy()
    tpx = thinned.load()
    for y in range(nh):
        for x in range(nw):
            a = gpx[x, y][3]
            if a < 40:
                tpx[x, y] = (0, 0, 0, 0)
                continue
            # if any neighbor is empty, reduce alpha (edge thin)
            edge = False
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    xx, yy = x + dx, y + dy
                    if xx < 0 or yy < 0 or xx >= nw or yy >= nh or gpx[xx, yy][3] < 40:
                        edge = True
                        break
                if edge:
                    break
            if edge:
                tpx[x, y] = (255, 255, 255, max(0, a - 90))
            else:
                tpx[x, y] = (255, 255, 255, a)
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    ox = (CANVAS - nw) // 2
    oy = (CANVAS - nh) // 2
    canvas.alpha_composite(thinned, (ox, oy))
    out = OUT / dst_name
    canvas.save(out)
    box2 = opaque_bbox(canvas)
    print(f"{dst_name}: from {src_name} content={nw}x{nh} bbox={box2}")


def main():
    for src, dst in MAP.items():
        build(src, dst)
    print("OK")


if __name__ == "__main__":
    main()
