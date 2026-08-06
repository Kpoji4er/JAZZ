# -*- coding: utf-8 -*-
"""Dump all RIS-related Russian strings for artistic review."""
import csv
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]


def load(path):
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("sep="):
        text = text.split("\n", 1)[1]
    return {r[0]: r for r in csv.reader(io.StringIO(text)) if r}


def main():
    ru = load(ROOT / "Russian.csv")
    # Collect RIS loc ids from Code + items
    ids = set()
    for p in [
        ROOT / "Code/System_RIS_Content.lua",
        ROOT / "Code/System_RIS_Mail.lua",
        ROOT / "Code/System_RIS_Browser.lua",
        ROOT / "Code/System_RIS_Combat.lua",
        ROOT / "items.lua",
    ]:
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        # RIS-related T ids near RIS comments or RIS_ strings
        for m in re.finditer(r"T\((\d{12,})", t):
            tid = m.group(1)
            # keep if in RIS band or tagged JAZZ-UI-RIS in csv
            row = ru.get(tid)
            if not row:
                continue
            tag = row[4] if len(row) > 4 else ""
            if "RIS" in tag or tid.startswith("890000000011") or tid.startswith("8900000000069"):
                ids.add(tid)
    # Also all CSV rows tagged RIS
    for tid, row in ru.items():
        tag = row[4] if len(row) > 4 else ""
        if "RIS" in tag:
            ids.add(tid)

    def cyr(s):
        return any("\u0400" <= ch <= "\u04FF" for ch in s)

    print(f"ids={len(ids)}")
    for tid in sorted(ids, key=lambda x: int(x)):
        row = ru.get(tid)
        if not row:
            print(f"\n=== {tid} MISSING")
            continue
        c1, c2 = row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else ""
        text = c2 if cyr(c2) else (c1 if cyr(c1) else c2 or c1)
        print(f"\n=== {tid} tag={row[4] if len(row)>4 else ''}")
        print(text)


if __name__ == "__main__":
    main()
