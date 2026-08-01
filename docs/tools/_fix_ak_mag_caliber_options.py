# -*- coding: utf-8 -*-
"""Split AK magazine options by caliber: 7.62 vs 5.45.

Union wrongly put MagLarge_30_45 (5.45 bakelite 45) on AKM/AK47 and
MagLarge_30_40 (7.62 expanded 40) on AK74. Fix AvailableComponents on
companions + items.lua ModItems; trim MagLarge_30_45 AK47 visual remnant.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
ITEMS = ROOT / "items.lua"
sys.path.insert(0, str(ROOT / "docs" / "tools"))
from _apply_attach_001 import placeobj_blocks, prop
from _union_mag_family_options import replace_mag_options

# 7.62×39 mag well
AK762 = {
    "AK47",
    "AKM",
    "Type56",
    "RPK",
    "Zastava_M70",
    "ZastavaM92",
}
# 5.45×39 mag well
AK545 = {
    "AK74",
    "AKSU",
    "RPK74",
    "AN94",
}

# Shared across both (factory + quick — quick stays AK-family for now)
SHARED = ["JAZZ_MagNormal", "JAZZ_MagQuick_AK"]

OPTS_762 = SHARED + [
    "JAZZ_MagLarge_30_40",
    "JAZZ_MagDrum_30_75",
]
OPTS_545 = SHARED + [
    "JAZZ_MagLarge_30_45",
]

DEFAULT_762 = {
    "RPK": "JAZZ_MagLarge_30_40",
}
DEFAULT_545 = {
    "RPK74": "JAZZ_MagLarge_30_45",
}


def set_default(text: str, default_id: str) -> str:
    return re.sub(
        r"('DefaultComponent',\s*\")[^\"]+(\")",
        rf"\1{default_id}\2",
        text,
        count=1,
    )


def patch_weapon_file(path: Path, opts: list[str], default: str | None) -> bool:
    text = path.read_text(encoding="utf-8")
    new = replace_mag_options(text, opts)
    if new is None:
        print("WARN no mag slot", path.name)
        return False
    if default:
        # only replace DefaultComponent inside Magazine slot roughly:
        # after AvailableComponents we just wrote — safer full-file first DefaultComponent in mag context
        m = re.search(
            r"'SlotType',\s*\"Magazine\".*?('DefaultComponent',\s*\")[^\"]+(\")",
            new,
            flags=re.S,
        )
        if m:
            new = new[: m.start(1)] + f"'DefaultComponent', \"{default}\"" + new[m.end(2) :]
    if new == text:
        return False
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


def patch_items_moditem(items: str, weapon_id: str, opts: list[str], default: str | None) -> str:
    for b in placeobj_blocks(items, "ModItemInventoryItemCompositeDef"):
        if prop(b.text, "Id") != weapon_id:
            continue
        new_block = replace_mag_options(b.text, opts)
        if new_block is None:
            return items
        if default:
            m = re.search(
                r"'SlotType',\s*\"Magazine\".*?('DefaultComponent',\s*\")[^\"]+(\")",
                new_block,
                flags=re.S,
            )
            if m:
                new_block = (
                    new_block[: m.start(1)]
                    + f"'DefaultComponent', \"{default}\""
                    + new_block[m.end(2) :]
                )
        if new_block != b.text:
            items = items[: b.start] + new_block + items[b.end :]
        return items
    print("WARN no ModItem", weapon_id)
    return items


def remove_ak47_from_mag45(items: str) -> str:
    """Drop ApplyTo=AK47 visual from MagLarge_30_45 (wrong caliber)."""
    for b in placeobj_blocks(items, "ModItemWeaponComponent"):
        if prop(b.text, "id") != "JAZZ_MagLarge_30_45":
            continue
        new = re.sub(
            r"\s*PlaceObj\('WeaponComponentVisual',\s*\{"
            r"[^}]*ApplyTo\s*=\s*\"AK47\"[^}]*\}\),",
            "\n",
            b.text,
            flags=re.S,
        )
        if new != b.text:
            return items[: b.start] + new + items[b.end :]
        return items
    return items


def main() -> int:
    apply = "--apply" in sys.argv
    plan: list[tuple[str, list[str], str | None]] = []
    for w in sorted(AK762):
        plan.append((w, OPTS_762, DEFAULT_762.get(w, "JAZZ_MagNormal")))
    for w in sorted(AK545):
        plan.append((w, OPTS_545, DEFAULT_545.get(w, "JAZZ_MagNormal")))

    for w, opts, default in plan:
        print(f"{w}: {opts} default={default}")

    if not apply:
        print("dry-run; pass --apply")
        return 0

    n = 0
    for w, opts, default in plan:
        path = INV / f"{w}.lua"
        if path.exists() and patch_weapon_file(path, opts, default):
            n += 1
            print("companion", w)

    items = ITEMS.read_text(encoding="utf-8")
    for w, opts, default in plan:
        items = patch_items_moditem(items, w, opts, default)
    items = remove_ak47_from_mag45(items)

    tmp = ITEMS.with_suffix(".lua.tmp_ak_caliber")
    tmp.write_text(items, encoding="utf-8")
    tmp.replace(ITEMS)

    from _validate_items_quick import check
    from _lupa_load_items import try_load2

    problems = check(ITEMS) + check(ROOT / "metadata.lua")
    if problems:
        print("FAIL validate", problems)
        return 1
    err = try_load2(ITEMS)
    if err and "syntax" in err.lower():
        print("FAIL lupa", err)
        return 1
    print(f"OK companions={n}; items+validate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
