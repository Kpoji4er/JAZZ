UndefineClass('Jazz_Perk_Ricochet')
DefineClass.Jazz_Perk_Ricochet = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results or results.miss then
					return
				end
				if not action or action.ActionType ~= "Melee Attack" then
					return
				end
				if not IsKindOf(attack_target, "Unit") then
					return
				end
				local dmg = results.total_damage or results.dealt_damage or 0
				if type(dmg) ~= "number" or dmg <= 0 then
					return
				end
				local splash = Max(1, MulDivRound(dmg, 35, 100))
				local slab = const.SlabSizeX
				for _, u in ipairs(g_Units or empty_table) do
					if IsValid(u) and u ~= attack_target and not u:IsDead() and attacker:IsOnEnemySide(u) then
						if DivRound(attack_target:GetDist(u), slab) <= 1 then
							u:TakeDirectDamage(splash)
							break
						end
					end
				end
			end,
		}),
	},
	DisplayName = T(890000000004600, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Ricochet DisplayName]] "Рикошет"),
	Description = T(890000000004601, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Ricochet Description]] "Ближний бой: часть урона переходит на врага в ≤1 клетке от цели."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Ricochet.png",
	Tier = "Personal",
}
