# -*- coding: utf-8 -*-
"""Quick structural checks for items.lua / metadata.lua (no JA3 required)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def missing_comma_before_placeobj(text: str, name: str) -> list[str]:
    """Catch `})\\nPlaceObj` without comma — Mod Editor: `'}' expected ... near 'PlaceObj'`."""
    problems: list[str] = []
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if not (s.endswith("})") or (s.endswith("}") and not s.endswith("},"))):
            continue
        if s.endswith("}),") or s.endswith("},") or s.endswith("),"):
            continue
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and lines[j].lstrip().startswith("PlaceObj("):
            problems.append(
                f"{name}: L{i+1} closes without comma before PlaceObj at L{j+1}"
            )
    return problems


def check(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    head = text.lstrip()[:80]
    if path.name == "metadata.lua":
        if not (head.startswith("return PlaceObj") or head.startswith("PlaceObj") or "'id'" in head[:200]):
            # ModDef / metadata may start with return PlaceObj('ModDef'...
            if "ModDef" not in text[:500] and "ModContent" not in text[:500]:
                problems.append(f"{path.name}: unexpected start: {head[:40]!r}")
    elif not (head.startswith("return {") or head.startswith("return PlaceObj")):
        problems.append(f"{path.name}: unexpected start")
    lone = [i for i, ln in enumerate(text.splitlines(), 1) if ln.strip() == ","]
    if lone:
        problems.append(f"{path.name}: {len(lone)} lone-comma lines (e.g. {lone[:5]})")
    if "}),)," in text or re.search(r"\}\),\s*\),", text):
        problems.append(f"{path.name}: stacked closers" + " }),),")
    # Exact `}),,` (MagSizeSet split artifact). Avoid `\s*,` — false-positives on normal `}),\n...`.
    if "}),," in text:
        problems.append(f"{path.name}: double-comma after closer" + " }),,")
    if "\\1" in text:
        problems.append(f"{path.name}: regex-replace artifact \\1")
    brace = text.count("{") - text.count("}")
    if brace != 0:
        problems.append(f"{path.name}: brace imbalance {brace}")
    problems.extend(missing_comma_before_placeobj(text, path.name))
    # Corrupt id lines from partial MagLarge_50_AK remove / bad insert
    for i, ln in enumerate(text.splitlines(), 1):
        s = ln.strip()
        if re.match(r"^id\s*=\s*\}\),?\s*$", s) or re.match(r"^id\s*=\s*,?\s*$", s):
            problems.append(f"{path.name}: L{i} corrupt id line: {s!r}")
    return problems


def main() -> int:
    problems: list[str] = []
    for name in ("items.lua", "metadata.lua"):
        problems.extend(check(ROOT / name))
    if problems:
        print("FAIL")
        for p in problems:
            print(" -", p)
        return 1
    print("OK items.lua + metadata.lua structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
