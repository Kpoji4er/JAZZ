# -*- coding: utf-8 -*-
"""Static MED-003 kit package audit."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units" / "items.lua"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def must(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def main() -> int:
    errors: list[str] = []
    stack = read("Code/System_JazzStackableMedicine.lua")
    med = read("Code/Systems_Medicine.lua")
    inv = read("Code/System_UnitInventory.lua")
    bobby = read("Code/System_BobbyRay_ECON004.lua")
    small = read("InventoryItem/FirstAidKit.lua")
    mid = read("InventoryItem/Medkit.lua")
    large = read("InventoryItem/Reanimationsset.lua")
    items = read("items.lua")

    must("return 80" in stack and "Reanimationsset" in stack, "Large Medical gate 80 missing", errors)
    # MED-006 supersedes kit heal_modifier +0/+50/+100 → % MaxHP table
    med6 = read("Code/System_Medicine_MED006.lua")
    must("JazzKitHealAtFullMedical" in med6 and "Reanimationsset = 100" in med6, "MED-006 Large 100% heal table", errors)
    must("MaxStacks = 5" in small and "MaxStacks = 10" in mid and "MaxStacks = 15" in large, "MaxStacks 5/10/15", errors)
    must("Cost = 1800" in large and "Tier = 3" in large and "CanAppearInShop = true" in large, "Large Bobby fields", errors)
    must("RestockWeight = 15" in large, "Large RestockWeight", errors)
    must("JazzKitTraumaMaxRank" in med and "FirstAidKit = 1" in med and "Medkit = 2" in med, "trauma rank table", errors)
    # MED-006: kit path stabilizes; aliases still expose Unhealed/Healing names
    must(
        ("JazzMarkKitTraumaStabilized" in med6 or "JazzMarkKitTraumaHealing" in med)
        and ("JazzFindKitEligibleUnstabilizedTrauma" in med6 or "JazzFindKitEligibleUnhealedTrauma" in med),
        "trauma stabilize/heal helpers",
        errors,
    )
    must("JazzClearAllBleeding(self)" in inv, "full bleed clear in GetBandaged", errors)
    must("JazzClearBleedStrong" not in inv or inv.count("JazzClearBleedStrong") == 0 or "is_kit" in inv, "check bleed path", errors)
    # kits should not use ClearBleedStrong for Reanimationsset
    must("JazzClearBleedStrong(self, 2)" not in inv, "Large partial bleed clear still present", errors)
    must("AddStatusEffect(\"Analgesia\")" in inv, "Analgesia on kit Bandage", errors)
    must("JazzClearWoundInfected" in inv, "infection clear on kit Bandage", errors)
    must("soft-tail specialty" in bobby or "Reanimationsset" in bobby, "Bobby note for Large", errors)
    must("FirstAidKit = true" in bobby and "Medkit = true" in bobby, "S/M staples", errors)
    must("Reanimationsset = true" not in bobby.split("JAZZ_BOBBY_FLAT")[1].split("}")[0], "Large must not be flat staple", errors)

    units = UNITS.read_text(encoding="utf-8")
    i = units.find('id = "Bonemaker_Inventory"')
    must(i >= 0, "Bonemaker_Inventory missing", errors)
    window = units[i : i + 5000]
    must('item = "FirstAidKit"' in window and "stack_max = 5" in window, "Bonemaker FirstAidKit guaranteed", errors)
    must("generate_chance = 5" in window and 'item = "Medkit"' in window, "Bonemaker Medkit 5%", errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK MED-003 kit package")
    return 0


if __name__ == "__main__":
    sys.exit(main())
