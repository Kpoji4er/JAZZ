# -*- coding: utf-8 -*-
"""Ship JA2/NightOps archive voices onto Jazz merc VoiceResponse T-ids.

Reads mapping: docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv
Extracts WAV from Data/SPEECH.SLF + BATTLESNDS.SLF (and NightOps/SPEECH overlays),
or ingests ja2mercs folder banks (WAV ADPCM / OGG → opus).

speech_source forms:
  data_slf | nightops_speech | nightops_npc | sj_folder | ub_cs_folder |
  ub_wildfire_folder | horg_stogie_folder | folder:<path> |
  ja2mercs:<cat>/<merc>[|battle=<pid>][|merge_speech]

ja2mercs path override: prefer Downloads/ja2mercs/ja2mercs; filter by profile_id
(+ optional battle pid for ЦС dual-bank mercs). Do not mix co-folder pids
unless `|merge_speech` (same-merc dual file prefixes, e.g. Grom 076+047).

Usage (jazz/):
  python docs/tools/_ship_ja2_merc_voices.py --dry-run
  python docs/tools/_ship_ja2_merc_voices.py --only ira,dimitri
  python docs/tools/_ship_ja2_merc_voices.py --queue
  python docs/tools/_ship_ja2_merc_voices.py --ja2mercs-remesh
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
JA2MERCS_ROOT = Path(r"C:\Users\SsAnd\Downloads\ja2mercs\ja2mercs")
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
AUDIO_EXTS = (".wav", ".ogg", ".mp3")

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
    if stem == "ENEM":
        out.extend(["ENEMY", "ENEMY2"])
    return out


# folder → {(pid_upper, stem_upper) → Path}
_JA2MERCS_INDEX: dict[str, dict[tuple[str, str], Path]] = {}


def parse_ja2mercs_source(source: str) -> tuple[Path, str, bool] | None:
    """Parse ja2mercs:<rel>[|battle=<pid>][|merge_speech] → (folder, battle, merge_speech)."""
    if not source.startswith("ja2mercs:"):
        return None
    raw = source.split(":", 1)[1].strip()
    merge_speech = False
    battle = ""
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    if not parts:
        return None
    rel = parts[0].replace("\\", "/")
    for flag in parts[1:]:
        if flag == "merge_speech":
            merge_speech = True
        elif flag.startswith("battle="):
            battle = flag.split("=", 1)[1].strip()
    folder = JA2MERCS_ROOT.joinpath(*rel.split("/"))
    return folder, battle, merge_speech


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
        return [UB_CS_FOLDER] if UB_CS_FOLDER.exists() else []
    if source == "ub_wildfire_folder":
        return [UB_WF_FOLDER] if UB_WF_FOLDER.exists() else []
    if source == "sj_folder":
        return [SJ_FOLDER] if SJ_FOLDER.exists() else []
    parsed = parse_ja2mercs_source(source)
    if parsed:
        folder, _battle, _merge = parsed
        return [folder] if folder.is_dir() else []
    return []


def _pid_variants(pid: str) -> list[str]:
    """Filename prefixes allowed for this profile (exact match only)."""
    pid = (pid or "").strip()
    if not pid:
        return []
    out = [pid]
    if pid.upper().startswith("U_"):
        num = pid.split("_", 1)[-1]
        out.extend([f"U_{num}", f"u_{num}"])
    elif pid.isdigit():
        z = pid.zfill(3)
        out.extend([z, pid.lstrip("0") or "0"])
    seen: set[str] = set()
    uniq: list[str] = []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def index_ja2mercs_folder(folder: Path) -> dict[tuple[str, str], Path]:
    key = str(folder.resolve())
    if key in _JA2MERCS_INDEX:
        return _JA2MERCS_INDEX[key]
    idx: dict[tuple[str, str], Path] = {}
    if not folder.is_dir():
        _JA2MERCS_INDEX[key] = idx
        return idx
    for f in folder.rglob("*"):
        if not f.is_file() or f.suffix.lower() not in AUDIO_EXTS:
            continue
        if f.stat().st_size < 100:
            continue
        parts = f.stem.split("_")
        if len(parts) < 2:
            continue
        if parts[0].upper() in ("R", "D") and len(parts) >= 3:
            pid = parts[1]
            stem = "_".join(parts[2:])
        elif parts[0].upper() == "U" and len(parts) >= 3:
            pid = f"U_{parts[1]}"
            stem = "_".join(parts[2:])
        else:
            pid = parts[0]
            stem = "_".join(parts[1:])
        k = (pid.upper(), stem.upper())
        # Prefer wav over ogg if both exist
        prev = idx.get(k)
        if prev is None or (
            f.suffix.lower() == ".wav" and prev.suffix.lower() != ".wav"
        ):
            idx[k] = f
    _JA2MERCS_INDEX[key] = idx
    return idx


# Numeric speech stub: prefer alt pid when primary is tiny and alt is clearly fuller.
_MERGE_SPEECH_STUB_BYTES = 8000


def _pick_longer_audio(
    primary: Path | None,
    alt: Path | None,
    *,
    prefer_primary_on_tie: bool = True,
) -> Path | None:
    """Same-merc dual-prefix: fullest bank; prefer primary when comparable."""
    if primary is None:
        return alt
    if alt is None:
        return primary
    sa = primary.stat().st_size
    sb = alt.stat().st_size
    if sa <= 0:
        return alt if sb > 0 else primary
    if sb <= 0:
        return primary
    if sa < _MERGE_SPEECH_STUB_BYTES and sb > sa * 1.5:
        return alt
    if sb > sa * 1.2:
        return alt
    if sb > sa and not prefer_primary_on_tie:
        return alt
    return primary


def resolve_ja2mercs_audio(
    folder: Path,
    pid: str,
    battle_pid: str,
    stem: str,
    *,
    merge_speech: bool = False,
) -> Path | None:
    """Find WAV/OGG/MP3 for stem under ja2mercs merc folder; pid-filter only.

    Named battle stems prefer battle_pid when set (ЦС dual-bank / Grom 047 battle).
    With merge_speech, numeric stems pick the longer of speech pid vs battle_pid
    (prefer speech pid when sizes are close) — for same-merc dual prefixes only.
    """
    if not folder.is_dir():
        return None
    idx = index_ja2mercs_folder(folder)
    aliases = _stem_aliases(stem)
    named_battle = stem.upper() in {
        "ATTN",
        "COOL",
        "HUMM",
        "OK1",
        "OK2",
        "GOTIT",
        "HIT1",
        "HIT2",
        "CURSE",
        "DIE",
        "DYING",
        "ENEMY",
        "ENEM",
        "ENEMY2",
        "LMATTN",
        "LMOK1",
        "LMOK2",
        "LOCKED",
        "NOTH",
        "LAUGH",
    }

    def _norm_pids(raw: str) -> list[str]:
        out: list[str] = []
        seen: set[str] = set()
        for p in _pid_variants(raw):
            pu = p.upper()
            if pu not in seen:
                seen.add(pu)
                out.append(pu)
            if pu.startswith(("R_", "D_")):
                bare = pu.split("_", 1)[1]
                if bare not in seen:
                    seen.add(bare)
                    out.append(bare)
        return out

    if merge_speech and battle_pid and not named_battle:
        # Dual same-merc numeric lines: gather both banks, pick fullest.
        for alias in aliases:
            au = alias.upper()
            primary = None
            alt = None
            for p in _norm_pids(pid):
                hit = idx.get((p, au))
                if hit:
                    primary = hit
                    break
            for p in _norm_pids(battle_pid):
                hit = idx.get((p, au))
                if hit:
                    alt = hit
                    break
            picked = _pick_longer_audio(primary, alt)
            if picked:
                return picked
        return None

    pid_order: list[str] = []
    if named_battle and battle_pid:
        pid_order.extend(_pid_variants(battle_pid))
    pid_order.extend(_pid_variants(pid))
    if battle_pid:
        pid_order.extend(_pid_variants(battle_pid))
    seen: set[str] = set()
    pids: list[str] = []
    for p in pid_order:
        pu = p.upper()
        if pu not in seen:
            seen.add(pu)
            pids.append(pu)
        if pu.startswith(("R_", "D_")):
            bare = pu.split("_", 1)[1]
            if bare not in seen:
                seen.add(bare)
                pids.append(bare)

    for alias in aliases:
        au = alias.upper()
        for p in pids:
            hit = idx.get((p, au))
            if hit:
                return hit
    return None


def resolve_wav(
    pid: str,
    stem: str,
    speech_idx: dict,
    battle_idx: dict,
    source: str,
) -> Path | None:
    """Return path to cached audio for profile+stem (wav/ogg/mp3)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    aliases = _stem_aliases(stem)

    # ja2mercs: preferred path override with strict pid filter
    parsed = parse_ja2mercs_source(source)
    if parsed:
        folder, battle, merge_speech = parsed
        hit = resolve_ja2mercs_audio(
            folder, pid, battle, stem, merge_speech=merge_speech
        )
        if hit:
            # Cache by chosen file stem so dual-prefix swaps refresh correctly.
            dest = CACHE / f"ja2mercs_{hit.stem}{hit.suffix.lower()}"
            if not dest.exists() or dest.stat().st_size != hit.stat().st_size:
                shutil.copy2(hit, dest)
            return dest
        return None

    # External folder pack (Horg 166 «Бычок», etc.)
    for root in _folder_roots(source):
        for alias in aliases:
            for name in (
                f"{pid}_{alias}.WAV",
                f"{pid}_{alias}.wav",
                f"{pid}_{alias}.ogg",
                f"R_{pid}_{alias}.WAV",
                f"r_{pid}_{alias}.wav",
                f"U_{pid.split('_')[-1]}_{alias}.WAV"
                if pid.upper().startswith("U_")
                else "",
            ):
                if not name:
                    continue
                for p in root.rglob(name):
                    if p.is_file() and p.stat().st_size > 100:
                        dest = CACHE / f"{pid}_{alias}{p.suffix.lower()}"
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
        # normalize cache key to pid_stem.wav
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
    """Convert wav/ogg/mp3 → opus (Colby loudnorm pipeline)."""
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
    ap.add_argument(
        "--ja2mercs-remesh",
        action="store_true",
        help="Process all CSV rows with speech_source=ja2mercs:* (incl done/shipped)",
    )
    ap.add_argument("--ja2mercs-root", type=Path, default=None)
    ap.add_argument("--force-missing-skip", action="store_true", default=True)
    args = ap.parse_args()

    global JA2MERCS_ROOT
    if args.ja2mercs_root:
        JA2MERCS_ROOT = args.ja2mercs_root

    rows = load_map()
    by_slug = {r["slug"]: r for r in rows}
    if args.ja2mercs_remesh and not args.only:
        order = [
            r["slug"]
            for r in rows
            if (r.get("speech_source") or "").startswith("ja2mercs:")
        ]
    elif args.only:
        order = [s.strip() for s in args.only.split(",") if s.strip()]
    elif args.queue:
        order = list(QUEUE)
    else:
        order = list(QUEUE)

    items_text = ITEMS.read_text(encoding="utf-8")
    vr = parse_vr_blocks(items_text)
    print(f"VR units parsed: {len(vr)}")

    ffmpeg = find_ffmpeg()
    needs_slf = any(
        not (by_slug.get(s, {}).get("speech_source") or "").startswith("ja2mercs:")
        for s in order
        if s in by_slug
    )
    speech_idx: dict = {}
    battle_idx: dict = {}
    if needs_slf and SPEECH_SLF.exists() and BATTLE_SLF.exists():
        speech_idx = list_slf(SPEECH_SLF)
        battle_idx = list_slf(BATTLE_SLF)
        print(f"SLF speech={len(speech_idx)} battle={len(battle_idx)} ffmpeg={ffmpeg.name}")
    else:
        print(f"SLF skipped (ja2mercs-only batch) ffmpeg={ffmpeg.name} root={JA2MERCS_ROOT}")

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
        if (
            status == "done"
            and not args.include_done
            and not args.ja2mercs_remesh
            and not source.startswith("ja2mercs:")
            and slug == "colby"
        ):
            print(f"SKIP {slug}: already done")
            summary.append((slug, "skip-done", 0, 0))
            continue
        # ready/shipped/done + need_pack with assigned pid (ja2mercs fill)
        shippable = status in (
            "ready",
            "ready_tentative",
            "done",
            "shipped",
            "need_pack",
        )
        if not pid or not shippable or status in ("new_voice", "done_manual", "missing"):
            print(f"SKIP {slug}: no profile in pack ({status})")
            summary.append((slug, "skip-missing", 0, 0))
            continue
        if args.ja2mercs_remesh and not source.startswith("ja2mercs:"):
            print(f"SKIP {slug}: not ja2mercs source")
            summary.append((slug, "skip-not-ja2mercs", 0, 0))
            continue
        if unit not in vr and unit.replace("JAZZ_", "Jazz_") not in vr:
            alt = unit.replace("JAZZ_Merc_", "Jazz_").replace("JAZZ_", "Jazz_")
            if alt in vr:
                unit = alt
            else:
                print(f"SKIP {slug}: no VR block for {row['unit_id']}")
                summary.append((slug, "skip-no-vr", 0, 0))
                continue

        entries = vr[unit]
        if not entries:
            print(f"SKIP {slug}: empty VR (inject/expand first)")
            summary.append((slug, "skip-empty-vr", 0, 0))
            continue
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
            # Show actual source file stem (e.g. 047_ATTN vs 076_000) for dual-prefix.
            src_label = wav.stem
            if src_label.startswith("ja2mercs_"):
                src_label = src_label[len("ja2mercs_") :]
            print(f"  {tid} {slot} <- {src_label} (want {used})")
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
