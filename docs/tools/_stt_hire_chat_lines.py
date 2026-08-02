# -*- coding: utf-8 -*-
"""STT hire stems for AIM mercs whose Jazz text ≠ JA2 audio (Quinten/Highball).

Writes stem→RU draft and optionally applies to UnitData chat via classic AIM_CHAT_WAV map.

Usage (jazz/):
  python docs/tools/_stt_hire_chat_lines.py --only quinten,highball --dry-run
  python docs/tools/_stt_hire_chat_lines.py --only quinten,highball --apply
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(JAZZ / "docs" / "tools"))
from _ship_ja2_merc_voices import (  # noqa: E402
    AIM_CHAT_WAV,
    CACHE,
    JA2MERCS_ROOT,
    find_ffmpeg,
    load_map,
    parse_unitdata_chat,
    resolve_wav,
    wav_to_opus,
)
from _pour_ja12_design_hire_chat import (  # noqa: E402
    load_csv,
    replace_t_string,
    set_csv_translation,
    write_csv,
)

JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
UNITDATA = JU / "UnitData"
ITEMS = JU / "items.lua"
RU_CSV = JAZZ / "Russian.csv"
EN_CSV = JAZZ / "English.csv"

# Hire UI lines the player hears first (keep STT short).
HIRE_STEMS = ["084", "108", "096", "109", "091", "089", "090"]


def stt_wav(wav: Path, model_name: str = "small") -> str:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(wav), language="ru", vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=str, required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", type=str, default="small")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    rows = {r["slug"]: r for r in load_map()}
    items = ITEMS.read_text(encoding="utf-8")
    ru_h, ru_by, ru_orig = load_csv(RU_CSV)
    en_h, en_by, en_orig = load_csv(EN_CSV)
    ffmpeg = find_ffmpeg()

    for slug in [s.strip().lower() for s in args.only.split(",") if s.strip()]:
        row = rows.get(slug)
        if not row:
            print(f"SKIP {slug}: not in map")
            continue
        unit = row["unit_id"]
        pid = row["profile_id"]
        source = row["speech_source"]
        upath = UNITDATA / f"{unit}.lua"
        utext = upath.read_text(encoding="utf-8")
        chat = parse_unitdata_chat(unit)
        print(f"=== {slug} root={JA2MERCS_ROOT}")

        # STT each unique hire stem used by chat slots
        stem_text: dict[str, str] = {}
        for stem in HIRE_STEMS:
            wav = resolve_wav(pid, stem, {}, {}, source)
            if not wav:
                continue
            print(f"  STT {stem} <- {wav.name} ...", flush=True)
            try:
                text = stt_wav(wav, args.model)
            except Exception as e:
                print(f"    FAIL {e}")
                continue
            print(f"    -> {text[:100]}")
            stem_text[stem] = text

        # Map chat slots → first AIM stem with STT
        slot_i: dict[str, int] = {}
        for slot, tid in chat:
            pool = AIM_CHAT_WAV.get(slot) or []
            idx = slot_i.get(slot, 0)
            slot_i[slot] = idx + 1
            ordered = pool[idx % len(pool) :] + pool[: idx % len(pool)] if pool else []
            picked = next((s for s in ordered if s in stem_text and stem_text[s]), None)
            if not picked:
                print(f"  {slot} tid={tid}: no STT")
                continue
            ru = stem_text[picked]
            print(f"  APPLY {slot} tid={tid} stem={picked}: {ru[:60]}")
            utext, _ = replace_t_string(utext, tid, ru)
            items, _ = replace_t_string(items, tid, ru)
            set_csv_translation(ru_by, str(tid), ru, "ru")
            # keep EN as rough copy unless already good — mark [STT-RU]
            set_csv_translation(en_by, str(tid), f"[JA2] {ru}", "en")

        if not args.dry_run:
            upath.write_text(utext, encoding="utf-8")

    if not args.dry_run:
        ITEMS.write_text(items, encoding="utf-8")
        write_csv(RU_CSV, ru_h, ru_by, ru_orig)
        write_csv(EN_CSV, en_h, en_by, en_orig)
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
