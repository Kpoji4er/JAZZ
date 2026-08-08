UndefineClass('Jazz_CombatMedicBuff')
DefineClass.Jazz_CombatMedicBuff = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, 15)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcCritChance",
			Handler = function (self, target, attacker, attack_target, action, weapon, data)
				if target == attacker and data then
					data.crit_chance = (data.crit_chance or 0) + 15
				end
			end,
		}),
	},
	DisplayName = T(890000000006220, --[[ModItemCharacterEffectCompositeDef Jazz_CombatMedicBuff DisplayName]] "Боевой медик"),
	Description = T(890000000006221, --[[ModItemCharacterEffectCompositeDef Jazz_CombatMedicBuff Description]] "+15 к шансу попадания и критическому удару до конца следующего хода."),
	type = "Buff",
	lifetime = "Until End of Next Turn",
	Icon = "UI/Hud/Status effects/accuracy",
	RemoveOnEndCombat = true,
	Shown = true,
}
