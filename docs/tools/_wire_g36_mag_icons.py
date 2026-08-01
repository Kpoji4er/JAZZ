"""Wire MagNormal ApplyTo G36 + G36c → Magazine/G36_Mag30.png."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "Mod/e6L4ECj/WeaponComponents/Magazine/G36_Mag30.png"
MARKER = 'id = "JAZZ_MagNormal"'

TARGETS = [
    (
        "G36",
        'ApplyTo = "G36",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineHKG36_01",\n'
        '\t\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/G36_magazine",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "G36",\n'
        '\t\t\t\t\t\t\t\tEntity = "WeaponAttA_MagazineHKG36_01",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
    ),
    (
        "G36c",
        'ApplyTo = "G36c",\n'
        '\t\t\t\t\t\t\t\tEntity = "G36cMag",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "G36c",\n'
        '\t\t\t\t\t\t\t\tEntity = "G36cMag",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
    ),
]


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    for name, old, new in TARGETS:
        if ICON in body and f'ApplyTo = "{name}"' in body and old not in body:
            # may already be wired — check specifically
            if f'ApplyTo = "{name}"' in body and ICON in body[
                body.find(f'ApplyTo = "{name}"') : body.find(f'ApplyTo = "{name}"') + 300
            ]:
                print(name, "already")
                continue
        if old not in body:
            print(name, "needle missing")
            continue
        body = body.replace(old, new, 1)
        print(name, "ok")
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
