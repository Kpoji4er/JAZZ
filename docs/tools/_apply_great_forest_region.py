# -*- coding: utf-8 -*-
"""Add GreatForest Region (G22+K21); wire Global AI lists on both outposts."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps")
ITEMS = JAZZ / "items.lua"
META = JAZZ / "metadata.lua"
MAPS_ITEMS = MAPS / "items.lua"

GLOBAL_AI_LISTS = """\t\t\t\t\t'EnemySquadsGarrisonList', {
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
"""


def sector_list(ranges):
    out = []
    for col, a, b in ranges:
        for n in range(a, b + 1):
            out.append(f"{col}{n}")
    return out


def fmt_sectors(sectors, indent="\t\t\t\t\t"):
    return ",\n".join(f'{indent}"{s}"' for s in sectors)


def wire_sector_lists(maps: str, sector_id: str) -> tuple[str, int]:
    """Insert Global AI lists after StrongEnemySquadsList for each SatelliteSector Id=sector_id."""
    if maps.count(f"'Id', \"{sector_id}\"") == 0:
        raise SystemExit(f"{sector_id} not found in maps items")

    # Already wired?
    already = 0
    for m in re.finditer(rf"'Id',\s*\"{sector_id}\"", maps):
        chunk = maps[m.start() : m.start() + 4000]
        if "EnemySquadsGarrisonList" in chunk and "LegionGlobalAI_Garrison" in chunk:
            already += 1
    if already >= 2 or (already >= 1 and maps.count(f"'Id', \"{sector_id}\"") == already):
        print(f"maps: {sector_id} already has Global AI lists ({already})")
        return maps, 0

    wired = 0
    out = []
    last = 0
    for m in re.finditer(rf"'Id',\s*\"{sector_id}\"", maps):
        # Search Strong→Militia only within this sector block (~4k)
        block_start = m.start()
        block = maps[block_start : block_start + 4000]
        if "EnemySquadsGarrisonList" in block and "LegionGlobalAI_Garrison" in block:
            continue
        sm = re.search(
            r"('StrongEnemySquadsList',\s*\{.*?\n\t\t\t\t\t\},\n)(\t\t\t\t\t'Militia')",
            block,
            re.S,
        )
        if not sm:
            continue
        abs_start = block_start + sm.start(1)
        abs_mid = block_start + sm.end(1)
        abs_end = block_start + sm.end(2)
        # write up to Strong close, insert lists, keep Militia
        out.append(maps[last:abs_mid])
        out.append(GLOBAL_AI_LISTS)
        out.append(maps[abs_mid:abs_end])
        last = abs_end
        wired += 1
    if wired == 0:
        raise SystemExit(f"failed to wire {sector_id} (no Strong→Militia insert point)")
    out.append(maps[last:])
    return "".join(out), wired


def main():
    text = ITEMS.read_text(encoding="utf-8")
    if 'id = "GreatForest"' in text:
        raise SystemExit("GreatForest already present")

    secs = sector_list(
        [
            ("K", 21, 24),
            ("J", 20, 24),
            ("I", 20, 24),
            ("H", 20, 24),
            ("G", 22, 25),
        ]
    )
    assert "G22" in secs and "K21" in secs
    assert len(secs) == 23

    region = f"""\t\t\tPlaceObj('ModItemRegion', {{
\t\t\t\tDisplayName = \"Великий лес\",
\t\t\t\tLateAwakenMinTier = 21,
\t\t\t\tLegionAIEnabled = true,
\t\t\t\tMajorHQSector = \"B28\",
\t\t\t\tStartingManpower = 0,
\t\t\t\tStartingSupply = 0,
\t\t\t\tMajorResponseSquads = {{
\t\t\t\t\t\"LegionJAZZSquadT3\",
\t\t\t\t\t\"LegionHeavyTroops\",
\t\t\t\t}},
\t\t\t\tManagedOutposts = {{
\t\t\t\t\t\"G22\",
\t\t\t\t\t\"K21\",
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
\t\t\t\tid = \"GreatForest\",
\t\t\t}}),
"""

    marker = '\t\t\t\tid = "LaBarrier",\n\t\t\t}),\n\t\t\t}),'
    if marker not in text:
        raise SystemExit("LaBarrier end marker not found")
    text = text.replace(
        marker,
        '\t\t\t\tid = "LaBarrier",\n\t\t\t}),\n' + region + "\t\t\t}),",
        1,
    )
    ITEMS.write_text(text, encoding="utf-8")
    print(f"GreatForest sectors={len(secs)}; outposts G22+K21")

    mt = META.read_text(encoding="utf-8")
    if "GreatForest" not in mt:
        old = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"LaBarrier\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        ins = old + """
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"GreatForest\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        if old not in mt:
            raise SystemExit("metadata LaBarrier missing")
        META.write_text(mt.replace(old, ins, 1), encoding="utf-8")
        print("metadata: GreatForest added")

    maps = MAPS_ITEMS.read_text(encoding="utf-8")
    for sid in ("G22", "K21"):
        maps, n = wire_sector_lists(maps, sid)
        print(f"maps: wired {sid} ({n} occurrences)")
    MAPS_ITEMS.write_text(maps, encoding="utf-8")


if __name__ == "__main__":
    main()
