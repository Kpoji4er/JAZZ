#!/usr/bin/env python3
"""JAZZ-INV-003: CraftAmmo picker allow-list is homemade JAZZ only."""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALLOWED_EXTRA = {"JAZZ_AMMO_12gauge_Saltshot"}

# Owner 2026-08-23: 100 Parts + powder; yield by caliber.
EXPECTED = {
    "JAZZ_9x18_Crafted": {"item": "JAZZ_AMMO_9x18_Crafted", "parts": 100, "powder": 1, "time": 10, "qty": 50},
    "JAZZ_9x19_Crafted": {"item": "JAZZ_AMMO_9x19_Crafted", "parts": 100, "powder": 1, "time": 10, "qty": 40},
    "JAZZ_45ACP_Crafted": {"item": "JAZZ_AMMO_45ACP_Crafted", "parts": 100, "powder": 1, "time": 10, "qty": 30},
    "JAZZ_545_Crafted": {"item": "JAZZ_AMMO_545_Crafted", "parts": 100, "powder": 2, "time": 15, "qty": 30},
    "JAZZ_556_Crafted": {"item": "JAZZ_AMMO_556_Crafted", "parts": 100, "powder": 2, "time": 15, "qty": 30},
    "JAZZ_762x39_Crafted": {"item": "JAZZ_AMMO_762x39_Crafted", "parts": 100, "powder": 2, "time": 15, "qty": 30},
    "JAZZ_762x51_Crafted": {"item": "JAZZ_AMMO_762x51_Crafted", "parts": 100, "powder": 2, "time": 15, "qty": 20},
    "JAZZ_762x54_Crafted": {"item": "JAZZ_AMMO_762x54_Crafted", "parts": 100, "powder": 3, "time": 15, "qty": 20},
    "JAZZ_9x39_Crafted": {"item": "JAZZ_AMMO_9x39_Crafted", "parts": 100, "powder": 2, "time": 15, "qty": 20},
    "JAZZ_12gauge_Saltshot": {"item": "JAZZ_AMMO_12gauge_Saltshot", "parts": 100, "powder": 1, "time": 7, "qty": 20},
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def homemade_result(item: str) -> bool:
    return bool(re.match(r"^JAZZ_AMMO_.+_Crafted$", item)) or item in ALLOWED_EXTRA


def ingredient_amount(block: str, item: str) -> int:
    m = re.search(
        rf"'item', \"{re.escape(item)}\"(?:,\s*'amount', (\d+))?",
        block,
    )
    if not m:
        return 0
    return int(m.group(1)) if m.group(1) else 1


def parse_recipe(block: str) -> dict | None:
    rid = re.search(r"id = \"(JAZZ_[^\"]+)\"", block)
    result = re.search(
        r"ResultItem = PlaceObj\('RecipeIngredient',\s*\{\s*'item', \"([^\"]+)\"(?:,\s*'amount', (\d+))?",
        block,
    )
    time = re.search(r"CraftTime = (\d+)", block)
    if not (rid and result and time):
        return None
    return {
        "id": rid.group(1),
        "item": result.group(1),
        "qty": int(result.group(2)) if result.group(2) else 1,
        "time": int(time.group(1)),
        "parts": ingredient_amount(block, "Parts"),
        "powder": ingredient_amount(block, "BlackPowder"),
    }


def jazz_ammo_recipes(items_text: str) -> list[dict]:
    folder = items_text.find("'name', \"JAZZ_Ammo\"")
    check(folder >= 0, "JAZZ_Ammo craft folder exists")
    chunk = items_text[folder : items_text.find("'name', \"EditorExtension\"", folder)]
    recipes = []
    for block in re.split(r"PlaceObj\('ModItemCraftOperationsRecipeDef'", chunk)[1:]:
        parsed = parse_recipe(block)
        if parsed:
            recipes.append(parsed)
    return recipes


def main() -> int:
    unit = (ROOT / "Code" / "VanillaDesyncFixes.lua").read_text(encoding="utf-8")
    items = (ROOT / "items.lua").read_text(encoding="utf-8")
    meta = (ROOT / "metadata.lua").read_text(encoding="utf-8")

    check("function Jazz_IsAllowedCraftAmmoRecipe" in unit, "allow-list helper exists")
    check('string.match(item, "^JAZZ_AMMO_.+_Crafted$")' in unit, "Crafted result pattern is checked")
    check('item == "JAZZ_AMMO_12gauge_Saltshot"' in unit, "saltshot is allowed")
    check("not Jazz_IsAllowedCraftAmmoRecipe(recipe)" in unit, "FillItemsToCraft skips non-homemade")
    check("g_JAZZ_CraftAddResWrapped" in unit, "AdditionalResources wrap flags exist")
    check("Jazz_InstallCraftAddResFilter" in unit, "AdditionalResources install exists")

    recipes = jazz_ammo_recipes(items)
    check(len(recipes) == len(EXPECTED), f"JAZZ_Ammo recipe count {len(recipes)} == {len(EXPECTED)}")
    bad = [f"{r['id']}->{r['item']}" for r in recipes if not homemade_result(r["item"])]
    check(not bad, f"JAZZ_Ammo results are allow-list: {bad or 'ok'}")
    check(any(r["id"] == "JAZZ_9x39_Crafted" for r in recipes), "JAZZ_9x39_Crafted recipe exists")
    check("'Id', \"JAZZ_9x39_Crafted\"" in meta, "metadata resource lists JAZZ_9x39_Crafted")

    by_id = {r["id"]: r for r in recipes}
    missing = sorted(set(EXPECTED) - set(by_id))
    extra = sorted(set(by_id) - set(EXPECTED))
    check(not missing and not extra, f"recipe ids match expected (missing={missing}, extra={extra})")
    for rid, exp in EXPECTED.items():
        got = by_id[rid]
        check(got["item"] == exp["item"], f"{rid} result {got['item']}")
        check(got["parts"] == exp["parts"], f"{rid} Parts {got['parts']} == {exp['parts']}")
        check(got["powder"] == exp["powder"], f"{rid} powder {got['powder']} == {exp['powder']}")
        check(got["time"] == exp["time"], f"{rid} time {got['time']} == {exp['time']}")
        check(got["qty"] == exp["qty"], f"{rid} qty {got['qty']} == {exp['qty']}")

    print("RESULT: PASSED (JAZZ-INV-003 homemade CraftAmmo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
