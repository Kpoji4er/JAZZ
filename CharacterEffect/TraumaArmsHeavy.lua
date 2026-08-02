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
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, -self:ResolveValue("cth_penalty"))
				end
			end,
		}),
	},
	DisplayName = T(890000000010104, "Arm Trauma (Heavy)"),
	Description = T(890000000010105, "Severe accuracy penalty <color EmStyle><cth_penalty>%</color>. Nearly unable to fight. Pain rises each turn."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaArmsHeavy.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
