#!/usr/bin/env python3
"""Static MED-005 audit: field bandage/morphine AP ladder by Medical."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def require(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing {needle!r}")


def bandage_ap(med: int) -> int:
    if med >= 80:
        return 1
    if med >= 60:
        return 2
    if med >= 40:
        return 3
    if med >= 20:
        return 4
    return 5


def morphine_ap(med: int) -> int:
    if med >= 80:
        return 1
    if med >= 40:
        return 2
    return 3


def csv_text(path: str, loc_id: str, col: int) -> str:
    with (ROOT / path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if row and row[0] == loc_id:
                return row[col] if col < len(row) else ""
    return ""


def main() -> int:
    errors: list[str] = []
    medicine = read("Code/Systems_Medicine.lua")
    combat_ai = read("Code/CombatAI.lua")
    items = read("items.lua")
    bandage_item = read("InventoryItem/JAZZ_Bandage.lua")
    morphine_item = read("InventoryItem/JAZZ_Morphine.lua")

    table = {
        0: (5, 3),
        19: (5, 3),
        20: (4, 3),
        39: (4, 3),
        40: (3, 2),
        59: (3, 2),
        60: (2, 2),
        79: (2, 2),
        80: (1, 1),
        100: (1, 1),
    }
    for med, (b, m) in table.items():
        got_b, got_m = bandage_ap(med), morphine_ap(med)
        if got_b != b or got_m != m:
            errors.append(f"table Medical {med}: expected bandage {b} morphine {m}, got {got_b}/{got_m}")

    require(medicine, "function JazzFieldMedicineBandageAP(unit)", "bandage AP helper", errors)
    require(medicine, "function JazzFieldMedicineMorphineAP(unit)", "morphine AP helper", errors)
    require(medicine, "function JazzFieldMedicineAPCost(unit, kind)", "scaled AP helper", errors)
    require(medicine, "if med >= 80 then\n\t\treturn 1", "bandage 80→1", errors)
    require(medicine, "if med >= 60 then\n\t\treturn 2", "bandage 60→2", errors)
    require(medicine, "if med >= 40 then\n\t\treturn 3", "bandage 40→3", errors)
    require(medicine, "if med >= 20 then\n\t\treturn 4", "bandage 20→4", errors)
    require(medicine, "kind == \"morphine\"", "morphine kind", errors)

    require(items, 'cost_fn(unit, "bandage")', "JazzBandage GetAPCost helper", errors)
    require(items, 'cost_fn(unit, "morphine")', "JazzMorphine GetAPCost helper", errors)
    if re.search(
        r"JazzGetBandageItem\(unit\) then return -1 end\s+return self\.ActionPoints",
        items,
    ):
        errors.append("JazzBandage GetAPCost still returns self.ActionPoints")
    if re.search(
        r"JazzGetMorphineItem\(unit\) then return -1 end\s+return self\.ActionPoints",
        items,
    ):
        errors.append("JazzMorphine GetAPCost still returns self.ActionPoints")

    require(items, "local cost = self:GetAPCost(unit, args)", "GetUIState uses GetAPCost", errors)
    if "JazzGetFieldBandageTargets(unit, \"any\", \"reachable\")" in items:
        bandage_ui = items.split("JazzGetFieldBandageTargets(unit, \"any\", \"reachable\")", 1)[0][-400:]
        if "HasAP(self.ActionPoints)" in bandage_ui:
            errors.append("JazzBandage GetUIState still HasAP(self.ActionPoints)")
    if "JazzGetMorphineTargets(unit, \"any\", \"reachable\")" in items:
        morphine_ui = items.split("JazzGetMorphineTargets(unit, \"any\", \"reachable\")", 1)[0][-400:]
        if "HasAP(self.ActionPoints)" in morphine_ui:
            errors.append("JazzMorphine GetUIState still HasAP(self.ActionPoints)")

    require(combat_ai, "field_action:GetAPCost(context.unit)", "AI field AP from GetAPCost", errors)
    if "CombatActions.JazzBandage.ActionPoints" in combat_ai:
        errors.append("CombatAI still reads JazzBandage.ActionPoints")

    require(items, "AP cost by Medical: 5 (0–19)", "items bandage hint ladder", errors)
    require(items, "AP cost by Medical: 3 (0–39)", "items morphine hint ladder", errors)
    require(bandage_item, "AP cost by Medical: 5 (0–19)", "companion bandage hint", errors)
    require(morphine_item, "AP cost by Medical: 3 (0–39)", "companion morphine hint", errors)
    require(items, "AP 5/4/3/2/1 at Medical 0/20/40/60/80", "JazzBandage description", errors)
    require(items, "AP 3/2/1 at Medical 0/40/80", "JazzMorphine description", errors)

    for loc_id, needle in (
        ("890000000010013", "AP cost by Medical: 5 (0–19)"),
        ("890000000010016", "AP cost by Medical: 3 (0–39)"),
        ("890000000010201", "AP 5/4/3/2/1 at Medical 0/20/40/60/80"),
        ("890000000010028", "AP 3/2/1 at Medical 0/40/80"),
    ):
        en = csv_text("English.csv", loc_id, 1)
        ru_src = csv_text("Russian.csv", loc_id, 1)
        ru_tr = csv_text("Russian.csv", loc_id, 2)
        if needle not in en:
            errors.append(f"English.csv {loc_id} missing {needle!r}")
        if needle not in ru_src:
            errors.append(f"Russian.csv source {loc_id} missing {needle!r}")
        if "ОД" not in ru_tr and "од" not in ru_tr:
            errors.append(f"Russian.csv translation {loc_id} missing ОД ladder")

    if errors:
        print("FAIL")
        for err in errors:
            print(" -", err)
        return 1
    print("OK MED-005 field AP ladder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
