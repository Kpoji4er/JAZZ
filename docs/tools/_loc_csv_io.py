"""Safe read/write for JA3-style Russian.csv / English.csv.

Never pre-split the file with str.splitlines() before csv.DictReader —
that destroys quoted multiline fields (weapon AdditionalHint bullets, perk
text, map outcomes). Always parse via StringIO / file handle.

IMPORTANT: jazz *runtime* root `Russian.csv` / `English.csv` are often
`sep=,` + data rows with **no** `ID,Text,Translation,...` header. DictReader
will treat the first data row as field names and corrupt the file on write.
For those files use raw `csv.reader` (see `_fix_med_en_in_ru_loc.py`).
This helper is for catalog-style CSVs that *do* include a header row.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path

DEFAULT_FIELDS = ["ID", "Text", "Translation", "VoiceActor", "Context"]


def strip_sep_prefix(text: str) -> tuple[str | None, str]:
    if text.startswith("sep="):
        nl = text.find("\n")
        if nl < 0:
            return text.rstrip("\r"), ""
        return text[:nl].rstrip("\r"), text[nl + 1 :]
    return None, text


def load_rows(path: Path):
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sep, body = strip_sep_prefix(text)
    reader = csv.DictReader(io.StringIO(body))
    fields = list(reader.fieldnames or DEFAULT_FIELDS)
    rows = list(reader)
    by_id = {(r.get("ID") or "").strip(): r for r in rows if (r.get("ID") or "").strip()}
    return sep, fields, rows, by_id


def write_rows(path: Path, sep, fields, rows) -> None:
    buf = io.StringIO(newline="")
    w = csv.DictWriter(
        buf, fieldnames=fields, lineterminator="\n", quoting=csv.QUOTE_MINIMAL
    )
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in fields})
    path.write_text((sep + "\n" if sep else "") + buf.getvalue(), encoding="utf-8")


def existing_ids(path: Path) -> set[str]:
    _, _, _, by_id = load_rows(path)
    return set(by_id)
