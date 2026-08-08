UndefineClass('Jazz_Perk_Vince')
DefineClass.Jazz_Perk_Vince = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "med_skip_chance",
			'Value', 25,
			'Tag', "<med_skip_chance>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "med_amount_mul",
			'Value', 75,
			'Tag', "<med_amount_mul>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000005029, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vince DisplayName]] "Дефицит ресурсов"),
	Description = T(890000000005030, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vince Description]] "Пока Винс в отряде, расход аптечек и медикаментов снижен примерно на 25% (шанс не потратить заряд)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Vince.png",
	Tier = "Personal",
}
