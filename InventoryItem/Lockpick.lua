UndefineClass('Lockpick')
DefineClass.Lockpick = {
	__parents = { "LockpickBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "LockpickBase",
	ScrapParts = 2,
	Repairable = false,
	Icon = "UI/Icons/Items/lockpick",
	DisplayName = T(363189070824, --[[ModItemInventoryItemCompositeDef Lockpick DisplayName]] "Locksmith's Kit"),
	DisplayNamePlural = T(983215060783, --[[ModItemInventoryItemCompositeDef Lockpick DisplayNamePlural]] "Locksmith's Kits"),
	AdditionalHint = T(630066806420, --[[ModItemInventoryItemCompositeDef Lockpick AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вскрывает замки на дверях и контейнерах (зависит от навыка механики)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неквалифицированное применение может безвозвратно повредить замок\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Изнашивается при каждом употреблении\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не поддается ремонту\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Mechanical",
	Cost = 200,
	CanAppearInShop = true,
	CategoryPair = "Tool",
}

