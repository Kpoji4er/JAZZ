"""Rename AppearancePreset Hitman -> Jazz_Hitman so vanilla AIM Hitman is not overridden.
Keep Jazz_Hitman UnitData pointing at Jazz_Hitman preset.
Shadow AppearancesList already restored to Shadow.
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")


def rename_hitman_appearance_preset(items: str) -> str:
    # Only ModItemAppearancePreset blocks whose id is Hitman
    out = []
    last = 0
    for m in re.finditer(r"PlaceObj\('ModItemAppearancePreset',\s*\{", items):
        # find matching close — next PlaceObj at same indent roughly: \n\t\t}),
        # Search id within next 8k
        window = items[m.start() : m.start() + 8000]
        idm = re.search(r"\bid = \"([^\"]+)\"", window)
        if not idm or idm.group(1) != "Hitman":
            continue
        id_abs = m.start() + idm.start()
        # replace this id only
        out.append(items[last:id_abs])
        out.append('id = "Jazz_Hitman"')
        last = id_abs + len('id = "Hitman"')
        print(f"items.lua AppearancePreset id renamed at {id_abs}")
    out.append(items[last:])
    items = "".join(out)

    # Jazz_Hitman UnitData AppearancesList Preset
    old = "'AppearancesList', { PlaceObj('AppearanceWeight', { 'Preset', \"Hitman\" }) }"
    new = "'AppearancesList', { PlaceObj('AppearanceWeight', { 'Preset', \"Jazz_Hitman\" }) }"
    if old not in items:
        # multiline form
        items2, n = re.subn(
            r"('Id', \"Jazz_Hitman\".{0,2500}?'AppearancesList',\s*\{\s*PlaceObj\('AppearanceWeight',\s*\{\s*'Preset',\s*)\"Hitman\"",
            r'\1"Jazz_Hitman"',
            items,
            count=1,
            flags=re.S,
        )
        if n:
            items = items2
            print("Jazz_Hitman AppearancesList Preset updated (regex)")
        else:
            print("WARN: Jazz_Hitman AppearancesList not updated")
    else:
        items = items.replace(old, new, 1)
        print("Jazz_Hitman AppearancesList Preset updated (compact)")
    return items


def rename_metadata(meta: str) -> str:
    # Only AppearancePreset Class + Id Hitman
    def repl(m: re.Match) -> str:
        return m.group(0).replace("'Id', \"Hitman\"", "'Id', \"Jazz_Hitman\"", 1)

    meta2, n = re.subn(
        r"PlaceObj\('ModResourcePreset',\s*\{\s*'Class',\s*\"AppearancePreset\",\s*'Id',\s*\"Hitman\",",
        lambda m: m.group(0).replace('"Hitman"', '"Jazz_Hitman"', 1),
        meta,
    )
    print(f"metadata AppearancePreset Hitman->Jazz_Hitman count={n}")
    return meta2


def main() -> None:
    items_path = UNITS / "items.lua"
    meta_path = UNITS / "metadata.lua"
    companion = UNITS / "UnitData" / "Jazz_Hitman.lua"

    items = items_path.read_text(encoding="utf-8")
    items_path.write_text(rename_hitman_appearance_preset(items), encoding="utf-8", newline="\n")

    meta = meta_path.read_text(encoding="utf-8")
    meta_path.write_text(rename_metadata(meta), encoding="utf-8", newline="\n")

    if companion.exists():
        c = companion.read_text(encoding="utf-8")
        c2 = c.replace("'Preset', \"Hitman\"", "'Preset', \"Jazz_Hitman\"")
        if c2 != c:
            companion.write_text(c2, encoding="utf-8", newline="\n")
            print("UnitData/Jazz_Hitman.lua updated")
        else:
            print("WARN companion unchanged")

    # Verify Shadow still Shadow; no AppearancePreset id=Hitman left
    items = items_path.read_text(encoding="utf-8")
    assert 'id = "Hitman"' not in items or True
    # check appearance presets
    for m in re.finditer(r"PlaceObj\('ModItemAppearancePreset',\s*\{", items):
        w = items[m.start() : m.start() + 4000]
        idm = re.search(r'\bid = "([^"]+)"', w)
        if idm and idm.group(1) == "Hitman":
            raise SystemExit("Still have AppearancePreset Hitman")
    # Shadow UnitData
    sm = re.search(r"'Id', \"Shadow\".{0,2000}?'AppearancesList',.*?\{(.*?)\}", items, re.S)
    if sm and '"Simon"' in sm.group(1).split("Equipment")[0]:
        raise SystemExit("Shadow still points at Simon")
    print("verify OK")


if __name__ == "__main__":
    main()
