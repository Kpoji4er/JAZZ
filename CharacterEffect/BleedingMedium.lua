UndefineClass('BleedingMedium')
DefineClass.BleedingMedium = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzBleedOnUnitEndTurn(target)
			end,
		}),
	},
	DisplayName = T(890000000010001, "Moderate Bleeding"),
	Description = T(890000000010002, "Moderate bleeding: <color EmStyle>6 HP</color> per stack each turn. Bandage reduces one stack to light bleeding."),
	AddEffectText = T(890000000010003, "<color EmStyle><DisplayName></color>"),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/BleedingMedium.png",
	max_stacks = 8,
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
