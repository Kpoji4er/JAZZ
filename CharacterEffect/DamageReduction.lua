UndefineClass('DamageReduction')
DefineClass.DamageReduction = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(890000000000257, --[[ModItemCharacterEffectCompositeDef DamageReduction DisplayName]] "Падение скорости пули"),
	Description = "",
	OnAdded = function (self, obj)  end,
	type = "Debuff",
	lifetime = "Until End of Turn",
	Icon = "Mod/e6L4ECj/Icons/MarkedTraccers.png",
	max_stacks = 5,
	RemoveOnEndCombat = true,
}

