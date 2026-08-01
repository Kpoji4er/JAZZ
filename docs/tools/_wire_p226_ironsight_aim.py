"""Wire JAZZ_IronSight_AIM P226 rear Visual → Optics/P226_IronSight_AIM.png.

Also stamps ApplyTo=P226 on AccF/AccR so they stay P226-only (P210 has its own Visual).
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Optics/P226_IronSight_AIM.png"
MARKER = 'id = "JAZZ_IronSight_AIM"'

OLD_R = (
    "PlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tEntity = "P226SightsAccR",\n'
    '\t\t\t\t\t\t\t\tSlot = "Sightsr",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),"
)
NEW_R = (
    "PlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "P226",\n'
    '\t\t\t\t\t\t\t\tEntity = "P226SightsAccR",\n'
    f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
    '\t\t\t\t\t\t\t\tSlot = "Sightsr",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),"
)

OLD_F = (
    "PlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tEntity = "P226SightsAccF",\n'
    '\t\t\t\t\t\t\t\tSlot = "Sightsf",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),"
)
NEW_F = (
    "PlaceObj('WeaponComponentVisual', {\n"
    '\t\t\t\t\t\t\t\tApplyTo = "P226",\n'
    '\t\t\t\t\t\t\t\tEntity = "P226SightsAccF",\n'
    '\t\t\t\t\t\t\t\tSlot = "Sightsf",\n'
    "\t\t\t\t\t\t\t\tparam_bindings = false,\n"
    "\t\t\t\t\t\t\t}),"
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("missing AIM")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]

    if ICON in body and "P226SightsAccR" in body:
        print("Icon already")
    elif OLD_R in body:
        body = body.replace(OLD_R, NEW_R, 1)
        print("rear ok")
    else:
        raise SystemExit("rear needle missing")

    if 'ApplyTo = "P226"' in body and "P226SightsAccF" in body:
        # may already after rear replace only on R
        if OLD_F in body:
            body = body.replace(OLD_F, NEW_F, 1)
            print("front ApplyTo ok")
        else:
            print("front already")
    elif OLD_F in body:
        body = body.replace(OLD_F, NEW_F, 1)
        print("front ApplyTo ok")
    else:
        print("front skip")

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
