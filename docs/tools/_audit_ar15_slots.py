"""Read-only audit of the AR15 family component slots (JAZZ-WEAPON-AR15-FAMILY-001).

Checks, for M16A1/M16A2/M16A4/M4A1/CAR15:
  1. slot sets in items.lua and in the generated companion InventoryItem/<Id>.lua match;
  2. every referenced component exists as a ModItemWeaponComponent with the same Slot;
  3. every DefaultComponent is listed in its own AvailableComponents.

Run from the jazz package root: python docs/tools/_audit_ar15_slots.py
Exit 0 = OK, 1 = mismatch.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
COMPANIONS = ROOT / "InventoryItem"
WEAPONS = ["M16A1", "M16A2", "M16A4", "M4A1", "CAR15"]

slot_open = re.compile(r"PlaceObj\('WeaponComponentSlot',\s*\{")
slot_type = re.compile(r"'SlotType',\s*\"([^\"]+)\"")
default_re = re.compile(r"'DefaultComponent',\s*\"([^\"]+)\"")
comp_re = re.compile(r"\"([A-Za-z0-9_]+)\"")
flag_re = re.compile(r"'(CanBeEmpty|Modifiable)',\s*(true|false)")


def parse_slots(text: str) -> dict[str, dict]:
    """Parse WeaponComponentSlot blocks out of a ComponentSlots body."""
    slots: dict[str, dict] = {}
    for m in slot_open.finditer(text):
        depth = 0
        i = m.end() - 1
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        body = text[m.end() : i]
        st = slot_type.search(body)
        if not st:
            continue
        avail_start = body.find("'AvailableComponents'")
        avail = []
        if avail_start >= 0:
            brace = body.find("{", avail_start)
            end = body.find("}", brace)
            avail = comp_re.findall(body[brace:end])
        slots[st.group(1)] = {
            "components": avail,
            "default": (default_re.search(body).group(1) if default_re.search(body) else None),
            "flags": {k: v for k, v in flag_re.findall(body)},
        }
    return slots


def moditem_body(text: str, weapon: str) -> str:
    anchor = text.find(f"'Id', \"{weapon}\",")
    if anchor < 0:
        raise SystemExit(f"items.lua: ModItem {weapon} not found")
    cs = text.find("'ComponentSlots', {", anchor)
    if cs < 0:
        raise SystemExit(f"items.lua: {weapon} has no ComponentSlots")
    depth = 0
    i = text.find("{", cs)
    start = i
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return text[start : i + 1]


def components_index(text: str) -> dict[str, str]:
    """Map component id -> declared Slot."""
    index: dict[str, str] = {}
    for block in text.split("PlaceObj('ModItemWeaponComponent'")[1:]:
        cid = re.search(r'^\s*id = "([^"]+)",\s*$', block, re.M)
        if not cid:
            continue
        head = block[: cid.end()]
        slot = re.search(r"Slot = \"([^\"]+)\"", head)
        index[cid.group(1)] = slot.group(1) if slot else "?"
    return index


def main() -> int:
    items_text = ITEMS.read_text(encoding="utf-8", errors="replace")
    comps = components_index(items_text)
    problems: list[str] = []

    for weapon in WEAPONS:
        from_items = parse_slots(moditem_body(items_text, weapon))
        companion = COMPANIONS / f"{weapon}.lua"
        if not companion.is_file():
            problems.append(f"{weapon}: companion {companion.name} missing")
            continue
        ctext = companion.read_text(encoding="utf-8", errors="replace")
        cs = ctext.find("ComponentSlots = {")
        from_comp = parse_slots(ctext[cs:]) if cs >= 0 else {}

        if set(from_items) != set(from_comp):
            problems.append(
                f"{weapon}: slot sets differ. items={sorted(from_items)} companion={sorted(from_comp)}"
            )
        for slot in sorted(set(from_items) & set(from_comp)):
            a, b = from_items[slot], from_comp[slot]
            if a["components"] != b["components"]:
                problems.append(f"{weapon}.{slot}: components differ {a['components']} vs {b['components']}")
            if a["default"] != b["default"]:
                problems.append(f"{weapon}.{slot}: default differs {a['default']} vs {b['default']}")
            if a["flags"] != b["flags"]:
                problems.append(f"{weapon}.{slot}: flags differ {a['flags']} vs {b['flags']}")

        for slot, data in sorted(from_items.items()):
            for cid in data["components"]:
                if cid not in comps:
                    problems.append(f"{weapon}.{slot}: component {cid} is not a ModItemWeaponComponent")
                elif comps[cid] != slot:
                    problems.append(
                        f"{weapon}.{slot}: component {cid} declares Slot={comps[cid]}"
                    )
            if data["default"] and data["default"] not in data["components"]:
                problems.append(
                    f"{weapon}.{slot}: default {data['default']} not in AvailableComponents"
                )

        flags = {s: d["flags"] for s, d in from_items.items() if d["flags"]}
        print(f"{weapon}: slots={sorted(from_items)}")
        for slot, data in sorted(from_items.items()):
            print(f"    {slot:<10} default={data['default']} n={len(data['components'])}"
                  + (f" flags={flags[slot]}" if slot in flags else ""))

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("\nPASS: AR15 family slots consistent between items.lua and companions; components resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
