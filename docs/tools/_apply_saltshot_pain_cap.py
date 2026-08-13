# -*- coding: utf-8 -*-
"""HOTFIX-007: saltshot AppliedEffects → Pain; companions + items.lua.

Runtime fill-to-cap lives in Systems_Medicine.lua (JazzTrySaltshotPain).
This script only syncs AppliedEffects / cut-content AdditionalHint text.

Run from jazz root:
  python docs/tools/_apply_saltshot_pain_cap.py
  python docs/tools/_validate_items_quick.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
COMPANIONS = (
    ROOT / "InventoryItem" / "JAZZ_AMMO_12gauge_Saltshot.lua",
    ROOT / "InventoryItem" / "_12gauge_Saltshot.lua",
)

OLD_COMPOUND = "HeadshotTorsoshotArmsshotLegsshot"
OLD_LIST = '"Headshot",\n\t\t\t\t\t\t\t"Torsoshot",\n\t\t\t\t\t\t\t"Armsshot",\n\t\t\t\t\t\t\t"Legsshot",'
NEW_LIST = '"Pain",'
HINT_OLD = "Вызывает у цели <color EmStyle>случайные травмы</color>"
HINT_NEW = "Сразу заполняет <color EmStyle>боль</color> до капа"


def patch_companion(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = text.replace(f'"{OLD_COMPOUND}"', '"Pain"')
    text = text.replace(HINT_OLD, HINT_NEW)
    # four-line AppliedEffects list (items-style in companion unlikely)
    text = re.sub(
        r'AppliedEffects = \{\s*"Headshot",\s*"Torsoshot",\s*"Armsshot",\s*"Legsshot",\s*\}',
        'AppliedEffects = {\n\t\t"Pain",\n\t}',
        text,
    )
    if text == orig:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def patch_items() -> bool:
    text = ITEMS.read_text(encoding="utf-8")
    orig = text
    # JAZZ + cut salt AppliedEffects blocks
    text = re.sub(
        r"('Id', \"(?:JAZZ_AMMO_12gauge_Saltshot|_12gauge_Saltshot)\".*?'AppliedEffects', \{\s*)"
        r'(?:"Headshot",\s*"Torsoshot",\s*"Armsshot",\s*"Legsshot",|"Pain",|"'
        + OLD_COMPOUND
        + r'")(\s*\},)',
        r'\1"Pain",\2',
        text,
        flags=re.S,
    )
    text = text.replace(HINT_OLD, HINT_NEW)
    if text == orig:
        return False
    tmp = ITEMS.with_suffix(".lua.tmp_salt")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(ITEMS)
    return True


def main() -> int:
    n = 0
    for p in COMPANIONS:
        if patch_companion(p):
            print(f"patched {p.relative_to(ROOT)}")
            n += 1
        else:
            print(f"ok {p.relative_to(ROOT)}")
    if patch_items():
        print("patched items.lua")
        n += 1
    else:
        print("ok items.lua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
