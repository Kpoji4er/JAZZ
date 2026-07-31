UndefineClass('Jazz_Perk_Lucky')
DefineClass.Jazz_Perk_Lucky = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target:SetEffectValue("Jazz_Perk_Lucky", nil)
			end,
		}),
	},
	DisplayName = T(890000000005023, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Lucky DisplayName]] "Второе дыхание"),
	Description = T(890000000005024, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Lucky Description]] "Раз за бой первый промах из огнестрела становится попаданием."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Lucky.png",
	Tier = "Personal",
}
