# -*- coding: utf-8 -*-
"""Flood-fill near-white PDA mark backgrounds → alpha.

Fixes `Icons/PDA/MERC_Mark.png` (opaque light-gray plate). Yellow $ / teal fill
stay: key only low-chroma high-luma pixels reachable from image edges.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    "Icons/PDA/MERC_Mark.png",
]

# flat studio plate: near-white / light gray, almost no chroma
LUMA_MIN = 220
CHROMA_MAX = 18


def is_bg(px) -> bool:
    r, g, b, a = px
    if a < 8:
        return True
    mx = max(r, g, b)
    mn = min(r, g, b)
    return mx >= LUMA_MIN and (mx - mn) <= CHROMA_MAX


def key_file(path: Path) -> dict:
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    pix = im.load()
    visited = [[False] * h for _ in range(w)]
    q = deque()

    def try_push(x: int, y: int) -> None:
        if 0 <= x < w and 0 <= y < h and not visited[x][y] and is_bg(pix[x, y]):
            visited[x][y] = True
            q.append((x, y))

    for x in range(w):
        try_push(x, 0)
        try_push(x, h - 1)
    for y in range(h):
        try_push(0, y)
        try_push(w - 1, y)

    bg: set[tuple[int, int]] = set()
    while q:
        x, y = q.popleft()
        bg.add((x, y))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            try_push(x + dx, y + dy)

    out = im.copy()
    op = out.load()
    for x, y in bg:
        op[x, y] = (0, 0, 0, 0)

    # soft fringe on light plate neighbors still attached to subject
    fringe: list[tuple[int, int, int]] = []
    for x in range(w):
        for y in range(h):
            if (x, y) in bg:
                continue
            r, g, b, a = op[x, y]
            mx = max(r, g, b)
            mn = min(r, g, b)
            if mx >= LUMA_MIN - 25 and (mx - mn) <= CHROMA_MAX + 6:
                if any(
                    (x + dx, y + dy) in bg
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                ):
                    # fade toward transparent as luma rises
                    t = (mx - (LUMA_MIN - 25)) / max(1, 255 - (LUMA_MIN - 25))
                    alpha = max(0, min(255, int(220 * (1.0 - t))))
                    fringe.append((x, y, alpha))
    for x, y, alpha in fringe:
        r, g, b, _ = op[x, y]
        op[x, y] = (r, g, b, alpha)

    out.save(path)
    corners = [op[0, 0], op[w - 1, 0], op[0, h - 1], op[w - 1, h - 1]]
    return {
        "path": path.as_posix(),
        "keyed": len(bg),
        "fringe": len(fringe),
        "corners": corners,
        "ok": all(c[3] < 10 for c in corners),
    }


def main() -> int:
    results = []
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING {rel}")
            return 1
        results.append(key_file(path))
    for r in results:
        status = "OK" if r["ok"] else "FAIL"
        print(
            f"{status} {r['path']} keyed={r['keyed']} fringe={r['fringe']} corners={r['corners']}"
        )
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
