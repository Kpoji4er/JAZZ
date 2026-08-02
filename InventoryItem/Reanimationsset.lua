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
					data.heal_modifier = data.heal_modifier + 60
				end
			end,
		}),
	},
	ScrapParts = 1,
	Repairable = false,
	Icon = "UI/Icons/Items/reanimationsset.png",
	DisplayName = T(717284834554, --[[ModItemInventoryItemCompositeDef Reanimationsset DisplayName]] "Reanimationsset"),
	DisplayNamePlural = T(900536705401, --[[ModItemInventoryItemCompositeDef Reanimationsset DisplayNamePlural]] "Reanimationssets"),
	AdditionalHint = T(890000000010030, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Required for Bandage\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage restores 60% more HP\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"),
	UnitStat = "Medical",
	MaxStacks = 2,
	UsePriority = 2,
}
