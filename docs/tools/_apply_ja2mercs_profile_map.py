# -*- coding: utf-8 -*-
"""Apply ja2mercs folder map onto jazz_to_ja2_profile.csv.

Writes jazz_to_ja2mercs_folders.csv and updates profile speech_source /
profile_id / status for remesh + need_pack rows. Does not touch Spouke /
workshop Merc_* / skip_ambiguous (except documenting in folders CSV).

Usage (jazz/):
  python docs/tools/_apply_ja2mercs_profile_map.py --dry-run
  python docs/tools/_apply_ja2mercs_profile_map.py
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
MAP_CSV = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
FOLDERS_CSV = (
    JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2mercs_folders.csv"
)

from _ja2mercs_folder_map import JA2MERCS_MAP, speech_source_for, write_csv  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    write_csv(FOLDERS_CSV)
    print(f"folders csv -> {FOLDERS_CSV}")

    by_slug = {r["slug"]: r for r in JA2MERCS_MAP}
    with MAP_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys()) if rows else [
        "slug",
        "unit_id",
        "profile_id",
        "speech_source",
        "status",
        "notes",
    ]

    changes = []
    for row in rows:
        slug = row.get("slug", "")
        m = by_slug.get(slug)
        if not m:
            continue
        decision = m["decision"]
        if decision in ("remesh", "need_pack"):
            src = speech_source_for(m)
            old = (
                row.get("profile_id", ""),
                row.get("speech_source", ""),
                row.get("status", ""),
            )
            row["profile_id"] = m["profile_id"]
            row["speech_source"] = src
            # keep done for colby; need_pack → ready for ship; remesh stay shipped/done
            if decision == "need_pack":
                row["status"] = "ready"
            elif row.get("status") == "missing":
                row["status"] = "shipped"
            note = (row.get("notes") or "").strip()
            tag = f"ja2mercs:{m['folder']}"
            if m.get("battle_pid"):
                tag += f"+battle={m['battle_pid']}"
            if m.get("reason"):
                tag += f"; {m['reason']}"
            if "ja2mercs:" not in note:
                row["notes"] = f"{note}; {tag}".strip("; ")
            new = (row["profile_id"], row["speech_source"], row["status"])
            if old != new:
                changes.append((slug, old, new))
        elif decision.startswith("skip"):
            # annotate notes only
            reason = m.get("reason") or decision
            note = (row.get("notes") or "").strip()
            marker = f"[ja2mercs:{decision}]"
            if marker not in note:
                row["notes"] = f"{note}; {marker} {reason}".strip("; ")
                changes.append((slug, "notes+", reason[:60]))

    print(f"profile changes: {len(changes)}")
    for c in changes:
        print(" ", c)

    if args.dry_run:
        print("DRY — profile not written")
        return 0

    with MAP_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {MAP_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
