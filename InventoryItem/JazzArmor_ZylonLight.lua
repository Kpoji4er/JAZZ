UndefineClass('JazzArmor_ZylonLight')
DefineClass.JazzArmor_ZylonLight = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 L T3",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 40,
	Icon = "Mod/e6L4ECj/ArmorIcons/ZylonL.png",
	DisplayName = T(580063580276, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonLight DisplayName]] "Бронежилет Зилон, Легкий"),
	DisplayNamePlural = T(586029190644, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonLight DisplayNamePlural]] "Бронежилеты Зилон, Легкий"),
	Description = T(328063220388, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonLight Description]] "Легкий бронежилет Зилон в камуфляжой раскраске. Имеет большу крепость на разрыв, чем другие типы брони, но быстрее приходит в негодность"),
	AdditionalHint = T(436739161545, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonLight AdditionalHint]] "Модульный бронежилет. Облегченный вариант"),
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 55,
	ArmorRating = 10,
	MeleeArmorRating = 4,
	ExplosiveArmorRating = 16,
	CamouflagePercent = 15,
	CanHoldPlate = true,
	ArmorResource = 200,
	Repairability = 70,
}

