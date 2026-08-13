#!/usr/bin/env python3
"""Prepend HOTFIX-005 last_changes bullet and bump metadata version."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "metadata.lua"
BULLET = "- HOTFIX-005: identical remountables (bipods) stack in squad bag; no longer vanish on sort/load [no new game]\\n"


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    match = re.search(r"'version', (\d+),", text)
    if not match:
        raise SystemExit("version not found")
    old = int(match.group(1))
    new = old + 1
    text, n = re.subn(r"'version', %d," % old, "'version', %d," % new, text, count=1)
    if n != 1:
        raise SystemExit("version replace failed")
    needle = "'last_changes', \""
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit("last_changes not found")
    insert_at = idx + len(needle)
    text = text[:insert_at] + BULLET + text[insert_at:]
    start = insert_at
    end = text.find('"', start)
    field = text[start:end]
    if "\n" in field.replace("\\n", ""):
        raise SystemExit("raw newline in last_changes")
    PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"version {old} -> {new}")
    print("last_changes head:", field[:160])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
