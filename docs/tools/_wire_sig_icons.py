"""Wire SIG MagNormal + SigDefHandGuard + SigErgoHandGrip Style B Icons."""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON_MAG = "Mod/e6L4ECj/WeaponComponents/Magazine/Sig_Mag30.png"
ICON_DEF = "Mod/e6L4ECj/WeaponComponents/Handgrip/Sig_Handgrip_Default.png"
ICON_ERGO = "Mod/e6L4ECj/WeaponComponents/Handgrip/Sig_Handgrip_Ergo.png"


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

    mag_targets = [
        ("Sig550", 'Entity = "SigMagDef"'),
        ("Sig550Custom", 'Entity = "SigMagDef"'),
        ("Sig552", 'Entity = "SigMagDef"'),
        ("Sig552SWAT", 'Entity = "Sig552Mag"'),
    ]
    end = text.find('id = "JAZZ_MagNormal"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    for apply, ent in mag_targets:
        old = (
            f'ApplyTo = "{apply}",\n'
            f"\t\t\t\t\t\t\t\t{ent},\n"
            '\t\t\t\t\t\t\t\tSlot = "Magazine",'
        )
        new = (
            f'ApplyTo = "{apply}",\n'
            f"\t\t\t\t\t\t\t\t{ent},\n"
            f'\t\t\t\t\t\t\t\tIcon = "{ICON_MAG}",\n'
            '\t\t\t\t\t\t\t\tSlot = "Magazine",'
        )
        if ICON_MAG in body and f'ApplyTo = "{apply}"' in body:
            # check this apply block
            i = body.find(f'ApplyTo = "{apply}",')
            chunk = body[i : i + 250]
            if ICON_MAG in chunk and ent in chunk:
                print(f"Mag {apply}", "already")
                continue
        if old not in body:
            print(f"Mag {apply}", "needle missing")
            continue
        body = body.replace(old, new, 1)
        print(f"Mag {apply}", "ok")
    text = text[:start] + body + rest

    # Default grip — set component Icon after DisplayName
    text = patch_component(
        text,
        'id = "JAZZ_SigDefHandGuard"',
        'DisplayName = T(890000000000990, --[[ModItemWeaponComponent SigDefHandGuard DisplayName]] "Заводская рукоять Sig"),\n'
        '\t\t\t\t\t\tSlot = "Handguard",',
        'DisplayName = T(890000000000990, --[[ModItemWeaponComponent SigDefHandGuard DisplayName]] "Заводская рукоять Sig"),\n'
        f'\t\t\t\t\t\tIcon = "{ICON_DEF}",\n'
        '\t\t\t\t\t\tSlot = "Handguard",',
        "Def grip Icon",
    )
    text = patch_component(
        text,
        'id = "JAZZ_SigDefHandGuard"',
        'Entity = "SIGHandGripDef",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        'Entity = "SIGHandGripDef",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_DEF}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        "Def grip Visual",
    )

    # Ergo — Icon after DisplayName (before ModificationDifficulty)
    text = patch_component(
        text,
        'id = "JAZZ_SigErgoHandGrip"',
        'DisplayName = T(890000000000153, --[[ModItemWeaponComponent SigErgoHandGrip DisplayName]] "Эргономичная рукоять для Sig"),\n'
        '\t\t\t\t\t\t\tModificationDifficulty = 0,',
        'DisplayName = T(890000000000153, --[[ModItemWeaponComponent SigErgoHandGrip DisplayName]] "Эргономичная рукоять для Sig"),\n'
        f'\t\t\t\t\t\t\tIcon = "{ICON_ERGO}",\n'
        '\t\t\t\t\t\t\tModificationDifficulty = 0,',
        "Ergo grip Icon",
    )
    text = patch_component(
        text,
        'id = "JAZZ_SigErgoHandGrip"',
        'Entity = "SIGErgoHandGrip",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        'Entity = "SIGErgoHandGrip",\n'
        f'\t\t\t\t\t\t\t\tIcon = "{ICON_ERGO}",\n'
        '\t\t\t\t\t\t\t\tSlot = "Handgrip",',
        "Ergo grip Visual",
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
