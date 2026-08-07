#!/usr/bin/env python3
"""Safely bump a JAZZ package revision and prepend last_changes bullets."""

from __future__ import annotations

import argparse
import codecs
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", type=Path)
    parser.add_argument("--expected-version", type=int, required=True)
    parser.add_argument("--bullet", action="append", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    metadata = args.package_root.resolve() / "metadata.lua"
    raw = metadata.read_bytes()
    has_bom = raw.startswith(codecs.BOM_UTF8)
    text = raw.decode("utf-8-sig")

    version_pattern = re.compile(r"^(\t'version', )(\d+)(,)(\r?)$", re.MULTILINE)
    matches = list(version_pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"{metadata}: expected one package revision, found {len(matches)}")
    current = int(matches[0].group(2))
    if current != args.expected_version:
        raise ValueError(f"{metadata}: expected revision {args.expected_version}, found {current}")
    patched = version_pattern.sub(
        lambda match: f"{match.group(1)}{current + 1}{match.group(3)}{match.group(4)}",
        text,
        count=1,
    )

    changes_pattern = re.compile(r'^(\t\'last_changes\', ")([^\r\n]*)(",)(\r?)$', re.MULTILINE)
    change_matches = list(changes_pattern.finditer(patched))
    if len(change_matches) != 1:
        raise ValueError(f"{metadata}: last_changes must be one physical Lua line")
    prefix = "".join(f"- {bullet}\\n" for bullet in args.bullet)
    patched = changes_pattern.sub(
        lambda match: f"{match.group(1)}{prefix}{match.group(2)}{match.group(3)}{match.group(4)}",
        patched,
        count=1,
    )

    mode = "apply" if args.apply else "check"
    print(f"mode={mode} package={args.package_root.resolve().name} revision={current}->{current + 1}")
    if args.apply:
        payload = patched.encode("utf-8")
        if has_bom:
            payload = codecs.BOM_UTF8 + payload
        metadata.write_bytes(payload)
        print(f"updated: {metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
