# -*- coding: utf-8 -*-
"""Patch items.lua for JAZZ-ECON-004: ModItemCode, Other SubCategories, TCE 4/5."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"

MODITEM_CODE = """\
		PlaceObj('ModItemCode', {
			'name', "System_BobbyRay_ECON004",
			'CodeFileName', "Code/System_BobbyRay_ECON004.lua",
		}),
"""

SUBCATS = """\
				PlaceObj('ModItemBobbyRayShopSubCategory', {
					Category = "Other",
					DisplayName = T(890000000020150, --[[ModItemBobbyRayShopSubCategory Other Optics DisplayName]] "Optics"),
					SortKey = 51,
					group = "Other",
					id = "Optics",
				}),
				PlaceObj('ModItemBobbyRayShopSubCategory', {
					Category = "Other",
					DisplayName = T(890000000020151, --[[ModItemBobbyRayShopSubCategory Other Magazines DisplayName]] "Magazines"),
					SortKey = 52,
					group = "Other",
					id = "Magazines",
				}),
				PlaceObj('ModItemBobbyRayShopSubCategory', {
					Category = "Other",
					DisplayName = T(890000000020152, --[[ModItemBobbyRayShopSubCategory Other Muzzle DisplayName]] "Muzzle"),
					SortKey = 53,
					group = "Other",
					id = "Muzzle",
				}),
				PlaceObj('ModItemBobbyRayShopSubCategory', {
					Category = "Other",
					DisplayName = T(890000000020153, --[[ModItemBobbyRayShopSubCategory Other Side DisplayName]] "Side"),
					SortKey = 54,
					group = "Other",
					id = "Side",
				}),
				PlaceObj('ModItemBobbyRayShopSubCategory', {
					Category = "Other",
					DisplayName = T(890000000020154, --[[ModItemBobbyRayShopSubCategory Other Under DisplayName]] "Underbarrel"),
					SortKey = 55,
					group = "Other",
					id = "Under",
				}),
				PlaceObj('ModItemBobbyRayShopSubCategory', {
					Category = "Other",
					DisplayName = T(890000000020155, --[[ModItemBobbyRayShopSubCategory Other Bipod DisplayName]] "Bipod"),
					SortKey = 56,
					group = "Other",
					id = "Bipod",
				}),
"""

TCE4 = r"""				PlaceObj('TriggeredConditionalEvent', {
					Conditions = {
						PlaceObj('AND', {
							Conditions = {
								PlaceObj('QuestIsVariableBool', {
									Condition = "or",
									QuestId = "04_Betrayal",
									Vars = set( "TriggerWorldFlip", "WorldFlipDone" ),
								}),
								PlaceObj('PlayerControlSectors', {
									Amount = 4,
									Condition = ">=",
									POIs = "Mine",
									QuestId = "BobbyRayQuest",
								}),
								PlaceObj('QuestIsVariableNum', {
									Amount = 3,
									Condition = "<=",
									Prop = "UnlockedTier",
									QuestId = "BobbyRayQuest",
								}),
							},
							QuestId = "BobbyRayQuest",
						}),
					},
					Effects = {
						PlaceObj('ExecuteCode', {
							FuncCode = 'bobby_tier_print("--------------------- unlocking tier 4 with quest")\nif obj.BlockingEmails then\n	bobby_tier_print("\\t\\tEmail timer not yet passed, will not send e-mail...")\nelse\n	bobby_tier_print("\\t\\tSending e-mail!")\n	ReceiveEmail("BobbyRayShopTier3Unlocked")\nend',
							QuestId = "BobbyRayQuest",
						}),
						PlaceObj('BobbyRaySetState', {
							QuestId = "BobbyRayQuest",
							State = 4,
						}),
					},
					Once = true,
					ParamId = "TCE_Tier4Unlock",
					QuestId = "BobbyRayQuest",
				}),
"""

TCE5 = r"""				PlaceObj('TriggeredConditionalEvent', {
					Conditions = {
						PlaceObj('AND', {
							Conditions = {
								PlaceObj('QuestIsVariableBool', {
									Condition = "or",
									QuestId = "04_Betrayal",
									Vars = set( "TriggerWorldFlip", "WorldFlipDone" ),
								}),
								PlaceObj('PlayerControlSectors', {
									Amount = 5,
									Condition = ">=",
									POIs = "Mine",
									QuestId = "BobbyRayQuest",
								}),
								PlaceObj('QuestIsVariableNum', {
									Amount = 4,
									Condition = "<=",
									Prop = "UnlockedTier",
									QuestId = "BobbyRayQuest",
								}),
							},
							QuestId = "BobbyRayQuest",
						}),
					},
					Effects = {
						PlaceObj('ExecuteCode', {
							FuncCode = 'bobby_tier_print("--------------------- unlocking tier 5 with quest")\nif obj.BlockingEmails then\n	bobby_tier_print("\\t\\tEmail timer not yet passed, will not send e-mail...")\nelse\n	bobby_tier_print("\\t\\tSending e-mail!")\n	ReceiveEmail("BobbyRayShopTier3Unlocked")\nend',
							QuestId = "BobbyRayQuest",
						}),
						PlaceObj('BobbyRaySetState', {
							QuestId = "BobbyRayQuest",
							State = 5,
						}),
					},
					Once = true,
					ParamId = "TCE_Tier5Unlock",
					QuestId = "BobbyRayQuest",
				}),
"""

VARS45 = """\
				PlaceObj('QuestVarTCEState', {
					Name = "TCE_Tier4Unlock",
					QuestId = "BobbyRayQuest",
				}),
				PlaceObj('QuestVarTCEState', {
					Name = "TCE_Tier5Unlock",
					QuestId = "BobbyRayQuest",
				}),
"""


def main() -> int:
    text = ITEMS.read_text(encoding="utf-8")
    changed = False

    if "System_BobbyRay_ECON004" not in text:
        anchor = (
            "\t\tPlaceObj('ModItemCode', {\n"
            "\t\t\t'name', \"System_RIS_Browser\",\n"
            "\t\t\t'CodeFileName', \"Code/System_RIS_Browser.lua\",\n"
            "\t\t}),\n"
        )
        if anchor not in text:
            raise SystemExit("ModItemCode anchor missing")
        text = text.replace(anchor, anchor + MODITEM_CODE, 1)
        changed = True
        print("inserted ModItemCode")
    else:
        print("ModItemCode already present")

    if 'id = "Optics"' not in text:
        idx = text.find('id = "3006"')
        if idx < 0:
            raise SystemExit("3006 not found")
        end_3006 = text.find("}),\n", idx)
        if end_3006 < 0:
            raise SystemExit("3006 close missing")
        insert_at = end_3006 + 4
        text = text[:insert_at] + SUBCATS + text[insert_at:]
        changed = True
        print("inserted Other SubCategories")
    else:
        print("Optics already in items.lua")

    if "TCE_Tier4Unlock" not in text:
        needle = (
            '\t\t\t\t\tParamId = "TCE_Tier3Unlock",\n'
            '\t\t\t\t\tQuestId = "BobbyRayQuest",\n'
            "\t\t\t\t}),\n"
        )
        if needle not in text:
            raise SystemExit("TCE3 close needle missing")
        text = text.replace(needle, needle + TCE4 + TCE5, 1)
        changed = True
        print("inserted TCE 4/5")
    else:
        print("TCE4 already present")

    if 'Name = "TCE_Tier4Unlock"' not in text:
        needle = (
            "\t\t\t\tPlaceObj('QuestVarTCEState', {\n"
            '\t\t\t\t\tName = "TCE_Tier3Unlock",\n'
            '\t\t\t\t\tQuestId = "BobbyRayQuest",\n'
            "\t\t\t\t}),\n"
        )
        if needle not in text:
            raise SystemExit("TCE3 var needle missing")
        text = text.replace(needle, needle + VARS45, 1)
        changed = True
        print("inserted QuestVar TCE 4/5")
    else:
        print("TCE4 var already present")

    if not changed:
        print("nothing to write")
        return 0

    tmp = ITEMS.with_suffix(".lua.bobby_tce_tmp")
    tmp.write_bytes(text.encode("utf-8"))
    bak = ITEMS.with_suffix(".lua.bak_bobby_tce")
    if not bak.exists():
        bak.write_bytes(ITEMS.read_bytes())
    ITEMS.write_bytes(tmp.read_bytes())
    tmp.unlink(missing_ok=True)
    print("wrote", ITEMS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
