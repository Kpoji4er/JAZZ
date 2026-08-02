"""Import alternate Legion Raider voice takes (*-1.opus) into jazz-units/voices.

Source archive (default): Downloads/1.rar — same localization T-ids as vanilla
LegionRaider lines, alternate recordings with `-1` postfix (engine voice variant).

Usage (from jazz/):
  python docs/tools/_import_legion_raider_alt_voices.py
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

JAZZ = Path(__file__).resolve().parents[2]
JU = JAZZ.parent / "jazz-units"
VOICES = JU / "voices"
DEFAULT_RAR = Path.home() / "Downloads" / "1.rar"
OPUS_RE = re.compile(r"(?i)(\d+)-1\.opus$")


def list_rar(rar: Path) -> list[str]:
    out = subprocess.check_output(["tar", "-tf", str(rar)], text=True, errors="replace")
    return [ln.strip().replace("\\", "/") for ln in out.splitlines() if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rar", type=Path, default=DEFAULT_RAR)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.rar.is_file():
        print(f"FAIL: rar not found: {args.rar}", file=sys.stderr)
        return 1
    if not VOICES.is_dir():
        print(f"FAIL: voices dir missing: {VOICES}", file=sys.stderr)
        return 1

    entries = [e for e in list_rar(args.rar) if OPUS_RE.search(Path(e).name)]
    print(f"rar={args.rar}")
    print(f"alt_opus={len(entries)}")
    if not entries:
        print("FAIL: no *-1.opus in archive", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="jazz-legion-raider-alt-") as tmp:
        tmp_path = Path(tmp)
        subprocess.check_call(["tar", "-xf", str(args.rar), "-C", str(tmp_path)])
        copied = 0
        skipped = 0
        missing = 0
        for entry in entries:
            src = tmp_path / entry
            if not src.is_file():
                # tar may flatten or use different nesting
                matches = list(tmp_path.rglob(Path(entry).name))
                if not matches:
                    missing += 1
                    print(f"  missing extract: {entry}")
                    continue
                src = matches[0]
            name = src.name  # keep <tid>-1.opus
            dest = VOICES / name
            if args.dry_run:
                print(f"  would copy {name} -> {dest}")
                copied += 1
                continue
            if dest.exists() and dest.stat().st_size == src.stat().st_size:
                skipped += 1
                continue
            shutil.copy2(src, dest)
            copied += 1
        print(f"copied={copied} skipped_same={skipped} missing={missing} dry_run={args.dry_run}")
    return 0 if missing == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
