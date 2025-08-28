UndefineClass('_12gauge_Buckshot')
DefineClass._12gauge_Buckshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Дробь - 20 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(822972834709, "12-й калибр, дробь"),
	DisplayNamePlural = T(768069058913, "12-й калибр, дробь"),
	colorStyle = "AmmoBasicColor",
	Description = T(535559779997, "Дробь 12-го калибра."),
	AdditionalHint = T(134836596865, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 20 частиц. Вызывают <color EmStyle>кровотечение</color>"),
	Cost = 60,
	MaxStock = 50,
	RestockWeight = 80,
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 20000,
			target_prop = "AutoShots",
		}),
	},
	AppliedEffects = {
		"BleedingChance",
	},
}

