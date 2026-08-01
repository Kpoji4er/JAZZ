"""Wire JAZZ_IronSight_AIM: component Icon + P210 Visual style-B."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
COMP_ICON = "UI/Icons/Upgrades/ironsights_hands"
P210_ICON = "Mod/e6L4ECj/WeaponComponents/Optics/P210_IronSight_AIM.png"
MARKER = 'id = "JAZZ_IronSight_AIM"'


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("missing AIM")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]

    # component Icon if missing (after DisplayName / before ChipIcon or Slot)
    if "Icon = " not in body.split("Visuals")[0]:
        # insert after Slot = "Scope",
        old_slot = '\t\t\t\t\t\tSlot = "Scope",\n\t\t\t\t\tChipIcon'
        # actual indent may vary — ChipIcon line has less tabs in file
        if 'Slot = "Scope",' in body and "ChipIcon" in body:
            body = body.replace(
                'Slot = "Scope",\n\t\t\t\t\tChipIcon',
                f'Slot = "Scope",\n\t\t\t\t\t\tIcon = "{COMP_ICON}",\n\t\t\t\t\tChipIcon',
                1,
            )
            print("comp Icon ok")
        else:
            print("comp Icon skip")
    else:
        print("comp Icon already")

    old = (
        'ApplyTo = "P210",\n'
        '\t\t\t\t\t\t\t\tEntity = "P210SightSport",\n'
        '\t\t\t\t\t\t\t\tSlot = "Scope",'
    )
    new = (
        'ApplyTo = "P210",\n'
        '\t\t\t\t\t\t\t\tEntity = "P210SightSport",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{P210_ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Scope",'
    )
    if old not in body:
        i = body.find("P210SightSport")
        print(repr(body[max(0, i - 80) : i + 140]))
        raise SystemExit("P210 needle missing")
    if P210_ICON in body:
        print("P210 already")
    else:
        body = body.replace(old, new, 1)
        print("P210 ok")

    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
    for _ in range(15):
        try:
            os.replace(tmp, ITEMS)
            break
        except OSError:
            time.sleep(0.4)
    else:
        raise SystemExit("locked")
    print("done")


if __name__ == "__main__":
    main()
