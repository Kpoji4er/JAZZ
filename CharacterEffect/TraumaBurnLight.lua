UndefineClass('TraumaBurnLight')
DefineClass.TraumaBurnLight = {
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
	DisplayName = T(890000000010124, "Burn Trauma (Light)"),
	Description = T(890000000010125, "Lingering burn after fire. Pain on exertion. Bandage does not clear burns."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaBurnLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
