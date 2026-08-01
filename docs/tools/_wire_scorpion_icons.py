"""Wire Scorpion MagNormal + StockLight Folded/UnFolded style-B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_MAG = "Mod/e6L4ECj/WeaponComponents/Magazine/Scorpion_Mag20.png"
ICON_STOCK = "Mod/e6L4ECj/WeaponComponents/Stock/Scorpion_Stock.png"

MAG_BLOCK = (
    "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "Scorpion",\n'
    '\t\t\t\t\t\t\t\tEntity = "",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON_MAG}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),\n"
)


def patch_stock(text: str, marker: str, entity: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    old = (
        'ApplyTo = "Scorpion",\n'
        f'\t\t\t\t\t\t\t\tEntity = "{entity}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",'
    )
    new = (
        'ApplyTo = "Scorpion",\n'
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
    return text[:start] + body.replace(old, new, 1) + rest


def patch_mag(text: str) -> str:
    marker = 'id = "JAZZ_MagNormal"'
    end = text.find(marker)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if 'ApplyTo = "Scorpion"' in body and "Scorpion_Mag20" in body:
        print("Mag already")
        return text
    needle = (
        "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
        '\t\t\t\t\t\t\t\tApplyTo = "FiveSeven",'
    )
    i = body.find(needle)
    if i < 0:
        needle = (
            "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\tApplyTo = "Colt1911",'
        )
        i = body.find(needle)
    if i < 0:
        raise SystemExit("mag insert point missing")
    print("Mag insert ok")
    return text[:start] + body[:i] + MAG_BLOCK + body[i:] + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = patch_mag(text)
    text = patch_stock(text, 'id = "JAZZ_StockLightFolded"', "ScorpionStockF", "Folded")
    text = patch_stock(text, 'id = "JAZZ_StockLightUnFolded"', "ScorpionStockU", "UnFolded")
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
