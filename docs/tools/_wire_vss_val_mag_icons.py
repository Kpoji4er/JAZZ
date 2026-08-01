"""Wire VSS/AS_Val MagNormal (10) + MagLarge_10_20_VAL (20) Style B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON10 = "Mod/e6L4ECj/WeaponComponents/Magazine/VSS_Mag10.png"
ICON20 = "Mod/e6L4ECj/WeaponComponents/Magazine/VSS_Mag20.png"


def patch_component(text: str, marker: str, old: str, new: str, label: str) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    if new in body and old not in body:
        print(label, "already")
        return text
    if old not in body:
        print(label, "needle missing")
        return text
    print(label, "ok")
    return text[:start] + body.replace(old, new, 1) + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")

    for name in ("VSS", "AS_Val"):
        text = patch_component(
            text,
            'id = "JAZZ_MagNormal"',
            f'ApplyTo = "{name}",\n'
            '\t\t\t\t\t\t\t\tEntity = "VSSMagSmall",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            f'ApplyTo = "{name}",\n'
            '\t\t\t\t\t\t\t\tEntity = "VSSMagSmall",\n'
            f'\t\t\t\t\t\t\t\tIcon = "{ICON10}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",',
            f"MagNormal {name}",
        )

    text = patch_component(
        text,
        'id = "JAZZ_MagLarge_10_20_VAL"',
        'ApplyTo = "AS_Val",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "ValMag20",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "AS_Val",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "ValMag20",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON20}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagLarge AS_Val",
    )
    text = patch_component(
        text,
        'id = "JAZZ_MagLarge_10_20_VAL"',
        'ApplyTo = "VSS",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "VSSMagLarge",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        'ApplyTo = "VSS",\n'
        '\t\t\t\t\t\t\t\t\tEntity = "VSSMagLarge",\n'
        f'\t\t\t\t\t\t\t\t\tIcon = "{ICON20}",\n'
        '\t\t\t\t\t\t\t\t\tSlot = "Magazine",',
        "MagLarge VSS",
    )

    # component-level Icon if still vanilla/missing — leave if shared MagLarge template
    end = text.find('id = "JAZZ_MagLarge_10_20_VAL"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    # set comp Icon to Mag20 if it's a generic large icon
    for old_icon in (
        'Icon = "UI/Icons/Upgrades/expanded_AK74_bakelite_magazine",',
        'Icon = "UI/Icons/Upgrades/galil_magazine_large",',
        'Icon = "UI/Icons/Upgrades/default_magazine",',
    ):
        if old_icon in body[:600]:
            body = body.replace(old_icon, f'Icon = "{ICON20}",', 1)
            text = text[:start] + body + rest
            print("MagLarge comp Icon ok")
            break
    else:
        if ICON20 in body[:600]:
            print("MagLarge comp Icon already")
        else:
            print("MagLarge comp Icon skip")

    inv_marker = "'Id', \"JAZZ_MagLarge_10_20_VAL\""
    inv_pos = text.find(inv_marker)
    if inv_pos >= 0:
        inv_start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, inv_pos)
        inv_end = text.find("}),", inv_pos)
        chunk = text[inv_start:inv_end]
        if ICON20 in chunk:
            print("Inv already")
        else:
            for old_inv in (
                "'Icon', \"UI/Icons/Upgrades/expanded_AK74_bakelite_magazine\",",
                "'Icon', \"UI/Icons/Upgrades/galil_magazine_large\",",
                "'Icon', \"UI/Icons/Upgrades/default_magazine\",",
                "'Icon', \"UI/Icons/Upgrades/AK74_Bakelite_magazine\",",
            ):
                if old_inv in chunk:
                    text = (
                        text[:inv_start]
                        + chunk.replace(old_inv, f"'Icon', \"{ICON20}\",", 1)
                        + text[inv_end:]
                    )
                    print("Inv ok")
                    break
            else:
                print("Inv needle missing")

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
