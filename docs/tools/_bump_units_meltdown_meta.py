# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua")
t = p.read_text(encoding="utf-8")
m = re.search(r"'version', (\d+)", t)
assert m
nv = int(m.group(1)) + 1
t = t.replace(f"'version', {m.group(1)}", f"'version', {nv}", 1)
bullet = (
    "- UNITS-006: Meltdown VengefulTemperament active fear AoE (no RnG) "
    "[no new game] [skip discord]\\n"
)
m2 = re.search(r"('last_changes', \")(.+?)(\",)", t, re.S)
assert m2
body = m2.group(2)
if "active fear AoE (no RnG)" not in body.split("\\n")[0]:
    body = bullet + body
t = t[: m2.start()] + m2.group(1) + body + m2.group(3) + t[m2.end() :]
chunk_start = t.find("'last_changes', \"") + len("'last_changes', \"")
chunk_end = t.find('",', chunk_start)
chunk = t[chunk_start:chunk_end]
if "\n" in chunk or "\r" in chunk:
    raise SystemExit("raw LF")
p.write_text(t, encoding="utf-8")
print("jazz-units version", nv)
