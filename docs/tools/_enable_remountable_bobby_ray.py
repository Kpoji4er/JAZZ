# -*- coding: utf-8 -*-
"""Enable remountable attachment InventoryItems in Bobby Ray (temporary shop pass).

Sets CanAppearInShop=true + RestockWeight/MaxStock/Tier on RemovableAttachments
companions and matching ModItems in items.lua.

Skips permanent/toggle junk: *SuppressorIntegrated, FlashlightOff.

Usage:
  python docs/tools/_enable_remountable_bobby_ray.py           # dry-run
  python docs/tools/_enable_remountable_bobby_ray.py --apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
INV = ROOT / "InventoryItem"

RESTOCK = 10
MAX_STOCK = 1
TIER = 1

SKIP_SUBSTRINGS = ("SuppressorIntegrated",)
SKIP_IDS = {
    "JAZZ_FlashlightOff",
    "JAZZ_RemovableAttachment",  # base class, not a sellable module
}


def should_skip(cid: str) -> bool:
    if cid in SKIP_IDS:
        return True
    for sub in SKIP_SUBSTRINGS:
        if sub in cid:
            return True
    return False


def is_remountable_companion(text: str) -> bool:
    return "RemovableComponentId" in text or (
        'object_class = "JAZZ_RemovableAttachment"' in text
        and "RemovableComponentId" in text
    )


def patch_companion(text: str) -> tuple[str, bool]:
    changed = False
    if re.search(r"CanAppearInShop\s*=\s*false", text):
        text = re.sub(r"CanAppearInShop\s*=\s*false", "CanAppearInShop = true", text, count=1)
        changed = True
    elif not re.search(r"CanAppearInShop\s*=", text):
        # insert after Cost or before CategoryPair
        if "CategoryPair" in text:
            text = text.replace(
                "\tCategoryPair",
                "\tCanAppearInShop = true,\n\tCategoryPair",
                1,
            )
            changed = True

    def ensure_prop(name: str, value: str) -> None:
        nonlocal text, changed
        pat = rf"{name}\s*="
        if re.search(pat, text):
            text2, n = re.subn(rf"{name}\s*=\s*[^,\n]+", f"{name} = {value}", text, count=1)
            if n and text2 != text:
                text = text2
                changed = True
        else:
            # after CanAppearInShop
            text2, n = re.subn(
                r"(CanAppearInShop\s*=\s*true,)",
                rf"\1\n\t{name} = {value},",
                text,
                count=1,
            )
            if n:
                text = text2
                changed = True

    ensure_prop("Tier", str(TIER))
    ensure_prop("MaxStock", str(MAX_STOCK))
    ensure_prop("RestockWeight", str(RESTOCK))
    return text, changed


def patch_moditem_block(block: str) -> tuple[str, bool]:
    """Patch one ModItemInventoryItemCompositeDef text for remountable shop flags."""
    changed = False
    if "'CanAppearInShop', false" in block:
        block = block.replace("'CanAppearInShop', false", "'CanAppearInShop', true", 1)
        changed = True
    elif "'CanAppearInShop', true" not in block:
        block = block.replace(
            "'CategoryPair', \"Components\",",
            "'CanAppearInShop', true,\n\t\t\t\t\t'CategoryPair', \"Components\",",
            1,
        )
        changed = True

    def ensure(key: str, value: str) -> None:
        nonlocal block, changed
        quoted = f"'{key}',"
        if quoted in block:
            block2, n = re.subn(
                rf"'{key}',\s*[^,\n]+",
                f"'{key}', {value}",
                block,
                count=1,
            )
            if n and block2 != block:
                block = block2
                changed = True
        else:
            block2, n = re.subn(
                r"('CanAppearInShop',\s*true,)",
                rf"\1\n\t\t\t\t\t'{key}', {value},",
                block,
                count=1,
            )
            if n:
                block = block2
                changed = True

    ensure("Tier", str(TIER))
    ensure("MaxStock", str(MAX_STOCK))
    ensure("RestockWeight", str(RESTOCK))
    return block, changed


def patch_items_lua(text: str) -> tuple[str, int]:
    begin = text.find("-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-BEGIN")
    end = text.find("-- JAZZ-WEAPONS-002-REMOVABLE-ITEMS-END")
    if begin < 0 or end < 0:
        print("WARN: remountable folder markers missing in items.lua")
        return text, 0
    section = text[begin:end]
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        block = m.group(0)
        idm = re.search(r"'Id',\s*\"([^\"]+)\"", block)
        if not idm:
            return block
        cid = idm.group(1)
        if should_skip(cid):
            return block
        new_block, ch = patch_moditem_block(block)
        if ch:
            count += 1
        return new_block

    new_section = re.sub(
        r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{.*?\}\),",
        repl,
        section,
        flags=re.S,
    )
    return text[:begin] + new_section + text[end:], count


def main() -> int:
    apply = "--apply" in sys.argv
    companion_n = 0
    skipped = []
    for path in sorted(INV.glob("JAZZ_*.lua")):
        text = path.read_text(encoding="utf-8")
        if "RemovableComponentId" not in text:
            continue
        cid = path.stem
        if should_skip(cid):
            skipped.append(cid)
            continue
        new, ch = patch_companion(text)
        if ch:
            companion_n += 1
            print(f"companion {cid}")
            if apply:
                path.write_text(new, encoding="utf-8", newline="\n")

    items_text = ITEMS.read_text(encoding="utf-8")
    new_items, items_n = patch_items_lua(items_text)
    print(f"companions patched: {companion_n}")
    print(f"items.lua remountables patched: {items_n}")
    print(f"skipped: {skipped}")

    if not apply:
        print("dry-run; pass --apply")
        return 0

    if items_n:
        tmp = ITEMS.with_suffix(".lua.tmp_bobby_attach")
        tmp.write_text(new_items, encoding="utf-8")
        tmp.replace(ITEMS)

    sys.path.insert(0, str(ROOT / "docs" / "tools"))
    from _validate_items_quick import check

    problems = check(ITEMS) + check(ROOT / "metadata.lua")
    if problems:
        print("FAIL validate")
        for p in problems:
            print(" -", p)
        return 1
    print("OK wrote + validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
