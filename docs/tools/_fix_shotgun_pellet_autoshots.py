#!/usr/bin/env python3
"""Restore shotgun AutoShots/BurstShots pellet base after WEAPONS-003 RPM authoring.

Runtime (`Code/System_OR_Weapons.lua`) sets buckshot `num_shots = self.AutoShots`.
12g Buckshot ammo applies `mod_mul = 9000` (×9) on AutoShots, so weapon base must be 1
→ 9 pellets. Authoring that zeros AutoShots for non-AutoFire weapons yields 0 damage.

Usage (from jazz/):
  python docs/tools/_fix_shotgun_pellet_autoshots.py
  python docs/tools/_fix_shotgun_pellet_autoshots.py --apply
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "InventoryItem"
CSV = ROOT / "docs/technical/weapons/data/weapons.csv"


def fix_companion(path: Path, apply: bool) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r'object_class = "Shotgun"', text):
        return False
    new = text
    new = re.sub(r"^(\tAutoShots = )0(,?\s*)$", r"\g<1>1\2", new, count=1, flags=re.M)
    if re.search(r"^(\tBurstShots = )0(,?\s*)$", new, flags=re.M):
        new = re.sub(r"^(\tBurstShots = )0(,?\s*)$", r"\g<1>1\2", new, count=1, flags=re.M)
    if new == text:
        return False
    print(f"{'APPLY' if apply else 'DRY'} {path.relative_to(ROOT)}")
    if apply:
        path.write_text(new, encoding="utf-8", newline="\n")
    return True


def fix_csv(apply: bool) -> int:
    if not CSV.exists():
        return 0
    with CSV.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
        if not fieldnames and rows:
            fieldnames = list(rows[0].keys())
    n = 0
    for row in rows:
        if (row.get("object_class") or "").lower() != "shotgun":
            continue
        if row.get("auto_shots") == "0" or row.get("burst_shots") == "0":
            print(
                f"{'APPLY' if apply else 'DRY'} csv {row['id']}: "
                f"auto {row.get('auto_shots')}->1 burst {row.get('burst_shots')}->1"
            )
            row["auto_shots"] = "1"
            row["burst_shots"] = "1"
            n += 1
    if apply and n:
        with CSV.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    return n


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    fixed = 0
    for path in sorted(INV.rglob("*.lua")):
        if fix_companion(path, args.apply):
            fixed += 1
    csv_n = fix_csv(args.apply)
    print(f"companions={'wrote' if args.apply else 'would write'} {fixed}; csv rows {csv_n}")


if __name__ == "__main__":
    main()
