"""Print ModDef version triple from metadata.lua."""
from __future__ import annotations

import re
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "metadata.lua")
text = path.read_text(encoding="utf-8-sig")
# First occurrence of each key after ModDef start is the package version
out = {}
for key in ("version_major", "version_minor", "version"):
    m = re.search(rf"'{key}',\s*(\d+)", text)
    out[key] = m.group(1) if m else "?"
print(f"{path}: {out['version_major']}.{out['version_minor']}-{out['version']}")
