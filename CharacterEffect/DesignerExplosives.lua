UndefineClass('DesignerExplosives')
DefineClass.DesignerExplosives = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "craft_discount",
			'Value', 30,
			'Tag', "<craft_discount>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000009885, --[[ModItemCharacterEffectCompositeDef DesignerExplosives DisplayName]] "Конструктор взрывчатки"),
	Description = T(890000000009886, --[[ModItemCharacterEffectCompositeDef DesignerExplosives Description]] "Может крафтить гранаты. Крафт патронов/гранат стоит на 30% меньше Parts."),
	Icon = "UI/Icons/Perks/DesignerExplosives",
	Tier = "Personal",
}
