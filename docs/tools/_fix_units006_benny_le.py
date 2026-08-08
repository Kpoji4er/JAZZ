# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def fix_csv(path: Path) -> None:
    raw = path.read_text(encoding="utf-8-sig")
    rows = list(csv.reader(io.StringIO(raw)))
    for row in rows:
        if not row or row[0] != "890000000009921":
            continue
        for i in (1, 2):
            if len(row) > i and row[i]:
                row[i] = (
                    row[i]
                    .replace("\u2265", "\u2264")
                    .replace(">=8", "<=8")
                )
        print("fixed", path.name)  # avoid console encode of unicode
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")
    return True

def main() -> None:
    fix_csv(ROOT / "Russian.csv")
    fix_csv(ROOT / "English.csv")
    # generator source
    gen = ROOT / "docs/tools/_gen_units006_batch5.py"
    t = gen.read_text(encoding="utf-8")
    t2 = t.replace(
        "\\u0434\\u0435\\u043a\\u043e\\u0439 \\u22658",
        "\\u0434\\u0435\\u043a\\u043e\\u0439 \\u22648",
    ).replace("decoy lure \\u22658", "decoy lure \\u22648")
    if t2 != t:
        gen.write_text(t2, encoding="utf-8", newline="\n")
        print("gen fixed")
    print("OK")


if __name__ == "__main__":
    main()
