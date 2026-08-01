#!/usr/bin/env python3
"""Export ATTACH-001 CSV snapshots directly from the working tree.

The game/editor export is unavailable here, so this intentionally reads the
same generated-data sources that runtime loads: items.lua for component and
effect definitions, and InventoryItem companions for weapon slot wiring.
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

from _apply_attach_001 import list_ids, placeobj_blocks, prop

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
INVENTORY = ROOT / "InventoryItem"
DATA = ROOT / "docs" / "technical" / "weapons" / "data"
SNAPSHOT = "working-tree"


def scalar(block: str, key: str, default: str = "") -> str:
    """Read a quoted or numeric Lua property from a PlaceObj/class block."""
    match = re.search(
        rf"(?:'{re.escape(key)}',|\b{re.escape(key)}\s*=)\s*(?:\"([^\"]*)\"|(-?\d+(?:\.\d+)?)|(true|false))",
        block,
        re.I,
    )
    return next((value for value in match.groups() if value is not None), default) if match else default


def params(block: str) -> str:
    rows: list[str] = []
    for param in placeobj_blocks(block, "PresetParamNumber") + placeobj_blocks(block, "PresetParamPercent"):
        name, value = prop(param.text, "Name"), scalar(param.text, "Value")
        if name and value:
            rows.append(f"{name}={value}")
    return ";".join(sorted(set(rows)))


def display_name(block: str, fallback: str) -> str:
    match = re.search(r"(?:DisplayName|display_name)\s*=\s*T\([\s\S]*?\"([^\"]*)\"\)", block)
    return match.group(1) if match else fallback


def costs(block: str) -> str:
    pairs = re.findall(r'"([^"]+)"\s*,\s*(-?\d+)', block[block.find("AdditionalCosts"):])
    return ";".join(f"{key}={value}" for key, value in pairs)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    items = ITEMS.read_text(encoding="utf-8")
    component_blocks = placeobj_blocks(items, "ModItemWeaponComponent")
    effect_blocks = placeobj_blocks(items, "ModItemWeaponComponentEffect")

    components: dict[str, dict[str, str]] = {}
    for block in component_blocks:
        cid = prop(block.text, "id")
        if not cid:
            continue
        components[cid] = {
            "component_id": cid,
            "display_name": display_name(block.text, cid),
            "slot": prop(block.text, "Slot") or "",
            "cost": scalar(block.text, "Cost"),
            "modification_difficulty": scalar(block.text, "ModificationDifficulty"),
            "effects": ";".join(sorted(list_ids(block.text, "ModificationEffects"))),
            "parameters": params(block.text),
            "additional_costs": costs(block.text),
            "group": prop(block.text, "group") or "",
            "used_by_count": "0",
            "source": "jazz",
            "snapshot_commit": SNAPSHOT,
        }

    effects: list[dict[str, str]] = []
    for block in effect_blocks:
        eid = prop(block.text, "id")
        if not eid:
            continue
        description = re.search(r"Description\s*=\s*T\([\s\S]*?\"([^\"]*)\"\)", block.text)
        effects.append({
            "effect_id": eid,
            "display_name": display_name(block.text, eid),
            "description": description.group(1) if description else "",
            "parameters": params(block.text),
            "source": "jazz",
            "snapshot_commit": SNAPSHOT,
        })

    options: list[dict[str, str]] = []
    references = Counter()
    seen_weapons: set[str] = set()

    def append_weapon_slots(weapon_id: str, text: str, source_file: str) -> None:
        seen_weapons.add(weapon_id)
        for slot_index, slot in enumerate(placeobj_blocks(text, "WeaponComponentSlot"), start=1):
            slot_type = prop(slot.text, "SlotType") or ""
            modifiable = scalar(slot.text, "Modifiable", "true")
            can_be_empty = scalar(slot.text, "CanBeEmpty", "false")
            default = scalar(slot.text, "DefaultComponent")
            available = sorted(list_ids(slot.text, "AvailableComponents"))
            if default and default not in available:
                available.insert(0, default)
            for option_index, cid in enumerate(available, start=1):
                references[cid] += 1
                component = components.get(cid)
                options.append({
                    "weapon_id": weapon_id,
                    "slot_index": str(slot_index),
                    "slot_type": slot_type,
                    "modifiable": modifiable,
                    "can_be_empty": can_be_empty,
                    "default_component": default,
                    "default_in_options": str(bool(default and default in available)).lower(),
                    "option_index": str(option_index),
                    "component_id": cid,
                    "component_name": component["display_name"] if component else cid,
                    "component_source": component["source"] if component else "vanilla_ref",
                    "is_default": str(cid == default).lower(),
                    "source_file": source_file,
                    "snapshot_commit": SNAPSHOT,
                })

    for path in sorted(INVENTORY.glob("*.lua")):
        append_weapon_slots(path.stem, path.read_text(encoding="utf-8"), f"InventoryItem/{path.name}")

    # Weapons that exist only as ModItems (no companion), e.g. LionRoar.
    for block in placeobj_blocks(items, "ModItemInventoryItemCompositeDef"):
        weapon_id = prop(block.text, "id")
        if not weapon_id or weapon_id in seen_weapons:
            continue
        append_weapon_slots(weapon_id, block.text, "items.lua")

    for cid, count in references.items():
        if cid in components:
            components[cid]["used_by_count"] = str(count)
        else:
            first_option = next(option for option in options if option["component_id"] == cid)
            components[cid] = {
                "component_id": cid, "display_name": cid, "slot": first_option["slot_type"],
                "cost": "", "modification_difficulty": "", "effects": "", "parameters": "",
                "additional_costs": "", "group": "", "used_by_count": str(count),
                "source": "vanilla_ref", "snapshot_commit": SNAPSHOT,
            }

    component_fields = list(next(csv.DictReader((DATA / "weapon-components.csv").open(encoding="utf-8-sig"))).keys())
    effect_fields = list(next(csv.DictReader((DATA / "weapon-component-effects.csv").open(encoding="utf-8-sig"))).keys())
    option_fields = list(next(csv.DictReader((DATA / "weapon-component-options.csv").open(encoding="utf-8-sig"))).keys())
    write_csv(DATA / "weapon-components.csv", component_fields, sorted(components.values(), key=lambda row: row["component_id"]))
    write_csv(DATA / "weapon-component-effects.csv", effect_fields, sorted(effects, key=lambda row: row["effect_id"]))
    write_csv(DATA / "weapon-component-options.csv", option_fields, options)

    weapons_path = DATA / "weapons.csv"
    with weapons_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        weapon_fields = list(reader.fieldnames or [])
        weapons = list(reader)
    for field in (
        "weapon_mass", "cyclic_rpm", "weapon_size_class", "burst_limiter",
        "close_range", "close_range_factor",
    ):
        if field not in weapon_fields:
            weapon_fields.append(field)
    for row in weapons:
        companion = INVENTORY / f"{row['id']}.lua"
        if companion.exists():
            text = companion.read_text(encoding="utf-8")
        else:
            text = next(
                (
                    block.text
                    for block in placeobj_blocks(items, "ModItemInventoryItemCompositeDef")
                    if prop(block.text, "id") == row["id"]
                ),
                "",
            )
        row["close_range"] = scalar(text, "CloseRange")
        row["close_range_factor"] = scalar(text, "CloseRangeFactor")
        row["weapon_mass"] = scalar(text, "WeaponMass")
        row["cyclic_rpm"] = scalar(text, "CyclicRPM")
        row["weapon_size_class"] = scalar(text, "WeaponSizeClass")
        row["burst_limiter"] = scalar(text, "BurstLimiter")
        row["recoil"] = scalar(text, "Recoil")
        row["burst_shots"] = scalar(text, "BurstShots")
        row["auto_shots"] = scalar(text, "AutoShots")
        row["snapshot_commit"] = SNAPSHOT
    write_csv(weapons_path, weapon_fields, weapons)
    print(f"components={len(components)} effects={len(effects)} options={len(options)} weapons={len(weapons)}")
    print(f"vanilla_ref_stubs={sum(row['source'] == 'vanilla_ref' for row in components.values())}")


if __name__ == "__main__":
    main()
