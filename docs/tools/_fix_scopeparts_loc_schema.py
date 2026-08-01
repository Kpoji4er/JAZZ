# -*- coding: utf-8 -*-
"""Rewrite ScopeParts loc rows into full Russian.csv / English.csv schema."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# id -> (en_text, ru_text, context)
ROWS = {
    990002500: ("Scope Parts", "Детали прицелов", "jazz:InventoryItem/JAZZ_ScopeParts.lua"),
    990002501: ("Scope Parts", "Детали прицелов", "jazz:InventoryItem/JAZZ_ScopeParts.lua"),
    990002502: (
        "Used when repairing a firearm that has a scope installed. Also salvaged when a scope breaks on a failed removal.",
        "Нужны при ремонте оружия с установленным прицелом. Также получаются при поломке прицела при неудачном снятии.",
        "jazz:InventoryItem/JAZZ_ScopeParts.lua",
    ),
    990002503: (
        "Removal failed. Attachment broken.",
        "Снятие провалилось. Модуль сломан.",
        "jazz:Code/System_WeaponRemovableModify.lua",
    ),
    990002504: (
        "Removal failed. Weapon resource max reduced.",
        "Снятие провалилось. Ресурс оружия снижен.",
        "jazz:Code/System_WeaponRemovableModify.lua",
    ),
    990002505: (
        "Attachment broken on removal.",
        "Модуль сломан при снятии.",
        "jazz:Code/System_WeaponResourceMaintenance.lua",
    ),
}


def esc(val: str) -> str:
    if any(c in val for c in ',"\n'):
        return '"' + val.replace('"', '""') + '"'
    return val


def rewrite(path: Path, lang: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    seen = set()
    for line in lines:
        if line and line[0].isdigit():
            tid = line.split(",", 1)[0]
            if tid.isdigit() and int(tid) in ROWS:
                seen.add(int(tid))
                continue
        out.append(line)
    for tid, (en, ru, ctx) in ROWS.items():
        if lang == "ru":
            out.append(f"{tid},{esc(en)},{esc(ru)},,{ctx}")
        else:
            out.append(f"{tid},{esc(en)},,,{ctx}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(path.name, "rewrote", len(ROWS))


def main() -> None:
    rewrite(ROOT / "Russian.csv", "ru")
    rewrite(ROOT / "English.csv", "en")


if __name__ == "__main__":
    main()
