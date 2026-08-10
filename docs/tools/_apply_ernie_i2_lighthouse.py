"""I2 lighthouse: custom base 25 + ExtraFireArms 15 = 40 (UNITS-007).

Band B Outpost — little T3 in pools; wide class variance; no Hyenas/vanilla Balanced stack.
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
META = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")

SQUAD_ID = "LegionErnie_I2_Lighthouse"


def slot(types: list[tuple[str, int | None]], lo: int, hi: int | None = None) -> str:
    hi = lo if hi is None else hi
    lines = [
        "\t\t\t\t\tPlaceObj('EnemySquadUnit', {",
        "\t\t\t\t\t\t'weightedList', {",
    ]
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


LINE = [
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_AssaultT1_Roughneck", 50),
]
MARKS = [
    ("JAZZ_Legion_FrontT2_Marksman", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
    ("JAZZ_Legion_FlankerT2_Skirmisher", 40),
]
FLANK = [
    ("JAZZ_Legion_FlankerT2_Scout", None),
    ("JAZZ_Legion_FlankerT1_Warden", None),
    ("JAZZ_Legion_FlankerT2_Skirmisher", 40),
]
AMBUSH = [
    ("JAZZ_Legion_FrontT2_Ambusher", None),
    ("JAZZ_Legion_FrontT3_Sniper", 25),
]
ASSAULT = [
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
    ("JAZZ_Legion_AssaultT2_Pillager", 50),
    ("JAZZ_Legion_FrontT2_Raider", 50),
]
GUN = [
    ("JAZZ_Legion_GunnerT1_Gunner", None),
    ("JAZZ_Legion_GunnerT2_GMPG", 40),
]
MEAT = [
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
    ("JAZZ_Legion_Recruit", 60),
    ("JAZZ_Legion_FrontT1_Marauder", 40),
]

# Normal base 25 (+ ExtraFireArms 15 = 40 sector)
BODY = "\n".join(
    [
        slot([("JAZZ_Legion_LeaderT1_Sergeant", None)], 1),
        slot([("JAZZ_Legion_LeaderT2_Lieutenant", None)], 1),
        slot([("JAZZ_Legion_FrontT1_Bonemaker", None)], 2),
        slot(MEAT, 4),
        slot(LINE, 4),
        slot(MARKS, 4),
        slot(FLANK, 2),
        slot(AMBUSH, 2),
        slot(ASSAULT, 2),
        slot(GUN, 2),
        slot([("JAZZ_Legion_AssaultT1_Grenadier", None)], 1),  # 25
    ]
)

MODITEM = f"""\t\t\t\tPlaceObj('ModItemEnemySquads', {{
\t\t\t\t\tUnits = {{
{BODY}
\t\t\t\t\t}},
\t\t\t\t\tcomment = "-- I2 lighthouse/outpost: base 25 + ExtraFireArms 15 = 40; band B",
\t\t\t\t\tdisplayName = T(890000000012401, --[[ModItemEnemySquads LegionErnie_I2_Lighthouse displayName]] "Гарнизон маяка"),
\t\t\t\t\tgroup = "Ernie",
\t\t\t\t\tid = "{SQUAD_ID}",
\t\t\t\t}}),
"""


def set_sector_init(maps_text: str, sector_id: str, squad_ids: list[str]) -> str:
    body = "\n".join(f'\t\t\t\t\t\t"{sid}",' for sid in squad_ids) + "\n\t\t\t\t\t"
    pat = re.compile(
        rf"('sectorId', \"{sector_id}\"[\s\S]*?'InitialSquads', \{{)\s*[\s\S]*?(\s*\}},)",
        re.M,
    )
    new, n = pat.subn(rf"\1\n{body}\2", maps_text)
    if n < 1:
        raise SystemExit(f"{sector_id} InitialSquads not found")
    print(f"{sector_id}: replaced {n} Init -> {squad_ids}")
    return new


def main() -> None:
    units = UNITS.read_text(encoding="utf-8")
    if SQUAD_ID in units:
        # replace existing Units block
        idx = units.find(f'id = "{SQUAD_ID}"')
        start = units.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
        m = re.search(r"Units = \{", units[start:idx])
        assert m
        us = start + m.start()
        depth = 0
        i = us + len("Units = ")
        depth = 1
        i += 1
        while i < len(units) and depth:
            if units[i] == "{":
                depth += 1
            elif units[i] == "}":
                depth -= 1
            i += 1
        end = i + (1 if i < len(units) and units[i] == "," else 0)
        units = units[:us] + f"Units = {{\n{BODY}\n\t\t\t\t}}," + units[end:]
        print(f"updated existing {SQUAD_ID}")
    else:
        anchor = '\tid = "LegionErnieVillage",\n\t\t\t\t}),\n'
        if anchor not in units:
            raise SystemExit("anchor LegionErnieVillage not found")
        units = units.replace(anchor, anchor + MODITEM, 1)
        print(f"inserted {SQUAD_ID}")

    UNITS.write_text(units, encoding="utf-8", newline="\n")

    meta = META.read_text(encoding="utf-8")
    if SQUAD_ID not in meta:
        meta_anchor = """\t\t\t'Id', "LegionErnieVillage",
\t\t\t'ClassDisplayName', "Enemy Squads",
\t\t}),
"""
        meta_ins = meta_anchor + f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', "EnemySquads",
\t\t\t'Id', "{SQUAD_ID}",
\t\t\t'ClassDisplayName', "Enemy Squads",
\t\t}}),
"""
        if meta_anchor not in meta:
            raise SystemExit("metadata anchor missing")
        meta = meta.replace(meta_anchor, meta_ins, 1)
        META.write_text(meta, encoding="utf-8", newline="\n")
        print("metadata preset added")
    else:
        print("metadata already has preset")

    maps = MAPS.read_text(encoding="utf-8")
    maps = set_sector_init(maps, "I2", [SQUAD_ID, "LegionExtraSquadFireArms"])
    MAPS.write_text(maps, encoding="utf-8", newline="\n")

    # verify
    u2 = UNITS.read_text(encoding="utf-8")
    idx = u2.find(f'id = "{SQUAD_ID}"')
    start = u2.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    total = sum(int(x) for x in re.findall(r"'UnitCountMin', (\d+)", u2[start:idx]))
    print(f"{SQUAD_ID} sum={total} + ExtraFireArms 15 = {total + 15}")


if __name__ == "__main__":
    main()
