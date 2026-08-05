"""Patch ErnieCounterAttack heavies: 1 Rocketeer + 2 AssaultT1_Grenadier + 1 Mortarman."""
from __future__ import annotations

import re
from pathlib import Path

MODS = Path(__file__).resolve().parents[3]
UNITS_ITEMS = MODS / "jazz-units" / "items.lua"


def main() -> None:
    text = UNITS_ITEMS.read_text(encoding="utf-8")
    marker = 'id = "ErnieCounterAttack"'
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit("ErnieCounterAttack not found")

    start = text.rfind("-- Quest Ernie_CounterAttack", 0, idx)
    if start < 0:
        raise SystemExit("quest comment not found")
    end = text.find("}),", idx) + 3
    old = text[start:end]
    new = old

    new = re.sub(
        r"-- Quest Ernie_CounterAttack[^\n]*\n\t\t\t-- Dedicated def:[^\n]*\n",
        "-- Quest Ernie_CounterAttack / custom_quest_id ErnieCounterAttack.\n"
        "\t\t\t-- Dedicated def: size ~37; 1 rocketeer + 2 T1 thrower grenadiers + 1 mortar. "
        "Does NOT change Global AI retribution recipes.\n",
        new,
        count=1,
    )
    new = re.sub(
        r'Comment = "Ernie_CounterAttack quest punitive[^"]*"',
        'Comment = "Ernie_CounterAttack quest punitive (I7->I5); 1 RPG + 2 AssaultT1_Grenadier + 1 mortar"',
        new,
        count=1,
    )

    if "JAZZ_Legion_HeavyT2_Grenadier" in new:
        new = new.replace(
            "'unitType', \"JAZZ_Legion_HeavyT2_Grenadier\"",
            "'unitType', \"JAZZ_Legion_AssaultT1_Grenadier\"",
            1,
        )

    m = re.search(
        r"('unitType', \"JAZZ_Legion_HeavyT1_Rocketeer\",\s*\}\),\s*\},\s*"
        r"'UnitCountMin', )(\d+)(,\s*'UnitCountMax', )(\d+)",
        new,
        re.S,
    )
    if not m:
        raise SystemExit("rocketeer count lines not found")
    new = new[: m.start()] + m.group(1) + "1" + m.group(3) + "1" + new[m.end() :]

    if "HeavyT2_Grenadier" in new:
        raise SystemExit("HeavyT2_Grenadier still present")
    if "JAZZ_Legion_AssaultT1_Grenadier" not in new:
        raise SystemExit("AssaultT1_Grenadier missing")
    if "JAZZ_Legion_HeavyT1_Rocketeer" not in new:
        raise SystemExit("Rocketeer missing")
    if "JAZZ_Legion_HeavyT3_Mortarman" not in new:
        raise SystemExit("Mortarman missing")

    for label, pat in (
        ("Rocketeer", r"HeavyT1_Rocketeer.*?UnitCountMin', (\d+).*?UnitCountMax', (\d+)"),
        ("AssaultT1_Grenadier", r"AssaultT1_Grenadier.*?UnitCountMin', (\d+).*?UnitCountMax', (\d+)"),
        ("Mortarman", r"HeavyT3_Mortarman.*?UnitCountMin', (\d+).*?UnitCountMax', (\d+)"),
    ):
        mm = re.search(pat, new, re.S)
        print(f"{label}: {mm.group(1)}-{mm.group(2)}" if mm else f"{label}: MISSING")

    # Full composition tally
    counts = {}
    for um in re.finditer(
        r"'unitType', \"([^\"]+)\",\s*\}\),\s*\},\s*'UnitCountMin', (\d+),\s*'UnitCountMax', (\d+)",
        new,
        re.S,
    ):
        ut, mn, mx = um.group(1), int(um.group(2)), int(um.group(3))
        counts[ut] = counts.get(ut, 0) + mn
        if mn != mx:
            print(f"WARN range {ut}: {mn}-{mx}")
    print("composition:", counts)
    print("total:", sum(counts.values()))

    UNITS_ITEMS.write_text(text[:start] + new + text[end:], encoding="utf-8")
    print(f"patched {UNITS_ITEMS}")


if __name__ == "__main__":
    main()
