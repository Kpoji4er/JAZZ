UndefineClass('DedicatedCamper')
DefineClass.DedicatedCamper = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				target:SetEffectValue("Jazz_CamperOrigin", target:GetPos())
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= attacker or not data then
					return
				end
				local origin = attacker:GetEffectValue("Jazz_CamperOrigin")
				local moved = attack_args and attack_args.unit_moved
				if not moved and origin and attacker:GetPos() == origin then
					data.damage_percent = (data.damage_percent or 100) + 25
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results then
					return
				end
				local dmg = results.total_damage or results.dealt_damage or 0
				if type(dmg) ~= "number" or dmg <= 0 then
					for _, hit in ipairs(results.hits or empty_table) do
						if hit and type(hit.damage) == "number" then
							dmg = dmg + hit.damage
						end
					end
				end
				if dmg >= 25 then
					attacker:ApplyTempHitPoints(15)
				end
			end,
		}),
	},
	DisplayName = T(890000000009863, --[[ModItemCharacterEffectCompositeDef DedicatedCamper DisplayName]] "Оседлый стрелок"),
	Description = T(890000000009864, --[[ModItemCharacterEffectCompositeDef DedicatedCamper Description]] "Пока не сдвинулся с места в этом ходу: +25% урона. Если атака нанесла ≥25 урона — +15 Силы воли (Grit)."),
	Icon = "UI/Icons/Perks/DedicatedCamper",
	Tier = "Personal",
}
