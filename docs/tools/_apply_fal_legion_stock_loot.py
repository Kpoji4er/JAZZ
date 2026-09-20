# -*- coding: utf-8 -*-
"""Pin both FN FAL stocks in Legion loot: regular JAZZ_StockNormal and Para UnFolded.

JAZZ-WEAPON-FAL-FAMILY-001-REQ-007. Edit jazz-units/items.lua only.
"""
from __future__ import annotations

import sys
from pathlib import Path

UNITS = Path(__file__).resolve().parents[3] / "jazz-units"
ITEMS = UNITS / "items.lua"


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)


def apply(text: str) -> str:
    text = _replace_once(
        text,
        (
            '\t\t\t\t\tid = "BattleRifles_FNFAL",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
            '\t\t\t\t\t\titem = "FNFAL",\n'
            "\t\t\t\t\t\tstack_max = 1,\n"
            "\t\t\t\t\t\tstack_min = 1,\n"
            "\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\tid = "BattleRifles_FNFAL",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t"JAZZ_StockNormal",\n'
            "\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t}),\n"
        ),
        "BattleRifles_FNFAL",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\tid = "BattleRifles_FNFAL_AP",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {\n"
            '\t\t\t\t\t\titem = "FNFAL",\n'
            "\t\t\t\t\t\tstack_max = 1,\n"
            "\t\t\t\t\t\tstack_min = 1,\n"
            "\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\tid = "BattleRifles_FNFAL_AP",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t"JAZZ_StockNormal",\n'
            "\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t}),\n"
        ),
        "BattleRifles_FNFAL_AP",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\tid = "BattleRifles_FNFALLight",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t"JAZZ_StockLight",\n'
            "\t\t\t\t\t\t},\n"
        ),
        (
            '\t\t\t\t\tid = "BattleRifles_FNFALLight",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t"JAZZ_StockLightUnFolded",\n'
            "\t\t\t\t\t\t},\n"
        ),
        "BattleRifles_FNFALLight",
    )

    stock_pins = (
        (
            "BattleRifles_FNFAL3xScope",
            '"JAZZ_CombatScope_2x",\n',
            '"JAZZ_StockNormal",\n\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n',
        ),
        (
            "BattleRifles_FNFALDTK",
            '"JAZZ_Compensator",\n',
            '"JAZZ_StockNormal",\n\t\t\t\t\t\t\t"JAZZ_Compensator",\n',
        ),
        (
            "BattleRifles_FNFAL_AP_Grip",
            '"JAZZ_VerticalGrip",\n',
            '"JAZZ_StockNormal",\n\t\t\t\t\t\t\t"JAZZ_VerticalGrip",\n',
        ),
        (
            "BattleRifles_FNFAL_AP_Grip_Scope",
            '"JAZZ_VerticalGrip",\n\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n',
            '"JAZZ_StockNormal",\n\t\t\t\t\t\t\t"JAZZ_VerticalGrip",\n\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n',
        ),
        (
            "BattleRifles_FNFAL_AP_Grip_Reflex",
            '"JAZZ_VerticalGrip",\n\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n',
            '"JAZZ_StockNormal",\n\t\t\t\t\t\t\t"JAZZ_VerticalGrip",\n\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n',
        ),
    )
    for loot_id, old_up, new_up in stock_pins:
        needle = (
            f'\t\t\t\t\tid = "{loot_id}",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            f"\t\t\t\t\t\t\t{old_up}"
        )
        repl = (
            f'\t\t\t\t\tid = "{loot_id}",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            f"\t\t\t\t\t\t\t{new_up}"
        )
        text = _replace_once(text, needle, repl, loot_id)

    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFAL",\n'
            "\t\t\t\t\t\t\tweight = 2000,\n"
            "\t\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFAL",\n'
            "\t\t\t\t\t\t\tweight = 2000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tcomment = "T2-3",\n'
            "\t\t\t\t\t\t\tgame_conditions = {\n"
            "\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableNum', {\n"
            "\t\t\t\t\t\t\t\t\tAmount = 23,\n"
            '\t\t\t\t\t\t\t\t\tProp = "JAZZ_Legion_Tier",\n'
            '\t\t\t\t\t\t\t\t\tQuestId = "JAZZ_LegionTier",\n'
            "\t\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFALLight",\n'
            "\t\t\t\t\t\t\tweight = 2000,\n"
            "\t\t\t\t\t\t}),\n"
        ),
        "LegionT2_BattleRifle FNFALLight",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFALDTK",\n'
            "\t\t\t\t\t\t\tweight = 24000,\n"
            "\t\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFALDTK",\n'
            "\t\t\t\t\t\t\tweight = 24000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tcomment = "T2-3",\n'
            "\t\t\t\t\t\t\tgame_conditions = {\n"
            "\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableNum', {\n"
            "\t\t\t\t\t\t\t\t\tAmount = 23,\n"
            '\t\t\t\t\t\t\t\t\tProp = "JAZZ_Legion_Tier",\n'
            '\t\t\t\t\t\t\t\t\tQuestId = "JAZZ_LegionTier",\n'
            "\t\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFALLight",\n'
            "\t\t\t\t\t\t\tweight = 24000,\n"
            "\t\t\t\t\t\t}),\n"
        ),
        "LegionT2_BattleRifle_Elite FNFALLight",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFAL_AP",\n'
            "\t\t\t\t\t\t\tweight = 100000,\n"
            "\t\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFAL_AP",\n'
            "\t\t\t\t\t\t\tweight = 100000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tcomment = "T2-1",\n'
            "\t\t\t\t\t\t\tgame_conditions = {\n"
            "\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableNum', {\n"
            "\t\t\t\t\t\t\t\t\tAmount = 21,\n"
            '\t\t\t\t\t\t\t\t\tProp = "JAZZ_Legion_Tier",\n'
            '\t\t\t\t\t\t\t\t\tQuestId = "JAZZ_LegionTier",\n'
            "\t\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tloot_def = "BattleRifles_FNFALLight",\n'
            "\t\t\t\t\t\t\tweight = 100000,\n"
            "\t\t\t\t\t\t}),\n"
        ),
        "LegionMercenary_AssaultRifle FNFALLight",
    )

    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\tid = "JAZZ_GenW_FNFAL_rifle_m1_762x51_ar_ammo_ap",\n'
            '\t\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n'
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\t\tid = "JAZZ_GenW_FNFAL_rifle_m1_762x51_ar_ammo_ap",\n'
            '\t\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t\t"JAZZ_StockNormal",\n'
            '\t\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n'
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t\t}),\n"
        ),
        "JAZZ_GenW_FNFAL m1",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\tid = "JAZZ_GenW_FNFAL_rifle_m2_762x51_ar_ammo_ap",\n'
            '\t\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n'
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\t\tid = "JAZZ_GenW_FNFAL_rifle_m2_762x51_ar_ammo_ap",\n'
            '\t\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t\t"JAZZ_StockLightUnFolded",\n'
            '\t\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n'
            "\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t\t}),\n"
        ),
        "JAZZ_GenW_FNFAL m2",
    )
    return text


def main() -> int:
    raw = ITEMS.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    if newline == "\r\n":
        work = text.replace("\r\n", "\n")
    else:
        work = text
    updated = apply(work)
    if newline == "\r\n":
        out = updated.replace("\n", "\r\n")
    else:
        out = updated
    encoded = out.encode("utf-8")
    if "--apply" in sys.argv:
        ITEMS.write_bytes(encoded)
        print(f"applied {ITEMS} ({len(encoded) - len(raw):+d} bytes)")
    else:
        old_lines = text.splitlines()
        new_lines = out.splitlines()
        changed = sum(1 for a, b in zip(old_lines, new_lines) if a != b)
        changed += abs(len(new_lines) - len(old_lines))
        print(
            f"dry-run ok, bytes {len(encoded) - len(raw):+d}, "
            f"lines {len(old_lines)} -> {len(new_lines)}, changed~{changed}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
