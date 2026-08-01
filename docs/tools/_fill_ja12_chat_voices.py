# -*- coding: utf-8 -*-
"""Fill missing AIM-chat voice opus for Jazz_* mercs from Selection donor.

Copies Selection (first line) opus onto UnitData/items chat T-ids that have
`voice:Jazz_*` in the T() comment and no usable opus yet.
Skips Name/Nick/Bio (no voice: tag).

Usage (jazz/):
  python docs/tools/_fill_ja12_chat_voices.py --dry-run
  python docs/tools/_fill_ja12_chat_voices.py --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
ITEMS = JU / "items.lua"
VOICES = JU / "voices"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    items = ITEMS.read_text(encoding="utf-8", errors="replace")
    # Collect VR Selection donors
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

    total = 0
    for uid, donor in sorted(donors.items()):
        donor_path = VOICES / f"{donor}.opus"
        if not donor_path.exists() or donor_path.stat().st_size < 50:
            print(f"SKIP {uid}: donor missing {donor}")
            continue
        chat: set[str] = set()
        for blob_path in (ITEMS, JU / "UnitData" / f"{uid}.lua"):
            if not blob_path.exists():
                continue
            text = blob_path.read_text(encoding="utf-8", errors="replace")
            chat.update(
                re.findall(
                    rf"T\((\d+),\s*--\[\[[^\]]*voice:{re.escape(uid)}\]\]",
                    text,
                )
            )
        filled = 0
        for tid in sorted(chat):
            dest = VOICES / f"{tid}.opus"
            if dest.exists() and dest.stat().st_size > 50:
                continue
            if apply:
                dest.write_bytes(donor_path.read_bytes())
            filled += 1
        if filled:
            print(f"{uid}: fill {filled} chat from Selection {donor}")
            total += filled
    print(f"TOTAL fill={total} mode={'APPLY' if apply else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
