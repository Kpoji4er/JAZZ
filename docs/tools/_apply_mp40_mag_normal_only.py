# -*- coding: utf-8 -*-
"""MP40: only MagNormal (32). Drop MagLarge_50_MP40 from weapon/loot/catalog.

Owner: MP40 has a single fixed 32-round mag — no expanded family.

Writes:
  jazz/items.lua — MP40 slot; remove WeaponComponent + RemovableAttachment
  jazz/InventoryItem/MP40.lua — AvailableComponents
  jazz/metadata.lua — drop companion + InventoryItemCompositeDef resource
  jazz-units/items.lua — GenW MagLarge-only UpgradedWeapon → InventoryItem
Deletes:
  jazz/InventoryItem/JAZZ_MagLarge_50_MP40.lua

Does not touch Localization CSV (orphan T-ids harmless).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
MAG_ID = "JAZZ_MagLarge_50_MP40"


def atomic_write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_mp40_slot(text: str) -> tuple[str, int]:
    """Remove MagLarge from MP40 AvailableComponents (items ModItem + companion)."""
    n = 0

    def repl_items(m: re.Match[str]) -> str:
        nonlocal n
        block = m.group(0)
        if MAG_ID not in block:
            return block
        new = re.sub(
            rf',\s*\n\s*"{re.escape(MAG_ID)}"',
            "",
            block,
            count=1,
        )
        if new == block:
            new = re.sub(rf'"{re.escape(MAG_ID)}",\s*\n\s*', "", block, count=1)
        if new != block:
            n += 1
        return new

    # ModItemInventoryItemCompositeDef MP40 in items.lua
    text2, c1 = re.subn(
        r"(PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{[^\}]*?'Id',\s*\"MP40\".*?'AvailableComponents',\s*\{)(.*?)(\},)",
        lambda m: m.group(1)
        + re.sub(rf'[ \t]*"{re.escape(MAG_ID)}",?\r?\n', "", m.group(2))
        + m.group(3),
        text,
        count=1,
        flags=re.S,
    )
    if c1:
        n += c1
        text = text2
    else:
        # companion style: AvailableComponents block near MagazineSize = 32 Entity Weapon_MP40
        text2, c2 = re.subn(
            rf'("JAZZ_MagNormal",)\s*\n\s*"{re.escape(MAG_ID)}",',
            r"\1",
            text,
            count=1,
        )
        if c2:
            n += c2
            text = text2
    return text, n


def remove_placeobj_by_id(text: str, place_kind: str, id_key: str, id_value: str) -> tuple[str, int]:
    """Remove one PlaceObj('<place_kind>', { ... id ... }), by Id field."""
    # Match either 'Id', "X" or id = "X"
    id_pat = re.compile(
        rf"(?:'Id',\s*\"{re.escape(id_value)}\"|{re.escape(id_key)}\s*=\s*\"{re.escape(id_value)}\")"
    )
    needle = f"PlaceObj('{place_kind}'"
    pos = 0
    while True:
        m = id_pat.search(text, pos)
        if not m:
            return text, 0
        start = text.rfind(needle, 0, m.start())
        if start < 0:
            pos = m.end()
            continue
        i = text.find("{", start)
        depth = 0
        end = None
        for j in range(i, len(text)):
            ch = text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    break
        if end is None:
            return text, 0
        k = end
        while k < len(text) and text[k] in " \t\r\n":
            k += 1
        if text.startswith("),", k):
            end = k + 2
        return text[:start] + text[end:], 1


def remove_moditem_weaponcomponent(text: str, cid: str) -> tuple[str, int]:
    return remove_placeobj_by_id(text, "ModItemWeaponComponent", "id", cid)


def remove_moditem_inventory(text: str, iid: str) -> tuple[str, int]:
    return remove_placeobj_by_id(text, "ModItemInventoryItemCompositeDef", "Id", iid)


def strip_metadata(text: str, iid: str) -> tuple[str, int]:
    n = 0
    text2, c = re.subn(
        rf'\s*"InventoryItem/{re.escape(iid)}\.lua",\r?\n',
        "\n",
        text,
        count=1,
    )
    n += c
    text = text2
    text2, c = re.subn(
        rf"\s*PlaceObj\('ModResourcePreset',\s*\{{\s*'Class',\s*\"InventoryItemCompositeDef\",\s*'Id',\s*\"{re.escape(iid)}\",\s*'ClassDisplayName',\s*\"Inventory item\",\s*\}}\),",
        "",
        text,
        count=1,
    )
    n += c
    return text2, n


def convert_units_loot(text: str) -> tuple[str, int]:
    """UpgradedWeapon with sole MagLarge_50_MP40 → LootEntryInventoryItem."""
    pat = re.compile(
        r"PlaceObj\('LootEntryUpgradedWeapon',\s*\{\s*upgrades = \{\s*"
        + rf'"{re.escape(MAG_ID)}",\s*'
        + r"\},\s*weapon = \"MP40\",\s*\}\),",
        re.S,
    )
    repl = (
        "PlaceObj('LootEntryInventoryItem', {\n"
        "\t\t\t\t\t\t\titem = \"MP40\",\n"
        "\t\t\t\t\t\t\tstack_max = 1,\n"
        "\t\t\t\t\t\t\tstack_min = 1,\n"
        "\t\t\t\t\t\t}),"
    )
    text2, n = pat.subn(repl, text)
    return text2, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    items_path = JAZZ / "items.lua"
    mp40_path = JAZZ / "InventoryItem" / "MP40.lua"
    meta_path = JAZZ / "metadata.lua"
    units_path = UNITS / "items.lua"
    rem_path = JAZZ / "InventoryItem" / f"{MAG_ID}.lua"

    items = items_path.read_text(encoding="utf-8")
    mp40 = mp40_path.read_text(encoding="utf-8")
    meta = meta_path.read_text(encoding="utf-8")
    units = units_path.read_text(encoding="utf-8")

    items, n_slot_items = strip_mp40_slot(items)
    # fallback explicit for items ModItem AvailableComponents list
    if MAG_ID in items and '"MP40"' in items:
        items2, c = re.subn(
            rf'("JAZZ_MagNormal",)\s*\n\s*"{re.escape(MAG_ID)}",',
            r"\1",
            items,
            count=1,
        )
        if c:
            items = items2
            n_slot_items += c

    mp40, n_slot_comp = strip_mp40_slot(mp40)
    if MAG_ID in mp40:
        mp402, c = re.subn(
            rf'("JAZZ_MagNormal",)\s*\n\s*"{re.escape(MAG_ID)}",',
            r"\1",
            mp40,
            count=1,
        )
        mp40, n_slot_comp = mp402, n_slot_comp + c

    items, n_wc = remove_moditem_weaponcomponent(items, MAG_ID)
    items, n_inv = remove_moditem_inventory(items, MAG_ID)
    meta, n_meta = strip_metadata(meta, MAG_ID)
    units, n_loot = convert_units_loot(units)

    leftover_jazz = len(re.findall(MAG_ID, items)) + len(re.findall(MAG_ID, mp40)) + len(
        re.findall(MAG_ID, meta)
    )
    leftover_units = len(re.findall(MAG_ID, units))

    print(
        f"slot items={n_slot_items} companion={n_slot_comp} "
        f"WeaponComponent={n_wc} Removable={n_inv} metadata={n_meta} loot={n_loot}"
    )
    print(f"leftover MAG_ID jazz={leftover_jazz} units={leftover_units} rem_file={rem_path.exists()}")

    if leftover_jazz or leftover_units:
        print("WARNING: leftover references remain")
        for label, blob in (("items", items), ("mp40", mp40), ("meta", meta), ("units", units)):
            for m in re.finditer(rf".{{0,80}}{re.escape(MAG_ID)}.{{0,80}}", blob):
                print(f"  {label}: ...{m.group(0)}...")

    if not args.apply:
        print("dry-run only; pass --apply to write")
        return 0 if n_loot and n_wc else 1

    atomic_write(items_path, items)
    atomic_write(mp40_path, mp40)
    atomic_write(meta_path, meta)
    atomic_write(units_path, units)
    if rem_path.exists():
        rem_path.unlink()
        print(f"deleted {rem_path.name}")
    print("applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
