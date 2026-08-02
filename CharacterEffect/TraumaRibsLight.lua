UndefineClass('TraumaRibsLight')
DefineClass.TraumaRibsLight = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Ribs")
				return value
			end,
		}),
	},
	DisplayName = T(890000000010112, "Rib Trauma (Light)"),
	Description = T(890000000010113, "Pain at the start of the turn."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
