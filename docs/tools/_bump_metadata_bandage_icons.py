# -*- coding: utf-8 -*-
"""Bump jazz/metadata.lua version + append last_changes (escape \\n only)."""
from __future__ import annotations

import re
from pathlib import Path

p = Path("metadata.lua")
text = p.read_text(encoding="utf-8")

m = re.search(r"'version',\s*(\d+)", text)
assert m
ver = int(m.group(1))
text = text[: m.start(1)] + str(ver + 1) + text[m.end(1) :]

# last_changes: 'last_changes', "....\n...."
pat = re.compile(r"""('last_changes',\s*)\"((?:\\.|[^\"\\])*)\"""")
mm = pat.search(text)
assert mm, "last_changes not found"
bullet = (
	"- MED-001: field bandage spends one per bleed stack; "
	"stock/flash HUD glyphs + stock ChipIcon flat glyphs [no new game]\\n"
)
new_val = bullet + mm.group(2)
text = text[: mm.start()] + mm.group(1) + '"' + new_val + '"' + text[mm.end() :]

for line in text.splitlines():
	if "'last_changes'" in line:
		assert "\n" not in line[line.find("'last_changes'") + 1 :]
		print("last_changes single-line OK")
		break
else:
	raise SystemExit("last_changes line missing after edit")

p.write_text(text, encoding="utf-8")
print(f"version {ver} -> {ver + 1}")
