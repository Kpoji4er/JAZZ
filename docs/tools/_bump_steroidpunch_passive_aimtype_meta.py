# -*- coding: utf-8 -*-
"""Bump metadata for SteroidPunch Passive AimType=none (no melee-range rollover error)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"


def main() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    ver = int(m.group(1)) + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    bullet = (
        "- UNITS-006: SteroidPunch Passive — AimType none (drop melee-range rollover error) "
        "[no new game]\\n"
    )
    m2 = re.search(r"'last_changes',\s*\"", text)
    i = m2.end()
    if "SteroidPunch Passive — AimType none" not in text[i : i + 200]:
        text = text[:i] + bullet + text[i:]
    META.write_text(text, encoding="utf-8")
    print(f"metadata version -> {ver}")


if __name__ == "__main__":
    main()
