# Sync StartingSalary from UnitData companions into jazz-units/items.lua for AME.
from __future__ import annotations

import re
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\UnitData")
ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")


def main():
    new_map = {}
    for p in sorted(UNITS.glob("JAZZ_AME_*.lua")):
        m = re.search(r"StartingSalary\s*=\s*(\d+)", p.read_text(encoding="utf-8"))
        if not m:
            raise SystemExit(f"no salary in {p}")
        new_map[p.stem] = int(m.group(1))

    items = ITEMS.read_text(encoding="utf-8")
    changed = 0
    for uid, sal in sorted(new_map.items()):
        pattern = re.compile(
            rf"('Id',\s*\"{uid}\")([\s\S]{{0,5000}}?)('StartingSalary',\s*)\d+",
            re.M,
        )

        def sub(m, sal=sal):
            nonlocal changed
            changed += 1
            return f"{m.group(1)}{m.group(2)}{m.group(3)}{sal}"

        items, c = pattern.subn(sub, items, count=1)
        if c != 1:
            print("WARN", uid, "replacements", c)

    ITEMS.write_text(items, encoding="utf-8", newline="\n")
    print("updated", changed, "of", len(new_map))
    sals = list(new_map.values())
    print("daily min/med/max", min(sals), sorted(sals)[len(sals) // 2], max(sals))
    print("weekly min/med/max", min(sals) * 7, sorted(sals)[len(sals) // 2] * 7, max(sals) * 7)


if __name__ == "__main__":
    main()
