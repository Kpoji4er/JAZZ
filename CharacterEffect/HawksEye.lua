UndefineClass('HawksEye')
DefineClass.HawksEye = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "pindownCostOverwrite",
			'Value', 1,
			'Tag', "<pindownCostOverwrite>",
		}),
	},
	DisplayName = T(890000000009869, --[[ModItemCharacterEffectCompositeDef HawksEye DisplayName]] "Ястребиный глаз"),
	Description = T(890000000009870, --[[ModItemCharacterEffectCompositeDef HawksEye Description]] "Pin Down / Focus Fire стоит 1 ОД. Снайперские атаки дают вдвое больше подавления. Печенье прилагается."),
	Icon = "UI/Icons/Perks/HawksEye",
	Tier = "Personal",
}
