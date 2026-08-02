# -*- coding: utf-8 -*-
"""Pour AIM-chat phrases from docs/design/mercs-ja12/<slug>.md into UnitData.

Updates companion UnitData, jazz-units/items.lua T() strings, Russian.csv + English.csv.
Also injects missing PartingWords ChatMessage blocks when design has the phrase.

Usage (jazz/):
  python docs/tools/_pour_ja12_design_hire_chat.py --dry-run --only gaston,biggens
  python docs/tools/_pour_ja12_design_hire_chat.py --apply --only vince,devin,carlos,hitman,eskimo,biggens,kulba,gaston,quinten,highball,nervous,hobbit,cord,dynamo,gamos
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
DESIGN = JAZZ / "docs/design/mercs-ja12"
UNITDATA = JU / "UnitData"
ITEMS = JU / "items.lua"
RU_CSV = JAZZ / "Russian.csv"
EN_CSV = JAZZ / "English.csv"

CHAT_FIELDS = [
    "Offline",
    "GreetingAndOffer",
    "ConversationRestart",
    "IdleLine",
    "PartingWords",
    "RehireIntro",
    "RehireOutro",
    "ExtraPartingWords",
]


def esc_lua(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def parse_design_chat(slug: str) -> dict[str, dict[str, str]]:
    path = DESIGN / f"{slug}.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    m = re.search(r"## Phrases — AIM chat\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        return {}
    body = m.group(1)
    out: dict[str, dict[str, str]] = {}
    for field in CHAT_FIELDS:
        fm = re.search(
            rf"### {field}\s*\n(.*?)(?=\n### |\n## |\Z)",
            body,
            re.S,
        )
        if not fm:
            continue
        block = fm.group(1)
        ru_m = re.search(r"-\s*RU:\s*(.+)", block)
        en_m = re.search(r"-\s*EN:\s*(.+)", block)
        ru = (ru_m.group(1).strip() if ru_m else "").strip()
        en = (en_m.group(1).strip() if en_m else "").strip()
        if ru == "..." and en == "...":
            continue
        if ru or en:
            out[field] = {"ru": ru or en, "en": en or ru}
    return out


def replace_t_string(text: str, tid: int, new: str) -> tuple[str, bool]:
    pat = re.compile(
        rf"(T\({tid}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?)(?P<q>[\"'])(?P<body>.*?)(?P=q)",
        re.S,
    )

    def repl(m: re.Match) -> str:
        q = m.group("q")
        body = esc_lua(new) if q == '"' else new.replace("\\", "\\\\").replace("'", "\\'")
        return f"{m.group(1)}{q}{body}{q}"

    new_text, n = pat.subn(repl, text, count=1)
    return new_text, n > 0


def load_csv(path: Path) -> tuple[list[str] | None, dict[str, list[str]], list[list[str]]]:
    if not path.exists():
        return None, {}, []
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return None, {}, []
    header = None
    start = 0
    if rows[0] and not re.fullmatch(r"\d+", (rows[0][0] or "").strip()):
        header = rows[0]
        start = 1
    by_id: dict[str, list[str]] = {}
    for row in rows[start:]:
        if row and row[0]:
            by_id[row[0]] = row
    return header, by_id, rows


def set_csv_translation(by_id: dict[str, list[str]], tid: str, text: str, lang: str) -> None:
    """JA3 CSV: col0=id, later cols hold translation; keep row width."""
    row = by_id.get(tid)
    if not row:
        # id, translation
        by_id[tid] = [tid, text]
        return
    if len(row) == 1:
        row.append(text)
    else:
        # Prefer last non-empty slot or index 1
        if len(row) >= 2:
            row[1] = text
        else:
            row.append(text)
    by_id[tid] = row


def write_csv(path: Path, header: list[str] | None, by_id: dict[str, list[str]], orig: list[list[str]]) -> None:
    # Preserve order from orig where possible
    ordered: list[list[str]] = []
    seen: set[str] = set()
    start = 0
    if header is not None:
        ordered.append(header)
        start = 1
    for row in orig[start:]:
        if not row or not row[0]:
            continue
        tid = row[0]
        if tid in by_id:
            ordered.append(by_id[tid])
            seen.add(tid)
    for tid, row in by_id.items():
        if tid not in seen:
            ordered.append(row)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(ordered)


def field_block_re(field: str) -> re.Pattern[str]:
    return re.compile(rf"({field}\s*=\s*\{{)(.*?)(\}}\s*,)", re.S)


def parting_from_items(items_text: str, unit: str) -> tuple[int, str] | None:
    """Return (tid, ru) for PartingWords in items.lua UnitData block."""
    m = re.search(rf"'Id',\s*\"{unit}\".*?MedicalDeposit", items_text, re.S)
    if not m:
        return None
    pm = re.search(r"'PartingWords',\s*\{(.*?)\}", m.group(0), re.S)
    if not pm:
        return None
    tm = re.search(
        r"T\((\d+),\s*(?:--\[\[[^\]]*\]\]\s*)?\"((?:\\.|[^\"\\])*)\"",
        pm.group(1),
        re.S,
    )
    if not tm:
        return None
    return int(tm.group(1)), tm.group(2).replace('\\"', '"').replace("\\\\", "\\")


def ensure_parting_words(
    unit_text: str,
    unit: str,
    ru: str,
    next_tid: int,
    *,
    prefer_tid: int | None = None,
) -> tuple[str, int | None]:
    """If PartingWords missing or empty of T(), inject a ChatMessage."""
    m = re.search(r"(?<!Extra)PartingWords\s*=\s*\{(.*?)\}\s*,", unit_text, re.S)
    if m and re.search(r"T\(\d+,", m.group(1)):
        return unit_text, None
    # Repair prior bad inject that split ExtraPartingWords → "Extra\tPartingWords"
    unit_text = re.sub(
        r"Extra\tPartingWords\s*=\s*\{.*?\}\s*,\n*",
        "",
        unit_text,
        count=1,
        flags=re.S,
    )
    m = re.search(r"(?<!Extra)PartingWords\s*=\s*\{(.*?)\}\s*,", unit_text, re.S)
    if m and re.search(r"T\(\d+,", m.group(1)):
        return unit_text, None
    tid = prefer_tid if prefer_tid is not None else next_tid
    block = (
        f"\tPartingWords = {{\n"
        f"\t\tPlaceObj('ChatMessage', {{\n"
        f"\t\t\t'Text', T({tid}, --[[ModItemUnitDataCompositeDef {unit} Text PartingWords ChatMessage voice:{unit}]] \"{esc_lua(ru)}\"),\n"
        f"\t\t}}),\n"
        f"\t}},\n"
    )
    if m:
        unit_text = (
            unit_text[: m.start()]
            + block.rstrip("\n")
            + "\n"
            + unit_text[m.end() :]
        )
        return unit_text, tid
    # insert before RehireIntro or MedicalDeposit
    ins = re.search(r"\n\t(RehireIntro|MedicalDeposit)\s*=", unit_text)
    if not ins:
        return unit_text, None
    unit_text = unit_text[: ins.start()] + "\n" + block + unit_text[ins.start() + 1 :]
    return unit_text, tid


def max_tid_in_text(text: str) -> int:
    ids = [int(x) for x in re.findall(r"T\((\d+),", text)]
    return max(ids) if ids else 890000000004900


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, required=True)
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True

    slugs = [s.strip().lower() for s in args.only.split(",") if s.strip()]
    items = ITEMS.read_text(encoding="utf-8") if ITEMS.exists() else ""
    ru_header, ru_by, ru_orig = load_csv(RU_CSV)
    en_header, en_by, en_orig = load_csv(EN_CSV)
    changed = 0

    for slug in slugs:
        phrases = parse_design_chat(slug)
        if not phrases:
            print(f"SKIP {slug}: no design AIM chat")
            continue
        unit = f"Jazz_{slug.capitalize()}" if slug != "quinten" else "Jazz_Quinten"
        # capitalize fixes: highball→Highball, etc. Special cases:
        special = {
            "quinten": "Jazz_Quinten",
            "highball": "Jazz_Highball",
            "biggens": "Jazz_Biggens",
            "kulba": "Jazz_Kulba",
            "gaston": "Jazz_Gaston",
            "manuel": "Jazz_Manuel",
            "vince": "Jazz_Vince",
            "devin": "Jazz_Devin",
            "carlos": "Jazz_Carlos",
            "hitman": "Jazz_Hitman",
            "eskimo": "Jazz_Eskimo",
            "nervous": "Jazz_Nervous",
            "hobbit": "Jazz_Hobbit",
            "cord": "Jazz_Cord",
            "dynamo": "Jazz_Dynamo",
            "gamos": "Jazz_Gamos",
            "mike": "Jazz_Mike",
            "ira": "Jazz_Ira",
        }
        unit = special.get(slug, unit)
        upath = UNITDATA / f"{unit}.lua"
        if not upath.exists():
            print(f"SKIP {slug}: no {upath.name}")
            continue
        utext = upath.read_text(encoding="utf-8")
        print(f"=== {slug} {unit}")

        # Sync / inject PartingWords into companion when missing (items often has it).
        if "PartingWords" in phrases:
            pw = phrases["PartingWords"]["ru"]
            from_items = parting_from_items(items, unit)
            prefer = from_items[0] if from_items else None
            if from_items and from_items[1].strip():
                pw = from_items[1]
            nxt = max(max_tid_in_text(utext), max_tid_in_text(items)) + 1
            utext2, new_tid = ensure_parting_words(
                utext, unit, pw, nxt, prefer_tid=prefer
            )
            if new_tid and utext2 != utext:
                print(f"  sync/inject PartingWords tid={new_tid}")
                utext = utext2

        for field, langs in phrases.items():
            # Avoid ExtraPartingWords matching when looking up PartingWords.
            fm = re.search(
                rf"(?<![A-Za-z]){field}\s*=\s*\{{(.*?)\}}\s*,",
                utext,
                re.S,
            )
            if not fm:
                print(f"  {field}: no field in companion")
                continue
            tids = [int(x) for x in re.findall(r"T\((\d+),", fm.group(1))]
            if not tids:
                print(f"  {field}: no T-id")
                continue
            tid = tids[0]
            ru, en = langs["ru"], langs["en"]
            print(f"  {field} tid={tid} <- {ru[:50]}")
            utext, ok_u = replace_t_string(utext, tid, ru)
            items, ok_i = replace_t_string(items, tid, ru)
            set_csv_translation(ru_by, str(tid), ru, "ru")
            set_csv_translation(en_by, str(tid), en, "en")
            if ok_u or ok_i:
                changed += 1
            else:
                changed += 1  # csv / already-equal still counts as processed

        if not args.dry_run:
            upath.write_text(utext, encoding="utf-8")

    if not args.dry_run:
        if items:
            ITEMS.write_text(items, encoding="utf-8")
        write_csv(RU_CSV, ru_header, ru_by, ru_orig)
        write_csv(EN_CSV, en_header, en_by, en_orig)
    print(f"done changed_fields~={changed} dry={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
