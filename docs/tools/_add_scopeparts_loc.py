# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = {
    "Russian.csv": [
        (990002500, "Детали прицелов"),
        (990002501, "Детали прицелов"),
        (
            990002502,
            "Нужны при ремонте оружия с установленным прицелом. Также получаются при поломке прицела при неудачном снятии.",
        ),
        (990002503, "Снятие провалилось. Модуль сломан."),
        (990002504, "Снятие провалилось. Ресурс оружия снижен."),
        (990002505, "Модуль сломан при снятии."),
    ],
    "English.csv": [
        (990002500, "Scope Parts"),
        (990002501, "Scope Parts"),
        (
            990002502,
            "Used when repairing a firearm that has a scope installed. Also salvaged when a scope breaks on a failed removal.",
        ),
        (990002503, "Removal failed. Attachment broken."),
        (990002504, "Removal failed. Weapon resource max reduced."),
        (990002505, "Attachment broken on removal."),
    ],
}


def esc(val: str) -> str:
    if "," in val or '"' in val or "\n" in val:
        return '"' + val.replace('"', '""') + '"'
    return val


def main() -> None:
    for name, rows in ROWS.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        existing = set()
        for line in text.splitlines():
            if line and line[0].isdigit():
                existing.add(line.split(",", 1)[0])
        add = []
        for tid, val in rows:
            if str(tid) in existing:
                continue
            add.append(f"{tid},{esc(val)}")
        if add:
            if not text.endswith("\n"):
                text += "\n"
            path.write_text(text + "\n".join(add) + "\n", encoding="utf-8", newline="\n")
            print(name, "added", len(add))
        else:
            print(name, "ok")


if __name__ == "__main__":
    main()
