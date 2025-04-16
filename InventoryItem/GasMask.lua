UndefineClass('GasMask')
DefineClass.GasMask = {
	__parents = { "GasMaskBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "GasMaskBase",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmyGasMask.png",
	DisplayName = T(999957869604, --[[ModItemInventoryItemCompositeDef GasMask DisplayName]] "Противогаз"),
	DisplayNamePlural = T(607515076320, --[[ModItemInventoryItemCompositeDef GasMask DisplayNamePlural]] "Противогазы"),
	Description = T(832036550490, --[[ModItemInventoryItemCompositeDef GasMask Description]] "Классический противогаз с угольными фильтрами и резиновой шлем-маской, призванный защитить носителя от воздействия дыма, отравляющих газов и радиоактивной пыли. Ограничивает поле зрения и слуха, но это необходимая цена, за то, чтобы остаться живым."),
	AdditionalHint = T(352447628446, --[[ModItemInventoryItemCompositeDef GasMask AdditionalHint]] "Защищает от воздействия дыма и отравляющих газов"),
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 15,
	Slot = "HeadGear",
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	Weight = 4,
	Vision = -20,
	DustStormProtection = 30,
	StunGrenadeProtection = 20,
	SuppressionProtection = 20,
}

