# -*- coding: utf-8 -*-
from pathlib import Path
import re
t = Path("items.lua").read_text(encoding="utf-8")
for m in re.finditer(r"PlaceObj\('ModItemWeaponComponentEffect'", t):
    block = t[m.start():m.start()+900]
    im = re.search(r'id = "([^"]+)"', block)
    if not im:
        continue
    eid = im.group(1)
    if "Reload" not in eid:
        continue
    dm = re.search(r'Description = T\((\d+),\s*--\[\[.*?\]\]\s*"((?:\\.|[^"\\])*)"', block, re.S)
    print(eid, "->", dm.group(2) if dm else "NO DESC", "tid", dm.group(1) if dm else "-")
