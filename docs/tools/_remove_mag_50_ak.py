# -*- coding: utf-8 -*-
"""Remove JAZZ_MagLarge_50_AK — AK expanded mag is MagLarge_30_40 (40 rounds)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CID = "JAZZ_MagLarge_50_AK"

def strip_from_available(text: str) -> str:
    # Only strip quoted ids that appear as AvailableComponents list entries
    # (indented string lines), not 'Id', "..." ModItem fields.
    text = re.sub(rf'(?m)^\s*"{re.escape(CID)}",?\s*\n', "", text)
    return text


def remove_placeobj_by_id(text: str, cls: str, oid: str) -> str:
    from _apply_attach_001 import placeobj_blocks, prop

    blocks = placeobj_blocks(text, cls)
    for b in reversed(blocks):
        if (prop(b.text, "Id") or prop(b.text, "id")) == oid:
            # also drop trailing comma/newline before
            start = b.start
            end = b.end
            # include trailing comma
            if end < len(text) and text[end] == ",":
                end += 1
            while end < len(text) and text[end] in "\r\n":
                end += 1
            text = text[:start] + text[end:]
    return text


def main() -> None:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _apply_attach_001 import placeobj_blocks, prop

    inv = ROOT / "InventoryItem"
    for path in inv.glob("*.lua"):
        t = path.read_text(encoding="utf-8")
        if CID not in t:
            continue
        if path.name == f"{CID}.lua":
            continue
        path.write_text(strip_from_available(t), encoding="utf-8", newline="\n")
        print("stripped options", path.name)

    items = ROOT / "items.lua"
    it = items.read_text(encoding="utf-8")
    it = strip_from_available(it)
    it = remove_placeobj_by_id(it, "ModItemWeaponComponent", CID)
    it = remove_placeobj_by_id(it, "ModItemInventoryItemCompositeDef", CID)
    items.write_text(it, encoding="utf-8", newline="\n")
    print("items.lua cleaned")

    meta = ROOT / "metadata.lua"
    mt = meta.read_text(encoding="utf-8")
    mt = re.sub(rf'\s*"InventoryItem/{re.escape(CID)}\.lua",\n', "\n", mt)
    # remove ModResourcePreset blocks with this Id
    mt = re.sub(
        rf"\s*PlaceObj\('ModResourcePreset',\s*\{{[^}}]*'Id',\s*\"{re.escape(CID)}\"[^}}]*\}}\),",
        "\n",
        mt,
        flags=re.S,
    )
    meta.write_text(mt, encoding="utf-8", newline="\n")
    print("metadata cleaned")

    companion = inv / f"{CID}.lua"
    if companion.exists():
        companion.unlink()
        print("deleted", companion.name)

    # hint on MagLarge_30_40 inventory
    p40 = inv / "JAZZ_MagLarge_30_40.lua"
    if p40.exists():
        t = p40.read_text(encoding="utf-8")
        if "Семья магазинов: AK" not in t:
            t = t.replace(
                "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации.",
                "Семья магазинов: AK (вкл. РПК). Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации.",
            )
            p40.write_text(t, encoding="utf-8", newline="\n")
            print("updated MagLarge_30_40 hint")


if __name__ == "__main__":
    main()
