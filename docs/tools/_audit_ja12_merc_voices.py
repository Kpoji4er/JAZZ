# -*- coding: utf-8 -*-
"""Audit JA12 Jazz_* VoiceResponse T-ids vs jazz-units/voices opus + ship CSV.

Usage (jazz/):
  python docs/tools/_audit_ja12_merc_voices.py
  python docs/tools/_audit_ja12_merc_voices.py --critical  # Selection/AimAttack only
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
MAP_CSV = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
ITEMS = JU / "items.lua"
VOICES = JU / "voices"
VOICES_CAP = JU / "Voices"

CRITICAL_SLOTS = {
    "Selection",
    "SelectionStealth",
    "AimAttack",
    "AimAttackStealth",
    "AimAttack_Low",
    "CombatMovement",
    "GroupOrder",
    "GreetingAndOffer",  # chat — may live in UnitData
}


def voice_exists(vdir: Path, tid: str) -> bool:
    for ext in (".opus", ".wav", ".ogg", ""):
        p = vdir / f"{tid}{ext}" if ext else vdir / tid
        if p.exists() and p.is_file() and p.stat().st_size > 50:
            return True
    return False


def parse_vr_blocks(items_text: str) -> dict[str, list[tuple[str, str]]]:
    parts = re.split(r"PlaceObj\('ModItemVoiceResponse',\s*\{", items_text)
    out: dict[str, list[tuple[str, str]]] = {}
    for part in parts[1:]:
        m = re.search(r"'id',\s*\"([^\"]+)\"", part) or re.search(
            r'id\s*=\s*"([^"]+)"', part
        )
        if not m:
            m = re.search(r"'name',\s*\"([^\"]+)\"", part)
        if not m:
            continue
        uid = m.group(1)
        # Bound body to this PlaceObj (depth-ish: until next sibling PlaceObj at similar indent)
        end = re.search(r"\n\t+PlaceObj\(", part[200:])
        body = part[: end.start() + 200] if end else part[:120000]
        entries: list[tuple[str, str]] = []
        for km in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*=\s*TConcat\(\{", body, re.M):
            slot = km.group(1)
            start = km.end()
            nxt = re.search(r"^\s*[A-Za-z0-9_]+\s*=\s*", body[start:], re.M)
            chunk = body[start : start + nxt.start()] if nxt else body[start:]
            for tid in re.findall(r"T\((\d+),", chunk):
                entries.append((slot, tid))
        out[uid] = entries
    return out


def load_ship_csv() -> dict[str, dict]:
    rows = {}
    if not MAP_CSV.exists():
        return rows
    with MAP_CSV.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            uid = (row.get("unit_id") or "").strip()
            if uid:
                rows[uid] = row
    return rows


def find_translated_voices(items: str) -> list[str]:
    out = []
    for m in re.finditer(
        r"PlaceObj\('ModItemTranslatedVoices',\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}\)",
        items,
    ):
        block = m.group(1)
        folder = re.search(r"'translatedVoicesFolder',\s*\"([^\"]+)\"", block)
        lang = re.search(r"'language',\s*\"([^\"]+)\"", block)
        out.append(
            f"lang={lang.group(1) if lang else '?'} folder={folder.group(1) if folder else 'MISSING'}"
        )
    return out


def g_voice_variations_refs(ju: Path) -> list[str]:
    hits = []
    for p in ju.rglob("*.lua"):
        if "node_modules" in str(p):
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "g_VoiceVariations[" in t or 'g_VoiceVariations["' in t:
            # skip comments-only
            if re.search(r"^\s*g_VoiceVariations\[", t, re.M):
                hits.append(str(p.relative_to(ju)))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--critical", action="store_true")
    args = ap.parse_args()

    items = ITEMS.read_text(encoding="utf-8", errors="replace")
    vr = parse_vr_blocks(items)
    ship = load_ship_csv()
    opus_count = sum(1 for p in VOICES.glob("*.opus") if p.stat().st_size > 50)
    cap_count = (
        sum(1 for p in VOICES_CAP.glob("*.opus") if p.stat().st_size > 50)
        if VOICES_CAP.exists()
        else 0
    )

    print("=== Mount / overrides ===")
    for line in find_translated_voices(items):
        print("  ModItemTranslatedVoices:", line)
    vv = g_voice_variations_refs(JU)
    print(f"  g_VoiceVariations assignments: {len(vv)}")
    for h in vv[:20]:
        print("   ", h)
    print(f"  voices/*.opus usable: {opus_count}")
    print(f"  Voices/*.opus (capital): {cap_count}")

    jazz_vr = {k: v for k, v in vr.items() if k.startswith("Jazz_")}
    print(f"\n=== Jazz_* VoiceResponse presets: {len(jazz_vr)} ===")

    # UnitData with VoiceResponseId
    vr_links = dict(
        re.findall(
            r"'Id',\s*\"(Jazz_[^\"]+)\"[\s\S]{0,4000}?'VoiceResponseId',\s*\"([^\"]+)\"",
            items,
        )
    )

    should = []
    for uid, row in ship.items():
        st = (row.get("status") or "").strip()
        if st in ("need_pack", "missing") and not (row.get("profile_id") or "").strip():
            continue
        if st == "done_manual":
            continue
        should.append(uid)

    print(f"Ship CSV voice-eligible (excl need_pack empty / done_manual): {len(should)}")

    ok = partial = none = need_pack = 0
    rows_out = []
    for uid in sorted(set(list(jazz_vr.keys()) + should + list(vr_links.keys()))):
        entries = jazz_vr.get(uid, [])
        if args.critical:
            entries = [(s, t) for s, t in entries if s in CRITICAL_SLOTS]
        tids = sorted({t for _, t in entries})
        present = [t for t in tids if voice_exists(VOICES, t)]
        missing = [t for t in tids if not voice_exists(VOICES, t)]
        ship_row = ship.get(uid)
        status_csv = ship_row.get("status") if ship_row else "-"
        if ship_row and status_csv in ("need_pack", "missing") and not (
            ship_row.get("profile_id") or ""
        ).strip():
            tag = "need_pack"
            need_pack += 1
        elif not tids:
            tag = "no_VR"
        elif not missing:
            tag = "ok"
            ok += 1
        elif present:
            tag = f"missing {len(missing)}"
            partial += 1
        else:
            tag = f"NONE ({len(tids)} tids)"
            none += 1
        link = vr_links.get(uid, "?")
        crit_miss = []
        for slot, tid in entries:
            if slot in CRITICAL_SLOTS and not voice_exists(VOICES, tid):
                crit_miss.append(f"{slot}:{tid}")
        rows_out.append(
            (
                uid,
                tag,
                status_csv,
                len(tids),
                len(present),
                len(missing),
                link,
                crit_miss[:6],
                missing[:8],
            )
        )

    print(
        f"\n{'unit':28} {'tag':18} csv_status  tids present miss VR_link  crit_miss / sample_miss"
    )
    for uid, tag, st, n, p, m, link, cm, sm in rows_out:
        extra = (" crit=" + ",".join(cm)) if cm else ""
        if m and not cm:
            extra = " miss=" + ",".join(sm)
        print(f"{uid:28} {tag:18} {str(st):10} {n:4} {p:4} {m:4} link={link}{extra}")

    print(
        f"\nSummary: ok={ok} partial={partial} none={none} need_pack={need_pack} "
        f"jazz_VR={len(jazz_vr)} ship_eligible={len(should)}"
    )

    # Colby vs first silent with NONE or many missing
    colby = jazz_vr.get("Jazz_Colby", [])
    print(f"\n=== Colby gold: {len(colby)} lines, "
          f"present={sum(1 for _,t in colby if voice_exists(VOICES,t))} ===")
    for sample_uid in (
        "Jazz_Ira",
        "Jazz_Hobbit",
        "Jazz_Spider",
        "Jazz_Hitman",
        "Jazz_Barry",
        "Jazz_Lynx",
        "Jazz_Blade",
        "Jazz_Benny",
        "Jazz_Grom",
    ):
        ents = jazz_vr.get(sample_uid)
        if ents is None:
            print(f"{sample_uid}: NO VR preset")
            continue
        tids = {t for _, t in ents}
        print(
            f"{sample_uid}: {len(ents)} lines / {len(tids)} unique; "
            f"present={sum(1 for t in tids if voice_exists(VOICES,t))} "
            f"missing={sum(1 for t in tids if not voice_exists(VOICES,t))}"
        )
        # Selection / AimAttack sample
        for slot in ("Selection", "AimAttack"):
            slot_t = [t for s, t in ents if s == slot]
            for t in slot_t[:3]:
                print(f"  {slot} T({t}) file={'YES' if voice_exists(VOICES,t) else 'NO'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
