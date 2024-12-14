UndefineClass('TakeAim')
DefineClass.TakeAim = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				if id == "SameTarget" and target == attacker then
					data.mod_add = data.mod_add + self:ResolveValue("chanceToHitBonus")
					data.meta_text[#data.meta_text+1] = T{776394275735, "Perk: <name>", name = self.DisplayName}
				end
			end,
		}),
	},
	DisplayName = T(500170452730, --[[ModItemCharacterEffectCompositeDef TakeAim DisplayName]] "Пристрелка"),
	Description = T(518636342491, --[[ModItemCharacterEffectCompositeDef TakeAim Description]] "<color EmStyle>Повторные атаки</color> по одной и той же <color EmStyle>цели</color> получают все больший бонус к <color EmStyle>точности</color>."),
	Icon = "UI/Icons/Perks/TakeAim",
	Tier = "Bronze",
	Stat = "Strength",
	StatValue = 70,
}

