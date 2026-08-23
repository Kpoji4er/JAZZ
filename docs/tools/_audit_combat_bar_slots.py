#!/usr/bin/env python3
"""Static check: two-row CombatActionBar has UIAction presets for slots 14-25.

RecalcUIActions padding to 24 is not enough: CombatActionsToActions only
spawns buttons for Action1..ActionN presets. TakeCover/Overwatch at index
14+ stay invisible without Action14-24; signature remap needs Action25.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    unit = (ROOT / "Code" / "System_OR_Unit.lua").read_text(encoding="utf-8")
    items = (ROOT / "items.lua").read_text(encoding="utf-8")

    recalc = unit.find("function Unit:RecalcUIActions")
    check(recalc >= 0, "RecalcUIActions override exists")
    window = unit[recalc : unit.find("function Unit:GetActiveWeapons", recalc)]
    check("combat_bar_slots = 24" in window, "RecalcUIActions reserves 24 combat slots")
    check("signature_slot = combat_bar_slots + 1" in window, "signature sits at slot 25")

    check("function Jazz_RegisterExtraCombatBarSlots" in unit or "local function Jazz_RegisterExtraCombatBarSlots" in unit,
          "Jazz_RegisterExtraCombatBarSlots is present")
    check("Jazz_ResolveCombatBarSlot" in unit, "slot ResolveAction helper is present")
    check("for i = 14, 24 do" in unit, "registers Action14-Action24")
    check('Jazz_CopyCombatBarSlotProxy(proto, "Action25", 25' in unit
          or "Action25" in unit and "signature" in unit.lower(),
          "registers Action25 signature slot")
    check('KeybindingFromAction = "actionRedirectSignatureAbility"' in unit,
          "Action25 keeps signature key redirect")
    check("function OnMsg.DataLoaded" in unit, "registers slots on DataLoaded")
    check("function OnMsg.ModsReloaded" in unit, "registers slots on ModsReloaded")

    bar = items.find("'Id', \"idCombatActionsContainer\"")
    if bar < 0:
        bar = items.find('"Id", "idCombatActionsContainer"')
    check(bar >= 0, "CombatActionBar override still in items.lua")
    container = items[bar : bar + 800]
    check("'LayoutMethod', \"HWrap\"" in container or '"LayoutMethod", "HWrap"' in container,
          "combat actions container is HWrap")

    print("RESULT: PASSED (combat bar Action14-25 slots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
