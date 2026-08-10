UndefineClass('Reanimationsset')
DefineClass.Reanimationsset = {
	__parents = { "JazzStackableMedicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",
	object_class = "JazzStackableMedicine",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function(self, target, patient, medic, medkit, data)
				if self == medkit then
					data.heal_modifier = data.heal_modifier + 100
				end
			end,
		}),
	},
	ScrapParts = 1,
	Repairable = false,
	Icon = "UI/Icons/Items/reanimationsset.png",
	DisplayName = T(890000000010031, "Large Medkit"),
	DisplayNamePlural = T(890000000010032, "Large Medkits"),
	AdditionalHint = T(890000000010030, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage healing bonus: 100%\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Starts healing on any untreated trauma\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically from inventory"),
	UnitStat = "Medical",
	Cost = 1800,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Medicine",
	MaxStacks = 15,
	UsePriority = 2,
}
