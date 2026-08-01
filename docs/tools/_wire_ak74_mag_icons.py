"""Wire AK74_Mag30/45 Icons onto MagNormal + MagLarge_30_45 for AK74 / RPK74 / AKSU."""
from __future__ import annotations

from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON30 = "Mod/e6L4ECj/WeaponComponents/Magazine/AK74_Mag30.png"
ICON45 = "Mod/e6L4ECj/WeaponComponents/Magazine/AK74_Mag45_long.png"


def patch_visual_icons(text: str, comp_id: str, apply_to: str, icon: str) -> tuple[str, int]:
    marker = f'id = "{comp_id}"'
    end = text.find(marker)
    if end < 0:
        raise SystemExit(f"missing {comp_id}")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body = text[start:end]
    count = 0

    lines = body.splitlines(keepends=True)
    i = 0
    new_lines: list[str] = []
    while i < len(lines):
        if (
            "PlaceObj('WeaponComponentVisual'" in lines[i]
            and i + 1 < len(lines)
            and f'ApplyTo = "{apply_to}"' in lines[i + 1]
        ):
            block = [lines[i], lines[i + 1]]
            j = i + 2
            while j < len(lines):
                block.append(lines[j])
                if lines[j].rstrip().endswith("}),") or lines[j].rstrip() == "}),":
                    break
                j += 1
            has_icon = False
            entity_indent = "\t\t\t\t\t\t\t\t"
            for k, bl in enumerate(block):
                if "Entity =" in bl:
                    entity_indent = bl[: len(bl) - len(bl.lstrip("\t"))]
                if bl.lstrip().startswith("Icon ="):
                    has_icon = True
                    block[k] = f'{entity_indent}Icon = "{icon}",\n'
                    count += 1
            if not has_icon:
                for k, bl in enumerate(block):
                    if "Entity =" in bl:
                        ind = bl[: len(bl) - len(bl.lstrip("\t"))]
                        block.insert(k + 1, f'{ind}Icon = "{icon}",\n')
                        count += 1
                        break
                else:
                    raise SystemExit(f"no Entity in block {comp_id}/{apply_to}")
            new_lines.extend(block)
            i = j + 1
            continue
        new_lines.append(lines[i])
        i += 1

    return text[:start] + "".join(new_lines) + text[end:], count


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    total = 0
    jobs = (
        ("JAZZ_MagNormal", "AK74", ICON30),
        ("JAZZ_MagNormal", "RPK74", ICON30),
        ("JAZZ_MagNormal", "AKSU", ICON30),
        ("JAZZ_MagLarge_30_45", "AK74", ICON45),
        ("JAZZ_MagLarge_30_45", "RPK74", ICON45),
        ("JAZZ_MagLarge_30_45", "AKSU", ICON45),
    )
    for comp, apply, icon in jobs:
        text, n = patch_visual_icons(text, comp, apply, icon)
        print(f"{comp}/{apply}: {n}")
        total += n
    if total < 6:
        raise SystemExit(f"expected >=6 patches, got {total}")
    ITEMS.write_text(text, encoding="utf-8", newline="\n")
    print("ok", total)


if __name__ == "__main__":
    main()
