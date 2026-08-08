UndefineClass('NailsPerk')
DefineClass.NailsPerk = {
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
				if self:ResolveValue("bloodthirst") then
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
				if killed then
					self:SetParameter("bloodthirst", true)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				self:SetParameter("bloodthirst", nil)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarting",
			Handler = function (self, target)
				self:SetParameter("bloodthirst", nil)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarted",
			Handler = function (self, target, load_game)
				self:SetParameter("bloodthirst", nil)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= attacker or not data then
					return
				end
				if self:ResolveValue("bloodthirst") then
					data.damage_percent = (data.damage_percent or 100) + 20
				end
			end,
		}),
	},
	DisplayName = T(890000000006504, --[[ModItemCharacterEffectCompositeDef NailsPerk DisplayName]] "Гвоздь в цель"),
	Description = T(890000000006505, --[[ModItemCharacterEffectCompositeDef NailsPerk Description]] "После первого убийства в бою все атаки наносят <em>+20% урона</em> до конца боя."),
	Icon = "UI/Icons/Perks/NailsPerk",
	Tier = "Personal",
}
