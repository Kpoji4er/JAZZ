UndefineClass('MakeThemBleed')
DefineClass.MakeThemBleed = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= attacker or not data then
					return
				end
				local n = 0
				for _, u in ipairs(attacker:GetVisibleEnemies() or empty_table) do
					if IsValid(u) and not u:IsDead() then
						if u:HasStatusEffect("Bleeding") or u:HasStatusEffect("BleedingMedium") or u:HasStatusEffect("BleedingHeavy") then
							n = n + 1
						end
					end
				end
				local bonus = Min(50, n * 10)
				if bonus > 0 then
					data.damage_percent = (data.damage_percent or 100) + bonus
				end
			end,
		}),
	},
	DisplayName = T(890000000009861, --[[ModItemCharacterEffectCompositeDef MakeThemBleed DisplayName]] "Пусть кровоточат"),
	Description = T(890000000009862, --[[ModItemCharacterEffectCompositeDef MakeThemBleed Description]] "Удары в пах и по животным вызывают кровотечение. +10% урона за каждого врага с кровотечением в зоне видимости (макс. +50%)."),
	Icon = "UI/Icons/Perks/MakeThemBleed",
	Tier = "Personal",
}
