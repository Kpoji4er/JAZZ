#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Allocate the next unused JAZZ mod-only localization ID in 890000000000000..890000000099999.

Scans jazz/jazz-maps/jazz-units T() IDs plus Russian.csv, English.csv, Localization/*.csv.
Does not recurse jazz-maps/Maps/.

Usage (from jazz/):
  python docs/tools/_alloc_mod_loc_id.py
  python docs/tools/_alloc_mod_loc_id.py --check 890000000006500
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

RANGE_START = 890000000000000
RANGE_END = 890000000099999
T_ID = re.compile(r"\bT(?:\{|\()\s*(\d{12,18})\b")

JAZZ = Path(__file__).resolve().parents[2]
MODS = JAZZ.parent
PACKAGES = [JAZZ, MODS / "jazz-maps", MODS / "jazz-units"]


def collect_ids() -> set[int]:
    used: set[int] = set()
    skip_parts = {"Maps", ".git", "node_modules", "__pycache__", ".tmp"}
    for root in PACKAGES:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(p in skip_parts for p in path.parts):
                continue
            if path.suffix.lower() not in {".lua", ".csv", ".md", ".json"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for m in T_ID.finditer(text):
                used.add(int(m.group(1)))
            if path.suffix.lower() == ".csv":
                try:
                    with path.open(encoding="utf-8", newline="") as f:
                        reader = csv.reader(f)
                        header = next(reader, None)
                        if not header:
                            continue
                        id_idx = 0
                        if header and header[0].lower() in {"sep=", "sep=,"}:
                            header = next(reader, None)
                        if header:
                            lowered = [h.strip() for h in header]
                            if "ID" in lowered:
                                id_idx = lowered.index("ID")
                            elif "AnchorID" in lowered:
                                id_idx = lowered.index("AnchorID")
                        for row in reader:
                            if not row or id_idx >= len(row):
                                continue
                            cell = row[id_idx].strip()
                            if cell.isdigit():
                                used.add(int(cell))
                except (OSError, csv.Error):
                    continue
    return used


def next_id(used: set[int]) -> int:
    in_range = {i for i in used if RANGE_START <= i <= RANGE_END}
    cand = (max(in_range) + 1) if in_range else RANGE_START
    while cand in used and cand <= RANGE_END:
        cand += 1
    if cand > RANGE_END:
        raise SystemExit("No free ID left in reserved range")
    return cand


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", type=int)
    args = ap.parse_args()
    used = collect_ids()
    in_range = sorted(i for i in used if RANGE_START <= i <= RANGE_END)
    print(f"used_total={len(used)} used_in_range={len(in_range)} max_in_range={in_range[-1] if in_range else None}")
    if args.check is not None:
        print(f"check={args.check} used={args.check in used}")
        return 0 if args.check not in used else 1
    nid = next_id(used)
    print(f"next_id={nid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
