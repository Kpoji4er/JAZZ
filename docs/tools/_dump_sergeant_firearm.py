#!/usr/bin/env python3
"""Dump Sergeant_Firearm primary unlocks after regenerate."""
from __future__ import annotations

import re
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
text = ITEMS.read_text(encoding="utf-8")
i = text.find('id = "Sergeant_Firearm"')
start = text.rfind("PlaceObj('ModItemLootDef'", 0, i)
brace = text.find("{", start)
depth = 0
j = brace
while j < len(text):
    if text[j] == "{":
        depth += 1
    elif text[j] == "}":
        depth -= 1
        if depth == 0:
            block = text[start : j + 1]
            break
    j += 1

parts = block.split("PlaceObj('LootEntryLootDef'")
rows = []
for p in parts[1:]:
    amounts = [int(x) for x in re.findall(r"Amount = (\d+)", p)]
    loot = re.search(r'loot_def = "([^"]+)"', p)
    weight = re.search(r"weight = (\d+)", p)
    if not loot:
        continue
    cid = loot.group(1)
    m = re.match(r"JAZZ_GenW_(.+?)_(m0|cqb_m1|assault_m1)_", cid)
    weapon = m.group(1) if m else cid
    pkg = m.group(2) if m else "?"
    amin = amounts[0] if amounts else None
    amax = amounts[1] if len(amounts) > 1 else None
    rows.append((amin or 0, weapon, amin, amax, int(weight.group(1)) if weight else 0, pkg, cid))

# Deduplicate by weapon+amin (keep first)
seen = set()
for amin_sort, weapon, amin, amax, wt, pkg, cid in sorted(rows, key=lambda r: (r[0], r[1], r[4])):
    key = (weapon, amin, amax, wt)
    if key in seen:
        continue
    seen.add(key)
    label = f"{amin}" if amax is None else f"{amin}-{amax}"
    print(f"{weapon:14} unlock={label:8} wt={wt:6} pkg={pkg}")
