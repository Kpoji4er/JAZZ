"""Tighten Villa Sentry + Attackers so sector Init (Sentry+Attacker) is Normal base 20–30.

Targets (Normal base; Easy = base−10 / Hard = base+10 when settings exist):
  SentryAroundVilla: 10
  VillaAttackers_K3: 12  → K3 = 22
  VillaAttackers_K5: 13  → K5 = 23
  VillaAttackers_L3: 14  → L3 = 24
  VillaAttackers_L4: 15  → L4 = 25
  VillaAttackers_L5: 16  → L5 = 26
Variance: ±1 only on one meat slot where noted (keeps sector in 20–30).
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")


def slot(types: list[tuple[str, int | None]], lo: int, hi: int | None = None) -> str:
    hi = lo if hi is None else hi
    lines = ["\t\t\t\t\tPlaceObj('EnemySquadUnit', {", "\t\t\t\t\t\t'weightedList', {"]
    for ut, w in types:
        lines.append("\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {")
        lines.append(f'\t\t\t\t\t\t\t\t\'unitType\', "{ut}",')
        if w is not None:
            lines.append(f"\t\t\t\t\t\t\t\t'spawnWeight', {w},")
        lines.append("\t\t\t\t\t\t\t}),")
    lines.append("\t\t\t\t\t\t},")
    lines.append(f"\t\t\t\t\t\t'UnitCountMin', {lo},")
    lines.append(f"\t\t\t\t\t\t'UnitCountMax', {hi},")
    lines.append("\t\t\t\t\t}),")
    return "\n".join(lines)


def units_block(slots: list[str]) -> str:
    return "Units = {\n" + "\n".join(slots) + "\n\t\t\t\t},"


MEAT = [
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
    ("JAZZ_Legion_AssaultT1_Grenadier", None),
    ("JAZZ_Legion_AssaultT1_Crusher", None),
]
AMBUSH = [
    ("JAZZ_Legion_FrontT2_Ambusher", None),
    ("JAZZ_Legion_FrontT3_Sniper", 50),
    ("JAZZ_Legion_FrontT2_Raider", 50),
    ("JAZZ_Legion_FlankerT2_Skirmisher", None),
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_FrontT1_Bonemaker", None),
]
RAID = [
    ("JAZZ_Legion_FrontT2_Raider", None),
    ("JAZZ_Legion_AssaultT2_Pillager", 50),
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
]
SHOCK = [
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
    ("JAZZ_Legion_FrontT2_Marksman", 50),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_FrontT1_Marauder", None),
]
SHOCK_VET = SHOCK + [("JAZZ_Legion_FrontT3_Veteran", None)]
CRUSH = [
    ("JAZZ_Legion_AssaultT1_Crusher", None),
    ("JAZZ_Legion_AssaultT1_Grenadier", 50),
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
]
PYRO = [
    ("JAZZ_Legion_AssaultT2_Pillager", None),
    ("JAZZ_Legion_AssaultT2_Pyro", 50),
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
]
HEAVY_ASSAULT = [
    ("JAZZ_Legion_FrontT2_Raider", None),
    ("JAZZ_Legion_AssaultT2_Pillager", 50),
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
    ("JAZZ_Legion_AssaultT1_Crusher", None),
]
LIGHT = [
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_FrontT1_Marauder", None),
]
GMPG = [
    ("JAZZ_Legion_GunnerT2_GMPG", None),
    ("JAZZ_Legion_GunnerT3_VeteranGunner", 25),
]

# Sentry Normal base 10 (Easy 0 / Hard 20 later via ±10 on sector or pack).
SQUADS = {
    "JAZZ_Legion_SentrySquad_AroundVilla": units_block(
        [
            slot([("JAZZ_Legion_FlankerT2_Scout", 30)], 1),
            slot(
                [
                    ("JAZZ_Legion_FlankerT1_Warden", None),
                    ("JAZZ_Legion_FlankerT2_Scout", 30),
                ],
                2,
            ),
            slot(
                [
                    ("JAZZ_Legion_FlankerT1_Warden", None),
                    ("JAZZ_Legion_FlankerT2_Scout", 30),
                    ("JAZZ_Legion_FlankerT2_Skirmisher", 50),
                ],
                1,
            ),
            slot([("JAZZ_Legion_FrontT1_Bonemaker", None)], 1),
            slot(MEAT, 3),
            slot(MEAT, 1),
            slot([("JAZZ_Legion_GunnerT1_Gunner", None)], 1),  # Sentry base 10
        ]
    ),
}

SQUADS["JAZZ_Legion_VillaAttackers_K3"] = units_block(
    [
        slot([("JAZZ_Legion_FlankerT4_Ranger", None)], 1),
        slot(AMBUSH, 3),
        slot(AMBUSH, 3),
        slot(AMBUSH, 3),
        slot(AMBUSH, 2),  # 12
    ]
)

SQUADS["JAZZ_Legion_VillaAttackers_K5"] = units_block(
    [
        slot([("JAZZ_Legion_LeaderT3_Captain", None)], 1),
        slot(
            [
                ("JAZZ_Legion_AssaultT2_Pillager", 50),
                ("JAZZ_Legion_AssaultT1_Roughneck", None),
            ],
            3,
        ),
        slot([("JAZZ_Legion_AssaultT1_Roughneck", None)], 3),
        slot(
            [
                ("JAZZ_Legion_FrontT2_Raider", None),
                ("JAZZ_Legion_AssaultT1_Roughneck", None),
            ],
            3,
        ),
        slot(SHOCK_VET, 2),
        slot(GMPG, 1),  # 13
    ]
)

SQUADS["JAZZ_Legion_VillaAttackers_L3"] = units_block(
    [
        slot([("JAZZ_Legion_LeaderT2_Lieutenant", None)], 1),
        slot(RAID, 3),
        slot(RAID, 3),
        slot(RAID, 3),
        slot(SHOCK, 2),
        slot(SHOCK, 1),
        slot(GMPG, 1),  # 14; was dual MG
    ]
)

SQUADS["JAZZ_Legion_VillaAttackers_L4"] = units_block(
    [
        slot([("JAZZ_Legion_LeaderT1_Sergeant", None)], 1),
        slot(CRUSH, 3),
        slot(CRUSH, 3),
        slot(CRUSH, 2),
        slot(PYRO, 2),
        slot(PYRO, 2),
        slot([("JAZZ_Legion_GunnerT2_AssaultGunner", 50)], 1),
        slot([("JAZZ_Legion_HeavyT1_Rocketeer", None)], 1),  # 15; no GL in pool
    ]
)

SQUADS["JAZZ_Legion_VillaAttackers_L5"] = units_block(
    [
        slot([("JAZZ_Legion_AssaultT4_Headsman", None)], 1),
        slot(
            [
                ("JAZZ_Legion_FrontT2_Raider", None),
                ("JAZZ_Legion_AssaultT2_Pillager", 50),
                ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
                ("JAZZ_Legion_AssaultT2_Pyro", None),
            ],
            3,
        ),
        slot(HEAVY_ASSAULT, 3),
        slot(HEAVY_ASSAULT, 3),
        slot(LIGHT, 2),
        slot(LIGHT, 2),
        slot(GMPG, 1),
        slot([("JAZZ_Legion_HeavyT3_Mortarman", None)], 1),  # 16
    ]
)


def replace_units(text: str, squad_id: str, new_units: str, comment: str | None = None) -> str:
    idx = text.find(f'id = "{squad_id}"')
    if idx < 0:
        raise SystemExit(f"missing {squad_id}")
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    if comment:
        chunk = text[start:idx]
        chunk2, n = re.subn(r'Comment = "[^"]*"', f'Comment = "{comment}"', chunk, count=1)
        if n != 1:
            raise SystemExit(f"comment fail {squad_id}")
        text = text[:start] + chunk2 + text[idx:]
        idx = text.find(f'id = "{squad_id}"')
        start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    u0 = text.find("Units = {", start, idx)
    if u0 < 0:
        raise SystemExit(f"Units not found for {squad_id}")
    i = text.find("{", u0)
    depth = 0
    j = i
    while j < idx:
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    else:
        raise SystemExit(f"Units brace fail {squad_id}")
    end = j
    if text[end : end + 1] == ",":
        end += 1
    return text[:u0] + new_units + text[end:]


COMMENTS = {
    "JAZZ_Legion_SentrySquad_AroundVilla": "Villa sentry Normal base 10; sector+Attacker 22-26; Easy/Hard +-10",
    "JAZZ_Legion_VillaAttackers_K3": "Villa attackers K3 Normal base 12 (sector 22; Easy/Hard +-10)",
    "JAZZ_Legion_VillaAttackers_K5": "Villa attackers K5 Normal base 13 (sector 23; Easy/Hard +-10)",
    "JAZZ_Legion_VillaAttackers_L3": "Villa attackers L3 Normal base 14 (sector 24; Easy/Hard +-10)",
    "JAZZ_Legion_VillaAttackers_L4": "Villa attackers L4 Normal base 15 (sector 25; Easy/Hard +-10)",
    "JAZZ_Legion_VillaAttackers_L5": "Villa attackers L5 Normal base 16 (sector 26; Easy/Hard +-10)",
}


def main() -> None:
    text = UNITS.read_text(encoding="utf-8")
    for sid, block in SQUADS.items():
        text = replace_units(text, sid, block, COMMENTS.get(sid))
        print("patched", sid)
    UNITS.write_text(text, encoding="utf-8")
    print("wrote", UNITS)


if __name__ == "__main__":
    main()