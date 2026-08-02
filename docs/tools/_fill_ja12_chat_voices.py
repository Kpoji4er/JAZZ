# -*- coding: utf-8 -*-
"""Fill AIM-chat voice opus for Jazz_* mercs (hire UI).

Bayun / схема реплик AIM.xlsx: chat must NOT copy Selection/ATTN.
Delegates to `_ship_ja2_merc_voices.py --aim-chat-only`.

Modes (auto in ship):
  classic   — SPEECH 081–120 when bank has hire
  fallback  — combat 000–080 proxies for MERK/RPC/Biff (never ATTN)
  ub-proxy  — UB ЦС campaign-in-081–120 → self-ID / readiness proxies

Usage (jazz/):
  python docs/tools/_fill_ja12_chat_voices.py --dry-run
  python docs/tools/_fill_ja12_chat_voices.py --apply
  python docs/tools/_fill_ja12_chat_voices.py --apply --only colby,vicious,gaston
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
SHIP = JAZZ / "docs" / "tools" / "_ship_ja2_merc_voices.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, default="")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    cmd = [
        sys.executable,
        str(SHIP),
        "--aim-chat-only",
        "--ja2mercs-remesh",
        "--include-done",
    ]
    if args.dry_run or not args.apply:
        cmd.append("--dry-run")
    if args.only:
        cmd.extend(["--only", args.only])
    print("RUN:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(JAZZ))


if __name__ == "__main__":
    raise SystemExit(main())
