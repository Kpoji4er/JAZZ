# -*- coding: utf-8 -*-
"""Dump Ernie sector InitialSquads + design-Normal UnitCountMin sums.

Canon source: ModItemSector blocks (not CampaignPreset). Campaign drift is a
separate check in `_audit_ernie_empty_squad_risk.py` / `_sync_ernie_campaign_inits.py`.

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
camp_start = maps.find("PlaceObj('ModItemCampaignPreset'")
if camp_start < 0:
    camp_start = len(maps)
mod_region = maps[:camp_start]


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
        elif f"'Difficulty', \"{ENG_NORMAL_DESIGN}\"" in body or f'Difficulty = "{ENG_NORMAL_DESIGN}"' in body:
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


def moditem_packs(sid: str) -> list[str] | None:
    """Return Init pack ids for ModItemSector, or None if sector missing.

    Empty list = sector exists with no InitialSquads / empty {}.
    Does not cross into the next ModItemSector (loose sectorId…InitialSquads is unsafe).
    """
    m = re.search(rf"'sectorId', \"{re.escape(sid)}\"", mod_region)
    if not m:
        return None
    start = maps.rfind("PlaceObj('ModItemSector'", 0, m.start())
    if start < 0:
        return None
    nxt = maps.find("PlaceObj('ModItemSector'", start + 1)
    end = nxt if 0 < nxt < camp_start else camp_start
    block = maps[start:end]
    im = re.search(r"'InitialSquads', \{([\s\S]*?)\}", block)
    if not im:
        return []
    return re.findall(r'"([^"]+)"', im.group(1))


for sid in SECTORS:
    packs = moditem_packs(sid)
    if packs is None:
        print(f"{sid}\t—\t(no ModItemSector)")
        continue
    if not packs:
        print(f"{sid}\t0\t(empty / no InitialSquads)")
        continue
    parts = []
    total = 0
    for i in packs:
        n = squad_sum.get(i)
        if n is None:
            parts.append(f"{i}(?)")
        else:
            parts.append(f"{i}({n})")
            total += n
    print(f"{sid}\t{total}\t{'; '.join(parts)}")
