# -*- coding: utf-8 -*-
"""Fill missing AIM-chat voice opus for Jazz_Benny / Jazz_Simon / Jazz_Grom.

Copies Selection line opus onto chat T-ids that have no audio file yet.
JA2 combat VR lines already shipped; hire chat was silent.

Usage (jazz/):
  python docs/tools/_fill_sj_chat_voices.py --dry-run
  python docs/tools/_fill_sj_chat_voices.py --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MERCS = ("Jazz_Benny", "Jazz_Simon", "Jazz_Grom")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    items = (JU / "items.lua").read_text(encoding="utf-8", errors="replace")
    vdir = JU / "voices"

    for merc in MERCS:
        donor = None
        for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", items):
            win = items[m.start() : m.start() + 50000]
            mid = re.search(r'id\s*=\s*"([^"]+)"', win)
            if not mid or mid.group(1) != merc:
                continue
            body = win[: mid.start()]
            sm = re.search(r"Selection\s*=\s*TConcat\(\{\s*T\((\d+),", body)
            if sm:
                donor = sm.group(1)
            break
        chat = re.findall(
            rf"T\((\d+),\s*--\[\[[^\]]*voice:{re.escape(merc)}\]\]",
            items,
        )
        ud = JU / "UnitData" / f"{merc}.lua"
        if ud.exists():
            chat += re.findall(
                rf"T\((\d+),\s*--\[\[[^\]]*voice:{re.escape(merc)}\]\]",
                ud.read_text(encoding="utf-8", errors="replace"),
            )
        chat = sorted(set(chat))
        if not donor:
            print(f"{merc}: no Selection donor")
            continue
        donor_path = vdir / f"{donor}.opus"
        if not donor_path.exists():
            print(f"{merc}: donor missing {donor}")
            continue
        filled = 0
        for tid in chat:
            dest = vdir / f"{tid}.opus"
            if dest.exists() and dest.stat().st_size > 50:
                continue
            print(f"{merc}: {donor} -> {tid}")
            if apply:
                dest.write_bytes(donor_path.read_bytes())
            filled += 1
        print(f"{merc}: filled {filled} (donor Selection {donor})")
    print("APPLY" if apply else "DRY-RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
