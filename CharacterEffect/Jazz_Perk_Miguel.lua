UndefineClass('Jazz_Perk_Miguel')
DefineClass.Jazz_Perk_Miguel = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if type(Jazz_MiguelRefreshAura) == "function" then
					Jazz_MiguelRefreshAura()
				end
			end,
		}),
	},
	DisplayName = T(890000000003200, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Miguel DisplayName]] "Команданте"),
	Description = T(890000000003201, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Miguel Description]] "Аура 30: если Мигель на ногах — союзники +30 Will / +15 CTH; если сбит — −30 Will / −15 CTH."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Miguel.png",
	Tier = "Personal",
}
