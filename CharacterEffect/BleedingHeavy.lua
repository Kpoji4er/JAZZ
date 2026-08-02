UndefineClass('BleedingHeavy')
DefineClass.BleedingHeavy = {
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
	DisplayName = T(890000000010004, "Heavy Bleeding"),
	Description = T(890000000010005, "Heavy bleeding: <color EmStyle>12 HP</color> per stack each turn. From expanding ammo or worsened moderate bleeding. Bandage reduces one stack to moderate."),
	AddEffectText = T(890000000010006, "<color EmStyle><DisplayName></color>"),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/BleedingHeavy.png",
	max_stacks = 8,
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
