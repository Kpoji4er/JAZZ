#!/usr/bin/env python3
"""Bump package metadata version (+1) and prepend last_changes bullet (escaped \\n)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def bump(path: Path, bullet: str, version_minor: int | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    versions = list(re.finditer(r"'version', (\d+),", text))
    if not versions:
        raise SystemExit(f"no version in {path}")

    if version_minor is not None:
        # Prefer the version that follows the given version_minor nearby.
        chosen = None
        for m in versions:
            window = text[max(0, m.start() - 80) : m.start()]
            if f"'version_minor', {version_minor}," in window:
                chosen = m
                break
        target = chosen or versions[-1]
    else:
        target = versions[-1]

    old = int(target.group(1))
    new = old + 1
    text = text[: target.start()] + f"'version', {new}," + text[target.end() :]

    m2 = re.search(r"'last_changes', \"((?:\\.|[^\"\\])*)\"\s*,", text)
    if not m2:
        raise SystemExit(f"last_changes not found in {path}")
    # Write literal backslash-n into the Lua string (two chars: \ and n)
    insert = f"- {bullet}\\n"
    text = text[: m2.start(1)] + insert + m2.group(1) + text[m2.end(1) :]

    # Ensure no raw newline inside last_changes quotes
    m3 = re.search(r"'last_changes', \"", text)
    assert m3
    end = text.find('"', m3.end())
    chunk = text[m3.end() : end]
    if "\n" in chunk or "\r" in chunk:
        raise SystemExit("raw newline leaked into last_changes")

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"{path}: version {old} -> {new}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("metadata")
    ap.add_argument("bullet")
    ap.add_argument("--version-minor", type=int, default=None)
    args = ap.parse_args()
    bump(Path(args.metadata), args.bullet, args.version_minor)


if __name__ == "__main__":
    main()
