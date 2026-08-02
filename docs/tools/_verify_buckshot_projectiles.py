#!/usr/bin/env python3
"""Static AC checks for JAZZ-WEAPONS-006. Exit 1 on FAIL."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
fails: list[str] = []


def main() -> int:
    # AC-001 companions
    for path in (ROOT / "InventoryItem").rglob("*.lua"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if 'object_class = "Shotgun"' not in text:
            continue
        bp = re.search(r"BuckshotProjectiles = (\d+)", text)
        auto = re.search(r"AutoShots = (\d+)", text)
        if not bp or int(bp.group(1)) < 1:
            fails.append(f"AC-001 {path.name}: BuckshotProjectiles missing/0")
        if auto and int(auto.group(1)) != 0:
            # allow only if AutoFire in AvailableAttacks
            if "AutoFire" not in text:
                fails.append(f"AC-001 {path.name}: AutoShots={auto.group(1)} without AutoFire")

    # AC-002 wiring
    orw = (ROOT / "Code/System_OR_Weapons.lua").read_text(encoding="utf-8", errors="replace")
    if "num_shots = self.BuckshotProjectiles" not in orw:
        fails.append("AC-002 GetAttackResults missing BuckshotProjectiles")
    if re.search(r"IsKindOf\(self,\s*\"Shotgun\"\).*AutoShots", orw, re.S):
        # crude: shotgun block should not assign AutoShots
        chunk = orw[orw.find("IsKindOf(self, \"Shotgun\")") : orw.find("IsKindOf(self, \"Shotgun\")") + 200]
        if "AutoShots" in chunk:
            fails.append("AC-002 Shotgun block still uses AutoShots")

    items = (ROOT / "items.lua").read_text(encoding="utf-8", errors="replace")
    if 'target_prop = "AutoShots"' in items and "12gauge" in items[
        max(0, items.find('target_prop = "AutoShots"') - 200) : items.find('target_prop = "AutoShots"') + 50
    ]:
        # any remaining AutoShots target_prop on 12g
        for m in re.finditer(r'target_prop = "AutoShots"', items):
            ctx = items[max(0, m.start() - 400) : m.start()]
            if "12gauge" in ctx or "12g" in ctx:
                fails.append("AC-002 items.lua still has 12g AutoShots mod")
                break
    if "weapon.BuckshotProjectiles" not in items:
        fails.append("AC-002 CombatAction missing BuckshotProjectiles")

    for path in (ROOT / "InventoryItem").rglob("*12gauge*.lua"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if 'target_prop = "AutoShots"' in text:
            fails.append(f"AC-002 ammo {path.name} still AutoShots")

    # AC-003 rebalance
    rb = (ROOT / "docs/tools/_rebalance_recoil_physical.py").read_text(encoding="utf-8", errors="replace")
    if 'if "shotgun" in cls:\n        burst = 1\n        auto = 1' in rb:
        fails.append("AC-003 rebalance still forces shotgun AutoShots=1")

    # AC-006 equal pellet CTH (no recoil queue)
    if "pellet_pack" not in orw:
        fails.append("AC-006 missing pellet_pack gate")
    if "pellet_pack and 1 or i" not in orw and "pellet_pack and 1" not in orw:
        fails.append("AC-006 missing bullet_index=1 for pellet pack")
    if 'action.id == "Buckshot" and shot_cth > 90 and i > 1' in orw:
        fails.append("AC-006 legacy Buckshot i>1 CTH cap still present")

    with (ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if (row.get("object_class") or "").lower() != "shotgun":
                continue
            if row.get("buckshot_projectiles") != "1":
                fails.append(f"AC-001 csv {row['id']} buckshot_projectiles={row.get('buckshot_projectiles')}")
            if row.get("auto_shots") != "0":
                fails.append(f"AC-001 csv {row['id']} auto_shots={row.get('auto_shots')}")

    if fails:
        print("FAIL")
        for f in fails:
            print(" ", f)
        return 1
    print("PASS WEAPONS-006 static AC-001..003, AC-006")
    return 0


if __name__ == "__main__":
    sys.exit(main())
