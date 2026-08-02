# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
t = p.read_text(encoding="utf-8")
print("before brace diff", t.count("{") - t.count("}"))

# Fix }}), -> }), on JAZZ med loot one-liners
pat = re.compile(
    r'(PlaceObj\(\'LootEntryInventoryItem\', \{ item = "JAZZ_(?:Bandage|Morphine|SurgicalKit)"[^}]*?)\}\}\),'
)
nt, n = pat.subn(r"\1}),", t)
print("fixed double-close", n)

# Also fix any remaining `}}),` that are only on those lines
nt2, n2 = re.subn(
    r'(item = "JAZZ_(?:Bandage|Morphine|SurgicalKit)"[^\n]*?)\}\}\),',
    r"\1}),",
    nt,
)
print("fixed alt", n2)
print("after brace diff", nt2.count("{") - nt2.count("}"))
for line in nt2.splitlines():
    if "JAZZ_Bandage" in line:
        print(repr(line.strip()[:140]))
        break
p.write_text(nt2, encoding="utf-8")
