"""Insert MagNormal Visual ApplyTo=M1Garand → Magazine/M1Garand_Enbloc.png.

M1 Garand has no Magazine slot (en-bloc in action); Visual for Icon catalog.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/M1Garand_Enbloc.png"
MARKER = 'id = "JAZZ_MagNormal"'
BLOCK = (
    "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "M1Garand",\n'
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
    if 'ApplyTo = "M1Garand"' in body and "M1Garand_Enbloc" in body:
        print("already")
    else:
        for key in (
            'ApplyTo = "M16A2"',
            'ApplyTo = "M16A1"',
            'ApplyTo = "M14SAW"',
            'ApplyTo = "M3GreaseGun"',
            'ApplyTo = "M1A"',
            'ApplyTo = "FG42"',
        ):
            needle = (
                "\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {\n"
                f"\t\t\t\t\t\t\t\t{key},"
            )
            i = body.find(needle)
            if i >= 0:
                body = body[:i] + BLOCK + body[i:]
                print("ok near", key)
                break
        else:
            raise SystemExit("insert point missing")
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
