"""Wire AK74 folding skeleton stock Icons."""
from __future__ import annotations

from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Stock/AK74_StockFold_v2.png"


def patch_comp(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing marker")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if f'Icon = "{ICON}"' in body and "AK74" in body and old.split("Entity")[1][:40] in body:
        # crude already-check
        pass
    if old not in body:
        print(label, "needle missing")
        return text
    if new in body:
        print(label, "already")
        return text
    print(label, "ok")
    return text[:start] + body.replace(old, new, 1) + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = patch_comp(
        text,
        'id = "JAZZ_StockLightUnFolded"',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\t\tEntity = "AK74Stockfld",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\t\tEntity = "AK74Stockfld",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        "StockLightUnFolded",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_StockLight"',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_StockAK74_01",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/ak74_stock_foldable",',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_StockAK74_01",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",',
        "StockLight",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_UnfoldStocks"',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\tEntity = "AK74StockUnFld",\n'
        '\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\tEntity = "AK74StockUnFld",\n'
        f'\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\tSlot = "Stock",',
        "UnfoldStocks",
    )
    # Same art for folded option until we have a distinct folded silhouette
    text = patch_comp(
        text,
        'id = "JAZZ_StockLightFolded"',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\t\tEntity = "AK74StockUnFld",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "AK74",\n'
        '\t\t\t\t\t\t\t\tEntity = "AK74StockUnFld",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        "StockLightFolded",
    )
    ITEMS.write_text(text, encoding="utf-8", newline="\n")
    print("done")


if __name__ == "__main__":
    main()
