UndefineClass('Spotter')
DefineClass.Spotter = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not action then
					return
				end
				if action.id == "PinDown" and IsKindOf(attack_target, "Unit") and not attack_target:IsDead() then
					attack_target:AddStatusEffect("Marked")
					attack_target:SetEffectValue("Jazz_SpotterCritPending", true)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcCritChance",
			Handler = function (self, target, attacker, attack_target, action, weapon, data)
				if target ~= attacker or not data or not IsKindOf(attack_target, "Unit") then
					return
				end
				if attack_target:GetEffectValue("Jazz_SpotterCritPending") then
					data.crit_chance = 100
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if not IsKindOf(attack_target, "Unit") then
					return
				end
				if attack_target:GetEffectValue("Jazz_SpotterCritPending") and results and not results.miss then
					-- Consume after a resolved hit by anyone.
					local hits = results.hits or results
					local hit_ok = results.crit or results.high_accuracy
					if not hit_ok then
						for _, hit in ipairs(results.hits or empty_table) do
							if hit and not hit.miss then
								hit_ok = true
								break
							end
						end
					end
					if hit_ok then
						attack_target:SetEffectValue("Jazz_SpotterCritPending", nil)
					end
				end
			end,
		}),
	},
	DisplayName = T(890000000009871, --[[ModItemCharacterEffectCompositeDef Spotter DisplayName]] "Наводчик"),
	Description = T(890000000009872, --[[ModItemCharacterEffectCompositeDef Spotter Description]] "Pin Down помечает цель (Marked). Следующее попадание по помеченной цели — гарантированный крит."),
	Icon = "UI/Icons/Perks/Spotter",
	Tier = "Personal",
}
