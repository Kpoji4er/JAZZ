# -*- coding: utf-8 -*-
"""Remove Freeswap WeaponComponentSlot from Handguns (pistols/revolvers/handgun autopistols).

Keeps Freeswap on SubmachineGuns that still use it (MP5K, MicroUZI, Scorpion).
Patches InventoryItem companions + matching ModItemInventoryItemCompositeDef in items.lua.
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


SLOT_RE = re.compile(
    r"PlaceObj\('WeaponComponentSlot',\s*\{.*?\}\),",
    re.S,
)


def is_freeswap_slot(block: str) -> bool:
    return bool(
        re.search(r"""['\"]SlotType['\"],\s*['\"]Freeswap['\"]""", block)
    )


def strip_freeswap_slots(text: str) -> tuple[str, int]:
    removed = 0

    def repl(m: re.Match) -> str:
        nonlocal removed
        if is_freeswap_slot(m.group(0)):
            removed += 1
            return ""
        return m.group(0)

    new = SLOT_RE.sub(repl, text)
    # collapse blank runs left by deleted slot blocks
    new = re.sub(r"\n{3,}", "\n\n", new)
    return new, removed


def handgun_companions() -> list[Path]:
    out = []
    for p in sorted(INV.rglob("*.lua")):
        t = p.read_text(encoding="utf-8")
        if not re.search(r"""['\"]SlotType['\"],\s*['\"]Freeswap['\"]""", t):
            continue
        cat = re.search(r'CategoryPair\s*=\s*"([^"]+)"', t)
        if not cat or cat.group(1) != "Handguns":
            continue
        out.append(p)
    return out


def patch_items_for_ids(text: str, weapon_ids: set[str]) -> tuple[str, int]:
    total = 0
    blocks = list(placeobj_blocks(text, "ModItemInventoryItemCompositeDef"))
    replacements: list[tuple[int, int, str]] = []
    for b in blocks:
        wid = prop(b.text, "Id") or prop(b.text, "id")
        if wid not in weapon_ids:
            continue
        new_block, n = strip_freeswap_slots(b.text)
        if n:
            total += n
            replacements.append((b.start, b.end, new_block))
    if not replacements:
        return text, 0
    parts = []
    cursor = 0
    for start, end, repl in sorted(replacements):
        parts.append(text[cursor:start])
        parts.append(repl)
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts), total


def main() -> int:
    apply = "--apply" in sys.argv
    companions = handgun_companions()
    weapon_ids = {p.stem for p in companions}
    print(f"handguns with Freeswap: {len(companions)}")
    for p in companions:
        print(" ", p.as_posix())

    companion_changes: list[tuple[Path, str, int]] = []
    for p in companions:
        old = p.read_text(encoding="utf-8")
        new, n = strip_freeswap_slots(old)
        if n:
            companion_changes.append((p, new, n))
            print(f"companion {p.name}: remove {n}")

    items_text = ITEMS.read_text(encoding="utf-8")
    new_items, items_n = patch_items_for_ids(items_text, weapon_ids)
    print(f"items.lua slots removed: {items_n}")

    if not apply:
        print("dry-run; pass --apply")
        return 0

    for p, new, _ in companion_changes:
        p.write_text(new, encoding="utf-8")
    if items_n:
        tmp = ITEMS.with_suffix(".lua.tmp_freeswap")
        tmp.write_text(new_items, encoding="utf-8")
        tmp.replace(ITEMS)

    from _validate_items_quick import check

    problems = check(ITEMS) + check(ROOT / "metadata.lua")
    if problems:
        print("FAIL validate")
        for pr in problems:
            print(" -", pr)
        return 1
    print("OK wrote companions + items.lua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
