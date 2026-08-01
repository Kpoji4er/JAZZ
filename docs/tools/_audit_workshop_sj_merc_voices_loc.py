# -*- coding: utf-8 -*-
"""Audit Workshop AIM + Shady Job merc voices + RU/EN localization wiring.

Scope: Merc_AnnieDubois, Merc_CarolThompson, Merc_HectorSanchez,
Merc_JerrySinclair, Merc_MildredPatterson, Merc_SamuelNkosi,
Jazz_Benny, Jazz_Simon, Jazz_Grom.

Usage (jazz/):
  python docs/tools/_audit_workshop_sj_merc_voices_loc.py
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
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
    "Jazz_Benny",
    "Jazz_Simon",
    "Jazz_Grom",
]

WORKSHOP_IDS = ("sH5nmG", "Q6ivSk4", "jkp5GEJ", "E5rtcCe", "QkMtGCa", "HgzATh3")

PORTRAIT_STEM = {
    "Merc_AnnieDubois": "Annie",
    "Merc_CarolThompson": "Carol",
    "Merc_HectorSanchez": "Hector",
    "Merc_JerrySinclair": "Jerry",
    "Merc_MildredPatterson": "Mildred",
    "Merc_SamuelNkosi": "Samuel",
    "Jazz_Benny": "Benny",
    "Jazz_Simon": "Simon",
    "Jazz_Grom": "Grom",
}


def load_csv_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    # Skip sep=,
    lines = text.splitlines()
    if lines and lines[0].startswith("sep="):
        lines = lines[1:]
    reader = csv.DictReader(lines)
    ids = set()
    for row in reader:
        i = (row.get("ID") or "").strip()
        if i:
            ids.add(i)
    return ids


def voice_exists(vdir: Path, tid: str) -> bool:
    for ext in (".opus", ".wav", ".ogg", ""):
        p = vdir / f"{tid}{ext}" if ext else vdir / tid
        if p.exists() and p.is_file() and p.stat().st_size > 50:
            return True
    return False


def parse_vr_blocks(items_text: str) -> dict[str, list[tuple[str, str]]]:
    """unit_id -> [(slot, tid), ...]"""
    parts = re.split(r"PlaceObj\('ModItemVoiceResponse',\s*\{", items_text)
    out: dict[str, list[tuple[str, str]]] = {}
    for part in parts[1:]:
        m = re.search(r'id\s*=\s*"([^"]+)"', part)
        if not m:
            continue
        uid = m.group(1)
        body = part[: m.start()]
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


def extract_merc_tids(items_text: str, unit_data_text: str, perk_texts: list[str], voices_lua: str | None) -> set[str]:
    tids: set[str] = set()
    # All T(id, ... voice:Unit) or any T near merc name in items block
    for blob in [items_text, unit_data_text] + perk_texts:
        if not blob:
            continue
        for tid in re.findall(r"T\((\d+)\s*,", blob):
            tids.add(tid)
    if voices_lua:
        for tid in re.findall(r"g_VoiceVariations\['(\d+)'\]", voices_lua):
            tids.add(tid)
    return tids


def find_folder_block(items: str, folder_name: str) -> str:
    """Extract ModItemFolder named folder_name content table."""
    needle = f"'name', \"{folder_name}\""
    i = items.find(needle)
    if i < 0:
        # UnitData-only slice
        pat2 = re.compile(
            rf"PlaceObj\('ModItemUnitDataCompositeDef',\s*\{{[\s\S]*?'Id',\s*\"{re.escape(folder_name)}\"",
        )
        m2 = pat2.search(items)
        if not m2:
            return ""
        return items[m2.start() : m2.start() + 40000]
    j = items.find("}, {", i)
    if j < 0:
        j = items.find("},{", i)
    start = (j + 4) if j >= 0 else i
    nxt = items.find("\n\t\tPlaceObj('ModItemFolder',", start)
    end = nxt if nxt >= 0 else min(len(items), start + 150000)
    return items[start:end]


def main() -> int:
    items = (JU / "items.lua").read_text(encoding="utf-8", errors="replace")
    meta = (JU / "metadata.lua").read_text(encoding="utf-8", errors="replace")
    vdir = JU / "voices"
    portraits = JU / "MercPortraits"
    ru_ids = load_csv_ids(JAZZ / "Russian.csv")
    en_ids = load_csv_ids(JAZZ / "English.csv")
    # also jazz-units csv if present
    ju_ru = load_csv_ids(JU / "Russian.csv") if (JU / "Russian.csv").exists() else set()
    ju_en = load_csv_ids(JU / "English.csv") if (JU / "English.csv").exists() else set()
    ru_all = ru_ids | ju_ru
    en_all = en_ids | ju_en

    vr = parse_vr_blocks(items)
    print(f"Parsed VR units: {len(vr)}")
    print(f"Russian.csv IDs: jazz={len(ru_ids)} ju={len(ju_ru)}")
    print(f"English.csv IDs: jazz={len(en_ids)} ju={len(ju_en)}")
    print()

    # Workshop leftovers in merc-related code/data only (not full-tree crawl)
    leftover_hits: list[str] = []
    scan_files: list[Path] = []
    for root in (
        JAZZ / "Code" / "WorkshopMercs",
        JAZZ / "CharacterEffect",
        JU / "Code" / "WorkshopMercs",
        JU / "UnitData",
    ):
        if root.exists():
            scan_files.extend(root.rglob("*.lua"))
    for p in scan_files:
        name = p.name
        if not any(
            x in name
            for x in (
                "Annie",
                "Carol",
                "Hector",
                "Jerry",
                "Mildred",
                "Samuel",
                "Benny",
                "Simon",
                "Grom",
            )
        ):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for wid in WORKSHOP_IDS:
            if wid in txt:
                leftover_hits.append(f"{p}: {wid}")

    print("=== Workshop mod ID leftovers ===")
    if leftover_hits:
        for h in leftover_hits:
            print(f"  {h}")
    else:
        print("  none")
    print()

    rows = []
    all_missing_loc_ru: set[str] = set()
    all_missing_loc_en: set[str] = set()

    critical_slots = {
        "Selection",
        "AimAttack",
        "DeathGeneral",
        "Downed",
        "CombatStartDetected",
        "AmmoLow",
        "OpponentKilled",
    }

    for merc in MERCS:
        ud_path = JU / "UnitData" / f"{merc}.lua"
        ud_exists = ud_path.exists()
        ud_text = ud_path.read_text(encoding="utf-8", errors="replace") if ud_exists else ""
        voices_code = JU / "Code" / "WorkshopMercs" / f"{merc}_Voices.lua"
        voices_code_exists = voices_code.exists()
        voices_lua = voices_code.read_text(encoding="utf-8", errors="replace") if voices_code_exists else ""
        voices_in_meta_code = f"Code/WorkshopMercs/{merc}_Voices.lua" in meta or (
            f"UnitData/{merc}.lua" in meta
        )
        ud_in_meta = f"UnitData/{merc}.lua" in meta
        voices_in_meta = f"{merc}_Voices.lua" in meta

        # items UnitData + VR
        folder = find_folder_block(items, merc)
        has_unitdata_item = f"'Id', \"{merc}\"" in items or f'Id", "{merc}"' in items
        has_vr_meta = f"'Id', \"{merc}\"" in meta and "VoiceResponse" in meta
        # more precise VR resource
        vr_meta = bool(
            re.search(
                rf"PlaceObj\('ModResourcePreset',\s*\{{[^}}]*'Class',\s*\"VoiceResponse\"[^}}]*'Id',\s*\"{re.escape(merc)}\"",
                meta,
                re.S,
            )
            or re.search(
                rf"'Class',\s*\"VoiceResponse\",\s*'Id',\s*\"{re.escape(merc)}\"",
                meta,
            )
        )
        ud_meta = bool(
            re.search(
                rf"'Class',\s*\"UnitDataCompositeDef\",\s*'Id',\s*\"{re.escape(merc)}\"",
                meta,
            )
        )

        vr_entries = vr.get(merc, [])
        # also chat T ids with voice:merc from folder/items
        chat_tids = re.findall(
            rf"T\((\d+),\s*--\[\[.*?voice:{re.escape(merc)}\]\]",
            folder or items,
        )
        # UnitData companion chat tids
        chat_tids += re.findall(
            rf"T\((\d+),\s*--\[\[.*?voice:{re.escape(merc)}\]\]",
            ud_text,
        )

        # VoiceVariations registered tids (legacy; Grom-style uses TranslatedVoices mount)
        vv_tids = re.findall(r"g_VoiceVariations\['(\d+)'\]", voices_lua)
        vv_bad_paths = sorted(
            set(
                re.findall(
                    r"CurrentModPath\s*\.\.\s*'((?:Voices|voices)/[^']+)'",
                    voices_lua,
                )
            )
        )
        # Prefer lowercase voices/ matching ModItemTranslatedVoices folder
        vv_case_risk = [p for p in vv_bad_paths if p.startswith("Voices/")]

        # All VR + chat voice tids that need audio
        audio_tids = sorted(set([t for _, t in vr_entries] + chat_tids + vv_tids))
        miss_audio = [t for t in audio_tids if not voice_exists(vdir, t)]
        ok_audio = len(audio_tids) - len(miss_audio)

        # critical VR slots missing files
        crit_miss = []
        by_slot: dict[str, list[str]] = defaultdict(list)
        for slot, tid in vr_entries:
            by_slot[slot].append(tid)
        for slot in critical_slots:
            tids = by_slot.get(slot, [])
            if not tids:
                crit_miss.append(f"{slot}:NO_LINE")
            elif all(not voice_exists(vdir, t) for t in tids):
                crit_miss.append(f"{slot}:NO_FILE")

        # Portrait
        stem = PORTRAIT_STEM.get(merc, merc)
        port = (portraits / f"{stem}.png").exists()
        big = (portraits / f"{stem}_Big.png").exists()
        # portrait paths in UnitData
        port_paths = re.findall(r"Portrait\s*=\s*\"([^\"]+)\"", ud_text)
        port_paths += re.findall(r"'Portrait',\s*\"([^\"]+)\"", folder)
        big_paths = re.findall(r"BigPortrait\s*=\s*\"([^\"]+)\"", ud_text)
        big_paths += re.findall(r"'BigPortrait',\s*\"([^\"]+)\"", folder)

        # Localization: all T ids in merc folder + companion + perk in jazz CharacterEffect
        perk_paths = list((JAZZ / "CharacterEffect").glob(f"{merc}*.lua"))
        perk_paths += list((JU / "CharacterEffect").glob(f"{merc}*.lua")) if (JU / "CharacterEffect").exists() else []
        perk_texts = [p.read_text(encoding="utf-8", errors="replace") for p in perk_paths]
        # CombatAction in jazz
        ca_paths = list((JAZZ / "Code" / "WorkshopMercs").glob(f"{merc}*.lua")) if (JAZZ / "Code" / "WorkshopMercs").exists() else []
        ca_texts = [p.read_text(encoding="utf-8", errors="replace") for p in ca_paths]

        # Collect T ids that appear with merc context
        loc_tids: set[str] = set()
        # SJ stubs are not in ModItemFolder — UnitData companion + VR/chat only
        sj_stub = merc.startswith("Jazz_")
        blobs = [ud_text] + perk_texts + ca_texts
        if not sj_stub:
            blobs.insert(0, folder)
        for blob in blobs:
            if not blob:
                continue
            for tid in re.findall(r"T\((\d+)\s*,", blob):
                loc_tids.add(tid)
        # VR entries
        for _, tid in vr_entries:
            loc_tids.add(tid)
        for tid in chat_tids:
            loc_tids.add(tid)

        # Filter: only IDs that look mod-only OR appear in jazz csv already; report missing from both
        # For workshop mercs, IDs are 12-digit random; for Jazz_ SJ stubs, 8900...
        miss_ru = sorted(t for t in loc_tids if t not in ru_all)
        miss_en = sorted(t for t in loc_tids if t not in en_all)
        all_missing_loc_ru.update(miss_ru)
        all_missing_loc_en.update(miss_en)

        # VV vs VR coverage for workshop
        vv_missing_reg = [t for t in audio_tids if voices_code_exists and t not in set(vv_tids) and (t in [x for _, x in vr_entries] or t in chat_tids)]

        rows.append(
            {
                "merc": merc,
                "ud_file": ud_exists,
                "ud_meta_code": ud_in_meta,
                "ud_meta_res": ud_meta,
                "vr_lines": len(vr_entries),
                "vr_meta": vr_meta,
                "voices_lua": voices_code_exists,
                "voices_meta": voices_in_meta,
                "audio_ok": ok_audio,
                "audio_miss": len(miss_audio),
                "crit_miss": crit_miss,
                "miss_sample": miss_audio[:8],
                "vv_unreg": len(vv_missing_reg) if voices_code_exists else "n/a",
                "loc_total": len(loc_tids),
                "miss_ru": len(miss_ru),
                "miss_en": len(miss_en),
                "portrait": port and big,
                "port_paths": port_paths[:1] + big_paths[:1],
            }
        )

        print(f"=== {merc} ===")
        print(f"  UnitData file: {ud_exists}  meta.code: {ud_in_meta}  meta.resource: {ud_meta}")
        print(f"  VR lines: {len(vr_entries)}  meta.VR resource: {vr_meta}")
        print(f"  Voices.lua: {voices_code_exists}  meta.code: {voices_in_meta}")
        print(f"  Audio: ok={ok_audio} missing={len(miss_audio)} critical_gaps={crit_miss or 'none'}")
        if miss_audio[:8]:
            print(f"  Missing sample: {miss_audio[:8]}")
        if voices_code_exists:
            print(f"  VV registered: {len(vv_tids)}  VR/chat not in VV: {len(vv_missing_reg)}")
            if vv_tids:
                print(
                    "  WARN: g_VoiceVariations overrides bypass ModItemTranslatedVoices "
                    "(Grom has none — prefer empty Voices.lua)"
                )
            if vv_case_risk:
                print(
                    f"  WARN: VV paths use Voices/ (capital V) — mount is voices/; "
                    f"sample={vv_case_risk[:3]}"
                )
        # Affiliation / salary (SJ stubs)
        aff = re.search(r"Affiliation\s*=\s*\"([^\"]+)\"", ud_text)
        sal = re.search(r"StartingSalary\s*=\s*(\d+)", ud_text)
        if merc.startswith("Jazz_") or merc.startswith("Merc_"):
            print(
                f"  Affiliation: {aff.group(1) if aff else '(default)'}  "
                f"StartingSalary: {sal.group(1) if sal else '?'}"
            )
            if aff and aff.group(1) != "AIM" and merc.startswith("Jazz_"):
                print("  WARN: SJ merc Affiliation is not AIM")
            if sal and int(sal.group(1)) == 0:
                print("  WARN: StartingSalary=0 (AIM hire div0 risk)")
        print(f"  Loc T-ids: {len(loc_tids)}  needs RU={len(miss_ru)} EN={len(miss_en)}")
        if miss_ru[:10]:
            print(f"  Missing RU sample: {miss_ru[:10]}")
        if miss_en[:10]:
            print(f"  Missing EN sample: {miss_en[:10]}")
        print(f"  Portraits disk: {port}/{big}  paths={port_paths[:1]} {big_paths[:1]}")
        print()

    print("=== MATRIX ===")
    print(
        f"{'merc':28s} {'UD':4s} {'VR':4s} {'V.lua':5s} {'audio':12s} {'locRU':6s} {'locEN':6s} {'port':5s}"
    )
    for r in rows:
        print(
            f"{r['merc']:28s} "
            f"{'Y' if r['ud_file'] else 'N':4s} "
            f"{r['vr_lines']:4d} "
            f"{'Y' if r['voices_lua'] else 'N':5s} "
            f"{r['audio_ok']}/{r['audio_miss']:<6d} "
            f"{r['miss_ru']:6d} "
            f"{r['miss_en']:6d} "
            f"{'Y' if r['portrait'] else 'N':5s}"
        )

    print()
    print(f"TOTAL unique missing loc RU={len(all_missing_loc_ru)} EN={len(all_missing_loc_en)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
