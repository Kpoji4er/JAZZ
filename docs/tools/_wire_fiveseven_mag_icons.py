"""Insert MagNormal Visual ApplyTo=FiveSeven → Magazine/FiveSeven_Mag20.png.

FiveSeven currently has no Magazine slot; Visual is for future MagNormal wiring
(base mag icons for all weapons). Entity empty — mag is in the grip mesh.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/FiveSeven_Mag20.png"
MARKER = 'id = "JAZZ_MagNormal"'

BLOCK = (
    "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "FiveSeven",\n'
    '\t\t\t\t\t\t\t\tEntity = "",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),\n"
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("missing MagNormal")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]

    if 'ApplyTo = "FiveSeven"' in body and "FiveSeven_Mag20" in body:
        print("already")
    elif 'ApplyTo = "FiveSeven"' in body:
        # upgrade Icon only
        old = (
            'ApplyTo = "FiveSeven",\n'
            '\t\t\t\t\t\t\t\tEntity = "",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",'
        )
        new = (
            'ApplyTo = "FiveSeven",\n'
            '\t\t\t\t\t\t\t\tEntity = "",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",'
        )
        if old in body:
            body = body.replace(old, new, 1)
            print("icon added")
        else:
            raise SystemExit("FiveSeven present but unexpected shape")
    else:
        # insert before Colt1911 MagNormal visual (or before MagNormal id close)
        needle = (
            "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\tApplyTo = "Colt1911",'
        )
        i = body.find(needle)
        if i < 0:
            raise SystemExit("Colt1911 MagNormal visual not found")
        body = body[:i] + BLOCK + body[i:]
        print("inserted before Colt1911")

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
