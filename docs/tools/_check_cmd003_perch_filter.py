# CMD-003: perch is family/UnitData/keywords — no aura OccupyHeights short-circuit,
# no current_archetype Frontliner. HighGround ×175 gated on jazz_occupy_heights
# after ApplyProfile sets it only for perch/spotter.
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMBAT = ROOT / "Code" / "CombatAI.lua"
PROFILES = ROOT / "Code" / "AIContextProfiles.lua"


def extract_fn(text: str, name: str) -> str:
    start = text.find(f"function {name}")
    if start < 0:
        return ""
    nxt = text.find("\nfunction ", start + 1)
    if nxt < 0:
        nxt = len(text)
    return text[start:nxt]


def main() -> int:
    combat = COMBAT.read_text(encoding="utf-8")
    profiles = PROFILES.read_text(encoding="utf-8")
    failed: list[str] = []

    perch = extract_fn(combat, "JazzAI_UnitIsLinePerchHolder")
    if not perch:
        failed.append("JazzAI_UnitIsLinePerchHolder missing")
    else:
        if "jazz_occupy_heights" in perch:
            failed.append("perch still short-circuits on jazz_occupy_heights")
        if "OccupyHeights" in perch:
            failed.append("perch still short-circuits on directive OccupyHeights")
        if "current_archetype" in perch or "Frontliner" in perch:
            failed.append("perch must not use current_archetype / Frontliner stance")
        if "JazzAI_UnitRoleFamily" not in perch:
            failed.append("perch must use JazzAI_UnitRoleFamily")
        if 'family == "Scout"' not in perch:
            failed.append("perch must reject Scout family")

    family = extract_fn(combat, "JazzAI_UnitRoleFamily")
    if "JazzAI_InferRoleFamily" not in family:
        failed.append("JazzAI_UnitRoleFamily must call jazz-units InferRoleFamily when present")

    apply = extract_fn(profiles, "JazzAI_ApplyProfileToContext")
    if "jazz_heights_cling" not in apply:
        failed.append("ApplyProfile missing jazz_heights_cling")
    if "JazzAI_UnitIsLinePerchHolder" not in apply:
        failed.append("ApplyProfile must gate occupy_heights on perch")
    if re.search(r'jazz_occupy_heights = directive == "OccupyHeights"', apply):
        failed.append("ApplyProfile still sets occupy_heights for whole aura")

    picker = extract_fn(profiles, "JazzAI_PickOfficerDirective")
    if "JazzAI_AuraHasLiveSpotterShot" not in picker:
        failed.append("picker missing live spotter Push")
    if "JazzAI_DirectivePushLiveShot" not in picker:
        failed.append("picker missing Push 600 live-shot weight")

    if "function JazzAI_UnitHasLiveShot" not in profiles:
        failed.append("JazzAI_UnitHasLiveShot missing")
    cling = extract_fn(profiles, "JazzAI_PickHeightsClingAnchor")
    if not cling:
        failed.append("JazzAI_PickHeightsClingAnchor missing")
    else:
        if "ally == unit then" in cling and "return false" in cling.split("ally == unit then", 1)[1][:80]:
            failed.append("medic cling must not abort on self before other patients")
        if "45 *" not in cling:
            failed.append("medic cling missing OptLoc 45 radius")
    if "function JazzAI_ScoreHeightsClingDest" not in combat:
        failed.append("JazzAI_ScoreHeightsClingDest missing")

    if failed:
        print("FAIL: CMD-003 perch/cling/push")
        for e in failed:
            print(" -", e)
        return 1
    print("PASS: CMD-003 perch family filter, cling, live-shot Push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
