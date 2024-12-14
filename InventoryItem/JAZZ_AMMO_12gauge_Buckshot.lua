UndefineClass('JAZZ_AMMO_12gauge_Buckshot')
DefineClass.JAZZ_AMMO_12gauge_Buckshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Картечь - 9 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gBUCKSHOT.png",
	DisplayName = T(365779430314, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot DisplayName]] "12-й калибр, Картечь"),
	DisplayNamePlural = T(789991711408, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot DisplayNamePlural]] "12-й калибр, Картечь"),
	colorStyle = "AmmoGreenColor",
	Description = T(569006389836, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot Description]] "Картечь 12-го калибра."),
	AdditionalHint = T(898015548142, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Buckshot AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 9 частиц. Повышенный урон"),
	Cost = 90,
	CanAppearInShop = true,
	MaxStock = 30,
	RestockWeight = 25,
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 9000,
			target_prop = "AutoShots",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 4000,
			target_prop = "Damage",
		}),
	},
}

