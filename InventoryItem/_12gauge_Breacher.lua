UndefineClass('_12gauge_Breacher')
DefineClass._12gauge_Breacher = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Картечь - 9 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(142187478707, --[[ModItemInventoryItemCompositeDef _12gauge_Breacher DisplayName]] "12-й калибр, Картечь"),
	DisplayNamePlural = T(147186638408, --[[ModItemInventoryItemCompositeDef _12gauge_Breacher DisplayNamePlural]] "12-й калибр, Картечь"),
	colorStyle = "AmmoGreenColor",
	Description = T(473082214606, --[[ModItemInventoryItemCompositeDef _12gauge_Breacher Description]] "Картечь 12-го калибра."),
	AdditionalHint = T(879074273943, --[[ModItemInventoryItemCompositeDef _12gauge_Breacher AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 9 частиц. Повышенный урон"),
	Cost = 90,
	MaxStock = 30,
	RestockWeight = 25,
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "12gauge",
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

