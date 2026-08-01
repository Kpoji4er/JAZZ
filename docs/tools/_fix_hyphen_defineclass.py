# -*- coding: utf-8 -*-
"""Fix DefineClass.Id-With-Hyphen = { ... } → DefineClass(\"Id-With-Hyphen\", { ... })"""
from __future__ import annotations

import re
from pathlib import Path

INV = Path(__file__).resolve().parents[2] / "InventoryItem"
PAT = re.compile(
    r"^DefineClass\.(?P<cid>[A-Za-z0-9_]*-[A-Za-z0-9_-]*)\s*=\s*\{",
    re.M,
)


def fix_text(text: str) -> str | None:
    m = PAT.search(text)
    if not m:
        return None
    cid = m.group("cid")
    text = PAT.sub(f'DefineClass("{cid}", {{', text, count=1)
    # Close with }) instead of bare }
    stripped = text.rstrip()
    if stripped.endswith("})"):
        return text if text.endswith("\n") else text + "\n"
    if stripped.endswith("}"):
        return stripped[:-1] + "})\n"
    return text


def main() -> int:
    n = 0
    for path in sorted(INV.glob("*.lua")):
        original = path.read_text(encoding="utf-8")
        fixed = fix_text(original)
        if fixed is None or fixed == original:
            continue
        path.write_text(fixed, encoding="utf-8", newline="\n")
        print("fixed", path.name)
        n += 1
    print("total", n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
