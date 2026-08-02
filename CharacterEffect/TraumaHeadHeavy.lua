UndefineClass('TraumaHeadHeavy')
DefineClass.TraumaHeadHeavy = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 40,
			'Tag', "<cth_penalty>%",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "sight_modifier",
			'Value', -50,
			'Tag', "<sight_modifier>",
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
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcSightModifier",
			Handler = function(self, target, value, observer, other, step_pos, darkness)
				if target == observer then
					return value + self:ResolveValue("sight_modifier")
				end
			end,
		}),
	},
	DisplayName = T(890000000010122, "Head Trauma (Heavy)"),
	Description = T(890000000010123, "Severe sight/accuracy loss. Nearly combat-ineffective. Pain rises each turn."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaHeadHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
