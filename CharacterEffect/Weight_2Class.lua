UndefineClass('Weight_2Class')
DefineClass.Weight_2Class = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {},
	DisplayName = T(118150789498, --[[ModItemCharacterEffectCompositeDef Weight_2Class DisplayName]] "Вес брони (2 Класс)"),
	Description = T(997296420646, --[[ModItemCharacterEffectCompositeDef Weight_2Class Description]] "ОД и ОД свободного перемещения уменьшены. Чем больше уровень, тем больше дебафов"),
	AddEffectText = "",
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/light_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}

