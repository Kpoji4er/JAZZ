UndefineClass('MarkedTraccers')
DefineClass.MarkedTraccers = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				return value - 1
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				target:RemoveStatusEffect(self.class)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				local effect = target:GetStatusEffect("MarkedTraccers")
				local count = 1
												if effect then
												 	count = effect.stacks 
												end
				
				if target == attacker then
					ApplyCthModifier_Add(self, data, count * self:ResolveValue("accuracy_modifier"))
				end
			end,
		}),
	},
	DisplayName = T(279226942480, --[[ModItemCharacterEffectCompositeDef MarkedTraccers DisplayName]] "Помечен Трассерами"),
	Description = T(697150397247, --[[ModItemCharacterEffectCompositeDef MarkedTraccers Description]] "Незначительное повышение шанса попадания за каждый уровень эффекта"),
	AddEffectText = T(551437047571, --[[ModItemCharacterEffectCompositeDef MarkedTraccers AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)  end,
	type = "Debuff",
	lifetime = "Until End of Turn",
	Icon = "Mod/e6L4ECj/Icons/MarkedTraccers.png",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
}

