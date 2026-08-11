# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path("metadata.lua")
t = p.read_text(encoding="utf-8")
t = t.replace("panic ?8", "panic <=8").replace("panic ≤8", "panic <=8")

sig = (
    "- UNITS-006: Lynx/Buzz/Spider/Colby Passive hotbar icons "
    "(SignatureAbilities 108x54) [no new game]\\n"
)
m = re.search(r"('last_changes', \")(.+?)(\",)", t, re.S)
assert m
body = m.group(2)
if "SignatureAbilities 108x54" not in body:
    first, sep, rest = body.partition("\\n")
    body = first + "\\n" + sig.rstrip("\\n") + (("\\n" + rest) if sep else "")
t = t[: m.start()] + m.group(1) + body + m.group(3) + t[m.end() :]

chunk_start = t.find("'last_changes', \"") + len("'last_changes', \"")
chunk_end = t.find('",', chunk_start)
chunk = t[chunk_start:chunk_end]
if "\n" in chunk or "\r" in chunk:
    raise SystemExit("raw LF in last_changes")

p.write_text(t, encoding="utf-8")
print("ok")
for line in body.split("\\n")[:4]:
    print(line)
