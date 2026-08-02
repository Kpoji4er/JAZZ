UndefineClass('TraumaRibsMedium')
DefineClass.TraumaRibsMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 2,
			'Tag', "<APLoss>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				if self.class == "TraumaRibsMedium" then
					JazzTraumaPainOnZoneUse(target, "Ribs")
				end
				return value - self:ResolveValue("APLoss") * const.Scale.AP
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
	DisplayName = T(890000000010114, "Rib Trauma (Medium)"),
	Description = T(890000000010115, "Start-of-turn AP <color EmStyle>-<APLoss></color>. No Free Move. Pain at the start of the turn. No Tiredness."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
