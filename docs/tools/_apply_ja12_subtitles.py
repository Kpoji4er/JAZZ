# -*- coding: utf-8 -*-
"""Apply ja2mercs subtitle banks onto Jazz UnitData chat + VoiceResponse T().

Maps slots → stems via AIM_CHAT_WAV / SLOT_WAV (first stem with non-empty RU).
Updates companion UnitData, items.lua VR/UnitData strings, Russian.csv Translation.
English.csv left as-is when already filled; if empty, keeps prior EN stub from T().

Usage (jazz/):
  python docs/tools/_apply_ja12_subtitles.py --dry-run --only kulba,biggens
  python docs/tools/_apply_ja12_subtitles.py --apply --only kulba,biggens,gaston,horg
  python docs/tools/_apply_ja12_subtitles.py --apply --only kulba --slots chat
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
SUB = JAZZ / "docs/design/mercs-ja12/_voice-source/subtitles"
MAP = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
RU_CSV = JAZZ / "Russian.csv"
EN_CSV = JAZZ / "English.csv"

sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _ship_ja2_merc_voices import (  # noqa: E402
    AIM_CHAT_WAV,
    SLOT_WAV,
    parse_unitdata_chat,
    parse_vr_blocks,
)


def load_bank(slug: str) -> dict[str, str]:
    path = SUB / f"{slug}.csv"
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    with path.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            text = (row.get("ru_text") or "").strip()
            if text:
                out[row["stem"].zfill(3)] = text
    return out


def esc_lua(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def pick_text(bank: dict[str, str], stems: list[str]) -> tuple[str, str] | None:
    for stem in stems:
        key = stem if not stem.isdigit() else stem.zfill(3)
        if key in bank:
            return key, bank[key]
        # named battle stems have no txt lines
    return None


def replace_t_string(text: str, tid: int, new_ru: str) -> tuple[str, bool]:
    """Replace the quoted string of T(tid, … "old") with new_ru."""
    pat = re.compile(
        rf"(T\({tid}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?)(?P<q>[\"'])(?P<body>.*?)(?P=q)",
        re.S,
    )

    def repl(m: re.Match) -> str:
        q = m.group("q")
        body = esc_lua(new_ru) if q == '"' else new_ru.replace("\\", "\\\\").replace("'", "\\'")
        return f"{m.group(1)}{q}{body}{q}"

    new, n = pat.subn(repl, text, count=1)
    return new, n > 0


def load_csv_map(path: Path) -> tuple[list[str], dict[str, list[str]]]:
    if not path.exists():
        return [], {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return [], {}
    # header may be absent in JA3 csv — first row is data if looks numeric
    header: list[str] = []
    start = 0
    if rows[0] and not re.fullmatch(r"\d+", rows[0][0] or ""):
        header = rows[0]
        start = 1
    by_id: dict[str, list[str]] = {}
    for row in rows[start:]:
        if not row or not row[0]:
            continue
        by_id[row[0]] = row
    return header, by_id


def write_csv_map(path: Path, header: list[str], by_id: dict[str, list[str]], order: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if header:
            w.writerow(header)
        for tid in order:
            if tid in by_id:
                w.writerow(by_id[tid])
        # append any new ids not in order
        for tid, row in by_id.items():
            if tid not in order:
                w.writerow(row)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, default="")
    ap.add_argument(
        "--slots",
        type=str,
        default="chat,combat",
        help="chat | combat | chat,combat",
    )
    args = ap.parse_args()
    apply = args.apply and not args.dry_run
    only = {s.strip().lower() for s in args.only.split(",") if s.strip()}
    want_chat = "chat" in args.slots
    want_combat = "combat" in args.slots

    slug_unit = {
        r["slug"]: r["unit_id"]
        for r in csv.DictReader(MAP.open(encoding="utf-8-sig"))
    }
    items_path = JU / "items.lua"
    items = items_path.read_text(encoding="utf-8", errors="replace")
    vr = parse_vr_blocks(items)
    ru_header, ru_map = load_csv_map(RU_CSV)
    en_header, en_map = load_csv_map(EN_CSV)
    ru_order = list(ru_map.keys())
    en_order = list(en_map.keys())

    total = 0
    for slug, unit in sorted(slug_unit.items()):
        if only and slug not in only:
            continue
        bank = load_bank(slug)
        if not bank:
            continue
        jobs: list[tuple[str, int, str, str]] = []  # kind, tid, stem, ru

        if want_chat:
            chat_i: dict[str, int] = {}
            for slot, tid in parse_unitdata_chat(unit):
                stems = AIM_CHAT_WAV.get(slot) or []
                # rotate like ship
                i = chat_i.get(slot, 0)
                chat_i[slot] = i + 1
                ordered = stems[i % len(stems) :] + stems[: i % len(stems)] if stems else []
                picked = pick_text(bank, ordered)
                if not picked:
                    continue
                stem, ru = picked
                jobs.append((f"chat:{slot}", tid, stem, ru))

        if want_combat and unit in vr:
            slot_i: dict[str, int] = {}
            for slot, tid in vr[unit]:
                pool = SLOT_WAV.get(slot) or []
                i = slot_i.get(slot, 0)
                slot_i[slot] = i + 1
                ordered = (
                    pool[i % len(pool) :] + pool[: i % len(pool)] if pool else []
                )
                # only numeric stems have txt lines
                numeric = [s for s in ordered if s.isdigit()]
                picked = pick_text(bank, numeric)
                if not picked:
                    continue
                stem, ru = picked
                jobs.append((f"vr:{slot}", tid, stem, ru))

        if not jobs:
            print(f"{slug}: no apply jobs")
            continue

        ud_path = JU / "UnitData" / f"{unit}.lua"
        ud_text = ud_path.read_text(encoding="utf-8", errors="replace") if ud_path.exists() else ""
        new_items = items
        new_ud = ud_text
        n_ok = 0
        for kind, tid, stem, ru in jobs:
            hit_items = False
            hit_ud = False
            if want_chat and kind.startswith("chat:") and ud_text:
                new_ud, hit_ud = replace_t_string(new_ud, tid, ru)
            new_items, hit_items = replace_t_string(new_items, tid, ru)
            if not hit_items and not hit_ud:
                print(f"  MISS T({tid}) {kind} stem={stem}")
                continue
            print(f"  {unit} {kind} T({tid}) <- {stem}: {ru[:60]!r}")
            n_ok += 1
            # Russian.csv: col0=ID, col1=Text(EN), col2=Translation(RU)
            row = ru_map.get(str(tid))
            if row is None:
                row = [str(tid), "", ru, "", unit]
                ru_map[str(tid)] = row
                ru_order.append(str(tid))
            else:
                while len(row) < 3:
                    row.append("")
                row[2] = ru
                ru_map[str(tid)] = row
            # English: keep existing Translation; ensure row exists
            erow = en_map.get(str(tid))
            if erow is None:
                # seed from old Text/EN stub if any
                en_stub = row[1] if row and len(row) > 1 else ""
                en_map[str(tid)] = [str(tid), en_stub or ru, en_stub or ru, "", unit]
                en_order.append(str(tid))

        total += n_ok
        print(f"{slug}: {n_ok} lines")
        if apply:
            if ud_path.exists() and new_ud != ud_text:
                ud_path.write_text(new_ud, encoding="utf-8")
            items = new_items

    if apply:
        items_path.write_text(items, encoding="utf-8")
        write_csv_map(RU_CSV, ru_header, ru_map, ru_order)
        write_csv_map(EN_CSV, en_header, en_map, en_order)
        print("Wrote items.lua + UnitData + Russian.csv (+ English.csv rows if missing)")
    print(f"TOTAL {total} mode={'APPLY' if apply else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
