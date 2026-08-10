"""Dump Ernie sector InitialSquads + design-Normal UnitCountMin sums.

For difficulty-gated packs (CheckDifficulty):
  design Easy   -> engine Normal
  design Normal -> engine Hard   <-- default dump column
  design Hard   -> engine VeryHard
Ungated slots always count.
"""
from __future__ import annotations

import re
from pathlib import Path

MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

ENG_NORMAL_DESIGN = "Hard"  # design Normal

maps = MAPS.read_text(encoding="utf-8")
units = UNITS.read_text(encoding="utf-8")


def squad_design_normal_sum(block: str) -> int:
    total = 0
    for m in re.finditer(
        r"PlaceObj\('EnemySquadUnit', \{([\s\S]*?)\n\t\t\t\t\t\}\),",
        block,
    ):
        body = m.group(1)
        lo = re.search(r"'UnitCountMin', (\d+)", body)
        if not lo:
            continue
        n = int(lo.group(1))
        if "CheckDifficulty" not in body:
            total += n
        elif f"'Difficulty', \"{ENG_NORMAL_DESIGN}\"" in body:
            total += n
    return total


squad_sum: dict[str, int] = {}
for sid_m in re.finditer(r'id = "([^"]+)"', units):
    sid = sid_m.group(1)
    pos = sid_m.start()
    start = units.rfind("PlaceObj('ModItemEnemySquads'", 0, pos)
    if start < 0:
        continue
    mid = units[start:pos]
    if mid.count("PlaceObj('ModItem") != 1:
        continue
    squad_sum[sid] = squad_design_normal_sum(mid)

SECTORS = [
    "M1", "M2", "M3", "M4", "M5", "M6",
    "I2", "I3", "I4", "I5", "I6", "I6_Underground", "I7",
    "J4", "J5", "J6", "J7",
    "K3", "K4", "K5", "K6",
    "L1", "L2", "L3", "L4", "L5", "L6", "L6_Underground", "L7",
]

for sid in SECTORS:
    hits = list(
        re.finditer(
            rf"'sectorId', \"{re.escape(sid)}\"[\s\S]{{0,2000}}?'InitialSquads', \{{([\s\S]*?)\}},",
            maps,
        )
    )
    if not hits:
        print(f"{sid}\t—\t(no InitialSquads block)")
        continue
    for h in hits:
        ids = re.findall(r'"([^"]+)"', h.group(1))
        if not ids:
            print(f"{sid}\t0\t(empty)")
            continue
        parts = []
        total = 0
        for i in ids:
            n = squad_sum.get(i)
            if n is None:
                parts.append(f"{i}(?)")
            else:
                parts.append(f"{i}({n})")
                total += n
        print(f"{sid}\t{total}\t{'; '.join(parts)}")
