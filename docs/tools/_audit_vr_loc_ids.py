# -*- coding: utf-8 -*-
"""Audit jazz-units ModItemVoiceResponse T() IDs against runtime CSVs."""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
ITEMS = UNITS / "items.lua"


def load_csv_ids(path: Path) -> set[str]:
    out: set[str] = set()
    if not path.exists():
        return out
    with path.open(encoding="utf-8-sig", newline="") as f:
        first = f.readline()
        if not first.startswith("sep="):
            f.seek(0)
        reader = csv.DictReader(f)
        for row in reader:
            i = (row.get("ID") or "").strip()
            if i.isdigit():
                out.add(i)
    return out


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    grouped: dict[str, list[str]] = defaultdict(list)
    for tid, merc in re.findall(
        r"T\((\d{9,}),\s*--\[\[ModItemVoiceResponse\s+(\S+)\s+",
        text,
    ):
        grouped[merc].append(tid)
    presets = sorted(grouped.items())

    ru = load_csv_ids(JAZZ / "Russian.csv")
    en = load_csv_ids(JAZZ / "English.csv")
    uen = load_csv_ids(UNITS / "English.csv")

    print(
        f"csv jazzRU={len(ru)} jazzEN={len(en)} unitsEN={len(uen)} vr_presets={len(presets)}"
    )
    all_ids: set[str] = set()
    miss = defaultdict(list)
    for vid, ids in sorted(presets):
        all_ids.update(ids)
        mr = [i for i in ids if i not in ru]
        me = [i for i in ids if i not in en]
        mu = [i for i in ids if i not in uen]
        if mr or me or mu:
            miss[vid] = (len(ids), len(mr), len(me), len(mu), mr[:5], mu[:5])
            print(
                f"{vid}: n={len(ids)} miss_jazzRU={len(mr)} miss_jazzEN={len(me)} miss_unitsEN={len(mu)}"
            )
            if mr:
                print("  sample_ru", mr[:5])
            if mu:
                print("  sample_uen", mu[:5])

    print("total VR T-ids", sum(len(ids) for _, ids in presets))
    print("unique VR ids", len(all_ids))
    print(
        "unique missing jazzRU",
        sum(1 for i in all_ids if i not in ru),
        "jazzEN",
        sum(1 for i in all_ids if i not in en),
        "unitsEN",
        sum(1 for i in all_ids if i not in uen),
    )
    if not miss:
        print("OK all VoiceResponse T-ids present in jazz RU/EN and units EN")


if __name__ == "__main__":
    main()
