UndefineClass('TraumaArmsMedium')
DefineClass.TraumaArmsMedium = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 20,
			'Tag', "<cth_penalty>%",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Arms")
				end
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
	},
	DisplayName = T(890000000009228, "Arm Trauma (Medium)"),
	Description = T(890000000009229, "Accuracy penalty <color EmStyle><cth_penalty>%</color>. Pain when using arms."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaArmsMedium.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
