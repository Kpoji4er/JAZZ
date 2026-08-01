# -*- coding: utf-8 -*-
"""Fix items.lua lone commas from PlaceObj deletions; revert empty visual stubs.

Writes via .tmp then replace (avoids locked-file Errno 22 when game holds items.lua).
"""
from __future__ import annotations

import re
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import placeobj_blocks, prop, rename_slots, remove_resources, atomic_write

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
INVENTORY = ROOT / "InventoryItem"

STUB_IDS = {
    "JAZZ_AKSU_Hanguard_Basic",
    "JAZZ_AUGCompensator_01",
    "JAZZ_AUGCompensator_03",
    "JAZZ_BarrelShort_Winchester",
    "JAZZ_DefaultMuzzle_HK21",
    "JAZZ_FNFAL_Handguard",
    "JAZZ_Galil_Handguard_Default",
    "JAZZ_MuzzleBooster_Glock18",
    "JAZZ_Compensator_cosmetic",
}
REVERT = {
    "JAZZ_AKSU_Hanguard_Basic": "AKSU_Hanguard_Basic",
    "JAZZ_AUGCompensator_01": "AUGCompensator_01",
    "JAZZ_AUGCompensator_03": "AUGCompensator_03",
    "JAZZ_BarrelShort_Winchester": "BarrelShort_Winchester",
    "JAZZ_DefaultMuzzle_HK21": "DefaultMuzzle_HK21",
    "JAZZ_FNFAL_Handguard": "FNFAL_Handguard",
    "JAZZ_Galil_Handguard_Default": "Galil_Handguard_Default",
    "JAZZ_MuzzleBooster_Glock18": "MuzzleBooster_Glock18",
    "JAZZ_Compensator_cosmetic": "Compensator_cosmetic",
}


def strip_lone_commas(text: str) -> tuple[str, int]:
    return re.subn(r"(?m)^[ \t]*,\s*\n", "", text)


def delete_placeobj_with_comma(text: str, cls: str, ids: set[str]) -> tuple[str, int]:
    removed = 0
    for block in reversed(placeobj_blocks(text, cls)):
        cid = prop(block.text, "id")
        if cid not in ids:
            continue
        end = block.end
        m = re.match(r"[ \t]*\,[ \t]*\n?", text[end:])
        if m:
            end = end + m.end()
        text = text[: block.start] + text[end:]
        removed += 1
    return text, removed


def write_retry(path: Path, content: str, attempts: int = 8) -> None:
    tmp = path.with_suffix(path.suffix + ".fix_tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    last_err = None
    for i in range(attempts):
        try:
            tmp.replace(path)
            return
        except OSError as err:
            last_err = err
            time.sleep(0.4 * (i + 1))
    # fallback copy
    try:
        path.write_text(content, encoding="utf-8", newline="\n")
        tmp.unlink(missing_ok=True)
        return
    except OSError:
        pass
    raise last_err  # type: ignore[misc]


def main() -> int:
    items = ITEMS.read_text(encoding="utf-8")
    items, n = strip_lone_commas(items)
    print(f"stripped lone commas={n}")

    items, n = rename_slots(items, REVERT)
    print(f"items slot refs reverted={n}")

    companions_changed = []
    for path in INVENTORY.rglob("*.lua"):
        text = path.read_text(encoding="utf-8")
        new, n_rev = rename_slots(text, REVERT)
        new, n_lone = strip_lone_commas(new)
        if n_rev or n_lone or new != text:
            companions_changed.append((path, new, n_rev, n_lone))
            if n_rev or n_lone:
                print(f" companion {path.name} reverted={n_rev} lone_commas={n_lone}")

    items, n = delete_placeobj_with_comma(items, "ModItemWeaponComponent", STUB_IDS)
    print(f"stub components deleted={n}")
    # strip again in case delete left holes
    items, n2 = strip_lone_commas(items)
    print(f"post-delete lone commas={n2}")

    meta = META.read_text(encoding="utf-8")
    meta, n = remove_resources(meta, "WeaponComponent", STUB_IDS)
    print(f"metadata stubs removed={n}")
    meta, n = strip_lone_commas(meta)
    print(f"metadata lone commas stripped={n}")

    print("writing items.lua ...")
    write_retry(ITEMS, items)
    print("writing metadata.lua ...")
    write_retry(META, meta)
    for path, new, *_ in companions_changed:
        write_retry(path, new)

    left_items = len(re.findall(r"(?m)^[ \t]*,\s*$", ITEMS.read_text(encoding="utf-8")))
    left_meta = len(re.findall(r"(?m)^[ \t]*,\s*$", META.read_text(encoding="utf-8")))
    print(f"remaining lone commas items={left_items} metadata={left_meta}")
    verify = ITEMS.read_text(encoding="utf-8")
    for sid in STUB_IDS:
        if f'id = "{sid}"' in verify:
            print("WARN still present", sid)
    return 0 if left_items == 0 and left_meta == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
