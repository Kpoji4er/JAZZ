UndefineClass('TraumaLegsLight')
DefineClass.TraumaLegsLight = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function(self, target, value, action)
				JazzTraumaPainOnZoneUse(target, "Legs")
				return value
			end,
		}),
	},
	DisplayName = T(890000000009232, "Leg Trauma (Light)"),
	Description = T(890000000009233, "Pain when moving. No direct move-cost penalty."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
