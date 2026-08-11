# -*- coding: utf-8 -*-
"""Upsert BuildingConfidence loc rows."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = {
    "890000000009877": (
        "Уверенность растёт",
        "Building Confidence",
        "jazz:CharacterEffect/BuildingConfidence.lua",
    ),
    "890000000009878": (
        "На 2-м ходу и каждые 3 хода после (2/5/8…) — Inspired (+4 ОД). Лечение: ±<percentPerLevel>% за разницу уровней с пациентом (макс. ±<percentCap>%), в бою и на спутнике.",
        "On turn 2 and every 3 turns after (2/5/8…) — Inspired (+4 AP). Healing: ±<percentPerLevel>% per level difference vs patient (cap ±<percentCap>%), in combat and satellite.",
        "jazz:CharacterEffect/BuildingConfidence.lua",
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
    print(f"{path.name}: {sorted(found)}")


def main() -> None:
    for name in ("English.csv", "Russian.csv"):
        patch(ROOT / name)


if __name__ == "__main__":
    main()
