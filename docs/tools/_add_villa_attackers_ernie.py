"""Insert JAZZ_Legion_VillaAttackers_Ernie (Normal base 30) into jazz-units QuestSquads."""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
META = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua")

SQUAD_ID = "JAZZ_Legion_VillaAttackers_Ernie"


def slot(types: list[tuple[str, int | None]], n: int) -> str:
    lines = ["\t\t\t\t\tPlaceObj('EnemySquadUnit', {", "\t\t\t\t\t\t'weightedList', {"]
    for ut, w in types:
        lines.append("\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {")
        lines.append(f'\t\t\t\t\t\t\t\t\'unitType\', "{ut}",')
        if w is not None:
            lines.append(f"\t\t\t\t\t\t\t\t'spawnWeight', {w},")
        lines.append("\t\t\t\t\t\t\t}),")
    lines += [
        "\t\t\t\t\t\t},",
        f"\t\t\t\t\t\t'UnitCountMin', {n},",
        f"\t\t\t\t\t\t'UnitCountMax', {n},",
        "\t\t\t\t\t}),",
    ]
    return "\n".join(lines)


BLOCK = f"""\t\t\tPlaceObj('ModItemEnemySquads', {{
\t\t\t\tComment = "Villa siege Ernie column Normal base 30; Easy/Hard +-10 later; not ClearTheWay-clearable",
\t\t\t\tUnits = {{
{slot([("JAZZ_Legion_LeaderT1_Sergeant", None)], 1)}
{slot([("JAZZ_Legion_FrontT1_Bonemaker", None)], 1)}
{slot([
    ("JAZZ_Legion_AssaultT2_ShockTrooper", None),
    ("JAZZ_Legion_AssaultT1_Roughneck", 40),
], 6)}
{slot([
    ("JAZZ_Legion_FrontT2_Raider", None),
    ("JAZZ_Legion_FrontT1_Marauder", 40),
], 6)}
{slot([
    ("JAZZ_Legion_FrontT2_Ambusher", None),
    ("JAZZ_Legion_FrontT2_Marksman", 50),
], 3)}
{slot([
    ("JAZZ_Legion_AssaultT1_Roughneck", None),
    ("JAZZ_Legion_FrontT1_Rifleman", None),
], 5)}
{slot([
    ("JAZZ_Legion_GunnerT2_GMPG", None),
    ("JAZZ_Legion_GunnerT1_Gunner", 40),
], 3)}
{slot([("JAZZ_Legion_AssaultT1_Grenadier", None)], 2)}
{slot([("JAZZ_Legion_HeavyT3_Mortarman", None)], 1)}
{slot([("JAZZ_Legion_HeavyT1_Rocketeer", None)], 1)}
{slot([
    ("JAZZ_Legion_FrontT3_Veteran", None),
    ("JAZZ_Legion_AssaultT3_Punisher", 40),
], 1)}
\t\t\t\t}},
\t\t\t\tcomment = "-- Villa siege Ernie column base 30",
\t\t\t\tdisplayName = T(623794979175, --[[ModItemEnemySquads {SQUAD_ID} displayName]] "Осадный отряд"),
\t\t\t\tgroup = "Default",
\t\t\t\tid = "{SQUAD_ID}",
\t\t\t}}),
"""

META_PRESET = f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', \"EnemySquads\",
\t\t\t'Id', \"{SQUAD_ID}\",
\t\t\t'ClassDisplayName', \"Enemy Squads\",
\t\t}}),
"""


def main() -> None:
    text = UNITS.read_text(encoding="utf-8")
    if f'id = "{SQUAD_ID}"' in text:
        print("already present in items")
    else:
        # Insert after SentrySquad_AroundVilla
        idx = text.find('id = "JAZZ_Legion_SentrySquad_AroundVilla"')
        if idx < 0:
            raise SystemExit("Sentry not found")
        # end of that PlaceObj
        start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, idx)
        brace = text.find("{", start)
        depth = 0
        j = brace
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        if text[j : j + 2] == "),":
            j += 2
        text = text[:j] + "\n" + BLOCK + text[j:]
        UNITS.write_text(text, encoding="utf-8")
        print("inserted", SQUAD_ID, "into items")

    meta = META.read_text(encoding="utf-8")
    if f'Id", "{SQUAD_ID}"' in meta or f"Id', \"{SQUAD_ID}\"" in meta:
        print("already in metadata")
    else:
        # after SentrySquad preset
        needle = "'Id', \"JAZZ_Legion_SentrySquad_AroundVilla\","
        m = meta.find(needle)
        if m < 0:
            raise SystemExit("sentry meta not found")
        # end of that ModResourcePreset
        start = meta.rfind("PlaceObj('ModResourcePreset'", 0, m)
        brace = meta.find("{", start)
        depth = 0
        j = brace
        while j < len(meta):
            if meta[j] == "{":
                depth += 1
            elif meta[j] == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        if meta[j : j + 2] == "),":
            j += 2
        meta = meta[:j] + "\n" + META_PRESET + meta[j:]
        META.write_text(meta, encoding="utf-8")
        print("inserted metadata preset")


if __name__ == "__main__":
    main()
