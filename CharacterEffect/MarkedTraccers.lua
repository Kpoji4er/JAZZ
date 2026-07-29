UndefineClass('MarkedTraccers')
DefineClass.MarkedTraccers = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(890000000000261, --[[ModItemCharacterEffectCompositeDef MarkedTraccers DisplayName]] "Помечен Трассерами"),
	Description = T(697150397247, --[[ModItemCharacterEffectCompositeDef MarkedTraccers Description]] "Незначительное повышение шанса попадания за каждый уровень эффекта"),
	OnAdded = function (self, obj)  end,
	type = "Debuff",
	lifetime = "Until End of Turn",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/MarkedTraccers.png",
	max_stacks = 5,
	RemoveOnEndCombat = true,
	Shown = true,
}

