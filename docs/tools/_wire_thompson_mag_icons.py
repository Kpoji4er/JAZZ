"""Wire Thompson MagNormal (stick) + MagDrum_30_50_THOMPSON style-B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON30 = "Mod/e6L4ECj/WeaponComponents/Magazine/Thompson_Mag30.png"
ICON_DRUM = "Mod/e6L4ECj/WeaponComponents/Magazine/Thompson_MagDrum.png"


def patch_component(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if new in body:
        print(label, "already")
        return text
    if old not in body:
        print(label, "needle missing")
        return text
    print(label, "ok")
    return text[:start] + body.replace(old, new, 1) + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = patch_component(
        text,
        'id = "JAZZ_MagNormal"',
        'ApplyTo = "Thompson",\n'
        '\t\t\t\t\t\t\t\tEntity = "THOMPSON_MAG",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "Thompson",\n'
        '\t\t\t\t\t\t\t\tEntity = "THOMPSON_MAG",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON30}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "Mag30",
    )
    text = patch_component(
        text,
        'id = "JAZZ_MagDrum_30_50_THOMPSON"',
        'ApplyTo = "Thompson",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "ThompsonDrum",\n'
        '\t\t\t\t\t\t\t\t\tIcon = "Mod/e6L4ECj/magpictures/thompsondrum.png",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "Thompson",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "ThompsonDrum",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON_DRUM}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "Drum",
    )
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
