UndefineClass('Jazz_MiguelAuraDown')
DefineClass.Jazz_MiguelAuraDown = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker then
					return
				end
				ApplyCthModifier_Add(self, data, -15)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "StatusEffectAdded",
			Handler = function (self, target, id)
				if id ~= self.class then
					return
				end
				if type(target.WillPoints) == "number" then
					target.WillPoints = Max(0, target.WillPoints - 30)
				end
			end,
		}),
	},
	DisplayName = T(890000000009897, --[[ModItemCharacterEffectCompositeDef Jazz_MiguelAuraDown DisplayName]] "Команданте (−)"),
	Description = T(890000000009898, --[[ModItemCharacterEffectCompositeDef Jazz_MiguelAuraDown Description]] "−15 CTH и −30 Will, пока Мигель сбит в ауре."),
	Icon = "UI/Hud/Status effects/injured",
	type = "Debuff",
	lifetime = "Until End of Turn",
	RemoveOnEndCombat = true,
	Shown = true,
}
