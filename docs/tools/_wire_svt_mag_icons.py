"""Wire SVT40 MagDef → SVT_Mag10; AVT40 MagLarge → SVT_MagLarge (Style B)."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON10 = "Mod/e6L4ECj/WeaponComponents/Magazine/SVT_Mag10.png"
ICON_LG = "Mod/e6L4ECj/WeaponComponents/Magazine/SVT_MagLarge.png"
MARKER = 'id = "JAZZ_MagNormal"'

JOBS = (
    (
        'ApplyTo = "SVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagDef",\n'
        '\t\t\t\t\t\t\t\tIcon = "Mod/e6L4ECj/WeaponComponents/Magazine/SVT_Mag10.png",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "SVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagDef",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON10}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "SVT40 already",
    ),
    (
        'ApplyTo = "AVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagLarge",\n'
        '\t\t\t\t\t\t\t\tIcon = "Mod/e6L4ECj/WeaponComponents/Magazine/SVT_Mag10.png",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "AVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagLarge",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_LG}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "AVT40 -> MagLarge",
    ),
    (
        'ApplyTo = "SVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagDef",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "SVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagDef",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON10}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "SVT40 insert",
    ),
    (
        'ApplyTo = "AVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagLarge",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "AVT40",\n'
        '\t\t\t\t\t\t\t\tEntity = "SVT40_MagLarge",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_LG}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "AVT40 insert",
    ),
)


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    changed = False
    for old, new, label in JOBS:
        if old == new:
            continue
        if old in body:
            body = body.replace(old, new, 1)
            print(label, "ok")
            changed = True
    if not changed:
        # verify final state
        if ICON10 in body and ICON_LG in body:
            print("already split")
        else:
            raise SystemExit("no job matched")
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
