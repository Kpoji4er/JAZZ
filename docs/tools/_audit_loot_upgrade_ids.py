#!/usr/bin/env python3
"""Count legacy vs JAZZ component IDs in jazz-units LootEntryUpgradedWeapon upgrades."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
text = UNITS.read_text(encoding="utf-8")

# upgrades = { "A", "B", }
blocks = re.findall(
    r"PlaceObj\('LootEntryUpgradedWeapon',\s*\{(.*?)\}\),",
    text,
    re.S,
)
print(f"LootEntryUpgradedWeapon blocks: {len(blocks)}")
ids = Counter()
for body in blocks:
    for u in re.findall(r'"([A-Za-z0-9_]+)"', body):
        if u in ("Difficulty", "VeryHard", "Easy", "Hard", "Normal") or u.startswith("condition"):
            continue
        # skip weapon= ids by crude filter: only inside upgrades tables
        pass
    um = re.search(r"upgrades\s*=\s*\{([^}]*)\}", body)
    if not um:
        continue
    for u in re.findall(r'"([A-Za-z0-9_]+)"', um.group(1)):
        ids[u] += 1

print("Top upgrade IDs:")
for k, v in ids.most_common(40):
    jazz = "JAZZ_" if k.startswith("JAZZ_") else ("legacy?" if not k.startswith("JAZZ_") else "")
    print(f"  {v:4} {k}")

legacy = [k for k in ids if not k.startswith("JAZZ_") and k not in ("true", "false")]
print(f"\nNon-JAZZ_ upgrade ids: {len(legacy)}")
for k in sorted(legacy):
    print(f"  {ids[k]:4} {k}")
