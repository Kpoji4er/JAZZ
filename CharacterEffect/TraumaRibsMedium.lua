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
				local loss = JazzTraumaRibsApLoss and JazzTraumaRibsApLoss(self, target)
				return value - (loss or self:ResolveValue("APLoss")) * const.Scale.AP
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function(self, target, data)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					data.add = 0
					data.mul = 0
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function(self, target)
				if not JazzTraumaBlocksFreeMove or JazzTraumaBlocksFreeMove(self, target) then
					target:RemoveStatusEffect("FreeMove")
				end
			end,
		}),
	},
	DisplayName = T(890000000010114, "Rib Trauma (Medium)"),
	Description = T(890000000010115, "Start-of-turn AP <color EmStyle>-<APLoss></color>. No Free Move. +2 Pain at the start of the turn. No Tiredness."),
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
