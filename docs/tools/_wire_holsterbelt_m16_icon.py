"""Ensure HolsterBelt MagVisual Icons for M16A1 + TMP (empty-slot ghost).

M16A1 Visual without Icon → ModifyWeaponDlg empty General slot is blank
(engine prefers matching ApplyTo Visual.Icon over component.Icon).
Also documents removal of stray M16A1Holster Visual from JAZZ_TacGrip.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Misc/JAZZ_HolsterBelt.png"
MARKER = 'id = "JAZZ_HolsterBelt"'


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    old = (
        'ApplyTo = "M16A1",\n'
        '\t\t\t\t\t\t\tEntity = "M16A1Holster",\n'
        '\t\t\t\t\t\t\tSlot = "General",'
    )
    new = (
        'ApplyTo = "M16A1",\n'
        '\t\t\t\t\t\t\tEntity = "M16A1Holster",\n'
        f'\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\tSlot = "General",'
    )
    if f'ApplyTo = "M16A1"' in body and "M16A1Holster" in body and ICON in body.split('M16A1Holster')[1][:200]:
        print("M16A1 already")
    elif old in body:
        body = body.replace(old, new, 1)
        print("M16A1 ok")
    else:
        raise SystemExit("M16A1 needle missing")
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
