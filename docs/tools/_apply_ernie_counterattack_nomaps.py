# -*- coding: utf-8 -*-
"""Add ErnieCounterAttack_NoMaps (20, no mortar) + remap in jazz-nomaps."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")
UNITS = ROOT / "jazz-units" / "items.lua"
META = ROOT / "jazz-units" / "metadata.lua"
NOMAPS = ROOT / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"

PACK_ID = "ErnieCounterAttack_NoMaps"

# 20 bodies: cut from maps 30; drop Mortarman
PACK = f"""\t\t\tPlaceObj('ModItemEnemySquads', {{
\t\t\t\tComment = \"NoMaps Ernie_CounterAttack punitive (I7->I5); base 20; no mortar\",
\t\t\t\tUnits = {{
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_LeaderT1_Sergeant\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_AssaultT1_Roughneck\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_AssaultT2_ShockTrooper\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 5,
\t\t\t\t\t\t'UnitCountMax', 5,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT2_Ambusher\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT2_Raider\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 3,
\t\t\t\t\t\t'UnitCountMax', 3,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_AssaultT1_Grenadier\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_GunnerT2_GMPG\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_HeavyT1_Rocketeer\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT3_Veteran\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {{
\t\t\t\t\t\t'weightedList', {{
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {{
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT1_Bonemaker\",
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}}),
\t\t\t\t}},
\t\t\t\tcomment = \"-- NoMaps ErnieCounterAttack ~20; no Mortarman (maps keeps 30+mortar)\",
\t\t\t\tdisplayName = T(890000000012601, --[[ModItemEnemySquads ErnieCounterAttack_NoMaps displayName]] \"Штурмовики Легиона\"),
\t\t\t\tgroup = \"Special\",
\t\t\t\tid = \"{PACK_ID}\",
\t\t\t}}),
"""


def main() -> None:
    units = UNITS.read_text(encoding="utf-8")
    if f'id = "{PACK_ID}"' in units:
        print(f"{PACK_ID} already in items")
    else:
        anchor = '\tid = "FortressDefenders_NoMaps",\n\t\t\t}),\n'
        if anchor not in units:
            raise SystemExit("FortressDefenders_NoMaps anchor missing")
        units = units.replace(anchor, anchor + PACK, 1)
        UNITS.write_text(units, encoding="utf-8", newline="\n")
        print(f"inserted {PACK_ID}")

    meta = META.read_text(encoding="utf-8")
    if f"'Id', \"{PACK_ID}\"" not in meta:
        anchor = """\t\t\t'Id', "FortressDefenders_NoMaps",
\t\t\t'ClassDisplayName', "Enemy Squads",
\t\t}),
"""
        ins = (
            anchor
            + f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', "EnemySquads",
\t\t\t'Id', "{PACK_ID}",
\t\t\t'ClassDisplayName', "Enemy Squads",
\t\t}}),
"""
        )
        if anchor not in meta:
            raise SystemExit("metadata anchor missing")
        META.write_text(meta.replace(anchor, ins, 1), encoding="utf-8", newline="\n")
        print("metadata preset added")
    else:
        print("metadata already has preset")

    nomaps = NOMAPS.read_text(encoding="utf-8")
    if 'ErnieCounterAttack = "ErnieCounterAttack_NoMaps"' in nomaps:
        print("remap already present")
    else:
        needle = '\tFortressDefenders = "FortressDefenders_NoMaps",\n'
        if needle not in nomaps:
            raise SystemExit("FortressDefenders remap line missing")
        nomaps = nomaps.replace(
            needle,
            needle + '\tErnieCounterAttack = "ErnieCounterAttack_NoMaps",\n',
            1,
        )
        NOMAPS.write_text(nomaps, encoding="utf-8", newline="\n")
        print("SQUAD_REMAP added")

    # verify sum
    u = UNITS.read_text(encoding="utf-8")
    i = u.find(f'id = "{PACK_ID}"')
    s = u.rfind("PlaceObj('ModItemEnemySquads'", 0, i)
    total = sum(int(x) for x in re.findall(r"'UnitCountMin', (\d+)", u[s:i]))
    assert total == 20, total
    assert "'unitType', \"JAZZ_Legion_HeavyT3_Mortarman\"" not in u[s:i]
    print(f"OK {PACK_ID} sum={total}, no mortar unit")


if __name__ == "__main__":
    main()
