#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply JAZZ-ATTACH-001's absolute MagazineSizeSet data migration.

Default mode only validates the transformation.  ``--apply`` writes atomically
with ``.bak`` backups beside each changed generated-data or localization file.
The script intentionally leaves Auto5 barrel high-cap components untouched.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
from collections import Counter
from pathlib import Path

from _apply_attach_001 import (
    atomic_write,
    consume_trailing_list_comma,
    list_ids,
    list_region,
    placeobj_blocks,
    prop,
)
import _rebalance_magazine_tiers as magazine


ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
METADATA = ROOT / "metadata.lua"
INVENTORY = ROOT / "InventoryItem"
RUSSIAN = ROOT / "Russian.csv"
ENGLISH = ROOT / "English.csv"
LOC_ID = "543656846802"

LARGE_TARGETS = {
    50: {"AK47", "AR15", "M16A2", "M4Commando", "MP5", "Sig550", "Sig550Custom",
         "Sig552", "Sig552SWAT", "MP40"},
    28: {"Bereta92", "Glock17"},
    27: {"Beretta93r", "CZ75", "SWModel5906"},
    25: {"AA12", "USAS12", "VectorCP1"},
    13: {"CZ52", "DesertEagle", "MAC1950", "P38"},
    8: {"BarretM82", "PSG1", "SWModel52"},
}
WEAPON_TARGET = {
    weapon: f"JAZZ_MagLarge_{size}"
    for size, weapons in LARGE_TARGETS.items()
    for weapon in weapons
}
NEW_LARGE_IDS = tuple(sorted(set(WEAPON_TARGET.values())))


def effect_block() -> str:
    return """PlaceObj('ModItemWeaponComponentEffect', {
					Description = T(543656846802, --[[ModItemWeaponComponentEffect MagazineSizeSet Description]] "Размер магазина <MagazineSize>"),
					ModificationType = "Set",
					Parameters = {
						PlaceObj('PresetParamNumber', {
							'Name', "MagazineSize",
							'Tag', "<MagazineSize>",
						}),
					},
					RequiredParams = {
						"MagazineSize",
					},
					StatToModify = "MagazineSize",
					group = "Stats",
					id = "MagazineSizeSet",
				}),
				"""


def component_block(text: str, component_id: str) -> str:
    for block in placeobj_blocks(text, "ModItemWeaponComponent"):
        if prop(block.text, "id") == component_id:
            return block.text
    raise ValueError(f"missing WeaponComponent {component_id}")


def replace_component_id(block: str, component_id: str) -> str:
    changed, count = re.subn(
        r'(\bid\s*=\s*)"JAZZ_MagLarge"', rf'\1"{component_id}"', block, count=1
    )
    if count != 1:
        raise ValueError("could not clone JAZZ_MagLarge id")
    return changed


def set_large_profile(block: str, size: int) -> str:
    profile = {
        "kind": "large",
        "comment": f"Mag Large — size-{size} Reload+2 Rel-15 AA-15%",
        "size_mode": "set",
        "size_value": size,
        "cost": 40,
        "diff": 0,
    }
    return magazine.patch_block(block, profile)


def add_set_effect(items: str) -> tuple[str, int]:
    if re.search(r'\bid\s*=\s*"MagazineSizeSet"', items):
        repaired = re.sub(
            r"(?m)^\s*,\s*$\n(?=\s*PlaceObj\('ModItemWeaponComponentEffect')",
            "",
            items,
            count=1,
        )
        return repaired, int(repaired != items)
    for block in placeobj_blocks(items, "ModItemWeaponComponentEffect"):
        if prop(block.text, "id") == "MagazineSizeAdd":
            next_item = consume_trailing_list_comma(items, block.end)
            return items[:block.end] + ",\n\t\t\t\t" + effect_block() + items[next_item:], 1
    raise ValueError("MagazineSizeAdd effect was not found")


def add_large_variants(items: str) -> tuple[str, int]:
    existing = {prop(block.text, "id") for block in placeobj_blocks(items, "ModItemWeaponComponent")}
    missing = [component_id for component_id in NEW_LARGE_IDS if component_id not in existing]
    if not missing:
        return items, 0
    generic = component_block(items, "JAZZ_MagLarge")
    additions = "\n".join(
        set_large_profile(replace_component_id(generic, component_id), int(component_id.rsplit("_", 1)[1]))
        + ","
        for component_id in missing
    )
    position = next(
        block.end for block in placeobj_blocks(items, "ModItemWeaponComponent")
        if prop(block.text, "id") == "JAZZ_MagLarge"
    )
    return items[:position] + ",\n\t\t\t\t\t\t" + additions + items[position:], len(missing)


def rewrite_slot(block: str, old: str, new: str | None) -> tuple[str, int]:
    changed = 0
    region = list_region(block, "AvailableComponents")
    if region:
        body = block[region[0]:region[1]]
        if new is None:
            body, count = re.subn(rf'^\s*"{re.escape(old)}",\s*\n', "", body, flags=re.M)
        else:
            body, count = re.subn(rf'"{re.escape(old)}"', f'"{new}"', body)
        changed += count
        block = block[:region[0]] + body + block[region[1]:]
    default = re.search(r"('DefaultComponent',\s*)\"([^\"]+)\"", block)
    if default and default.group(2) == old:
        if new is None:
            raise ValueError(f"cannot remove default component {old}")
        block = block[:default.start()] + default.group(1) + f'"{new}"' + block[default.end():]
        changed += 1
    return block, changed


def rewrite_slots(text: str, old: str, new: str | None) -> tuple[str, int]:
    """Rewrite every component slot in one weapon definition or companion."""
    changed = 0
    for slot in reversed(placeobj_blocks(text, "WeaponComponentSlot")):
        updated, count = rewrite_slot(slot.text, old, new)
        text = text[:slot.start] + updated + text[slot.end:]
        changed += count
    return text, changed


def rewrite_weapon_slots(text: str, weapon_map: dict[str, str], remove_psg_fine: bool) -> tuple[str, int]:
    changed = 0
    for weapon in weapon_map:
        for owner in reversed(placeobj_blocks(text, "ModItemInventoryItemCompositeDef")):
            if prop(owner.text, "id") != weapon:
                continue
            updated, count = rewrite_slots(owner.text, "JAZZ_MagLarge", weapon_map[weapon])
            if remove_psg_fine and weapon == "PSG1":
                updated, removed = rewrite_slots(updated, "JAZZ_MagLargeFine", None)
                count += removed
            text = text[:owner.start] + updated + text[owner.end:]
            changed += count
    return text, changed


def find_slot_references(text: str, component_id: str) -> int:
    return sum(
        len(re.findall(rf'"{re.escape(component_id)}"', block.text))
        for block in placeobj_blocks(text, "WeaponComponentSlot")
    )


def delete_component_and_resource(items: str, metadata: str, component_id: str) -> tuple[str, str]:
    for block in reversed(placeobj_blocks(items, "ModItemWeaponComponent")):
        if prop(block.text, "id") == component_id:
            items = items[:block.start] + items[consume_trailing_list_comma(items, block.end):]
    for block in reversed(placeobj_blocks(metadata, "ModResourcePreset")):
        if prop(block.text, "Class") == "WeaponComponent" and prop(block.text, "Id") == component_id:
            metadata = metadata[:block.start] + metadata[consume_trailing_list_comma(metadata, block.end):]
    return items, metadata


def add_resources(metadata: str) -> tuple[str, int]:
    additions: list[str] = []
    if not re.search(r"'Class',\s*\"WeaponComponentEffect\",\s*'Id',\s*\"MagazineSizeSet\"", metadata, re.S):
        additions.append(
            '\t\tPlaceObj(\'ModResourcePreset\', {\n'
            '\t\t\t\'Class\', "WeaponComponentEffect",\n'
            '\t\t\t\'Id\', "MagazineSizeSet",\n'
            '\t\t\t\'ClassDisplayName\', "Modification Effects",\n'
            '\t\t}),\n'
        )
    existing = set(re.findall(
        r"'Class',\s*\"WeaponComponent\",\s*'Id',\s*\"([^\"]+)\"", metadata, re.S
    ))
    additions.extend(
        '\t\tPlaceObj(\'ModResourcePreset\', {\n'
        '\t\t\t\'Class\', "WeaponComponent",\n'
        f'\t\t\t\'Id\', "{component_id}",\n'
        '\t\t\t\'ClassDisplayName\', "Weapon Component",\n'
        '\t\t}),\n'
        for component_id in NEW_LARGE_IDS if component_id not in existing
    )
    if not additions:
        return metadata, 0
    anchor = next(
        block.start for block in placeobj_blocks(metadata, "ModResourcePreset")
        if prop(block.text, "Class") == "WeaponComponentEffect"
        and prop(block.text, "Id") == "MagazineSizeAdd"
    )
    return metadata[:anchor] + "".join(additions) + metadata[anchor:], len(additions)


def add_localization(path: Path, source: str, translation: str) -> bool:
    content = path.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(io.StringIO(content.removeprefix("sep=,\n")))
    if LOC_ID in {row["ID"] for row in reader}:
        return False
    row = io.StringIO()
    writer = csv.writer(row, lineterminator="\n")
    writer.writerow([LOC_ID, source, translation, "", "jazz:items.lua:MagazineSizeSet"])
    atomic_write(path, content.rstrip("\r\n") + "\n" + row.getvalue())
    return True


def validate(items: str, metadata: str, companions: dict[Path, str]) -> list[str]:
    problems: list[str] = []
    mag_blocks = [
        block for block in placeobj_blocks(items, "ModItemWeaponComponent")
        if (prop(block.text, "id") or "").startswith("JAZZ_Mag")
    ]
    multiplied = [prop(block.text, "id") for block in mag_blocks if "MagazineSizeMultiplier" in block.text]
    if multiplied:
        problems.append(f"live Mag components still use MagazineSizeMultiplier: {multiplied}")
    generic_refs = find_slot_references(items, "JAZZ_MagLarge") + sum(
        find_slot_references(text, "JAZZ_MagLarge") for text in companions.values()
    )
    if generic_refs:
        problems.append(f"JAZZ_MagLarge slot references remain: {generic_refs}")
    if re.search(r'\bid\s*=\s*"JAZZ_MagLarge"', items):
        problems.append("obsolete JAZZ_MagLarge definition remains")
    if re.search(r"'Class',\s*\"WeaponComponent\",\s*'Id',\s*\"JAZZ_MagLarge\"", metadata, re.S):
        problems.append("obsolete JAZZ_MagLarge metadata resource remains")
    sample = component_block(items, "JAZZ_MagLarge_30_45")
    if "MagazineSizeSet" not in sample or not re.search(
        r"'Name',\s*\"MagazineSize\",\s*'Value',\s*45,", sample, re.S
    ):
        problems.append("JAZZ_MagLarge_30_45 is not MagazineSizeSet=45")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write data and localization changes")
    args = parser.parse_args()
    for path in (ITEMS, METADATA, RUSSIAN, ENGLISH):
        if not path.exists():
            raise FileNotFoundError(path)
    items = ITEMS.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    companions = {
        path: path.read_text(encoding="utf-8")
        for path in INVENTORY.glob("*.lua")
    }
    summary = Counter()

    items, summary["MagazineSizeSet_effect_added"] = add_set_effect(items)
    items, summary["MagLarge_variants_added"] = add_large_variants(items)
    items, changed = rewrite_weapon_slots(items, WEAPON_TARGET, remove_psg_fine=True)
    summary["item_slot_refs_rewritten_or_removed"] = changed
    for path, content in companions.items():
        weapon_id = path.stem
        if weapon_id not in WEAPON_TARGET:
            continue
        content, changed = rewrite_slots(content, "JAZZ_MagLarge", WEAPON_TARGET[weapon_id])
        if weapon_id == "PSG1":
            content, removed = rewrite_slots(content, "JAZZ_MagLargeFine", None)
            changed += removed
        companions[path] = content
        summary["companion_slot_refs_rewritten_or_removed"] += changed

    # Rebalance all named/small/drum/belt profiles with the shared profile table.
    for block in reversed(placeobj_blocks(items, "ModItemWeaponComponent")):
        component_id = prop(block.text, "id")
        if component_id not in magazine.PROFILES:
            continue
        updated = magazine.patch_block(block.text, magazine.PROFILES[component_id])
        items = items[:block.start] + updated + items[block.end:]
        summary["profiles_rebalanced"] += 1

    items, metadata = delete_component_and_resource(items, metadata, "JAZZ_MagLarge")
    metadata, summary["resources_added"] = add_resources(metadata)
    problems = validate(items, metadata, companions)

    print(f"mode: {'apply' if args.apply else 'dry-run'}")
    for name in sorted(summary):
        print(f"{name}: {summary[name]}")
    print(f"MagLarge variants: {', '.join(NEW_LARGE_IDS)}")
    print("Auto5 LMag: skipped (barrel-specific MagazineSizeMultiplier)")
    if problems:
        print("validation failed:")
        print("\n".join(f" - {problem}" for problem in problems))
        return 1
    print("verification: no live Mag multiplier; generic MagLarge refs=0; 30_45=Set(45)")
    if not args.apply:
        return 0
    atomic_write(ITEMS, items)
    atomic_write(METADATA, metadata)
    for path, content in companions.items():
        if content != path.read_text(encoding="utf-8"):
            atomic_write(path, content)
    if LOC_ID in RUSSIAN.read_text(encoding="utf-8-sig") or LOC_ID in ENGLISH.read_text(encoding="utf-8-sig"):
        if LOC_ID not in RUSSIAN.read_text(encoding="utf-8-sig") or LOC_ID not in ENGLISH.read_text(encoding="utf-8-sig"):
            raise ValueError(f"{LOC_ID} must exist in both localization tables or neither")
    else:
        summary["Russian_localization_added"] = add_localization(
            RUSSIAN, "Размер магазина <MagazineSize>", "Размер магазина <MagazineSize>"
        )
        summary["English_localization_added"] = add_localization(
            ENGLISH, "Размер магазина <MagazineSize>", "Magazine size <MagazineSize>"
        )
    print("apply completed; .bak backups were written beside changed files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
