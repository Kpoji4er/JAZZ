"""Set Jazz_Madman hire salary in jazz-units/items.lua (companion already patched)."""
from __future__ import annotations

import re
from pathlib import Path

ITEMS = Path(__file__).resolve().parents[3].parent / "jazz-units" / "items.lua"
# parents: tools -> docs -> jazz; sibling jazz-units
ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    m = re.search(r"(['\"]name['\"],\s*['\"]Jazz_Madman['\"].{0,12000}?)'StartingSalary',\s*0,", text, re.S)
    if not m:
        m = re.search(r"(Id',\s*['\"]Jazz_Madman['\"].{0,12000}?)'StartingSalary',\s*0,", text, re.S)
    if not m:
        raise SystemExit("Madman StartingSalary=0 not found in items.lua")

    start = m.start(1)
    end = start + 12000
    chunk = text[start:end]
    chunk2 = chunk.replace("'StartingSalary', 0,", "'StartingSalary', 900,", 1)
    chunk2 = chunk2.replace("'SalaryLv1', 0,", "'SalaryLv1', 400,", 1)
    chunk2 = chunk2.replace("'SalaryMaxLv', 500,", "'SalaryMaxLv', 2500,", 1)
    if chunk2 == chunk:
        raise SystemExit("no salary fields replaced in Madman chunk")
    ITEMS.write_text(text[:start] + chunk2 + text[end:], encoding="utf-8")
    print("OK: Jazz_Madman salary -> 900 / lv1 400 / max 2500")


if __name__ == "__main__":
    main()
