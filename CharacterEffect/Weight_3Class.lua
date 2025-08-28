UndefineClass('Weight_3Class')
DefineClass.Weight_3Class = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(696428661966, "Вес брони (3 Класс)"),
	Description = T(806830590860, "ОД и ОД свободного перемещения уменьшены. Чем больше уровень, тем больше дебафов"),
	AddEffectText = "",
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/medium_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}

