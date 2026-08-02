# -*- coding: utf-8 -*-
"""Fill AIM-chat for Jazz_Benny / Jazz_Simon / Jazz_Grom via hire remesh.

Deprecated Selection-donor path. Delegates to `_fill_ja12_chat_voices.py`
(hire stems 081–120 via `_ship_ja2_merc_voices.py --aim-chat-only`).

Note: SJ banks often lack 081–120 — script will SKIP rather than copy ATTN.

Usage (jazz/):
  python docs/tools/_fill_sj_chat_voices.py --dry-run
  python docs/tools/_fill_sj_chat_voices.py --apply
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
FILL = JAZZ / "docs" / "tools" / "_fill_ja12_chat_voices.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cmd = [sys.executable, str(FILL), "--only", "benny,simon,grom"]
    if args.apply and not args.dry_run:
        cmd.append("--apply")
    else:
        cmd.append("--dry-run")
    print("RUN:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(JAZZ))


if __name__ == "__main__":
    raise SystemExit(main())
