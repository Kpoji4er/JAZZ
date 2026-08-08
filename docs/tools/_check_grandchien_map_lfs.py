# -*- coding: utf-8 -*-
"""Fail if jazz-maps Images/GrandChien2.png is still a Git LFS pointer (black sat map)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Prefer sibling jazz-maps next to jazz/
CANDIDATES = [
    ROOT.parent / "jazz-maps" / "Images" / "GrandChien2.png",
    ROOT / ".." / "jazz-maps" / "Images" / "GrandChien2.png",
]
EXPECTED_MIN = 1_000_000  # real art is ~70MB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
LFS_MAGIC = b"version https://git-lfs.github.com/spec/v1"


def main() -> int:
    path = next((p.resolve() for p in CANDIDATES if p.exists()), None)
    if path is None:
        print("FAIL: GrandChien2.png not found (expected ../jazz-maps/Images/)")
        return 2
    data = path.read_bytes()[:64]
    size = path.stat().st_size
    print(f"path={path}")
    print(f"size={size}")
    if data.startswith(LFS_MAGIC) or size < EXPECTED_MIN:
        print("RESULT: FAIL — LFS pointer or incomplete file (satellite map will be black)")
        print("Fix: install Git LFS, then from jazz-maps:  git lfs install && git lfs pull")
        return 1
    if not data.startswith(PNG_MAGIC):
        print("RESULT: FAIL — not a PNG")
        return 1
    print("RESULT: OK — real GrandChien2.png present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
