"""Wire TMP MagNormal/MagSmall + HolsterBelt Style B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON30 = "Mod/e6L4ECj/WeaponComponents/Magazine/TMP_Mag30.png"
ICON15 = "Mod/e6L4ECj/WeaponComponents/Magazine/TMP_Mag15.png"
ICON_BELT = "Mod/e6L4ECj/WeaponComponents/Misc/JAZZ_HolsterBelt.png"


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
        'ApplyTo = "TMP",\n'
        '\t\t\t\t\t\t\t\tEntity = "TMP_Normal_Mag",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/M14_magazine",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "TMP",\n'
        '\t\t\t\t\t\t\t\tEntity = "TMP_Normal_Mag",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagNormal",
    )

    text = patch_component(
        text,
        'id = "JAZZ_MagSmall30_15_TMP"',
        'Icon = "UI/Icons/Upgrades/mp5_mag_normal",',
        f'Icon = "{ICON15}",',
        "MagSmall comp Icon",
    )
    text = patch_component(
        text,
        'id = "JAZZ_MagSmall30_15_TMP"',
        'ApplyTo = "TMP",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "TMP_Small_Mag",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "TMP",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "TMP_Small_Mag",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagSmall Visual",
    )

    # remountable MagSmall30_15_TMP
    inv_marker = "'Id', \"JAZZ_MagSmall30_15_TMP\""
    inv_pos = text.find(inv_marker)
    if inv_pos >= 0:
        inv_start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, inv_pos)
        inv_end = text.find("}),", inv_pos)
        chunk = text[inv_start:inv_end]
        old_inv = "'Icon', \"UI/Icons/Upgrades/mp5_mag_normal\","
        new_inv = f"'Icon', \"{ICON15}\","
        if ICON15 in chunk:
            print("Inv MagSmall already")
        elif old_inv in chunk:
            text = text[:inv_start] + chunk.replace(old_inv, new_inv, 1) + text[inv_end:]
            print("Inv MagSmall ok")
        else:
            print("Inv MagSmall needle missing")

    # HolsterBelt component Icon (broken belt.png) + TMP Visual Icon
    text = patch_component(
        text,
        'id = "JAZZ_HolsterBelt"',
        'Icon = "Mod/e6L4ECj/WeaponComponents/belt.png",',
        f'Icon = "{ICON_BELT}",',
        "Belt comp Icon",
    )
    text = patch_component(
        text,
        'id = "JAZZ_HolsterBelt"',
        'ApplyTo = "TMP",\n'
        '\t\t\t\t\t\t\tEntity = "TMP_Holster",\n'
        '\t\t\t\t\t\t\tSlot = "General",',
        'ApplyTo = "TMP",\n'
        '\t\t\t\t\t\t\tEntity = "TMP_Holster",\n'
        f'\t\t\t\t\t\t\tIcon = "{ICON_BELT}",\n'
        '\t\t\t\t\t\t\tSlot = "General",',
        "Belt TMP Visual",
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
