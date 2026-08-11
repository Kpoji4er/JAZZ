# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = {
    "890000000009869": (
        "Ястребиный глаз",
        "Eagle Eye",
        "jazz:CharacterEffect/HawksEye.lua",
    ),
    "890000000009870": (
        "Со снайперской винтовкой: Overwatch за <overwatchCostOverwrite> ОД (остальные ОД остаются). Pin Down / Focus Fire — мин. <pindownCostOverwrite> ОД. Снайперские выстрелы дают ×2 подавления. При найме печёт печенье (перезарядка сигнатур).",
        "With a sniper rifle: Overwatch costs <overwatchCostOverwrite> AP (remaining AP kept). Pin Down / Focus Fire min <pindownCostOverwrite> AP. Sniper shots deal ×2 suppression. On hire, bakes biscuits (recharge signatures).",
        "jazz:CharacterEffect/HawksEye.lua",
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
    print(path.name, sorted(found))


def main() -> None:
    for name in ("English.csv", "Russian.csv"):
        patch(ROOT / name)


if __name__ == "__main__":
    main()
