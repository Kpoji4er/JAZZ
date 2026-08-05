#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit MachineGunEmplacement blocks in jazz-maps for weapon/ammo IDs."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2].parent / "jazz-maps" / "Maps"


def main() -> None:
    count = 0
    weapon_classes: Counter[str] = Counter()
    ammo_classes: Counter[str] = Counter()
    calibers: Counter[str] = Counter()
    samples: list[tuple[str, str]] = []
    no_weapon = 0
    maps_with = []

    for p in sorted(ROOT.rglob("objects.lua")):
        text = p.read_text(encoding="utf-8", errors="replace")
        if "MachineGunEmplacement" not in text:
            continue
        map_id = p.parent.name
        maps_with.append(map_id)
        for m in re.finditer(
            r"PlaceObj\('MachineGunEmplacement',\s*\{(.*?)\n\}\)",
            text,
            re.S,
        ):
            block = m.group(1)
            count += 1
            # Nested PlaceObj class names near Inventory
            nested = re.findall(r"PlaceObj\('([A-Za-z0-9_]+)'", block)
            weapons = [
                c
                for c in nested
                if c
                not in (
                    "WeaponComponent",
                    "WeaponComponentVisual",
                    "PropertyDef",
                )
                and (
                    "MG" in c
                    or "Gun" in c
                    or "Browning" in c
                    or c.endswith("HMG")
                    or "Machine" in c
                    or c.startswith("JAZZ_AMMO")
                    or c.startswith("_50")
                    or "Ammo" in c
                    or c.startswith("Mag")
                )
            ]
            # Better: find Inventory section items
            inv_m = re.search(r"Inventory\s*=\s*\{(.*)\}\s*,?\s*$", block, re.S | re.M)
            # fall back: look for BrowningM2HMG / ammo PlaceObj at top level of inventory
            w_match = re.search(
                r"PlaceObj\('(BrowningM2HMG|HK21|MG42|M60|FNMAG|PKM|AA52|RPK[^']*|MachineGun[^']*)'",
                block,
            )
            a_match = re.search(
                r"PlaceObj\('((?:JAZZ_)?AMMO_[^']+|_50BMG[^']*|_50[^']*|Ammo[^']*)'",
                block,
            )
            cal_match = re.search(r"Caliber\s*=\s*\"([^\"]+)\"", block)
            if w_match:
                weapon_classes[w_match.group(1)] += 1
            else:
                no_weapon += 1
                # dump nested for first few
                if len(samples) < 5:
                    head = "\n".join(block.splitlines()[:60])
                    samples.append((map_id + " NO_WEAPON", head))
            if a_match:
                ammo_classes[a_match.group(1)] += 1
            if cal_match:
                calibers[cal_match.group(1)] += 1
            if w_match and len(samples) < 3:
                head = "\n".join(block.splitlines()[:70])
                samples.append((map_id, head))

    print(f"maps={len(maps_with)} emplacements={count} no_weapon_match={no_weapon}")
    print("weapon_classes:", dict(weapon_classes))
    print("ammo_classes:", dict(ammo_classes))
    print("calibers:", dict(calibers))
    for name, s in samples:
        print("=" * 20, name, "=" * 20)
        print(s)
        print("...")


if __name__ == "__main__":
    main()
