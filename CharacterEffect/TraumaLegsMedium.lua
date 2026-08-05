UndefineClass('TraumaLegsMedium')
DefineClass.TraumaLegsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "move_ap_modifier",
			'Value', 50,
			'Tag', "<move_ap_modifier>",
		}),
	},
	unit_reactions = {
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
	DisplayName = T(890000000010108, "Leg Trauma (Medium)"),
	Description = T(890000000010109, "Move cost <color EmStyle>+<move_ap_modifier>%</color>. No Free Move / sprint. +2 Pain when moving."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaLegsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
