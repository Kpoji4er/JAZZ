# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []

with (ROOT / "Russian.csv").open(encoding="utf-8", newline="") as f:
    rows = {r[0]: r for r in csv.reader(f) if r}

for rid in ("890000000010024", "890000000010027", "890000000010030"):
    ru = rows[rid][2]
    if "при Медицине от" not in ru:
        errors.append(f"{rid}: missing polished Medical phrasing")
    if "Стабилизирует" not in ru:
        errors.append(f"{rid}: missing stabilize RU")

r213 = rows["890000000010213"][2]
if "заживление" in r213:
    errors.append("010213 RU still mentions healing trauma")
if "стабилиз" not in r213.lower():
    errors.append("010213 RU missing stabilize")
if "у порога кита" in r213:
    errors.append("010213 RU awkward «кита»")
if "у порога аптечки" not in r213:
    errors.append("010213 RU missing «у порога аптечки»")

# Manual: at most one active MED-006 SourceText row per kit id (no duplicate append)
for manual_name in ("RussianManual.csv", "EnglishManual.csv"):
    path = ROOT / "Localization" / manual_name
    with path.open(encoding="utf-8", newline="") as f:
        mrows = list(csv.reader(f))[1:]
    counts = {}
    for r in mrows:
        if len(r) < 3:
            continue
        aid = r[1]
        if aid in ("890000000010024", "890000000010027", "890000000010030", "890000000010213"):
            counts[aid] = counts.get(aid, 0) + 1
        if aid == "890000000010213" and "starts healing on the heaviest" in r[2]:
            errors.append(f"{manual_name}: stale Bandage CA SourceText still present")
    for aid, n in counts.items():
        if n > 1:
            errors.append(f"{manual_name}: {aid} has {n} rows (expect 1 after cleanup)")

for rid in ("890000000010290", "890000000010291", "890000000010292"):
    ru = rows[rid][2]
    if not any("\u0400" <= c <= "\u04FF" for c in ru):
        errors.append(f"{rid}: no Cyrillic in RU Translation")

items = (ROOT / "items.lua").read_text(encoding="utf-8")
if "starts healing on a light trauma" in items:
    errors.append("items.lua still has old kit healing Bandage description")
if "stabilizes one eligible trauma" not in items.lower():
    errors.append("items.lua Bandage CA missing stabilize wording")

with (ROOT / "English.csv").open(encoding="utf-8", newline="") as f:
    en_rows = {r[0]: r for r in csv.reader(f) if r}
if "starts healing" in en_rows["890000000010213"][2].lower():
    errors.append("010213 EN still starts healing")

# VoiceResponse IDs must not be medicine in jazz CSV
for rid in ("890000000010220", "890000000010221", "890000000010222"):
    t = en_rows[rid][2]
    if "trauma stabilized" in t.lower() or "Max HP debt" in t:
        errors.append(f"{rid} still medicine text in English.csv")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
print("OK MED-006 loc review")
