#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ITEMS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
BEGIN = "-- JAZZ-UNITS-005-AME-APP-BEGIN"
END = "-- JAZZ-UNITS-005-AME-APP-END"


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    section = text[text.find(BEGIN) : text.find(END)]
    i = 0
    needle = "PlaceObj('ModItemAppearancePreset'"
    while True:
        start = section.find(needle, i)
        if start < 0:
            break
        brace = section.find("{", start)
        depth = 0
        j = brace
        while j < len(section):
            c = section[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    block = section[start : j + 1]
                    aid = re.search(r'id\s*=\s*"([^"]+)"', block)
                    hat = re.search(r'Hat\s*=\s*"([^"]*)"', block)
                    hat2 = re.search(r'Hat2\s*=\s*"([^"]*)"', block)
                    h1 = hat.group(1) if hat else ""
                    h2 = hat2.group(1) if hat2 else ""
                    if h1 or h2:
                        print(f"{aid.group(1) if aid else '?'}\t{h1}\t{h2}")
                    i = j + 1
                    break
            j += 1
        else:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
