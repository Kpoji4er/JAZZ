UndefineClass('Jazz_Perk_Blade')
DefineClass.Jazz_Perk_Blade = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker and action and action.ActionType == "Melee Attack" then
					ApplyCthModifier_Add(self, data, 20)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcCritChance",
			Handler = function (self, target, attacker, attack_target, action, weapon, data)
				if target == attacker and action and action.ActionType == "Melee Attack" then
					data.crit_chance = 0
				end
			end,
		}),
	},
	DisplayName = T(890000000001800, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Blade DisplayName]] "Ураган клинков"),
	Description = T(890000000001801, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Blade Description]] "Атаки ближнего боя: +20 к шансу попадания, критические удары невозможны."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Blade.png",
	Tier = "Personal",
}
