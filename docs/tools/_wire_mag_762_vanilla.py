"""Wire MagNormal 7.62 steel 30-rd Icon (vanilla AK47_magazine) on AK family."""
from __future__ import annotations

from pathlib import Path

ITEMS = Path(__file__).resolve().parents[2] / "items.lua"
ICON = "UI/Icons/Upgrades/AK47_magazine"
MARKER = 'id = "JAZZ_MagNormal"'

# (ApplyTo, Entity line fragment that uniquely identifies the Visual)
TARGETS = [
    ('AK47', 'Entity = "J_AK47_Mag"'),
    ('AKM', 'Entity = "AKMWaffleMag"'),
    ('RPK', 'Entity = "WeaponAttA_MagazineAK47_01"'),
    ('Type56', 'Entity = "Type56Mag"'),
]


def patch_visual(body: str, apply: str, entity_line: str) -> tuple[str, bool]:
    # Find ApplyTo block containing this entity
    needle_start = f'ApplyTo = "{apply}",'
    idx = 0
    while True:
        i = body.find(needle_start, idx)
        if i < 0:
            return body, False
        # find end of this PlaceObj
        end = body.find("}),", i)
        if end < 0:
            return body, False
        block = body[i:end]
        if entity_line not in block:
            idx = i + 1
            continue
        if f'Icon = "{ICON}"' in block:
            return body, True  # already
        # insert Icon after Entity line
        if "Icon =" in block:
            # replace existing Icon
            lines = block.splitlines(keepends=True)
            out = []
            for ln in lines:
                if ln.lstrip().startswith("Icon ="):
                    ind = ln[: len(ln) - len(ln.lstrip("\t"))]
                    out.append(f'{ind}Icon = "{ICON}",\n')
                else:
                    out.append(ln)
            new_block = "".join(out)
        else:
            ent = block.find(entity_line)
            # find full Entity line end
            line_end = block.find("\n", ent)
            ind = "\t\t\t\t\t\t\t\t"
            for ln in block.splitlines():
                if "Entity =" in ln:
                    ind = ln[: len(ln) - len(ln.lstrip("\t"))]
                    break
            new_block = (
                block[: line_end + 1]
                + f'{ind}Icon = "{ICON}",\n'
                + block[line_end + 1 :]
            )
        return body[:i] + new_block + body[end:], True


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    end = text.find(MARKER)
    if end < 0:
        raise SystemExit("MagNormal missing")
    start = text.rfind("PlaceObj('ModItemWeaponComponent'", 0, end)
    body, rest = text[start:end], text[end:]
    for apply, ent in TARGETS:
        body, ok = patch_visual(body, apply, ent)
        print(apply, "ok" if ok else "FAIL")
    tmp = ITEMS.with_suffix(".lua.tmp")
    tmp.write_text(text[:start] + body + rest, encoding="utf-8", newline="\n")
    import os
    import time

    for _ in range(15):
        try:
            os.replace(tmp, ITEMS)
            break
        except OSError:
            time.sleep(0.4)
    else:
        raise SystemExit(f"could not replace {ITEMS} (locked?)")
    print("done", ICON)


if __name__ == "__main__":
    main()
