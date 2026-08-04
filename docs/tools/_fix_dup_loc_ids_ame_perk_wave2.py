# -*- coding: utf-8 -*-
"""Remap remaining JA2 perks off AME filter IDs 5001-5008; fix AME_UI 5000 EN Text."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PERK_REMAP = {
    # Meat
    890000000005001: (890000000005050, "Толстокожий", "Thick-Skinned"),
    890000000005002: (
        890000000005051,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Carlos
    890000000005003: (890000000005052, "Тихая тень", "Quiet Shadow"),
    890000000005004: (
        890000000005053,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Devin
    890000000005005: (890000000005054, "IRA", "IRA"),
    890000000005006: (
        890000000005055,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Shank
    890000000005007: (890000000005056, "Не трогай меня", "Don't Touch Me"),
    890000000005008: (
        890000000005057,
        "Враги в ближнем бою по Шенку получают −50 к шансу попадания.",
        "Enemies in melee against Shank take −50 chance to hit.",
    ),
}

PERK_FILES = [
    "CharacterEffect/Jazz_Perk_Meat.lua",
    "CharacterEffect/Jazz_Perk_Carlos.lua",
    "CharacterEffect/Jazz_Perk_Devin.lua",
    "CharacterEffect/Jazz_Perk_Shank.lua",
    "items.lua",
]

RESTORATIONS = [
    (
        "Jazz_Perk_Meat",
        890000000005050,
        "Толстокожий",
        890000000005051,
        "WIP — механика сигнатурного перка в разработке.",
    ),
    (
        "Jazz_Perk_Carlos",
        890000000005052,
        "Тихая тень",
        890000000005053,
        "WIP — механика сигнатурного перка в разработке.",
    ),
    (
        "Jazz_Perk_Devin",
        890000000005054,
        "IRA",
        890000000005055,
        "WIP — механика сигнатурного перка в разработке.",
    ),
    (
        "Jazz_Perk_Shank",
        890000000005056,
        "Не трогай меня",
        890000000005057,
        "Враги в ближнем бою по Шенку получают −50 к шансу попадания.",
    ),
]


def escape(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def load_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def save_csv(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def upsert(rows, lid, text, tr, ctx):
    sid = str(lid)
    for i, row in enumerate(rows):
        if row and row[0] == sid:
            while len(row) < 5:
                row.append("")
            row[1] = text
            row[2] = tr
            if ctx:
                row[4] = ctx
            rows[i] = row
            return
    rows.append([sid, text, tr, "", ctx])


def main():
    for rel in PERK_FILES:
        path = ROOT / rel
        t = path.read_text(encoding="utf-8")
        orig = t
        for old, (new, _ru, _en) in PERK_REMAP.items():
            t = re.sub(rf"T\(\s*{old}\s*,", f"T({new},", t)
        if t != orig:
            path.write_text(t, encoding="utf-8", newline="\n")
            print("patched", rel)

    items_path = ROOT / "items.lua"
    items = items_path.read_text(encoding="utf-8")
    for perk_id, dn_id, dn, desc_id, desc in RESTORATIONS:
        block_re = re.compile(
            rf"('Id',\s*\"{perk_id}\".*?)('DisplayName',\s*)T\([^)]*\)(.*?)('Description',\s*)T\([^)]*\)",
            re.DOTALL,
        )

        def repl(m, perk_id=perk_id, dn_id=dn_id, dn=dn, desc_id=desc_id, desc=desc):
            return (
                f"{m.group(1)}{m.group(2)}"
                f'T({dn_id}, --[[ModItemCharacterEffectCompositeDef {perk_id} DisplayName]] {escape(dn)})'
                f"{m.group(3)}{m.group(4)}"
                f'T({desc_id}, --[[ModItemCharacterEffectCompositeDef {perk_id} Description]] {escape(desc)})'
            )

        items, n = block_re.subn(repl, items, count=1)
        print(f"restore {perk_id}: {n}")

    items_path.write_text(items, encoding="utf-8", newline="\n")

    ru = load_csv(ROOT / "Russian.csv")
    en = load_csv(ROOT / "English.csv")
    for old, (new, ru_t, en_t) in PERK_REMAP.items():
        upsert(ru, new, ru_t, ru_t, f"perk-remap-from-{old}")
        upsert(en, new, ru_t, en_t, f"perk-remap-from-{old}")

    # Fix AME filter/UI English.csv Text to match T()/Russian.csv
    ame_fix = {
        890000000005000: ("A.M.E. Exchange", "A.M.E. Exchange"),
        890000000005001: ("Irregulars", "Irregulars"),
        890000000005002: ("Irregulars", "Irregulars"),
        890000000005003: ("Fighters", "Fighters"),
        890000000005004: ("Fighters", "Fighters"),
        890000000005005: ("Hardened", "Hardened"),
        890000000005006: ("Hardened", "Hardened"),
        890000000005007: ("Specialists", "Specialists"),
        890000000005008: ("Specialists", "Specialists"),
    }
    for lid, (text, tr) in ame_fix.items():
        upsert(en, lid, text, tr, "AME_Filter")
        # Russian.csv already has correct EN Text for filters; ensure 5000
        if lid == 890000000005000:
            upsert(ru, lid, "A.M.E. Exchange", "Африканская биржа наёмников", "AME_UI")

    save_csv(ROOT / "Russian.csv", ru)
    save_csv(ROOT / "English.csv", en)

    # verify no perk leftovers
    bad = []
    for p in (ROOT / "CharacterEffect").glob("Jazz_Perk_*.lua"):
        t = p.read_text(encoding="utf-8")
        for m in re.finditer(r"T\(\s*(89000000000500[0-8])\s*,", t):
            bad.append(f"{p.name}:{m.group(1)}")
    print("leftovers", bad or "none")
    print("OK")


if __name__ == "__main__":
    main()
