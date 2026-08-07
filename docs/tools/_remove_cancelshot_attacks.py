#!/usr/bin/env python3
"""Remove CancelShot from weapon AvailableAttacks (companions already edited)."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
CSV_PATH = ROOT / "docs/technical/weapons/data/weapons.csv"
WEAPON_IDS = ("M16A2", "M4Commando", "MP5", "AR15")


def clean_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    for wid in WEAPON_IDS:
        start = text.find(f"'Id', \"{wid}\"")
        if start < 0:
            print("missing", wid)
            continue
        chunk = text[start : start + 6000]
        m = re.search(r"'AvailableAttacks',\s*\{(.*?)\n\s*\},", chunk, re.S)
        if not m:
            print("no attacks", wid)
            continue
        body = m.group(1)
        if "CancelShot" not in body:
            print("already clean", wid)
            continue
        new_body = re.sub(r'\n\s*"CancelShot",', "", body)
        new_chunk = chunk[: m.start(1)] + new_body + chunk[m.end(1) :]
        text = text[:start] + new_chunk + text[start + len(chunk) :]
        print("cleaned items", wid)
    ITEMS.write_text(text, encoding="utf-8", newline="\n")


def clean_csv() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8", newline="")))
    fields = list(rows[0].keys())
    n = 0
    for row in rows:
        atts = row.get("available_attacks") or ""
        if "CancelShot" not in atts:
            continue
        parts = [p for p in atts.split(";") if p and p != "CancelShot"]
        row["available_attacks"] = ";".join(parts)
        n += 1
        print("csv", row["id"])
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("csv rows cleaned", n)


def main() -> None:
    clean_items()
    clean_csv()


if __name__ == "__main__":
    main()
