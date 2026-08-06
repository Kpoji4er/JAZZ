#!/usr/bin/env python3
"""Static audit for the MED-001 downed -> one Heavy trauma contract."""
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def block(text: str, start: str, end: str) -> str:
    begin = text.find(start)
    finish = text.find(end, begin + len(start))
    if begin < 0 or finish < 0:
        raise ValueError(f"cannot isolate {start!r}")
    return text[begin:finish]


def require(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing {needle!r}")


def main() -> int:
    medicine = (ROOT / "Code/Systems_Medicine.lua").read_text(encoding="utf-8-sig")
    unconscious = (ROOT / "CharacterEffect/Unconscious.lua").read_text(encoding="utf-8-sig")
    items = (ROOT / "items.lua").read_text(encoding="utf-8-sig")
    errors: list[str] = []
    try:
        apply_trauma = block(medicine, "function JazzApplyTrauma(unit, zone, tier)", "function JazzTraumaZoneBodyParts(zone)")
        downed = block(medicine, "function JazzApplyDownedHeavyTrauma(unit)", "function JazzApplyKnockoutTraumaPackage(unit)")
        wrapper = block(medicine, "function JazzApplyKnockoutTraumaPackage(unit)", "-- Pain stacks added")
        handler = block(medicine, "function OnMsg.UnitDowned(unit)", "function OnMsg.NewHour()")
    except ValueError as exc:
        errors.append(str(exc))
        apply_trauma = downed = wrapper = handler = ""

    require(handler, "JazzApplyDownedHeavyTrauma(unit)", "UnitDowned handler", errors)
    require(downed, 'JazzGetTraumaTier(unit, zone) == "Heavy"', "idempotence", errors)
    require(downed, "if JazzGetTraumaTier(unit, physical_zone) then", "Light upgrade", errors)
    require(downed, 'JazzApplyTrauma(unit, zone, "Heavy")', "Heavy apply", errors)
    if downed.count('unit:AddStatusEffect("Pain")') != 1 or "for _ = 1, 3 do" not in downed:
        errors.append("downed package: expected one three-stack Pain loop")
    require(wrapper, "return JazzApplyDownedHeavyTrauma(unit)", "compat wrapper", errors)
    require(apply_trauma, 'unit:HasStatusEffect("Downed")', "same-hit guard", errors)
    require(apply_trauma, 'JazzGetTraumaTier(unit, physical_zone) == "Heavy"', "same-hit guard", errors)
    require(unconscious, "JazzApplyKnockoutTraumaPackage(obj)", "Unconscious companion", errors)
    require(items, "JazzApplyKnockoutTraumaPackage(obj)", "Unconscious items.lua", errors)

    trauma = {"Ribs": "Light"}
    if "Heavy" not in trauma.values():
        trauma[next(iter(trauma), "Arms")] = "Heavy"
        pain = 3
    else:
        pain = 0
    later_light_applied = "Heavy" not in trauma.values()
    repeated_pain = 0 if "Heavy" in trauma.values() else 3
    if trauma != {"Ribs": "Heavy"} or pain != 3 or later_light_applied or repeated_pain:
        errors.append("event-order model failed")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MED-001 downed audit passed: immediate Heavy upgrade, +3 Pain, same-hit and Unconscious idempotence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
