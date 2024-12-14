UndefineClass('FlareAmmo')
DefineClass.FlareAmmo = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Repairable = false,
	Icon = "UI/Icons/Items/FlareBullet",
	DisplayName = T(483700492318, --[[ModItemInventoryItemCompositeDef FlareAmmo DisplayName]] "Сигнальная ракета"),
	DisplayNamePlural = T(165119929821, --[[ModItemInventoryItemCompositeDef FlareAmmo DisplayNamePlural]] "Сигнальные ракеты"),
	Description = T(691614229608, --[[ModItemInventoryItemCompositeDef FlareAmmo Description]] "Осветительные боеприпасы для ракетницы."),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 30,
	CategoryPair = "UtilityAmmo",
	MaxStacks = 500,
	AreaOfEffect = 5,
	PenetrationClass = 1,
	Caliber = "JAZZ_Caliber_Flare",
	BaseDamage = 0,
	Noise = 0,
}

