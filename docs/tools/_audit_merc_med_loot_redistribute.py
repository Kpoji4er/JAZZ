# -*- coding: utf-8 -*-
"""Audit merc hire medicine loot vs MED-003 redistribute rules."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Reuse planner
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _apply_merc_med_loot_redistribute import (  # noqa: E402
    MED_ITEMS,
    extract_loot_blocks,
    iter_loot_entry_spans,
    load_mercs,
    pick_equipment_owner,
    plan_merc,
    resolve_leaves,
    UNITS_ITEMS,
)
from collections import defaultdict


def entries_in_block(block: str) -> dict[str, list[int]]:
    found: dict[str, list[int]] = {k: [] for k in MED_ITEMS}
    for _, _, inner in iter_loot_entry_spans(block):
        im = re.search(r'item\s*=\s*"([^"]+)"', inner)
        if not im or im.group(1) not in MED_ITEMS:
            continue
        item = im.group(1)
        sm = re.search(r"stack_min\s*=\s*(\d+)", inner)
        stack = int(sm.group(1)) if sm else 1
        found[item].append(stack)
    return found


def main() -> int:
    mercs = load_mercs()
    text = UNITS_ITEMS.read_text(encoding="utf-8")
    loots = extract_loot_blocks(text)
    fails: list[str] = []
    checked = 0
    by_eq: dict[str, list] = defaultdict(list)
    for merc in mercs:
        if merc.equipment:
            by_eq[merc.equipment].append(merc)
    for eq, owners in by_eq.items():
        merc = pick_equipment_owner(owners)
        if merc is None:
            continue
        leaves = resolve_leaves(eq, loots)
        plans = plan_merc(merc, leaves)
        for lid, plan in plans.items():
            if lid not in loots:
                fails.append(f"{lid}: missing loot def")
                continue
            checked += 1
            _, _, block = loots[lid]
            got = entries_in_block(block)
            # med<20: no kits, no morphine
            if merc.medical < 20:
                for kit in ("FirstAidKit", "Medkit", "Reanimationsset"):
                    if got[kit]:
                        fails.append(f"{lid}: med<20 has {kit}")
                if got["JAZZ_Morphine"]:
                    fails.append(f"{lid}: med<20 has Morphine")
            # bandage present if planned
            if plan.bandage > 0:
                if sum(got["JAZZ_Bandage"]) != plan.bandage:
                    fails.append(
                        f"{lid}: bandage {sum(got['JAZZ_Bandage'])} != plan {plan.bandage}"
                    )
            elif got["JAZZ_Bandage"]:
                fails.append(f"{lid}: unexpected bandage")
            if plan.morphine > 0:
                if sum(got["JAZZ_Morphine"]) != plan.morphine:
                    fails.append(
                        f"{lid}: morphine {sum(got['JAZZ_Morphine'])} != plan {plan.morphine}"
                    )
            elif got["JAZZ_Morphine"]:
                fails.append(f"{lid}: unexpected morphine")
            if plan.kit:
                kits_present = [k for k in ("FirstAidKit", "Medkit", "Reanimationsset") if got[k]]
                if kits_present != [plan.kit]:
                    fails.append(f"{lid}: kits {kits_present} != [{plan.kit}]")
            else:
                for kit in ("FirstAidKit", "Medkit", "Reanimationsset"):
                    if got[kit]:
                        fails.append(f"{lid}: unexpected {kit}")
            if merc.is_ame:
                for kit in ("Medkit", "Reanimationsset"):
                    if got[kit]:
                        fails.append(f"{lid}: AME has non-small {kit}")

    if fails:
        print(f"FAIL checked={checked} fails={len(fails)}")
        for f in fails[:40]:
            print(" -", f)
        return 1
    print(f"OK merc med loot redistribute audit (leaves={checked})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
