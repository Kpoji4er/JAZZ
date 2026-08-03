#!/usr/bin/env python3
"""Install PDAAIMEBrowser as ModItemXTemplate in items.lua + metadata resource."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_AME_Browser_Template.lua"
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
BEGIN = "-- JAZZ-UNITS-005-AME-XTEMPLATE-BEGIN"
END = "-- JAZZ-UNITS-005-AME-XTEMPLATE-END"


def build_moditem_block() -> str:
    text = SRC.read_text(encoding="utf-8")
    lines = text.splitlines()
    while lines and (lines[0].startswith("--") or not lines[0].strip()):
        lines.pop(0)
    body = "\n".join(lines)
    if not body.startswith("PlaceObj('XTemplate'"):
        raise RuntimeError(f"unexpected template start: {body[:80]!r}")
    body = body.replace("PlaceObj('XTemplate'", "PlaceObj('ModItemXTemplate'", 1)
    body = body.replace("XTemplate PDAAIMEBrowser", "ModItemXTemplate PDAAIMEBrowser")
    indented = "\n".join(("\t\t" + ln if ln.strip() else ln) for ln in body.splitlines())
    return f"\t\t{BEGIN}\n{indented.rstrip()},\n\t\t{END}\n"


def patch_items(block: str) -> None:
    text = ITEMS.read_text(encoding="utf-8")
    if BEGIN in text:
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.S)
        text = pattern.sub(block, text, count=1)
        ITEMS.write_text(text, encoding="utf-8")
        print("replaced existing AME XTemplate block in items.lua")
        return
    # Insert before Constants folder (first occurrence after PDAAIMBrowser)
    needle = "\tPlaceObj('ModItemFolder', {\n\t\t'name', \"Constants\","
    idx = text.find(needle)
    if idx < 0:
        raise RuntimeError("Constants folder anchor not found in items.lua")
    text = text[:idx] + block + text[idx:]
    ITEMS.write_text(text, encoding="utf-8")
    print("inserted AME XTemplate before Constants folder")


def patch_metadata() -> None:
    text = META.read_text(encoding="utf-8")
    # Remove from code[] if present
    text2 = text.replace('\n\t\t"Code/System_AME_Browser_Template.lua",', "")
    text2 = text2.replace('\t\t"Code/System_AME_Browser_Template.lua",\n', "")
    if text2 == text:
        print("note: template code entry already absent or different formatting")
    text = text2
    res = (
        "\t\tPlaceObj('ModResourcePreset', {\n"
        '\t\t\t\'Class\', "XTemplate",\n'
        '\t\t\t\'Id\', "PDAAIMEBrowser",\n'
        '\t\t\t\'ClassDisplayName\', "UI Template (XTemplate)",\n'
        "\t\t}),\n"
    )
    if "'Id', \"PDAAIMEBrowser\"" not in text:
        anchor = "'Id', \"PDAAIMBrowser\","
        aidx = text.find(anchor)
        if aidx < 0:
            raise RuntimeError("PDAAIMBrowser resource anchor missing")
        end = text.find("}),", aidx)
        if end < 0:
            raise RuntimeError("PDAAIMBrowser resource close missing")
        end += 3
        text = text[:end] + "\n" + res + text[end:]
        print("added ModResourcePreset PDAAIMEBrowser")
    else:
        print("ModResourcePreset PDAAIMEBrowser already present")
    META.write_text(text, encoding="utf-8")


def main() -> int:
    block = build_moditem_block()
    patch_items(block)
    patch_metadata()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
