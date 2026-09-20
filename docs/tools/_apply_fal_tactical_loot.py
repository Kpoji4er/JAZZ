# -*- coding: utf-8 -*-
"""Add JAZZ_FNFAL_Tactical to Legion T2-4 and Adonis assault pools.

JAZZ-WEAPON-FAL-FAMILY-001-REQ-008.
"""
from __future__ import annotations

import sys
from pathlib import Path

UNITS = Path(__file__).resolve().parents[3] / "jazz-units"
ITEMS = UNITS / "items.lua"
META = UNITS / "metadata.lua"

BATTLE_BLOCK = """\t\t\t\tPlaceObj('ModItemLootDef', {
\t\t\t\t\tComment = "T2-4",
\t\t\t\t\tcomment = "T2-4",
\t\t\t\t\tgroup = "Default",
\t\t\t\t\tid = "BattleRifles_FNFAL_Tactical",
\t\t\t\t\tloot = "all",
\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {
\t\t\t\t\t\tweapon = "JAZZ_FNFAL_Tactical",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('LootEntryLootDef', {
\t\t\t\t\t\tloot_def = "762x51_ar_ammo",
\t\t\t\t\t}),
\t\t\t\t}),
\t\t\t\tPlaceObj('ModItemLootDef', {
\t\t\t\t\tComment = "T2-4",
\t\t\t\t\tcomment = "T2-4",
\t\t\t\t\tgroup = "Default",
\t\t\t\t\tid = "BattleRifles_FNFAL_Tactical_AP",
\t\t\t\t\tloot = "all",
\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {
\t\t\t\t\t\tweapon = "JAZZ_FNFAL_Tactical",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('LootEntryLootDef', {
\t\t\t\t\t\tloot_def = "762x51_ar_ammo_ap",
\t\t\t\t\t}),
\t\t\t\t}),
\t\t\t\tPlaceObj('ModItemLootDef', {
\t\t\t\t\tComment = "T2-4",
\t\t\t\t\tcomment = "T2-4",
\t\t\t\t\tgroup = "Default",
\t\t\t\t\tid = "BattleRifles_FNFAL_Tactical_Scope",
\t\t\t\t\tloot = "all",
\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {
\t\t\t\t\t\tupgrades = {
\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",
\t\t\t\t\t\t},
\t\t\t\t\t\tweapon = "JAZZ_FNFAL_Tactical",
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('LootEntryLootDef', {
\t\t\t\t\t\tloot_def = "762x51_ar_ammo_ap",
\t\t\t\t\t}),
\t\t\t\t}),
"""

ADONIS_PRESETS = """\t\t\t\t\t\tPlaceObj('ModItemLootDef', {
\t\t\t\t\t\t\tcomment = "T2",
\t\t\t\t\t\t\tgroup = "Enemy - General",
\t\t\t\t\t\t\tid = "Adonis_FNFAL_Tactical",
\t\t\t\t\t\t\tloot = "all",
\t\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {
\t\t\t\t\t\t\t\tupgrades = {
\t\t\t\t\t\t\t\t\t"JAZZ_LaserDot",
\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\tweapon = "JAZZ_FNFAL_Tactical",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {
\t\t\t\t\t\t\t\tloot_def = "Adonis_762x51",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('ModItemLootDef', {
\t\t\t\t\t\t\tcomment = "T2",
\t\t\t\t\t\t\tgroup = "Enemy - General",
\t\t\t\t\t\t\tid = "Adonis_FNFAL_Tactical_Reflex",
\t\t\t\t\t\t\tloot = "all",
\t\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {
\t\t\t\t\t\t\t\tupgrades = {
\t\t\t\t\t\t\t\t\t"JAZZ_Reflex_M68",
\t\t\t\t\t\t\t\t\t"JAZZ_LaserDot",
\t\t\t\t\t\t\t\t},
\t\t\t\t\t\t\t\tweapon = "JAZZ_FNFAL_Tactical",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {
\t\t\t\t\t\t\t\tloot_def = "Adonis_762x51",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t}),
"""

RESOURCE = """\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', "LootDef",
\t\t\t'Id', "{id}",
\t\t\t'ClassDisplayName', "LootDef",
\t\t}}),
"""


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)


def _tier_entry(comment: str, amount: int, loot_def: str, weight: int) -> str:
    return (
        "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
        f'\t\t\t\t\t\t\tcomment = "{comment}",\n'
        "\t\t\t\t\t\t\tgame_conditions = {\n"
        "\t\t\t\t\t\t\t\tPlaceObj('QuestIsVariableNum', {\n"
        f"\t\t\t\t\t\t\t\t\tAmount = {amount},\n"
        '\t\t\t\t\t\t\t\t\tProp = "JAZZ_Legion_Tier",\n'
        '\t\t\t\t\t\t\t\t\tQuestId = "JAZZ_LegionTier",\n'
        "\t\t\t\t\t\t\t\t}),\n"
        "\t\t\t\t\t\t\t},\n"
        f'\t\t\t\t\t\t\tloot_def = "{loot_def}",\n'
        f"\t\t\t\t\t\t\tweight = {weight},\n"
        "\t\t\t\t\t\t}),\n"
    )


def apply_items(text: str) -> str:
    text = _replace_once(
        text,
        (
            '\t\t\t\t\tid = "BattleRifles_FNFAL_AP_Grip_Reflex",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t"JAZZ_StockNormal",\n'
            '\t\t\t\t\t\t\t"JAZZ_VerticalGrip",\n'
            '\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n'
            "\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t}),\n"
            "\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\tloot_def = "762x51_ar_ammo_ap",\n'
            "\t\t\t\t\t}),\n"
            "\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\tid = "BattleRifles_FNFAL_AP_Grip_Reflex",\n'
            '\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t"JAZZ_StockNormal",\n'
            '\t\t\t\t\t\t\t"JAZZ_VerticalGrip",\n'
            '\t\t\t\t\t\t\t"JAZZ_CombatScope_2x",\n'
            "\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\tweapon = "FNFAL",\n'
            "\t\t\t\t\t}),\n"
            "\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\tloot_def = "762x51_ar_ammo_ap",\n'
            "\t\t\t\t\t}),\n"
            "\t\t\t\t}),\n"
            + BATTLE_BLOCK
        ),
        "BattleRifles_FNFAL_Tactical defs",
    )

    galil_regular = (
        '\t\t\t\t\t\t\tloot_def = "BattleRifles_Galil",\n'
        "\t\t\t\t\t\t\tweight = 2000,\n"
        "\t\t\t\t\t\t}),\n"
    )
    text = _replace_once(
        text,
        galil_regular,
        galil_regular + _tier_entry("T2-4", 24, "BattleRifles_FNFAL_Tactical", 2000),
        "LegionT2_BattleRifle tactical",
    )

    galil_elite = (
        '\t\t\t\t\t\t\tloot_def = "BattleRifles_Galil_AP_DTK",\n'
        "\t\t\t\t\t\t\tweight = 42000,\n"
        "\t\t\t\t\t\t}),\n"
    )
    text = _replace_once(
        text,
        galil_elite,
        galil_elite
        + _tier_entry("T2-4", 24, "BattleRifles_FNFAL_Tactical_AP", 42000)
        + _tier_entry("T2-4", 24, "BattleRifles_FNFAL_Tactical_Scope", 42000),
        "LegionT2_BattleRifle_Elite tactical",
    )

    galil_merc = (
        '\t\t\t\t\t\t\tloot_def = "BattleRifles_Galil_AP_Bipod_Scope",\n'
        "\t\t\t\t\t\t\tweight = 800000,\n"
        "\t\t\t\t\t\t}),\n"
    )
    text = _replace_once(
        text,
        galil_merc,
        galil_merc + _tier_entry("T2-4", 24, "BattleRifles_FNFAL_Tactical_Scope", 800000),
        "LegionMercenary_AssaultRifle tactical",
    )

    text = _replace_once(
        text,
        'comment = "HK33 M4 M16A4 AKM",\n',
        'comment = "HK33 M4 M16A4 AKM FAL Tac",\n',
        "Adonis_AssaultRifle comment",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\t\tloot_def = "Adonis_AKMAdvReflex",\n'
            "\t\t\t\t\t\t\tweight = 2000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t}),\n"
            "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
            '\t\t\t\t\t\tcomment = "G36 AUG SIG550",\n'
        ),
        (
            '\t\t\t\t\t\t\tloot_def = "Adonis_AKMAdvReflex",\n'
            "\t\t\t\t\t\t\tweight = 2000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tloot_def = "Adonis_FNFAL_Tactical",\n'
            "\t\t\t\t\t\t\tweight = 3000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tloot_def = "Adonis_FNFAL_Tactical_Reflex",\n'
            "\t\t\t\t\t\t\tweight = 2000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t}),\n"
            "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
            '\t\t\t\t\t\tcomment = "G36 AUG SIG550 FAL Tac",\n'
        ),
        "Adonis_AssaultRifle entries",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\t\tloot_def = "Adonis_SG552SWATReflex",\n'
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t}),\n"
            "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
            '\t\t\t\t\t\tcomment = "MP5 UMP MP7",\n'
        ),
        (
            '\t\t\t\t\t\t\tloot_def = "Adonis_SG552SWATReflex",\n'
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tloot_def = "Adonis_FNFAL_Tactical",\n'
            "\t\t\t\t\t\t\tweight = 4000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\tloot_def = "Adonis_FNFAL_Tactical_Reflex",\n'
            "\t\t\t\t\t\t\tweight = 6000,\n"
            "\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t}),\n"
            "\t\t\t\t\tPlaceObj('ModItemLootDef', {\n"
            '\t\t\t\t\t\tcomment = "MP5 UMP MP7",\n'
        ),
        "AdonisElite_AssaultRifle entries",
    )
    text = _replace_once(
        text,
        (
            '\t\t\t\t\t\t\tid = "Adonis_SG552Reflex",\n'
            '\t\t\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t\t\t"JAZZ_Reflex_Open",\n'
            "\t\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\t\tweapon = "Sig552",\n'
            "\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\t\tloot_def = "Adonis_556",\n'
            "\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t}),\n"
        ),
        (
            '\t\t\t\t\t\t\tid = "Adonis_SG552Reflex",\n'
            '\t\t\t\t\t\t\tloot = "all",\n'
            "\t\t\t\t\t\t\tPlaceObj('LootEntryUpgradedWeapon', {\n"
            "\t\t\t\t\t\t\t\tupgrades = {\n"
            '\t\t\t\t\t\t\t\t\t"JAZZ_Reflex_Open",\n'
            "\t\t\t\t\t\t\t\t},\n"
            '\t\t\t\t\t\t\t\tweapon = "Sig552",\n'
            "\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t\tPlaceObj('LootEntryLootDef', {\n"
            '\t\t\t\t\t\t\t\tloot_def = "Adonis_556",\n'
            "\t\t\t\t\t\t\t}),\n"
            "\t\t\t\t\t\t}),\n"
            + ADONIS_PRESETS
        ),
        "Adonis FAL presets",
    )
    return text


def apply_meta(text: str) -> str:
    battle_ids = (
        "BattleRifles_FNFAL_Tactical",
        "BattleRifles_FNFAL_Tactical_AP",
        "BattleRifles_FNFAL_Tactical_Scope",
    )
    battle_res = "".join(RESOURCE.format(id=i) for i in battle_ids)
    text = _replace_once(
        text,
        (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "LootDef",\n'
            '\t\t\t\'Id\', "BattleRifles_FNFAL_AP_Grip_Reflex",\n'
            '\t\t\t\'ClassDisplayName\', "LootDef",\n'
            "\t\t}),\n"
        ),
        (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "LootDef",\n'
            '\t\t\t\'Id\', "BattleRifles_FNFAL_AP_Grip_Reflex",\n'
            '\t\t\t\'ClassDisplayName\', "LootDef",\n'
            "\t\t}),\n"
            + battle_res
        ),
        "metadata BattleRifles_FNFAL_Tactical",
    )
    adonis_res = "".join(
        RESOURCE.format(id=i)
        for i in ("Adonis_FNFAL_Tactical", "Adonis_FNFAL_Tactical_Reflex")
    )
    text = _replace_once(
        text,
        (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "LootDef",\n'
            '\t\t\t\'Id\', "Adonis_SG552Reflex",\n'
            '\t\t\t\'ClassDisplayName\', "LootDef",\n'
            "\t\t}),\n"
        ),
        (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "LootDef",\n'
            '\t\t\t\'Id\', "Adonis_SG552Reflex",\n'
            '\t\t\t\'ClassDisplayName\', "LootDef",\n'
            "\t\t}),\n"
            + adonis_res
        ),
        "metadata Adonis_FNFAL_Tactical",
    )
    return text


def _roundtrip(path: Path, transform) -> tuple[int, int]:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")
    work = text.replace("\r\n", "\n") if newline == "\r\n" else text
    updated = transform(work)
    out = updated.replace("\n", "\r\n") if newline == "\r\n" else updated
    encoded = out.encode("utf-8")
    return raw, encoded


def main() -> int:
    items_raw, items_out = _roundtrip(ITEMS, apply_items)
    meta_raw, meta_out = _roundtrip(META, apply_meta)
    if "--apply" in sys.argv:
        ITEMS.write_bytes(items_out)
        META.write_bytes(meta_out)
        print(f"applied items {len(items_out) - len(items_raw):+d} meta {len(meta_out) - len(meta_raw):+d}")
    else:
        print(
            f"dry-run items {len(items_out) - len(items_raw):+d} "
            f"meta {len(meta_out) - len(meta_raw):+d}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
