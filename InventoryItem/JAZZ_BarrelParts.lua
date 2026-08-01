UndefineClass('JAZZ_BarrelParts')
DefineClass.JAZZ_BarrelParts = {
	__parents = { "ResourceItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "ResourceItem",
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_BarrelParts.png",
	DisplayName = T(990002002, --[[ModItemInventoryItemCompositeDef JAZZ_BarrelParts DisplayName]] "Ствольные запчасти"),
	DisplayNamePlural = T(990002003, --[[ModItemInventoryItemCompositeDef JAZZ_BarrelParts DisplayNamePlural]] "Ствольные запчасти"),
	AdditionalHint = T(990002004, --[[ModItemInventoryItemCompositeDef JAZZ_BarrelParts AdditionalHint]] "Используются для установки и ремонта стволов."),
	Cost = 500,
	CanAppearInShop = true,
	MaxStock = 25,
	RestockWeight = 75,
	CategoryPair = "Resource",
	ShopStackSize = 5,
	MaxStacks = 5000,
}
