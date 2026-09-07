# JAZZ-AI-DBG-001: option + CombatLog gate + dest/attack/abort hooks; no extra wrap.
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DBG = ROOT / "Code" / "AiDebugLog.lua"
ACTIONS = ROOT / "Code" / "AiActions.lua"
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"


def main() -> int:
    failed: list[str] = []
    dbg = DBG.read_text(encoding="utf-8")
    actions = ACTIONS.read_text(encoding="utf-8")
    items = ITEMS.read_text(encoding="utf-8")
    meta = META.read_text(encoding="utf-8")

    if "function JazzAI_DebugLogEnabled" not in dbg:
        failed.append("JazzAI_DebugLogEnabled missing")
    if "CurrentModOptions" not in dbg or "AIDebugLog" not in dbg:
        failed.append("enabled() must read CurrentModOptions.AIDebugLog")
    if "CombatLog" not in dbg:
        failed.append("CombatLog missing in AiDebugLog.lua")
    if not re.search(r'function JazzAI_DebugLogEnabled.*?clog\("short"', dbg, re.S):
        if 'clog("short"' not in dbg and 'CombatLog("short"' not in dbg:
            failed.append("CombatLog must use short (Snype / combat log)")
    if "dest_target_score" in dbg:
        failed.append("AiDebugLog must not dump dest_target_score")

    for name in (
        "JazzAI_DebugLogDest",
        "JazzAI_DebugLogAttack",
        "JazzAI_DebugLogAbort",
        "JazzAI_DebugStampAbort",
    ):
        if f"function {name}" not in dbg:
            failed.append(f"{name} missing")

    if "JazzAI_DebugLogDest(unit, unit.ai_context)" not in actions:
        failed.append("AIExecuteUnitBehavior must log dest")
    if 'kind = "dump"' not in actions:
        failed.append("Dump fire must call JazzAI_DebugLogAttack")
    if 'kind = "sig"' not in actions:
        failed.append("signature must call JazzAI_DebugLogAttack")
    if 'kind = "melee"' not in actions:
        failed.append("melee must call JazzAI_DebugLogAttack")
    if 'JazzAI_DebugLogDest(unit, context, "closest")' not in actions:
        failed.append("closest fallback must log dest")
    if "JazzAI_DebugLogAbort(unit, context, did_attack)" not in actions:
        failed.append("AIPlayAttacks must flush abort")
    for reason in ("no-target", "no-lof", "no-team-vis", "no-ap"):
        if f'JazzAI_DebugStampAbort(context, "{reason}")' not in actions:
            failed.append(f"missing abort stamp {reason}")

    wraps = len(re.findall(r"function AIPlayAttacks\(", actions))
    if wraps > 2:
        failed.append(f"extra AIPlayAttacks wrap ({wraps} defs)")

    if not re.search(r"name',\s*\"AIDebugLog\"", items):
        failed.append("items.lua missing ModItemOptionToggle AIDebugLog")
    if not re.search(r"name',\s*\"AiDebugLog\"", items):
        failed.append("items.lua missing ModItemCode AiDebugLog")
    if not re.search(
        r"name',\s*\"AIDebugLog\".*?DefaultValue',\s*false",
        items,
        re.S,
    ):
        failed.append("AIDebugLog toggle default must be false")
    if 'CodeFileName", "Code/AiDebugLog.lua"' not in items and "Code/AiDebugLog.lua" not in items:
        failed.append("items.lua missing Code/AiDebugLog.lua")

    if 'AIDebugLog = false' not in meta:
        failed.append("metadata.default_options missing AIDebugLog = false")
    if '"Code/AiDebugLog.lua"' not in meta:
        failed.append("metadata.code missing Code/AiDebugLog.lua")

    if failed:
        print("JAZZ-AI-DBG-001 FAIL:")
        for row in failed:
            print(" -", row)
        return 1
    print("JAZZ-AI-DBG-001 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
