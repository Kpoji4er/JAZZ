UndefineClass('JazzArmor_GuardianHelmHeavy')
DefineClass.JazzArmor_GuardianHelmHeavy = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/GuardianHelmH.png",
	DisplayName = T(822054995436, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelmHeavy DisplayName]] "Шлем Гвардиан, тяжелый"),
	DisplayNamePlural = T(907492755122, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelmHeavy DisplayNamePlural]] "Шлемы Гвардиан, тяжелый"),
	Description = T(154040441272, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelmHeavy Description]] 'Тяжелые шлемы фирмы "Guardian" используются Ассоциацией для проведения штурмовых операций - взятие или освобождение заложников, ликвидация VIP, заминирование стратегических объектов и так далее.'),
	AdditionalHint = T(540364296206, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelmHeavy AdditionalHint]] "Модульный шлем, тяжелый"),
	Valuable = 1,
	Cost = 8500,
	CanAppearInShop = true,
	RestockWeight = 15,
	CategoryPair = "Heavy",
	Slot = "Head",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head", "Neck" ),
	ArmorRating = 30,
	MeleeArmorRating = 8,
	BlockFaceSlot = true,
	Weight = 4,
	Vision = -5,
	StunGrenadeProtection = function ()
		    return 0--self.StunGrenadeProtection *  self:GetConditionPercent()/100 * (101-self.Deterioration)/100 or 0
	end,
	SuppressionProtection = function ()
		    return 0--self.SuppressionProtection *  self:GetConditionPercent()/100 * (101-self.Deterioration)/100 or 0
	end,
}

