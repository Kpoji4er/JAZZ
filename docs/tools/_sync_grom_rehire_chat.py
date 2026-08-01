"""Sync Grom RehireIntro chat (no longer 'free') into items.lua + CSVs."""
from __future__ import annotations

import re
from pathlib import Path

OLD = "Контракт заканчивается. Я всё равно бесплатный — продолжаем службу?"
NEW = "Контракт заканчивается. Продлеваем службу, или мне искать другой аэродром?"
EN = "Contract's ending. Extending service, or should I find another airfield?"
LID = "890000000002417"

PATHS = [
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua"),
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\Russian.csv"),
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\English.csv"),
]


def main() -> None:
    for p in PATHS:
        text = p.read_text(encoding="utf-8")
        if OLD not in text and LID not in text:
            print(f"skip {p.name}")
            continue
        text = text.replace(OLD, NEW)
        if p.name == "English.csv":

            def sub(m: re.Match[str]) -> str:
                ru = m.group(2)
                rest = m.group(4)
                en_q = '"' + EN.replace('"', '""') + '"'
                return f"{m.group(1)},{ru},{en_q},{rest}"

            text, n = re.subn(
                rf'^({LID}),("(?:[^"]|"")*"|[^,]*),("(?:[^"]|"")*"|[^,]*),(.*)$',
                sub,
                text,
                flags=re.M,
            )
            print(f"English.csv EN rows: {n}")
        p.write_text(text, encoding="utf-8")
        print(f"OK {p.name}")


if __name__ == "__main__":
    main()
