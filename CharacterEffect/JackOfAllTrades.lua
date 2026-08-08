UndefineClass('JackOfAllTrades')
DefineClass.JackOfAllTrades = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "jazz_ops_bonus",
			'Value', 33,
			'Tag', "<jazz_ops_bonus>%",
		}),
	},
	DisplayName = T(890000000006506, --[[ModItemCharacterEffectCompositeDef JackOfAllTrades DisplayName]] "Мастер на все руки"),
	Description = T(890000000006507, --[[ModItemCharacterEffectCompositeDef JackOfAllTrades Description]] "Любые спутниковые операции выполняются примерно на <em>33% быстрее</em>."),
	Icon = "UI/Icons/Perks/JackOfAllTrades",
	Tier = "Personal",
}
