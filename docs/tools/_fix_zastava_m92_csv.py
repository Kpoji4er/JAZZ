"""One-shot: set ZastavaM92 burst/auto/RPM in weapons.csv (WEAPONS-003)."""
from __future__ import annotations

import csv
from pathlib import Path

CSV = Path(__file__).resolve().parents[1] / "technical" / "weapons" / "data" / "weapons.csv"


def main() -> None:
    with CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    changed = False
    for row in rows:
        if row.get("id") == "ZastavaM92":
            row["burst_shots"] = "4"
            row["auto_shots"] = "7"
            row["cyclic_rpm"] = "700"
            changed = True
            break
    if not changed:
        raise SystemExit("ZastavaM92 row not found")
    with CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("OK: ZastavaM92 burst=4 auto=7 rpm=700")


if __name__ == "__main__":
    main()
