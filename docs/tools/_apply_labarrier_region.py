# -*- coding: utf-8 -*-
"""Add LaBarrier + Ernie MajorSupplyPriority; wire L15 Global AI lists."""
from __future__ import annotations

from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps")
ITEMS = JAZZ / "items.lua"
META = JAZZ / "metadata.lua"
MAPS_ITEMS = MAPS / "items.lua"


def sector_list(ranges):
    out = []
    for col, a, b in ranges:
        for n in range(a, b + 1):
            out.append(f"{col}{n}")
    return out


def fmt_sectors(sectors, indent="\t\t\t\t\t"):
    return ",\n".join(f'{indent}"{s}"' for s in sectors)


def main():
    text = ITEMS.read_text(encoding="utf-8")
    if 'id = "LaBarrier"' in text:
        raise SystemExit("LaBarrier already present")

    # ErnieIsland: MajorSupplyPriority = 100
    old_ernie = """\t\t\tPlaceObj('ModItemRegion', {
\t\t\t\tDisplayName = \"Остров Эрни\",
\t\t\t\tLegionAIEnabled = true,
\t\t\t\tMajorHQSector = \"B28\","""
    new_ernie = """\t\t\tPlaceObj('ModItemRegion', {
\t\t\t\tDisplayName = \"Остров Эрни\",
\t\t\t\tLegionAIEnabled = true,
\t\t\t\tMajorHQSector = \"B28\",
\t\t\t\tMajorSupplyPriority = 100,"""
    if old_ernie not in text:
        raise SystemExit("ErnieIsland header not found")
    text = text.replace(old_ernie, new_ernie, 1)

    secs = sector_list([("K", 9, 19), ("L", 11, 19)])
    assert "L15" in secs

    region = f"""\t\t\tPlaceObj('ModItemRegion', {{
\t\t\t\tDisplayName = \"Ла-Барьер\",
\t\t\t\tLateAwakenMinTier = 21,
\t\t\t\tLegionAIEnabled = true,
\t\t\t\tMajorHQSector = \"B28\",
\t\t\t\tMajorSupplyPriority = 80,
\t\t\t\tGarrisonCapBonus = 4,
\t\t\t\tPatrolCap = 4,
\t\t\t\tStartingManpower = 0,
\t\t\t\tStartingSupply = 0,
\t\t\t\tExportPatrolRegionIds = {{
\t\t\t\t\t\"PortCacaoEnvirons\",
\t\t\t\t\t\"FleatownEnvirons\",
\t\t\t\t}},
\t\t\t\tMajorResponseSquads = {{
\t\t\t\t\t\"LegionJAZZSquadT3\",
\t\t\t\t\t\"LegionHeavyTroops\",
\t\t\t\t}},
\t\t\t\tManagedOutposts = {{
\t\t\t\t\t\"L15\",
\t\t\t\t}},
\t\t\t\tSectors = {{
{fmt_sectors(secs)},
\t\t\t\t}},
\t\t\t\tShipmentSquads = {{
\t\t\t\t\t\"LegionGlobalAI_Convoy\",
\t\t\t\t}},
\t\t\t\tSupplySquads = {{
\t\t\t\t\t\"LegionGlobalAI_Convoy\",
\t\t\t\t}},
\t\t\t\tgroup = \"Default\",
\t\t\t\tid = \"LaBarrier\",
\t\t\t}}),
"""

    marker = '\t\t\t\tid = "FleatownEnvirons",\n\t\t\t}),\n\t\t\t}),'
    if marker not in text:
        # maybe order different — try after Seagull
        marker = '\t\t\t\tid = "FleatownEnvirons",\n\t\t\t}),\n\t\t\t}),'
    if marker not in text:
        raise SystemExit("FleatownEnvirons end marker not found")
    text = text.replace(
        marker,
        '\t\t\t\tid = "FleatownEnvirons",\n\t\t\t}),\n' + region + "\t\t\t}),",
        1,
    )
    ITEMS.write_text(text, encoding="utf-8")
    print(f"LaBarrier sectors={len(secs)}; Ernie MajorSupplyPriority=100")

    mt = META.read_text(encoding="utf-8")
    if "LaBarrier" not in mt:
        old = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"FleatownEnvirons\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        ins = old + """
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"LaBarrier\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        if old not in mt:
            raise SystemExit("metadata FleatownEnvirons missing")
        META.write_text(mt.replace(old, ins, 1), encoding="utf-8")
        print("metadata: LaBarrier added")

    # Wire L15 Global AI lists (both representations share StrongEnemySquadsList block)
    maps = MAPS_ITEMS.read_text(encoding="utf-8")
    needle = """\t\t\t\t\t'StrongEnemySquadsList', {
\t\t\t\t\t\t\"LegionAttackers_Balanced_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Balanced_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Balanced_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Shock_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Shock_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t},
\t\t\t\t\t'Militia', true,
\t\t\t\t\t'MaxMilitia', 12,
\t\t\t\t\t'ForceConflict', true,
\t\t\t\t\t'InitialSquads', {
\t\t\t\t\t\t\"NightCombatGarrison\",
\t\t\t\t\t\t\"LegionExtraSquadFireArms\",
\t\t\t\t\t\t\"LegionExtraSquadFireArms_T2\",
\t\t\t\t\t\t\"LegionExtraSquadMelee_T2\",
\t\t\t\t\t},"""
    repl = """\t\t\t\t\t'StrongEnemySquadsList', {
\t\t\t\t\t\t\"LegionAttackers_Balanced_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Balanced_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Balanced_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Shock_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Shock_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t\t\"LegionAttackers_Ordnance_Hard\",
\t\t\t\t\t},
\t\t\t\t\t'EnemySquadsGarrisonList', {
\t\t\t\t\t\t\"LegionGlobalAI_Garrison\",
\t\t\t\t\t},
\t\t\t\t\t'EnemySquadsPatroolList', {
\t\t\t\t\t\t\"LegionGlobalAI_Patrol\",
\t\t\t\t\t},
\t\t\t\t\t'EnemySquadsReconList', {
\t\t\t\t\t\t\"LegionGlobalAI_Recon\",
\t\t\t\t\t},
\t\t\t\t\t'EnemySquadsQRFList', {
\t\t\t\t\t\t\"LegionJAZZSquadT2\",
\t\t\t\t\t},
\t\t\t\t\t'Militia', true,
\t\t\t\t\t'MaxMilitia', 12,
\t\t\t\t\t'ForceConflict', true,
\t\t\t\t\t'InitialSquads', {
\t\t\t\t\t\t\"NightCombatGarrison\",
\t\t\t\t\t\t\"LegionExtraSquadFireArms\",
\t\t\t\t\t\t\"LegionExtraSquadFireArms_T2\",
\t\t\t\t\t\t\"LegionExtraSquadMelee_T2\",
\t\t\t\t\t},"""
    if "EnemySquadsGarrisonList" in maps and maps.count("NightCombatGarrison") >= 1:
        # only replace if L15 block not yet wired — count occurrences of needle
        n = maps.count(needle)
        if n == 0:
            print("maps: L15 strong-list needle not found (maybe already wired)")
        else:
            maps = maps.replace(needle, repl)
            MAPS_ITEMS.write_text(maps, encoding="utf-8")
            print(f"maps: wired L15 Global AI lists ({n} occurrences)")


if __name__ == "__main__":
    main()
