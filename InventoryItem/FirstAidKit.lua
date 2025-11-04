UndefineClass('FirstAidKit')
DefineClass.FirstAidKit = {
	__parents = { "Medicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Medicine",
	ScrapParts = 1,
	Repairable = false,
	Icon = "UI/Icons/Items/first_aid_kit",
	DisplayName = T(177286255676, --[[ModItemInventoryItemCompositeDef FirstAidKit DisplayName]] "Набор первой помощи"),
	DisplayNamePlural = T(111146552342, --[[ModItemInventoryItemCompositeDef FirstAidKit DisplayNamePlural]] "Наборы первой помощи"),
	AdditionalHint = T(833018739707, --[[ModItemInventoryItemCompositeDef FirstAidKit AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает потерянные ОЗ и стабилизирует состояние умирающих персонажей\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Требуется для использования перевязки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тратится при каждом употреблении, но запас медикаментов можно восполнить\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Medical",
	Cost = 300,
	CanAppearInShop = true,
	RestockWeight = 150,
	CategoryPair = "Medicine",
	max_meds_parts = 8,
}

