# -*- coding: utf-8 -*-
"""Promote 9 dangling vanilla_ref WeaponComponents → JAZZ_* with Visuals from Data.hpk."""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_attach_001 import (  # noqa: E402
    placeobj_blocks,
    prop,
    rename_slots,
    matching_paren,
)

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
INVENTORY = ROOT / "InventoryItem"
VANILLA = ROOT / ".tmp" / "data-extract" / "WeaponComponentSharedClass.lua"

OLD_IDS = [
    "AKSU_Hanguard_Basic",
    "AUGCompensator_01",
    "AUGCompensator_03",
    "BarrelShort_Winchester",
    "Compensator_cosmetic",
    "DefaultMuzzle_HK21",
    "FNFAL_Handguard",
    "Galil_Handguard_Default",
    "MuzzleBooster_Glock18",
]
RENAME = {old: f"JAZZ_{old}" for old in OLD_IDS}

# T-IDs for DisplayName comments (reuse vanilla numeric IDs where present; new ModItem comment)
TID = {
    "JAZZ_AKSU_Hanguard_Basic": 982641740201,
    "JAZZ_AUGCompensator_01": 982641740202,
    "JAZZ_AUGCompensator_03": 982641740203,
    "JAZZ_BarrelShort_Winchester": 982641740204,
    "JAZZ_Compensator_cosmetic": 982641740205,
    "JAZZ_DefaultMuzzle_HK21": 982641740206,
    "JAZZ_FNFAL_Handguard": 982641740207,
    "JAZZ_Galil_Handguard_Default": 982641740208,
    "JAZZ_MuzzleBooster_Glock18": 982641740209,
}


def write_retry(path: Path, content: str, attempts: int = 8) -> None:
    tmp = path.with_suffix(path.suffix + ".rename_tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    last = None
    for i in range(attempts):
        try:
            tmp.replace(path)
            return
        except OSError as err:
            last = err
            time.sleep(0.4 * (i + 1))
    path.write_text(content, encoding="utf-8", newline="\n")
    tmp.unlink(missing_ok=True)
    if last:
        pass


def extract_vanilla_block(text: str, old_id: str) -> str:
    needle = f'id = "{old_id}"'
    pos = text.find(needle)
    if pos < 0:
        raise SystemExit(f"missing vanilla id {old_id}")
    # walk back to PlaceObj('WeaponComponent'
    start = text.rfind("PlaceObj('WeaponComponent'", 0, pos)
    if start < 0:
        raise SystemExit(f"no PlaceObj start for {old_id}")
    # matching_paren expects index of '('
    paren = text.find("(", start)
    end = matching_paren(text, paren)
    # include trailing )\n
    block_end = end + 1
    if text[block_end : block_end + 1] == "\n":
        block_end += 1
    return text[start:block_end]


def to_moditem(block: str, new_id: str) -> str:
    # Strip StoreAsTable = true,
    block = re.sub(r"(?m)^\tStoreAsTable = true,\n", "", block)
    # WeaponComponent → ModItemWeaponComponent
    block = block.replace("PlaceObj('WeaponComponent'", "PlaceObj('ModItemWeaponComponent'", 1)
    # id
    old_id = new_id[len("JAZZ_") :]
    block = re.sub(rf'id = "{re.escape(old_id)}"', f'id = "{new_id}"', block, count=1)
    # DisplayName T comment
    tid = TID[new_id]
    block = re.sub(
        r"DisplayName = T\((\d+), --\[\[[^\]]+\]\]",
        f"DisplayName = T({tid}, --[[ModItemWeaponComponent {new_id} DisplayName]]",
        block,
        count=1,
    )
    # indent as nested ModItem (tabs used in items.lua WeaponComponent section: 4–5 tabs)
    # Existing comps use either 4 or 5 leading tabs inside return PlaceObj('ModItem...', { items = { ...
    # Mirror JAZZ_RPK74_Hanguard_Basic style: tab depth of surrounding = 4 tabs before PlaceObj
    lines = block.strip("\n").split("\n")
    # normalize: vanilla uses single tab; wrap with 4-tab indent for items.lua list
    out_lines = []
    for line in lines:
        if line.startswith("\t"):
            out_lines.append("\t\t\t\t" + line)  # +4
        elif line.strip() == "":
            out_lines.append("")
        else:
            out_lines.append("\t\t\t\t" + line)
    body = "\n".join(out_lines).rstrip()
    # Vanilla ends with `})`; ModItem list entry needs `}),`
    if body.endswith("})"):
        body = body[:-2] + "}),"
    elif body.endswith(")"):
        body = body[:-1] + "}),"
    return body + "\n"


def main() -> int:
    if not VANILLA.is_file():
        raise SystemExit(f"missing vanilla extract: {VANILLA}")

    vanilla = VANILLA.read_text(encoding="utf-8")
    items = ITEMS.read_text(encoding="utf-8")
    meta = META.read_text(encoding="utf-8")

    # Skip if already present
    for new_id in RENAME.values():
        if f'id = "{new_id}"' in items:
            print("already present", new_id)

    inserts = []
    for old in OLD_IDS:
        new_id = RENAME[old]
        if f'id = "{new_id}"' in items:
            continue
        raw = extract_vanilla_block(vanilla, old)
        inserts.append(to_moditem(raw, new_id))
        print("prepared", new_id)

    if inserts:
        anchor = items.find("PlaceObj('ModItemWeaponComponent'")
        if anchor < 0:
            raise SystemExit("no ModItemWeaponComponent anchor")
        # Prefer insert near other Specific comps — use first WeaponComponent as before
        blob = "".join(inserts)
        items = items[:anchor] + blob + items[anchor:]
        print("inserted", len(inserts), "blocks")

    items, n = rename_slots(items, RENAME)
    print("items slot renames", n)

    companions_changed = 0
    for path in INVENTORY.rglob("*.lua"):
        text = path.read_text(encoding="utf-8")
        new, n = rename_slots(text, RENAME)
        if n:
            write_retry(path, new)
            companions_changed += 1
            print("companion", path.relative_to(ROOT), n)

    # metadata resources
    for new_id in RENAME.values():
        if f"'Id', \"{new_id}\"" in meta:
            continue
        entry = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"WeaponComponent\",\n"
            f"\t\t\t'Id', \"{new_id}\",\n"
            "\t\t\t'ClassDisplayName', \"Weapon Component\",\n"
            "\t\t}),\n"
        )
        m = re.search(
            r"\t\tPlaceObj\('ModResourcePreset', \{\s*\n\t\t\t'Class', \"WeaponComponent\"",
            meta,
        )
        if not m:
            raise SystemExit("no metadata WeaponComponent anchor")
        meta = meta[: m.start()] + entry + meta[m.start() :]
        print("metadata+", new_id)

    write_retry(ITEMS, items)
    write_retry(META, meta)

    # verify
    verify = ITEMS.read_text(encoding="utf-8")
    for old, new in RENAME.items():
        if f'id = "{new}"' not in verify:
            print("FAIL missing def", new)
            return 1
        # old id as AvailableComponents string should be gone (except inside comments of DisplayName T)
        # count string refs in option lists
        old_refs = len(re.findall(rf'"{re.escape(old)}"', verify))
        if old_refs:
            print("WARN old string refs left in items.lua", old, old_refs)
        print("ok", new)
    print("companions_changed", companions_changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
