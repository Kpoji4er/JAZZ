# -*- coding: utf-8 -*-
"""Key solid black inventory backgrounds to alpha (flood from edges).

Safer than global near-black key: preserves dark zippers/straps on Medkit/IFAK.
"""
from pathlib import Path
from collections import deque

from PIL import Image

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
FILES = [
    "Icons/Items/JAZZ_Bandage.png",
    "Icons/Items/JAZZ_Morphine.png",
    "Icons/Items/JAZZ_IFAK.png",
    "Icons/Items/JAZZ_Medkit.png",
    "Icons/Items/JAZZ_SurgicalKit.png",
]

# near-black background threshold (max channel + chroma)
BLACK_MAX = 32
CHROMA_MAX = 14


def is_bg(px):
    r, g, b, a = px
    if a < 8:
        return True
    mx = max(r, g, b)
    mn = min(r, g, b)
    return mx <= BLACK_MAX and (mx - mn) <= CHROMA_MAX


def key_file(path: Path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    pix = im.load()
    visited = [[False] * h for _ in range(w)]
    q = deque()

    def try_push(x, y):
        if 0 <= x < w and 0 <= y < h and not visited[x][y] and is_bg(pix[x, y]):
            visited[x][y] = True
            q.append((x, y))

    for x in range(w):
        try_push(x, 0)
        try_push(x, h - 1)
    for y in range(h):
        try_push(0, y)
        try_push(w - 1, y)

    bg = set()
    while q:
        x, y = q.popleft()
        bg.add((x, y))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            try_push(x + dx, y + dy)

    out = im.copy()
    op = out.load()
    for x, y in bg:
        op[x, y] = (0, 0, 0, 0)

    # soft fringe: near-black neighbors of subject get partial alpha
    fringe = []
    for x in range(w):
        for y in range(h):
            if (x, y) in bg:
                continue
            r, g, b, a = op[x, y]
            mx = max(r, g, b)
            mn = min(r, g, b)
            if mx <= BLACK_MAX + 18 and (mx - mn) <= CHROMA_MAX + 6:
                # adjacent to keyed bg?
                if any((x + dx, y + dy) in bg for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    # fade by darkness
                    alpha = max(0, min(255, int((mx / (BLACK_MAX + 18)) * 180)))
                    fringe.append((x, y, alpha))
    for x, y, alpha in fringe:
        r, g, b, _ = op[x, y]
        op[x, y] = (r, g, b, alpha)

    out.save(path)
    corner = out.getpixel((0, 0))[3]
    # count opaque
    opaque = sum(1 for yy in range(h) for xx in range(w) if out.getpixel((xx, yy))[3] > 8)
    print(f"{path.name}: bg_px={len(bg)} opaque={opaque} cornerA={corner} size={w}x{h}")


def main():
    for rel in FILES:
        key_file(ROOT / rel)


if __name__ == "__main__":
    main()
