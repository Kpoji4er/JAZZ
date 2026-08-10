# -*- coding: utf-8 -*-
"""Legion class-inventory medicine (MED-003): T2 bandages, T3 morphine chance, medic stacks.

Reads scripts/legion-loadouts/data/recipes.json class_tier + utility.medkit.
Patches jazz-units/items.lua ModItemLootDef for each recipe inventory id.

Policy (owner 2026-08-10):
- class_tier 2: JAZZ_Bandage stack 1–2 (guaranteed entry)
- class_tier 3: JAZZ_Morphine ×1 with generate_chance 30
- utility.medkit (Bonemaker): Bandage 1–10, Morphine 0–3; keep FirstAidKit×5 + Medkit 5%
- T1/T4 non-medic: no bandage/morphine
- Strip accidental Bandage/Morphine from Mortarman_Launcher

Idempotent. Does not touch Mercs hire loot.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECIPES = ROOT / "scripts" / "legion-loadouts" / "data" / "recipes.json"
UNITS_ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")

T2_BANDAGE = (1, 2)
T3_MORPHINE_CHANCE = 30
MEDIC_BANDAGE = (1, 10)
MEDIC_MORPHINE = (0, 3)
MED_FIELD = ("JAZZ_Bandage", "JAZZ_Morphine")
STRIP_EXTRA = ("Mortarman_Launcher",)


def extract_loot_blocks(text: str) -> dict[str, tuple[int, int, str]]:
    results: dict[str, tuple[int, int, str]] = {}
    for m in re.finditer(r"PlaceObj\('ModItemLootDef',\s*\{", text):
        start = m.start()
        i = text.find("{", start)
        depth = 0
        end = None
        for j in range(i, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(text) and text[end] == ")":
                        end += 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    break
        if end is None:
            continue
        block = text[start:end]
        idm = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
        if idm:
            results[idm.group(1)] = (start, end, block)
    return results


def iter_loot_entry_spans(block: str) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    for m in re.finditer(r"PlaceObj\('LootEntryInventoryItem',\s*\{", block):
        start = m.start()
        i = block.find("{", m.start())
        depth = 0
        for j in range(i, len(block)):
            if block[j] == "{":
                depth += 1
            elif block[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(block) and block[end] == ")":
                        end += 1
                    if end < len(block) and block[end] == ",":
                        end += 1
                    line_start = start
                    while line_start > 0 and block[line_start - 1] in " \t":
                        line_start -= 1
                    if line_start > 0 and block[line_start - 1] == "\n":
                        line_start -= 1
                    spans.append((line_start, end, block[i + 1 : j]))
                    break
    return spans


def strip_field_med(block: str) -> tuple[str, str]:
    indent = "\t\t\t\t\t\t"
    for line in block.splitlines():
        m = re.match(r"^(\t+)PlaceObj\('LootEntry", line)
        if m:
            indent = m.group(1)
            break
    remove: list[tuple[int, int]] = []
    for start, end, inner in iter_loot_entry_spans(block):
        im = re.search(r'item\s*=\s*"([^"]+)"', inner)
        if im and im.group(1) in MED_FIELD:
            remove.append((start, end))
    if not remove:
        return block, indent
    parts: list[str] = []
    last = 0
    for start, end in remove:
        parts.append(block[last:start])
        last = end
    parts.append(block[last:])
    cleaned = re.sub(r"\n{3,}", "\n\n", "".join(parts))
    return cleaned, indent


def entry_lines(indent: str, *, bandage: tuple[int, int] | None = None, morphine: tuple[int, int] | None = None, morphine_chance: int | None = None) -> list[str]:
    lines: list[str] = []
    if bandage is not None:
        a, b = bandage
        lines.append(
            f"{indent}PlaceObj('LootEntryInventoryItem', {{ "
            f'item = "JAZZ_Bandage", stack_min = {a}, stack_max = {b} }}),'
        )
    if morphine is not None:
        a, b = morphine
        if morphine_chance is not None and morphine_chance < 100:
            lines.append(
                f"{indent}PlaceObj('LootEntryInventoryItem', {{ "
                f"generate_chance = {morphine_chance}, "
                f'item = "JAZZ_Morphine", stack_min = {a}, stack_max = {b} }}),'
            )
        else:
            lines.append(
                f"{indent}PlaceObj('LootEntryInventoryItem', {{ "
                f'item = "JAZZ_Morphine", stack_min = {a}, stack_max = {b} }}),'
            )
    return lines


def insert_after_kits_or_firearm(block: str, lines: list[str]) -> str:
    if not lines:
        return block
    payload = "\n".join(lines) + "\n"
    for key in ("JAZZ_Morphine", "JAZZ_Bandage", "Medkit", "FirstAidKit", "Meds"):
        # prefer after existing kits if present
        idx = block.find(f'item = "{key}"')
        if idx < 0:
            continue
        end_entry = block.find("}),", idx)
        if end_entry >= 0:
            return block[: end_entry + 3] + "\n" + payload + block[end_entry + 3 :]
    # after firearm loot_def
    m = re.search(r"loot_def\s*=\s*\"[^\"]+_Firearm\"", block)
    if m:
        end_entry = block.find("}),", m.start())
        if end_entry >= 0:
            return block[: end_entry + 3] + "\n" + payload + block[end_entry + 3 :]
    last = block.rfind("}")
    return block[:last] + payload + block[last:]


def plan_for(tier: int, is_medic: bool) -> tuple[tuple[int, int] | None, tuple[int, int] | None, int | None]:
    """Return (bandage, morphine, morphine_chance)."""
    if is_medic:
        return MEDIC_BANDAGE, MEDIC_MORPHINE, None
    if tier == 2:
        return T2_BANDAGE, None, None
    if tier == 3:
        return None, (1, 1), T3_MORPHINE_CHANCE
    return None, None, None


def field_med_ok(block: str, bandage, morphine, morphine_chance) -> bool:
    """True if block already matches the planned Bandage/Morphine entries."""
    got: dict[str, list[str]] = {}
    for _, _, inner in iter_loot_entry_spans(block):
        im = re.search(r'item\s*=\s*"([^"]+)"', inner)
        if im and im.group(1) in MED_FIELD:
            got.setdefault(im.group(1), []).append(inner)
    band = got.get("JAZZ_Bandage", [])
    morph = got.get("JAZZ_Morphine", [])
    if bandage is None:
        if band:
            return False
    else:
        if len(band) != 1:
            return False
        a, b = bandage
        if f"stack_min = {a}" not in band[0] or f"stack_max = {b}" not in band[0]:
            return False
    if morphine is None:
        if morph:
            return False
    else:
        if len(morph) != 1:
            return False
        a, b = morphine
        if f"stack_min = {a}" not in morph[0] or f"stack_max = {b}" not in morph[0]:
            return False
        if morphine_chance is not None:
            if f"generate_chance = {morphine_chance}" not in morph[0]:
                return False
        elif "generate_chance" in morph[0]:
            return False
    return True


def apply_block(block: str, bandage, morphine, morphine_chance) -> str:
    if field_med_ok(block, bandage, morphine, morphine_chance):
        return block
    cleaned, indent = strip_field_med(block)
    lines = entry_lines(indent, bandage=bandage, morphine=morphine, morphine_chance=morphine_chance)
    if not lines:
        return cleaned
    return insert_after_kits_or_firearm(cleaned, lines)


def main() -> int:
    dry = "--dry" in sys.argv
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    text = UNITS_ITEMS.read_text(encoding="utf-8")
    loots = extract_loot_blocks(text)

    targets: dict[str, tuple] = {}
    for uid, recipe in recipes.items():
        inv = recipe.get("inventory")
        if not inv:
            continue
        tier = int(recipe.get("class_tier") or 0)
        is_medic = bool((recipe.get("utility") or {}).get("medkit"))
        bandage, morphine, chance = plan_for(tier, is_medic)
        targets[inv] = (uid, tier, is_medic, bandage, morphine, chance)

    replacements: list[tuple[int, int, str]] = []
    stats = {"t2": 0, "t3": 0, "medic": 0, "strip_extra": 0, "rewritten": 0, "missing": []}

    for inv, (uid, tier, is_medic, bandage, morphine, chance) in sorted(targets.items()):
        if inv not in loots:
            stats["missing"].append(inv)
            continue
        start, end, block = loots[inv]
        if is_medic:
            stats["medic"] += 1
        elif tier == 2:
            stats["t2"] += 1
        elif tier == 3:
            stats["t3"] += 1
        new_block = apply_block(block, bandage, morphine, chance)
        if new_block != block:
            replacements.append((start, end, new_block))
            stats["rewritten"] += 1
            # refresh loots offsets? apply from end later

    # Strip accidental med on launcher / non-recipe junk
    for extra in STRIP_EXTRA:
        if extra not in loots:
            continue
        # if already replaced via recipes, use replacements; else from original loots
        start, end, block = loots[extra]
        # find current text version after replacements applied at end — handle separately
        cleaned, _ = strip_field_med(block)
        if cleaned != block:
            replacements.append((start, end, cleaned))
            stats["strip_extra"] += 1

    replacements.sort(key=lambda x: x[0], reverse=True)
    # dedupe by start (last write wins if duplicate)
    seen = set()
    uniq: list[tuple[int, int, str]] = []
    for start, end, nb in replacements:
        if start in seen:
            continue
        seen.add(start)
        uniq.append((start, end, nb))

    new_text = text
    for start, end, nb in uniq:
        new_text = new_text[:start] + nb + new_text[end:]

    print(
        f"t2={stats['t2']} t3={stats['t3']} medic={stats['medic']} "
        f"rewritten={len(uniq)} strip_extra={stats['strip_extra']} "
        f"missing={stats['missing']}"
    )
    if dry:
        for sample in ("Raider_Inventory", "Sniper_Inventory", "Bonemaker_Inventory", "Mortarman_Launcher", "Roughneck_Inventory"):
            im = re.search(rf'\bid\s*=\s*"{sample}"', new_text)
            if not im:
                print("missing sample", sample)
                continue
            start = new_text.rfind("PlaceObj('ModItemLootDef'", 0, im.start())
            i = new_text.find("{", start)
            depth = 0
            for j in range(i, len(new_text)):
                if new_text[j] == "{":
                    depth += 1
                elif new_text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        print(f"---- {sample} ----")
                        for line in new_text[start : j + 1].splitlines():
                            if any(k in line for k in ("Bandage", "Morphine", "FirstAid", "Medkit", "id =")):
                                print(line)
                        break
        print("DRY RUN — no write")
        return 0

    UNITS_ITEMS.write_text(new_text, encoding="utf-8")
    print(f"wrote {UNITS_ITEMS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
