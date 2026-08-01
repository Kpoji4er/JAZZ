#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the generated-data portion of JAZZ-ATTACH-001.

The default mode is intentionally read-only.  ``--apply`` writes a sibling
``.bak`` backup before atomically replacing items.lua and metadata.lua.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
METADATA = ROOT / "metadata.lua"
INVENTORY = ROOT / "InventoryItem"
WEAPONS_CSV = ROOT / "docs/technical/weapons/data/weapons.csv"
AUDIT = ROOT / "docs/tools/_attach_001_audit.tsv"

HANDLING_EFFECTS = frozenset(
    {
        "ScopeHandlingReduce", "MagazineHandlingDecrease",
        "MagazineHandlingIncrease", "BarrelHandlingIncrease",
        "BarrelHandlingReduce", "SilencerHandlingReduce",
        "SilencerHandlingDecrease", "GripHandlingIncrease",
        "StockHandlingIncrease", "GLHandlingDecrease",
        "BipodsHandlingDecrease", "Cumbersome",
    }
)
PURE_ERGO = frozenset({"TacGrip", "Handgrip_Ergo", "SigErgoHandGrip", "HandlingWrap"})
DELETE_EFFECTS = HANDLING_EFFECTS | {
    "ScopeCTHBonus", "ScopeAccuracyIncreace", "ScopeAccuracyReduce",
    "ReduceRange50Percent", "ReduceAuto50Percent",
    "ReduceAimAccuracy50Percent", "ReduceAimAccuracy80Percent",
}
CLOSE_EFFECTS = (
    ("CloseRangeIncrease", None, "CloseRange", "CloseRangeIncrease", 2,
     982641736301, "Ближняя зона: Увеличивает ближнюю зону на <CloseRangeIncrease>"),
    ("CloseRangeDecrease", "Subtract", "CloseRange", "CloseRangeDecrease", 2,
     982641736302, "Ближняя зона: Уменьшает ближнюю зону на <CloseRangeDecrease>"),
    ("CloseRangeFactorIncrease", None, "CloseRangeFactor", "CloseRangeFactorIncrease", 5,
     982641736303, "Ближняя зона: Усиливает эффективность на ближней дистанции на <CloseRangeFactorIncrease>"),
    ("CloseRangeFactorDecrease", "Subtract", "CloseRangeFactor", "CloseRangeFactorDecrease", 5,
     982641736304, "Ближняя зона: Ослабляет эффективность на ближней дистанции на <CloseRangeFactorDecrease>"),
)
BASE_CLOSE_RANGE = {
    "pistol": (0, 100), "autopistol": (0, 100), "revolver": (0, 100),
    "submachine-gun": (2, 95), "carbine": (4, 90), "shotgun": (4, 90),
    "assault-rifle": (6, 85), "machine-gun": (6, 85),
    "light-machine-gun": (6, 85), "battle-rifle": (8, 80),
    "sniper-rifle": (12, 70),
}


@dataclass
class Block:
    start: int
    end: int
    text: str


def matching_paren(text: str, start: int) -> int:
    """Return the closing parenthesis for ``start`` while ignoring Lua strings/comments."""
    depth, i, quote = 0, start, None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif text.startswith("--[[", i):
            end = text.find("]]", i + 4)
            i = len(text) if end < 0 else end + 1
        elif text.startswith("--", i):
            end = text.find("\n", i + 2)
            i = len(text) if end < 0 else end
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError(f"unclosed PlaceObj at offset {start}")


def placeobj_blocks(text: str, cls: str) -> list[Block]:
    marker = f"PlaceObj('{cls}'"
    result, at = [], 0
    while (at := text.find(marker, at)) >= 0:
        end = matching_paren(text, text.find("(", at))
        result.append(Block(at, end + 1, text[at:end + 1]))
        at = end + 1
    return result


def prop(block: str, name: str) -> str | None:
    match = re.search(
        rf"(?:\b{name}\s*=|'{re.escape(name)}',)\s*\"([^\"]+)\"", block,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else None


def replace_blocks(text: str, blocks: list[Block], fn) -> str:
    for block in reversed(blocks):
        text = text[:block.start] + fn(block.text) + text[block.end:]
    return text


def list_region(block: str, property_name: str) -> tuple[int, int] | None:
    match = re.search(
        rf"(?:\b{re.escape(property_name)}\s*=|'{re.escape(property_name)}',)\s*\{{",
        block, flags=re.IGNORECASE,
    )
    if not match:
        return None
    start = block.find("{", match.start())
    depth = 0
    for pos in range(start, len(block)):
        if block[pos] == "{":
            depth += 1
        elif block[pos] == "}":
            depth -= 1
            if depth == 0:
                return start, pos + 1
    raise ValueError(f"unclosed {property_name} list")


def list_ids(block: str, property_name: str) -> set[str]:
    region = list_region(block, property_name)
    return set(re.findall(r'"([^"]+)"', block[region[0]:region[1]])) if region else set()


def delete_named_params(block: str, names: set[str]) -> tuple[str, int]:
    """Remove complete PresetParam PlaceObj blocks with a matching Name."""
    removed = 0
    params = placeobj_blocks(block, "PresetParamNumber") + placeobj_blocks(block, "PresetParamPercent")
    for param in reversed(sorted(params, key=lambda item: item.start)):
        name = prop(param.text, "Name")
        if name in names:
            block = block[:param.start] + block[param.end:] 
            removed += 1
    return block, removed


def append_effect(block: str, effect: str) -> str:
    region = list_region(block, "ModificationEffects")
    if region is None:
        anchor = re.search(r"(\s*)Parameters\s*=", block)
        if not anchor:
            raise ValueError("component missing Parameters and ModificationEffects")
        indent = anchor.group(1)
        insert = f'{indent}ModificationEffects = {{\n{indent}\t"{effect}",\n{indent}}},\n'
        return block[:anchor.start()] + insert + block[anchor.start():]
    body = block[region[0]:region[1]]
    if f'"{effect}"' not in body:
        indent = re.search(r"\n([ \t]*)", body).group(1)
        body = body[:-1] + f'\n{indent}"{effect}",\n{indent[:-1] if indent else ""}}}'
        return block[:region[0]] + body + block[region[1]:]
    return block


def append_param(block: str, name: str, value: int) -> str:
    if re.search(rf"'Name',\s*\"{re.escape(name)}\"", block):
        return block
    region = list_region(block, "Parameters")
    entry = (
        "\n\t\t\t\tPlaceObj('PresetParamNumber', {\n"
        f"\t\t\t\t\t'Name', \"{name}\",\n"
        f"\t\t\t\t\t'Value', {value},\n"
        f"\t\t\t\t\t'Tag', \"<{name}>\",\n"
        "\t\t\t\t}),"
    )
    if region is None:
        anchor = re.search(r"(\s*)Slot\s*=", block)
        if not anchor:
            raise ValueError("component missing Parameters and Slot")
        indent = anchor.group(1)
        entry = entry.replace("\t\t\t\t", indent + "\t").replace("\t\t\t\t\t", indent + "\t\t")
        return block[:anchor.start()] + f"{indent}Parameters = {{{entry}\n{indent}}},\n" + block[anchor.start():]
    return block[:region[1] - 1] + entry + "\n\t\t\t}" + block[region[1]:]


def normalize_component(block: str, summary: Counter, audit: list[tuple[str, str, str]]) -> str:
    cid = prop(block, "id") or "<unknown>"
    region = list_region(block, "ModificationEffects")
    effects = list_ids(block, "ModificationEffects")
    removed = effects & HANDLING_EFFECTS
    if region and removed:
        old = block[region[0]:region[1]]
        new = re.sub(r'^\s*"(' + "|".join(map(re.escape, removed)) + r')",\s*\n', "", old, flags=re.M)
        block = block[:region[0]] + new + block[region[1]:]
        summary["stripped_handling"] += len(removed)
        audit.append((cid, "strip", ";".join(sorted(removed))))
    block, parameters_removed = delete_named_params(block, HANDLING_EFFECTS)
    summary["handling_parameters_removed"] += parameters_removed
    if cid in PURE_ERGO:
        before = block
        block = append_effect(block, "RecoilDecrease")
        block = append_param(block, "Recoil", 1)
        if block != before:
            summary["pure_ergo_fixed"] += 1
            audit.append((cid, "pure_ergo", "ensure RecoilDecrease; Recoil=1"))
    if cid == "JAZZ_Scope_8x_SCROME":
        block, n = re.subn(
            r"('Name',\s*\"ShotAP\",\s*'Value',\s*)([2-9]\d*)",
            r"\g<1>1", block, flags=re.S,
        )
        summary["scrome_shotap_fixed"] += n
    return block


def component_ids(text: str) -> dict[str, Block]:
    return {prop(block.text, "id"): block for block in placeobj_blocks(text, "ModItemWeaponComponent") if prop(block.text, "id")}


def slot_blocks(text: str) -> list[Block]:
    return placeobj_blocks(text, "WeaponComponentSlot")


def slot_refs(text: str, active_only: set[str] | None = None) -> set[str]:
    refs: set[str] = set()
    if active_only is None:
        containers = [text]
    else:
        containers = [
            block.text for block in placeobj_blocks(text, "ModItemInventoryItemCompositeDef")
            if (prop(block.text, "id") in active_only)
        ]
    for container in containers:
        for slot in slot_blocks(container):
            if prop(slot.text, "SlotType") == "Mount":
                continue
            refs |= list_ids(slot.text, "AvailableComponents")
            default = re.search(r"'DefaultComponent',\s*\"([^\"]+)\"", slot.text)
            if default:
                refs.add(default.group(1))
    return refs


def rename_slots(text: str, rename: dict[str, str]) -> tuple[str, int]:
    """Rename component ids in AvailableComponents / DefaultComponent only.

    Never rewrite SlotType (or other) quoted strings — component ids can collide
    with slot names (Bipod, Handguard, Freeswap).
    """
    changed = 0
    for block in reversed(slot_blocks(text)):
        new = block.text
        region = list_region(new, "AvailableComponents")
        if region:
            body = new[region[0]:region[1]]
            for old, fresh in rename.items():
                body, count = re.subn(rf'("{re.escape(old)}")', f'"{fresh}"', body)
                changed += count
            new = new[:region[0]] + body + new[region[1]:]
        default_match = re.search(r"('DefaultComponent',\s*)\"([^\"]+)\"", new)
        if default_match:
            old_default = default_match.group(2)
            if old_default in rename:
                fresh = rename[old_default]
                new = (
                    new[:default_match.start()]
                    + default_match.group(1)
                    + f'"{fresh}"'
                    + new[default_match.end():]
                )
                changed += 1
        text = text[:block.start] + new + text[block.end:]
    return text, changed


def remove_mount_slots(text: str) -> tuple[str, int]:
    removed = 0
    for block in reversed(slot_blocks(text)):
        if prop(block.text, "SlotType") == "Mount":
            end = consume_trailing_list_comma(text, block.end)
            text = text[: block.start] + text[end:]
            removed += 1
    return text, removed


def close_effect_blocks() -> str:
    pieces = []
    for eid, modification, stat, param, default, loc, desc in CLOSE_EFFECTS:
        modline = f'\n\t\t\t\t\tModificationType = "{modification}",' if modification else ""
        pieces.append(
            "\t\t\t\tPlaceObj('ModItemWeaponComponentEffect', {"
            f'\n\t\t\t\t\tDescription = T({loc}, --[[ModItemWeaponComponentEffect {eid} Description]] "{desc}"),'
            f"{modline}\n\t\t\t\t\tParameters = {{\n\t\t\t\t\t\tPlaceObj('PresetParamNumber', {{"
            f'\n\t\t\t\t\t\t\t\'Name\', "{param}",\n\t\t\t\t\t\t\t\'Value\', {default},'
            f'\n\t\t\t\t\t\t\t\'Tag\', "<{param}>",\n\t\t\t\t\t\t}}),\n\t\t\t\t\t}},'
            f'\n\t\t\t\t\tStatToModify = "{stat}",\n\t\t\t\t\tgroup = "Stats",\n\t\t\t\t\tid = "{eid}",\n\t\t\t\t}}),\n'
        )
    return "".join(pieces)


def add_close_effects(text: str, summary: Counter) -> str:
    if "id = \"CloseRangeIncrease\"" in text:
        return text
    anchor = text.find("PlaceObj('ModItemWeaponComponentEffect', {", text.find('id = "BarrelRangeIncrease"') - 2000)
    # The anchor must be the BarrelRangeIncrease block, rather than an arbitrary nearby effect.
    for block in placeobj_blocks(text, "ModItemWeaponComponentEffect"):
        if prop(block.text, "id") == "BarrelRangeIncrease":
            text = text[:block.start] + close_effect_blocks() + text[block.start:]
            summary["close_effects_added"] += 4
            return text
    raise ValueError("BarrelRangeIncrease effect was not found")


def add_close_barrel_effects(text: str, summary: Counter, audit: list[tuple[str, str, str]]) -> str:
    blocks = placeobj_blocks(text, "ModItemWeaponComponent")
    for block in reversed(blocks):
        cid, slot = prop(block.text, "id"), prop(block.text, "Slot")
        if not cid or slot != "Barrel":
            continue
        short = "BarrelShort" in cid or cid.endswith("_Short")
        long = cid.startswith("BarrelLong") or cid == "BarrelHeavy"
        if not (short or long):
            continue
        if cid == "BarrelShort_Pistol" or "Shotgun" in cid:
            changes = (("CloseRangeDecrease", 1), ("CloseRangeFactorIncrease", 10))
        elif short:
            changes = (("CloseRangeDecrease", 2), ("CloseRangeFactorIncrease", 5))
        else:
            changes = (("CloseRangeIncrease", 2), ("CloseRangeFactorDecrease", 5))
        new = block.text
        for effect, value in changes:
            new = append_effect(new, effect)
            new = append_param(new, effect, value)
        if new != block.text:
            summary["barrels_close_wired"] += 1
            audit.append((cid, "close_range", ";".join(f"{e}={v}" for e, v in changes)))
        text = text[:block.start] + new + text[block.end:]
    return text


def active_weapons() -> dict[str, tuple[int, int]]:
    result = {}
    with WEAPONS_CSV.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row.get("catalog_status") == "active" and row.get("family_id") in BASE_CLOSE_RANGE:
                result[row["id"]] = BASE_CLOSE_RANGE[row["family_id"]]
    return result


def add_close_to_weapon_block(block: str, values: tuple[int, int]) -> tuple[str, bool]:
    if "'CloseRange'," in block and "'CloseRangeFactor'," in block:
        return block, False
    anchor = re.search(r"(\s*)'BulletDropRange',\s*[^,]+,", block)
    if not anchor:
        anchor = re.search(r"(\s*)'Handling',\s*[^,]+,", block)
    if not anchor:
        return block, False
    indent = anchor.group(1)
    insert = f"\n{indent}'CloseRange', {values[0]},\n{indent}'CloseRangeFactor', {values[1]},"
    return block[:anchor.end()] + insert + block[anchor.end():], True


def add_close_to_companion(text: str, values: tuple[int, int]) -> tuple[str, bool]:
    if re.search(r"\bCloseRange\s*=", text) and re.search(r"\bCloseRangeFactor\s*=", text):
        return text, False
    anchor = re.search(r"(\s*)(BulletDropRange|Handling)\s*=\s*[^,]+,", text)
    if not anchor:
        return text, False
    indent = anchor.group(1)
    insert = f"\n{indent}CloseRange = {values[0]},\n{indent}CloseRangeFactor = {values[1]},"
    return text[:anchor.end()] + insert + text[anchor.end():], True


def add_close_to_firearms(items: str, companions: dict[Path, str], summary: Counter) -> str:
    families = active_weapons()
    for block in reversed(placeobj_blocks(items, "ModItemInventoryItemCompositeDef")):
        wid = prop(block.text, "id")
        if wid not in families:
            continue
        fresh, changed = add_close_to_weapon_block(block.text, families[wid])
        if changed:
            items = items[:block.start] + fresh + items[block.end:]
            summary["weapons_close_set_items"] += 1
    for wid, values in families.items():
        path = INVENTORY / f"{wid}.lua"
        if path not in companions:
            continue
        fresh, changed = add_close_to_companion(companions[path], values)
        if changed:
            companions[path] = fresh
            summary["weapons_close_set_companions"] += 1
    return items


def resource_blocks(text: str) -> list[Block]:
    return placeobj_blocks(text, "ModResourcePreset")


def consume_trailing_list_comma(text: str, end: int) -> int:
    """Extend ``end`` past optional whitespace + comma after a deleted PlaceObj."""
    match = re.match(r"[ \t]*\,[ \t]*\n?", text[end:])
    return end + match.end() if match else end


def delete_placeobj_blocks(text: str, cls: str, pred) -> tuple[str, int]:
    """Delete matching PlaceObj blocks and their trailing list commas."""
    removed = 0
    for block in reversed(placeobj_blocks(text, cls)):
        if not pred(block):
            continue
        end = consume_trailing_list_comma(text, block.end)
        text = text[: block.start] + text[end:]
        removed += 1
    return text, removed


def remove_resources(text: str, cls: str, ids: set[str]) -> tuple[str, int]:
    removed = 0
    for block in reversed(resource_blocks(text)):
        if prop(block.text, "Class") == cls and prop(block.text, "Id") in ids:
            end = consume_trailing_list_comma(text, block.end)
            text = text[: block.start] + text[end:]
            removed += 1
    return text, removed


def add_close_resources(text: str) -> str:
    if '"CloseRangeIncrease"' in text:
        return text
    anchor = next((block.start for block in resource_blocks(text)
                   if prop(block.text, "Class") == "WeaponComponentEffect"), None)
    if anchor is None:
        raise ValueError("metadata has no WeaponComponentEffect resources")
    entries = "".join(
        "\t\tPlaceObj('ModResourcePreset', {\n"
        "\t\t\t'Class', \"WeaponComponentEffect\",\n"
        f"\t\t\t'Id', \"{effect[0]}\",\n"
        "\t\t\t'ClassDisplayName', \"Weapon Component Effect\",\n"
        "\t\t}),\n" for effect in CLOSE_EFFECTS
    )
    return text[:anchor] + entries + text[anchor:]


def validate(items: str) -> list[str]:
    problems = []
    counts = Counter()
    i, quote = 0, None
    while i < len(items):
        ch = items[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif items.startswith("--[[", i):
            end = items.find("]]", i + 4)
            i = len(items) if end < 0 else end + 1
        elif items.startswith("--", i):
            end = items.find("\n", i + 2)
            i = len(items) if end < 0 else end
        elif ch in "(){}[]":
            counts[ch] += 1
        i += 1
    for left, right in (("(", ")"), ("{", "}"), ("[", "]")):
        if counts[left] != counts[right]:
            problems.append(f"unbalanced {left}{right}: {counts[left]} != {counts[right]}")
    if "}),)," in items:
        problems.append("stacked closer '}),),' found")
    for block in placeobj_blocks(items, "ModItemWeaponComponent"):
        leaked = list_ids(block.text, "ModificationEffects") & HANDLING_EFFECTS
        if leaked:
            problems.append(f"{prop(block.text, 'id')}: handling effects remain: {sorted(leaked)}")
    return problems


def atomic_write(path: Path, content: str) -> None:
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8", newline="")
    os.replace(temp, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="report changes only (default)")
    mode.add_argument("--apply", action="store_true", help="write generated data and .bak files")
    args = parser.parse_args()
    apply = args.apply
    if not ITEMS.exists() or not METADATA.exists():
        raise FileNotFoundError("run from a JAZZ checkout with items.lua and metadata.lua")

    summary, audit = Counter(), []
    items = ITEMS.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    companions = {path: path.read_text(encoding="utf-8") for path in INVENTORY.glob("*.lua")}

    items = replace_blocks(items, placeobj_blocks(items, "ModItemWeaponComponent"),
                           lambda block: normalize_component(block, summary, audit))
    items = add_close_effects(items, summary)
    items = add_close_barrel_effects(items, summary, audit)
    items = add_close_to_firearms(items, companions, summary)

    # Mount slots are not part of the live component graph.
    items, mounts = remove_mount_slots(items)
    summary["mounts_removed_items"] += mounts
    for path, content in list(companions.items()):
        content, mounts = remove_mount_slots(content)
        companions[path] = content
        summary["mounts_removed_companions"] += mounts

    # Rename every defined component that is referenced from any weapon slot
    # (including excluded_disabled). SlotType names must not be rewritten.
    definitions = component_ids(items)
    referenced_any = slot_refs(items)
    rename = {
        cid: ("JAZZ_" + cid[5:] if cid.startswith("Jazz_") else "JAZZ_" + cid)
        for cid in (referenced_any & definitions.keys())
        if not cid.startswith("JAZZ_") and cid.strip(' ,"')
    }
    for old, fresh in sorted(rename.items()):
        audit.append((old, "rename", fresh))
    items, n = rename_slots(items, rename)
    summary["slot_references_renamed_items"] += n
    for path, content in list(companions.items()):
        content, n = rename_slots(content, rename)
        companions[path] = content
        summary["slot_references_renamed_companions"] += n
    # Rename the definitions, metadata, and ID-named icon paths only.
    for old, fresh in rename.items():
        for block in reversed(placeobj_blocks(items, "ModItemWeaponComponent")):
            if prop(block.text, "id") == old:
                replacement = re.sub(rf'(\bid\s*=\s*)"{re.escape(old)}"', rf'\1"{fresh}"', block.text)
                replacement = replacement.replace(f"/Chips/{old}.png", f"/Chips/{fresh}.png")
                replacement = replacement.replace(f"/Full/{old}.png", f"/Full/{fresh}.png")
                items = items[:block.start] + replacement + items[block.end:]
                summary["component_definitions_renamed"] += 1
                break
        metadata = re.sub(
            rf"('Class',\s*\"WeaponComponent\",\s*'Id',\s*)\"{re.escape(old)}\"",
            rf'\1"{fresh}"', metadata, flags=re.S,
        )

    referenced = slot_refs(items)
    definitions = component_ids(items)
    unused = set(definitions) - referenced
    for cid in sorted(unused):
        audit.append((cid, "delete", "unreferenced component"))
    items, n = delete_placeobj_blocks(
        items, "ModItemWeaponComponent", lambda block: prop(block.text, "id") in unused
    )
    summary["unused_components_deleted"] += n

    items, n = delete_placeobj_blocks(
        items, "ModItemWeaponComponentEffect", lambda block: prop(block.text, "id") in DELETE_EFFECTS
    )
    summary["effects_deleted"] += n
    metadata, n = remove_resources(metadata, "WeaponComponentEffect", set(DELETE_EFFECTS))
    summary["effect_resources_deleted"] += n
    metadata, n = remove_resources(metadata, "WeaponComponent", unused)
    summary["component_resources_deleted"] += n
    metadata = add_close_resources(metadata)

    problems = validate(items)
    AUDIT.write_text(
        "component_id\taction\tdetails\n" + "".join("\t".join(row) + "\n" for row in audit),
        encoding="utf-8",
    )
    print(f"mode: {'apply' if apply else 'dry-run'}")
    for key in sorted(summary):
        print(f"{key}: {summary[key]}")
    print(f"audit: {AUDIT.relative_to(ROOT)} ({len(audit)} rows)")
    if problems:
        print("validation failed:", file=sys.stderr)
        print("\n".join(f" - {problem}" for problem in problems), file=sys.stderr)
        return 1
    if not apply:
        return 0

    atomic_write(ITEMS, items)
    atomic_write(METADATA, metadata)
    for path, content in companions.items():
        if content != path.read_text(encoding="utf-8"):
            atomic_write(path, content)
    for old, fresh in rename.items():
        for folder in (ROOT / "Icons/Upgrades/Chips", ROOT / "Icons/Upgrades/Full"):
            source, target = folder / f"{old}.png", folder / f"{fresh}.png"
            if source.exists() and not target.exists():
                source.rename(target)
                summary["icons_renamed"] += 1
    for cid in unused:
        for folder in (ROOT / "Icons/Upgrades/Chips", ROOT / "Icons/Upgrades/Full"):
            path = folder / f"{cid}.png"
            if path.exists():
                path.unlink()
                summary["unused_icons_deleted"] += 1
    print("apply completed; .bak backups were written beside changed Lua files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
