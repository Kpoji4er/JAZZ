"""Wire P226 Handgrip Default + Ergo style-B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_DEF = "Mod/e6L4ECj/WeaponComponents/Handgrip/P226_Handgrip_Default.png"
ICON_ERGO = "Mod/e6L4ECj/WeaponComponents/Handgrip/P226_Handgrip_Ergo_v2.png"


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
        'id = "JAZZ_Handgrip_Default"',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\tEntity = "P226Grip",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\tEntity = "P226Grip",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_DEF}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        "Default",
    )
    text = patch(
        text,
        'id = "JAZZ_Handgrip_Ergo"',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\tEntity = "P226GripErgo",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        'ApplyTo = "P226",\n'
        '\t\t\t\t\t\t\t\tEntity = "P226GripErgo",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_ERGO}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        "Ergo",
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
