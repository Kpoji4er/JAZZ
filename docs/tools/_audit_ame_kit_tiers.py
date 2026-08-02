"""Audit docs/design/ame-roster-60.md kits vs category tier caps (UNITS-005).

Caps: Irregulars ≤1-2, Fighters ≤1-3, Hardened/Specialists ≤2-1.
Uses docs/technical/weapons/data/weapons.csv tier_label.
Exit 0 always; prints violations count (0 = OK).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPS = {"Irregulars": (1, 2), "Fighters": (1, 3), "Hardened": (2, 1), "Specialists": (2, 1)}


def parse_tier(tl: str) -> tuple[int, int] | None:
    if not tl:
        return None
    m = re.match(r"(\d+)-(?:(\d+)|UNIQ)", tl)
    if not m:
        return None
    return int(m.group(1)), (99 if m.group(2) is None else int(m.group(2)))


def main() -> None:
    rows = {
        r["id"]: r
        for r in csv.DictReader((ROOT / "technical/weapons/data/weapons.csv").open(encoding="utf-8"))
    }
    text = (ROOT / "design/ame-roster-60.md").read_text(encoding="utf-8")
    cat = None
    bad: list[tuple] = []
    for line in text.splitlines():
        if line.startswith("## "):
            cat = line[3:].strip()
        if not (line.startswith("- **Inventory (fixed):**") and cat in CAPS):
            continue
        inv = line.split(":", 1)[1].strip()
        cmaj, csub = CAPS[cat]
        for tok in re.split(r"\s*[·]\s*", inv):
            wid = tok.strip().split()[0] if tok.strip() else ""
            if wid not in rows:
                continue
            t = parse_tier(rows[wid]["tier_label"])
            if not t:
                continue
            maj, sub = t
            if not ((maj < cmaj) or (maj == cmaj and sub <= csub)):
                bad.append((cat, wid, rows[wid]["tier_label"], inv[:70]))
    # Type56 = Hardened-only AR ceiling
    cat = None
    for line in text.splitlines():
        if line.startswith("## "):
            cat = line[3:].strip()
        if line.startswith("- **Inventory (fixed):**") and "Type56" in line and cat != "Hardened":
            bad.append((cat, "Type56", "Hardened-only", line[:70]))

    print(f"violations={len(bad)}")
    for b in bad:
        print(b)


if __name__ == "__main__":
    main()
