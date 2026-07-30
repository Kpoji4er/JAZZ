#!/usr/bin/env python3
"""Static AC checks for JAZZ-UNITS-003 (no game required)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"
ITEMS = UNITS / "items.lua"
RECIPES = Path(__file__).resolve().parent / "data" / "recipes.json"

fails: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print("FAIL:", msg)


def ok(msg: str) -> None:
    print("PASS:", msg)


def block_for(text: str, loot_id: str) -> str:
    i = text.find(f'id = "{loot_id}"')
    if i < 0:
        raise KeyError(loot_id)
    start = text.rfind("PlaceObj('ModItemLootDef'", 0, i)
    brace = text.find("{", start)
    depth = 0
    j = brace
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[start : j + 1]
        j += 1
    raise RuntimeError(loot_id)


def main() -> int:
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    text = ITEMS.read_text(encoding="utf-8")

    # AC-001 / AC-005
    if len(recipes) != 37:
        fail(f"recipes count {len(recipes)} != 37")
    else:
        ok("AC-005 recipes=37")
    if "JAZZ_Legion_Recruit" in recipes:
        fail("Recruit must not have combat recipe")
    else:
        ok("AC-005 Recruit excluded")

    if text.count("JAZZ-UNITS-003-GENERATED-BEGIN") != 1 or text.count("JAZZ-UNITS-003-GENERATED-END") != 1:
        fail("generated markers missing/duplicated")
    else:
        ok("AC-001 markers present")

    gen = text[text.find("JAZZ-UNITS-003-GENERATED-BEGIN") : text.find("JAZZ-UNITS-003-GENERATED-END")]
    if "DiamondBriefcase" in gen:
        fail("AC-006 DiamondBriefcase in generated region")
    else:
        ok("AC-006 no DiamondBriefcase in generated region")

    for pool in (
        "JAZZ_Gen_NightEquipment",
        "JAZZ_Gen_Sidearm",
        "JAZZ_Gen_FlareGun",
        "JAZZ_Gen_MiscGear",
        "JAZZ_Gen_Valuables_Low",
    ):
        if f'id = "{pool}"' not in text:
            fail(f"missing shared pool {pool}")
    else:
        ok("AC-001 shared pools present")

    # AC-002 pilots
    pilots = {
        "Roughneck_Inventory": {
            "firearm": "Roughneck_Firearm",
            "night": True,
            "valuables": True,
            "frag_chance": True,
            "armor": "LightArmor",
        },
        "Shocktrooper_Inventory": {
            "firearm": "Shocktrooper_Firearm",
            "night": True,
            "valuables": True,
            "frag_guaranteed": True,
            "armor": "MiddleArmor",
        },
        "Sniper_Inventory": {
            "firearm": "Sniper_Firearm",
            "night": True,
            "valuables": True,
            "frag_chance": True,
            "armor": "LightArmor",
        },
    }
    for inv, expect in pilots.items():
        b = block_for(text, inv)
        if "JAZZ-UNITS-003 generated" not in b:
            fail(f"{inv} missing generated comment")
        if expect["firearm"] not in b:
            fail(f"{inv} missing firearm link")
        if expect.get("night") and "JAZZ_Gen_NightEquipment" not in b:
            fail(f"{inv} missing night")
        if expect.get("valuables") and "JAZZ_Gen_Valuables_" not in b:
            fail(f"{inv} missing valuables")
        if expect.get("armor") and expect["armor"] not in b:
            fail(f"{inv} missing armor {expect['armor']}")
        if expect.get("frag_guaranteed"):
            # FragGrenade without generate_chance in same entry — check contexts
            idx = 0
            found = 0
            while True:
                p = b.find("FragGrenade", idx)
                if p < 0:
                    break
                ctx = b[max(0, p - 200) : p + 80]
                if "generate_chance" not in ctx:
                    found += 1
                idx = p + 1
            if found < 3:
                fail(f"{inv} expected 3 guaranteed Frag bands, got {found}")
        if expect.get("frag_chance"):
            if "FragGrenade" not in b:
                fail(f"{inv} missing FragGrenade chance entries")
    ok("AC-002 pilot inventories structure")

    # Roughneck: no early assault/carbine-ish combos
    rf = block_for(text, "Roughneck_Firearm")
    early_assault = 0
    idx = 0
    while True:
        p = rf.find("PlaceObj('LootEntryLootDef'", idx)
        if p < 0:
            break
        br = rf.find("{", p)
        depth = 0
        j = br
        while j < len(rf):
            if rf[j] == "{":
                depth += 1
            elif rf[j] == "}":
                depth -= 1
                if depth == 0:
                    body = rf[br : j + 1]
                    amounts = [int(x) for x in re.findall(r"Amount = (\d+)", body)]
                    loot = re.search(r'loot_def = "([^"]+)"', body)
                    if amounts and loot and amounts[0] < 31:
                        name = loot.group(1)
                        if any(k in name for k in ("_AK", "M16", "M4A", "CAR15", "STG44", "FAMAS", "Galil", "FNFAL")):
                            early_assault += 1
                    break
            j += 1
        idx = p + 1
    if early_assault:
        fail(f"AC-002/008 static: Roughneck early assault-ish refs={early_assault}")
    else:
        ok("AC-002 Roughneck no mid carbine/AR norm")

    # AC-004 Roughneck remnant ~1%
    entries = []
    idx = 0
    while True:
        p = rf.find("PlaceObj('LootEntryLootDef'", idx)
        if p < 0:
            break
        br = rf.find("{", p)
        depth = 0
        j = br
        while j < len(rf):
            if rf[j] == "{":
                depth += 1
            elif rf[j] == "}":
                depth -= 1
                if depth == 0:
                    body = rf[br : j + 1]
                    amounts = [int(x) for x in re.findall(r"Amount = (\d+)", body)]
                    w = re.search(r"weight = (\d+)", body)
                    has_le = 'Condition = "<="' in body
                    if w and amounts:
                        entries.append((amounts, int(w.group(1)), has_le))
                    break
            j += 1
        idx = p + 1

    open_early = sum(1 for amounts, w, has_le in entries if amounts[0] < 30 and not has_le)
    if open_early:
        fail(f"AC-004 open-ended early firearm entries={open_early}")
    else:
        ok("AC-004 no open-ended early firearm entries on Roughneck")

    active25 = []
    for amounts, w, has_le in entries:
        lo = amounts[0]
        hi = amounts[1] if has_le and len(amounts) > 1 else None
        if lo > 25:
            continue
        if hi is not None and hi < 25:
            continue
        active25.append(w)
    tot = sum(active25)
    rem = sum(w for w in active25 if w == 1400)
    pct = (100.0 * rem / tot) if tot else 0.0
    if not (0.5 <= pct <= 1.5):
        fail(f"AC-004 remnant pct {pct:.3f} outside 0.5–1.5 (tot={tot} rem={rem})")
    else:
        ok(f"AC-004 remnant pct={pct:.3f}% (tol ±0.5 around 1%)")

    # AC-005 all inventory/firearm ids exist and marked generated
    missing = []
    unmarked = []
    for uid, r in recipes.items():
        for key in ("inventory", "firearm"):
            lid = r[key]
            if f'id = "{lid}"' not in text:
                missing.append((uid, lid))
            else:
                try:
                    b = block_for(text, lid)
                    if "JAZZ-UNITS-003 generated" not in b:
                        unmarked.append(lid)
                except Exception as e:
                    missing.append((uid, f"{lid}:{e}"))
        if r.get("keep_existing_heavy"):
            la = r["inventory"].replace("_Inventory", "_Launcher")
            if f'id = "{la}"' not in text:
                missing.append((uid, la))
    if missing:
        fail(f"AC-005 missing loot ids: {missing[:5]}")
    else:
        ok("AC-005 all recipe loot ids present")
    if unmarked:
        fail(f"AC-005 unmarked generated blocks: {unmarked[:5]}")
    else:
        ok("AC-005 all class blocks marked generated")

    # metadata resources
    meta = (UNITS / "metadata.lua").read_text(encoding="utf-8")
    needed = set(re.findall(r'id = "(JAZZ_Gen[^"]+)"', text))
    have = set(re.findall(r"'Id',\s*\"(JAZZ_Gen[^\"]+)\"", meta))
    miss_meta = sorted(needed - have)
    if miss_meta:
        fail(f"AC-007 metadata missing {len(miss_meta)} JAZZ_Gen* e.g. {miss_meta[:3]}")
    else:
        ok(f"AC-007 metadata has all {len(needed)} JAZZ_Gen* resources")

    print("---")
    if fails:
        print(f"RESULT: FAILED ({len(fails)} issues)")
        return 1
    print("RESULT: PASSED (static AC suite)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
