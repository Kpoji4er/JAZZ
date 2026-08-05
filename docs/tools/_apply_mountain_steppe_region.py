# -*- coding: utf-8 -*-
"""Trim GreatDesert + add MountainSteppe Region (Горная Степь / D18)."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ITEMS = JAZZ / "items.lua"
META = JAZZ / "metadata.lua"


def sector_list(ranges: list[tuple[str, int, int]]) -> list[str]:
    out: list[str] = []
    for col, a, b in ranges:
        for n in range(a, b + 1):
            out.append(f"{col}{n}")
    return out


def fmt_sectors(sectors: list[str], indent: str = "\t\t\t\t\t") -> str:
    return ",\n".join(f'{indent}"{s}"' for s in sectors)


def replace_region_sectors(text: str, region_id: str, sectors: list[str]) -> str:
    # Find ModItemRegion block ending with id = "region_id"
    pat = re.compile(
        rf"(PlaceObj\('ModItemRegion', \{{.*?Sectors = \{{)(.*?)(\n\t\t\t\t\}},.*?id = \"{re.escape(region_id)}\",)",
        re.S,
    )
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Region {region_id} Sectors block not found")
    body = "\n" + fmt_sectors(sectors) + ","
    return text[: m.start(2)] + body + text[m.end(2) :]


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    if 'id = "MountainSteppe"' in text:
        raise SystemExit("MountainSteppe already present")

    # GreatDesert after trim
    gd = sector_list(
        [
            ("A", 1, 8),
            ("B", 4, 8),
            ("C", 6, 7),
            ("D", 7, 12),
        ]
    ) + ["E10"] + sector_list(
        [
            ("F", 8, 12),
            ("G", 9, 12),
            ("H", 10, 13),
            ("I", 11, 13),
            ("J", 12, 13),
        ]
    )
    text = replace_region_sectors(text, "GreatDesert", gd)

    ms = sector_list(
        [
            ("A", 9, 20),
            ("B", 9, 20),
            ("C", 8, 20),
            ("D", 11, 20),
            ("E", 12, 20),
            ("F", 18, 19),
        ]
    )
    # Ensure D18 in list (already in D11-D20)
    assert "D18" in ms

    region = f"""\t\t\tPlaceObj('ModItemRegion', {{
\t\t\t\tDisplayName = \"Горная Степь\",
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
\t\t\t\t\t\"D18\",
\t\t\t\t}},
\t\t\t\tSectors = {{
{fmt_sectors(ms)},
\t\t\t\t}},
\t\t\t\tShipmentSquads = {{
\t\t\t\t\t\"LegionGlobalAI_Convoy\",
\t\t\t\t}},
\t\t\t\tSupplySquads = {{
\t\t\t\t\t\"LegionGlobalAI_Convoy\",
\t\t\t\t}},
\t\t\t\tgroup = \"Default\",
\t\t\t\tid = \"MountainSteppe\",
\t\t\t}}),
"""

    marker = '\t\t\t\tid = "GreatDesert",\n\t\t\t}),\n\t\t\t}),'
    if marker not in text:
        raise SystemExit("GreatDesert end marker not found")
    text = text.replace(
        marker,
        '\t\t\t\tid = "GreatDesert",\n\t\t\t}),\n' + region + "\t\t\t}),",
        1,
    )
    ITEMS.write_text(text, encoding="utf-8")
    print(f"GreatDesert sectors={len(gd)}; MountainSteppe sectors={len(ms)}")

    mt = META.read_text(encoding="utf-8")
    if "MountainSteppe" not in mt:
        old = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"GreatDesert\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        ins = old + """
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"MountainSteppe\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        if old not in mt:
            raise SystemExit("metadata GreatDesert missing")
        META.write_text(mt.replace(old, ins, 1), encoding="utf-8")
        print("metadata: MountainSteppe added")
    else:
        print("metadata: MountainSteppe already present")


if __name__ == "__main__":
    main()
