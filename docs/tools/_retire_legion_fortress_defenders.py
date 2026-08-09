"""Delete LegionFortressDefenders; add FortressDefenders_NoMaps (~16); patch NoMaps remap."""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
META = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua")
NOMAPS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-nomaps\Code\NoMaps_Autonomy.lua")

NOMAPS_PACK = """\t\t\tPlaceObj('ModItemEnemySquads', {
\t\t\t\tComment = \"NoMaps fort/outpost garrison ~16 (half of retired LegionFortressDefenders 32)\",
\t\t\t\tUnits = {
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_LeaderT1_Sergeant\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT1_Bonemaker\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_GunnerT2_GMPG\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_GunnerT1_Gunner\",
\t\t\t\t\t\t\t\t'spawnWeight', 40,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT2_Marksman\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT2_Ambusher\",
\t\t\t\t\t\t\t\t'spawnWeight', 50,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT2_Raider\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FrontT1_Marauder\",
\t\t\t\t\t\t\t\t'spawnWeight', 40,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 3,
\t\t\t\t\t\t'UnitCountMax', 3,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_AssaultT2_ShockTrooper\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_AssaultT1_Roughneck\",
\t\t\t\t\t\t\t\t'spawnWeight', 50,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 3,
\t\t\t\t\t\t'UnitCountMax', 3,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_AssaultT1_Grenadier\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_HeavyT1_Rocketeer\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 1,
\t\t\t\t\t\t'UnitCountMax', 1,
\t\t\t\t\t}),
\t\t\t\t\tPlaceObj('EnemySquadUnit', {
\t\t\t\t\t\t'weightedList', {
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FlankerT2_Scout\",
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t\tPlaceObj('UnitTypeListWithWeights', {
\t\t\t\t\t\t\t\t'unitType', \"JAZZ_Legion_FlankerT1_Warden\",
\t\t\t\t\t\t\t\t'spawnWeight', 40,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\t'UnitCountMin', 2,
\t\t\t\t\t\t'UnitCountMax', 2,
\t\t\t\t\t}),
\t\t\t\t},
\t\t\t\tcomment = \"-- NoMaps fort garrison ~16 (half of old LegionFortressDefenders)\",
\t\t\t\tdisplayName = T(323511335269, --[[ModItemEnemySquads FortressDefenders_NoMaps displayName]] \"Гарнизон Ло Блё\"),
\t\t\t\tgroup = \"Special\",
\t\t\t\tid = \"FortressDefenders_NoMaps\",
\t\t\t}),
"""


def main() -> None:
    text = UNITS.read_text(encoding="utf-8")

    if 'id = "LegionFortressDefenders"' in text:
        i = text.find('id = "LegionFortressDefenders"')
        start = text.rfind("PlaceObj('ModItemEnemySquads'", 0, i)
        end_m = re.search(r"\n\t\t\t\t\}\),\n", text[i:])
        if not end_m:
            raise SystemExit("end of LegionFortressDefenders not found")
        end = i + end_m.end()
        text = text[:start] + text[end:]
        print("removed LegionFortressDefenders")
    else:
        print("LegionFortressDefenders already absent")

    if 'id = "FortressDefenders_NoMaps"' not in text:
        anchor = "\t\t\t}),\n\t\tPlaceObj('ModItemFolder', {\n\t\t\t'name', \"Deprecated\","
        if anchor not in text:
            idx = text.find("'name', \"Deprecated\"")
            print(repr(text[max(0, idx - 100) : idx + 40]))
            raise SystemExit("Vanilla→Deprecated anchor missing")
        text = text.replace(anchor, NOMAPS_PACK + "\t\t\t}),\n\t\tPlaceObj('ModItemFolder', {\n\t\t\t'name', \"Deprecated\",", 1)
        print("inserted FortressDefenders_NoMaps into Vanilla")
    else:
        print("FortressDefenders_NoMaps already present")

    UNITS.write_text(text, encoding="utf-8")

    meta = META.read_text(encoding="utf-8")
    meta_new, n = re.subn(
        r"\t\tPlaceObj\('ModResourcePreset', \{\n\t\t\t'Class', \"EnemySquads\",\n\t\t\t'Id', \"LegionFortressDefenders\",\n\t\t\t'ClassDisplayName', \"Enemy Squads\",\n\t\t\}\),\n",
        "",
        meta,
        count=1,
    )
    print(f"metadata removed LegionFortressDefenders={n}")
    meta = meta_new
    if "'Id', \"FortressDefenders_NoMaps\"" not in meta:
        add = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"EnemySquads\",\n"
            "\t\t\t'Id', \"FortressDefenders_NoMaps\",\n"
            "\t\t\t'ClassDisplayName', \"Enemy Squads\",\n"
            "\t\t}),\n"
        )
        for key in ("LegionAttackSquad_01", "LegionRaidSquad_01", "ErnieCounterAttack"):
            block = (
                "\t\tPlaceObj('ModResourcePreset', {\n"
                f"\t\t\t'Class', \"EnemySquads\",\n"
                f"\t\t\t'Id', \"{key}\",\n"
                "\t\t\t'ClassDisplayName', \"Enemy Squads\",\n"
                "\t\t}),\n"
            )
            if block in meta:
                meta = meta.replace(block, block + add, 1)
                print(f"metadata added FortressDefenders_NoMaps after {key}")
                break
        else:
            raise SystemExit("could not place FortressDefenders_NoMaps in metadata")
    META.write_text(meta, encoding="utf-8")

    nm = NOMAPS.read_text(encoding="utf-8")
    nm2 = nm.replace(
        'FortressDefenders = "LegionFortressDefenders",',
        'FortressDefenders = "FortressDefenders_NoMaps",',
        1,
    )
    nm2 = nm2.replace(
        'garrison = { "LegionGlobalAI_Garrison", "FortressDefenders", "LegionFortressDefenders" },',
        'garrison = { "LegionGlobalAI_Garrison", "FortressDefenders_NoMaps" },',
        1,
    )
    if nm2 == nm:
        raise SystemExit("NoMaps Autonomy unchanged — check strings")
    NOMAPS.write_text(nm2, encoding="utf-8")
    print("NoMaps Autonomy updated")


if __name__ == "__main__":
    main()
