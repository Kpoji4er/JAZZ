#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List ChanceToHitModifier RequireActionType in items.lua CTHMod folder."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / "items.lua").read_text(encoding="utf-8", errors="replace")

# Narrow to CTHMod folder if present
start = text.find("'name', \"CTHMod\"")
if start < 0:
	start = 0
chunk = text[start:]

pat = re.compile(
	r"PlaceObj\('ModItemChanceToHitModifier',\s*\{(?P<body>.*?)\n\t\t\t\}\),",
	re.S,
)
for m in pat.finditer(chunk):
	body = m.group("body")
	mid = re.search(r'id = "([^"]+)"', body)
	if not mid:
		continue
	req = re.search(r'RequireActionType = "([^"]+)"', body)
	print(f"{mid.group(1):40s} RequireActionType={req.group(1) if req else 'MISSING'}")
