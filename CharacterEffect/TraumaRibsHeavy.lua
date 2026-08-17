UndefineClass('TraumaRibsHeavy')
DefineClass.TraumaRibsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 5,
			'Tag', "<APLoss>",
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
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				JazzTraumaPainOnZoneUse(target, "Ribs")
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
	DisplayName = T(890000000010116, "Rib Trauma (Heavy)"),
	Description = T(890000000010117, "Start-of-turn AP <color EmStyle>-<APLoss></color>. Combat-ineffective. +3 Pain at turn start; +1 Pain/turn if unused. No Tiredness."),
	OnAdded = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function(self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaRibsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
