# Static check for JAZZ-STRATEGY-015 medic density helpers + composition wiring.
# Run: python docs/tools/_test_legion_medic_density.py
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMP = (ROOT / "Code" / "LegionSquadComposition.lua").read_text(encoding="utf-8")
GEN = (ROOT / "Code" / "LegionSquadGenerator.lua").read_text(encoding="utf-8")

errors: list[str] = []


def expect(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


def max_medics(n: int, difficulty: str | None = None) -> int:
    """Mirror JAZZ_GetLegionMaxMedics (Normal +1 / Hard 0 / VeryHard −1)."""
    if n < 1:
        return 0
    per = 15
    min_size = 10
    by_ratio = n // per
    if n >= min_size:
        base = max(1, by_ratio)
    else:
        base = by_ratio
    diff = difficulty
    if diff in ("Easy", "VeryEasy"):
        diff = "Normal"
    if diff == "VeryHard":
        delta = -1
    elif diff == "Hard":
        delta = 0
    else:
        # Normal, unknown, or omitted (tests treat omit as Normal).
        delta = 1
    result = base + delta
    if n >= min_size:
        return max(1, result)
    return max(0, result)


expect("MedicPerMen = 15" in COMP, "MedicPerMen=15 missing")
expect("MedicMinSquadSize = 10" in COMP, "MedicMinSquadSize=10 missing")
expect("NormalMedicBonus = 1" in COMP, "NormalMedicBonus missing")
expect("VeryHardMedicPenalty = 1" in COMP, "VeryHardMedicPenalty missing")
expect("EasyMedicBonus" not in COMP, "stale EasyMedicBonus still present")
expect("function JAZZ_GetLegionMedicDifficultyDelta" in COMP, "difficulty delta helper missing")
expect("JAZZ_Legion_FrontT1_Bonemaker" in COMP, "Bonemaker unit id missing")
expect("function JAZZ_GetLegionMaxMedics" in COMP, "JAZZ_GetLegionMaxMedics missing")
expect("lMedicPlan" in GEN, "lMedicPlan missing in generator")
expect('entry.bucket ~= "medic"' in GEN, "generator must exclude medic from random line picks")
expect("medic_need" in GEN, "top-up medic preference missing")

# Hard (Commando) = usual / base formula.
hard_cases = {8: 0, 10: 1, 12: 1, 14: 1, 15: 1, 18: 1, 29: 1, 30: 2, 40: 2, 60: 4}
for n, want in hard_cases.items():
    got = max_medics(n, "Hard")
    expect(got == want, f"max_medics({n},Hard)={got}, want {want}")

# Default / omit in this mirror = Normal (+1). Runtime omit uses Game.game_difficulty.
normal_cases = {8: 1, 10: 2, 12: 2, 14: 2, 15: 2, 18: 2, 29: 2, 30: 3, 40: 3, 60: 5}
for n, want in normal_cases.items():
    got = max_medics(n, "Normal")
    expect(got == want, f"max_medics({n},Normal)={got}, want {want}")
    got_omit = max_medics(n)
    expect(got_omit == want, f"max_medics({n}) omit={got_omit}, want Normal {want}")

diff_cases = [
    (8, "Normal", 1),
    (8, "Hard", 0),
    (8, "VeryHard", 0),
    (8, "Easy", 1),
    (12, "Normal", 2),
    (12, "Hard", 1),
    (12, "VeryHard", 1),
    (30, "Normal", 3),
    (30, "Hard", 2),
    (30, "VeryHard", 1),
    (40, "Normal", 3),
    (40, "Hard", 2),
    (40, "VeryHard", 1),
    (60, "Normal", 5),
    (60, "Hard", 4),
    (60, "VeryHard", 3),
    (60, "VeryEasy", 5),
]
for n, diff, want in diff_cases:
    got = max_medics(n, diff)
    expect(got == want, f"max_medics({n},{diff})={got}, want {want}")

# qrf/retribution allow medic without FrontT1 prefix
expect('role == "retribution"' in COMP, "retribution medic allow missing")
expect('role == "qrf"' in COMP, "qrf medic allow missing")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK STRATEGY-015 medic density static checks")
for n, want in hard_cases.items():
    print(f"  n={n} Hard -> {want}")
for n, diff, want in diff_cases[:6]:
    print(f"  n={n} {diff} -> {want}")
