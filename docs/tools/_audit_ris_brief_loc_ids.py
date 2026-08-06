# -*- coding: utf-8 -*-
import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("sep="):
        text = text.split("\n", 1)[1]
    return {r[0]: r for r in csv.reader(io.StringIO(text)) if r}


def main():
    ru = load(ROOT / "Russian.csv")
    en = load(ROOT / "English.csv")
    text = (ROOT / "items.lua").read_text(encoding="utf-8")
    start = text.find("RIS_LegionBrief_11")
    end = text.find("PlaceObj('ModItemQuestsDef'", start)
    block = text[start - 120 : end]
    pat = re.compile(
        r'T\((\d+), --\[\[ModItemEmail (RIS_LegionBrief_\d+) (title|body)\]\] "(.*?)"\)',
        re.S,
    )
    for m in pat.finditer(block):
        tid, eid, kind, src = m.groups()
        src1 = src.replace("\\n", " ")[:55]
        print(f"{eid} {kind} id={tid} items={src1!r}")
        for label, table in (("RU", ru), ("EN", en)):
            row = table.get(tid)
            if not row:
                print(f"  {label}: MISSING")
                continue
            c1 = row[1] if len(row) > 1 else ""
            c2 = row[2] if len(row) > 2 else ""
            # Prefer the column that matches language
            print(f"  {label}.c1={c1.replace(chr(10),' ')[:60]!r}")
            print(f"  {label}.c2={c2.replace(chr(10),' ')[:60]!r}")


if __name__ == "__main__":
    main()
