#!/usr/bin/env python3
"""Export the AME bilingual biography bank for localization memory updates."""

from __future__ import annotations

import argparse
import csv
import importlib.util
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
DEFAULT_OUT = TOOLS / "localization-copy-edits" / "ame_bios_bilingual.csv"
MERC_LOC_BASE = 890000000005100
MERC_LOC_STRIDE = 10


def load_roster() -> list[dict]:
    path = TOOLS / "_gen_ame_roster_60.py"
    spec = importlib.util.spec_from_file_location("jazz_ame_roster_for_copy", path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    roster = module.ROSTER
    if len(roster) != 60:
        raise ValueError(f"expected 60 AME slots, found {len(roster)}")
    return roster


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=("ID", "SourceText", "Russian", "English", "Notes"),
        )
        writer.writeheader()
        for slot, merc in enumerate(load_roster(), 1):
            writer.writerow(
                {
                    "ID": MERC_LOC_BASE + (slot - 1) * MERC_LOC_STRIDE + 3,
                    "SourceText": merc["bio_en"],
                    "Russian": merc["bio"],
                    "English": merc["bio_en"],
                    "Notes": "JAZZ-UNITS-005",
                }
            )
    print(f"wrote {output} rows=60")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
