# Restore CR/LF that a loc pass flattened out of Russian.csv / English.csv.
# Strategy: for each ID present in HEAD, if working-tree Text/Translation match HEAD
# after collapsing whitespace (incl. newlines → spaces), copy HEAD cell values back.
# Does not touch IDs missing from HEAD or rows whose wording truly changed.
from __future__ import annotations

import argparse
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def flatten(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"\s+", " ", s).strip()


def compact(s: str) -> str:
    """Whitespace-insensitive compare; loc strip often glued words across former \\n."""
    return re.sub(r"\s+", "", s.replace("\r\n", "\n").replace("\r", "\n"))


def load_csv_bytes(data: str) -> tuple[list[str], list[list[str]]]:
    r = csv.reader(io.StringIO(data))
    rows = list(r)
    return rows[0], rows[1:]


def git_show(rel: str) -> str:
    p = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return p.stdout.decode("utf-8-sig")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    for name in ("Russian.csv", "English.csv"):
        head_data = git_show(name)
        wt_path = ROOT / name
        wt_data = wt_path.read_text(encoding="utf-8-sig")
        h_header, h_rows = load_csv_bytes(head_data)
        w_header, w_rows = load_csv_bytes(wt_data)
        by_h = {r[0]: r for r in h_rows if r}
        restored = 0
        skipped_changed = 0
        for row in w_rows:
            if not row:
                continue
            tid = row[0]
            href = by_h.get(tid)
            if not href:
                continue
            while len(row) < 3:
                row.append("")
            while len(href) < 3:
                href.append("")
            changed = False
            for col in (1, 2):
                h = href[col] or ""
                w = row[col] or ""
                if not h or "\n" not in h:
                    continue
                if "\n" in w:
                    continue
                if flatten(h) != flatten(w) and compact(h) != compact(w):
                    skipped_changed += 1
                    continue
                row[col] = h
                changed = True
            if changed:
                restored += 1
        print(f"{name}: restore_from_head={restored} skipped_wording_diff={skipped_changed}")
        if args.apply and restored:
            tmp = wt_path.with_suffix(wt_path.suffix + ".tmp")
            with tmp.open("w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(w_header)
                w.writerows(w_rows)
            tmp.replace(wt_path)
            print(f"  wrote {wt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
