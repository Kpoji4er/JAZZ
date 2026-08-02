UndefineClass('TraumaRibsLight')
DefineClass.TraumaRibsLight = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Ribs")
				return value
			end,
		}),
	},
	DisplayName = T(890000000009238, "Rib Trauma (Light)"),
	Description = T(890000000009239, "Pain when exerting. No Tiredness from ribs. No direct AP penalty."),
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
