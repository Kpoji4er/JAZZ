# -*- coding: utf-8 -*-
"""Clear AIM-chat opus that is battle/Selection-donated or has no hire bank.

Bayun: hire chat must come from SPEECH 081–120, never ATTN/Selection.
- If chat opus bytes == current Selection → delete.
- If merc is MERK / ja2mercs folder has no 081–120 → delete all chat opus
  (silent chat > wrong battle VO). Hire-remeshed AIM/ЦС/WF are left alone.

Usage (jazz/):
  python docs/tools/_clear_ja12_selection_chat_donors.py --dry-run
  python docs/tools/_clear_ja12_selection_chat_donors.py --apply
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _ship_ja2_merc_voices import (  # noqa: E402
    folder_has_hire_stems,
    is_merk_ja2mercs_source,
    parse_unitdata_chat,
)

JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
ITEMS = JU / "items.lua"
VOICES = JU / "voices"
MAP_CSV = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    items = ITEMS.read_text(encoding="utf-8", errors="replace")
    donors: dict[str, str] = {}
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',\s*\{", items):
        win = items[m.start() : m.start() + 80000]
        mid = re.search(r'\bid\s*=\s*"(Jazz_[^"]+)"', win)
        if not mid:
            continue
        uid = mid.group(1)
        body = win[: mid.start()]
        sm = re.search(r"Selection\s*=\s*TConcat\(\{\s*T\((\d+),", body)
        if sm:
            donors[uid] = sm.group(1)

    by_unit: dict[str, dict[str, str]] = {}
    with MAP_CSV.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            by_unit[row["unit_id"]] = row

    cleared = 0
    for uid, donor in sorted(donors.items()):
        row = by_unit.get(uid, {})
        source = row.get("speech_source") or ""
        pid = (row.get("profile_id") or "").strip()
        no_hire = False
        if is_merk_ja2mercs_source(source):
            no_hire = True
        elif source.startswith("ja2mercs:") and pid and not folder_has_hire_stems(
            source, pid
        ):
            no_hire = True

        donor_bytes = b""
        donor_path = VOICES / f"{donor}.opus"
        if donor_path.exists():
            donor_bytes = donor_path.read_bytes()

        chat = parse_unitdata_chat(uid)
        n = 0
        for slot, tid in chat:
            dest = VOICES / f"{tid}.opus"
            if not dest.exists() or dest.stat().st_size < 50:
                continue
            data = dest.read_bytes()
            reason = ""
            if no_hire:
                reason = "no-hire-bank"
            elif donor_bytes and data == donor_bytes:
                reason = f"==Selection {donor}"
            else:
                continue
            print(f"{uid}: clear {tid} ({slot}; {reason})")
            n += 1
            if apply:
                dest.unlink()
        cleared += n
    print(f"TOTAL clear={cleared} mode={'APPLY' if apply else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
