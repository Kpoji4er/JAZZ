#!/usr/bin/env python3
"""JAZZ-WEAPONS-008: soften Poor/Crafted ammo jam mods in items.lua + companions.

Dry-run by default; --apply writes .bak once per touched file.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
INV = ROOT / "InventoryItem"

# Exact (old_jam, old_rel) -> (new_jam, new_rel) for known tiers.
REPLACEMENTS = {
    (200, -25): (140, -18),  # Crafted (all calibers)
    (180, -15): (120, -10),  # 9x19 Poor
    (150, -15): (100, -10),  # 45ACP Poor (and similar)
    (100, -5): (70, -4),     # rifle Poor
    (100, -8): (70, -5),     # 545-ish Poor
}


def write(path: Path, content: str, apply: bool) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == content:
        return False
    if apply:
        backup = path.with_suffix(path.suffix + ".bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(content, encoding="utf-8", newline="\n")
    return True


def _pair_sub(match: re.Match[str]) -> str:
    jam = int(match.group("jam"))
    rel = int(match.group("rel"))
    key = (jam, rel)
    if key not in REPLACEMENTS:
        return match.group(0)
    new_jam, new_rel = REPLACEMENTS[key]
    text = match.group(0)
    text = re.sub(rf"mod_add\s*=\s*{rel}\b", f"mod_add = {new_rel}", text, count=1)
    text = re.sub(rf"mod_add\s*=\s*{jam}\b", f"mod_add = {new_jam}", text, count=1)
    return text


def soften_block(text: str) -> tuple[str, int]:
    pat = re.compile(
        r"PlaceObj\('CaliberModification',\s*\{\s*"
        r"mod_add\s*=\s*(?P<rel>-?\d+),\s*"
        r"target_prop\s*=\s*\"Reliability\",\s*"
        r"\}\),\s*"
        r"PlaceObj\('CaliberModification',\s*\{\s*"
        r"mod_add\s*=\s*(?P<jam>-?\d+),\s*"
        r"target_prop\s*=\s*\"BaseJamChance\",",
        re.M,
    )
    out, n = pat.subn(_pair_sub, text)
    return out, n


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    total = 0
    items_text = ITEMS.read_text(encoding="utf-8")
    new_items, n = soften_block(items_text)
    total += n
    if write(ITEMS, new_items, args.apply):
        print(f"items.lua pairs={n}")
    for path in sorted(INV.glob("JAZZ_AMMO_*.lua")):
        if "_Poor" not in path.name and "_Crafted" not in path.name:
            continue
        text = path.read_text(encoding="utf-8")
        if "BaseJamChance" not in text:
            continue
        new_text, n = soften_block(text)
        total += n
        if write(path, new_text, args.apply) and n:
            print(f"{path.name} pairs={n}")
    print(f"{'applied' if args.apply else 'dry-run'} total_pairs={total}")


if __name__ == "__main__":
    main()
