UndefineClass('Jazz_Perk_Static')
DefineClass.Jazz_Perk_Static = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "parts_per_level",
			'Value', 5,
			'Tag', "<parts_per_level>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "parts_cap",
			'Value', 25,
			'Tag', "<parts_cap>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000004100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Static DisplayName]] "Собрал на коленке"),
	Description = T(890000000004101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Static Description]] "Ремонт и крафт Статика стоят на −5% Parts за уровень (макс. −25%)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Static.png",
	Tier = "Personal",
}
