UndefineClass('Jazz_Perk_Shank')
DefineClass.Jazz_Perk_Shank = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attack_target and action and action.ActionType == "Melee Attack" then
					ApplyCthModifier_Add(self, data, -50)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attack_target then
					return
				end
				if not results or not results.miss then
					return
				end
				if not action or action.ActionType ~= "Melee Attack" then
					return
				end
				if not IsKindOf(attacker, "Unit") or attacker:IsDead() then
					return
				end
				if DivRound(attack_target:GetDist(attacker), const.SlabSizeX) > 8 then
					return
				end
				local knife
				attack_target:ForEachItemInSlot("Handheld A", "MeleeWeapon", function(item)
					if not knife then knife = item end
				end)
				if not knife then
					attack_target:ForEachItemInSlot("Handheld B", "MeleeWeapon", function(item)
						if not knife then knife = item end
					end)
				end
				if knife and CombatActions and CombatActions.KnifeThrow and CombatActions.KnifeThrow.Run then
					CombatActions.KnifeThrow:Run(attack_target, { target = attacker, weapon = knife })
				end
			end,
		}),
	},
	DisplayName = T(890000000005056, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Shank DisplayName]] "Не подходи ко мне!"),
	Description = T(890000000005057, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Shank Description]] "50% защита в ближнем бою. При промахе по Шенку он отбрасывает нож, если цель в 8 клетках."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Shank.png",
	Tier = "Personal",
}
