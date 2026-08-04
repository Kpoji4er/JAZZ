# -*- coding: utf-8 -*-
"""Static: Guardpost scripted ForceSet vs managed auto-aggro mute.

Invariant (Ernie_CounterAttack / Legion AI managed posts):
  - ForceSetNextSpawnTimeAndSector must NOT call CanSpawnNewSquad (deadlock).
  - CanSpawnNewSquad / Update / SpawnEnemySquad keep JAZZ_IsLegionAIManagedGuardpost
    early-out so vanilla auto aggro stays muted.

Exit 0 = OK, 1 = FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GP = ROOT / "Code" / "Guardpost.lua"


def extract_function(src: str, name: str) -> str | None:
    # Match from "function Guardpost:Name" to next top-level function/end of file heuristic
    m = re.search(
        rf"(function Guardpost:{re.escape(name)}\s*\(.*?)\n(?=function |\Z)",
        src,
        re.DOTALL,
    )
    return m.group(1) if m else None


def main() -> int:
    if not GP.is_file():
        print(f"FAIL: missing {GP}")
        return 1
    src = GP.read_text(encoding="utf-8")
    fail = 0

    fs = extract_function(src, "ForceSetNextSpawnTimeAndSector")
    if not fs:
        print("FAIL: ForceSetNextSpawnTimeAndSector not found")
        return 1
    # Strip Lua comments before call detection
    fs_code = re.sub(r"--[^\n]*", "", fs)
    if re.search(r"CanSpawnNewSquad\s*\(", fs_code):
        print("FAIL: ForceSet still calls CanSpawnNewSquad (scripted deadlock risk)")
        fail = 1
    else:
        print("OK: ForceSet does not call CanSpawnNewSquad")
    if "forced_attack = true" not in fs and "forced_attack=true" not in fs.replace(" ", ""):
        # tolerate spacing
        if not re.search(r"forced_attack\s*=\s*true", fs):
            print("FAIL: ForceSet missing forced_attack = true")
            fail = 1
        else:
            print("OK: ForceSet sets forced_attack")
    else:
        print("OK: ForceSet sets forced_attack")
    if "primed_squad" not in fs:
        print("FAIL: ForceSet busy check should mention primed_squad")
        fail = 1

    for fname in ("CanSpawnNewSquad", "SpawnEnemySquad", "Update"):
        body = extract_function(src, fname)
        if not body:
            print(f"FAIL: {fname} not found")
            fail = 1
            continue
        if "JAZZ_IsLegionAIManagedGuardpost" not in body:
            print(f"FAIL: {fname} missing managed early-out (auto aggro would return)")
            fail = 1
        else:
            print(f"OK: {fname} keeps managed early-out")

    return fail


if __name__ == "__main__":
    sys.exit(main())
