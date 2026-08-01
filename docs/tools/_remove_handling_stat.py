# -*- coding: utf-8 -*-
"""Remove Firearm Handling stat (property, data, UI presets).

Idempotent: safe to re-run after ATTACH-001 owner decision (2026-08-01).
Does not touch component id ``JAZZ_HandlingWrap``.

Usage (from jazz/ root)::

    python docs/tools/_remove_handling_stat.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import delete_placeobj_blocks, prop, remove_resources

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
INVENTORY = ROOT / "InventoryItem"
WEAPONS_CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
ADD_PROPS = ROOT / "Code/System_Firearm_AddProperties.lua"
OR_UNIT = ROOT / "Code/System_OR_Unit.lua"


def strip_companion(text: str) -> tuple[str, int]:
    return re.subn(r"(?m)^\tHandling = -?\d+,\n", "", text)


def strip_items_weapon_fields(text: str) -> tuple[str, int]:
    return re.subn(r"(?m)^\t+'Handling', -?\d+,\n", "", text)


def delete_preset(text: str, cls: str, preset_id: str) -> tuple[str, int]:
    return delete_placeobj_blocks(text, cls, lambda block: prop(block.text, "id") == preset_id)


def main() -> int:
    code = ADD_PROPS.read_text(encoding="utf-8")
    code2, n = re.subn(
        r"\nFirearmProperties\.properties\[#FirearmProperties\.properties\+1\] = \{\n"
        r"    category = \"New Weapon System\",\n"
        r"    id = \"Handling\",\n"
        r".*?\n\}\n",
        "\n",
        code,
        count=1,
        flags=re.S,
    )
    if n:
        ADD_PROPS.write_text(code2, encoding="utf-8", newline="\n")
    print(f"FirearmProperties.Handling removed={n}")

    ut = OR_UNIT.read_text(encoding="utf-8")
    ut2, n = re.subn(r"\n\tHandling = true,", "", ut, count=1)
    if n:
        OR_UNIT.write_text(ut2, encoding="utf-8", newline="\n")
    print(f"CTH hide Handling removed={n}")

    items = ITEMS.read_text(encoding="utf-8")
    items, n_fields = strip_items_weapon_fields(items)
    print(f"items weapon Handling fields={n_fields}")
    for cls in ("ModItemWeaponPropertyDef", "ModItemGameTerm", "ModItemChanceToHitModifier"):
        items, n = delete_preset(items, cls, "Handling")
        print(f"deleted {cls} Handling={n}")
    ITEMS.write_text(items, encoding="utf-8", newline="\n")

    meta = META.read_text(encoding="utf-8")
    for cls in ("WeaponPropertyDef", "GameTerm", "ChanceToHitModifier"):
        meta, n = remove_resources(meta, cls, {"Handling"})
        print(f"metadata {cls} Handling={n}")
    META.write_text(meta, encoding="utf-8", newline="\n")

    total = 0
    for path in INVENTORY.rglob("*.lua"):
        text = path.read_text(encoding="utf-8")
        new, n = strip_companion(text)
        if n:
            path.write_text(new, encoding="utf-8", newline="\n")
            total += n
    print(f"companions Handling lines={total}")

    if WEAPONS_CSV.exists():
        with WEAPONS_CSV.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            fields = list(reader.fieldnames or [])
            rows = list(reader)
        if "handling" in fields:
            fields = [f for f in fields if f != "handling"]
            rows = [{k: r.get(k, "") for k in fields} for r in rows]
            with WEAPONS_CSV.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            print("weapons.csv dropped handling column")
        else:
            print("weapons.csv already without handling")

    items = ITEMS.read_text(encoding="utf-8")
    if 'id = "JAZZ_HandlingWrap"' not in items:
        print("WARN: JAZZ_HandlingWrap missing", file=sys.stderr)
    leftover = list(re.finditer(r'id = "Handling"', items))
    print(f"leftover id=Handling presets={len(leftover)}")
    return 0 if not leftover else 1


if __name__ == "__main__":
    raise SystemExit(main())
