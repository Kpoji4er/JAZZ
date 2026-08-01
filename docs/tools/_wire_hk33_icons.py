"""Wire HK33 Style B: Mag30, MagDrum, Handguards; fix default Handguard entity."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_MAG = "Mod/e6L4ECj/WeaponComponents/Magazine/HK33_Mag30.png"
ICON_DRUM = "Mod/e6L4ECj/WeaponComponents/Magazine/HK33_MagDrum.png"
ICON_HG = "Mod/e6L4ECj/WeaponComponents/Handguard/JAZZ_HK33Handguard.png"
ICON_HG_MOD = "Mod/e6L4ECj/WeaponComponents/Handguard/JAZZ_HK33HandguardMod.png"


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
        print(label, "needle missing")
        return text
    print(label, "ok")
    return text[:start] + chunk.replace(old, new, 1) + text[end:]


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")

    # Fix default handguard: wrong Entity HK_33_Lower / Slot General → HandGuardStock / Handguard
    text = patch_comp(
        text,
        'id = "JAZZ_HK33Handguard"',
        'Icon = "UI/Icons/Upgrades/default_handguard",',
        f'Icon = "{ICON_HG}",',
        "HG comp Icon",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_HK33Handguard"',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\tEntity = "HK_33_Lower",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/AK47_default_handguard",\n'
        '\t\t\t\t\t\t\t\tSlot = "General",',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\tEntity = "HK33_HandGuardStock",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_HG}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handguard",',
        "HG Visual fix",
    )

    text = patch_comp(
        text,
        'id = "JAZZ_HK33HandguardMod"',
        'Icon = "UI/Icons/Upgrades/default_handguard",',
        f'Icon = "{ICON_HG_MOD}",',
        "HGMod comp Icon",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_HK33HandguardMod"',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\tEntity = "HK33_HandGuardMod",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/AK47_default_handguard",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handguard",',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\tEntity = "HK33_HandGuardMod",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_HG_MOD}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handguard",',
        "HGMod Visual",
    )

    text = patch_comp(
        text,
        'id = "JAZZ_MagNormal"',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\tEntity = "HK33_MagDef",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\tEntity = "HK33_MagDef",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_MAG}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagNormal Visual",
    )

    text = patch_comp(
        text,
        'id = "JAZZ_MagDrum_30_100_HK33"',
        'Icon = "UI/Icons/Upgrades/galil_magazine_large",',
        f'Icon = "{ICON_DRUM}",',
        "Drum comp Icon",
    )
    text = patch_comp(
        text,
        'id = "JAZZ_MagDrum_30_100_HK33"',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "HK_33_Drum",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "HK33",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "HK_33_Drum",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON_DRUM}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "Drum Visual",
    )

    text = patch_inv(
        text,
        "JAZZ_MagDrum_30_100_HK33",
        "UI/Icons/Upgrades/galil_magazine_large",
        ICON_DRUM,
        "Inv Drum",
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
