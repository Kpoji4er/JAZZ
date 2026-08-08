# -*- coding: utf-8 -*-
"""Remap MERC loc IDs off VoiceResponse range 007xxx -> 009900+; restore stolen VR rows from HEAD."""
from __future__ import annotations

import csv
import io
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# old MERC id -> new free id (avoid jazz-units VR 890000000007000+)
MAP = {
    "890000000007018": "890000000009900",  # Org:
    "890000000007019": "890000000009901",  # Status:
    "890000000007049": "890000000009902",  # copyright M.E.R.C.
    "890000000007100": "890000000009903",  # All
    "890000000007101": "890000000009904",  # Available
    "890000000007102": "890000000009905",  # My Team
    "890000000007103": "890000000009906",  # M.E.R.C. tab
    "890000000007120": "890000000009907",  # KIA
    "890000000007121": "890000000009908",  # MIA
    "890000000007200": "890000000009909",  # welcome sender
    "890000000007201": "890000000009910",  # welcome body
    "890000000007202": "890000000009911",  # welcome title
    "890000000007203": "890000000009912",  # reminder sender
    "890000000007204": "890000000009913",  # reminder body
    "890000000007205": "890000000009914",  # reminder title
    "890000000007206": "890000000009915",  # quit sender
    "890000000007207": "890000000009916",  # quit body
    "890000000007208": "890000000009917",  # quit title
    "890000000007211": "890000000009918",  # due
    "890000000007212": "890000000009919",  # Pay Account
}

STOLEN = list(MAP.keys())

CODE_GLOBS = [
    "items.lua",
    "Code/System_MERC_Browser.lua",
    "Code/System_MERC_Mail.lua",
    "Code/System_MERC_Filters.lua",
    "Code/System_MERC_Browser_Template.lua",
    "docs/tools/_append_merc_mail_loc.py",
    "docs/tools/README.md",
    "docs/design/merc-recruiting-center.md",
]


def load_csv(path: Path):
    raw = path.read_text(encoding="utf-8")
    sep = ""
    body = raw
    if raw.startswith("sep="):
        first, rest = raw.split("\n", 1)
        sep = first + "\n"
        body = rest
    rows = list(csv.reader(io.StringIO(body)))
    return sep, rows


def dump_csv(sep: str, rows: list) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
    return sep + buf.getvalue()


def head_csv(name: str) -> dict[str, list[str]]:
    out = subprocess.check_output(
        ["git", "show", f"HEAD:{name}"],
        cwd=str(ROOT),
        encoding="utf-8",
        errors="replace",
    )
    body = out.split("\n", 1)[1] if out.startswith("sep=") else out
    return {r[0]: r for r in csv.reader(io.StringIO(body)) if r}


def remap_text(text: str) -> str:
    # longest-first not needed; all same length. Replace whole IDs only.
    def repl(m: re.Match) -> str:
        old = m.group(0)
        return MAP.get(old, old)

    return re.sub(r"890000000007(?:018|019|049|100|101|102|103|120|121|200|201|202|203|204|205|206|207|208|211|212)\b", repl, text)


def restore_and_upsert_csv(name: str, merc_rows_by_new: dict[str, list[str]]):
    sep, rows = load_csv(ROOT / name)
    head = head_csv(name)
    by_id = {r[0]: i for i, r in enumerate(rows) if r}

    # Restore stolen VoiceResponse rows from HEAD
    for old in STOLEN:
        if old not in head:
            continue
        restored = list(head[old])
        if old in by_id:
            rows[by_id[old]] = restored
        else:
            # insert near neighbors if possible
            rows.append(restored)
            by_id[old] = len(rows) - 1

    # Remove any leftover MERC text on old IDs already restored above.
    # Upsert new MERC IDs
    for new_id, row in merc_rows_by_new.items():
        if new_id in by_id:
            rows[by_id[new_id]] = row
        else:
            rows.append(row)
            by_id[new_id] = len(rows) - 1

    (ROOT / name).write_text(dump_csv(sep, rows), encoding="utf-8", newline="\n")


def main():
    # Remap code/docs first
    for rel in CODE_GLOBS:
        path = ROOT / rel
        if not path.exists():
            print("skip missing", rel)
            continue
        text = path.read_text(encoding="utf-8")
        new = remap_text(text)
        # also update prose mentions of old ranges in docs
        new = new.replace("890000000007018+", "890000000009900+")
        new = new.replace("890000000007100+", "890000000009900+")
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n" if rel.endswith(".py") else None)
            print("remapped", rel)
        else:
            print("unchanged", rel)

    # Build merc rows from current English/Russian (MERC text still on old IDs)
    en_sep, en_rows = load_csv(ROOT / "English.csv")
    ru_sep, ru_rows = load_csv(ROOT / "Russian.csv")
    en_by = {r[0]: r for r in en_rows if r}
    ru_by = {r[0]: r for r in ru_rows if r}

    en_new: dict[str, list[str]] = {}
    ru_new: dict[str, list[str]] = {}
    for old, new in MAP.items():
        er = en_by.get(old)
        rr = ru_by.get(old)
        if not er or not rr:
            raise SystemExit(f"missing current MERC row for {old}")
        # English.csv: Text=RU source?, Translation=EN — keep same column layout as current row
        en_new[new] = [new] + er[1:]
        ru_new[new] = [new] + rr[1:]

    restore_and_upsert_csv("English.csv", en_new)
    restore_and_upsert_csv("Russian.csv", ru_new)
    print("csv restored VR + upserted", len(MAP), "MERC ids at 009900+")


if __name__ == "__main__":
    main()
