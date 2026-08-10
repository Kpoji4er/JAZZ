#!/usr/bin/env python3
"""Static MED-001 AC-017: Large Medkit marks heaviest unhealed trauma healing."""
from __future__ import annotations

import re
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
    med = read("Code/Systems_Medicine.lua")
    inv = read("Code/System_UnitInventory.lua")
    hint = read("InventoryItem/Reanimationsset.lua")

    must("function JazzFindHeaviestUnhealedTrauma" in med, "missing JazzFindHeaviestUnhealedTrauma", errors)
    must("function JazzMarkHeaviestTraumaHealing" in med, "missing JazzMarkHeaviestTraumaHealing", errors)
    must("JazzTraumaIsHealing(effect)" in med, "unhealed filter must skip jazz_healing", errors)
    must("JazzSetTraumaHealing(effect, true)" in med, "must set jazz_healing", errors)
    must("function JazzUnitNeedsKitBandage" in med, "missing JazzUnitNeedsKitBandage", errors)
    must('kit.class == "Reanimationsset"' in med, "kit targeting must gate on Reanimationsset", errors)
    must("JazzUnitNeedsKitBandage(target, unit)" in med, "GetBandageTargets must use kit need helper", errors)
    must("JazzUnitNeedsKitBandage(target, attacker)" in med, "CanBandageUI FullHP must use kit need helper", errors)
    must("JazzKitBandageLoopContinue" in med, "exploration bandage loop must allow trauma-only large kit", errors)

    must('medkit.class == "Reanimationsset"' in inv, "GetBandaged must special-case Reanimationsset", errors)
    must("JazzMarkHeaviestTraumaHealing" in inv, "GetBandaged must call JazzMarkHeaviestTraumaHealing", errors)
    must("trauma_marked" in inv, "consume path must include trauma_marked", errors)
    must("890000000010033" in inv, "combat log id for trauma healing missing", errors)

    must("Starts healing on the heaviest untreated trauma" in hint, "Large Medkit hint missing trauma line", errors)
    must("890000000010030" in hint, "Large Medkit AdditionalHint id drift", errors)

    items = read("items.lua")
    must("Starts healing on the heaviest untreated trauma" in items, "items.lua Large hint not synced", errors)
    must("Large medkit starts healing on the heaviest untreated trauma" in items, "Bandage Description not synced", errors)

    ru = read("Russian.csv")
    en = read("English.csv")
    must("890000000010033" in ru and "заживление" in ru, "Russian.csv missing 010033", errors)
    must("890000000010033" in en, "English.csv missing 010033", errors)
    must("Starts healing on the heaviest untreated trauma" in ru, "Russian.csv hint SourceText not updated", errors)
    must("Запускает заживление самой тяжёлой" in ru, "Russian.csv hint Translation missing", errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("OK MED-001 large kit trauma healing (AC-017)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
