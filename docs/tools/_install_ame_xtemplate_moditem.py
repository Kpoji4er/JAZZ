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


def _find_moditem_xtemplate_span(text: str, template_id: str) -> tuple[int, int] | None:
    """Return [start, end) of PlaceObj('ModItemXTemplate' … id=<template_id> …), or None."""
    needle = f'id = "{template_id}"'
    id_idx = text.find(needle)
    if id_idx < 0:
        return None
    start = text.rfind("PlaceObj('ModItemXTemplate'", 0, id_idx)
    if start < 0:
        return None
    # Walk braces from the PlaceObj '(' after ModItemXTemplate
    open_paren = text.find("(", start)
    if open_paren < 0:
        return None
    depth = 0
    i = open_paren
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
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    while end < len(text) and text[end] in " \t\r":
                        end += 1
                    if end < len(text) and text[end] == "\n":
                        end += 1
                    return start, end
        i += 1
    return None


def patch_items(block: str) -> None:
    text = ITEMS.read_text(encoding="utf-8")
    # Match markers with any leading whitespace so reinstalls don't leave orphan tabs.
    if BEGIN in text:
        pattern = re.compile(
            r"[ \t]*" + re.escape(BEGIN) + r".*?" + r"[ \t]*" + re.escape(END) + r"[ \t]*\n?",
            re.S,
        )
        # Callable replacement: re.sub treats \n/\1 in a plain string as escapes
        # and would corrupt Lua "\\n" inside T(...) bios.
        text, n = pattern.subn(lambda _m: block, text, count=1)
        if n != 1:
            raise RuntimeError(f"AME XTemplate replace count={n}")
        ITEMS.write_text(text, encoding="utf-8")
        print("replaced existing AME XTemplate block in items.lua")
        return
    # Editor save can strip install markers; replace by ModItem id instead of duplicating.
    span = _find_moditem_xtemplate_span(text, "PDAAIMEBrowser")
    if span is not None:
        start, end = span
        text = text[:start] + block + text[end:]
        ITEMS.write_text(text, encoding="utf-8")
        print("replaced markerless PDAAIMEBrowser ModItemXTemplate in items.lua")
        return
    # Insert before Constants folder (first occurrence after PDAAIMBrowser)
    needle = "\tPlaceObj('ModItemFolder', {\n\t\t'name', \"Constants\","
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit("Constants folder anchor not found in items.lua")
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
