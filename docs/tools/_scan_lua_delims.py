# -*- coding: utf-8 -*-
"""String/comment-aware delimiter scan for items.lua; report first imbalance."""
from __future__ import annotations

from pathlib import Path

CLOSE_TO_OPEN = {")": "(", "}": "{", "]": "["}


def scan(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    stack: list[tuple[str, int, int]] = []
    line = 1
    col = 0
    i = 0
    n = len(text)
    in_str = None
    escape = False
    long_str = False
    issues: list[str] = []

    while i < n:
        ch = text[i]
        if ch == "\n":
            line += 1
            col = 0
            i += 1
            escape = False
            continue
        col += 1

        if long_str:
            if text.startswith("]]", i):
                long_str = False
                i += 2
                col += 1
            else:
                i += 1
            continue

        if in_str:
            if escape:
                escape = False
                i += 1
                continue
            if ch == "\\":
                escape = True
                i += 1
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue

        if text.startswith("--[[", i):
            end = text.find("]]", i + 4)
            if end < 0:
                issues.append(f"unfinished long comment at {line}:{col}")
                break
            chunk = text[i:end]
            line += chunk.count("\n")
            i = end + 2
            col = 0
            continue
        if text.startswith("--", i):
            nl = text.find("\n", i)
            if nl < 0:
                break
            i = nl
            continue

        if text.startswith("[[", i):
            long_str = True
            i += 2
            col += 1
            continue
        if ch in ("'", '"'):
            in_str = ch
            i += 1
            continue

        if ch in "({[":
            stack.append((ch, line, col))
        elif ch in ")}]":
            if not stack:
                issues.append(f"extra {ch} at {line}:{col}")
            else:
                open_ch, ol, oc = stack.pop()
                if open_ch != CLOSE_TO_OPEN[ch]:
                    issues.append(f"mismatch {open_ch}@{ol}:{oc} vs {ch}@{line}:{col}")
        i += 1

    if in_str:
        issues.append(f"unfinished string {in_str!r} at EOF line {line}")
    if long_str:
        issues.append(f"unfinished long string at EOF line {line}")
    if stack:
        print("unclosed count", len(stack))
        for ch, ol, oc in stack[:20]:
            issues.append(f"unclosed {ch} opened {ol}:{oc}")
    print(path.name, "issues", len(issues))
    for msg in issues[:40]:
        print(" ", msg)


if __name__ == "__main__":
    scan(Path("items.lua"))
    print("---")
    scan(Path("metadata.lua"))
