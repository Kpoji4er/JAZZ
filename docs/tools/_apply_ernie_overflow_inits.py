# -*- coding: utf-8 -*-
"""JAZZ-UNITS-007: Ernie overflow Init — base packs + Extra + I7 FortressDefenders 48 + Deprecated.

Difficulty mapping (JA3 has no Easy GameDifficultyDef):
  design Easy   -> engine Normal
  design Normal -> engine Hard
  design VeryHard wait: design Hard -> engine VeryHard

Size targets (design E/N/H):
  Medium 20/25/40 · Large 30/40/70 · FortressDefenders 38/48/58
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")
UNITS = ROOT / "jazz-units" / "items.lua"
META = ROOT / "jazz-units" / "metadata.lua"
MAPS = ROOT / "jazz-maps" / "items.lua"
JAZZ = ROOT / "jazz"

# engine Difficulty id -> design tier name
ENG_EASY = "Normal"
ENG_NORMAL = "Hard"
ENG_HARD = "VeryHard"

T_BASE = 890000000012500


def T(n: int, name: str, ru: str) -> str:
    return f'T({T_BASE + n}, --[[ModItemEnemySquads {name} displayName]] "{ru}")'


def wentry(ut: str, weight: int | None, eng: str | None) -> str:
    lines = [
        "\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {",
        f'\t\t\t\t\t\t\t\t\'unitType\', "{ut}",',
    ]
    if weight is not None:
        lines.append(f"\t\t\t\t\t\t\t\t'spawnWeight', {weight},")
    if eng is not None:
        lines.append("\t\t\t\t\t\t\t\t'conditions', {")
        lines.append("\t\t\t\t\t\t\t\t\tPlaceObj('CheckDifficulty', {")
        lines.append(f'\t\t\t\t\t\t\t\t\t\tDifficulty = "{eng}",')
        lines.append("\t\t\t\t\t\t\t\t\t}),")
        lines.append("\t\t\t\t\t\t\t\t},")
    lines.append("\t\t\t\t\t\t\t}),")
    return "\n".join(lines)


def slot(types: list[tuple[str, int | None]], lo: int, hi: int | None = None, eng: str | None = None) -> str:
    hi = lo if hi is None else hi
    if lo <= 0 and hi <= 0:
        return ""
    body = "\n".join(wentry(ut, w, eng) for ut, w in types)
    return "\n".join(
        [
            "\t\t\t\t\tPlaceObj('EnemySquadUnit', {",
            "\t\t\t\t\t\t'weightedList', {",
            body,
            "\t\t\t\t\t\t},",
            f"\t\t\t\t\t\t'UnitCountMin', {lo},",
            f"\t\t\t\t\t\t'UnitCountMax', {hi},",
            "\t\t\t\t\t}),",
        ]
    )


def gated(types: list[tuple[str, int | None]], e: tuple[int, int], n: tuple[int, int], h: tuple[int, int]) -> str:
    """Three parallel slots: design Easy/Normal/Hard counts."""
    parts = [
        slot(types, e[0], e[1], ENG_EASY),
        slot(types, n[0], n[1], ENG_NORMAL),
        slot(types, h[0], h[1], ENG_HARD),
    ]
    return "\n".join(p for p in parts if p)


def always(types: list[tuple[str, int | None]], lo: int, hi: int | None = None) -> str:
    return slot(types, lo, hi, eng=None)


# --- pools (island: all T1–T2 roles appear; T2 lean toward I7; rare T3 on keys) ---
LINE_T1 = [
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_AssaultT1_Roughneck", 50),
    ("JAZZ_Legion_FrontT2_Raider", 25),
]
LINE_BAL = [
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_FrontT2_Raider", None),
    ("JAZZ_Legion_AssaultT1_Roughneck", 30),
]
LINE_T2 = [
    ("JAZZ_Legion_FrontT2_Raider", None),
    ("JAZZ_Legion_FrontT1_Marauder", 50),
    ("JAZZ_Legion_FrontT1_Rifleman", 40),
    ("JAZZ_Legion_FrontT3_Veteran", 20),
]
# legacy aliases used below
LINE_A = LINE_T1
LINE_B = LINE_T2
MEAT_T1 = [
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
    ("JAZZ_Legion_Recruit", 60),
    ("JAZZ_Legion_FrontT1_Marauder", 40),
]
MEAT_T2 = [
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_Recruit", 25),
    ("JAZZ_Legion_FrontT2_Raider", 30),
]
MEAT = MEAT_T1
FLANK = [
    ("JAZZ_Legion_FlankerT1_Warden", None),
    ("JAZZ_Legion_FlankerT2_Scout", None),
    ("JAZZ_Legion_FlankerT2_Skirmisher", None),
]
FLANK_T2 = [
    ("JAZZ_Legion_FlankerT2_Scout", None),
    ("JAZZ_Legion_FlankerT2_Skirmisher", None),
    ("JAZZ_Legion_FlankerT1_Warden", 35),
]
MARKS = [
    ("JAZZ_Legion_FrontT2_Marksman", None),
    ("JAZZ_Legion_FrontT2_Ambusher", None),
    ("JAZZ_Legion_FrontT1_Rifleman", 40),
]
ASSAULT_T1 = [
    ("JAZZ_Legion_AssaultT1_Crusher", None),
    ("JAZZ_Legion_AssaultT1_Grenadier", None),
    ("JAZZ_Legion_AssaultT2_ShockTrooper", 35),
    ("JAZZ_Legion_AssaultT2_Pillager", 35),
]
ASSAULT_T2 = [
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
    ("JAZZ_Legion_AssaultT2_Pillager", None),
    ("JAZZ_Legion_AssaultT1_Crusher", 40),
    ("JAZZ_Legion_AssaultT1_Grenadier", 30),
    ("JAZZ_Legion_AssaultT2_Pyro", 25),
]
ASSAULT = ASSAULT_T2
GUN = [
    ("JAZZ_Legion_GunnerT1_Gunner", None),
    ("JAZZ_Legion_GunnerT2_GMPG", None),
    ("JAZZ_Legion_GunnerT2_AssaultGunner", 35),
]
GUN_PORT = [
    ("JAZZ_Legion_GunnerT2_GMPG", None),
    ("JAZZ_Legion_GunnerT2_AssaultGunner", None),
    ("JAZZ_Legion_GunnerT1_Gunner", 40),
]
MELEE = [
    ("JAZZ_Legion_AssaultT1_Crusher", None),
    ("JAZZ_Legion_AssaultT2_Pillager", None),
    ("JAZZ_Legion_AssaultT1_Roughneck", 40),
    ("JAZZ_Legion_AssaultT3_SkullCrusher", 12),
]
GRENADE = [
    ("JAZZ_Legion_AssaultT1_Grenadier", None),
    ("JAZZ_Legion_AssaultT2_Pyro", None),
]
VET = [
    ("JAZZ_Legion_FrontT2_Raider", None),
    ("JAZZ_Legion_FrontT3_Veteran", 45),
    ("JAZZ_Legion_AssaultT2_ShockTrooper", 40),
    ("JAZZ_Legion_FlankerT3_Recon", 20),
]
FOREST_FLANK = [
    ("JAZZ_Legion_FlankerT2_Scout", None),
    ("JAZZ_Legion_FlankerT2_Skirmisher", None),
    ("JAZZ_Legion_FrontT2_Ambusher", 40),
    ("JAZZ_Legion_FlankerT1_Warden", 35),
]
LITTLE_T3 = [
    ("JAZZ_Legion_FrontT3_Veteran", None),
    ("JAZZ_Legion_AssaultT3_Punisher", 50),
    ("JAZZ_Legion_AssaultT3_SkullCrusher", 40),
    ("JAZZ_Legion_FlankerT3_Recon", 35),
    ("JAZZ_Legion_FlankerT3_Pathfinder", 25),
]
# coast/early: no T3 in base spice
# keys near I7: LITTLE_T3 rare


def medium_base(
    *,
    line=LINE_BAL,
    meat=MEAT_T1,
    flank=FLANK,
    marks=MARKS,
    assault=ASSAULT_T1,
    gun=GUN,
    spice_t3: list | None = None,
    extra_gun: bool = False,
) -> str:
    """Medium design 20/25/40 with STRATEGY-005/015 officer+medic density."""
    # officers+medics (design E/N/H)
    # E20: 2 SGT, 1 LT, 2 medic → 15 body
    # N25: 3 SGT, 1 LT, 1 medic → 20 body
    # H40: 5 SGT, 2 LT, 1 CPT, 1 medic → 31 body
    parts = [
        gated([("JAZZ_Legion_LeaderT1_Sergeant", None)], (2, 2), (3, 3), (5, 5)),
        gated([("JAZZ_Legion_LeaderT2_Lieutenant", None)], (1, 1), (1, 1), (2, 2)),
        gated([("JAZZ_Legion_LeaderT3_Captain", None)], (0, 0), (0, 0), (1, 1)),
        gated([("JAZZ_Legion_FrontT1_Bonemaker", None)], (2, 2), (1, 1), (1, 1)),
        # body split (~15 / 20 / 31)
        gated(meat, (3, 4), (5, 6), (7, 8)),
        gated(line, (3, 4), (5, 5), (6, 7)),
        gated(flank, (2, 2), (2, 3), (4, 5)),
        gated(marks, (2, 2), (2, 2), (4, 4)),
        gated(assault, (2, 2), (3, 3), (5, 5)),
        gated(gun if not extra_gun else gun, (1, 2), (2, 2), (3, 4)),
        gated(GRENADE, (1, 1), (1, 1), (2, 2)),
    ]
    if spice_t3:
        parts.append(gated(spice_t3, (0, 0), (1, 1), (1, 2)))
    return "\n".join(p for p in parts if p)


def large_outpost_b() -> str:
    # Large 30/40/70; band B little T3
    # E30: 3SGT 2LT 1CPT 3medic = 9 → body 21
    # N40: 5SGT 2LT 1CPT 2medic = 10 → body 30
    # H70: 8SGT 4LT 2CPT 3medic = 17 → body 53
    return "\n".join(
        p
        for p in [
            gated([("JAZZ_Legion_LeaderT1_Sergeant", None)], (3, 3), (5, 5), (8, 8)),
            gated([("JAZZ_Legion_LeaderT2_Lieutenant", None)], (2, 2), (2, 2), (4, 4)),
            gated([("JAZZ_Legion_LeaderT3_Captain", None)], (1, 1), (1, 1), (2, 2)),
            gated([("JAZZ_Legion_FrontT1_Bonemaker", None)], (3, 3), (2, 2), (3, 3)),
            gated(MEAT_T2, (4, 5), (7, 7), (12, 14)),
            gated(LINE_T2, (5, 6), (7, 8), (12, 14)),
            gated(FLANK_T2, (2, 3), (3, 4), (6, 7)),
            gated(MARKS, (2, 3), (3, 4), (5, 6)),
            gated(ASSAULT_T2, (3, 3), (4, 5), (8, 9)),
            gated(GUN_PORT, (2, 2), (3, 3), (5, 6)),
            gated(GRENADE, (1, 1), (1, 2), (2, 3)),
            gated(LITTLE_T3, (1, 1), (2, 2), (3, 3)),
        ]
        if p
    )


def fortress_48() -> str:
    """Locked FortressDefenders roles; design Easy38 / Normal48 / Hard58."""
    # Anchors mostly fixed; scale line/assault/flank/meat
    # N48 locked table; E=-10 soft roles; H=+10 soft roles
    return "\n".join(
        p
        for p in [
            always([("JAZZ_Legion_LeaderT2_Lieutenant", None)], 1),
            always([("JAZZ_Legion_LeaderT1_Sergeant", None)], 2),
            gated([("JAZZ_Legion_FrontT1_Bonemaker", None)], (3, 3), (2, 2), (1, 1)),
            always([("JAZZ_Legion_HeavyT3_Mortarman", None)], 1),
            always([("JAZZ_Legion_HeavyT1_Rocketeer", None)], 1),
            always([("JAZZ_Legion_HeavyT2_Grenadier", None)], 1),
            # MG 4
            always(
                [
                    ("JAZZ_Legion_GunnerT2_GMPG", None),
                    ("JAZZ_Legion_GunnerT1_Gunner", 40),
                    ("JAZZ_Legion_GunnerT2_AssaultGunner", 40),
                ],
                4,
            ),
            # Precision 3 (2 sniper + marks)
            always(
                [
                    ("JAZZ_Legion_FrontT3_Sniper", None),
                    ("JAZZ_Legion_FrontT2_Marksman", 40),
                ],
                3,
            ),
            always([("JAZZ_Legion_FrontT2_Ambusher", None)], 2),
            # Flank locked: 1× Recon (T3) + Warden/Scout/Skirmisher rest
            always([("JAZZ_Legion_FlankerT3_Recon", None)], 1),
            gated(
                [
                    ("JAZZ_Legion_FlankerT1_Warden", None),
                    ("JAZZ_Legion_FlankerT2_Scout", None),
                    ("JAZZ_Legion_FlankerT2_Skirmisher", None),
                ],
                (3, 3),
                (5, 5),
                (7, 7),
            ),
            # Line 8± : E6 N8 H10
            gated(LINE_T2, (6, 6), (8, 8), (10, 10)),
            # Assault 8± : E6 N8 H10 — full T1–T2 assault roles
            gated(ASSAULT_T2, (6, 6), (8, 8), (10, 10)),
            # Meat 6± : E4 N6 H8
            gated(MEAT_T2, (4, 4), (6, 6), (8, 8)),
            # Little T3 3 (Veteran/Punisher/Skull; Pathfinder rare)
            always(
                [
                    ("JAZZ_Legion_FrontT3_Veteran", None),
                    ("JAZZ_Legion_AssaultT3_Punisher", 50),
                    ("JAZZ_Legion_AssaultT3_SkullCrusher", 40),
                ],
                3,
            ),
        ]
        if p
    )


def extra_pack(types: list[tuple[str, int | None]], lo: int, hi: int) -> str:
    return always(types, lo, hi)


def extra_pack_mixed(types: list[tuple[str, int | None]], lo: int, hi: int) -> str:
    """One roll per unit. Vanilla GenerateRandEnemySquadUnits picks type once per
    EnemySquadUnit slot then clones UnitCount — a single 6–9 slot always looks mono.
    """
    parts = [slot(types, 1, 1) for _ in range(lo)]
    for _ in range(max(0, hi - lo)):
        parts.append(slot(types, 0, 1))
    return "\n".join(p for p in parts if p)


def moditem(squad_id: str, units: str, comment: str, display: str, group: str, t_off: int) -> str:
    return (
        f"\t\t\t\tPlaceObj('ModItemEnemySquads', {{\n"
        f"\t\t\t\t\tUnits = {{\n"
        f"{units}\n"
        f"\t\t\t\t\t}},\n"
        f'\t\t\t\t\tcomment = "{comment}",\n'
        f"\t\t\t\t\tdisplayName = {T(t_off, squad_id, display)},\n"
        f'\t\t\t\t\tgroup = "{group}",\n'
        f'\t\t\t\t\tid = "{squad_id}",\n'
        f"\t\t\t\t}}),\n"
    )


PACKS: dict[str, tuple[str, str, str, int]] = {}  # id -> (units, comment, ru_name, t_off)


def define_packs() -> None:
    # Far/coast/forest: T1-lean, full T1–T2 roles in pools, no base T3
    PACKS["LegionErnie_Medium_Coast_A"] = (
        medium_base(line=LINE_T1, meat=MEAT_T1, flank=FOREST_FLANK, assault=ASSAULT_T1, gun=GUN),
        "-- UNITS-007 Medium Coast A T1-lean; design E/N/H 20/25/40",
        "Гарнизон побережья",
        1,
    )
    PACKS["LegionErnie_Medium_Port_A"] = (
        medium_base(line=LINE_T1, meat=MEAT_T1, flank=FLANK, assault=ASSAULT_T1, gun=GUN_PORT),
        "-- UNITS-007 Medium Port A T1-lean; design E/N/H 20/25/40",
        "Гарнизон старого порта",
        2,
    )
    PACKS["LegionErnie_Medium_Road_A"] = (
        medium_base(line=LINE_BAL, meat=MEAT_T1, flank=FLANK, assault=ASSAULT_T1, gun=GUN),
        "-- UNITS-007 Medium Road A balanced T1–T2; design E/N/H 20/25/40",
        "Дорожный гарнизон",
        3,
    )
    PACKS["LegionErnie_Medium_Forest_A"] = (
        medium_base(line=LINE_T1, meat=MEAT_T1, flank=FOREST_FLANK, assault=MELEE, gun=GUN),
        "-- UNITS-007 Medium Forest A T1-lean; design E/N/H 20/25/40",
        "Лесной гарнизон",
        4,
    )
    # Near fort / bunker: T2-lean + rare T3
    PACKS["LegionErnie_Medium_Bunker_AB"] = (
        medium_base(
            line=LINE_T2,
            meat=MEAT_T2,
            flank=FLANK_T2,
            assault=ASSAULT_T2,
            gun=GUN_PORT,
            spice_t3=LITTLE_T3,
        ),
        "-- UNITS-007 Medium Bunker A/B T2-lean + rare T3; design E/N/H 20/25/40",
        "Гарнизон бункера",
        5,
    )
    PACKS["LegionErnie_Large_Outpost_B"] = (
        large_outpost_b(),
        "-- UNITS-007 Large Outpost B T2-lean + rare T3; design E/N/H 30/40/70",
        "Крупный аванпост",
        6,
    )
    PACKS["LegionErnie_I2_Lighthouse"] = (
        medium_base(
            line=LINE_T2,
            meat=MEAT_T2,
            flank=FLANK_T2,
            assault=ASSAULT_T2,
            gun=GUN,
            spice_t3=LITTLE_T3,
        ),
        "-- UNITS-007 I2 lighthouse B T2-lean + rare T3; + Veterans Extra",
        "Гарнизон маяка",
        7,
    )
    # Extras 5-10
    PACKS["LegionExtra_Ernie_Gunners"] = (
        extra_pack(GUN_PORT, 6, 8),
        "-- UNITS-007 Extra Gunners 6-8",
        "Усиление: пулемётчики",
        10,
    )
    PACKS["LegionExtra_Ernie_Marksmen"] = (
        extra_pack(
            [
                ("JAZZ_Legion_FrontT2_Marksman", None),
                ("JAZZ_Legion_FrontT2_Ambusher", 40),
                ("JAZZ_Legion_FrontT3_Sniper", 20),
            ],
            6,
            8,
        ),
        "-- UNITS-007 Extra Marksmen 6-8",
        "Усиление: стрелки",
        11,
    )
    PACKS["LegionExtra_Ernie_Grenadiers"] = (
        extra_pack(
            [
                ("JAZZ_Legion_AssaultT1_Grenadier", None),
                ("JAZZ_Legion_AssaultT2_Pyro", 40),
                ("JAZZ_Legion_HeavyT2_Grenadier", 15),
            ],
            5,
            7,
        ),
        "-- UNITS-007 Extra Grenadiers 5-7",
        "Усиление: гранатомётчики",
        12,
    )
    PACKS["LegionExtra_Ernie_Veterans"] = (
        extra_pack(VET, 5, 7),
        "-- UNITS-007 Extra Veterans light 5-7",
        "Усиление: ветераны",
        13,
    )
    PACKS["LegionExtra_Ernie_Melee"] = (
        extra_pack(MELEE, 6, 8),
        "-- UNITS-007 Extra Melee 6-8",
        "Усиление: ближний бой",
        14,
    )
    PACKS["LegionExtra_Ernie_Flankers"] = (
        extra_pack(FOREST_FLANK, 6, 8),
        "-- UNITS-007 Extra Flankers 6-8",
        "Усиление: фланкеры",
        15,
    )
    PACKS["LegionExtra_Ernie_Mixed"] = (
        extra_pack_mixed(
            [
                ("JAZZ_Legion_GunnerT1_Gunner", None),
                ("JAZZ_Legion_FrontT2_Marksman", None),
                ("JAZZ_Legion_AssaultT1_Grenadier", None),
                ("JAZZ_Legion_FrontT2_Raider", None),
                ("JAZZ_Legion_AssaultT1_Crusher", None),
                ("JAZZ_Legion_FlankerT2_Scout", None),
            ],
            6,
            9,
        ),
        "-- UNITS-007 Extra Mixed 6-9; per-unit specialty roll (not one type×N)",
        "Усиление: смешанное",
        16,
    )


def replace_units_block(text: str, squad_id: str, new_units: str) -> str:
    idx = text.find(f'id = "{squad_id}"')
    if idx < 0:
        raise SystemExit(f"missing id {squad_id}")
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    m = re.search(r"Units = \{", text[start:idx])
    if not m:
        raise SystemExit(f"no Units in {squad_id}")
    us = start + m.start()
    i = us + len("Units = ")
    assert text[i] == "{"
    depth = 1
    i += 1
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    end = i + (1 if i < len(text) and text[i] == "," else 0)
    return text[:us] + f"Units = {{\n{new_units}\n\t\t\t\t}}," + text[end:]


def upsert_comment(text: str, squad_id: str, comment: str) -> str:
    idx = text.find(f'id = "{squad_id}"')
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    block = text[start:idx]
    if "comment =" in block or "Comment =" in block:
        block2 = re.sub(
            r"(?:comment|Comment) = \"[^\"]*\"",
            f'comment = "{comment}"',
            block,
            count=1,
        )
        return text[:start] + block2 + text[idx:]
    # insert before displayName or id
    ins_at = block.rfind("displayName")
    if ins_at < 0:
        ins_at = len(block)
    return text[: start + ins_at] + f'\t\t\t\t\tcomment = "{comment}",\n' + text[start + ins_at :]


def set_sector_init(maps_text: str, sector_id: str, squad_ids: list[str]) -> str:
    body = "\n".join(f'\t\t\t\t\t\t"{sid}",' for sid in squad_ids) + "\n\t\t\t\t\t"
    pat = re.compile(
        rf"('sectorId', \"{sector_id}\"[\s\S]*?'InitialSquads', \{{)\s*[\s\S]*?(\s*\}},)",
        re.M,
    )
    new, n = pat.subn(rf"\1\n{body}\2", maps_text, count=1)
    if n < 1:
        raise SystemExit(f"{sector_id} InitialSquads not found")
    print(f"  Init {sector_id} -> {squad_ids}")
    return new


def ensure_meta(meta: str, squad_id: str, after_id: str = "LegionErnieVillage") -> str:
    if f"'Id', \"{squad_id}\"" in meta:
        return meta
    anchor = f"""\t\t\t'Id', "{after_id}",
\t\t\t'ClassDisplayName', "Enemy Squads",
\t\t}}),
"""
    ins = (
        anchor
        + f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', "EnemySquads",
\t\t\t'Id', "{squad_id}",
\t\t\t'ClassDisplayName', "Enemy Squads",
\t\t}}),
"""
    )
    if anchor not in meta:
        raise SystemExit(f"metadata anchor {after_id} missing for {squad_id}")
    return meta.replace(anchor, ins, 1)


def extract_squad_block(text: str, squad_id: str) -> tuple[str, str, str]:
    """Return (before, block, after) for a ModItemEnemySquads."""
    idx = text.find(f'id = "{squad_id}"')
    if idx < 0:
        raise SystemExit(f"cannot extract {squad_id}")
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    # find matching close of PlaceObj — walk from start
    i = start + len("PlaceObj('ModItemEnemySquads', ")
    assert text[i] == "{"
    depth = 1
    i += 1
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    # expect ), after
    while i < len(text) and text[i] in " \t\r\n":
        i += 1
    if text[i : i + 2] == "),":
        i += 2
    elif text[i] == ")":
        i += 1
        if i < len(text) and text[i] == ",":
            i += 1
    if i < len(text) and text[i] == "\n":
        i += 1
    return text[:start], text[start:i], text[i:]


def move_to_deprecated(text: str, squad_id: str) -> str:
    if f'id = "{squad_id}"' not in text:
        print(f"  skip retire {squad_id}: missing")
        return text
    # already under Deprecated?
    idx = text.find(f'id = "{squad_id}"')
    folder_pos = text.rfind("'name', \"Deprecated\"", 0, idx)
    # if Deprecated folder is closer than another folder after previous ModItemFolder
    prev_folder = text.rfind("PlaceObj('ModItemFolder'", 0, idx)
    if prev_folder >= 0 and folder_pos > prev_folder:
        print(f"  already Deprecated: {squad_id}")
        return text
    before, block, after = extract_squad_block(text, squad_id)
    text2 = before + after
    # mark comment
    if "comment =" not in block and "Comment =" not in block:
        block = block.replace(
            "PlaceObj('ModItemEnemySquads', {",
            f"PlaceObj('ModItemEnemySquads', {{\n\t\t\t\t\tcomment = \"-- UNITS-007 retired unused Ernie Init stack\",",
            1,
        )
    else:
        block = re.sub(
            r"(?:comment|Comment) = \"[^\"]*\"",
            'comment = "-- UNITS-007 retired unused Ernie Init stack"',
            block,
            count=1,
        )
    # insert into Deprecated children (empty folder currently)
    marker = """\t\tPlaceObj('ModItemFolder', {
\t\t\t'name', \"Deprecated\",
\t\t\t'comment', \"Retired packs (keep Id if still referenced elsewhere)\",
\t\t}, {
\t\t\t}),"""
    # current may be `}, {` then `}),` empty
    m = re.search(
        r"PlaceObj\('ModItemFolder', \{\s*'name', \"Deprecated\",[\s\S]*?\}, \{\s*\}\),",
        text2,
    )
    if not m:
        # try non-empty
        m = re.search(
            r"(PlaceObj\('ModItemFolder', \{\s*'name', \"Deprecated\",[\s\S]*?\}, \{)",
            text2,
        )
        if not m:
            raise SystemExit("Deprecated folder not found")
        insert_at = m.end()
        text2 = text2[:insert_at] + "\n" + block + text2[insert_at:]
    else:
        # replace empty children
        old = m.group(0)
        new = old.replace("}, {\n\t\t\t}),", "}, {\n" + block + "\t\t\t}),", 1)
        if new == old:
            new = old.replace("}, {\r\n\t\t\t}),", "}, {\n" + block + "\t\t\t}),", 1)
        if new == old:
            # looser
            new = re.sub(
                r"(\}, \{)\s*(\}\),)",
                r"\1\n" + block + r"\2",
                old,
                count=1,
            )
        text2 = text2[: m.start()] + new + text2[m.end() :]
    print(f"  retired -> Deprecated: {squad_id}")
    return text2


def count_refs(haystacks: list[str], squad_id: str) -> int:
    pat = re.compile(rf'(?<![\\w]){re.escape(squad_id)}(?![\\w])')
    return sum(len(pat.findall(h)) for h in haystacks)


def normal_sum_estimate(units_src: str) -> int:
    """Sum UnitCountMin for Hard-gated (design Normal) + ungated slots."""
    # rough: parse slots — if block contains Difficulty Hard, count it; if no CheckDifficulty in slot, count it
    total = 0
    for m in re.finditer(
        r"PlaceObj\('EnemySquadUnit', \{([\s\S]*?)\n\t\t\t\t\t\}\),",
        units_src,
    ):
        body = m.group(1)
        lo = re.search(r"'UnitCountMin', (\d+)", body)
        if not lo:
            continue
        n = int(lo.group(1))
        if "CheckDifficulty" not in body:
            total += n
        elif f"'Difficulty', \"{ENG_NORMAL}\"" in body or f'Difficulty = "{ENG_NORMAL}"' in body:
            total += n
    return total


def main() -> None:
    define_packs()
    units = UNITS.read_text(encoding="utf-8")
    meta = META.read_text(encoding="utf-8")
    maps = MAPS.read_text(encoding="utf-8")

    # --- Outlook rewrite (keep id) — mid-island Outpost, balanced/T1 lean ---
    outlook_units = medium_base(
        line=LINE_BAL, meat=MEAT_T1, flank=FLANK, assault=ASSAULT_T1, gun=GUN
    )
    units = replace_units_block(units, "LegionOutlook_Easy", outlook_units)
    units = upsert_comment(
        units,
        "LegionOutlook_Easy",
        "-- UNITS-007 M4 Outlook Medium Outpost A; design E/N/H 20/25/40 + Marksmen Extra",
    )
    print("rewrote LegionOutlook_Easy")

    # --- FortressDefenders ---
    units = replace_units_block(units, "FortressDefenders", fortress_48())
    units = upsert_comment(
        units,
        "FortressDefenders",
        "-- UNITS-007 I7 FortressDefenders design E/N/H 38/48/58; locked roles",
    )
    print("rewrote FortressDefenders")

    # --- insert / upsert new packs near LegionErnieVillage ---
    for sid, (u, comment, ru, t_off) in PACKS.items():
        block = moditem(sid, u, comment, ru, "Ernie", t_off)
        if f'id = "{sid}"' in units:
            units = replace_units_block(units, sid, u)
            units = upsert_comment(units, sid, comment)
            print(f"updated {sid}")
        else:
            anchor = '\tid = "LegionErnieVillage",\n\t\t\t\t}),\n'
            if anchor not in units:
                # try tab variants
                anchor = '\t\t\t\tid = "LegionErnieVillage",\n\t\t\t\t}),\n'
            if anchor not in units:
                raise SystemExit("LegionErnieVillage anchor missing")
            units = units.replace(anchor, anchor + block, 1)
            print(f"inserted {sid}")
        meta = ensure_meta(meta, sid)

    # --- Init rewire ---
    init_map = {
        "M4": ["LegionOutlook_Easy", "LegionExtra_Ernie_Marksmen"],
        "M5": ["LegionErnie_Medium_Coast_A", "LegionExtra_Ernie_Mixed"],
        "M6": ["LegionErnie_Medium_Port_A", "LegionExtra_Ernie_Gunners"],
        "I2": ["LegionErnie_I2_Lighthouse", "LegionExtra_Ernie_Veterans"],
        "I3": ["LegionErnie_Medium_Road_A", "LegionExtra_Ernie_Flankers"],
        "I4": ["LegionErnie_Medium_Road_A", "LegionExtra_Ernie_Mixed"],
        "L1": ["LegionErnie_Large_Outpost_B"],
        "L2": ["LegionErnie_Medium_Forest_A", "LegionExtra_Ernie_Melee"],
        "L6": ["LegionErnie_Medium_Forest_A", "LegionExtra_Ernie_Flankers"],
        "L6_Underground": ["LegionErnie_Medium_Bunker_AB", "LegionExtra_Ernie_Grenadiers"],
        "I7": ["FortressPierre", "FortressDefenders"],
    }
    for sec, ids in init_map.items():
        maps = set_sector_init(maps, sec, ids)

    # write interim for ref audit
    UNITS.write_text(units, encoding="utf-8", newline="\n")
    MAPS.write_text(maps, encoding="utf-8", newline="\n")
    META.write_text(meta, encoding="utf-8", newline="\n")

    # --- retire unused ---
    units = UNITS.read_text(encoding="utf-8")
    maps = MAPS.read_text(encoding="utf-8")
    meta = META.read_text(encoding="utf-8")
    code_blobs = []
    for p in (JAZZ / "Code").glob("*.lua"):
        code_blobs.append(p.read_text(encoding="utf-8", errors="ignore"))
    nomaps = ROOT / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"
    if nomaps.exists():
        code_blobs.append(nomaps.read_text(encoding="utf-8", errors="ignore"))

    candidates = [
        "LegionAttackers_JazzBalanced_Easy_Assault",
        "LegionAttackers_Marksmen_Easy",
        "LegionAttackers_Balanced_Easy",
        "LegionDefenders_Mobile_Easy",
        "LegionDefenders_Entrenched_Easy",
        "LegionAttackers_Ordnance_Easy",
        "LegionHeavyTroops_Gunners",
        # do NOT auto-retire shared ExtraFireArms / Raid / Patrol — only if zero external
        "LegionExtraSquadFireArms_T2",
        "LegionExtraSquadFireArms",
        "LegionExtraSquadMelee_T2",
        "LegionExtraSquadMeleeV2",
    ]
    hay = [maps, meta] + code_blobs
    # also other packs in units (exclude self definition roughly by counting)
    for cid in candidates:
        # refs outside the squad's own ModItem block
        if f'id = "{cid}"' not in units:
            print(f"  retire skip missing {cid}")
            continue
        before, block, after = extract_squad_block(units, cid)
        others = before + after
        refs = count_refs([others, maps, meta] + code_blobs, cid)
        # metadata always has ModResourcePreset — subtract 1 if present
        if f"'Id', \"{cid}\"" in meta:
            refs -= 1
        if refs <= 0:
            units = move_to_deprecated(units, cid)
        else:
            print(f"  keep {cid}: still referenced (~{refs})")

    UNITS.write_text(units, encoding="utf-8", newline="\n")

    # --- verify Normal sums ---
    units = UNITS.read_text(encoding="utf-8")
    for sid in [
        "LegionOutlook_Easy",
        "LegionErnie_Medium_Coast_A",
        "LegionErnie_Medium_Port_A",
        "LegionErnie_Medium_Road_A",
        "LegionErnie_Medium_Forest_A",
        "LegionErnie_Medium_Bunker_AB",
        "LegionErnie_Large_Outpost_B",
        "LegionErnie_I2_Lighthouse",
        "FortressDefenders",
        "LegionExtra_Ernie_Veterans",
        "LegionExtra_Ernie_Flankers",
    ]:
        idx = units.find(f'id = "{sid}"')
        start = units.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
        end = idx
        s = normal_sum_estimate(units[start:end])
        print(f"  Normal~ {sid} = {s}")


if __name__ == "__main__":
    main()
