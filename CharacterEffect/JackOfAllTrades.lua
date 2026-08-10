UndefineClass('JackOfAllTrades')
DefineClass.JackOfAllTrades = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		-- Vanilla id: SectorOperation.ProgressPerTick reads this via CharacterEffectDefs.
		-- Renaming to jazz_ops_bonus broke MulDivRound (nil) on every Wolf op assign.
		PlaceObj('PresetParamPercent', {
			'Name', "activityDurationMod",
			'Value', 33,
			'Tag', "<activityDurationMod>%",
		}),
	},
	DisplayName = T(890000000006506, --[[ModItemCharacterEffectCompositeDef JackOfAllTrades DisplayName]] "Мастер на все руки"),
	Description = T(890000000006507, --[[ModItemCharacterEffectCompositeDef JackOfAllTrades Description]] "Любые спутниковые операции выполняются примерно на <em>33% быстрее</em>."),
	Icon = "UI/Icons/Perks/JackOfAllTrades",
	Tier = "Personal",
}
