# -*- coding: utf-8 -*-
"""Repair JA2 voice remaps after wrong prior ships.

1) Jazz_Gaston: delete Malice/032 opus for his VR T-ids; replace Malice subtitle
   texts with generic Gaston fallbacks (no SPEECH pack found in NO/ЦС/Бычок).
2) Jazz_Nervous / Jazz_Hitman: refresh VR RU texts from mercedt for CSV pids
   (041 Haywire / 064 Slay) and re-ship opus via _ship_ja2_merc_voices.

Usage (jazz/):
  python docs/tools/_repair_ja2_voice_remaps.py --dry-run
  python docs/tools/_repair_ja2_voice_remaps.py
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MERCEDT = JAZZ / "docs/design/mercs-ja12/_voice-source/ja2no-mercedt"
ITEMS = JU / "items.lua"
VOICES = JU / "voices"
RU = JAZZ / "Russian.csv"
EN = JAZZ / "English.csv"
SHIP = JAZZ / "docs/tools/_ship_ja2_merc_voices.py"

# Gaston T-ids from wrong Malice ship (keep IDs, clear audio + texts).
GASTON_TIDS = list(range(890000000006360, 890000000006372))
GASTON_TEXTS: list[tuple[str, str, str]] = [
    # slot, ru, en
    ("Selection", "Gaston à l'appareil.", "Gaston here."),
    ("AimAttack", "Есть цель!", "Target!"),
    ("AimAttack", "В бой!", "Engage!"),
    ("OpponentKilled", "Готов.", "Down."),
    ("DeathGeneral", "Конец...", "That's it..."),
    ("Downed", "Ранен!", "I'm hit!"),
    ("AmmoLow", "Патроны!", "Low ammo!"),
    ("CombatStartDetected", "Контакт!", "Contact!"),
    ("Idle", "Жду.", "Waiting."),
    ("LevelUp", "Учусь.", "Learning."),
    ("MockDislike1", "Только не это.", "Not this."),
    ("PraisesBuddy1", "Отличная работа.", "Nice work."),
]

# slot -> mercedt line prefs, en fallback (same as inject stubs)
SLOT_LINES: list[tuple[str, list[str], str]] = [
    ("Selection", ["108", "084", "072"], "Online."),
    ("AimAttack", ["000", "001", "027"], "Target!"),
    ("AimAttack", ["001", "000", "027"], "Engage!"),
    ("OpponentKilled", ["027", "028", "032"], "Down."),
    ("DeathGeneral", ["014", "015", "016"], "That's it..."),
    ("Downed", ["021", "024", "014"], "I'm hit!"),
    ("AmmoLow", ["013", "012"], "Low ammo!"),
    ("CombatStartDetected", ["001", "000", "072"], "Contact!"),
    ("Idle", ["035", "045", "046"], "Waiting."),
    ("LevelUp", ["046", "035"], "Learning."),
    ("MockDislike1", ["029", "031"], "Not this."),
    ("PraisesBuddy1", ["051", "053", "052"], "Nice work."),
]

REMAP_UNITS = {
    "Jazz_Nervous": "041",
    "Jazz_Hitman": "064",
}


def load_mercedt(pid: str) -> dict[str, str]:
    files = list(MERCEDT.glob(f"{pid}_*.csv"))
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


def find_vr_span(items: str, unit_id: str) -> tuple[int, int] | None:
    for pm in re.finditer(r"PlaceObj\('ModItemVoiceResponse',\s*\{", items):
        window = items[pm.start() : pm.start() + 8000]
        im = re.search(rf'id\s*=\s*\"{re.escape(unit_id)}\"', window)
        if not im:
            continue
        body = window[: im.start()]
        if re.search(r"\bid\s*=\s*\"", body):
            continue
        # end of PlaceObj: first `}),` after id line that closes VR
        end_rel = window.find("}),", im.end())
        if end_rel < 0:
            return None
        return pm.start(), pm.start() + end_rel + 3
    return None


def replace_t_texts_in_vr(
    items: str, unit_id: str, new_pairs: list[tuple[int, str]]
) -> tuple[str, list[int]]:
    """Replace T(tid, ... \"old\") texts inside unit VR block in order of appearance."""
    span = find_vr_span(items, unit_id)
    if not span:
        raise RuntimeError(f"VR block not found for {unit_id}")
    a, b = span
    block = items[a:b]
    tids_found: list[int] = []
    i = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal i
        tid = int(m.group(1))
        tids_found.append(tid)
        if i >= len(new_pairs):
            return m.group(0)
        expect_tid, new_text = new_pairs[i]
        i += 1
        if tid != expect_tid:
            raise RuntimeError(
                f"{unit_id}: tid mismatch at slot {i}: got {tid}, expect {expect_tid}"
            )
        esc = new_text.replace("\\", "\\\\").replace('"', '\\"')
        return f'T({tid}, --[[{m.group(2)}]] "{esc}")'

    new_block, n = re.subn(
        r'T\((\d+),\s*--\[\[(.*?)\]\]\s*\"(?:\\.|[^\"\\])*\"\)',
        repl,
        block,
        flags=re.S,
    )
    if n != len(new_pairs):
        raise RuntimeError(f"{unit_id}: replaced {n} T() but expected {len(new_pairs)}")
    return items[:a] + new_block + items[b:], tids_found


def update_loc_row(path: Path, tid: int, text: str, dry: bool) -> bool:
    raw = path.read_text(encoding="utf-8-sig")
    lines = raw.splitlines()
    key = f"{tid},"
    for idx, line in enumerate(lines):
        if not line.startswith(key) and not line.startswith(f'"{tid}"'):
            # numeric id unquoted
            if not (line.startswith(str(tid) + ",") or line.startswith(f'"{tid}",')):
                continue
        # rebuild: ID,Text,Translation,VoiceActor,Context — keep context/actor if present
        parts = list(csv.reader([line]))[0]
        if len(parts) < 2:
            continue

        def esc(s: str) -> str:
            if any(c in s for c in ',|"\n'):
                return '"' + s.replace('"', '""') + '"'
            return s

        actor = parts[3] if len(parts) > 3 else ""
        ctx = parts[4] if len(parts) > 4 else "jazz-units:items.lua:VoiceResponse"
        lines[idx] = f"{tid},{esc(text)},{esc(text)},{actor},{ctx}"
        if not dry:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    return False


def delete_gaston_opus(dry: bool) -> int:
    n = 0
    for tid in GASTON_TIDS:
        p = VOICES / f"{tid}.opus"
        if p.exists():
            print(f"  DEL {p.name}")
            if not dry:
                p.unlink()
            n += 1
        else:
            print(f"  MISS {p.name}")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-ship", action="store_true")
    args = ap.parse_args()

    items = ITEMS.read_text(encoding="utf-8")

    print("=== Gaston: clear Malice opus + generic texts ===")
    deleted = delete_gaston_opus(args.dry_run)
    gaston_pairs = [(tid, ru) for tid, (_, ru, _) in zip(GASTON_TIDS, GASTON_TEXTS)]
    items, _ = replace_t_texts_in_vr(items, "Jazz_Gaston", gaston_pairs)
    for tid, (_, ru, en) in zip(GASTON_TIDS, GASTON_TEXTS):
        ok_ru = update_loc_row(RU, tid, ru, args.dry_run)
        ok_en = update_loc_row(EN, tid, en, args.dry_run)
        print(f"  loc {tid}: ru={ok_ru} en={ok_en} <- {ru[:40]}")
    print(f"  opus_deleted={deleted}")

    print("=== Nervous/Hitman: refresh VR texts from mercedt ===")
    for unit, pid in REMAP_UNITS.items():
        lines = load_mercedt(pid)
        # discover current tids in order
        span = find_vr_span(items, unit)
        if not span:
            print(f"FAIL {unit}: no VR")
            return 1
        block = items[span[0] : span[1]]
        tids = [int(x) for x in re.findall(r"T\((\d+),", block)]
        if len(tids) != len(SLOT_LINES):
            print(f"FAIL {unit}: tid count {len(tids)} != {len(SLOT_LINES)}")
            return 1
        pairs: list[tuple[int, str]] = []
        for tid, (slot, prefs, en_fb) in zip(tids, SLOT_LINES):
            ru_fb = {
                "Online.": "На связи.",
                "Target!": "Есть цель!",
                "Engage!": "В бой!",
                "Down.": "Готов.",
                "That's it...": "Конец...",
                "I'm hit!": "Ранен!",
                "Low ammo!": "Патроны!",
                "Contact!": "Контакт!",
                "Waiting.": "Жду.",
                "Learning.": "Учусь.",
                "Not this.": "Только не это.",
                "Nice work.": "Отличная работа.",
            }.get(en_fb, "…")
            ru = pick_text(lines, prefs, ru_fb)
            pairs.append((tid, ru))
            ok_ru = update_loc_row(RU, tid, ru, args.dry_run)
            ok_en = update_loc_row(EN, tid, en_fb, args.dry_run)
            print(f"  {unit} {slot} {tid} pid={pid} ru_loc={ok_ru} en_loc={ok_en} <- {ru[:60]}")
        items, _ = replace_t_texts_in_vr(items, unit, pairs)

    if not args.dry_run:
        ITEMS.write_text(items, encoding="utf-8")
        print("Wrote items.lua")

    if not args.skip_ship and not args.dry_run:
        print("=== Re-ship nervous,hitman opus ===")
        r = subprocess.run(
            [sys.executable, str(SHIP), "--only", "nervous,hitman"],
            cwd=str(JAZZ),
        )
        if r.returncode != 0:
            return r.returncode
    elif args.dry_run:
        print("DRY: skip ship")

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
