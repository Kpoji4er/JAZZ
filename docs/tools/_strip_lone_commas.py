# -*- coding: utf-8 -*-
"""Strip lone-comma lines from jazz items.lua / metadata.lua."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def strip(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(r"(?m)^[ \t]*,\s*\n", "", text)
    if n:
        tmp = path.with_suffix(path.suffix + ".tmp_lone")
        tmp.write_text(new, encoding="utf-8")
        tmp.replace(path)
    return n


def main() -> int:
    total = 0
    for name in ("items.lua", "metadata.lua"):
        n = strip(ROOT / name)
        print(f"{name}: removed {n}")
        total += n
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
