#!/usr/bin/env python3
"""Sync Affiliation=MERC into jazz-units/items.lua ModItemUnitDataCompositeDef blocks."""
from __future__ import annotations

import re
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
IDS = [
    "Jazz_Flo",
    "Jazz_Cougar",
    "Jazz_Madman",
    "Jazz_Blade",
    "Jazz_Conrad",
    "Jazz_Dynamo",
    "Jazz_Gaston",
    "Jazz_Nervous",
    "Jazz_Ricochet",
    "Jazz_Cord",
    "Jazz_Hobbit",
    "Jazz_Horg",
    "Jazz_Meat",
    "Jazz_Shank",
    "Jazz_Biff",
    "Larry",
    "Larry_Clean",
    "Smiley",
]


def patch_block(text: str, unit_id: str) -> tuple[str, bool]:
    # Find id = "UnitId" inside a PlaceObj and patch Affiliation nearby (within 4k chars)
    needle = f'id = "{unit_id}"'
    idx = text.find(needle)
    if idx < 0:
        print("missing in items", unit_id)
        return text, False
    start = text.rfind("PlaceObj(", 0, idx)
    if start < 0:
        return text, False
    # find matching close for this PlaceObj roughly by next PlaceObj at same indent — use brace walk from (
    open_paren = text.find("(", start)
    depth = 0
    i = open_paren
    in_str = False
    str_ch = ""
    escape = False
    end = None
    while i < len(text):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == str_ch:
                in_str = False
        else:
            if ch in ("'", '"'):
                in_str = True
                str_ch = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1
    if end is None:
        raise RuntimeError(f"unclosed PlaceObj {unit_id}")
    block = text[start:end]
    if re.search(r'Affiliation\s*=\s*"MERC"', block):
        print("ok items", unit_id)
        return text, False
    if re.search(r"Affiliation\s*=", block):
        block2, n = re.subn(
            r'Affiliation\s*=\s*"[^"]*"',
            'Affiliation = "MERC"',
            block,
            count=1,
        )
        if n != 1:
            raise RuntimeError(unit_id)
        print("replaced items", unit_id)
    else:
        # insert after id line
        block2 = re.sub(
            rf'(id = "{re.escape(unit_id)}",)',
            r'\1\n\t\t\tAffiliation = "MERC",',
            block,
            count=1,
        )
        if block2 == block:
            raise RuntimeError(f"insert failed {unit_id}")
        print("inserted items", unit_id)
    return text[:start] + block2 + text[end:], True


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    changed = False
    for uid in IDS:
        text, ch = patch_block(text, uid)
        changed = changed or ch
    if changed:
        ITEMS.write_text(text, encoding="utf-8")
        print("wrote", ITEMS)
    else:
        print("no items.lua changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
