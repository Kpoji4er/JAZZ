# -*- coding: utf-8 -*-
"""Audit Ernie Extra packs vs UNITS-007 + vanilla one-type-per-slot spawn."""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
text = UNITS.read_text(encoding="utf-8")
maps = MAPS.read_text(encoding="utf-8")

# Spec-ish expectations from apply script / baseline
EXPECT = {
    "LegionExtra_Ernie_Marksmen": {"lo": 6, "hi": 8, "kind": "specialty"},
    "LegionExtra_Ernie_Gunners": {"lo": 6, "hi": 8, "kind": "specialty"},
    "LegionExtra_Ernie_Grenadiers": {"lo": 5, "hi": 7, "kind": "specialty"},
    "LegionExtra_Ernie_Veterans": {"lo": 5, "hi": 7, "kind": "specialty"},
    "LegionExtra_Ernie_Melee": {"lo": 6, "hi": 8, "kind": "specialty"},
    "LegionExtra_Ernie_Flankers": {"lo": 6, "hi": 8, "kind": "specialty"},
    "LegionExtra_Ernie_Mixed": {"lo": 6, "hi": 9, "kind": "mixed"},
}


def extract_block(sid: str) -> str | None:
    idx = text.find(f'id = "{sid}"')
    if idx < 0:
        return None
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    if start < 0:
        return None
    mid = text[start:idx]
    if mid.count("PlaceObj('ModItem") != 1:
        return None
    return mid


def analyze(sid: str, block: str) -> dict:
    slots = []
    for m in re.finditer(
        r"PlaceObj\('EnemySquadUnit', \{([\s\S]*?)\n\t\t\t\t\t\}\),",
        block,
    ):
        body = m.group(1)
        lo = re.search(r"'UnitCountMin', (\d+)", body)
        hi = re.search(r"'UnitCountMax', (\d+)", body)
        types = re.findall(r"'unitType', \"([^\"]+)\"", body)
        slots.append(
            {
                "lo": int(lo.group(1)) if lo else None,
                "hi": int(hi.group(1)) if hi else None,
                "types": types,
                "n_types": len(types),
            }
        )
    min_sum = sum(s["lo"] or 0 for s in slots)
    max_sum = sum(s["hi"] or 0 for s in slots)
    # mono risk: any slot with >1 count and >1 pool types → all clones of one roll
    mono_risk = [
        s
        for s in slots
        if (s["hi"] or 0) > 1 and (s["n_types"] or 0) > 1
    ]
    return {
        "slots": len(slots),
        "min_sum": min_sum,
        "max_sum": max_sum,
        "mono_risk_slots": len(mono_risk),
        "detail": slots,
    }


print("=== Extra packs ===")
for sid, exp in EXPECT.items():
    block = extract_block(sid)
    if not block:
        print(f"MISSING {sid}")
        continue
    a = analyze(sid, block)
    ok_size = a["min_sum"] >= exp["lo"] and a["max_sum"] <= exp["hi"] or (
        a["min_sum"] == exp["lo"] and a["max_sum"] == exp["hi"]
    )
    # looser: range should match design lo..hi as total capacity
    size_match = a["min_sum"] == exp["lo"] and a["max_sum"] == exp["hi"]
    mixed_ok = True
    if exp["kind"] == "mixed":
        # mixed must not have mono_risk; prefer many 1-count slots
        mixed_ok = a["mono_risk_slots"] == 0
    print(
        f"{sid}: slots={a['slots']} sum={a['min_sum']}-{a['max_sum']} "
        f"expect={exp['lo']}-{exp['hi']} size_ok={size_match} "
        f"mono_risk={a['mono_risk_slots']} mixed_ok={mixed_ok}"
    )
    if a["mono_risk_slots"] and exp["kind"] == "mixed":
        print("  FAIL mixed mono")
    if a["mono_risk_slots"] and exp["kind"] == "specialty":
        print(
            "  NOTE specialty: one roll×N is OK for themed Extra "
            "(all marksmen etc.); pool only picks which subtype"
        )

print("\n=== ModItemSector InitialSquads Extra refs ===")
for m in re.finditer(
    r"'sectorId', \"([^\"]+)\"[\s\S]{0,2500}?'InitialSquads', \{([\s\S]*?)\},",
    maps,
):
    sid, body = m.group(1), m.group(2)
    ids = re.findall(r'"([^"]+)"', body)
    extras = [i for i in ids if i.startswith("LegionExtra_Ernie_")]
    if extras or sid in {
        "M4",
        "M5",
        "M6",
        "I2",
        "I3",
        "I4",
        "L2",
        "L6",
        "L6_Underground",
    }:
        print(f"  {sid}: {ids}")
