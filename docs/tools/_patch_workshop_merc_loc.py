# -*- coding: utf-8 -*-
"""Apply missing + patch Carol EN invents / SJ EN gaps in jazz Russian.csv & English.csv.

Usage (jazz/):
  python docs/tools/_patch_workshop_merc_loc.py --dry-run
  python docs/tools/_patch_workshop_merc_loc.py --apply
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

# Import invent map from seed module
sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _loc_csv_io import load_rows, write_rows  # noqa: E402
from _seed_workshop_merc_loc import (  # noqa: E402
    CAROL_EN,
    collect_active,
    invent_en,
    invent_ru,
    looks_cyrillic,
    parse_t_map,
)

# SJ stub EN invents for Cyrillic UnitData / chat (RU already in items).
SJ_EN: dict[str, str] = {
    "890000000002402": '[WIP] Major Sergey "Grom" Gromov',
    "890000000002403": "Grom",
    "890000000002404": "GROM",
    "890000000002405": "work in progress",
    "890000000002406": "The Afghan",
    "890000000002407": "Grom@vvs.ru",
    "890000000002408": "gromov",
    "890000000002409": "Not while you've got Scope. He's always criticizing other people's spotting, and I don't want to hear it.",
    "890000000002410": "Ivan, Igor or Iggy already here? Then I don't leave my own behind.",
    "890000000002411": "If you find Ivan or Igor — hire them without hesitation, proven fighters.",
    "890000000002412": "Gromov. Contact me later — busy checking the ammo loadout.",
    "890000000002413": "Major Gromov. Your airfield — means I'm yours.",
    "890000000002414": "Connection dropped. Continue, comrade.",
    "890000000002415": "Awaiting orders. Launcher loaded.",
    "890000000002416": "Launcher with me. Let's go.",
    "890000000002417": "Contract ending. Extending service, or should I find another airfield?",
    "890000000002418": "Staying. Duty is duty.",
    "890000000002419": "Major Gromov in position.",
    "890000000002420": "Fire on target!",
    "890000000002421": "Launcher ready.",
    "890000000002422": "Target destroyed.",
    "890000000002423": "Hold on, guys...",
    "890000000002424": "Wounded, but keeping my weapon.",
    "890000000002425": "Enemy approaching, to battle!",
    "890000000002426": "Afghan experience isn't forgotten.",
    "890000000002427": "Charges running low!",
    "890000000002428": "Awaiting orders, major ready.",
    "890000000002429": "Scope would correct something here, probably.",
    "890000000002430": "Good to serve with our own.",
}



def sj_tids(ju_items: str) -> dict[str, str]:
    out = {}
    for merc in ("Jazz_Benny", "Jazz_Simon", "Jazz_Grom"):
        # UnitData + VR only
        ud = JU / "UnitData" / f"{merc}.lua"
        blob = ud.read_text(encoding="utf-8", errors="replace") if ud.exists() else ""
        for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',", ju_items):
            win = ju_items[m.start() : m.start() + 80000]
            mid = re.search(r'id\s*=\s*"([^"]+)"', win)
            if mid and mid.group(1) == merc:
                blob += win[: mid.end() + 40]
                break
        # also chat in items UnitData composite
        idx = ju_items.find(f"'Id', \"{merc}\"")
        if idx >= 0:
            blob += ju_items[idx : idx + 25000]
        parsed = parse_t_map(blob)
        for tid, text in parsed.items():
            if tid.startswith("89000000000"):
                out[tid] = text
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    ju_items = (JU / "items.lua").read_text(encoding="utf-8", errors="replace")
    active = collect_active(ju_items)
    active.update(sj_tids(ju_items))

    ru_path, en_path = JAZZ / "Russian.csv", JAZZ / "English.csv"
    ru_sep, ru_fields, ru_rows, ru_by = load_rows(ru_path)
    en_sep, en_fields, en_rows, en_by = load_rows(en_path)

    patched_en = patched_ru = added_en = added_ru = 0
    invent_notes = []

    for tid, src in sorted(active.items(), key=lambda x: int(x[0])):
        en, n1 = invent_en(tid, src)
        if tid in CAROL_EN:
            en = CAROL_EN[tid]
            n1 = "carol-unitdata-invent"
        elif tid in SJ_EN:
            en = SJ_EN[tid]
            n1 = "sj-en-invent"
        ru, n2 = invent_ru(en, src)

        en_text = en if not looks_cyrillic(en) else (src if not looks_cyrillic(src) else en)
        if tid in CAROL_EN:
            en_text = CAROL_EN[tid]
        elif tid in SJ_EN:
            en_text = SJ_EN[tid]
        if looks_cyrillic(en_text) and not looks_cyrillic(src):
            en_text = src

        force_en = tid in CAROL_EN or tid in SJ_EN

        # English.csv
        if tid in en_by:
            row = en_by[tid]
            old = row.get("Translation") or ""
            # Patch if we have better EN invent and current is Cyrillic or empty
            if force_en and (looks_cyrillic(old) or old != en):
                invent_notes.append(f"PATCH EN {tid}")
                patched_en += 1
                if args.apply:
                    row["Text"] = en_text
                    row["Translation"] = en
                    row["Context"] = row.get("Context") or "WorkshopMerc"
            elif not old:
                invent_notes.append(f"FILL EN empty {tid}")
                patched_en += 1
                if args.apply:
                    row["Text"] = en_text if not looks_cyrillic(en_text) else src
                    row["Translation"] = en
        else:
            added_en += 1
            invent_notes.append(f"ADD EN {tid}" + (f" ({n1})" if n1 else ""))
            if args.apply:
                row = {k: "" for k in en_fields}
                row["ID"] = tid
                row["Text"] = en_text if not looks_cyrillic(en_text) else (src if not looks_cyrillic(src) else en)
                row["Translation"] = en
                row["Context"] = "WorkshopMerc"
                en_rows.append(row)
                en_by[tid] = row

        # Russian.csv
        if tid in ru_by:
            row = ru_by[tid]
            old = row.get("Translation") or ""
            if not old:
                patched_ru += 1
                invent_notes.append(f"FILL RU empty {tid}")
                if args.apply:
                    row["Translation"] = ru
                    row["Text"] = row.get("Text") or (en_text if not looks_cyrillic(en_text) else src)
        else:
            added_ru += 1
            invent_notes.append(f"ADD RU {tid}" + (f" ({n2})" if n2 else ""))
            if args.apply:
                row = {k: "" for k in ru_fields}
                row["ID"] = tid
                row["Text"] = en_text if not looks_cyrillic(en_text) else (CAROL_EN.get(tid, en))
                row["Translation"] = ru
                row["Context"] = "WorkshopMerc"
                ru_rows.append(row)
                ru_by[tid] = row

    print(f"Active tids: {len(active)}")
    print(f"EN: add={added_en} patch={patched_en}  RU: add={added_ru} patch={patched_ru}")
    for n in invent_notes[:40]:
        print(" ", n)
    if len(invent_notes) > 40:
        print(f"  ... +{len(invent_notes)-40}")

    if args.apply:
        write_rows(en_path, en_sep, en_fields, en_rows)
        write_rows(ru_path, ru_sep, ru_fields, ru_rows)
        print("Wrote Russian.csv + English.csv")
    else:
        print("DRY-RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
