"""Wire P226 MagNormal (15) + MagLarge_18_20 (20) style-B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON15 = "Mod/e6L4ECj/WeaponComponents/Magazine/P226_Mag15.png"
ICON20 = "Mod/e6L4ECj/WeaponComponents/Magazine/P226_Mag20.png"


def patch(text: str, marker: str, old: str, new: str, label: str) -> str:
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
    text = patch(
        text,
        'id = "JAZZ_MagNormal"',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\tEntity = "P226MagD",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\tEntity = "P226MagD",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON15}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagNormal 15",
    )
    text = patch(
        text,
        'id = "JAZZ_MagLarge_18_20"',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "P226MagExt",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "P226MagExt",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON20}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagLarge 20",
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
