# Fix BobbyRay restock Assert: InventoryItem Tier must be a number.
# Vanilla PrepareShopItemsForRestock does `item.Tier <= unlocked_tier`.
# Some JAZZ ammo companions used Tier = "4" / "5" (string).
#
# Usage (from jazz/):
#   python docs/tools/_fix_bobbyray_string_tier.py
#   python docs/tools/_fix_bobbyray_string_tier.py --apply
# Exit 0 if clean or apply succeeded.

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
INV = ROOT / "InventoryItem"

TIER_ITEMS_RE = re.compile(r"""('Tier',\s*)\"(\d+)\"""")
TIER_COMPANION_RE = re.compile(r"""(^(\t*)Tier\s*=\s*)\"(\d+)\"(,?\s*)$""", re.M)


def scan() -> list[tuple[Path, int, str, str]]:
    hits: list[tuple[Path, int, str, str]] = []
    text = ITEMS.read_text(encoding="utf-8")
    for m in TIER_ITEMS_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        hits.append((ITEMS, line, m.group(0), f"{m.group(1)}{m.group(2)}"))
    for path in sorted(INV.glob("*.lua")):
        body = path.read_text(encoding="utf-8")
        for m in TIER_COMPANION_RE.finditer(body):
            line = body.count("\n", 0, m.start()) + 1
            hits.append((path, line, m.group(0).rstrip("\n"), f"{m.group(1)}{m.group(3)}{m.group(4)}"))
    return hits


def apply(hits: list[tuple[Path, int, str, str]]) -> int:
    by_file: dict[Path, list[tuple[str, str]]] = {}
    for path, _line, old, new in hits:
        by_file.setdefault(path, []).append((old, new))
    changed = 0
    for path, pairs in by_file.items():
        text = path.read_text(encoding="utf-8")
        orig = text
        # Prefer regex replace on whole file for items.lua numeric Tier strings.
        if path == ITEMS:
            text2, n = TIER_ITEMS_RE.subn(r"\1\2", text)
            if n:
                path.write_text(text2, encoding="utf-8", newline="\n")
                changed += n
            continue
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new, 1)
        if text != orig:
            path.write_text(text, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    hits = scan()
    print(f"string Tier hits: {len(hits)}")
    for path, line, old, new in hits:
        rel = path.relative_to(ROOT)
        print(f"  {rel}:{line}: {old!r} -> {new!r}")
    if not hits:
        return 0
    if not args.apply:
        print("Dry-run only. Pass --apply to write.")
        return 1
    n = apply(hits)
    print(f"applied changes: {n}")
    leftover = scan()
    print(f"remaining: {len(leftover)}")
    return 0 if not leftover else 2


if __name__ == "__main__":
    raise SystemExit(main())
