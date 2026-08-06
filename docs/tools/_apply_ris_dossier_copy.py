# -*- coding: utf-8 -*-
"""Apply artistic RIS dossier/UI/welcome copy into Content.lua + CSV + design canon."""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "docs/tools"))
from _ris_dossier_copy import DOSSIERS, QUEST_DOSSIERS, STRING_FIXES  # noqa: E402

CONTENT = ROOT / "Code/System_RIS_Content.lua"
TAG = "JAZZ-UI-RIS-001-B"


def lua_esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def load_csv(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    prefix = ""
    if text.startswith("sep="):
        i = text.find("\n")
        prefix = text[: i + 1]
        body = text[i + 1 :]
    else:
        body = text
    return prefix, list(csv.reader(io.StringIO(body)))


def write_csv(path: Path, prefix: str, rows):
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    for row in rows:
        w.writerow(row)
    path.write_text(prefix + out.getvalue(), encoding="utf-8-sig")


def upsert(rows, rid, en, ru, *, en_file: bool):
    row = [rid, ru, en, "", TAG] if en_file else [rid, en, ru, "", TAG]
    for i, r in enumerate(rows):
        if r and r[0] == rid:
            rows[i] = row
            return
    rows.append(row)


def patch_content_and_collect_ids():
    text = CONTENT.read_text(encoding="utf-8")
    id_map = {}  # (kind, key, field) -> id  unused; we parse from lua

    # Replace dossier bodies/titles by matching T(id, "old")
    def repl_entry(block: str, bank: dict, key: str) -> str:
        if key not in bank:
            return block
        d = bank[key]
        # title
        m = re.search(
            rf'\["{re.escape(key)}"\]\s*=\s*\{{\s*title\s*=\s*T\((\d+),\s*"(.*?)"\)\s*,\s*body\s*=\s*T\((\d+),\s*"(.*?)"\)\s*\}}',
            block,
            re.S,
        )
        if not m:
            # try single-line
            m = re.search(
                rf'\["{re.escape(key)}"\] = \{{ title = T\((\d+), "(.*?)"\), body = T\((\d+), "(.*?)"\) \}}',
                block,
            )
        if not m:
            raise SystemExit(f"cannot parse dossier {key}")
        tid_t, _old_t, tid_b, _old_b = m.group(1), m.group(2), m.group(3), m.group(4)
        new = (
            f'["{key}"] = {{ title = T({tid_t}, "{lua_esc(d["title_en"])}"), '
            f'body = T({tid_b}, "{lua_esc(d["body_en"])}") }}'
        )
        return re.sub(
            rf'\["{re.escape(key)}"\]\s*=\s*\{{.*?\}}',
            new,
            block,
            count=1,
            flags=re.S,
        ), (tid_t, tid_b, d)

    # Simpler: for each key, replace title and body T strings separately with known IDs from content
    pairs = []
    for key, d in {**DOSSIERS, **{f"QUEST::{k}": v for k, v in QUEST_DOSSIERS.items()}}.items():
        pass

    updates = []  # (id, en, ru)

    def sub_t(field: str, key: str, en: str, ru: str, bank_label: str):
        nonlocal text
        # Find: ["key"] = { title = T(ID, "..."), body = T(ID, "...") }
        pat = re.compile(
            rf'(\["{re.escape(key)}"\]\s*=\s*\{{\s*{field}\s*=\s*T\()(\d+)(,\s*")(.*?)("\))',
            re.S,
        )
        m = pat.search(text)
        if not m:
            raise SystemExit(f"missing {bank_label} {key} {field}")
        tid = m.group(2)
        text = pat.sub(
            lambda mm: mm.group(1) + tid + mm.group(3) + lua_esc(en) + mm.group(5),
            text,
            count=1,
        )
        updates.append((tid, en, ru))

    for key, d in DOSSIERS.items():
        sub_t("title", key, d["title_en"], d["title_ru"], "dossier")
        sub_t("body", key, d["body_en"], d["body_ru"], "dossier")
    for key, d in QUEST_DOSSIERS.items():
        sub_t("title", key, d["title_en"], d["title_ru"], "quest")
        sub_t("body", key, d["body_en"], d["body_ru"], "quest")

    # UI keys in JAZZ_RIS_UI
    ui_map = {sid: (en, ru) for sid, en, ru in STRING_FIXES}
    for m in re.finditer(r"(\w+)\s*=\s*T\((\d+),\s*\"(.*?)\"\)", text):
        name, tid, _old = m.group(1), m.group(2), m.group(3)
        if tid in ui_map and name in (
            "site_title",
            "tab_bulletin",
            "tab_dossiers",
            "tab_reports",
            "empty_bulletin",
            "empty_dossiers",
            "empty_reports",
            "kills_progress",
            "dossier_locked",
            "section_quest",
            "section_legion",
            "supply_header",
            "mail_archive",
        ):
            en, ru = ui_map[tid]
            text = text[: m.start(3)] + lua_esc(en) + text[m.end(3) :]
            # careful: offsets invalidate — better rebuild differently

    CONTENT.write_text(text, encoding="utf-8")
    return updates


def patch_content_v2():
    text = CONTENT.read_text(encoding="utf-8")
    updates = []

    def replace_t_for_key(key: str, field: str, en: str, ru: str):
        nonlocal text
        pat = re.compile(
            rf'(\["{re.escape(key)}"\]\s*=\s*\{{[^}}]*?{field}\s*=\s*T\()(\d+)(,\s*")(.*?)("\))',
            re.S,
        )
        m = pat.search(text)
        if not m:
            raise SystemExit(f"parse fail {key}.{field}")
        tid = m.group(2)

        def _repl(mm, _en=en, _tid=tid):
            return mm.group(1) + _tid + mm.group(3) + lua_esc(_en) + mm.group(5)

        text, n = pat.subn(_repl, text, count=1)
        if n != 1:
            raise SystemExit(f"replace n={n} {key}.{field}")
        updates.append((tid, en, ru))

    for key, d in DOSSIERS.items():
        replace_t_for_key(key, "title", d["title_en"], d["title_ru"])
        replace_t_for_key(key, "body", d["body_en"], d["body_ru"])
    for key, d in QUEST_DOSSIERS.items():
        replace_t_for_key(key, "title", d["title_en"], d["title_ru"])
        replace_t_for_key(key, "body", d["body_en"], d["body_ru"])

    # Replace any T(id, "...") for STRING_FIXES by id
    for sid, en, ru in STRING_FIXES:
        pat = re.compile(rf'(T\({sid},\s*")(.*?)("\))', re.S)
        if pat.search(text):
            text, n = pat.subn(lambda m, e=en: m.group(1) + lua_esc(e) + m.group(3), text, count=1)
            if n != 1:
                print("warn content T replace", sid, n)
        updates.append((sid, en, ru))

    # Also items.lua welcome email
    items = (ROOT / "items.lua").read_text(encoding="utf-8")
    for sid, en, ru in STRING_FIXES:
        if sid not in ("890000000006922", "890000000006923", "890000000006924"):
            continue
        pat = re.compile(rf'(T\({sid}, --\[\[[^\]]*\]\] ")(.*?)("\))', re.S)
        if not pat.search(items):
            pat = re.compile(rf'(T\({sid}, --\[\[[^\]]*\]\] ")(.*?)("\))', re.S)
        items2, n = pat.subn(lambda m, e=en: m.group(1) + lua_esc(e) + m.group(3), items, count=1)
        if n == 1:
            items = items2
            print("items", sid)
        else:
            # fallback without comment
            pat2 = re.compile(rf'(T\({sid},\s*")(.*?)("\))', re.S)
            items2, n = pat2.subn(lambda m, e=en: m.group(1) + lua_esc(e) + m.group(3), items, count=1)
            if n == 1:
                items = items2
                print("items fallback", sid)

    CONTENT.write_text(text, encoding="utf-8")
    (ROOT / "items.lua").write_text(items, encoding="utf-8")
    return updates


def patch_csvs(updates):
    ru_p, ru_rows = load_csv(ROOT / "Russian.csv")
    en_p, en_rows = load_csv(ROOT / "English.csv")
    for sid, en, ru in updates:
        upsert(ru_rows, sid, en, ru, en_file=False)
        upsert(en_rows, sid, en, ru, en_file=True)
    write_csv(ROOT / "Russian.csv", ru_p, ru_rows)
    write_csv(ROOT / "English.csv", en_p, en_rows)
    print("csv updates", len(updates))


def patch_design():
    lines = [
        "# R.I.S. Legion unit dossiers (canon)",
        "",
        "Unlock: contact sighting mail (catalog) and/or ≥3 player-side kills (full body).",
        "Copy source: `docs/tools/_ris_dossier_copy.py` → apply via `_apply_ris_dossier_copy.py`.",
        "",
        "| UnitData id | Title | Notes |",
        "| --- | --- | --- |",
    ]
    for key, d in sorted(DOSSIERS.items()):
        note = d["body_en"].replace("\n", " ")[:100] + "…"
        lines.append(f"| `{key}` | **{d['title_en']}** / {d['title_ru']} | {note} |")
    lines.append("")
    lines.append("Quest cards:")
    for key, d in QUEST_DOSSIERS.items():
        lines.append(f"- **{key}**: {d['title_en']} — {d['body_en'][:120]}…")
    (ROOT / "docs/design/ris-legion-dossiers.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    updates = patch_content_v2()
    patch_csvs(updates)
    patch_design()
    print("done", len(updates))


if __name__ == "__main__":
    main()
