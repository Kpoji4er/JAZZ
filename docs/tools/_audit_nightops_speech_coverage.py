# -*- coding: utf-8 -*-
"""Audit NightOps/JA2 speech packs vs jazz_to_ja2_profile.csv.

Important: EDT *filenames* / index nick fields often LIE in NightOps
(e.g. 030_Hitman.csv is Rothman; 022 is Hitman/Hennessey; 036_Conrad is Scope).
Identity must come from mercedt *text* (greeting 108, hire 080/084, buddy lines)
including Russian nicknames — not from English CSV filenames alone.
"""
from __future__ import annotations

import csv
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:\Users\SsAnd\Downloads\NightOps_v1.50.14\ja2no150")
JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
MAP = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
MERCEDT_DIR = JAZZ / "docs/design/mercs-ja12/_voice-source/ja2no-mercedt"
UB_CS = JAZZ / "docs/design/mercs-ja12/_voice-source/_ub_cs_cache"
HORG_CACHE = JAZZ / "docs/design/mercs-ja12/_voice-source/_horg_stogie_cache"

# RU/EN tokens for need_pack identity search (filename-independent)
IDENTITY_KEYWORDS: dict[str, list[str]] = {
    "blade": ["Бритва", "Ламонт", "Razor"],
    "madman": ["Бешеный", "Камерон", "Maddog", "Madman"],
    "conrad": ["Конрад", "Джиллет", "Джилет", "Conrad"],
    "mike": ["Майк", "Mike"],
    "grom": ["Громов", "Гром", "Сергей"],
    "vicious": ["Злобный", "Вийо", "Вилло", "Malice", "Алле"],
    "biff": ["Биф", "Апскот", "Biff"],
    "cougar": ["Пума", "Уоллас", "Валлэс", "Cougar"],
    "gamos": ["Гамос", "Хамуз", "Hamous"],
    "dynamo": ["Динамо", "Дункан", "Dynamo"],
    "horg": ["Хорг", "Сигара", "Stogie", "Бычок"],
    "manuel": ["Мануэль", "Фатиму", "Пакос", "Manuel"],
    "cord": ["Кардан", "Милтон", "Gasket"],
    "hobbit": ["Хоббит", "Хиллман", "Gumpy"],
    "ricochet": ["Рикошет", "Саттон", "Numb"],
    "devin": ["Девин", "Коннел", "Devin"],
    "vince": ["Винс", "Воймонт", "Vince"],
    "hitman": ["Убийца", "Слэй", "Slay", "Терри", "Рутвен"],
    "biggens": ["Биггенс", "Biggens"],
    "kulba": ["Кульба", "Kulba"],
    "nervous": ["Нервный", "Haywire"],
}


def list_slf_names(path: Path) -> list[tuple[str, int]]:
    data = path.read_bytes()
    i_used = struct.unpack_from("<i", data, 516)[0]
    entry = 280
    start = len(data) - i_used * entry
    out = []
    for i in range(i_used):
        off = start + i * entry
        raw = data[off : off + 256]
        fname = raw.split(b"\x00", 1)[0].decode("latin1", "replace")
        ui_off, ui_len = struct.unpack_from("<II", data, off + 256)
        name = Path(fname.replace("\\", "/")).name
        out.append((name, ui_len))
    return out


def profiles_from_names(names: list[tuple[str, int]]) -> dict[str, int]:
    pfx: dict[str, int] = defaultdict(int)
    for n, ln in names:
        if ln <= 100:
            continue
        u = n.upper()
        if not (u.endswith(".WAV") or u.endswith(".GAP")):
            continue
        stem = u.rsplit(".", 1)[0]
        parts = stem.split("_")
        if parts[0] == "R" and len(parts) >= 2 and parts[1].isdigit():
            pid = parts[1].zfill(3)
        elif parts[0] == "U" and len(parts) >= 2 and parts[1].isdigit():
            pid = "U_" + parts[1]
        elif parts[0].isdigit():
            pid = parts[0].zfill(3)
        else:
            continue
        if u.endswith(".WAV"):
            pfx[pid] += 1
    return dict(pfx)


def folder_profiles(d: Path) -> dict[str, int]:
    if not d.exists():
        return {}
    names = [(p.name, p.stat().st_size) for p in d.rglob("*") if p.is_file()]
    return profiles_from_names(names)


def load_mercedt_identity() -> dict[str, dict[str, str]]:
    """Load per-profile identity from texts (prefer 108/084), not filenames."""
    all_lines = MERCEDT_DIR / "all_lines.csv"
    by: dict[str, dict[str, str]] = defaultdict(dict)
    file_nick: dict[str, str] = {}
    if not all_lines.exists():
        return {}
    with all_lines.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            pid = (row.get("profile_id") or "").zfill(3)
            file_nick[pid] = row.get("nick") or ""
            by[pid][row.get("line") or ""] = row.get("text") or ""

    out: dict[str, dict[str, str]] = {}
    for pid, lines in by.items():
        greeting = ""
        for code in ("108", "084", "080", "051", "000"):
            t = lines.get(code, "")
            if t and not t.startswith("я") and sum(c.isalpha() for c in t) >= 4:
                greeting = t[:120]
                break
        out[pid] = {
            "file_nick": file_nick.get(pid, ""),
            "greeting": greeting,
            "blob": " ".join(lines.values()),
        }
    return out


def search_identity(
    mercedt: dict[str, dict[str, str]], keywords: list[str]
) -> list[str]:
    hits = []
    for pid, info in mercedt.items():
        blob = info.get("blob", "")
        g = info.get("greeting", "")
        for kw in keywords:
            if kw and kw.lower() in blob.lower():
                hits.append(f"{pid}:[{kw}] {g[:70]}")
                break
    return hits


def main() -> None:
    speech = profiles_from_names(list_slf_names(ROOT / "Data" / "SPEECH.SLF"))
    battle = profiles_from_names(list_slf_names(ROOT / "Data" / "BATTLESNDS.SLF"))
    npc = profiles_from_names(list_slf_names(ROOT / "Data" / "NPC_SPEECH.SLF"))
    no_speech = folder_profiles(ROOT / "NightOps" / "SPEECH")
    no_battle = folder_profiles(ROOT / "NightOps" / "Battlesnds")
    no_npc = folder_profiles(ROOT / "NightOps" / "npc_speech")
    ub_cs = folder_profiles(UB_CS)
    horg = folder_profiles(HORG_CACHE)

    print(f"Data/SPEECH profiles={len(speech)} count_sum={sum(speech.values())}")
    print("pids:", ",".join(sorted(speech, key=lambda x: (len(x), x))))
    print(f"\nData/BATTLESNDS profiles={len(battle)}")
    print(f"\nNightOps overlays SPEECH={no_speech} BATTLE={no_battle}")
    print(f"NightOps/npc_speech pids={','.join(sorted(no_npc))}")
    print(f"\nExternal UB/ЦС folder profiles: {dict(sorted(ub_cs.items()))}")
    print(f"External Horg/Бычок folder profiles: {dict(sorted(horg.items()))}")

    mercedt = load_mercedt_identity()
    print("\n=== MERCEDT identity (greeting≠filename) ===")
    for pid in sorted(mercedt, key=lambda x: int(x) if x.isdigit() else 999):
        info = mercedt[pid]
        fn = info["file_nick"]
        g = info["greeting"]
        lie = ""
        if fn and g and fn.lower() not in g.lower() and len(g) > 10:
            # crude mismatch flag when greeting names someone else
            lie = " [CHECK: filename may not match speaker]"
        print(
            f"  {pid}: file_nick={fn!r} speech={pid in speech} "
            f"wavs={speech.get(pid, 0)} greet={g!r}{lie}"
        )

    print("\n=== jazz map vs packs ===")
    with MAP.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        slug = row["slug"]
        pid = (row.get("profile_id") or "").strip()
        status = row.get("status")
        source = row.get("speech_source") or ""
        if pid:
            avail = []
            # numeric / R_ profiles
            num = pid[2:] if pid.upper().startswith("U_") else pid
            numz = num.zfill(3) if num.isdigit() else num
            if numz in speech:
                avail.append(f"SPEECH:{speech[numz]}")
            if numz in no_speech:
                avail.append(f"NO_SPEECH:{no_speech[numz]}")
            if numz in no_npc:
                avail.append(f"NO_NPC:{no_npc[numz]}")
            if pid in ub_cs:
                avail.append(f"UB_CS:{ub_cs[pid]}")
            if numz in ub_cs:
                avail.append(f"UB_CS:{ub_cs[numz]}")
            if numz in horg:
                avail.append(f"HORG:{horg[numz]}")
            print(
                f"  {slug:12s} pid={pid:6s} src={source:18s} status={status} "
                f"avail={','.join(avail) or 'NONE'}"
            )
        else:
            keys = IDENTITY_KEYWORDS.get(slug, [slug])
            hits = search_identity(mercedt, keys)[:5]
            print(
                f"  {slug:12s} pid=--- status={status} "
                f"ru_text_hits={hits or '-'}"
            )

    used = set()
    for r in rows:
        pid = (r.get("profile_id") or "").strip()
        if not pid:
            continue
        if pid.upper().startswith("U_"):
            used.add(pid)
        elif pid.isdigit():
            used.add(pid.zfill(3))
    unused = sorted(set(speech) - used, key=lambda x: int(x) if x.isdigit() else 0)
    print(f"\nSPEECH profiles not in map ({len(unused)}): {','.join(unused)}")
    for pid in unused[:25]:
        info = mercedt.get(pid, {})
        print(
            f"  {pid}: file_nick={info.get('file_nick','?')!r} "
            f"greet={info.get('greeting','')[:70]!r} wavs={speech[pid]}"
        )


if __name__ == "__main__":
    main()
