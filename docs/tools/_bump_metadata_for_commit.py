"""Append a last_changes bullet and bump Revision in metadata.lua.

Usage (from jazz package root, or pass --path):
  python docs/tools/_bump_metadata_for_commit.py "IMP-001: HList spacing 12 + ImpCalcAnswers sanitize"
  python docs/tools/_bump_metadata_for_commit.py --path ../jazz-units/metadata.lua "UNITS-005: ..."

Writes literal backslash-n between bullets (never raw LF inside the Lua string).
Does not touch saved/code_hash.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def bump(path: Path, bullet: str) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+),", text)
    if not m:
        raise SystemExit(f"version field not found in {path}")
    old_v = int(m.group(1))
    new_v = old_v + 1
    text = text.replace(f"'version', {old_v},", f"'version', {new_v},", 1)

    bullet = bullet.strip().lstrip("- ").strip()
    if not bullet:
        raise SystemExit("empty bullet")
    # Python string with \\n → file gets two chars \ and n (Lua escape).
    insert = f"- {bullet}\\n"
    needle = "'last_changes', \""
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit(f"last_changes not found in {path}")
    insert_at = idx + len(needle)
    text = text[:insert_at] + insert + text[insert_at:]

    # Guard: no raw newline between the opening quote of last_changes and its closer.
    start = insert_at - 1  # opening "
    end = text.find('",', start + 1)
    if end < 0:
        raise SystemExit("could not find end of last_changes string")
    segment = text[start : end + 1]
    if "\n" in segment or "\r" in segment:
        raise SystemExit("REFUSING: raw LF/CR inside last_changes quotes")

    path.write_text(text, encoding="utf-8", newline="\n")
    return old_v, new_v


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bullet", help="last_changes bullet text (without leading '- ')")
    ap.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "metadata.lua",
        help="path to metadata.lua (default: jazz/metadata.lua)",
    )
    args = ap.parse_args()
    path = args.path.resolve()
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    old_v, new_v = bump(path, args.bullet)
    print(f"{path}: version {old_v} -> {new_v}; prepended last_changes bullet")


if __name__ == "__main__":
    main()
