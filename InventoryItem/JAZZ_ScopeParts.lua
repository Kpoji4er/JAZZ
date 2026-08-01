UndefineClass('JAZZ_ScopeParts')
DefineClass.JAZZ_ScopeParts = {
	__parents = { "ResourceItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "ResourceItem",
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_ScopeParts.png",
	DisplayName = T(990002500, --[[ModItemInventoryItemCompositeDef JAZZ_ScopeParts DisplayName]] "Детали прицелов"),
	DisplayNamePlural = T(990002501, --[[ModItemInventoryItemCompositeDef JAZZ_ScopeParts DisplayNamePlural]] "Детали прицелов"),
	AdditionalHint = T(990002502, --[[ModItemInventoryItemCompositeDef JAZZ_ScopeParts AdditionalHint]] "Нужны при ремонте оружия с установленным прицелом. Также получаются при поломке прицела при неудачном снятии."),
	Cost = 600,
	CanAppearInShop = true,
	MaxStock = 20,
	RestockWeight = 60,
	CategoryPair = "Resource",
	ShopStackSize = 5,
	MaxStacks = 5000,
}
