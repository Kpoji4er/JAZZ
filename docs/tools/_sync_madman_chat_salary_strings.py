"""Sync Madman salary + chat string updates into jazz-units/items.lua and jazz CSV."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")

REPLACEMENTS = [
    (
        'Ха! Поехали крушить. Бесплатно, лишь бы весело было.',
        'Ха! Поехали крушить. Дёшево и сердито — лишь бы весело было.',
    ),
    (
        'Контракт заканчивается, но я всё равно бесплатный — продлеваем?',
        'Контракт заканчивается — продлеваем, или сам пойду кого-нибудь чинить?',
    ),
]

EN_BY_ID = {
    "890000000002115": "Ha! Let's go smash stuff. Cheap and nasty — as long as it's fun.",
    "890000000002116": "Contract's up — renewing, or do I wander off and fix somebody else's junk?",
}


def replace_all(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    n = 0
    for old, new in REPLACEMENTS:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    if n:
        path.write_text(text, encoding="utf-8")
    return n


def patch_csv(path: Path, id_to_text: dict[str, str], column: str) -> int:
    """column: 'ru' keeps id,ru,en,... updating both if mirrored; 'en' updates English field."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = 0
    out = []
    for line in lines:
        m = re.match(r"^(\d+),(.*)$", line.rstrip("\r\n"))
        if not m:
            out.append(line)
            continue
        lid = m.group(1)
        if lid not in id_to_text and lid not in ("890000000002115", "890000000002116"):
            out.append(line)
            continue
        # naive CSV: id,field1,field2,,comment — fields may be quoted
        # Prefer exact id known replacements for RU source strings
        new_line = line
        for old, new in REPLACEMENTS:
            if old in new_line:
                new_line = new_line.replace(old, new)
        if lid in EN_BY_ID and column == "en":
            # Replace English column: pattern id,RU,EN,,
            # After RU replace, set EN from map via regex
            en = EN_BY_ID[lid].replace('"', '""')
            # Match: id, <ru>, <en>, ,
            mm = re.match(
                r'^(\d+),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*),(.*)$',
                new_line.rstrip("\r\n"),
            )
            if mm:
                ru = mm.group(2)
                rest = mm.group(4)
                new_line = f'{lid},{ru},"{en}",{rest}\n'
                if not line.endswith("\n"):
                    new_line = new_line.rstrip("\n")
        if new_line != line:
            changed += 1
        out.append(new_line if new_line.endswith("\n") or not line.endswith("\n") else new_line)
        if not out[-1].endswith("\n") and line.endswith("\n"):
            out[-1] += "\n"
    if changed:
        path.write_text("".join(out), encoding="utf-8")
    return changed


def main() -> None:
    n_items = replace_all(UNITS / "items.lua")
    n_ru = 0
    n_en = 0
    # Update RU strings in both CSVs' first text field; EN column in English.csv
    for csv_name in ("Russian.csv", "English.csv"):
        p = JAZZ / csv_name
        text = p.read_text(encoding="utf-8")
        orig = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if csv_name == "English.csv":
            for lid, en in EN_BY_ID.items():
                # replace english field for these ids when still Russian or old EN
                pattern = re.compile(
                    rf'^({lid}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*),(.*)$',
                    re.M,
                )

                def sub(m: re.Match[str]) -> str:
                    ru = m.group(2)
                    rest = m.group(4)
                    en_q = '"' + en.replace('"', '""') + '"'
                    return f"{m.group(1)},{ru},{en_q},{rest}"

                text2, c = pattern.subn(sub, text)
                text = text2
                n_en += c
        if text != orig:
            p.write_text(text, encoding="utf-8")
            if csv_name == "Russian.csv":
                n_ru = 1
    print(f"items replacements={n_items} russian_touched={n_ru} english_id_rows={n_en}")


if __name__ == "__main__":
    main()
