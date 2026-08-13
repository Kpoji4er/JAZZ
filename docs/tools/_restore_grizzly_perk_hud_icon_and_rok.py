# -*- coding: utf-8 -*-
"""Restore GrizzlyPerk hotbar to stock HUD icon + recharge_on_kill=1.

HOTFIX-006 had rewired CombatAction.Icon to Perks/SignatureAbilities/GrizzlyPerk.png
and left recharge_on_kill off. Owner: keep vanilla Hud glyph; CD clears after 1 kill.

Run from jazz root:
  python docs/tools/_restore_grizzly_perk_hud_icon_and_rok.py
  python docs/tools/_validate_items_quick.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

STOCK_ICON = "UI/Icons/Hud/perk_grizzly_perk"
MOD_ICON = "Mod/e6L4ECj/Perks/SignatureAbilities/GrizzlyPerk.png"

ROK_BLOCK = """\t\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t\t'Name', "recharge_on_kill",
\t\t\t\t\t\t\t'Value', 1,
\t\t\t\t\t\t\t'Tag', "<recharge_on_kill>",
\t\t\t\t\t\t}),
"""


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    pat = re.compile(
        r"(PlaceObj\('ModItemCombatAction',\s*\{(?:(?!PlaceObj\('ModItemCombatAction').)*?"
        r'id = "GrizzlyPerk"\s*,?\s*\}\),)',
        re.S,
    )
    m = pat.search(text)
    if not m:
        print("FAIL: GrizzlyPerk CombatAction not found")
        return 1
    block = m.group(1)
    new_block = block.replace(f'Icon = "{MOD_ICON}"', f'Icon = "{STOCK_ICON}"')
    new_block = new_block.replace(
        f'Icon = "{STOCK_ICON}"', f'Icon = "{STOCK_ICON}"'
    )  # idempotent if already stock
    if 'Icon = "UI/Icons/Hud/perk_grizzly_perk"' not in new_block:
        # force whatever Icon line
        new_block, n = re.subn(
            r'Icon = "[^"]+"',
            f'Icon = "{STOCK_ICON}"',
            new_block,
            count=1,
        )
        if not n:
            print("FAIL: Icon line missing in GrizzlyPerk CA")
            return 1
    if "'Name', \"recharge_on_kill\"" not in new_block:
        # insert before closing of Parameters = { ... },
        new_block2, n = re.subn(
            r"(Parameters = \{)(.*?)(\n\t\t\t\t\t\},)",
            lambda mm: mm.group(1) + mm.group(2) + "\n" + ROK_BLOCK + mm.group(3),
            new_block,
            count=1,
            flags=re.S,
        )
        if not n:
            print("FAIL: could not insert recharge_on_kill")
            return 1
        new_block = new_block2
    if new_block == block:
        print("OK: already restored")
        return 0
    text = text[: m.start(1)] + new_block + text[m.end(1) :]
    tmp = ITEMS.with_suffix(".lua.tmp_grizzly")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(ITEMS)
    print("OK: GrizzlyPerk Icon=stock HUD, recharge_on_kill=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
