# -*- coding: utf-8 -*-
"""Peek JAZZ_Stock* Cost / ModificationDifficulty from items.lua."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / "items.lua").read_text(encoding="utf-8")
want = {
    "JAZZ_StockNormal",
    "JAZZ_StockHeavy",
    "JAZZ_StockLight",
    "JAZZ_StockLightUnFolded",
    "JAZZ_StockLightFolded",
    "JAZZ_StockNo",
    "JAZZ_StockFolded",
}
for block in placeobj_blocks(text, "ModItemWeaponComponent"):
    cid = prop(block.text, "id")
    if cid not in want:
        continue
    cost_m = re.search(r"(?m)^\s*Cost = (-?\d+),", block.text)
    print(
        cid,
        "Cost=" + (cost_m.group(1) if cost_m else "?"),
        "diff=" + str(prop(block.text, "ModificationDifficulty")),
    )
