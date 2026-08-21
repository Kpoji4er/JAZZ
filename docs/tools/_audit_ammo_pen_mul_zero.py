"""Flag CaliberModification PenetrationBonus with mod_mul=0 (zeros add in MulDivRound).

Saltshot-style mod_mul=0 on PenetrationClass is valid. Bonus with a non-zero
mod_add must use default mul 1000 (omit the field).

  python docs/tools/_audit_ammo_pen_mul_zero.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AMMO_DIR = ROOT / "InventoryItem"

PLACEOBJ = re.compile(
    r"PlaceObj\(\s*'CaliberModification'\s*,\s*\{(.*?)\}\s*\)",
    re.S,
)


def mods_in(text: str) -> list[dict[str, str]]:
    out = []
    for body in PLACEOBJ.findall(text):
        fields = {}
        for key in ("target_prop", "mod_mul", "mod_add"):
            m = re.search(rf"{key}\s*=\s*([^\n,]+)", body)
            if m:
                fields[key] = m.group(1).strip().strip("'\"")
        if fields:
            out.append(fields)
    return out


def main() -> int:
    errors: list[str] = []
    for path in sorted(AMMO_DIR.glob("JAZZ_AMMO_*.lua")):
        text = path.read_text(encoding="utf-8")
        for fields in mods_in(text):
            if fields.get("target_prop") != "PenetrationBonus":
                continue
            if fields.get("mod_mul") != "0":
                continue
            add = fields.get("mod_add", "0")
            errors.append(f"{path.name}: PenetrationBonus mod_mul=0 (mod_add={add})")
    if errors:
        print("FAIL: bonus mul=0 zeros CaliberModification add")
        for line in errors:
            print(" ", line)
        return 1
    print("OK: no PenetrationBonus mod_mul=0 on JAZZ_AMMO_*")
    return 0


if __name__ == "__main__":
    sys.exit(main())
