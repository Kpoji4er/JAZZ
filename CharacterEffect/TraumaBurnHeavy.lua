UndefineClass('TraumaBurnHeavy')
DefineClass.TraumaBurnHeavy = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
	},
	DisplayName = T(890000000009254, "Burn Trauma (Heavy)"),
	Description = T(890000000009255, "Severe burn debt. Pain rises each turn. Infection/hospital clear deferred."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaBurnHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
