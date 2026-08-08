#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ITEMS = Path(__file__).resolve().parents[2].parent / "jazz-units" / "items.lua"
text = ITEMS.read_text(encoding="utf-8")
# find JAZZ_AME_17 block
m = re.search(
    r"PlaceObj\('ModItemAppearancePreset',\s*\{(.*?)\bid\s*=\s*\"JAZZ_AME_17\"",
    text,
    re.S,
)
if not m:
    # id at end — search backwards
    idx = text.find('id = "JAZZ_AME_17"')
    print("idx", idx)
    chunk = text[idx - 2500 : idx + 80]
else:
    chunk = m.group(0)[-2500:]
print(chunk)
