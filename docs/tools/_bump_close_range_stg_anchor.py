#!/usr/bin/env python3
"""Bump Firearm CloseRange with STG44 as anchor (6 → 8).

Scale every existing non-zero CloseRange by 8/6 (nearest int).
Pistols / CR=0 stay 0. Does not touch CloseRangeFactor or barrel CloseΔ.

Companions InventoryItem/*.lua + items.lua ModItemInventoryItemCompositeDef.
Also updates BASE_CLOSE_RANGE in _apply_attach_001.py (role table).

Usage:
  python docs/tools/_bump_close_range_stg_anchor.py           # dry-run
  python docs/tools/_bump_close_range_stg_anchor.py --apply
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "InventoryItem"
ITEMS = ROOT / "items.lua"
APPLY_ATTACH = ROOT / "docs" / "tools" / "_apply_attach_001.py"

# STG44 was 6; owner wants 8 → scale factor 8/6.
OLD_STG = 6
NEW_STG = 8
SCALE = NEW_STG / OLD_STG

# Explicit OLD→NEW tier map (nearest int of old * 8/6).
# Guard: if STG44 already has CloseRange=8, --apply is a no-op (AR tier is also 8;
# without the guard a second run would mis-map AR 8→11 via the old battle-rifle row).
TIER_MAP = {
    0: 0,
    2: 3,   # round(2 * 8/6) = 3
    4: 5,   # round(4 * 8/6) = 5
    6: 8,   # STG / AR / MG anchor
    8: 11,  # round(8 * 8/6) = 11
    12: 16, # 12 * 8/6 = 16
}


def scale_close(old: int) -> int:
    if old in TIER_MAP:
        return TIER_MAP[old]
    return int(round(old * SCALE))


def stg_close_range() -> int | None:
    path = INVENTORY / "STG44.lua"
    if not path.exists():
        return None
    m = re.search(r"CloseRange\s*=\s*(\d+)", path.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def patch_companion(text: str) -> tuple[str, int | None, int | None]:
    m = re.search(r"(CloseRange\s*=\s*)(\d+)", text)
    if not m:
        return text, None, None
    old = int(m.group(2))
    new = scale_close(old)
    if old == new:
        return text, old, new
    return text[: m.start(2)] + str(new) + text[m.end(2) :], old, new


def patch_items(text: str) -> tuple[str, Counter]:
    """Replace 'CloseRange', N inside ModItemInventoryItemCompositeDef blocks only."""
    counts: Counter = Counter()
    # Match property lines; weapons use 'CloseRange', N,
    pattern = re.compile(r"('CloseRange',\s*)(\d+)(\s*,)")

    def repl(m: re.Match[str]) -> str:
        old = int(m.group(2))
        new = scale_close(old)
        counts[f"{old}->{new}"] += 1
        if old == new:
            return m.group(0)
        return f"{m.group(1)}{new}{m.group(3)}"

    return pattern.sub(repl, text), counts


def patch_base_table(text: str) -> str:
    """Update BASE_CLOSE_RANGE role defaults in _apply_attach_001.py."""
    mapping = {
        '"submachine-gun": (2, 95)': '"submachine-gun": (3, 95)',
        '"carbine": (4, 90)': '"carbine": (5, 90)',
        '"shotgun": (4, 90)': '"shotgun": (5, 90)',
        '"assault-rifle": (6, 85)': '"assault-rifle": (8, 85)',
        '"machine-gun": (6, 85)': '"machine-gun": (8, 85)',
        '"light-machine-gun": (6, 85)': '"light-machine-gun": (8, 85)',
        '"battle-rifle": (8, 80)': '"battle-rifle": (11, 80)',
        '"sniper-rifle": (12, 70)': '"sniper-rifle": (16, 70)',
    }
    out = text
    for old, new in mapping.items():
        if old not in out:
            raise SystemExit(f"BASE_CLOSE_RANGE entry missing: {old}")
        out = out.replace(old, new, 1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    stg = stg_close_range()
    if stg == NEW_STG:
        print(f"STG44 CloseRange already {NEW_STG}; nothing to do (idempotent).")
        return
    if stg is not None and stg != OLD_STG:
        raise SystemExit(f"Unexpected STG44 CloseRange={stg}; expected {OLD_STG} or {NEW_STG}")

    companion_changes: list[tuple[str, int, int]] = []
    for path in sorted(INVENTORY.glob("*.lua")):
        text = path.read_text(encoding="utf-8")
        new_text, old, new = patch_companion(text)
        if old is None:
            continue
        if old != new:
            companion_changes.append((path.stem, old, new))
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    items_text = ITEMS.read_text(encoding="utf-8")
    new_items, item_counts = patch_items(items_text)

    attach_text = APPLY_ATTACH.read_text(encoding="utf-8")
    # Skip BASE_CLOSE_RANGE rewrite if already new ladder (assault-rifle 8).
    if '"assault-rifle": (8, 85)' in attach_text:
        new_attach = attach_text
    else:
        new_attach = patch_base_table(attach_text)

    print(f"Scale: {OLD_STG}->{NEW_STG} (x{SCALE:.4f})  TIER_MAP={TIER_MAP}")
    print(f"Companions changed: {len(companion_changes)}")
    by_pair: Counter = Counter()
    samples = {"short": None, "mid": None, "long": None, "stg": None}
    for wid, old, new in companion_changes:
        by_pair[f"{old}->{new}"] += 1
        if wid == "STG44":
            samples["stg"] = (old, new)
        if old == 2 and samples["short"] is None:
            samples["short"] = (wid, old, new)
        if old == 4 and samples["mid"] is None:
            samples["mid"] = (wid, old, new)
        if old == 12 and samples["long"] is None:
            samples["long"] = (wid, old, new)
    for k, v in sorted(by_pair.items()):
        print(f"  companions {k}: {v}")
    print(f"items.lua replacements: {dict(item_counts)}")
    print(f"samples: STG={samples['stg']} short={samples['short']} mid={samples['mid']} long={samples['long']}")

    if args.apply:
        ITEMS.write_text(new_items, encoding="utf-8")
        APPLY_ATTACH.write_text(new_attach, encoding="utf-8")
        print("APPLIED companions + items.lua + BASE_CLOSE_RANGE")
    else:
        print("DRY-RUN (pass --apply to write)")


if __name__ == "__main__":
    main()
