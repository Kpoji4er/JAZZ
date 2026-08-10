# -*- coding: utf-8 -*-
"""Sync MED-003 kit defs into jazz/items.lua and Bonemaker loot in jazz-units."""
from __future__ import annotations

import re
from pathlib import Path

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")


def replace_between(text: str, start_pat: str, end_pat: str, new_mid: str) -> tuple[str, bool]:
    m = re.search(start_pat, text)
    if not m:
        return text, False
    start = m.start()
    m2 = re.search(end_pat, text[m.end() :])
    if not m2:
        return text, False
    end = m.end() + m2.start()
    return text[:start] + new_mid + text[end:], True


def sync_jazz_items() -> None:
    path = JAZZ / "items.lua"
    text = path.read_text(encoding="utf-8")

    # FirstAidKit AdditionalHint + keep MaxStacks 5 (already)
    text2, ok = replace_between(
        text,
        r"'Id', \"FirstAidKit\",",
        r"'Id', \"Medkit\",",
        """'Id', "FirstAidKit",
				'object_class', "JazzStackableMedicine",
				'ScrapParts', 1,
				'Repairable', false,
				'Icon', "Mod/e6L4ECj/Icons/Items/JAZZ_IFAK.png",
				'DisplayName', T(890000000010022, "Small Medkit"),
				'DisplayNamePlural', T(890000000010023, "Small Medkits"),
				'AdditionalHint', T(890000000010024, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on one untreated light trauma\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"),
				'UnitStat', "Medical",
				'Cost', 300,
				'CanAppearInShop', true,
					'Tier', 1,
				'RestockWeight', 150,
				'CategoryPair', "Medicine",
				'MaxStacks', 5,
				'UsePriority', 0,
			}),
			PlaceObj('ModItemInventoryItemCompositeDef', {
				'Group', "Other - Meds",
""",
    )
    if not ok:
        raise SystemExit("FirstAidKit block replace failed")
    text = text2

    text2, ok = replace_between(
        text,
        r"'Id', \"Medkit\",",
        r"'Id', \"MetaviraShot\",",
        """'Id', "Medkit",
				'object_class', "JazzStackableMedicine",
				'unit_reactions', {
					PlaceObj('UnitReaction', {
						Event = "OnCalcHealAmount",
						Handler = function (self, target, patient, medic, medkit, data)
							if self == medkit then
								data.heal_modifier = data.heal_modifier + 50
							end
					end,
					}),
				},
				'ScrapParts', 1,
				'Repairable', false,
				'Icon', "Mod/e6L4ECj/Icons/Items/JAZZ_Medkit.png",
				'DisplayName', T(890000000010025, "Medium Medkit"),
				'DisplayNamePlural', T(890000000010026, "Medium Medkits"),
				'AdditionalHint', T(890000000010027, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage healing bonus: 50%.\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on one untreated medium or light trauma\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack"),
				'UnitStat', "Medical",
				'Cost', 500,
				'CanAppearInShop', true,
				'Tier', 1,
				'RestockWeight', 80,
				'CategoryPair', "Medicine",
				'MaxStacks', 10,
				'UsePriority', 1,
			}),
			PlaceObj('ModItemInventoryItemCompositeDef', {
				'Group', "Other - Meds",
""",
    )
    if not ok:
        raise SystemExit("Medkit block replace failed")
    text = text2

    text2, ok = replace_between(
        text,
        r"'Id', \"Reanimationsset\",",
        r"'Id', \"PlasmaGun_Crowbar\",",
        """'Id', "Reanimationsset",
				'object_class', "JazzStackableMedicine",
				'unit_reactions', {
					PlaceObj('UnitReaction', {
						Event = "OnCalcHealAmount",
						Handler = function (self, target, patient, medic, medkit, data)
							if self == medkit then
								data.heal_modifier = data.heal_modifier + 100
							end
						end,
					}),
				},
				'ScrapParts', 1,
				'Repairable', false,
				'Icon', "UI/Icons/Items/reanimationsset.png",
				'DisplayName', T(890000000010031, "Large Medkit"),
				'DisplayNamePlural', T(890000000010032, "Large Medkits"),
				'AdditionalHint', T(890000000010030, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage healing bonus: 100%\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on any untreated trauma\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically from inventory"),
				'UnitStat', "Medical",
				'Cost', 1800,
				'CanAppearInShop', true,
				'Tier', 3,
				'MaxStock', 1,
				'RestockWeight', 15,
				'CategoryPair', "Medicine",
				'MaxStacks', 15,
				'UsePriority', 2,
			}),
			PlaceObj('ModItemInventoryItemCompositeDef', {
				'Group', "Quest - Equipment",
""",
    )
    if not ok:
        raise SystemExit("Reanimationsset block replace failed")
    text = text2

    # Bandage description
    old_desc = (
        'Description = T(890000000010213, "Treat an ally with a small, medium, or large medkit. '
        "Restores HP based on Medical and stops bleeding. Small and medium medkits remove all bleeding. "
        'Large medkit starts healing on the heaviest untreated trauma. Field bandages use a separate action.")'
    )
    new_desc = (
        'Description = T(890000000010213, "Treat an ally with a small, medium, or large medkit. '
        "Restores HP based on Medical, clears all bleeding, eases pain, clears wound infection, and can rally the downed. "
        "Small starts healing on a light trauma; medium on medium or light; large on any trauma. "
        'Field bandages use a separate action.")'
    )
    if old_desc not in text:
        # try looser
        text, n = re.subn(
            r'Description = T\(890000000010213, "[^"]*"\)',
            new_desc.replace("Description = ", "Description = ", 1),
            text,
            count=1,
        )
        print("Bandage Description regex replacements", n)
    else:
        text = text.replace(old_desc, new_desc)
        print("Bandage Description exact replace OK")

    path.write_text(text, encoding="utf-8")
    print("jazz items.lua synced")


def sync_bonemaker() -> None:
    text = UNITS.read_text(encoding="utf-8")
    old = """\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {
\t\t\t\t\t\t\titem = "Medkit",
\t\t\t\t\t\t\tstack_max = 1,
\t\t\t\t\t\t\tstack_min = 1,
\t\t\t\t\t\t}),"""
    new = """\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {
\t\t\t\t\t\t\titem = "FirstAidKit",
\t\t\t\t\t\t\tstack_max = 5,
\t\t\t\t\t\t\tstack_min = 5,
\t\t\t\t\t\t}),
\t\t\t\t\t\tPlaceObj('LootEntryInventoryItem', {
\t\t\t\t\t\t\tgenerate_chance = 5,
\t\t\t\t\t\t\titem = "Medkit",
\t\t\t\t\t\t\tstack_max = 1,
\t\t\t\t\t\t\tstack_min = 1,
\t\t\t\t\t\t}),"""
    # Only inside Bonemaker_Inventory: find unique occurrence near that id
    idx = text.find('id = "Bonemaker_Inventory"')
    if idx < 0:
        raise SystemExit("Bonemaker_Inventory not found")
    # search Medkit entry after id within next 5k
    window = text[idx : idx + 5000]
    if 'item = "Medkit"' not in window:
        raise SystemExit("Medkit entry not in Bonemaker window")
    # replace first Medkit guaranteed entry in that window
    m = re.search(
        r"PlaceObj\('LootEntryInventoryItem', \{\s*item = \"Medkit\",\s*stack_max = 1,\s*stack_min = 1,\s*\}\),",
        window,
    )
    if not m:
        raise SystemExit("exact Medkit loot pattern not found")
    abs_start = idx + m.start()
    abs_end = idx + m.end()
    text = text[:abs_start] + new.replace("\t", "\t") + text[abs_end:]
    # fix: new used tabs from old style - use m.group indentation
    # Actually write using the matched style from file - re-read match and build with same indent
    indent = "\t\t\t\t\t\t"
    new2 = (
        f"{indent}PlaceObj('LootEntryInventoryItem', {{\n"
        f"{indent}\titem = \"FirstAidKit\",\n"
        f"{indent}\tstack_max = 5,\n"
        f"{indent}\tstack_min = 5,\n"
        f"{indent}}}),\n"
        f"{indent}PlaceObj('LootEntryInventoryItem', {{\n"
        f"{indent}\tgenerate_chance = 5,\n"
        f"{indent}\titem = \"Medkit\",\n"
        f"{indent}\tstack_max = 1,\n"
        f"{indent}\tstack_min = 1,\n"
        f"{indent}}}),"
    )
    text = UNITS.read_text(encoding="utf-8")
    idx = text.find('id = "Bonemaker_Inventory"')
    window = text[idx : idx + 5000]
    m = re.search(
        r"PlaceObj\('LootEntryInventoryItem', \{\s*item = \"Medkit\",\s*stack_max = 1,\s*stack_min = 1,\s*\}\),",
        window,
    )
    abs_start = idx + m.start()
    abs_end = idx + m.end()
    text = text[:abs_start] + new2 + text[abs_end:]
    UNITS.write_text(text, encoding="utf-8")
    print("Bonemaker_Inventory medicine updated")


if __name__ == "__main__":
    sync_jazz_items()
    sync_bonemaker()
