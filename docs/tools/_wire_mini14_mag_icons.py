"""Wire Mini14 MagNormal (20) + MagLarge_20_30_MINI14 (30) Style B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON20 = "Mod/e6L4ECj/WeaponComponents/Magazine/Mini14_Mag20.png"
ICON30 = "Mod/e6L4ECj/WeaponComponents/Magazine/Mini14_Mag30.png"


def patch_component(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if new in body and old not in body:
        print(label, "already")
        return text
    if old not in body:
        print(label, "needle missing")
        return text
    print(label, "ok")
    return text[:start] + body.replace(old, new, 1) + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = patch_component(
        text,
        'id = "JAZZ_MagNormal"',
        'ApplyTo = "Mini14",\n'
        '\t\t\t\t\t\t\t\tEntity = "Mini14_Small_Mag",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/M14_magazine",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "Mini14",\n'
        '\t\t\t\t\t\t\t\tEntity = "Mini14_Small_Mag",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON20}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagNormal",
    )
    text = patch_component(
        text,
        'id = "JAZZ_MagLarge_20_30_MINI14"',
        'Icon = "UI/Icons/Upgrades/galil_magazine_large",',
        f'Icon = "{ICON30}",',
        "MagLarge comp Icon",
    )
    text = patch_component(
        text,
        'id = "JAZZ_MagLarge_20_30_MINI14"',
        'ApplyTo = "Mini14",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "Mini14_Large_Mag",\n'
        '\t\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/expanded_M14_magazine",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "Mini14",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "Mini14_Large_Mag",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagLarge Visual",
    )

    inv_marker = "'Id', \"JAZZ_MagLarge_20_30_MINI14\""
    inv_pos = text.find(inv_marker)
    if inv_pos >= 0:
        inv_start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, inv_pos)
        inv_end = text.find("}),", inv_pos)
        chunk = text[inv_start:inv_end]
        # remountable often uses expanded_M14 or galil large
        for old_inv in (
            "'Icon', \"UI/Icons/Upgrades/expanded_M14_magazine\",",
            "'Icon', \"UI/Icons/Upgrades/galil_magazine_large\",",
            "'Icon', \"UI/Icons/Upgrades/M14_magazine\",",
        ):
            if ICON30 in chunk:
                print("Inv MagLarge already")
                break
            if old_inv in chunk:
                text = (
                    text[:inv_start]
                    + chunk.replace(old_inv, f"'Icon', \"{ICON30}\",", 1)
                    + text[inv_end:]
                )
                print("Inv MagLarge ok")
                break
        else:
            if ICON30 not in chunk:
                print("Inv MagLarge needle missing")

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
