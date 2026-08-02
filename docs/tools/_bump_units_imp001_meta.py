# -*- coding: utf-8 -*-
"""Bump jazz-units metadata revision for IMP_equipment_basic placeholder change."""
from pathlib import Path
import re

path = Path(r"C:/Users/SsAnd/AppData/Roaming/Jagged Alliance 3/Mods/jazz-units/metadata.lua")
text = path.read_text(encoding="utf-8")
m = re.search(r"'version',\s*(\d+)", text)
if not m:
    raise SystemExit("version not found")
ver = int(m.group(1))
text = text.replace(m.group(0), f"'version', {ver + 1}", 1)
bullet = "- IMP-001: IMP_equipment_basic campaign placeholder (hire rebuilds dynamic gear) [new game recommended]\n"
lc = re.search(r"'last_changes',\s*\"", text)
if not lc:
    raise SystemExit("last_changes not found")
start = lc.end()
if "IMP-001:" not in text[start : start + 400]:
    text = text[:start] + bullet + text[start:]
path.write_text(text, encoding="utf-8")
print("units version", ver, "->", ver + 1)
