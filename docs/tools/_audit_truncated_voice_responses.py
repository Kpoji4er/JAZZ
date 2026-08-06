# -*- coding: utf-8 -*-
"""Audit truncated VoiceResponse strings vs ja2mercs XLSX speech schemas.

Finds JA2-style ~80-char hard cuts in jazz English.csv VoiceResponse rows and
tries to complete them from Downloads/ja2mercs (1) per-merc *.xlsx dialogue.

Usage (jazz/):
  python docs/tools/_audit_truncated_voice_responses.py
  python docs/tools/_audit_truncated_voice_responses.py --ja2mercs "C:/path/to/ja2mercs"

Output: docs/tools/_tmp_truncated_vr_strict.txt (report only; does not apply).
"""
from __future__ import annotations

import argparse
import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
DEFAULT_JA2MERCS = Path(r"C:\Users\SsAnd\Downloads\ja2mercs (1)\ja2mercs")
OUT = JAZZ / "docs/tools/_tmp_truncated_vr_strict.txt"

# Handoff IDs + known completions from XLSX / STT (RU). EN is proposed, not audio-synced.
KNOWN_REPAIRS: dict[str, dict[str, str]] = {
    "890000000006347": {
        "ru": (
            "Потрясающе, Биф! Ну разве удивительно, что ты мне нравишься... "
            "я хочу сказать, что мне так нравится с тобой работать!"
        ),
        "en": (
            "Amazing, Biff! Is it any wonder I like you... "
            "I mean, that I like working with you so much!"
        ),
        "source": "ja2mercs 044-фуфло.xlsx",
    },
    "890000000006372": {
        "ru": (
            "Говорит Кирк Стивенсон. Известный по кличке Статик. "
            "Раньше я говорил только кличку, и все думали, что у меня плохой видеотелефон."
        ),
        "en": (
            "This is Kirk Stevenson, better known as Static. "
            "I used to go only by my nickname, and everyone thought I had a bad video phone."
        ),
        "source": "ja2mercs 026-статик.xlsx",
    },
    "890000000006556": {
        "ru": (
            "Оуууу... Ох, господи, мне так последний раз было, "
            "когда я попробовал починить папашин шредер, знаешь."
        ),
        "en": (
            "Ohhh... Oh, God, the last time I felt like this was "
            "when I tried to fix dad's shredder, you know."
        ),
        "source": "ja2mercs 042-Кардан.xlsx",
    },
    "890000000006430": {
        "ru": (
            "Я не доверяю Игги. Он был враг, стал друг. "
            "Что он будет завтра? Нельзя быть уверенным."
        ),
        "en": (
            "I don't trust Iggy. He was an enemy, became a friend. "
            "What will he be tomorrow? You can never be sure."
        ),
        "source": "STT 058_029.WAV (faster-whisper base) + truncated prefix",
    },
    "890000000006598": {
        "ru": (
            "Эй, слушай и запоминай. Сдоба - пижонка, каких свет не видывал, "
            "и я не обещаю, что сумею удержать свою винтовку, пока она так лачивается. "
            "Нервишки не в порядке, понимаешь?"
        ),
        "en": (
            "Listen and remember. Buns is the biggest poser I've ever seen, "
            "and I don't promise I can keep my rifle off her while she's posing like that. "
            "Nerves aren't good, you know?"
        ),
        "source": "STT 061_031.WAV (faster-whisper base) + truncated prefix; note MockDislike1 SLOT_WAV=029 but matching audio is 031",
    },
}


def looks_hard_cut(s: str) -> bool:
    s = s.strip()
    if len(s) < 70 or len(s) > 95:
        return False
    if s.endswith(("...", "…", "!", "?", ".", "»", '"', ")", "]")):
        return False
    if s.endswith("—"):
        return True
    if re.search(r"[А-Яа-яA-Za-z]$", s):
        return True
    if s.endswith(","):
        return True
    return False


def shared_strings(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        data = zf.read("xl/sharedStrings.xml")
    root = ET.fromstring(data)
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    out = []
    for si in root.findall("m:si", ns):
        parts = [t.text or "" for t in si.findall(".//m:t", ns)]
        out.append("".join(parts))
    return out


def build_prefix_index(ja2mercs: Path) -> dict[str, str]:
    idx: dict[str, str] = {}
    if not ja2mercs.exists():
        return idx
    for f in ja2mercs.rglob("*.xlsx"):
        try:
            strings = shared_strings(f)
        except KeyError:
            continue
        for s in strings:
            s = s.strip()
            if len(s) < 50:
                continue
            if s.startswith(("XXX_", "R_ХХХ", "000 ", "Юнит ")):
                continue
            key = s[:40]
            if key not in idx or len(s) > len(idx[key]):
                idx[key] = s
    return idx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ja2mercs", type=Path, default=DEFAULT_JA2MERCS)
    args = ap.parse_args()

    idx = build_prefix_index(args.ja2mercs)
    hits = []
    with (JAZZ / "English.csv").open(encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            if not row or not row[0].isdigit():
                continue
            loc_id, ru, en = row[0], row[1], row[2] if len(row) > 2 else ""
            joined = ",".join(row)
            if "VoiceResponse" not in joined and "jazz-units" not in joined:
                continue
            if not (looks_hard_cut(ru) or looks_hard_cut(en)):
                continue
            full = idx.get(ru[:40])
            if not (full and full != ru and len(full) > len(ru)):
                full = None
                for k, v in idx.items():
                    if ru.startswith(k[:30]) or k.startswith(ru[:30]):
                        if len(v) > len(ru) + 5:
                            full = v
                            break
            known = KNOWN_REPAIRS.get(loc_id)
            if known:
                status = "KNOWN_REPAIR"
                full = known["ru"]
            elif full:
                status = "FULL_FOUND"
            else:
                status = "NEED_SOURCE"
            hits.append((status, loc_id, ru, en, full or "", known))

    lines = [
        f"strict_hits={len(hits)} "
        f"known={sum(1 for h in hits if h[0]=='KNOWN_REPAIR')} "
        f"xlsx={sum(1 for h in hits if h[0]=='FULL_FOUND')} "
        f"need={sum(1 for h in hits if h[0]=='NEED_SOURCE')}"
    ]
    for status, loc_id, ru, en, full, known in hits:
        lines.append(f"{status}\t{loc_id}")
        lines.append(f"  RU: {ru}")
        lines.append(f"  EN: {en}")
        if full:
            lines.append(f"  FULL_RU: {full}")
        if known:
            lines.append(f"  FULL_EN: {known['en']}")
            lines.append(f"  SOURCE: {known['source']}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(lines[0])
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
