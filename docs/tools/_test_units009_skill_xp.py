"""Static AC-001..004 / AC-016 checks for JAZZ-UNITS-009 skill XP.

No JA3 runtime. Parses jazz-units/Code/StatGainRework.lua and melee UnitStat files.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
LUA = UNITS / "Code" / "StatGainRework.lua"
EXP = UNITS / "Code" / "ExperienceSys.lua"


def muldivround(a: int, b: int, c: int) -> int:
    return (a * b + c // 2) // c


def threshold(s: int) -> int | None:
    if s >= 100:
        return None
    if s <= 29:
        return 150
    if s <= 49:
        return 250
    if s <= 64:
        return 400
    if s <= 79:
        return 800
    t = 1600
    for _ in range(80, s):
        t = muldivround(t, 3, 2)
    return t


def cumulative(a: int, b: int) -> int:
    return sum(threshold(s) or 0 for s in range(a, b))


def parse_frozen_table(text: str) -> dict[int, int]:
    block = re.search(r"local kTFrom80 = \{(.*?)\}", text, re.S)
    if not block:
        raise SystemExit("kTFrom80 table missing")
    return {int(s): int(v) for s, v in re.findall(r"\[(\d+)\]\s*=\s*(\d+)", block.group(1))}


def main() -> int:
    errors: list[str] = []
    lua = LUA.read_text(encoding="utf-8")
    frozen = parse_frozen_table(lua)

    for s in range(80, 100):
        got = frozen.get(s)
        want = threshold(s)
        if got != want:
            errors.append(f"T({s}) frozen {got} != {want}")
    if frozen.get(90) != 92267:
        errors.append(f"T(90) {frozen.get(90)} != 92267")
    if frozen.get(99) != 3547083:
        errors.append(f"T(99) {frozen.get(99)} != 3547083")

    checks = {
        (50, 70): 10000,
        (80, 81): 1600,
        (80, 82): 4000,
        (80, 83): 7600,
        (80, 90): 181331,
    }
    for (a, b), want in checks.items():
        got = cumulative(a, b)
        if got != want:
            errors.append(f"cumul {a}->{b} {got} != {want}")

    exp = EXP.read_text(encoding="utf-8")
    if re.search(r"statGainingPoints\s*=", exp):
        errors.append("ExperienceSys still assigns statGainingPoints")
    award = lua.split("function Jazz_AwardSkillPractice", 1)[-1]
    award = award.split("function Jazz_MeleePracticeStat", 1)[0]
    if "InteractionRand" in award:
        errors.append("InteractionRand inside Jazz_AwardSkillPractice")
    roll = lua.split("function RollForStatGaining", 1)[-1]
    roll = roll.split("function ReceiveStatGainingPoints", 1)[0]
    if "InteractionRand" in roll:
        errors.append("InteractionRand inside RollForStatGaining")

    for wis, want in ((0, 0), (15, 25), (30, 50), (60, 100), (90, 150), (100, 167)):
        got = muldivround(100, wis, 60)
        if got != want:
            errors.append(f"Wis {wis} preset100 -> {got} != {want}")
    for wis, want in ((0, 0), (15, 4), (30, 8), (60, 16), (90, 24), (100, 27)):
        got = muldivround(16, wis, 60)
        if got != want:
            errors.append(f"Wis {wis} marks aim2 hit -> {got} != {want}")

    melee = {
        "Machete": "Strength",
        "Machete_Balanced": "Strength",
        "Machete_Sharpened": "Strength",
        "PierreMachete": "Strength",
        "Bayonet": "Strength",
        "Trench_Shovel": "Strength",
        "Unarmed": "Strength",
        "Knife": "Dexterity",
        "Knife_Balanced": "Dexterity",
        "Knife_Sharpened": "Dexterity",
    }
    for name, stat in melee.items():
        path = JAZZ / "InventoryItem" / f"{name}.lua"
        body = path.read_text(encoding="utf-8")
        if f'UnitStat = "{stat}"' not in body:
            errors.append(f"{name} UnitStat != {stat}")

    needed = (
        "function Jazz_SkillXPThreshold",
        "function Jazz_AwardSkillPractice",
        "function Jazz_MeleePracticeStat",
        "function Jazz_SkillPracticeRollover",
        "function Jazz_FindWillRegenLeader",
        "function RollForStatGaining",
        "function ReceiveStatGainingPoints",
        "890000000010900",
        "Jazz_SkillXPThreshold = Jazz_SkillXPThreshold",
        "Jazz_AwardSkillPractice = Jazz_AwardSkillPractice",
    )
    for token in needed:
        if token not in lua:
            errors.append(f"missing {token}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK AC-001/002/003/004/016 static")
    print("T(90)=92267 T(99)=3547083 cumul50-70=10000 cumul80-90=181331")
    return 0


if __name__ == "__main__":
    sys.exit(main())
