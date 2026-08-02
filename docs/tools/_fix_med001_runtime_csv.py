# -*- coding: utf-8 -*-
"""Fix MED-001 runtime CSV: correct RU Text/Translation order + real newlines.

JA3 Russian.csv must be: Text=English source, Translation=Russian.
Collision remap had written Text=RU, Translation=EN → UI fell back to English T() defaults.
Also replace literal \\n in AdditionalHint fields with real LF (quoted CSV).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MED_PREFIX = "890000000010"


def has_cyrillic(s: str) -> bool:
    return any("\u0400" <= c <= "\u04FF" for c in s or "")


def looks_english(s: str) -> bool:
    if not s:
        return False
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    return not has_cyrillic(s) and any("a" <= c.lower() <= "z" for c in letters)


def fix_newlines(s: str) -> str:
    if not s:
        return s
    # Only convert escaped sequences, keep already-real newlines.
    return s.replace("\\n", "\n")


def rewrite(path: Path, *, russian: bool) -> None:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    swapped = 0
    newlines = 0
    out = []
    for row in rows:
        if not row or not row[0].startswith(MED_PREFIX):
            out.append(row)
            continue
        while len(row) < 5:
            row.append("")
        text, trans = row[1], row[2]
        if russian and has_cyrillic(text) and looks_english(trans):
            text, trans = trans, text
            swapped += 1
        # English.csv: keep Text=EN; ensure Translation is EN too
        if not russian and looks_english(text) and has_cyrillic(trans):
            # accidental swap — put EN in both
            trans = text
            swapped += 1
        new_text = fix_newlines(text)
        new_trans = fix_newlines(trans)
        if new_text != text or new_trans != trans:
            newlines += 1
        row[1], row[2] = new_text, new_trans
        out.append(row)

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerows(out)
    print(f"{path.name}: swapped={swapped} newline_fields={newlines} rows={len(out)}")


def main() -> None:
    rewrite(ROOT / "Russian.csv", russian=True)
    rewrite(ROOT / "English.csv", russian=False)


if __name__ == "__main__":
    main()
