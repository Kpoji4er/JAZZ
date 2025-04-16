UndefineClass('JAZZ_AMMO_50BMG_Basic_copy')
DefineClass.JAZZ_AMMO_50BMG_Basic_copy = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_basic",
	DisplayName = T(224747486019, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Basic_copy DisplayName]] ".50, обычный"),
	DisplayNamePlural = T(272581385016, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Basic_copy DisplayNamePlural]] ".50, обычные"),
	colorStyle = "AmmoBasicColor",
	Description = T(928449338739, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Basic_copy Description]] "Боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	Cost = 250,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 10,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	Caliber = "JAZZ_Caliber_50BMG",
}

