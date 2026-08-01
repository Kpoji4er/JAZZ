"""Wire APS MagNormal + BarrelNormal_Sil style-B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_MAG = "Mod/e6L4ECj/WeaponComponents/Magazine/APS_Mag18.png"
ICON_SIL = "Mod/e6L4ECj/WeaponComponents/Barrel/APS_BarrelSil.png"

MAG_BLOCK = (
    "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "APS",\n'
    '\t\t\t\t\t\t\t\tEntity = "",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON_MAG}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),\n"
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")

    # MagNormal insert
    end = text.find('id = "JAZZ_MagNormal"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if 'ApplyTo = "APS"' in body and "APS_Mag18" in body:
        print("Mag already")
    else:
        needle = (
            "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\tApplyTo = "Scorpion",'
        )
        i = body.find(needle)
        if i < 0:
            needle = (
                "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
                '\t\t\t\t\t\t\t\tApplyTo = "FiveSeven",'
            )
            i = body.find(needle)
        if i < 0:
            raise SystemExit("mag insert missing")
        body = body[:i] + MAG_BLOCK + body[i:]
        print("Mag ok")
    text = text[:start] + body + rest

    # BarrelNormal_Sil Visual Icon
    end = text.find('id = "JAZZ_BarrelNormal_Sil"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    old = (
        'ApplyTo = "APS",\n'
        '\t\t\t\t\t\t\t\tEntity = "APSBarrelSilencer",\n'
        '\t\t\t\t\t\t\t\tSlot = "Barrel",'
    )
    new = (
        'ApplyTo = "APS",\n'
        '\t\t\t\t\t\t\t\tEntity = "APSBarrelSilencer",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_SIL}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Barrel",'
    )
    if ICON_SIL in body:
        print("Sil already")
    elif old not in body:
        raise SystemExit("sil needle missing")
    else:
        body = body.replace(old, new, 1)
        print("Sil ok")
    # also upgrade component Icon if still vanilla
    head, _, vis = body.partition("Visuals")
    if 'Icon = "UI/Icons/Upgrades/default_barrel"' in head:
        head = head.replace(
            'Icon = "UI/Icons/Upgrades/default_barrel"',
            f'Icon = "{ICON_SIL}"',
            1,
        )
        body = head + "Visuals" + vis
        print("comp Icon ok")
    text = text[:start] + body + rest

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
