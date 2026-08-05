# -*- coding: utf-8 -*-
"""Apply GreatDesert Region + PortCacao late-awaken fields (STRATEGY-021)."""
from pathlib import Path

jazz = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\items.lua")
text = jazz.read_text(encoding="utf-8")

old_pc = """\t\t\tPlaceObj('ModItemRegion', {
\t\t\t\tDisplayName = \"Окрестности Порта Какао\",
\t\t\t\tLegionAIEnabled = true,
\t\t\t\tMajorHQSector = \"B28\","""

new_pc = """\t\t\tPlaceObj('ModItemRegion', {
\t\t\t\tDisplayName = \"Окрестности Порта Какао\",
\t\t\t\tLateAwakenMinTier = 21,
\t\t\t\tLegionAIEnabled = true,
\t\t\t\tMajorHQSector = \"B28\",
\t\t\t\tStartingManpower = 0,
\t\t\t\tStartingSupply = 0,"""

if old_pc not in text:
    raise SystemExit("PortCacao block not found")
if "id = \"GreatDesert\"" in text:
    print("GreatDesert already in items.lua")
else:
    text = text.replace(old_pc, new_pc, 1)

    sectors = []

    def add(col, a, b):
        for n in range(a, b + 1):
            sectors.append(f"{col}{n}")

    add("A", 1, 12)
    add("B", 4, 12)
    add("C", 6, 12)
    add("D", 7, 12)
    sectors.append("E10")
    add("F", 8, 12)
    add("G", 9, 12)
    add("H", 10, 13)
    add("I", 11, 13)
    add("J", 12, 13)
    sec_lines = ",\n".join(f'\t\t\t\t\t"{s}"' for s in sectors)

    great = f"""\t\t\tPlaceObj('ModItemRegion', {{
\t\t\t\tDisplayName = \"Великая Пустыня\",
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
\t\t\t\t\t\"E10\",
\t\t\t\t}},
\t\t\t\tSectors = {{
{sec_lines},
\t\t\t\t}},
\t\t\t\tShipmentSquads = {{
\t\t\t\t\t\"LegionGlobalAI_Convoy\",
\t\t\t\t}},
\t\t\t\tSupplySquads = {{
\t\t\t\t\t\"LegionGlobalAI_Convoy\",
\t\t\t\t}},
\t\t\t\tgroup = \"Default\",
\t\t\t\tid = \"GreatDesert\",
\t\t\t}}),
"""

    marker = '\t\t\t\tid = "PortCacaoEnvirons",\n\t\t\t}),\n\t\t\t}),'
    if marker not in text:
        raise SystemExit("PortCacao end marker not found")
    text = text.replace(
        marker,
        '\t\t\t\tid = "PortCacaoEnvirons",\n\t\t\t}),\n' + great + "\t\t\t}),",
        1,
    )
    jazz.write_text(text, encoding="utf-8")
    print(f"jazz items: PortCacao patched + GreatDesert inserted ({len(sectors)} sectors)")

meta = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\metadata.lua")
mt = meta.read_text(encoding="utf-8")
if "GreatDesert" in mt:
    print("metadata: GreatDesert already present")
else:
    old = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"PortCacaoEnvirons\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
    ins = old + """
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"Region\",
\t\t\t'Id', \"GreatDesert\",
\t\t\t'ClassDisplayName', \"Region\",
\t\t}),"""
    if old not in mt:
        raise SystemExit("metadata PortCacao resource missing")
    meta.write_text(mt.replace(old, ins, 1), encoding="utf-8")
    print("metadata: GreatDesert resource added")
