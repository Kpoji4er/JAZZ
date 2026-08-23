#!/usr/bin/env python3
"""Set Crafted ammo Rel/jam between Poor and FMJ (owner 2026-08-23).

Card mods: Reliability -3, BaseJamChance +40.
Worse than FMJ (0/0), better than rifle Poor (~-4/+70) and pistol Poor (-10/+100..120).

Dry-run default; --apply writes items.lua + InventoryItem/JAZZ_AMMO_*_Crafted.lua.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
INV = ROOT / "InventoryItem"

NEW_REL = -3
NEW_JAM = 40

REL_JAM_PAIR = re.compile(
    r"(PlaceObj\('CaliberModification',\s*\{\s*"
    r"mod_add\s*=\s*)(?P<rel>-?\d+)(,\s*"
    r"target_prop\s*=\s*\"Reliability\",\s*"
    r"\}\),\s*"
    r"PlaceObj\('CaliberModification',\s*\{\s*"
    r"mod_add\s*=\s*)(?P<jam>-?\d+)(,\s*"
    r"target_prop\s*=\s*\"BaseJamChance\",)",
    re.M,
)


def set_pair(text: str) -> tuple[str, int]:
    def repl(match: re.Match[str]) -> str:
        return f"{match.group(1)}{NEW_REL}{match.group(3)}{NEW_JAM}{match.group(5)}"

    return REL_JAM_PAIR.subn(repl, text)


def crafted_item_blocks(items_text: str) -> list[tuple[int, int]]:
    spans = []
    for match in re.finditer(
        r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{",
        items_text,
    ):
        start = match.start()
        ident = re.search(r"'Id',\s*\"(JAZZ_AMMO_[^\"]+_Crafted)\"", items_text[start : start + 800])
        if not ident:
            continue
        nxt = items_text.find("PlaceObj('ModItemInventoryItemCompositeDef'", start + 10)
        end = nxt if nxt != -1 else start + 4000
        spans.append((start, end))
    return spans


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    items = ITEMS.read_text(encoding="utf-8")
    new_items = items
    item_hits = 0
    for start, end in reversed(crafted_item_blocks(items)):
        chunk, n = set_pair(items[start:end])
        if n:
            new_items = new_items[:start] + chunk + new_items[end:]
            item_hits += n

    companion_hits = 0
    companion_files = 0
    for path in sorted(INV.glob("JAZZ_AMMO_*_Crafted.lua")):
        text = path.read_text(encoding="utf-8")
        new_text, n = set_pair(text)
        companion_hits += n
        if n:
            companion_files += 1
            if args.apply and new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                print(f"{path.name} Rel {NEW_REL} jam +{NEW_JAM}")

    if args.apply and new_items != items:
        ITEMS.write_text(new_items, encoding="utf-8", newline="\n")
    print(
        f"{'applied' if args.apply else 'dry-run'} "
        f"items_pairs={item_hits} companion_files={companion_files} companion_pairs={companion_hits}"
    )
    if item_hits != 9 or companion_hits != 9:
        raise SystemExit(f"expected 9+9 Crafted pairs, got items={item_hits} companions={companion_hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
