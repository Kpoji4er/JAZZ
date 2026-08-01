# -*- coding: utf-8 -*-
"""Rebuild Jazz_Colby voices from JA2 Trevor archive only (no neural TTS/RVC).

Missing VR/AIM slots get a duplicate of a related archive line (same file → same opus).

Input:
  - JA2 WAVs: Downloads/trevor_extract/trevor/*.WAV  (or --ja2)
  - Mapping: Downloads/trevor_extract/ship_colby.py VR_LINES + AIM_WAV below

Output:
  - jazz-units/voices/<T-id>.opus

Usage (from jazz/):
  python docs/tools/_ship_colby_voices_ja2_only.py
  python docs/tools/_ship_colby_voices_ja2_only.py --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

FFMPEG_CANDIDATES = [
    Path(r"C:\Users\SsAnd\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"),
    Path(r"D:\py-voice\RVC-WebUI\ffmpeg.exe"),
]
DEFAULT_JA2 = Path(r"C:\Users\SsAnd\Downloads\trevor_extract\trevor")
DEFAULT_SHIP = Path(r"C:\Users\SsAnd\Downloads\trevor_extract\ship_colby.py")
DEFAULT_VOICES = Path(
    r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\voices"
)

# AIM chat T-ids → archive WAV (JA2 hire-sheet numbers)
AIM_WAV: dict[int, str] = {
    890000000001709: "005_086.WAV",  # refuse Fidel
    890000000001710: "005_081.WAV",  # refuse death toll
    890000000001711: "005_097.WAV",  # refuse money
    890000000001712: "005_116.WAV",  # haggle / raise price (closest)
    890000000001713: "005_094.WAV",  # Thor mitigation
    890000000001714: "005_053.WAV",  # recommend Thor (praise buddy)
    890000000001715: "005_084.WAV",  # offline answering machine
    890000000001716: "005_108.WAV",  # greeting
    890000000001717: "005_096.WAV",  # conversation restart
    890000000001718: "005_109.WAV",  # idle chat
    890000000001719: "005_091.WAV",  # parting / contract accept
    890000000001720: "005_089.WAV",  # rehire intro
    890000000001721: "005_090.WAV",  # rehire outro
}

# Explicit donors for VR slots with wav=None in ship_colby (slot → preferred WAV).
# Round-robin within a slot uses SLOT_DONOR_POOL when listed; else FALLBACK_BY_SLOT.
SLOT_DONOR_POOL: dict[str, list[str]] = {
    "SelectionStealth": ["005_LMATTN.WAV", "005_LMOK1.WAV", "005_LMOK2.WAV"],
    "Order": ["005_OK1.WAV", "005_OK2.WAV", "005_GOTIT.WAV"],
    "CombatMovement": ["005_OK1.WAV", "005_OK2.WAV", "005_GOTIT.WAV"],
    "CombatMovementStealth": ["005_LMOK1.WAV", "005_LMOK2.WAV", "005_LMATTN.WAV"],
    "GroupOrder": ["005_GOTIT.WAV", "005_OK1.WAV", "005_073.WAV"],  # 073 = agree
    "AimAttack": ["005_ENEMY.WAV", "005_000.WAV", "005_027.WAV"],
    "AimAttackStealth": ["005_LMOK1.WAV", "005_LMATTN.WAV", "005_006.WAV"],
    "OpponentKilled": ["005_027.WAV", "005_028.WAV", "005_032.WAV"],
    "AmmoLow": ["005_013.WAV"],
    "CombatStartPlayer": ["005_072.WAV"],
    "CombatStartDetected": ["005_001.WAV", "005_ENEMY.WAV"],
    "DeathGeneral": ["005_DIE.WAV", "005_CURSE.WAV"],
    "Idle": ["005_COOL.WAV", "005_HUMM.WAV", "005_NOTH.WAV"],
    "BecomeHidden": ["005_LMATTN.WAV", "005_LMOK1.WAV", "005_006.WAV"],
    "HealReceived": ["005_058.WAV", "005_COOL.WAV"],
    "Overwatch": ["005_060.WAV"],
    "ThreatSelection": ["005_008.WAV", "005_007.WAV"],
    "OverwatchSelection": ["005_060.WAV", "005_072.WAV"],
    "GasAreaSelection": ["005_CURSE.WAV", "005_HIT1.WAV"],
    "TakeCover": ["005_042.WAV", "005_020.WAV"],
    "ThrowGrenade": ["005_027.WAV", "005_ENEMY.WAV"],
    "Autofire": ["005_027.WAV", "005_OK1.WAV"],
    "CombatTaskGiven": ["005_035.WAV", "005_HUMM.WAV"],
    "CombatTaskCompleted": ["005_048.WAV", "005_035.WAV"],
    "CombatTaskFailed": ["005_047.WAV", "005_057.WAV"],
    "Climbing": ["005_026.WAV", "005_HIT1.WAV"],
    "Jumping": ["005_026.WAV", "005_HIT2.WAV"],
}

FALLBACK_GLOBAL = [
    "005_OK1.WAV",
    "005_OK2.WAV",
    "005_GOTIT.WAV",
    "005_COOL.WAV",
    "005_ATTN.WAV",
]


def find_ffmpeg() -> Path:
    for p in FFMPEG_CANDIDATES:
        if p.exists():
            return p
    which = shutil.which("ffmpeg")
    if which:
        return Path(which)
    raise SystemExit("ffmpeg not found")


def load_ship(path: Path):
    spec = importlib.util.spec_from_file_location("ship_colby", str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


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
    if r.returncode != 0:
        print("ffmpeg fail", wav.name, (r.stderr or "")[-300:])
        return False
    return True


def resolve_jobs(mod, ja2: Path) -> list[tuple[int, str, str, str]]:
    """Return (tid, wav_name, source_kind, slot_or_aim)."""
    jobs: list[tuple[int, str, str, str]] = []

    for tid, wav in AIM_WAV.items():
        jobs.append((tid, wav, "aim-archive", "AIM"))

    none_idx: dict[str, int] = defaultdict(int)
    for slot, tid, _ru, _en, wav in mod.VR_LINES:
        if wav:
            jobs.append((tid, wav, "vr-archive", slot))
            continue
        pool = SLOT_DONOR_POOL.get(slot) or FALLBACK_GLOBAL
        # Prefer first pool entry that exists on disk; rotate for variety
        start = none_idx[slot]
        none_idx[slot] += 1
        chosen = None
        for i in range(len(pool)):
            cand = pool[(start + i) % len(pool)]
            if (ja2 / cand).exists():
                chosen = cand
                break
        if not chosen:
            for cand in FALLBACK_GLOBAL:
                if (ja2 / cand).exists():
                    chosen = cand
                    break
        if not chosen:
            raise SystemExit(f"no donor WAV for slot={slot} tid={tid}")
        jobs.append((tid, chosen, "vr-duplicate", slot))

    return jobs


def file_sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ja2", type=Path, default=DEFAULT_JA2)
    ap.add_argument("--ship", type=Path, default=DEFAULT_SHIP)
    ap.add_argument("--voices", type=Path, default=DEFAULT_VOICES)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.ja2.is_dir():
        raise SystemExit(f"JA2 dir missing: {args.ja2}")
    if not args.ship.is_file():
        raise SystemExit(f"ship_colby missing: {args.ship}")

    ffmpeg = find_ffmpeg()
    mod = load_ship(args.ship)
    jobs = resolve_jobs(mod, args.ja2)

    archive = sum(1 for j in jobs if j[2].endswith("archive"))
    dupes = sum(1 for j in jobs if j[2].endswith("duplicate"))
    print(f"jobs={len(jobs)} archive={archive} duplicate={dupes} ffmpeg={ffmpeg.name}")

    # Cache: wav_name → opus bytes path (temp) so duplicates share one encode
    cache_dir = args.voices / "_tmp_colby_ja2_cache"
    if not args.dry_run:
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        cache_dir.mkdir(parents=True)

    ok = 0
    fail = 0
    wav_cache: dict[str, Path] = {}

    for tid, wav_name, kind, slot in jobs:
        src = args.ja2 / wav_name
        if not src.exists():
            print(f"MISSING WAV {wav_name} for {tid} ({slot}/{kind})")
            fail += 1
            continue
        dest = args.voices / f"{tid}.opus"
        print(f"{tid} <- {wav_name} [{kind}/{slot}]")
        if args.dry_run:
            ok += 1
            continue
        if wav_name not in wav_cache:
            cached = cache_dir / f"{src.stem}.opus"
            if not wav_to_opus(ffmpeg, src, cached):
                fail += 1
                continue
            wav_cache[wav_name] = cached
        shutil.copy2(wav_cache[wav_name], dest)
        ok += 1

    if not args.dry_run and cache_dir.exists():
        shutil.rmtree(cache_dir)

    # Report content uniqueness
    if not args.dry_run:
        hashes: dict[str, list[int]] = defaultdict(list)
        for tid, wav_name, kind, slot in jobs:
            p = args.voices / f"{tid}.opus"
            if p.exists():
                hashes[file_sha1(p)].append(tid)
        unique = len(hashes)
        print(f"DONE ok={ok} fail={fail} unique_opus_hashes={unique}")
        multi = {h: tids for h, tids in hashes.items() if len(tids) > 1}
        print(f"shared_audio_groups={len(multi)} (expected for duplicates)")
    else:
        print(f"DRY-RUN ok={ok} fail={fail}")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
