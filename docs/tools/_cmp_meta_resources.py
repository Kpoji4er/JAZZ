# -*- coding: utf-8 -*-
import subprocess
import re
from pathlib import Path

def presets(raw: bytes) -> set[tuple[str, str]]:
    text = raw.decode("utf-8-sig")
    # Class + Id pairs
    pairs = re.findall(
        r"'Class',\s*\"([^\"]+)\"\s*,\s*\n\s*'Id',\s*\"([^\"]+)\"",
        text,
    )
    return set(pairs)

head = subprocess.check_output(["git", "show", "HEAD:metadata.lua"])
cur = Path("metadata.lua").read_bytes()
h, c = presets(head), presets(cur)
print("HEAD pairs", len(h), "CUR", len(c))
print("added", len(c - h))
for p in sorted(c - h)[:40]:
    print(" +", p)
print("removed", len(h - c))
for p in sorted(h - c)[:40]:
    print(" -", p)
