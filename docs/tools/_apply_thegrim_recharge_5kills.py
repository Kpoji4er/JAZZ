# -*- coding: utf-8 -*-
"""UNITS-006: TheGrim (Reaper) recharge after N kills (default 5).

Patches CombatActions.TheGrim recharge_on_kill + wraps signature recharge
counters in Code/System_NamedPerks.lua (already applied by agent). This script
only appends RU/EN loc rows if missing.

Run from jazz root:
  python docs/tools/_apply_thegrim_recharge_5kills.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = [
    (
        "890000000009940",
        "<newline><newline>Перезаряжается после <em><need></em> убийств (другой атакой).",
        "<newline><newline>Recharges after <em><need></em> kills (with another attack).",
        "jazz:Code/System_NamedPerks.lua:TheGrim",
    ),
    (
        "890000000009941",
        "<newline><newline>Перезарядка: <em><done>/<need></em> убийств.",
        "<newline><newline>Recharge: <em><done>/<need></em> kills.",
        "jazz:Code/System_NamedPerks.lua:TheGrim",
    ),
]


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def append_loc(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    added = 0
    if not text.endswith("\n"):
        text += "\n"
    for lid, ru, en, ctx in ROWS:
        if lid in text:
            continue
        line = ",".join([lid, csv_escape(ru), csv_escape(en), "", ctx])
        text += line + "\n"
        added += 1
    path.write_text(text, encoding="utf-8")
    return added


def main() -> int:
    for name in ("English.csv", "Russian.csv"):
        n = append_loc(ROOT / name)
        print(f"{name}: +{n} rows")
    print("Runtime: Code/System_NamedPerks.lua Jazz_TheGrimKillsToRecharge=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
