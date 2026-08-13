# -*- coding: utf-8 -*-
"""Bump jazz Revision + prepend BulletHell recharge_on_kill cache fix bullet."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"
BULLET = (
    "- UNITS-006: Spike BulletHell CD on kill (fix g_PresetParamCache for recharge_on_kill) "
    "[no new game]"
)


def main() -> None:
    t = META.read_text(encoding="utf-8")
    m = re.search(r"'version', (\d+)", t)
    if not m:
        raise SystemExit("version not found")
    ver = int(m.group(1))
    t = t.replace(f"'version', {ver}", f"'version', {ver + 1}", 1)

    m2 = re.search(r"""('last_changes', ")(.+?)(",)""", t, flags=re.S)
    if not m2:
        raise SystemExit("last_changes not found")
    body = m2.group(2)
    insert = BULLET + "\\n"
    if not body.startswith(BULLET):
        body = insert + body
    t = t[: m2.start(2)] + body + t[m2.end(2) :]

    m3 = re.search(r"""'last_changes', "(.+?)",""", t, flags=re.S)
    assert m3
    chunk = m3.group(1)
    if "\n" in chunk or "\r" in chunk:
        raise SystemExit("raw LF/CR inside last_changes")

    META.write_text(t, encoding="utf-8")
    print(f"version {ver} -> {ver + 1}")
    print("head:", chunk[:160])


if __name__ == "__main__":
    main()
