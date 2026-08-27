#!/usr/bin/env python3
"""Fail if two suite Code files wrap the same Class:Method or global.

Catches the stack-overflow cycle: wrap A saves wrap B as base, wrap B
still calls wrap A (ModsReloaded / DataLoaded re-base).

Allowlisted intentional chains must stay install-once / never re-base.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
CODE_DIRS = [
    JAZZ / "Code",
    JAZZ.parent / "jazz-units" / "Code",
    JAZZ.parent / "jazz-maps" / "Code",
    JAZZ.parent / "jazz-nomaps" / "Code",
]

# Existing multi-file chains only. Do not add another wrap. Prefer merging.
# New dual owners of one symbol must FAIL, not be silently added here.
ALLOW = {
    ("UnitMarker", "SpawnObjects"): "RIS + NoMaps; RIS never re-bases",
    ("Unit", "OnAttack"): "SigRecharge + ExplodingPalm; both install-once",
    ("NetSyncEvents", "MarkEmailAsRead"): "AME/MERC/RIS mail; do not add a fourth",
}

ASSIGN_CLS = re.compile(
    r"(?:local\s+)?(\w+)\s*=\s*rawget\(\s*_G\s*,\s*['\"](\w+)['\"]\s*\)"
)
FUNC_METHOD = re.compile(r"^function\s+(\w+)\s*:\s*(\w+)\s*\(")
FUNC_GLOBAL = re.compile(r"^function\s+([A-Z][\w]*)\s*\(")
ASSIGN_SLOT = re.compile(r"(\w+)\s*\.\s*(\w+)\s*=\s*(\w+)\s*$")
BASE_IN_BODY = re.compile(
    r"(?:g_JAZZ_\w+Base|JAZZ_\w+Base|\w+(?:Execute|Spawn|Fn)?Base)\s*[\(\.]"
    r"|rawget\(\s*_G\s*,\s*['\"][^'\"]*Base['\"]"
)
WRAP_RHS = re.compile(
    r"^(wrap|lWrapped\w*|g_JAZZ_\w+(?:Fn|Wrap)|JAZZ_\w+Wrap)$"
    r"|Wrap$|wrap$"
)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(JAZZ.parent)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _is_wrap_rhs(name: str) -> bool:
    return bool(WRAP_RHS.search(name))


def _scan_file(path: Path) -> list[tuple[str, str, int]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    locals_to_class: dict[str, str] = {}
    found: list[tuple[str, str, int]] = []

    for i, raw in enumerate(lines):
        line = raw.strip()
        m = ASSIGN_CLS.search(line)
        if m:
            locals_to_class[m.group(1)] = m.group(2)

        m = FUNC_METHOD.match(line)
        if m:
            window = "\n".join(lines[i : i + 80])
            if BASE_IN_BODY.search(window):
                found.append((m.group(1), m.group(2), i + 1))
            continue

        m = FUNC_GLOBAL.match(line)
        if m and not line.startswith("function OnMsg"):
            window = "\n".join(lines[i : i + 80])
            if BASE_IN_BODY.search(window):
                found.append(("_G", m.group(1), i + 1))
            continue

        m = ASSIGN_SLOT.search(line)
        if m and _is_wrap_rhs(m.group(3)):
            cls = locals_to_class.get(m.group(1), m.group(1))
            if cls[:1].isupper() or m.group(1) in locals_to_class:
                found.append((cls, m.group(2), i + 1))

    return found


def main() -> int:
    sites: dict[tuple[str, str], list[tuple[str, int]]] = defaultdict(list)
    for folder in CODE_DIRS:
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.lua")):
            for cls, method, line in _scan_file(path):
                sites[(cls, method)].append((_rel(path), line))

    failures = []
    for key, hits in sorted(sites.items()):
        files = {p for p, _ in hits}
        if len(files) < 2:
            continue
        reason = ALLOW.get(key)
        shown = ", ".join(f"{p}:{ln}" for p, ln in hits)
        if reason:
            print(f"ALLOW {key[0]}:{key[1]} ({reason}) — {shown}")
            continue
        failures.append(f"FAIL {key[0]}:{key[1]} wrapped in {len(files)} files — {shown}")

    if failures:
        print("Dual wraps on one symbol re-base into a cycle (Call stack too big).")
        print("Hook the existing wrap; do not add a second. Allowlist only install-once chains.")
        for row in failures:
            print(row)
        return 1

    n = sum(len(v) for v in sites.values())
    print(f"OK wrap-cycle check ({n} wrap site(s), no unallowed dual owners)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
