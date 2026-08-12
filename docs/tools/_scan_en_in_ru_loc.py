# -*- coding: utf-8 -*-
"""Scan runtime Russian.csv for English Translation on Cyrillic Text (EN-in-RU)."""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RU = ROOT / "Russian.csv"
OUT = ROOT / ".tmp" / "en_in_ru.txt"

ABILITY_KEYS = ("CharacterEffect", "CombatAction", "Perk", "Signature")


def has_cyrillic(s: str) -> bool:
    return any("\u0400" <= c <= "\u04FF" for c in s or "")


def looks_english(s: str) -> bool:
    if not s:
        return False
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    return not has_cyrillic(s) and any("a" <= c.lower() <= "z" for c in letters)


def main() -> None:
    raw = RU.read_text(encoding="utf-8-sig")
    rows = list(csv.reader(io.StringIO(raw)))
    hits: list[tuple[str, str, str, str]] = []
    both_en: list[tuple[str, str, str]] = []
    for r in rows:
        if not r or r[0] in ("sep=", "ID"):
            continue
        if len(r) < 3:
            continue
        rid, text, trans = r[0], r[1], r[2]
        ctx = r[4] if len(r) > 4 else ""
        if has_cyrillic(text) and looks_english(trans):
            hits.append((rid, ctx, text, trans))
        elif looks_english(text) and looks_english(trans) and text == trans:
            if any(k in ctx for k in ABILITY_KEYS):
                both_en.append((rid, ctx, text))

    abil = [h for h in hits if any(k in h[1] for k in ABILITY_KEYS)]
    other = [h for h in hits if h not in abil]
    lines = [
        f"EN-in-RU total={len(hits)} ability-ish={len(abil)} other={len(other)} both-EN-ability={len(both_en)}",
        "",
        "=== ABILITY EN-in-RU ===",
    ]
    for rid, ctx, text, trans in abil:
        lines.append(f"ID {rid}")
        lines.append(f"CTX {ctx}")
        lines.append(f"TEXT {text.replace(chr(10), ' / ')}")
        lines.append(f"TRANS {trans.replace(chr(10), ' / ')}")
        lines.append("")
    lines.append("=== OTHER EN-in-RU ===")
    for rid, ctx, text, trans in other:
        lines.append(f"ID {rid}")
        lines.append(f"CTX {ctx}")
        lines.append(f"TEXT {text.replace(chr(10), ' / ')}")
        lines.append(f"TRANS {trans.replace(chr(10), ' / ')}")
        lines.append("")
    lines.append("=== ABILITY BOTH-EN (needs real translation) ===")
    for rid, ctx, text in both_en:
        lines.append(f"ID {rid}")
        lines.append(f"CTX {ctx}")
        lines.append(f"TEXT {text.replace(chr(10), ' / ')}")
        lines.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} total={len(hits)} abil={len(abil)} other={len(other)} both_en={len(both_en)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
