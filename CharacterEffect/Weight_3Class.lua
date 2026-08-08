UndefineClass('Weight_3Class')
DefineClass.Weight_3Class = {
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
	DisplayName = T(696428661966, --[[ModItemCharacterEffectCompositeDef Weight_3Class DisplayName]] "Вес брони (3 Класс)"),
	Description = T(806830590860, --[[ModItemCharacterEffectCompositeDef Weight_3Class Description]] "Каждый стак: −1 ОД свободного перемещения. Тяжёлый комплект может снизить стартовые ОД (до −2). При 6+ стаках: +1 боль при первом перемещении за ход."),
	AddEffectText = "",
	OnRemoved = function (self, obj)  end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/ArmorHudIcons/medium_armor",
	max_stacks = 10,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}
