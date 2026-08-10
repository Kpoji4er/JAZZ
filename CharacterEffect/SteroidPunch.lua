UndefineClass('SteroidPunch')
DefineClass.SteroidPunch = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				-- Successful fist / melee weapon hits → KnockDown + Unconscious.
				if target ~= attacker or not results or results.miss then
					return
				end
				if not action or action.ActionType ~= "Melee Attack" then
					return
				end
				if not IsKindOf(attack_target, "Unit") or attack_target:IsDead() then
					return
				end
				attack_target:AddStatusEffect("KnockDown")
				attack_target:AddStatusEffect("Unconscious")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcStimmedTiredness",
			Handler = function (self, target, value)
				-- Combat stims: no Energy / Tiredness loss when Stimmed wears off.
				return 0
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				-- Also clear Stimmed accuracy penalty (vanilla “negative stim effects”).
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
				-- Instant fire hits: −30% damage taken (Burning DoT is wrapped separately).
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
					data.damage_percent = MulDivRound(data.damage_percent or 100, 70, 100)
				end
			end,
		}),
	},
	DisplayName = T(890000000009930, --[[ModItemCharacterEffectCompositeDef SteroidPunch DisplayName]] "Удар анаболика"),
	Description = T(890000000009931, --[[ModItemCharacterEffectCompositeDef SteroidPunch Description]] "Пассивный навык. Точность всех ударов кулаками и оружием ближнего боя зависит от <em>Силы</em> вместо Ловкости. Успешные удары кулаками и оружием ближнего боя дают <em>Нокдаун</em> и <em>Без сознания</em>. Стимуляторы не вызывают потери <em>энергии</em> (усталости). Урон со временем от эффекта <em>горения</em> снижен на <em>30%</em>."),
	Icon = "UI/Icons/Perks/SteroidPunch",
	Tier = "Personal",
}
