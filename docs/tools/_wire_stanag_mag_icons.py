"""Wire STANAG Icons for CAR15/M4/M16/AR15 family.

MagNormal + MagSmall30_20 → vanilla m16_magazine.
MagQuick_AR15 gaps → vanilla quick_STANAG_magazine.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "UI/Icons/Upgrades/m16_magazine"

# MagNormal: (ApplyTo, unique Entity line)
MAG_NORMAL = [
    ("AR15", 'Entity = "WeaponAttA_MagazineCAR15_02"'),
    ("M4A1", 'Entity = "M4A1StanagV3"'),
    ("M4Commando", 'Entity = "WeaponAttA_MagazineCAR15_02"'),
    ("M16A1", 'Entity = "Stanag30V2"'),
    ("M16A2", 'Entity = "Stanag30V2"'),
    ("M16A4", 'Entity = "Stanag30V2"'),
    ("CAR15", 'Entity = "Stanag"'),
]

# MagSmall30_20 (20-rd STANAG): same family where Visual exists
MAG_SMALL = [
    ("M4A1", 'Entity = "M16A1Stanag20"'),
    ("M16A1", 'Entity = "M16A1Stanag20"'),
    ("M16A2", 'Entity = "M16A1Stanag20"'),
    ("M16A4", 'Entity = "M16A1Stanag20"'),
    ("CAR15", 'Entity = "M16A1Stanag20"'),
]

ICON_QUICK = "UI/Icons/Upgrades/quick_STANAG_magazine"
# MagQuick_AR15 missing Visual Icons on several ApplyTo
MAG_QUICK = [
    ("M4A1", 'Entity = "M16A1Stanag20"'),
    ("M16A1", 'Entity = "M16A1Stanag20"'),
    ("M16A4", 'Entity = "M16A1Stanag20"'),
    ("CAR15", 'Entity = "M16A1Stanag20"'),
]


def patch_visual(
    body: str, apply: str, entity_line: str, icon: str
) -> tuple[str, str]:
    needle_start = f'ApplyTo = "{apply}",'
    idx = 0
    while True:
        i = body.find(needle_start, idx)
        if i < 0:
            return body, "missing"
        end = body.find("}),", i)
        if end < 0:
            return body, "missing"
        block = body[i:end]
        if entity_line not in block:
            idx = i + 1
            continue
        if f'Icon = "{icon}"' in block:
            return body, "already"
        if "Icon =" in block:
            lines = block.splitlines(keepends=True)
            out = []
            for ln in lines:
                if ln.lstrip().startswith("Icon ="):
                    ind = ln[: len(ln) - len(ln.lstrip("\t"))]
                    out.append(f'{ind}Icon = "{icon}",\n')
                else:
                    out.append(ln)
            new_block = "".join(out)
        else:
            line_end = block.find("\n", block.find(entity_line))
            ind = "\t\t\t\t\t\t\t\t"
            for ln in block.splitlines():
                if "Entity =" in ln:
                    ind = ln[: len(ln) - len(ln.lstrip("\t"))]
                    break
            new_block = (
                block[: line_end + 1]
                + f'{ind}Icon = "{icon}",\n'
                + block[line_end + 1 :]
            )
        return body[:i] + new_block + body[end:], "ok"


def patch_comp(
    text: str,
    marker: str,
    targets: list[tuple[str, str]],
    label: str,
    icon: str,
) -> str:
    end = text.find(marker)
    if end < 0:
        print(label, "comp missing")
        return text
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    for apply, ent in targets:
        body, status = patch_visual(body, apply, ent, icon)
        print(f"{label} {apply}", status)
    return text[:start] + body + rest


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    text = patch_comp(text, 'id = "JAZZ_MagNormal"', MAG_NORMAL, "MagNormal", ICON)
    text = patch_comp(
        text, 'id = "JAZZ_MagSmall30_20"', MAG_SMALL, "MagSmall20", ICON
    )
    text = patch_comp(
        text, 'id = "JAZZ_MagQuick_AR15"', MAG_QUICK, "MagQuick", ICON_QUICK
    )

    # MagSmall30_20 component Icon — only the top-level Icon= near DisplayName
    end = text.find('id = "JAZZ_MagSmall30_20"')
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    # Prefer exact header Icon after DisplayName MagSmall30_20
    old = (
        'DisplayName = T(927657862290, --[[ModItemWeaponComponent MagSmall30_20 DisplayName]] "Магазин на 20 патрон"),\n'
        '\t\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/mp5_mag_normal",'
    )
    new = (
        'DisplayName = T(927657862290, --[[ModItemWeaponComponent MagSmall30_20 DisplayName]] "Магазин на 20 патрон"),\n'
        f'\t\t\t\t\t\t\tIcon = "{ICON}",'
    )
    if f'Icon = "{ICON}"' in body[:800] and "mp5_mag_normal" not in body[:800]:
        print("MagSmall20 comp Icon already")
    elif old in body:
        body = body.replace(old, new, 1)
        print("MagSmall20 comp Icon ok")
        text = text[:start] + body + rest
    else:
        print("MagSmall20 comp Icon needle missing")

    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    for _ in range(25):
        try:
            os.replace(tmp, ITEMS)
            print("done", ICON)
            return
        except OSError:
            time.sleep(0.3)
    raise SystemExit("locked")


if __name__ == "__main__":
    main()
