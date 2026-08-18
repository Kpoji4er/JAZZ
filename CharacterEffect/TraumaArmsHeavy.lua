UndefineClass('TraumaArmsHeavy')
DefineClass.TraumaArmsHeavy = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 50,
			'Tag', "<cth_penalty>%",
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
					ApplyCthModifier_Add(self, data, -JazzTraumaResolveNum(self, attacker, JazzTraumaArmsCthPenalty, "cth_penalty"))
				end
			end,
		}),
	},
	DisplayName = T(890000000010104, "Arm Trauma (Heavy)"),
	Description = T(890000000010105, "Severe accuracy penalty <color EmStyle><cth_penalty>%</color>. Nearly unable to fight. +3 Pain when using arms; +1 Pain/turn if unused."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaArmsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
