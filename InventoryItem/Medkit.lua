UndefineClass('Medkit')
DefineClass.Medkit = {
	__parents = { "JazzStackableMedicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",
	object_class = "JazzStackableMedicine",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function(self, target, patient, medic, medkit, data)
				if self == medkit then
					data.heal_modifier = data.heal_modifier + 50
				end
			end,
		}),
	},
	ScrapParts = 1,
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_Medkit.png",
	DisplayName = T(890000000010025, "Med Kit"),
	DisplayNamePlural = T(890000000010026, "Med Kits"),
	AdditionalHint = T(890000000010027, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage healing bonus: 50%.\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack"),
	UnitStat = "Medical",
	Cost = 500,
	CanAppearInShop = true,
	Tier = 1,
	RestockWeight = 80,
	CategoryPair = "Medicine",
	MaxStacks = 3,
	UsePriority = 1,
}
