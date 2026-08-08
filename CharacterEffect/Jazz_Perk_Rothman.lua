UndefineClass('Jazz_Perk_Rothman')
DefineClass.Jazz_Perk_Rothman = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "mine_bonus_base",
			'Value', 10,
			'Tag', "<mine_bonus_base>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "mine_bonus_loyalty_span",
			'Value', 30,
			'Tag', "<mine_bonus_loyalty_span>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000002431, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Rothman DisplayName]] "Я вас научу работать!"),
	Description = T(890000000002432, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Rothman Description]] "Пока Ротман в секторе с шахтой: доход шахты +10…+40% (сильнее при низкой loyalty)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Rothman.png",
	Tier = "Personal",
}
