#!/usr/bin/env python3
"""Static regression checks for JAZZ-HOTFIX-003 (no game runtime required)."""
from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TIP_ID = "890000000001235"
RU_TIP = "Количество ОД — не более 4.\nНе может контратаковать или поддерживать подготовленные атаки."
EN_TIP = "AP is capped at 4.\nCannot counterattack or maintain prepared attacks."


def normalize_newlines(value: str | None) -> str:
    return (value or "").replace("\r\n", "\n")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def placeobj_block(text: str, class_name: str, marker: str) -> str:
    marker_pos = text.find(marker)
    if marker_pos < 0:
        raise AssertionError(f"missing marker: {marker}")
    start = text.rfind(f"PlaceObj('{class_name}'", 0, marker_pos)
    if start < 0:
        raise AssertionError(f"missing {class_name} block for: {marker}")
    brace = text.find("{", start)
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[start : pos + 1]
    raise AssertionError(f"unbalanced {class_name} block for: {marker}")


def runtime_row(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.reader(handle) if row and row[0] == TIP_ID]
    check(len(rows) == 1, f"{path.name} has one {TIP_ID} row")
    return rows[0]


def main() -> int:
    items = (ROOT / "items.lua").read_text(encoding="utf-8")
    companion = (ROOT / "CharacterEffect" / "suppressionPinned.lua").read_text(encoding="utf-8")
    executor = (ROOT / "Code" / "ExecFirearmAttacks.lua").read_text(encoding="utf-8")

    unjam = placeobj_block(items, "ModItemCombatAction", 'id = "Unjam"')
    check('ShowIn = "SignatureAbilities"' not in unjam, "Unjam is not forced into SignatureAbilities")
    check('ShowIn = "CombatActions"' in unjam, "Unjam is explicitly on CombatActions action bar")
    check('group = "Default"' in unjam and "SortKey = 10" in unjam, "Unjam keeps Default/SortKey action-bar contract")
    check("can_unjam" in unjam and "GetWeaponResourceMax" in unjam, "Unjam jam gate uses WeaponResource, not Condition Broken alone")
    check("weapon.jammed" in unjam and 'IsKindOf(weapon, "Firearm")' in unjam, "Unjam stays gated by a jammed active firearm")
    check("MulDivRound(Clamp(mech, 0, 100), 3, 100)" in unjam, "Unjam AP scales with Mechanical 4..1")
    check("ActionPoints = 4000" in unjam, "Unjam ActionPoints default is 4 AP ceiling")
    check("unit:UIHasAP(cost)" in unjam, "Unjam keeps AP gate")

    unit_or = (ROOT / "Code" / "System_OR_Unit.lua").read_text(encoding="utf-8")
    weapons_or = (ROOT / "Code" / "System_OR_Weapons.lua").read_text(encoding="utf-8")
    check("function FirearmBase:IsCondition" in weapons_or and "GetConditionPercent()" in weapons_or, "FirearmBase:IsCondition follows WeaponResource percent")
    check('should_interrupt = self:HasStatusEffect("suppressionPinned")' in unit_or, "BeginTurn interrupts permanent OW when pinned")
    check('data.effect == "suppressionPinned"' in unit_or and "self:InterruptPreparedAttack()" in unit_or, "ApplySuppressionStatus re-interrupts while already pinned")

    pinned_generated = placeobj_block(items, "ModItemCharacterEffectCompositeDef", "suppressionPinned Description")
    for label, layer in (("companion", companion), ("generated", pinned_generated)):
        check(layer.count("obj:InterruptPreparedAttack()") == 1, f"suppressionPinned {label} OnAdded interrupts prepared attacks once")
        check(layer.index("obj:InterruptPreparedAttack()") < layer.index("local unitStance"), f"suppressionPinned {label} interrupts before stance change")
        check("StationedMachineGun" in layer and "g_Overwatch" in layer, f"suppressionPinned {label} strips residual MG OW")
        check('Event = "OnBeginTurn"' in layer and "InterruptPreparedAttack()" in layer, f"suppressionPinned {label} OnBeginTurn clears prepared attacks")
        check(RU_TIP.replace("\n", "\\n") in layer, f"suppressionPinned {label} tooltip describes prepared-attack cleanup")

    check("attackArg.single_fx = true" in executor, "shotgun pellet pack enables single FX")
    check('attackArg.fx_action = "WeaponBuckshot"' in executor, "shotgun pellet pack has a default buckshot FX")
    fire_pos = executor.find("attack.weapon:FireBullet")
    clear_pos = executor.find('attackArg.fx_action = ""', fire_pos)
    check(fire_pos >= 0 and clear_pos > fire_pos, "shotgun FX is cleared after the first FireBullet")
    buckshot_burst = placeobj_block(items, "ModItemCombatAction", 'id = "BuckshotBurst"')
    check("table.copy(args or {})" in buckshot_burst and 'args.fx_action = "WeaponBuckshot"' in buckshot_burst and "args.single_fx = true" in buckshot_burst, "BuckshotBurst forwards the pellet-pack FX contract")

    with (ROOT / "Localization" / "Strings.csv").open("r", encoding="utf-8-sig", newline="") as handle:
        all_catalog_rows = list(csv.DictReader(handle))
    catalog_rows = [row for row in all_catalog_rows if row.get("ID") == TIP_ID]
    check(len(catalog_rows) == 1, f"catalog has one {TIP_ID} row")
    catalog = catalog_rows[0]
    check(normalize_newlines(catalog.get("SourceText")) == RU_TIP and normalize_newlines(catalog.get("Russian")) == RU_TIP and normalize_newlines(catalog.get("English")) == EN_TIP, "catalog RU/EN tooltip is complete")
    check("collision" not in (catalog.get("Status") or ""), "tooltip ID has no catalog collision")
    english = runtime_row(ROOT / "English.csv")
    russian = runtime_row(ROOT / "Russian.csv")
    check(len(english) >= 3 and normalize_newlines(english[1]) == RU_TIP and normalize_newlines(english[2]) == EN_TIP, "English runtime tooltip matches catalog")
    check(len(russian) >= 3 and normalize_newlines(russian[1]) == RU_TIP and normalize_newlines(russian[2]) == RU_TIP, "Russian runtime tooltip matches catalog")

    mod_ids = {row["ID"] for row in all_catalog_rows if "new-id" in (row.get("Status") or "")}
    runtime_sets = []
    for name in ("English.csv", "Russian.csv"):
        raw = (ROOT / name).read_text(encoding="utf-8-sig")
        runtime_sets.append(set(re.findall(r"(?m)^(\d+),", raw)) & mod_ids)
    check(runtime_sets[0] == runtime_sets[1] == mod_ids, f"RU/EN runtime mod-only ID sets match catalog ({len(mod_ids)})")

    print("RESULT: PASSED (JAZZ-HOTFIX-003 static audit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
