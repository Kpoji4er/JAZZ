UndefineClass('FlareAmmo')
DefineClass.FlareAmmo = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Repairable = false,
	Icon = "UI/Icons/Items/FlareBullet",
	DisplayName = T(422329947007, --[[ModItemInventoryItemCompositeDef FlareAmmo DisplayName]] "Flare Cartridge"),
	DisplayNamePlural = T(355303195226, --[[ModItemInventoryItemCompositeDef FlareAmmo DisplayNamePlural]] "Flare Cartridges"),
	Description = T(286757968282, --[[ModItemInventoryItemCompositeDef FlareAmmo Description]] "Ammo for the Flare Gun."),
	Cost = 150,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 8,
	RestockWeight = 40,
	CategoryPair = "UtilityAmmo",
	MaxStacks = 3,
	AreaOfEffect = 5,
	PenetrationClass = 1,
	Caliber = "JAZZ_Caliber_Flare",
	BaseDamage = 0,
	Noise = 0,
}

