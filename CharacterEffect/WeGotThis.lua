UndefineClass('WeGotThis')
DefineClass.WeGotThis = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results then
					return
				end
				local killed = false
				if results.killed_units then
					for _, u in ipairs(results.killed_units) do
						if IsValid(u) then
							killed = true
							break
						end
					end
				end
				if not killed and IsKindOf(attack_target, "Unit") and attack_target:IsDead() then
					killed = true
				end
				if not killed then
					return
				end
				for _, ally in ipairs(attacker.team and attacker.team.units or empty_table) do
					if IsValid(ally) and not ally:IsDead() then
						ally:ApplyTempHitPoints(10)
					end
				end
			end,
		}),
	},
	DisplayName = T(890000000006502, --[[ModItemCharacterEffectCompositeDef WeGotThis DisplayName]] "Мы справимся"),
	Description = T(890000000006503, --[[ModItemCharacterEffectCompositeDef WeGotThis Description]] "После убийства весь отряд получает <em>+10 Силы воли (Grit)</em>."),
	Icon = "UI/Icons/Perks/WeGotThis",
	Tier = "Personal",
}
