"""Set paid hire salaries for Jazz mercs that still have StartingSalary=0 (Grom, Hitman)."""
from __future__ import annotations

import re
from pathlib import Path

UNITS_ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
UNITDATA = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\UnitData")

# id -> (StartingSalary, SalaryIncrease, SalaryLv1, SalaryMaxLv)
SALARIES = {
    "Jazz_Grom": (2500, 200, 1000, 6000),
    "Jazz_Hitman": (1500, 150, 600, 3000),
}


def patch_companion(unit_id: str, start: int, increase: int, lv1: int, max_lv: int) -> None:
    path = UNITDATA / f"{unit_id}.lua"
    text = path.read_text(encoding="utf-8")
    new = text
    new = re.sub(r"StartingSalary\s*=\s*\d+", f"StartingSalary = {start}", new, count=1)
    new = re.sub(r"SalaryIncrease\s*=\s*\d+", f"SalaryIncrease = {increase}", new, count=1)
    new = re.sub(r"SalaryLv1\s*=\s*\d+", f"SalaryLv1 = {lv1}", new, count=1)
    new = re.sub(r"SalaryMaxLv\s*=\s*\d+", f"SalaryMaxLv = {max_lv}", new, count=1)
    if new == text:
        raise SystemExit(f"no salary fields changed in {path.name}")
    path.write_text(new, encoding="utf-8")
    print(f"companion {unit_id}: {start}/{lv1}/{max_lv}")


def patch_items(unit_id: str, start: int, increase: int, lv1: int, max_lv: int) -> None:
    text = UNITS_ITEMS.read_text(encoding="utf-8")
    m = re.search(
        rf"(['\"]name['\"],\s*['\"]{re.escape(unit_id)}['\"].{{0,12000}}?)'StartingSalary',\s*\d+,",
        text,
        re.S,
    )
    if not m:
        m = re.search(
            rf"(Id',\s*['\"]{re.escape(unit_id)}['\"].{{0,12000}}?)'StartingSalary',\s*\d+,",
            text,
            re.S,
        )
    if not m:
        raise SystemExit(f"{unit_id} StartingSalary not found in items.lua")
    start_i = m.start(1)
    end_i = start_i + 12000
    chunk = text[start_i:end_i]
    chunk2 = re.sub(r"'StartingSalary',\s*\d+,", f"'StartingSalary', {start},", chunk, count=1)
    chunk2 = re.sub(r"'SalaryIncrease',\s*\d+,", f"'SalaryIncrease', {increase},", chunk2, count=1)
    chunk2 = re.sub(r"'SalaryLv1',\s*\d+,", f"'SalaryLv1', {lv1},", chunk2, count=1)
    chunk2 = re.sub(r"'SalaryMaxLv',\s*\d+,", f"'SalaryMaxLv', {max_lv},", chunk2, count=1)
    if chunk2 == chunk:
        raise SystemExit(f"no salary fields replaced for {unit_id} in items.lua")
    UNITS_ITEMS.write_text(text[:start_i] + chunk2 + text[end_i:], encoding="utf-8")
    print(f"items.lua {unit_id}: {start}/{lv1}/{max_lv}")


def main() -> None:
    for unit_id, vals in SALARIES.items():
        patch_companion(unit_id, *vals)
        patch_items(unit_id, *vals)


if __name__ == "__main__":
    main()
