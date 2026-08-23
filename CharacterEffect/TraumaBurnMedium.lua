UndefineClass('TraumaBurnMedium')
DefineClass.TraumaBurnMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Burn")
				return value
			end,
		}),
	},
	DisplayName = T(890000000010126, "Burn Trauma (Medium)"),
	Description = T(890000000010127, "Moderate burn. +2 Pain on exertion."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaBurnMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
