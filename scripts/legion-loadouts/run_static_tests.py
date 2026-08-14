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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate import parse_prices, valuables_tiny_stack  # noqa: E402

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


def placeobj_blocks(text: str, class_name: str) -> list[str]:
    """Return balanced blocks for a specific nested PlaceObj class."""
    needle = f"PlaceObj('{class_name}'"
    blocks: list[str] = []
    pos = 0
    while True:
        start = text.find(needle, pos)
        if start < 0:
            return blocks
        brace = text.find("{", start)
        if brace < 0:
            raise RuntimeError(f"{class_name}: missing opening brace")
        depth = 0
        end = brace
        while end < len(text):
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
                if depth == 0:
                    blocks.append(text[start : end + 1])
                    pos = end + 1
                    break
            end += 1
        else:
            raise RuntimeError(f"{class_name}: unbalanced block")


def entries_with(entries: list[str], field: str, value: str) -> list[str]:
    return [entry for entry in entries if f'{field} = "{value}"' in entry]


def chance_values(entries: list[str]) -> list[int]:
    values: list[int] = []
    for entry in entries:
        match = re.search(r"generate_chance = (\d+)", entry)
        if match:
            values.append(int(match.group(1)))
    return values


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

    # Parse health: buggy replace_or_warn used to stack `}),),),),` and unbalance parens,
    # which prevents the whole items.lua chunk from loading (mercs + all loot).
    if "}),)," in text:
        fail("stacked PlaceObj closers `}),),` present (regen replace bug)")
    else:
        ok("AC-001 no stacked `}),),` closers")
    paren_delta = text.count("(") - text.count(")")
    brace_delta = text.count("{") - text.count("}")
    if paren_delta != 0 or brace_delta != 0:
        fail(f"items.lua delimiter imbalance paren={paren_delta} brace={brace_delta}")
    else:
        ok("AC-001 items.lua paren/brace balanced")

    gen = text[text.find("JAZZ-UNITS-003-GENERATED-BEGIN") : text.find("JAZZ-UNITS-003-GENERATED-END")]
    if "DiamondBriefcase" in gen:
        fail("AC-006 DiamondBriefcase in generated region")
    else:
        ok("AC-006 no DiamondBriefcase in generated region")

    # Weapon+ammo combos must not nest LegionT*_Shotgun (weapon pool) as "ammo"
    weapon_pool_as_ammo = re.findall(
        r'loot_def = "(LegionT[123]_Shotgun)"',
        gen,
    )
    if weapon_pool_as_ammo:
        fail(f"GenW combo uses weapon pool as ammo: {sorted(set(weapon_pool_as_ammo))}")
    else:
        ok("no LegionT*_Shotgun nested as ammo in GenW combos")

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

    night = block_for(text, "JAZZ_Gen_NightEquipment")
    if "IsTimeOfDay" in night:
        fail("JAZZ_Gen_NightEquipment must not gate CSE on IsTimeOfDay")
    elif 'item = "GlowStick"' not in night or 'item = "FlareStick"' not in night:
        fail("JAZZ_Gen_NightEquipment missing GlowStick/FlareStick")
    elif 'loot = "all"' not in night:
        fail("JAZZ_Gen_NightEquipment should be loot=all")
    else:
        ok("AC-001 night lights spawn always (no TOD gate)")

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
        if expect.get("valuables") and 'item = "TinyDiamonds"' not in b:
            fail(f"{inv} missing valuables TinyDiamonds")
        if expect.get("valuables") and "generate_chance = 30" not in b:
            fail(f"{inv} valuables drop_chance != 30")
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


    # HOTFIX-003: recipe -> generated inventory -> UnitData contract, all 37 classes.
    armor_defs = {
        "Light": ("LegionTorsoLightArmor", "LegionLegsLightArmor", "LegionHelmetsLightArmor"),
        "Middle": ("LegionTorsoMiddleArmor", "LegionLegsMiddleArmor", "LegionHelmetsMiddleArmor"),
        "Heavy": ("LegionTorsoHeavyArmor", "LegionLegsHeavyArmor", "LegionHelmetsHeavyArmor"),
    }
    contract_failures: list[str] = []

    def contract(condition: bool, message: str) -> None:
        if not condition:
            contract_failures.append(message)

    prices = parse_prices()
    for uid, recipe in recipes.items():
        inv_id = recipe["inventory"]
        firearm_id = recipe["firearm"]
        inv = block_for(text, inv_id)
        loot_entries = placeobj_blocks(inv, "LootEntryLootDef")
        item_entries = placeobj_blocks(inv, "LootEntryInventoryItem")

        unit_path = UNITS / "UnitData" / f"{uid}.lua"
        contract(unit_path.is_file(), f"{uid}: missing UnitData file")
        if unit_path.is_file():
            unit_text = unit_path.read_text(encoding="utf-8")
            equipment = re.search(r"Equipment\s*=\s*\{(.*?)\}", unit_text, re.S)
            contract(bool(equipment), f"{uid}: missing Equipment table")
            if equipment:
                contract(f'"{inv_id}"' in equipment.group(1), f"{uid}: Equipment does not reference {inv_id}")

        contract(len(entries_with(loot_entries, "loot_def", firearm_id)) == 1, f"{uid}: root inventory firearm link")
        launcher = inv_id.replace("_Inventory", "_Launcher")
        contract(
            len(entries_with(loot_entries, "loot_def", launcher)) == (1 if recipe.get("keep_existing_heavy") else 0),
            f"{uid}: launcher materialization",
        )

        side = recipe.get("sidearm")
        side_entries = entries_with(loot_entries, "loot_def", "JAZZ_Gen_Sidearm")
        contract(len(side_entries) == (1 if side else 0), f"{uid}: sidearm materialization")
        if side and side_entries:
            contract(f"Amount = {int(side.get('unlock') or 11)}" in side_entries[0], f"{uid}: sidearm unlock")
            contract(f"generate_chance = {int(side.get('chance') or 50)}" in side_entries[0], f"{uid}: sidearm chance")

        melee = recipe.get("melee")
        melee_item = (melee or {}).get("item") or "Knife"
        if melee_item == "Weapon_Knife":
            melee_item = "Knife"
        melee_entries = entries_with(item_entries, "item", melee_item) if melee else []
        expected_melee = [int(ch) for ch in ((melee or {}).get("chance_by_arch") or []) if int(ch) > 0]
        all_melee_entries = entries_with(item_entries, "item", "Knife") + entries_with(item_entries, "item", "Machete")
        contract(len(all_melee_entries) == len(expected_melee), f"{uid}: melee entry count")
        contract(sorted(chance_values(melee_entries)) == sorted(expected_melee), f"{uid}: melee chances")

        util = recipe.get("utility") or {}
        he = util.get("he") or {}
        frag_entries = entries_with(item_entries, "item", "FragGrenade")
        if he.get("mode") == "guaranteed":
            counts = [int(n) for n in (he.get("count_by_arch") or [3, 4, 5])]
            contract(len(frag_entries) == len(counts), f"{uid}: guaranteed HE count")
            contract(not chance_values(frag_entries), f"{uid}: guaranteed HE has chance")
            actual_counts = sorted(int(m.group(1)) for e in frag_entries if (m := re.search(r"stack_max = (\d+)", e)))
            contract(actual_counts == sorted(counts), f"{uid}: guaranteed HE stacks")
        elif he.get("mode") == "chance":
            expected = [int(ch) for ch in (he.get("chance_by_arch") or [10, 25, 40]) if int(ch) > 0]
            contract(len(frag_entries) == len(expected), f"{uid}: HE chance entry count")
            contract(sorted(chance_values(frag_entries)) == sorted(expected), f"{uid}: HE chances")
        else:
            contract(not frag_entries, f"{uid}: unexpected HE")

        pipe = util.get("pipe") or {}
        pipe_entries = entries_with(item_entries, "item", "PipeBomb")
        expected_pipe = [int(ch) for ch in (pipe.get("chance_by_arch") or []) if int(ch) > 0]
        contract(len(pipe_entries) == len(expected_pipe), f"{uid}: pipe entry count")
        contract(sorted(chance_values(pipe_entries)) == sorted(expected_pipe), f"{uid}: pipe chances")

        molotov_entries = entries_with(item_entries, "item", "Molotov")
        expected_molotov = int(bool(util.get("molotov_guaranteed"))) + int(bool(util.get("molotov_chance")))
        contract(len(molotov_entries) == expected_molotov, f"{uid}: Molotov materialization")
        if util.get("molotov_guaranteed"):
            guaranteed = [e for e in molotov_entries if "generate_chance" not in e]
            n = int(util["molotov_guaranteed"])
            contract(len(guaranteed) == 1 and f"stack_min = {n}" in guaranteed[0] and f"stack_max = {n}" in guaranteed[0], f"{uid}: guaranteed Molotov")
        if util.get("molotov_chance"):
            contract(int(util["molotov_chance"]) in chance_values(molotov_entries), f"{uid}: Molotov chance")

        for key, item in (("smoke_chance", "SmokeGrenade"), ("conc_chance", "ConcussiveGrenade")):
            entries = entries_with(item_entries, "item", item)
            contract(len(entries) == int(bool(util.get(key))), f"{uid}: {key} materialization")
            if util.get(key) and entries:
                contract(chance_values(entries) == [int(util[key])], f"{uid}: {key} value")
        contract(len(entries_with(item_entries, "item", "Medkit")) == int(bool(util.get("medkit"))), f"{uid}: medkit materialization")
        contract(len(entries_with(loot_entries, "loot_def", "LegionGL_5pc")) == int(bool(util.get("gl_5pc"))), f"{uid}: GL materialization")

        # MED-003 Legion field medicine by class_tier / medic
        band_entries = entries_with(item_entries, "item", "JAZZ_Bandage")
        morph_entries = entries_with(item_entries, "item", "JAZZ_Morphine")
        fak_entries = entries_with(item_entries, "item", "FirstAidKit")
        tier = int(recipe.get("class_tier") or 0)
        if util.get("medkit"):
            contract(len(fak_entries) == 1 and "stack_min = 5" in fak_entries[0], f"{uid}: medic FirstAidKit×5")
            medkit_entries = entries_with(item_entries, "item", "Medkit")
            contract(len(medkit_entries) == 1 and 5 in chance_values(medkit_entries), f"{uid}: medic Medkit 5%")
            contract(len(band_entries) == 1 and "stack_min = 1" in band_entries[0] and "stack_max = 10" in band_entries[0], f"{uid}: medic bandage 1-10")
            contract(len(morph_entries) == 1 and "stack_min = 0" in morph_entries[0] and "stack_max = 3" in morph_entries[0], f"{uid}: medic morphine 0-3")
        elif tier == 2:
            contract(len(band_entries) == 1 and "stack_min = 1" in band_entries[0] and "stack_max = 2" in band_entries[0], f"{uid}: T2 bandage 1-2")
            contract(not morph_entries, f"{uid}: T2 no morphine")
        elif tier == 3:
            contract(len(morph_entries) == 1 and 30 in chance_values(morph_entries), f"{uid}: T3 morphine 30%")
            contract(not band_entries, f"{uid}: T3 no bandage")
        else:
            contract(not band_entries and not morph_entries, f"{uid}: T{tier} no field medicine")
            contract(not fak_entries, f"{uid}: non-medic no FirstAidKit")

        contract(len(entries_with(loot_entries, "loot_def", "JAZZ_Gen_NightEquipment")) == 1, f"{uid}: night pool")
        contract(len(entries_with(loot_entries, "loot_def", "JAZZ_Gen_FlareGun")) == (3 if int(recipe.get("flaregun") or 0) > 0 else 0), f"{uid}: flare pool")
        contract(len(entries_with(loot_entries, "loot_def", "JAZZ_Gen_MiscGear")) == int(int(recipe.get("misc_chance") or 0) > 0), f"{uid}: misc pool")
        expected_values = recipe.get("valuables") not in (None, False, "none", "None")
        tiny_entries = entries_with(item_entries, "item", "TinyDiamonds")
        contract(len(tiny_entries) == int(expected_values), f"{uid}: valuables materialization")
        if expected_values and tiny_entries:
            drop = int(recipe["valuables"]["drop_chance"]) if isinstance(recipe.get("valuables"), dict) and recipe["valuables"].get("drop_chance") is not None else 30
            contract(chance_values(tiny_entries) == [drop], f"{uid}: valuables drop_chance")
            price = prices.get(uid, 500)
            mult = recipe["valuables"].get("mult") if isinstance(recipe.get("valuables"), dict) else None
            tmin, tmax = valuables_tiny_stack(price, mult)
            contract(f"stack_min = {tmin}" in tiny_entries[0] and f"stack_max = {tmax}" in tiny_entries[0], f"{uid}: valuables stack ~price")
        for armor_id in armor_defs[recipe.get("armor") or "Middle"]:
            contract(len(entries_with(loot_entries, "loot_def", armor_id)) == 1, f"{uid}: armor {armor_id}")

    if contract_failures:
        for message in contract_failures[:20]:
            fail(f"HOTFIX-003 contract: {message}")
        if len(contract_failures) > 20:
            fail(f"HOTFIX-003 contract: {len(contract_failures) - 20} more failures")
    else:
        ok("HOTFIX-003 recipe/inventory/UnitData contracts 37/37")

    commando = block_for(text, "AssaultGunner_Inventory")
    commando_items = placeobj_blocks(commando, "LootEntryInventoryItem")
    machetes = entries_with(commando_items, "item", "Machete")
    molotovs = entries_with(commando_items, "item", "Molotov")
    commando_unit = (UNITS / "UnitData" / "JAZZ_Legion_GunnerT2_AssaultGunner.lua").read_text(encoding="utf-8")
    if len(machetes) != 3 or chance_values(machetes) != [100, 100, 100]:
        fail("HOTFIX-003 Commando Machete is not guaranteed in all three arch bands")
    elif len(molotovs) != 1 or "generate_chance" in molotovs[0]:
        fail("HOTFIX-003 Commando Molotov is not unconditional")
    elif 'TryEquip(items, "Handheld B", "MeleeWeapon")' not in commando_unit:
        fail("HOTFIX-003 Commando does not equip melee in Handheld B")
    else:
        ok("HOTFIX-003 Commando guaranteed Machete + Molotov and melee equip")

    skirmisher_recipe = recipes["JAZZ_Legion_FlankerT2_Skirmisher"]
    skirmisher = block_for(text, skirmisher_recipe["firearm"])
    skirmisher_refs = re.findall(r'loot_def = "(JAZZ_GenW_[^"]+)"', skirmisher)
    if skirmisher_recipe.get("primary_tags") != ["battle"]:
        fail("HOTFIX-003 Skirmisher recipe is not battle-only")
    elif not all(str(p).startswith("rifle_") for p in skirmisher_recipe.get("packages_by_arch") or []):
        fail("HOTFIX-003 Skirmisher packages are not rifle packages")
    elif skirmisher_recipe.get("ammo_cap") != "Match":
        fail("HOTFIX-003 Skirmisher ammo cap is not Match")
    elif not skirmisher_refs or any("_rifle_" not in ref or "_flanker_" in ref for ref in skirmisher_refs):
        fail("HOTFIX-003 Skirmisher generated firearm uses non-rifle package")
    elif not any(ref.endswith("_ammo_ap") for ref in skirmisher_refs):
        fail("HOTFIX-003 Skirmisher generated firearm lacks upgraded ammo combos")
    else:
        ok("HOTFIX-003 Skirmisher battle/rifle/Match contract")

    # UNITS-004: unconditional firearm fallback
    missing_fb = []
    for uid, r in recipes.items():
        b = block_for(text, r["firearm"])
        if "JAZZ-UNITS-004 unconditional fallback" not in b:
            missing_fb.append(r["firearm"])
    if missing_fb:
        fail(f"AC-004-fallback missing on {missing_fb[:5]}")
    else:
        ok("UNITS-004 unconditional firearm fallback present")

    # metadata resources
    meta = (UNITS / "metadata.lua").read_text(encoding="utf-8")
    needed = set(re.findall(r'id = "(JAZZ_Gen[^"]+)"', text))
    have = set(re.findall(r"'Id',\s*\"(JAZZ_Gen[^\"]+)\"", meta))
    miss_meta = sorted(needed - have)
    if miss_meta:
        fail(f"AC-007 metadata missing {len(miss_meta)} JAZZ_Gen* e.g. {miss_meta[:3]}")
    else:
        ok(f"AC-007 metadata has all {len(needed)} JAZZ_Gen* resources")

    # UNITS-008: M1 carbine exception + SMG no-stock + folded AR into carbine
    m1_id = "JAZZ_GenW_M2Carbine_early_m1_30cal_carbine_ammo"
    smg_id = "JAZZ_GenW_M2Carbine_early_m1_smg_30cal_carbine_ammo"
    if f'id = "{m1_id}"' not in text:
        fail("UNITS-008 missing M1 combo LootDef")
    else:
        m1 = block_for(text, m1_id)
        if "JAZZ_StockNormal" not in m1:
            fail("UNITS-008 M1 combo missing JAZZ_StockNormal")
        elif "JAZZ_Autofire" in m1:
            fail("UNITS-008 M1 combo must not include Autofire")
        else:
            ok("UNITS-008 M1 combo is stocked semi")
    if f'id = "{smg_id}"' not in text:
        fail("UNITS-008 missing no-stock SMG combo LootDef")
    else:
        smg = block_for(text, smg_id)
        if "JAZZ_StockNo" not in smg:
            fail("UNITS-008 SMG combo missing JAZZ_StockNo")
        else:
            ok("UNITS-008 no-stock M1 combo")

    warden_f = block_for(text, "Warden_Firearm")
    if m1_id not in warden_f:
        fail("UNITS-008 Warden missing early M1")
    else:
        # Find the early_m1 entry: only Amount 19 with <=, no Amount 11/12 lower bound.
        m1_ok = False
        idx = 0
        while True:
            p = warden_f.find("PlaceObj('LootEntryLootDef'", idx)
            if p < 0:
                break
            br = warden_f.find("{", p)
            depth = 0
            j = br
            while j < len(warden_f):
                if warden_f[j] == "{":
                    depth += 1
                elif warden_f[j] == "}":
                    depth -= 1
                    if depth == 0:
                        body = warden_f[br : j + 1]
                        if m1_id in body:
                            amounts = [int(x) for x in re.findall(r"Amount = (\d+)", body)]
                            has_le = 'Condition = "<="' in body
                            has_ge_only = "Condition" not in body or (
                                has_le and len(amounts) == 1 and amounts[0] == 19
                            )
                            if has_le and amounts == [19]:
                                m1_ok = True
                            elif has_ge_only:
                                m1_ok = True
                            else:
                                fail(f"UNITS-008 Warden M1 still gated Amount={amounts}")
                        break
                j += 1
            idx = p + 1
        if m1_ok:
            ok("UNITS-008 Warden M1 has no lower Amount gate")
        elif not any("UNITS-008 Warden M1 still gated" in f for f in fails):
            fail("UNITS-008 Warden M1 entry not found with <=19 only")

    rf_block = block_for(text, "Roughneck_Firearm")
    if smg_id not in rf_block:
        fail("UNITS-008 Roughneck missing no-stock M1 SMG")
    elif m1_id in rf_block:
        fail("UNITS-008 Roughneck must not get stocked M1 carbine")
    else:
        ok("UNITS-008 Roughneck no-stock SMG only")

    fold_refs = re.findall(r'loot_def = "(JAZZ_GenW_[^"]+_carbine_fold_[^"]+)"', warden_f)
    if not fold_refs:
        fail("UNITS-008 Warden missing carbine_fold AR borrow")
    else:
        fold_w = None
        idx = 0
        while fold_w is None:
            p = warden_f.find("PlaceObj('LootEntryLootDef'", idx)
            if p < 0:
                break
            br = warden_f.find("{", p)
            depth = 0
            j = br
            while j < len(warden_f):
                if warden_f[j] == "{":
                    depth += 1
                elif warden_f[j] == "}":
                    depth -= 1
                    if depth == 0:
                        body = warden_f[br : j + 1]
                        if "_carbine_fold_" in body:
                            wm = re.search(r"weight = (\d+)", body)
                            am = [int(x) for x in re.findall(r"Amount = (\d+)", body)]
                            if wm:
                                fold_w = int(wm.group(1))
                                if fold_w != 6000:
                                    fail(f"UNITS-008 carbine_fold weight {fold_w} != 6000")
                                elif am and am[0] < 21:
                                    fail(f"UNITS-008 carbine_fold unlock too early Amount={am}")
                                else:
                                    ok(f"UNITS-008 carbine_fold {fold_refs[0]} weight=6000 Amount={am}")
                        break
                j += 1
            idx = p + 1
        if fold_w is None:
            fail("UNITS-008 carbine_fold entry body not parsed")

    print("---")
    if fails:
        print(f"RESULT: FAILED ({len(fails)} issues)")
        return 1
    print("RESULT: PASSED (static AC suite)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
