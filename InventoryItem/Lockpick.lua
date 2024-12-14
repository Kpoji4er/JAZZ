UndefineClass('Lockpick')
DefineClass.Lockpick = {
	__parents = { "LockpickBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "LockpickBase",
	ScrapParts = 2,
	Repairable = false,
	Icon = "UI/Icons/Items/lockpick",
	DisplayName = T(135853991513, --[[ModItemInventoryItemCompositeDef Lockpick DisplayName]] "Набор отмычек"),
	DisplayNamePlural = T(972477228590, --[[ModItemInventoryItemCompositeDef Lockpick DisplayNamePlural]] "Наборы отмычек"),
	AdditionalHint = T(630066806420, --[[ModItemInventoryItemCompositeDef Lockpick AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вскрывает замки на дверях и контейнерах (зависит от навыка механики)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неквалифицированное применение может безвозвратно повредить замок\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Изнашивается при каждом употреблении\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не поддается ремонту\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Mechanical",
	Cost = 200,
	CanAppearInShop = true,
	CategoryPair = "Tool",
}

