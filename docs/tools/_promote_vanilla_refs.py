# -*- coding: utf-8 -*-
"""Promote dangling vanilla_ref live options to JAZZ_ ModItemWeaponComponent stubs."""
from __future__ import annotations

import re
from pathlib import Path
import sys

sys.path.insert(0, "docs/tools")
from _apply_attach_001 import (
    placeobj_blocks, prop, rename_slots, matching_paren, remove_resources,
)

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
INVENTORY = ROOT / "InventoryItem"

# old_id -> (display, slot, cost, difficulty, effects list, params dict, group)
STUBS = {
    "AKSU_Hanguard_Basic": ("Default Handguard", "Handguard", 0, -25, [], {}, "AKSU Specific"),
    "AUGCompensator_01": ("Default Compensator", "Muzzle", 10, -25, ["AccuracyBonusSameTarget"], {}, "AUG Specific"),
    "AUGCompensator_03": (
        "Advanced Compensator", "Muzzle", 15, 0,
        ["AccuracyBonusSameTarget", "IncreaseReliability"], {"ReliabilityIncrease": 10}, "AUG Specific",
    ),
    "BarrelShort_Winchester": (
        "Short Barrel", "Barrel", 15, 0,
        [
            "ReduceShootAP", "ReduceRange", "ReduceReliability", "ReduceMagazineSize",
            "CloseRangeDecrease", "CloseRangeFactorIncrease",
        ],
        {
            "ShootAPDecrease": 1, "RangeDecrease": 4, "ReliabilityDecrease": 10,
            "MagazineSizeDecrease": 4, "CloseRangeDecrease": 1, "CloseRangeFactorIncrease": 10,
        },
        "Winchester Specific",
    ),
    "DefaultMuzzle_HK21": ("Default Flash Hider", "Muzzle", 0, -25, [], {}, "HK 21 Specific"),
    "FNFAL_Handguard": ("Default Handguard", "Handguard", 0, -25, [], {}, "FNFAL Specific"),
    "Galil_Handguard_Default": ("Default Handguard", "Under", 2, -25, [], {}, "Galil Specific"),
    "MuzzleBooster_Glock18": ("Default Chamber", "Handguard", 15, 0, [], {}, "Glock18 Specific"),
    "Compensator_cosmetic": ("Compensator", "Muzzle", 25, 0, [], {}, "Muzzle"),
}

ORPHAN_EFFECTS = {
    "ExtraAutoShots", "ExtraBurstShots", "FirstShotIncreasedAim",
    "ReduceAimAccuracy20Percent", "ReduceAuto25Percent", "ReduceAuto75Percent",
    "ReduceBurst25Percent", "ReduceBurst50Percent",
}


def fmt_effects(effects: list[str]) -> str:
    if not effects:
        return ""
    lines = "\n".join(f'\t\t\t\t\t\t"{e}",' for e in effects)
    return f"""
					ModificationEffects = {{
{lines}
					}},"""


def fmt_params(params: dict[str, int]) -> str:
    if not params:
        return ""
    chunks = []
    for name, value in params.items():
        chunks.append(
            f"""						PlaceObj('PresetParamNumber', {{
							'Name', "{name}",
							'Value', {value},
							'Tag', "<{name}>",
						}}),"""
        )
    return f"""
					Parameters = {{
{chr(10).join(chunks)}
					}},"""


def stub_block(old_id: str, meta, tid: int) -> str:
    display, slot, cost, diff, effects, params, group = meta
    new_id = "JAZZ_" + old_id
    return f"""				PlaceObj('ModItemWeaponComponent', {{
					DisplayName = T({tid}, --[[ModItemWeaponComponent {new_id} DisplayName]] "{display}"),
					Cost = {cost},
					ModificationDifficulty = {diff},
					Slot = "{slot}",{fmt_effects(effects)}{fmt_params(params)}
					group = "{group}",
					id = "{new_id}",
				}}),
"""


def main():
    items = ITEMS.read_text(encoding="utf-8")
    metadata = META.read_text(encoding="utf-8")
    companions = {p: p.read_text(encoding="utf-8") for p in INVENTORY.glob("*.lua")}

    rename = {old: "JAZZ_" + old for old in STUBS}
    tid_base = 982641740101
    for i, (old, meta) in enumerate(STUBS.items()):
        new_id = rename[old]
        if f'id = "{new_id}"' in items:
            print("already", new_id)
            continue
        block = stub_block(old, meta, tid_base + i)
        anchor = items.find("PlaceObj('ModItemWeaponComponent'")
        if anchor < 0:
            raise SystemExit("no WeaponComponent anchor")
        items = items[:anchor] + block + items[anchor:]
        print("inserted", new_id)

    # Ensure metadata resources for new ids
    for new_id in rename.values():
        if f"'Id', \"{new_id}\"" in metadata:
            continue
        entry = (
            "\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"WeaponComponent\",\n"
            f"\t\t\t'Id', \"{new_id}\",\n"
            "\t\t\t'ClassDisplayName', \"Weapon Component\",\n"
            "\t\t}),\n"
        )
        # insert before first WeaponComponent resource
        m = re.search(r"\t\tPlaceObj\('ModResourcePreset', \{\s*\n\t\t\t'Class', \"WeaponComponent\"", metadata)
        if not m:
            raise SystemExit("no metadata WeaponComponent anchor")
        metadata = metadata[: m.start()] + entry + metadata[m.start() :]
        print("metadata+", new_id)

    items, n1 = rename_slots(items, rename)
    print("items slot renames", n1)
    for p, t in list(companions.items()):
        companions[p], n = rename_slots(t, rename)
        if n:
            print("companion", p.name, n)

    # Delete orphan effect presets (consume trailing list commas)
    from _apply_attach_001 import delete_placeobj_blocks

    items, n_fx = delete_placeobj_blocks(
        items, "ModItemWeaponComponentEffect", lambda block: prop(block.text, "id") in ORPHAN_EFFECTS
    )
    print("deleted orphan effects", n_fx)
    metadata, n = remove_resources(metadata, "WeaponComponentEffect", ORPHAN_EFFECTS)
    print("metadata effect resources removed", n)

    ITEMS.write_text(items, encoding="utf-8", newline="\n")
    META.write_text(metadata, encoding="utf-8", newline="\n")
    for p, t in companions.items():
        p.write_text(t, encoding="utf-8", newline="\n")

    # Loc stubs for display names (RU=EN for now)
    # skip — DisplayName T ids will be picked by localization audit later

    print("done")


if __name__ == "__main__":
    main()
