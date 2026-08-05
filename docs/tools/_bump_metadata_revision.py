"""Bump package metadata revision + prepend last_changes bullet (escape \\n only)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("metadata", type=Path)
    ap.add_argument("--bullet", required=True)
    args = ap.parse_args()
    p = args.metadata
    t = p.read_text(encoding="utf-8")
    m = re.search(r"'version', (\d+),", t)
    if not m:
        sys.exit("version not found")
    old, new = int(m.group(1)), int(m.group(1)) + 1
    t = t.replace(f"'version', {old},", f"'version', {new},", 1)

    needle = "'last_changes', \""
    i = t.find(needle)
    if i < 0:
        sys.exit("last_changes not found")
    insert_at = i + len(needle)
    bullet = args.bullet.strip()
    if bullet.startswith("- "):
        bullet = bullet[2:]
    ins = f"- {bullet}\\n"
    t = t[:insert_at] + ins + t[insert_at:]

    seg_m = re.search(r"'last_changes', \"((?:\\.|[^\"\\])*)\"", t)
    if not seg_m:
        sys.exit("last_changes parse failed after edit")
    if "\n" in seg_m.group(1) or "\r" in seg_m.group(1):
        sys.exit("RAW newline inside last_changes — abort")

    p.write_text(t, encoding="utf-8")
    print(f"OK {p}: version {old} -> {new}")


if __name__ == "__main__":
    main()
