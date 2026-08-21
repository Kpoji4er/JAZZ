# -*- coding: utf-8 -*-
"""Historical Mixed-only split. Canon: _apply_ernie_overflow_inits.py --extras-only."""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

POOL = [
    "JAZZ_Legion_GunnerT1_Gunner",
    "JAZZ_Legion_FrontT2_Marksman",
    "JAZZ_Legion_AssaultT1_Grenadier",
    "JAZZ_Legion_FrontT2_Raider",
    "JAZZ_Legion_AssaultT1_Crusher",
    "JAZZ_Legion_FlankerT2_Scout",
]


def one_slot(lo: int, hi: int) -> str:
    weights = "\n".join(
        "\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {\n"
        f'\t\t\t\t\t\t\t\t\'unitType\', "{ut}",\n'
        "\t\t\t\t\t\t\t}),"
        for ut in POOL
    )
    return (
        "\t\t\t\t\tPlaceObj('EnemySquadUnit', {\n"
        "\t\t\t\t\t\t'weightedList', {\n"
        f"{weights}\n"
        "\t\t\t\t\t\t},\n"
        f"\t\t\t\t\t\t'UnitCountMin', {lo},\n"
        f"\t\t\t\t\t\t'UnitCountMax', {hi},\n"
        "\t\t\t\t\t}),"
    )


# 6× guaranteed independent + 3× optional (0–1) → total 6–9, each present unit rolled alone
NEW_UNITS = "\n".join([one_slot(1, 1) for _ in range(6)] + [one_slot(0, 1) for _ in range(3)])

raw = UNITS.read_bytes()
nl = b"\r\n" if b"\r\n" in raw else b"\n"
text = raw.decode("utf-8")

idx = text.find('id = "LegionExtra_Ernie_Mixed"')
if idx < 0:
    raise SystemExit("missing LegionExtra_Ernie_Mixed")
start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
m = re.search(r"Units = \{", text[start:idx])
if not m:
    raise SystemExit("no Units")
us = start + m.start()
i = us + len("Units = ")
assert text[i] == "{"
depth = 1
j = i + 1
while j < len(text) and depth:
    if text[j] == "{":
        depth += 1
    elif text[j] == "}":
        depth -= 1
    j += 1
# j points past closing }; replace Units = { ... }
new_block = "Units = {\n" + NEW_UNITS + "\n\t\t\t\t\t}"
text2 = text[:us] + new_block + text[j:]
# bump comment
text2 = text2.replace(
    "-- UNITS-007 Extra Mixed 6-9 random specialties",
    "-- UNITS-007 Extra Mixed 6-9; per-unit specialty roll (not one type×N)",
    1,
)
UNITS.write_bytes(text2.replace("\r\n", "\n").replace("\n", nl.decode("ascii")).encode("utf-8"))
print("rewrote LegionExtra_Ernie_Mixed:", 6, "x1 +", 3, "x0-1 slots")
