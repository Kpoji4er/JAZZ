UndefineClass('Jazz_Perk_Madman')
DefineClass.Jazz_Perk_Madman = {
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
				if not IsKindOf(attack_target, "Unit") then
					return
				end
				local is_kill = attack_target:IsDead()
				if not is_kill and results.killed_units then
					for _, u in ipairs(results.killed_units) do
						if u == attack_target then
							is_kill = true
							break
						end
					end
				end
				if not is_kill then
					return
				end
				if DivRound(attacker:GetDist(attack_target), const.SlabSizeX) <= 1 then
					attacker:AddStatusEffect("Inspired")
				end
			end,
		}),
	},
	DisplayName = T(890000000002100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Madman DisplayName]] "Штурм в упор"),
	Description = T(890000000002101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Madman Description]] "Убийство в упор (дистанция 1 клетка) даёт Воодушевление."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Madman.png",
	Tier = "Personal",
}
