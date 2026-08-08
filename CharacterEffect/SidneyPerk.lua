UndefineClass('SidneyPerk')
DefineClass.SidneyPerk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarted",
			Handler = function (self, target, load_game)
				target:SetEffectValue("Jazz_SidneySmug", true)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if target:GetEffectValue("Jazz_SidneySmug") then
					target:GainAP(2 * const.Scale.AP)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target == attacker and results and results.miss then
					attacker:SetEffectValue("Jazz_SidneySmug", nil)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnDamageTaken",
			Handler = function (self, target, attacker, dmg)
				if dmg and dmg > 0 then
					target:SetEffectValue("Jazz_SidneySmug", nil)
				end
			end,
		}),
	},
	DisplayName = T(890000000009879, --[[ModItemCharacterEffectCompositeDef SidneyPerk DisplayName]] "Самодовольство"),
	Description = T(890000000009880, --[[ModItemCharacterEffectCompositeDef SidneyPerk Description]] "+2 ОД в начале хода, пока не промахнётся и не получит урон."),
	Icon = "UI/Icons/Perks/SidneyPerk",
	Tier = "Personal",
}
