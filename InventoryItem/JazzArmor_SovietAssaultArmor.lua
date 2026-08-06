UndefineClass('JazzArmor_SovietAssaultArmor')
DefineClass.JazzArmor_SovietAssaultArmor = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class 1 M T1",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 60,
	Icon = "Mod/e6L4ECj/ArmorIcons/USSRArmor.png",
	DisplayName = T(910956023361, --[[ModItemInventoryItemCompositeDef JazzArmor_SovietAssaultArmor DisplayName]] "Советский штурмовой нагрудник"),
	DisplayNamePlural = T(499755425254, --[[ModItemInventoryItemCompositeDef JazzArmor_SovietAssaultArmor DisplayNamePlural]] "Советские штурмовые нагрудники"),
	Description = T(745507740881, --[[ModItemInventoryItemCompositeDef JazzArmor_SovietAssaultArmor Description]] "Советская штурмовая кираса, использовавшаяся специальными подразделениями РККА в ходе Великой Отечественной войны. С уверенностью останавливает 9-мм пистолетную пулю из МП40, что, безусловно, послужило неприятным сюрпризом для солдат Вермахта в схватках накоротке."),
	AdditionalHint = T(521194187625, --[[ModItemInventoryItemCompositeDef JazzArmor_SovietAssaultArmor AdditionalHint]] "Советская штурмовая броня второй мировой войны"),
	Cost = 1600,
	CanAppearInShop = false,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 40,
	ArmorRating = 26,
	MeleeArmorRating = 10,
	ExplosiveArmorRating = 5,
	Weight = 3,
	ArmorResource = 180,
}

