UndefineClass('SteroidPunch')
DefineClass.SteroidPunch = {
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
				if not IsKindOf(attack_target, "Unit") or attack_target:IsDead() then
					return
				end
				local is_crit = results.crit or results.high_accuracy
				if not is_crit then
					-- Also accept per-hit critical flags when present.
					for _, hit in ipairs(results or empty_table) do
						if type(hit) == "table" and hit.critical then
							is_crit = true
							break
						end
					end
				end
				if not is_crit and results.hits then
					for _, hit in ipairs(results.hits) do
						if hit and hit.critical then
							is_crit = true
							break
						end
					end
				end
				if not is_crit then
					return
				end
				-- Unconscious implies incapacitated/prone handling in engine.
				attack_target:AddStatusEffect("Unconscious")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				-- No Stimmed accuracy penalty while Steroid holds the perk.
				if target ~= attacker then
					return
				end
				if id == "Stimmed" or id == "Stim" then
					data.mod_add = 0
					data.mod_mul = 100
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				-- Take 30% fire damage (Burning ticks / fire hits on Steroid as defender).
				if owner ~= target or not data then
					return
				end
				local from_fire = false
				if hit and (hit.fire or hit.burning) then
					from_fire = true
				end
				if action and (action.id == "Burning" or action.ActionType == "Fire") then
					from_fire = true
				end
				if weapon and IsKindOf(weapon, "FireSurface") then
					from_fire = true
				end
				if from_fire then
					data.damage_percent = MulDivRound(data.damage_percent or 100, 30, 100)
				end
			end,
		}),
	},
	DisplayName = T(890000000006512, --[[ModItemCharacterEffectCompositeDef SteroidPunch DisplayName]] "Удар анаболика"),
	Description = T(890000000006513, --[[ModItemCharacterEffectCompositeDef SteroidPunch Description]] "Точность всего ближнего боя считается от <em>Силы</em>. Критический удар в ближнем бою валит цель (<em>Нокаут</em>). Нет штрафа от стимуляторов. От огня получает только <em>30%</em> урона."),
	Icon = "UI/Icons/Perks/SteroidPunch",
	Tier = "Personal",
}
