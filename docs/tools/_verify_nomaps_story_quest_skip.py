# -*- coding: utf-8 -*-
"""Static: COMPAT-010/011 story/quest UnitData remap skips in jazz-nomaps.

G6 WaterWell, A2 DiamondRedSquad, F5 beach, Pierrot; I1 Flag Hill; H4 Pierre.
Exit 0 = OK, 1 = FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NOMAPS = Path(__file__).resolve().parents[2].parent / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"


def main() -> int:
    if not NOMAPS.is_file():
        print("FAIL: missing", NOMAPS)
        return 1
    text = NOMAPS.read_text(encoding="utf-8")
    errors: list[str] = []

    def need(pat: str, msg: str) -> None:
        if not re.search(pat, text, re.M):
            errors.append(msg)

    need(
        r"local STORY_SQUAD_KEEP_VANILLA_UNITS\s*=\s*\{[^}]*DiamondRedSquad\s*=\s*true",
        "STORY_SQUAD_KEEP_VANILLA_UNITS missing DiamondRedSquad",
    )
    need(
        r"local QUEST_MARKER_GROUPS_KEEP_VANILLA\s*=\s*\{[^}]*LegionWaterWell\s*=\s*true",
        "QUEST_MARKER_GROUPS_KEEP_VANILLA missing LegionWaterWell",
    )
    need(
        r'g_JAZZ_NoMapsSkipUnitRemap\s*=\s*rawget\(_G,\s*"g_JAZZ_NoMapsSkipUnitRemap"\)',
        "g_JAZZ_NoMapsSkipUnitRemap not predeclared at load",
    )
    need(
        r"function lRemapUnitTemplate\([^)]*\)\s*\n\s*if rawget\(_G, \"g_JAZZ_NoMapsSkipUnitRemap\"\)",
        "lRemapUnitTemplate does not honor skip flag first",
    )
    need(
        r"sector_id == \"F5\" and squad_def_id == \"LegionDefenders_Balanced_Easy\"",
        "F5 LegionDefenders_Balanced_Easy skip missing in GenerateEnemySquad",
    )
    need(
        r"not lShouldKeepVanillaUnitClass\(session_id, unitdata\)",
        "lRemapEnemyUnitTemplates missing keep-vanilla gate",
    )
    need(
        r"lMarkerHasQuestKeepGroup",
        "UnitMarker wrapper missing quest-group skip helper",
    )
    need(
        r"unit\.conflict_ignore = true",
        "Pierrot conflict_ignore assign missing",
    )
    need(
        r"NPC_CaptainPierrot",
        "NPC_CaptainPierrot persist id missing",
    )
    need(
        r"lProtectCaptainPierrot\(\)",
        "lProtectCaptainPierrot never called",
    )
    need(
        r"lShouldKeepVanillaUnitClass\(unit_id, unitdata\)",
        "lRefreshEnemyLoadouts missing keep-vanilla gear skip",
    )
    need(
        r"local SECTORS_KEEP_VANILLA_UNITS\s*=\s*\{[^}]*I1\s*=\s*true",
        "SECTORS_KEEP_VANILLA_UNITS missing I1",
    )
    need(
        r"local STORY_SQUAD_KEEP_VANILLA_UNITS\s*=\s*\{[^}]*FortressPierre\s*=\s*true",
        "STORY_SQUAD_KEEP_VANILLA_UNITS missing FortressPierre",
    )
    need(
        r'class == "Pierre"',
        "Pierre class keep-vanilla missing",
    )
    need(
        r"NPC_Pierre",
        "NPC_Pierre persist keep-vanilla missing",
    )
    need(
        r"lSectorKeepsVanillaUnits\(rawget\(_G, \"gv_CurrentSectorId\"\)\)",
        "UnitMarker I1 sector skip missing",
    )
    if "function GenerateEnemySquad(squad_def_id, ...)" in text:
        errors.append("GenerateEnemySquad still uses varargs-only remap (need sector_id skip)")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK — COMPAT-010/011 story/quest skip + Pierrot/Pierre protect present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
