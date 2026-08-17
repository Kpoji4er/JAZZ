# -*- coding: utf-8 -*-
"""Sync MED-006 polished strings into companions + items.lua T() fallbacks."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EN = {
    "890000000010024": (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible light trauma "
        "(eases combat penalties one tier; does not heal trauma)\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP "
        "(scales with Medical: 9–30% from Medical 30 to 100)\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"
    ),
    "890000000010027": (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible medium or light trauma "
        "(eases combat penalties one tier; does not heal trauma)\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP "
        "(scales with Medical: 18–60% from Medical 50 to 100)\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack"
    ),
    "890000000010030": (
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible trauma of any severity "
        "(eases combat penalties one tier; does not heal trauma)\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP "
        "(scales with Medical: 30–100% from Medical 80 to 100)\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\\n"
        "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically from inventory"
    ),
    "890000000010213": (
        "Treat an ally with a small, medium, or large medkit. Restores HP as a % of max HP scaled by Medical "
        "(at Medical 100: 30/60/100%; at the kit's Medical gate: 30% of those values). Clears all bleeding, eases pain, "
        "clears wound infection, can rally the downed, and stabilizes one eligible trauma "
        "(eases combat penalties one tier — does not heal trauma). Field bandages use a separate action."
    ),
}


def replace_t(text: str, rid: str, new_en: str) -> tuple[str, int]:
    # Match T(id, "...") with possible escaped quotes; non-greedy until "), or ");
    pat = re.compile(
        rf'(T\({rid}, ")((?:\\.|[^"\\])*)(")',
        re.S,
    )

    def repl(m: re.Match) -> str:
        return m.group(1) + new_en + m.group(3)

    return pat.subn(repl, text, count=1)


def main() -> None:
    files = [
        ROOT / "InventoryItem/FirstAidKit.lua",
        ROOT / "InventoryItem/Medkit.lua",
        ROOT / "InventoryItem/Reanimationsset.lua",
        ROOT / "items.lua",
    ]
    for path in files:
        text = path.read_text(encoding="utf-8")
        total = 0
        for rid, en in EN.items():
            text, n = replace_t(text, rid, en)
            total += n
        path.write_text(text, encoding="utf-8", newline="\n" if path.suffix == ".lua" and "items" not in path.name else None)
        # items.lua keep original newlines - write utf-8 without forcing
        if path.name == "items.lua":
            path.write_text(text, encoding="utf-8")
        print(path.name, "replacements", total)


if __name__ == "__main__":
    main()
