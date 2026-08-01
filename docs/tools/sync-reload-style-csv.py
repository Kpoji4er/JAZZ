"""Add/update JAZZ-WEAPONS-004 reload_style in the canonical weapon snapshot."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "docs" / "technical" / "weapons" / "data" / "weapons.csv"

STYLES = {
    **dict.fromkeys(("Auto5", "Auto5_quest", "Ithaca", "M1897", "R870", "SPAS12", "Winchester1894", "Winchester_Quest"), "Tube"),
    **dict.fromkeys(("DoubleBarrelShotgun", "Stoeger"), "Break"),
    **dict.fromkeys(("Colt38Special", "ColtAnaconda", "ColtM1917", "ColtPeacemaker", "Korth", "MR73", "RSH12", "SWModel10", "SWModel19", "SWModel29", "TexRevolver", "Webley", "Welrod"), "Revolver"),
}

with CSV_PATH.open("r", encoding="utf-8", newline="") as source:
    rows = list(csv.DictReader(source))
    fields = source.seek(0) or next(csv.reader(source))

if "reload_style" not in fields:
    fields.append("reload_style")
for row in rows:
    row["reload_style"] = STYLES.get(row["id"], "Magazine")

with CSV_PATH.open("w", encoding="utf-8", newline="") as destination:
    writer = csv.DictWriter(destination, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
