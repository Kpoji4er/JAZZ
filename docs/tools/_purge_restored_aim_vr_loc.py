# -*- coding: utf-8 -*-
"""Safely drop orphaned 8900* AIM-VR loc rows without rewriting whole CSV."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
MERCS = ("Raven", "Thor", "Vicki", "Wolf")
OLD_REV = "bb6d97a^"


def git_show(rev: str, rel: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{rev}:{rel}"],
        cwd=UNITS,
        encoding="utf-8",
        errors="replace",
    )


def extract_vr_block(text: str, merc: str) -> str:
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',\s*\{", text):
        start = m.start()
        window = text[start : start + 300000]
        gm = re.search(r'group = "MercenariesOld",\s*id = "([^"]+)"', window)
        if gm and gm.group(1) == merc:
            return window[: gm.end()]
    raise RuntimeError(merc)


def tids(block: str) -> list[str]:
    return re.findall(r"T\((\d+),", block)


def orphan_mod_ids() -> set[str]:
    old = git_show(OLD_REV, "items.lua")
    cur = (UNITS / "items.lua").read_text(encoding="utf-8")
    orphan: set[str] = set()
    for merc in MERCS:
        for o, n in zip(tids(extract_vr_block(old, merc)), tids(extract_vr_block(cur, merc))):
            # After restore, cur has vanilla ids; orphan keys are the 8900 that were removed from items
            pass
    # Rebuild from commit pair instead
    new = git_show("bb6d97a", "items.lua")
    for merc in MERCS:
        for o, n in zip(tids(extract_vr_block(old, merc)), tids(extract_vr_block(new, merc))):
            if o != n and n.startswith("8900"):
                orphan.add(n)
    return orphan


def quote_parity(s: str) -> int:
    """Count unescaped quotes roughly for CSV row continuation."""
    return s.count('"') % 2


def purge_csv(path: Path, orphan: set[str]) -> int:
    raw = path.read_text(encoding="utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.splitlines()
    out: list[str] = []
    i = 0
    removed = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\d+),", line)
        if m and m.group(1) in orphan:
            # skip full logical CSV record (may be multiline)
            chunk = [line]
            odd = quote_parity(line)
            i += 1
            while odd and i < len(lines):
                chunk.append(lines[i])
                odd ^= quote_parity(lines[i])
                i += 1
            removed += 1
            continue
        out.append(line)
        i += 1
    path.write_text(newline.join(out) + (newline if raw.endswith(("\n", "\r\n")) else ""), encoding="utf-8")
    return removed


def main() -> None:
    orphan = orphan_mod_ids()
    print(f"orphan 8900 ids: {len(orphan)}")
    # ensure none still referenced in items.lua
    items = (UNITS / "items.lua").read_text(encoding="utf-8")
    still = [oid for oid in orphan if oid in items]
    if still:
        raise SystemExit(f"still referenced in items.lua: {still[:5]}")
    for path in (JAZZ / "Russian.csv", JAZZ / "English.csv", UNITS / "English.csv"):
        if path.exists():
            n = purge_csv(path, orphan)
            print(f"{path}: removed {n}")


if __name__ == "__main__":
    main()
