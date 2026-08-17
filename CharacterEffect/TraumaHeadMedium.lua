UndefineClass('TraumaHeadMedium')
DefineClass.TraumaHeadMedium = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 15,
			'Tag', "<cth_penalty>%",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "sight_modifier",
			'Value', -20,
			'Tag', "<sight_modifier>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Head")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					local pen = JazzTraumaHeadCthPenalty and JazzTraumaHeadCthPenalty(self, attacker)
					ApplyCthModifier_Add(self, data, -(pen or self:ResolveValue("cth_penalty")))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcSightModifier",
			Handler = function(self, target, value, observer, other, step_pos, darkness)
				if target == observer then
					local sight = JazzTraumaHeadSightModifier and JazzTraumaHeadSightModifier(self, target)
					return value + (sight or self:ResolveValue("sight_modifier"))
				end
			end,
		}),
	},
	DisplayName = T(890000000010120, "Head Trauma (Medium)"),
	Description = T(890000000010121, "Sight and accuracy penalties. +2 Pain when aiming or firing."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaHeadMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
