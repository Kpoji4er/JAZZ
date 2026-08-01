# -*- coding: utf-8 -*-
"""Find items.lua structural holes that break Mod Editor (missing commas / bad closes)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Pattern: }) or } followed by PlaceObj on next non-empty line without comma
    problems: list[str] = []
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if not (s.endswith("})") or s.endswith("}")):
            continue
        if s.endswith("}),") or s.endswith("},") or s.endswith("),"):
            continue
        # look ahead
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j >= len(lines):
            continue
        nxt = lines[j].lstrip()
        if nxt.startswith("PlaceObj(") or nxt.startswith("PlaceObj '"):
            problems.append(f"L{i+1}: closes without comma before PlaceObj at L{j+1}: {s[-40:]!r} -> {nxt[:60]!r}")

    print(f"missing-comma-before-PlaceObj: {len(problems)}")
    for p in problems[:80]:
        print(p)

    # Also: PlaceObj at column 0 inside file (suspicious insert)
    col0 = [i + 1 for i, ln in enumerate(lines) if ln.startswith("PlaceObj(")]
    print(f"PlaceObj at column 0: {len(col0)} e.g. {col0[:20]}")

    # Lua-ish brace walk ignoring strings roughly — report first depth mismatch near known area
    # Use apply_attach matching_paren style on return { ... }
    sys_path = str(ROOT / "docs" / "tools")
    import sys

    sys.path.insert(0, sys_path)
    from _apply_attach_001 import matching_paren

    start = text.find("return {")
    if start < 0:
        print("no return {")
        return
    brace = text.find("{", start)
    try:
        end = matching_paren(text.replace("return {", "return (", 1), text.find("(", text.find("return")))
        # hacky — better walk braces
    except Exception as e:
        print("matching failed", e)

    # Brace depth tracker (ignore strings/comments lightly)
    depth = 0
    i = 0
    n = len(text)
    quote = None
    line = 1
    first_neg = None
    while i < n:
        ch = text[i]
        if ch == "\n":
            line += 1
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            # long comments --[[
            quote = ch
            i += 1
            continue
        if ch == "-" and i + 3 < n and text[i : i + 4] == "--[[":
            endc = text.find("]]", i + 4)
            if endc < 0:
                break
            line += text[i:endc].count("\n")
            i = endc + 2
            continue
        if ch == "-" and i + 1 < n and text[i + 1] == "-":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0 and first_neg is None:
                first_neg = line
                print(f"depth went negative at L{line}")
        i += 1
    print(f"final brace depth={depth} (expect 0)")


if __name__ == "__main__":
    main()
