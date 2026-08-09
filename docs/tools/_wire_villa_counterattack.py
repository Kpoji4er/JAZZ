"""Wire Jazz_VillaCounterAttack quest + FlagHill_Emma_1 guests + ModItemCode + metadata."""
from __future__ import annotations

from pathlib import Path

ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\items.lua")
META = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-maps\metadata.lua")

QUEST = r'''
			PlaceObj('ModItemQuestsDef', {
				Author = "JAZZ",
				DevNotes = "JAZZ-QUESTS-003 Flag Hill villa counterattack: move camp Attackers + Ernie30; Wave2 CombatTurn; late dump",
				DisplayName = T(890000000013100, --[[ModItemQuestsDef Jazz_VillaCounterAttack DisplayName]] "Контратака на виллу"),
				NoteDefs = {
					PlaceObj('QuestNote', {{
						Badges = {{
							PlaceObj('QuestBadgePlacement', {{
								Sector = "K4",
							}}),
						}},
						Text = T(890000000013101, --[[ModItemQuestsDef Jazz_VillaCounterAttack Text]] "Легион идёт на виллу Коразон. Приготовьтесь к обороне — уйти из сектора нельзя."),
					}}),
					PlaceObj('QuestNote', {{
						CompletionConditions = {{
							PlaceObj('QuestIsVariableBool', {{
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set( "Completed" ),
							}}),
						}},
						ShowOnRead = true,
						Text = T(890000000013102, --[[ModItemQuestsDef Jazz_VillaCounterAttack Text]] "Контратака на виллу отбита."),
					}}),
				},
				QuestGroup = "Ernie Island",
				TCEs = {{
					PlaceObj('TriggeredConditionalEvent', {{
						Conditions = {{
							PlaceObj('QuestIsVariableBool', {{
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set({{
	Given = true,
	Completed = false,
	Failed = false,
	Wave2Spawn = false,
}}),
							}}),
							PlaceObj('PlayerIsInSectors', {{
								Sectors = {{
									"K4",
								}},
							}}),
							PlaceObj('CombatIsActive', {{}}),
							PlaceObj('CombatTurn', {{
								Amount = 3,
								Condition = ">=",
							}}),
							PlaceObj('QuestIsVariableBool', {{
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set( "SiegeCombat" ),
							}}),
						}},
						Effects = {{
							PlaceObj('QuestSetVariableBool', {{
								Prop = "Wave2Spawn",
								QuestId = "Jazz_VillaCounterAttack",
							}}),
							PlaceObj('ExecuteCode', {{
								FuncCode = "Jazz_VillaCounterAttack_OnWave2()",
							}}),
							PlaceObj('GroupAlert', {{
								TargetUnit = "VillaSiege_Wave2",
							}}),
						}},
						Once = true,
						ParamId = "TCE_Wave2",
						QuestId = "Jazz_VillaCounterAttack",
						requiredSectors = {{
							"K4",
						}},
					}}),
					PlaceObj('TriggeredConditionalEvent', {{
						Conditions = {{
							PlaceObj('QuestIsVariableBool', {{
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set({{
	Given = true,
	Completed = false,
	SiegeCombat = false,
}}),
							}}),
							PlaceObj('PlayerIsInSectors', {{
								Sectors = {{
									"K4",
								}},
							}}),
							PlaceObj('CombatIsActive', {{}}),
						}},
						Effects = {{
							PlaceObj('QuestSetVariableBool', {{
								Prop = "SiegeCombat",
								QuestId = "Jazz_VillaCounterAttack",
							}}),
							PlaceObj('ExecuteCode', {{
								FuncCode = "Jazz_VillaCounterAttack_PushAdvanceToEmma()",
							}}),
						}},
						Once = true,
						ParamId = "TCE_SiegeCombatStarted",
						QuestId = "Jazz_VillaCounterAttack",
						requiredSectors = {{
							"K4",
						}},
					}}),
					PlaceObj('TriggeredConditionalEvent', {{
						Conditions = {{
							PlaceObj('QuestIsVariableBool', {{
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set({{
	Given = true,
	Completed = false,
	Failed = false,
}}),
							}}),
							PlaceObj('PlayerIsInSectors', {{
								Sectors = {{
									"K4",
								}},
							}}),
							PlaceObj('CombatIsActive', {{
								Negate = true,
							}}),
							PlaceObj('QuestIsVariableBool', {{
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set( "Wave2Spawn" ),
							}}),
							PlaceObj('GroupIsDead', {{
								Group = "VillaSiege_Wave2",
							}}),
							PlaceObj('CheckOR', {{
								Conditions = {{
									PlaceObj('SquadDefeated', {{
										custom_squad_id = "VillaAttackers_Ernie",
									}}),
									PlaceObj('SectorCheckOwner', {{
										sector_id = "K4",
									}}),
								}},
							}}),
						}},
						Effects = {{
							PlaceObj('QuestSetVariableBool', {{
								Prop = "Completed",
								QuestId = "Jazz_VillaCounterAttack",
							}}),
							PlaceObj('SectorEnterConflict', {{
								conflict_mode = false,
								sector_id = "K4",
							}}),
						}},
						Once = true,
						ParamId = "TCE_Won",
						QuestId = "Jazz_VillaCounterAttack",
						requiredSectors = {{
							"K4",
						}},
					}}),
				}},
				Variables = {{
					PlaceObj('QuestVarTCEState', {{
						Name = "TCE_Wave2",
					}}),
					PlaceObj('QuestVarTCEState', {{
						Name = "TCE_SiegeCombatStarted",
					}}),
					PlaceObj('QuestVarTCEState', {{
						Name = "TCE_Won",
					}}),
					PlaceObj('QuestVarBool', {{
						Name = "Completed",
					}}),
					PlaceObj('QuestVarBool', {{
						Name = "Given",
					}}),
					PlaceObj('QuestVarBool', {{
						Name = "Failed",
					}}),
					PlaceObj('QuestVarBool', {{
						Name = "NotStarted",
						Value = true,
					}}),
					PlaceObj('QuestVarBool', {{
						Name = "Wave2Spawn",
					}}),
					PlaceObj('QuestVarBool', {{
						Name = "SiegeCombat",
					}}),
				}},
				group = "Ernie",
				id = "Jazz_VillaCounterAttack",
			}}),
'''

# Fix double braces from f-string style - I used {{ for escaping incorrectly in raw string
# Rebuild QUEST without double braces

QUEST = """
			PlaceObj('ModItemQuestsDef', {
				Author = "JAZZ",
				DevNotes = "JAZZ-QUESTS-003 Flag Hill villa counterattack",
				DisplayName = T(890000000013100, --[[ModItemQuestsDef Jazz_VillaCounterAttack DisplayName]] "Контратака на виллу"),
				NoteDefs = {
					PlaceObj('QuestNote', {
						Badges = {
							PlaceObj('QuestBadgePlacement', {
								Sector = "K4",
							}),
						},
						Text = T(890000000013101, --[[ModItemQuestsDef Jazz_VillaCounterAttack Text]] "Легион идёт на виллу Коразон. Приготовьтесь к обороне — уйти из сектора нельзя."),
					}),
					PlaceObj('QuestNote', {
						CompletionConditions = {
							PlaceObj('QuestIsVariableBool', {
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set( "Completed" ),
							}),
						},
						ShowOnRead = true,
						Text = T(890000000013102, --[[ModItemQuestsDef Jazz_VillaCounterAttack Text]] "Контратака на виллу отбита."),
					}),
				},
				QuestGroup = "Ernie Island",
				TCEs = {
					PlaceObj('TriggeredConditionalEvent', {
						Conditions = {
							PlaceObj('QuestIsVariableBool', {
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set({
	Given = true,
	Completed = false,
	Failed = false,
	Wave2Spawn = false,
}),
							}),
							PlaceObj('PlayerIsInSectors', {
								Sectors = {
									"K4",
								},
							}),
							PlaceObj('CombatIsActive', {}),
							PlaceObj('CombatTurn', {
								Amount = 3,
								Condition = ">=",
							}),
							PlaceObj('QuestIsVariableBool', {
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set( "SiegeCombat" ),
							}),
						},
						Effects = {
							PlaceObj('QuestSetVariableBool', {
								Prop = "Wave2Spawn",
								QuestId = "Jazz_VillaCounterAttack",
							}),
							PlaceObj('ExecuteCode', {
								FuncCode = "Jazz_VillaCounterAttack_OnWave2()",
							}),
							PlaceObj('GroupAlert', {
								TargetUnit = "VillaSiege_Wave2",
							}),
						},
						Once = true,
						ParamId = "TCE_Wave2",
						QuestId = "Jazz_VillaCounterAttack",
						requiredSectors = {
							"K4",
						},
					}),
					PlaceObj('TriggeredConditionalEvent', {
						Conditions = {
							PlaceObj('QuestIsVariableBool', {
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set({
	Given = true,
	Completed = false,
	SiegeCombat = false,
}),
							}),
							PlaceObj('PlayerIsInSectors', {
								Sectors = {
									"K4",
								},
							}),
							PlaceObj('CombatIsActive', {}),
						},
						Effects = {
							PlaceObj('QuestSetVariableBool', {
								Prop = "SiegeCombat",
								QuestId = "Jazz_VillaCounterAttack",
							}),
							PlaceObj('ExecuteCode', {
								FuncCode = "Jazz_VillaCounterAttack_PushAdvanceToEmma()",
							}),
						},
						Once = true,
						ParamId = "TCE_SiegeCombatStarted",
						QuestId = "Jazz_VillaCounterAttack",
						requiredSectors = {
							"K4",
						},
					}),
					PlaceObj('TriggeredConditionalEvent', {
						Conditions = {
							PlaceObj('QuestIsVariableBool', {
								QuestId = "Jazz_VillaCounterAttack",
								Vars = set({
	Given = true,
	Completed = false,
	Failed = false,
	Wave2Spawn = true,
}),
							}),
							PlaceObj('PlayerIsInSectors', {
								Sectors = {
									"K4",
								},
							}),
							PlaceObj('CombatIsActive', {
								Negate = true,
							}),
							PlaceObj('GroupIsDead', {
								Group = "VillaSiege_Wave2",
							}),
						},
						Effects = {
							PlaceObj('QuestSetVariableBool', {
								Prop = "Completed",
								QuestId = "Jazz_VillaCounterAttack",
							}),
							PlaceObj('SectorEnterConflict', {
								conflict_mode = false,
								sector_id = "K4",
							}),
						},
						Once = true,
						ParamId = "TCE_Won",
						QuestId = "Jazz_VillaCounterAttack",
						requiredSectors = {
							"K4",
						},
					}),
				},
				Variables = {
					PlaceObj('QuestVarTCEState', {
						Name = "TCE_Wave2",
					}),
					PlaceObj('QuestVarTCEState', {
						Name = "TCE_SiegeCombatStarted",
					}),
					PlaceObj('QuestVarTCEState', {
						Name = "TCE_Won",
					}),
					PlaceObj('QuestVarBool', {
						Name = "Completed",
					}),
					PlaceObj('QuestVarBool', {
						Name = "Given",
					}),
					PlaceObj('QuestVarBool', {
						Name = "Failed",
					}),
					PlaceObj('QuestVarBool', {
						Name = "NotStarted",
						Value = true,
					}),
					PlaceObj('QuestVarBool', {
						Name = "Wave2Spawn",
					}),
					PlaceObj('QuestVarBool', {
						Name = "SiegeCombat",
					}),
				},
				group = "Ernie",
				id = "Jazz_VillaCounterAttack",
			}),
"""

GUESTS = """
					PlaceObj('ConversationPhrase', {
						AutoRemove = true,
						Effects = {
							PlaceObj('QuestSetVariableBool', {
								Prop = "Given",
								QuestId = "Jazz_VillaCounterAttack",
							}),
							PlaceObj('QuestSetVariableBool', {
								Prop = "NotStarted",
								QuestId = "Jazz_VillaCounterAttack",
								Set = false,
							}),
							PlaceObj('SectorEnterConflict', {
								disable_travel = true,
								lock_conflict = true,
								sector_id = "K4",
								descr_id = "InitialConflict",
							}),
							PlaceObj('ExecuteCode', {
								FuncCode = "Jazz_VillaCounterAttack_Start()",
							}),
							PlaceObj('QuestSetVariableTimer', {
								Prop = "PrepTimer",
								QuestId = "Jazz_VillaCounterAttack",
								TimeAmount = 2,
								Timescale = "h",
							}),
						},
						GoTo = "<end conversation>",
						Keyword = "Guests",
						KeywordT = T(890000000013103, --[[ModItemConversation FlagHill_Emma_1 KeywordT]] "Guests"),
						Lines = {
							PlaceObj('ConversationLine', {
								Character = "CorazonSantiago",
								Text = T(890000000013104, --[[ModItemConversation FlagHill_Emma_1 Text voice:CorazonSantiago section:FlagHill_Emma_1 keyword:Guests]] "Тихо. У нас гости."),
							}),
							PlaceObj('ConversationLine', {
								Character = "Emma",
								Text = T(890000000013105, --[[ModItemConversation FlagHill_Emma_1 Text voice:Emma section:FlagHill_Emma_1 keyword:Guests]] "Легион снова идёт на виллу — с лагерей и со стороны Эрни. У вас пара часов, чтобы занять позиции. Уйти отсюда сейчас нельзя."),
							}),
						},
						Enabled = false,
						id = "Guests",
					}),
"""

# Enable Guests from Redirect effects
REDIRECT_HOOK = """PlaceObj('PhraseSetEnabled', {
								Conversation = "FlagHill_Emma_1",
								PhraseId = "Guests",
								param_bindings = false,
							}),
"""


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")

    # ModItemCode
    if "System_VillaCounterAttack" not in text:
        needle = """\t\tPlaceObj('ModItemCode', {
\t\t\t'name', "System_JAZZ_VehicleCombat",
\t\t\t'CodeFileName', "Code/System_JAZZ_VehicleCombat.lua",
\t\t}),"""
        insert = needle + """
\t\tPlaceObj('ModItemCode', {
\t\t\t'name', "System_VillaCounterAttack",
\t\t\t'CodeFileName', "Code/System_VillaCounterAttack.lua",
\t\t}),"""
        if needle not in text:
            raise SystemExit("ModItemCode VehicleCombat not found")
        text = text.replace(needle, insert, 1)
        print("added ModItemCode")
    else:
        print("ModItemCode already present")

    # Quest
    if 'id = "Jazz_VillaCounterAttack"' not in text:
        # insert before Ernie_CounterAttack
        idx = text.find('id = "Ernie_CounterAttack"')
        if idx < 0:
            raise SystemExit("Ernie_CounterAttack not found")
        start = text.rfind("PlaceObj('ModItemQuestsDef'", 0, idx)
        text = text[:start] + QUEST + "\n" + text[start:]
        print("added quest")
    else:
        print("quest already present")

    # Guests phrase before Goodbye in FlagHill_Emma_1
    if 'id = "Guests"' not in text or "Jazz_VillaCounterAttack_Start" not in text:
        # Find FlagHill_Emma_1 Goodbye phrase
        emma = text.find('id = "FlagHill_Emma_1"')
        if emma < 0:
            raise SystemExit("FlagHill_Emma_1 missing")
        goodbye = text.find('id = "Goodbye"', emma)
        # find PlaceObj ConversationPhrase for Goodbye - walk back
        phrase_start = text.rfind("PlaceObj('ConversationPhrase'", emma, goodbye)
        if phrase_start < 0:
            raise SystemExit("Goodbye phrase not found")
        text = text[:phrase_start] + GUESTS + "\n" + text[phrase_start:]
        print("added Guests phrase")
    else:
        print("Guests already present")

    # Hook Redirect to enable Guests
    if 'PhraseId = "Guests"' not in text:
        # FlagHill Redirect GiveQuests block
        marker = """GiveQuests = {
							"03A_PresidentNotes",
							"02_LiberateErnie",
						},"""
        # Only first occurrence in FlagHill - search within Emma conversation
        emma = text.find('id = "FlagHill_Emma_1"')
        # Redirect is BEFORE id FlagHill ends - actually Redirect is inside conversation before id line
        # Find GiveQuests near Emma
        pos = text.find(marker)
        if pos < 0:
            raise SystemExit("GiveQuests marker not found")
        # Insert PhraseSetEnabled into Effects of Redirect - find Effects = { before GiveQuests
        effects = text.rfind("Effects = {", 0, pos)
        # Redirect has Effects then Enabled=false then GiveQuests - insert into Effects after opening
        brace = text.find("{", effects)
        insert_at = brace + 1
        text = text[:insert_at] + "\n\t\t\t\t\t\t\t" + REDIRECT_HOOK + text[insert_at:]
        print("hooked Redirect -> Guests")
    else:
        print("Guests PhraseSetEnabled already present")

    # Add PrepTimer var if quest exists without it
    if 'Name = "PrepTimer"' not in text and 'id = "Jazz_VillaCounterAttack"' in text:
        text = text.replace(
            """PlaceObj('QuestVarBool', {
						Name = "SiegeCombat",
					}),
				},
				group = "Ernie",
				id = "Jazz_VillaCounterAttack",""",
            """PlaceObj('QuestVarBool', {
						Name = "SiegeCombat",
					}),
					PlaceObj('QuestVarNum', {
						Name = "PrepTimer",
					}),
				},
				group = "Ernie",
				id = "Jazz_VillaCounterAttack",""",
            1,
        )
        print("added PrepTimer var")

    ITEMS.write_text(text, encoding="utf-8")

    meta = META.read_text(encoding="utf-8")
    if "Code/System_VillaCounterAttack.lua" not in meta:
        meta = meta.replace(
            '"Code/System_JAZZ_VehicleCombat.lua",',
            '"Code/System_JAZZ_VehicleCombat.lua",\n\t\t"Code/System_VillaCounterAttack.lua",',
            1,
        )
        print("metadata.code updated")
    # QuestsDef preset
    if '"Jazz_VillaCounterAttack"' not in meta and "'Jazz_VillaCounterAttack'" not in meta:
        # after Jazz_ClearTheWay
        needle = "'Id', \"Jazz_ClearTheWay\","
        m = meta.find(needle)
        if m < 0:
            print("WARN: Jazz_ClearTheWay meta not found — skip preset")
        else:
            start = meta.rfind("PlaceObj('ModResourcePreset'", 0, m)
            brace = meta.find("{", start)
            depth = 0
            j = brace
            while j < len(meta):
                if meta[j] == "{":
                    depth += 1
                elif meta[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            if meta[j : j + 2] == "),":
                j += 2
            preset = """
		PlaceObj('ModResourcePreset', {
			'Class', "QuestsDef",
			'Id', "Jazz_VillaCounterAttack",
			'ClassDisplayName', "Quests",
		}),
"""
            meta = meta[:j] + preset + meta[j:]
            print("metadata QuestsDef preset added")
    META.write_text(meta, encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
