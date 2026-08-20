# docs/tools/_audit_russian_csv_swapped_columns.py
"""Find Russian.csv rows where Translation is English T() source and Text is Russian.

JA3 displays Translation. English-source T() rows must be:
  Text=English source, Translation=Russian
not the reverse (a COMBAT-007 apply-script bug).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path) -> dict[str, list[str]]:
	by: dict[str, list[str]] = {}
	with path.open(encoding="utf-8", newline="") as f:
		reader = csv.reader(f)
		header = next(reader, None)
		if header and header[0] == "sep=":
			header = next(reader, None)
		for row in reader:
			if row and row[0].isdigit():
				by[row[0]] = row
	return by


def has_cyrillic(s: str) -> bool:
	return any("\u0400" <= c <= "\u04FF" for c in s)


def main() -> int:
	ru = load(ROOT / "Russian.csv")
	en = load(ROOT / "English.csv")
	swapped: list[str] = []
	for id_ in sorted(set(ru) & set(en), key=lambda x: int(x)):
		r, e = ru[id_], en[id_]
		if len(r) < 3 or len(e) < 3:
			continue
		e_text, e_tr = e[1], e[2]
		r_text, r_tr = r[1], r[2]
		if e_text != e_tr or has_cyrillic(e_text) or not e_text.strip():
			continue
		if has_cyrillic(r_text) and r_tr == e_text:
			swapped.append(id_)
	print(f"swapped English-source rows: {len(swapped)}")
	for id_ in swapped:
		ctx = ru[id_][4] if len(ru[id_]) > 4 else ""
		print(f"{id_}\t{ctx}")
	return 1 if swapped else 0


if __name__ == "__main__":
	sys.exit(main())
