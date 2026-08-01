"""Wire UZI MagDrum + StockLight UnFolded (and Folded same icon) style-B."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_DRUM = "Mod/e6L4ECj/WeaponComponents/Magazine/UZI_MagDrum.png"
ICON_STOCK = "Mod/e6L4ECj/WeaponComponents/Stock/UZI_Stock.png"


def patch(text: str, marker: str, old: str, new: str, label: str, all_occ: bool = False) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if new in body:
        print(label, "already")
        return text
    if old not in body:
        print(label, "needle missing")
        return text
    n = body.count(old) if all_occ else 1
    body = body.replace(old, new) if all_occ else body.replace(old, new, 1)
    print(label, f"ok x{n}" if all_occ else "ok")
    return text[:start] + body + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    # Drum — replace magpictures Thompson drum on MagDrum_30_50_UZI
    text = patch(
        text,
        'id = "JAZZ_MagDrum_30_50_UZI"',
        'Icon = "Mod/e6L4ECj/magpictures/Thompsondrum.png"',
        f'Icon = "{ICON_DRUM}"',
        "Drum",
        all_occ=True,
    )
    text = patch(
        text,
        'id = "JAZZ_StockLightUnFolded"',
        'ApplyTo = "UZI",\n'
        '\t\t\t\t\t\t\t\tEntity = "UziUnflStock",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "UZI",\n'
        '\t\t\t\t\t\t\t\tEntity = "UziUnflStock",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_STOCK}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        "UnFolded",
    )
    text = patch(
        text,
        'id = "JAZZ_StockLightFolded"',
        'ApplyTo = "UZI",\n'
        '\t\t\t\t\t\t\t\tEntity = "UzifldStock",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        'ApplyTo = "UZI",\n'
        '\t\t\t\t\t\t\t\tEntity = "UzifldStock",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_STOCK}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Stock",',
        "Folded",
    )
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
