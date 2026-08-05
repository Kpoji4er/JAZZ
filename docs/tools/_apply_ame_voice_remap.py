#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply AME VoiceResponseId / FallbackMissingVR from roster voice_for().

Patches jazz-units UnitData/JAZZ_AME_*.lua companions and matching fields in
items.lua without regenerating bios/kits/portraits.

Usage (jazz/):
  python docs/tools/_apply_ame_voice_remap.py
  python docs/tools/_apply_ame_voice_remap.py --dry-run
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = JAZZ.parent / "jazz-units"
ROSTER_SCRIPT = JAZZ / "docs" / "tools" / "_gen_ame_roster_60.py"
UD = JU / "UnitData"
ITEMS = JU / "items.lua"


def load_roster_module():
    spec = importlib.util.spec_from_file_location("gen_ame_roster_60", ROSTER_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def patch_companion(path: Path, voice: str, fallback: str, dry: bool) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    old_vr = "?"
    m = re.search(r'VoiceResponseId\s*=\s*"([^"]+)"', text)
    if m:
        old_vr = m.group(1)
    new = re.sub(
        r'VoiceResponseId\s*=\s*"[^"]+"',
        f'VoiceResponseId = "{voice}"',
        text,
        count=1,
    )
    if re.search(r"FallbackMissingVR\s*=", new):
        new = re.sub(
            r'FallbackMissingVR\s*=\s*"[^"]+"',
            f'FallbackMissingVR = "{fallback}"',
            new,
            count=1,
        )
    else:
        new = re.sub(
            rf'(VoiceResponseId = "{re.escape(voice)}",)',
            rf'\1\n\tFallbackMissingVR = "{fallback}",',
            new,
            count=1,
        )
    if new != text and not dry:
        path.write_text(new, encoding="utf-8")
    return old_vr, voice


def patch_items(text: str, slot: int, voice: str, fallback: str) -> str:
    uid = f"JAZZ_AME_{slot:02d}"
    # UnitDataCompositeDef uses 'Id', "JAZZ_AME_NN" (LootDef uses id = "Loot_...").
    anchor = f"'Id', \"{uid}\","
    start = text.find(anchor)
    if start < 0:
        print(f"WARNING: items.lua Id not found for {uid}", file=sys.stderr)
        return text
    # Bound the unit block so we do not spill into the next AME folder.
    end = text.find("'DaysUntilOnline'", start)
    if end < 0 or end - start > 8000:
        print(f"WARNING: items.lua block bound failed for {uid}", file=sys.stderr)
        return text
    chunk = text[start:end]
    chunk2, n1 = re.subn(
        r"'VoiceResponseId',\s*\"[^\"]*\"",
        f"'VoiceResponseId', \"{voice}\"",
        chunk,
        count=1,
    )
    chunk3, n2 = re.subn(
        r"'FallbackMissingVR',\s*\"[^\"]*\"",
        f"'FallbackMissingVR', \"{fallback}\"",
        chunk2,
        count=1,
    )
    if n1 == 0:
        print(f"WARNING: items.lua VoiceResponseId not found for {uid}", file=sys.stderr)
    if n2 == 0:
        print(f"WARNING: items.lua FallbackMissingVR not found for {uid}", file=sys.stderr)
    return text[:start] + chunk3 + text[end:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    mod = load_roster_module()
    roster = mod.ROSTER
    assert len(roster) == 60

    before: Counter[str] = Counter()
    after: Counter[str] = Counter()
    items_text = ITEMS.read_text(encoding="utf-8")

    for i, m in enumerate(roster, 1):
        path = UD / f"JAZZ_AME_{i:02d}.lua"
        if not path.exists():
            print(f"MISSING {path}", file=sys.stderr)
            continue
        voice = mod.voice_for(m)
        fallback = mod.voice_fallback(m)
        old, new = patch_companion(path, voice, fallback, args.dry_run)
        before[old] += 1
        after[new] += 1
        items_text = patch_items(items_text, i, voice, fallback)
        print(f"JAZZ_AME_{i:02d}: {old} → {new} (fb={fallback})")

    if not args.dry_run:
        ITEMS.write_text(items_text, encoding="utf-8")

    def summarize(c: Counter[str], label: str) -> None:
        n = sum(c.values())
        imp = sum(v for k, v in c.items() if k.startswith("IMP_"))
        jazz = sum(v for k, v in c.items() if k.startswith("Jazz_"))
        other = n - imp - jazz
        print(f"\n{label}: n={n} IMP={imp} ({100 * imp / n:.1f}%) Jazz={jazz} ({100 * jazz / n:.1f}%) other={other} ({100 * other / n:.1f}%)")
        for k, v in c.most_common():
            print(f"  {k}: {v}")

    summarize(before, "BEFORE")
    summarize(after, "AFTER")
    if args.dry_run:
        print("\n(dry-run — no files written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
