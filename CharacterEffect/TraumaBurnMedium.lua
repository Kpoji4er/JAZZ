UndefineClass('TraumaBurnMedium')
DefineClass.TraumaBurnMedium = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Burn")
				return value
			end,
		}),
	},
	DisplayName = T(890000000009252, "Burn Trauma (Medium)"),
	Description = T(890000000009253, "Moderate burn debt. Pain on exertion. Infection risk deferred."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaBurnMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
