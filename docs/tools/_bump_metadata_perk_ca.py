# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path("metadata.lua")
t = p.read_text(encoding="utf-8")
m = re.search(r"'version', (\d+)", t)
assert m
nv = int(m.group(1)) + 1
t = t.replace(f"'version', {m.group(1)}", f"'version', {nv}", 1)
bullet = "- HOTFIX: Jazz_Perk_* Passive SignatureAbilities CombatAction companions on hotbar [no new game]\\n"
# last_changes value is a single Lua string with \\n escapes
pat = re.compile(r"('last_changes', \")(.+?)(\",)", re.S)
m2 = pat.search(t)
assert m2, "last_changes not found"
body = m2.group(2)
if "Passive SignatureAbilities CombatAction" not in body:
    body = bullet + body
    # ensure no raw newlines inside the string
    assert "\n" not in body or body.count("\\n") >= 1
    t = t[: m2.start()] + m2.group(1) + body + m2.group(3) + t[m2.end() :]
p.write_text(t, encoding="utf-8", newline="\n")
print("version", nv)
# verify no raw LF inside last_changes quotes
lc = re.search(r"'last_changes', \"([^\"]*)\"", t)
assert lc and "\n" not in lc.group(1)
print("last_changes OK")
