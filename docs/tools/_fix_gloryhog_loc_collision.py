# -*- coding: utf-8 -*-
"""Fix Pierre loc ID collision with SteroidPunch 9930/9931."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Restore SteroidPunch rows
STEROID = {
    "890000000009930": (
        "Удар анаболика",
        "Anabolic Punch",
        "jazz:CharacterEffect/SteroidPunch.lua",
    ),
    "890000000009931": (
        "Пассивный навык. Точность всех ударов кулаками и оружием ближнего боя зависит от <em>Силы</em> вместо Ловкости. Успешные удары кулаками и оружием ближнего боя дают <em>Нокдаун</em> и <em>Без сознания</em>. Стимуляторы не вызывают потери <em>энергии</em> (усталости). Урон со временем от эффекта <em>горения</em> снижен на <em>30%</em>.",
        "Passive. All fist and melee weapon accuracy uses <em>Strength</em> instead of Agility. Successful fist/melee hits apply <em>Knockdown</em> and <em>Unconscious</em>. Combat stims do not cause <em>Energy</em> (tiredness) loss. Burning DoT reduced by <em>30%</em>.",
        "jazz:CharacterEffect/SteroidPunch.lua",
    ),
}

# New free IDs for Pierre recruit desc / used
NEW_DESC = "890000000009933"
NEW_USED = "890000000009934"

PIERRE = {
    NEW_DESC: (
        "Перевербовать видимого врага в союзника под управлением ИИ. Один раз за бой. Не действует на боссов.",
        "Recruit a visible enemy as an AI-controlled ally. Once per combat. Does not affect bosses.",
        "jazz:items.lua:Jazz_PierreRecruit",
    ),
    NEW_USED: (
        "Уже использовано в этом бою",
        "Already used this combat",
        "jazz:items.lua:Jazz_PierreRecruit",
    ),
}


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_csv(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    all_rows = {**STEROID, **PIERRE}
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in all_rows:
            ru, en, src = all_rows[rid]
            nl = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "\n")
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    for rid, (ru, en, src) in PIERRE.items():
        if rid not in found:
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(path.name, "restored steroid + pierre", sorted(found | set(PIERRE)))


def patch_items() -> None:
    p = ROOT / "items.lua"
    t = p.read_text(encoding="utf-8")
    t2 = t.replace(
        "T(890000000009930, --[[ModItemCombatAction Jazz_PierreRecruit Description]]",
        f"T({NEW_DESC}, --[[ModItemCombatAction Jazz_PierreRecruit Description]]",
    ).replace(
        'T(890000000009931, "Уже использовано в этом бою")',
        f'T({NEW_USED}, "Уже использовано в этом бою")',
    )
    if t2 == t:
        raise SystemExit("items.lua Pierre IDs not updated")
    p.write_text(t2, encoding="utf-8")
    print("items.lua IDs remapped")


def patch_apply_script() -> None:
    p = ROOT / "docs" / "tools" / "_apply_gloryhog_pierre.py"
    t = p.read_text(encoding="utf-8")
    t = t.replace('DESC_REC = "890000000009930"', f'DESC_REC = "{NEW_DESC}"')
    t = t.replace('USED_ID = "890000000009931"', f'USED_ID = "{NEW_USED}"')
    p.write_text(t, encoding="utf-8")
    print("apply script IDs updated")


def main() -> None:
    patch_csv(ROOT / "English.csv")
    patch_csv(ROOT / "Russian.csv")
    patch_items()
    patch_apply_script()
    print("OK collision fix")


if __name__ == "__main__":
    main()
