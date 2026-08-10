# -*- coding: utf-8 -*-
"""Find EnemySquad packs that can spawn 0 units on a given engine difficulty."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
text = UNITS.read_text(encoding="utf-8")
maps = MAPS.read_text(encoding="utf-8")

camp_start = maps.find("PlaceObj('ModItemCampaignPreset'")
if camp_start < 0:
    camp_start = len(maps)
camp_end = maps.find('id = "HotDiamonds"', camp_start)
if camp_end < 0:
    camp_end = len(maps)

_BETWEEN_ID = r"(?:(?!'Id', \")[\s\S])*?"

ERNIE_KEYS = (
    "M4", "M5", "M6",
    "I2", "I3", "I4", "I5", "I7",
    "J5",
    "K3", "K5",
    "L1", "L2", "L3", "L4", "L5", "L6", "L6_Underground",
)
CLEAR_KEYS = ("I6", "J6", "L7", "K4", "K6")


def moditem_packs(sid: str) -> list[str] | None:
    region = maps[:camp_start]
    m = re.search(rf"'sectorId', \"{re.escape(sid)}\"", region)
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


def campaign_packs(sid: str) -> list[str] | None:
    camp = maps[camp_start:camp_end]
    m = re.search(
        rf"'Id', \"{re.escape(sid)}\"{_BETWEEN_ID}'InitialSquads', \{{([\s\S]*?)\}}",
        camp,
    )
    if not m:
        return None
    return re.findall(r'"([^"]+)"', m.group(1))


INIT_IDS: set[str] = set()
for sid in ERNIE_KEYS + CLEAR_KEYS:
    for packs in (moditem_packs(sid), campaign_packs(sid)):
        if packs:
            INIT_IDS.update(packs)


def squad_block(sid: str) -> str | None:
    idx = text.find(f'id = "{sid}"')
    if idx < 0:
        return None
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    if start < 0 or text[start:idx].count("PlaceObj('ModItem") != 1:
        return None
    return text[start:idx]


def sum_for(block: str, eng: str) -> tuple[int, int, int]:
    """Return (min_sum, max_sum, ungated_or_matching_slots)."""
    mn = mx = slots = 0
    for m in re.finditer(
        r"PlaceObj\('EnemySquadUnit', \{([\s\S]*?)\n\t\t\t\t\t\}\),",
        block,
    ):
        body = m.group(1)
        lo = re.search(r"'UnitCountMin', (\d+)", body)
        hi = re.search(r"'UnitCountMax', (\d+)", body)
        if not lo:
            continue
        nlo, nhi = int(lo.group(1)), int(hi.group(1)) if hi else int(lo.group(1))
        if "CheckDifficulty" not in body:
            mn += nlo
            mx += nhi
            slots += 1
            continue
        diffs = set(re.findall(r"'Difficulty', \"(\w+)\"", body))
        diffs |= set(re.findall(r'Difficulty = "(\w+)"', body))
        if eng in diffs:
            mn += nlo
            mx += nhi
            slots += 1
    return mn, mx, slots


print("=== Ernie Init squads that can be EMPTY on engine difficulty ===")
for sid in sorted(INIT_IDS):
    block = squad_block(sid)
    if not block:
        # FortressPierre etc. may be vanilla-only
        print(f"MISSING DEF (mod): {sid}")
        continue
    for eng in ("Normal", "Hard", "VeryHard"):
        mn, mx, slots = sum_for(block, eng)
        if mn == 0:
            print(f"EMPTY RISK {sid} @ {eng}: min={mn} max={mx} matching_slots={slots}")
    if "CheckDifficulty" in block:
        n = sum_for(block, "Normal")
        h = sum_for(block, "Hard")
        vh = sum_for(block, "VeryHard")
        ungated_slots = 0
        for m in re.finditer(
            r"PlaceObj\('EnemySquadUnit', \{([\s\S]*?)\n\t\t\t\t\t\}\),",
            block,
        ):
            if "CheckDifficulty" not in m.group(1):
                ungated_slots += 1
        if ungated_slots == 0:
            print(
                f"{sid}: fully gated; Normal={n[0]}-{n[1]} Hard={h[0]}-{h[1]} VH={vh[0]}-{vh[1]}"
            )

print("\n=== CampaignPreset vs ModItemSector Init drift (Ernie keys) ===")
drift = 0
for sid in ERNIE_KEYS:
    mod = moditem_packs(sid)
    camp = campaign_packs(sid)
    if mod is None and camp is None:
        continue
    if (mod or []) != (camp or []):
        print(f"  DRIFT {sid}: ModItem={mod} Campaign={camp}")
        drift += 1
    else:
        print(f"  OK {sid}: {mod}")
for sid in CLEAR_KEYS:
    mod = moditem_packs(sid)
    camp = campaign_packs(sid)
    bad_m = bool(mod)
    bad_c = bool(camp)
    if bad_m or bad_c:
        print(f"  CLEAR-FAIL {sid}: ModItem={mod} Campaign={camp}")
        drift += 1
    else:
        print(f"  OK clear {sid}: ModItem={mod} Campaign={camp}")
print(f"drift_count={drift}")
