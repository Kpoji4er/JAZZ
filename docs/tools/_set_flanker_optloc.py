# Set OptLocSearchRadius on Legion_Flanker / Rebels_Flanker in jazz-units/items.lua
from __future__ import annotations

import re
from pathlib import Path

ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
TARGET_IDS = ("Legion_Flanker", "Rebels_Flanker")
NEW_RADIUS = 55


def extract_block(text: str, archetype_id: str) -> tuple[int, int]:
    needle = f'\tid = "{archetype_id}",'
    id_pos = text.find(needle)
    if id_pos < 0:
        raise SystemExit(f"missing id {archetype_id}")
    start = text.rfind("PlaceObj('ModItemAIArchetype'", 0, id_pos)
    if start < 0:
        raise SystemExit(f"missing PlaceObj for {archetype_id}")
    brace = text.find("{", start)
    depth = 0
    i = brace
    in_str = False
    str_ch = ""
    escape = False
    while i < len(text):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == str_ch:
                in_str = False
        else:
            if ch in ("'", '"'):
                in_str = True
                str_ch = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return start, i + 1
        i += 1
    raise SystemExit(f"unclosed {archetype_id}")


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    for aid in TARGET_IDS:
        s, e = extract_block(text, aid)
        block = text[s:e]
        new_block, n = re.subn(
            r"OptLocSearchRadius = \d+",
            f"OptLocSearchRadius = {NEW_RADIUS}",
            block,
            count=1,
        )
        if n != 1:
            raise SystemExit(f"{aid}: OptLoc replacements={n}")
        text = text[:s] + new_block + text[e:]
        print(f"{aid}: OptLocSearchRadius -> {NEW_RADIUS}")
    ITEMS.write_text(text, encoding="utf-8", newline="\n")
    print("OK")


if __name__ == "__main__":
    main()
