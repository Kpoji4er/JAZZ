#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check AME blue accents are not on Hat/Hat2."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ITEMS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
BEGIN = "-- JAZZ-UNITS-005-AME-APP-BEGIN"
END = "-- JAZZ-UNITS-005-AME-APP-END"


def is_blue(r, g, b):
    return b >= 90 and b > r + 20 and b >= g


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    section = text[text.find(BEGIN) : text.find(END)]
    bad = []
    for part in ("HatColor", "Hat2Color"):
        for m in re.finditer(
            rf"{part}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{([\s\S]*?)\}}\)",
            section,
        ):
            body = m.group(1)
            for cm in re.finditer(
                r"'EditableColor(\d+)',\s*RGBA\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)",
                body,
            ):
                ch, r, g, b = int(cm.group(1)), int(cm.group(2)), int(cm.group(3)), int(cm.group(4))
                if is_blue(r, g, b):
                    bad.append((part, ch, r, g, b))
    print(f"blue_on_hat_channels={len(bad)}")
    for x in bad[:10]:
        print(" ", x)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
