# -*- coding: utf-8 -*-
"""Static MED-006 audit: stabilize, heal%, MaxHP debt, icon helpers."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def must(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def main() -> int:
    errors: list[str] = []
    med6 = read("Code/System_Medicine_MED006.lua")
    med = read("Code/Systems_Medicine.lua")
    inv = read("Code/System_UnitInventory.lua")
    meta = read("metadata.lua")
    mid = read("InventoryItem/Medkit.lua")
    large = read("InventoryItem/Reanimationsset.lua")
    small = read("InventoryItem/FirstAidKit.lua")

    must("System_Medicine_MED006.lua" in meta, "MED006 not in metadata.code", errors)
    must("JazzMarkKitTraumaStabilized" in med6, "stabilize helper missing", errors)
    must("JazzKitHealAtFullMedical" in med6 and "FirstAidKit = 30" in med6, "heal% table", errors)
    must("Medkit = 60" in med6 and "Reanimationsset = 100" in med6, "heal% M/L", errors)
    must("JazzTraumaMaxHpDebtByTier" in med6, "MaxHP debt table", errors)
    must("JazzResolveTraumaStatusIcon" in med6 and "JazzApplyTraumaStatusIcon" in med6, "icon helpers", errors)
    must("JazzCalcKitHealAmount" in inv or "JazzCalcKitHealAmount" in med6, "kit heal calc", errors)
    must("JazzMarkKitTraumaStabilized" in inv, "GetBandaged stabilize", errors)
    must("JazzMarkKitTraumaHealing(self" not in inv, "GetBandaged still marks healing", errors)
    must("heal_modifier + 50" not in mid and "heal_modifier + 100" not in large, "old heal_modifier in companions", errors)
    must("Starts healing" not in small and "Starts healing" not in mid and "Starts healing" not in large, "old healing hint", errors)
    must("stabiliz" in small.lower() or "Stabiliz" in small, "small kit stabilize hint", errors)

    icons = ROOT / "Icons" / "StatusEffects"
    for zone in ("Arms", "Legs", "Ribs", "Head", "Burn"):
        for tier in ("Light", "Medium", "Heavy"):
            for suf in ("Stabilized", "Healing"):
                p = icons / f"Trauma{zone}{tier}{suf}.png"
                must(p.is_file(), f"missing icon {p.name}", errors)

    must("JazzTraumaLegsMoveAp" in read("CharacterEffect/TraumaLegsHeavy.lua"), "LegsHeavy effective move", errors)
    must("JazzTraumaArmsCthPenalty" in read("CharacterEffect/TraumaArmsHeavy.lua"), "ArmsHeavy effective cth", errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK MED-006 static audit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
