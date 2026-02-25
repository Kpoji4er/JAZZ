UndefineClass('Weight_5Class')
DefineClass.Weight_5Class = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(410074002761, "Вес брони (5 Класс)"),
	Description = T(549247357132, "ОД и ОД свободного перемещения уменьшены. Чем больше уровень, тем больше дебафов"),
	AddEffectText = "",
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/super-heavy_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}

