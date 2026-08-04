#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restore Jazz_Buzz / Jazz_Lynx / Jazz_Spider opus from pre-JA2-remesh commit.

These three (Тоска / Рысь / Паук) shipped with full original JA3 VO, same class
as Spouke (`done_manual`). Remesh commit 792d1c5 overwrote their Voices/*.opus
even though CSV said skip_no_folder. Spouke was protected and is never touched.

Usage (from jazz/ or any cwd):
  python docs/tools/_restore_lynx_tosca_spider_voices.py

Restores from jazz-units commit a626ebc (parent of 792d1c5).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
VOICES = UNITS / "Voices"
ITEMS = UNITS / "items.lua"
PRE_REMESH = "a626ebc"

# Original JA3 VO — restore these only; never Spouke.
MERCS = {
    "Jazz_Buzz": "tosca",
    "Jazz_Lynx": "lynx",
    "Jazz_Spider": "spider",
}

_VOICE_T = re.compile(
    r"T\((\d+)\s*,\s*--\[\[[^\]]*?\bvoice:([A-Za-z0-9_]+)\b[^\]]*\]\]",
    re.S,
)


def collect_ids() -> list[tuple[str, str, str]]:
    text = ITEMS.read_text(encoding="utf-8", errors="replace")
    by_voice: dict[str, set[str]] = {k: set() for k in MERCS}
    for tid, voice in _VOICE_T.findall(text):
        if voice in by_voice:
            by_voice[voice].add(tid)
    rows: list[tuple[str, str, str]] = []
    for vid, slug in MERCS.items():
        for tid in sorted(by_voice[vid], key=int):
            rows.append((slug, vid, tid))
    return rows


def git_blob(rel: str) -> bytes | None:
    """Repo path is lowercase voices/; avoid Voices/ on Windows case-fold."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{PRE_REMESH}:{rel}"],
            cwd=UNITS,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None


def main() -> int:
    if not ITEMS.is_file():
        print(f"FAIL: missing {ITEMS}", file=sys.stderr)
        return 1
    rows = collect_ids()
    print(f"IDs to restore: {len(rows)} from {PRE_REMESH}")

    restored = 0
    missing_in_commit = 0
    unchanged = 0
    missing_now = 0

    for slug, _vid, tid in rows:
        rel = f"voices/{tid}.opus"
        dest = VOICES / f"{tid}.opus"
        blob = git_blob(rel)
        if blob is None:
            missing_in_commit += 1
            continue

        if not dest.exists():
            missing_now += 1

        if dest.exists() and dest.read_bytes() == blob:
            unchanged += 1
            continue

        dest.write_bytes(blob)
        restored += 1
        if restored <= 5 or restored % 50 == 0:
            print(f"  restored {slug} {tid} from {rel} ({len(blob)} bytes)")

    print(
        f"DONE restored={restored} unchanged={unchanged} "
        f"missing_in_commit={missing_in_commit} missing_on_disk_before={missing_now}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
