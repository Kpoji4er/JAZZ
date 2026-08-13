# -*- coding: utf-8 -*-
from pathlib import Path
import re

META = Path("metadata.lua")
text = META.read_text(encoding="utf-8")
m = re.search(r"'version',\s*(\d+)", text)
ver = int(m.group(1)) + 1
text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
bullet = (
    "- UNITS-006: SteroidPunch Passive icon — cool blue from Hud LEFT half "
    "(was cream white) [no new game]\\n"
)
m2 = re.search(r"'last_changes',\s*\"", text)
i = m2.end()
if "SteroidPunch Passive icon — cool blue" not in text[i : i + 220]:
    text = text[:i] + bullet + text[i:]
META.write_text(text, encoding="utf-8")
print("version", ver)
