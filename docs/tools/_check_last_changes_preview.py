"""Preview jazz metadata last_changes after Steam replace."""
from __future__ import annotations

import re
from pathlib import Path

text = Path("metadata.lua").read_text(encoding="utf-8-sig")
m = re.search(r"'last_changes',\s*\"((?:\\.|[^\"\\])*)\"", text)
if not m:
    raise SystemExit("last_changes not found")
s = m.group(1)
raw = ("\n" in s) or ("\r" in s)
print("raw_newline", raw)
print("bullets", s.count("\\n") + 1)
print("---")
print(s.replace("\\n", "\n"))
