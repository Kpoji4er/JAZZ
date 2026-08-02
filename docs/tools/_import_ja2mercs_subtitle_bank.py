# -*- coding: utf-8 -*-
"""Import ja2mercs per-merc *.txt transcripts → stem CSV banks.

Line index i (including blank lines) ↔ SPEECH stem i (000–…).
Encoding: try utf-8-sig, utf-8, cp1251, utf-16.

Usage (jazz/):
  python docs/tools/_import_ja2mercs_subtitle_bank.py
  python docs/tools/_import_ja2mercs_subtitle_bank.py --root "C:/Users/.../ja2mercs (1)/ja2mercs"
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
OUT = JAZZ / "docs/design/mercs-ja12/_voice-source/subtitles"
FOLDERS = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2mercs_folders.csv"
DEFAULT_ROOTS = [
    Path(r"C:\Users\SsAnd\Downloads\ja2mercs (1)\ja2mercs"),
    Path(r"C:\Users\SsAnd\Downloads\ja2mercs\ja2mercs"),
]


def read_txt(path: Path) -> list[str]:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1251", "utf-16", "utf-16-le"):
        try:
            return raw.decode(enc).splitlines()
        except UnicodeDecodeError:
            continue
    return raw.decode("cp1251", errors="replace").splitlines()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=None)
    args = ap.parse_args()
    root = args.root or next((p for p in DEFAULT_ROOTS if p.is_dir()), DEFAULT_ROOTS[0])
    OUT.mkdir(parents=True, exist_ok=True)

    # slug → folder from map
    slug_folder: dict[str, str] = {}
    if FOLDERS.exists():
        with FOLDERS.open(encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if row.get("folder"):
                    slug_folder[row["slug"]] = row["folder"].replace("\\", "/")

    # Also index every *.txt under root by parent folder name
    txts = sorted(root.rglob("*.txt"))
    written = 0
    for txt in txts:
        if txt.name.lower() == "desktop.ini":
            continue
        rel_parent = txt.parent.relative_to(root).as_posix()
        # match slug by folder suffix
        slug = None
        for s, folder in slug_folder.items():
            if folder == rel_parent or folder.endswith("/" + txt.parent.name):
                slug = s
                break
        if not slug:
            # derive from filename 164_kulba.txt / 170_Monk.txt
            stem = txt.stem.lower()
            for s in slug_folder:
                if s in stem or stem.endswith(s):
                    slug = s
                    break
        if not slug:
            # WF / special names
            name = txt.parent.name.lower()
            aliases = {
                "brains": "allik",
                "scream": "vilde",
                "rudolf": "steiger",
                "gromov": "grom",
                "benni": "benny",
                "escimo": "eskimo",
                "stogie": "horg",
                "monk": "monk",
                "henning": "henning",
                "lucky": "lucky",
                "laura": "laura",
                "grace": "grace",
                "kulba": "kulba",
                "gaston": "gaston",
                "biggens": "biggens",
                "simon": "simon",
            }
            for key, s in aliases.items():
                if key in name or key in stem:
                    slug = s
                    break
        if not slug:
            print(f"SKIP unmapped {rel_parent}/{txt.name}")
            continue

        lines = read_txt(txt)
        # audio sizes by numeric stem under same folder
        audio: dict[str, int] = {}
        for f in txt.parent.rglob("*"):
            if f.suffix.lower() not in (".wav", ".ogg", ".mp3"):
                continue
            parts = f.stem.split("_")
            if len(parts) < 2:
                continue
            num = parts[-1]
            if not num.isdigit():
                continue
            key = num.zfill(3)
            audio[key] = max(audio.get(key, 0), f.stat().st_size)

        out_path = OUT / f"{slug}.csv"
        with out_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(
                f, fieldnames=["stem", "ru_text", "wav_bytes", "has_audio", "source_txt"]
            )
            w.writeheader()
            for i, line in enumerate(lines):
                stem = f"{i:03d}"
                text = line.strip()
                wb = audio.get(stem, 0)
                w.writerow(
                    {
                        "stem": stem,
                        "ru_text": text,
                        "wav_bytes": wb,
                        "has_audio": "1" if wb > 100 else "0",
                        "source_txt": txt.name,
                    }
                )
        nonempty = sum(1 for ln in lines if ln.strip())
        print(f"{slug}: {out_path.name} lines={len(lines)} nonempty={nonempty}")
        written += 1

    readme = OUT / "README.md"
    readme.write_text(
        "# Subtitle banks (from ja2mercs *.txt)\n\n"
        "Generated by `docs/tools/_import_ja2mercs_subtitle_bank.py`.\n"
        "Column `stem` = SPEECH line id (`000`…); blank `ru_text` = no line in source.\n"
        "Apply via `_apply_ja12_subtitles.py` (slot→stem via SLOT_WAV / AIM_CHAT_WAV).\n",
        encoding="utf-8",
    )
    print(f"Wrote {written} banks → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
