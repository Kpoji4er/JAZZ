# -*- coding: utf-8 -*-
"""Prepend bullets to metadata.lua last_changes without inserting raw newlines."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def find_last_changes_span(text: str) -> tuple[int, int, str]:
    key = "'last_changes', "
    i = text.find(key)
    if i < 0:
        raise ValueError("no last_changes")
    q = i + len(key)
    quote = text[q]
    if quote not in ("'", '"'):
        raise ValueError(f"unexpected quote {quote!r}")
    j = q + 1
    while j < len(text):
        if text[j] == "\\":
            j += 2
            continue
        if text[j] == quote:
            return q + 1, j, quote
        if text[j] in "\r\n":
            raise ValueError("raw newline inside last_changes")
        j += 1
    raise ValueError("unclosed last_changes")


def prepend_last_changes(path: Path, bullets: list[str], bump_version: int | None) -> None:
    text = path.read_text(encoding="utf-8")
    start, end, _quote = find_last_changes_span(text)
    old = text[start:end]
    prefix = "".join(f"- {b}\\n" for b in bullets)
    text = text[:start] + prefix + old + text[end:]
    if bump_version is not None:
        text, n = re.subn(r"(?m)^(\t'version', )\d+,", rf"\g<1>{bump_version},", text, count=1)
        if n != 1:
            raise ValueError(f"version replace failed: {n}")
    find_last_changes_span(text)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--bullet", action="append", required=True)
    parser.add_argument("--version", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prepend_last_changes(args.metadata, args.bullet, args.version)
    print(f"OK {args.metadata} version={args.version}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"FAIL: {exc}\n")
        raise SystemExit(1)
