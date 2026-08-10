# -*- coding: utf-8 -*-
"""Bump package metadata version + append last_changes bullet (escaped \\n)."""
from __future__ import annotations

import re
from pathlib import Path


def bump(path: Path, bullet: str) -> None:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"'version', (\d+),", t)
    if not m:
        raise SystemExit(f"no version in {path}")
    old = int(m.group(1))
    t = t[: m.start(1)] + str(old + 1) + t[m.end(1) :]

    m2 = re.search(r"('last_changes', \")(.*?)(\",)", t)
    if not m2:
        raise SystemExit(f"no last_changes in {path}")
    oldv = m2.group(2)
    if "UNITS-007" in oldv[:200]:
        print(f"{path.name}: version {old}->{old+1}, last_changes already has UNITS-007")
    else:
        # write literal backslash-n into file content
        ins = f"- {bullet}\\n"
        t = t[: m2.start(2)] + ins + oldv + t[m2.end(2) :]
        print(f"{path.name}: version {old}->{old+1}, appended last_changes")

    m3 = re.search(r"'last_changes', \"(.*)\",", t)
    val = m3.group(1)
    if "\n" in val or "\r" in val:
        raise SystemExit(f"RAW newline in last_changes: {path}")
    path.write_text(t, encoding="utf-8", newline="\n")


ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")
bump(
    ROOT / "jazz" / "metadata.lua",
    "UNITS-007: Ernie Init overflow cut + E/N/H gated packs + FortressDefenders 48 [new game]",
)
bump(
    ROOT / "jazz-units" / "metadata.lua",
    "UNITS-007: Ernie Medium/Large/Extra packs + FortressDefenders 48 E/N/H [new game]",
)
bump(
    ROOT / "jazz-maps" / "metadata.lua",
    "UNITS-007: Ernie overflow InitialSquads rewire (M4-M6/I2-I4/L1-L2/L6/I7) [new game]",
)
