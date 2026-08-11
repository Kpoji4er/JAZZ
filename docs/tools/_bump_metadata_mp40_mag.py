# -*- coding: utf-8 -*-
"""Bump jazz + jazz-units metadata for MP40 MagNormal-only commit."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\metadata.lua")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua")

BULLET_JAZZ = "- MP40: MagNormal-only (32); drop MagLarge_50 + LoadGame reseat [no new game]"
BULLET_UNITS = "- MP40 GenW loot: drop MagLarge_50 (fixed MagNormal 32) [no new game] [skip discord]"


def bump(path: Path, bullet: str, old_ver: int, new_ver: int) -> None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"'last_changes', \"", text)
    if not m:
        raise SystemExit(f"no last_changes in {path}")
    after = text[m.end() :]
    if after.startswith(bullet):
        print(f"{path.parent.name}: bullet already present")
    else:
        text = text[: m.end()] + bullet + "\\n" + text[m.end() :]

    text2, n = re.subn(
        rf"('version', ){old_ver},",
        rf"\g<1>{new_ver},",
        text,
        count=1,
    )
    if n != 1:
        # already bumped?
        if re.search(rf"'version', {new_ver},", text):
            text2 = text
            print(f"{path.parent.name}: version already {new_ver}")
        else:
            raise SystemExit(f"version bump failed in {path}: n={n} want {old_ver}->{new_ver}")

    m2 = re.search(r"'last_changes', \"(.*?)\"\s*,", text2, re.S)
    if not m2:
        raise SystemExit("last_changes parse fail")
    body = m2.group(1)
    if "\n" in body or "\r" in body:
        raise SystemExit(f"RAW newline inside last_changes in {path}")
    if not body.startswith(bullet):
        raise SystemExit(f"bullet not at start in {path}: {body[:100]!r}")
    path.write_text(text2, encoding="utf-8", newline="\n")
    print(f"OK {path.parent.name}: version {old_ver}->{new_ver}")


bump(JAZZ, BULLET_JAZZ, 6118, 6119)
bump(UNITS, BULLET_UNITS, 2306, 2307)
