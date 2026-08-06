# -*- coding: utf-8 -*-
"""Add R.I.S. queue Email presets for unit sightings + obituaries (JAZZ-UI-RIS-001).

IDs: 890000000011200+ (after Phase B content bank ending ~11156).
Idempotent by Email id / loc id.
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "JAZZ-UI-RIS-001-Q"
BASE = 890000000011200

EMAILS = [
    # id, title_en, title_ru, body_en, body_ru, sender_en (shared), repeatable
    (
        "RIS_UnitSighting",
        "R.I.S. — new Legion type on file: <unit_title>",
        "R.I.S. — новый тип Легиона: <unit_title>",
        "R.I.S. field note — contact\n\nWe logged a new Legion archetype after your contact: <unit_title>.\n\n<dossier>\n\nFull dossier on the R.I.S. site unlocks after more confirmed kills.\n\n— Recon Intelligence Services",
        "Полевая заметка R.I.S. — контакт\n\nПосле вашего контакта на файл поставлен новый архетип Легиона: <unit_title>.\n\n<dossier>\n\nПолное досье на сайте R.I.S. откроется после дополнительных подтверждённых убийств.\n\n— Recon Intelligence Services",
    ),
    (
        "RIS_EliteObit",
        "R.I.S. — obituary: <name>",
        "R.I.S. — некролог: <name>",
        "R.I.S. desk notice — elite down\n\nConfirmed: <name> is down. Named Legion elites do not grow on trees — expect the Major to notice the hole in his roster.\n\n— Recon Intelligence Services",
        "Уведомление стола R.I.S. — элита снята\n\nПодтверждено: <name> снят(а). Именные элиты Легиона на деревьях не растут — Майор заметит дыру в списке.\n\n— Recon Intelligence Services",
    ),
    (
        "RIS_NpcObit",
        "R.I.S. — key figure down: <name>",
        "R.I.S. — ключевая фигура снята: <name>",
        "R.I.S. desk notice — person of interest\n\nConfirmed: <name> is off the board. A named person of interest just moved the local power map.\n\n— Recon Intelligence Services",
        "Уведомление стола R.I.S. — важное лицо\n\nПодтверждено: <name> больше не на доске. Именное лицо интереса только что сдвинуло карту силы.\n\n— Recon Intelligence Services",
    ),
]

SENDER_EN = "R.I.S. <desk@ris-intel.net>"
SENDER_RU = "R.I.S. <desk@ris-intel.net>"


def csv_line(row):
    bio = io.StringIO()
    csv.writer(bio, lineterminator="").writerow(row)
    return bio.getvalue()


def append_loc(rows):
    for name in ("English.csv", "Russian.csv"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8-sig")
        existing = set()
        for line in text.splitlines():
            if not line.strip() or line.startswith("sep="):
                continue
            try:
                row = next(csv.reader([line]))
            except Exception:
                continue
            if row:
                existing.add(row[0])
        additions = []
        for id_, en, ru in rows:
            if id_ in existing:
                continue
            if name == "English.csv":
                additions.append([id_, ru, en, "", TAG])
            else:
                additions.append([id_, en, ru, "", TAG])
        if not text.endswith("\n"):
            text += "\n"
        for row in additions:
            text += csv_line(row) + "\n"
        path.write_text(text, encoding="utf-8-sig")
        print(name, "appended", len(additions))


def email_block(eid, title_id, body_id, sender_id, title_en, body_en):
    def esc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    return f"""\t\tPlaceObj('ModItemEmail', {{
\t\t\tbody = T({body_id}, --[[ModItemEmail {eid} body]] "{esc(body_en)}"),
\t\t\tdelayAfterCombat = false,
\t\t\tgroup = "Default",
\t\t\tid = "{eid}",
\t\t\tlabel = "Important",
\t\t\trepeatable = true,
\t\t\tsender = T({sender_id}, --[[ModItemEmail {eid} sender]] "{SENDER_EN}"),
\t\t\ttitle = T({title_id}, --[[ModItemEmail {eid} title]] "{esc(title_en)}"),
\t\t}}),
"""


def patch_items(rows_by_email):
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")
    sender_id = rows_by_email["_sender"]
    # Insert after RIS_Welcome block
    anchor = "\t\tPlaceObj('ModItemEmail', {\n\t\t\tbody = T(890000000006923,"
    if "id = \"RIS_UnitSighting\"" in text or "id = 'RIS_UnitSighting'" in text:
        print("items: emails already present")
        return
    # Find end of RIS_Welcome PlaceObj — after title line and }),
    m = re.search(
        r"(PlaceObj\('ModItemEmail', \{\n\t\t\tbody = T\(890000000006923,.*?id = \"RIS_Welcome\".*?\n\t\t\}\),)",
        text,
        re.S,
    )
    if not m:
        raise SystemExit("RIS_Welcome anchor not found")
    chunk = m.group(1)
    extra = ""
    for eid, title_id, body_id, title_en, body_en in rows_by_email["emails"]:
        extra += email_block(eid, title_id, body_id, sender_id, title_en, body_en)
    text = text.replace(chunk, chunk + "\n" + extra, 1)
    path.write_text(text, encoding="utf-8")
    print("items: inserted", len(rows_by_email["emails"]), "emails")


def patch_metadata_resources():
    path = ROOT / "metadata.lua"
    text = path.read_text(encoding="utf-8")
    for eid in ("RIS_UnitSighting", "RIS_EliteObit", "RIS_NpcObit"):
        if f"'Id', \"{eid}\"" in text or f"'Id', '{eid}'" in text:
            continue
        needle = "'Id', \"RIS_Welcome\","
        if needle not in text:
            raise SystemExit("metadata RIS_Welcome resource missing")
        # insert ModResourcePreset after welcome resource block end is hard; append near welcome
        block = f"""\t\tPlaceObj('ModResourcePreset', {{
\t\t\t'Class', \"Email\",
\t\t\t'Id', \"{eid}\",
\t\t\t'ClassDisplayName', \"Email\",
\t\t}}),
"""
        # find welcome resource and insert after its closing
        m = re.search(
            r"PlaceObj\('ModResourcePreset', \{\n\t\t\t'Class', \"Email\",\n\t\t\t'Id', \"RIS_Welcome\",.*?\n\t\t\}\),",
            text,
            re.S,
        )
        if not m:
            raise SystemExit("welcome resource block not found")
        text = text.replace(m.group(0), m.group(0) + "\n" + block, 1)
        print("metadata +", eid)
    path.write_text(text, encoding="utf-8")


def patch_content_key_npcs():
    path = ROOT / "Code" / "System_RIS_Content.lua"
    text = path.read_text(encoding="utf-8")
    if "JAZZ_RIS_KEY_NPCS" in text:
        print("content: KEY_NPCS already present")
        return
    block = """
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
    path.write_text(text.rstrip() + "\n" + block + "\n", encoding="utf-8")
    print("content: KEY_NPCS appended")


def main():
    n = BASE
    loc_rows = []  # id, en, ru
    sender_id = str(n)
    loc_rows.append((sender_id, SENDER_EN, SENDER_RU))
    n += 1
    emails_meta = []
    for eid, ten, tru, ben, bru in EMAILS:
        tid, bid = str(n), str(n + 1)
        n += 2
        loc_rows.append((tid, ten, tru))
        loc_rows.append((bid, ben, bru))
        emails_meta.append((eid, tid, bid, ten, ben))
    append_loc(loc_rows)
    patch_items({"_sender": sender_id, "emails": emails_meta})
    patch_metadata_resources()
    patch_content_key_npcs()
    print("done, next free", n)


if __name__ == "__main__":
    main()
