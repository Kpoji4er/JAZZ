# -*- coding: utf-8 -*-
"""Remove duplicate JAZZ_Bipod ModItems left after cut-id remap; keep the richest one."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, atomic_write, list_region

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"


def visual_count(text: str) -> int:
    region = list_region(text, "Visuals")
    if not region:
        return 0
    return text[region[0] : region[1]].count("PlaceObj('WeaponComponentVisual'")


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    blocks = [
        b
        for b in placeobj_blocks(text, "ModItemWeaponComponent")
        if prop(b.text, "id") == "JAZZ_Bipod"
    ]
    print("found", len(blocks))
    if len(blocks) <= 1:
        print("nothing to do")
        return 0
    ranked = sorted(blocks, key=lambda b: visual_count(b.text), reverse=True)
    keep = ranked[0]
    print("keep visuals", visual_count(keep.text), "start", keep.start)
    # remove others from end
    for b in sorted(ranked[1:], key=lambda x: x.start, reverse=True):
        end = b.end
        if end < len(text) and text[end] == ",":
            end += 1
        if end < len(text) and text[end] == "\n":
            end += 1
        text = text[: b.start] + text[end:]
        print("removed duplicate at", b.start, "visuals", visual_count(b.text))
    atomic_write(ITEMS, text)
    left = [
        b
        for b in placeobj_blocks(text, "ModItemWeaponComponent")
        if prop(b.text, "id") == "JAZZ_Bipod"
    ]
    print("remaining", len(left), "visuals", visual_count(left[0].text) if left else 0)
    return 0 if len(left) == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
