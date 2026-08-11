UndefineClass('MakeThemBleed')
DefineClass.MakeThemBleed = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if type(Jazz_MakeThemBleedSyncBuff) == "function" then
					Jazz_MakeThemBleedSyncBuff(target)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= attacker or not data then
					return
				end
				local n = 0
				if type(Jazz_MakeThemBleedCountVisible) == "function" then
					n = Jazz_MakeThemBleedCountVisible(attacker) or 0
				end
				local bonus = Min(50, n * 10)
				if bonus > 0 then
					data.damage_percent = (data.damage_percent or 100) + bonus
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				-- Refresh after Flay's attack (bleed may have been applied).
				if target == attacker and type(Jazz_MakeThemBleedSyncBuff) == "function" then
					Jazz_MakeThemBleedSyncBuff(attacker)
				end
			end,
		}),
	},
	DisplayName = T(890000000009861, --[[ModItemCharacterEffectCompositeDef MakeThemBleed DisplayName]] "Пусть кровоточат"),
	Description = T(890000000009862, --[[ModItemCharacterEffectCompositeDef MakeThemBleed Description]] "Удары в пах и по животным вызывают кровотечение. +10% урона за каждого врага с кровотечением в зоне видимости (макс. +50%)."),
	Icon = "UI/Icons/Perks/MakeThemBleed",
	Tier = "Personal",
}
