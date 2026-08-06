# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import io

ROOT = Path(__file__).resolve().parents[2]


def csv_line(row):
    bio = io.StringIO()
    csv.writer(bio, lineterminator="").writerow(row)
    return bio.getvalue()


updates = {
    "890000000011202": (
        "R.I.S. field note — contact\n\nWe logged a new Legion archetype after your contact: <unit_title>.\n\n<dossier>\n\nThis type is now on the R.I.S. site dossier catalog.\n\n— Recon Intelligence Services",
        "Полевая заметка R.I.S. — контакт\n\nПосле вашего контакта на файл поставлен новый архетип Легиона: <unit_title>.\n\n<dossier>\n\nЭтот тип добавлен в каталог досье на сайте R.I.S.\n\n— Recon Intelligence Services",
    ),
    "890000000011204": (
        "R.I.S. desk notice — elite down\n\n<field_note>\n\n— Recon Intelligence Services",
        "Уведомление стола R.I.S. — элита снята\n\n<field_note>\n\n— Recon Intelligence Services",
    ),
    "890000000011206": (
        "R.I.S. desk notice — person of interest\n\n<field_note>\n\n— Recon Intelligence Services",
        "Уведомление стола R.I.S. — важное лицо\n\n<field_note>\n\n— Recon Intelligence Services",
    ),
    "890000000011005": (
        "No dossiers unlocked yet. New Legion types appear here when their R.I.S. contact note arrives.",
        "Досье ещё не открыты. Новые типы Легиона появляются здесь, когда приходит заметка R.I.S. о контакте.",
    ),
}

for name in ("English.csv", "Russian.csv"):
    p = ROOT / name
    lines = p.read_text(encoding="utf-8-sig").splitlines()
    out = []
    n = 0
    for line in lines:
        if not line.strip() or line.startswith("sep="):
            out.append(line)
            continue
        row = next(csv.reader([line]))
        if row and row[0] in updates:
            en, ru = updates[row[0]]
            tag = row[4] if len(row) > 4 else "JAZZ-UI-RIS-001"
            empty = row[3] if len(row) > 3 else ""
            if name == "English.csv":
                row = [row[0], ru, en, empty, tag]
            else:
                row = [row[0], en, ru, empty, tag]
            out.append(csv_line(row))
            n += 1
        else:
            out.append(line)
    p.write_text("\n".join(out) + "\n", encoding="utf-8-sig")
    print(name, "updated", n)

c = ROOT / "Code" / "System_RIS_Content.lua"
t = c.read_text(encoding="utf-8")
old = 'empty_dossiers = T(890000000011005, "No dossiers unlocked. Kill three fighters of the same Legion type to open their file."),'
new = 'empty_dossiers = T(890000000011005, "No dossiers unlocked yet. New Legion types appear here when their R.I.S. contact note arrives."),'
if old in t:
    t = t.replace(old, new)
    print("content empty_dossiers updated")
if "JAZZ_RIS_KEY_NPCS" not in t:
    t = t.rstrip() + """

-- Key NPC session_ids for R.I.S. obituaries (same desk queue).
JAZZ_RIS_KEY_NPCS = {
	Pierre = true,
	Bastien = true,
	TheMajor = true,
	Spike = true,
	Faucheux = true,
	CorazonSantiago = true,
	Boss = true,
	Emma = true,
	Biff = true,
	FleatownBoss = true,
	Luigi = true,
	Baron = true,
	DiamondRedBoss = true,
}
"""
    print("KEY_NPCS appended")
if not t.endswith("\n"):
    t += "\n"
c.write_text(t, encoding="utf-8")
print("ok")
