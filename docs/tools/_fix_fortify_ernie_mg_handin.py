#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix FortifyErnie GreasyBasil MG hand-in: MG42 → Jazz_Browning_* pair.

Root cause: loot/notes use Jazz_Browning_MuchineGun + Jazz_Browning_Bench,
but GreasyBasil_1 still gated/took MG42, so players with quest items never
complete MachineGun_Done → I5 emplacement never spawns.
"""
from __future__ import annotations

import re
from pathlib import Path

MAPS = Path(__file__).resolve().parents[2].parent / "jazz-maps"
ITEMS = MAPS / "items.lua"
I5 = MAPS / "Maps" / "ubRwFgf" / "objects.lua"

HAS_GUN = """PlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tItemId = "Jazz_Browning_MuchineGun",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitSquadHasItem', {
\t\t\t\t\t\t\t\tItemId = "Jazz_Browning_Bench",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),"""

TAKE_BOTH = """PlaceObj('UnitTakeItem', {
\t\t\t\t\t\t\t\t\tAnySquad = true,
\t\t\t\t\t\t\t\t\tItemId = "Jazz_Browning_MuchineGun",
\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\t\tPlaceObj('UnitTakeItem', {
\t\t\t\t\t\t\t\t\tAnySquad = true,
\t\t\t\t\t\t\t\t\tItemId = "Jazz_Browning_Bench",
\t\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t\t}),"""

# Pattern: single UnitSquadHasItem MG42 (with optional param_bindings)
HAS_MG42 = re.compile(
    r"PlaceObj\('UnitSquadHasItem',\s*\{\s*"
    r"ItemId\s*=\s*\"MG42\",\s*"
    r"(?:param_bindings\s*=\s*false,\s*)?"
    r"\}\),",
    re.M,
)

TAKE_MG42 = re.compile(
    r"PlaceObj\('UnitTakeItem',\s*\{\s*"
    r"AnySquad\s*=\s*true,\s*"
    r"ItemId\s*=\s*\"MG42\",\s*"
    r"(?:param_bindings\s*=\s*false,\s*)?"
    r"\}\),",
    re.M,
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text2, n_has = HAS_MG42.subn(HAS_GUN, text)
    text3, n_take = TAKE_MG42.subn(TAKE_BOTH, text2)
    if "ItemId = \"MG42\"" in text3 and "GreasyBasil" in text3:
        # leftover MG42 near FortifyErnie?
        leftovers = [
            i
            for i, line in enumerate(text3.splitlines(), 1)
            if 'ItemId = "MG42"' in line
        ]
        print(f"WARN leftover MG42 lines: {leftovers[:20]}")
    ITEMS.write_text(text3, encoding="utf-8")
    print(f"items.lua: UnitSquadHasItem MG42->Jazz pair x{n_has}; UnitTakeItem x{n_take}")

    if I5.exists():
        ot = I5.read_text(encoding="utf-8")
        ot2, n_ammo = re.subn(
            r"('ammo_template',\s*)\"_50BMG_Basic\"",
            r'\1"JAZZ_AMMO_50BMG_Basic"',
            ot,
        )
        I5.write_text(ot2, encoding="utf-8")
        print(f"ubRwFgf objects.lua: ammo_template _50BMG_Basic->JAZZ_AMMO_50BMG_Basic x{n_ammo}")


if __name__ == "__main__":
    main()
