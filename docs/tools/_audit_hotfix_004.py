#!/usr/bin/env python3
"""Static regression checks for JAZZ-HOTFIX-004 (no game runtime required)."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    emp = (ROOT / "Code" / "System_EmplacementAmmo.lua").read_text(encoding="utf-8")
    unit = (ROOT / "Code" / "System_OR_Unit.lua").read_text(encoding="utf-8")

    check("function Jazz_ReseatMannedEmplacements" in emp, "reseat helper is a top-level function")
    check("g_JAZZ_EnterEmplacementWrapped" in emp and "g_JAZZ_EnterEmplacementBase" in emp, "EnterEmplacement wrap flags are declared")
    check("function Unit:EnterEmplacement" in emp, "EnterEmplacement wrap is installed")
    check("GetOperatePos" in emp and "SetEffectValue" in emp and '"hmg_emplacement"' in emp, "nil-weapon EnterEmplacement keeps handle without requiring owner")
    check("function OnMsg.LoadGame" in emp and "function OnMsg.EnterSector" in emp, "LoadGame and EnterSector queue reseat")
    check('QueueCommand("MGTarget"' in emp or "QueueCommand('MGTarget'" in emp, "Idle reseat restores MGTarget cone")
    check("FlushCombatCache" in emp and "RecalcUIActions(true)" in emp, "reseat refreshes combat cache and HUD")

    check("obj:Update()" in unit, "GetActiveWeapons retries emplacement Update when weapon is missing")
    check("weapon and firing_id == \"Attack\"" in unit or "weapon and firing_id == 'Attack'" in unit, "ResolveDefaultFiringModeAction gates Attack HasComponent on weapon")
    check("weapon:HasComponent(\"EnableRunNGun\")" in unit, "EnableRunNGun still consulted")
    enable_rng = unit.find("weapon:HasComponent(\"EnableRunNGun\")")
    check(enable_rng > 0, "EnableRunNGun call exists")
    window = unit[max(0, enable_rng - 80) : enable_rng]
    check("weapon and" in window or "if weapon" in window, "EnableRunNGun HasComponent is nil-guarded")

    recalc = unit.find("function Unit:RecalcUIActions")
    check(recalc >= 0, "RecalcUIActions override exists")
    manning = unit.find('HasStatusEffect("ManningEmplacement")', recalc)
    action_id = unit.find("action.id", manning)
    check(manning > 0 and action_id > manning, "ManningEmplacement HUD still uses default attack id")
    prefix = unit[max(recalc, action_id - 220) : action_id]
    check("if action then" in prefix or "if action and" in prefix, "RecalcUIActions does not index nil default attack")

    print("RESULT: PASSED (JAZZ-HOTFIX-004 static audit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
