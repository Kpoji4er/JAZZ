# -*- coding: utf-8 -*-
"""Patch HaveABlast description in English.csv / Russian.csv without rewriting whole files."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RU_DESC = (
    "Переключатель. Пока активен: после атаки по себе (попадание или промах) "
    "отвечает гранатой (руки или из инвентаря); урон от взрывов по себе −50%. Выключен — без эффекта."
)
EN_DESC = (
    "Toggle. While active: when attacked (hit or miss), retaliate with a grenade "
    "(hands or pulled from inventory); take 50% explosion damage. Off: no effect."
)
OLD_MARKER = "отвечает гранатой из рук"
ID_NAME = "890000000009873"
ID_DESC = "890000000009874"
CTX = "jazz:CharacterEffect/HaveABlast.lua"


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found_name = found_desc = False
    out = []
    for line in lines:
        if line.startswith(ID_NAME + ","):
            out.append(f"{ID_NAME},Взрывной характер,Have a Blast,,{CTX}\n")
            found_name = True
            continue
        if line.startswith(ID_DESC + ","):
            out.append(f"{ID_DESC},{csv_escape(RU_DESC)},{csv_escape(EN_DESC)},,{CTX}\n")
            found_desc = True
            continue
        out.append(line)
    if not found_name:
        out.append(f"{ID_NAME},Взрывной характер,Have a Blast,,{CTX}\n")
    if not found_desc:
        out.append(f"{ID_DESC},{csv_escape(RU_DESC)},{csv_escape(EN_DESC)},,{CTX}\n")
    path.write_text("".join(out), encoding="utf-8", newline="")
    print(f"{path.name}: name={found_name} desc={found_desc} (appended missing if False)")


def main() -> None:
    for name in ("English.csv", "Russian.csv"):
        patch_file(ROOT / name)
    # sanity: old inventory wording gone from English
    en = (ROOT / "English.csv").read_text(encoding="utf-8")
    if OLD_MARKER in en and ID_DESC in en:
        # only fail if still on HaveABlast row
        for line in en.splitlines():
            if line.startswith(ID_DESC + ",") and OLD_MARKER in line:
                raise SystemExit("English still has inventory wording on HaveABlast")
    print("OK")


if __name__ == "__main__":
    main()
