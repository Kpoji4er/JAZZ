# -*- coding: utf-8 -*-
"""Extract speech-related trees from Jagged Alliance 2 1.13 Wildfire RUS FreeArc (.arc).

7-Zip cannot open FreeArc. Use PeaZip's bundled Arc.exe (or system FreeArc).

Default source: Downloads\\Jagged_Alliance_2_1_13_Wildfire_RUS.arc
Cache: docs/design/mercs-ja12/_voice-source/_wildfire_cache/

Important: this pack is 1.13 RUS + Wildfire *maps* (Data-WildFire6.07).
Data/SPEECH + MercEdt = vanilla RU AIM (Trevor 005, Malice 032, …).
UB Gaston SPEECH lives under Data-UB/ (profile 058). Commercial WF AIM
mercs (Allik/Monk/Henning/…) are NOT in this archive.

Usage (jazz/):
  python docs/tools/_extract_wildfire_rus_arc.py
  python docs/tools/_extract_wildfire_rus_arc.py --arc PATH --list-only
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
DEFAULT_ARC = Path(r"C:\Users\SsAnd\Downloads\Jagged_Alliance_2_1_13_Wildfire_RUS.arc")
CACHE = JAZZ / "docs/design/mercs-ja12/_voice-source/_wildfire_cache"
PEAZIP_ARC = (
    JAZZ
    / "docs/design/mercs-ja12/_voice-source/_tools/peazip"
    / "peazip_portable-10.4.0.WINDOWS/res/bin/arc/Arc.exe"
)

# Selective extract — full arc ~1.1 GiB; speech subset is enough for voice ship.
PATTERNS = [
    r"Jagged Alliance 2 RUS\Data\SPEECH.SLF",
    r"Jagged Alliance 2 RUS\Data\BATTLESNDS.SLF",
    r"Jagged Alliance 2 RUS\Data\MERCEDT.SLF",
    r"Jagged Alliance 2 RUS\Data\MercEdt\*",
    r"Jagged Alliance 2 RUS\Data\Speech\*",
    r"Jagged Alliance 2 RUS\Data-1.13\Speech\*",
    r"Jagged Alliance 2 RUS\Data-UB\Speech\*",
    r"Jagged Alliance 2 RUS\Data-UB\MercEdt\*",
    r"Jagged Alliance 2 RUS\Data-UB\BattleSNDS\*",
]


def find_arc_exe() -> Path:
    if PEAZIP_ARC.exists():
        return PEAZIP_ARC
    which = Path(subprocess.check_output(["where", "Arc.exe"], text=True).splitlines()[0])
    if which.exists():
        return which
    raise SystemExit(
        "Arc.exe not found. Unpack PeaZip portable under "
        "_voice-source/_tools/peazip/ or install FreeArc and put Arc.exe on PATH."
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arc", type=Path, default=DEFAULT_ARC)
    ap.add_argument("--out", type=Path, default=CACHE)
    ap.add_argument("--list-only", action="store_true")
    args = ap.parse_args()
    if not args.arc.exists():
        raise SystemExit(f"missing archive: {args.arc}")
    arc_exe = find_arc_exe()
    print(f"Arc.exe={arc_exe}")
    print(f"archive={args.arc} ({args.arc.stat().st_size} bytes)")
    if args.list_only:
        subprocess.run([str(arc_exe), "l", str(args.arc)], check=False)
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    cmd = [str(arc_exe), "x", "-o+", f"-dp{args.out}", str(args.arc), *PATTERNS]
    print("extracting:", " ".join(PATTERNS[:3]), "…")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        return r.returncode
    ub = args.out / "Jagged Alliance 2 RUS" / "Data-UB" / "Speech"
    print(f"OK cache={args.out}")
    if ub.exists():
        n058 = len(list(ub.glob("058_*.WAV"))) + len(list(ub.glob("058_*.wav")))
        print(f"Data-UB/Speech 058_*.WAV count={n058}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
