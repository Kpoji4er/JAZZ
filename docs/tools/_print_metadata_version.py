"""Print ModDef engine version from metadata.lua.

Root keys only (one tab): not ModDependency version_major/minor.
Engine display matches ModDef:GetVersionString() — ``%d.%02d-%03d``.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_root_version(text: str) -> tuple[int, int, int]:
    def grab(key: str, default: int = 0) -> int:
        match = re.search(rf"(?m)^\t'{key}',\s*(\d+)", text)
        return int(match.group(1)) if match else default

    return grab("version_major"), grab("version_minor"), grab("version")


def format_engine_version(major: int, minor: int, revision: int) -> str:
    return f"{major}.{minor:02d}-{revision:03d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "metadata",
        nargs="?",
        type=Path,
        default=Path("metadata.lua"),
    )
    parser.add_argument(
        "--engine",
        action="store_true",
        help="Print only major.minor-revision (for Discord / dispatch)",
    )
    args = parser.parse_args()
    path = args.metadata
    if not path.is_file():
        print(f"missing {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8-sig")
    major, minor, revision = parse_root_version(text)
    engine = format_engine_version(major, minor, revision)
    if args.engine:
        print(engine)
        return 0
    print(f"{path}: {engine}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
