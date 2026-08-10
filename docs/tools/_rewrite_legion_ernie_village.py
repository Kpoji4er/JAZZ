"""Rewrite Ernie village (I5) + farms (J5) Init garrisons.

Owner locks 2026-08-10:
  I5 LegionErnieVillage Normal ~60 — mostly meat/T1, ~10 Recruit, up to ~10 Pillager, few pyro
  J5 LegionDefenders_Shooters_Easy_Ernie Normal ~40 — second-largest island pack
  I5/J5 Init = single pack each (no Extra stacking)
  Easy/Hard ±10 later
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")


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


def units_block(slots: list[str]) -> str:
    return "Units = {\n" + "\n".join(slots) + "\n\t\t\t\t},"


LINE_T1 = [
    ("JAZZ_Legion_FrontT1_Marauder", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
]
CRUSH = [
    ("JAZZ_Legion_AssaultT1_Crusher", None),
    ("JAZZ_Legion_AssaultT3_SkullCrusher", 20),
]
ASSAULT_T2 = [
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
    ("JAZZ_Legion_AssaultT2_Pillager", 40),
]
MARKS = [
    ("JAZZ_Legion_FrontT2_Marksman", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
]
AMBUSH = [
    ("JAZZ_Legion_FrontT2_Ambusher", None),
    ("JAZZ_Legion_FrontT3_Sniper", 25),
]
GUN = [
    ("JAZZ_Legion_GunnerT1_Gunner", None),
    ("JAZZ_Legion_GunnerT2_GMPG", 40),
]

# I5 Normal 60 (Easy 50 / Hard 70 later)
# Meat-heavy: 12 Recruit + 10 Roughneck + 8 line + 6 crush + 10 Pillager + spice
VILLAGE = units_block(
    [
        slot([("JAZZ_Legion_LeaderT1_Sergeant", None)], 1),
        slot([("JAZZ_Legion_FrontT1_Bonemaker", None)], 4),
        slot([("JAZZ_Legion_Recruit", None)], 12),
        slot([("JAZZ_Legion_AssaultT1_Roughneck", None)], 8),
        slot(LINE_T1, 6),
        slot(CRUSH, 6),
        slot([("JAZZ_Legion_AssaultT2_Pillager", None)], 10),
        slot([("JAZZ_Legion_AssaultT1_Grenadier", None)], 2),
        slot([("JAZZ_Legion_FrontT2_Raider", None)], 2),
        slot(ASSAULT_T2, 2),
        slot([("JAZZ_Legion_AssaultT2_Pyro", None)], 1),
        slot(MARKS, 2),
        slot(AMBUSH, 2),
        slot(GUN, 2),  # 60
    ]
)

# J5 farms Normal 40 — still large, more rifle line than I5 meat
FARMS = units_block(
    [
        slot([("JAZZ_Legion_LeaderT1_Sergeant", None)], 1),
        slot([("JAZZ_Legion_FrontT1_Bonemaker", None)], 2),
        slot([("JAZZ_Legion_Recruit", None)], 6),
        slot([("JAZZ_Legion_AssaultT1_Roughneck", None)], 6),
        slot(LINE_T1, 10),
        slot(MARKS, 4),
        slot(AMBUSH, 3),
        slot(GUN, 3),
        slot([("JAZZ_Legion_AssaultT2_Pillager", None)], 2),
        slot(ASSAULT_T2, 2),
        slot([("JAZZ_Legion_AssaultT1_Grenadier", None)], 1),  # 40
    ]
)


def replace_squad(text: str, squad_id: str, new_units: str) -> str:
    idx = text.find(f'id = "{squad_id}"')
    if idx < 0:
        raise SystemExit(f"missing id {squad_id}")
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    block = text[start:idx]
    m = re.search(r"Units = \{", block)
    if not m:
        raise SystemExit(f"no Units in {squad_id}")
    units_start = start + m.start()
    depth = 0
    i = units_start + len("Units = ")
    assert text[i] == "{"
    depth = 1
    i += 1
    while i < len(text) and depth:
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    end = i
    if end < len(text) and text[end] == ",":
        end += 1
    return text[:units_start] + new_units + text[end:]


def set_sector_init(maps_text: str, sector_id: str, squad_ids: list[str]) -> str:
    body = "\n".join(f'\t\t\t\t\t\t"{sid}",' for sid in squad_ids) + "\n\t\t\t\t\t"
    pat = re.compile(
        rf"('sectorId', \"{sector_id}\"[\s\S]*?'InitialSquads', \{{)\s*[\s\S]*?(\s*\}},)",
        re.M,
    )
    new, n = pat.subn(rf"\1\n{body}\2", maps_text)
    if n < 1:
        raise SystemExit(f"{sector_id} InitialSquads not found")
    print(f"{sector_id}: replaced {n} InitialSquads block(s) -> {squad_ids}")
    return new


def squad_sum(text: str, squad_id: str) -> int:
    idx = text.find(f'id = "{squad_id}"')
    start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
    block = text[start:idx]
    return sum(int(x) for x in re.findall(r"'UnitCountMin', (\d+)", block))


def main() -> None:
    units = UNITS.read_text(encoding="utf-8")
    units = replace_squad(units, "LegionErnieVillage", VILLAGE)
    units = replace_squad(units, "LegionDefenders_Shooters_Easy_Ernie", FARMS)
    units = re.sub(
        r'(comment = ")[^"]*("\s*,\s*\n\s*group = "Ernie",\s*\n\s*id = "LegionErnieVillage")',
        r'\1-- Hub I5 meat garrison: ~60, Recruit+Pillager, mostly T1\2',
        units,
        count=1,
    )
    units = re.sub(
        r'(comment = ")[^"]*("\s*,\s*\n\s*displayName = T\([^)]+LegionDefenders_Shooters_Easy_Ernie[^,]*,[^\n]+\n\s*group = "Ernie",\s*\n\s*id = "LegionDefenders_Shooters_Easy_Ernie")',
        r'\1-- J5 Ernie farms garrison: Normal 40\2',
        units,
        count=1,
    )
    # simpler comment replace for farms if displayName-before-group order differs
    if "J5 Ernie farms" not in units:
        units = re.sub(
            r'(comment = ")[^"]*("[\s\S]{0,200}?id = "LegionDefenders_Shooters_Easy_Ernie")',
            r'\1-- J5 Ernie farms garrison: Normal 40\2',
            units,
            count=1,
        )
    UNITS.write_text(units, encoding="utf-8", newline="\n")

    maps = MAPS.read_text(encoding="utf-8")
    maps = set_sector_init(maps, "I5", ["LegionErnieVillage"])
    maps = set_sector_init(maps, "J5", ["LegionDefenders_Shooters_Easy_Ernie"])
    MAPS.write_text(maps, encoding="utf-8", newline="\n")

    units2 = UNITS.read_text(encoding="utf-8")
    print("LegionErnieVillage sum", squad_sum(units2, "LegionErnieVillage"))
    print("Shooters_Easy_Ernie sum", squad_sum(units2, "LegionDefenders_Shooters_Easy_Ernie"))


if __name__ == "__main__":
    main()
