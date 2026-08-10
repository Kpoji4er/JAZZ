# -*- coding: utf-8 -*-
"""Audit Legion class-inventory medicine vs MED-003 redistribute policy."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_legion_med_loot_redistribute import (  # noqa: E402
    MEDIC_BANDAGE,
    MEDIC_MORPHINE,
    RECIPES,
    STRIP_EXTRA,
    T2_BANDAGE,
    T3_MORPHINE_CHANCE,
    UNITS_ITEMS,
    extract_loot_blocks,
    iter_loot_entry_spans,
    plan_for,
)


def entry_map(block: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for _, _, inner in iter_loot_entry_spans(block):
        im = re.search(r'item\s*=\s*"([^"]+)"', inner)
        if not im:
            continue
        found.setdefault(im.group(1), []).append(inner)
    return found


def main() -> int:
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    text = UNITS_ITEMS.read_text(encoding="utf-8")
    loots = extract_loot_blocks(text)
    fails: list[str] = []

    for uid, recipe in recipes.items():
        inv = recipe.get("inventory")
        if not inv or inv not in loots:
            fails.append(f"{uid}: missing inventory {inv}")
            continue
        _, _, block = loots[inv]
        got = entry_map(block)
        tier = int(recipe.get("class_tier") or 0)
        is_medic = bool((recipe.get("utility") or {}).get("medkit"))
        bandage, morphine, chance = plan_for(tier, is_medic)

        band = got.get("JAZZ_Bandage", [])
        morph = got.get("JAZZ_Morphine", [])
        if bandage is None:
            if band:
                fails.append(f"{inv}: unexpected bandage")
        else:
            if len(band) != 1:
                fails.append(f"{inv}: bandage entries {len(band)}")
            else:
                a, b = bandage
                if f"stack_min = {a}" not in band[0] or f"stack_max = {b}" not in band[0]:
                    fails.append(f"{inv}: bandage stacks != {a}-{b}")
        if morphine is None:
            if morph:
                fails.append(f"{inv}: unexpected morphine")
        else:
            if len(morph) != 1:
                fails.append(f"{inv}: morphine entries {len(morph)}")
            else:
                a, b = morphine
                if f"stack_min = {a}" not in morph[0] or f"stack_max = {b}" not in morph[0]:
                    fails.append(f"{inv}: morphine stacks != {a}-{b}")
                if chance is not None:
                    if f"generate_chance = {chance}" not in morph[0]:
                        fails.append(f"{inv}: morphine chance != {chance}")
                elif "generate_chance" in morph[0]:
                    fails.append(f"{inv}: medic morphine should be guaranteed range")

        if is_medic:
            fak = got.get("FirstAidKit", [])
            mk = got.get("Medkit", [])
            if not fak or "stack_min = 5" not in fak[0]:
                fails.append(f"{inv}: medic FirstAidKit×5 missing")
            if not mk or "generate_chance = 5" not in mk[0]:
                fails.append(f"{inv}: medic Medkit 5% missing")

    for extra in STRIP_EXTRA:
        if extra not in loots:
            continue
        _, _, block = loots[extra]
        got = entry_map(block)
        if got.get("JAZZ_Bandage") or got.get("JAZZ_Morphine"):
            fails.append(f"{extra}: leftover field medicine")

    if fails:
        print(f"FAIL n={len(fails)}")
        for f in fails[:40]:
            print(" -", f)
        return 1
    print(
        f"OK legion med loot (T2 bandage {T2_BANDAGE[0]}-{T2_BANDAGE[1]}, "
        f"T3 morphine {T3_MORPHINE_CHANCE}%, medic bandage {MEDIC_BANDAGE[0]}-{MEDIC_BANDAGE[1]} "
        f"morphine {MEDIC_MORPHINE[0]}-{MEDIC_MORPHINE[1]})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
