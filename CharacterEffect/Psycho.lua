UndefineClass('Psycho')
DefineClass.Psycho = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function (self, target, attacker, attack_target, action, attack_args)
				if target == attacker and (action.id == "SingleShot" or action.id == "BurstFire") then
					if attacker:Random(100) < self:ResolveValue("procChance") then
						local weapon = action:GetAttackWeapons(attacker)
						if action.id == "SingleShot" and table.find(weapon.AvailableAttacks, "BurstFire") then
							attack_args.replace_action = "BurstFire"
							PlayVoiceResponse(attacker, "Psycho")
						elseif action.id == "BurstFire" and table.find(weapon.AvailableAttacks, "AutoFire") then
							attack_args.replace_action = "AutoFire"
							PlayVoiceResponse(attacker, "Psycho")
						end
					end
				end
			end,
		}),
	},
	DisplayName = T(256373672615, --[[ModItemCharacterEffectCompositeDef Psycho DisplayName]] "Психопат"),
	Description = T(966163673727, --[[ModItemCharacterEffectCompositeDef Psycho Description]] "Может выполнить более жестокую атаку, чем была выбрана.\n\nОткрывает дополнительные <em>варианты диалогов</em>."),
	Icon = "UI/Icons/Perks/Psycho",
	Tier = "Personality",
}

