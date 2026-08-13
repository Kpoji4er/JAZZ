#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert one single-line mod-only localization row without rewriting the CSV.

Does not parse the whole table (multiline quoted fields stay intact).
Finds the predecessor ID line and splices the new row after it.
Manuals are appended.

Usage (from jazz/):
  python docs/tools/_insert_runtime_loc_row.py ^
    --id 890000000020156 ^
    --source "Старая ретрансляционная башня" ^
    --russian "Старая ретрансляционная башня" ^
    --english "Old Relay Tower" ^
    --after 890000000020155 ^
    --context "jazz-maps:items.lua HotDiamonds K2 display_name" ^
    --packages jazz-maps
"""
from __future__ import annotations

import argparse
import csv
import re
from io import StringIO
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]


def csv_row(fields: list[str]) -> str:
    sio = StringIO()
    csv.writer(sio, lineterminator="", quoting=csv.QUOTE_MINIMAL).writerow(fields)
    return sio.getvalue()


def splice_after_id(path: Path, after_id: str, new_id: str, line: str) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(rf"^{re.escape(new_id)},", text, re.M):
        raise SystemExit(f"{path.name}: ID {new_id} already present")
    pattern = re.compile(rf"^{re.escape(after_id)},[^\n]*\n", re.M)
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"{path.name}: predecessor ID {after_id} not found")
    insert = line if line.endswith("\n") else line + "\n"
    path.write_text(text[: match.end()] + insert + text[match.end() :], encoding="utf-8")


def append_manual(path: Path, new_id: str, source: str, translation: str, notes: str) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(rf",{re.escape(new_id)},", text):
        raise SystemExit(f"{path.name}: ID {new_id} already present")
    last_n = 0
    for m in re.finditer(r"^(\d+),", text, re.M):
        last_n = max(last_n, int(m.group(1)))
    row = csv_row([str(last_n + 1), new_id, source, translation, notes])
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + row + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--russian", required=True)
    ap.add_argument("--english", required=True)
    ap.add_argument("--context", default="")
    ap.add_argument("--packages", default="jazz")
    ap.add_argument("--notes", default="manual-translation")
    args = ap.parse_args()
    if not args.id.isdigit() or not args.after.isdigit():
        raise SystemExit("ID and --after must be digits")

    splice_after_id(
        JAZZ / "Russian.csv",
        args.after,
        args.id,
        csv_row([args.id, args.source, args.russian, "", args.context]),
    )
    splice_after_id(
        JAZZ / "English.csv",
        args.after,
        args.id,
        csv_row([args.id, args.source, args.english, "", args.context]),
    )
    splice_after_id(
        JAZZ / "Localization" / "Strings.csv",
        args.after,
        args.id,
        csv_row(
            [
                args.id,
                args.source,
                "",
                args.russian,
                args.english,
                "russian-override;new-id",
                args.context,
                args.packages,
                args.context,
                args.notes,
            ]
        ),
    )
    append_manual(
        JAZZ / "Localization" / "RussianManual.csv",
        args.id,
        args.source,
        args.russian,
        args.notes,
    )
    append_manual(
        JAZZ / "Localization" / "EnglishManual.csv",
        args.id,
        args.source,
        args.english,
        args.notes,
    )
    print(f"inserted {args.id} after {args.after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
