#!/usr/bin/env python3
"""Compile modified and untracked Lua files in JAZZ package worktrees."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from lupa import LuaRuntime


CORE = Path(__file__).resolve().parents[2]


def dirty_lua_files(root: Path) -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--modified",
            "--others",
            "--exclude-standard",
            "--",
            "*.lua",
        ],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        root / entry.decode("utf-8", errors="surrogateescape")
        for entry in result.stdout.split(b"\0")
        if entry
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, action="append")
    args = parser.parse_args()
    roots = args.package_root or [CORE, CORE.parent / "jazz-maps", CORE.parent / "jazz-units"]

    lua = LuaRuntime(unpack_returned_tuples=True)
    compile_lua = lua.eval(
        "function(source, name) "
        "local chunk, err = load(source, name, 't'); "
        "return chunk ~= nil, err "
        "end"
    )
    failures: list[str] = []
    checked = 0
    for candidate in roots:
        root = candidate.resolve()
        if not (root / ".git").exists():
            continue
        for path in dirty_lua_files(root):
            if not path.is_file():
                continue
            checked += 1
            ok, error = compile_lua(path.read_text(encoding="utf-8-sig"), f"@{path}")
            if not ok:
                failures.append(f"{path}: {error}")

    if failures:
        print(f"FAIL dirty Lua syntax: {len(failures)} of {checked}")
        for failure in failures:
            print(f"  {failure}")
        return 1
    print(f"PASS dirty Lua syntax: {checked} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
