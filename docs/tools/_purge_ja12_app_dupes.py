# -*- coding: utf-8 -*-
"""Remove ModItemAppearancePreset blocks for given ids that appear BEFORE JA12-APP section."""
import re
from pathlib import Path

ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
MARK = "-- JAZZ-UNITS-002-JA12-APP-BEGIN"
IDS = {"Mike", "Horg"}

text = ITEMS.read_text(encoding="utf-8")
cut = text.find(MARK)
if cut < 0:
    raise SystemExit("JA12 mark missing")
head, tail = text[:cut], text[cut:]

# Find PlaceObj('ModItemAppearancePreset', { ... }), that contain id = "X"
pattern = re.compile(
    r"\t\tPlaceObj\('ModItemAppearancePreset',\s*\{[\s\S]*?\n\t\t\}\),?\n?",
    re.M,
)

removed = []
kept_parts = []
last = 0
for m in pattern.finditer(head):
    block = m.group(0)
    idm = re.search(r'\bid\s*=\s*"([^"]+)"', block)
    pid = idm.group(1) if idm else None
    if pid in IDS:
        kept_parts.append(head[last : m.start()])
        last = m.end()
        removed.append(pid)
        print(f"remove {pid} @ {m.start()}")
kept_parts.append(head[last:])
new_head = "".join(kept_parts)
# collapse excessive blank lines
new_head = re.sub(r"\n{4,}", "\n\n\n", new_head)
ITEMS.write_text(new_head + tail, encoding="utf-8")
print("removed", removed, "size", ITEMS.stat().st_size)
