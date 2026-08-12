# -*- coding: utf-8 -*-
"""Fix EN-in-RU Translation on perk / signature CombatAction rows.

UNITS-006 `upsert_csv` wrote English into Russian.csv Translation. The game
shows Translation, so ability tooltips stayed English while titles (vanilla
nicknames / Cyrillic T() fallback) looked translated.

Does not touch VoiceResponse or InventoryItem rows. English.csv is unchanged.

Run from jazz root:
  python docs/tools/_fix_en_in_ru_ability_loc.py
  python docs/tools/_fix_en_in_ru_ability_loc.py --apply
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RU = ROOT / "Russian.csv"

ABILITY_KEYS = (
    "CharacterEffect",
    "CombatAction",
    "Perk",
    "Signature",
    "Nazdarovya",
    "PierreRecruit",
)
SKIP_KEYS = ("VoiceResponse", "InventoryItem")


def has_cyrillic(s: str) -> bool:
    return any("\u0400" <= c <= "\u04FF" for c in s or "")


def looks_english(s: str) -> bool:
    if not s:
        return False
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    return not has_cyrillic(s) and any("a" <= c.lower() <= "z" for c in letters)


def is_ability_row(ctx: str) -> bool:
    if any(k in ctx for k in SKIP_KEYS):
        return False
    return any(k in ctx for k in ABILITY_KEYS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    raw = RU.read_text(encoding="utf-8-sig")
    sep = None
    body = raw
    if raw.startswith("sep="):
        nl = raw.find("\n")
        sep = raw[: nl].rstrip("\r") if nl >= 0 else raw.rstrip("\r")
        body = raw[nl + 1 :] if nl >= 0 else ""

    rows = list(csv.reader(io.StringIO(body)))
    hits: list[tuple[int, str, str]] = []
    for i, row in enumerate(rows):
        if not row or row[0] in ("ID",):
            continue
        if len(row) < 3:
            continue
        rid, text, trans = row[0], row[1], row[2]
        ctx = row[4] if len(row) > 4 else ""
        if not is_ability_row(ctx):
            continue
        if has_cyrillic(text) and looks_english(trans):
            hits.append((i, rid, ctx))

    print(f"EN-in-RU ability rows: {len(hits)}")
    for _, rid, ctx in hits:
        print(f"  {rid}  {ctx}")

    multiline = []
    for i, rid, _ in hits:
        if "\n" in (rows[i][1] or "") or "\n" in (rows[i][2] or ""):
            multiline.append(rid)
    if multiline:
        raise SystemExit(f"multiline EN-in-RU rows, refuse line rewrite: {multiline}")

    if not args.apply:
        print("dry-run; pass --apply to write Russian.csv")
        return 0

    lines = body.splitlines(keepends=True)
    by_start: dict[str, int] = {}
    for li, line in enumerate(lines):
        for _, rid, _ in hits:
            if line.startswith(rid + ",") or line.startswith("\ufeff" + rid + ","):
                by_start[rid] = li
                break
    missing = [rid for _, rid, _ in hits if rid not in by_start]
    if missing:
        raise SystemExit(f"could not find source lines for {missing[:8]}")

    changed = 0
    for i, rid, ctx in hits:
        row = list(rows[i])
        while len(row) < 5:
            row.append("")
        row[2] = row[1]
        buf = io.StringIO()
        csv.writer(buf, lineterminator="", quoting=csv.QUOTE_MINIMAL).writerow(row)
        new_line = buf.getvalue()
        old = lines[by_start[rid]]
        nl = "\n" if old.endswith("\n") else ""
        if old.endswith("\r\n"):
            nl = "\r\n"
        elif old.endswith("\n"):
            nl = "\n"
        lines[by_start[rid]] = new_line + nl
        if old != lines[by_start[rid]]:
            changed += 1

    payload = ((sep + "\n") if sep else "") + "".join(lines)
    RU.write_text(payload, encoding="utf-8")
    print(f"updated {RU} rows={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
