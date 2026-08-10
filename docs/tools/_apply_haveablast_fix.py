# -*- coding: utf-8 -*-
"""Sync HaveABlast ModItem in items.lua from CharacterEffect/HaveABlast.lua."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
CE = ROOT / "CharacterEffect" / "HaveABlast.lua"


def main() -> None:
    ce = CE.read_text(encoding="utf-8")
    # Extract unit_reactions block from DefineClass body
    m = re.search(
        r"unit_reactions = \{\n(.*?)\n\t\},\n\tDisplayName",
        ce,
        re.S,
    )
    if not m:
        raise SystemExit("unit_reactions not found in companion")
    reactions_inner = m.group(1)
    # Indent for items.lua ModItem (tabs: unit_reactions under ModItem uses extra tab)
    # Companion uses one tab for PlaceObj inside unit_reactions; items uses more.
    desc = re.search(
        r'Description = T\(890000000009874, --\[\[ModItemCharacterEffectCompositeDef HaveABlast Description\]\] "([^"]*)"\)',
        ce,
    )
    if not desc:
        raise SystemExit("Description not found")
    new_desc = desc.group(1)

    text = ITEMS.read_text(encoding="utf-8")
    # Replace Description string for HaveABlast
    text2, n = re.subn(
        r"('Description', T\(890000000009874, --\[\[ModItemCharacterEffectCompositeDef HaveABlast Description\]\] \")(.*?)(\"\))",
        lambda m: m.group(1) + new_desc + m.group(3),
        text,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"Description replace count={n}")

    # Replace unit_reactions inside HaveABlast ModItem
    pat = re.compile(
        r"('Id', \"HaveABlast\",\n\t\t\t\t\t'object_class', \"Perk\",\n\t\t\t\t\t'unit_reactions', \{\n)"
        r"(.*?)"
        r"(\n\t\t\t\t\t\},\n\t\t\t\t\t'DisplayName')",
        re.S,
    )

    def repl(mm: re.Match) -> str:
        # Re-indent companion reactions (which use \t\t for PlaceObj) to items depth (\t\t\t\t\t\t)
        body = reactions_inner
        # companion PlaceObj lines start with \t\t
        lines = []
        for line in body.splitlines():
            if line.startswith("\t\t"):
                lines.append("\t\t\t\t\t\t" + line[2:])
            elif line.startswith("\t"):
                lines.append("\t\t\t\t\t\t" + line[1:])
            else:
                lines.append("\t\t\t\t\t\t" + line)
        return mm.group(1) + "\n".join(lines) + mm.group(3)

    text3, n2 = pat.subn(repl, text2, count=1)
    if n2 != 1:
        raise SystemExit(f"unit_reactions replace count={n2}")

    ITEMS.write_text(text3, encoding="utf-8", newline="\n")
    print("HaveABlast synced into items.lua")


if __name__ == "__main__":
    main()
