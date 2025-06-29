UndefineClass('JazzArmor_MotoKneePads')
DefineClass.JazzArmor_MotoKneePads = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 M",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 70,
	Icon = "Mod/e6L4ECj/ArmorIcons/MotoKneePads.png",
	DisplayName = T(795145634495, --[[ModItemInventoryItemCompositeDef JazzArmor_MotoKneePads DisplayName]] "Мотоциклетная защита"),
	DisplayNamePlural = T(100815129525, --[[ModItemInventoryItemCompositeDef JazzArmor_MotoKneePads DisplayNamePlural]] "Мотоциклетная защита"),
	Description = T(384678181247, --[[ModItemInventoryItemCompositeDef JazzArmor_MotoKneePads Description]] "Мотоциклетные щитки на голени из прочного пластика. Пули, понятное дело, не держат, но вот удар арматуриной - вполне."),
	AdditionalHint = T(805310507119, --[[ModItemInventoryItemCompositeDef JazzArmor_MotoKneePads AdditionalHint]] "Мотоциклетная защита. Не держит пули"),
	Valuable = 1,
	Cost = 100,
	CanAppearInShop = true,
	RestockWeight = 1,
	CategoryPair = "Light",
	Slot = "Legs",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Legs" ),
	Coverage = 40,
	ArmorRating = 3,
	MeleeArmorRating = 15,
	Weight = 2,
	ArmorResource = 50,
	Repairability = 90,
}

