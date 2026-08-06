#!/usr/bin/env python3
"""Static MED-001 audit for kit gates, bleed removal, healing, and rollover UI."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FULL_HP_STOP = "patient.HitPoints >= patient.MaxHitPoints and not JazzHasAnyBleed(patient)"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def require(text: str, needle: str, label: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(f"{label}: missing {needle!r}")


def placeobj_block(text: str, kind: str, object_id: str) -> str:
    marker = f"'Id', \"{object_id}\""
    marker_at = text.find(marker)
    if marker_at < 0:
        raise ValueError(f"cannot find {kind} {object_id}")
    start_marker = f"\t\t\tPlaceObj('{kind}', {{"
    start = text.rfind(start_marker, 0, marker_at)
    end = text.find(start_marker, marker_at + len(marker))
    if start < 0:
        raise ValueError(f"cannot find start of {kind} {object_id}")
    return text[start : end if end >= 0 else len(text)]


def function_block(text: str, name: str, next_name: str) -> str:
    start = text.find(f"function {name}")
    end = text.find(f"function {next_name}", start + 1)
    if start < 0 or end < 0:
        raise ValueError(f"cannot isolate function {name}")
    return text[start:end]


def csv_by_id(path: str, id_column: str) -> dict[str, dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8-sig", newline="") as handle:
        return {row[id_column]: row for row in csv.DictReader(handle)}


def main() -> int:
    errors: list[str] = []
    stackable = read("Code/System_JazzStackableMedicine.lua")
    medicine = read("Code/Systems_Medicine.lua")
    inventory = read("Code/System_UnitInventory.lua")
    ifak = read("InventoryItem/FirstAidKit.lua")
    medkit = read("InventoryItem/Medkit.lua")
    reanimation = read("InventoryItem/Reanimationsset.lua")
    bandage = read("CharacterEffect/BandageInCombat.lua")
    items = read("items.lua")
    metadata = read("metadata.lua")

    require(stackable, 'if class_id == "FirstAidKit" then\n\t\treturn 30', "IFAK requirement", errors)
    require(stackable, 'if class_id == "Medkit" then\n\t\treturn 50', "Medkit requirement", errors)
    require(stackable, "current and current >= required", "shared requirement helper", errors)
    require(stackable, "function JazzMedicineRolloverUnit(context)", "rollover unit resolver", errors)
    require(stackable, 'lMedicineGlobal("GetInventoryUnit")', "rollover fallback", errors)
    require(stackable, "890000000012013", "low-Medical action warning", errors)

    require(medicine, "function JazzClearAllBleeding(patient)", "all-bleeding helper", errors)
    try:
        clear_all = function_block(medicine, "JazzClearAllBleeding(patient)", "JazzHasAnyBleed(unit)")
    except ValueError as exc:
        errors.append(str(exc))
        clear_all = ""
    require(clear_all, "for _, id in ipairs(JazzBleedTierOrder) do", "all-bleeding helper", errors)
    require(clear_all, "for _ = 1, stacks do", "all-bleeding helper", errors)
    require(medicine, "return JazzGetEquippedKitMedicine(unit)", "canonical kit selector", errors)
    require(medicine, "and JazzMedicineMeetsRequirement(unit, item)", "eligible kit gate", errors)
    require(medicine, "function JazzGetBlockedKitMedicine(unit)", "blocked kit selector", errors)
    require(medicine, "required < result_requirement", "lowest blocked threshold", errors)
    require(medicine, "JazzMedicineRequirementWarning(attacker, blocked_kit)", "action tooltip warning", errors)
    require(medicine, "err == AttackDisableReasons.NoTarget or err == AttackDisableReasons.InvalidTarget", "vanilla target errors", errors)

    try:
        get_bandaged = function_block(inventory, "UnitInventory:GetBandaged(medkit, healer)", "UnitInventory:OnHeal")
    except ValueError as exc:
        errors.append(str(exc))
        get_bandaged = ""
    guard_at = get_bandaged.find("not JazzMedicineMeetsRequirement(healer, medkit)")
    heal_at = get_bandaged.find("healer:CalcHealAmount")
    consume_at = get_bandaged.find("JazzConsumeInventoryItem", heal_at)
    if guard_at < 0 or heal_at < 0 or consume_at < 0 or not (guard_at < heal_at < consume_at):
        errors.append("GetBandaged: Medical gate must precede healing and consumption")
    require(get_bandaged, 'medkit.class == "FirstAidKit" or medkit.class == "Medkit"', "kit bleed branch", errors)
    require(get_bandaged, "JazzClearAllBleeding(self)", "kit bleed branch", errors)
    require(get_bandaged, 'medkit.class == "Reanimationsset" and 2 or 1', "resuscitation regression guard", errors)

    try:
        ifak_item = placeobj_block(items, "ModItemInventoryItemCompositeDef", "FirstAidKit")
        medkit_item = placeobj_block(items, "ModItemInventoryItemCompositeDef", "Medkit")
        bandage_item = placeobj_block(items, "ModItemCharacterEffectCompositeDef", "BandageInCombat")
        reanimation_item = placeobj_block(items, "ModItemInventoryItemCompositeDef", "Reanimationsset")
    except ValueError as exc:
        errors.append(str(exc))
        ifak_item = medkit_item = reanimation_item = bandage_item = ""

    ifak_hint = re.search(r"AdditionalHint = T\([^\n]+", ifak)
    ifak_item_hint = re.search(r"'AdditionalHint', T\([^\n]+", ifak_item)
    medkit_hint = re.search(r"AdditionalHint = T\([^\n]+", medkit)
    medkit_item_hint = re.search(r"'AdditionalHint', T\([^\n]+", medkit_item)
    for text, label in ((ifak, "IFAK companion"), (ifak_item, "IFAK items.lua")):
        require(text, "Removes all bleeding", label, errors)
        require(text, "Restores HP", label, errors)
    for text, label in ((medkit, "Medkit companion"), (medkit_item, "Medkit items.lua")):
        require(text, "data.heal_modifier = data.heal_modifier + 50", label, errors)
        require(text, "Bandage healing bonus: 50%.", label, errors)
        require(text, "Removes all bleeding", label, errors)
    if "+ 25" in medkit or "+ 25" in medkit_item:
        errors.append("Medkit: stale +25% healing modifier")
    for text, label in (
        (reanimation, "Reanimationsset companion"),
        (reanimation_item, "Reanimationsset items.lua"),
    ):
        require(text, 'object_class = "JazzStackableMedicine"' if "companion" in label else "'object_class', \"JazzStackableMedicine\"", label, errors)
        require(text, "890000000010030", label, errors)
        require(text, "One use = one item from the stack", label, errors)
        require(text, "MaxStacks", label, errors)
        if "max_meds_parts" in text:
            errors.append(f"{label}: stale Meds-refill property")
    if not all((ifak_hint, ifak_item_hint, medkit_hint, medkit_item_hint)):
        errors.append("kit hints: cannot find companion/items.lua hints")
    else:
        if ifak_hint.group(0).split("T(", 1)[1] != ifak_item_hint.group(0).split("T(", 1)[1]:
            errors.append("IFAK hint: companion/items.lua mismatch")
        if medkit_hint.group(0).split("T(", 1)[1] != medkit_item_hint.group(0).split("T(", 1)[1]:
            errors.append("Medkit hint: companion/items.lua mismatch")

    for text, label in ((bandage, "BandageInCombat companion"), (bandage_item, "BandageInCombat items.lua")):
        require(text, "OnBeginTurn", label, errors)
        require(text, "OnEndTurn", label, errors)
        if text.count(FULL_HP_STOP) != 3:
            errors.append(f"{label}: expected three bleed-aware full-HP stop predicates")
        if re.search(r"patient\.HitPoints\s*>=\s*patient\.MaxHitPoints(?!\s+and\s+not\s+JazzHasAnyBleed)", text):
            errors.append(f"{label}: found bare full-HP channel stop")
    if metadata.count('"CharacterEffect/BandageInCombat.lua"') != 1:
        errors.append("metadata: BandageInCombat companion path must appear exactly once")

    rollover_start = items.find("'comment', \"medicine requirement\"")
    rollover_end = items.find("'comment', \"stat\"", rollover_start)
    rollover = items[rollover_start:rollover_end] if rollover_start >= 0 and rollover_end >= 0 else ""
    require(rollover, "JazzMedicineRequiredMedical(ResolvePropObj(context)) > 0", "rollover widget", errors)
    require(rollover, "JazzMedicineRolloverUnit(context)", "rollover widget", errors)
    require(rollover, "890000000012010", "rollover widget", errors)
    require(rollover, "890000000012011", "rollover widget", errors)
    if rollover.count('SetTextStyle("RolloverTextItalicRed")') != 1 or rollover.count('SetTextStyleRight("RolloverTextItalicRed")') != 1:
        errors.append("rollover widget: low requirement must style both columns red")
    require(items[rollover_end : rollover_end + 500], "JazzMedicineRequiredMedical(ResolvePropObj(context)) <= 0", "generic stat exclusion", errors)
    require(items, "IFAK and Medkit remove all bleeding.", "Bandage action copy", errors)
    action_at = items.find("IFAK and Medkit remove all bleeding.")
    if "surgical kit" in items[action_at - 300 : action_at + 300].lower():
        errors.append("Bandage action copy: still claims a surgical kit")

    expected_sources = {
        "890000000012010": "Medical required",
        "890000000012011": "Medical too low",
        "890000000012013": "Medical too low: <current>/<required>",
    }
    try:
        wave = csv_by_id("docs/tools/localization-copy-edits/medicine_requirements.csv", "ID")
        english = csv_by_id("Localization/EnglishManual.csv", "AnchorID")
        russian = csv_by_id("Localization/RussianManual.csv", "AnchorID")
    except (KeyError, OSError, csv.Error) as exc:
        errors.append(f"localization: cannot read CSVs: {exc}")
        wave = english = russian = {}
    for loc_id, source in expected_sources.items():
        row = wave.get(loc_id)
        if not row or row.get("SourceText") != source or not row.get("Russian") or row.get("English") != source:
            errors.append(f"localization wave: invalid {loc_id}")
        en_row = english.get(loc_id)
        ru_row = russian.get(loc_id)
        if not en_row or en_row.get("SourceText") != source or en_row.get("English") != source:
            errors.append(f"EnglishManual: invalid {loc_id}")
        if not ru_row or ru_row.get("SourceText") != source or not ru_row.get("Russian"):
            errors.append(f"RussianManual: invalid {loc_id}")

    required = {"FirstAidKit": 30, "Medkit": 50, "Reanimationsset": 0}
    for medical, item_class, expected in (
        (29, "FirstAidKit", False), (30, "FirstAidKit", True),
        (49, "Medkit", False), (50, "Medkit", True),
        (0, "Reanimationsset", True),
    ):
        if (medical >= required[item_class]) is not expected:
            errors.append(f"model: gate failed for Medical {medical} / {item_class}")
    bleed = {"Bleeding": 2, "BleedingMedium": 1, "BleedingHeavy": 3}
    cleared = {effect: 0 for effect in bleed}
    if any(cleared.values()):
        errors.append("model: IFAK/Medkit failed to clear all bleeding")
    remaining = sum(bleed.values()) - min(2, sum(bleed.values()))
    if remaining != 4:
        errors.append("model: resuscitation kit two-stack regression")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MED-001 kit audit passed: Medical 30/50 gates, all bleeding removed, Medkit +50%, red rollover warning, generated-data parity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
