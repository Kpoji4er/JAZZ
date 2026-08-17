# -*- coding: utf-8 -*-
"""Dedupe MED-006 Manual memory rows; prefer latest polish; drop stale Bandage CA."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

KEEP_IDS = {
    "890000000010024",
    "890000000010027",
    "890000000010030",
    "890000000010213",
    "890000000010290",
    "890000000010291",
    "890000000010292",
}

STALE_213_SNIPPET = "starts healing on the heaviest untreated trauma"


def polish_ru_213(text: str) -> str:
    return text.replace("у порога кита", "у порога аптечки")


def load_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def save_rows(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def clean_manual(path: Path, lang: str) -> None:
    rows = load_rows(path)
    hdr, body = rows[0], rows[1:]
    # keep last occurrence per (AnchorID, SourceText) for KEEP_IDS
    last_idx: dict[tuple[str, str], int] = {}
    for i, r in enumerate(body):
        if len(r) < 3:
            continue
        aid, src = r[1], r[2]
        if aid in KEEP_IDS:
            last_idx[(aid, src)] = i

    drop = set()
    for i, r in enumerate(body):
        if len(r) < 3:
            continue
        aid, src = r[1], r[2]
        if aid == "890000000010213" and STALE_213_SNIPPET in src:
            drop.add(i)
            continue
        if aid in KEEP_IDS:
            key = (aid, src)
            if last_idx.get(key) != i:
                drop.add(i)

    new_body = []
    for i, r in enumerate(body):
        if i in drop:
            continue
        if lang == "ru" and len(r) >= 4 and r[1] == "890000000010213":
            r = list(r)
            r[3] = polish_ru_213(r[3])
        new_body.append(r)

    # renumber N
    out = [hdr]
    for n, r in enumerate(new_body, start=1):
        rr = list(r)
        rr[0] = str(n)
        out.append(rr)
    save_rows(path, out)
    print(path.name, "dropped", len(drop), "rows; now", len(new_body))


def patch_runtime_ru() -> None:
    path = ROOT / "Russian.csv"
    rows = load_rows(path)
    changed = 0
    for r in rows:
        if r and r[0] == "890000000010213" and len(r) >= 3:
            new = polish_ru_213(r[2])
            if new != r[2]:
                r[2] = new
                changed += 1
    if changed:
        save_rows(path, rows)
    print("Russian.csv 010213 kit->aptecki", changed)


def main() -> None:
    clean_manual(ROOT / "Localization" / "RussianManual.csv", "ru")
    clean_manual(ROOT / "Localization" / "EnglishManual.csv", "en")
    patch_runtime_ru()


if __name__ == "__main__":
    main()
