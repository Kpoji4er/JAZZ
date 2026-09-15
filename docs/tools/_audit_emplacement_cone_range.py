#!/usr/bin/env python3
"""Static checks: stationary MG cone uses map/max range, not COMBAT-009 MinRange / sight."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    emp = (ROOT / "Code" / "System_EmplacementAmmo.lua").read_text(encoding="utf-8")

    check("function Jazz_EmplacementConeDist" in emp, "cone helper is a top-level function")
    check("g_JAZZ_EndEmplacementInteractionWrapped" in emp, "EndInteraction wrap flag is declared")
    check("function MachineGunEmplacement:EndInteraction" in emp, "EndInteraction wrap is installed")
    check("local prev_dist = self.target_dist" in emp, "Update saves authored target_dist before vanilla reset")
    check("self.target_dist = prev_dist" in emp, "Update restores authored target_dist after vanilla Update")
    check("Jazz_EmplacementConeDist(self)" in emp, "Update clamps restored dist through the helper")
    check("Jazz_EmplacementConeDist(obj)" in emp, "reseat uses the helper instead of sight-clamped Overwatch range")
    check("GetMaxAimRange(" not in emp, "emplacement cone path no longer calls sight-clamped GetMaxAimRange")
    check('if not dist or dist < min_r then' in emp and "dist = max_r" in emp, "short/default dist promotes to MaxRange, not MinRange")

    print("RESULT: PASSED (emplacement cone range static audit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
