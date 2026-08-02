UndefineClass('TraumaLegsHeavy')
DefineClass.TraumaLegsHeavy = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "move_ap_modifier",
			'Value', 150,
			'Tag', "<move_ap_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzTraumaHeavyPainRamp(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function(self, target, value, action)
				if self.class == "TraumaLegsMedium" then
					JazzTraumaPainOnZoneUse(target, "Legs")
				end
				return value + self:ResolveValue("move_ap_modifier")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function(self, target, data)
				data.add = 0
				data.mul = 0
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function(self, target)
				target:RemoveStatusEffect("FreeMove")
			end,
		}),
	},
	DisplayName = T(890000000010110, "Leg Trauma (Heavy)"),
	Description = T(890000000010111, "Move cost <color EmStyle>+<move_ap_modifier>%</color>. Almost immobile. Pain rises each turn."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
