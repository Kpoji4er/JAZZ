# -*- coding: utf-8 -*-
"""Upsert Nazdarovya/Drunk loc rows in English.csv / Russian.csv."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ROWS = {
    "890000000009887": (
        "Наздаровье",
        "Nazdarovya",
        "jazz:CharacterEffect/Nazdarovya.lua",
    ),
    "890000000009888": (
        "Активка каждый ход: снимает боль, лечит <healMin>–<healMax> HP, даёт стак опьянения (до <maxStacks>). За стак: <range_cth_mod> CTH, +<melee_damage_flat> урона в ближке. Опьянение в долг — −1 стак каждые <hoursPerStack> ч.",
        "Active each turn: clears Pain, heals <healMin>–<healMax> HP, adds an intoxication stack (max <maxStacks>). Per stack: <range_cth_mod> CTH, +<melee_damage_flat> melee damage. Debt wears off −1 stack every <hoursPerStack> h.",
        "jazz:CharacterEffect/Nazdarovya.lua",
    ),
    "890000000009889": (
        "Опьянение (стаки ≤5): −15 точности дальнего боя и +20 урона в ближнем бою за стак. Спадает по 1 стаку каждые 3 часа.",
        "Intoxication (stacks ≤5): −15 ranged accuracy and +20 melee damage per stack. Loses 1 stack every 3 hours.",
        "jazz:CharacterEffect/Drunk.lua",
    ),
    "890000000009890": (
        "Снимает боль, лечит 15–20 HP, даёт стак опьянения (до 5). За стак: −15 CTH и +20 урона в ближке. Без перезарядки — каждый ход (2 ОД). Опьянение сходит по 1 стаку / 3 ч.",
        "Clears Pain, heals 15–20 HP, adds an intoxication stack (max 5). Per stack: −15 CTH and +20 melee damage. No recharge — every turn (2 AP). Intoxication decays 1 stack / 3 h.",
        "jazz:items.lua:Nazdarovya",
    ),
    "890000000009891": (
        "Слишком пьян",
        "Too drunk",
        "jazz:items.lua:Nazdarovya",
    ),
}


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found = set()
    out = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in ROWS:
            ru, en, ctx = ROWS[rid]
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{ctx}\n")
            found.add(rid)
            continue
        out.append(line)
    for rid, (ru, en, ctx) in ROWS.items():
        if rid not in found:
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{ctx}\n")
    path.write_text("".join(out), encoding="utf-8", newline="")
    print(f"{path.name}: updated {sorted(found)}; appended {sorted(set(ROWS) - found)}")


def main() -> None:
    for name in ("English.csv", "Russian.csv"):
        patch(ROOT / name)


if __name__ == "__main__":
    main()
