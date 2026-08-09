# Bump jazz metadata version + prepend last_changes for STRATEGY-024.
from __future__ import annotations

import re
from pathlib import Path

p = Path("metadata.lua")
t = p.read_text(encoding="utf-8")
m = re.search(r"'version',\s*(\d+)", t)
if not m:
    raise SystemExit("version not found")
ver = int(m.group(1))
t = t[: m.start(1)] + str(ver + 1) + t[m.end(1) :]

bullet = (
    "- STRATEGY-024: Legion support role (sniper/MG/mortar T3-4) "
    "+ squad icon folders [no new game]\\n"
)
m2 = re.search(r"'last_changes',\s*\"", t)
if not m2:
    raise SystemExit("last_changes not found")
idx = m2.end()
t = t[:idx] + bullet + t[idx:]
p.write_text(t, encoding="utf-8")
print(f"version {ver} -> {ver + 1}")

# Hard gate: last_changes value must be one physical line (no raw LF between quotes).
for i, line in enumerate(t.splitlines(), 1):
    if "'last_changes'" in line:
        if line.count('"') < 2:
            raise SystemExit(f"last_changes spans multiple lines at {i}")
        print(f"last_changes OK line {i}")
        break
