# -*- coding: utf-8 -*-
"""Read-only inventory of Downloads/ja2mercs/ja2mercs vs jazz_to_ja2_profile.csv.

Does NOT extract, convert, or ship voices. Prints folder layout, audio counts,
profile-id guesses from filenames, and optional crosswalk to Jazz slugs.

Usage (jazz/):
  python docs/tools/_inventory_ja2mercs.py
  python docs/tools/_inventory_ja2mercs.py --root \"C:/path/to/ja2mercs\"
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
MAP_CSV = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
DEFAULT_ROOT = Path(r"C:\Users\SsAnd\Downloads\ja2mercs\ja2mercs")

AUDIO_EXT = {".wav", ".ogg", ".mp3"}
PID_RE = re.compile(
    r"^(?:[RrDd]_)?(?:U_)?(?P<pid>\d{2,3})_(?P<rest>.+)$", re.IGNORECASE
)
U_RE = re.compile(r"^U_(?P<pid>\d+)_(?P<rest>.+)$", re.IGNORECASE)


def guess_pids(merc_dir: Path) -> tuple[set[str], int, set[str], bool, bool, str]:
    pids: set[str] = set()
    n_audio = 0
    formats: set[str] = set()
    has_xlsx = False
    has_edt = False
    layout = "flat"
    for dirpath, _dirs, files in os_walk(merc_dir):
        rel = Path(dirpath).relative_to(merc_dir).as_posix().lower()
        if any(part in ("speech", "battlesnds", "npcspeech") for part in rel.split("/")):
            layout = "nested"
        for name in files:
            ext = Path(name).suffix.lower()
            if ext == ".xlsx":
                has_xlsx = True
            if ext == ".edt":
                has_edt = True
            if ext not in AUDIO_EXT:
                continue
            n_audio += 1
            formats.add(ext)
            stem = Path(name).stem
            m = U_RE.match(stem)
            if m:
                pids.add(f"U_{m.group('pid')}")
                continue
            m = PID_RE.match(stem)
            if m:
                pids.add(m.group("pid").zfill(3))
    return pids, n_audio, formats, has_xlsx, has_edt, layout


def os_walk(root: Path):
    import os

    return os.walk(root)


def load_jazz_map() -> list[dict[str, str]]:
    if not MAP_CSV.exists():
        return []
    with MAP_CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    # Normalize keys (defensive) and empty fields.
    out = []
    for row in rows:
        clean = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
        out.append(clean)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = ap.parse_args()
    root: Path = args.root
    if not root.is_dir():
        print(f"ROOT missing: {root}")
        return 1

    rows = []
    for cat in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not cat.is_dir():
            continue
        for merc in sorted(cat.iterdir(), key=lambda p: p.name.lower()):
            if not merc.is_dir():
                continue
            pids, n, fmts, xlsx, edt, layout = guess_pids(merc)
            rows.append(
                {
                    "cat": cat.name,
                    "merc": merc.name,
                    "pids": ",".join(sorted(pids)),
                    "n_audio": n,
                    "fmt": ",".join(sorted(fmts)),
                    "xlsx": int(xlsx),
                    "edt": int(edt),
                    "layout": layout,
                }
            )

    print(f"ROOT {root}")
    print(f"mercs={len(rows)}")
    print("cat/merc\tpids\tn\tfmt\txlsx\tedt\tlayout")
    for r in rows:
        print(
            f"{r['cat']}/{r['merc']}\t{r['pids']}\t{r['n_audio']}\t"
            f"{r['fmt']}\t{r['xlsx']}\t{r['edt']}\t{r['layout']}"
        )

    jazz = load_jazz_map()
    if not jazz:
        return 0

    print("\n--- Jazz crosswalk (profile_id match in filenames) ---")
    pid_to_pack = {}
    for r in rows:
        for pid in (r["pids"].split(",") if r["pids"] else []):
            pid_to_pack.setdefault(pid, []).append(f"{r['cat']}/{r['merc']} (n={r['n_audio']})")

    for row in jazz:
        slug = row.get("slug", "")
        pid = (row.get("profile_id") or "").strip()
        status = row.get("status", "")
        if not pid:
            print(f"{slug}\t(no pid)\t{status}\t-")
            continue
        keys = [pid]
        if pid.isdigit():
            keys.append(pid.zfill(3))
        hits = []
        for k in keys:
            hits.extend(pid_to_pack.get(k, []))
        # also U_ form without zero-pad mismatch
        if pid.startswith("U_"):
            hits.extend(pid_to_pack.get(pid, []))
        hits = sorted(set(hits))
        mark = "HIT" if hits else "MISS"
        shown = " | ".join(hits) if hits else "-"
        print(f"{slug}\t{pid}\t{status}\t{mark}\t{shown}")

    print("\n--- missing / need_pack: folder-name heuristic ---")
    name_hints = {
        "monk": ["monk"],
        "allik": ["brains"],
        "henning": ["henning"],
        "grace": ["grace"],
        "lucky": ["lucky"],
        "laura": ["laura"],
        "vilde": ["scream"],
        "steiger": ["rudolf"],
        "biggens": ["biggens"],
        "mike": ["mike"],
        "horg": ["bychok"],
        "spouke": [],
    }
    for row in jazz:
        status = row.get("status", "")
        source = row.get("speech_source", "")
        notes = row.get("notes", "")
        if status not in ("missing", "need_pack") and "need_pack" not in notes and source != "missing":
            continue
        if status == "done_manual":
            continue
        slug = row.get("slug", "")
        hints = name_hints.get(slug, [slug] if slug else [])
        name_hits = []
        for r in rows:
            merc_l = r["merc"].lower()
            if hints and any(h in merc_l for h in hints):
                name_hits.append(
                    f"{r['cat']}/{r['merc']} pids={r['pids']} n={r['n_audio']}"
                )
        shown = " | ".join(name_hits) if name_hits else "no folder-name hit"
        print(
            f"{slug}\tpid={row.get('profile_id') or '-'}\t"
            f"status={status}\tsrc={source}\t{shown}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
