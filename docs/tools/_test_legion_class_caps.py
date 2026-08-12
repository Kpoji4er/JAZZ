# Static check for JAZZ-HOTFIX-006 class caps (same-id + escort Front + Marksman deny).
# Run: python docs/tools/_test_legion_class_caps.py
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMP = (ROOT / "Code" / "LegionSquadComposition.lua").read_text(encoding="utf-8")
GEN = (ROOT / "Code" / "LegionSquadGenerator.lua").read_text(encoding="utf-8")

errors: list[str] = []


def expect(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


def same_id_cap(n: int) -> int:
    n = max(n, 1)
    return max(1, min(3, math.floor(n * 0.34)))


def escort_front_cap(n: int) -> int:
    n = max(n, 1)
    return min(2, max(1, math.floor(n * 0.25)))


expect("lSameIdCap" in GEN, "lSameIdCap missing")
expect("lEscortFrontCap" in GEN, "lEscortFrontCap missing")
expect("lIsEscortFrontLine" in GEN, "lIsEscortFrontLine missing")
expect("lWouldBreakSoftCap(units, candidate, target_size, role)" in GEN, "lWouldBreakSoftCap must take role")
expect("lWouldBreakSoftCap(units, entry.id, target, role)" in GEN, "build path must pass role")
expect("lWouldBreakSoftCap(current, entry.id, target, recipe_role)" in GEN, "top-up must pass recipe_role")
expect("JAZZ_LegionRoleIsLogisticsEscort" in GEN, "escort role helper missing in generator")
expect("JAZZ_LegionUncappedLineIds" in COMP, "uncapped line table missing")
expect("function JAZZ_IsLegionUncappedLineUnit" in COMP, "uncapped helper missing")
expect("function JAZZ_LegionSameIdCapApplies" in COMP, "VeryHard same-id gate missing")
expect('diff ~= "VeryHard"' in COMP, "same-id must skip VeryHard")
expect("JAZZ_LegionSameIdCapApplies" in GEN, "generator must honor VeryHard same-id gate")
for uid in (
    "JAZZ_Legion_AssaultT1_Roughneck",
    "JAZZ_Legion_AssaultT2_Pillager",
    "JAZZ_Legion_AssaultT2_ShockTrooper",
    "JAZZ_Legion_FrontT1_Rifleman",
    "JAZZ_Legion_FrontT1_Marauder",
    "JAZZ_Legion_FrontT2_Raider",
    "JAZZ_Legion_FrontT3_Veteran",
):
    expect(uid in COMP, f"uncapped list missing {uid}")

expect("deny_ids = base.deny_ids" in COMP, "Resolve must copy deny_ids")
expect("recipe.deny_ids" in COMP, "AllowedForRole must honor deny_ids")

# Marksman denied on the three FrontT2 escort recipes (tax/supply/shipment).
for role in ("tax", "supply", "shipment"):
    block = re.search(rf"{role}\s*=\s*\{{(.*?)\n\t\}},", COMP, re.S)
    expect(block is not None, f"{role} recipe block missing")
    if block:
        expect(
            "JAZZ_Legion_FrontT2_Marksman" in block.group(1),
            f"{role} must deny FrontT2_Marksman",
        )

same_cases = {4: 1, 5: 1, 6: 2, 8: 2, 9: 3, 12: 3, 25: 3, 40: 3}
for n, want in same_cases.items():
    got = same_id_cap(n)
    expect(got == want, f"same_id_cap({n})={got}, want {want}")

front_cases = {4: 1, 6: 1, 7: 1, 8: 2, 12: 2, 15: 2}
for n, want in front_cases.items():
    got = escort_front_cap(n)
    expect(got == want, f"escort_front_cap({n})={got}, want {want}")

# STRATEGY-008 bucket numbers must still be present (HOTFIX-006 is additive).
expect("mg = math.min(4, math.floor(n * 0.35))" in GEN, "MG soft cap formula changed")
expect("sniper = math.min(3, math.floor(n * 0.25))" in GEN, "sniper soft cap formula changed")
expect("specialist = math.min(3, math.floor(n * 0.20))" in GEN, "specialist soft cap formula changed")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK")
