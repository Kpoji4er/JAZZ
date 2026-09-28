UndefineClass('KillingWind')
DefineClass.KillingWind = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker then
					return
				end
				-- Aggregate firearm grit: ExecFirearmAttacks after all OnAttack; CE for melee/other.
				if type(Jazz_KillingWindTryGrit) == "function" then
					Jazz_KillingWindTryGrit(attacker, results)
				end
			end,
		}),
	},
	DisplayName = T(890000000009875, --[[ModItemCharacterEffectCompositeDef KillingWind DisplayName]] "Убийственный ветер"),
	Description = T(890000000009876, --[[ModItemCharacterEffectCompositeDef KillingWind Description]] "При попадании по ≥2 врагам: +<gritPerEnemyHit> Grit за каждого. Ещё −50% штрафа Free Move от брони (вместе с Железной кожей — без штрафа FM от брони). Громоздкое оружие не лишает Free Move."),
	Icon = "UI/Icons/Perks/KillingWind",
	Tier = "Personal",
}

