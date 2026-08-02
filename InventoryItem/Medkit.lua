UndefineClass('Medkit')
DefineClass.Medkit = {
	__parents = { "Medicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",
	object_class = "Medicine",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function(self, target, patient, medic, medkit, data)
				if self == medkit then
					data.heal_modifier = data.heal_modifier + 25
				end
			end,
		}),
	},
	ScrapParts = 1,
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_Medkit.png",
	DisplayName = T(890000000010025, "Med Kit"),
	DisplayNamePlural = T(890000000010026, "Med Kits"),
	AdditionalHint = T(890000000010027, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage restores 25% more HP\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes up to two worst bleeding stacks\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Consumed on use; refill with Meds"),
	UnitStat = "Medical",
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Medicine",
	max_meds_parts = 12,
	UsePriority = 1,
}
