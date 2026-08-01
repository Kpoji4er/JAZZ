# -*- coding: utf-8 -*-
"""Inject minimal VoiceResponse stubs for Jazz mercs that have JA2 profile but empty VR.

Uses Ira-like slot set (12 lines). Texts from mercedt when available.
Allocates T-ids from 890000000006300+.
Updates jazz-units/items.lua + jazz Russian.csv/English.csv.

Usage (jazz/):
  python docs/tools/_inject_vr_stubs_ja2_voices.py --dry-run
  python docs/tools/_inject_vr_stubs_ja2_voices.py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MAP = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
MERCEDT = JAZZ / "docs/design/mercs-ja12/_voice-source/ja2no-mercedt"
ITEMS = JU / "items.lua"
RU = JAZZ / "Russian.csv"
EN = JAZZ / "English.csv"
TID_START = 890000000006300

# slot -> preferred mercedt line numbers
SLOT_LINES: list[tuple[str, list[str], str, str]] = [
    # slot, mercedt line prefs, ru_fallback, en_fallback
    ("Selection", ["108", "084", "072"], "На связи.", "Online."),
    ("AimAttack", ["000", "001", "027"], "Есть цель!", "Target!"),
    ("AimAttack", ["001", "000", "027"], "В бой!", "Engage!"),
    ("OpponentKilled", ["027", "028", "032"], "Готов.", "Down."),
    ("DeathGeneral", ["014", "015", "016"], "Конец...", "That's it..."),
    ("Downed", ["021", "024", "014"], "Ранен!", "I'm hit!"),
    ("AmmoLow", ["013", "012"], "Патроны!", "Low ammo!"),
    ("CombatStartDetected", ["001", "000", "072"], "Контакт!", "Contact!"),
    ("Idle", ["035", "045", "046"], "Жду.", "Waiting."),
    ("LevelUp", ["046", "035"], "Учусь.", "Learning."),
    ("MockDislike1", ["029", "031"], "Только не это.", "Not this."),
    ("PraisesBuddy1", ["051", "053", "052"], "Отличная работа.", "Nice work."),
]


def load_mercedt(pid: str) -> dict[str, str]:
    files = list(MERCEDT.glob(f"{pid}_*.csv"))
    # NightOps overlay-only profiles may lack Data CSV — try synthetic from overlay later
    if not files:
        return {}
    out: dict[str, str] = {}
    with files[0].open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = (row.get("text") or "").strip()
            if t and not t.startswith("я"):
                out[row["line"].zfill(3)] = t
    return out


def pick_text(lines: dict[str, str], prefs: list[str], fallback: str) -> str:
    for p in prefs:
        t = lines.get(p.zfill(3))
        if t and len(t) < 160:
            return t
    for p in prefs:
        t = lines.get(p.zfill(3))
        if t:
            return t[:120]
    return fallback


def empty_vr_pattern(unit_id: str) -> re.Pattern[str]:
    # Match empty VR PlaceObj ... id = "Jazz_X", }),  (trailing comma included)
    return re.compile(
        rf"PlaceObj\('ModItemVoiceResponse',\s*\{{\s*"
        rf"(?:group\s*=\s*\"[^\"]+\",\s*)?"
        rf"id\s*=\s*\"{re.escape(unit_id)}\",\s*\}}\),?",
        re.S,
    )


def build_vr_block(unit_id: str, group: str, entries: list[tuple[str, int, str]]) -> str:
    # group entries by slot preserving order
    by_slot: dict[str, list[tuple[int, str]]] = {}
    order: list[str] = []
    for slot, tid, text in entries:
        if slot not in by_slot:
            order.append(slot)
            by_slot[slot] = []
        by_slot[slot].append((tid, text))
    parts = ["\t\t\t\tPlaceObj('ModItemVoiceResponse', {"]
    for slot in order:
        parts.append(f"\t\t\t\t\t{slot} = TConcat({{")
        lines = by_slot[slot]
        for i, (tid, text) in enumerate(lines):
            esc = text.replace("\\", "\\\\").replace('"', '\\"')
            comma = "," if i < len(lines) - 1 else ""
            parts.append(
                f"\t\t\t\t\t\tT({tid}, --[[ModItemVoiceResponse {unit_id} {slot} "
                f"VoiceResponse {slot} voice:{unit_id}]] \"{esc}\"){comma}"
            )
        parts.append("\t\t\t\t\t}),")
    parts.append(f'\t\t\t\t\tgroup = "{group}",')
    parts.append(f'\t\t\t\t\tid = "{unit_id}",')
    parts.append("\t\t\t\t}),")
    return "\n".join(parts)


def append_loc(path: Path, rows: list[tuple[int, str]], dry: bool) -> None:
    if dry or not rows:
        return
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.endswith("\n"):
        raw += "\n"
    # Format: ID,Text,Translation,VoiceActor,Context
    additions = []
    for tid, text in rows:
        # escape CSV fields that contain commas/quotes
        def esc(s: str) -> str:
            if any(c in s for c in ',|"\n'):
                return '"' + s.replace('"', '""') + '"'
            return s

        additions.append(
            f"{tid},{esc(text)},{esc(text)},,jazz-units:items.lua:VoiceResponse"
        )
    path.write_text(raw + "\n".join(additions) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with MAP.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    items = ITEMS.read_text(encoding="utf-8")
    tid = TID_START
    # bump past any existing
    existing = [int(x) for x in re.findall(r"T\((8900\d+),", items)]
    if existing:
        tid = max(max(existing) + 1, TID_START)

    ru_rows: list[tuple[int, str]] = []
    en_rows: list[tuple[int, str]] = []
    changed = 0

    for row in rows:
        status = row.get("status", "")
        pid = (row.get("profile_id") or "").strip()
        unit = row["unit_id"]
        if status not in ("ready", "ready_tentative") or not pid:
            continue
        # Find VR block by id= line, then look backwards to PlaceObj start
        id_re = re.compile(
            rf"PlaceObj\('ModItemVoiceResponse',\s*\{{(.*?)\bid\s*=\s*\"{re.escape(unit)}\"",
            re.S,
        )
        # Non-greedy can span previous blocks — take the LAST match before id within a short window
        matches = list(
            re.finditer(
                rf"PlaceObj\('ModItemVoiceResponse',\s*\{{",
                items,
            )
        )
        target = None
        for pm in matches:
            window = items[pm.start() : pm.start() + 8000]
            im = re.search(rf'id\s*=\s*\"{re.escape(unit)}\"', window)
            if not im:
                continue
            # ensure no other id= before this id in window
            body = window[: im.start()]
            if re.search(r"\bid\s*=\s*\"", body):
                continue
            target = (pm.start(), im.start() + pm.start(), body)
            break
        if not target:
            print(f"SKIP {unit}: no VR PlaceObj")
            continue
        start, id_abs, body = target
        if "TConcat" in body:
            n_t = body.count("T(")
            print(f"SKIP {unit}: VR already filled ({n_t} T)")
            continue

        lines = load_mercedt(pid)
        # NightOps overlay EDT (eskimo 065, manuel 071, …); UB/ЦС packs are voice-only
        if not lines:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "ex", JAZZ / "docs/tools/_extract_ja2_mercedt.py"
            )
            ex = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ex)
            edt_dir = Path(
                r"C:\Users\SsAnd\Downloads\NightOps_v1.50.14\ja2no150\NightOps\Mercedt"
            )
            # strip U_ prefix for numeric lookup when needed
            num = pid[2:] if pid.upper().startswith("U_") else pid
            for cand in (
                edt_dir / f"{pid}.edt",
                edt_dir / f"{pid}.EDT",
                edt_dir / f"{num.zfill(3)}.edt",
                edt_dir / f"{num.zfill(3)}.EDT",
            ):
                if cand.exists():
                    for i, t in enumerate(ex.decode_edt(cand.read_bytes())):
                        if t:
                            lines[f"{i:03d}"] = t
                    break

        group_m = re.search(r'group\s*=\s*"([^"]+)"', body)
        group = group_m.group(1) if group_m else "MercenariesOld"

        entries: list[tuple[str, int, str]] = []
        for slot, prefs, ru_fb, en_fb in SLOT_LINES:
            ru = pick_text(lines, prefs, ru_fb)
            en = en_fb
            entries.append((slot, tid, ru))
            ru_rows.append((tid, ru))
            en_rows.append((tid, en))
            print(f"  {unit} {slot} tid={tid} <- {ru[:60]}")
            tid += 1

        new_block = build_vr_block(unit, group, entries)
        pat = empty_vr_pattern(unit)
        new_items, n = pat.subn(new_block, items, count=1)
        if n != 1:
            print(f"FAIL {unit}: empty VR regex replace n={n}")
            continue
        items = new_items
        changed += 1
        print(f"INJECT {unit} pid={pid} lines={len(entries)}")

    print(f"\nWould inject {changed} mercs, new tids up to {tid - 1}")
    if args.dry_run:
        return 0
    if changed:
        ITEMS.write_text(items, encoding="utf-8")
        append_loc(RU, ru_rows, False)
        append_loc(EN, en_rows, False)
        print(f"Wrote items.lua + {len(ru_rows)} loc rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
