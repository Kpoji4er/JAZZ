UndefineClass('Jazz_OrderCTH')
DefineClass.Jazz_OrderCTH = {
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
				ApplyCthModifier_Add(self, data, 5)
				target:RemoveStatusEffect("Jazz_OrderCTH")
			end,
		}),
	},
	DisplayName = T(890000000006200, --[[ModItemCharacterEffectCompositeDef Jazz_OrderCTH DisplayName]] "Приказ: точность"),
	Description = T(890000000006201, --[[ModItemCharacterEffectCompositeDef Jazz_OrderCTH Description]] "+5 к шансу попадания на следующую атаку."),
	type = "Buff",
	lifetime = "Until End of Turn",
	Icon = "UI/Hud/Status effects/accuracy",
	RemoveOnEndCombat = true,
	Shown = true,
}
