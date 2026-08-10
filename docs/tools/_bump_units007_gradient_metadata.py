# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")


def bump(path: Path, bullet: str) -> None:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"'version', (\d+),", t)
    old = int(m.group(1))
    t = t[: m.start(1)] + str(old + 1) + t[m.end(1) :]
    m2 = re.search(r"('last_changes', \")(.*?)(\",)", t)
    oldv = m2.group(2)
    if bullet[:20] in oldv[:180]:
        print(path.name, old, "->", old + 1, "(bullet exists)")
    else:
        t = t[: m2.start(2)] + f"- {bullet}\\n" + oldv + t[m2.end(2) :]
        print(path.name, old, "->", old + 1)
    val = re.search(r"'last_changes', \"(.*)\",", t).group(1)
    if "\n" in val or "\r" in val:
        raise SystemExit("raw newline")
    path.write_text(t, encoding="utf-8", newline="\n")


bump(
    ROOT / "jazz-units" / "metadata.lua",
    "UNITS-007: T1-T2 island role coverage; T2 lean near I7; Fortress FlankerT3_Recon [new game]",
)
bump(
    ROOT / "jazz" / "metadata.lua",
    "UNITS-007: island T1-T2 role gradient toward I7 + rare T3 on keys [new game]",
)
