"""Wire MAC10 MagNormal + StockLight Folded/UnFolded style-B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_MAG = "Mod/e6L4ECj/WeaponComponents/Magazine/MAC10_Mag30.png"
ICON_STOCK = "Mod/e6L4ECj/WeaponComponents/Stock/MAC10_Stock.png"


def component_body(text: str, marker: str) -> tuple[int, int, str]:
    end = text.find(marker)
    if end < 0:
        raise SystemExit(f"missing {marker}")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    return start, end, text[start:end]


def patch_mag(text: str) -> str:
    start, end, body = component_body(text, 'id = "JAZZ_MagNormal"')
    old = (
        'ApplyTo = "MAC10",\n'
        '\t\t\t\t\t\t\t\tEntity = "MAC10mag",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",'
    )
    new = (
        'ApplyTo = "MAC10",\n'
        '\t\t\t\t\t\t\t\tEntity = "MAC10mag",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_MAG}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",'
    )
    count = body.count(old)
    if count == 0:
        if ICON_MAG in body:
            print("Mag already")
            return text
        print("Mag needle missing")
        return text
    body = body.replace(old, new)  # all duplicates in MagNormal
    print(f"Mag ok x{count}")
    return text[:start] + body + text[end:]


def patch_stock(text: str, marker: str, entity: str, label: str) -> str:
    start, end, body = component_body(text, marker)
    old = (
        'ApplyTo = "MAC10",\n'
        f'\t\t\t\t\t\t\t\tEntity = "{entity}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",'
    )
    new = (
        'ApplyTo = "MAC10",\n'
        f'\t\t\t\t\t\t\t\tEntity = "{entity}",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_STOCK}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",'
    )
    if new in body or (ICON_STOCK in body and entity in body):
        print(label, "already")
        return text
    if old not in body:
        print(label, "needle missing")
        return text
    print(label, "ok")
    return text[:start] + body.replace(old, new, 1) + text[end:]


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = patch_mag(text)
    text = patch_stock(text, 'id = "JAZZ_StockLightFolded"', "MAC10FldStock", "Folded")
    text = patch_stock(text, 'id = "JAZZ_StockLightUnFolded"', "MAC10UnfldStock", "UnFolded")
    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    for _ in range(25):
        try:
            os.replace(tmp, ITEMS)
            print("done")
            return
        except OSError:
            time.sleep(0.3)
    raise SystemExit("locked")


if __name__ == "__main__":
    main()
