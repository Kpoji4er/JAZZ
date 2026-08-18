"""List UnitMarker keys and suspicious combat/aware flags on M3 isJdmPy."""
from __future__ import annotations

import re
from pathlib import Path

MAP = Path(__file__).resolve().parents[3] / "jazz-maps" / "Maps" / "isJdmPy" / "objects.lua"
SUSPECT = re.compile(
    r"Aware|Combat|Conflict|Alert|Unaware|Force|dummy|StatusEffect|Always",
    re.I,
)


def main() -> None:
    text = MAP.read_text(encoding="utf-8", errors="replace")
    keys: set[str] = set()
    suspect_lines: list[str] = []
    count = 0
    for m in re.finditer(
        r"PlaceObj\('UnitMarker',\s*\{(.*?)\},\s*nil,\s*\d+\)",
        text,
        re.S,
    ):
        count += 1
        body = m.group(1)
        for k in re.findall(r"'([A-Za-z_][A-Za-z0-9_]*)'\s*,", body):
            keys.add(k)
        for line in body.splitlines():
            if SUSPECT.search(line):
                ud = re.search(r"UnitDataDefId',\s*\"([^\"]+)\"", body)
                suspect_lines.append(
                    f"{ud.group(1) if ud else '?'}: {line.strip()}"
                )
    print(f"UnitMarkers={count}")
    print("keys:")
    for k in sorted(keys):
        print(f"  {k}")
    print(f"\nsuspect prop lines ({len(suspect_lines)}):")
    for s in suspect_lines[:80]:
        print(f"  {s}")


if __name__ == "__main__":
    main()
