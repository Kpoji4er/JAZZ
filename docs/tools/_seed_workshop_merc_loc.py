# -*- coding: utf-8 -*-
"""Seed jazz Russian.csv / English.csv for Workshop AIM merc T-ids (+ verify SJ).

Usage (jazz/):
  python docs/tools/_seed_workshop_merc_loc.py
  python docs/tools/_seed_workshop_merc_loc.py --apply
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")

MERCS = [
    "Merc_AnnieDubois",
    "Merc_CarolThompson",
    "Merc_HectorSanchez",
    "Merc_JerrySinclair",
    "Merc_MildredPatterson",
    "Merc_SamuelNkosi",
]

# Hand EN invents for Carol UnitData / AIM chat (workshop shipped Russian body text).
# Combat VR Cyrillic lines still fall back to en-from-ru-pending unless listed here.
CAROL_EN: dict[str, str] = {
    "333387953860": "Carol Thompson",
    "478926966328": "Nuts",
    "650483012873": "NUTS",
    "765028851206": "Nuts",
    "888795602514": "Carol",
    "813818008991": (
        "Carol Thompson is a driven British woman whose remarkable path began on the "
        "oil-stained floors of her father's garage in a rough London suburb. After finishing "
        "school she left home and enlisted in the British Army, serving four years with a "
        "squadron of the Royal Tank Regiment. After her service she moved into contract work "
        "and joined A.I.M. Known as an experienced mechanic, she is available for hire when "
        "the battlefield needs mechanical expertise."
    ),
    "258446624568": (
        "Sorry, but I noticed you've already hired that Bobby. If you really want me to put "
        "up with his misogynistic remarks, you'll have to pay an extra fee."
    ),
    "999137065414": (
        "Hey! You've reached Carol Thompson. Sorry, I'm not available right now. Leave your "
        "contact details and I'll call you back as soon as I can. Thanks!"
    ),
    "808934242004": "You're speaking with Carol Thompson. How can I help you?",
    "943445652391": "Hey! Thanks for calling me again. What can I do for you today?",
    "571131529692": (
        "Hey, you know calling girls just to breathe heavily into the phone is pretty creepy, right?"
    ),
    "814301384362": "Deal. I accept your terms.",
    "711717669491": (
        "Sorry, but we need to talk about our contract. It's ending soon. Would you be "
        "interested in extending it?"
    ),
    "236611551986": "Thank you for your trust.",
}


def looks_cyrillic(s: str) -> bool:
    return bool(re.search(r"[\u0400-\u04FF]", s or ""))


def parse_t_map(blob: str) -> dict[str, str]:
    out: dict[str, str] = {}
    if not blob:
        return out
    for m in re.finditer(
        r'T\((\d+)\s*,\s*--\[\[[^\]]*\]\]\s*"((?:\\.|[^"\\])*)"', blob, re.S
    ):
        t = m.group(2).replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
        out[m.group(1)] = t
    for m in re.finditer(
        r"T\((\d+)\s*,\s*--\[\[[^\]]*\]\]\s*'((?:\\.|[^'\\])*)'", blob, re.S
    ):
        t = m.group(2).replace("\\n", "\n").replace("\\'", "'").replace("\\\\", "\\")
        out[m.group(1)] = t
    return out


def folder_slice(items: str, merc: str) -> str:
    needle = f"'name', \"{merc}\""
    i = items.find(needle)
    if i < 0:
        return ""
    j = items.find("}, {", i)
    if j < 0:
        j = items.find("},{", i)
    start = (j + 4) if j >= 0 else i
    nxt = items.find("\n\t\tPlaceObj('ModItemFolder',", start)
    end = nxt if nxt >= 0 else min(len(items), start + 150000)
    return items[start:end]


sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _loc_csv_io import existing_ids, load_rows, write_rows  # noqa: E402


def merge_csv(path: Path, additions: dict[str, dict[str, str]]) -> int:
    sep, fields, rows, by_id = load_rows(path)
    have = set(by_id)
    added = 0
    for tid, r in additions.items():
        if tid in have:
            continue
        rows.append({k: r.get(k, "") for k in fields})
        added += 1
    write_rows(path, sep, fields, rows)
    return added


def collect_active(ju_items: str) -> dict[str, str]:
    tid_active: dict[str, str] = {}
    for merc in MERCS:
        tid_active.update(parse_t_map(folder_slice(ju_items, merc)))
        ud = JU / "UnitData" / f"{merc}.lua"
        if ud.exists():
            tid_active.update(
                parse_t_map(ud.read_text(encoding="utf-8", errors="replace"))
            )
        for p in (JAZZ / "CharacterEffect").glob(f"{merc}*"):
            tid_active.update(
                parse_t_map(p.read_text(encoding="utf-8", errors="replace"))
            )
        for p in (JAZZ / "Code" / "WorkshopMercs").glob(f"{merc}*"):
            tid_active.update(
                parse_t_map(p.read_text(encoding="utf-8", errors="replace"))
            )
    return tid_active


def invent_en(tid: str, src: str) -> tuple[str, str]:
    """Return (en, note). note empty if not invent."""
    if tid in CAROL_EN:
        return CAROL_EN[tid], "carol-unitdata-invent"
    if not looks_cyrillic(src):
        return src, ""
    # Carol / RU VR: keep RU in EN as last-resort invent (audio is English VO)
    return src, "en-from-ru-pending"


def invent_ru(en: str, src: str) -> tuple[str, str]:
    if looks_cyrillic(src):
        return src, ""
    # No RU source — technical copy of EN
    return en, "ru-technical-copy"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    ju_items = (JU / "items.lua").read_text(encoding="utf-8", errors="replace")
    tid_active = collect_active(ju_items)
    print(f"Active workshop merc T-ids: {len(tid_active)}")

    ru_path, en_path = JAZZ / "Russian.csv", JAZZ / "English.csv"
    ru_have, en_have = existing_ids(ru_path), existing_ids(en_path)

    new_ru: dict[str, dict[str, str]] = {}
    new_en: dict[str, dict[str, str]] = {}
    notes: dict[str, int] = {}

    for tid, src in sorted(tid_active.items(), key=lambda x: int(x[0])):
        en, n1 = invent_en(tid, src)
        ru, n2 = invent_ru(en, src)
        for n in (n1, n2):
            if n:
                notes[n] = notes.get(n, 0) + 1

        en_text = en if not looks_cyrillic(en) else (src if not looks_cyrillic(src) else en)
        # Prefer latin Text field for both tables
        if looks_cyrillic(en_text) and tid in CAROL_EN:
            en_text = CAROL_EN[tid]
        if looks_cyrillic(en_text) and not looks_cyrillic(src):
            en_text = src

        if tid not in en_have:
            new_en[tid] = {
                "ID": tid,
                "Text": en_text if not looks_cyrillic(en_text) else en,
                "Translation": en,
                "VoiceActor": "",
                "Context": "WorkshopMerc",
            }
        if tid not in ru_have:
            new_ru[tid] = {
                "ID": tid,
                "Text": en_text if not looks_cyrillic(en_text) else (CAROL_EN.get(tid, en)),
                "Translation": ru,
                "VoiceActor": "",
                "Context": "WorkshopMerc",
            }

    print(f"Need add EN={len(new_en)} RU={len(new_ru)}")
    print("Invent notes:", notes)
    for tid in ("507100823787", "333387953860", "813818008991", "847491090899"):
        print(
            f"  {tid}: src={tid_active.get(tid, '')[:40]!r} "
            f"new_en={tid in new_en} new_ru={tid in new_ru}"
        )

    if args.apply:
        a1 = merge_csv(en_path, new_en) if new_en else 0
        a2 = merge_csv(ru_path, new_ru) if new_ru else 0
        print(f"Applied EN+{a1} RU+{a2}")
    else:
        print("DRY-RUN (pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
