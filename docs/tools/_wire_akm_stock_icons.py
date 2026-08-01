"""Wire AKM wood + underfolder stock Icons (folded/unfolded share fold art)."""
from __future__ import annotations

from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
WOOD = "Mod/e6L4ECj/WeaponComponents/Stock/AKM_StockNormal.png"
FOLD = "Mod/e6L4ECj/WeaponComponents/Stock/AKM_StockFold.png"


def patch_comp(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing marker")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
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
        'id = "JAZZ_StockNormal"',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\t\tEntity = "AKMFullStock",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",\n'
        '\t\t\t\t\t\t\t\tWeaponName = "АКМ",',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\t\tEntity = "AKMFullStock",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{WOOD}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",\n'
        '\t\t\t\t\t\t\t\tWeaponName = "АКМ",',
        "StockNormal wood",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_StockLightUnFolded"',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\t\tEntity = "AKMUnfoldStock",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\t\tEntity = "AKMUnfoldStock",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{FOLD}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        "StockLightUnFolded",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_StockLightFolded"',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\t\tEntity = "AKMFoldStock",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",\n'
        '\t\t\t\t\t\t\t\tWeaponName = "АКМС",',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\t\tEntity = "AKMFoldStock",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{FOLD}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",\n'
        '\t\t\t\t\t\t\t\tWeaponName = "АКМС",',
        "StockLightFolded",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_UnfoldStocks"',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\tEntity = "AKMUnfoldStock",\n'
        '\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "AKM",\n'
        '\t\t\t\t\t\t\tEntity = "AKMUnfoldStock",\n'
        f'\t\t\t\t\t\t\tIcon = "{FOLD}",\n'
        '\t\t\t\t\t\t\tSlot = "Stock",',
        "UnfoldStocks",
    )
    ITEMS.write_text(text, encoding="utf-8", newline="\n")
    print("done")


if __name__ == "__main__":
    main()
