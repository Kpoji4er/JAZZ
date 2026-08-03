#!/usr/bin/env python3
"""Process AME Big raws: copy → rembg → 2000² → bust crop 300².

Expects raw Big frames (opaque #504633) named JAZZ_AME_NN_Big_raw.png in:
  - cursor assets/, or
  - jazz-units/MercPortraits/_wip/_raw/

Writes finals to jazz-units/MercPortraits/JAZZ_AME_NN.png (+ _Big).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"
PORTRAITS = UNITS / "MercPortraits"
RAW_DIR = PORTRAITS / "_wip" / "_raw"
ASSETS = Path.home() / ".cursor" / "projects" / (
    "c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
) / "assets"
BUST = ROOT / ".agents" / "skills" / "create-jazz-merc-portraits" / "scripts" / "bust_crop_tight.py"
REMBG = Path(sys.executable).with_name("Scripts") / "rembg.exe"
if not REMBG.exists():
    REMBG = Path(shutil.which("rembg") or "")


def slot_id(n: int) -> str:
    return f"JAZZ_AME_{n:02d}"


def find_raw(n: int) -> Path | None:
    name = f"{slot_id(n)}_Big_raw.png"
    for base in (ASSETS, RAW_DIR, PORTRAITS / "_ame_face_refs" / "_raw"):
        p = base / name
        if p.exists():
            return p
    return None


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def rembg_cut(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not REMBG or not Path(REMBG).exists():
        raise RuntimeError("rembg.exe not found")
    cmd = [str(REMBG), "i", "-m", "birefnet-general", str(src), str(dst)]
    subprocess.run(cmd, check=True)


def resize_square(src: Path, dst: Path, size: int) -> None:
    im = Image.open(src).convert("RGBA")
    im = im.resize((size, size), Image.Resampling.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "PNG")


def bust_crop(big: Path, portrait: Path) -> None:
    cmd = [
        sys.executable,
        str(BUST),
        str(big),
        str(portrait),
        "--frac",
        "0.28",
        "--size",
        "300",
    ]
    subprocess.run(cmd, check=True)


def process_slot(n: int, force: bool = False) -> str:
    uid = slot_id(n)
    final_big = PORTRAITS / f"{uid}_Big.png"
    final_por = PORTRAITS / f"{uid}.png"
    raw = find_raw(n)
    if not raw:
        return f"{uid}: SKIP no raw"
    staged = RAW_DIR / f"{uid}_Big.png"
    if raw.resolve() != staged.resolve():
        shutil.copy2(raw, staged)

    cut = RAW_DIR / f"{uid}_Big_cut.png"
    if force or not cut.exists():
        rembg_cut(staged, cut)
    resize_square(cut, final_big, 2000)
    bust_crop(final_big, final_por)
    return f"{uid}: OK"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--to", dest="end", type=int, default=60)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    ensure_dirs()
    for n in range(args.start, args.end + 1):
        print(process_slot(n, force=args.force), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
