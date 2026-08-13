# -*- coding: utf-8 -*-
"""Restore RecklessAssault 9935/9936; move Pierre recruit/charge tooltip to 9942/9943."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RA = {
    "890000000009935": (
        "Безрассудный натиск",
        "Reckless Rush",
        "jazz:CharacterEffect/RecklessAssault.lua",
    ),
    "890000000009936": (
        "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. "
        "<em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>.",
        "Improved <em>Run and Gun</em>: up to <em>4</em> attacks with an SMG, carbine, or assault rifle. "
        "<em>+<cth_bonus></em> Accuracy. No <GameTerm('Energy')> loss.",
        "jazz:CharacterEffect/RecklessAssault.lua",
    ),
}

PI = {
    "890000000009942": (
        "<merc> перевербовал(а) <target> в союзники.",
        "<merc> recruited <target> as an ally.",
        "jazz:Code/CombatActions.lua:Jazz_PierreRecruit",
    ),
    "890000000009943": (
        "Спецатака мачете <em>Charge</em> без прямой линии пути; даёт <em><grit></em> <GameTerm('Grit')>.",
        "Machete <em>Charge</em> without a straight-line path; grants <em><grit></em> <GameTerm('Grit')>.",
        "jazz:Code/CombatActions.lua:GloryHog",
    ),
}


def esc(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_csv(path: Path, rows: dict) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in rows:
            ru, en, src = rows[rid]
            nl = "\r\n" if line.endswith("\r\n") else "\n"
            out.append(f"{rid},{esc(ru)},{esc(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    missing = [rid for rid in rows if rid not in found]
    if missing:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        for rid in missing:
            ru, en, src = rows[rid]
            out.append(f"{rid},{esc(ru)},{esc(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(f"{path.name}: {sorted(found)}; appended={missing}")


def main() -> None:
    rows = {**RA, **PI}
    for p in (ROOT / "English.csv", ROOT / "Russian.csv"):
        patch_csv(p, rows)
    ca = ROOT / "Code" / "CombatActions.lua"
    t = ca.read_text(encoding="utf-8")
    t2 = t.replace("890000000009935", "890000000009942").replace("890000000009936", "890000000009943")
    # only Pierre combat-log / charge tooltip lines should change; RecklessAssault not in this file
    if t2 == t:
        print("CombatActions: no ID rewrite needed (already remapped?)")
    else:
        ca.write_text(t2, encoding="utf-8")
        print("CombatActions: 9935/9936 -> 9942/9943")
    # keep apply script in sync
    fix = ROOT / "docs" / "tools" / "_fix_pierre_recruit_uibegin.py"
    ft = fix.read_text(encoding="utf-8")
    ft = ft.replace("890000000009935", "890000000009942").replace("890000000009936", "890000000009943")
    fix.write_text(ft, encoding="utf-8")
    print("OK loc collision fixed")


if __name__ == "__main__":
    main()
