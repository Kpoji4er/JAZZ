# PERF-004: AI shot gate is GetLoFData (CombatAI args), not a homemade object-ray.
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEAPONS = ROOT / "Code" / "System_OR_Weapons.lua"
ACTIONS = ROOT / "Code" / "AiActions.lua"
POLICY = ROOT / "Code" / "AIPolicy.lua"


def extract_fn(text: str, name: str) -> str:
    pat = re.compile(rf"(?:local )?function {re.escape(name)}\b")
    m = pat.search(text)
    if not m:
        return ""
    start = m.start()
    nxt = text.find("\nfunction ", start + 1)
    nxt_local = text.find("\nlocal function ", start + 1)
    cuts = [i for i in (nxt, nxt_local) if i > start]
    end = min(cuts) if cuts else len(text)
    return text[start:end]


def main() -> int:
    weapons = WEAPONS.read_text(encoding="utf-8")
    actions = ACTIONS.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")
    failed: list[str] = []

    for banned in (
        "Jazz_LookupEngineFn",
        "Jazz_DumpHardBlockObj",
        "Jazz_DumpCheapObjOnLine",
        "IntersectSegmentWithClosestObj",
        "JAZZ_DUMP_CHEAP_IMPASSABLE_SLABS",
    ):
        if banned in weapons:
            failed.append(f"homemade LoF leftover: {banned}")

    cheap = extract_fn(weapons, "Jazz_DumpCheapLineOfFire")
    helper = extract_fn(weapons, "Jazz_DumpGetAttackData")
    body = cheap + "\n" + helper
    if "GetLoFData" not in body:
        failed.append("Jazz_DumpCheapLineOfFire/GetAttackData must call GetLoFData")
    for token in ("obj = attacker", 'target_spot_group = "Torso"', "prediction = true"):
        if token not in helper:
            failed.append(f"GetLoFData args missing {token}")

    opts = extract_fn(actions, "AIGetAttackTargetingOptions")
    if "Jazz_DumpCheapLineBlocked" not in opts:
        failed.append("AIGetAttackTargetingOptions must abort on cheap LoF")

    basic = extract_fn(policy, "AIActionBasicAttack:Execute")
    if "Jazz_DumpCheapLineBlocked" not in basic:
        failed.append("AIActionBasicAttack:Execute must abort on cheap LoF")

    dump = extract_fn(actions, "AIPlayAttacks")
    if "Jazz_DumpCheapLineOfFire" not in dump:
        failed.append("AIPlayAttacks DumpFire must still call Jazz_DumpCheapLineOfFire")

    if failed:
        print("FAIL")
        for item in failed:
            print(f"  {item}")
        return 1
    print("OK cheap LoF: GetLoFData (CombatAI args) + targeting/execute abort")
    return 0


if __name__ == "__main__":
    sys.exit(main())
