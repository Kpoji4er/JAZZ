# -*- coding: utf-8 -*-
"""JAZZ-INV-004: grenadier powder loot, TNT/C4/PETN powder recipes, mine salvage."""
from __future__ import annotations

import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"

RECIPES = {
    "JAZZ_TNT_Disassemble_Powder": {"src": "TNT", "amount": 2, "diff": 25},
    "JAZZ_C4_Disassemble_Powder": {"src": "C4", "amount": 3, "diff": 40},
    "JAZZ_PETN_Disassemble_Powder": {"src": "PETN", "amount": 4, "diff": 55},
}

LOOT = {
    "Grenadier_Inventory": (1, 2),
    "HeavyGrenadier_Inventory": (2, 3),
    "ArmyDemo": (1, 2),
    "ArmyDemo_Elite": (1, 2),
    "ArmyCommando_Demo": (1, 2),
    "AdonisDemolitions": (2, 3),
    "AdonisDemolitions_Elite": (2, 3),
    "RebelGrenadier": (1, 2),
    "RebelRPG": (2, 3),
}


def _loot_block(text: str, loot_id: str) -> str | None:
    needle = f'id = "{loot_id}"'
    pos = 0
    while True:
        i = text.find(needle, pos)
        if i < 0:
            return None
        start = text.rfind("PlaceObj('ModItemLootDef'", 0, i)
        if start < 0 or text[start:i].count("PlaceObj('ModItemLootDef'") != 1:
            pos = i + 1
            continue
        brace = text.find("{", start)
        depth = 0
        for j in range(brace, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    return text[start : j + 1]
        return None


def _recipe_block(text: str, recipe_id: str) -> str | None:
    m = re.search(
        rf"PlaceObj\('ModItemRecipeDef',\s*\{{(.*?)\bid\s*=\s*\"{re.escape(recipe_id)}\",",
        text,
        re.S,
    )
    return m.group(0) if m else None


def main() -> int:
    problems: list[str] = []
    units = (UNITS / "items.lua").read_text(encoding="utf-8")
    jazz_items = (JAZZ / "items.lua").read_text(encoding="utf-8")
    meta = (JAZZ / "metadata.lua").read_text(encoding="utf-8")
    traps = (JAZZ / "Code" / "System_OR_Traps.lua").read_text(encoding="utf-8")

    for loot_id, (pmin, pmax) in LOOT.items():
        block = _loot_block(units, loot_id)
        if not block:
            problems.append(f"missing LootDef {loot_id}")
            continue
        if 'item = "BlackPowder"' not in block:
            problems.append(f"{loot_id}: no BlackPowder")
            continue
        if f"stack_min = {pmin}" not in block or f"stack_max = {pmax}" not in block:
            problems.append(f"{loot_id}: expected BlackPowder {pmin}-{pmax}")

    for rid, spec in RECIPES.items():
        block = _recipe_block(jazz_items, rid)
        if not block:
            problems.append(f"missing RecipeDef {rid}")
            continue
        if f'Difficulty = {spec["diff"]}' not in block:
            problems.append(f"{rid}: Difficulty != {spec['diff']}")
        if f"'item', \"{spec['src']}\"" not in block:
            problems.append(f"{rid}: missing ingredient {spec['src']}")
        if f"'amount', {spec['amount']}" not in block:
            problems.append(f"{rid}: powder amount != {spec['amount']}")
        if "'item', \"Wirecutter\"" not in block:
            problems.append(f"{rid}: missing Wirecutter")
        if f"'Id', \"{rid}\"" not in meta:
            problems.append(f"metadata missing ModResourcePreset {rid}")

    if "function Jazz_TrySalvageMineCharge" not in traps:
        problems.append("missing Jazz_TrySalvageMineCharge")
    if "function OnMsg.TrapDisarm" not in traps:
        problems.append("missing OnMsg.TrapDisarm")
    if "if roll >= 40 then" not in traps:
        problems.append("mine salvage chance is not 40")
    for thrown, base in (
        ("ProximityC4", "C4"),
        ("ProximityTNT", "TNT"),
        ("ProximityPETN", "PETN"),
    ):
        if f'{thrown} = "{base}"' not in traps:
            problems.append(f"missing thrown map {thrown}->{base}")

    if problems:
        print("FAIL")
        for p in problems:
            print(" -", p)
        return 1
    print("OK INV-004 powder loot, recipes, mine salvage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
