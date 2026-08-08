UndefineClass('Jazz_Perk_Carlos')
DefineClass.Jazz_Perk_Carlos = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "detection_reduction",
			'Value', 33,
			'Tag', "<detection_reduction>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "keep_hidden_chance",
			'Value', 50,
			'Tag', "<keep_hidden_chance>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000005052, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Carlos DisplayName]] "Тихая тень"),
	Description = T(890000000005053, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Carlos Description]] "Обнаружение идёт на 33% медленнее. Провал скрытого убийства с 50% шансом оставляет Hidden."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Carlos.png",
	Tier = "Personal",
}
