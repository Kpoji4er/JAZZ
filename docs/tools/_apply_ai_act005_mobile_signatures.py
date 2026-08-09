#!/usr/bin/env python3
"""JAZZ-AI-ACT-005: patch jazz-units AIActionMobileShot keywords.

- Remove RequiredKeywords Control / RunAndGun / MobileShot from AIActionMobileShot
  (weapon AvailableAttacks gate is enough).
- Leave action_id / BiasId as-is; runtime JazzAI_ResolveMobileAttackId overrides.
"""
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
text = UNITS.read_text(encoding="utf-8")


def extract_blocks(src: str, classname: str) -> list[tuple[int, int, str]]:
    needle = f"PlaceObj('{classname}',"
    out = []
    i = 0
    while True:
        j = src.find(needle, i)
        if j < 0:
            break
        k = src.find("{", j)
        depth = 0
        for p in range(k, len(src)):
            if src[p] == "{":
                depth += 1
            elif src[p] == "}":
                depth -= 1
                if depth == 0:
                    out.append((k + 1, p, src[k + 1 : p]))
                    i = p + 1
                    break
        else:
            break
    return out


kw_pat = re.compile(
    r"\n(\t+)'RequiredKeywords',\s*\{\s*(?:\"(?:Control|RunAndGun|MobileShot)\"\s*,?\s*)+\},",
    re.S,
)

changed = 0
# Process from end so offsets stay valid
blocks = extract_blocks(text, "AIActionMobileShot")
new_text = text
for start, end, body in reversed(blocks):
    new_body, n = kw_pat.subn("\n", body)
    # Also remove empty RequiredKeywords left? handled by pattern requiring keywords
    if n:
        changed += n
        new_text = new_text[:start] + new_body + new_text[end:]

if changed:
    UNITS.write_text(new_text, encoding="utf-8", newline="\n")
print(f"removed RequiredKeywords blocks from AIActionMobileShot: {changed}")

# Verify no Control on mobile
left = 0
for _, _, body in extract_blocks(new_text if changed else text, "AIActionMobileShot"):
    if re.search(r"'RequiredKeywords'[\s\S]*?\"Control\"", body):
        left += 1
print(f"AIActionMobileShot still with Control keyword: {left}")
