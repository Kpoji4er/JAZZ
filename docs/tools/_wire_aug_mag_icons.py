"""Wire AUG magazine Style B Icons: Mag30 / Mag42 / MagQuick."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON30 = "Mod/e6L4ECj/WeaponComponents/Magazine/AUG_Mag30.png"
ICON42 = "Mod/e6L4ECj/WeaponComponents/Magazine/AUG_Mag42.png"
ICONQ = "Mod/e6L4ECj/WeaponComponents/Magazine/AUG_MagQuick.png"


def patch_comp(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing marker")
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


def patch_inv(text: str, inv_id: str, old_icon: str, new_icon: str, label: str) -> str:
    marker = f"'Id', \"{inv_id}\""
    pos = text.find(marker)
    if pos < 0:
        print(label, "inv missing")
        return text
    start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, pos)
    end = text.find("}),", pos)
    chunk = text[start:end]
    old = f"'Icon', \"{old_icon}\","
    new = f"'Icon', \"{new_icon}\","
    if new_icon in chunk and old_icon not in chunk:
        print(label, "already")
        return text
    if old not in chunk:
        print(label, "needle missing", chunk[chunk.find("'Icon'") : chunk.find("'Icon'") + 80])
        return text
    print(label, "ok")
    return text[:start] + chunk.replace(old, new, 1) + text[end:]


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")

    text = patch_comp(
        text,
        'id = "JAZZ_MagNormal"',
        'ApplyTo = "AUG",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineSteyr_01",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/steyr_AUG_magazine",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "AUG",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineSteyr_01",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagNormal Visual",
    )

    text = patch_comp(
        text,
        'id = "JAZZ_MagLarge_30_42"',
        'Icon = "UI/Icons/Upgrades/galil_magazine_large",',
        f'Icon = "{ICON42}",',
        "MagLarge comp Icon",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_MagLarge_30_42"',
        'ApplyTo = "AUG",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineSteyr_02",\n'
        '\t\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/expanded_steyr_AUG_magazine",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "AUG",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineSteyr_02",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON42}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagLarge Visual",
    )

    text = patch_comp(
        text,
        'id = "JAZZ_MagQuick_AUG"',
        'Icon = "UI/Icons/Upgrades/galil_magazine_quick",',
        f'Icon = "{ICONQ}",',
        "MagQuick comp Icon",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_MagQuick_AUG"',
        'ApplyTo = "AUG",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineSteyr_03",\n'
        '\t\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/steyr_AUG_magazine",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "AUG",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineSteyr_03",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICONQ}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagQuick Visual",
    )

    text = patch_inv(
        text,
        "JAZZ_MagLarge_30_42",
        "UI/Icons/Upgrades/expanded_steyr_AUG_magazine",
        ICON42,
        "Inv MagLarge",
    )
    text = patch_inv(
        text,
        "JAZZ_MagQuick_AUG",
        "UI/Icons/Upgrades/galil_magazine_quick",
        ICONQ,
        "Inv MagQuick",
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
