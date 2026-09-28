UndefineClass('JazzArmor_WieldingHelm')
DefineClass.JazzArmor_WieldingHelm = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/WieldingHelm.png",
	DisplayName = T(370026149313, --[[ModItemInventoryItemCompositeDef JazzArmor_WieldingHelm DisplayName]] "Сварочная маска"),
	DisplayNamePlural = T(210740079061, --[[ModItemInventoryItemCompositeDef JazzArmor_WieldingHelm DisplayNamePlural]] "Сварочная маска"),
	Description = T(930235849895, --[[ModItemInventoryItemCompositeDef JazzArmor_WieldingHelm Description]] "Тяжеленная сварочная маска, укрепленная решеткой в области прорези для глаз. Защитные свойства скорее психологические, конечно."),
	AdditionalHint = "",
	Valuable = 1,
	RestockWeight = 0,
	Slot = "Head",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head", "Neck" ),
	ArmorRating = 40,
	MeleeArmorRating = 50,
	BlockFaceSlot = true,
	Weight = 4,
	Vision = -20,
	ArmorResource = 400,
	Repairability = 95,
}

