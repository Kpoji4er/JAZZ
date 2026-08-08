UndefineClass('Jazz_Perk_Madman')
DefineClass.Jazz_Perk_Madman = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "will_drain",
			'Value', 10,
			'Tag', "<will_drain>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "radius",
			'Value', 5,
			'Tag', "<radius>",
		}),
	},
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
				local is_kill = attack_target:IsDead()
				if not is_kill and results.killed_units then
					for _, u in ipairs(results.killed_units) do
						if u == attack_target then
							is_kill = true
							break
						end
					end
				end
				local is_crit = results.crit or results.high_accuracy
				if not is_kill and not is_crit then
					return
				end
				if type(Jazz_MadmanDrainWill) == "function" then
					Jazz_MadmanDrainWill(attacker)
				end
			end,
		}),
	},
	DisplayName = T(890000000002100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Madman DisplayName]] "Бешеный пес"),
	Description = T(890000000002101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Madman Description]] "Критический удар или убийство в ближнем бою снижает силу воли всех в радиусе 5 клеток на 10 (включая союзников)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Madman.png",
	Tier = "Personal",
}
