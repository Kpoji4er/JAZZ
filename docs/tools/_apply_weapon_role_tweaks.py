#!/usr/bin/env python3
"""Apply owner role tweaks: FAMAS / Agram2000 / Sig550* / PSG1.

Updates InventoryItem companions, matching ModItem blocks in items.lua,
and docs/technical/weapons/data/weapons.csv. Default dry-run; --apply writes.
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
CSV_PATH = ROOT / "docs/technical/weapons/data/weapons.csv"

# companion path -> property updates (Lua bare style)
COMPANION_PROPS: dict[str, dict[str, object]] = {
    "InventoryItem/FAMAS.lua": {
        "ShootAP": 5000,
    },
    "InventoryItem/Agram2000.lua": {
        "Damage": 22,
        "AimAccuracy": 8,
        "WeaponRange": 20,
        "Recoil": 16,
        "CloseRange": 0,
        "CloseRangeFactor": 115,
        "Grouping": 82,
        "CritChanceScaled": 20,
    },
    "InventoryItem/Sig550.lua": {
        "ShootAP": 5000,
        "AimAccuracy": 16,
    },
    "InventoryItem/Sig550Custom.lua": {
        "ShootAP": 5000,
        "AimAccuracy": 16,
    },
    "InventoryItem/PSG1.lua": {
        "AimAccuracy": 22,
        "CritChanceScaled": 45,
        "Recoil": 18,
        "Grouping": 58,
        "MaxAimActions": 4,
    },
}

# CSV column updates by weapon id
CSV_PROPS: dict[str, dict[str, object]] = {
    "FAMAS": {"shoot_ap": 5000},
    "Agram2000": {
        "damage": 22,
        "aim_accuracy": 8,
        "weapon_range": 20,
        "recoil": 16,
        "close_range": 0,
        "close_range_factor": 115,
        "grouping": 82,
        "crit_chance_scaled": 20,
    },
    "Sig550": {"shoot_ap": 5000, "aim_accuracy": 16},
    "Sig550Custom": {"shoot_ap": 5000, "aim_accuracy": 16},
    "PSG1": {
        "aim_accuracy": 22,
        "crit_chance_scaled": 45,
        "recoil": 18,
        "grouping": 58,
        "max_aim_actions": 4,
    },
}

SIG550_SIDE_SLOT = """\
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_FlashlightOff",
				"JAZZ_LaserDot",
				"JAZZ_FlashlightDot",
				"JAZZ_UVDot",
			},
		}),
"""

SIG550_SIDE_SLOT_ITEMS = """\
						PlaceObj('WeaponComponentSlot', {
							'SlotType', "Side",
							'CanBeEmpty', true,
							'AvailableComponents', {
								"JAZZ_Flashlight",
								"JAZZ_FlashlightOff",
								"JAZZ_LaserDot",
								"JAZZ_FlashlightDot",
								"JAZZ_UVDot",
							},
						}),
"""


def set_lua_prop(text: str, key: str, value: object, placeobj: bool) -> str:
    if isinstance(value, str):
        rendered = f'"{value}"'
    else:
        rendered = str(value)
    if placeobj:
        pattern = rf"(['\"]{re.escape(key)}['\"]\s*,\s*)([^,\n]+)"
        repl = rf"\g<1>{rendered}"
    else:
        pattern = rf"(\b{re.escape(key)}\s*=\s*)([^,\n]+)"
        repl = rf"\g<1>{rendered}"
    new, n = re.subn(pattern, repl, text, count=1)
    if n == 0:
        # insert near ShootAP / Recoil / CloseRange block
        anchor = re.search(
            r"(\n\s*(?:ShootAP|Recoil|CloseRange|AimAccuracy|Grouping)\s*=)",
            text,
        )
        if not anchor:
            raise RuntimeError(f"cannot set {key}={value}")
        indent = "\t"
        insertion = f"\n{indent}{key} = {rendered},"
        new = text[: anchor.start()] + insertion + text[anchor.start() :]
    return new


def set_placeobj_prop(block: str, key: str, value: object) -> str:
    if isinstance(value, str):
        rendered = f'"{value}"'
    else:
        rendered = str(value)
    pattern = rf"('{re.escape(key)}',\s*)([^,\n]+)"
    new, n = re.subn(pattern, rf"\g<1>{rendered}", block, count=1)
    if n == 0:
        # insert before CloseRange or after AutoShots if present
        m = re.search(r"\n(\s*)'CloseRange'", block)
        if not m:
            m = re.search(r"\n(\s*)'WeaponResource'", block)
        if not m:
            raise RuntimeError(f"cannot insert {key} in items block")
        indent = m.group(1)
        insertion = f"\n{indent}'{key}', {rendered},"
        new = block[: m.start()] + insertion + block[m.start() :]
    return new


def extract_moditem(items: str, weapon_id: str) -> tuple[int, int, str]:
    marker = f"'Id', \"{weapon_id}\""
    start = items.find(marker)
    if start < 0:
        raise RuntimeError(f"ModItem {weapon_id} not found")
    # walk back to PlaceObj('ModItemInventoryItemCompositeDef'
    p = items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, start)
    if p < 0:
        raise RuntimeError(f"PlaceObj start for {weapon_id} not found")
    # find matching end: next sibling PlaceObj at same indent after this block's closing
    # Use brace/paren balance from p
    i = p + len("PlaceObj(")
    depth = 1
    while i < len(items) and depth:
        ch = items[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        i += 1
    # include trailing comma/newline if present
    end = i
    if end < len(items) and items[end] == ",":
        end += 1
    return p, end, items[p:end]


def apply_companion(path: Path, props: dict[str, object], write: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    orig = text
    notes = []
    for key, value in props.items():
        before = text
        text = set_lua_prop(text, key, value, placeobj=False)
        if text != before:
            notes.append(f"{path.name}: {key}={value}")
    if path.name == "Sig550.lua" and "SlotType', \"Side\"" not in text:
        m = re.search(r"\n(\t)\},\n\tHolsterSlot = ", text)
        if not m:
            raise RuntimeError("Sig550 companion: cannot find ComponentSlots close")
        # Insert Side inside ComponentSlots, before its closing },
        text = (
            text[: m.start()]
            + "\n"
            + SIG550_SIDE_SLOT.rstrip("\n")
            + "\n"
            + m.group(1)
            + "},\n\tHolsterSlot = "
            + text[m.end() :]
        )
        notes.append("Sig550.lua: +Side slot")
    if write and text != orig:
        bak = path.with_suffix(path.suffix + ".bak_role_tweaks")
        if not bak.exists():
            shutil.copy2(path, bak)
        path.write_text(text, encoding="utf-8", newline="\n")
    return notes


def apply_items(write: bool) -> list[str]:
    text = ITEMS.read_text(encoding="utf-8")
    orig = text
    notes: list[str] = []
    id_to_props = {
        "FAMAS": COMPANION_PROPS["InventoryItem/FAMAS.lua"],
        "Agram2000": COMPANION_PROPS["InventoryItem/Agram2000.lua"],
        "Sig550": COMPANION_PROPS["InventoryItem/Sig550.lua"],
        "Sig550Custom": COMPANION_PROPS["InventoryItem/Sig550Custom.lua"],
        "PSG1": COMPANION_PROPS["InventoryItem/PSG1.lua"],
    }
    for wid, props in id_to_props.items():
        start, end, block = extract_moditem(text, wid)
        new_block = block
        for key, value in props.items():
            new_block = set_placeobj_prop(new_block, key, value)
        if wid == "Sig550" and "'SlotType', \"Side\"" not in new_block:
            m = re.search(
                r"\n(\t\t\t\t\t)\},\n\t\t\t\t\t'HolsterSlot',", new_block
            )
            if not m:
                raise RuntimeError("Sig550 items: ComponentSlots close not found")
            new_block = (
                new_block[: m.start()]
                + "\n"
                + SIG550_SIDE_SLOT_ITEMS.rstrip("\n")
                + "\n"
                + m.group(1)
                + "},\n\t\t\t\t\t'HolsterSlot',"
                + new_block[m.end() :]
            )
            notes.append("items.lua Sig550: +Side slot")
        if new_block != block:
            text = text[:start] + new_block + text[end:]
            notes.append(f"items.lua {wid}: props updated")
    if write and text != orig:
        bak = ITEMS.with_suffix(ITEMS.suffix + ".bak_role_tweaks")
        if not bak.exists():
            shutil.copy2(ITEMS, bak)
        ITEMS.write_text(text, encoding="utf-8", newline="\n")
    return notes


def apply_csv(write: bool) -> list[str]:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8", newline="")))
    fieldnames = list(rows[0].keys()) if rows else []
    notes = []
    for row in rows:
        wid = row["id"]
        if wid not in CSV_PROPS:
            continue
        for k, v in CSV_PROPS[wid].items():
            old = row.get(k)
            row[k] = str(v)
            if old != row[k]:
                notes.append(f"csv {wid}.{k}: {old} -> {v}")
        # Sig550 component_slot_count bump if we added Side
        if wid == "Sig550":
            try:
                n = int(row.get("component_slot_count") or 0)
                if n == 6:
                    row["component_slot_count"] = "7"
                    notes.append("csv Sig550.component_slot_count: 6 -> 7")
            except ValueError:
                pass
            try:
                o = int(row.get("component_option_count") or 0)
                # +5 side options
                row["component_option_count"] = str(o + 5)
                notes.append(f"csv Sig550.component_option_count: {o} -> {o+5}")
            except ValueError:
                pass
    if write:
        bak = CSV_PATH.with_suffix(CSV_PATH.suffix + ".bak_role_tweaks")
        if not bak.exists():
            shutil.copy2(CSV_PATH, bak)
        with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return notes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    write = args.apply
    notes: list[str] = []
    for rel, props in COMPANION_PROPS.items():
        notes.extend(apply_companion(ROOT / rel, props, write))
    notes.extend(apply_items(write))
    notes.extend(apply_csv(write))
    mode = "APPLY" if write else "DRY"
    print(f"[{mode}] {len(notes)} changes")
    for n in notes:
        print(" ", n)


if __name__ == "__main__":
    main()
