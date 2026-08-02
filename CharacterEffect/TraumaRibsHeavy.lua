UndefineClass('TraumaRibsHeavy')
DefineClass.TraumaRibsHeavy = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
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
	DisplayName = T(890000000010116, "Rib Trauma (Heavy)"),
	Description = T(890000000010117, "Start-of-turn AP <color EmStyle>-<APLoss></color>. Combat-ineffective. Pain rises each turn. No Tiredness."),
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
