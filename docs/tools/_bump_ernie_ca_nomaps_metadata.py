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
    if "ErnieCounterAttack_NoMaps" not in oldv[:220]:
        t = t[: m2.start(2)] + f"- {bullet}\\n" + oldv + t[m2.end(2) :]
    val = re.search(r"'last_changes', \"(.*)\",", t).group(1)
    if "\n" in val or "\r" in val:
        raise SystemExit(f"raw newline in {path}")
    path.write_text(t, encoding="utf-8", newline="\n")
    print(path.parent.name, old, "->", old + 1)


bump(
    ROOT / "jazz-units" / "metadata.lua",
    "NoMaps: ErnieCounterAttack_NoMaps base 20, no mortar [new game]",
)
bump(
    ROOT / "jazz-nomaps" / "metadata.lua",
    "Remap ErnieCounterAttack -> ErnieCounterAttack_NoMaps (20, no mortar) [new game]",
)
bump(
    ROOT / "jazz" / "metadata.lua",
    "Docs: NoMaps ErnieCounterAttack 20 without mortar [new game]",
)
