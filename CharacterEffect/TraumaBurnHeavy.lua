UndefineClass('TraumaBurnHeavy')
DefineClass.TraumaBurnHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Burn")
				return value
			end,
		}),
	},
	DisplayName = T(890000000010128, "Burn Trauma (Heavy)"),
	Description = T(890000000010129, "Severe burn debt. +3 Pain on exertion; +1 Pain/turn if unused. Infection/hospital clear deferred."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaBurnHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
