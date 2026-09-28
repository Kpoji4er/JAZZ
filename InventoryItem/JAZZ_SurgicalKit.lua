UndefineClass('JAZZ_SurgicalKit')
DefineClass.JAZZ_SurgicalKit = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_SurgicalKit.png",
	DisplayName = T(890000000010017, --[[ModItemInventoryItemCompositeDef JAZZ_SurgicalKit DisplayName]] "Surgical Kit"),
	DisplayNamePlural = T(890000000010018, --[[ModItemInventoryItemCompositeDef JAZZ_SurgicalKit DisplayNamePlural]] "Surgical Kits"),
	AdditionalHint = T(890000000010019, --[[ModItemInventoryItemCompositeDef JAZZ_SurgicalKit AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used via item menu\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Grants long analgesia (v1)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Rare; doctors use this for field surgery later"),
	Cost = 800,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 25,
	CategoryPair = "Medicine",
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitAddStatusEffect', {
			Status = "Analgesia",
		}),
	},
	action_name = T(890000000010020, --[[ModItemInventoryItemCompositeDef JAZZ_SurgicalKit action_name]] "USE"),
	destroy_item = true,
}

