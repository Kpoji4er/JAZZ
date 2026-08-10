# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

p = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-nomaps\metadata.lua")
t = p.read_text(encoding="utf-8")
m = re.search(r"'version', (\d+),", t)
old = int(m.group(1))
t = t[: m.start(1)] + str(old + 1) + t[m.end(1) :]
bullet = "FortressDefenders remap -> FortressDefenders_NoMaps (~16) [new game]"
m2 = re.search(r"('last_changes', \")(.*?)(\",)", t)
oldv = m2.group(2)
if "FortressDefenders_NoMaps" not in oldv[:200]:
    t = t[: m2.start(2)] + f"- {bullet}\\n" + oldv + t[m2.end(2) :]
val = re.search(r"'last_changes', \"(.*)\",", t).group(1)
assert "\n" not in val and "\r" not in val
p.write_text(t, encoding="utf-8", newline="\n")
print("nomaps", old, "->", old + 1)
