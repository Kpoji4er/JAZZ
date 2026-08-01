# -*- coding: utf-8 -*-
"""Hide fold-only Stock slots (Modifiable=false) on weapons.

A Stock slot is fold-only when AvailableComponents is exactly the LightFold
pair: JAZZ_StockLightFolded + JAZZ_StockLightUnFolded (any order).
Weapons that also offer StockNormal/Heavy/NoStock are left alone.

Patches InventoryItem companions + matching ModItemInventoryItemCompositeDef
in items.lua.

Usage:
  python docs/tools/_hide_fold_only_stock_slots.py           # dry-run
  python docs/tools/_hide_fold_only_stock_slots.py --apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
INV = ROOT / "InventoryItem"
sys.path.insert(0, str(ROOT / "docs" / "tools"))
from _apply_attach_001 import placeobj_blocks, prop

FOLD_PAIR = frozenset({"JAZZ_StockLightFolded", "JAZZ_StockLightUnFolded"})


def extract_available(body: str) -> list[str]:
    am = re.search(r"AvailableComponents['\"],\s*\{([^}]*)\}", body, re.S)
    if not am:
        return []
    return re.findall(r'"([^"]+)"', am.group(1))


def is_fold_only(comps: list[str]) -> bool:
    return set(comps) == FOLD_PAIR


def set_modifiable_false(slot_block: str) -> tuple[str, str]:
    """Return (new_block, action)."""
    if re.search(r"""['\"]Modifiable['\"],\s*false""", slot_block):
        return slot_block, "already"
    if re.search(r"""['\"]Modifiable['\"],\s*true""", slot_block):
        new = re.sub(
            r"""(['\"]Modifiable['\"],\s*)true""",
            r"\1false",
            slot_block,
            count=1,
        )
        return new, "flipped"
    # insert after SlotType line
    new, n = re.subn(
        r"""(['\"]SlotType['\"],\s*['\"]Stock['\"],)""",
        r"\1\n\t\t\t'Modifiable', false,",
        slot_block,
        count=1,
    )
    if n:
        return new, "inserted"
    return slot_block, "no-slottype"


def patch_stock_slots_in_text(text: str) -> tuple[str, int, list[str]]:
    changed = 0
    actions: list[str] = []

    def repl(m: re.Match) -> str:
        nonlocal changed
        block = m.group(0)
        body = m.group(1)
        st = re.search(r"""['\"]SlotType['\"],\s*['\"]([^'\"]+)['\"]""", body)
        if not st or st.group(1) != "Stock":
            return block
        comps = extract_available(body)
        if not is_fold_only(comps):
            return block
        new_body, action = set_modifiable_false(body)
        if action != "already" and new_body != body:
            changed += 1
            actions.append(action)
            return "PlaceObj('WeaponComponentSlot', {" + new_body + "}),"
        if action == "already":
            actions.append("already")
        return block

    new = re.sub(
        r"PlaceObj\('WeaponComponentSlot',\s*\{(.*?)\}\),",
        repl,
        text,
        flags=re.S,
    )
    return new, changed, actions


def main() -> int:
    apply = "--apply" in sys.argv
    companion_hits: list[tuple[Path, int]] = []
    for path in sorted(INV.rglob("*.lua")):
        text = path.read_text(encoding="utf-8")
        if "StockLightFolded" not in text and "StockLightUnFolded" not in text:
            continue
        new, n, actions = patch_stock_slots_in_text(text)
        if n or "already" in actions:
            # count fold-only even if already
            fold_n = sum(1 for a in actions if a in ("already", "inserted", "flipped"))
            if fold_n:
                print(f"companion {path.as_posix()}: {actions}")
            if n:
                companion_hits.append((path, n))
                if apply:
                    path.write_text(new, encoding="utf-8", newline="\n")

    # items.lua: only weapon ModItems that match fold-only
    items_text = ITEMS.read_text(encoding="utf-8")
    weapon_ids = {p.stem for p, _ in companion_hits}
    # also include already-modifiable-false companions for items sync
    for path in sorted(INV.rglob("*.lua")):
        text = path.read_text(encoding="utf-8")
        new, n, actions = patch_stock_slots_in_text(text)
        if any(a != "already" for a in actions) or (
            "already" in actions and is_fold_only_file(text)
        ):
            if "already" in actions and path.stem not in weapon_ids:
                # need items sync for already-hidden too if items still open
                weapon_ids.add(path.stem)

    # Simpler: patch all ModItemInventoryItemCompositeDef that contain fold-only stock
    items_changed = 0
    blocks = list(placeobj_blocks(items_text, "ModItemInventoryItemCompositeDef"))
    replacements: list[tuple[int, int, str]] = []
    for b in blocks:
        new_block, n, actions = patch_stock_slots_in_text(b.text)
        if n:
            items_changed += n
            replacements.append((b.start, b.end, new_block))
            wid = prop(b.text, "Id") or prop(b.text, "id") or "?"
            print(f"items.lua {wid}: {actions}")

    print(f"companions to write: {len(companion_hits)}")
    print(f"items.lua slots patched: {items_changed}")

    if not apply:
        print("dry-run; pass --apply")
        return 0

    if items_changed:
        parts = []
        cursor = 0
        for start, end, repl in sorted(replacements):
            parts.append(items_text[cursor:start])
            parts.append(repl)
            cursor = end
        parts.append(items_text[cursor:])
        tmp = ITEMS.with_suffix(".lua.tmp_fold_stock")
        tmp.write_text("".join(parts), encoding="utf-8")
        tmp.replace(ITEMS)

    from _validate_items_quick import check

    problems = check(ITEMS) + check(ROOT / "metadata.lua")
    if problems:
        print("FAIL validate")
        for p in problems:
            print(" -", p)
        return 1
    print("OK wrote + validated")
    return 0


def is_fold_only_file(text: str) -> bool:
    for m in re.finditer(
        r"PlaceObj\('WeaponComponentSlot',\s*\{(.*?)\}\),", text, re.S
    ):
        body = m.group(1)
        st = re.search(r"""['\"]SlotType['\"],\s*['\"]([^'\"]+)['\"]""", body)
        if st and st.group(1) == "Stock" and is_fold_only(extract_available(body)):
            return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
