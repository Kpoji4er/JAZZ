# -*- coding: utf-8 -*-
"""Fix RIS_LegionBrief_11 closing calque + related 'берите за' RU; rewrite items T source."""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Full bodies for brief 11 (EN source / RU) — accurate tone, no PPSh claim until we remap weapons.
# Keep structure; fix only the awful closing for now + soften PPSh to generic scrap (user flagged accuracy).
BODY_EN = (
    "R.I.S. field note — Legion supply\n\n"
    "The Major is still emptying old warehouses. Early patrols carry wartime leftovers: "
    "bolt rifles, cheap shotguns, tired pistols and the odd submachine gun that survived the last war. "
    "Ammo is thin; armor is mostly wishful thinking.\n\n"
    "Early Legion patrols are poorly equipped — but there are a lot of them. "
    "Do not mistake rust for safety.\n\n"
    "— Recon Intelligence Services"
)
BODY_RU = (
    "Полевая заметка R.I.S. — снабжение Легиона\n\n"
    "Майор по-прежнему вычищает старые склады. У ранних патрулей — военный хлам: "
    "болтовые винтовки, дешёвые дробовики, уставшие пистолеты и редкий пистолет-пулемёт, переживший прошлую войну. "
    "Патронов мало; броня — в основном фантазия.\n\n"
    "Ранние патрули Легиона слабо экипированы — но их много. "
    "Не путайте ржавчину с безопасностью.\n\n"
    "— Recon Intelligence Services"
)

ID = "890000000006942"


def csv_line(row):
    bio = io.StringIO()
    csv.writer(bio, lineterminator="").writerow(row)
    return bio.getvalue()


def upsert_csv():
    for name in ("English.csv", "Russian.csv"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8-sig")
        # Parse with csv to handle multiline
        start = 0
        prefix = ""
        if text.startswith("sep="):
            first_nl = text.find("\n")
            prefix = text[: first_nl + 1]
            body = text[first_nl + 1 :]
        else:
            body = text
        reader = csv.reader(io.StringIO(body))
        rows = list(reader)
        found = False
        for i, row in enumerate(rows):
            if row and row[0] == ID:
                tag = row[4] if len(row) > 4 else "JAZZ-UI-RIS-001"
                empty = row[3] if len(row) > 3 else ""
                if name == "English.csv":
                    rows[i] = [ID, BODY_RU, BODY_EN, empty, tag]
                else:
                    rows[i] = [ID, BODY_EN, BODY_RU, empty, tag]
                found = True
                break
        if not found:
            raise SystemExit(f"{name}: id {ID} not found")
        out = io.StringIO()
        w = csv.writer(out, lineterminator="\n")
        for row in rows:
            w.writerow(row)
        path.write_text(prefix + out.getvalue(), encoding="utf-8-sig")
        print(name, "updated", ID)


def patch_items():
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")
    # Escape for Lua string in T(...)
    esc = BODY_EN.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    # bodies may contain \n escapes already spanning one line, or raw newlines from a bad prior write
    pat2 = re.compile(
        r"body = T\(890000000006942, --\[\[ModItemEmail RIS_LegionBrief_11 body\]\] \".*?\"\),",
        re.S,
    )
    repl = f'body = T(890000000006942, --[[ModItemEmail RIS_LegionBrief_11 body]] "{esc}"),'
    # lambda: re.sub must not interpret \n in the replacement string
    new, n = pat2.subn(lambda _m: repl, text, count=1)
    if n != 1:
        raise SystemExit(f"items replace failed n={n}")
    path.write_text(new, encoding="utf-8")
    print("items.lua body updated")


def patch_tool_source():
    path = ROOT / "docs/tools/_apply_ris_mail_emails.py"
    if not path.exists():
        return
    t = path.read_text(encoding="utf-8")
    t2 = t.replace(
        "Ранние патрули Легиона берите за плохо экипированных, но многочисленных.\\n\\n",
        "Ранние патрули Легиона слабо экипированы — но их много. Не путайте ржавчину с безопасностью.\\n\\n",
    )
    t2 = t2.replace(
        "Treat early Legion patrols as poorly equipped but numerous.\\n\\n",
        "Early Legion patrols are poorly equipped — but there are a lot of them. Do not mistake rust for safety.\\n\\n",
    )
    # also fix other берите за if present
    t2 = t2.replace(
        "ветеранов берите за нормально вооружённых, а не за «улучшенных мародёров»",
        "ветеранов стоит считать нормально вооружёнными, а не «чуть лучшими мародёрами»",
    )
    if t2 != t:
        path.write_text(t2, encoding="utf-8")
        print("tool source patched")


def main():
    upsert_csv()
    patch_items()
    patch_tool_source()


if __name__ == "__main__":
    main()
