UndefineClass('Jazz_Perk_Nervous')
DefineClass.Jazz_Perk_Nervous = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results or not action then
					return
				end
				local aid = action.id or ""
				local is_auto = aid == "BurstFire" or aid == "AutoFire" or aid == "MGBurstFire"
					or aid == "Fanning" or string.find(aid, "AutoFire", 1, true) or string.find(aid, "Burst", 1, true)
				if not is_auto then
					return
				end
				local hits = 0
				if results.hit_objs then
					hits = #(results.hit_objs) 
				elseif not results.miss then
					hits = 1
				end
				if results.killed_units then
					-- keep hit count from bullets if available
				end
				if type(results.shots) == "table" then
					hits = 0
					for _, sh in ipairs(results.shots) do
						if sh and not sh.miss then
							hits = hits + 1
						end
					end
				end
				attacker:SetEffectValue("Jazz_NervousBonusShots", Clamp(hits, 0, 10))
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target:SetEffectValue("Jazz_NervousBonusShots", nil)
			end,
		}),
	},
	DisplayName = T(890000000002900, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Nervous DisplayName]] "Нервный, но азартный"),
	Description = T(890000000002901, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Nervous Description]] "Каждое попадание очереди или автоогня добавляет пулю к следующей очереди (максимум +10)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Nervous.png",
	Tier = "Personal",
}
