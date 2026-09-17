#!/usr/bin/env python3
"""Static checks: stationary MG cone uses gun MaxRange, not map slider / MinRange / sight."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    emp = (ROOT / "Code" / "System_EmplacementAmmo.lua").read_text(encoding="utf-8")
    ow = (ROOT / "Code" / "System_OR_Weapons.lua").read_text(encoding="utf-8")
    imode = (ROOT / "Code" / "IModeCombatAreaAim.lua").read_text(encoding="utf-8")
    ai = (ROOT / "Code" / "CombatAI.lua").read_text(encoding="utf-8")

    check("function Jazz_EmplacementConeDist" in emp, "cone helper is a top-level function")
    check("g_JAZZ_EndEmplacementInteractionWrapped" in emp, "EndInteraction wrap flag is declared")
    check("function MachineGunEmplacement:EndInteraction" in emp, "EndInteraction wrap is installed")
    check("Jazz_EmplacementConeDist(self)" in emp, "Update sets dist through the helper")
    check("Jazz_EmplacementConeDist(obj)" in emp, "reseat uses the helper")
    check("GetMaxAimRange(" not in emp, "emplacement cone path no longer calls sight-clamped GetMaxAimRange")
    check("return max_tiles * slab" in emp, "helper returns gun MaxRange, not map target_dist")
    check("if not dist or dist < min_r then" not in emp, "helper no longer preserves authored map dist")
    check("local function JazzOwIsEmplacementWeapon" in ow, "GetMaxAimRange wrap is emplacement-gated")
    check("g_JAZZ_OwGetMaxAimRangeBase" in ow, "handheld GetMaxAimRange base is saved")
    check("function Jazz_EmplacementConeAngle" in emp, "45° helper is a top-level function")
    check("return 45 * 60" in emp, "emplacement cone is 45 degrees")
    check("Jazz_EmplacementConeAngle" in ow, "placed cone and GetAreaAttackParams use the 45° helper")
    check("Jazz_EmplacementConeAngle" in imode, "aim preview pins emplacement cone to 45°")
    check("scale_ow and not weapon.emplacement_weapon" in ai, "AI zone skip COMBAT-009 scale on emplacement")

    print("RESULT: PASSED (emplacement cone range static audit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
