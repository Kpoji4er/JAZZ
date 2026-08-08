UndefineClass('Jazz_Perk_Benny')
DefineClass.Jazz_Perk_Benny = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "lure_range",
			'Value', 8,
			'Tag', "<lure_range>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000009920, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Benny DisplayName]] "Вам посылка"),
	Description = T(890000000009921, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Benny Description]] "Актив: приманка-декой ≤8 (цель с низким Will); взрыв при подходе. CombatAction soft-cut — helpers готовы."),
	Icon = "UI/Icons/Perks/DesignerExplosives",
	Tier = "Personal",
}
