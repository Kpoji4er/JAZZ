UndefineClass('Jazz_Perk_Mike')
DefineClass.Jazz_Perk_Mike = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcOverwatchAttacks",
			Handler = function (self, target, value, ...)
				return (value or 0) + 2
			end,
		}),
	},
	DisplayName = T(890000000002300, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Mike DisplayName]] "Быстрая реакция"),
	Description = T(890000000002301, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Mike Description]] "Овервотч и контроль получают +2 дополнительные атаки. Ответные атаки срабатывают, когда доступны."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Mike.png",
	Tier = "Personal",
}
