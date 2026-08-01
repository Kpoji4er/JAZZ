"""Insert MagNormal Visual ApplyTo=PPS43 → Magazine/PPS43_Mag35.png.

PPS43 has no Magazine slot; Visual for future base-mag icons.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/PPS43_Mag35.png"
MARKER = 'id = "JAZZ_MagNormal"'
BLOCK = (
    "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "PPS43",\n'
    '\t\t\t\t\t\t\t\tEntity = "",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Magazine",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),\n"
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if 'ApplyTo = "PPS43"' in body and "PPS43_Mag35" in body:
        print("already")
    else:
        needle = (
            "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
            '\t\t\t\t\t\t\t\tApplyTo = "Sterling",'
        )
        i = body.find(needle)
        if i < 0:
            needle = (
                "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
                '\t\t\t\t\t\t\t\tApplyTo = "M3GreaseGun",'
            )
            i = body.find(needle)
        if i < 0:
            raise SystemExit("insert point missing")
        body = body[:i] + BLOCK + body[i:]
        print("ok")
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
