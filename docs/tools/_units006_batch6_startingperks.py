# -*- coding: utf-8 -*-
"""Wire Jazz_Perk_Benny / Jazz_Perk_Simon into jazz-units StartingPerks."""
from __future__ import annotations

from pathlib import Path

UNITS = Path(__file__).resolve().parents[3] / "jazz-units"
if not UNITS.exists():
    UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")

UPDATES = {
    "Jazz_Benny": "Jazz_Perk_Benny",
    "Jazz_Simon": "Jazz_Perk_Simon",
}


def patch_companion(unit_id: str, perk: str) -> None:
    path = UNITS / "UnitData" / f"{unit_id}.lua"
    text = path.read_text(encoding="utf-8")
    if perk in text:
        print("companion already", unit_id)
        return
    old = "\tStartingPerks = {\n"
    new = f'\tStartingPerks = {{\n\t\t"{perk}",\n'
    if old not in text:
        raise SystemExit(f"StartingPerks missing in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print("companion", unit_id)


def patch_items(unit_id: str, perk: str) -> None:
    path = UNITS / "items.lua"
    text = path.read_text(encoding="utf-8")
    needle = f"'Id', \"{unit_id}\""
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit(f"ModItem {unit_id} missing")
    # Prefer UnitDataCompositeDef StartingPerks after this Id
    sp = text.find("'StartingPerks'", idx)
    if sp < 0 or sp - idx > 5000:
        raise SystemExit(f"StartingPerks not near {unit_id}")
    block_end = text.find("},", sp)
    chunk = text[sp:block_end]
    if perk in chunk:
        print("items already", unit_id)
        return
    insert_at = text.find("{", sp) + 1
    text = text[:insert_at] + f'\n\t\t\t\t\t\t"{perk}",' + text[insert_at:]
    path.write_text(text, encoding="utf-8", newline="\n")
    print("items", unit_id)


def main() -> None:
    for unit_id, perk in UPDATES.items():
        patch_companion(unit_id, perk)
        patch_items(unit_id, perk)
    print("OK jazz-units StartingPerks")


if __name__ == "__main__":
    main()
