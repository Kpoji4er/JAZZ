UndefineClass('Jazz_Perk_Meat')
DefineClass.Jazz_Perk_Meat = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcPersonalMorale",
			Handler = function (self, target, value)
				if type(value) == "number" and value < 0 then
					return 0
				end
			end,
		}),
	},
	DisplayName = T(890000000005050, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Meat DisplayName]] "Толстокожий"),
	Description = T(890000000005051, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Meat Description]] "Воля не падает от морали. Урон по Will переходит в Grit. Не подавляется."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Meat.png",
	Tier = "Personal",
}
