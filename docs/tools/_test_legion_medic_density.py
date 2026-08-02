# Static check for JAZZ-STRATEGY-015 medic density helpers + composition wiring.
# Run: python docs/tools/_test_legion_medic_density.py
from __future__ import annotations

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

# Mirror Lua formula in Python
def max_medics(n: int) -> int:
    if n < 1:
        return 0
    per = 15
    min_size = 10
    by_ratio = n // per
    if n >= min_size:
        return max(1, by_ratio)
    return by_ratio

expect('MedicPerMen = 15' in COMP, "MedicPerMen=15 missing")
expect('MedicMinSquadSize = 10' in COMP, "MedicMinSquadSize=10 missing")
expect("JAZZ_Legion_FrontT1_Bonemaker" in COMP, "Bonemaker unit id missing")
expect("function JAZZ_GetLegionMaxMedics" in COMP, "JAZZ_GetLegionMaxMedics missing")
expect("lMedicPlan" in GEN, "lMedicPlan missing in generator")
expect('entry.bucket ~= "medic"' in GEN, "generator must exclude medic from random line picks")
expect("medic_need" in GEN, "top-up medic preference missing")

cases = {8: 0, 10: 1, 12: 1, 14: 1, 15: 1, 18: 1, 29: 1, 30: 2, 40: 2}
for n, want in cases.items():
    got = max_medics(n)
    expect(got == want, f"max_medics({n})={got}, want {want}")

# qrf/retribution allow medic without FrontT1 prefix
expect('role == "retribution"' in COMP, "retribution medic allow missing")
expect('role == "qrf"' in COMP, "qrf medic allow missing")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK STRATEGY-015 medic density static checks")
for n, want in cases.items():
    print(f"  n={n} -> {want}")
