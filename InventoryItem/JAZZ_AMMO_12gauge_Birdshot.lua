UndefineClass('JAZZ_AMMO_12gauge_Birdshot')
DefineClass.JAZZ_AMMO_12gauge_Birdshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Дробь - 20 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gBIRDSHOT.png",
	DisplayName = T(503250075758, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot DisplayName]] "12-й калибр, дробь"),
	DisplayNamePlural = T(408475040527, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot DisplayNamePlural]] "12-й калибр, дробь"),
	colorStyle = "AmmoBasicColor",
	Description = T(561107124860, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot Description]] "Дробь 12-го калибра."),
	AdditionalHint = T(526169544903, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Birdshot AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> 20 частиц. Вызывают <color EmStyle>кровотечение</color>"),
	Cost = 60,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 80,
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 20000,
			target_prop = "AutoShots",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"BleedingChance",
	},
}

