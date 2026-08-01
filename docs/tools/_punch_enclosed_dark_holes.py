"""Punch enclosed near-black fills inside Style-B skeleton stocks.

Edge flood-key leaves closed hollows as opaque charcoal; this marks
interior dark blobs that do not touch the canvas border and clears them.
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

LUMA_MAX = 48  # r+g+b
ALPHA_MIN = 160
MIN_COMP = 12


def punch(im: Image.Image, luma_max: int = LUMA_MAX) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    pix = list(im.getdata())
    dark = [False] * (w * h)
    for i, (r, g, b, a) in enumerate(pix):
        if a >= ALPHA_MIN and (r + g + b) <= luma_max:
            dark[i] = True

    visited = [False] * (w * h)
    hole = [False] * (w * h)
    nbr = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for i0 in range(w * h):
        if not dark[i0] or visited[i0]:
            continue
        q: deque[int] = deque([i0])
        visited[i0] = True
        comp: list[int] = []
        touch_border = False
        while q:
            i = q.popleft()
            comp.append(i)
            x, y = i % w, i // w
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                touch_border = True
            for dx, dy in nbr:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                ni = ny * w + nx
                if visited[ni] or not dark[ni]:
                    continue
                visited[ni] = True
                q.append(ni)
        if (not touch_border) and len(comp) >= MIN_COMP:
            for i in comp:
                hole[i] = True

    out = []
    for i, (r, g, b, a) in enumerate(pix):
        if hole[i]:
            out.append((0, 0, 0, 0))
        else:
            out.append((r, g, b, a))
    res = Image.new("RGBA", (w, h))
    res.putdata(out)
    # soft AA into punched hole
    alpha = res.getchannel("A").filter(ImageFilter.GaussianBlur(0.55))
    rgb = res.convert("RGB")
    return Image.merge("RGBA", (*rgb.split(), alpha))


def main() -> None:
    paths = [Path(a) for a in sys.argv[1:]]
    if not paths:
        raise SystemExit("usage: _punch_enclosed_dark_holes.py <png>...")
    for p in paths:
        im = Image.open(p)
        before = sum(1 for px in im.convert("RGBA").getdata() if px[3] > 200)
        out = punch(im)
        out.save(p)
        after = sum(1 for px in out.getdata() if px[3] > 200)
        print(f"{p}: opaque {before} -> {after} (cleared {before - after})")


if __name__ == "__main__":
    main()
