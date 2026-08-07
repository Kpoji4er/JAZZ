# -*- coding: utf-8 -*-
"""Audit JA12 AIM-hire-chat localization slots against shipped opus files."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
VOICES = UNITS / "voices"
CROSSWALK = JAZZ / "docs" / "design" / "mercs-ja12" / "_voice-source" / "jazz_to_ja2_profile.csv"

sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _ship_ja2_merc_voices import aim_chat_mode_for, parse_unitdata_chat  # noqa: E402


def parse_only(value: str) -> set[str]:
    return {part.strip().lower() for part in value.split(",") if part.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default="", help="Comma-separated merc slugs")
    parser.add_argument("--fail-on-silent", action="store_true")
    args = parser.parse_args()

    selected = parse_only(args.only)
    rows = list(csv.DictReader(CROSSWALK.open(encoding="utf-8-sig")))
    audited = silent_mercs = missing_slots = 0

    for row in rows:
        slug = row["slug"].strip().lower()
        if selected and slug not in selected:
            continue
        unit = row["unit_id"].strip()
        chat = parse_unitdata_chat(unit)
        if not chat:
            continue

        tids = [tid for _slot, tid in chat]
        missing = [tid for tid in tids if not (VOICES / f"{tid}.opus").is_file()]
        voiced = len(chat) - len(missing)
        status = "OK" if not missing else ("SILENT" if voiced == 0 else "PARTIAL")
        mode = aim_chat_mode_for(slug, row["speech_source"].strip(), row["profile_id"].strip())
        print(
            f"{unit}: {status} {voiced}/{len(chat)} "
            f"mode={mode} missing={','.join(map(str, missing)) or '-'}"
        )
        audited += 1
        missing_slots += len(missing)
        silent_mercs += voiced == 0

    print(
        f"SUMMARY audited={audited} silent_mercs={silent_mercs} "
        f"missing_slots={missing_slots}"
    )
    return 1 if args.fail_on_silent and silent_mercs else 0


if __name__ == "__main__":
    raise SystemExit(main())
