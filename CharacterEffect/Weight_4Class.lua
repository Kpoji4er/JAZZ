UndefineClass('Weight_4Class')
DefineClass.Weight_4Class = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(617262153487, --[[ModItemCharacterEffectCompositeDef Weight_4Class DisplayName]] "Вес брони (4 Класс)"),
	Description = T(197266793683, --[[ModItemCharacterEffectCompositeDef Weight_4Class Description]] "ОД и ОД свободного перемещения уменьшены. Чем больше уровень, тем больше дебафов"),
	AddEffectText = "",
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/heavy_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}

