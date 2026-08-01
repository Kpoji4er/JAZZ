# One-shot: clone Legion_Flanker -> Rebels_Flanker in jazz-units/items.lua
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
ITEMS = UNITS / "items.lua"


def extract_moditem_aiarchetype(text: str, archetype_id: str) -> tuple[str, int, int]:
    """Return (block, start, end) for PlaceObj('ModItemAIArchetype'...) with given id."""
    needle = f'\tid = "{archetype_id}",'
    id_pos = text.find(needle)
    if id_pos < 0:
        raise SystemExit(f"id not found: {archetype_id}")
    # Walk backward to PlaceObj('ModItemAIArchetype'
    start = text.rfind("PlaceObj('ModItemAIArchetype'", 0, id_pos)
    if start < 0:
        raise SystemExit(f"PlaceObj start not found for {archetype_id}")
    # Brace match from first '{' after PlaceObj
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
                    # include trailing ),
                    end = i + 1
                    if end < len(text) and text[end] == ")":
                        end += 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    # keep following newline if present
                    if end < len(text) and text[end] == "\n":
                        end += 1
                    return text[start:end], start, end
        i += 1
    raise SystemExit(f"unclosed block for {archetype_id}")


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    if re.search(r'\tid = "Rebels_Flanker",', text):
        print("Rebels_Flanker already present — skip insert")
        return

    legion_block, _, _ = extract_moditem_aiarchetype(text, "Legion_Flanker")
    rebels = legion_block.replace(
        '\tid = "Legion_Flanker",',
        '\tid = "Rebels_Flanker",',
        1,
    )
    # Keep group = "Legion" like other Rebels_* archetypes in this folder, or set Rebels?
    # Existing Rebels_Assaulter/Frontliner use group = "Legion" — keep as-is from clone.
    if 'Comment = "Keywords: Flank' in rebels:
        rebels = rebels.replace(
            'Comment = "Keywords: Flank, Explosives",',
            'Comment = "Rebels flanker (clone of Legion_Flanker); Keywords: Flank, Explosives",',
            1,
        )

    # Insert after Rebels_Assaulter block
    assaulter, a_start, a_end = extract_moditem_aiarchetype(text, "Rebels_Assaulter")
    # Ensure rebels block has same indent leading (PlaceObj is indented with tabs)
    insert = rebels
    if not insert.endswith("\n"):
        insert += "\n"

    new_text = text[:a_end] + insert + text[a_end:]
    ITEMS.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"Inserted Rebels_Flanker after Rebels_Assaulter at offset {a_end}")
    print(f"Block chars: {len(insert)}")


if __name__ == "__main__":
    main()
