# -*- coding: utf-8 -*-
"""Ship JA2/NightOps archive voices onto Jazz merc VoiceResponse T-ids.

Reads mapping: docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv
Extracts WAV from Data/SPEECH.SLF + BATTLESNDS.SLF (and NightOps/SPEECH overlays).
Fills each ModItemVoiceResponse T-id: archive line when known, else donor duplicate.

Usage (jazz/):
  python docs/tools/_ship_ja2_merc_voices.py --dry-run
  python docs/tools/_ship_ja2_merc_voices.py --only ira,dimitri
  python docs/tools/_ship_ja2_merc_voices.py --queue
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import struct
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MAP_CSV = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
ITEMS = JU / "items.lua"
VOICES = JU / "voices"
CACHE = JAZZ / "docs/design/mercs-ja12/_voice-source/_wav_cache"
NO_ROOT = Path(r"C:\Users\SsAnd\Downloads\NightOps_v1.50.14\ja2no150")
SPEECH_SLF = NO_ROOT / "Data" / "SPEECH.SLF"
BATTLE_SLF = NO_ROOT / "Data" / "BATTLESNDS.SLF"
NO_SPEECH = NO_ROOT / "NightOps" / "SPEECH"
NO_NPC_SPEECH = NO_ROOT / "NightOps" / "npc_speech"
NO_BATTLE = NO_ROOT / "NightOps" / "Battlesnds"
# External folder packs (speech_source=folder:<rel-or-abs> | horg_stogie_folder | ub_cs_folder).
HORG_FOLDER = (
    JAZZ / "docs/design/mercs-ja12/_voice-source/_horg_stogie_cache"
)
UB_CS_FOLDER = JAZZ / "docs/design/mercs-ja12/_voice-source/_ub_cs_cache"
# JA2 1.13 Wildfire RUS .arc → Data-UB (Gaston 058 Speech+BattleSNDS). Not WF merc voices.
UB_WF_FOLDER = (
    JAZZ
    / "docs/design/mercs-ja12/_voice-source/_wildfire_cache"
    / "Jagged Alliance 2 RUS"
    / "Data-UB"
)
# Shady Job unpacked (Downloads/SJ/data) → _sj_cache (066 Simon, 067 Benny, 076 Gromov)
SJ_FOLDER = JAZZ / "docs/design/mercs-ja12/_voice-source/_sj_cache"

FFMPEG_CANDIDATES = [
    Path(
        r"C:\Users\SsAnd\AppData\Local\Programs\Python\Python312\Lib\site-packages"
        r"\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
    ),
    Path(r"D:\py-voice\RVC-WebUI\ffmpeg.exe"),
]

# Generation-queue order. Spouke is never queued (done_manual — full JA3 voice acting).
# lynx/tosca/spider may be re-shipped from JA2 archive; Spouke must not.
QUEUE = [
    "colby",
    "blade",
    "ira",
    "dimitri",
    "madman",
    "conrad",
    "mike",
    "grom",
    "benny",
    "simon",
    "rothman",
    "quinten",
    "vicious",
    "biff",
    "nervous",
    "flo",
    "cougar",
    "miguel",
    "gamos",
    "dynamo",
    "gaston",
    "horg",
    "manuel",
    "monk",
    "allik",
    "henning",
    "static",
    "highball",
    "bull",
    "cord",
    "hobbit",
    "ricochet",
    "meat",
    "carlos",
    "devin",
    "shank",
    "vince",
    "hitman",
    "biggens",
    "kulba",
    "vilde",
    "grace",
    "steiger",
    "lucky",
    "laura",
    "eskimo",
    "lynx",
    "tosca",
    "spider",
]

# Slot → preferred JA2 stems (without profile prefix). First existing nonempty wins.
# Numeric = SPEECH; named = BATTLESNDS.
SLOT_WAV: dict[str, list[str]] = {
    "Selection": ["ATTN", "COOL", "HUMM", "OK1"],
    "SelectionStealth": ["LMATTN", "LMOK1", "LMOK2"],
    "Order": ["OK1", "OK2", "GOTIT"],
    "CombatMovement": ["OK1", "OK2", "GOTIT"],
    "CombatMovementStealth": ["LMOK1", "LMOK2", "LMATTN"],
    "GroupOrder": ["GOTIT", "OK1", "073"],
    "AimAttack": ["ENEMY", "000", "027"],
    "AimAttackStealth": ["LMOK1", "LMATTN", "006"],
    "AimAttack_Low": ["023"],
    "AimAttack_LowStealth": ["057", "023"],
    "OpponentFound": ["000", "001", "ENEMY"],
    "ManyEnemiesSelection": ["002"],
    "OpponentKilled": ["027", "028", "032"],
    "NoAmmo": ["013"],
    "AmmoLow": ["013"],
    "WeaponJammed": ["019"],
    "WeaponBroken": ["074"],
    "ItemDeteriorates": ["043"],
    "Pain": ["HIT1", "HIT2", "CURSE"],
    "Wounded": ["014", "021"],
    "SeriouslyWounded": ["024"],
    "Downed": ["DIE", "DYING"],
    "SurroundedPain": ["020"],
    "HeavilyWoundedSelection": ["040"],
    "CombatStartPlayer": ["072"],
    "CombatStartDetected": ["001", "ENEMY"],
    "CombatEndNoEnemies": ["065"],
    "CombatEndEnemiesRemain": ["059"],
    "CombatEndEnemiesRetreated": ["070"],
    "DeathGeneral": ["DIE", "CURSE"],
    "DeathBuddy1": ["017", "015"],
    "MockDislike1": ["029"],
    "PraisesBuddy1": ["053"],
    "LevelUp": ["046"],
    "Idle": ["COOL", "HUMM", "045", "NOTH"],
    "BecomeHidden": ["LMATTN", "006"],
    "MineNearbySelection": ["075", "076"],
    "DoorLocked": ["LOCKED"],
    "LootFound": ["011", "012"],
    "ValuableItemFound": ["061"],
    "InteractableFound": ["NOTH", "011"],
    "Tired": ["025"],
    "Exhausted": ["071", "025"],
    "HeavyBreathing": ["026"],
    "SectorArrived": ["078"],
    "ActivityFinished": ["035"],
    "NotNow": ["036"],
    "HealReceived": ["058", "COOL"],
    "Overwatch": ["060"],
    "ThreatSelection": ["008", "007"],
    "OverwatchSelection": ["060", "072"],
    "GasAreaSelection": ["CURSE", "HIT1"],
    "TakeCover": ["042", "020"],
    "MissedByKillShot": ["022"],
    "AnimalFound": ["068", "003"],
    "ThrowGrenade": ["027", "ENEMY"],
    "Autofire": ["027", "OK1"],
    "CombatTaskGiven": ["035", "HUMM"],
    "CombatTaskCompleted": ["048", "035"],
    "CombatTaskFailed": ["047", "057"],
    "Startled": ["006"],
    "Climbing": ["026", "HIT1"],
    "Jumping": ["026", "HIT2"],
    # AIM / chat-ish if present on VR
    "Offline": ["084"],
    "Greeting": ["108"],
    "FriendlyFire": ["CURSE"],
}

FALLBACK = ["OK1", "OK2", "GOTIT", "ATTN", "COOL", "000", "027"]


def find_ffmpeg() -> Path:
    for p in FFMPEG_CANDIDATES:
        if p.exists():
            return p
    which = shutil.which("ffmpeg")
    if which:
        return Path(which)
    raise SystemExit("ffmpeg not found")


def list_slf(path: Path) -> dict[str, tuple[int, int, bytes]]:
    data = path.read_bytes()
    i_used = struct.unpack_from("<i", data, 516)[0]
    entry = 280
    start = len(data) - i_used * entry
    out: dict[str, tuple[int, int, bytes]] = {}
    for i in range(i_used):
        off = start + i * entry
        fname = data[off : off + 256].split(b"\0", 1)[0].decode("latin1", "replace")
        ui_off, ui_len = struct.unpack_from("<II", data, off + 256)
        key = Path(fname.replace("\\", "/")).name.upper()
        out[key] = (ui_off, ui_len, data)
    return out


def extract_slf_file(index: dict[str, tuple[int, int, bytes]], name: str, dest: Path) -> bool:
    key = name.upper()
    if key not in index:
        return False
    ui_off, ui_len, data = index[key]
    if ui_len < 100:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data[ui_off : ui_off + ui_len])
    return True


def _stem_aliases(stem: str) -> list[str]:
    out = [stem]
    if stem == "DIE":
        out.append("DYING")
    if stem == "ENEMY":
        out.extend(["ENEM", "ENEMY2"])
    return out


def _folder_roots(source: str) -> list[Path]:
    """Resolve speech_source=folder:... to search roots."""
    if source.startswith("folder:"):
        raw = source.split(":", 1)[1].strip()
        p = Path(raw)
        if not p.is_absolute():
            p = JAZZ / raw
        return [p] if p.exists() else []
    if source == "horg_stogie_folder":
        return [HORG_FOLDER] if HORG_FOLDER.exists() else []
    if source == "ub_cs_folder":
        # Цена Свободы / UB: U_59 Horg, U_62 Kulba, …
        return [UB_CS_FOLDER] if UB_CS_FOLDER.exists() else []
    if source == "ub_wildfire_folder":
        # Wildfire RUS arc Data-UB (numeric 058 Gaston, …) — not commercial WF AIM voices
        return [UB_WF_FOLDER] if UB_WF_FOLDER.exists() else []
    if source == "sj_folder":
        # Shady Job Khalif: 066 Simon, 067 Benny, 076 Gromov (+ 058 Gaston alt)
        return [SJ_FOLDER] if SJ_FOLDER.exists() else []
    return []


def resolve_wav(
    pid: str,
    stem: str,
    speech_idx: dict,
    battle_idx: dict,
    source: str,
) -> Path | None:
    """Return path to cached WAV for profile+stem."""
    CACHE.mkdir(parents=True, exist_ok=True)
    aliases = _stem_aliases(stem)

    # External folder pack (Horg 166 «Бычок», etc.)
    for root in _folder_roots(source):
        for alias in aliases:
            for name in (
                f"{pid}_{alias}.WAV",
                f"{pid}_{alias}.wav",
                f"R_{pid}_{alias}.WAV",
                f"r_{pid}_{alias}.wav",
            ):
                for p in root.rglob(name):
                    if p.is_file() and p.stat().st_size > 100:
                        dest = CACHE / f"{pid}_{alias}.wav"
                        if not dest.exists() or dest.stat().st_size != p.stat().st_size:
                            shutil.copy2(p, dest)
                        return dest

    # NightOps overlay folders
    if source in ("nightops_speech", "nightops_npc"):
        search_dirs = [NO_SPEECH]
        if source == "nightops_npc":
            search_dirs = [NO_NPC_SPEECH, NO_BATTLE, NO_SPEECH]
        for alias in aliases:
            for d in search_dirs:
                if not d.exists():
                    continue
                for p in list(d.glob(f"{pid}_{alias}.wav")) + list(
                    d.glob(f"{pid}_{alias}.WAV")
                ) + list(d.glob(f"r_{pid}_{alias}.wav")) + list(
                    d.glob(f"R_{pid}_{alias}.WAV")
                ):
                    if p.suffix.lower() == ".wav" and p.stat().st_size > 100:
                        dest = CACHE / f"{pid}_{alias}.wav"
                        if not dest.exists():
                            shutil.copy2(p, dest)
                        return dest

    # Numeric stems → SPEECH; named → BATTLESNDS (DIE also as DYING)
    # NightOps RPC often uses R_NNN_XXX.WAV inside SPEECH.SLF.
    candidates: list[str] = []
    for alias in aliases:
        candidates.append(f"{pid}_{alias}.WAV")
        candidates.append(f"R_{pid}_{alias}.WAV")
        candidates.append(f"r_{pid}_{alias}.wav")

    for name in candidates:
        dest = CACHE / Path(name).name.replace("R_", "").replace("r_", "")
        # normalize cache key to pid_stem.wav
        stem_part = name.split("_", 1)[-1] if name.upper().startswith("R_") else name
        if name.upper().startswith("R_"):
            # R_061_000.WAV → cache 061_000.WAV
            parts = Path(name).stem.split("_")
            if len(parts) >= 3:
                dest = CACHE / f"{parts[1]}_{parts[2]}.wav"
            else:
                dest = CACHE / Path(name).name
        else:
            dest = CACHE / Path(name).name
        if dest.exists() and dest.stat().st_size > 100:
            return dest
        # try SPEECH then BATTLE (exact archive name)
        if extract_slf_file(speech_idx, name, dest):
            return dest
        if extract_slf_file(battle_idx, name, dest):
            return dest
        # case variants in SLF index keys
        for key in (name, name.upper(), name.lower()):
            if extract_slf_file(speech_idx, key, dest):
                return dest
            if extract_slf_file(battle_idx, key, dest):
                return dest
        # NightOps override on top of Data
        if NO_SPEECH.exists():
            for p in NO_SPEECH.glob(name):
                if p.stat().st_size > 100:
                    shutil.copy2(p, dest)
                    return dest
    return None


def wav_to_opus(ffmpeg: Path, wav: Path, opus: Path) -> bool:
    opus.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(ffmpeg),
        "-y",
        "-i",
        str(wav),
        "-af",
        "loudnorm=I=-16:TP=-1.5:LRA=16",
        "-ac",
        "1",
        "-ar",
        "24000",
        "-c:a",
        "libopus",
        "-b:a",
        "48k",
        str(opus),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def load_map() -> list[dict[str, str]]:
    with MAP_CSV.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_vr_blocks(items_text: str) -> dict[str, list[tuple[str, int]]]:
    """unit_id -> list of (slot, tid) in appearance order."""
    parts = re.split(r"PlaceObj\('ModItemVoiceResponse',\s*\{", items_text)
    out: dict[str, list[tuple[str, int]]] = {}
    for part in parts[1:]:
        m = re.search(r'id\s*=\s*"(Jazz_[A-Za-z0-9_]+|JAZZ_[A-Za-z0-9_]+)"', part)
        if not m:
            continue
        uid = m.group(1)
        # Body ends at id= — earlier `}),` matches nested TConcat closers.
        body = part[: m.start()]
        entries: list[tuple[str, int]] = []
        for km in re.finditer(
            r"^\s*([A-Za-z0-9_]+)\s*=\s*TConcat\(\{",
            body,
            re.M,
        ):
            slot = km.group(1)
            start = km.end()
            nxt = re.search(r"^\s*[A-Za-z0-9_]+\s*=\s*", body[start:], re.M)
            chunk = body[start : start + nxt.start()] if nxt else body[start:]
            for tid in re.findall(r"T\((\d+),", chunk):
                entries.append((slot, int(tid)))
        out[uid] = entries
    return out


def pick_stems(slot: str, index_in_slot: int) -> list[str]:
    pool = SLOT_WAV.get(slot) or FALLBACK
    # rotate
    return pool[index_in_slot % len(pool) :] + pool[: index_in_slot % len(pool)] + FALLBACK


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, default="")
    ap.add_argument("--queue", action="store_true", help="Process QUEUE order")
    ap.add_argument("--include-done", action="store_true")
    ap.add_argument("--force-missing-skip", action="store_true", default=True)
    args = ap.parse_args()

    rows = load_map()
    by_slug = {r["slug"]: r for r in rows}
    order = QUEUE if args.queue or not args.only else []
    if args.only:
        order = [s.strip() for s in args.only.split(",") if s.strip()]
    elif not order:
        order = QUEUE

    items_text = ITEMS.read_text(encoding="utf-8")
    vr = parse_vr_blocks(items_text)
    print(f"VR units parsed: {len(vr)}")

    ffmpeg = find_ffmpeg()
    speech_idx = list_slf(SPEECH_SLF)
    battle_idx = list_slf(BATTLE_SLF)
    print(f"SLF speech={len(speech_idx)} battle={len(battle_idx)} ffmpeg={ffmpeg.name}")

    summary = []
    for slug in order:
        row = by_slug.get(slug)
        if not row:
            print(f"SKIP {slug}: not in map csv")
            continue
        status = row.get("status", "")
        pid = (row.get("profile_id") or "").strip()
        unit = row["unit_id"]
        source = row.get("speech_source") or "data_slf"
        # Never overwrite mercs with complete manual JA3 voice acting (e.g. Spouke).
        if status == "done_manual" or slug == "spouke":
            print(f"SKIP {slug}: done_manual — keep existing opus")
            summary.append((slug, "skip-done-manual", 0, 0))
            continue
        if status == "done" and not args.include_done and slug == "colby":
            print(f"SKIP {slug}: already done")
            summary.append((slug, "skip-done", 0, 0))
            continue
        # ready/shipped/done — allow re-ship for remaps (e.g. Hitman→Slay, Nervous→041)
        shippable = status in ("ready", "ready_tentative", "done", "shipped")
        if not pid or not shippable or status in ("new_voice", "done_manual", "missing"):
            print(f"SKIP {slug}: no profile in pack ({status})")
            summary.append((slug, "skip-missing", 0, 0))
            continue
        if unit not in vr and unit.replace("JAZZ_", "Jazz_") not in vr:
            # try Jazz_ form
            alt = unit.replace("JAZZ_Merc_", "Jazz_").replace("JAZZ_", "Jazz_")
            if alt in vr:
                unit = alt
            else:
                print(f"SKIP {slug}: no VR block for {row['unit_id']}")
                summary.append((slug, "skip-no-vr", 0, 0))
                continue

        entries = vr[unit]
        slot_i: dict[str, int] = defaultdict(int)
        ok = fail = 0
        print(f"=== {slug} {unit} pid={pid} lines={len(entries)} source={source}")
        opus_cache: dict[str, Path] = {}

        for slot, tid in entries:
            stems = pick_stems(slot, slot_i[slot])
            slot_i[slot] += 1
            wav = None
            used = None
            for stem in stems:
                wav = resolve_wav(pid, stem, speech_idx, battle_idx, source)
                if wav:
                    used = stem
                    break
            if not wav:
                print(f"  FAIL {tid} {slot}: no wav")
                fail += 1
                continue
            dest = VOICES / f"{tid}.opus"
            print(f"  {tid} {slot} <- {pid}_{used}")
            if args.dry_run:
                ok += 1
                continue
            key = str(wav.resolve())
            if key not in opus_cache:
                tmp = CACHE / f"_opus_{wav.stem}.opus"
                if not wav_to_opus(ffmpeg, wav, tmp):
                    print(f"  ffmpeg fail {wav.name}")
                    fail += 1
                    continue
                opus_cache[key] = tmp
            shutil.copy2(opus_cache[key], dest)
            ok += 1

        summary.append((slug, "shipped" if not args.dry_run else "dry", ok, fail))
        print(f"  -> ok={ok} fail={fail}")

    print("\nSUMMARY")
    for s in summary:
        print(f"  {s[0]:12s} {s[1]:12s} ok={s[2]} fail={s[3]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
