UndefineClass('MortarShell_Smoke')
DefineClass.MortarShell_Smoke = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_smoke",
	DisplayName = T(725759308030, --[[ModItemInventoryItemCompositeDef MortarShell_Smoke DisplayName]] "Mortar Smoke Cartridge"),
	DisplayNamePlural = T(438787593786, --[[ModItemInventoryItemCompositeDef MortarShell_Smoke DisplayNamePlural]] "Mortar Smoke Cartridges"),
	Description = T(497568730512, --[[ModItemInventoryItemCompositeDef MortarShell_Smoke Description]] "Ordnance ammo for Mortars."),
	AdditionalHint = T(651925772567, --[[ModItemInventoryItemCompositeDef MortarShell_Smoke AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не наносит урона\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Почти бесшумно"),
	Cost = 750,
	Tier = 2,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "Ordnance",
	MaxStacks = 100,
	PenetrationClass = 1,
	BurnGround = false,
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 0,
	Noise = 0,
	aoeType = "smoke",
}

