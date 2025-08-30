UndefineClass('Weight_1Class')
DefineClass.Weight_1Class = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(355508047345, --[[ModItemCharacterEffectCompositeDef Weight_1Class DisplayName]] "Вес брони (1 Класс)"),
	Description = T(538937825340, --[[ModItemCharacterEffectCompositeDef Weight_1Class Description]] "ОД и ОД свободного перемещения уменьшены. Чем больше уровень, тем больше дебафов"),
	AddEffectText = "",
	OnAdded = function (self, obj)  end,
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/none_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}

