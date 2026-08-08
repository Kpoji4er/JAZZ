UndefineClass('Weight_2Class')
DefineClass.Weight_2Class = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function(self, target, value, action)
				JazzArmorWeightPainOnMove(target)
				return value
			end,
		}),
	},
	DisplayName = T(118150789498, --[[ModItemCharacterEffectCompositeDef Weight_2Class DisplayName]] "Вес брони (2 Класс)"),
	Description = T(997296420646, --[[ModItemCharacterEffectCompositeDef Weight_2Class Description]] "Каждый стак: −1 ОД свободного перемещения. Тяжёлый комплект может снизить стартовые ОД (до −2). При 6+ стаках: +1 боль при первом перемещении за ход."),
	AddEffectText = "",
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/light_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}
