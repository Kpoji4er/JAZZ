"""Wire MP5 MagNormal (30) + MagSmall30_15_MP5 (15) Style B Icons on all variants."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON30 = "Mod/e6L4ECj/WeaponComponents/Magazine/MP5_Mag30.png"
ICON15 = "Mod/e6L4ECj/WeaponComponents/Magazine/MP5_Mag15.png"


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

    # --- MagNormal: all five ApplyTo ---
    normal_replacements = [
        (
            "MP5",
            'ApplyTo = "MP5",\n'
            '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_01",\n'
            '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_normal",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5",\n'
            '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_01",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5K",
            'ApplyTo = "MP5K",\n'
            '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_02",\n'
            '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_large",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5K",\n'
            '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_02",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5A2",
            'ApplyTo = "MP5A2",\n'
            '\t\t\t\t\t\t\t\tEntity = "MP5Mag",\n'
            '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_normal",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5A2",\n'
            '\t\t\t\t\t\t\t\tEntity = "MP5Mag",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5A4",
            'ApplyTo = "MP5A4",\n'
            '\t\t\t\t\t\t\t\tEntity = "MP5MagV2",\n'
            '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_normal",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5A4",\n'
            '\t\t\t\t\t\t\t\tEntity = "MP5MagV2",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5SD",
            'ApplyTo = "MP5SD",\n'
            '\t\t\t\t\t\t\t\tEntity = "MP5MagV2",\n'
            '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_normal",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5SD",\n'
            '\t\t\t\t\t\t\t\tEntity = "MP5MagV2",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
    ]
    for name, old, new in normal_replacements:
        text = patch_component(text, 'id = "JAZZ_MagNormal"', old, new, f"MagNormal {name}")

    # --- MagSmall30_15_MP5: component Icon + visuals ---
    text = patch_component(
        text,
        'id = "JAZZ_MagSmall30_15_MP5"',
        'Icon = "UI/Icons/Upgrades/mp5_mag_normal",',
        f'Icon = "{ICON15}",',
        "MagSmall comp Icon",
    )
    small_replacements = [
        (
            "MP5K",
            'ApplyTo = "MP5K",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_01",\n'
            '\t\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_normal",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5K",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_01",\n'
            f'\t\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5A2",
            'ApplyTo = "MP5A2",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "MP5SmallMag",\n'
            '\t\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_quick",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5A2",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "MP5SmallMag",\n'
            f'\t\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5A4",
            'ApplyTo = "MP5A4",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "MP5SmallMag",\n'
            '\t\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_quick",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5A4",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "MP5SmallMag",\n'
            f'\t\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
        (
            "MP5SD",
            'ApplyTo = "MP5SD",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "MP5SmallMag",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
            'ApplyTo = "MP5SD",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "MP5SmallMag",\n'
            f'\t\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        ),
    ]
    for name, old, new in small_replacements:
        text = patch_component(
            text, 'id = "JAZZ_MagSmall30_15_MP5"', old, new, f"MagSmall {name}"
        )

    # Add missing ApplyTo MP5 visual (entity from MagQuick short mag)
    end = text.find('id = "JAZZ_MagSmall30_15_MP5"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if 'ApplyTo = "MP5"' in body:
        print("MagSmall MP5 already")
    else:
        needle = (
            "PlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\t\tApplyTo = "MP5K",'
        )
        insert = (
            "PlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\t\tApplyTo = "MP5",\n'
            '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineMP5_03",\n'
            f'\t\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
            '\t\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
            "\t\t\t\t\t\t\t\t\tparam_bindings = false,\n"
            "\t\t\t\t\t\t\t\t}),\n"
            "PlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\t\tApplyTo = "MP5K",'
        )
        if needle not in body:
            print("MagSmall MP5 insert needle missing")
        else:
            body = body.replace(needle, insert, 1)
            text = text[:start] + body + rest
            print("MagSmall MP5 inserted")

    # Remountable InventoryItem icon for MagSmall30_15_MP5
    inv_marker = "'Id', \"JAZZ_MagSmall30_15_MP5\""
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
    else:
        print("Inv MagSmall missing")

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
