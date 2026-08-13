# -*- coding: utf-8 -*-
"""Bump jazz metadata revision + prepend HOTFIX-007 / Grizzly last_changes."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"

BULLET = (
    "- HOTFIX-007: 12g salt fills Pain to cap on hit; "
    "GrizzlyPerk stock HUD icon + recharge_on_kill=1 [no new game]\\n"
)


def main() -> int:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version', (\d+),", text)
    if not m:
        print("FAIL: version")
        return 1
    v = int(m.group(1))
    text = text.replace(f"'version', {v},", f"'version', {v + 1},", 1)
    marker = "'last_changes', \""
    i = text.find(marker)
    if i < 0:
        print("FAIL: last_changes")
        return 1
    j = i + len(marker)
    if "HOTFIX-007: 12g salt" not in text[j : j + 200]:
        text = text[:j] + BULLET + text[j:]
    # ensure no raw LF inside last_changes quotes
    end = text.find('",', j)
    chunk = text[j:end]
    if "\n" in chunk or "\r" in chunk:
        print("FAIL: raw newline in last_changes")
        return 1
    META.write_text(text, encoding="utf-8", newline="\n")
    print(f"OK version {v}->{v + 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
