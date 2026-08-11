# -*- coding: utf-8 -*-
"""Bump jazz metadata version + prepend TheGrim last_changes bullet."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"

BULLET = (
    "- UNITS-006: Reaper TheGrim — recharge after 5 kills (not 1); panic ≤8 kept "
    "[no new game]\\n"
)


def main() -> int:
    t = META.read_text(encoding="utf-8")
    m = re.search(r"'version', (\d+)", t)
    assert m
    nv = int(m.group(1)) + 1
    t = t.replace(f"'version', {m.group(1)}", f"'version', {nv}", 1)
    m2 = re.search(r"('last_changes', \")(.+?)(\",)", t, re.S)
    assert m2
    body = m2.group(2)
    if "Reaper TheGrim" not in body and "TheGrim — recharge" not in body:
        body = BULLET + body
        assert "\n" not in body or body.count("\\n") >= 1
        # ensure no raw newlines inside string value
        if "\n" in body:
            raise SystemExit("raw newline in last_changes")
        t = t[: m2.start()] + m2.group(1) + body + m2.group(3) + t[m2.end() :]
    META.write_text(t, encoding="utf-8")
    print("version", nv)
    print("last_changes head:", body.split("\\n")[0][:120])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
