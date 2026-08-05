# -*- coding: utf-8 -*-
"""Add FleatownEnvirons Region; drop F18 from MountainSteppe (overlap)."""
from __future__ import annotations

from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
ITEMS = JAZZ / "items.lua"
META = JAZZ / "metadata.lua"


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
    if 'id = "FleatownEnvirons"' in text:
        raise SystemExit("FleatownEnvirons already present")

    # Drop F18 from MountainSteppe (keep F19)
    old_f = '\t\t\t\t\t"F18",\n\t\t\t\t\t"F19",\n\t\t\t\t},\n\t\t\t\tShipmentSquads = {\n\t\t\t\t\t"LegionGlobalAI_Convoy",\n\t\t\t\t},\n\t\t\t\tSupplySquads = {\n\t\t\t\t\t"LegionGlobalAI_Convoy",\n\t\t\t\t},\n\t\t\t\tgroup = "Default",\n\t\t\t\tid = "MountainSteppe",'
    new_f = '\t\t\t\t\t"F19",\n\t\t\t\t},\n\t\t\t\tShipmentSquads = {\n\t\t\t\t\t"LegionGlobalAI_Convoy",\n\t\t\t\t},\n\t\t\t\tSupplySquads = {\n\t\t\t\t\t"LegionGlobalAI_Convoy",\n\t\t\t\t},\n\t\t\t\tgroup = "Default",\n\t\t\t\tid = "MountainSteppe",'
    if old_f not in text:
        raise SystemExit("MountainSteppe F18/F19 block not found")
    text = text.replace(old_f, new_f, 1)

    secs = sector_list(
        [
            ("F", 14, 18),
            ("G", 14, 18),
            ("H", 14, 19),
            ("I", 14, 19),
            ("J", 14, 19),
        ]
    )
    assert "H19" in secs and "F18" in secs

    region = f"""\t\t\tPlaceObj('ModItemRegion', {{
\t\t\t\tDisplayName = \"Окрестности Флитауна\",
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
\t\t\t\t\t\"H19\",
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
\t\t\t\tid = \"FleatownEnvirons\",
\t\t\t}}),
"""

    marker = '\t\t\t\tid = "SeagullIsland",\n\t\t\t}),\n\t\t\t}),'
    if marker not in text:
        raise SystemExit("SeagullIsland end marker not found")
    text = text.replace(
        marker,
        '\t\t\t\tid = "SeagullIsland",\n\t\t\t}),\n' + region + "\t\t\t}),",
        1,
    )
    ITEMS.write_text(text, encoding="utf-8")
    print(f"FleatownEnvirons sectors={len(secs)}; MountainSteppe dropped F18")

    mt = META.read_text(encoding="utf-8")
    if "FleatownEnvirons" not in mt:
        old = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"SeagullIsland\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        ins = old + """
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"FleatownEnvirons\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
        if old not in mt:
            raise SystemExit("metadata SeagullIsland missing")
        META.write_text(mt.replace(old, ins, 1), encoding="utf-8")
        print("metadata: FleatownEnvirons added")


if __name__ == "__main__":
    main()
