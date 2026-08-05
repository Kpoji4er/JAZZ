"""Verify items.lua AME VoiceResponseId matches UnitData companions."""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

JU = Path(__file__).resolve().parents[2].parent / "jazz-units"
ITEMS = JU / "items.lua"
UD = JU / "UnitData"


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    begin = text.find("-- JAZZ-UNITS-005-AME-BEGIN")
    end = text.find("-- JAZZ-UNITS-005-AME-END")
    chunk = text[begin:end] if begin >= 0 and end > begin else text
    pairs = re.findall(
        r"'Id',\s*\"(JAZZ_AME_\d+)\".{0,4000}?'VoiceResponseId',\s*\"([^\"]+)\"",
        chunk,
        re.S,
    )
    c = Counter(v for _, v in pairs)
    print(f"items AME VoiceResponseId count={len(pairs)}")
    for k, v in c.most_common():
        print(f"  {k}: {v}")

    mismatches = []
    for uid, vr in pairs:
        p = UD / f"{uid}.lua"
        ut = p.read_text(encoding="utf-8")
        m = re.search(r'VoiceResponseId\s*=\s*"([^"]+)"', ut)
        if not m or m.group(1) != vr:
            mismatches.append((uid, vr, m.group(1) if m else "?"))
    print(f"companion mismatches={len(mismatches)}")
    for row in mismatches[:20]:
        print(" ", row)
    return 1 if mismatches or len(pairs) != 60 else 0


if __name__ == "__main__":
    raise SystemExit(main())
