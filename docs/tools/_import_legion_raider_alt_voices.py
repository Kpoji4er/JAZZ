"""Import alternate Legion Raider voice takes (*-1.opus) into jazz-units/voices.

Source (default): Downloads/1.rar or extracted folder Downloads/1 — same
localization T-ids as vanilla LegionRaider lines, alternate recordings with
`-1` postfix (engine voice variant / AME Male_Low donor).

Usage (from jazz/):
  python docs/tools/_import_legion_raider_alt_voices.py
  python docs/tools/_import_legion_raider_alt_voices.py --dir "C:/Users/.../Downloads/1"
  python docs/tools/_import_legion_raider_alt_voices.py --rar "C:/path/1.rar" --dry-run
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

JU = Path(__file__).resolve().parents[2].parent / "jazz-units"
VOICES = JU / "voices"
DEFAULT_RAR = Path.home() / "Downloads" / "1.rar"
DEFAULT_DIR = Path.home() / "Downloads" / "1"
OPUS_RE = re.compile(r"(?i)^(\d+)-1\.opus$")


def list_rar(rar: Path) -> list[str]:
    out = subprocess.check_output(["tar", "-tf", str(rar)], text=True, errors="replace")
    return [ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()]


def collect_from_dir(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*-1.opus") if OPUS_RE.match(p.name))


def copy_one(src: Path, dry: bool) -> str:
    dest = VOICES / src.name
    if dry:
        return "would"
    if dest.exists() and dest.stat().st_size == src.stat().st_size:
        return "skip"
    shutil.copy2(src, dest)
    return "copy"


def finish(sources: list[Path], dry: bool) -> int:
    copied = skipped = 0
    for src in sources:
        st = copy_one(src, dry)
        if st == "skip":
            skipped += 1
        else:
            copied += 1
            if dry:
                print(f"  would copy {src.name}")
    print(f"copied={copied} skipped_same={skipped} dry_run={dry}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rar", type=Path, default=None)
    ap.add_argument("--dir", type=Path, default=None, help="Extracted folder with *-1.opus")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not VOICES.is_dir():
        print(f"FAIL: voices dir missing: {VOICES}", file=sys.stderr)
        return 1

    if args.dir is not None:
        if not args.dir.is_dir():
            print(f"FAIL: dir not found: {args.dir}", file=sys.stderr)
            return 1
        sources = collect_from_dir(args.dir)
        print(f"dir={args.dir} alt_opus={len(sources)}")
        if not sources:
            print("FAIL: no *-1.opus found", file=sys.stderr)
            return 1
        return finish(sources, args.dry_run)

    rar = args.rar or DEFAULT_RAR
    if rar.is_file():
        entries = [e for e in list_rar(rar) if OPUS_RE.search(Path(e).name)]
        print(f"rar={rar} alt_opus={len(entries)}")
        if not entries:
            print("FAIL: no *-1.opus in archive", file=sys.stderr)
            return 1
        with tempfile.TemporaryDirectory(prefix="jazz-legion-raider-alt-") as tmp:
            tmp_path = Path(tmp)
            subprocess.check_call(["tar", "-xf", str(rar), "-C", str(tmp_path)])
            sources: list[Path] = []
            for entry in entries:
                src = tmp_path / entry
                if not src.is_file():
                    matches = list(tmp_path.rglob(Path(entry).name))
                    if not matches:
                        print(f"  missing extract: {entry}")
                        continue
                    src = matches[0]
                sources.append(src)
            return finish(sources, args.dry_run)

    if DEFAULT_DIR.is_dir():
        sources = collect_from_dir(DEFAULT_DIR)
        print(f"dir={DEFAULT_DIR} alt_opus={len(sources)}")
        if not sources:
            print("FAIL: no *-1.opus found", file=sys.stderr)
            return 1
        return finish(sources, args.dry_run)

    print(f"FAIL: no --dir/--rar and missing {rar} / {DEFAULT_DIR}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
