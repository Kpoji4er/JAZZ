"""Add MagNormal Visual Icon for Colt1911 (+ Kimber) style-B 1911 mag."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/Colt1911_MagNormal.png"
MARKER = 'id = "JAZZ_MagNormal"'

COLT_BLOCK = (
    "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "Colt1911",\n'
    '\t\t\t\t\t\t\t\tEntity = "",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),\n"
)

KIMBER_OLD = (
    'ApplyTo = "Kimber",\n'
    '\t\t\t\t\t\t\t\tEntity = "KimberMag",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",'
)
KIMBER_NEW = (
    'ApplyTo = "Kimber",\n'
    '\t\t\t\t\t\t\t\tEntity = "KimberMag",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",'
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]

    if 'ApplyTo = "Colt1911"' in body:
        print("Colt1911 already in MagNormal")
    else:
        # insert before Kimber block if present, else before M2Carbine / closing
        anchor = 'ApplyTo = "Kimber",\n\t\t\t\t\t\t\t\tEntity = "KimberMag"'
        if anchor in body:
            body = body.replace(
                "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n\t\t\t\t\t\t\t\t" + anchor,
                COLT_BLOCK + "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n\t\t\t\t\t\t\t\t" + anchor,
                1,
            )
            print("Colt1911 inserted before Kimber")
        else:
            raise SystemExit("no Kimber anchor")

    if ICON.split("/")[-1] in body and 'Entity = "KimberMag"' in body and f'Icon = "{ICON}"' in body:
        # may already have Kimber icon
        pass
    if KIMBER_OLD in body:
        body = body.replace(KIMBER_OLD, KIMBER_NEW, 1)
        print("Kimber icon ok")
    elif f'Icon = "{ICON}"' in body and "KimberMag" in body:
        print("Kimber already")
    else:
        print("Kimber skip")

    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
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
